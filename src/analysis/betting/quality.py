"""
Data quality analysis for betting dataset.

This module identifies potential data quality issues but does not
modify the underlying dataset.
"""

from collections import Counter


def analyze_quality(data):
    """
    Analyze betting dataset quality.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data()

    Returns
    -------
    dict
    """

    spreads = data["spread_values"]
    totals = data["total_values"]

    provider_counter = data["provider_counter"]

    provider_variants = {}

    # Very simple normalization check.
    # Later we can replace this with a canonical provider mapping.
    normalized = Counter()

    for provider in provider_counter:

        key = (
            provider.lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        normalized[key] += 1

    for provider in provider_counter:

        key = (
            provider.lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        if normalized[key] > 1:
            provider_variants.setdefault(key, []).append(provider)

    invalid_spreads = [
        value
        for value in spreads
        if value is None
    ]

    negative_totals = [
        value
        for value in totals
        if value is not None and value < 0
    ]

    zero_totals = [
        value
        for value in totals
        if value == 0
    ]

    extreme_spreads = [
        value
        for value in spreads
        if value is not None and abs(value) >= 40
    ]

    return {
        "provider_variants": provider_variants,
        "negative_totals": {
            "count": len(negative_totals),
            "values": sorted(set(negative_totals))
        },
        "zero_totals": {
            "count": len(zero_totals)
        },
        "invalid_spreads": {
            "count": len(invalid_spreads)
        },
        "extreme_spreads": {
            "count": len(extreme_spreads),
            "maximum": max(extreme_spreads) if extreme_spreads else None
        }
    }
