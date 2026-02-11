import sqlite3
conn = sqlite3.connect(r"C:\Users\john_\dev\ArtemisOps\server\artemisops.db")
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='missions'")
print(c.fetchone()[0])
print()
c.execute("SELECT id, name, patch_url FROM missions")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]} -> {row[2]}")
conn.close()
