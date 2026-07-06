# College Football ATS Research Platform

# DATASET_CATALOG.md

**Document Status:** Canonical **Lifecycle Status:** Active **Version:**
1.0.0 **Project Phase:** Implementation Planning **Last Updated:**
2026-07-04

------------------------------------------------------------------------

# Purpose

This document is the canonical acquisition planning index for the
platform. It defines every dataset the platform intends to acquire, its
priority, acquisition strategy, and the acquisition job responsible for
retrieving it.

It intentionally does **not** duplicate API documentation.

------------------------------------------------------------------------

# Acquisition Categories

## Reference

Acquired only when required by project changes.

## Seasonal

Acquired once per season for historical completeness.

## Operational

Acquired during the season to keep the Master Database current.

## Derived

Generated internally by the platform and never retrieved directly.

------------------------------------------------------------------------

# Dataset Catalog

  --------------------------------------------------------------------------------
  Dataset       Priority   Category    Planned Job      Primary Source   Status
  ------------- ---------- ----------- ---------------- ---------------- ---------
  Games         Critical   Seasonal    games.py         CFBD             Planned

  Teams         Critical   Seasonal    teams.py         CFBD             Planned

  Conferences   High       Reference   conferences.py   CFBD             Planned

  Rankings      Critical   Seasonal    rankings.py      CFBD             Planned

  Betting Lines Critical   Seasonal    betting.py       CFBD             Planned

  Records       High       Seasonal    records.py       CFBD             Planned

  Team          Medium     Seasonal    stats.py         CFBD             Planned
  Statistics                                                             

  Advanced      Medium     Seasonal    metrics.py       CFBD             Future
  Metrics                                                                

  Recruiting    Low        Seasonal    recruiting.py    CFBD             Future

  Draft         Low        Seasonal    draft.py         CFBD             Future
  --------------------------------------------------------------------------------

------------------------------------------------------------------------

# Dataset Specification Template

Each dataset specification shall document:

-   Purpose
-   Business value
-   Acquisition category
-   Acquisition frequency
-   Official endpoint(s)
-   Required parameters
-   Optional parameters
-   Storage location
-   Archive location
-   Acquisition job
-   Downstream dependencies
-   Estimated API request cost
-   Validation requirements

------------------------------------------------------------------------

# Initial Implementation Order

Sprint 1 - Games

Sprint 2 - Teams - Conferences

Sprint 3 - Rankings - Betting Lines - Records

Sprint 4 - Statistics

Sprint 5 - Advanced Metrics - Recruiting - Draft

------------------------------------------------------------------------

# Immediate Next Deliverables

The following dataset specifications should be created first:

-   GAMES.md
-   TEAMS.md
-   CONFERENCES.md
-   RANKINGS.md
-   BETTING.md

These documents become the implementation contract for each acquisition
job.

------------------------------------------------------------------------

# Living Document Statement

This Dataset Catalog defines the planned acquisition datasets for the
College Football ATS Research Platform and evolves through controlled,
versioned revisions.
