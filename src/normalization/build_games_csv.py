import csv
import json
from pathlib import Path


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

INPUT_FILE = Path("data/raw/games/regular/2016_gd.json")
OUTPUT_DIR = Path("data/normalized/games")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "2016_regular.csv"


# ---------------------------------------------------------------------
# Load Games
# ---------------------------------------------------------------------

with INPUT_FILE.open("r", encoding="utf-8") as f:
    games = json.load(f)

print(f"Loaded {len(games)} games.")


# ---------------------------------------------------------------------
# CSV Columns
# ---------------------------------------------------------------------

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


# ---------------------------------------------------------------------
# Write CSV
# ---------------------------------------------------------------------

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=FIELDS)

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

print(f"Wrote {len(games)} records.")
print("PASS")
