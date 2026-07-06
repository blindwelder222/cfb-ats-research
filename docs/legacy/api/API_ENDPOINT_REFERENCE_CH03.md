# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH03.md

## Chapter 3 --- Tier 1 Research Endpoints

**Document Status:** Canonical Development Draft\
**Parent Document:** API_ENDPOINT_REFERENCE.md\
**Chapter:** 3 of N\
**Version:** 1.0-draft\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This chapter documents the Tier 1 endpoints that enrich the core game
records with information required for ATS research. These datasets
provide rankings, betting markets, and season performance metadata that
transform schedules and scores into research-ready records.

------------------------------------------------------------------------

# Rankings Endpoint

## Purpose

Provides nationally recognized team rankings used throughout the
platform.

## Priority

Tier 1 --- Required

## Primary Parameters

-   season
-   week
-   seasonType

## Output File

rankings\_`<season>`{=html}.json

## Update Frequency

Weekly during the season.

## Dependencies

-   Effective Rank
-   Ranked matchup identification
-   Ranked team research

## Validation

-   Poll names present
-   Team identifiers populated
-   Ranking values valid

## Implementation Status

Planned

------------------------------------------------------------------------

# Betting Lines Endpoint

## Purpose

Provides betting market data required for ATS calculations.

## Priority

Tier 1 --- Required

## Primary Parameters

-   season
-   week
-   seasonType
-   provider (when supported)

## Output File

lines\_`<season>`{=html}.json

## Update Frequency

Weekly during the season.

## Dependencies

-   ATS Margin
-   Covered field
-   Line movement
-   Betting research

## Validation

-   Game identifiers present
-   Spread values available
-   Duplicate lines detected
-   Provider recorded

## Notes

Consensus betting information is preferred whenever available.

## Implementation Status

Planned

------------------------------------------------------------------------

# Team Records Endpoint

## Purpose

Provides season record summaries for research enrichment.

## Priority

Tier 1 --- Required

## Output File

records\_`<season>`{=html}.json

## Update Frequency

Weekly during the season.

## Dependencies

-   Team summaries
-   Record-based filtering
-   Supplemental analytics

## Validation

-   Team identifiers
-   Wins and losses
-   Season consistency

## Implementation Status

Planned

------------------------------------------------------------------------

# Tier 1 Completion Summary

Together, Chapters 2 and 3 define the complete Tier 1 acquisition layer:

-   Games
-   Teams
-   Conferences
-   Rankings
-   Betting Lines
-   Team Records

These datasets provide the minimum information required to construct the
project's master database.

------------------------------------------------------------------------

# Looking Ahead

Chapter 4 introduces Tier 2 enrichment endpoints, including coaching
data, venues, and additional metadata that enhance research without
being mandatory for database construction.
