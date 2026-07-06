# College Football ATS Research Platform

# ACQ_MANUAL.md

**Document Status:** Canonical\
**Lifecycle Status:** Active\
**Version:** 1.0.1\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Canonical Responsibilities

This manual governs:

-   Acquisition workflow
-   Pipeline stages
-   Scheduling strategy
-   Validation workflow
-   Retry and recovery procedures
-   Operational lifecycle

This manual does **not** define:

-   API endpoint specifications
-   Database field definitions
-   ATS methodology
-   Research terminology
-   Project governance

Those responsibilities are delegated to the API Endpoint Reference, Data
Dictionary, Research Dictionary, ATS Policy, and Constitution.

------------------------------------------------------------------------

# Purpose

This document defines the canonical acquisition workflow for the College
Football ATS Research Platform.

------------------------------------------------------------------------

# Canonical Acquisition Pipeline

1.  Acquire
2.  Archive Raw JSON
3.  Validate
4.  Normalize
5.  Load Master Database
6.  Execute Research Modules

The API Endpoint Reference defines **what** is acquired. This manual
defines **how** acquisition is performed.

------------------------------------------------------------------------

# Pipeline States

-   Pending
-   Acquiring
-   Archived
-   Validated
-   Normalized
-   Loaded
-   Complete
-   Failed

------------------------------------------------------------------------

# Data Lineage

External Source

↓

Raw JSON Archive

↓

Validation

↓

Normalization

↓

Master Database

↓

Research Modules

↓

Reports

------------------------------------------------------------------------

# Validation Requirements

-   Required source files present.
-   Referential integrity verified.
-   Duplicate detection completed.
-   Required field validation passed.
-   Acquisition log recorded.

------------------------------------------------------------------------

# Retry Strategy

-   Retry transient failures.
-   Use progressive backoff.
-   Preserve failed responses.
-   Escalate persistent failures.
-   Never overwrite archived raw data.

------------------------------------------------------------------------

# Failure Handling

-   Network failures
-   API response failures
-   Validation failures
-   Duplicate conflicts
-   Schema mismatches

All failures shall be logged for reproducibility.

------------------------------------------------------------------------

# Operational Principles

-   Preserve immutable raw data.
-   Validate before normalization.
-   Normalize before loading.
-   Version operational procedures.

------------------------------------------------------------------------

# Living Document Statement

This Data Acquisition Manual defines the canonical acquisition workflow
for the College Football ATS Research Platform and evolves through
controlled, versioned revisions.
