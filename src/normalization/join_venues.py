
"""
Join canonical venue data to the betting/rankings game layer and derive
venue-local kickoff timestamps.

Inputs:
    data/normalized/rankings/joined/YYYY_games_teams_betting_rankings.csv
    data/normalized/venues/venues.csv

Output:
    data/normalized/venues/joined/YYYY_games_teams_betting_rankings_venues.csv

Timezone policy:
    1. Use the CFBD venue timezone when present.
    2. For the small set of research-population venues with missing CFBD
       timezone values, use explicitly documented venue resolutions below.
    3. Do not infer timezones from state, city, or coordinates in this module.

Verified venue timezone resolutions:
    - 5455 Ford Center At The Star -> America/Chicago
    - Thomas A. Robinson National Stadium -> America/Nassau
    - Wrigley Field -> America/Chicago
    - SoFi Stadium -> America/Los_Angeles
    - StubHub Center -> America/Los_Angeles
    - Orlando City Stadium -> America/New_York
    - Petco Park -> America/Los_Angeles
    - The Dome at America's Center -> America/Chicago

The UTC start_date supplied by the games dataset is preserved. A localized
timestamp is derived with the venue timezone. No day/evening/night bucket is
created here.
"""

import csv
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


YEARS = range(2016, 2026)

GAME_DIR = Path("data/normalized/rankings/joined")
VENUE_PATH = Path("data/normalized/venues/venues.csv")
OUTPUT_DIR = Path("data/normalized/venues/joined")

VENUE_FIELDS = [
    "venue_id",
    "venue_name",
    "capacity",
    "grass",
    "dome",
    "city",
    "state",
    "zip",
    "country_code",
    "timezone",
    "latitude",
    "longitude",
    "elevation",
    "construction_year",
]

VENUE_TIMEZONE_OVERRIDES = {
    # CFBD timezone missing; venue location independently verified.
    # IDs are the canonical venue IDs from data/normalized/venues/venues.csv.
    "5455": {
        "timezone": "America/Chicago",
        "source": "documented_venue_resolution",
    },
    "4779": {
        "timezone": "America/Nassau",
        "source": "documented_venue_resolution",
    },
    "4250": {
        "timezone": "America/Chicago",
        "source": "documented_venue_resolution",
    },
    "7065": {
        "timezone": "America/Los_Angeles",
        "source": "documented_venue_resolution",
    },
    "538": {
        "timezone": "America/Los_Angeles",
        "source": "documented_venue_resolution",
    },
    "5403": {
        "timezone": "America/New_York",
        "source": "documented_venue_resolution",
    },
    "4205": {
        "timezone": "America/Los_Angeles",
        "source": "documented_venue_resolution",
    },
    "3494": {
        "timezone": "America/Chicago",
        "source": "documented_venue_resolution",
    },
}


def load_csv(path):
    """Load a CSV and return its fields and rows."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return reader.fieldnames or [], list(reader)


def validate_unique_ids(rows, field, source):
    """Ensure a reference dataset contains unique IDs."""
    seen = set()

    for row in rows:
        value = row.get(field, "")

        if value in ("", None):
            raise ValueError(f"{source}: row missing {field}.")

        if value in seen:
            raise ValueError(
                f"{source}: duplicate {field} detected: {value}"
            )

        seen.add(value)


def parse_utc(value):
    """Parse a CFBD ISO timestamp and ensure it is timezone-aware."""
    if not value:
        return None

    normalized = value.replace("Z", "+00:00")

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Unable to parse start_date: {value}"
        ) from exc

    if parsed.tzinfo is None:
        raise ValueError(
            f"start_date is missing timezone information: {value}"
        )

    return parsed


def resolve_timezone(venue):
    """Resolve a venue timezone using only explicit source/override data."""
    venue_id = str(venue["venue_id"])

    override = VENUE_TIMEZONE_OVERRIDES.get(venue_id)
    if override:
        return override["timezone"], override["source"]

    timezone = (venue.get("timezone") or "").strip()

    if timezone:
        return timezone, "CFBD"

    return "", ""


def localize_start_date(start_date, timezone_name):
    """Convert a UTC/offset-aware start timestamp to venue-local time."""
    if not timezone_name:
        return ""

    parsed = parse_utc(start_date)

    if parsed is None:
        return ""

    try:
        timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(
            f"Unknown IANA timezone: {timezone_name}"
        ) from exc

    return parsed.astimezone(timezone).isoformat()


def join_season(year, venue_lookup):
    """Join venue reference data to one season."""
    game_path = (
        GAME_DIR /
        f"{year}_games_teams_betting_rankings.csv"
    )
    output_path = (
        OUTPUT_DIR /
        f"{year}_games_teams_betting_rankings_venues.csv"
    )

    game_fields, games = load_csv(game_path)

    required_game = {
        "game_id",
        "start_date",
        "venue_id",
        "venue",
    }

    missing_game = required_game - set(game_fields)
    if missing_game:
        raise ValueError(
            f"{game_path}: missing required columns: "
            f"{sorted(missing_game)}"
        )

    output_fields = list(game_fields)

    added_fields = [
        "venue_timezone",
        "venue_timezone_source",
        "venue_local_start_date",
        "venue_local_time_available",
    ]

    for field in added_fields:
        if field not in output_fields:
            output_fields.append(field)

    output_rows = []
    venue_matches = 0
    missing_venues = 0
    timezone_available = 0
    timezone_missing = 0

    for game in games:
        venue_id = str(game.get("venue_id", ""))
        venue = venue_lookup.get(venue_id)

        if venue is None:
            missing_venues += 1
            timezone_name = ""
            timezone_source = ""
        else:
            venue_matches += 1
            timezone_name, timezone_source = resolve_timezone(venue)

        local_start = localize_start_date(
            game.get("start_date", ""),
            timezone_name,
        )

        if timezone_name:
            timezone_available += 1
        else:
            timezone_missing += 1

        output = dict(game)
        output["venue_timezone"] = timezone_name
        output["venue_timezone_source"] = timezone_source
        output["venue_local_start_date"] = local_start
        output["venue_local_time_available"] = (
            "True" if local_start else "False"
        )

        output_rows.append(output)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=output_fields,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    if len(output_rows) != len(games):
        raise RuntimeError(
            f"{year}: output row count changed during venue join."
        )

    print("--------------------------------------------")
    print(f"{year}")
    print(f"Games                 : {len(games):,}")
    print(f"Venue records matched : {venue_matches:,}")
    print(f"Missing venue records : {missing_venues:,}")
    print(f"Timezone available    : {timezone_available:,}")
    print(f"Timezone missing      : {timezone_missing:,}")
    print(f"Output                : {output_path}")
    print("PASS")


def main():
    print("============================================")
    print("College Football ATS Research Platform")
    print("Venue / Local Time Join")
    print("============================================")

    venue_fields, venue_rows = load_csv(VENUE_PATH)

    missing_venue_fields = set(VENUE_FIELDS) - set(venue_fields)
    if missing_venue_fields:
        raise ValueError(
            f"{VENUE_PATH}: missing required columns: "
            f"{sorted(missing_venue_fields)}"
        )

    validate_unique_ids(
        venue_rows,
        "venue_id",
        str(VENUE_PATH),
    )

    venue_lookup = {
        str(row["venue_id"]): row
        for row in venue_rows
    }

    for year in YEARS:
        join_season(year, venue_lookup)

    print("============================================")
    print("Venue / Local Time Join Complete")
    print("============================================")


if __name__ == "__main__":
    main()
