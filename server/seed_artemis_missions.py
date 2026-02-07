"""
Populate Artemis missions database with NASA-sourced data.

Sources:
- https://www.nasa.gov/humans-in-space/artemis/
- https://www.nasa.gov/mission/artemis-ii/
- https://www.nasa.gov/mission/artemis-iii/
- https://www.nasa.gov/general/nasas-artemis-iv-building-first-lunar-space-station/
- https://en.wikipedia.org/wiki/Artemis_program (for timeline/dates)
- https://www.nasa.gov/reference/human-landing-systems-2/
- https://www.nasa.gov/missions/artemis/faq-nasas-artemis-campaign-and-recent-updates/

Run: python seed_artemis_missions.py
"""
import sqlite3
import sys
from datetime import datetime

DB_PATH = r"C:\Users\john_\dev\ArtemisOps\server\artemisops.db"

def main():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    c = db.cursor()
    now = datetime.utcnow().isoformat() + "Z"
    
    # =========================================================================
    # CLEANUP: Remove non-Artemis-program mission and duplicate phase entries
    # =========================================================================
    
    # artemis-bsat-2b is the ESA Artemis communications satellite, not NASA Artemis program
    cleanup_ids = [
        "artemis-bsat-2b",        # ESA satellite, not Artemis program
        "artemis-ii-orbit",       # Duplicate phase entry from Space Devs
        "artemis-ii-launch",      # Duplicate phase entry from Space Devs
        "artemis-ii-countdown",   # Duplicate phase entry from Space Devs
    ]
    for mid in cleanup_ids:
        c.execute("DELETE FROM crew WHERE mission_id = ?", (mid,))
        c.execute("DELETE FROM milestones WHERE mission_id = ?", (mid,))
        c.execute("DELETE FROM missions WHERE id = ?", (mid,))
        print(f"  Cleaned up: {mid}")
    
    # =========================================================================
    # ARTEMIS I — Completed (already in DB, update description)
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            description = 'First integrated flight test of SLS and Orion. Uncrewed mission sent Orion 280,000 miles from Earth in a 25.5-day mission, including distant retrograde orbit around the Moon. Launched Nov 16, 2022; splashdown Dec 11, 2022.',
            mission_type = 'Artemis',
            status = 'Complete',
            landing_date = '2022-12-11T17:40:00Z',
            agencies = 'NASA,ESA',
            rocket = 'SLS Block 1',
            spacecraft = 'Orion MPCV',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-i'
    """, (now,))
    print("  Updated: artemis-i")
    
    # =========================================================================
    # ARTEMIS II — Already well-populated, just normalize fields
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            description = 'First crewed Artemis mission. Four astronauts will fly around the Moon on a ~10-day mission, testing Orion life support systems and deep space navigation. First crewed flight beyond low Earth orbit since Apollo 17 (1972). Includes laser communications demo via OACS.',
            mission_type = 'Artemis',
            agencies = 'NASA,CSA',
            rocket = 'SLS Block 1',
            spacecraft = 'Orion MPCV',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-ii'
    """, (now,))
    print("  Updated: artemis-ii")
    
    # =========================================================================
    # ARTEMIS III — First lunar landing since Apollo 17
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            name = 'Artemis III',
            description = 'First crewed lunar landing since Apollo 17 (1972). Four crew launch in Orion, two transfer to SpaceX Starship HLS in lunar orbit and descend to the South Pole for ~1 week of surface EVAs. Crew will collect samples, deploy instruments, and test new exploration technologies. ~30 day total mission.',
            mission_type = 'Artemis',
            status = 'In Development',
            launch_date = '2027-06-15T00:00:00Z',
            agencies = 'NASA,SpaceX',
            rocket = 'SLS Block 1',
            spacecraft = 'Orion MPCV + Starship HLS',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-iii'
    """, (now,))
    
    # Fix crew — Artemis III crew is TBD (Wiseman/Glover/Koch/Hansen is Artemis II)
    c.execute("DELETE FROM crew WHERE mission_id = 'artemis-iii'")
    # No crew assigned yet for Artemis III
    
    # Add milestones
    c.execute("DELETE FROM milestones WHERE mission_id = 'artemis-iii'")
    artemis_iii_milestones = [
        ("Starship HLS Development", "SpaceX developing Starship lunar lander variant with in-space refueling capability", "In Progress", 0),
        ("Starship Propellant Transfer Demo", "Orbital fuel transfer demonstration required before crewed landing", "Pending", 1),
        ("Starship Uncrewed Lunar Landing Demo", "Uncrewed Starship HLS demonstration landing at lunar south pole", "Pending", 2),
        ("Axiom Space Suit Development", "Advanced EVA suits (AxEMU) for lunar surface operations", "In Progress", 3),
        ("Orion Heat Shield Enhancements", "Manufacturing improvements based on Artemis I char loss investigation", "In Progress", 4),
        ("Crew Announcement", "NASA to announce Artemis III crew assignments", "Pending", 5),
        ("Starship HLS Launch to Lunar Orbit", "Starship pre-positioned in lunar orbit awaiting crew", "Pending", 6),
        ("SLS/Orion Launch", "Crew of four launches from KSC on SLS Block 1", "Pending", 7),
        ("Lunar Orbit Rendezvous", "Orion docks with Starship HLS; two crew transfer for descent", "Pending", 8),
        ("Lunar South Pole Landing", "First humans on the Moon since December 1972", "Pending", 9),
        ("Surface EVAs", "Moonwalks for sample collection, instrument deployment, and exploration", "Pending", 10),
        ("Lunar Ascent & Crew Transfer", "Crew returns to Orion in lunar orbit via Starship", "Pending", 11),
        ("Trans-Earth Injection", "Orion departs lunar orbit for return to Earth", "Pending", 12),
        ("Splashdown", "Orion splashdown in Pacific Ocean", "Pending", 13),
    ]
    for title, desc, status, order in artemis_iii_milestones:
        c.execute("""
            INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
            VALUES ('artemis-iii', ?, ?, ?, ?, ?, ?)
        """, (title, desc, status.lower(), order, now, now))
    print("  Updated: artemis-iii (mission + milestones, crew set to TBD)")
    
    # =========================================================================
    # ARTEMIS IV — Gateway debut, SLS Block 1B
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            name = 'Artemis IV',
            description = 'Debuts humanity''s first lunar space station, Gateway. First flight of SLS Block 1B with Exploration Upper Stage and new Mobile Launcher 2. Delivers ESA''s I-Hab module to Gateway. Two crew descend to lunar south pole via upgraded Starship HLS (Gateway-compatible) while two remain aboard Gateway. ~30 day mission.',
            mission_type = 'Artemis',
            status = 'In Development',
            launch_date = '2028-09-01T00:00:00Z',
            agencies = 'NASA,ESA,JAXA,SpaceX',
            rocket = 'SLS Block 1B',
            spacecraft = 'Orion MPCV + Gateway + Starship HLS',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-iv'
    """, (now,))
    
    c.execute("DELETE FROM crew WHERE mission_id = 'artemis-iv'")
    c.execute("DELETE FROM milestones WHERE mission_id = 'artemis-iv'")
    artemis_iv_milestones = [
        ("Gateway PPE+HALO Launch", "SpaceX Falcon Heavy launches Power and Propulsion Element + Habitation and Logistics Outpost to NRHO", "In Progress", 0),
        ("Gateway PPE+HALO Arrival at NRHO", "First Gateway elements reach near-rectilinear halo orbit around Moon", "Pending", 1),
        ("SLS Block 1B & ML-2 Development", "Upgraded rocket with Exploration Upper Stage and new mobile launcher", "In Progress", 2),
        ("Starship HLS Upgrade for Gateway", "SpaceX adapts Starship for Gateway docking and increased payload", "In Progress", 3),
        ("I-Hab Module Construction", "ESA builds International Habitation module with JAXA life support", "In Progress", 4),
        ("SpaceX Dragon XL Logistics Launch", "Pre-positioned logistics module with supplies and experiments", "Pending", 5),
        ("Starship HLS Pre-Position at Gateway", "Upgraded Starship launched to Gateway ahead of crew", "Pending", 6),
        ("SLS/Orion + I-Hab Launch", "Crew of four launches with I-Hab module aboard SLS Block 1B", "Pending", 7),
        ("I-Hab Installation on Gateway", "Orion maneuvers I-Hab to dock with HALO module", "Pending", 8),
        ("Gateway Activation", "Crew enters and activates humanity's first lunar space station", "Pending", 9),
        ("Lunar Surface Expedition", "Two crew descend in Starship HLS for ~6 days on surface", "Pending", 10),
        ("Return & Splashdown", "All four crew return to Earth aboard Orion", "Pending", 11),
    ]
    for title, desc, status, order in artemis_iv_milestones:
        c.execute("""
            INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
            VALUES ('artemis-iv', ?, ?, ?, ?, ?, ?)
        """, (title, desc, status.lower(), order, now, now))
    print("  Updated: artemis-iv (mission + milestones)")
    
    # =========================================================================
    # ARTEMIS V — Blue Origin debut, ESPRIT + Canadarm3 + LTV
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            name = 'Artemis V',
            description = 'Third crewed lunar landing and first flight of Blue Origin''s Blue Moon lander. Delivers ESA''s ESPRIT refueling/communications module and CSA''s Canadarm3 robotic arm to Gateway. NASA''s Lunar Terrain Vehicle deployed to surface. First unpressurized rover since Apollo 17. ~30 day mission.',
            mission_type = 'Artemis',
            status = 'In Development',
            launch_date = '2030-03-01T00:00:00Z',
            agencies = 'NASA,ESA,CSA,Blue Origin',
            rocket = 'SLS Block 1B',
            spacecraft = 'Orion MPCV + Gateway + Blue Moon HLS',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-v'
    """, (now,))
    
    c.execute("DELETE FROM crew WHERE mission_id = 'artemis-v'")
    c.execute("DELETE FROM milestones WHERE mission_id = 'artemis-v'")
    artemis_v_milestones = [
        ("Blue Moon Mk.1 Uncrewed Demo", "Blue Origin uncrewed cargo lander demonstration to lunar surface", "In Progress", 0),
        ("Blue Moon Mk.2 Development", "Blue Origin crewed lander development, test, and verification", "In Progress", 1),
        ("ESPRIT Module Construction", "ESA builds Enhanced System Providing Refueling, Infrastructure & Telecommunications", "In Progress", 2),
        ("Canadarm3 Development", "CSA develops robotic arm system with AI-enabled autonomous operations", "In Progress", 3),
        ("Lunar Terrain Vehicle Development", "NASA procures unpressurized rover for astronaut surface mobility", "In Progress", 4),
        ("ESPRIT + Canadarm3 Delivery to Gateway", "New Gateway elements launched and installed", "Pending", 5),
        ("Blue Moon HLS Pre-Position", "Crewed Blue Moon lander pre-positioned at Gateway", "Pending", 6),
        ("LTV Pre-Position on Surface", "Lunar Terrain Vehicle delivered to landing site area", "Pending", 7),
        ("SLS/Orion Crew Launch", "Four crew launch aboard SLS Block 1B to Gateway", "Pending", 8),
        ("Lunar Surface Expedition", "Two crew descend in Blue Moon for ~1 week; first rover drives since Apollo", "Pending", 9),
        ("Return & Splashdown", "All four crew return to Earth aboard Orion", "Pending", 10),
    ]
    for title, desc, status, order in artemis_v_milestones:
        c.execute("""
            INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
            VALUES ('artemis-v', ?, ?, ?, ?, ?, ?)
        """, (title, desc, status.lower(), order, now, now))
    print("  Updated: artemis-v (mission + milestones)")
    
    # =========================================================================
    # ARTEMIS VI — Science Airlock for Gateway
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            name = 'Artemis VI',
            description = 'Fourth crewed lunar landing. Integrates the Crew and Science Airlock Module with Gateway, enabling direct EVA access from the station. Expands Gateway''s capabilities for science and exploration. Regular cadence of annual lunar landings begins.',
            mission_type = 'Artemis',
            status = 'Planning',
            launch_date = '2031-03-01T00:00:00Z',
            agencies = 'NASA',
            rocket = 'SLS Block 1B',
            spacecraft = 'Orion MPCV + Gateway + HLS (TBD)',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-vi'
    """, (now,))
    
    c.execute("DELETE FROM crew WHERE mission_id = 'artemis-vi'")
    c.execute("DELETE FROM milestones WHERE mission_id = 'artemis-vi'")
    artemis_vi_milestones = [
        ("Crew & Science Airlock Construction", "Airlock module under construction for Gateway integration", "In Progress", 0),
        ("HLS Provider Selection", "SpaceX or Blue Origin selected for Artemis VI landing", "Pending", 1),
        ("Airlock Delivery to Gateway", "Crew & Science Airlock launched and installed on Gateway", "Pending", 2),
        ("SLS/Orion Crew Launch", "Four crew launch to Gateway", "Pending", 3),
        ("Lunar Surface Expedition", "Two crew descend for surface operations", "Pending", 4),
        ("Return & Splashdown", "Crew returns to Earth aboard Orion", "Pending", 5),
    ]
    for title, desc, status, order in artemis_vi_milestones:
        c.execute("""
            INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
            VALUES ('artemis-vi', ?, ?, ?, ?, ?, ?)
        """, (title, desc, status.lower(), order, now, now))
    print("  Updated: artemis-vi (mission + milestones)")
    
    # =========================================================================
    # ARTEMIS VII — Lunar Cruiser (JAXA pressurized rover)
    # =========================================================================
    c.execute("""
        UPDATE missions SET
            name = 'Artemis VII',
            description = 'Fifth crewed lunar landing. Delivers the Habitable Mobility Platform (Lunar Cruiser), a JAXA-developed pressurized rover enabling multi-day traverses across the lunar surface. Crew can drive shirt-sleeve in the pressurized cabin, dramatically expanding exploration range beyond EVA walkback limits.',
            mission_type = 'Artemis',
            status = 'Planning',
            launch_date = '2032-03-01T00:00:00Z',
            agencies = 'NASA,JAXA',
            rocket = 'SLS Block 1B',
            spacecraft = 'Orion MPCV + Gateway + HLS (TBD)',
            site = 'Kennedy Space Center, LC-39B',
            updated_at = ?
        WHERE id = 'artemis-vii'
    """, (now,))
    
    c.execute("DELETE FROM crew WHERE mission_id = 'artemis-vii'")
    c.execute("DELETE FROM milestones WHERE mission_id = 'artemis-vii'")
    artemis_vii_milestones = [
        ("Lunar Cruiser Development", "JAXA/Toyota pressurized rover development for multi-day surface traverses", "In Progress", 0),
        ("HMP Delivery to Surface", "Habitable Mobility Platform pre-positioned on lunar surface", "Pending", 1),
        ("SLS/Orion Crew Launch", "Four crew launch to Gateway", "Pending", 2),
        ("Lunar Surface Expedition", "Extended surface operations with pressurized rover", "Pending", 3),
        ("Return & Splashdown", "Crew returns to Earth aboard Orion", "Pending", 4),
    ]
    for title, desc, status, order in artemis_vii_milestones:
        c.execute("""
            INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
            VALUES ('artemis-vii', ?, ?, ?, ?, ?, ?)
        """, (title, desc, status.lower(), order, now, now))
    print("  Updated: artemis-vii (mission + milestones)")
    
    # =========================================================================
    # ARTEMIS VIII — Future planning (add if not exists)
    # =========================================================================
    c.execute("SELECT id FROM missions WHERE id = 'artemis-viii'")
    if not c.fetchone():
        c.execute("""
            INSERT INTO missions (id, name, slug, description, mission_type, status, launch_date, 
                                  agencies, rocket, spacecraft, site, is_active, created_at, updated_at)
            VALUES ('artemis-viii', 'Artemis VIII', 'artemis-viii',
                    'Sixth crewed lunar landing. Delivers Foundational Surface Habitat and logistics for long-duration surface stays. Part of NASA''s plan for annual crewed lunar landings and sustained presence.',
                    'Artemis', 'Planning', '2033-03-01T00:00:00Z',
                    'NASA,Blue Origin', 'SLS Block 1B', 'Orion MPCV + Gateway + Blue Moon HLS',
                    'Kennedy Space Center, LC-39B', 1, ?, ?)
        """, (now, now))
        artemis_viii_milestones = [
            ("Surface Habitat Development", "Foundational Surface Habitat for extended lunar stays", "Concept", 0),
            ("Surface Logistics Planning", "Cargo lander missions to pre-position habitat and supplies", "Concept", 1),
            ("SLS/Orion Crew Launch", "Four crew launch to Gateway", "Pending", 2),
            ("Lunar Surface Expedition", "Extended surface operations with habitat", "Pending", 3),
            ("Return & Splashdown", "Crew returns to Earth aboard Orion", "Pending", 4),
        ]
        for title, desc, status, order in artemis_viii_milestones:
            c.execute("""
                INSERT INTO milestones (mission_id, title, description, status, sort_order, created_at, updated_at)
                VALUES ('artemis-viii', ?, ?, ?, ?, ?, ?)
            """, (title, desc, status.lower(), order, now, now))
        print("  Created: artemis-viii (new mission + milestones)")
    else:
        print("  Skipped: artemis-viii (already exists)")
    
    db.commit()
    
    # =========================================================================
    # VERIFY
    # =========================================================================
    print("\n=== VERIFICATION ===")
    c.execute("""
        SELECT id, name, status, launch_date, rocket, agencies 
        FROM missions 
        WHERE mission_type = 'Artemis' OR id LIKE 'artemis%'
        ORDER BY launch_date
    """)
    for r in c.fetchall():
        print(f"  {r['id']:18s} | {r['name']:18s} | {str(r['status']):18s} | {str(r['launch_date'])[:10]:10s} | {str(r['rocket']):15s} | {str(r['agencies'])}")
    
    print("\n=== MILESTONE COUNTS ===")
    c.execute("""
        SELECT m.id, m.name, COUNT(ms.id) as milestone_count
        FROM missions m
        LEFT JOIN milestones ms ON m.id = ms.mission_id
        WHERE m.mission_type = 'Artemis' OR m.id LIKE 'artemis%'
        GROUP BY m.id
        ORDER BY m.launch_date
    """)
    for r in c.fetchall():
        print(f"  {r['name']:18s} | {r['milestone_count']} milestones")
    
    print("\n=== CREW COUNTS ===")
    c.execute("""
        SELECT m.id, m.name, COUNT(cr.id) as crew_count
        FROM missions m
        LEFT JOIN crew cr ON m.id = cr.mission_id
        WHERE m.mission_type = 'Artemis' OR m.id LIKE 'artemis%'
        GROUP BY m.id
        ORDER BY m.launch_date
    """)
    for r in c.fetchall():
        crew_label = f"{r['crew_count']} assigned" if r['crew_count'] > 0 else "TBD"
        print(f"  {r['name']:18s} | {crew_label}")
    
    db.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
