"""Update Artemis II crew photos, bios, and bio_urls from official NASA 'Our Artemis Crew' page sources."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "artemisops.db")

UPDATES = [
    {
        "name": "Gregory R. Wiseman",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/06/jsc2023e0016434-alt.jpg",
        "bio": "Reid Wiseman was selected as a NASA astronaut in 2009 and is currently assigned as commander of NASA's Artemis II mission to the Moon. He flew aboard the International Space Station for Expedition 40/41 in 2014, logging more than 165 days in space, and served as chief of the Astronaut Office from 2020 to 2022.",
        "bio_url": "https://www.nasa.gov/humans-in-space/astronauts/g-reid-wiseman/",
    },
    {
        "name": "Victor J. Glover",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/06/jsc2023e0016433-alt.jpg",
        "bio": "Victor J. Glover was selected as a NASA astronaut in 2013 and is currently assigned as the pilot of NASA's Artemis II mission to the Moon. He previously served as pilot of NASA's SpaceX Crew-1, spending 168 days aboard the International Space Station as part of Expedition 64 and participating in four spacewalks.",
        "bio_url": "https://www.nasa.gov/humans-in-space/astronauts/victor-j-glover/",
    },
    {
        "name": "Christina Koch",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/06/jsc2023e0016435-alt.jpg",
        "bio": "Christina Hammock Koch was selected as a NASA astronaut in 2013 and is currently assigned as a mission specialist on the Artemis II mission to the Moon. She set a record for the longest single spaceflight by a woman at 328 days aboard the ISS and participated in the first all-female spacewalks.",
        "bio_url": "https://www.nasa.gov/humans-in-space/astronauts/christina-koch/",
    },
    {
        "name": "Jeremy Hansen",
        "photo_url": "https://www.nasa.gov/wp-content/uploads/2023/06/jsc2023e0016436-alt.jpg",
        "bio": "Jeremy Hansen was selected as a Canadian Space Agency astronaut in 2009 and is a former CF-18 fighter pilot with the Royal Canadian Air Force. He will become the first Canadian to venture to the Moon as a mission specialist on NASA's Artemis II mission.",
        "bio_url": "https://www.asc-csa.gc.ca/eng/astronauts/canadian/active/bio-jeremy-hansen.asp",
    },
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    for crew in UPDATES:
        cur.execute(
            "UPDATE crew SET photo_url=?, bio=?, bio_url=? WHERE name=?",
            (crew["photo_url"], crew["bio"], crew["bio_url"], crew["name"])
        )
        if cur.rowcount:
            print(f"  Updated: {crew['name']}")
        else:
            print(f"  NOT FOUND: {crew['name']}")
    
    conn.commit()
    
    # Verify
    print("\nVerification:")
    cur.execute("SELECT name, photo_url, bio, bio_url FROM crew WHERE mission_id='artemis-ii'")
    for row in cur.fetchall():
        print(f"  {row[0]}")
        print(f"    photo: {row[1][:80]}...")
        print(f"    bio: {row[2][:80]}...")
        print(f"    bio_url: {row[3]}")
    
    conn.close()

if __name__ == "__main__":
    main()
