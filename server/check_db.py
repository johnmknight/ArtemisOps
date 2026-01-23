"""Quick DB query to check missions"""
import asyncio
import aiosqlite
from datetime import datetime, timezone

DB_PATH = r"C:\Users\john_\ArtemisOps\server\artemisops.db"

async def check_missions():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        
        # Get all missions
        async with db.execute("SELECT id, name, launch_date, status, patch_url, agency_logo_url FROM missions ORDER BY launch_date") as cursor:
            rows = await cursor.fetchall()
        
        now = datetime.now(timezone.utc)
        
        print(f"Total missions in DB: {len(rows)}\n")
        print(f"{'Mission':<30} {'Launch Date':<25} {'Status':<10} {'Patch?':<8} {'Logo?':<8}")
        print("-" * 90)
        
        future_count = 0
        past_count = 0
        
        for row in rows:
            row = dict(row)
            launch_date = row.get('launch_date', '')
            
            # Check if future
            is_future = False
            if launch_date:
                try:
                    dt = datetime.fromisoformat(launch_date.replace('Z', '+00:00'))
                    is_future = dt > now
                except:
                    pass
            
            if is_future:
                future_count += 1
                marker = ">"
            else:
                past_count += 1
                marker = " "
            
            has_patch = "Y" if row.get('patch_url') else "N"
            has_logo = "Y" if row.get('agency_logo_url') else "N"
            
            print(f"{marker} {row['name']:<28} {launch_date[:19] if launch_date else 'N/A':<25} {row.get('status', 'N/A'):<10} {has_patch:<8} {has_logo:<8}")
        
        print("-" * 90)
        print(f"Future missions: {future_count}")
        print(f"Past missions: {past_count}")

if __name__ == "__main__":
    asyncio.run(check_missions())
