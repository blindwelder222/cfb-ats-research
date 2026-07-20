"""
Markdown report generation for betting analysis.

This module is responsible ONLY for rendering analysis results
into a Markdown report.

It intentionally performs no analysis.
"""

from pathlib import Path


def _line(text=""):
    return text + "\n"


def write_report(
    summary,
    providers,
    spreads,
    totals,
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
