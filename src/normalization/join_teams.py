import csv
import json
from pathlib import Path

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

YEARS = range(2016, 2026)

GAME_DIR = Path("data/normalized/seasons")
TEAM_DIR = Path("data/raw/teams")
OUTPUT_DIR = Path("data/normalized/games_teams")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Processing
# ---------------------------------------------------------------------

for year in YEARS:

    print("===================================================")
    print(f"Season {year}")

    # -------------------------------------------------
    # Load Games
    # -------------------------------------------------

    with (GAME_DIR / f"{year}_games.csv").open(
        "r",
        encoding="utf-8",
        newline=""
    ) as f:

        games = list(csv.DictReader(f))

    # -------------------------------------------------
    # Load Teams
    # -------------------------------------------------

    with (TEAM_DIR / f"{year}_teams.json").open(
        "r",
        encoding="utf-8"
    ) as f:

        teams = json.load(f)

    # -------------------------------------------------
    # Build Team Lookup
    # -------------------------------------------------

    team_lookup = {
        team["id"]: team
        for team in teams
    }

    print(f"Games Loaded : {len(games)}")
    print(f"Teams Loaded : {len(teams)}")

    # -------------------------------------------------
    # Output Fields
    # -------------------------------------------------

    fields = list(games[0].keys()) + [

        "home_abbreviation",
        "home_conference",
        "home_classification",

        "away_abbreviation",
        "away_conference",
        "away_classification"

    ]

    output_file = OUTPUT_DIR / f"{year}_games_teams.csv"

    missing_home = 0
    missing_away = 0

    # -------------------------------------------------
    # Write Output
    # -------------------------------------------------

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as outfile:

        writer = csv.DictWriter(
            outfile,
            fieldnames=fields
        )

        writer.writeheader()

        for game in games:

            home = team_lookup.get(
                int(game["home_team_id"])
            )

            away = team_lookup.get(
                int(game["away_team_id"])
            )

            if home is None:
                missing_home += 1
                home = {}

            if away is None:
                missing_away += 1
                away = {}

            game.update({

                "home_abbreviation":
                    home.get("abbreviation"),

                "home_conference":
                    home.get("conference"),

                "home_classification":
                    home.get("classification"),

                "away_abbreviation":
                    away.get("abbreviation"),

                "away_conference":
                    away.get("conference"),

                "away_classification":
                    away.get("classification")

            })

            writer.writerow(game)

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    print(f"Missing Home Teams : {missing_home}")
    print(f"Missing Away Teams : {missing_away}")

    if missing_home or missing_away:
        raise RuntimeError(
            f"Team join failed for {year}."
        )

    print("PASS")

print("===================================================")
print("Team Join Complete")
print("===================================================")
