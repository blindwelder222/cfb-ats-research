
"""
Normalize the canonical CFBD venue reference list.

Input:
    data/raw/venues/venues.json

Output:
    data/normalized/venues/venues.csv

The venue endpoint is a parameterless master reference list. This module
preserves the canonical venue ID and the venue attributes needed by the
project, including timezone for later game-level local-time derivation.

Raw venue data is never modified.
"""

import csv
import json
from pathlib import Path


INPUT_PATH = Path("data/raw/venues/venues.json")
OUTPUT_PATH = Path("data/normalized/venues/venues.csv")

FIELDS = [
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


def load_venues():
    """Load and validate the raw venue master list."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_PATH}")

    with INPUT_PATH.open("r", encoding="utf-8") as json_file:
        venues = json.load(json_file)

    if not isinstance(venues, list):
        raise ValueError("Expected venues.json to contain a list.")

    return venues


def normalize_venue(venue):
    """Convert one CFBD venue record to the canonical normalized schema."""
    if venue.get("id") is None:
        raise ValueError("Venue record is missing its canonical id.")

    return {
        "venue_id": venue.get("id"),
        "venue_name": venue.get("name", ""),
        "capacity": venue.get("capacity", ""),
        "grass": venue.get("grass", ""),
        "dome": venue.get("dome", ""),
        "city": venue.get("city", ""),
        "state": venue.get("state", ""),
        "zip": venue.get("zip", ""),
        "country_code": venue.get("countryCode", ""),
        "timezone": venue.get("timezone", ""),
        "latitude": venue.get("latitude", ""),
        "longitude": venue.get("longitude", ""),
        "elevation": venue.get("elevation", ""),
        "construction_year": venue.get("constructionYear", ""),
    }


def validate_unique_ids(rows):
    """Ensure every normalized venue has one unique canonical ID."""
    seen = set()

    for row in rows:
        venue_id = row["venue_id"]

        if venue_id in seen:
            raise ValueError(
                f"Duplicate venue_id detected: {venue_id}"
            )

        seen.add(venue_id)


def main():
    print("===================================================")
    print("College Football ATS Research Platform")
    print("Venue Normalization")
    print("===================================================")

    raw_venues = load_venues()
    rows = [normalize_venue(venue) for venue in raw_venues]

    validate_unique_ids(rows)

    rows.sort(
        key=lambda row: (
            int(row["venue_id"])
            if str(row["venue_id"]).isdigit()
            else 999999999
        )
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Raw venues       : {len(raw_venues):,}")
    print(f"Normalized venues: {len(rows):,}")
    print(f"Output           : {OUTPUT_PATH}")
    print("Validation       : PASS")
    print("===================================================")


if __name__ == "__main__":
    main()
