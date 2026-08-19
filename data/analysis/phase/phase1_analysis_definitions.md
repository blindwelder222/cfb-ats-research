# Phase 1 Exploratory Analysis — Calculation Definitions
Version: 1.0
Status: Working Analysis Specification
Scope: 2016–2025 Phase 1 Master Dataset

---

## 1. Purpose

This document establishes the explicit calculation definitions for the Phase 1
exploratory analysis.

The purpose is to prevent ambiguous use of "ATS %" and to ensure that every
reported percentage identifies the subject being measured.

These definitions govern the exploratory analysis and should be used when
updating the Phase 1 anomaly reference.

---

# 2. ATS Market Convention

The `consensus_spread` field uses the home-team spread convention:

- Negative spread = home team is the favorite.
- Positive spread = away team is the favorite.
- Zero spread = pick'em.

For a game with consensus spread `S`:

`home_ats_margin = (home_points - away_points) + S`

Interpretation:

- `home_ats_margin > 0` → home team covered.
- `home_ats_margin < 0` → away team covered.
- `home_ats_margin = 0` → ATS push.

The favorite is determined from the consensus spread, not from the game result.

---

# 3. Required ATS Reporting

Every ATS percentage must explicitly identify the subject.

The standard market-level metric is:

## Favorite Cover Rate

`favorite covers / ATS decisions`

The corresponding underdog result is automatically:

`underdog covers / ATS decisions`

Because every ATS decision has exactly one winning side unless there is a
push, favorite and underdog cover rates should sum to 100% of decisions.

**Pushes must always be reported separately.**

Recommended reporting format:

| Metric | Value |
|---|---:|
| Favorite covers | N |
| Underdog covers | N |
| Pushes | N |
| ATS decisions | N |
| Favorite cover rate | X% |
| Underdog cover rate | X% |

---

# 4. Pick'em Games

Consensus spread of exactly 0 is not assigned to favorite or underdog.

Pick'em games should be reported separately or excluded from favorite/underdog
cover-rate calculations.

They remain valid ATS observations when calculating home-team or away-team
cover rates.

---

# 5. Home/Away ATS

When the analysis is explicitly about location:

## Home-Team Cover Rate

`home teams covering / ATS decisions`

## Away-Team Cover Rate

`away teams covering / ATS decisions`

Pushes are reported separately.

These are not equivalent to favorite/underdog cover rates.

---

# 6. Season and Week Analysis

Season and week do not have an intrinsic subject team.

Therefore the default market-level metric is:

> **Favorite cover rate**

Every season or week table must include:

- favorite covers
- underdog covers
- pushes
- ATS decisions
- favorite cover rate
- underdog cover rate

Additional home/away rates may be included separately.

---

# 7. Spread Buckets

Spread buckets are market-level categories.

The default metric is:

> **Favorite cover rate**

For each spread bucket, report:

- favorite covers
- underdog covers
- pushes
- ATS decisions
- favorite cover rate
- underdog cover rate

The spread bucket is based on absolute consensus spread.

Pick'em games are handled separately.

---

# 8. Kickoff-Time Analysis

Kickoff-time categories are market-level categories.

The default metric is:

> **Favorite cover rate**

Kickoff time is derived from `venue_local_start_date`.

The analysis should initially preserve relatively fine-grained local-time
categories rather than forcing Day/Evening/Night buckets.

Each time bucket reports:

- favorite covers
- underdog covers
- pushes
- ATS decisions
- favorite cover rate
- underdog cover rate

---

# 9. Conference Analysis

Conference analysis must identify the subject.

For a conference team:

> **Conference-team cover rate**

means the conference team's ATS result, regardless of whether that team was
the favorite or underdog.

Additional market-level analysis may report:

> **Favorite cover rate for games involving the conference**

These are separate metrics and must not be combined under a generic "ATS %"
label.

---

# 10. Individual Team Analysis

Individual-team performance requires multiple views because a team's ATS
performance may differ substantially depending on market status.

For each team, where sample size permits, calculate at minimum:

1. Overall team cover rate.
2. Team-as-favorite cover rate.
3. Team-as-underdog cover rate.
4. Home-team cover rate.
5. Road-team cover rate.
6. Favorite/underdog game counts.
7. Push counts.

A team-level table should therefore distinguish:

- `team_cover_rate`
- `favorite_cover_rate`
- `underdog_cover_rate`
- `home_cover_rate`
- `road_cover_rate`

No team should be characterized as an ATS "edge" using overall performance
alone.

---

# 11. Ranked Matchups

Ranked matchups require multiple explicitly defined perspectives.

A team with rank 1 is higher-ranked than a team with rank 10.

For games where both teams are ranked, identify:

- higher-ranked team
- lower-ranked team
- favorite
- underdog

These are separate concepts.

## Required Ranked-Matchup Metrics

### 11.1 Favorite Cover Rate

`favorite covers / decisions`

### 11.2 Underdog Cover Rate

`underdog covers / decisions`

### 11.3 Higher-Ranked Team Cover Rate

`higher-ranked team covers / decisions`

### 11.4 Lower-Ranked Team Cover Rate

`lower-ranked team covers / decisions`

### 11.5 Higher-Ranked Team Is Favorite

Count and percentage of ranked matchups where the higher-ranked team is also
the favorite.

### 11.6 Higher-Ranked Team Is Underdog

Count and percentage of ranked matchups where the higher-ranked team is the
underdog.

These categories must not be collapsed into one "ranked ATS %" measure.

---

# 12. Ranked Matchup Cross-Classification

For both-ranked games, the most informative four-way classification is:

1. Higher-ranked team is favorite.
2. Higher-ranked team is underdog.
3. Lower-ranked team is favorite.
4. Lower-ranked team is underdog.

Because favorite/underdog and higher/lower rank are independent concepts, this
cross-classification should be retained.

For each category report:

- games
- favorite covers
- underdog covers
- higher-ranked team covers
- lower-ranked team covers
- pushes
- relevant cover rates

---

# 13. Totals

Totals are separate from ATS spread analysis.

For games with a valid consensus total:

`total_margin = home_points + away_points - consensus_total`

Interpretation:

- `total_margin > 0` → Over
- `total_margin < 0` → Under
- `total_margin = 0` → Push

Every totals analysis must report:

- Over count
- Under count
- Push count
- decisions
- Over rate
- Under rate

A generic "ATS %" label must never be used for totals.

---

# 14. Market Dispersion

When examining sportsbook disagreement, the subject is the ATS market.

Default metric:

> **Favorite cover rate**

For each dispersion category, report:

- games
- favorite covers
- underdog covers
- pushes
- decisions
- favorite cover rate
- underdog cover rate

Provider count should also be reported because dispersion is partly a function
of market coverage.

---

# 15. Neutral-Site Analysis

Neutral-site games should initially be evaluated using:

- favorite cover rate
- underdog cover rate
- pushes
- decisions

They should then be separated into:

- regular season neutral-site games
- postseason/bowl neutral-site games

before drawing conclusions.

---

# 16. Day-of-Week Analysis

Day-of-week categories have no intrinsic subject.

Default metric:

> **Favorite cover rate**

Report favorite covers, underdog covers, pushes, decisions, and both cover
rates.

Conference/day combinations should use the conference-team metric when the
conference is the subject.

---

# 17. Season Stability

A finding should not be treated as a persistent effect merely because the
2016–2025 aggregate is unusual.

Important findings should be examined by:

- season
- sample size
- point estimate
- push count
- consistency of direction

A result concentrated in one or two seasons should be identified as such.

---

# 18. Sample Size

Exploratory analysis should retain all observations but clearly distinguish
small samples from well-supported categories.

No arbitrary minimum sample threshold should be silently applied.

When ranking teams or categories, the report should display the sample size so
that extreme percentages from small samples are not mistaken for strong
evidence.

---

# 19. Statistical Interpretation

The exploratory pass is for anomaly detection.

A deviation from 50% is not automatically:

- statistically significant;
- profitable;
- causal;
- persistent;
- predictive.

Step 2 should test promising findings using appropriate statistical methods,
season stability, and multiple-comparison awareness.

---

# 20. Standard Terminology

Use these terms consistently:

- **Favorite cover rate**
- **Underdog cover rate**
- **Home-team cover rate**
- **Road-team cover rate**
- **Team cover rate**
- **Higher-ranked team cover rate**
- **Lower-ranked team cover rate**
- **Over rate**
- **Under rate**
- **Pushes**
- **ATS decisions**

Avoid the unqualified phrase:

> "ATS %"

unless the subject has already been explicitly established in the same table
or section.

---

# 21. Research Principle

The purpose of explicit definitions is not to limit exploration.

It is to ensure that when a pattern appears, we know exactly what it means.

A result should be reproducible from the raw fields and the calculation
definition without relying on interpretation or context that is no longer
visible.
