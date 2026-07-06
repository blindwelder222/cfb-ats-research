# College Football ATS Research Platform

# DATA_DICT.md

**Document Status:** Canonical\
**Lifecycle Status:** Active\
**Version:** 1.0.1\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-07-04

------------------------------------------------------------------------

# Canonical Responsibilities

This Data Dictionary governs:

-   Canonical field definitions
-   Data types
-   Field lifecycle classification
-   Source classification
-   Primary and foreign key definitions
-   Nullability expectations
-   Schema evolution

This Data Dictionary does **not** define:

-   ATS methodology
-   API acquisition behavior
-   Acquisition workflows
-   Research terminology
-   Software implementation

Those responsibilities are delegated to the ATS Policy, API Endpoint
Reference, Data Acquisition Manual, and Research Dictionary.

------------------------------------------------------------------------

# Purpose

This document is the canonical schema specification for the College
Football ATS Research Platform.

------------------------------------------------------------------------

# Canonical Source Classification

-   **CFBD API**
-   **Reference Dataset**
-   **External Source**
-   **Platform Derived**

------------------------------------------------------------------------

# Field Definitions

  -------------------------------------------------------------------------------------------------------
  Field              Type       Source      Lifecycle   Owner          Key               Description
  ------------------ ---------- ----------- ----------- -------------- ----------------- ----------------
  season             Integer    CFBD API    Raw         Data           ---               Season
                                                        Dictionary                       identifier

  game_id            Integer    CFBD API    Raw         Data           Primary           Unique game
                                                        Dictionary                       identifier

  team_id            Integer    CFBD API    Raw         Data           Primary/Foreign   Canonical team
                                                        Dictionary                       identifier

  conference_id      Integer    Reference   Reference   Data           Foreign           Canonical
                                Dataset                 Dictionary                       conference
                                                                                         identifier

  consensus_spread   Float      External    Raw         Data           ---               Consensus
                                Source                  Dictionary                       betting spread

  line_movement      Float      Platform    Derived     Data           ---               Closing minus
                                Derived                 Dictionary                       opening spread

  ats_margin         Float      Platform    Derived     ATS Policy     ---               Canonical ATS
                                Derived                 (method), Data                   margin
                                                        Dictionary                       
                                                        (definition)                     

  covered            Enum       Platform    Derived     ATS Policy     ---               Home, Away, or
                                Derived                 (method), Data                   Push
                                                        Dictionary                       
                                                        (definition)                     

  effective_rank     Integer    Platform    Derived     ATS Policy     ---               CFP→AP→Coaches
                                Derived                 (method), Data                   precedence
                                                        Dictionary                       
                                                        (definition)                     
  -------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# Planned Fields

  Field           Planned Version   Expected Source
  --------------- ----------------- -------------------
  head_coach_id   1.1               Reference Dataset
  stadium_id      1.1               CFBD API
  weather_id      Future            External Source

------------------------------------------------------------------------

# Data Integrity

-   Every field shall have a documented source.
-   Every derived field shall reference its governing methodology.
-   Raw fields remain immutable.
-   Schema revisions require version-controlled updates.

------------------------------------------------------------------------

# Living Document Statement

This Data Dictionary is the **canonical** schema specification for the
College Football ATS Research Platform and evolves through controlled,
versioned revisions.
