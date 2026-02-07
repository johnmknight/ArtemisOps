"""Update Artemis II milestones and launch date to match current NASA status (Feb 7, 2026)"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "artemisops.db")

milestones = [
    ("Dec 2025", "Flight Readiness Review", "Final comprehensive review of all mission systems", "completed"),
    ("Jan 17, 2026", "Rollout to Pad 39B", "SLS transported from VAB to Launch Complex 39B", "completed"),
    ("Feb 2-3, 2026", "Wet Dress Rehearsal", "Cryogenic propellant loaded, terminal countdown reached T-5:15, LH2 leak identified", "completed"),
    ("Feb 2026", "WDR Data Review & Issue Resolution", "Teams reviewing test data, resolving LH2 leak and valve issues before setting launch date", "active"),
    ("TBD", "Launch Readiness Review", "Final go/no-go assessment before committing to launch attempt", "pending"),
    ("~L-14 days", "Crew Quarantine", "Flight crew enters health stabilization at Kennedy Space Center", "pending"),
    ("T-6:40:00", "Cryo Loading", "Begin loading liquid hydrogen and oxygen into SLS tanks", "pending"),
    ("T-2:35:00", "Crew Ingress", "Four astronauts board Orion spacecraft", "pending"),
    ("T-00:00", "LIFTOFF", "RS-25 engines and SRBs ignite", "pending"),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Update milestones
cur.execute("DELETE FROM milestones WHERE mission_id = 'artemis-ii'")
for i, (date_label, title, desc, status) in enumerate(milestones):
    cur.execute(
        "INSERT INTO milestones (mission_id, date_label, title, description, status, sort_order) VALUES (?, ?, ?, ?, ?, ?)",
        ("artemis-ii", date_label, title, desc, status, i)
    )
print(f"Inserted {len(milestones)} milestones")

# Update launch date: NET March 6, 2026 (per Wikipedia/Planetary Society, latest available)
# Time TBD - using 12:00 UTC placeholder
cur.execute(
    "UPDATE missions SET launch_date = ?, status = ? WHERE id = 'artemis-ii'",
    ("2026-03-06T12:00:00Z", "Launch window opens March 6, 2026. NASA reviewing WDR data before setting official date.")
)
print(f"Updated launch date to 2026-03-06, rows affected: {cur.rowcount}")

conn.commit()

# Verify
cur.execute("SELECT date_label, title, status FROM milestones WHERE mission_id = 'artemis-ii' ORDER BY sort_order")
print("\nCurrent milestones:")
for row in cur.fetchall():
    print(f"  [{row[2]:10s}] {row[0]:20s} - {row[1]}")

cur.execute("SELECT launch_date, status FROM missions WHERE id = 'artemis-ii'")
row = cur.fetchone()
print(f"\nLaunch date: {row[0]}")
print(f"Status: {row[1]}")

conn.close()
