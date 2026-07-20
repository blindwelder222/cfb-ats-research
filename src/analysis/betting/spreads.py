"""
Spread analysis for the betting dataset.

This module computes statistics related to point spreads from
the normalized data returned by loader.py.

It intentionally performs no Markdown formatting.
"""

from statistics import mean


def analyze_spreads(data):
    """
    Analyze spread values across the betting dataset.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data().

    Returns
    -------
    dict
        Spread analysis results.
    """

    spreads = data["spread_values"]

    if not spreads:
        return {
            "spread_count": 0,
            "minimum_spread": None,
            "maximum_spread": None,
            "average_spread": None,
            "median_spread": None,
        }

    sorted_spreads = sorted(spreads)

    count = len(sorted_spreads)

    # Compute median without requiring the statistics module.
    if count % 2 == 1:
        median = sorted_spreads[count // 2]
    else:
        median = (
            sorted_spreads[(count // 2) - 1]
            + sorted_spreads[count // 2]
        ) / 2

    return {
        "spread_count": count,
        "minimum_spread": min(sorted_spreads),
        "maximum_spread": max(sorted_spreads),
        "average_spread": round(mean(sorted_spreads), 2),
        "median_spread": round(median, 2),
    }
