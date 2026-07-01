# College Football ATS Research Platform

# DATA_ACQUISITION_MANUAL.md

**Document Status:** Canonical\
**Version:** 1.0\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This manual defines the official process for acquiring data used by the
College Football ATS Research Platform. It establishes the standards for
downloading, storing, validating, and preserving source data so that
every master database build is reproducible.

------------------------------------------------------------------------

# Design Principles

-   Automate whenever practical.
-   Preserve every raw response.
-   Never modify raw source files.
-   Make every build reproducible.
-   Validate before processing.

------------------------------------------------------------------------

# Primary Data Source

The primary source of game and team information is the
CollegeFootballData API.

Additional reference datasets (conference history, coaches, rankings,
and metadata) may be incorporated as documented reference sources.

------------------------------------------------------------------------

# Acquisition Pipeline

1.  Acquire data from approved sources.
2.  Archive the unmodified raw response.
3.  Validate structure and completeness.
4.  Transform into processed datasets.
5.  Build the master database.
6.  Execute research modules.

------------------------------------------------------------------------

# Repository Data Flow

    data/
      raw/
      processed/
      reference/
      master/

Raw data is immutable. All transformations occur downstream.

------------------------------------------------------------------------

# Automation Standard

GitHub Actions is the preferred execution environment.

Automated workflows may:

-   Download API data
-   Validate responses
-   Archive raw files
-   Build processed datasets
-   Generate the master database
-   Publish research artifacts

------------------------------------------------------------------------

# Validation Requirements

Every acquisition run should verify:

-   Successful API responses
-   Expected schema
-   Required fields
-   Consistent file naming
-   File integrity

Failures should stop downstream processing until corrected.

------------------------------------------------------------------------

# Rebuild Standard

The project shall be fully reproducible from:

-   Repository documentation
-   Reference datasets
-   Archived raw data
-   Processing scripts

------------------------------------------------------------------------

# Living Document Statement

This manual defines the canonical acquisition process for the College
Football ATS Research Platform and shall evolve through
version-controlled revisions.
