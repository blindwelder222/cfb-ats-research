# College Football ATS Research Platform

# DATA_DICTIONARY.md

**Document Status:** Canonical\
**Version:** 1.0\
**Project Phase:** Foundation Migration\
**Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This document defines the canonical schema for the College Football ATS
Research Platform. Every field in the master database shall be
documented here before use.

------------------------------------------------------------------------

# Field Definitions

  ----------------------------------------------------------------------------
  Field              Type         Source           Description
  ------------------ ------------ ---------------- ---------------------------
  season             Integer      API              Season in which the game
                                                   was played.

  game_id            Integer      API              Unique game identifier.

  game_date          Date         API              Official game date.

  week               Integer      API              Regular season or
                                                   postseason week number.

  home_team          String       API              Home team name.

  away_team          String       API              Away team name.

  home_score         Integer      API              Final home score.

  away_score         Integer      API              Final away score.

  team_id            Integer      API              Unique team identifier.

  conference_id      Integer      Reference        Unique conference
                                                   identifier.

  consensus_spread   Float        Betting          Consensus point spread.

  opening_spread     Float        Betting          Opening betting line.

  closing_spread     Float        Betting          Closing betting line.

  line_movement      Float        Calculated       Closing spread minus
                                                   opening spread.

  ats_margin         Float        Calculated       (home_score - away_score) +
                                                   spread

  covered            Enum         Calculated       Home, Away, or Push.

  push               Boolean      Calculated       True if ATS Margin equals
                                                   zero.

  cfp_rank           Integer      API              College Football Playoff
                                                   ranking.

  ap_rank            Integer      API              Associated Press ranking.

  coaches_rank       Integer      API              Coaches Poll ranking.

  effective_rank     Integer      Calculated       CFP \> AP \> Coaches
                                                   ranking priority.
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

# Planned Fields

The following fields are expected to become part of future versions of
the master database:

-   head_coach_id
-   stadium_id
-   conference_game
-   ranked_matchup
-   fbs_vs_fcs
-   neutral_site
-   overtime
-   weather_id

These fields are documented as planned but are not yet required by
Version 1.0.

------------------------------------------------------------------------

# Data Integrity

-   Every field must have a documented source.
-   Calculated fields shall be reproducible from stored data.
-   Raw API fields are never modified.
-   Changes to field definitions require a version-controlled revision.

------------------------------------------------------------------------

# Living Document Statement

This Data Dictionary is the authoritative schema reference for the
College Football ATS Research Platform and will evolve as new
capabilities are introduced while preserving complete version history.
