"""
ArtemisOps ISS Data Service
Server-side proxy for ISS position and crew data.

Data Sources:
- Where The ISS At API: Position, altitude, velocity, visibility
- Open Notify API: Crew roster (Phase 1: names)
- NASA ISS Blog: Crew enrichment (Phase 2: agency affiliations)

Note: NASA Lightstreamer telemetry (cabin pressure, temp, O2) is currently
handled client-side due to complexity of Python Lightstreamer integration.
This can be moved server-side in a future update.
"""
import asyncio
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import logging
from crew_enrichment import fetch_crew_agencies, enrich_crew_with_agencies

logger = logging.getLogger(__name__)

# === Configuration ===

WHERETHEISS_API = "https://api.wheretheiss.at/v1/satellites/25544"
OPEN_NOTIFY_POSITION_API = "http://api.open-notify.org/iss-now.json"
OPEN_NOTIFY_CREW_API = "http://api.open-notify.org/astros.json"

# Cache settings (seconds)
POSITION_CACHE_TTL = 10   # ~77km drift at ISS speed, fine for world map
CREW_CACHE_TTL = 3600     # Crew changes rarely (1 hour)

# In-memory cache
_cache = {
    "position": {"data": None, "timestamp": None},
    "crew": {"data": None, "timestamp": None},
}

# Shared HTTP client (connection pooling)
_http_client: Optional[httpx.AsyncClient] = None


def _get_client() -> httpx.AsyncClient:
    """Get or create shared HTTP client for connection pooling."""
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)
    return _http_client


# === Helper Functions ===

def _is_cache_valid(cache_entry: dict, ttl: int) -> bool:
    """Check if cache entry is still valid"""
    if not cache_entry["data"] or not cache_entry["timestamp"]:
        return False
    age = (datetime.now(timezone.utc) - cache_entry["timestamp"]).total_seconds()
    return age < ttl


def _get_cache_age(cache_entry: dict) -> Optional[float]:
    """Get cache age in seconds"""
    if not cache_entry["timestamp"]:
        return None
    return (datetime.now(timezone.utc) - cache_entry["timestamp"]).total_seconds()


# === Position Data ===

async def get_iss_position() -> Dict[str, Any]:
    """
    Get current ISS position from Where The ISS At API.
    Falls back to Open Notify if primary fails.
    Returns cached data if within TTL.
    """
    cached = _cache["position"]
    
    # Return valid cache
    if _is_cache_valid(cached, POSITION_CACHE_TTL):
        return {
            **cached["data"],
            "cached": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    now = datetime.now(timezone.utc)
    
    client = _get_client()
    
    # Try primary API: Where The ISS At
    try:
        response = await client.get(WHERETHEISS_API)
        response.raise_for_status()
        data = response.json()
        
        result = {
            "latitude": round(data["latitude"], 4),
            "longitude": round(data["longitude"], 4),
            "altitude_km": round(data["altitude"], 1),
            "velocity_kmh": round(data["velocity"], 0),
            "visibility": data["visibility"],
            "footprint_km": round(data["footprint"], 1),
            "timestamp": data["timestamp"],
            "source": "wheretheiss",
            "cached": False,
        }
        
        _cache["position"] = {"data": result, "timestamp": now}
        return result
        
    except Exception as e:
        logger.warning(f"Where The ISS At API failed: {e}")
    
    # Try fallback API: Open Notify
    try:
        response = await client.get(OPEN_NOTIFY_POSITION_API)
        response.raise_for_status()
        data = response.json()
        
        if data.get("message") == "success":
            result = {
                "latitude": round(float(data["iss_position"]["latitude"]), 4),
                "longitude": round(float(data["iss_position"]["longitude"]), 4),
                "altitude_km": None,
                "velocity_kmh": None,
                "visibility": None,
                "footprint_km": None,
                "timestamp": data["timestamp"],
                "source": "open-notify",
                "cached": False,
            }
            
            _cache["position"] = {"data": result, "timestamp": now}
            return result
            
    except Exception as e:
        logger.error(f"Fallback API also failed: {e}")
    
    # Return stale cache if available
    if cached["data"]:
        return {
            **cached["data"],
            "cached": True,
            "stale": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    raise Exception("Unable to fetch ISS position from any source")


# === Crew Data ===

async def get_iss_crew() -> Dict[str, Any]:
    """
    Get current ISS crew roster using two-phase approach:
      Phase 1: Open Notify API → crew names and craft (fast, always available)
      Phase 2: NASA ISS Blog → agency affiliations (scraped, cached 24h)
    
    Phase 2 enrichment is non-blocking: if it fails, crew list
    returns without agency tags and the client handles gracefully.
    """
    cached = _cache["crew"]
    
    # Return valid cache (already enriched)
    if _is_cache_valid(cached, CREW_CACHE_TTL):
        return {
            **cached["data"],
            "cached": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    now = datetime.now(timezone.utc)
    
    client = _get_client()
    
    try:
        response = await client.get(OPEN_NOTIFY_CREW_API)
        response.raise_for_status()
        data = response.json()
        
        if data.get("message") == "success":
            # Phase 1: Filter to ISS crew only
            iss_crew = [
                {"name": person["name"], "craft": person["craft"]}
                for person in data.get("people", [])
                if person.get("craft") == "ISS"
            ]
            
            # Phase 2: Enrich with agency data from NASA blog
            try:
                agency_lookup = await fetch_crew_agencies()
                if agency_lookup:
                    iss_crew = enrich_crew_with_agencies(iss_crew, agency_lookup)
                    logger.info(f"Crew enriched: {sum(1 for c in iss_crew if c.get('agency'))}/{len(iss_crew)} have agency")
            except Exception as e:
                logger.warning(f"Phase 2 enrichment failed (non-fatal): {e}")
            
            result = {
                "count": len(iss_crew),
                "crew": iss_crew,
                "total_in_space": data.get("number", 0),
                "source": "open-notify+nasa-blog",
                "cached": False,
            }
            
            _cache["crew"] = {"data": result, "timestamp": now}
            return result
            
    except Exception as e:
        logger.error(f"Failed to fetch ISS crew: {e}")
    
    # Return stale cache if available
    if cached["data"]:
        return {
            **cached["data"],
            "cached": True,
            "stale": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    raise Exception("Unable to fetch ISS crew data")


# === NASA Telemetry (Placeholder) ===

def get_nasa_telemetry() -> Dict[str, Any]:
    """
    Get NASA ISS telemetry data.
    
    Currently returns a placeholder - NASA Lightstreamer telemetry is
    handled client-side. Future enhancement: implement server-side
    Lightstreamer connection or alternative telemetry source.
    """
    return {
        "cabin_pressure_psia": None,
        "cabin_temp_c": None,
        "o2_level_mmhg": None,
        "co2_level_mmhg": None,
        "solar_arrays": {
            "port_deg": None,
            "starboard_deg": None,
        },
        "attitude": {
            "roll_deg": None,
            "pitch_deg": None,
            "yaw_deg": None,
        },
        "connection_status": "client-side",
        "last_update": None,
        "source": "nasa-lightstreamer",
        "note": "Telemetry currently fetched client-side via Lightstreamer"
    }


# === Combined ISS Data ===

async def get_iss_combined() -> Dict[str, Any]:
    """
    Get all ISS data combined: position and crew.
    Telemetry is noted as client-side.
    """
    # Fetch position and crew in parallel
    position, crew = await asyncio.gather(
        get_iss_position(),
        get_iss_crew(),
        return_exceptions=True
    )
    
    # Handle errors gracefully
    if isinstance(position, Exception):
        position = {"error": str(position)}
    if isinstance(crew, Exception):
        crew = {"error": str(crew)}
    
    return {
        "position": position,
        "crew": crew,
        "telemetry": get_nasa_telemetry(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }



# === Reverse Geocoding ===

GEOCODE_CACHE_TTL = 120  # Location names are cosmetic, 2 min staleness is fine

_geocode_cache = {}

async def get_location_name(lat: float, lng: float) -> Dict[str, Any]:
    """
    Get location name from coordinates using Where The ISS At API.
    """
    # Round coords for caching
    cache_key = f"{round(lat, 1)},{round(lng, 1)}"
    now = datetime.now(timezone.utc)
    
    # Check cache
    if cache_key in _geocode_cache:
        cached = _geocode_cache[cache_key]
        age = (now - cached["timestamp"]).total_seconds()
        if age < GEOCODE_CACHE_TTL:
            return {**cached["data"], "cached": True, "cache_age_seconds": round(age, 1)}
    
    client = _get_client()
    
    try:
        url = f"https://api.wheretheiss.at/v1/coordinates/{lat},{lng}"
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        
        location = "Ocean"
        country = "International Waters"
        
        if data.get("timezone_id"):
            parts = data["timezone_id"].split("/")
            location = parts[-1].replace("_", " ")
            country = data.get("country_code", "")
        
        result = {
            "location": location,
            "country_code": country,
            "timezone_id": data.get("timezone_id"),
            "source": "wheretheiss",
            "cached": False,
        }
        
        _geocode_cache[cache_key] = {"data": result, "timestamp": now}
        return result
        
    except Exception as e:
        logger.warning(f"Geocode lookup failed: {e}")
        return {
            "location": f"{abs(lat):.1f}°{'N' if lat >= 0 else 'S'}",
            "country_code": f"{abs(lng):.1f}°{'E' if lng >= 0 else 'W'}",
            "timezone_id": None,
            "source": "coordinates",
            "cached": False,
        }


# === ISS News (delegates to shared news service) ===

# ISS-relevant feed IDs from news.py
ISS_NEWS_FEED_IDS = {"nasa-iss", "spaceflight-now-iss"}


async def get_iss_news(limit: int = 10) -> Dict[str, Any]:
    """
    Get ISS-specific news. Delegates to the shared news service
    (news.py) which caches all RSS feeds for 15 minutes, avoiding
    duplicate fetches when both /api/news and /api/iss/news are called.
    """
    from news import get_news
    
    # get_news() returns cached results — no extra HTTP calls
    all_news = await get_news(limit=100)  # Get all, then filter
    
    # Filter to ISS-relevant feeds
    iss_items = [
        item for item in all_news.get("news", [])
        if item.get("feed_id") in ISS_NEWS_FEED_IDS
    ][:limit]
    
    return {
        "news": iss_items,
        "count": len(iss_items),
        "timestamp": all_news.get("timestamp"),
        "cached": all_news.get("cached", False),
        "cache_age_seconds": all_news.get("cache_age_seconds"),
    }
