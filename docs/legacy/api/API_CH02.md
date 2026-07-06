# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH02.md

## Chapter 2 --- Tier 1 Core Endpoints

**Document Status:** Canonical Development Draft\
**Parent Document:** API_ENDPOINT_REFERENCE.md\
**Chapter:** 2 of N\
**Version:** 1.0-draft\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This chapter documents the Tier 1 endpoints that form the foundation of
the College Football ATS Research Platform. These endpoints are required
to construct the master database and support nearly every downstream
research workflow.

------------------------------------------------------------------------

# Tier 1 Overview

Tier 1 endpoints are considered essential because they define the games,
teams, conferences, rankings, and betting information used throughout
the platform.

Characteristics:

-   Required for master database construction.
-   Downloaded automatically through GitHub Actions.
-   Archived in raw form.
-   Validated before processing.
-   Used by multiple downstream datasets.

------------------------------------------------------------------------

# Endpoint Specification Template

Each Tier 1 endpoint follows the same specification:

-   Purpose
-   Priority
-   Primary Parameters
-   Output File
-   Update Frequency
-   Dependencies
-   Validation Expectations
-   Implementation Status

------------------------------------------------------------------------

# Games Endpoint

## Purpose

Provides the canonical game schedule and final results used to construct
the master database.

## Priority

Tier 1 --- Required

## Typical Parameters

-   season
-   week
-   seasonType
-   team (optional)

## Output File

games\_`<season>`{=html}.json

## Update Frequency

-   Historical seasons: once
-   Current season: weekly or as needed

## Dependencies

Supports:

-   Master database
-   Score calculations
-   Opponent relationships
-   Research modules

## Validation

Verify:

-   Successful response
-   Expected game count
-   Unique game identifiers
-   Required score fields

## Implementation Status

Planned

------------------------------------------------------------------------

# Teams Endpoint

## Purpose

Provides the canonical list of FBS teams and associated identifiers.

## Priority

Tier 1 --- Required

## Output File

teams.json

## Update Frequency

Seasonally or when membership changes.

## Dependencies

Supports team normalization and identifier mapping.

## Validation

-   Unique team IDs
-   Team names present
-   Required metadata populated

## Implementation Status

Planned

------------------------------------------------------------------------

# Conferences Endpoint

## Purpose

Defines conference membership and identifiers used throughout the
platform.

## Priority

Tier 1 --- Required

## Output File

conferences.json

## Update Frequency

As conference alignment changes.

## Dependencies

Conference reference tables and conference-based research.

## Validation

-   Unique conference IDs
-   Valid conference names
-   Active conference records

## Implementation Status

Planned

------------------------------------------------------------------------

# Chapter Summary

Games, Teams, and Conferences form the structural backbone of the master
database. Subsequent chapters document additional Tier 1 endpoints,
including rankings and betting data, which enrich these core records for
ATS research.
