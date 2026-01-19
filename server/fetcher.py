"""
ArtemisOps Data Fetcher
Fetches mission data from Space Devs API and updates database
"""
import httpx
from datetime import datetime, timezone
from typing import Optional
import re

from database import (
    upsert_mission, upsert_crew, upsert_milestones,
    log_sync, get_all_missions
)


# Space Devs API endpoints
SPACE_DEVS_BASE = "https://ll.thespacedevs.com/2.2.0"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


async def fetch_artemis_missions() -> list[dict]:
    """Fetch all Artemis missions from Space Devs API"""
    missions = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Search for Artemis launches
            response = await client.get(
                f"{SPACE_DEVS_BASE}/launch/",
                params={
                    "search": "artemis",
                    "mode": "detailed",
                    "limit": 20
                }
            )
            response.raise_for_status()
            data = response.json()
            
            for launch in data.get("results", []):
                name = launch.get("name", "")
                
                # Filter for actual Artemis missions
                if "artemis" not in name.lower():
                    continue
                
                mission = parse_launch_to_mission(launch)
                if mission:
                    missions.append(mission)
            
            print(f"Fetched {len(missions)} Artemis missions from Space Devs")
            
    except Exception as e:
        print(f"Error fetching from Space Devs: {e}")
    
    return missions


def parse_launch_to_mission(launch: dict) -> Optional[dict]:
    """Parse Space Devs launch data into our mission format"""
    try:
        name = launch.get("name", "Unknown Mission")
        
        # Extract mission name (e.g., "Artemis II" from "SLS | Artemis II")
        if "|" in name:
            name = name.split("|")[-1].strip()
        
        mission_id = slugify(name)
        
        # Get status info
        status = launch.get("status", {})
        status_name = status.get("abbrev", "Unknown")
        status_desc = status.get("description", "")
        
        # Get pad/site info
        pad = launch.get("pad", {})
        location = pad.get("location", {})
        site = location.get("name", "Unknown")
        
        # Get rocket info
        rocket = launch.get("rocket", {})
        rocket_name = rocket.get("configuration", {}).get("name", "")
        
        # Get spacecraft info
        spacecraft = ""
        mission_info = launch.get("mission", {}) or {}
        if mission_info:
            spacecraft = mission_info.get("name", "")
        
        # Get image
        image_url = launch.get("image")
        
        return {
            "id": mission_id,
            "name": name,
            "slug": mission_id,
            "launch_date": launch.get("net"),
            "status": status_name,
            "status_description": status_desc,
            "site": site,
            "rocket": rocket_name,
            "spacecraft": spacecraft,
            "mission_type": mission_info.get("type", ""),
            "description": mission_info.get("description", ""),
            "image_url": image_url,
            "api_id": launch.get("id"),
            "api_source": "spacedevs",
            "is_active": 1
        }
        
    except Exception as e:
        print(f"Error parsing launch: {e}")
        return None


async def fetch_crew_for_mission(api_id: str) -> list[dict]:
    """Fetch crew for a specific launch from Space Devs"""
    crew = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{SPACE_DEVS_BASE}/launch/{api_id}/"
            )
            response.raise_for_status()
            launch = response.json()
            
            # Get crew from rocket configuration
            rocket = launch.get("rocket", {})
            spacecraft_stage = rocket.get("spacecraft_stage", {})
            
            if spacecraft_stage:
                launch_crew = spacecraft_stage.get("launch_crew", [])
                
                for i, crew_member in enumerate(launch_crew):
                    astronaut = crew_member.get("astronaut", {})
                    if astronaut:
                        crew.append({
                            "name": astronaut.get("name"),
                            "role": crew_member.get("role", {}).get("role", "Crew"),
                            "agency": astronaut.get("agency", {}).get("abbrev", ""),
                            "photo_url": astronaut.get("profile_image"),
                            "bio": astronaut.get("bio", ""),
                            "bio_url": astronaut.get("wiki"),
                            "api_id": str(astronaut.get("id")),
                            "sort_order": i
                        })
            
            print(f"Fetched {len(crew)} crew members for launch {api_id}")
            
    except Exception as e:
        print(f"Error fetching crew: {e}")
    
    return crew


# Fallback crew data for Artemis II (in case API doesn't have it)
ARTEMIS_II_CREW_FALLBACK = [
    {
        "name": "Reid Wiseman",
        "role": "Commander",
        "agency": "NASA",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2013e090068.jpg",
        "bio": "NASA astronaut and U.S. Navy Captain. Previously flew on Expedition 41 aboard the ISS in 2014.",
        "bio_url": "https://www.nasa.gov/people/reid-wiseman/",
    },
    {
        "name": "Victor Glover",
        "role": "Pilot",
        "agency": "NASA",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2018e038718.jpg",
        "bio": "NASA astronaut and U.S. Navy Captain. Pilot of SpaceX Crew-1 and ISS Expedition 64 crew member.",
        "bio_url": "https://www.nasa.gov/people/victor-j-glover/",
    },
    {
        "name": "Christina Koch",
        "role": "Mission Specialist",
        "agency": "NASA",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/03/jsc2018e038864.jpg",
        "bio": "NASA astronaut and electrical engineer. Holds record for longest single spaceflight by a woman (328 days).",
        "bio_url": "https://www.nasa.gov/people/christina-h-koch/",
    },
    {
        "name": "Jeremy Hansen",
        "role": "Mission Specialist",
        "agency": "CSA",
        "photo_url": "https://www.asc-csa.gc.ca/images/recherche/tiles/5eed17e3-4a8f-46f5-8317-f372c3b79ece.jpg",
        "bio": "Canadian Space Agency astronaut and former CF-18 fighter pilot. First Canadian to fly to the Moon.",
        "bio_url": "https://www.asc-csa.gc.ca/eng/astronauts/canadian/active/bio-jeremy-hansen.asp",
    }
]

# Fallback milestones for Artemis II
ARTEMIS_II_MILESTONES_FALLBACK = [
    {"date_label": "Dec 2025", "title": "Flight Readiness Review", "description": "Final comprehensive review of all mission systems", "status": "completed"},
    {"date_label": "Jan 2, 2026", "title": "Crew Quarantine Begins", "description": "Flight crew enters health stabilization program", "status": "completed"},
    {"date_label": "Jan 17, 2026", "title": "Rollout to Pad 39B", "description": "SLS transported from VAB to launch complex", "status": "active"},
    {"date_label": "Jan 27, 2026", "title": "Wet Dress Rehearsal", "description": "Full countdown simulation with propellant loading", "status": "pending"},
    {"date_label": "T-6:40:00", "title": "Cryo Loading", "description": "Begin loading liquid hydrogen and oxygen", "status": "pending"},
    {"date_label": "T-2:35:00", "title": "Crew Ingress", "description": "Four astronauts board Orion spacecraft", "status": "pending"},
    {"date_label": "T-00:00", "title": "LIFTOFF", "description": "RS-25 engines and SRBs ignite", "status": "pending"},
]


async def sync_all_missions() -> dict:
    """
    Main sync function - fetches all Artemis missions and updates database
    Called hourly by scheduler
    """
    result = {
        "status": "success",
        "missions_updated": 0,
        "errors": []
    }
    
    try:
        # Fetch missions from API
        missions = await fetch_artemis_missions()
        
        for mission in missions:
            try:
                # Save mission
                await upsert_mission(mission)
                result["missions_updated"] += 1
                
                # Fetch and save crew if API has it
                if mission.get("api_id"):
                    crew = await fetch_crew_for_mission(mission["api_id"])
                    
                    # Use fallback for Artemis II if API doesn't have crew
                    if not crew and "artemis-ii" in mission["id"]:
                        crew = ARTEMIS_II_CREW_FALLBACK
                    
                    if crew:
                        await upsert_crew(mission["id"], crew)
                
                # Add fallback milestones for Artemis II
                if "artemis-ii" in mission["id"]:
                    await upsert_milestones(mission["id"], ARTEMIS_II_MILESTONES_FALLBACK)
                
            except Exception as e:
                error_msg = f"Error syncing {mission.get('name')}: {e}"
                print(error_msg)
                result["errors"].append(error_msg)
        
        # Log successful sync
        await log_sync("spacedevs", "success", result["missions_updated"])
        print(f"Sync complete: {result['missions_updated']} missions updated")
        
    except Exception as e:
        result["status"] = "error"
        result["errors"].append(str(e))
        await log_sync("spacedevs", "error", 0, str(e))
        print(f"Sync failed: {e}")
    
    return result


async def ensure_default_missions():
    """Ensure we have at least Artemis II in the database"""
    missions = await get_all_missions()
    
    if not any("artemis-ii" in m["id"] for m in missions):
        print("No Artemis II found, creating default...")
        
        # Create default Artemis II mission
        await upsert_mission({
            "id": "artemis-ii",
            "name": "Artemis II",
            "slug": "artemis-ii",
            "launch_date": "2026-02-06T12:00:00Z",
            "status": "Go",
            "status_description": "Artemis II is in final preparations for humanity's return to lunar orbit.",
            "site": "Kennedy Space Center, FL",
            "rocket": "SLS Block 1",
            "spacecraft": "Orion",
            "mission_type": "Human Exploration",
            "description": "First crewed Artemis mission, sending four astronauts around the Moon.",
            "image_url": "https://www.nasa.gov/wp-content/uploads/2023/04/52790983768-79132211b6-k-2.jpg",
            "api_source": "fallback",
            "is_active": 1
        })
        
        await upsert_crew("artemis-ii", ARTEMIS_II_CREW_FALLBACK)
        await upsert_milestones("artemis-ii", ARTEMIS_II_MILESTONES_FALLBACK)
        
        print("Created default Artemis II mission with crew and milestones")
