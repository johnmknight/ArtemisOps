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
from weather import get_mission_weather, is_within_forecast_window, is_same_day, get_hours_until
from iss import get_iss_position, get_iss_crew, get_nasa_telemetry, get_iss_combined, get_location_name, get_iss_news

# Paths
BASE_DIR = Path(__file__).parent
CLIENT_DIR = BASE_DIR.parent / "client"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# In-memory state
app_state = {
    "connected_clients": set(),  # WebSocket connections
    "last_sync": None,
    "weather_cache": {},  # Cache weather data per mission
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
    
    # Initial sync (fetch upcoming missions)
    await sync_all_missions()
    app_state["last_sync"] = datetime.now(timezone.utc)
    
    # Schedule sync every 12 hours (upcoming missions don't change often)
    scheduler.add_job(scheduled_sync, 'interval', hours=12, id='mission_sync')
    scheduler.start()
    print("Scheduler started - syncing every 12 hours")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("ArtemisOps Server stopped")


# === FastAPI App ===

app = FastAPI(
    title="ArtemisOps API",
    description="Mission Control Backend for NASA and ESA Crewed Missions",
    version="0.5.0",
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
    """Get default mission (Artemis II) - legacy endpoint"""
    return await get_mission_detail("artemis-ii")


@app.get("/api/crew")
async def get_default_crew():
    """Get crew for default mission - legacy endpoint"""
    mission = await get_full_mission("artemis-ii")
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
async def get_iss_position_data():
    """
    Get current ISS position (latitude, longitude, altitude, velocity).
    Data from Where The ISS At API, with Open Notify as fallback.
    """
    try:
        return await get_iss_position()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS position unavailable: {str(e)}")


@app.get("/api/iss/crew")
async def get_iss_crew_data():
    """
    Get current ISS crew roster.
    Data from Open Notify API.
    """
    try:
        return await get_iss_crew()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS crew data unavailable: {str(e)}")


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


@app.get("/api/iss/news")
async def get_iss_news_data(limit: int = 10):
    """
    Get latest ISS news from NASA ISS Blog and Spaceflight Now.
    Data is cached for 15 minutes.
    """
    try:
        return await get_iss_news(limit)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ISS news unavailable: {str(e)}")


@app.get("/api/status")
async def get_status():
    """Server status endpoint"""
    last_sync = await get_last_sync()
    missions = await get_all_missions()
    return {
        "status": "ok",
        "last_sync": last_sync["synced_at"] if last_sync else None,
        "connected_clients": len(app_state["connected_clients"]),
        "total_missions": len(missions),
        "weather_cache_size": len(app_state["weather_cache"]),
        "version": "0.5.0"
    }


@app.post("/api/sync")
async def trigger_sync():
    """Manually trigger data sync"""
    result = await sync_all_missions()
    await broadcast_missions_list()
    return result


# === WebSocket ===

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
        mission = await get_full_mission("artemis-ii")
        if mission:
            await websocket.send_json({
                "type": "mission_update",
                "data": await get_mission_detail("artemis-ii")
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
    
    @app.get("/")
    async def serve_client():
        return FileResponse(CLIENT_DIR / "index.html")
    
    @app.get("/shell")
    async def serve_shell():
        """New iframe-based shell architecture"""
        return FileResponse(CLIENT_DIR / "index-shell.html")
    
    @app.get("/mission-control.html")
    async def serve_mission_control():
        return FileResponse(CLIENT_DIR / "mission-control.html")
    
    @app.get("/mission-control")
    async def serve_mission_control_alt():
        return FileResponse(CLIENT_DIR / "mission-control.html")


# === Run directly ===

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
