"""
Consensus betting line analysis.

This module summarizes sportsbook agreement without attempting to
identify a preferred betting line.
"""

from statistics import mean


def analyze_consensus(data):
    """
    Analyze betting consensus.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data()

    Returns
    -------
    dict
    """

    provider_counts = data["providers_per_game"]

    games_with_lines = len(provider_counts)

    if games_with_lines == 0:
        return {
            "games": 0,
            "average_providers": 0,
            "minimum_providers": 0,
            "maximum_providers": 0,
            "distribution": {}
        }

    distribution = {}

    for count in provider_counts:
        distribution[count] = distribution.get(count, 0) + 1

    return {
        "games": games_with_lines,
        "average_providers": round(mean(provider_counts), 2),
        "minimum_providers": min(provider_counts),
        "maximum_providers": max(provider_counts),
        "distribution": dict(sorted(distribution.items()))
    }
