"""
ArtemisOps SpaceX Tracking Service
Fetches TLE data from CelesTrak for active SpaceX Crew Dragon capsules.
Enriches with mission data from our database for crew info, capsule names, etc.
Client-side satellite.js handles SGP4 propagation from TLEs.
"""
import time
import logging
import httpx
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Cache: { "data": [...], "fetched_at": timestamp }
_tle_cache: Dict[str, Any] = {"data": [], "fetched_at": 0}
TLE_CACHE_TTL = 3600  # 1 hour

# CelesTrak endpoints
CELESTRAK_ACTIVE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"
CELESTRAK_STATIONS_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"

# Pattern matching for Dragon identification in CelesTrak data
DRAGON_PATTERNS = ["CREW DRAGON", "DRAGON", "CREW-"]

# Known Dragon capsule names (for matching CelesTrak names to missions)
CAPSULE_NAMES = {
    "RESILIENCE": "C207",
    "ENDEAVOUR": "C206",
    "ENDURANCE": "C210",
    "FREEDOM": "C212",
    "GRACE": "C213",
}


def parse_tle_text(tle_text: str) -> List[Dict[str, Any]]:
    """Parse 3-line TLE format into structured objects."""
    lines = [l.strip() for l in tle_text.strip().splitlines() if l.strip()]
    satellites = []

    i = 0
    while i < len(lines) - 2:
        name_line = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        if line1.startswith("1 ") and line2.startswith("2 "):
            norad_id = line1[2:7].strip()
            satellites.append({
                "name": name_line.strip(),
                "norad_id": norad_id,
                "tle_line1": line1,
                "tle_line2": line2,
            })
            i += 3
        else:
            i += 1

    return satellites


def filter_dragons(satellites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter satellite list to only Dragon objects."""
    dragons = []
    for sat in satellites:
        name_upper = sat["name"].upper()
        if any(pattern in name_upper for pattern in DRAGON_PATTERNS):
            sat["type"] = classify_dragon(sat["name"])
            dragons.append(sat)
    return dragons


def classify_dragon(name: str) -> str:
    """Classify a Dragon satellite by its name."""
    name_upper = name.upper()
    if "CREW" in name_upper:
        return "crew"
    elif "CARGO" in name_upper or "CRS" in name_upper:
        return "cargo"
    elif any(cap in name_upper for cap in CAPSULE_NAMES):
        return "crew"  # Named capsules are crew
    else:
        return "dragon"


def match_tle_to_mission(tle_name: str, missions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Try to match a CelesTrak TLE name to a mission in our database."""
    name_upper = tle_name.upper()

    for mission in missions:
        m_name = (mission.get("name") or "").upper()
        m_spacecraft = (mission.get("spacecraft") or "").upper()

        # Direct name match: "CREW DRAGON 12" matches "Crew-12"
        # Extract number from TLE name
        for pattern in ["CREW DRAGON ", "CREW-", "DRAGON CRS-", "CRS-"]:
            if pattern in name_upper:
                suffix = name_upper.split(pattern)[-1].strip()
                if suffix and suffix in m_name:
                    return mission

        # Capsule name match: "FREEDOM" in TLE matches spacecraft "Crew Dragon Freedom"
        for capsule in CAPSULE_NAMES:
            if capsule in name_upper and capsule in m_spacecraft:
                return mission

    return None


async def fetch_dragon_tles() -> List[Dict[str, Any]]:
    """Fetch and cache Dragon TLEs from CelesTrak."""
    now = time.time()

    if _tle_cache["data"] and (now - _tle_cache["fetched_at"]) < TLE_CACHE_TTL:
        logger.debug("Returning cached Dragon TLEs (%d objects)", len(_tle_cache["data"]))
        return _tle_cache["data"]

    dragons = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        for url, label in [
            (CELESTRAK_STATIONS_URL, "stations"),
            (CELESTRAK_ACTIVE_URL, "active"),
        ]:
            try:
                logger.info("Fetching TLEs from CelesTrak [%s]...", label)
                resp = await client.get(url)
                resp.raise_for_status()

                all_sats = parse_tle_text(resp.text)
                found = filter_dragons(all_sats)
                logger.info("Found %d Dragon objects in [%s] (%d total satellites)",
                            len(found), label, len(all_sats))

                for d in found:
                    if not any(existing["norad_id"] == d["norad_id"] for existing in dragons):
                        dragons.append(d)

            except Exception as e:
                logger.warning("Failed to fetch TLEs from [%s]: %s", label, e)

    _tle_cache["data"] = dragons
    _tle_cache["fetched_at"] = now

    logger.info("Dragon TLE cache updated: %d objects", len(dragons))
    return dragons


def _is_dragon_mission(mission: Dict[str, Any]) -> bool:
    """Check if a mission is a Dragon mission (crew or cargo)."""
    name = (mission.get("name") or "").lower()
    spacecraft = (mission.get("spacecraft") or "").lower()
    rocket = (mission.get("rocket") or "").lower()

    # Crew Dragon missions
    if "crew-" in name or "crew dragon" in spacecraft or "dragon" in spacecraft:
        return True
    # CRS cargo missions
    if "crs-" in name or "cargo dragon" in spacecraft:
        return True
    # Falcon 9 + Dragon combo
    if "falcon" in rocket and "dragon" in spacecraft:
        return True

    return False


def _is_mission_inflight(mission: Dict[str, Any]) -> bool:
    """
    Determine if a mission is currently in flight.
    Handles multiple status formats:
      - Our seed data: "In Flight", "Go"
      - SpaceDevs API: "The launch vehicle successfully inserted its payload(s)..."
      - Completed missions: "Success", "Complete"
    """
    from datetime import datetime, timezone

    status = (mission.get("status") or "").lower()
    now = datetime.now(timezone.utc)

    # Explicit in-flight status
    if "in flight" in status:
        return True

    # Explicitly completed/failed — not in flight
    COMPLETED_KEYWORDS = ["success", "complete", "failed", "failure", "partial failure", "retired"]
    is_completed = any(kw in status for kw in COMPLETED_KEYWORDS)
    if is_completed:
        return False

    # Check if launched but not yet landed
    launch_date = mission.get("launch_date")
    landing_date = mission.get("landing_date")

    if launch_date:
        try:
            ld = datetime.fromisoformat(launch_date.replace("Z", "+00:00"))
            has_launched = ld < now
        except (ValueError, TypeError):
            has_launched = False
    else:
        has_launched = False

    if landing_date:
        try:
            rd = datetime.fromisoformat(landing_date.replace("Z", "+00:00"))
            has_landed = rd < now
        except (ValueError, TypeError):
            has_landed = False
    else:
        has_landed = False

    # Launched + no landing date = in flight (covers SpaceDevs "inserted into orbit" status)
    if has_launched and not landing_date:
        return True

    # Launched + landing date in the future = in flight
    if has_launched and landing_date and not has_landed:
        return True

    # "Go" with past launch date = in flight (pre-launch status that wasn't updated)
    if status == "go" and has_launched:
        return True

    return False


async def get_inflight_dragon_missions() -> List[Dict[str, Any]]:
    """
    Query our missions database for Dragon missions currently in flight.
    Returns mission metadata for enrichment.
    """
    try:
        from database import get_all_missions, get_full_mission

        all_missions = await get_all_missions()
        inflight = []

        for m in all_missions:
            if _is_mission_inflight(m) and _is_dragon_mission(m):
                # Get full mission data including crew
                full = await get_full_mission(m["id"])
                if full:
                    inflight.append(full)

        logger.info("Found %d in-flight Dragon missions in database", len(inflight))
        return inflight

    except Exception as e:
        logger.warning("Failed to query in-flight missions: %s", e)
        return []


def _build_dragon_entry(
    tle_data: Optional[Dict[str, Any]],
    mission: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build a unified Dragon entry from TLE data and/or mission data."""
    entry: Dict[str, Any] = {}

    if tle_data:
        entry["name"] = tle_data["name"]
        entry["norad_id"] = tle_data["norad_id"]
        entry["type"] = tle_data.get("type", "dragon")
        entry["tle"] = {
            "line1": tle_data["tle_line1"],
            "line2": tle_data["tle_line2"],
        }
        entry["tracking"] = "tle"
    else:
        entry["tle"] = None
        entry["tracking"] = "iss_position"  # Client should use ISS position

    if mission:
        entry["mission_id"] = mission.get("id")
        entry["mission_name"] = mission.get("name")
        entry["spacecraft"] = mission.get("spacecraft")
        entry["status"] = mission.get("status_description") or mission.get("status")
        entry["launch_date"] = mission.get("launch_date")
        entry["site"] = mission.get("site")
        entry["patch_url"] = mission.get("patch_url")
        entry["agencies"] = mission.get("agencies")
        entry["description"] = mission.get("description")

        # Crew info
        crew_list = mission.get("crew", [])
        entry["crew"] = [
            {
                "name": c.get("name"),
                "role": c.get("role"),
                "agency": c.get("agency"),
                "photo": c.get("photo_url"),
            }
            for c in crew_list
        ]
        entry["crew_count"] = len(crew_list)

        # Override type and name from mission if available
        name = (mission.get("name") or "").lower()
        if "crs" in name or "cargo" in name:
            entry["type"] = "cargo"
        else:
            entry["type"] = "crew"

        if not tle_data:
            entry["name"] = mission.get("spacecraft") or mission.get("name")
            entry["norad_id"] = None
    else:
        entry["mission_id"] = None
        entry["mission_name"] = None
        entry["spacecraft"] = None
        entry["crew"] = []
        entry["crew_count"] = 0

    return entry


async def get_dragons_response() -> Dict[str, Any]:
    """
    Build comprehensive API response with all Dragons currently in space.
    Merges CelesTrak TLE tracking data with mission database info.
    """
    # Fetch TLEs from CelesTrak
    tle_dragons = await fetch_dragon_tles()

    # Fetch in-flight Dragon missions from our DB
    inflight_missions = await get_inflight_dragon_missions()

    # Build merged results
    results = []
    matched_mission_ids = set()

    # Process TLE-tracked Dragons first
    for tle in tle_dragons:
        mission = match_tle_to_mission(tle["name"], inflight_missions)
        if mission:
            matched_mission_ids.add(mission["id"])
        results.append(_build_dragon_entry(tle, mission))

    # Add in-flight missions without TLEs (just launched, etc.)
    for mission in inflight_missions:
        if mission["id"] not in matched_mission_ids:
            results.append(_build_dragon_entry(None, mission))

    return {
        "count": len(results),
        "cache_age_seconds": int(time.time() - _tle_cache["fetched_at"]) if _tle_cache["fetched_at"] else 0,
        "dragons": results,
    }
