import json
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

YEARS = range(2016, 2026)

DATA_DIR = Path("data/raw/betting")

REPORT_DIR = Path("reports/profiling")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = REPORT_DIR / "betting_profile.md"

# ----------------------------------------------------
# Statistics
# ----------------------------------------------------

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

# ----------------------------------------------------
# Read Files
# ----------------------------------------------------

for year in YEARS:

    season_games = 0
    season_with_lines = 0
    season_provider_counts = []

    for season in ["regular", "post"]:

        filename = (
            DATA_DIR /
            season /
            f"{year}_{'lines' if season == 'regular' else 'lines_post'}.json"
        )

        with filename.open(
            "r",
            encoding="utf-8"
        ) as f:

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
        "avg_providers":
            round(mean(season_provider_counts), 2)
            if season_provider_counts else 0
    }

# ----------------------------------------------------
# Report
# ----------------------------------------------------

with REPORT.open(
    "w",
    encoding="utf-8"
) as report:

    report.write("# Betting Dataset Profile\n\n")

    report.write("## Dataset Summary\n\n")

    report.write(f"* Games: {games_total}\n")
    report.write(f"* Games With Lines: {games_with_lines}\n")
    report.write(f"* Games Without Lines: {games_without_lines}\n")
    report.write(f"* Coverage: {games_with_lines/games_total:.2%}\n\n")

    report.write("## Providers\n\n")

    for provider, count in provider_counter.most_common():

        report.write(f"- {provider}: {count}\n")

    report.write("\n")

    report.write("## Providers Per Game\n\n")

    for providers, count in sorted(providers_per_game.items()):

        report.write(f"- {providers}: {count}\n")

    report.write("\n")

    report.write("## Spread Summary\n\n")

    report.write(f"* Spread Values: {spread_count}\n")

    if spread_values:

        report.write(f"* Minimum: {min(spread_values)}\n")
        report.write(f"* Maximum: {max(spread_values)}\n")

    report.write("\n")

    report.write("## Total Summary\n\n")

    report.write(f"* Totals: {total_count}\n")

    if total_values:

        report.write(f"* Minimum: {min(total_values)}\n")
        report.write(f"* Maximum: {max(total_values)}\n")

    report.write("\n")

    report.write("## Seasonal Summary\n\n")

    report.write("|Season|Games|Coverage|Avg Providers|\n")
    report.write("|---|---:|---:|---:|\n")

    for year, data in season_summary.items():

        report.write(
            f"|{year}|"
            f"{data['games']}|"
            f"{data['coverage']}|"
            f"{data['avg_providers']}|\n"
        )

print("==========================================")
print("Betting Dataset Profile Complete")
print("==========================================")
print(f"Report: {REPORT}")
