# College Football ATS Research Platform

# REPO_STRUCTURE.md

**Document Status:** Canonical **Lifecycle Status:** Active **Version:**
1.0.0 **Project Phase:** Foundation Migration **Last Updated:**
2026-07-04

------------------------------------------------------------------------

# Purpose

This document defines the canonical repository organization for the
College Football ATS Research Platform. It specifies where files belong
and the responsibility of each top-level directory.

------------------------------------------------------------------------

# Top-Level Structure

-   docs/ --- Canonical documentation and specifications.
-   config/ --- Configuration files for APIs, databases, logging, and
    research.
-   src/ --- Production source code.
-   tests/ --- Automated tests mirroring the source tree.
-   data/ --- Raw, processed, master, reference, and export datasets.
-   reports/ --- Generated research reports and figures.
-   notebooks/ --- Exploratory notebooks and one-off analyses.
-   scripts/ --- Utility and maintenance scripts.
-   sandbox/ --- Experimental prototypes and proof-of-concepts.
-   archive/ --- Historical or deprecated artifacts retained for
    reference.

------------------------------------------------------------------------

# Directory Responsibilities

## docs/

Contains only maintained documentation. All specifications, governance
documents, API references, and reference material belong here.

## src/

Contains production code only. Experimental code belongs in sandbox/.

## data/

Raw data is immutable. Processed and master datasets are generated from
raw data. Reference datasets are maintained separately.

## tests/

Mirrors the src/ package layout to simplify navigation and coverage.

## reports/

Contains generated outputs, never canonical specifications.

------------------------------------------------------------------------

# Placement Rules

-   Every file should have one logical home.
-   Avoid duplicate copies of canonical documents.
-   Reference documents rather than copying their content.
-   Experimental work graduates from sandbox/ into src/ only after
    validation.

------------------------------------------------------------------------

# Recommended Growth

Future additions such as web applications, mobile clients, analytics
modules, or machine learning models should receive dedicated top-level
directories only when they become substantial components.

------------------------------------------------------------------------

# Living Document Statement

This document defines the canonical repository organization and evolves
through controlled, versioned revisions.
