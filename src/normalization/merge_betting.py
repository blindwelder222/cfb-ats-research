
"""
Merge regular-season and postseason normalized betting data.

Input:
    data/normalized/betting/regular/YYYY_betting.csv
    data/normalized/betting/post/YYYY_betting.csv

Output:
    data/normalized/betting/YYYY_betting.csv

The merge is an append operation. Provider-level observations are preserved;
this script does not deduplicate, select consensus lines, or otherwise alter
betting records. The season_type column remains available so downstream
research can distinguish regular-season and postseason games.
"""

from pathlib import Path

import pandas as pd


YEARS = range(2016, 2026)

BETTING_DIR = Path("data/normalized/betting")
REGULAR_DIR = BETTING_DIR / "regular"
POST_DIR = BETTING_DIR / "post"

REQUIRED_COLUMNS = {
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
}


def validate_columns(frame, source):
    """Ensure an input file has the canonical betting schema."""
    missing = REQUIRED_COLUMNS - set(frame.columns)

    if missing:
        raise ValueError(
            f"{source} is missing required columns: "
            f"{sorted(missing)}"
        )


def load_season_file(path):
    """Load and validate one normalized betting file."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    frame = pd.read_csv(path)
    validate_columns(frame, path)

    return frame


def merge_season(year):
    """Merge one season's regular and postseason betting records."""
    regular_path = REGULAR_DIR / f"{year}_betting.csv"
    post_path = POST_DIR / f"{year}_betting.csv"
    output_path = BETTING_DIR / f"{year}_betting.csv"

    regular = load_season_file(regular_path)
    post = load_season_file(post_path)

    # A postseason game must not already exist in the regular-season file.
    # Provider-level duplicates within either source are intentionally
    # preserved because this stage is not responsible for line selection.
    regular_games = set(regular["game_id"].dropna())
    post_games = set(post["game_id"].dropna())
    overlap = regular_games.intersection(post_games)

    if overlap:
        raise ValueError(
            f"{year}: {len(overlap)} game_id values occur in both "
            "regular and postseason data."
        )

    combined = pd.concat(
        [regular, post],
        ignore_index=True,
    )

    # Keep the canonical column order and make the output deterministic.
    combined = combined[
        [
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
    ]

    combined = combined.sort_values(
        ["game_id", "provider"],
        kind="stable",
        na_position="last",
    ).reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(output_path, index=False)

    # Validate the append operation did not lose records.
    expected_rows = len(regular) + len(post)

    if len(combined) != expected_rows:
        raise RuntimeError(
            f"{year}: expected {expected_rows:,} rows but wrote "
            f"{len(combined):,} rows."
        )

    print(
        f"{year}: {len(regular):,} regular + "
        f"{len(post):,} postseason = "
        f"{len(combined):,} rows -> {output_path}"
    )


def main():
    print("===================================================")
    print("College Football ATS Research Platform")
    print("Betting Season Merge")
    print("===================================================")

    for year in YEARS:
        merge_season(year)

    print("===================================================")
    print("Betting Season Merge Complete")
    print("===================================================")


if __name__ == "__main__":
    main()
