"""
ArtemisOps Database Layer
SQLite database for missions, crew, milestones with async support
"""
import aiosqlite
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional
import json

DB_PATH = Path(__file__).parent / "artemisops.db"

# Mission statuses that indicate a completed/returned mission
COMPLETED_STATUSES = [
    "success",      # Launch was successful and mission completed
    "failure",      # Mission failed
    "partial failure",
]

# Statuses that indicate mission is still active/upcoming
ACTIVE_STATUSES = [
    "go",           # Go for launch
    "tbd",          # To be determined
    "tbc",          # To be confirmed  
    "hold",         # On hold
    "in flight",    # Currently in space
]


def is_mission_active(mission: dict) -> bool:
    """
    Determine if a mission should be shown in the active list.
    
    A mission is active if:
    1. Launch date is in the future (hasn't launched yet), OR
    2. Status indicates it's still in progress (not success/failure)
    
    For crewed missions, we also consider if they might still be in space
    (within ~6 months of launch for typical ISS missions).
    """
    status = (mission.get("status") or "").lower()
    launch_date_str = mission.get("launch_date")
    
    # If status clearly indicates completion, it's not active
    if status in COMPLETED_STATUSES:
        # However, for very recent completions (within 7 days), still show them
        # so users can see mission results
        if launch_date_str:
            try:
                launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                days_since_launch = (now - launch_date).days
                
                # Show completed missions for up to 7 days after launch
                if days_since_launch <= 7:
                    return True
            except:
                pass
        return False
    
    # If launch date is in the future, definitely active
    if launch_date_str:
        try:
            launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            
            if launch_date > now:
                return True
            
            # For past launches without a "success" status, check if they might still be in space
            # Most crewed missions are under 6 months, ISS expeditions up to 6 months
            days_since_launch = (now - launch_date).days
            
            if days_since_launch <= 200:  # ~6.5 months max mission duration
                # If status isn't explicitly "success", assume still active
                return True
                
        except:
            pass
    
    # Default: if status is in active list, show it
    return status in ACTIVE_STATUSES or status == ""


async def init_db():
    """Initialize database schema"""
    async with aiosqlite.connect(DB_PATH) as db:
        # Missions table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                launch_date TEXT,
                landing_date TEXT,
                status TEXT,
                status_description TEXT,
                site TEXT,
                rocket TEXT,
                spacecraft TEXT,
                mission_type TEXT,
                description TEXT,
                image_url TEXT,
                api_id TEXT,
                api_source TEXT,
                agencies TEXT,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add columns if they don't exist (migrations)
        migrations = [
            "ALTER TABLE missions ADD COLUMN agencies TEXT",
            "ALTER TABLE missions ADD COLUMN landing_date TEXT",
            "ALTER TABLE missions ADD COLUMN patch_url TEXT",
            "ALTER TABLE missions ADD COLUMN agency_logo_url TEXT",
        ]
        for migration in migrations:
            try:
                await db.execute(migration)
            except:
                pass  # Column already exists
        
        # Crew table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS crew (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT,
                agency TEXT,
                photo_url TEXT,
                bio TEXT,
                bio_url TEXT,
                api_id TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mission_id) REFERENCES missions(id)
            )
        """)
        
        # Milestones table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                date_label TEXT,
                target_date TEXT,
                status TEXT DEFAULT 'pending',
                completed_at TEXT,
                sort_order INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (mission_id) REFERENCES missions(id)
            )
        """)
        
        # Data sync log
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                status TEXT NOT NULL,
                missions_updated INTEGER DEFAULT 0,
                error_message TEXT,
                synced_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await db.commit()
        print(f"Database initialized at {DB_PATH}")


# === Mission Operations ===

async def get_all_missions(active_only: bool = True, include_completed_recent: bool = True) -> list[dict]:
    """
    Get all missions, optionally filtering to only active ones.
    
    Args:
        active_only: If True, filter to missions that haven't completed yet
        include_completed_recent: If True, include recently completed missions (within 7 days)
    
    A mission is considered "active" if:
    - It hasn't launched yet, OR
    - It has launched but crew hasn't returned (still in space), OR
    - It completed within the last 7 days (so users can see results)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Get all missions first, then filter in Python
        # (More complex date logic is easier in Python than SQL)
        query = "SELECT * FROM missions WHERE is_active = 1 ORDER BY launch_date ASC"
        
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            all_missions = [dict(row) for row in rows]
        
        if not active_only:
            return all_missions
        
        # Filter to only active missions
        active_missions = [m for m in all_missions if is_mission_active(m)]
        
        # Sort: upcoming missions first (by launch date), then in-progress
        def sort_key(m):
            launch_date_str = m.get("launch_date")
            if launch_date_str:
                try:
                    launch_date = datetime.fromisoformat(launch_date_str.replace("Z", "+00:00"))
                    now = datetime.now(timezone.utc)
                    
                    # Upcoming missions: sort by launch date ascending
                    if launch_date > now:
                        return (0, launch_date)
                    # Past/in-progress: sort by launch date descending (most recent first)
                    else:
                        return (1, datetime.max.replace(tzinfo=timezone.utc) - launch_date)
                except:
                    pass
            # No date: put at end
            return (2, datetime.max.replace(tzinfo=timezone.utc))
        
        active_missions.sort(key=sort_key)
        
        return active_missions


async def get_mission(mission_id: str) -> Optional[dict]:
    """Get a single mission by ID or slug"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM missions WHERE id = ? OR slug = ?",
            (mission_id, mission_id)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def upsert_mission(mission: dict) -> str:
    """Insert or update a mission"""
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.now(timezone.utc).isoformat()
        
        # Check if exists
        async with db.execute(
            "SELECT id FROM missions WHERE id = ?", (mission['id'],)
        ) as cursor:
            exists = await cursor.fetchone()
        
        if exists:
            await db.execute("""
                UPDATE missions SET
                    name = ?, slug = ?, launch_date = ?, landing_date = ?, status = ?,
                    status_description = ?, site = ?, rocket = ?, spacecraft = ?,
                    mission_type = ?, description = ?, image_url = ?, patch_url = ?,
                    agency_logo_url = ?, api_id = ?, api_source = ?, agencies = ?, 
                    is_active = ?, updated_at = ?
                WHERE id = ?
            """, (
                mission.get('name'), mission.get('slug'), mission.get('launch_date'),
                mission.get('landing_date'), mission.get('status'), 
                mission.get('status_description'),
                mission.get('site'), mission.get('rocket'), mission.get('spacecraft'),
                mission.get('mission_type'), mission.get('description'),
                mission.get('image_url'), mission.get('patch_url'),
                mission.get('agency_logo_url'), mission.get('api_id'), 
                mission.get('api_source'), mission.get('agencies'), 
                mission.get('is_active', 1), now, mission['id']
            ))
        else:
            await db.execute("""
                INSERT INTO missions (
                    id, name, slug, launch_date, landing_date, status, status_description,
                    site, rocket, spacecraft, mission_type, description,
                    image_url, patch_url, agency_logo_url, api_id, api_source, agencies, 
                    is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mission['id'], mission.get('name'), mission.get('slug'),
                mission.get('launch_date'), mission.get('landing_date'),
                mission.get('status'), mission.get('status_description'), 
                mission.get('site'), mission.get('rocket'), mission.get('spacecraft'),
                mission.get('mission_type'), mission.get('description'),
                mission.get('image_url'), mission.get('patch_url'),
                mission.get('agency_logo_url'), mission.get('api_id'),
                mission.get('api_source'), mission.get('agencies'),
                mission.get('is_active', 1), now, now
            ))
        
        await db.commit()
        return mission['id']


async def mark_mission_completed(mission_id: str, landing_date: str = None):
    """Mark a mission as completed (returned from space)"""
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.now(timezone.utc).isoformat()
        landing = landing_date or now
        
        await db.execute("""
            UPDATE missions SET
                status = 'Success',
                landing_date = ?,
                updated_at = ?
            WHERE id = ?
        """, (landing, now, mission_id))
        
        await db.commit()


# === Crew Operations ===

async def get_crew(mission_id: str) -> list[dict]:
    """Get crew for a mission"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM crew WHERE mission_id = ? ORDER BY sort_order ASC",
            (mission_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def upsert_crew(mission_id: str, crew_list: list[dict]):
    """Replace all crew for a mission"""
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.now(timezone.utc).isoformat()
        
        # Delete existing crew
        await db.execute("DELETE FROM crew WHERE mission_id = ?", (mission_id,))
        
        # Insert new crew
        for i, member in enumerate(crew_list):
            await db.execute("""
                INSERT INTO crew (
                    mission_id, name, role, agency, photo_url, bio, bio_url,
                    api_id, sort_order, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mission_id, member.get('name'), member.get('role'),
                member.get('agency'), member.get('photo_url') or member.get('photo'),
                member.get('bio'), member.get('bio_url') or member.get('nasa_bio'),
                member.get('api_id'), i, now, now
            ))
        
        await db.commit()


# === Milestone Operations ===

async def get_milestones(mission_id: str) -> list[dict]:
    """Get milestones for a mission"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM milestones WHERE mission_id = ? ORDER BY sort_order ASC",
            (mission_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def upsert_milestones(mission_id: str, milestones: list[dict]):
    """Replace all milestones for a mission"""
    async with aiosqlite.connect(DB_PATH) as db:
        now = datetime.now(timezone.utc).isoformat()
        
        # Delete existing milestones
        await db.execute("DELETE FROM milestones WHERE mission_id = ?", (mission_id,))
        
        # Insert new milestones
        for i, ms in enumerate(milestones):
            await db.execute("""
                INSERT INTO milestones (
                    mission_id, title, description, date_label, target_date,
                    status, completed_at, sort_order, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mission_id, ms.get('title'), ms.get('description'),
                ms.get('date_label') or ms.get('date'), ms.get('target_date'),
                ms.get('status', 'pending'), ms.get('completed_at'),
                i, now, now
            ))
        
        await db.commit()


# === Sync Log ===

async def log_sync(source: str, status: str, missions_updated: int = 0, error: str = None):
    """Log a sync operation"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO sync_log (source, status, missions_updated, error_message)
            VALUES (?, ?, ?, ?)
        """, (source, status, missions_updated, error))
        await db.commit()


async def get_last_sync() -> Optional[dict]:
    """Get most recent successful sync"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM sync_log WHERE status = 'success' ORDER BY synced_at DESC LIMIT 1"
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


# === Milestone Status Calculation ===

def parse_milestone_date(date_label: str, launch_date: datetime = None) -> Optional[datetime]:
    """
    Parse a milestone date_label into a datetime object.
    
    Supported formats:
    - "Dec 2025" -> last day of that month at 23:59:59
    - "Jan 2, 2026" -> that date at end of day
    - "T-6:40:00" -> launch_date minus 6h40m (requires launch_date)
    - "T-00:00" or "T-0:00" -> launch_date
    """
    import re
    
    if not date_label:
        return None
    
    date_label = date_label.strip()
    
    # Handle T-minus format (e.g., "T-6:40:00", "T-00:00")
    t_minus_match = re.match(r'^T-?(\d+):(\d+):?(\d+)?$', date_label)
    if t_minus_match:
        if not launch_date:
            return None
        hours = int(t_minus_match.group(1))
        minutes = int(t_minus_match.group(2))
        seconds = int(t_minus_match.group(3) or 0)
        return launch_date - timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    # Handle "Month Year" format (e.g., "Dec 2025")
    month_year_match = re.match(r'^([A-Za-z]+)\s+(\d{4})$', date_label)
    if month_year_match:
        try:
            month_name = month_year_match.group(1)
            year = int(month_year_match.group(2))
            # Parse month name
            parsed = datetime.strptime(f"{month_name} 1, {year}", "%b %d, %Y")
            # Get last day of that month
            if parsed.month == 12:
                last_day = datetime(year + 1, 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
            else:
                last_day = datetime(year, parsed.month + 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
            return last_day
        except:
            pass
    
    # Handle "Month Day, Year" format (e.g., "Jan 2, 2026")
    full_date_match = re.match(r'^([A-Za-z]+)\s+(\d+),?\s+(\d{4})$', date_label)
    if full_date_match:
        try:
            month_name = full_date_match.group(1)
            day = int(full_date_match.group(2))
            year = int(full_date_match.group(3))
            # End of that day
            return datetime(year, datetime.strptime(month_name, "%b").month, day, 23, 59, 59, tzinfo=timezone.utc)
        except:
            pass
    
    return None


def calculate_milestone_statuses(milestones: list[dict], launch_date: datetime = None) -> list[dict]:
    """
    Calculate dynamic status for milestones based on current date.
    
    Rules:
    - If milestone's target date has passed -> "completed"
    - First non-completed milestone -> "active" 
    - Everything after -> "pending"
    """
    now = datetime.now(timezone.utc)
    
    # First pass: determine which milestones are past their date
    for ms in milestones:
        target_dt = parse_milestone_date(ms.get('date_label'), launch_date)
        ms['_target_datetime'] = target_dt
        ms['_is_past'] = target_dt is not None and target_dt < now
    
    # Second pass: assign statuses
    found_active = False
    for ms in milestones:
        if ms['_is_past']:
            ms['status'] = 'completed'
        elif not found_active:
            ms['status'] = 'active'
            found_active = True
        else:
            ms['status'] = 'pending'
        
        # Clean up internal fields
        del ms['_target_datetime']
        del ms['_is_past']
    
    return milestones


# === Full Mission Data (with crew and milestones) ===

async def get_full_mission(mission_id: str) -> Optional[dict]:
    """Get mission with crew and milestones, with dynamic milestone status calculation"""
    mission = await get_mission(mission_id)
    if not mission:
        return None
    
    mission['crew'] = await get_crew(mission['id'])
    milestones = await get_milestones(mission['id'])
    
    # Parse launch date for T-minus calculations
    launch_date = None
    if mission.get('launch_date'):
        try:
            launch_date = datetime.fromisoformat(mission['launch_date'].replace('Z', '+00:00'))
        except:
            pass
    
    # Calculate dynamic milestone statuses
    mission['milestones'] = calculate_milestone_statuses(milestones, launch_date)
    
    return mission
