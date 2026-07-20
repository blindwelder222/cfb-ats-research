"""
College Football Betting Dataset Profiler

Version 2 (Refactor)

This script serves as the entry point for the betting analysis
pipeline. It coordinates data loading, executes analysis modules,
and generates the Markdown profiling report.

The analysis modules intentionally contain the analytical logic.
This file should remain lightweight.
"""

from betting.loader import load_betting_data
from betting.summary import build_summary
from betting.providers import analyze_providers
from betting.spreads import analyze_spreads
from betting.totals import analyze_totals
from betting.markdown import write_report


OUTPUT_REPORT = "reports/profiling/betting_profile_v2.md"


def main():
    """Execute the betting analysis workflow."""

    print("=" * 60)
    print("College Football Betting Dataset Profiler")
    print("Version 2 (Refactor)")
    print("=" * 60)

    print("Loading betting dataset...")
    data = load_betting_data()

    print("Building dataset summary...")
    summary = build_summary(data)

    print("Analyzing betting providers...")
    providers = analyze_providers(data)

    print("Analyzing point spreads...")
    spreads = analyze_spreads(data)

    print("Analyzing totals...")
    totals = analyze_totals(data)

    print("Generating Markdown report...")

    write_report(
        summary=summary,
        providers=providers,
        spreads=spreads,
        totals=totals,
        output_path=OUTPUT_REPORT,
    )

    print()
    print("Analysis complete.")
    print(f"Report written to: {OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
