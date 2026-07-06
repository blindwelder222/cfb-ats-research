# Documentation Guide

Welcome to the documentation for the **College Football ATS Research
Platform**.

This repository is organized so that every topic has a single canonical
owner. Before making changes, consult the appropriate document rather
than duplicating definitions or requirements.

------------------------------------------------------------------------

# Where to Start

1.  **SPEC_INDEX.md** --- Overview of the complete documentation system.
2.  **CONSTITUTION.md** --- Project governance and guiding principles.
3.  **MANIFEST.md** --- Vision, objectives, and strategic direction.
4.  **ATS_POLICY.md** --- Canonical ATS methodology.
5.  **DATA_DICT.md** --- Canonical schema and field definitions.
6.  **RESEARCH_DICT.md** --- Research terminology and analytical
    concepts.
7.  **ACQ_MANUAL.md** --- Acquisition workflow and operational behavior.
8.  **API Endpoint Reference** --- External API specifications and
    integration contracts.

------------------------------------------------------------------------

# Documentation Structure

## governance/

Project governance and strategic direction.

-   CONSTITUTION.md
-   MANIFEST.md
-   SPEC_INDEX.md
-   DOC_AUDIT.md
-   ATS_POLICY.md

## specifications/

Technical specifications.

-   DATA_DICT.md
-   RESEARCH_DICT.md
-   ACQ_MANUAL.md
-   API Endpoint Reference

## api/

Detailed endpoint reference chapters.

-   API_CH01.md through API_CH08.md

## reference/

Supporting reference material.

-   API reference exports
-   Team and conference reference tables
-   Other static reference datasets

------------------------------------------------------------------------

# Documentation Principles

-   Each concept has one canonical owner.
-   Documents reference one another rather than redefining content.
-   Changes are version controlled.
-   Repair or enhancement work should be tracked through the
    documentation audit.

------------------------------------------------------------------------

# Recommended Workflow

1.  Review SPEC_INDEX.md.
2.  Identify the canonical owner of the topic.
3.  Update only the owning document.
4.  Commit changes to GitHub.
5.  Verify cross-document consistency.
6.  Update the audit log if responsibilities or terminology changed.

------------------------------------------------------------------------

# Implementation Philosophy

Documentation serves as the implementation specification for the
platform. Code should implement the documented behavior rather than
introducing undocumented behavior.

------------------------------------------------------------------------

# Living Document Statement

This guide introduces the documentation system and should evolve as the
repository grows.
