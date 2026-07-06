# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH04.md

## Chapter 4 --- Tier 1 Integration and Acquisition Contracts

**Document Status:** Canonical Development Draft\
**Parent Document:** API_ENDPOINT_REFERENCE.md\
**Chapter:** 4 of 8\
**Version:** 1.1-draft\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Purpose

This chapter defines how Tier 1 endpoints are integrated into the
acquisition pipeline. Whereas Chapters 2 and 3 describe the structure of
the data and the supporting operational endpoints, this chapter
documents the rules governing acquisition order, endpoint dependencies,
validation, and loading into the master database.

------------------------------------------------------------------------

# Integration Philosophy

Tier 1 endpoints are acquired as a coordinated unit rather than as
isolated downloads.

Objectives:

-   Preserve referential integrity.
-   Ensure reproducible database builds.
-   Archive immutable raw JSON.
-   Detect incomplete or failed acquisitions early.
-   Support both historical rebuilds and in-season incremental updates.

------------------------------------------------------------------------

# Recommended Acquisition Order

1.  Calendar
2.  Conferences
3.  Teams
4.  Games
5.  Records
6.  Scoreboard (active season only)

Each stage provides reference data required by subsequent stages.

------------------------------------------------------------------------

# Endpoint Integration Contracts

## Calendar

### Role

Establishes season boundaries and acquisition windows.

### Downstream Consumers

-   Acquisition scheduler
-   Pipeline controller
-   Validation engine

### Validation Gate

Season calendar must be available before acquisition begins.

------------------------------------------------------------------------

## Conferences

### Role

Provides canonical conference references.

### Downstream Consumers

-   Teams
-   Games
-   Conference research
-   Historical normalization

### Validation Gate

Conference identities must be unique and internally consistent.

------------------------------------------------------------------------

## Teams

### Role

Defines canonical team identifiers used across the platform.

### Downstream Consumers

-   Games
-   Records
-   Rankings
-   Betting data
-   Research modules

### Validation Gate

Every referenced team identifier must resolve to a valid team.

------------------------------------------------------------------------

## Games

### Role

Acts as the central integration table for game-level research.

### Downstream Consumers

-   Betting Lines
-   Rankings
-   Team Records
-   ATS Engine
-   Master Database

### Validation Gate

Games cannot be promoted into the master database until required
identifiers and completed-game data pass validation.

------------------------------------------------------------------------

## Records

### Role

Provides historical validation and longitudinal context.

### Downstream Consumers

-   Team summaries
-   Conference summaries
-   Trend analysis

### Validation Gate

Records must reconcile with normalized team references.

------------------------------------------------------------------------

## Scoreboard

### Role

Supports operational monitoring during active seasons.

### Downstream Consumers

-   Refresh queue
-   Acquisition monitoring
-   Completeness validation

### Validation Gate

Operational only; historical rebuilds should rely on finalized Games
data.

------------------------------------------------------------------------

# Historical Build vs. Incremental Update

## Historical Build

-   Complete seasonal acquisition.
-   Immutable raw archive.
-   Full validation before loading.

## Incremental Update

-   Acquire current-season changes.
-   Refresh affected records only.
-   Revalidate dependent datasets.

------------------------------------------------------------------------

# Master Database Loading

Tier 1 data shall be promoted to the master database only after:

-   Required endpoints acquired.
-   Validation completed successfully.
-   Foreign-key relationships resolved.
-   Duplicate detection complete.
-   Acquisition log recorded.

------------------------------------------------------------------------

# Failure Handling

The acquisition pipeline shall:

-   Halt on critical validation failures.
-   Log endpoint-specific errors.
-   Preserve raw API responses.
-   Support restart from the last successful checkpoint.

------------------------------------------------------------------------

# Chapter Summary

This chapter defines the integration contracts that transform individual
CFBD endpoints into a coordinated acquisition system. Together with
Chapters 2 and 3, it establishes the structural, operational, and
integration foundations of the College Football ATS Research Platform,
providing a reproducible specification for future implementation.
