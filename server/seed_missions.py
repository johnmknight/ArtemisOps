"""
ArtemisOps Mission Seed Data
Seeds Crew Dragon missions alongside Artemis program missions.
Run: python seed_missions.py  (or imported by fetcher.py)
"""
import asyncio
from database import upsert_mission, upsert_crew, upsert_milestones, get_mission, init_db


# ============================================================================
# CREW DRAGON MISSION DATA
# Sources: NASA Commercial Crew Blog, Wikipedia, NASA press releases
# Last verified: Feb 9, 2026
# ============================================================================

CREW_DRAGON_MISSIONS = [
    # ------------------------------------------------------------------
    # CREW-10 (COMPLETED)
    # Launched: March 14, 2025 | Splashdown: August 9, 2025
    # Dragon Endurance (C210) | Falcon 9 B1094
    # ------------------------------------------------------------------
    {
        "mission": {
            "id": "crew-10",
            "name": "SpaceX Crew-10",
            "slug": "crew-10",
            "launch_date": "2025-03-14T23:03:48Z",
            "landing_date": "2025-08-09T15:33:00Z",
            "status": "Success",
            "status_description": "Crew-10 completed a 148-day mission aboard the ISS, splashing down in the Pacific Ocean off San Diego.",
            "site": "Kennedy Space Center, LC-39A",
            "rocket": "Falcon 9 Block 5",
            "spacecraft": "Crew Dragon Endurance",
            "mission_type": "Commercial Crew",
            "description": "NASA's 10th Commercial Crew rotation mission to the ISS. First Crew Dragon to splash down in the Pacific Ocean off California.",
            "patch_url": "/assets/patches/crew-10-patch.png",
            "api_source": "seed",
            "is_active": 1,
            "agencies": "NASA, JAXA, Roscosmos",
            "recovery_site": "Pacific Ocean, off San Diego",
            "recovery_lat": 32.5,
            "recovery_lon": -117.5,
            "launch_window_type": "instantaneous",
            "mission_profile": "leo-iss",
        },
        "crew": [
            {
                "name": "Anne McClain",
                "role": "Commander",
                "agency": "NASA",
                "bio": "Army colonel and combat helicopter pilot. Second spaceflight, logging 352 total days in space.",
                "sort_order": 0,
            },
            {
                "name": "Nichole Ayers",
                "role": "Pilot",
                "agency": "NASA",
                "bio": "Air Force major and F-22 Raptor pilot. First spaceflight.",
                "sort_order": 1,
            },
            {
                "name": "Takuya Onishi",
                "role": "Mission Specialist",
                "agency": "JAXA",
                "bio": "JAXA astronaut, second spaceflight. First Japanese astronaut to robotically capture Cygnus spacecraft.",
                "sort_order": 2,
            },
            {
                "name": "Kirill Peskov",
                "role": "Mission Specialist",
                "agency": "Roscosmos",
                "bio": "Roscosmos cosmonaut, former commercial airline pilot. First spaceflight.",
                "sort_order": 3,
            },
        ],
        "milestones": [
            {"date_label": "Mar 14, 2025", "title": "Launch", "description": "Falcon 9 liftoff from LC-39A, KSC", "status": "completed"},
            {"date_label": "Mar 16, 2025", "title": "ISS Docking", "description": "Docked to Harmony forward port at 12:04 AM EDT", "status": "completed"},
            {"date_label": "Aug 8, 2025", "title": "Undocking", "description": "Undocked from ISS at 6:15 PM EDT", "status": "completed"},
            {"date_label": "Aug 9, 2025", "title": "Splashdown", "description": "Pacific Ocean off San Diego at 11:33 AM EDT. First Pacific splashdown for Commercial Crew.", "status": "completed"},
        ],
    },
    # ------------------------------------------------------------------
    # CREW-11 (COMPLETED - Early return due to medical issue)
    # Launched: August 1, 2025 | Splashdown: January 15, 2026
    # Dragon Endeavour (C206) 6th flight | Falcon 9 B1094
    # ------------------------------------------------------------------
    {
        "mission": {
            "id": "crew-11",
            "name": "SpaceX Crew-11",
            "slug": "crew-11",
            "launch_date": "2025-08-01T15:43:00Z",
            "landing_date": "2026-01-15T17:00:00Z",
            "status": "Success",
            "status_description": "Crew-11 returned early after ~5.5 months due to a medical situation with a crew member. All crew returned safely.",
            "site": "Kennedy Space Center, LC-39A",
            "rocket": "Falcon 9 Block 5",
            "spacecraft": "Crew Dragon Endeavour",
            "mission_type": "Commercial Crew",
            "description": "NASA's 11th Commercial Crew rotation. Fastest Crew Dragon ISS rendezvous at 14h 43m. Returned early due to crew medical issue.",
            "patch_url": "/assets/patches/crew-11-patch.png",
            "api_source": "seed",
            "is_active": 1,
            "agencies": "NASA, JAXA, Roscosmos",
            "recovery_site": "Pacific Ocean, off California",
            "recovery_lat": 32.5,
            "recovery_lon": -117.5,
            "launch_window_type": "instantaneous",
            "mission_profile": "leo-iss",
        },
        "crew": [
            {
                "name": "Zena Cardman",
                "role": "Commander",
                "agency": "NASA",
                "bio": "Originally assigned to Crew-9, reassigned to Crew-11 in March 2025. First spaceflight.",
                "sort_order": 0,
            },
            {
                "name": "Michael Fincke",
                "role": "Pilot",
                "agency": "NASA",
                "bio": "Fourth spaceflight. Former chief of Commercial Crew Branch. Previously assigned to Boeing CFT and Starliner-1.",
                "sort_order": 1,
            },
            {
                "name": "Kimiya Yui",
                "role": "Mission Specialist",
                "agency": "JAXA",
                "bio": "JAXA astronaut, second spaceflight. Member of 2009 JAXA/NASA astronaut classes.",
                "sort_order": 2,
            },
            {
                "name": "Oleg Platonov",
                "role": "Mission Specialist",
                "agency": "Roscosmos",
                "bio": "Roscosmos cosmonaut. First spaceflight.",
                "sort_order": 3,
            },
        ],
        "milestones": [
            {"date_label": "Aug 1, 2025", "title": "Launch", "description": "Falcon 9 liftoff from LC-39A after 1-day weather scrub. Last booster landing at LZ-1.", "status": "completed"},
            {"date_label": "Aug 2, 2025", "title": "ISS Docking", "description": "Docked to Harmony zenith port at 2:26 AM EDT. Fastest rendezvous: 14h 43m.", "status": "completed"},
            {"date_label": "Jan 7, 2026", "title": "Medical Situation", "description": "Undisclosed medical issue with crew member. Planned EVA cancelled.", "status": "completed"},
            {"date_label": "Jan 8, 2026", "title": "Early Return Announced", "description": "NASA announced early return of Crew-11 due to medical concern.", "status": "completed"},
            {"date_label": "Jan 14, 2026", "title": "Undocking", "description": "Undocked from ISS at 5:00 PM EST", "status": "completed"},
            {"date_label": "Jan 15, 2026", "title": "Splashdown", "description": "Returned safely to Earth. All crew in good condition.", "status": "completed"},
        ],
    },

    # ------------------------------------------------------------------
    # CREW-12 (UPCOMING)
    # Target Launch: February 11, 2026, 6:01 AM EST from SLC-40 CCSFS
    # Dragon Freedom (C212) 5th flight | Falcon 9
    # ------------------------------------------------------------------
    {
        "mission": {
            "id": "crew-12",
            "name": "SpaceX Crew-12",
            "slug": "crew-12",
            "launch_date": "2026-02-11T11:01:00Z",
            "status": "Go",
            "status_description": "Flight Readiness Review complete. Crew in quarantine at KSC. Launch targeted Feb 11 at 6:01 AM EST.",
            "site": "Cape Canaveral SFS, SLC-40",
            "rocket": "Falcon 9 Block 5",
            "spacecraft": "Crew Dragon Freedom",
            "mission_type": "Commercial Crew",
            "description": "NASA's 12th Commercial Crew rotation. 8-month science expedition aboard ISS as Expedition 74.",
            "patch_url": "/assets/patches/crew-12-patch.png",
            "api_source": "seed",
            "is_active": 1,
            "agencies": "NASA, ESA, Roscosmos",
            "recovery_site": "Pacific Ocean, off California",
            "recovery_lat": 32.5,
            "recovery_lon": -117.5,
            "launch_window_type": "instantaneous",
            "mission_profile": "leo-iss",
        },
        "crew": [
            {
                "name": "Jessica Meir",
                "role": "Commander",
                "agency": "NASA",
                "bio": "Second spaceflight. Previously flew Expedition 61/62 (205 days). Completed first three all-woman spacewalks with Christina Koch.",
                "sort_order": 0,
            },
            {
                "name": "Jack Hathaway",
                "role": "Pilot",
                "agency": "NASA",
                "bio": "U.S. Navy commander, NASA 2021 astronaut class. First spaceflight.",
                "sort_order": 1,
            },
            {
                "name": "Sophie Adenot",
                "role": "Mission Specialist",
                "agency": "ESA",
                "bio": "ESA 2022 astronaut class. First career astronaut from that class to fly. Mission named 'Epsilon'. First spaceflight.",
                "sort_order": 2,
            },
            {
                "name": "Andrey Fedyaev",
                "role": "Mission Specialist",
                "agency": "Roscosmos",
                "bio": "Second spaceflight. Previously flew Crew-6 (186 days). Hero of the Russian Federation.",
                "sort_order": 3,
            },
        ],
        "milestones": [
            {"date_label": "Jan 28, 2026", "title": "Crew Quarantine", "description": "Crew begins 2-week quarantine at Johnson Space Center, Houston", "status": "completed"},
            {"date_label": "Feb 6, 2026", "title": "Flight Readiness Review", "description": "NASA, SpaceX, and international partners cleared Crew-12 for launch", "status": "completed"},
            {"date_label": "Feb 6, 2026", "title": "Crew Arrives at KSC", "description": "Crew arrived at Kennedy Space Center Launch and Landing Facility", "status": "completed"},
            {"date_label": "Feb 9, 2026", "title": "Dry Dress Rehearsal", "description": "Full rehearsal of launch day activities including suit-up and pad access", "status": "active"},
            {"date_label": "Feb 11, 2026", "title": "LAUNCH", "description": "Targeted 6:01 AM EST from SLC-40, Cape Canaveral Space Force Station", "status": "pending"},
            {"date_label": "Feb 12, 2026", "title": "ISS Docking", "description": "Targeted docking ~10:30 AM EST at Harmony module", "status": "pending"},
            {"date_label": "~Oct 2026", "title": "Undocking & Splashdown", "description": "Planned return after 8-month science expedition", "status": "pending"},
        ],
    },
]


# ============================================================================
# SEED FUNCTIONS
# ============================================================================

async def seed_crew_dragon_missions(force: bool = False):
    """
    Seed Crew Dragon missions into the database.
    
    Args:
        force: If True, overwrite existing missions. If False, skip existing.
    """
    seeded = 0
    skipped = 0
    
    for entry in CREW_DRAGON_MISSIONS:
        mission_data = entry["mission"]
        mission_id = mission_data["id"]
        
        existing = await get_mission(mission_id)
        if existing and not force:
            print(f"  Skipping {mission_data['name']} (already exists)")
            skipped += 1
            continue
        
        await upsert_mission(mission_data)
        
        if entry.get("crew"):
            await upsert_crew(mission_id, entry["crew"])
        
        if entry.get("milestones"):
            await upsert_milestones(mission_id, entry["milestones"])
        
        print(f"  Seeded {mission_data['name']} with {len(entry.get('crew', []))} crew, {len(entry.get('milestones', []))} milestones")
        seeded += 1
    
    return {"seeded": seeded, "skipped": skipped}


async def seed_all(force: bool = False):
    """Seed all mission data"""
    await init_db()
    
    print("Seeding Crew Dragon missions...")
    result = await seed_crew_dragon_missions(force=force)
    print(f"Done: {result['seeded']} seeded, {result['skipped']} skipped")
    
    return result


# CLI runner
if __name__ == "__main__":
    import sys
    force = "--force" in sys.argv
    if force:
        print("Force mode: overwriting existing missions")
    asyncio.run(seed_all(force=force))
