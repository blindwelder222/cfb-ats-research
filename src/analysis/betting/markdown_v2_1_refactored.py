"""
Markdown report renderer for the Betting Dataset Profiler.

Profiler Version: 2.1
"""

from pathlib import Path


def _line(text=""):
    return text + "\n"


def write_report(
    summary,
    providers,
    spreads,
    totals,
    quality, 
    consensus, 
    anomalies,
    output_path,
):
    """
    Write the betting profile report.

    Parameters
    ----------
    summary : dict
    providers : dict
    spreads : dict
    totals : dict
    output_path : str | pathlib.Path
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []

    # ---------------------------------------------------------
    # Header
    # ---------------------------------------------------------

    lines.append(_line("# Betting Dataset Profile (Version 2)"))
    lines.append(_line())

    lines.append(
        _line(
            "This report was generated automatically by "
            "`analyze_betting.py`."
        )
    )

    lines.append(_line())

    # ---------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------

    lines.append(_line("## Dataset Summary"))
    lines.append(_line())

    lines.append(
        _line(f"- Total Games: {summary['games_total']:,}")
    )

    lines.append(
        _line(
            f"- Games With Betting Lines: "
            f"{summary['games_with_lines']:,}"
        )
    )

    lines.append(
        _line(
            f"- Games Without Betting Lines: "
            f"{summary['games_without_lines']:,}"
        )
    )

    lines.append(
        _line(
            f"- Coverage: "
            f"{summary['coverage_percent']:.2f}%"
        )
    )

    lines.append(_line())

    # ---------------------------------------------------------
    # Seasonal Summary
    # ---------------------------------------------------------

    lines.append(_line("## Seasonal Summary"))
    lines.append(_line())

    lines.append(
        _line("| Season | Games | Coverage | Avg Providers |")
    )
    lines.append(
        _line("|-------:|------:|---------:|--------------:|")
    )

    for season, values in summary["season_summary"].items():

        lines.append(
            _line(
                f"| {season} "
                f"| {values['games']} "
                f"| {values['coverage']} "
                f"| {values['avg_providers']:.2f} |"
            )
        )

    lines.append(_line())

    # ---------------------------------------------------------
    # Provider Summary
    # ---------------------------------------------------------

    lines.append(_line("## Provider Summary"))
    lines.append(_line())

    lines.append(
        _line(
            f"- Unique Providers: "
            f"{providers['unique_provider_count']}"
        )
    )

    lines.append(
        _line(
            f"- Provider Entries: "
            f"{providers['total_provider_entries']:,}"
        )
    )

    lines.append(
        _line(
            f"- Average Providers Per Game: "
            f"{providers['average_providers_per_game']:.2f}"
        )
    )

    if providers["most_common_provider"]:

        name, count = providers["most_common_provider"]

        lines.append(
            _line(
                f"- Most Common Provider: "
                f"{name} ({count:,})"
            )
        )

    lines.append(_line())

    lines.append(_line("### Provider Counts"))
    lines.append(_line())

    lines.append(_line("| Provider | Entries |"))
    lines.append(_line("|---------|--------:|"))

    for provider, count in providers["provider_counts"].items():

        lines.append(
            _line(f"| {provider} | {count:,} |")
        )

    lines.append(_line())

    # ---------------------------------------------------------
    # Spread Summary
    # ---------------------------------------------------------

    lines.append(_line("## Spread Summary"))
    lines.append(_line())

    lines.append(
        _line(f"- Spread Values: {spreads['spread_count']:,}")
    )

    lines.append(
        _line(
            f"- Minimum Spread: "
            f"{spreads['minimum_spread']}"
        )
    )

    lines.append(
        _line(
            f"- Maximum Spread: "
            f"{spreads['maximum_spread']}"
        )
    )

    lines.append(
        _line(
            f"- Average Spread: "
            f"{spreads['average_spread']}"
        )
    )

    lines.append(
        _line(
            f"- Median Spread: "
            f"{spreads['median_spread']}"
        )
    )

    lines.append(_line())

    # ---------------------------------------------------------
    # Totals Summary
    # ---------------------------------------------------------

    lines.append(_line("## Totals Summary"))
    lines.append(_line())

    lines.append(
        _line(f"- Total Values: {totals['total_count']:,}")
    )

    lines.append(
        _line(
            f"- Minimum Total: "
            f"{totals['minimum_total']}"
        )
    )

    lines.append(
        _line(
            f"- Maximum Total: "
            f"{totals['maximum_total']}"
        )
    )

    lines.append(
        _line(
            f"- Average Total: "
            f"{totals['average_total']}"
        )
    )

    lines.append(
        _line(
            f"- Median Total: "
            f"{totals['median_total']}"
        )
    )

    lines.append(_line())

    output_path.write_text(
        "".join(lines),
        encoding="utf-8",
    )

    # ---------------------------------------------------------
    # Data Quality
    # ---------------------------------------------------------
    
    lines.append(_line("## Data Quality"))
    lines.append(_line())
    
    lines.append(
        _line(
            f"- Provider Variants: "
            f"{quality.get('provider_variants','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Negative Totals: "
            f"{quality.get('negative_totals','N/A')}"
        )
    )
    
    lines.append(
        _line(
             f"- Zero Totals: "
             f"{quality.get('zero_totals','N/A')}"
        )
    )
    
    lines.append(
     _line(
            f"- Invalid Spreads: "
            f"{quality.get('invalid_spreads','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Extreme Spreads: "
            f"{quality.get('extreme_spreads','N/A')}"
        )
    )

    lines.append(_line())

    # ---------------------------------------------------------
    # Consensus Analysis
    # ---------------------------------------------------------
    
    lines.append(_line("## Consensus Analysis"))
    lines.append(_line())
    
    lines.append(
        _line(
            f"- Games Evaluated: "
            f"{consensus.get('games',0):,}"
        )
    )
    
    lines.append(
        _line(
            f"- Average Providers/Game: "
            f"{consensus.get('average_providers',0):.2f}"
        )
    )
    
    lines.append(
        _line(
            f"- Minimum Providers: "
            f"{consensus.get('minimum_providers','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Maximum Providers: "
            f"{consensus.get('maximum_providers','N/A')}"
        )
    )
    
    lines.append(_line())
    
    lines.append(_line("### Provider Distribution"))
    lines.append(_line())
    
    lines.append(_line("| Providers | Games |"))
    lines.append(_line("|----------:|------:|"))
    
    for providers_per_game, count in consensus.get("distribution", {}).items():
        lines.append(
            _line(
                f"| {providers_per_game} | {count:,} |"
            )
        )
    
    lines.append(_line())
    
    # ---------------------------------------------------------
    # Anomaly Detection
    # ---------------------------------------------------------
    
    lines.append(_line("## Anomaly Detection"))
    lines.append(_line())
    
    lines.append(
        _line(
            f"- Largest Favorite: "
            f"{anomalies.get('largest_favorite','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Largest Underdog: "
            f"{anomalies.get('largest_underdog','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Highest Total: "
            f"{anomalies.get('highest_total','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Lowest Total: "
            f"{anomalies.get('lowest_total','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Largest Provider Count: "
            f"{anomalies.get('largest_provider_count','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Distinct Spread Values: "
            f"{anomalies.get('distinct_spreads','N/A')}"
        )
    )
    
    lines.append(
        _line(
            f"- Distinct Total Values: "
            f"{anomalies.get('distinct_totals','N/A')}"
        )
    )
    
    lines.append(_line())


# ---------------------------------------------------------
# Recommendations
# ---------------------------------------------------------

lines.append(_line("## Recommendations"))
lines.append(_line())
lines.append(_line("- Normalize sportsbook names before database integration."))
lines.append(_line("- Preserve provider-level betting lines."))
lines.append(_line("- Flag placeholder or invalid betting values."))
lines.append(_line("- Dataset is suitable for integration into the master research database."))
lines.append(_line())

output_path.write_text(
    "".join(lines),
    encoding="utf-8",
)
