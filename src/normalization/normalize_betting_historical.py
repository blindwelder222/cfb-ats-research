
"""
Normalize raw College Football Data betting lines into CSV datasets.

Input:
    data/raw/betting/regular/YYYY_lines.json
    data/raw/betting/post/YYYY_lines_b.json

Output:
    data/normalized/betting/regular/YYYY_betting.csv
    data/normalized/betting/post/YYYY_betting.csv

One output row represents one provider line for one game. Provider names
are normalized only where the repository's acquired data shows obvious
formatting variants (for example, "Draft Kings" -> "DraftKings").
Opening and current betting values are preserved separately.
"""

import csv
import json
from pathlib import Path


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

SEASON_TYPES = {
    "regular": "lines",
    "post": "lines_b",
}

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


# ---------------------------------------------------------------------
# Provider normalization
# ---------------------------------------------------------------------

PROVIDER_MAP = {
    "Draft Kings": "DraftKings",
}


def normalize_provider(provider):
    """Return the canonical provider name used by this dataset."""
    if provider is None:
        return None

    provider = str(provider).strip()

    return PROVIDER_MAP.get(provider, provider)


# ---------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------

def normalize_game(game, line):
    """Convert one raw game/provider line into the normalized schema."""

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


def process_file(year, season_folder, suffix):
    """Normalize one season/season-type betting JSON file."""

    input_file = INPUT_DIR / season_folder / f"{year}_{suffix}.json"
    output_dir = OUTPUT_DIR / season_folder
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{year}_betting.csv"

    print("---------------------------------------------------")
    print(f"Reading : {input_file}")

    with input_file.open("r", encoding="utf-8") as f:
        games = json.load(f)

    rows = []

    for game in games:
        lines = game.get("lines") or []

        for line in lines:
            rows.append(normalize_game(game, line))

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"Games Loaded : {len(games)}")
    print(f"Lines Loaded : {len(rows)}")
    print(f"Rows Written : {len(rows)}")

    if len(rows) != sum(1 for _ in open(output_file, encoding="utf-8")) - 1:
        raise RuntimeError(
            f"Record count mismatch for {output_file.name}"
        )

    print("PASS")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Betting Dataset Normalization")
    print("===================================================")

    total_files = 0

    for year in YEARS:

        for season_folder, suffix in SEASON_TYPES.items():

            process_file(
                year=year,
                season_folder=season_folder,
                suffix=suffix,
            )

            total_files += 1

    print("===================================================")
    print("Betting CSV Normalization Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Files Created   : {total_files}")
    print("Output Directory: data/normalized/betting/")
    print("===================================================")


if __name__ == "__main__":
    main()
