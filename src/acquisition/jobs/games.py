import json
import os
from pathlib import Path

import cfbd

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

SEASON_TYPES = {
    "regular": "gd",
    "postseason": "gdb"
}


# ---------------------------------------------------------------------
# Acquisition
# ---------------------------------------------------------------------

def acquire_games(api, year, season_type, suffix):

    print(f"Downloading {year} {season_type} games...")

    games = api.get_games(
        year=year,
        season_type=season_type,
        classification="fbs"
    )

    filename = f"{year}_{suffix}.json"

    output_dir = Path("data/raw/games")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(
            [
                game.to_dict() if hasattr(game, "to_dict") else game
                for game in games
            ],
            f,
            indent=2,
            default=str
        )

    print(f"  ✓ {filename} ({len(games)} games)")


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("===================================================")
    print("College Football ATS Research Platform")
    print("Historical Games Acquisition")
    print("===================================================")

    api_key = os.getenv("CFBD_API_KEY")

    if not api_key:
        raise RuntimeError("CFBD_API_KEY environment variable not found.")

    configuration = cfbd.Configuration(
        access_token=api_key
    )

    client = cfbd.ApiClient(configuration)

    api = cfbd.GamesApi(client)

    total_files = 0

    for year in YEARS:

        for season_type, suffix in SEASON_TYPES.items():

            acquire_games(
                api=api,
                year=year,
                season_type=season_type,
                suffix=suffix
            )

            total_files += 1

    print()
    print("===================================================")
    print("Historical Games Acquisition Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Files Created   : {total_files}")
    print("Output Directory: data/raw/games/")
    print("===================================================")


if __name__ == "__main__":
    main()
