"""
Summary analysis for the betting dataset.

This module computes high-level dataset statistics from the
normalized data returned by loader.py.

It intentionally performs no Markdown formatting.
"""


def build_summary(data):
    """
    Build the overall dataset summary.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data().

    Returns
    -------
    dict
        Summary statistics for the betting dataset.
    """

    games_total = data["games_total"]
    games_with_lines = data["games_with_lines"]
    games_without_lines = data["games_without_lines"]

    coverage_pct = (
        (games_with_lines / games_total) * 100
        if games_total
        else 0.0
    )

    return {
        "games_total": games_total,
        "games_with_lines": games_with_lines,
        "games_without_lines": games_without_lines,
        "coverage_percent": round(coverage_pct, 2),
        "season_summary": data["season_summary"],
    }
