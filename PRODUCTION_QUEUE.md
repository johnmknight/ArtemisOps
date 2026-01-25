# ArtemisOps - Production Queue & Integration Plan

## Overview
This document tracks development progress and the integration plan for the ArtemisOps application.

**Last Updated:** January 25, 2026

---

## 🎯 Current Sprint - Active Work

### Recently Completed (Jan 25)
- [x] Switch ISS tracker map to EPSG:4326 Equirectangular projection (NASA Mission Control style)
- [x] Integrate NASA GIBS Blue Marble satellite tiles
- [x] Add lat/lon grid lines overlay (30° intervals)
- [x] Enable fractional zoom for optimal map fill
- [x] Fix tile wrapping (no duplicate world maps)
- [x] Add spacecraft manifest data file (`client/data/spacecraft-manifest.json`)

### In Progress
- [ ] **Update ISS map icon** - Replace current icon with icon gallery style
- [ ] **Finish 3D ISS view updates** - Camera angles, dual-view layout (NASA reference)
- [ ] **Implement dual 3D panel layout** - Side-by-side orthogonal ISS views

### Up Next
- [ ] Add orbit track rendering (sinusoidal curves in equirectangular projection)
- [ ] Implement ground station visibility overlays
- [ ] Add day/night terminator line to map

---

## 📊 Current Status Summary

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | ISS Tracker + Icons + Backend | ✅ Complete |
| Phase 2 | Main App Integration | ✅ Complete |
| Phase 3 | Component Architecture | ✅ Complete |
| Phase 4 | Backend API Enhancements | 🔲 Not Started |
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

| Task | Description | Effort | Priority |
|------|-------------|--------|----------|
| Create `mission-control.html` | New standalone page for kiosk mode | 4 hrs | High |
| Full-screen API | Toggle full-screen with F11 or button | 1 hr | High |
| Auto-refresh | Continuous data updates without interaction | 2 hrs | High |
| Large countdown display | Oversized timer for visibility | 2 hrs | High |
| Status indicators | GO/NO-GO lights for all systems | 2 hrs | High |
| Crew photo strip | Horizontal crew display with roles | 2 hrs | Medium |
| Compact weather panel | Weather summary with GO/NO-GO | 1 hr | Medium |
| Horizontal timeline | Full-width milestone progress | 2 hrs | Medium |
| Live stream embed | NASA TV / YouTube embed | 4 hrs | Medium |
| Auto-rotate views | Cycle countdown → tracking → crew | 3 hrs | Low |
| News ticker | Scrolling news at bottom | 2 hrs | Low |
| Clock/date display | Current UTC time in header | 1 hr | Low |

#### Technical Requirements
- Standalone HTML file (can run independently)
- No scrolling - all content fits viewport
- CSS Grid for layout (fixed proportions)
- WebSocket for real-time updates
- Full-screen API support
- URL parameter for mission ID: `?mission=artemis-ii`
- Auto-hide cursor after 3 seconds of inactivity

---

## 🔲 Phase 4: Backend API Enhancements - NOT STARTED

### Planned Endpoints
| Endpoint | Purpose | Effort |
|----------|---------|--------|
| `GET /api/iss/position` | Proxy ISS API to avoid CORS | 2 hrs |
| `GET /api/iss/crew` | Cached ISS crew roster | 2 hrs |
| `GET /api/missions/{id}/trajectory` | Waypoint/path data for maps | 4 hrs |
| `GET /api/news` | NASA RSS feed aggregation | 4 hrs |

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
├── mission-control.html          # 🔄 NEW: Kiosk/signage mode
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
├── main.py                       # FastAPI backend (v0.5.0)
├── database.py                   # SQLite operations
├── fetcher.py                    # NASA/ESA API sync
├── weather.py                    # Weather integration
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
