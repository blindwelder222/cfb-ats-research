"""
Merge regular-season and postseason normalized betting data.

Input:
    data/normalized/betting/regular/YYYY_betting.csv
    data/normalized/betting/post/YYYY_betting.csv

Output:
    data/normalized/betting/YYYY_betting.csv

This is an append/validation step. It preserves provider-level observations
and does not select, deduplicate, or calculate consensus betting lines.
"""

from pathlib import Path
import csv


YEARS = range(2016, 2026)

BETTING_DIR = Path("data/normalized/betting")
REGULAR_DIR = BETTING_DIR / "regular"
POST_DIR = BETTING_DIR / "post"

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

REQUIRED_COLUMNS = set(FIELDS)


def load_season_file(path):
    """Load and validate one normalized betting CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        columns = reader.fieldnames or []

        missing = REQUIRED_COLUMNS - set(columns)
        if missing:
            raise ValueError(
                f"{path} is missing required columns: {sorted(missing)}"
            )

        rows = list(reader)

    return columns, rows


def merge_season(year):
    """Merge one season's regular and postseason betting records."""
    regular_path = REGULAR_DIR / f"{year}_betting.csv"
    post_path = POST_DIR / f"{year}_betting.csv"
    output_path = BETTING_DIR / f"{year}_betting.csv"

    regular_columns, regular = load_season_file(regular_path)
    post_columns, post = load_season_file(post_path)

    if set(regular_columns) != set(post_columns):
        raise ValueError(
            f"{year}: regular and postseason betting schemas differ."
        )

    regular_games = {
        row["game_id"] for row in regular if row["game_id"]
    }
    post_games = {
        row["game_id"] for row in post if row["game_id"]
    }

    overlap = regular_games.intersection(post_games)
    if overlap:
        raise ValueError(
            f"{year}: {len(overlap)} game_id values occur in both "
            "regular and postseason data."
        )

    combined = regular + post

    combined.sort(
        key=lambda row: (
            row["game_id"] or "",
            row["provider"] or "",
        )
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
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
        writer.writerows(combined)

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
