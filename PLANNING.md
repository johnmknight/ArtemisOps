# ArtemisOps - Feature Planning

## Architecture

### Server (Python)
- API backend for mission data
- Data caching and aggregation
- WebSocket support for real-time updates
- Scheduled data fetching from NASA/Space APIs

### Client (Web)
- Three UI modes based on viewport/device
- Shared core logic, mode-specific layouts

---

## UI Modes

| Mode | Target | Key Characteristics |
|------|--------|---------------------|
| **Mobile** | Phones | Compact, touch-friendly, notifications enabled |
| **Desktop** | Laptops/monitors | Full-featured, keyboard/mouse optimized |
| **Mission Control** | Large displays/kiosks/signage | High-density data, no interaction needed, ambient display |

### Mode-Specific Features
- **Notifications**: Mobile only
- **Touch optimization**: Mobile priority
- **Information density**: Mission Control > Desktop > Mobile
- **Live stream embed**: Mission Control only (enabled by default)
- **Upcoming live events**: All modes (with clickable URLs)

---

## Offline Mode

### Requirements
- Detect network status (online/offline)
- Cache mission data locally (localStorage/IndexedDB)
- Graceful degradation when offline
- Minimal, non-intrusive status indicators

### Status Indicators
| State | Indicator |
|-------|-----------|
| Live | Subtle "live" indicator (current green dot) |
| Cached | Small "cached" label, timestamp of last update |
| Offline | Brief toast on transition, subtle offline icon |

### Behavior
- No disruptive banners or modals
- Auto-reconnect silently
- Show data age when using cache

---

## Future Features (Unprioritized)

### Core Architecture
- [ ] Server/client architecture (Python backend)
- [ ] Real-time WebSocket updates
- [ ] Offline caching
- [ ] Network status handling (minimal UI feedback)

### UI Modes
- [ ] Mobile UI mode
- [ ] Desktop UI mode  
- [ ] Mission Control UI mode

### Mission Selection
- [ ] Multi-mission support (select which mission to display, one at a time)
- [ ] Mission switcher UI
- [ ] Per-mission data/config

### Notifications & Alerts
- [ ] Mobile push notifications
- [ ] Audio alerts (configurable)

### Content Panels
- [ ] Crew information panel
- [ ] Weather data integration
- [ ] Telemetry simulation

### Live Coverage (NASA/YouTube)
- [ ] Embedded live stream player (Mission Control mode, enabled by default)
- [ ] Auto-detect relevant live streams (launches, spacewalks, etc.)
- [ ] Smart stream matching (find correct video for current mission/event)
- [ ] Upcoming live events panel (all UI modes)
- [ ] Clickable URLs to live coverage
- [ ] Live event schedule/calendar

### Mission Visualization
- [ ] Graphical Earth/Moon orbit map with real-time position tracking
- [ ] Visually accurate (not to scale) orbital representation
- [ ] Inspirational concept images TBD
- [ ] *Low priority, high effort*

### Other
- [ ] Customizable dashboard widgets

---

## Priority Matrix

*To be determined*

| Priority | Feature | Effort | Impact |
|----------|---------|--------|--------|
| | | | |

---

## Notes

- Current app is single HTML file with vanilla JS
- Will need to restructure for client/server split
- Consider: Vite for client build, FastAPI/Flask for server
