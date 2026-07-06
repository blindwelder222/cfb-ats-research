# College Football ATS Research Platform

# ATS_POLICY.md

**Document Status:** Canonical\
**Lifecycle Status:** Active\
**Version:** 1.0.1\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Canonical Responsibilities

This policy governs:

-   ATS methodology
-   ATS calculations
-   Ranking precedence
-   Research universe defaults
-   Publication thresholds
-   ATS-derived methodology

This policy does **not** define:

-   Database schemas
-   API endpoint behavior
-   Acquisition workflows
-   Research terminology
-   Software implementation

Those responsibilities are delegated to the Constitution, Data
Dictionary, Research Dictionary, Data Acquisition Manual, and API
Endpoint Reference.

------------------------------------------------------------------------

# Purpose

This policy defines the canonical Against the Spread (ATS) methodology
used throughout the College Football ATS Research Platform. All research
modules, datasets, reports, and statistical analyses shall follow this
policy unless a documented exception is approved through
version-controlled revision.

------------------------------------------------------------------------

# Scope

This policy applies to:

-   ATS calculations
-   Master Database research outputs
-   Statistical studies
-   Automated research workflows
-   Published reports

------------------------------------------------------------------------

# Ranking Priority

When multiple ranking systems exist, the effective ranking shall be
determined in the following order:

1.  College Football Playoff (CFP)
2.  Associated Press (AP)
3.  Coaches Poll

The resulting **effective_rank** methodology is defined here. The
canonical field definition resides in the Data Dictionary.

------------------------------------------------------------------------

# ATS Margin

The canonical ATS methodology is:

(home_score - away_score) + spread

Interpretation:

-   ATS Margin \> 0 → Home team covered
-   ATS Margin \< 0 → Away team covered
-   ATS Margin = 0 → Push

The formula is governed by this policy. The field definition is owned by
the Data Dictionary.

------------------------------------------------------------------------

# Covered Indicator

The derived outcome shall be one of:

-   Home
-   Away
-   Push

Terminology is defined in the Research Dictionary.

------------------------------------------------------------------------

# Minimum Publication Standards

Unless explicitly documented otherwise:

-   Minimum 75 lined FBS games for leaderboard studies.

Any exception shall be documented and justified within the published
study.

------------------------------------------------------------------------

# Default Research Universe

Unless explicitly overridden and documented:

-   FBS games only
-   Regular season by default
-   Consensus betting lines when available

Study-specific deviations are permitted when transparently documented.

------------------------------------------------------------------------

# Data Integrity

-   Raw data is never modified.
-   Derived fields are created only in processed or master datasets.
-   Every ATS calculation must be reproducible from preserved source
    data.

------------------------------------------------------------------------

# Living Document Statement

This policy defines the canonical ATS methodology for the College
Football ATS Research Platform and evolves through controlled, versioned
revisions.
