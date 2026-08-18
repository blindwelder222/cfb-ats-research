# Master Game Record Specification
Version: 1.1
Status: Phase 1 Baseline
Owner: College Football ATS Research Project

---

# 1. Purpose

The Master Game Record is the canonical representation of a single football
game within the research platform.

Every normalization and integration process exists to populate or support
this structure.

The Phase 1 Master Game Record is derived from:

- Games
- Teams
- Betting data
- Betting consensus
- Rankings
- Venues
- Venue timezone data

Future datasets may contribute additional attributes.

---

# 2. Design Principles

The Master Game Record shall adhere to the following principles:

- One game equals one record.
- `game_id` is the authoritative game identity.
- IDs are authoritative for relationships.
- Raw data is never modified.
- Derived fields are clearly identified.
- Every value must have an identifiable source.
- Enrichment processes must not change the game population.
- Missing source values shall remain missing rather than being silently
  inferred.
- Reference data and game-level derived data should remain distinguishable.

---

# 3. Record Identity

| Field | Source |
|--------|--------|
| game_id | Games |
| season | Games |
| season_type | Games |
| week | Games |
| start_date | Games |

`start_date` is preserved as the source game timestamp.

---

# 4. Team Information

## Home Team

| Field | Source |
|--------|--------|
| home_team_id | Games |
| home_team | Games |
| home_abbreviation | Teams |
| home_conference | Teams |
| home_classification | Teams |

## Away Team

| Field | Source |
|--------|--------|
| away_team_id | Games |
| away_team | Games |
| away_abbreviation | Teams |
| away_conference | Teams |
| away_classification | Teams |

---

# 5. Scores

| Field | Source |
|--------|--------|
| home_points | Games |
| away_points | Games |

Quarter scoring remains available from the raw game data and is outside the
Phase 1 Master Game Record.

---

# 6. Game Characteristics

| Field | Source |
|--------|--------|
| neutral_site | Games |
| conference_game | Games |
| attendance | Games |
| completed | Games |

---

# 7. Betting

The Phase 1 betting model uses market consensus rather than selecting a
single sportsbook as the canonical provider.

## Consensus Spread

| Field | Source |
|--------|--------|
| spread_provider_count | Betting |
| consensus_spread | Betting consensus |
| spread_mean | Betting |
| spread_median | Betting |
| spread_min | Betting |
| spread_max | Betting |
| spread_range | Betting |
| spread_stddev | Betting |

## Opening Spread

| Field | Source |
|--------|--------|
| spread_open_provider_count | Betting |
| consensus_spread_open | Betting consensus |
| spread_open_mean | Betting |
| spread_open_median | Betting |
| spread_open_min | Betting |
| spread_open_max | Betting |
| spread_open_range | Betting |
| spread_open_stddev | Betting |

## Consensus Total

| Field | Source |
|--------|--------|
| total_provider_count | Betting |
| consensus_total | Betting consensus |
| total_mean | Betting |
| total_median | Betting |
| total_min | Betting |
| total_max | Betting |
| total_range | Betting |
| total_stddev | Betting |

## Opening Total

| Field | Source |
|--------|--------|
| total_open_provider_count | Betting |
| consensus_total_open | Betting consensus |
| total_open_mean | Betting |
| total_open_median | Betting |
| total_open_min | Betting |
| total_open_max | Betting |
| total_open_range | Betting |
| total_open_stddev | Betting |

## Betting Availability

| Field | Source |
|--------|--------|
| betting_available | Betting |

The Phase 1 record does not designate one sportsbook as the canonical
provider. Provider-level observations remain available in the betting data.

---

# 8. Rankings

| Field | Source |
|--------|--------|
| home_rank | Rankings |
| away_rank | Rankings |
| home_rank_source | Rankings |
| away_rank_source | Rankings |
| home_rank_available | Rankings |
| away_rank_available | Rankings |

Rankings represent the ranking applicable when the game was played.

For regular-season games, the ranking corresponding to the game's CFBD week is
used. Week 1 represents the preseason ranking and also applies to Week 0 games
when Week 0 games are present.

For postseason games, the final available regular-season ranking is used.
Postseason ranking records published after the postseason are not used as
entering-game rankings.

The effective ranking follows the project precedence policy:

1. CFP
2. AP
3. Coaches Poll

---

# 9. Venue

## Venue Identity

| Field | Source |
|--------|--------|
| venue_id | Games |
| venue | Games |
| venue_name | Venues |
| city | Venues |
| state | Venues |
| latitude | Venues |
| longitude | Venues |

Where the game source supplies the venue name directly, that source value is
preserved. The normalized venue reference dataset provides the canonical venue
attributes.

## Venue Characteristics

| Field | Source |
|--------|--------|
| capacity | Venues |
| grass | Venues |
| dome | Venues |
| country_code | Venues |
| elevation | Venues |
| construction_year | Venues |

These venue-level attributes are retained as reference data and may be
incorporated into future game-level analyses.

---

# 10. Venue Time and Local Kickoff

The source `start_date` is preserved. A localized kickoff timestamp is derived
using the venue timezone.

| Field | Source |
|--------|--------|
| venue_timezone | Venues / documented resolution |
| venue_timezone_source | Derived metadata |
| venue_local_start_date | Derived |
| venue_local_time_available | Derived |

Timezone precedence:

1. CFBD venue timezone when supplied.
2. Explicitly documented venue resolution when CFBD timezone is absent.

Timezone values shall use IANA timezone identifiers.

No Day/Evening/Night classification is part of the Phase 1 canonical record.
Such classifications, if needed, shall be defined as separate research
variables.

---

# 11. Phase 1 Derived Fields

Derived fields are generated during normalization or game-level enrichment.

Examples include:

- consensus betting values
- venue-local kickoff timestamp
- ranking availability indicators

Research metrics may later include:

- ATS winner
- straight-up winner
- favorite
- underdog
- margin of victory
- cover margin
- total points
- home win
- away win

Derived metrics shall not modify the raw source datasets.

---

# 12. Phase 1 Validation Rules

The Phase 1 normalization and integration pipeline shall validate:

- Unique game IDs.
- Preservation of the game population through joins.
- Valid team IDs.
- Valid venue IDs.
- Valid conference references where applicable.
- Betting joins without unintended row multiplication.
- Ranking joins without unintended row multiplication.
- Venue joins without unintended row multiplication.
- Valid venue timezone resolution for games requiring local time.
- Valid localized kickoff timestamps.
- Documented handling of source-data exceptions.

Any validation failures shall be reported separately.

---

# 13. Phase 1 Scope

Phase 1 establishes the reproducible game-level research foundation for the
2016–2025 dataset.

The Phase 1 baseline includes:

- Games
- Teams
- Betting
- Betting consensus
- Rankings
- Venues
- Venue timezone
- Venue-local kickoff time

Coaching is intentionally excluded from the Phase 1 Master Game Record.

The CFBD coach reference dataset has been acquired for investigation, but it
does not provide a sufficiently reliable game-level head-coach relationship
for the Phase 1 canonical join. Coaching is therefore deferred to Phase 2.

---

# 14. Phase 2 and Future Expansion

Future datasets may contribute:

- Coaching
- Weather
- Officials
- Recruiting
- Returning production
- SP+
- Elo
- Injury information
- Transfer portal
- Travel distance
- Additional research-specific variables

Phase 2 integrations must preserve the Phase 1 game identity and must not
silently alter established Phase 1 values.

---

# 15. Philosophy

The Master Game Record represents a football game, not merely a collection of
datasets.

Every integration script should move the project closer to this canonical
representation while preserving source provenance, reproducibility, and
one-game-one-record integrity.

Phase 1 is considered frozen when the documented specification and validated
implementation agree.
