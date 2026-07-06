# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH02.md

## Chapter 2 --- Tier 1 Core Endpoints

**Document Status:** Canonical Development Draft\
**Parent Document:** API_ENDPOINT_REFERENCE.md\
**Chapter:** 2 of 8\
**Version:** 1.1-draft\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Purpose

This chapter defines the Tier 1 core endpoints that establish the
structural foundation of the College Football ATS Research Platform.
These endpoints provide the authoritative game, team, and conference
data required to construct the master database and support downstream
research workflows.

This revision standardizes endpoint documentation by documenting API
routes, primary keys, foreign-key relationships, API-provided fields,
platform-derived fields, validation expectations, and implementation
status.

------------------------------------------------------------------------

# Canonical Endpoint Template

Every Tier 1 endpoint shall include:

-   Purpose
-   API Route
-   Priority
-   Required Status
-   Primary Parameters
-   Primary Key(s)
-   Foreign-Key Relationships
-   Output File
-   Update Frequency
-   Provided by API
-   Derived by Platform
-   Dependencies
-   Validation
-   Implementation Status
-   Notes

------------------------------------------------------------------------

# Games Endpoint

## API Route

`/games`

## Purpose

Provides the canonical schedule and completed game records used to
construct the master database.

## Priority

Tier 1 --- Required

## Required Status

Mandatory

## Primary Parameters

-   season
-   week
-   seasonType
-   team (optional)

## Primary Key

-   id

## Foreign-Key Relationships

-   homeId → Teams
-   awayId → Teams
-   venueId → Venues (Tier 2)

## Output File

`games_<season>.json`

## Update Frequency

Historical: once. Current season: weekly or as needed.

## Provided by API

Representative fields include: - id - season - week - seasonType -
startDate - completed - neutralSite - conferenceGame - venueId - venue -
homeId - awayId - homeTeam - awayTeam - homePoints - awayPoints -
homeConference - awayConference - excitementIndex

## Derived by Platform

-   ATS Margin
-   Covered
-   Effective Rank
-   Home Favorite
-   Road Underdog
-   Normalized conference-game flag
-   Additional research fields

## Dependencies

Supports the Master Database, Rankings, Betting Lines, Team Records, and
Research Modules.

## Validation

-   Successful API response
-   Unique game IDs
-   Valid team identifiers
-   Required score fields for completed games

## Implementation Status

Planned

## Notes

This endpoint is the canonical foundation for all game-level
relationships.

------------------------------------------------------------------------

# Teams Endpoint

## API Route

`/teams`

## Purpose

Provides the authoritative list of football teams and identifiers.

## Priority

Tier 1 --- Required

## Required Status

Mandatory

## Primary Key

-   id

## Foreign-Key Relationships

Referenced by Games, Records, Rankings, and Betting Lines.

## Output File

`teams.json`

## Update Frequency

Seasonally or when membership changes.

## Provided by API

Team identifiers and metadata.

## Derived by Platform

-   Normalized abbreviations
-   Historical conference mappings
-   Platform reference mappings

## Dependencies

Supports normalization, identifier mapping, and the Master Database.

## Validation

-   Unique team IDs
-   Team names present
-   Required metadata populated

## Implementation Status

Planned

------------------------------------------------------------------------

# Conferences Endpoint

## API Route

`/conferences`

## Purpose

Defines conference identities and metadata.

## Priority

Tier 1 --- Required

## Required Status

Mandatory

## Primary Key

-   API conference identifier (when provided)

## Foreign-Key Relationships

Referenced by Teams, Games, Records, and research modules.

## Output File

`conferences.json`

## Update Frequency

When conference membership changes.

## Provided by API

Conference identifiers and metadata.

## Derived by Platform

-   Historical conference classifications
-   Research groupings
-   Reference mappings

## Dependencies

Supports conference reference tables, conference ATS research, and the
Master Database.

## Validation

-   Unique conference identifiers
-   Valid conference names
-   Active conference records

## Implementation Status

Planned

------------------------------------------------------------------------

# Chapter Summary

The Games, Teams, and Conferences endpoints establish the canonical
structural layer of the platform. Together they define the identifiers
and relationships upon which Rankings, Betting Lines, Team Records,
enrichment datasets, and research modules depend. This standardized
template becomes the model for subsequent endpoint chapters.
