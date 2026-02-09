# ArtemisOps — SpaceX Crew Mission Integration Plan

## Comprehensive Codebase Audit & Sprint Proposal

**Date:** February 9, 2026  
**Scope:** Add NASA/SpaceX Commercial Crew (Crew Dragon) missions alongside existing Artemis program support

---

## 1. Current State Assessment

### Already Multi-Mission Ready ✅

These components need zero or minimal changes:

| Component | File(s) | Why It Works |
|-----------|---------|-------------|
| Database schema | `database.py` | Generic `missions`, `crew`, `milestones` tables keyed by `mission_id` |
| Core API routes | `main.py` | `/api/missions/{id}`, `/api/missions/{id}/weather` are mission-agnostic |
| Fetcher programs filter | `fetcher.py` | Already includes `"commercial crew"`, `"crew dragon"`, `"starliner"` in `PROGRAMS_OF_INTEREST` |
| Info tab | `info.html` | 100% data-driven from API — renders whatever mission data it receives |
| Crew tab | `crew.html` | Data-driven via `postMessage` from shell — no mission-specific logic |
| Trajectory registry aliases | `trajectories.py` | `"crew-dragon" → "iss"` fallback already defined |
| MissionMapRouter | `MissionMapRouter.js` | Routes `crew-dragon` to `ISSMap` component |
| Weather API | `weather.py` | Generic by lat/lon coordinates, launch site lookup by name |
| Patch/logo fallbacks | `fetcher.py` | Already has `"crew dragon"` and `"SpaceX"` entries in `FALLBACK_PATCHES` / `FALLBACK_AGENCY_LOGOS` |

### Hardcoded to Artemis ❌

These are the items that need work, organized by layer:

---

## 2. Detailed Audit — Backend

### 2.1 `server/fetcher.py` — Data Sync

| Issue | Location | Impact |
|-------|----------|--------|
| `ARTEMIS_II_CREW_FALLBACK` hardcoded crew array | Lines 490-540 | Only Artemis II has curated fallback crew data |
| `ARTEMIS_II_MILESTONES_FALLBACK` hardcoded milestones | Lines 543-580 | Only Artemis II has milestone timeline |
| `sync_all_missions()` special-cases `"artemis-ii"` for crew/milestones | Lines 620-640 | Crew Dragon missions get API crew only — no curated milestones |
| `ensure_default_missions()` only seeds Artemis II | Lines 650-690 | No Crew Dragon default if API is down |
| `LOCAL_PATCHES` only has `artemis-ii`, `artemis-iii` | Lines 33-36 | No local patches for SpaceX missions |

**What needs to change:** Add Crew Dragon fallback data pattern, make the special-casing extensible (e.g. a registry of curated overrides keyed by mission slug pattern), seed at least the next Crew Dragon mission.

### 2.2 `server/main.py` — API & WebSocket

| Issue | Location | Impact |
|-------|----------|--------|
| WebSocket `screen_websocket` sends `get_full_mission("artemis-ii")` on connect | Line 1018 | New screens always get Artemis II data first |
| WebSocket `/ws` sends `get_full_mission("artemis-ii")` on connect | Line 1098 | Same issue for legacy WebSocket |
| Legacy endpoint `GET /api/mission` returns `artemis-ii` | Line 248 | Hardcoded default mission |
| Legacy endpoint `GET /api/crew` returns `artemis-ii` crew | Line 256 | Hardcoded default crew |
| `DEFAULT_RECOVERY_SITE` is Atlantic (30°N, 75°W) | `weather.py` line 400 | Orion splashdown zone — Dragon lands Gulf Coast |
| Weather operations endpoint uses single hardcoded recovery zone | `main.py` line 340 | No per-mission recovery site |

**What needs to change:** WebSocket should send the *first active mission* (or the one the screen is configured for), not hardcoded `artemis-ii`. Recovery site needs to come from the mission record itself.

### 2.3 `server/weather.py` — Recovery Sites

| Issue | Detail |
|-------|--------|
| `DEFAULT_RECOVERY_SITE` = Atlantic (30°N, 75°W) | Correct for Artemis/Orion capsule splashdowns |
| SpaceX Crew Dragon recovery zones | Typically off Pensacola, Panama City, or Jacksonville FL |
| `SITE_COORDINATES` dict | Has "kennedy space center", "cape canaveral", etc. but no SpaceX-specific recovery zones |
| No `recovery_site` field on mission DB record | Recovery location can't vary per mission |

**What needs to change:** Add `recovery_site` and `recovery_lat`/`recovery_lon` fields to missions table. Populate from API or seed data. Weather operations endpoint should use per-mission recovery coordinates.

### 2.4 `server/trajectories.py` — Trajectory Data

| Status | Detail |
|--------|--------|
| ✅ Already handled | `"crew-dragon": "iss"` alias maps to ISS LEO trajectory |
| ⚠️ Missing | No Crew Dragon–specific waypoints (launch, MECO, orbit insertion, ISS rendezvous, docking) |
| ⚠️ Missing | No Dragon-specific phases (pre-launch, ascent, phasing, approach, docking, undocking, deorbit, splashdown) |

**What needs to change:** Add a `CREW_DRAGON_TRAJECTORY` with Dragon-specific waypoint names and timing. The ISS fallback works for now but doesn't show the rendezvous/docking profile.

### 2.5 `server/news.py` — RSS Feeds

| Current Feeds | Covers SpaceX Crew? |
|---------------|---------------------|
| NASA Breaking News | ✅ Sometimes covers Crew Dragon |
| NASA Artemis Blog | ❌ Artemis only |
| NASA ISS Blog | ✅ Covers crew rotations |
| Spaceflight Now | ✅ Covers all launches |

**What needs to change:** Add NASA Commercial Crew blog feed (`https://blogs.nasa.gov/commercialcrew/feed/`). Consider adding SpaceX news feed.

### 2.6 `server/streams.py` — Live Video

| Current Sources | Covers SpaceX? |
|-----------------|-----------------|
| YouTube @NASA/streams scraper | ✅ NASA streams SpaceX launches |
| Multiple channel scraper | Partially — depends on which channels are configured |

**What needs to change:** Add `@SpaceX` YouTube channel to the multi-channel scraper. SpaceX runs their own webcasts for every Crew Dragon launch/landing.

### 2.7 `server/seed_artemis_missions.py`

| Issue | Impact |
|-------|--------|
| Only seeds Artemis II, III, IV, V | No Crew Dragon missions seeded |
| Script name is Artemis-specific | Should be generic `seed_missions.py` |

**What needs to change:** Extend (or create new script) to seed upcoming Crew Dragon missions with crew/milestones.

---

## 3. Detailed Audit — Frontend

### 3.1 `client/index.html` (Main Shell)

| Issue | Location | Detail |
|-------|----------|--------|
| `currentMission: 'artemis-ii'` | Line 121 | Hardcoded default mission |
| No mission switcher UI in nav bar | Header area | User can't switch between missions without control panel |

**What needs to change:** Default mission should be the *next upcoming* mission from API. Add a mission selector to the main nav bar (or at least surface the existing one from control.html).

### 3.2 `client/index-shell.html` (iframe Shell)

| Issue | Location | Detail |
|-------|----------|--------|
| `currentMissionId: 'artemis-ii'` | Line 273 | Hardcoded default |
| `loadMissionData()` fetches `artemis-ii` initially | Shell init | Same issue |

**What needs to change:** Same as index.html — use API's first active mission.

### 3.3 `client/tabs/mission.html` — Countdown & Video

| Issue | Location | Detail |
|-------|----------|--------|
| `ARTEMIS II` hardcoded in header HTML | Line 755 | Should come from `missionData.name` |
| Fallback news ticker references "Artemis II" and "SLS" | Line 1480 | Fallback should be generic or mission-aware |
| Countdown layout assumes single launch window | Layout | Crew Dragon has instantaneous windows — different UX than Artemis's multi-hour windows |
| No mission-type awareness for status display | Throughout | LEO missions show different info than lunar |
| `apiBase: '/api/missions/artemis-ii'` | Line 934 | Hardcoded API path |

**What needs to change:** Header and API path must use dynamic mission ID from parent shell. Fallback news should be generic. Consider showing docking countdown / undocking countdown for ISS missions.

### 3.4 `client/tabs/tracking.html` — Map Views

| Issue | Location | Detail |
|-------|----------|--------|
| Three hardcoded Artemis iframe views | Lines 65-77 | `view-artemis-ii`, `view-artemis-ii-3d`, `view-artemis-iii` |
| No LEO tracking view for Crew Dragon | Entire file | Would need ISS-style orbit view showing Dragon approach |
| Mode buttons hardwired to artemis-ii/iii | Parent shell | Shell sends `setTrackingMode` with fixed mode IDs |
| No dynamic view generation from mission list | Architecture | Views are static HTML, not data-driven |

**What needs to change:** This is the biggest frontend lift. Tracking needs to dynamically show appropriate views based on mission type. For Crew Dragon: show the ISS tracker with Dragon position overlay. For Artemis: show lunar trajectory. Could use MissionMapRouter pattern that already exists in the component system.

### 3.5 `client/tabs/trajectory3d.html` — 3D Visualization

| Issue | Location | Detail |
|-------|----------|--------|
| Title: `<title>Artemis II — 3D Trajectory</title>` | Line 6 | Hardcoded |
| Loading screen: "ARTEMIS II" | Line 211 | Hardcoded |
| HUD label: "ARTEMIS II" | Line 227 | Hardcoded |
| Entire 3D scene is Artemis II lunar trajectory | All JS | Earth-Moon system with free-return path |
| No LEO 3D mode | Architecture | Would need Earth-only with ISS orbit |

**What needs to change:** Make title/labels dynamic. For Sprint 1, the 3D view can remain Artemis-only — Crew Dragon missions would use the 2D ISS tracker instead. Long-term: add LEO 3D mode showing ISS orbit + Dragon rendezvous.

### 3.6 `client/tabs/weather.html` — Launch Site Weather

| Issue | Location | Detail |
|-------|----------|--------|
| `missionId: 'artemis-ii'` default | Line 1158 | Hardcoded |
| Section title: "Launch Weather" with 🚀 | Header | Generic enough — works for any mission |
| `ARTEMIS II` referenced in WDR countdown label | Line 1173 | Hardcoded fallback |
| GOES satellite imagery is KSC-area specific | Satellite sub-tab | Works for SpaceX at KSC too (same pad area) |

**What needs to change:** Mission ID should come from parent shell. KSC-area weather and satellite imagery works for both Artemis (39B) and SpaceX (39A) — they're adjacent pads. Minimal changes needed.

### 3.7 `client/tabs/recovery.html` — Splashdown Weather

| Issue | Location | Detail |
|-------|----------|--------|
| `missionId: 'artemis-ii'` default | Line 669 | Hardcoded |
| Recovery zone hardcoded to Atlantic | Backend | Orion splashdown area ≠ Dragon splashdown area |
| Radar/satellite imagery centered on Atlantic | Map config | Would need to shift for Gulf Coast Dragon recovery |
| Section title: "Recovery Weather" with 🎯 | Header | Generic enough |

**What needs to change:** Recovery site coordinates must come from mission data. Map center should be dynamic based on recovery site location.

### 3.8 `client/tabs/control.html` — Multi-Screen Control

| Issue | Location | Detail |
|-------|----------|--------|
| Mission selector has `<option value="artemis-ii">` hardcoded | Line 616 | Should populate from API |
| Page icons only cover existing tabs | Line ~540 | Works as-is |

**What needs to change:** Mission selector should populate dynamically from `/api/missions`.

### 3.9 `client/mission-control.html` — Kiosk Display

| Issue | Location | Detail |
|-------|----------|--------|
| Default mission: `artemis-ii` (from URL param fallback) | Line 818 | Should use first active mission |
| Layout optimized for lunar countdown | Structure | Works for any countdown — generic enough |
| Status indicators (Vehicle, Weather, Range, Crew, Ground) | GO/NO-GO section | Generic — works for any mission |

**What needs to change:** URL param fallback should query API for default. Layout is actually mission-agnostic already.

---

## 4. SpaceX Crew Dragon — Mission Profile Differences

| Attribute | Artemis II | Crew Dragon (e.g. Crew-10) |
|-----------|-----------|---------------------------|
| Rocket | SLS Block 1 | Falcon 9 Block 5 |
| Spacecraft | Orion | Crew Dragon |
| Launch Site | KSC Pad 39B | KSC Pad 39A |
| Orbit | Lunar free-return | LEO → ISS (408 km) |
| Duration | ~10 days | ~6 months (docked at ISS) |
| Recovery | Atlantic Ocean splashdown | Gulf Coast or Atlantic FL coast |
| Launch Window | Multi-hour window | Instantaneous (ISS phasing) |
| Milestones | WDR → Cryo → Ingress → Launch | Static Fire → Launch → Docking → Undocking → Splashdown |
| Trajectory Type | Earth-Moon-Earth | LEO rendezvous & docking |
| Live Streams | NASA TV | NASA TV + SpaceX webcast |
| News Sources | NASA Artemis Blog | NASA Commercial Crew Blog |
| Agency | NASA/CSA | NASA/SpaceX |

---

## 5. Database Schema Changes

### New fields on `missions` table:

```sql
ALTER TABLE missions ADD COLUMN recovery_site TEXT;      -- "Gulf Coast, FL"
ALTER TABLE missions ADD COLUMN recovery_lat REAL;       -- 29.5
ALTER TABLE missions ADD COLUMN recovery_lon REAL;       -- -87.0
ALTER TABLE missions ADD COLUMN launch_window_type TEXT;  -- "instantaneous" | "multi-hour" | "tbd"
ALTER TABLE missions ADD COLUMN mission_profile TEXT;     -- "lunar" | "leo-iss" | "leo-free" | "gateway"
ALTER TABLE missions ADD COLUMN docking_date TEXT;        -- For ISS missions
ALTER TABLE missions ADD COLUMN undocking_date TEXT;      -- For ISS missions
```

These enable mission-type-aware UI decisions without hardcoding.

---

## 6. Sprint Plan

### Sprint 1: Multi-Mission Foundation (Backend + Data Layer)
**Goal:** Any mission from Space Devs API renders correctly across all tabs  
**Effort:** ~16 hours

| # | Task | File(s) | Effort | Detail |
|---|------|---------|--------|--------|
| 1.1 | DB schema migration — add recovery/profile fields | `database.py` | 1h | Add columns listed in Section 5, with migration safety |
| 1.2 | Fetcher: populate new fields from Space Devs API | `fetcher.py` | 2h | Parse `mission_profile` from program type, extract recovery site from API data, set `launch_window_type` |
| 1.3 | Fetcher: make curated overrides extensible | `fetcher.py` | 2h | Replace `if "artemis-ii"` special-cases with a `CURATED_MISSIONS` registry dict keyed by slug pattern |
| 1.4 | Seed Crew Dragon missions | `seed_missions.py` (new) | 3h | Crew-10, Crew-11 with crew, milestones (Static Fire → Launch → Docking → Undocking → Splashdown), recovery sites, SpaceX patches |
| 1.5 | Weather: per-mission recovery site | `weather.py`, `main.py` | 1.5h | `get_weather_operations` reads `recovery_lat/lon` from mission record instead of `DEFAULT_RECOVERY_SITE` |
| 1.6 | News: add Commercial Crew blog feed | `news.py` | 0.5h | Add `https://blogs.nasa.gov/commercialcrew/feed/` to `FEEDS` list |
| 1.7 | Streams: add @SpaceX YouTube channel | `streams.py` | 0.5h | Add to multi-channel scraper source list |
| 1.8 | WebSocket: dynamic default mission | `main.py` | 1h | On connect, send first active mission from `get_all_missions()` instead of hardcoded `artemis-ii` |
| 1.9 | Trajectory: Crew Dragon waypoints | `trajectories.py` | 2h | Add `CREW_DRAGON_TRAJECTORY` with launch, MECO, orbit insertion, phasing burns, approach, docking, undocking, deorbit, splashdown |
| 1.10 | Local patches for Crew Dragon | `assets/patches/` | 0.5h | Download SpaceX Crew-10/11 mission patches, add to `LOCAL_PATCHES` |
| 1.11 | Legacy endpoints: use first active mission | `main.py` | 1h | `/api/mission` and `/api/crew` return first active instead of `artemis-ii` |

### Sprint 2: Frontend Multi-Mission Awareness
**Goal:** All tabs dynamically adapt to whichever mission is selected  
**Effort:** ~14 hours

| # | Task | File(s) | Effort | Detail |
|---|------|---------|--------|--------|
| 2.1 | Shell: dynamic default mission | `index.html`, `index-shell.html` | 1h | Fetch `/api/missions`, use first result as `currentMission` instead of `'artemis-ii'` |
| 2.2 | Shell: mission selector in nav bar | `index.html` | 2h | Add dropdown to header showing all active missions, switches all tabs on change |
| 2.3 | Mission tab: dynamic header & API path | `mission.html` | 1.5h | Replace hardcoded "ARTEMIS II" with `missionData.name`, replace hardcoded API path with dynamic `missionId` from shell |
| 2.4 | Mission tab: generic fallback news | `mission.html` | 0.5h | Replace Artemis-specific fallback ticker items with generic "Loading latest mission news..." |
| 2.5 | Weather tab: dynamic mission ID | `weather.html` | 0.5h | Use `missionId` from parent shell instead of hardcoded `'artemis-ii'` |
| 2.6 | Recovery tab: dynamic mission ID + map center | `recovery.html` | 1.5h | Dynamic `missionId`, map center from recovery site coordinates in API response |
| 2.7 | Control tab: dynamic mission selector | `control.html` | 1h | Populate mission dropdown from `/api/missions` API instead of hardcoded option |
| 2.8 | Mission-control kiosk: dynamic default | `mission-control.html` | 0.5h | URL param fallback queries API for first active mission |
| 2.9 | Trajectory 3D: dynamic labels | `trajectory3d.html` | 1h | Title, loading screen, HUD label read from mission data. Show "3D view not available" for non-lunar missions |
| 2.10 | Mission tab: LEO-aware info boxes | `mission.html` | 2h | For `mission_profile: "leo-iss"`: show docking countdown (if pre-dock), show mission elapsed time (if docked), show undocking countdown (if near end). Hide lunar-specific displays |
| 2.11 | Mission tab: mission-type milestone icons | `mission.html` | 0.5h | Use 🚀 for launch on any mission, use appropriate phase icons for Dragon vs Artemis milestones |
| 2.12 | Tracking tab: mission-type view routing | `tracking.html` | 2h | If mission is `leo-iss`: show ISS tracker view. If `lunar`: show Artemis views. Dynamic iframe src selection based on `mission_profile` from API |

### Sprint 3: Polish & Full Integration
**Goal:** Seamless experience switching between Artemis and Crew Dragon missions  
**Effort:** ~10 hours

| # | Task | File(s) | Effort | Detail |
|---|------|---------|--------|--------|
| 3.1 | Mission tab: instantaneous window indicator | `mission.html` | 1h | For `launch_window_type: "instantaneous"`: show "INSTANTANEOUS WINDOW" badge, no window-open/close display |
| 3.2 | Tracking tab: Dragon rendezvous overlay | `tracking.html`, ISS mockup | 3h | When viewing a Crew Dragon mission on ISS tracker, show Dragon icon approaching ISS on the same orbit track |
| 3.3 | Recovery tab: Dragon recovery zone presets | `weather.py`, `recovery.html` | 1.5h | Add Gulf Coast, Jacksonville, Pensacola recovery zone coordinates. Radar/satellite imagery auto-selects based on recovery site region |
| 3.4 | Cross-tab mission switching | Shell + all tabs | 1.5h | When user switches mission in nav bar, all tabs update simultaneously via `postMessage`. Tracking switches view type automatically |
| 3.5 | Crew tab: extended mission roster display | `crew.html` | 1h | For 6-month ISS missions with 4+ crew, ensure grid layout scales. Show "Expedition XX" badge for ISS crews |
| 3.6 | PRODUCTION_QUEUE.md update | `PRODUCTION_QUEUE.md` | 0.5h | Add SpaceX Crew integration to completed phases, update file tree, add new API endpoints |
| 3.7 | End-to-end testing | All files | 1.5h | Test full flow: switch between Artemis II and Crew-10, verify countdown, weather, tracking, crew, recovery all update correctly |

---

## 7. Sprint Summary

| Sprint | Focus | Effort | Deliverable |
|--------|-------|--------|-------------|
| **Sprint 1** | Backend + Data | ~16h | SpaceX missions in DB, dynamic API, feeds, patches, trajectories |
| **Sprint 2** | Frontend Adaptation | ~14h | All tabs mission-aware, no hardcoded Artemis references |
| **Sprint 3** | Polish + Testing | ~10h | Seamless multi-mission switching, Dragon-specific UX |
| **Total** | | **~40h** | Full SpaceX Crew Dragon support alongside Artemis |

---

## 8. Risk Assessment

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Space Devs API doesn't have complete Crew Dragon data | Medium | Curated fallback data in seed script, same pattern as Artemis II |
| SpaceX YouTube channel scraping breaks | Low | Fallback to NASA TV streams (already covers SpaceX launches) |
| Crew Dragon recovery site varies per mission | High | Store per-mission in DB, update during sync. Default to "off FL coast" |
| 6-month ISS missions overwhelm milestone timeline | Medium | Group milestones by phase (pre-launch, ascent, on-orbit, return). Collapse on-orbit months |
| Tracking tab iframe architecture limits flexibility | High | Sprint 2 task 2.12 adds routing logic. Long-term: refactor to component-based rendering |

---

## 9. Files Changed Per Sprint

### Sprint 1 (Backend)
```
server/database.py          — Schema migration
server/fetcher.py           — Extensible curated overrides, new field population
server/main.py              — Dynamic default mission, recovery site from DB
server/weather.py           — Per-mission recovery coordinates
server/trajectories.py      — Crew Dragon trajectory data
server/news.py              — Commercial Crew feed
server/streams.py           — SpaceX YouTube channel
server/seed_missions.py     — NEW: Crew Dragon seed data
client/assets/patches/      — Crew Dragon mission patches
```

### Sprint 2 (Frontend)
```
client/index.html           — Dynamic default, mission selector
client/index-shell.html     — Dynamic default, mission selector
client/tabs/mission.html    — Dynamic header/API, LEO awareness
client/tabs/tracking.html   — Mission-type view routing
client/tabs/weather.html    — Dynamic mission ID
client/tabs/recovery.html   — Dynamic mission ID, map center
client/tabs/control.html    — Dynamic mission selector
client/tabs/trajectory3d.html — Dynamic labels
client/mission-control.html — Dynamic default
```

### Sprint 3 (Polish)
```
client/tabs/mission.html    — Window type indicator
client/tabs/tracking.html   — Dragon overlay
client/tabs/recovery.html   — Recovery zone presets
client/tabs/crew.html       — Extended roster display
client/index.html           — Cross-tab switching
PRODUCTION_QUEUE.md         — Documentation update
```