# ArtemisOps - Production Queue & Integration Plan

## Overview
This document tracks the mockups ready for production and the integration plan for the main application.

**Last Updated:** January 2026

---

## 📋 Mockups Ready for Production

### Mode 3 - Mission Tracking (Orbital Maps)

| Mockup | File | Status | Priority |
|--------|------|--------|----------|
| Artemis II (Free Return) | `mode3-artemis2-nasa-style.html` | ✅ Ready | High |
| Artemis III (NRHO + Landing) | `mode3-artemis3-nrho.html` | ✅ Ready | High |
| ISS Live Tracker | `mode3-iss-live.html` | ✅ Ready | High |
| ISS / Earth Orbit (legacy) | `mode3-iss-earth-orbit.html` | ⚠️ Superseded by iss-live | Low |

### Mode 1 - Pre-Launch / Countdown
| Mockup | File | Status | Priority |
|--------|------|--------|----------|
| Pre-Launch Countdown | `mode1-prelaunch.html` | ✅ Ready | Medium |
| Pre-Launch v1 | `mode1-prelaunch_1.html` | ⚠️ Archive | Low |
| Pre-Launch v2 | `mode1-prelaunch_2.html` | ⚠️ Archive | Low |

### Mode 2 - Post-Launch / Ascent
| Mockup | File | Status | Priority |
|--------|------|--------|----------|
| Ascent Phase | `mode2-ascent.html` | ✅ Ready | Medium |

### Supporting Assets
| Asset | File | Status |
|-------|------|--------|
| Icon Library | `icon-library.html` | ✅ Complete |
| Icon Gallery v2-v7 | `icon-gallery-v*.html` | ✅ Archive/Reference |
| ISS Icon Demo | `iss-icon.html` | ✅ Complete |
| Starship HLS Icon Demo | `starship-hls-icon.html` | ✅ Complete |

---

## ✅ Completed Components

### Phase 1: ISS Tracker Implementation - COMPLETE ✅

**Status:** Fully implemented and tested

#### Completed Features:
- [x] Real-time ISS position on world map (Leaflet.js)
- [x] Ground track (orbit path preview)
- [x] ISS footprint circle (visibility area)
- [x] Position data overlay (lat, lon, alt, velocity)
- [x] Auto-refresh every 5 seconds
- [x] Crew roster integration (Open Notify API)
- [x] Location name reverse geocoding
- [x] Toggle controls for footprint/track visibility

#### Implementation Files:
```
client/
├── js/
│   └── iss-tracker.js          # ✅ ISS tracking class with Leaflet
└── mockups/
    └── mode3-iss-live.html     # ✅ Full working demo
```

#### APIs Used:
1. **Where The ISS At API** (Primary)
   - Endpoint: `https://api.wheretheiss.at/v1/satellites/25544`
   - Returns: latitude, longitude, altitude, velocity, visibility, footprint
   
2. **Open Notify API** (Fallback + Crew)
   - Position: `http://api.open-notify.org/iss-now.json`
   - Crew: `http://api.open-notify.org/astros.json`

---

### Icon Libraries - COMPLETE ✅

#### Spacecraft Icons (`client/js/spacecraft-icons.js`)
Full SVG icon library for mission spacecraft:
- [x] ISS - International Space Station
- [x] Orion - Crew Module
- [x] Orion-ESM - With European Service Module
- [x] Starship HLS - SpaceX Human Landing System
- [x] Crew Dragon - SpaceX capsule
- [x] Lunar Lander - Apollo-style
- [x] SLS - Space Launch System

#### UI Icons (`client/js/ui-icons.js`)
Complete icon set for application UI (40+ icons):
- [x] Navigation: mission, crew, info, timeline
- [x] Status: countdown, weather, status, notification
- [x] Actions: settings, live, news, event, video, link
- [x] Indicators: check, warning, alert, success
- [x] Space: orbit, moon, earth, vehicle, antenna
- [x] Milestones: complete, active, pending

---

### Server Backend - COMPLETE ✅

**Version:** 0.5.0

#### Features:
- [x] FastAPI server with async support
- [x] WebSocket for real-time updates
- [x] Multi-mission support
- [x] SQLite database with migrations
- [x] Hourly data sync from NASA/ESA APIs
- [x] Weather integration for launch sites
- [x] Mission patches and agency logos

#### Endpoints:
```
GET  /api/missions                    # List all missions
GET  /api/missions/{id}               # Mission details + crew + milestones
GET  /api/missions/{id}/weather       # Weather forecast
GET  /api/missions/{id}/weather/launch-day  # Launch day weather
GET  /api/weather/{site_name}         # Site-specific weather
GET  /api/status                      # Server status
POST /api/sync                        # Manual sync trigger
WS   /ws                              # WebSocket connection
```

---

## 🛠️ Remaining Integration Tasks

### Phase 2: Main Application Integration (IN PROGRESS)

**Goal:** Integrate completed components into the main ArtemisOps application.

#### Tasks:
1. [x] ISS Tracker module ready
2. [x] Icon libraries ready
3. [ ] Add "Tracking" tab to main app navigation
4. [ ] Import iss-tracker.js into main app
5. [ ] Import icon libraries into main app
6. [x] Create mission type router for orbital maps ✅
7. [ ] Integrate Artemis II/III orbital diagrams

#### UI Changes to main `index.html`:
```html
<!-- Add Leaflet CSS/JS -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- Add local scripts -->
<script src="js/spacecraft-icons.js"></script>
<script src="js/ui-icons.js"></script>
<script src="js/iss-tracker.js"></script>

<!-- Add to tab navigation -->
<button class="tab-btn" data-panel="tracking" onclick="ViewManager.switchPanel('tracking')">
  <span class="tab-icon">🛰️</span> TRACKING
</button>

<!-- Add tracking panel -->
<div class="tab-panel tracking-tab" id="panel-tracking">
  <div id="tracking-container"></div>
</div>
```

---

### Phase 3: Component Architecture - COMPLETE ✅

**Goal:** Create reusable orbital map components for different mission types.

**Status:** Fully implemented!

#### Implemented Structure:
```
client/js/components/
├── index.js                # ✅ Component registry & loader
├── OrbitalMap.js           # ✅ Base orbital map class
├── ArtemisIIMap.js         # ✅ Free return trajectory (SVG)
├── ArtemisIIIMap.js        # ✅ NRHO + lunar landing (SVG)
├── ISSMap.js               # ✅ Earth orbit with live tracking (Leaflet)
└── MissionMapRouter.js     # ✅ Factory for auto-selecting map type
```

#### Component Features:
- **OrbitalMap** (base class): Common functionality, event system, theming
- **ArtemisIIMap**: 15 waypoints, TLI/flyby/return trajectory, animated spacecraft
- **ArtemisIIIMap**: NRHO orbit, HLS descent/ascent paths, lunar landing site
- **ISSMap**: Real-time Leaflet tracking, ground track, footprint, crew roster
- **MissionMapRouter**: Auto-selects component based on mission type

#### Usage Example:
```javascript
// Quick start with router
const map = await MissionMapRouter.createAndInit('container', 'artemis-ii');

// Or create directly
const issMap = new ISSMap('iss-container');
await issMap.init();

// Mission type detection works with variations
MissionMapRouter.createMap('c', 'Artemis III');  // → ArtemisIIIMap
MissionMapRouter.createMap('c', 'iss');          // → ISSMap
MissionMapRouter.createMap('c', 'crew-dragon');  // → ISSMap (earth orbit)
```

#### Supported Mission Types:
```javascript
const MISSION_TYPES = {
  'artemis-i': 'lunar-flyby',       // ArtemisIIMap
  'artemis-ii': 'lunar-flyby',      // ArtemisIIMap
  'artemis-iii': 'lunar-landing',   // ArtemisIIIMap
  'artemis-iv': 'lunar-landing',    // ArtemisIIIMap
  'artemis-v': 'lunar-landing',     // ArtemisIIIMap
  'iss-expedition': 'earth-orbit',  // ISSMap (live)
  'iss': 'earth-orbit',             // ISSMap (live)
  'crew-dragon': 'earth-orbit',     // ISSMap
  'starliner': 'earth-orbit',       // ISSMap
  'lunar-gateway': 'nrho',          // ArtemisIIIMap
};
```

---

### Phase 4: Backend API Updates (FUTURE)

**Goal:** Add endpoints to support orbital tracking features.

#### Planned Endpoints:
```
GET /api/missions/{id}/trajectory
  - Returns mission trajectory data (waypoints, paths, current position)

GET /api/missions/{id}/position
  - Returns current spacecraft position (for active missions)

GET /api/iss/position
  - Proxies ISS APIs (to avoid CORS issues)

GET /api/iss/crew
  - Returns current ISS crew roster with caching
```

---

## 📅 Timeline

| Phase | Task | Est. Time | Status |
|-------|------|-----------|--------|
| 1 | ISS Tracker Implementation | 2-3 days | ✅ Complete |
| 1b | Icon Libraries | 1 day | ✅ Complete |
| 1c | Server Backend v0.5 | 3-4 days | ✅ Complete |
| 2 | Main App Integration | 1-2 days | 🔄 In Progress |
| 3 | Component Architecture | 1-2 days | ✅ Complete |
| 4 | Backend API Updates | 1 day | 🔲 Not Started |

---

## 🎨 Design System Reference

### Colors (from mockups)
```css
--bg-primary: #0a1628;
--bg-panel: #0d1a2d;
--border-color: #1a3a5c;
--text-primary: #ffffff;
--text-secondary: #8b949e;
--text-accent: #00d4ff;
--success-color: #7ed321;
--warning-color: #f5a623;
--danger-color: #ff3b30;
--trajectory-outbound: #00bcd4;
--trajectory-return: #8bc34a;
--trajectory-nrho: #9c27b0;
--trajectory-descent: #ff9800;
--waypoint-active: #ffd60a;
```

### Typography
- Headers: Inter / system fonts
- Data/Monospace: Courier New
- Labels: 0.65-0.75rem, letter-spacing: 1-2px

---

## 📁 File Locations

### JavaScript Modules
```
C:\Users\john_\dev\ArtemisOps\client\js\
├── iss-tracker.js          # ✅ ISS tracking with Leaflet
├── spacecraft-icons.js     # ✅ SVG spacecraft icons
└── ui-icons.js             # ✅ UI icon library
```

### Mockups
```
C:\Users\john_\dev\ArtemisOps\client\mockups\
├── index.html                      # Mockup index
├── mode1-prelaunch.html            # Pre-launch countdown
├── mode2-ascent.html               # Ascent phase
├── mode3-artemis2-nasa-style.html  # Artemis II (FREE RETURN) ⭐
├── mode3-artemis3-nrho.html        # Artemis III (NRHO + LANDING) ⭐
├── mode3-iss-live.html             # ISS Live Tracker ⭐ NEW
├── mode3-iss-earth-orbit.html      # ISS (legacy/embedded)
├── mode3-tracking.html             # v1 original (archive)
├── mode3-tracking-v2.html          # v2 technical (archive)
├── mode3-tracking-v3.html          # v3 NASA profile (archive)
├── icon-library.html               # Full icon showcase
└── icon-gallery-v*.html            # Icon iterations (archive)
```

### Server
```
C:\Users\john_\dev\ArtemisOps\server\
├── main.py                 # FastAPI backend v0.5.0
├── database.py             # SQLite operations
├── fetcher.py              # NASA/ESA API sync
├── weather.py              # Weather integration
├── artemisops.db           # SQLite database
└── requirements.txt        # Python dependencies
```

---

## 🔗 External Resources

### APIs
- Open Notify ISS: http://api.open-notify.org/
- Where The ISS At: https://wheretheiss.at/w/developer
- N2YO Satellite API: https://www.n2yo.com/api/

### Libraries
- Leaflet.js: https://leafletjs.com/ (v1.9.4)
- D3.js (for SVG orbital diagrams): https://d3js.org/

### NASA Reference
- Artemis II Mission Profile: https://www.nasa.gov/artemis-ii
- Artemis III Mission Profile: https://www.nasa.gov/artemis-iii
- ISS Tracker: https://spotthestation.nasa.gov/

---

## Notes

- ~~The ISS tracker mockup currently attempts to embed ESA's tracker which is blocked by CORS/iframe policies~~ **RESOLVED**: Custom Leaflet-based tracker implemented
- ~~We need to build our own tracker using the free APIs listed above~~ **DONE**
- The orbital SVG diagrams in the Artemis mockups are self-contained and ready for integration
- Consider using WebSocket for real-time position updates in production
- Icon libraries support multiple sizes and colors for responsive design
