"""
Totals analysis for the betting dataset.

This module computes statistics related to over/under totals from
the normalized data returned by loader.py.

It intentionally performs no Markdown formatting.
"""

from statistics import mean


def analyze_totals(data):
    """
    Analyze over/under values across the betting dataset.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data().

    Returns
    -------
    dict
        Totals analysis results.
    """

    totals = data["total_values"]

    if not totals:
        return {
            "total_count": 0,
            "minimum_total": None,
            "maximum_total": None,
            "average_total": None,
            "median_total": None,
        }

    sorted_totals = sorted(totals)

    count = len(sorted_totals)

    # Compute median without requiring the statistics module.
    if count % 2 == 1:
        median = sorted_totals[count // 2]
    else:
        median = (
            sorted_totals[(count // 2) - 1]
            + sorted_totals[count // 2]
        ) / 2

    return {
        "total_count": count,
        "minimum_total": min(sorted_totals),
        "maximum_total": max(sorted_totals),
        "average_total": round(mean(sorted_totals), 2),
        "median_total": round(median, 2),
    }
