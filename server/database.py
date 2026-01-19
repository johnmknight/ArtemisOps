"""
ArtemisOps Database Layer
SQLite database for missions, crew, milestones with async support
"""
import aiosqlite
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import json

DB_PATH = Path(__file__).parent / "artemisops.db"


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
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
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

async def get_all_missions(active_only: bool = True) -> list[dict]:
    """Get all missions"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT * FROM missions"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY launch_date ASC"
        
        async with db.execute(query) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


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
                    name = ?, slug = ?, launch_date = ?, status = ?,
                    status_description = ?, site = ?, rocket = ?, spacecraft = ?,
                    mission_type = ?, description = ?, image_url = ?,
                    api_id = ?, api_source = ?, is_active = ?, updated_at = ?
                WHERE id = ?
            """, (
                mission.get('name'), mission.get('slug'), mission.get('launch_date'),
                mission.get('status'), mission.get('status_description'),
                mission.get('site'), mission.get('rocket'), mission.get('spacecraft'),
                mission.get('mission_type'), mission.get('description'),
                mission.get('image_url'), mission.get('api_id'), mission.get('api_source'),
                mission.get('is_active', 1), now, mission['id']
            ))
        else:
            await db.execute("""
                INSERT INTO missions (
                    id, name, slug, launch_date, status, status_description,
                    site, rocket, spacecraft, mission_type, description,
                    image_url, api_id, api_source, is_active, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mission['id'], mission.get('name'), mission.get('slug'),
                mission.get('launch_date'), mission.get('status'),
                mission.get('status_description'), mission.get('site'),
                mission.get('rocket'), mission.get('spacecraft'),
                mission.get('mission_type'), mission.get('description'),
                mission.get('image_url'), mission.get('api_id'),
                mission.get('api_source'), mission.get('is_active', 1), now, now
            ))
        
        await db.commit()
        return mission['id']


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


# === Full Mission Data (with crew and milestones) ===

async def get_full_mission(mission_id: str) -> Optional[dict]:
    """Get mission with crew and milestones"""
    mission = await get_mission(mission_id)
    if not mission:
        return None
    
    mission['crew'] = await get_crew(mission['id'])
    mission['milestones'] = await get_milestones(mission['id'])
    return mission
