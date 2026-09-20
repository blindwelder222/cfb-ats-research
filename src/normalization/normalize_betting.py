"""
Normalize raw CFBD betting JSON into season-level provider-line CSV files.

The script discovers raw files recursively so the same workflow supports both
historical single-file data and weekly current-season acquisitions.

Inputs discovered under:
    data/raw/betting/

Examples:
    regular/2025_lines.json
    regular/2026/2026_lines_wk_1.json
    post/2025_lines_b.json

Outputs:
    data/normalized/betting/{season_type}/{season}_betting.csv

One output row represents one provider line for one game.
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

INPUT_DIR = Path("data/raw/betting")
OUTPUT_DIR = Path("data/normalized/betting")

FIELDS = [
    "game_id",
    "season",
    "season_type",
    "week",
    "start_date",
    "home_team_id",
    "home_team",
    "away_team_id",
    "away_team",
    "provider",
    "spread",
    "spread_open",
    "over_under",
    "over_under_open",
    "home_moneyline",
    "away_moneyline",
]

PROVIDER_MAP = {
    "Draft Kings": "DraftKings",
}


def normalize_provider(provider):
    if provider is None:
        return None
    provider = str(provider).strip()
    return PROVIDER_MAP.get(provider, provider)


def classify_file(path: Path):
    """Return (season, season_type) from a CFBD betting filename/path."""
    name = path.stem

    match = re.match(
        r"^(?P<year>\d{4})_lines(?:_b)?(?:_wk_\d+)?$",
        name,
    )
    if not match:
        return None

    season = int(match.group("year"))
    season_type = "post" if "_lines_b" in name else "regular"
    return season, season_type


def discover_inputs():
    groups = defaultdict(list)

    for path in sorted(INPUT_DIR.rglob("*.json")):
        classified = classify_file(path)
        if classified:
            groups[classified].append(path)

    return groups


def normalize_game_line(game, line):
    return {
        "game_id": game.get("id"),
        "season": game.get("season"),
        "season_type": game.get("seasonType"),
        "week": game.get("week"),
        "start_date": game.get("startDate"),
        "home_team_id": game.get("homeTeamId"),
        "home_team": game.get("homeTeam"),
        "away_team_id": game.get("awayTeamId"),
        "away_team": game.get("awayTeam"),
        "provider": normalize_provider(line.get("provider")),
        "spread": line.get("spread"),
        "spread_open": line.get("spreadOpen"),
        "over_under": line.get("overUnder"),
        "over_under_open": line.get("overUnderOpen"),
        "home_moneyline": line.get("homeMoneyline"),
        "away_moneyline": line.get("awayMoneyline"),
    }


def process_group(season, season_type, paths):
    rows = []

    for path in paths:
        print(f"Reading: {path}")

        with path.open("r", encoding="utf-8") as handle:
            games = json.load(handle)

        if not isinstance(games, list):
            raise ValueError(f"{path}: expected a JSON list.")

        for game in games:
            for line in game.get("lines") or []:
                rows.append(normalize_game_line(game, line))

    rows.sort(
        key=lambda row: (
            int(row["week"]) if str(row["week"]).isdigit() else 999,
            row["start_date"] or "",
            int(row["game_id"]),
            row["provider"] or "",
        )
    )

    output_dir = OUTPUT_DIR / season_type
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{season}_betting.csv"

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} provider lines -> {output}")
    return len(rows)


def main():
    print("=" * 60)
    print("CFB ATS Research Platform")
    print("Betting Normalization")
    print("=" * 60)

    groups = discover_inputs()

    if not groups:
        raise FileNotFoundError(f"No recognized betting JSON files under {INPUT_DIR}")

    total = 0

    for (season, season_type), paths in sorted(groups.items()):
        total += process_group(season, season_type, paths)

    print("=" * 60)
    print(f"Groups processed: {len(groups)}")
    print(f"Provider lines written: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()
