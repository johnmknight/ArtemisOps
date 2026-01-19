# ArtemisOps

Mission clock and status tracking app for NASA Artemis missions.

## Project Structure

```
ArtemisOps/
├── server/              # Python FastAPI backend
│   ├── main.py          # API server
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
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Open in browser

- **App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve client app |
| `/api/mission` | GET | Current mission data |
| `/api/status` | GET | Server status |
| `/api/refresh` | POST | Force data refresh |
| `/ws` | WebSocket | Real-time updates |

## Development

- Python 3.12+
- FastAPI + Uvicorn
- SQLite (planned)
- APScheduler for background data fetching

## Deployment (Raspberry Pi)

```bash
git clone https://github.com/johnmknight/ArtemisOps.git
cd ArtemisOps/server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

See PLANNING.md for feature roadmap.
