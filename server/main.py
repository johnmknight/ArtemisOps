"""
ArtemisOps Server - Mission Control Backend
Multi-mission support with hourly data sync
Supports NASA and ESA crewed missions
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import (
    init_db, get_all_missions, get_full_mission,
    get_last_sync
)
from fetcher import sync_all_missions, ensure_default_missions
from seed_missions import seed_crew_dragon_missions
from weather import get_mission_weather, is_within_forecast_window, is_same_day, get_hours_until, fetch_current_and_forecast, build_site_weather, find_site_coordinates, DEFAULT_RECOVERY_SITE, _get_client
from iss import get_iss_position, get_iss_crew, get_nasa_telemetry, get_iss_combined, get_location_name, get_iss_news
from crew_enrichment import get_cache_status as get_enrichment_status
from trajectories import get_trajectory, get_available_trajectories
from news import get_news
from streams import fetch_nasa_streams, get_all_sources
from spacex import get_dragons_response

# Paths
BASE_DIR = Path(__file__).parent
CLIENT_DIR = BASE_DIR.parent / "client"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)


async def get_default_mission_id() -> str:
    """
    Get the best default mission ID to show.
    Priority: first upcoming/active mission by launch date, then fall back to artemis-ii.
    """
    missions = await get_all_missions()
    if missions:
        # Prefer missions with status "Go" or "In Flight", sorted by soonest launch
        active = [m for m in missions if (m.get("status") or "").lower() in ("go", "in flight", "tbd", "tbc")]
        if active:
            # Sort by launch date (soonest first)
            active.sort(key=lambda m: m.get("launch_date") or "9999")
            return active[0]["id"]
        # Fall back to first mission in list
        return missions[0]["id"]
    return "artemis-ii"


# In-memory state
app_state = {
    "connected_clients": set(),  # WebSocket connections (legacy)
    "last_sync": None,
    "weather_cache": {},  # Cache weather data per mission
    "screens": {},  # Screen registry: {screen_id: {"ws": websocket, "page": page_id, "connected_at": datetime}}
    "screen_configs": {},  # Pre-provisioned screens: {screen_id: {"page": int, "label": str}}
}

# Page mapping
PAGES = {
    0: "control",
    1: "mission",
    2: "tracking",
    3: "crew",
    4: "info",
    5: "weather",
    "control": 0,
    "mission": 1,
    "tracking": 2,
    "crew": 3,
    "info": 4,
    "weather": 5
}

scheduler = AsyncIOScheduler()


# === WebSocket Broadcast ===

async def broadcast_update(data: dict):
    """Send update to all connected WebSocket clients"""
    disconnected = set()
    message = {"type": "mission_update", "data": data}
    
    for ws in app_state["connected_clients"]:
        try:
            await ws.send_json(message)
        except:
            disconnected.add(ws)
    
    app_state["connected_clients"] -= disconnected


async def broadcast_missions_list():
    """Broadcast updated missions list to all clients"""
    missions = await get_all_missions()
    message = {"type": "missions_list", "data": missions}
    
    disconnected = set()
    for ws in app_state["connected_clients"]:
        try:
            await ws.send_json(message)
        except:
            disconnected.add(ws)
    
    app_state["connected_clients"] -= disconnected


# === Scheduled Sync ===

async def scheduled_sync():
    """Hourly sync job"""
    print(f"[{datetime.now()}] Running scheduled sync...")
    
    result = await sync_all_missions()
    app_state["last_sync"] = datetime.now(timezone.utc)
    
    # Clear weather cache on sync (data may have changed)
    app_state["weather_cache"] = {}
    
    # Broadcast update to all clients
    await broadcast_missions_list()
    
    return result


# === Lifespan ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("ArtemisOps Server starting...")
    
    # Initialize database
    await init_db()
    
    # Ensure we have default data
    await ensure_default_missions()
    
    # Seed Crew Dragon missions if not present
    await seed_crew_dragon_missions()
    
    # Initial sync (fetch upcoming missions)
    await sync_all_missions()
    app_state["last_sync"] = datetime.now(timezone.utc)
    
    # Schedule sync every 24 hours (mission data changes rarely; use /api/sync for manual refresh)
    scheduler.add_job(scheduled_sync, 'interval', hours=24, id='mission_sync')
    scheduler.start()
    print("Scheduler started - syncing every 24 hours")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("ArtemisOps Server stopped")


# === FastAPI App ===

app = FastAPI(
    title="ArtemisOps API",
    description="Mission Control Backend for NASA and ESA Crewed Missions",
    version="0.7.0",
    lifespan=lifespan
)

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === API Routes ===

@app.get("/api/missions")
async def list_missions():
    """Get all active missions"""
    missions = await get_all_missions()
    return {"missions": missions}


# Default agency logos (fallback if nothing in DB)
DEFAULT_AGENCY_LOGOS = {
    "NASA": "https://www.nasa.gov/wp-content/uploads/2023/04/nasa-logo-web-rgb.png",
    "ESA": "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/05/esa_logo_white_background/21973314-1-eng-GB/ESA_logo_white_background_pillars.jpg",
    "JAXA": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Jaxa_logo.svg/1200px-Jaxa_logo.svg.png",
    "CSA": "https://www.asc-csa.gc.ca/images/recherche/tiles/csa-logo.jpg",
    "SpaceX": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/SpaceX-Logo.svg/1200px-SpaceX-Logo.svg.png",
    "Boeing": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Boeing_full_logo.svg/1200px-Boeing_full_logo.svg.png",
}


def get_fallback_agency_logo(agencies_str: str) -> str:
    """Get agency logo from defaults when DB doesn't have one"""
    if not agencies_str:
        return DEFAULT_AGENCY_LOGOS.get("NASA")
    
    primary = agencies_str.split(",")[0].strip()
    
    if primary in DEFAULT_AGENCY_LOGOS:
        return DEFAULT_AGENCY_LOGOS[primary]
    
    for key, url in DEFAULT_AGENCY_LOGOS.items():
        if key.lower() in primary.lower():
            return url
    
    return DEFAULT_AGENCY_LOGOS.get("NASA")


@app.get("/api/missions/{mission_id}")
async def get_mission_detail(mission_id: str):
    """
    Get full mission data including crew and milestones.
    
    Patch and logo URLs are stored in the database (fetched during sync).
    This provides fast, consistent access without per-request API calls.
    """
    mission = await get_full_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Get patch and logo from database (populated during sync)
    # Fall back to defaults if not present
    agency_logo = mission.get("agency_logo_url")
    if not agency_logo:
        agency_logo = get_fallback_agency_logo(mission.get("agencies"))
    
    mission_patch = mission.get("patch_url")
    if not mission_patch:
        mission_patch = mission.get("image_url")  # Fall back to launch image
    
    return {
        "id": mission["id"],
        "name": mission["name"],
        "launch_date": mission["launch_date"],
        "status": mission["status_description"] or mission["status"],
        "site": mission["site"],
        "source": mission.get("api_source", "database"),
        "image": mission.get("image_url"),
        "agency_logo": agency_logo,
        "mission_patch": mission_patch,
        "rocket": mission.get("rocket"),
        "spacecraft": mission.get("spacecraft"),
        "description": mission.get("description"),
        "agencies": mission.get("agencies"),
        "mission_type": mission.get("mission_type"),
        "crew": [
            {
                "name": c["name"],
                "role": c["role"],
                "agency": c["agency"],
                "photo": c["photo_url"],
                "bio": c["bio"],
                "nasa_bio": c["bio_url"]
            }
            for c in mission.get("crew", [])
        ],
        "milestones": [
            {
                "date": m["date_label"],
                "title": m["title"],
                "description": m["description"],
                "status": m["status"]
            }
            for m in mission.get("milestones", [])
        ]
    }


@app.get("/api/missions/{mission_id}/weather")
async def get_mission_weather_data(mission_id: str):
    """
    Get weather data for a mission's launch site.
    Only returns data if launch is within 7 days (forecast window).
    Weather data is cached for 30 minutes to avoid excessive API calls.
    """
    mission = await get_full_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Check cache first (30 min expiry)
    cache_key = mission_id
    cached = app_state["weather_cache"].get(cache_key)
    if cached:
        cache_time, cache_data = cached
        age_minutes = (datetime.now(timezone.utc) - cache_time).total_seconds() / 60
        if age_minutes < 30:
            return {
                "mission_id": mission_id,
                "mission_name": mission["name"],
                "cached": True,
                "cache_age_minutes": round(age_minutes, 1),
                **cache_data
            }
    
    # Parse launch date
    launch_date = None
    if mission.get("launch_date"):
        try:
            launch_date = datetime.fromisoformat(mission["launch_date"].replace("Z", "+00:00"))
        except:
            pass
    
    # Get weather data
    weather_data = await get_mission_weather(
        launch_date=launch_date,
        launch_site=mission.get("site"),
    )
    
    # Cache the result
    app_state["weather_cache"][cache_key] = (datetime.now(timezone.utc), weather_data)
    
    return {
        "mission_id": mission_id,
        "mission_name": mission["name"],
        "cached": False,
        **weather_data
    }


@app.get("/api/missions/{mission_id}/weather/launch-day")
async def get_launch_day_weather(mission_id: str):
    """
    Get weather data specifically for launch day display.
    Only returns data if launch is TODAY (same calendar day).
    Used by the client to show/hide the weather panel.
    """
    mission = await get_full_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Parse launch date
    launch_date = None
    if mission.get("launch_date"):
        try:
            launch_date = datetime.fromisoformat(mission["launch_date"].replace("Z", "+00:00"))
        except:
            pass
    
    # Check if launch is today
    launch_is_today = is_same_day(launch_date) if launch_date else False
    hours_until_launch = get_hours_until(launch_date) if launch_date else None
    
    # Parse landing date (if available)
    landing_date = None
    if mission.get("landing_date"):
        try:
            landing_date = datetime.fromisoformat(mission["landing_date"].replace("Z", "+00:00"))
        except:
            pass
    
    landing_is_today = is_same_day(landing_date) if landing_date else False
    hours_until_landing = get_hours_until(landing_date) if landing_date else None
    
    # Determine if we should show weather
    show_weather = launch_is_today or landing_is_today
    event_type = None
    
    if launch_is_today:
        event_type = "launch"
    elif landing_is_today:
        event_type = "recovery"
    
    result = {
        "mission_id": mission_id,
        "mission_name": mission["name"],
        "show_weather": show_weather,
        "event_type": event_type,
        "launch_site": mission.get("site"),
        "launch_is_today": launch_is_today,
        "hours_until_launch": round(hours_until_launch, 1) if hours_until_launch else None,
        "landing_is_today": landing_is_today,
        "hours_until_landing": round(hours_until_landing, 1) if hours_until_landing else None,
        "weather": None
    }
    
    # Only fetch weather if event is today
    if show_weather:
        weather_data = await get_mission_weather(
            launch_date=launch_date if launch_is_today else None,
            launch_site=mission.get("site") if launch_is_today else None,
            landing_date=landing_date if landing_is_today else None,
            landing_site=mission.get("landing_site") if landing_is_today else None,
        )
        result["weather"] = weather_data
    
    return result


# Legacy endpoint for backward compatibility
@app.get("/api/mission")
async def get_default_mission():
    """Get default mission - legacy endpoint"""
    default_id = await get_default_mission_id()
    return await get_mission_detail(default_id)


@app.get("/api/crew")
async def get_default_crew():
    """Get crew for default mission - legacy endpoint"""
    default_id = await get_default_mission_id()
    mission = await get_full_mission(default_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    return {
        "mission": mission["name"],
        "crew": [
            {
                "name": c["name"],
                "role": c["role"],
                "agency": c["agency"],
                "photo": c["photo_url"],
                "bio": c["bio"],
                "nasa_bio": c["bio_url"]
            }
            for c in mission.get("crew", [])
        ]
    }


@app.get("/api/weather/{site_name}")
async def get_site_weather(site_name: str, days: int = 5):
    """
    Get weather forecast for a specific launch site by name.
    Useful for checking weather at any known launch site.
    """
    from weather import find_site_coordinates, fetch_weather_forecast, get_forecast_summary
    
    coords = find_site_coordinates(site_name)
    if not coords:
        raise HTTPException(
            status_code=404, 
            detail=f"Unknown launch site: {site_name}. Try 'Kennedy Space Center', 'Cape Canaveral', 'Vandenberg', 'Kourou', etc."
        )
    
    forecast = await fetch_weather_forecast(coords["lat"], coords["lon"], days=days)
    if not forecast:
        raise HTTPException(status_code=503, detail="Weather service unavailable")
    
    return {
        "site": coords["name"],
        "coordinates": {"lat": coords["lat"], "lon": coords["lon"]},
        "forecast": get_forecast_summary(forecast, days=days)
    }


@app.get("/api/weather/operations/{mission_id}")
async def get_weather_operations(mission_id: str):
    """
    Get comprehensive weather for launch and recovery sites.
    Always returns current conditions regardless of launch date.
    Used by the Weather tab.
    """
    mission = await get_full_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    # Check cache (10 min expiry for operations data)
    cache_key = f"ops_{mission_id}"
    cached = app_state["weather_cache"].get(cache_key)
    if cached:
        cache_time, cache_data = cached
        age_minutes = (datetime.now(timezone.utc) - cache_time).total_seconds() / 60
        if age_minutes < 10:
            return {**cache_data, "cached": True, "cache_age_minutes": round(age_minutes, 1)}

    # Resolve launch site
    launch_site_name = mission.get("site", "")
    launch_coords = find_site_coordinates(launch_site_name)

    # Default recovery site
    recovery_coords = DEFAULT_RECOVERY_SITE
    
    # Use mission-specific recovery coordinates if available
    if mission.get("recovery_lat") and mission.get("recovery_lon"):
        recovery_coords = {
            "lat": mission["recovery_lat"],
            "lon": mission["recovery_lon"],
            "name": mission.get("recovery_site", "Recovery Zone"),
        }
    elif mission.get("recovery_site"):
        site_match = find_site_coordinates(mission["recovery_site"])
        if site_match:
            recovery_coords = site_match

    launch_weather = None
    recovery_weather = None

    # Fetch launch site weather (current + forecast)
    if launch_coords:
        raw = await fetch_current_and_forecast(launch_coords["lat"], launch_coords["lon"])
        launch_weather = build_site_weather(raw, launch_coords)

    # Fetch recovery site weather
    raw = await fetch_current_and_forecast(recovery_coords["lat"], recovery_coords["lon"])
    recovery_weather = build_site_weather(raw, recovery_coords)

    result = {
        "mission_id": mission_id,
        "mission_name": mission["name"],
        "launch_date": mission.get("launch_date"),
        "cached": False,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "launch_site": launch_weather,
        "recovery_site": recovery_weather
    }

    # Cache the result
    app_state["weather_cache"][cache_key] = (datetime.now(timezone.utc), result)

    return result


# === SWPC Space Weather Proxy ===
# Proxies NOAA Space Weather Prediction Center APIs to avoid CORS issues

SWPC_BASE = "https://services.swpc.noaa.gov"
SWPC_ENDPOINTS = {
    "kp": "/products/noaa-planetary-k-index.json",
    "solar-wind-plasma": "/products/solar-wind/plasma-5-minute.json",
    "solar-wind-mag": "/products/solar-wind/mag-5-minute.json",
    "xray": "/json/goes/primary/xrays-6-hour.json",
    "alerts": "/products/alerts.json",
    "sunspots": "/json/solar-cycle/sunspots.json",
    "solar-flux": "/products/summary/solar-radio-flux.json",
    "geomag-forecast": "/products/noaa-planetary-k-index-forecast.json",
    "proton": "/json/goes/primary/integral-protons-1-day.json",
    "electron": "/json/goes/primary/integral-electrons-1-day.json",
    "aurora": "/products/animations/ovation_north_24h.json",
    "aurora-image": "/images/animations/ovation/north/latest.jpg",
    "enlil": "/products/animations/enlil.json",
    "solar-regions": "/json/solar_regions.json",
    "mag-1day": "/products/solar-wind/mag-1-day.json",
    "plasma-1day": "/products/solar-wind/plasma-1-day.json",
    "kp-1min": "/json/planetary_k_index_1m.json",
}

_swpc_cache: dict = {}  # key -> (timestamp, data)
SWPC_CACHE_TTL = 120  # seconds


@app.get("/api/swpc/{endpoint}")
async def proxy_swpc(endpoint: str):
    """Proxy SWPC API endpoints with caching."""
    if endpoint not in SWPC_ENDPOINTS:
        raise HTTPException(status_code=404, detail=f"Unknown SWPC endpoint: {endpoint}")

    # Check cache
    now = datetime.now(timezone.utc)
    if endpoint in _swpc_cache:
        ts, data = _swpc_cache[endpoint]
        if (now - ts).total_seconds() < SWPC_CACHE_TTL:
            return data

    try:
        client = _get_client()
        url = SWPC_BASE + SWPC_ENDPOINTS[endpoint]
        resp = await client.get(url, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        _swpc_cache[endpoint] = (now, data)
        return data
    except Exception as e:
        # Return cached even if stale
        if endpoint in _swpc_cache:
            return _swpc_cache[endpoint][1]
        raise HTTPException(status_code=502, detail=f"SWPC API error: {str(e)}")


# === ISS Data Endpoints ===

@app.get("/api/iss")
async def get_iss_data():
    """
    Get all ISS data: position, crew, and NASA telemetry.
    This is the main endpoint for the ISS tracker.
    All external API calls are proxied through this server.
    """
    try:
        return await get_iss_combined()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS data unavailable: {str(e)}")


@app.get("/api/iss/position")
async def get_iss_position_data(include_location: bool = True):
    """
    Get current ISS position (latitude, longitude, altitude, velocity).
    Data from Where The ISS At API, with Open Notify as fallback.
    
    Query params:
        include_location: If true (default), includes reverse-geocoded location name.
                         This saves a separate API call for clients.
    """
    try:
        position = await get_iss_position()
        
        # Include location name to save client a second API call
        if include_location and position.get("latitude") and position.get("longitude"):
            location = await get_location_name(position["latitude"], position["longitude"])
            position["location"] = location
        
        return position
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS position unavailable: {str(e)}")


@app.get("/api/iss/crew")
async def get_iss_crew_data():
    """
    Get current ISS crew roster (two-phase).
    Phase 1: Open Notify API → crew names
    Phase 2: NASA ISS Blog → agency affiliations
    """
    try:
        return await get_iss_crew()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS crew data unavailable: {str(e)}")


@app.get("/api/iss/crew/enrichment")
async def get_crew_enrichment_status():
    """Diagnostic: view crew agency enrichment cache status."""
    return get_enrichment_status()


@app.get("/api/iss/telemetry")
async def get_iss_telemetry_data():
    """
    Get NASA ISS telemetry (cabin pressure, temperature, O2, CO2, etc.).
    Data from NASA Lightstreamer.
    Note: Telemetry may be unavailable if Lightstreamer connection fails.
    """
    return get_nasa_telemetry()


@app.get("/api/iss/news")
async def get_iss_news_data(limit: int = 10):
    """
    Get latest ISS news from NASA ISS Blog and Spaceflight Now RSS feeds.
    Cached for 15 minutes.
    """
    try:
        return await get_iss_news(limit)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS news unavailable: {str(e)}")


@app.get("/api/iss/location/{lat},{lng}")
async def get_iss_location_name(lat: float, lng: float):
    """
    Get location name from coordinates (reverse geocoding).
    Data from Where The ISS At API, cached.
    """
    try:
        return await get_location_name(lat, lng)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Location lookup unavailable: {str(e)}")


# === SpaceX Tracking ===

@app.get("/api/spacex/dragons")
async def get_spacex_dragons():
    """
    Get TLE data for active SpaceX Crew Dragon capsules.
    Client uses satellite.js for SGP4 orbit propagation.
    TLEs cached for 1 hour from CelesTrak.
    """
    try:
        return await get_dragons_response()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"SpaceX data unavailable: {str(e)}")


# === Trajectory Data ===

@app.get("/api/missions/{mission_id}/trajectory")
async def get_mission_trajectory(mission_id: str):
    """
    Get trajectory waypoints and path data for a mission.
    
    Returns SVG-coordinate waypoints, path segments, phase definitions,
    and orbital parameters. Used by client map components to render
    mission trajectories without hardcoded data.
    
    Supports: artemis-ii, artemis-iii, iss, and aliases (artemis-i,
    artemis-iv, artemis-v, crew-dragon, starliner, etc.)
    """
    trajectory = get_trajectory(mission_id)
    if not trajectory:
        raise HTTPException(
            status_code=404,
            detail=f"No trajectory data for mission '{mission_id}'. "
                   f"Available: {[t['mission_id'] for t in get_available_trajectories()]}"
        )
    
    return {
        "mission_id": mission_id,
        **trajectory
    }


@app.get("/api/trajectories")
async def list_trajectories():
    """List all missions with trajectory data available."""
    return {
        "trajectories": get_available_trajectories(),
        "count": len(get_available_trajectories()),
    }


# === General News ===

@app.get("/api/news")
async def get_news_feed(limit: int = 20, source: str = None):
    """
    Aggregated space news from NASA and industry RSS feeds.
    
    Sources: NASA Breaking News, NASA Artemis Blog, NASA ISS Blog,
    Spaceflight Now.
    
    Query params:
        limit: Max items (default 20)
        source: Filter by feed ID (nasa-breaking, nasa-artemis,
                nasa-iss, spaceflight-now)
    
    Cached for 15 minutes.
    """
    try:
        return await get_news(limit=limit, source=source)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"News unavailable: {str(e)}")


# === NASA YouTube Streams ===

@app.get("/api/streams")
async def get_streams(force: bool = False):
    """
    Live and upcoming NASA YouTube streams + always-on fallback sources.

    Scrapes youtube.com/@NASA/streams for current live broadcasts,
    upcoming scheduled streams, and recent past streams.

    Response includes:
        - live: Currently broadcasting streams
        - upcoming: Scheduled future streams
        - recent: Past streams (last 10)
        - recommended: Best auto-play pick (first live > first upcoming > first recent)
        - fallback: Always-on sources (NASA TV, ISS cams via IBM/Ustream)

    Query params:
        force: Skip cache and re-fetch (default false)

    Cached for 5 minutes.
    """
    try:
        return await get_all_sources(force=force)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Streams unavailable: {str(e)}")


@app.get("/api/status")
async def get_status():
    """Server status endpoint"""
    last_sync = await get_last_sync()
    missions = await get_all_missions()
    return {
        "status": "ok",
        "last_sync": last_sync["synced_at"] if last_sync else None,
        "connected_clients": len(app_state["connected_clients"]),
        "connected_screens": len(app_state["screens"]),
        "total_missions": len(missions),
        "weather_cache_size": len(app_state["weather_cache"]),
        "version": "0.7.0"
    }


# === Multi-Screen Control API ===

@app.get("/api/screens")
async def list_screens():
    """
    List all screens: connected + provisioned-but-offline.
    Used by control panels to see what screens are available.
    """
    screens = []
    seen_ids = set()
    
    # Connected screens first
    for screen_id, data in app_state["screens"].items():
        cfg = app_state["screen_configs"].get(screen_id)
        screens.append({
            "id": screen_id,
            "page": data["page"],
            "page_name": PAGES.get(data["page"], "unknown"),
            "connected_at": data["connected_at"].isoformat() if data.get("connected_at") else None,
            "mission": data.get("mission", "unknown"),
            "online": True,
            "configured": cfg is not None,
            "config_page": cfg["page"] if cfg else None,
            "label": cfg.get("label", "") if cfg else "",
        })
        seen_ids.add(screen_id)
    
    # Provisioned-but-offline screens
    for screen_id, cfg in app_state["screen_configs"].items():
        if screen_id not in seen_ids:
            screens.append({
                "id": screen_id,
                "page": cfg["page"],
                "page_name": PAGES.get(cfg["page"], "unknown"),
                "connected_at": None,
                "mission": cfg.get("mission", "unknown"),
                "online": False,
                "configured": True,
                "config_page": cfg["page"],
                "label": cfg.get("label", ""),
            })
    
    return {
        "screens": screens,
        "total": len(screens),
        "online": sum(1 for s in screens if s["online"]),
        "pages": {"0": "control", "1": "mission", "2": "tracking", "3": "crew", "4": "info"}
    }


@app.post("/api/screens/{screen_id}/page")
async def set_screen_page(screen_id: str, page: int = None, page_name: str = None):
    """
    Navigate a specific screen to a page.
    
    Args:
        screen_id: The screen identifier (from ?id= parameter)
        page: Page number (1=mission, 2=tracking, 3=crew, 4=info)
        page_name: Alternatively, page name ("mission", "tracking", "crew", "info")
    
    Example:
        POST /api/screens/1/page?page=2  (switch screen 1 to tracking)
        POST /api/screens/1/page?page_name=crew  (switch screen 1 to crew)
    """
    # Resolve page number
    target_page = page
    if page_name and not page:
        target_page = PAGES.get(page_name.lower())
    
    if target_page is None or target_page not in [0, 1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Invalid page. Use 0-4 or control/mission/tracking/crew/info")
    
    screen = app_state["screens"].get(screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail=f"Screen '{screen_id}' not connected")
    
    # Send navigation command via WebSocket
    try:
        await screen["ws"].send_json({
            "type": "navigate",
            "page": target_page,
            "page_name": PAGES.get(target_page)
        })
        screen["page"] = target_page
        return {
            "success": True,
            "screen_id": screen_id,
            "page": target_page,
            "page_name": PAGES.get(target_page)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send command: {str(e)}")


@app.post("/api/screens/all/page")
async def set_all_screens_page(page: int = None, page_name: str = None):
    """
    Navigate ALL connected screens to the same page.
    
    Example:
        POST /api/screens/all/page?page=1  (all screens to mission)
    """
    target_page = page
    if page_name and not page:
        target_page = PAGES.get(page_name.lower())
    
    if target_page is None or target_page not in [0, 1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Invalid page. Use 0-4 or control/mission/tracking/crew/info")
    
    results = []
    for screen_id, screen in app_state["screens"].items():
        try:
            await screen["ws"].send_json({
                "type": "navigate",
                "page": target_page,
                "page_name": PAGES.get(target_page)
            })
            screen["page"] = target_page
            results.append({"screen_id": screen_id, "success": True})
        except Exception as e:
            results.append({"screen_id": screen_id, "success": False, "error": str(e)})
    
    return {
        "page": target_page,
        "page_name": PAGES.get(target_page),
        "results": results,
        "total_screens": len(app_state["screens"])
    }


# === Screen Configuration (Provisioning) ===
# NOTE: These must be defined BEFORE /api/screens/{screen_id} to avoid route capture

@app.get("/api/screens/config")
async def list_screen_configs():
    """
    List all provisioned screen configurations.
    Includes online/offline status by checking live connections.
    """
    configs = []
    for screen_id, cfg in app_state["screen_configs"].items():
        live = app_state["screens"].get(screen_id)
        configs.append({
            "id": screen_id,
            "page": cfg["page"],
            "page_name": PAGES.get(cfg["page"], "unknown"),
            "label": cfg.get("label", ""),
            "online": live is not None,
            "current_page": live["page"] if live else None,
            "current_page_name": PAGES.get(live["page"]) if live else None,
        })
    return {"configs": configs, "total": len(configs)}


@app.post("/api/screens/config")
async def add_screen_config(screen_id: str, page: int = 1, label: str = ""):
    """
    Add or update a provisioned screen configuration.
    When a screen with this ID connects, it will auto-navigate to the configured page.
    
    Args:
        screen_id: The screen identifier (used in ?id= URL param)
        page: Default page (0=control, 1=mission, 2=tracking, 3=crew, 4=info)
        label: Optional friendly label for this screen
    """
    if page not in [0, 1, 2, 3, 4]:
        raise HTTPException(status_code=400, detail="Invalid page. Use 0-4.")
    
    app_state["screen_configs"][screen_id] = {
        "page": page,
        "label": label,
    }
    print(f"Screen config added: '{screen_id}' -> page {page} ({PAGES.get(page)})")
    
    # If screen is already connected, navigate it now
    live = app_state["screens"].get(screen_id)
    if live:
        try:
            await live["ws"].send_json({
                "type": "navigate",
                "page": page,
                "page_name": PAGES.get(page)
            })
            live["page"] = page
        except:
            pass
    
    return {
        "success": True,
        "screen_id": screen_id,
        "page": page,
        "page_name": PAGES.get(page),
        "label": label,
        "navigated": live is not None
    }


@app.delete("/api/screens/config/{screen_id}")
async def remove_screen_config(screen_id: str):
    """Remove a provisioned screen configuration."""
    if screen_id not in app_state["screen_configs"]:
        raise HTTPException(status_code=404, detail=f"Screen config '{screen_id}' not found")
    
    del app_state["screen_configs"][screen_id]
    print(f"Screen config removed: '{screen_id}'")
    
    return {"success": True, "screen_id": screen_id}


@app.get("/api/screens/{screen_id}")
async def get_screen_status(screen_id: str):
    """Get status of a specific screen"""
    screen = app_state["screens"].get(screen_id)
    if not screen:
        raise HTTPException(status_code=404, detail=f"Screen '{screen_id}' not connected")
    
    return {
        "id": screen_id,
        "page": screen["page"],
        "page_name": PAGES.get(screen["page"], "unknown"),
        "connected_at": screen["connected_at"].isoformat() if screen.get("connected_at") else None,
        "mission": screen.get("mission", "unknown")
    }


@app.post("/api/sync")
async def trigger_sync():
    """Manually trigger data sync"""
    result = await sync_all_missions()
    await broadcast_missions_list()
    return result


# === WebSocket ===

@app.websocket("/ws/screen/{screen_id}")
async def screen_websocket(websocket: WebSocket, screen_id: str):
    """
    WebSocket connection for a specific screen.
    Screen registers with ?id=X parameter in the client URL.
    Server can send navigation commands to specific screens.
    """
    await websocket.accept()
    
    # Check if there's a pre-provisioned config for this screen
    config = app_state["screen_configs"].get(screen_id)
    initial_page = config["page"] if config else 1  # Default to mission
    
    # Get current default mission for initial state
    default_id = await get_default_mission_id()
    
    # Register screen
    app_state["screens"][screen_id] = {
        "ws": websocket,
        "page": initial_page,
        "connected_at": datetime.now(timezone.utc),
        "mission": default_id
    }
    print(f"Screen '{screen_id}' connected (config: {'yes, page ' + str(initial_page) if config else 'none'}). Total screens: {len(app_state['screens'])}")
    
    try:
        # Send initial state to screen
        await websocket.send_json({
            "type": "registered",
            "screen_id": screen_id,
            "page": initial_page
        })
        
        # If config exists, send navigation command to override client's default
        if config:
            await websocket.send_json({
                "type": "navigate",
                "page": initial_page,
                "page_name": PAGES.get(initial_page)
            })
        
        # Send current mission data
        missions = await get_all_missions()
        await websocket.send_json({
            "type": "missions_list",
            "data": missions
        })
        
        mission = await get_full_mission(default_id)
        if mission:
            await websocket.send_json({
                "type": "mission_update",
                "data": await get_mission_detail(default_id)
            })
        
        # Keep connection alive, listen for messages from screen
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif data.startswith("page:"):
                # Screen reporting its current page
                try:
                    page_num = int(data.split(":")[1])
                    app_state["screens"][screen_id]["page"] = page_num
                except:
                    pass
            
            elif data.startswith("mission:"):
                # Screen changing mission
                mission_id = data.split(":")[1]
                app_state["screens"][screen_id]["mission"] = mission_id
                try:
                    mission_data = await get_mission_detail(mission_id)
                    await websocket.send_json({
                        "type": "mission_update",
                        "data": mission_data
                    })
                except HTTPException:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Mission {mission_id} not found"
                    })
            
            elif data.startswith("weather:"):
                # Screen requesting weather
                mission_id = data.split(":")[1]
                try:
                    weather_data = await get_mission_weather_data(mission_id)
                    await websocket.send_json({
                        "type": "weather_update",
                        "data": weather_data
                    })
                except HTTPException as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e.detail)
                    })
    
    except WebSocketDisconnect:
        pass
    finally:
        # Unregister screen
        if screen_id in app_state["screens"]:
            del app_state["screens"][screen_id]
        print(f"Screen '{screen_id}' disconnected. Total screens: {len(app_state['screens'])}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app_state["connected_clients"].add(websocket)
    print(f"Client connected. Total: {len(app_state['connected_clients'])}")
    
    try:
        # Send missions list on connect
        missions = await get_all_missions()
        await websocket.send_json({
            "type": "missions_list",
            "data": missions
        })
        
        # Send default mission data
        default_id = await get_default_mission_id()
        mission = await get_full_mission(default_id)
        if mission:
            await websocket.send_json({
                "type": "mission_update",
                "data": await get_mission_detail(default_id)
            })
        
        # Keep connection alive, listen for messages
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif data.startswith("subscribe:"):
                # Client subscribing to a specific mission
                mission_id = data.split(":")[1]
                try:
                    mission_data = await get_mission_detail(mission_id)
                    await websocket.send_json({
                        "type": "mission_update",
                        "data": mission_data
                    })
                except HTTPException:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Mission {mission_id} not found"
                    })
            
            elif data.startswith("weather:"):
                # Client requesting weather for a mission
                mission_id = data.split(":")[1]
                try:
                    weather_data = await get_mission_weather_data(mission_id)
                    await websocket.send_json({
                        "type": "weather_update",
                        "data": weather_data
                    })
                except HTTPException as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e.detail)
                    })
    
    except WebSocketDisconnect:
        pass
    finally:
        app_state["connected_clients"].discard(websocket)
        print(f"Client disconnected. Total: {len(app_state['connected_clients'])}")


# === Static Files (Client) ===

if CLIENT_DIR.exists():
    # Mount static files at /static for explicit access
    app.mount("/static", StaticFiles(directory=CLIENT_DIR), name="static")
    
    # Serve JS files from root /js/ path (for relative imports in index.html)
    if (CLIENT_DIR / "js").exists():
        app.mount("/js", StaticFiles(directory=CLIENT_DIR / "js"), name="js")
    
    # Serve CSS files from root /css/ path
    if (CLIENT_DIR / "css").exists():
        app.mount("/css", StaticFiles(directory=CLIENT_DIR / "css"), name="css")
    
    # Serve docs files from root /docs/ path
    docs_dir = CLIENT_DIR.parent / "docs"
    if docs_dir.exists():
        app.mount("/docs", StaticFiles(directory=docs_dir, html=True), name="docs")
    
    # Serve mockups from root /mockups/ path (for iframe embeds)
    if (CLIENT_DIR / "mockups").exists():
        app.mount("/mockups", StaticFiles(directory=CLIENT_DIR / "mockups"), name="mockups")
    
    # Serve assets from root /assets/ path
    if (CLIENT_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=CLIENT_DIR / "assets"), name="assets")
    
    # Serve components from root /components/ path
    if (CLIENT_DIR / "components").exists():
        app.mount("/components", StaticFiles(directory=CLIENT_DIR / "components"), name="components")
    
    # Serve tabs from root /tabs/ path (for iframe-based tab architecture)
    if (CLIENT_DIR / "tabs").exists():
        app.mount("/tabs", StaticFiles(directory=CLIENT_DIR / "tabs"), name="tabs")
    
    # Serve images from root /images/ path
    if (CLIENT_DIR / "images").exists():
        app.mount("/images", StaticFiles(directory=CLIENT_DIR / "images"), name="images")
    
    @app.get("/")
    async def serve_client():
        return FileResponse(CLIENT_DIR / "index.html")
    
    @app.get("/shell")
    async def serve_shell():
        """New iframe-based shell architecture"""
        return FileResponse(CLIENT_DIR / "index-shell.html")
    
    @app.get("/kiosk")
    async def serve_kiosk():
        """New kiosk mode interface"""
        return FileResponse(CLIENT_DIR / "index2.html")
    
    @app.get("/index2.html")
    async def serve_index2():
        return FileResponse(CLIENT_DIR / "index2.html")

# === Run directly ===

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

