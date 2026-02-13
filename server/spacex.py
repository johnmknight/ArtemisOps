"""
ArtemisOps SpaceX Tracking Service
Fetches TLE data from CelesTrak for active SpaceX Crew Dragon capsules.
Client-side satellite.js handles SGP4 propagation from these TLEs.
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

# Known Crew Dragon NORAD IDs and names (updated as missions fly)
# We also do pattern matching on satellite names containing "DRAGON" or "CREW"
DRAGON_PATTERNS = ["CREW DRAGON", "DRAGON", "CREW-"]
# Known NORAD catalog IDs for recent Crew Dragons (backup identification)
KNOWN_DRAGON_IDS = {
    # These change per mission — pattern matching is primary method
}


def parse_tle_text(tle_text: str) -> List[Dict[str, Any]]:
    """Parse 3-line TLE format into structured objects."""
    lines = [l.strip() for l in tle_text.strip().splitlines() if l.strip()]
    satellites = []

    i = 0
    while i < len(lines) - 2:
        # TLE format: Name line, Line 1, Line 2
        name_line = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        # Validate TLE line format
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
            i += 1  # Skip malformed entries

    return satellites


def filter_dragons(satellites: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter satellite list to only Crew Dragon objects."""
    dragons = []
    for sat in satellites:
        name_upper = sat["name"].upper()
        if any(pattern in name_upper for pattern in DRAGON_PATTERNS):
            # Classify the dragon
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
    elif "RESILIENCE" in name_upper or "ENDEAVOUR" in name_upper or "ENDURANCE" in name_upper or "FREEDOM" in name_upper:
        return "crew"  # Named capsules are crew
    else:
        return "dragon"  # Generic


async def fetch_dragon_tles() -> List[Dict[str, Any]]:
    """Fetch and cache Crew Dragon TLEs from CelesTrak."""
    now = time.time()

    # Return cache if fresh
    if _tle_cache["data"] and (now - _tle_cache["fetched_at"]) < TLE_CACHE_TTL:
        logger.debug("Returning cached Dragon TLEs (%d objects)", len(_tle_cache["data"]))
        return _tle_cache["data"]

    dragons = []

    async with httpx.AsyncClient(timeout=15.0) as client:
        # Try stations group first (ISS-related objects including docked Dragons)
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
                    # Deduplicate by NORAD ID
                    if not any(existing["norad_id"] == d["norad_id"] for existing in dragons):
                        dragons.append(d)

            except Exception as e:
                logger.warning("Failed to fetch TLEs from [%s]: %s", label, e)

    # Update cache
    _tle_cache["data"] = dragons
    _tle_cache["fetched_at"] = now

    logger.info("Dragon TLE cache updated: %d objects", len(dragons))
    return dragons


async def get_dragons_response() -> Dict[str, Any]:
    """Build API response with Dragon TLEs and metadata."""
    dragons = await fetch_dragon_tles()

    return {
        "count": len(dragons),
        "cache_age_seconds": int(time.time() - _tle_cache["fetched_at"]),
        "dragons": [
            {
                "name": d["name"],
                "norad_id": d["norad_id"],
                "type": d.get("type", "dragon"),
                "tle": {
                    "line1": d["tle_line1"],
                    "line2": d["tle_line2"],
                },
            }
            for d in dragons
        ],
    }
