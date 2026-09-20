"""
Normalize CFBD rankings into one season-level team/week CSV.

The script discovers both historical single-file rankings and current-season
weekly ranking files.

Inputs:
    data/raw/rankings/YYYY_r.json
    data/raw/rankings/YYYY/YYYY_r_wk_N.json

Output:
    data/normalized/rankings/YYYY_rankings.csv

Ranking precedence:
    1. CFP
    2. AP
    3. Coaches
"""

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

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


def classify_file(path: Path):
    match = re.match(r"^(?P<year>\d{4})_r(?:_wk_\d+)?$", path.stem)
    if not match:
        return None
    return int(match.group("year"))


def discover_inputs():
    groups = defaultdict(list)

    for path in sorted(INPUT_DIR.rglob("*.json")):
        year = classify_file(path)
        if year is not None:
            groups[year].append(path)

    return groups


def load_file(path):
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a list.")

    return data


def normalize_week(week_record):
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

            if not team["school"] and rank_record.get("school"):
                team["school"] = rank_record["school"]

            if not team["conference"] and rank_record.get("conference"):
                team["conference"] = rank_record["conference"]

    for team in teams.values():
        for key, source in (
            ("cfp_rank", "CFP"),
            ("ap_rank", "AP"),
            ("coaches_rank", "Coaches"),
        ):
            if team[key] not in ("", None):
                team["effective_rank"] = team[key]
                team["ranking_source"] = source
                break

    return list(teams.values())


def validate(rows, year):
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
                f"Duplicate ranking record: season={year}, "
                f"week={row['week']}, team_id={row['team_id']}"
            )
        seen.add(key)


def process_year(year, paths):
    rows = []

    for path in paths:
        print(f"Reading: {path}")
        for week_record in load_file(path):
            rows.extend(normalize_week(week_record))

    validate(rows, year)

    rows.sort(
        key=lambda row: (
            int(row["week"]) if str(row["week"]).isdigit() else 999,
            int(row["effective_rank"])
            if str(row["effective_rank"]).isdigit()
            else 999,
            int(row["team_id"]),
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{year}_rankings.csv"

    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} ranking records -> {output}")
    return len(rows)


def main():
    print("=" * 60)
    print("CFB ATS Research Platform")
    print("Rankings Normalization")
    print("=" * 60)

    groups = discover_inputs()

    if not groups:
        raise FileNotFoundError(
            f"No recognized ranking JSON files under {INPUT_DIR}"
        )

    total = 0

    for year, paths in sorted(groups.items()):
        total += process_year(year, paths)

    print("=" * 60)
    print(f"Seasons processed: {len(groups)}")
    print(f"Ranking records written: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()
