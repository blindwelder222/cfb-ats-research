"""
Provider analysis for the betting dataset.

This module computes statistics related to betting providers from
the normalized data returned by loader.py.

It intentionally performs no Markdown formatting.
"""

from collections import Counter
from statistics import mean


def analyze_providers(data):
    """
    Analyze provider usage across the betting dataset.

    Parameters
    ----------
    data : dict
        Dictionary returned by loader.load_betting_data().

    Returns
    -------
    dict
        Provider analysis results.
    """

    provider_counter = data["provider_counter"]
    providers_per_game = data["providers_per_game"]

    total_games_with_lines = data["games_with_lines"]

    total_provider_entries = sum(provider_counter.values())

    average_providers = (
        total_provider_entries / total_games_with_lines
        if total_games_with_lines
        else 0.0
    )

    return {
        "provider_counts": dict(
            sorted(
                provider_counter.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ),
        "providers_per_game": dict(
            sorted(
                Counter(providers_per_game).items()
            )
        ),
        "unique_provider_count": len(provider_counter),
        "total_provider_entries": total_provider_entries,
        "average_providers_per_game": round(
            average_providers,
            2,
        ),
        "most_common_provider": (
            provider_counter.most_common(1)[0]
            if provider_counter
            else None
        ),
    }
