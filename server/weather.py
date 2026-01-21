"""
ArtemisOps Weather Service
Fetches weather data for launch/landing sites
Only activates when events are within 7 days
Uses Open-Meteo API (free, no key required)
"""
import httpx
from datetime import datetime, timezone, timedelta
from typing import Optional
import asyncio

# Open-Meteo API endpoint
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

# Known launch site coordinates
LAUNCH_SITES = {
    # NASA sites
    "kennedy space center": {"lat": 28.5729, "lon": -80.6490, "name": "Kennedy Space Center, FL"},
    "ksc": {"lat": 28.5729, "lon": -80.6490, "name": "Kennedy Space Center, FL"},
    "cape canaveral": {"lat": 28.4889, "lon": -80.5778, "name": "Cape Canaveral, FL"},
    "vandenberg": {"lat": 34.7420, "lon": -120.5724, "name": "Vandenberg SFB, CA"},
    
    # ESA sites
    "kourou": {"lat": 5.2360, "lon": -52.7686, "name": "Kourou, French Guiana"},
    "guiana space centre": {"lat": 5.2360, "lon": -52.7686, "name": "Guiana Space Centre"},
    "csg": {"lat": 5.2360, "lon": -52.7686, "name": "Centre Spatial Guyanais"},
    
    # International
    "baikonur": {"lat": 45.9650, "lon": 63.3050, "name": "Baikonur Cosmodrome, Kazakhstan"},
    "tanegashima": {"lat": 30.4009, "lon": 130.9750, "name": "Tanegashima, Japan"},
    "jiuquan": {"lat": 40.9606, "lon": 100.2914, "name": "Jiuquan, China"},
    "wenchang": {"lat": 19.6145, "lon": 110.9510, "name": "Wenchang, China"},
    
    # Splashdown/recovery zones (approximate centers)
    "atlantic ocean": {"lat": 30.0, "lon": -75.0, "name": "Atlantic Recovery Zone"},
    "pacific ocean": {"lat": 25.0, "lon": -120.0, "name": "Pacific Recovery Zone"},
    "gulf of mexico": {"lat": 27.0, "lon": -90.0, "name": "Gulf of Mexico"},
}

# Weather condition codes from Open-Meteo (WMO codes)
WEATHER_CODES = {
    0: {"desc": "Clear sky", "icon": "☀️", "severity": "good"},
    1: {"desc": "Mainly clear", "icon": "🌤️", "severity": "good"},
    2: {"desc": "Partly cloudy", "icon": "⛅", "severity": "good"},
    3: {"desc": "Overcast", "icon": "☁️", "severity": "marginal"},
    45: {"desc": "Fog", "icon": "🌫️", "severity": "marginal"},
    48: {"desc": "Depositing rime fog", "icon": "🌫️", "severity": "bad"},
    51: {"desc": "Light drizzle", "icon": "🌧️", "severity": "marginal"},
    53: {"desc": "Moderate drizzle", "icon": "🌧️", "severity": "bad"},
    55: {"desc": "Dense drizzle", "icon": "🌧️", "severity": "bad"},
    61: {"desc": "Slight rain", "icon": "🌧️", "severity": "marginal"},
    63: {"desc": "Moderate rain", "icon": "🌧️", "severity": "bad"},
    65: {"desc": "Heavy rain", "icon": "🌧️", "severity": "bad"},
    71: {"desc": "Slight snow", "icon": "🌨️", "severity": "bad"},
    73: {"desc": "Moderate snow", "icon": "🌨️", "severity": "bad"},
    75: {"desc": "Heavy snow", "icon": "🌨️", "severity": "bad"},
    77: {"desc": "Snow grains", "icon": "🌨️", "severity": "bad"},
    80: {"desc": "Slight rain showers", "icon": "🌦️", "severity": "marginal"},
    81: {"desc": "Moderate rain showers", "icon": "🌦️", "severity": "bad"},
    82: {"desc": "Violent rain showers", "icon": "⛈️", "severity": "bad"},
    85: {"desc": "Slight snow showers", "icon": "🌨️", "severity": "bad"},
    86: {"desc": "Heavy snow showers", "icon": "🌨️", "severity": "bad"},
    95: {"desc": "Thunderstorm", "icon": "⛈️", "severity": "bad"},
    96: {"desc": "Thunderstorm with hail", "icon": "⛈️", "severity": "bad"},
    99: {"desc": "Thunderstorm with heavy hail", "icon": "⛈️", "severity": "bad"},
}

# Launch weather constraints (simplified)
LAUNCH_CONSTRAINTS = {
    "max_wind_speed_kmh": 48,  # ~30 mph / 26 knots
    "max_wind_gust_kmh": 64,   # ~40 mph / 35 knots
    "max_precipitation_mm": 0.1,
    "bad_weather_codes": [48, 53, 55, 63, 65, 71, 73, 75, 77, 81, 82, 85, 86, 95, 96, 99],
}


def find_site_coordinates(site_name: str) -> Optional[dict]:
    """Find coordinates for a launch site by name (fuzzy match)"""
    if not site_name:
        return None
    
    site_lower = site_name.lower()
    
    # Direct match
    for key, coords in LAUNCH_SITES.items():
        if key in site_lower or site_lower in key:
            return coords
    
    # Partial match on name field
    for key, coords in LAUNCH_SITES.items():
        if coords["name"].lower() in site_lower or site_lower in coords["name"].lower():
            return coords
    
    # Check for state/country codes
    if "fl" in site_lower or "florida" in site_lower:
        return LAUNCH_SITES["kennedy space center"]
    if "ca" in site_lower or "california" in site_lower:
        return LAUNCH_SITES["vandenberg"]
    if "french guiana" in site_lower or "guiana" in site_lower:
        return LAUNCH_SITES["kourou"]
    
    return None


def is_within_forecast_window(event_date: datetime, days: int = 7) -> bool:
    """Check if event is within the forecast window"""
    if not event_date:
        return False
    
    now = datetime.now(timezone.utc)
    
    # Ensure event_date is timezone-aware
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    
    delta = event_date - now
    return timedelta(0) <= delta <= timedelta(days=days)


def is_same_day(event_date: datetime) -> bool:
    """Check if event is on the same calendar day (UTC)"""
    if not event_date:
        return False
    
    now = datetime.now(timezone.utc)
    
    # Ensure event_date is timezone-aware
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    
    return now.date() == event_date.date()


def get_hours_until(event_date: datetime) -> float:
    """Get number of hours until event (can be negative if past)"""
    if not event_date:
        return float('inf')
    
    now = datetime.now(timezone.utc)
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    
    delta = event_date - now
    return delta.total_seconds() / 3600


def get_days_until(event_date: datetime) -> int:
    """Get number of days until event"""
    if not event_date:
        return -1
    
    now = datetime.now(timezone.utc)
    if event_date.tzinfo is None:
        event_date = event_date.replace(tzinfo=timezone.utc)
    
    delta = event_date - now
    return max(0, delta.days)


async def fetch_weather_forecast(lat: float, lon: float, days: int = 7) -> Optional[dict]:
    """Fetch weather forecast from Open-Meteo API"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(
                OPEN_METEO_BASE,
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "hourly": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_gusts_10m,cloud_cover",
                    "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max",
                    "timezone": "UTC",
                    "forecast_days": min(days + 1, 16),  # API max is 16 days
                }
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None


def analyze_launch_weather(forecast: dict, target_date: datetime) -> dict:
    """Analyze weather conditions for launch viability"""
    if not forecast or "daily" not in forecast:
        return {"status": "unknown", "message": "Weather data unavailable"}
    
    daily = forecast["daily"]
    hourly = forecast.get("hourly", {})
    
    # Find the target day index
    target_date_str = target_date.strftime("%Y-%m-%d")
    day_index = -1
    
    for i, date_str in enumerate(daily.get("time", [])):
        if date_str == target_date_str:
            day_index = i
            break
    
    if day_index == -1:
        # Target date not in forecast range
        return {
            "status": "unknown",
            "message": "Launch date outside forecast range",
            "days_until": get_days_until(target_date)
        }
    
    # Extract daily values
    weather_code = daily.get("weather_code", [])[day_index] if day_index < len(daily.get("weather_code", [])) else None
    temp_max = daily.get("temperature_2m_max", [])[day_index] if day_index < len(daily.get("temperature_2m_max", [])) else None
    temp_min = daily.get("temperature_2m_min", [])[day_index] if day_index < len(daily.get("temperature_2m_min", [])) else None
    precip = daily.get("precipitation_sum", [])[day_index] if day_index < len(daily.get("precipitation_sum", [])) else 0
    wind_max = daily.get("wind_speed_10m_max", [])[day_index] if day_index < len(daily.get("wind_speed_10m_max", [])) else 0
    gust_max = daily.get("wind_gusts_10m_max", [])[day_index] if day_index < len(daily.get("wind_gusts_10m_max", [])) else 0
    
    # Determine launch viability
    issues = []
    
    if weather_code in LAUNCH_CONSTRAINTS["bad_weather_codes"]:
        weather_info = WEATHER_CODES.get(weather_code, {"desc": "Unknown", "severity": "unknown"})
        issues.append(f"Weather: {weather_info['desc']}")
    
    if wind_max and wind_max > LAUNCH_CONSTRAINTS["max_wind_speed_kmh"]:
        issues.append(f"High winds: {wind_max:.0f} km/h")
    
    if gust_max and gust_max > LAUNCH_CONSTRAINTS["max_wind_gust_kmh"]:
        issues.append(f"Strong gusts: {gust_max:.0f} km/h")
    
    if precip and precip > LAUNCH_CONSTRAINTS["max_precipitation_mm"]:
        issues.append(f"Precipitation: {precip:.1f} mm")
    
    # Determine overall status
    if len(issues) == 0:
        status = "go"
        message = "Weather conditions favorable for launch"
    elif len(issues) <= 1 and weather_code not in [95, 96, 99]:  # Not thunderstorm
        status = "marginal"
        message = "Weather conditions marginal: " + ", ".join(issues)
    else:
        status = "no-go"
        message = "Weather conditions unfavorable: " + ", ".join(issues)
    
    weather_info = WEATHER_CODES.get(weather_code, {"desc": "Unknown", "icon": "❓", "severity": "unknown"})
    
    return {
        "status": status,
        "message": message,
        "date": target_date_str,
        "days_until": get_days_until(target_date),
        "conditions": {
            "code": weather_code,
            "description": weather_info["desc"],
            "icon": weather_info["icon"],
            "temperature_high_c": temp_max,
            "temperature_low_c": temp_min,
            "temperature_high_f": round(temp_max * 9/5 + 32, 1) if temp_max else None,
            "temperature_low_f": round(temp_min * 9/5 + 32, 1) if temp_min else None,
            "precipitation_mm": precip,
            "wind_speed_kmh": wind_max,
            "wind_speed_mph": round(wind_max * 0.621371, 1) if wind_max else None,
            "wind_gust_kmh": gust_max,
            "wind_gust_mph": round(gust_max * 0.621371, 1) if gust_max else None,
        },
        "issues": issues,
    }


def get_forecast_summary(forecast: dict, days: int = 5) -> list:
    """Get a multi-day forecast summary"""
    if not forecast or "daily" not in forecast:
        return []
    
    daily = forecast["daily"]
    summary = []
    
    times = daily.get("time", [])[:days]
    codes = daily.get("weather_code", [])[:days]
    temp_maxs = daily.get("temperature_2m_max", [])[:days]
    temp_mins = daily.get("temperature_2m_min", [])[:days]
    precips = daily.get("precipitation_sum", [])[:days]
    winds = daily.get("wind_speed_10m_max", [])[:days]
    
    for i, date_str in enumerate(times):
        code = codes[i] if i < len(codes) else None
        weather_info = WEATHER_CODES.get(code, {"desc": "Unknown", "icon": "❓", "severity": "unknown"})
        
        summary.append({
            "date": date_str,
            "day_name": datetime.strptime(date_str, "%Y-%m-%d").strftime("%a"),
            "icon": weather_info["icon"],
            "description": weather_info["desc"],
            "severity": weather_info["severity"],
            "temp_high_c": temp_maxs[i] if i < len(temp_maxs) else None,
            "temp_low_c": temp_mins[i] if i < len(temp_mins) else None,
            "temp_high_f": round(temp_maxs[i] * 9/5 + 32) if i < len(temp_maxs) and temp_maxs[i] else None,
            "temp_low_f": round(temp_mins[i] * 9/5 + 32) if i < len(temp_mins) and temp_mins[i] else None,
            "precipitation_mm": precips[i] if i < len(precips) else 0,
            "wind_kmh": winds[i] if i < len(winds) else 0,
        })
    
    return summary


async def get_mission_weather(
    launch_date: Optional[datetime],
    launch_site: Optional[str],
    landing_date: Optional[datetime] = None,
    landing_site: Optional[str] = None,
) -> dict:
    """
    Get weather data for a mission - only fetches if events are within 7 days.
    
    Returns weather for launch site, and optionally landing site if different.
    """
    result = {
        "launch": None,
        "landing": None,
        "should_fetch": False,
        "reason": None,
    }
    
    # Check if launch is within forecast window
    launch_in_window = is_within_forecast_window(launch_date, days=7) if launch_date else False
    landing_in_window = is_within_forecast_window(landing_date, days=7) if landing_date else False
    
    if not launch_in_window and not landing_in_window:
        days_until = get_days_until(launch_date) if launch_date else -1
        if days_until > 7:
            result["reason"] = f"Launch is {days_until} days away - weather forecast not yet available"
        elif days_until < 0:
            result["reason"] = "Launch date has passed"
        else:
            result["reason"] = "No upcoming events within forecast window"
        return result
    
    result["should_fetch"] = True
    
    # Fetch launch site weather
    if launch_in_window and launch_site:
        coords = find_site_coordinates(launch_site)
        if coords:
            print(f"Fetching weather for {coords['name']} (launch)")
            forecast = await fetch_weather_forecast(coords["lat"], coords["lon"])
            if forecast:
                result["launch"] = {
                    "site": coords["name"],
                    "coordinates": {"lat": coords["lat"], "lon": coords["lon"]},
                    "analysis": analyze_launch_weather(forecast, launch_date),
                    "forecast": get_forecast_summary(forecast, days=5),
                }
        else:
            result["launch"] = {
                "site": launch_site,
                "error": "Unknown launch site coordinates"
            }
    
    # Fetch landing site weather (if different and within window)
    if landing_in_window and landing_site:
        landing_coords = find_site_coordinates(landing_site)
        # Only fetch if different from launch site
        if landing_coords:
            launch_coords = find_site_coordinates(launch_site) if launch_site else None
            if not launch_coords or (landing_coords["lat"] != launch_coords["lat"]):
                print(f"Fetching weather for {landing_coords['name']} (landing)")
                forecast = await fetch_weather_forecast(landing_coords["lat"], landing_coords["lon"])
                if forecast:
                    result["landing"] = {
                        "site": landing_coords["name"],
                        "coordinates": {"lat": landing_coords["lat"], "lon": landing_coords["lon"]},
                        "analysis": analyze_launch_weather(forecast, landing_date),
                        "forecast": get_forecast_summary(forecast, days=5),
                    }
    
    return result


# Convenience function for testing
async def test_weather():
    """Test weather fetching"""
    # Simulate a launch 3 days from now
    test_date = datetime.now(timezone.utc) + timedelta(days=3)
    result = await get_mission_weather(
        launch_date=test_date,
        launch_site="Kennedy Space Center, FL"
    )
    print(f"Weather result: {result}")
    return result


if __name__ == "__main__":
    asyncio.run(test_weather())
