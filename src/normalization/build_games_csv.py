"""
Normalize raw CFBD game JSON into season-level CSV files.

The script is intentionally discovery-based rather than hard-coded to a
specific year. It supports both the historical single-file layout and the
weekly raw-file layout now used for current seasons.

Inputs discovered under:
    data/raw/games/

Examples:
    regular/2025_gd.json
    regular/2026/2026_gd_wk_1.json
    post/2025_gdb.json

Outputs:
    data/normalized/games/{season}_{season_type}.csv

One output row represents one game.
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

INPUT_DIR = Path("data/raw/games")
OUTPUT_DIR = Path("data/normalized/games")

FIELDS = [
    "game_id",
    "season",
    "season_type",
    "week",
    "start_date",
    "completed",
    "neutral_site",
    "conference_game",
    "attendance",
    "venue_id",
    "venue",
    "home_team_id",
    "home_team",
    "away_team_id",
    "away_team",
    "home_points",
    "away_points",
]


def classify_file(path: Path):
    """Return (season, season_type) from a CFBD game filename/path."""
    name = path.stem

    match = re.match(r"^(?P<year>\d{4})_(?P<kind>gd|gdb)(?:_wk_\d+)?$", name)
    if not match:
        return None

    season = int(match.group("year"))
    kind = match.group("kind")
    season_type = "post" if kind == "gdb" else "regular"
    return season, season_type


def discover_inputs():
    groups = defaultdict(list)

    for path in sorted(INPUT_DIR.rglob("*.json")):
        classified = classify_file(path)
        if classified:
            groups[classified].append(path)

    return groups


def load_games(path):
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON list.")

    return data


def normalize_game(game):
    return {
        "game_id": game.get("id"),
        "season": game.get("season"),
        "season_type": game.get("seasonType"),
        "week": game.get("week"),
        "start_date": game.get("startDate"),
        "completed": game.get("completed"),
        "neutral_site": game.get("neutralSite"),
        "conference_game": game.get("conferenceGame"),
        "attendance": game.get("attendance"),
        "venue_id": game.get("venueId"),
        "venue": game.get("venue"),
        "home_team_id": game.get("homeId"),
        "home_team": game.get("homeTeam"),
        "away_team_id": game.get("awayId"),
        "away_team": game.get("awayTeam"),
        "home_points": game.get("homePoints"),
        "away_points": game.get("awayPoints"),
    }


def process_group(season, season_type, paths):
    rows = []
    seen_games = {}

    for path in paths:
        print(f"Reading: {path}")

        for game in load_games(path):
            game_id = game.get("id")

            if game_id is None:
                raise ValueError(f"Missing game ID in {path}")

            if game_id in seen_games:
                if game == seen_games[game_id]:
                    print(
                        f"Duplicate identical game {game_id} found in {path}; "
                        "skipping duplicate raw record."
                    )
                    continue
                raise ValueError(
                    f"Conflicting duplicate game_id {game_id} discovered for "
                    f"{season} {season_type}."
                )

            seen_games[game_id] = game
            rows.append(normalize_game(game))

    rows.sort(
        key=lambda row: (
            int(row["week"]) if str(row["week"]).isdigit() else 999,
            row["start_date"] or "",
            int(row["game_id"]),
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{season}_{season_type}.csv"

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} games -> {output}")
    return len(rows)


def main():
    print("=" * 60)
    print("CFB ATS Research Platform")
    print("Games Normalization")
    print("=" * 60)

    groups = discover_inputs()

    if not groups:
        raise FileNotFoundError(f"No recognized game JSON files under {INPUT_DIR}")

    total = 0

    for (season, season_type), paths in sorted(groups.items()):
        total += process_group(season, season_type, paths)

    print("=" * 60)
    print(f"Groups processed: {len(groups)}")
    print(f"Games written: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()
