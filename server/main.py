"""
ArtemisOps Server - Mission Control Backend
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import httpx
import json
from pathlib import Path
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Paths
BASE_DIR = Path(__file__).parent
CLIENT_DIR = BASE_DIR.parent / "client"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# In-memory state
app_state = {
    "mission_data": None,
    "last_update": None,
    "connected_clients": set()
}

# Artemis II Crew Data - Official NASA Portraits
ARTEMIS_II_CREW = [
    {
        "name": "Reid Wiseman",
        "role": "Commander",
        "agency": "NASA",
        "photo": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2013e090068.jpg",
        "bio": "NASA astronaut and U.S. Navy Captain. Previously flew on Expedition 41 aboard the ISS in 2014.",
        "nasa_bio": "https://www.nasa.gov/people/reid-wiseman/",
        "missions": ["Expedition 41", "Artemis II"]
    },
    {
        "name": "Victor Glover",
        "role": "Pilot",
        "agency": "NASA",
        "photo": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2018e038718.jpg",
        "bio": "NASA astronaut and U.S. Navy Captain. Pilot of SpaceX Crew-1 and ISS Expedition 64 crew member.",
        "nasa_bio": "https://www.nasa.gov/people/victor-j-glover/",
        "missions": ["SpaceX Crew-1", "Expedition 64", "Artemis II"]
    },
    {
        "name": "Christina Koch",
        "role": "Mission Specialist",
        "agency": "NASA",
        "photo": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2018e038864.jpg",
        "bio": "NASA astronaut and electrical engineer. Holds record for longest single spaceflight by a woman (328 days).",
        "nasa_bio": "https://www.nasa.gov/people/christina-h-koch/",
        "missions": ["Expedition 59/60/61", "Artemis II"]
    },
    {
        "name": "Jeremy Hansen",
        "role": "Mission Specialist",
        "agency": "CSA",
        "photo": "https://www.asc-csa.gc.ca/images/recherche/tiles/5eed17e3-4a8f-46f5-8317-f372c3b79ece.jpg",
        "bio": "Canadian Space Agency astronaut and former CF-18 fighter pilot. First Canadian to fly to the Moon.",
        "nasa_bio": "https://www.asc-csa.gc.ca/eng/astronauts/canadian/active/bio-jeremy-hansen.asp",
        "missions": ["Artemis II"]
    }
]

scheduler = AsyncIOScheduler()


# === Data Fetching ===

async def fetch_mission_data():
    """Fetch latest mission data from Space Devs API"""
    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/?search=artemis"
    cache_file = CACHE_DIR / "mission_data.json"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Find Artemis II
            artemis2 = None
            for launch in data.get("results", []):
                name = launch.get("name", "").lower()
                if "artemis" in name and ("ii" in name or "2" in name):
                    artemis2 = launch
                    break
            
            if artemis2:
                mission_data = {
                    "name": artemis2.get("name"),
                    "launch_date": artemis2.get("net"),
                    "status": artemis2.get("status", {}).get("description"),
                    "site": artemis2.get("pad", {}).get("location", {}).get("name"),
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                    "source": "live"
                }
            else:
                mission_data = get_fallback_data()
                mission_data["source"] = "fallback"
            
            # Cache to file
            cache_file.write_text(json.dumps(mission_data, indent=2))
            
            # Update state
            app_state["mission_data"] = mission_data
            app_state["last_update"] = datetime.now(timezone.utc)
            
            # Notify connected WebSocket clients
            await broadcast_update(mission_data)
            
            print(f"[{datetime.now()}] Mission data updated: {mission_data.get('source')}")
            return mission_data
            
    except Exception as e:
        print(f"[{datetime.now()}] Fetch error: {e}")
        
        # Try to load from cache
        if cache_file.exists():
            cached = json.loads(cache_file.read_text())
            cached["source"] = "cached"
            app_state["mission_data"] = cached
            return cached
        
        # Use fallback
        fallback = get_fallback_data()
        app_state["mission_data"] = fallback
        return fallback


def get_fallback_data():
    """Fallback data when API unavailable"""
    return {
        "name": "Artemis II",
        "launch_date": "2026-04-01T12:00:00Z",
        "status": "Artemis II is in final preparations for humanity's return to lunar orbit.",
        "site": "Kennedy Space Center, FL",
        "source": "fallback"
    }


async def broadcast_update(data: dict):
    """Send update to all connected WebSocket clients"""
    disconnected = set()
    for ws in app_state["connected_clients"]:
        try:
            await ws.send_json({"type": "mission_update", "data": data})
        except:
            disconnected.add(ws)
    
    app_state["connected_clients"] -= disconnected


# === Lifespan ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("ArtemisOps Server starting...")
    await fetch_mission_data()
    scheduler.add_job(fetch_mission_data, 'interval', minutes=5)
    scheduler.start()
    print("Scheduler started - updating every 5 minutes")
    yield
    # Shutdown
    scheduler.shutdown()
    print("ArtemisOps Server stopped")


# === FastAPI App ===

app = FastAPI(
    title="ArtemisOps API",
    description="Mission Control Backend for NASA Artemis Missions",
    version="0.1.0",
    lifespan=lifespan
)


# === API Routes ===

@app.get("/api/mission")
async def get_mission():
    """Get current mission data"""
    if app_state["mission_data"]:
        return app_state["mission_data"]
    return await fetch_mission_data()


@app.get("/api/status")
async def get_status():
    """Server status endpoint"""
    return {
        "status": "ok",
        "last_update": app_state["last_update"].isoformat() if app_state["last_update"] else None,
        "connected_clients": len(app_state["connected_clients"]),
        "data_source": app_state["mission_data"].get("source") if app_state["mission_data"] else None
    }


@app.post("/api/refresh")
async def refresh_data():
    """Force refresh mission data"""
    data = await fetch_mission_data()
    return {"status": "refreshed", "data": data}


@app.get("/api/crew")
async def get_crew():
    """Get crew information for current mission"""
    return {
        "mission": "Artemis II",
        "crew": ARTEMIS_II_CREW
    }


# === WebSocket ===

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app_state["connected_clients"].add(websocket)
    print(f"Client connected. Total: {len(app_state['connected_clients'])}")
    
    try:
        # Send current data on connect
        if app_state["mission_data"]:
            await websocket.send_json({
                "type": "mission_update",
                "data": app_state["mission_data"]
            })
        
        # Keep connection alive, listen for messages
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
            if data == "ping":
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        pass
    finally:
        app_state["connected_clients"].discard(websocket)
        print(f"Client disconnected. Total: {len(app_state['connected_clients'])}")


# === Static Files (Client) ===

# Serve client files
if CLIENT_DIR.exists():
    app.mount("/static", StaticFiles(directory=CLIENT_DIR), name="static")
    
    @app.get("/")
    async def serve_client():
        return FileResponse(CLIENT_DIR / "index.html")


# === Run directly ===

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
