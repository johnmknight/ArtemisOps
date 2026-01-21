"""
ArtemisOps Data Fetcher
Fetches mission data from Space Devs API and updates database
Supports NASA and ESA crewed missions

PATCH & LOGO STRATEGY:
- Patches and logos are fetched DURING SYNC and stored in the database
- This provides consistent, fast access without per-request API calls
- Priority: Space Devs API → Hardcoded fallbacks → Launch image
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

# ============================================================================
# HARDCODED FALLBACKS
# These are used when the API doesn't have patch/logo data
# ============================================================================

FALLBACK_PATCHES = {
    "artemis ii": "https://www.nasa.gov/wp-content/uploads/2025/04/jsc2025e034746orig.jpg",
    "artemis iii": "https://www.nasa.gov/wp-content/uploads/2023/09/artemis-iii-patch-final.png",
    "crew dragon": "https://upload.wikimedia.org/wikipedia/commons/2/2e/SpaceX_Dragon_2_insignia.png",
}

FALLBACK_AGENCY_LOGOS = {
    "NASA": "https://www.nasa.gov/wp-content/uploads/2023/04/nasa-logo-web-rgb.png",
    "ESA": "https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2020/05/esa_logo_white_background/21973314-1-eng-GB/ESA_logo_white_background_pillars.jpg",
    "CSA": "https://www.asc-csa.gc.ca/images/recherche/tiles/csa-logo.jpg",
    "JAXA": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Jaxa_logo.svg/1200px-Jaxa_logo.svg.png",
    "SpaceX": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/SpaceX-Logo.svg/1200px-SpaceX-Logo.svg.png",
    "Boeing": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Boeing_full_logo.svg/1200px-Boeing_full_logo.svg.png",
    "Roscosmos": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Roscosmos_logo_en.svg/1200px-Roscosmos_logo_en.svg.png",
}

# Agency abbreviation to Space Devs ID mapping
AGENCY_NAME_TO_ID = {
    "NASA": 44,
    "ESA": 27,
    "CSA": 16,
    "JAXA": 37,
    "SpaceX": 121,
    "Roscosmos": 63,
    "CNSA": 17,
    "Boeing": 80,
}

# Agency IDs for filtering
AGENCY_IDS = {
    "nasa": 44,
    "esa": 27,
}

# Programs we're interested in
PROGRAMS_OF_INTEREST = [
    "artemis",
    "commercial crew",
    "iss",
    "international space station",
    "crew dragon",
    "starliner",
    "axiom",
]

# Maximum mission duration in days (for filtering old completed missions)
MAX_MISSION_DURATION_DAYS = 200


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


# ============================================================================
# PATCH & LOGO FETCHING (called during sync)
# ============================================================================

async def fetch_patch_from_api(mission_name: str, client: httpx.AsyncClient) -> Optional[str]:
    """
    Search Space Devs /mission_patch/ endpoint for a mission patch.
    Returns the image_url if found, None otherwise.
    """
    try:
        response = await client.get(
            f"{SPACE_DEVS_BASE}/mission_patch/",
            params={
                "name__contains": mission_name,
                "limit": 5,
                "ordering": "-priority"
            }
        )
        response.raise_for_status()
        data = response.json()
        
        results = data.get("results", [])
        if results:
            patch_url = results[0].get("image_url")
            if patch_url:
                print(f"  → Found API patch for '{mission_name}'")
                return patch_url
    except Exception as e:
        print(f"  → Patch API error for '{mission_name}': {e}")
    
    return None


async def fetch_agency_logo_from_api(agency_id: int, client: httpx.AsyncClient) -> Optional[str]:
    """
    Fetch agency logo from Space Devs /agencies/ endpoint.
    Returns logo_url or image_url if found.
    """
    try:
        response = await client.get(f"{SPACE_DEVS_BASE}/agencies/{agency_id}/")
        response.raise_for_status()
        data = response.json()
        
        logo_url = data.get("logo_url") or data.get("image_url")
        if logo_url:
            return logo_url
    except Exception as e:
        print(f"  → Agency logo API error for ID {agency_id}: {e}")
    
    return None


async def get_mission_patch(mission_name: str, launch_image: str, client: httpx.AsyncClient) -> str:
    """
    Get the best available patch for a mission.
    
    Priority:
    1. Space Devs /mission_patch/ API
    2. Hardcoded fallback patches
    3. Launch image from API
    """
    name_lower = mission_name.lower().strip()
    
    # 1. Try Space Devs mission_patch API
    api_patch = await fetch_patch_from_api(mission_name, client)
    if api_patch:
        return api_patch
    
    # 2. Check hardcoded fallbacks
    for key, url in FALLBACK_PATCHES.items():
        if key in name_lower:
            print(f"  → Using fallback patch for '{mission_name}'")
            return url
    
    # 3. Fall back to launch image
    if launch_image:
        print(f"  → Using launch image for '{mission_name}'")
        return launch_image
    
    return None


async def get_agency_logo(agencies_str: str, client: httpx.AsyncClient) -> str:
    """
    Get the primary agency logo.
    
    Priority:
    1. Space Devs /agencies/ API
    2. Hardcoded fallback logos
    3. NASA logo as default
    """
    if not agencies_str:
        return FALLBACK_AGENCY_LOGOS.get("NASA")
    
    # Get primary agency (first in comma-separated list)
    primary_agency = agencies_str.split(",")[0].strip()
    
    # Try to get agency ID
    agency_id = AGENCY_NAME_TO_ID.get(primary_agency)
    
    # 1. Try Space Devs API if we have an ID
    if agency_id:
        api_logo = await fetch_agency_logo_from_api(agency_id, client)
        if api_logo:
            return api_logo
    
    # 2. Check hardcoded fallbacks (with partial matching)
    for key, url in FALLBACK_AGENCY_LOGOS.items():
        if key.lower() in primary_agency.lower() or primary_agency.lower() in key.lower():
            return url
    
    # 3. Default to NASA
    return FALLBACK_AGENCY_LOGOS.get("NASA")


# ============================================================================
# MISSION FETCHING
# ============================================================================

async def fetch_crewed_missions() -> list[dict]:
    """
    Fetch NASA and ESA crewed missions from Space Devs API.
    Also fetches patch and logo URLs for each mission.
    """
    missions = []
    seen_ids = set()
    now = datetime.now(timezone.utc)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Fetch upcoming crewed launches
        try:
            response = await client.get(
                f"{SPACE_DEVS_BASE}/launch/upcoming/",
                params={
                    "mode": "detailed",
                    "limit": 50,
                    "include_suborbital": False,
                    "is_crewed": True,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            for launch in data.get("results", []):
                if is_nasa_or_esa_mission(launch):
                    mission = await parse_launch_to_mission(launch, client)
                    if mission and mission["id"] not in seen_ids:
                        missions.append(mission)
                        seen_ids.add(mission["id"])
            
            print(f"Fetched {len(missions)} upcoming crewed missions")
            
        except Exception as e:
            print(f"Error fetching upcoming crewed launches: {e}")
        
        # Fetch recent past crewed launches
        try:
            response = await client.get(
                f"{SPACE_DEVS_BASE}/launch/previous/",
                params={
                    "mode": "detailed",
                    "limit": 15,
                    "is_crewed": True,
                }
            )
            response.raise_for_status()
            data = response.json()
            
            past_count = 0
            for launch in data.get("results", []):
                launch_date_str = launch.get("net")
                if launch_date_str:
                    try:
                        launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
                        days_ago = (now - launch_date).days
                        if days_ago > MAX_MISSION_DURATION_DAYS:
                            continue
                    except:
                        pass
                
                if is_nasa_or_esa_mission(launch):
                    mission = await parse_launch_to_mission(launch, client)
                    if mission and mission["id"] not in seen_ids:
                        missions.append(mission)
                        seen_ids.add(mission["id"])
                        past_count += 1
            
            print(f"Fetched {past_count} recent/in-progress crewed missions")
            
        except Exception as e:
            print(f"Error fetching past crewed launches: {e}")
        
        # Also search for Artemis missions
        try:
            response = await client.get(
                f"{SPACE_DEVS_BASE}/launch/upcoming/",
                params={
                    "search": "artemis",
                    "mode": "detailed",
                    "limit": 20
                }
            )
            response.raise_for_status()
            data = response.json()
            
            artemis_count = 0
            for launch in data.get("results", []):
                name = launch.get("name", "").lower()
                if "artemis" in name:
                    mission = await parse_launch_to_mission(launch, client)
                    if mission and mission["id"] not in seen_ids:
                        missions.append(mission)
                        seen_ids.add(mission["id"])
                        artemis_count += 1
            
            print(f"Fetched {artemis_count} additional Artemis missions")
            
        except Exception as e:
            print(f"Error fetching Artemis launches: {e}")
    
    print(f"Total missions fetched: {len(missions)}")
    return missions


def is_nasa_or_esa_mission(launch: dict) -> bool:
    """Check if a launch involves NASA or ESA"""
    lsp = launch.get("launch_service_provider", {})
    lsp_id = lsp.get("id")
    lsp_name = (lsp.get("name") or "").lower()
    
    if lsp_id in AGENCY_IDS.values():
        return True
    if "nasa" in lsp_name or "esa" in lsp_name:
        return True
    
    rocket = launch.get("rocket", {})
    config = rocket.get("configuration", {})
    manufacturer = (config.get("manufacturer", {}).get("name") or "").lower()
    
    if "nasa" in manufacturer or "esa" in manufacturer:
        return True
    
    mission = launch.get("mission", {})
    if mission:
        agencies = mission.get("agencies", []) or []
        for agency in agencies:
            agency_name = (agency.get("name") or "").lower()
            agency_id = agency.get("id")
            if agency_id in AGENCY_IDS.values() or "nasa" in agency_name or "esa" in agency_name:
                return True
    
    programs = launch.get("program", []) or []
    for program in programs:
        prog_name = (program.get("name") or "").lower()
        for interest in PROGRAMS_OF_INTEREST:
            if interest in prog_name:
                return True
        prog_agencies = program.get("agencies", []) or []
        for agency in prog_agencies:
            agency_id = agency.get("id")
            if agency_id in AGENCY_IDS.values():
                return True
    
    pad = launch.get("pad", {})
    location = pad.get("location", {})
    country_code = location.get("country_code", "")
    if country_code in ["USA", "GUF"]:
        spacecraft_stage = rocket.get("spacecraft_stage", {})
        if spacecraft_stage and spacecraft_stage.get("launch_crew"):
            return True
    
    return False


async def parse_launch_to_mission(launch: dict, client: httpx.AsyncClient) -> Optional[dict]:
    """
    Parse Space Devs launch data into our mission format.
    Includes fetching patch and logo URLs.
    """
    try:
        name = launch.get("name", "Unknown Mission")
        if "|" in name:
            name = name.split("|")[-1].strip()
        
        mission_id = slugify(name)
        
        status = launch.get("status", {})
        status_name = status.get("abbrev", "Unknown")
        status_desc = status.get("description", "")
        
        pad = launch.get("pad", {})
        location = pad.get("location", {})
        site = location.get("name", "Unknown")
        
        rocket = launch.get("rocket", {})
        rocket_name = rocket.get("configuration", {}).get("name", "")
        
        spacecraft = ""
        spacecraft_stage = rocket.get("spacecraft_stage", {})
        if spacecraft_stage:
            spacecraft_config = spacecraft_stage.get("spacecraft", {})
            if spacecraft_config:
                spacecraft = spacecraft_config.get("name", "")
        
        mission_info = launch.get("mission", {}) or {}
        if not spacecraft and mission_info:
            spacecraft = mission_info.get("name", "")
        
        image_url = launch.get("image")
        
        programs = launch.get("program", []) or []
        program_names = [p.get("name", "") for p in programs]
        
        mission_type = mission_info.get("type", "") if mission_info else ""
        if not mission_type and programs:
            mission_type = ", ".join(program_names[:2])
        
        # Get agencies
        agencies = []
        lsp = launch.get("launch_service_provider", {})
        if lsp.get("name"):
            agencies.append(lsp.get("abbrev") or lsp.get("name"))
        
        if mission_info:
            for agency in (mission_info.get("agencies", []) or []):
                abbrev = agency.get("abbrev") or agency.get("name")
                if abbrev and abbrev not in agencies:
                    agencies.append(abbrev)
        
        agencies_str = ", ".join(agencies)
        
        description = mission_info.get("description", "") if mission_info else ""
        if not description and programs:
            for prog in programs:
                if prog.get("description"):
                    description = prog.get("description")
                    break
        
        # Fetch patch and logo URLs (THE KEY STEP)
        print(f"Fetching images for: {name}")
        patch_url = await get_mission_patch(name, image_url, client)
        agency_logo_url = await get_agency_logo(agencies_str, client)
        
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
            "mission_type": mission_type,
            "description": description,
            "image_url": image_url,
            "patch_url": patch_url,
            "agency_logo_url": agency_logo_url,
            "api_id": launch.get("id"),
            "api_source": "spacedevs",
            "is_active": 1,
            "agencies": agencies_str,
        }
        
    except Exception as e:
        print(f"Error parsing launch: {e}")
        return None


async def fetch_crew_for_mission(api_id: str) -> list[dict]:
    """Fetch crew for a specific launch from Space Devs"""
    crew = []
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{SPACE_DEVS_BASE}/launch/{api_id}/")
            response.raise_for_status()
            launch = response.json()
            
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


# ============================================================================
# FALLBACK DATA
# ============================================================================

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

ARTEMIS_II_MILESTONES_FALLBACK = [
    {"date_label": "Dec 2025", "title": "Flight Readiness Review", "description": "Final comprehensive review of all mission systems", "status": "completed"},
    {"date_label": "Jan 2, 2026", "title": "Crew Quarantine Begins", "description": "Flight crew enters health stabilization program", "status": "completed"},
    {"date_label": "Jan 17, 2026", "title": "Rollout to Pad 39B", "description": "SLS transported from VAB to launch complex", "status": "active"},
    {"date_label": "Jan 27, 2026", "title": "Wet Dress Rehearsal", "description": "Full countdown simulation with propellant loading", "status": "pending"},
    {"date_label": "T-6:40:00", "title": "Cryo Loading", "description": "Begin loading liquid hydrogen and oxygen", "status": "pending"},
    {"date_label": "T-2:35:00", "title": "Crew Ingress", "description": "Four astronauts board Orion spacecraft", "status": "pending"},
    {"date_label": "T-00:00", "title": "LIFTOFF", "description": "RS-25 engines and SRBs ignite", "status": "pending"},
]


# ============================================================================
# SYNC FUNCTIONS
# ============================================================================

async def sync_all_missions() -> dict:
    """
    Main sync function - fetches all NASA/ESA crewed missions and updates database.
    Called hourly by scheduler.
    
    This fetches patches and logos DURING sync, storing them in the database.
    """
    result = {
        "status": "success",
        "missions_updated": 0,
        "errors": []
    }
    
    try:
        missions = await fetch_crewed_missions()
        
        for mission in missions:
            try:
                await upsert_mission(mission)
                result["missions_updated"] += 1
                
                if mission.get("api_id"):
                    crew = await fetch_crew_for_mission(mission["api_id"])
                    
                    if not crew and "artemis-ii" in mission["id"]:
                        crew = ARTEMIS_II_CREW_FALLBACK
                    
                    if crew:
                        await upsert_crew(mission["id"], crew)
                
                if "artemis-ii" in mission["id"]:
                    await upsert_milestones(mission["id"], ARTEMIS_II_MILESTONES_FALLBACK)
                
            except Exception as e:
                error_msg = f"Error syncing {mission.get('name')}: {e}"
                print(error_msg)
                result["errors"].append(error_msg)
        
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
    missions = await get_all_missions(active_only=False)
    
    if not any("artemis-ii" in m["id"] for m in missions):
        print("No Artemis II found, creating default...")
        
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
            "patch_url": FALLBACK_PATCHES.get("artemis ii"),
            "agency_logo_url": FALLBACK_AGENCY_LOGOS.get("NASA"),
            "api_source": "fallback",
            "is_active": 1,
            "agencies": "NASA, CSA",
        })
        
        await upsert_crew("artemis-ii", ARTEMIS_II_CREW_FALLBACK)
        await upsert_milestones("artemis-ii", ARTEMIS_II_MILESTONES_FALLBACK)
        
        print("Created default Artemis II mission with crew and milestones")
