import sqlite3

conn = sqlite3.connect('artemisops.db')
cursor = conn.cursor()
cursor.execute('''
    SELECT title, date_label, target_date, status 
    FROM milestones 
    WHERE mission_id = 'artemis-ii' 
    ORDER BY sort_order
''')

print("Artemis II Milestones:")
print("-" * 80)
for row in cursor.fetchall():
    print(f"Title: {row[0]}")
    print(f"  date_label: {row[1]}")
    print(f"  target_date: {row[2]}")
    print(f"  status: {row[3]}")
    print()
