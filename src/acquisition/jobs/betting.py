import json
import os
from pathlib import Path

import cfbd

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

SEASON_TYPES = {
    "regular": "lines",
    "postseason": "lines_b"
}


# ---------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------

def acquire_lines(api, year, season_type, suffix):

    print(f"Downloading {year} {season_type} betting lines...")

    lines = api.get_lines(
        year=year,
        season_type=season_type
    )

    filename = f"{year}_{suffix}.json"

    output_dir = Path("data/raw/betting")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(
            [
                line.to_dict() if hasattr(line, "to_dict") else line
                for line in lines
            ],
            f,
            indent=2,
            default=str
        )

    print(f"  ✓ {filename} ({len(lines)} games)")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Historical Betting Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.BettingApi(client)

    total_files = 0

    for year in YEARS:

        for season_type, suffix in SEASON_TYPES.items():

            acquire_lines(
                api=api,
                year=year,
                season_type=season_type,
                suffix=suffix
            )

            total_files += 1

    print()
    print("===================================================")
    print("Historical Betting Acquisition Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Files Created   : {total_files}")
    print("Output Directory: data/raw/betting/")
    print("===================================================")


if __name__ == "__main__":
    main()
