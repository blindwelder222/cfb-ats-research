# College Football ATS Research Platform

# ATS_POLICY.md

**Document Status:** Canonical\
**Version:** 1.0\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This document defines the official Against the Spread (ATS) methodology
used throughout the College Football ATS Research Platform. All research
modules, datasets, reports, and statistical analyses shall follow this
policy unless a documented exception is approved through a
version-controlled revision.

------------------------------------------------------------------------

# Scope

This policy applies to:

-   Master database construction
-   ATS calculations
-   Research studies
-   Automated workflows
-   Published reports

------------------------------------------------------------------------

# Ranking Priority

When multiple ranking systems exist, the official ranking used by the
platform shall be:

1.  College Football Playoff (CFP)
2.  Associated Press (AP)
3.  Coaches Poll

The first available ranking becomes the **effective_rank**.

------------------------------------------------------------------------

# ATS Margin

The official ATS Margin formula is:

    (home_score - away_score) + spread

Interpretation:

-   ATS Margin \> 0 → Home team covered
-   ATS Margin \< 0 → Away team covered
-   ATS Margin = 0 → Push

This formula is the canonical definition used throughout the project.

------------------------------------------------------------------------

# Covered Indicator

The `covered` field shall contain one of:

-   Home
-   Away
-   Push

Derived directly from the ATS Margin.

------------------------------------------------------------------------

# Minimum Sample Size

Unless explicitly noted otherwise, leaderboards and published research
require:

-   Minimum 75 lined FBS games

Studies below this threshold must clearly identify their limited sample
size.

------------------------------------------------------------------------

# Research Universe

Unless a study specifies otherwise:

-   FBS games only
-   Regular season by default
-   Consensus betting lines when available

Any deviation must be documented in the study.

------------------------------------------------------------------------

# Data Integrity

-   Raw data is never modified.
-   Derived fields are created only in processed or master datasets.
-   Every ATS calculation must be reproducible from stored source data.

------------------------------------------------------------------------

# Amendments

Changes to this policy require a documented revision committed to the
repository. Historical versions shall remain available through version
control.
