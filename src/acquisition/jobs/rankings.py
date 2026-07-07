import json
import os
from pathlib import Path

import cfbd

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)


# ---------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------

def acquire_rankings(api, year):

    print(f"Downloading {year} rankings...")

    rankings = api.get_rankings(
        year=year
    )

    filename = f"{year}_r.json"

    output_dir = Path("data/raw/rankings")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            [
                ranking.to_dict() if hasattr(ranking, "to_dict") else ranking
                for ranking in rankings
            ],
            f,
            indent=2,
            default=str
        )

    print(f"  ✓ {filename} ({len(rankings)} weeks)")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Historical Rankings Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.RankingsApi(client)

    total_files = 0

    for year in YEARS:

        acquire_rankings(
            api=api,
            year=year
        )

        total_files += 1

    print()
    print("===================================================")
    print("Historical Rankings Acquisition Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Files Created   : {total_files}")
    print("Output Directory: data/raw/rankings/")
    print("===================================================")


if __name__ == "__main__":
    main()
