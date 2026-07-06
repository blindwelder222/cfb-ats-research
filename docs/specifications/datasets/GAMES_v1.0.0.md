# College Football ATS Research Platform

# GAMES.md

**Document Status:** Canonical\
**Lifecycle Status:** Active\
**Version:** 1.0.0\
**Project Phase:** Implementation Planning\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Purpose

The Games dataset is the foundational dataset for the College Football
ATS Research Platform. Nearly every downstream process depends on
complete and reproducible game records.

------------------------------------------------------------------------

# Business Value

This dataset provides the canonical historical schedule and game results
used to build the Master Database.

Priority: **Critical**

------------------------------------------------------------------------

# Acquisition Category

**Seasonal**

Historical acquisition is performed one season at a time. Operational
acquisition updates the current season after games are completed.

------------------------------------------------------------------------

# Primary Source

-   CollegeFootballData (CFBD)

The API Endpoint Reference is the canonical owner of endpoint details.
This document defines how the Platform uses the Games dataset.

------------------------------------------------------------------------

# Acquisition Job

**Job:** `src/acquisition/jobs/games.py`

Responsibilities:

-   Retrieve one season of FBS games.
-   Archive raw JSON without modification.
-   Record acquisition in the manifest.
-   Log success or failure.
-   Never overwrite archived raw data.

------------------------------------------------------------------------

# Required Inputs

-   Season (required)

------------------------------------------------------------------------

# Optional Inputs

-   Week
-   Season Type
-   Team
-   Conference

These are primarily intended for operational or targeted acquisitions.

------------------------------------------------------------------------

# Storage

Raw Archive:

`data/raw/games/<season>/`

Processed Output:

`data/processed/games/`

Master Database:

Loaded during the database build phase.

------------------------------------------------------------------------

# Downstream Dependencies

-   Validation
-   Normalization
-   Master Database
-   ATS calculations
-   Research modules
-   Reporting

------------------------------------------------------------------------

# Estimated API Cost

Historical acquisition:

Approximately one complete season per acquisition job.

Operational acquisition:

As needed during the season.

Actual request counts should be measured and documented during
implementation.

------------------------------------------------------------------------

# Validation Requirements

Before a season is marked complete:

-   JSON successfully archived.
-   Response validated.
-   Manifest updated.
-   Acquisition log written.
-   No duplicate archive created.

------------------------------------------------------------------------

# Definition of Done

The Games dataset is complete when:

-   The requested season has been archived.
-   Validation passes.
-   The manifest records successful completion.
-   The dataset is available for normalization.

------------------------------------------------------------------------

# Living Document Statement

This document defines the implementation contract for the Games dataset
and evolves through controlled, versioned revisions.
