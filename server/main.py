"""
ArtemisOps Server - Mission Control Backend
Multi-mission support with hourly data sync
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database import (
    init_db, get_all_missions, get_full_mission,
    get_last_sync
)
from fetcher import sync_all_missions, ensure_default_missions

# Paths
BASE_DIR = Path(__file__).parent
CLIENT_DIR = BASE_DIR.parent / "client"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# In-memory state
app_state = {
    "connected_clients": set(),  # WebSocket connections
    "last_sync": None
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
    
    # Initial sync
    await sync_all_missions()
    app_state["last_sync"] = datetime.now(timezone.utc)
    
    # Schedule hourly sync
    scheduler.add_job(scheduled_sync, 'interval', hours=1, id='hourly_sync')
    scheduler.start()
    print("Scheduler started - syncing every hour")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("ArtemisOps Server stopped")


# === FastAPI App ===

app = FastAPI(
    title="ArtemisOps API",
    description="Mission Control Backend for NASA Artemis Missions",
    version="0.2.0",
    lifespan=lifespan
)


# === API Routes ===

@app.get("/api/missions")
async def list_missions():
    """Get all active missions"""
    missions = await get_all_missions()
    return {"missions": missions}


@app.get("/api/missions/{mission_id}")
async def get_mission_detail(mission_id: str):
    """Get full mission data including crew and milestones"""
    mission = await get_full_mission(mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Transform for client compatibility
    return {
        "id": mission["id"],
        "name": mission["name"],
        "launch_date": mission["launch_date"],
        "status": mission["status_description"] or mission["status"],
        "site": mission["site"],
        "source": mission.get("api_source", "database"),
        "image_url": mission.get("image_url"),
        "rocket": mission.get("rocket"),
        "spacecraft": mission.get("spacecraft"),
        "description": mission.get("description"),
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


@app.get("/api/status")
async def get_status():
    """Server status endpoint"""
    last_sync = await get_last_sync()
    return {
        "status": "ok",
        "last_sync": last_sync["synced_at"] if last_sync else None,
        "connected_clients": len(app_state["connected_clients"]),
        "version": "0.2.0"
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
                mission_data = await get_full_mission(mission_id)
                if mission_data:
                    await websocket.send_json({
                        "type": "mission_update",
                        "data": await get_mission_detail(mission_id)
                    })
    
    except WebSocketDisconnect:
        pass
    finally:
        app_state["connected_clients"].discard(websocket)
        print(f"Client disconnected. Total: {len(app_state['connected_clients'])}")


# === Static Files (Client) ===

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
