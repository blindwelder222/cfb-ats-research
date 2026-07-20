"""
Anomaly detection for betting dataset.

This module identifies statistical outliers and unusual characteristics
without making judgments about data quality.
"""

from collections import Counter


def analyze_anomalies(data):
    """
    Analyze unusual betting characteristics.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data()

    Returns
    -------
    dict
    """

    spreads = [s for s in data["spread_values"] if s is not None]
    totals = [t for t in data["total_values"] if t is not None]

    providers_per_game = data["providers_per_game"]

    if not spreads:
        return {}

    spread_counter = Counter(spreads)
    total_counter = Counter(totals)

    return {
        "largest_favorite": max(spreads),
        "largest_underdog": min(spreads),

        "highest_total": max(totals) if totals else None,
        "lowest_total": min(totals) if totals else None,

        "largest_provider_count": max(providers_per_game)
        if providers_per_game else 0,

        "single_occurrence_spreads": sum(
            1 for count in spread_counter.values()
            if count == 1
        ),

        "single_occurrence_totals": sum(
            1 for count in total_counter.values()
            if count == 1
        ),

        "distinct_spreads": len(spread_counter),

        "distinct_totals": len(total_counter)
    }
