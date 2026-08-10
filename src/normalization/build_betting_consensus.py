
"""
Build one consensus betting record per game from canonical seasonal betting data.

Input:
    data/normalized/betting/YYYY_betting.csv

Output:
    data/normalized/betting/consensus/YYYY_consensus.csv

The input contains one row per provider observation. This module reduces those
observations to one game-level record while preserving useful information
about market breadth and provider disagreement.

Consensus policy:
    - Current spread consensus = median of valid current spreads.
    - Opening spread consensus = median of valid opening spreads.
    - Current total consensus = median of valid non-negative totals.
    - Opening total consensus = median of valid non-negative opening totals.
    - Provider counts are calculated independently for spread and total.
    - Missing values are excluded from the corresponding calculation.
    - Negative totals are treated as invalid placeholders and excluded.
    - Provider-level records are never modified or deleted.
"""

from pathlib import Path
from statistics import mean, median, stdev
import csv
import math


YEARS = range(2016, 2026)

BETTING_DIR = Path("data/normalized/betting")
OUTPUT_DIR = BETTING_DIR / "consensus"

FIELDS = [
    "game_id",
    "season",
    "season_type",
    "week",
    "start_date",
    "home_team_id",
    "home_team",
    "away_team_id",
    "away_team",
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


def numeric_values(rows, field, non_negative=False):
    """Return valid numeric observations for one field."""
    values = []

    for row in rows:
        value = row.get(field, "")

        if value in ("", None):
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            continue

        if not math.isfinite(number):
            continue

        if non_negative and number < 0:
            continue

        values.append(number)

    return values


def statistics(values):
    """Return the standard market statistics for a set of observations."""
    if not values:
        return {
            "provider_count": 0,
            "consensus": "",
            "mean": "",
            "median": "",
            "min": "",
            "max": "",
            "range": "",
            "stddev": "",
        }

    return {
        "provider_count": len(values),
        "consensus": median(values),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "range": max(values) - min(values),
        "stddev": stdev(values) if len(values) > 1 else 0.0,
    }


def load_season(path):
    """Load one canonical seasonal betting CSV."""
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")

    with path.open("r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    required = {
        "game_id",
        "season",
        "season_type",
        "week",
        "start_date",
        "home_team_id",
        "home_team",
        "away_team_id",
        "away_team",
        "provider",
        "spread",
        "spread_open",
        "over_under",
        "over_under_open",
    }

    missing = required - set(reader.fieldnames or [])
    if missing:
        raise ValueError(
            f"{path} is missing required columns: {sorted(missing)}"
        )

    return rows


def game_identity(rows):
    """Build the game-level identity fields from provider observations."""
    first = rows[0]

    return {
        "game_id": first.get("game_id", ""),
        "season": first.get("season", ""),
        "season_type": first.get("season_type", ""),
        "week": first.get("week", ""),
        "start_date": first.get("start_date", ""),
        "home_team_id": first.get("home_team_id", ""),
        "home_team": first.get("home_team", ""),
        "away_team_id": first.get("away_team_id", ""),
        "away_team": first.get("away_team", ""),
    }


def build_record(game_id, rows):
    """Build one game-level consensus record."""
    spread = statistics(numeric_values(rows, "spread"))
    spread_open = statistics(numeric_values(rows, "spread_open"))

    total = statistics(
        numeric_values(rows, "over_under", non_negative=True)
    )
    total_open = statistics(
        numeric_values(rows, "over_under_open", non_negative=True)
    )

    record = game_identity(rows)
    record["game_id"] = game_id

    record.update({
        "spread_provider_count": spread["provider_count"],
        "consensus_spread": spread["consensus"],
        "spread_mean": spread["mean"],
        "spread_median": spread["median"],
        "spread_min": spread["min"],
        "spread_max": spread["max"],
        "spread_range": spread["range"],
        "spread_stddev": spread["stddev"],

        "spread_open_provider_count": spread_open["provider_count"],
        "consensus_spread_open": spread_open["consensus"],
        "spread_open_mean": spread_open["mean"],
        "spread_open_median": spread_open["median"],
        "spread_open_min": spread_open["min"],
        "spread_open_max": spread_open["max"],
        "spread_open_range": spread_open["range"],
        "spread_open_stddev": spread_open["stddev"],

        "total_provider_count": total["provider_count"],
        "consensus_total": total["consensus"],
        "total_mean": total["mean"],
        "total_median": total["median"],
        "total_min": total["min"],
        "total_max": total["max"],
        "total_range": total["range"],
        "total_stddev": total["stddev"],

        "total_open_provider_count": total_open["provider_count"],
        "consensus_total_open": total_open["consensus"],
        "total_open_mean": total_open["mean"],
        "total_open_median": total_open["median"],
        "total_open_min": total_open["min"],
        "total_open_max": total_open["max"],
        "total_open_range": total_open["range"],
        "total_open_stddev": total_open["stddev"],
    })

    return record


def process_year(year):
    """Build the consensus file for one season."""
    input_path = BETTING_DIR / f"{year}_betting.csv"
    output_path = OUTPUT_DIR / f"{year}_consensus.csv"

    rows = load_season(input_path)

    grouped = {}
    for row in rows:
        game_id = row.get("game_id", "")

        if not game_id:
            raise ValueError(
                f"{input_path}: encountered a betting row without game_id."
            )

        grouped.setdefault(game_id, []).append(row)

    records = [
        build_record(game_id, game_rows)
        for game_id, game_rows in sorted(grouped.items())
    ]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDS,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(records)

    if len(records) != len(grouped):
        raise RuntimeError(
            f"{year}: consensus record count validation failed."
        )

    print(
        f"{year}: {len(rows):,} provider rows -> "
        f"{len(records):,} game consensus rows -> {output_path}"
    )


def main():
    print("===================================================")
    print("College Football ATS Research Platform")
    print("Betting Consensus Builder")
    print("===================================================")

    for year in YEARS:
        process_year(year)

    print("===================================================")
    print("Betting Consensus Build Complete")
    print("===================================================")


if __name__ == "__main__":
    main()
