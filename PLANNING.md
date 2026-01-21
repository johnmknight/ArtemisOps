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
| **Desktop** | Laptops/monitors | Full-featured, keyboard/mouse optimized, tabbed layout, no scrolling |
| **Mission Control** | Large displays/kiosks/signage | High-density data, no interaction needed, ambient display |

### Mode-Specific Features
- **Notifications**: Mobile only
- **Touch optimization**: Mobile priority
- **Information density**: Mission Control > Desktop > Mobile
- **Live stream embed**: Mission Control only (enabled by default)
- **Upcoming live events**: All modes (with clickable URLs)

---

## Desktop UI Mode Design

### Layout Principles
- **No scrolling** - All content fits within viewport
- **Tabbed navigation** - 3 main tabs to organize content
- **Full-height panels** - Content fills available vertical space
- **Responsive within bounds** - Adapts to different desktop sizes (1280px - 1920px+)

### Tab Structure

#### Tab 1: MISSION (Default)
Primary mission dashboard - the "at a glance" view

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] ARTEMIS II [Patch]     [Mission Selector] [🔔]      │
├─────────────────────────────────────────────────────────────┤
│  [ MISSION ]  [ CREW ]  [ INFO ]                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │           T-MINUS · COUNTDOWN TO LAUNCH             │   │
│   │              045 : 12 : 34 : 56                     │   │
│   │         Target Launch: April 1, 2026 | KSC          │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   ┌───────────────────────┐  ┌──────────────────────────┐   │
│   │   🚀 LAUNCH WEATHER   │  │     MISSION STATUS       │   │
│   │   ☀️ Clear Sky        │  │                          │   │
│   │   High: 78°F  GO      │  │  Artemis II is in final  │   │
│   │   Wind: 12 mph        │  │  preparations...         │   │
│   │   Precip: 0.0mm       │  │                          │   │
│   │                       │  │  NEXT: Rollout to Pad    │   │
│   └───────────────────────┘  └──────────────────────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  ○────●────○────○────○────○────○────○  TIMELINE     │   │
│   │  FRR  Quarantine  Checks  Rollout  WDR  ...         │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Components:
- Countdown timer (prominent, centered)
- Weather panel (left column)
- Mission status + next milestone (right column)
- Timeline (bottom, horizontal, compact)

#### Tab 2: CREW
Crew roster with photos and bios

```
┌─────────────────────────────────────────────────────────────┐
│  [ MISSION ]  [ CREW ]  [ INFO ]                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │  Photo   │  │  Photo   │  │  Photo   │  │  Photo   │   │
│   │          │  │          │  │          │  │          │   │
│   │ REID     │  │ VICTOR   │  │ CHRISTINA│  │ JEREMY   │   │
│   │ WISEMAN  │  │ GLOVER   │  │ KOCH     │  │ HANSEN   │   │
│   │          │  │          │  │          │  │          │   │
│   │Commander │  │ Pilot    │  │ Mission  │  │ Mission  │   │
│   │          │  │          │  │Specialist │  │Specialist │   │
│   │   NASA   │  │   NASA   │  │   NASA   │  │   CSA    │   │
│   │          │  │          │  │          │  │          │   │
│   │  Bio text│  │  Bio text│  │  Bio text│  │  Bio text│   │
│   │  ...     │  │  ...     │  │  ...     │  │  ...     │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Components:
- 4-column grid for crew cards
- Larger photos than current design
- Full bio visible (no truncation)
- Agency badges

#### Tab 3: INFO
Mission details, news, and additional information

```
┌─────────────────────────────────────────────────────────────┐
│  [ MISSION ]  [ CREW ]  [ INFO ]                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────┐  ┌──────────────────────────┐ │
│   │    MISSION DETAILS      │  │      LATEST NEWS         │ │
│   │                         │  │                          │ │
│   │  Vehicle: SLS Block 1   │  │  🔗 NASA Blog Update     │ │
│   │  Spacecraft: Orion      │  │     Jan 15, 2026         │ │
│   │  Duration: ~10 days     │  │                          │ │
│   │  Destination: Lunar     │  │  🔗 Press Conference     │ │
│   │    Free Return          │  │     Jan 12, 2026         │ │
│   │                         │  │                          │ │
│   │  Agencies: NASA, CSA    │  │  🔗 Crew Interview       │ │
│   │                         │  │     Jan 10, 2026         │ │
│   │  Launch Site: KSC       │  │                          │ │
│   │    Pad 39B              │  │                          │ │
│   │                         │  │                          │ │
│   └─────────────────────────┘  └──────────────────────────┘ │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              UPCOMING LIVE EVENTS                    │   │
│   │  📺 Pre-launch Press Conf  |  Jan 25  |  Watch →    │   │
│   │  📺 Launch Coverage        |  Apr 1   |  Watch →    │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Components:
- Mission details panel (rocket, spacecraft, agencies, etc.)
- News/updates feed (links to NASA blogs, press releases)
- Upcoming live events with watch links

### Visual Design
- Tab bar: Horizontal, below header, with active indicator
- Active tab: Highlighted with glow effect, underline
- Inactive tabs: Dimmed, hover effect
- Content area: Fixed height, no overflow scroll on body
- Panels: Can have internal scroll if needed (crew bios, news)

### Keyboard Navigation (Desktop only)
- `1`, `2`, `3` - Switch views
- `←` `→` - Navigate between views
- `Space` - Toggle weather panel (when on Mission view)

---

## Mobile UI Mode Design

### Layout Principles
- **No scrolling** - Same as desktop, content fits within viewport
- **Bottom icon bar** - Fixed navigation (thumb-friendly, always visible)
- **Same 3 views** - Mission, Crew, Info (identical content to desktop)
- **Touch optimized** - Larger tap targets, swipe between views

### Navigation: Bottom Icon Bar

```
┌─────────────────────────────────┐
│                                 │
│      [ Active View Content ]    │
│                                 │
├─────────────────────────────────┤
│   🚀        👨‍🚀        ℹ️       │
│ Mission    Crew      Info       │
└─────────────────────────────────┘
```

| Icon | Label | Content |
|------|-------|---------|
| 🚀 | Mission | Countdown, Weather, Status, Timeline |
| 👨‍🚀 | Crew | Crew roster cards (2-column grid) |
| ℹ️ | Info | Mission details, News, Live Events |

### Touch Gestures
- **Swipe left/right** - Switch between views
- **Tap icon** - Jump to view
- **Pull down** - Refresh data (on Mission view)

---

## Shared View Architecture

Desktop tabs and Mobile icon bar share the same underlying view system:

```
ViewManager
├── View: MISSION
│   ├── CountdownComponent
│   ├── WeatherComponent  
│   ├── StatusComponent
│   └── TimelineComponent
│
├── View: CREW
│   └── CrewGridComponent (4-col desktop, 2-col mobile)
│
└── View: INFO
    ├── MissionDetailsComponent
    ├── NewsFeedComponent
    └── LiveEventsComponent
```

### Responsive Breakpoints
| Breakpoint | Mode | Navigation |
|------------|------|------------|
| < 768px | Mobile | Bottom icon bar |
| ≥ 768px | Desktop | Top tab bar |

### CSS Strategy
- Shared `.view-panel` class for all views
- `.view-panel.active` shows current view
- Desktop: `.tab-nav` visible, `.icon-bar` hidden
- Mobile: `.icon-bar` visible, `.tab-nav` hidden
- Components use same classes, layout adapts via media queries

### ViewManager (JavaScript)
```javascript
const ViewManager = {
  currentView: 'mission',
  views: ['mission', 'crew', 'info'],
  
  switchView(viewId) {
    // Hide all views, show selected
    // Update both tab-nav and icon-bar active states
    // Save to localStorage
  },
  
  init() {
    // Keyboard nav (desktop): 1, 2, 3 and arrow keys
    // Swipe gestures (mobile): left/right
    // Load saved view preference
  }
};
```

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
