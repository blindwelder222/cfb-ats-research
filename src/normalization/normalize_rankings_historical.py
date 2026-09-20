"""
Normalize historical rankings into a weekly team-level dataset.

Input:
    data/raw/rankings/YYYY_r.json

Output:
    data/normalized/rankings/YYYY_rankings.csv

Ranking precedence is defined by ATS_POLICY_v1.0.1:
    1. College Football Playoff (CFP)
    2. Associated Press (AP)
    3. Coaches Poll

The effective ranking is selected independently for each team/week. A
ranking is associated with the same season/season_type/week as the CFBD
rankings record so downstream joins can select the ranking entering a game.

The raw ranking files are never modified.
"""

import csv
import json
from pathlib import Path


YEARS = range(2016, 2026)

INPUT_DIR = Path("data/raw/rankings")
OUTPUT_DIR = Path("data/normalized/rankings")

POLL_NAMES = {
    "cfp": "Playoff Committee Rankings",
    "ap": "AP Top 25",
    "coaches": "Coaches Poll",
}

FIELDS = [
    "season",
    "season_type",
    "week",
    "team_id",
    "school",
    "conference",
    "cfp_rank",
    "ap_rank",
    "coaches_rank",
    "effective_rank",
    "ranking_source",
]


def load_rankings(path):
    """Load and validate one raw rankings file."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a list of weekly rankings.")

    return data


def normalize_week(week_record):
    """Normalize one weekly rankings record."""
    season = week_record.get("season")
    season_type = week_record.get("seasonType")
    week = week_record.get("week")

    polls = {
        poll.get("poll"): poll.get("ranks", [])
        for poll in week_record.get("polls", [])
        if poll.get("poll")
    }

    teams = {}

    for source_key, poll_name in POLL_NAMES.items():
        for rank_record in polls.get(poll_name, []):
            team_id = rank_record.get("teamId")

            if team_id is None:
                continue

            team = teams.setdefault(
                team_id,
                {
                    "season": season,
                    "season_type": season_type,
                    "week": week,
                    "team_id": team_id,
                    "school": rank_record.get("school", ""),
                    "conference": rank_record.get("conference", ""),
                    "cfp_rank": "",
                    "ap_rank": "",
                    "coaches_rank": "",
                    "effective_rank": "",
                    "ranking_source": "",
                },
            )

            team[f"{source_key}_rank"] = rank_record.get("rank")

            # Prefer the most complete identity metadata if a later poll
            # contains it.
            if not team["school"] and rank_record.get("school"):
                team["school"] = rank_record["school"]

            if not team["conference"] and rank_record.get("conference"):
                team["conference"] = rank_record["conference"]

    for team in teams.values():
        if team["cfp_rank"] not in ("", None):
            team["effective_rank"] = team["cfp_rank"]
            team["ranking_source"] = "CFP"
        elif team["ap_rank"] not in ("", None):
            team["effective_rank"] = team["ap_rank"]
            team["ranking_source"] = "AP"
        elif team["coaches_rank"] not in ("", None):
            team["effective_rank"] = team["coaches_rank"]
            team["ranking_source"] = "Coaches"

    return list(teams.values())


def validate_week_records(rows):
    """Ensure one team has at most one normalized record per week."""
    seen = set()

    for row in rows:
        key = (
            row["season"],
            row["season_type"],
            row["week"],
            row["team_id"],
        )

        if key in seen:
            raise ValueError(
                "Duplicate ranking record detected for "
                f"season={row['season']} season_type={row['season_type']} "
                f"week={row['week']} team_id={row['team_id']}"
            )

        seen.add(key)


def process_year(year):
    """Normalize one season's rankings."""
    input_path = INPUT_DIR / f"{year}_r.json"
    output_path = OUTPUT_DIR / f"{year}_rankings.csv"

    weekly_rankings = load_rankings(input_path)

    rows = []

    for week_record in weekly_rankings:
        rows.extend(normalize_week(week_record))

    validate_week_records(rows)

    rows.sort(
        key=lambda row: (
            row["season"],
            row["season_type"],
            int(row["week"]) if str(row["week"]).isdigit() else 999,
            int(row["effective_rank"])
            if str(row["effective_rank"]).isdigit()
            else 999,
            int(row["team_id"])
            if str(row["team_id"]).isdigit()
            else 999999999,
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with output_path.open(
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

    print(
        f"{year}: {len(weekly_rankings):,} ranking weeks -> "
        f"{len(rows):,} team-week records -> {output_path}"
    )


def main():
    print("===================================================")
    print("College Football ATS Research Platform")
    print("Historical Rankings Normalization")
    print("===================================================")

    for year in YEARS:
        process_year(year)

    print("===================================================")
    print("Historical Rankings Normalization Complete")
    print("===================================================")
    print(f"Years Processed : {len(YEARS)}")
    print(f"Output Directory: {OUTPUT_DIR}/")
    print("===================================================")


if __name__ == "__main__":
    main()
