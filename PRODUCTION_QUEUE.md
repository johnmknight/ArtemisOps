# ArtemisOps - Production Queue & Integration Plan

## Overview
This document tracks development progress and the integration plan for the ArtemisOps application.

**Last Updated:** March 12, 2026

---

## 🎯 Current Sprint - Active Work

### Recently Completed (Feb 7)
- [x] ISS nadir view lighting improvements — brighter ambient, directional light from below, blue fill light
- [x] World map zoom adjustment — width+height fit to show full globe
- [x] Add keyboard navigation to index-shell.html — arrow keys, number keys, fullscreen toggle
- [x] Remove redundant tracking header — stripped CSS, HTML, and JS status text from tracking.html
- [x] Add iframe keyboard forwarding — all tabs and mockups forward navigation keys (←/→, 0-4, F, F11) to parent shell via postMessage
- [x] Improve shell keydown handler — null-safety on `e.target`, centralized `preventDefault`
- [x] Remove tracking tab mode selector buttons — simplified header to status indicator only
- [x] Fix crew card portrait aspect ratios (3:4 wrapper) and bio text clamping (5 lines)
- [x] Fix crew card alignment and hide EVA sidebar when no EVA data present
- [x] Update crew data source to NASA "Our Artemis Crew" page — bios, names, roles matched to official NASA/CSA astronaut pages, photos use official JSC Artemis II portraits

### Previously Completed (Jan 25)
- [x] Switch ISS tracker map to EPSG:4326 Equirectangular projection (NASA Mission Control style)
- [x] Integrate NASA GIBS Blue Marble satellite tiles
- [x] Add lat/lon grid lines overlay (30° intervals)
- [x] Enable fractional zoom for optimal map fill
- [x] Fix tile wrapping (no duplicate world maps)
- [x] Add spacecraft manifest data file (`client/data/spacecraft-manifest.json`)

### Completed (Mar 6)
- [x] ao-frames.css complete — all 4 tiers built (page, panel, sub, popup)
- [x] Corner border bug resolved — double clip-path layer technique (no more box-shadow on clipped elements)
- [x] Z-index stack formalized — content z:12, page-border SVG z:14, popups z:100
- [x] ao-frame-popup tier built out — octagonal clip, bright accent, corner pins, status variants
- [x] Utility components added — .ao-dot (status indicators), .ao-readout (label:value rows), .ao-divider
- [x] Responsive breakpoints — 900px and 600px countdown digit scaling
- [x] prefers-reduced-motion — kills sep-pulse and dot-pulse animations

### Completed (Mar 12)
- [x] Fixed tracking map regression — duplicate `const mapEl` SyntaxError in mode3-iss-live.html (commit e33d6c4)
- [x] Converted orion_capsule.stl → orion-capsule.glb via trimesh (932KB, committed f95e8fd)
- [x] Created craft.html — Spacecraft Reference tab with Three.js GLB viewer + spec sidebar
  - Selector buttons: ISS / Crew Dragon / Cargo Dragon / Orion
  - Auto-scaled GLB loader with HD/fallback chain for ISS
  - Manual orbit controls (drag + scroll zoom), auto-rotate toggle, reset view
  - Spec sidebar: name card, status badge (pulsing dot), spec table, mission note
  - ao-themes.css wired, postMessage key forwarding + theme switching

### Up Next (Current Sprint)
- [ ] Wire `'craft'` into `tabOrder` in `index-shell.html` (pending Dragon model downloads)
- [ ] Download Dragon GLB models from Sketchfab and commit: crew-dragon.glb, cargo-dragon.glb
- [ ] Apply ao-frames.css to panels — mission.html, tracking.html, crew.html panels need frame classes
- [ ] Continue fixing Mission page sizing — maximize countdown clock per design intent
- [ ] Add back video feeds for ISS tracking page
- [ ] Implement full theming system with switchable palettes, fonts, and border styles

### Completed (Mar 7)
- [x] ao-themes.css — 4 themes (nominal/expanse/hazard/stealth) with `--theme-*` CSS tokens
- [x] mission.html interior wired to theme system — all color vars reference `--theme-*` with fallbacks
- [x] crew.html wired to ao-themes.css — added link + remapped :root vars to `--theme-*` tokens
- [x] ao-frame-sub.horizontal variant — top accent stripe for header/footer/ticker elements
- [x] Mission page ao-frame-sub applied — header-bar, timeline-strip, news-ticker all use `.horizontal`
- [x] CSS specificity bug fixed — `.ao-page-border` added to ao-frames.css exclusion list; mission layout no longer pushed off-screen
- [x] postMessage type mismatch fixed — mission.html now handles both `setMissionData` and `missionData`; weather handler patched to match
- [x] Shell null guards — `updateHeader()` and `updateMissionSelector()` check element existence before setting properties
- [x] Info tab paused — removed from `tabOrder` and iframe commented out; code fully preserved for resumption
- [x] Countdown digit size increased — raised vh clamp ceilings on `.countdown-left .ao-digit-cell` and `.ao-digit-value`

### Recently Completed (Feb 11)
- [x] Asset localization: all crew photos, agency logos, hero images served from local /assets/ (zero remote image fetches)
- [x] Agency logo upgrades: ESA PNG, hi-res JAXA (40KB) and Roscosmos (73KB) PNGs replace corrupt/tiny files
- [x] ISS tracking header: text agency badges replaced with actual logo images (NASA, ESA, JAXA, CSA, Roscosmos)
- [x] Crew ISS mission branding rule: Crew-X missions always show NASA logo instead of SpaceX
- [x] Page architecture consolidation: deleted standalone mission-control.html, all UI lives in tabs/*.html via iframe shell
- [x] Mission patch fixes: API field mismatch (mission_patch vs patch_url), Crew-12 patch upgraded to 544KB with transparency
- [x] Font research: evaluated 24 space/sci-fi fonts, selected Orbitron + existing stack, samples page created

### Recently Completed (Feb 10)
- [x] Mission Control: NASA TV / YouTube live stream panel (60/40 split layout with source selector, load/mute/fullscreen controls)
- [x] Mission Control: Scrolling news ticker (fetches /api/news, auto-scroll with hover pause)
- [x] Mission Control: Countdown digit sizing adjusted for split-panel layout

### Recently Completed (Feb 9)
- [x] Weather tab: switched to live ops endpoint (`/api/weather/operations/`) — no longer gated on 7-day launch window
- [x] Weather tab: updated GOES satellite imagery from GOES-16/17 to GOES-19/18 (current operational satellites)
- [x] Weather tab: fixed satellite image loading (removed crossorigin attribute breaking redirected URLs)
- [x] Weather tab: fixed EVENT_DATE_KEY mapping to match operations response format
- [x] All weather sub-tabs verified operational: Radar, Satellite (5 bands + SLIDER), Space Wx, Lightning

### Recently Completed (Feb 8)
- [x] ISS map icon updated to icon gallery style
- [x] Mission tab message types fixed (missionData/weatherData)
- [x] Control panel mission selector for Add Screen form
- [x] 3D trajectory tab, Artemis II 3D mockups, earth/moon textures, Orion model
- [x] Fallback solar joint discovery in ISS 3D view
- [x] Day/night terminator overlay on ISS 2D map (solar position calc, night polygon, toggleable)
- [x] Ground station visibility overlays (12 stations, comm range circles, tooltips, toggleable)
- [x] Crew tab: agency badges, bio links, loading skeleton, error state, photo_url bug fix
- [x] Mission Control: fix agency_logo_url, patch_url, date_label field mismatches
- [x] Mission Control: GO/NO-GO status indicators (Vehicle, Weather, Range, Crew, Ground)
- [x] Mission Control: crew photo strip with portraits and roles
- [x] Mission Control: full horizontal timeline (all milestones, not just 3)
- [x] Mission Control: MET header display (T-minus/T-plus)
- [x] Mission Control: mission status info box
- [x] Weather tab: RainViewer + NOAA MRMS radar overlays
- [x] Weather tab: SWPC Space Weather proxy (Kp, solar wind, X-ray, proton, alerts, forecast)
- [x] Weather tab: GOES-19 satellite imagery (5 bands + ABI sectors)
- [x] Weather tab: Real Blitzortung WebSocket lightning + NWS fallback
- [x] Weather tab: GOES-19 GLM flash extent density overlay
- [x] Weather tab: RAMMB/CIRA SLIDER interactive satellite viewer
- [x] Weather tab: Aurora OVATION forecast image in Space Weather view
- [x] Weather tab: Additional SWPC endpoints (solar-regions, enlil, kp-1min)

### Completed
- [x] **Finish 3D ISS view updates** - Camera angles, dual-view layout (NASA reference)
- [x] **Implement dual 3D panel layout** - Side-by-side orthogonal ISS views

### Up Next
- [ ] **Control page: Data/API tab** — New tab listing all server-side API calls with last-fired timestamps, response status, and editable polling intervals
- [x] ~~Add orbit track rendering~~ — Already implemented (`calculatePredictedOrbit` with 51.6° inclination, Earth rotation, dateline wrapping)
- [x] ~~Implement ground station visibility overlays~~ — 12 stations (MCC-H, TsUP, TDRS, DSN, JAXA, ESA, CSA) with comm range circles
- [x] ~~Add day/night terminator line to map~~ — Solar declination + equation of time, polygon overlay, 60s refresh

---

## 📊 Current Status Summary

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | ISS Tracker + Icons + Backend | ✅ Complete |
| Phase 2 | Main App Integration | ✅ Complete |
| Phase 3 | Component Architecture | ✅ Complete |
| Phase 4 | Backend API Enhancements | ✅ Complete |
| Phase 5 | Mission Control Mode | ✅ Complete |
| Phase 6 | Border System + Theming | 🔄 In Progress |
| Phase 7 | Offline Support / PWA | 🔲 Not Started |
| Phase 8 | Mobile UI Mode | 🔲 Not Started (Low Priority) |

---

## ✅ Phase 1: Core Components - COMPLETE

### ISS Tracker Implementation
- [x] Real-time ISS position on world map (Leaflet.js)
- [x] Ground track (orbit path preview)
- [x] ISS footprint circle (visibility area)
- [x] Position data overlay (lat, lon, alt, velocity)
- [x] Auto-refresh every 5 seconds
- [x] Crew roster integration (Open Notify API)
- [x] Location name reverse geocoding
- [x] Toggle controls for footprint/track visibility

### Icon Libraries
- [x] Spacecraft Icons: ISS, Orion, Orion-ESM, Starship HLS, Crew Dragon, SLS
- [x] UI Icons: 40+ icons for navigation, status, actions, indicators

### Server Backend (v0.5.0)
- [x] FastAPI server with async support
- [x] WebSocket for real-time updates
- [x] Multi-mission support
- [x] SQLite database with migrations
- [x] Hourly data sync from NASA/ESA APIs
- [x] Weather integration for launch sites
- [x] Mission patches and agency logos

---

## ✅ Phase 2: Main App Integration - COMPLETE

### Desktop UI (4 Tabs)
- [x] **MISSION Tab**: Countdown, Weather, Status, Timeline
- [x] **TRACKING Tab**: ISS Live, Artemis II, Artemis III maps
- [x] **CREW Tab**: Photo grid with bios and agency badges
- [x] **INFO Tab**: Mission details, news placeholder, events

### Integration Tasks
- [x] Add "Tracking" tab to main app navigation
- [x] Import iss-tracker.js into main app
- [x] Import spacecraft-icons.js and ui-icons.js
- [x] Create TrackingManager with mode switching
- [x] Integrate Artemis II/III orbital diagrams (via iframe)
- [x] WebSocket connection for real-time updates
- [x] Mission selector dropdown
- [x] Notification system

---

## ✅ Phase 3: Component Architecture - COMPLETE

### Orbital Map Components
```
client/js/components/
├── index.js                # Component registry & loader
├── OrbitalMap.js           # Base orbital map class
├── ArtemisIIMap.js         # Free return trajectory (SVG)
├── ArtemisIIIMap.js        # NRHO + lunar landing (SVG)
├── ISSMap.js               # Earth orbit with live tracking
└── MissionMapRouter.js     # Factory for auto-selecting map type
```

### Supported Mission Types
- `artemis-i`, `artemis-ii` → ArtemisIIMap (lunar flyby)
- `artemis-iii`, `artemis-iv`, `artemis-v` → ArtemisIIIMap (lunar landing)
- `iss`, `iss-expedition`, `crew-dragon`, `starliner` → ISSMap (earth orbit)
- `lunar-gateway` → ArtemisIIIMap (NRHO)

---

## ✅ Phase 5: Mission Control Mode - COMPLETE

**Goal:** Create a high-density, ambient display mode for large screens, kiosks, and signage.

### Design Principles
- **No user interaction required** - Auto-rotating, hands-off display
- **Maximum information density** - All critical data visible at once
- **Ambient/always-on** - Suitable for 24/7 display on TVs/monitors
- **Full-screen/kiosk** - No browser chrome, immersive experience

### Mission Control Mode Features

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────────────────┐
│  [NASA] ARTEMIS II                    [LIVE●] Jan 21, 2026 17:45 UTC    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────────────────────────┐  ┌──────────────────────┐ │
│   │                                         │  │   MISSION STATUS     │ │
│   │         T-MINUS COUNTDOWN               │  │                      │ │
│   │                                         │  │   GO FOR LAUNCH      │ │
│   │     015 : 08 : 42 : 17                  │  │                      │ │
│   │                                         │  │   Weather: GO ✓      │ │
│   │     Target: Feb 6, 2026 12:00 UTC       │  │   Vehicle: GO ✓      │ │
│   │     Kennedy Space Center, Pad 39B       │  │   Range: GO ✓        │ │
│   │                                         │  │   Crew: GO ✓         │ │
│   └─────────────────────────────────────────┘  └──────────────────────┘ │
│                                                                          │
│   ┌─────────────────────────────────────────┐  ┌──────────────────────┐ │
│   │            CREW                         │  │   WEATHER            │ │
│   │                                         │  │                      │ │
│   │  [Photo] [Photo] [Photo] [Photo]        │  │   ☀️ Clear           │ │
│   │  Wiseman  Glover   Koch   Hansen        │  │   78°F | Wind: 12mph │ │
│   │   CDR      PLT     MS1     MS2          │  │   Precip: 0%         │ │
│   │                                         │  │   Status: GO         │ │
│   └─────────────────────────────────────────┘  └──────────────────────┘ │
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐│
│   │  TIMELINE  ●━━━━━━○━━━━━○━━━━━○━━━━━○━━━━━○━━━━━○━━━━━○            ││
│   │            FRR  Quarantine  Rollout  WDR  Cryo  Ingress  LAUNCH    ││
│   └─────────────────────────────────────────────────────────────────────┘│
│                                                                          │
│   [NASA TV: Coverage begins T-2:00:00] ─────────────────────────────────│
└─────────────────────────────────────────────────────────────────────────┘
```

#### Implementation Tasks

| Task | Description | Effort | Priority | Status |
|------|-------------|--------|----------|--------|
| Create `mission-control.html` | New standalone page for kiosk mode | 4 hrs | High | ✅ Done |
| Full-screen API | Toggle full-screen with F11 or button | 1 hr | High | ✅ Done |
| Auto-refresh | Continuous data updates without interaction | 2 hrs | High | ✅ Done |
| Large countdown display | Oversized timer for visibility | 2 hrs | High | ✅ Done |
| Status indicators | GO/NO-GO lights for all systems | 2 hrs | High | ✅ Done |
| Crew photo strip | Horizontal crew display with roles | 2 hrs | Medium | ✅ Done |
| Compact weather panel | Weather summary with GO/NO-GO | 1 hr | Medium | ✅ Done |
| Horizontal timeline | Full-width milestone progress (all milestones) | 2 hrs | Medium | ✅ Done |
| Clock/date display | UTC + ET time, MET in header | 1 hr | Low | ✅ Done |
| Mission status box | Status + description info box | 1 hr | Medium | ✅ Done |
| Live stream embed | NASA TV / YouTube embed | 4 hrs | Medium | ✅ Done |
| News ticker | Scrolling news at bottom | 2 hrs | Low | ✅ Done |

#### Technical Requirements
- Standalone HTML file (can run independently)
- No scrolling - all content fits viewport
- CSS Grid for layout (fixed proportions)
- WebSocket for real-time updates
- Full-screen API support
- URL parameter for mission ID: `?mission=artemis-ii`
- Auto-hide cursor after 3 seconds of inactivity

---

## ✅ Phase 4: Backend API Enhancements - COMPLETE

### Implemented Endpoints
| Endpoint | Purpose | Status |
|----------|---------|--------|
| `GET /api/iss` | Combined ISS data (position + crew + telemetry) | ✅ Complete |
| `GET /api/iss/position` | Proxy ISS API (Where The ISS At + Open Notify fallback) | ✅ Complete |
| `GET /api/iss/crew` | Two-phase crew roster (Open Notify + NASA blog enrichment) | ✅ Complete |
| `GET /api/iss/telemetry` | NASA telemetry placeholder (client-side Lightstreamer) | ✅ Complete |
| `GET /api/iss/news` | ISS-specific news (Spaceflight Now + NASA ISS Blog RSS) | ✅ Complete |
| `GET /api/iss/location/{lat},{lng}` | Reverse geocoding via Where The ISS At | ✅ Complete |
| `GET /api/iss/crew/enrichment` | Crew enrichment cache diagnostics | ✅ Complete |
| `GET /api/missions/{id}/trajectory` | Waypoint/path data for trajectory maps | ✅ Complete |
| `GET /api/trajectories` | List all missions with trajectory data | ✅ Complete |
| `GET /api/news` | Aggregated NASA + industry RSS news feeds | ✅ Complete |

### Implementation Details
- **ISS Position**: 3-second cache, auto-fallback to Open Notify if primary fails, stale cache on total failure
- **ISS Crew**: 1-hour cache, Phase 1 (names) + Phase 2 (agency enrichment from NASA blog)
- **Trajectory**: Supports 10 mission IDs via direct match + alias fallback (e.g. crew-dragon → iss profile)
- **General News**: 4 RSS feeds (NASA Breaking, Artemis Blog, ISS Blog, Spaceflight Now), 15-min cache, deduplication, source filtering
- **Server files**: `iss.py`, `crew_enrichment.py`, `trajectories.py`, `news.py`

---

## 🔄 Phase 6: Border System + Theming — IN PROGRESS

### Completed
- [x] ao-frames.css — 4-tier frame hierarchy (page, panel, sub, popup)
- [x] ao-frame-sub.horizontal variant — top stripe for headers/footers/tickers
- [x] Corner border fix — double clip-path technique
- [x] Z-index stack — documented and enforced
- [x] Utility components — .ao-dot, .ao-readout, .ao-divider
- [x] Responsive breakpoints + reduced-motion support
- [x] ao-themes.css — 4 themes (nominal / expanse / hazard / stealth) with --theme-* tokens
- [x] mission.html interior — fully wired to ao-themes.css token system
- [x] crew.html interior — wired to ao-themes.css token system

### Remaining
- [ ] **Fix 3-digit countdown clipping** (ISSUE-003) — DAYS digits clip at 3 chars (e.g. "195")
- [ ] **ISS video auto-load** (ISSUE-004) — auto-load added but not triggering; investigate autoplay policy
- [ ] **Fix default mission selection** (ISSUE-005) — cargo missions outranking crewed on some reloads
- [ ] Apply ao-frame-panel classes to crew.html EVA sidebar (currently inline styles)
- [ ] tracking.html theme wiring (DEFERRED-002) — requires postMessage bridge to inner mockup iframe

---

## 🔲 Phase 7: Offline Support / PWA — NOT STARTED

### Requirements
- Service Worker for offline caching
- IndexedDB for mission data
- Offline detection with UI feedback
- Cache age display
- Background sync when online

---

## 🔲 Phase 8: Mobile UI Mode — NOT STARTED (Low Priority)

### Requirements
- Bottom icon bar navigation
- Swipe gestures between views
- 2-column crew grid
- Pull-to-refresh
- Touch-optimized tracking maps

---

## 📋 Mockups Available

### Ready for Production
| Mockup | File | Use For |
|--------|------|---------|
| Pre-Launch Countdown | `mode1-prelaunch.html` | Mission Control Mode reference |
| Ascent Phase | `mode2-ascent.html` | Post-launch display reference |
| ISS Live Tracker | `mode3-iss-live.html` | ✅ Integrated (EPSG:4326 + NASA GIBS) |
| ISS Layout Mockup | `mode3-layout-mockup.html` | Dual 3D view reference |
| Artemis II Diagram | `mode3-artemis2-nasa-style.html` | ✅ Integrated |
| Artemis III Diagram | `mode3-artemis3-nrho.html` | ✅ Integrated |
| Icon Gallery v7 | `icon-gallery-v7.html` | Reference for spacecraft icons |
| Map Projection Test | `map-epsg4326-test.html` | EPSG:4326 projection demo |

---

## 📁 File Locations

### Client Files
```
client/
├── index.html                    # Iframe shell (primary entry point)
├── index-shell.html              # Second iteration shell
├── index2.html                   # Kiosk mode entry
├── assets/
│   ├── crew/                     # Local astronaut portraits (8 JPEGs)
│   ├── images/                   # Mission hero images
│   ├── logos/                    # Agency logos (NASA SVG, ESA/JAXA/Roscosmos/SpaceX/CSA PNG)
│   ├── patches/                  # Mission patches (Crew-10/11/12, Artemis II/III)
│   └── fonts/                    # Local fonts (Tabler, Spaceicons, pending Orbitron)
├── data/
│   └── spacecraft-manifest.json  # Spacecraft registry for icons/tracking
├── js/
│   ├── iss-tracker.js            # ISS tracking with Leaflet
│   ├── spacecraft-icons.js       # SVG spacecraft icons
│   ├── ui-icons.js               # UI icon library
│   └── components/               # Orbital map components
│       ├── index.js
│       ├── OrbitalMap.js
│       ├── ArtemisIIMap.js
│       ├── ArtemisIIIMap.js
│       ├── ISSMap.js
│       └── MissionMapRouter.js
├── tabs/                         # All UI pages (served via iframe shell)
│   ├── mission.html              # Mission countdown + status + crew strip
│   ├── tracking.html             # Map tracking modes
│   ├── crew.html                 # Astronaut photo grid + bios
│   ├── craft.html                # Spacecraft 3D viewer + specs (ISS/Dragon/Orion)
│   └── ...                       # info, trajectory3d, weather, recovery
└── mockups/                      # Design references
    ├── mode1-prelaunch.html
    ├── mode2-ascent.html
    ├── mode3-iss-live.html       # ISS tracker with dual 3D views
    ├── icon-gallery-v7.html
    └── map-epsg4326-test.html
```

### Server Files
```
server/
├── main.py                       # FastAPI backend (v0.7.0)
├── database.py                   # SQLite operations
├── fetcher.py                    # NASA/ESA API sync
├── weather.py                    # Weather integration
├── iss.py                        # ISS data proxy (position, crew, news)
├── crew_enrichment.py            # ISS crew agency enrichment
├── trajectories.py               # Trajectory waypoint/path data
├── news.py                       # General NASA RSS news aggregation
├── localize_images.py            # Download remote assets to local /assets/
├── fix_bg.py                     # Mission patch background removal
├── requirements.txt              # Python dependencies
└── artemisops.db                 # SQLite database
```

---

## 🔗 External APIs

| API | Purpose | URL |
|-----|---------|-----|
| Space Devs | Mission data | `ll.thespacedevs.com/2.2.0/` |
| Open-Meteo | Weather forecasts | `api.open-meteo.com/v1/` |
| Where The ISS At | ISS position | `api.wheretheiss.at/v1/` |
| Open Notify | ISS crew roster | `api.open-notify.org/` |

## 📚 Reference Sources

| Source | Description | URL |
|--------|-------------|-----|
| NASA Crew Page | Official Artemis crew bios & portraits | https://www.nasa.gov/feature/our-artemis-crew/ |
| NASA Artemis I Tracker | Real-time mission tracking reference (trajectory, telemetry display patterns) | https://www.nasa.gov/missions/artemis/orion/track-nasas-artemis-i-mission-in-real-time/ |
| NAIF/SPICE Frames & Coordinates | JPL tutorial on reference frames and coordinate systems for trajectory work | https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Tutorials/pdf/individual_docs/17_frames_and_coordinate_systems.pdf |
| NASA Shuttle GNC Calculations | Guidance, navigation & control math reference (state vectors, coordinate transforms) | https://www.nasa.gov/pdf/466741main_AP_ST_Calc_ShuttleGNC.pdf |

---

## 📅 Development Timeline

| Week | Focus | Deliverables |
|------|-------|--------------|
| Current | Mission Control Mode | `mission-control.html` basic layout |
| +1 | Mission Control Polish | Full-screen, auto-refresh, live stream |
| +2 | Backend Enhancements | ISS proxy, news feed APIs |
| +3 | Mobile UI | Bottom nav, responsive layouts |
| Future | PWA / Offline | Service worker, IndexedDB |

---

## Notes

### Architecture Decisions
- **Iframe shell consolidation (Feb 11):** All UI pages live in `tabs/*.html`, served through iframe shell (`index.html`). Standalone `mission-control.html` was deleted. No more standalone pages — everything accessed via tabbed shell.
- **Asset localization (Feb 11):** All crew photos, agency logos, mission patches, and hero images are served locally from `/assets/`. Zero remote image fetches for mission data. Supports offline kiosk mode. Only live streams, map tiles, and radar data remain remote by necessity.

### Page Design Intents
Each page follows a "maximize the hero element" philosophy:
- **Mission:** Largest possible countdown clock while maintaining correct space for the live feed panel. Countdown is king.
- **Tracking:** Maximize the tracking map and keep large 3D model views and video panels. Map dominates the layout.
- **Crew:** Maximize astronaut photo size, dynamically scaled based on crew count (e.g. 4 crew = larger cards than 7 crew).
- **Info:** Development paused.

### Design Rules
- **Crew ISS branding:** If missions are CREW missions to ISS, they use the NASA logo instead of SpaceX. Detected by mission name starting with "crew-" or containing "crew dragon".
- **Agency logos:** Served locally as SVG/PNG from `/assets/logos/`. ISS tracker header shows all 5 partner agencies (NASA, ESA, JAXA, CSA, Roscosmos).
- **Fonts:** Orbitron selected for display text. Space Mono + IBM Plex Sans for body. All hosted locally (no CDN) for offline kiosk support.

- Desktop mode is production-ready
- Tracking tab fully functional with live ISS data
- Mission Control mode is next priority
- Consider Raspberry Pi deployment for kiosk displays

**Last Updated:** March 6, 2026
