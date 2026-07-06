# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH03.md

## Chapter 3 --- Tier 1 Supporting Endpoints

**Document Status:** Canonical Development Draft\
**Parent Document:** API_ENDPOINT_REFERENCE.md\
**Chapter:** 3 of 8\
**Version:** 1.1-draft\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Purpose

This chapter documents the Tier 1 supporting endpoints that enrich and
validate the core game dataset. While Chapter 2 establishes the
structural foundation, these endpoints provide season context, records,
calendars, scoreboards, and supporting metadata required for
acquisition, validation, and downstream research.

------------------------------------------------------------------------

# Data Lineage

CFBD API

↓

Raw JSON Archive

↓

Normalization Pipeline

↓

Master Database

↓

Research Modules

Each endpoint documented below participates in this acquisition
pipeline.

------------------------------------------------------------------------

# Canonical Endpoint Template

Each endpoint documents:

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

# Records Endpoint

## API Route

`/records`

## Purpose

Provides historical team and conference record summaries used for
validation and longitudinal research.

## Priority

Tier 1 --- Supporting

## Required Status

Required

## Primary Parameters

-   year
-   team (optional)
-   conference (optional)

## Primary Key

Composite: season + team

## Foreign-Key Relationships

-   teamId → Teams
-   conference → Conferences

## Output File

`records_<season>.json`

## Update Frequency

Seasonally

## Provided by API

Season record information, win/loss statistics, conference records, and
related metadata.

## Derived by Platform

-   ATS win percentage
-   Historical trend classifications
-   Research aggregates

## Dependencies

Teams, Conferences, Games

## Validation

-   Valid season
-   Valid team mappings
-   No duplicate season/team combinations

## Implementation Status

Planned

------------------------------------------------------------------------

# Calendar Endpoint

## API Route

`/calendar`

## Purpose

Defines the official season calendar used to coordinate acquisition
scheduling and season boundaries.

## Priority

Tier 1 --- Supporting

## Required Status

Required

## Primary Parameters

-   year

## Primary Key

Season year

## Output File

`calendar_<season>.json`

## Update Frequency

Annually

## Provided by API

Season milestones, week structure, and calendar dates.

## Derived by Platform

-   Acquisition schedule
-   Pipeline checkpoints
-   Season state tracking

## Dependencies

Acquisition Pipeline

## Validation

Verify complete season calendar before acquisition begins.

## Implementation Status

Planned

------------------------------------------------------------------------

# Scoreboard Endpoint

## API Route

`/scoreboard`

## Purpose

Provides a near real-time snapshot of current games for operational
monitoring during active seasons.

## Priority

Tier 1 --- Operational

## Required Status

Optional for historical rebuilds; recommended during active seasons.

## Primary Parameters

-   classification
-   week (when applicable)

## Primary Key

Game identifier

## Foreign-Key Relationships

Games.id

## Output File

`scoreboard_current.json`

## Update Frequency

During active season

## Provided by API

Current game state, scores, status, and scheduling information.

## Derived by Platform

-   Acquisition completeness checks
-   Refresh queue generation
-   Live validation metrics

## Dependencies

Games

## Validation

Compare scoreboard results against Games endpoint after completion.

## Implementation Status

Future operational use

------------------------------------------------------------------------

# Chapter Summary

The endpoints in this chapter provide operational context that
complements the structural data acquired in Chapter 2. Together they
improve acquisition reliability, establish season boundaries, validate
historical completeness, and provide the supporting metadata necessary
for downstream normalization, database integrity, and ATS research.
