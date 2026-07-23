import json

from collections import Counter
from pathlib import Path
from statistics import mean


YEARS = range(2016, 2026)

DATA_DIR = Path("data/raw/betting")


def load_betting_data():
    """
    Load all betting JSON files and return a normalized analysis dictionary.

    This module intentionally preserves the behavior of
    analyze_betting.py v1. It performs no report formatting.
    """

    games_total = 0
    games_with_lines = 0
    games_without_lines = 0

    provider_counter = Counter()
    providers_per_game = Counter()

    spread_count = 0
    total_count = 0

    spread_values = []
    total_values = []

    season_summary = {}

    for year in YEARS:

        season_games = 0
        season_with_lines = 0
        season_provider_counts = []

        for season in ("regular", "post"):

            filename = (
                DATA_DIR
                / season
                / f"{year}_{'lines' if season == 'regular' else 'lines_b'}.json"
            )

            with filename.open("r", encoding="utf-8") as f:
                games = json.load(f)

            for game in games:

                games_total += 1
                season_games += 1

                lines = game.get("lines", [])

                if not lines:
                    games_without_lines += 1
                    continue

                games_with_lines += 1
                season_with_lines += 1

                providers_per_game[len(lines)] += 1
                season_provider_counts.append(len(lines))

                for line in lines:

                    provider = line.get("provider", "UNKNOWN")
                    provider_counter[provider] += 1

                    spread = line.get("spread")
                    if spread is not None:
                        spread_count += 1
                        spread_values.append(abs(float(spread)))

                    total = line.get("overUnder")
                    if total is not None:
                        total_count += 1
                        total_values.append(float(total))

        season_summary[year] = {
            "games": season_games,
            "coverage": season_with_lines,
            "avg_providers": (
                round(mean(season_provider_counts), 2)
                if season_provider_counts
                else 0
            ),
        }

    return {
        "games_total": games_total,
        "games_with_lines": games_with_lines,
        "games_without_lines": games_without_lines,
        "provider_counter": provider_counter,
        "providers_per_game": providers_per_game,
        "spread_count": spread_count,
        "total_count": total_count,
        "spread_values": spread_values,
        "total_values": total_values,
        "season_summary": season_summary,
    }
