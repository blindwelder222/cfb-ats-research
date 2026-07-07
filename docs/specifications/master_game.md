# Master Game Record Specification
Version: 1.0
Status: Draft
Owner: College Football ATS Research Project

---

# 1. Purpose

The Master Game Record is the canonical representation of a single football game within the research platform.

Every normalization and integration process exists to populate this structure.

The Master Game Record is derived from multiple raw datasets:

- Games
- Betting Lines
- Teams
- Rankings
- Conferences
- Venues

Future datasets may also contribute additional attributes.

---

# 2. Design Principles

The Master Game Record shall adhere to the following principles:

- One game equals one record.
- IDs are authoritative.
- Raw data is never modified.
- Derived fields are clearly identified.
- Every value must have an identifiable source.

---

# 3. Record Identity

Required fields

| Field | Source |
|--------|--------|
| game_id | Games |
| season | Games |
| season_type | Games |
| week | Games |
| start_date | Games |

---

# 4. Team Information

## Home Team

| Field | Source |
|--------|--------|
| home_team_id | Games |
| home_school | Games |
| home_abbreviation | Teams |
| home_conference | Teams |
| home_classification | Teams |

## Away Team

| Field | Source |
|--------|--------|
| away_team_id | Games |
| away_school | Games |
| away_abbreviation | Teams |
| away_conference | Teams |
| away_classification | Teams |

---

# 5. Scores

| Field | Source |
|--------|--------|
| home_points | Games |
| away_points | Games |

Quarter scoring shall remain available from the raw dataset and may be incorporated in future versions.

---

# 6. Betting

| Field | Source |
|--------|--------|
| spread | Betting |
| formatted_spread | Betting |
| over_under | Betting |
| provider | Betting |

Selection of the canonical betting provider is defined separately.

---

# 7. Rankings

| Field | Source |
|--------|--------|
| home_rank | Rankings |
| away_rank | Rankings |
| ranking_source | Rankings |

Rankings shall represent the rankings entering the game.

---

# 8. Venue

| Field | Source |
|--------|--------|
| venue_id | Games |
| venue_name | Venues |
| city | Venues |
| state | Venues |
| latitude | Venues |
| longitude | Venues |

---

# 9. Game Characteristics

| Field | Source |
|--------|--------|
| neutral_site | Games |
| conference_game | Games |
| attendance | Games |
| completed | Games |

---

# 10. Derived Fields

Derived fields are generated during normalization.

Examples include:

- ATS winner
- Straight-up winner
- Favorite
- Underdog
- Margin of victory
- Cover margin
- Total points
- Home win
- Away win

Additional derived metrics may be added without altering raw datasets.

---

# 11. Validation Rules

The normalization pipeline shall validate:

- Unique game IDs.
- Valid team IDs.
- Valid venue IDs.
- Valid conference references.
- Successful betting joins.
- Successful ranking joins.

Any validation failures shall be reported separately.

---

# 12. Future Expansion

The Master Game Record is intentionally extensible.

Future datasets may contribute:

- Weather
- Officials
- Coaching
- Recruiting
- Returning production
- SP+
- Elo
- Injury information
- Transfer portal
- Travel distance

without modifying the existing schema.

---

# 13. Philosophy

The Master Game Record represents a football game, not merely a collection of datasets.

Every integration script should move the project closer to this canonical representation.
