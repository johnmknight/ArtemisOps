# ArtemisOps - Production Queue & Integration Plan

## Overview
This document tracks development progress and the integration plan for the ArtemisOps application.

**Last Updated:** February 10, 2026

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
| Phase 5 | Mission Control Mode | 🔄 **IN PROGRESS** |
| Phase 6 | Mobile UI Mode | 🔲 Not Started |
| Phase 7 | Offline Support / PWA | 🔲 Not Started |

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

## 🔄 Phase 5: Mission Control Mode - IN PROGRESS

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
| Live stream embed | NASA TV / YouTube embed | 4 hrs | Medium | 🔲 Open |
| News ticker | Scrolling news at bottom | 2 hrs | Low | 🔲 Open |

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

## 🔲 Phase 6: Mobile UI Mode - NOT STARTED

### Requirements
- Bottom icon bar navigation
- Swipe gestures between views
- 2-column crew grid
- Pull-to-refresh
- Touch-optimized tracking maps

---

## 🔲 Phase 7: Offline Support / PWA - NOT STARTED

### Requirements
- Service Worker for offline caching
- IndexedDB for mission data
- Offline detection with UI feedback
- Cache age display
- Background sync when online

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
├── index.html                    # Main desktop app
├── mission-control.html          # ✅ Kiosk/signage mode (standalone)
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
└── mockups/                      # Design references
    ├── mode1-prelaunch.html
    ├── mode2-ascent.html
    ├── mode3-*.html
    ├── icon-gallery-v7.html      # Final icon references
    └── map-epsg4326-test.html    # Projection test
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

- Desktop mode is production-ready
- Tracking tab fully functional with live ISS data
- Mission Control mode is next priority
- Consider Raspberry Pi deployment for kiosk displays

**Last Updated:** February 10, 2026
