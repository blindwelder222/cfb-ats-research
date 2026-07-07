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

def acquire_teams(api, year):

    print(f"Downloading {year} teams...")

    teams = api.get_teams(
        year=year
    )

    filename = f"{year}_teams.json"

    output_dir = Path("data/raw/teams")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            [
                team.to_dict() if hasattr(team, "to_dict") else team
                for team in teams
            ],
            f,
            indent=2,
            default=str
        )

    print(f"  ✓ {filename} ({len(teams)} teams)")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Historical Teams Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.TeamsApi(client)

    total_files = 0

    for year in YEARS:

        acquire_teams(
            api=api,
            year=year
        )

        total_files += 1

    print()
    print("===================================================")
    print("Historical Teams Acquisition Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Files Created   : {total_files}")
    print("Output Directory: data/raw/teams/")
    print("===================================================")


if __name__ == "__main__":
    main()
