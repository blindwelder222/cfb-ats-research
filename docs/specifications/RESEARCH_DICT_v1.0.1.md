# College Football ATS Research Platform

# RESEARCH_DICT.md

**Document Status:** Canonical\
**Lifecycle Status:** Active\
**Version:** 1.0.1\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Canonical Responsibilities

This Research Dictionary governs:

-   Research terminology
-   Statistical definitions
-   Analytical concepts
-   Publication terminology
-   Standard abbreviations

This Research Dictionary does **not** define:

-   Database fields
-   ATS calculation methodology
-   API behavior
-   Acquisition workflows
-   Software implementation

Those responsibilities are delegated to the Data Dictionary, ATS Policy,
API Endpoint Reference, Data Acquisition Manual, and Constitution.

------------------------------------------------------------------------

# Purpose

This document is the canonical terminology reference for the College
Football ATS Research Platform. It defines the concepts and vocabulary
used throughout the project while avoiding duplication of field
definitions or implementation details.

------------------------------------------------------------------------

# Standard Abbreviations

-   ATS --- Against the Spread
-   FBS --- Football Bowl Subdivision
-   FCS --- Football Championship Subdivision
-   CFP --- College Football Playoff
-   AP --- Associated Press Poll
-   SOS --- Strength of Schedule
-   SOR --- Strength of Record

------------------------------------------------------------------------

# Canonical Research Terms

## ATS Margin

**Definition**

The numerical result used to determine whether the betting spread was
covered.

**Related Canonical Documents**

-   Formula --- ATS Policy
-   Field (`ats_margin`) --- Data Dictionary

------------------------------------------------------------------------

## Effective Ranking

**Definition**

The standardized ranking used by the Platform according to the approved
ranking precedence.

**Related Canonical Documents**

-   Methodology --- ATS Policy
-   Field (`effective_rank`) --- Data Dictionary

------------------------------------------------------------------------

## Conference Game

**Definition**

A game played between members of the same conference according to the
official conference alignment for that season.

**Related Canonical Documents**

-   Field --- Data Dictionary
-   Acquisition --- API Endpoint Reference

------------------------------------------------------------------------

## Sample Size

The number of qualifying observations included in a statistical
analysis.

------------------------------------------------------------------------

## Statistical Significance

Evidence that an observed result is unlikely to be explained by random
variation alone.

------------------------------------------------------------------------

## Selection Bias

Systematic distortion introduced by non-representative data selection.

------------------------------------------------------------------------

## Survivorship Bias

Bias introduced by considering only successful or remaining observations
while ignoring excluded data.

------------------------------------------------------------------------

## Regression to the Mean

The tendency for unusually high or low results to move toward long-term
averages over time.

------------------------------------------------------------------------

# Documentation Principles

-   Concepts are defined here.
-   Field definitions belong in the Data Dictionary.
-   Formulas belong in the ATS Policy.
-   Acquisition terminology belongs in the API Endpoint Reference and
    Data Acquisition Manual.

------------------------------------------------------------------------

# Living Document Statement

This Research Dictionary is the canonical terminology reference for the
College Football ATS Research Platform and evolves through controlled,
versioned revisions.
