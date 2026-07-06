# College Football ATS Research Platform

# API_ENDPOINT_REFERENCE_CH07.md

## Chapter 7 --- Appendix A: Endpoint Catalog & Parameter Matrix

**Document Status:** Canonical Development Draft **Parent Document:**
API_ENDPOINT_REFERENCE.md **Chapter:** 7 of N **Version:** 1.0-draft
**Project Phase:** Foundation Migration **Last Updated:** 2026-06-30

------------------------------------------------------------------------

# Purpose

This appendix provides a quick-reference catalog of the primary
endpoints used by the College Football ATS Research Platform. It is
intended to serve as a high-level engineering reference while
implementing acquisition workflows.

------------------------------------------------------------------------

# Endpoint Catalog

  --------------------------------------------------------------------------------------------------------------
  Endpoint      Tier       Primary Purpose  Output File                          Update Frequency    Required
  ------------- ---------- ---------------- ------------------------------------ ----------------- -------------
  Games         1          Schedule and     games\_`<season>`{=html}.json        Weekly /               Yes
                           final scores                                          Historical        

  Teams         1          Team identities  teams.json                           Seasonal               Yes
                           and metadata                                                            

  Conferences   1          Conference       conferences.json                     As needed              Yes
                           metadata                                                                

  Rankings      1          AP / CFP /       rankings\_`<season>`{=html}.json     Weekly                 Yes
                           Coaches rankings                                                        

  Betting Lines 1          ATS betting      lines\_`<season>`{=html}.json        Weekly                 Yes
                           information                                                             

  Team Records  1          Season records   records\_`<season>`{=html}.json      Weekly                 Yes

  Coaches       2          Coaching         coaches.json                         Seasonal           Recommended
                           information                                                             

  Venues        2          Stadium metadata venues.json                          As needed          Recommended

  Talent        2          Team talent      talent\_`<season>`{=html}.json       Annual              Optional
                           ratings                                                                 

  Recruiting    2          Recruiting       recruiting\_`<season>`{=html}.json   Annual              Optional
                           history                                                                 

  Weather\*     External   Historical       weather\_`<season>`{=html}.json      Future              Optional
                           weather                                                                 
                           enrichment                                                              
  --------------------------------------------------------------------------------------------------------------

\*Weather is not available through the CollegeFootballData API and is
planned as a future external data source.

------------------------------------------------------------------------

# Common Parameters

  Parameter    Purpose
  ------------ ----------------------------------
  season       Select season to query
  week         Select week within season
  seasonType   Regular season, postseason, etc.
  team         Limit results to a specific team
  conference   Limit results to a conference
  provider     Betting provider where supported

Not every endpoint supports every parameter. Individual endpoint
documentation remains authoritative.

------------------------------------------------------------------------

# Output Standards

All downloaded files should:

-   Be stored as JSON in the raw archive.
-   Follow documented naming conventions.
-   Preserve the original API response.
-   Be validated before downstream processing.

------------------------------------------------------------------------

# Dependency Matrix

  Dataset            Depends On
  ------------------ ----------------------
  Games              Teams, Conferences
  Rankings           Games, Teams
  Betting Lines      Games
  Team Records       Games, Teams
  Master Database    All Tier 1 endpoints
  Research Modules   Master Database

------------------------------------------------------------------------

# Acquisition Priority

1.  Teams
2.  Conferences
3.  Games
4.  Rankings
5.  Betting Lines
6.  Team Records
7.  Tier 2 Enrichment

------------------------------------------------------------------------

# Chapter Summary

This appendix provides a concise engineering reference for endpoint
priorities, parameters, dependencies, and output conventions. It
complements the detailed endpoint specifications presented in earlier
chapters and is intended for quick consultation during implementation.
