"""
Join normalized team-week rankings to the games + teams + betting layer.

Input:
    data/normalized/betting/joined/YYYY_games_teams_betting.csv
    data/normalized/rankings/YYYY_rankings.csv

Output:
    data/normalized/rankings/joined/YYYY_games_teams_betting_rankings.csv

Ranking timing policy:
    - Regular-season games use the ranking record for the same season,
      season_type, week, and team.
    - Postseason games use the latest available regular-season ranking for
      each team. The CFBD rankings data represents postseason week 1 as
      postseason/final poll data, which is not an entering-game ranking for
      the bowl games. The source data does not provide publication timestamps,
      so exact publication timing cannot be independently verified here.

The normalized ranking layer retains CFP, AP, Coaches, effective rank, and
source. This join adds only the game-level home/away ranking fields required
by the master-game specification.
"""

import csv
from pathlib import Path


YEARS = range(2016, 2026)

GAME_DIR = Path("data/normalized/betting/joined")
RANKING_DIR = Path("data/normalized/rankings")
OUTPUT_DIR = Path("data/normalized/rankings/joined")

RANKING_FIELDS = [
    "effective_rank",
    "ranking_source",
]


def load_csv(path):
    """Load a CSV and return fields and rows."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fields = reader.fieldnames or []
        rows = list(reader)

    return fields, rows


def validate_unique_game_ids(rows, source):
    """Ensure the game-level input has one row per game."""
    seen = set()

    for row in rows:
        game_id = row.get("game_id", "")

        if not game_id:
            raise ValueError(f"{source}: row without game_id.")

        if game_id in seen:
            raise ValueError(
                f"{source}: duplicate game_id detected: {game_id}"
            )

        seen.add(game_id)


def ranking_number(value):
    """Return an integer ranking or None for a missing value."""
    if value in ("", None):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def build_ranking_lookup(rows):
    """Build a lookup keyed by season, season type, week, and team."""
    lookup = {}

    for row in rows:
        key = (
            row["season"],
            row["season_type"],
            row["week"],
            row["team_id"],
        )

        if key in lookup:
            raise ValueError(
                "Duplicate ranking key detected: "
                f"{key}"
            )

        lookup[key] = row

    return lookup


def build_postseason_lookup(rows):
    """Return the latest regular-season ranking for each team."""
    regular = [
        row for row in rows
        if row.get("season_type") == "regular"
    ]

    if not regular:
        return {}

    latest_week = max(
        int(row["week"])
        for row in regular
        if str(row["week"]).isdigit()
    )

    return {
        row["team_id"]: row
        for row in regular
        if str(row["week"]).isdigit()
        and int(row["week"]) == latest_week
    }


def find_ranking(
    game,
    team_id,
    ranking_lookup,
    postseason_lookup,
):
    """Find the entering-game ranking for one team."""
    season = str(game["season"])
    season_type = game["season_type"]
    week = str(game["week"])

    if season_type == "regular":
        return ranking_lookup.get(
            (season, "regular", week, str(team_id))
        )

    if season_type == "postseason":
        return postseason_lookup.get(str(team_id))

    return None


def join_season(year):
    """Join rankings to one season of the betting-enriched games."""
    game_path = GAME_DIR / f"{year}_games_teams_betting.csv"
    ranking_path = RANKING_DIR / f"{year}_rankings.csv"
    output_path = OUTPUT_DIR / f"{year}_games_teams_betting_rankings.csv"

    game_fields, games = load_csv(game_path)
    ranking_fields, ranking_rows = load_csv(ranking_path)

    required_game = {
        "game_id",
        "season",
        "season_type",
        "week",
        "home_team_id",
        "away_team_id",
    }

    missing_game = required_game - set(game_fields)
    if missing_game:
        raise ValueError(
            f"{game_path}: missing required columns: "
            f"{sorted(missing_game)}"
        )

    required_ranking = {
        "season",
        "season_type",
        "week",
        "team_id",
        *RANKING_FIELDS,
    }

    missing_ranking = required_ranking - set(ranking_fields)
    if missing_ranking:
        raise ValueError(
            f"{ranking_path}: missing required columns: "
            f"{sorted(missing_ranking)}"
        )

    validate_unique_game_ids(games, str(game_path))

    ranking_lookup = build_ranking_lookup(ranking_rows)
    postseason_lookup = build_postseason_lookup(ranking_rows)

    output_fields = list(game_fields) + [
        "home_rank",
        "away_rank",
        "home_rank_source",
        "away_rank_source",
        "home_rank_available",
        "away_rank_available",
    ]

    output_rows = []
    home_matches = 0
    away_matches = 0

    for game in games:
        home = find_ranking(
            game,
            game["home_team_id"],
            ranking_lookup,
            postseason_lookup,
        )
        away = find_ranking(
            game,
            game["away_team_id"],
            ranking_lookup,
            postseason_lookup,
        )

        if home is not None:
            home_matches += 1

        if away is not None:
            away_matches += 1

        output = dict(game)

        output["home_rank"] = (
            home.get("effective_rank", "")
            if home is not None
            else ""
        )
        output["away_rank"] = (
            away.get("effective_rank", "")
            if away is not None
            else ""
        )
        output["home_rank_source"] = (
            home.get("ranking_source", "")
            if home is not None
            else ""
        )
        output["away_rank_source"] = (
            away.get("ranking_source", "")
            if away is not None
            else ""
        )
        output["home_rank_available"] = (
            "True" if ranking_number(output["home_rank"]) is not None
            else "False"
        )
        output["away_rank_available"] = (
            "True" if ranking_number(output["away_rank"]) is not None
            else "False"
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
            f"{year}: output row count changed during ranking join."
        )

    print("--------------------------------------------")
    print(f"{year}")
    print(f"Games                : {len(games):,}")
    print(f"Home ranking matched : {home_matches:,}")
    print(f"Away ranking matched : {away_matches:,}")
    print(f"Output               : {output_path}")
    print("PASS")


def main():
    print("============================================")
    print("College Football ATS Research Platform")
    print("Game Ranking Join")
    print("============================================")

    for year in YEARS:
        join_season(year)

    print("============================================")
    print("Game Ranking Join Complete")
    print("============================================")


if __name__ == "__main__":
    main()
