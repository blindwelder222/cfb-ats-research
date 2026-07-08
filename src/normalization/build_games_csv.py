import csv
import json
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

SEASON_TYPES = {
    "regular": "gd",
    "post": "gdb"
}

FIELDS = [
    "game_id",
    "season",
    "season_type",
    "week",
    "start_date",
    "completed",
    "neutral_site",
    "conference_game",
    "attendance",
    "venue_id",
    "venue",
    "home_team_id",
    "home_team",
    "away_team_id",
    "away_team",
    "home_points",
    "away_points",
]

OUTPUT_DIR = Path("data/normalized/games")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------

for year in YEARS:

    for season_folder, suffix in SEASON_TYPES.items():

        input_file = Path(
            f"data/raw/games/{season_folder}/{year}_{suffix}.json"
        )

        output_file = OUTPUT_DIR / f"{year}_{season_folder}.csv"

        print("---------------------------------------------------")
        print(f"Reading : {input_file.name}")

        with input_file.open("r", encoding="utf-8") as f:
            games = json.load(f)

        with output_file.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.DictWriter(
                csvfile,
                fieldnames=FIELDS
            )

            writer.writeheader()

            for game in games:

                writer.writerow({

                    "game_id": game.get("id"),
                    "season": game.get("season"),
                    "season_type": game.get("seasonType"),
                    "week": game.get("week"),
                    "start_date": game.get("startDate"),

                    "completed": game.get("completed"),
                    "neutral_site": game.get("neutralSite"),
                    "conference_game": game.get("conferenceGame"),
                    "attendance": game.get("attendance"),

                    "venue_id": game.get("venueId"),
                    "venue": game.get("venue"),

                    "home_team_id": game.get("homeId"),
                    "home_team": game.get("homeTeam"),

                    "away_team_id": game.get("awayId"),
                    "away_team": game.get("awayTeam"),

                    "home_points": game.get("homePoints"),
                    "away_points": game.get("awayPoints")

                })

        print(f"Loaded : {len(games)}")
        print(f"Wrote  : {len(games)}")

        if len(games) == sum(1 for _ in open(output_file, encoding="utf-8")) - 1:
            print("PASS")
        else:
            raise RuntimeError(
                f"Record count mismatch for {output_file.name}"
            )

print("===================================================")
print("Games CSV Normalization Complete")
print("===================================================")
