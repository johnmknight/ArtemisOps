"""
ArtemisOps Trajectory Data Service
Provides waypoint and path data for mission trajectory visualizations.

Each mission type has a defined set of waypoints with:
- Position (x, y) in SVG viewBox coordinates (900x500)
- Phase classification for color-coding
- Timing data (MET or T-minus) when available
- Descriptive metadata

Trajectory data is served from the API so clients don't need hardcoded
mission profiles. New missions can be added here without client updates.
"""
from typing import Dict, Any, Optional, List
from datetime import timedelta

# === Artemis II: Lunar Free Return ===

ARTEMIS_II_TRAJECTORY = {
    "mission_type": "lunar-flyby",
    "profile": "Free Return Trajectory",
    "duration_days": 10,
    "max_distance_km": 380000,
    "closest_approach_km": 7400,
    "viewBox": "0 0 900 500",
    "bodies": [
        {"name": "Earth", "x": 140, "y": 280, "radius": 45},
        {"name": "Moon", "x": 800, "y": 280, "radius": 20},
    ],
    "waypoints": [
        {
            "id": 1, "name": "Launch",
            "phase": "launch", "x": 140, "y": 250,
            "met": "T-0:00:00",
            "description": "Liftoff from KSC Pad 39B aboard SLS Block 1",
            "altitude_km": 0,
        },
        {
            "id": 2, "name": "Booster Sep",
            "phase": "launch", "x": 155, "y": 235,
            "met": "0:00:02:12",
            "description": "SRB separation at ~45 km altitude",
            "altitude_km": 45,
        },
        {
            "id": 3, "name": "Fairing Sep",
            "phase": "launch", "x": 165, "y": 225,
            "met": "0:00:03:30",
            "description": "Launch Abort System and fairing jettison",
            "altitude_km": 80,
        },
        {
            "id": 4, "name": "MECO",
            "phase": "launch", "x": 180, "y": 215,
            "met": "0:00:08:30",
            "description": "Core stage main engine cutoff, ICPS separation",
            "altitude_km": 185,
        },
        {
            "id": 5, "name": "Orbit Insertion",
            "phase": "orbit", "x": 195, "y": 205,
            "met": "0:00:20:00",
            "description": "ICPS burn for parking orbit (~185 km circular)",
            "altitude_km": 185,
        },
        {
            "id": 6, "name": "Systems Check",
            "phase": "orbit", "x": 210, "y": 198,
            "met": "0:01:30:00",
            "description": "Orion systems checkout in Earth parking orbit",
            "altitude_km": 185,
        },
        {
            "id": 7, "name": "TLI Burn",
            "phase": "tli", "x": 260, "y": 190,
            "met": "0:02:00:00",
            "description": "Trans-Lunar Injection — ICPS burn to escape velocity",
            "altitude_km": 185,
            "delta_v_ms": 3100,
        },
        {
            "id": 8, "name": "Outbound Coast",
            "phase": "outbound", "x": 420, "y": 75,
            "met": "2:00:00:00",
            "description": "Outbound transit coasting toward the Moon",
            "altitude_km": 200000,
        },
        {
            "id": 9, "name": "Mid-Course Correction",
            "phase": "outbound", "x": 580, "y": 85,
            "met": "3:00:00:00",
            "description": "Trajectory correction maneuver",
            "altitude_km": 300000,
        },
        {
            "id": 10, "name": "Lunar Approach",
            "phase": "approach", "x": 720, "y": 160,
            "met": "4:00:00:00",
            "description": "Final approach to the Moon",
            "altitude_km": 50000,
        },
        {
            "id": 11, "name": "Lunar Flyby",
            "phase": "flyby", "x": 800, "y": 290,
            "met": "4:12:00:00",
            "description": "Closest approach — ~7,400 km from lunar surface",
            "altitude_km": 7400,
        },
        {
            "id": 12, "name": "Trans-Earth Injection",
            "phase": "return", "x": 720, "y": 340,
            "met": "5:00:00:00",
            "description": "Free return trajectory curves back toward Earth",
            "altitude_km": 50000,
        },
        {
            "id": 13, "name": "Return Coast",
            "phase": "return", "x": 500, "y": 430,
            "met": "7:00:00:00",
            "description": "Return transit coasting toward Earth",
            "altitude_km": 200000,
        },
        {
            "id": 14, "name": "Earth Approach",
            "phase": "entry", "x": 320, "y": 420,
            "met": "9:00:00:00",
            "description": "Final approach and entry interface",
            "altitude_km": 50000,
        },
        {
            "id": 15, "name": "Splashdown",
            "phase": "splashdown", "x": 225, "y": 335,
            "met": "10:00:00:00",
            "description": "Pacific Ocean splashdown and crew recovery",
            "altitude_km": 0,
        },
    ],
    "phases": [
        {"id": "launch", "name": "Launch & Ascent", "color": "#ff6b35"},
        {"id": "orbit", "name": "Earth Orbit", "color": "#4a9eff"},
        {"id": "tli", "name": "Trans-Lunar Injection", "color": "#00d4ff"},
        {"id": "outbound", "name": "Outbound Transit", "color": "#22c55e"},
        {"id": "approach", "name": "Lunar Approach", "color": "#a78bfa"},
        {"id": "flyby", "name": "Lunar Flyby", "color": "#f59e0b"},
        {"id": "return", "name": "Return Transit", "color": "#22c55e"},
        {"id": "entry", "name": "Entry & Descent", "color": "#ef4444"},
        {"id": "splashdown", "name": "Splashdown", "color": "#00d4ff"},
    ],
    "path_segments": [
        {
            "phase": "outbound",
            "type": "cubic-bezier",
            "points": "M 195,205 C 260,60 600,30 800,280",
            "description": "Earth to Moon outbound arc",
        },
        {
            "phase": "return",
            "type": "cubic-bezier",
            "points": "M 800,280 C 600,500 300,480 195,320",
            "description": "Moon to Earth return arc",
        },
    ],
}


# === Artemis III: Lunar Landing via NRHO ===

ARTEMIS_III_TRAJECTORY = {
    "mission_type": "lunar-landing",
    "profile": "NRHO + HLS Lunar Landing",
    "duration_days": 30,
    "max_distance_km": 380000,
    "landing_site": "South Pole (Shackleton Crater region)",
    "surface_stay_days": 6.5,
    "viewBox": "0 0 900 500",
    "bodies": [
        {"name": "Earth", "x": 100, "y": 400, "radius": 40},
        {"name": "Moon", "x": 780, "y": 280, "radius": 25},
    ],
    "waypoints": [
        {
            "id": 1, "name": "Launch",
            "phase": "launch", "x": 100, "y": 400,
            "met": "T-0:00:00",
            "description": "Liftoff from KSC Pad 39B aboard SLS Block 1 Crew",
        },
        {
            "id": 2, "name": "TLI",
            "phase": "tli", "x": 180, "y": 320,
            "met": "0:02:00:00",
            "description": "Trans-Lunar Injection burn",
        },
        {
            "id": 3, "name": "Outbound Transit",
            "phase": "outbound", "x": 350, "y": 200,
            "met": "2:00:00:00",
            "description": "Multi-day coast to the Moon",
        },
        {
            "id": 4, "name": "NRHO Insertion",
            "phase": "nrho-insert", "x": 550, "y": 100,
            "met": "5:00:00:00",
            "description": "Powered flyby insertion into Near-Rectilinear Halo Orbit",
        },
        {
            "id": 5, "name": "Gateway Rendezvous",
            "phase": "gateway", "x": 650, "y": 80,
            "met": "6:00:00:00",
            "description": "Rendezvous and dock with Lunar Gateway (future missions)",
        },
        {
            "id": 6, "name": "HLS Transfer",
            "phase": "hls-transfer", "x": 720, "y": 120,
            "met": "7:00:00:00",
            "description": "Crew transfers to HLS (Starship) for descent",
        },
        {
            "id": 7, "name": "Descent Orbit",
            "phase": "descent", "x": 750, "y": 200,
            "met": "8:00:00:00",
            "description": "HLS deorbit burn from NRHO to descent trajectory",
        },
        {
            "id": 8, "name": "Lunar Landing",
            "phase": "landing", "x": 780, "y": 290,
            "met": "8:06:00:00",
            "description": "Powered descent and landing at South Pole",
        },
        {
            "id": 9, "name": "Surface Ops",
            "phase": "surface", "x": 780, "y": 310,
            "met": "9:00:00:00",
            "description": "~6.5 days of surface EVAs and science operations",
        },
        {
            "id": 10, "name": "Ascent",
            "phase": "ascent", "x": 750, "y": 250,
            "met": "15:00:00:00",
            "description": "HLS ascent from lunar surface to NRHO",
        },
        {
            "id": 11, "name": "Orion Rendezvous",
            "phase": "rendezvous", "x": 680, "y": 150,
            "met": "16:00:00:00",
            "description": "Dock with Orion in NRHO, crew transfer",
        },
        {
            "id": 12, "name": "TEI",
            "phase": "tei", "x": 580, "y": 180,
            "met": "24:00:00:00",
            "description": "Trans-Earth Injection burn to leave NRHO",
        },
        {
            "id": 13, "name": "Return Transit",
            "phase": "return", "x": 380, "y": 350,
            "met": "27:00:00:00",
            "description": "Multi-day coast back to Earth",
        },
        {
            "id": 14, "name": "Entry",
            "phase": "entry", "x": 200, "y": 420,
            "met": "30:00:00:00",
            "description": "Atmospheric entry at ~40,000 km/h",
        },
        {
            "id": 15, "name": "Splashdown",
            "phase": "splashdown", "x": 120, "y": 450,
            "met": "30:00:30:00",
            "description": "Pacific Ocean splashdown and recovery",
        },
    ],
    "phases": [
        {"id": "launch", "name": "Launch & Ascent", "color": "#ff6b35"},
        {"id": "tli", "name": "Trans-Lunar Injection", "color": "#00d4ff"},
        {"id": "outbound", "name": "Outbound Transit", "color": "#22c55e"},
        {"id": "nrho-insert", "name": "NRHO Insertion", "color": "#a78bfa"},
        {"id": "gateway", "name": "Gateway Ops", "color": "#4a9eff"},
        {"id": "hls-transfer", "name": "HLS Transfer", "color": "#f59e0b"},
        {"id": "descent", "name": "Powered Descent", "color": "#ef4444"},
        {"id": "landing", "name": "Lunar Landing", "color": "#ff6b35"},
        {"id": "surface", "name": "Surface Operations", "color": "#f59e0b"},
        {"id": "ascent", "name": "Ascent", "color": "#00ffcc"},
        {"id": "rendezvous", "name": "Rendezvous & Docking", "color": "#4a9eff"},
        {"id": "tei", "name": "Trans-Earth Injection", "color": "#a78bfa"},
        {"id": "return", "name": "Return Transit", "color": "#22c55e"},
        {"id": "entry", "name": "Entry & Descent", "color": "#ef4444"},
        {"id": "splashdown", "name": "Splashdown", "color": "#00d4ff"},
    ],
    "path_segments": [
        {
            "phase": "outbound",
            "type": "cubic-bezier",
            "points": "M 100,400 C 200,200 400,80 550,100",
            "description": "Earth to NRHO insertion",
        },
        {
            "phase": "nrho",
            "type": "ellipse",
            "cx": 720, "cy": 200, "rx": 120, "ry": 180,
            "description": "Near-Rectilinear Halo Orbit around Moon",
        },
        {
            "phase": "descent",
            "type": "line",
            "points": "M 720,120 L 780,290",
            "description": "HLS descent to surface",
        },
        {
            "phase": "ascent",
            "type": "line",
            "points": "M 780,310 L 750,250",
            "description": "HLS ascent from surface",
        },
        {
            "phase": "return",
            "type": "cubic-bezier",
            "points": "M 580,180 C 400,250 250,400 120,450",
            "description": "NRHO to Earth return",
        },
    ],
}


# === ISS: Low Earth Orbit ===

ISS_TRAJECTORY = {
    "mission_type": "earth-orbit",
    "profile": "Low Earth Orbit (LEO)",
    "orbital_period_minutes": 92,
    "altitude_km": 420,
    "inclination_deg": 51.6,
    "velocity_kmh": 27600,
    "viewBox": "0 0 900 500",
    "bodies": [
        {"name": "Earth", "x": 450, "y": 250, "radius": 150},
    ],
    "waypoints": [],
    "phases": [
        {"id": "orbit", "name": "Orbital Operations", "color": "#4a9eff"},
    ],
    "orbital_params": {
        "apogee_km": 422,
        "perigee_km": 418,
        "eccentricity": 0.0003,
        "period_minutes": 92.68,
        "revolutions_per_day": 15.54,
        "inclination_deg": 51.64,
    },
    "path_segments": [
        {
            "phase": "orbit",
            "type": "ellipse",
            "cx": 450, "cy": 250, "rx": 200, "ry": 200,
            "description": "Approximately circular LEO orbit",
        },
    ],
}


# === Registry ===

# Map mission IDs and types to trajectory data
_TRAJECTORY_REGISTRY: Dict[str, dict] = {
    # By mission ID
    "artemis-ii": ARTEMIS_II_TRAJECTORY,
    "artemis-iii": ARTEMIS_III_TRAJECTORY,
    "iss": ISS_TRAJECTORY,
}

# Mission type fallbacks (for missions not explicitly registered)
_TYPE_FALLBACKS: Dict[str, str] = {
    "artemis-i": "artemis-ii",       # Similar free-return profile
    "artemis-iv": "artemis-iii",     # Similar NRHO + landing profile
    "artemis-v": "artemis-iii",
    "crew-dragon": "iss",
    "starliner": "iss",
    "iss-expedition": "iss",
    "lunar-gateway": "artemis-iii",  # NRHO-based
}


def get_trajectory(mission_id: str) -> Optional[Dict[str, Any]]:
    """
    Get trajectory data for a mission.

    Looks up by mission ID first, then falls back to mission type mapping.
    Returns None if no trajectory is available.
    """
    # Direct match
    if mission_id in _TRAJECTORY_REGISTRY:
        return _TRAJECTORY_REGISTRY[mission_id]

    # Fallback by type
    fallback_id = _TYPE_FALLBACKS.get(mission_id)
    if fallback_id and fallback_id in _TRAJECTORY_REGISTRY:
        return _TRAJECTORY_REGISTRY[fallback_id]

    return None


def get_available_trajectories() -> List[Dict[str, str]]:
    """List all mission IDs that have trajectory data available."""
    results = []
    seen = set()

    for mission_id, data in _TRAJECTORY_REGISTRY.items():
        results.append({
            "mission_id": mission_id,
            "profile": data["profile"],
            "mission_type": data["mission_type"],
        })
        seen.add(mission_id)

    for alias, target in _TYPE_FALLBACKS.items():
        if alias not in seen and target in _TRAJECTORY_REGISTRY:
            results.append({
                "mission_id": alias,
                "profile": _TRAJECTORY_REGISTRY[target]["profile"],
                "mission_type": _TRAJECTORY_REGISTRY[target]["mission_type"],
                "alias_of": target,
            })

    return results
