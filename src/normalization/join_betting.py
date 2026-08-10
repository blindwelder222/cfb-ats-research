
"""
Join game/team records with game-level consensus betting data.

Input:
    data/normalized/teams/YYYY_games_teams.csv
    data/normalized/betting/consensus/YYYY_consensus.csv

Output:
    data/normalized/master/YYYY_games_master.csv

The games/teams dataset is the authoritative game population for the join.
The betting consensus is left-joined by game_id so games without betting
coverage remain in the master dataset.

Betting records that do not match a games/teams record are reported but are
not added to the master dataset. This is intentional: the current
games/teams dataset defines the canonical game population for this research
pipeline.

No betting values are recalculated or selected during this join.
"""

import csv
from pathlib import Path


YEARS = range(2016, 2026)

GAME_TEAM_DIR = Path("data/normalized/teams")
CONSENSUS_DIR = Path("data/normalized/betting/consensus")
OUTPUT_DIR = Path("data/normalized/joined")

CONSENSUS_FIELDS = [
    "spread_provider_count",
    "consensus_spread",
    "spread_mean",
    "spread_median",
    "spread_min",
    "spread_max",
    "spread_range",
    "spread_stddev",
    "spread_open_provider_count",
    "consensus_spread_open",
    "spread_open_mean",
    "spread_open_median",
    "spread_open_min",
    "spread_open_max",
    "spread_open_range",
    "spread_open_stddev",
    "total_provider_count",
    "consensus_total",
    "total_mean",
    "total_median",
    "total_min",
    "total_max",
    "total_range",
    "total_stddev",
    "total_open_provider_count",
    "consensus_total_open",
    "total_open_mean",
    "total_open_median",
    "total_open_min",
    "total_open_max",
    "total_open_range",
    "total_open_stddev",
]


def load_csv(path):
    """Load a CSV and return its fields and rows."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        fields = reader.fieldnames or []
        rows = list(reader)

    return fields, rows


def validate_unique_game_ids(rows, source):
    """Ensure a game-level input contains one record per game."""
    seen = set()

    for row in rows:
        game_id = row.get("game_id", "")

        if not game_id:
            raise ValueError(
                f"{source}: encountered a row without game_id."
            )

        if game_id in seen:
            raise ValueError(
                f"{source}: duplicate game_id detected: {game_id}"
            )

        seen.add(game_id)


def join_season(year):
    """Join one season's game/team records to betting consensus."""
    game_path = GAME_TEAM_DIR / f"{year}_games_teams.csv"
    consensus_path = CONSENSUS_DIR / f"{year}_consensus.csv"
    output_path = OUTPUT_DIR / f"{year}_games_master.csv"

    game_fields, games = load_csv(game_path)
    consensus_fields, consensus_rows = load_csv(consensus_path)

    if not game_fields:
        raise ValueError(f"{game_path}: no fields found.")

    required_consensus = {"game_id", *CONSENSUS_FIELDS}
    missing = required_consensus - set(consensus_fields)

    if missing:
        raise ValueError(
            f"{consensus_path}: missing required columns: "
            f"{sorted(missing)}"
        )

    validate_unique_game_ids(games, str(game_path))
    validate_unique_game_ids(consensus_rows, str(consensus_path))

    consensus_lookup = {
        row["game_id"]: row
        for row in consensus_rows
    }

    output_fields = list(game_fields) + [
        field for field in CONSENSUS_FIELDS
        if field not in game_fields
    ] + ["betting_available"]

    matched = 0
    missing_betting = 0
    output_rows = []

    for game in games:
        game_id = game["game_id"]
        betting = consensus_lookup.get(game_id)

        if betting is None:
            missing_betting += 1
            betting_available = "False"
        else:
            matched += 1
            betting_available = "True"

        output = dict(game)

        for field in CONSENSUS_FIELDS:
            output[field] = (
                betting.get(field, "")
                if betting is not None
                else ""
            )

        output["betting_available"] = betting_available
        output_rows.append(output)

    unmatched_betting = len(
        set(consensus_lookup) - {row["game_id"] for row in games}
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=output_fields,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    if len(output_rows) != len(games):
        raise RuntimeError(
            f"{year}: output row count changed during betting join."
        )

    if matched + missing_betting != len(games):
        raise RuntimeError(
            f"{year}: betting join accounting failed."
        )

    print("--------------------------------------------")
    print(f"{year}")
    print(f"Games/Teams       : {len(games):,}")
    print(f"Consensus Records  : {len(consensus_rows):,}")
    print(f"Betting Matched    : {matched:,}")
    print(f"Games Without Bet  : {missing_betting:,}")
    print(f"Betting Unmatched  : {unmatched_betting:,}")
    print(f"Master Records     : {len(output_rows):,}")
    print(f"Output             : {output_path}")
    print("PASS")


def main():
    print("============================================")
    print("College Football ATS Research Platform")
    print("Master Game Betting Join")
    print("============================================")

    for year in YEARS:
        join_season(year)

    print("============================================")
    print("Master Game Betting Join Complete")
    print("============================================")


if __name__ == "__main__":
    main()
