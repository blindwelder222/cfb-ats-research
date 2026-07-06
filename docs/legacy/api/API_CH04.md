# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH04.md

## Chapter 4 --- Tier 2 Enrichment Endpoints

**Document Status:** Canonical Development Draft **Parent Document:**
API_ENDPOINT_REFERENCE.md **Chapter:** 4 of N **Version:** 1.0-draft
**Project Phase:** Foundation Migration **Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

Tier 2 endpoints enhance the master database with contextual information
that expands research capabilities without being strictly required to
construct the database itself.

These datasets improve segmentation, historical analysis, and future
research modules while remaining secondary to the Tier 1 acquisition
layer.

------------------------------------------------------------------------

# Coaches Endpoint

## Purpose

Provides coaching information for teams and seasons.

## Priority

Tier 2 --- Recommended

## Primary Parameters

-   team
-   season (when applicable)

## Output File

coaches.json

## Update Frequency

Prior to each season and when coaching changes occur.

## Dependencies

-   Coach reference table
-   Coach ATS studies
-   Coaching tenure analysis

## Validation

-   Coach name present
-   Team identifier present
-   Season association valid

## Implementation Status

Planned

------------------------------------------------------------------------

# Venues Endpoint

## Purpose

Provides stadium and venue metadata for games.

## Priority

Tier 2 --- Recommended

## Output File

venues.json

## Update Frequency

As venue information changes.

## Dependencies

-   Stadium reference table
-   Home venue research
-   Geographic analysis

## Validation

-   Venue identifier
-   Venue name
-   Location metadata

## Implementation Status

Planned

------------------------------------------------------------------------

# Talent Endpoint

## Purpose

Provides roster talent ratings that may be incorporated into future
research.

## Priority

Tier 2 --- Optional Research

## Output File

talent\_`<season>`{=html}.json

## Update Frequency

Annually

## Dependencies

-   Talent-based studies
-   Team strength comparisons

## Validation

-   Team identifiers
-   Season consistency
-   Rating values present

## Implementation Status

Planned

------------------------------------------------------------------------

# Recruiting Endpoint

## Purpose

Provides historical recruiting information for long-term trend analysis.

## Priority

Tier 2 --- Optional Research

## Output File

recruiting\_`<season>`{=html}.json

## Update Frequency

Annually

## Dependencies

-   Recruiting studies
-   Multi-year program analysis

## Validation

-   Team identifiers
-   Recruiting class data
-   Season consistency

## Implementation Status

Planned

------------------------------------------------------------------------

# Tier 2 Summary

Tier 2 endpoints enrich the platform by providing context rather than
defining game outcomes.

These datasets support advanced research modules while remaining
independent of the minimum requirements needed to build the master
database.

------------------------------------------------------------------------

# Looking Ahead

Chapter 5 will define validation standards, acquisition workflow
integration, file naming conventions, dependency management, and
implementation sequencing for the complete acquisition pipeline.
