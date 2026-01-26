"""
ArtemisOps ISS Data Service
Server-side proxy for ISS position and crew data.

Data Sources:
- Where The ISS At API: Position, altitude, velocity, visibility
- Open Notify API: Crew roster, position fallback

Note: NASA Lightstreamer telemetry (cabin pressure, temp, O2) is currently
handled client-side due to complexity of Python Lightstreamer integration.
This can be moved server-side in a future update.
"""
import asyncio
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# === Configuration ===

WHERETHEISS_API = "https://api.wheretheiss.at/v1/satellites/25544"
OPEN_NOTIFY_POSITION_API = "http://api.open-notify.org/iss-now.json"
OPEN_NOTIFY_CREW_API = "http://api.open-notify.org/astros.json"

# Cache settings (seconds)
POSITION_CACHE_TTL = 3   # Position updates frequently
CREW_CACHE_TTL = 3600    # Crew changes rarely (1 hour)

# In-memory cache
_cache = {
    "position": {"data": None, "timestamp": None},
    "crew": {"data": None, "timestamp": None},
}


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
    
    async with httpx.AsyncClient(timeout=10.0) as client:
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
    Get current ISS crew roster from Open Notify API.
    Returns cached data if within TTL.
    """
    cached = _cache["crew"]
    
    # Return valid cache
    if _is_cache_valid(cached, CREW_CACHE_TTL):
        return {
            **cached["data"],
            "cached": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    now = datetime.now(timezone.utc)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(OPEN_NOTIFY_CREW_API)
            response.raise_for_status()
            data = response.json()
            
            if data.get("message") == "success":
                # Filter to ISS crew only
                iss_crew = [
                    {"name": person["name"], "craft": person["craft"]}
                    for person in data.get("people", [])
                    if person.get("craft") == "ISS"
                ]
                
                result = {
                    "count": len(iss_crew),
                    "crew": iss_crew,
                    "total_in_space": data.get("number", 0),
                    "source": "open-notify",
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

GEOCODE_CACHE_TTL = 30  # Cache location names for 30 seconds

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
    
    async with httpx.AsyncClient(timeout=10.0) as client:
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


# === ISS News ===

# Spaceflight Now ISS News (most reliable for ISS-specific news)
SPACEFLIGHT_NOW_ISS_RSS = "https://spaceflightnow.com/category/iss/feed/"
# NASA Space Station Blog
NASA_ISS_BLOG_RSS = "https://blogs.nasa.gov/spacestation/feed/"

NEWS_CACHE_TTL = 900  # 15 minutes

_news_cache = {
    "news": {"data": None, "timestamp": None}
}


def _parse_rss_date(date_str: str) -> Optional[datetime]:
    """Parse RSS date formats"""
    if not date_str:
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S GMT",
        "%a, %d %b %Y %H:%M:%S +0000",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except:
            continue
    return None


def _format_time_ago(dt: datetime) -> str:
    """Format datetime as relative time"""
    if not dt:
        return ""
    
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    diff = now - dt
    hours = diff.total_seconds() / 3600
    days = diff.days
    
    if hours < 1:
        return f"{int(diff.total_seconds() / 60)} min ago"
    elif hours < 24:
        return f"{int(hours)}h ago"
    elif days == 1:
        return "Yesterday"
    elif days < 7:
        return f"{days} days ago"
    else:
        return dt.strftime("%b %d")


async def get_iss_news(limit: int = 10) -> Dict[str, Any]:
    """
    Fetch latest ISS news from Spaceflight Now and NASA ISS Blog RSS feeds.
    Returns cached data if within TTL.
    """
    import xml.etree.ElementTree as ET
    
    cached = _news_cache["news"]
    
    # Return valid cache
    if _is_cache_valid(cached, NEWS_CACHE_TTL):
        return {
            **cached["data"],
            "cached": True,
            "cache_age_seconds": round(_get_cache_age(cached), 1)
        }
    
    now = datetime.now(timezone.utc)
    news_items = []
    
    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
        # Try Spaceflight Now ISS feed FIRST (most reliable for ISS-specific news)
        try:
            response = await client.get(SPACEFLIGHT_NOW_ISS_RSS)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            channel = root.find("channel")
            
            if channel:
                for item in channel.findall("item")[:limit]:
                    title = item.find("title")
                    pub_date = item.find("pubDate")
                    link = item.find("link")
                    
                    pub_dt = _parse_rss_date(pub_date.text if pub_date is not None else None)
                    
                    news_items.append({
                        "title": title.text if title is not None else "ISS News",
                        "time": pub_dt.isoformat() if pub_dt else None,
                        "time_ago": _format_time_ago(pub_dt),
                        "link": link.text if link is not None else None,
                        "source": "Spaceflight Now",
                        "summary": None
                    })
                    
            logger.info(f"Fetched {len(news_items)} news items from Spaceflight Now ISS feed")
            
        except Exception as e:
            logger.warning(f"Spaceflight Now ISS feed fetch failed: {e}")
        
        # Try NASA ISS Blog as supplement
        if len(news_items) < limit:
            try:
                response = await client.get(NASA_ISS_BLOG_RSS)
                response.raise_for_status()
                
                root = ET.fromstring(response.text)
                channel = root.find("channel")
                
                if channel:
                    remaining = limit - len(news_items)
                    for item in channel.findall("item")[:remaining]:
                        title = item.find("title")
                        pub_date = item.find("pubDate")
                        link = item.find("link")
                        description = item.find("description")
                        
                        pub_dt = _parse_rss_date(pub_date.text if pub_date is not None else None)
                        
                        news_items.append({
                            "title": title.text if title is not None else "NASA ISS Update",
                            "time": pub_dt.isoformat() if pub_dt else None,
                            "time_ago": _format_time_ago(pub_dt),
                            "link": link.text if link is not None else None,
                            "source": "NASA ISS Blog",
                            "summary": (description.text[:150] + "...") if description is not None and description.text else None
                        })
                        
                logger.info(f"Added NASA ISS Blog items, total: {len(news_items)}")
                
            except Exception as e:
                logger.warning(f"Spaceflight Now fetch failed: {e}")
    
    # Sort by date (newest first)
    news_items.sort(key=lambda x: x["time"] or "", reverse=True)
    
    result = {
        "news": news_items[:limit],
        "count": len(news_items),
        "timestamp": now.isoformat(),
    }
    
    _news_cache["news"] = {"data": result, "timestamp": now}
    
    return {
        **result,
        "cached": False
    }
