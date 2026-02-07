# ArtemisOps

Mission clock and status tracking app for NASA and ESA crewed space missions.

## Features

- **Multi-Mission Support**: Track multiple missions including Artemis, Commercial Crew (SpaceX Dragon, Boeing Starliner), ISS expeditions, and ESA missions
- **Real-Time Countdown**: Live countdown timers to launch
- **Crew Information**: Photos, bios, and roles for mission crew members
- **Mission Timeline**: Visual progress tracking for milestones
- **Weather Data**: Launch site weather forecasts (only when launch is within 7 days)
- **Live Updates**: WebSocket-based real-time data sync
- **Multi-Screen Kiosk Mode**: Control multiple displays from a central server
- **Remote Navigation**: API-driven page switching across screens
- **Offline Support**: Cached data when offline
- **Notifications**: Browser and in-app alerts for milestone and countdown events

## Project Structure

```
ArtemisOps/
├── server/              # Python FastAPI backend
│   ├── main.py          # API server
│   ├── database.py      # SQLite database layer
│   ├── fetcher.py       # Space Devs API data fetcher
│   ├── weather.py       # Weather data service (Open-Meteo API)
│   ├── requirements.txt # Python dependencies
│   └── cache/           # Cached API responses (gitignored)
├── client/              # Web frontend
│   └── index.html       # Main client app
├── PLANNING.md          # Feature planning & roadmap
└── README.md
```

## Quick Start

### 1. Set up Python environment

```bash
cd server
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### 3. Open in browser

- **App**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve client app |
| `/api/missions` | GET | List all active missions |
| `/api/missions/{id}` | GET | Full mission data with crew & milestones |
| `/api/missions/{id}/weather` | GET | Weather for mission (only if launch within 7 days) |
| `/api/weather/{site}` | GET | Weather for any launch site by name |
| `/api/mission` | GET | Default mission (Artemis II) - legacy |
| `/api/crew` | GET | Default mission crew - legacy |
| `/api/status` | GET | Server status |
| `/api/sync` | POST | Force data refresh |
| `/ws` | WebSocket | Real-time updates (legacy) |
| `/ws/screen/{id}` | WebSocket | Screen-specific connection for multi-display |
| `/api/screens` | GET | List all screens (online + provisioned offline) |
| `/api/screens/{id}` | GET | Get specific screen status |
| `/api/screens/{id}/page` | POST | Navigate screen to page (0-4) |
| `/api/screens/all/page` | POST | Navigate all screens to same page |
| `/api/screens/config` | GET | List provisioned screen configs |
| `/api/screens/config` | POST | Add/update screen config (auto-navigates on connect) |
| `/api/screens/config/{id}` | DELETE | Remove a provisioned screen config |

## Weather Feature

The weather service intelligently fetches forecasts only when relevant:

- **Smart Triggering**: Only fetches weather when launch/landing is within 7 days
- **Launch Site Detection**: Automatically maps mission sites to coordinates
- **Launch Viability Analysis**: Evaluates weather against launch constraints:
  - Wind speed limits (48 km/h sustained, 64 km/h gusts)
  - Precipitation thresholds
  - Thunderstorm/severe weather detection
- **5-Day Forecast**: Multi-day forecast summary
- **30-Minute Caching**: Reduces API calls while keeping data fresh

### Supported Launch Sites

- Kennedy Space Center, FL
- Cape Canaveral, FL
- Vandenberg SFB, CA
- Kourou/Guiana Space Centre (ESA)
- Baikonur Cosmodrome
- Tanegashima, Japan
- And more...

### Example Weather Response

```json
{
  "mission_id": "artemis-ii",
  "mission_name": "Artemis II",
  "should_fetch": true,
  "launch": {
    "site": "Kennedy Space Center, FL",
    "analysis": {
      "status": "go",
      "message": "Weather conditions favorable for launch",
      "days_until": 5,
      "conditions": {
        "icon": "🌤️",
        "description": "Mainly clear",
        "temperature_high_f": 78.2,
        "wind_speed_mph": 12.4
      }
    },
    "forecast": [
      { "date": "2026-01-20", "day_name": "Tue", "icon": "☀️", ... },
      { "date": "2026-01-21", "day_name": "Wed", "icon": "⛅", ... }
    ]
  }
}
```

## Data Sources

- **Mission Data**: [Space Devs Launch Library 2 API](https://thespacedevs.com/llapi)
- **Weather Data**: [Open-Meteo API](https://open-meteo.com/) (free, no API key required)

## Supported Missions

The app tracks crewed missions from:
- **NASA**: Artemis, Commercial Crew Program, ISS expeditions
- **ESA**: European astronaut missions
- **Commercial Partners**: SpaceX Crew Dragon, Boeing Starliner, Axiom Space

## Development

- Python 3.12+
- FastAPI + Uvicorn
- SQLite with aiosqlite
- APScheduler for background data fetching
- Vanilla JavaScript frontend

## Deployment (Raspberry Pi)

```bash
git clone https://github.com/johnmknight/ArtemisOps.git
cd ArtemisOps/server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Multi-Screen Kiosk Mode

ArtemisOps supports controlling multiple displays from a single server - perfect for mission control room setups.

### URL Parameters

```
http://localhost:8080?id=control&page=0  # Control panel
http://localhost:8080?id=lobby-1&page=1  # Screen "lobby-1", Mission page
http://localhost:8080?id=main&page=2     # Screen "main", Tracking page
http://localhost:8080?id=crew-tv&page=3  # Screen "crew-tv", Crew page
```

### Page Numbers

| Page | Name | Content |
|------|------|--------|
| 0 | Control | Control panel with screen management and remote navigation |
| 1 | Mission | Countdown, milestones, launch info |
| 2 | Tracking | ISS tracker / Artemis trajectory map |
| 3 | Crew | Astronaut profiles and bios |
| 4 | Info | Mission details and description |

### Screen Provisioning

Screens can be pre-configured so they auto-load the correct page on connect. Use the Page 0 Control Panel UI or the API directly:

```bash
# Add a screen config (will auto-navigate when it connects)
curl -X POST "http://localhost:8080/api/screens/config?screen_id=lobby-1&page=2&label=Lobby+Display"

# List all provisioned configs
curl http://localhost:8080/api/screens/config

# Remove a screen config
curl -X DELETE http://localhost:8080/api/screens/config/lobby-1
```

### Remote Control API

```bash
# List all screens (online + provisioned offline)
curl http://localhost:8080/api/screens

# Switch screen to Tracking page
curl -X POST "http://localhost:8080/api/screens/lobby-1/page?page=2"

# Switch all screens to Mission page
curl -X POST "http://localhost:8080/api/screens/all/page?page=1"

# Switch by page name
curl -X POST "http://localhost:8080/api/screens/lobby-1/page?page_name=crew"
```

### Architecture

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  lobby-1    │   │  main       │   │  crew-tv    │
│  page=1     │   │  page=2     │   │  page=3     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │ WebSocket        │                 │
       └──────────────────┴─────────────────┘
                          │
                  ┌───────▼───────┐
                  │    SERVER     │
                  │  Screen Hub + │
                  │  Config Store │
                  └───────┬───────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    Page 0 Control   REST API       Automation
    (add/remove/     POST /api/     (scripts,
     navigate)       screens/...    cron, etc.)
```

See PLANNING.md for feature roadmap.
