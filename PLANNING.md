# ArtemisOps - Feature Planning & Architecture

**Last Updated:** January 21, 2026

## Overview

ArtemisOps is a mission clock and status tracking application for NASA, ESA, and commercial crewed space missions. It provides real-time countdown timers, crew information, weather data, mission milestones, and orbital tracking visualizations.

---

## Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ARTEMISOPS                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    WebSocket     ┌──────────────────────────────┐ │
│  │   WEB CLIENT     │◄────────────────►│      PYTHON SERVER           │ │
│  │                  │    REST API      │      (FastAPI v0.5.0)        │ │
│  │  ┌────────────┐  │◄────────────────►│                              │ │
│  │  │  Desktop   │  │                  │  ┌─────────┐  ┌───────────┐  │ │
│  │  │   Mode ✅  │  │                  │  │ SQLite  │  │ Scheduler │  │ │
│  │  ├────────────┤  │                  │  │   DB    │  │ (Hourly)  │  │ │
│  │  │  Mission   │  │                  │  └─────────┘  └───────────┘  │ │
│  │  │  Control🔄 │  │                  │                              │ │
│  │  ├────────────┤  │                  └──────────────────────────────┘ │
│  │  │  Mobile 🔲 │  │                              │                     │
│  │  └────────────┘  │                              ▼                     │
│  └──────────────────┘                  ┌──────────────────────────────┐ │
│                                        │     EXTERNAL APIs            │ │
│                                        │  • Space Devs (missions)     │ │
│                                        │  • Open-Meteo (weather)      │ │
│                                        │  • Where The ISS At          │ │
│                                        │  • Open Notify (ISS crew)    │ │
│                                        └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Server (Python - FastAPI)
- ✅ API backend for mission data
- ✅ Data caching and aggregation
- ✅ WebSocket support for real-time updates
- ✅ Scheduled data fetching from NASA/Space APIs
- ✅ Weather integration with launch viability analysis

### Client (Web - Vanilla JS)
- ✅ Desktop mode with tabbed interface
- 🔄 Mission Control mode for kiosks/signage
- 🔲 Mobile mode with bottom navigation

---

## UI Modes

| Mode | Target | Status | Key Features |
|------|--------|--------|--------------|
| **Desktop** | Laptops/monitors | ✅ Complete | Tabbed layout, keyboard nav, full features |
| **Mission Control** | Large displays/kiosks | 🔄 In Progress | High-density, no interaction, ambient |
| **Mobile** | Phones | 🔲 Planned | Bottom nav, touch-optimized, compact |

---

## Desktop Mode (Complete ✅)

### Tab Structure
| Tab | Content | Status |
|-----|---------|--------|
| MISSION | Countdown, Weather, Status, Timeline | ✅ |
| TRACKING | ISS Live, Artemis II/III orbital maps | ✅ |
| CREW | Photo grid with bios, agency badges | ✅ |
| INFO | Mission details, news, live events | ✅ |

### Features Implemented
- [x] Real-time countdown with T-plus mode
- [x] Weather panel (auto-show on launch day)
- [x] Mission timeline with milestones
- [x] Crew information with photos
- [x] Mission selector dropdown
- [x] Notification system with sound
- [x] WebSocket real-time updates
- [x] ISS live tracking with Leaflet
- [x] Artemis II/III orbital diagrams

---

## Mission Control Mode (In Progress 🔄)

### Purpose
Ambient, always-on display for:
- Mission operations centers
- Museum/visitor center kiosks
- Home "space enthusiast" displays
- Raspberry Pi signage projects

### Design Principles
- **No interaction required** - Hands-off, auto-updating
- **Maximum density** - All key data visible at once
- **Always-on ready** - No screensaver interruption
- **Full-screen** - Immersive, no browser chrome

### Layout Design
```
┌─────────────────────────────────────────────────────────────────────────┐
│ [NASA] ARTEMIS II - First Crewed Lunar Mission    [●LIVE] 17:45:32 UTC  │
├───────────────────────────────────────────┬─────────────────────────────┤
│                                           │                             │
│        T - M I N U S                      │     MISSION STATUS          │
│                                           │                             │
│    0 1 5 : 0 8 : 4 2 : 1 7               │     ● GO FOR LAUNCH         │
│    DAYS   HRS   MIN   SEC                 │                             │
│                                           │     Weather    [GO] ✓       │
│    Target: Feb 6, 2026 12:00 UTC          │     Vehicle    [GO] ✓       │
│    Kennedy Space Center, Pad 39B          │     Range      [GO] ✓       │
│                                           │     Crew       [GO] ✓       │
├───────────────────────────────────────────┼─────────────────────────────┤
│                                           │                             │
│     CREW                                  │     WEATHER @ KSC           │
│                                           │                             │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐             │     ☀️ Clear Skies          │
│  │ 👨 │ │ 👨 │ │ 👩 │ │ 👨 │             │     Temp: 78°F (26°C)       │
│  └────┘ └────┘ └────┘ └────┘             │     Wind: 12 mph NE         │
│  Wiseman Glover  Koch  Hansen             │     Precip: 0%              │
│    CDR    PLT    MS1    MS2               │     Humidity: 45%           │
│                                           │                             │
├───────────────────────────────────────────┴─────────────────────────────┤
│                                                                          │
│  TIMELINE ━━━━●━━━━━━━━━○━━━━━━━━━○━━━━━━━━━○━━━━━━━━━○━━━━━━━━━▷       │
│              FRR     Rollout     WDR      Cryo    Ingress  LAUNCH       │
│            ✓ Done    Jan 24    Jan 27    T-6:40   T-2:35   T-0:00       │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│  📺 NASA TV: Launch coverage begins at T-2:00:00  |  Watch Live →       │
└──────────────────────────────────────────────────────────────────────────┘
```

### Implementation Plan

#### Phase 5a: Basic Layout (Priority: High)
- [ ] Create `mission-control.html` standalone file
- [ ] CSS Grid layout with fixed proportions
- [ ] Large countdown display (readable from 10+ feet)
- [ ] GO/NO-GO status indicators
- [ ] Compact crew strip with photos
- [ ] Weather summary panel
- [ ] Horizontal timeline

#### Phase 5b: Interactivity (Priority: Medium)
- [ ] Full-screen API toggle (F11 or button)
- [ ] WebSocket connection for live data
- [ ] Auto-refresh without user action
- [ ] URL parameter: `?mission=artemis-ii`
- [ ] Auto-hide cursor after inactivity

#### Phase 5c: Enhanced Features (Priority: Low)
- [ ] NASA TV / YouTube live embed
- [ ] Auto-rotate between views
- [ ] News ticker at bottom
- [ ] Multiple theme options (dark/light/NASA blue)

---

## Mobile Mode (Planned 🔲)

### Design Principles
- **Bottom navigation** - Thumb-friendly icon bar
- **No scrolling** - Content fits viewport
- **Touch optimized** - Large tap targets
- **Swipe gestures** - Navigate between views

### Navigation
```
┌─────────────────────────────────┐
│                                 │
│      [ Active View Content ]    │
│                                 │
├─────────────────────────────────┤
│   🚀        🛰️       👨‍🚀       ℹ️  │
│ Mission  Tracking  Crew    Info │
└─────────────────────────────────┘
```

### Implementation Tasks
- [ ] Bottom icon bar component
- [ ] Swipe gesture detection
- [ ] 2-column crew grid
- [ ] Compact tracking view
- [ ] Pull-to-refresh
- [ ] Touch-friendly controls

---

## API Endpoints

### Current (v0.5.0)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/missions` | GET | List all active missions |
| `/api/missions/{id}` | GET | Full mission with crew & milestones |
| `/api/missions/{id}/weather` | GET | Weather forecast (7-day window) |
| `/api/missions/{id}/weather/launch-day` | GET | Launch day weather only |
| `/api/weather/{site}` | GET | Any launch site weather |
| `/api/status` | GET | Server health check |
| `/api/sync` | POST | Manual data refresh |
| `/ws` | WebSocket | Real-time updates |

### Planned
| Endpoint | Method | Description | Priority |
|----------|--------|-------------|----------|
| `/api/iss/position` | GET | ISS position proxy (CORS) | Medium |
| `/api/iss/crew` | GET | Cached ISS crew roster | Medium |
| `/api/missions/{id}/trajectory` | GET | Trajectory waypoints | Low |
| `/api/news` | GET | NASA RSS aggregation | Low |

---

## Technology Stack

### Backend
- Python 3.12+
- FastAPI + Uvicorn
- SQLite + aiosqlite
- APScheduler (hourly sync)
- httpx (async HTTP client)

### Frontend
- Vanilla JavaScript (no framework)
- Leaflet.js (maps)
- CSS Grid/Flexbox
- WebSocket API

### External Services
- Space Devs Launch Library 2 API
- Open-Meteo Weather API
- Where The ISS At API
- Open Notify API

---

## Deployment Options

### Development
```bash
cd server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
# Open http://localhost:8080
```

### Raspberry Pi Kiosk
```bash
# Clone and setup
git clone https://github.com/johnmknight/ArtemisOps.git
cd ArtemisOps/server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in background
nohup python main.py &

# Open Chromium in kiosk mode
chromium-browser --kiosk http://localhost:8080/mission-control.html
```

### Docker (Future)
```dockerfile
# Planned for easier deployment
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r server/requirements.txt
EXPOSE 8080
CMD ["python", "server/main.py"]
```

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| Jan 21, 2026 | 0.5.0 | Desktop mode complete, Tracking tab integrated |
| Jan 21, 2026 | - | Documentation updated, Mission Control prioritized |
