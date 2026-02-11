"""
Download all remote images to local assets and update DB paths.
Run from ArtemisOps root: python server/localize_images.py
"""
import sqlite3
import urllib.request
import os
import re
from pathlib import Path

CLIENT = Path("client/assets")
DB_PATH = "server/artemisops.db"

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def download(url, dest):
    """Download url to dest. Skip if already exists."""
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  SKIP (exists): {dest.name}")
        return True
    print(f"  Downloading: {url[:80]}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ArtemisOps/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        dest.write_bytes(data)
        print(f"  OK: {dest.name} ({len(data)//1024}KB)")
        return True
    except Exception as e:
        print(f"  FAIL: {e}")
        return False

def ext_from_url(url):
    """Get file extension from URL."""
    path = url.split('?')[0].split('#')[0]
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.webp'):
        return ext
    return '.png'  # default

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # === 1. AGENCY LOGOS ===
    print("\n=== AGENCY LOGOS ===")
    logos_dir = CLIENT / "logos"
    logos_dir.mkdir(exist_ok=True)

    agency_logos = {
        'nasa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/NASA_logo.svg/200px-NASA_logo.svg.png',
        'esa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/ESA_logo.svg/200px-ESA_logo.svg.png',
        'jaxa': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Jaxa_logo.svg/200px-Jaxa_logo.svg.png',
        'spacex': 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/SpaceX-Logo.svg/200px-SpaceX-Logo.svg.png',
    }

    # NASA SVG already exists locally, but download PNG version too for consistency
    # Actually, we already have nasa-logo.svg. Let's download the others.
    for agency, url in agency_logos.items():
        # nasa-logo.svg already exists, but we need the PNG for <img> tags
        dest = logos_dir / f"{agency}-logo{ext_from_url(url)}"
        if agency == 'nasa' and (logos_dir / 'nasa-logo.svg').exists():
            print(f"  SKIP (have SVG): nasa-logo.svg")
            continue
        download(url, dest)

    # === 2. CREW PHOTOS ===
    print("\n=== CREW PHOTOS ===")
    crew_dir = CLIENT / "crew"
    crew_dir.mkdir(exist_ok=True)

    c.execute("SELECT id, mission_id, name, photo_url FROM crew WHERE photo_url IS NOT NULL AND photo_url != ''")
    crew_rows = c.fetchall()

    for crew_id, mission_id, name, photo_url in crew_rows:
        if photo_url.startswith('/assets/'):
            print(f"  SKIP (already local): {name}")
            continue
        filename = f"{slugify(name)}{ext_from_url(photo_url)}"
        dest = crew_dir / filename
        if download(photo_url, dest):
            local_path = f"/assets/crew/{filename}"
            c.execute("UPDATE crew SET photo_url = ? WHERE id = ?", (local_path, crew_id))
            print(f"  DB updated: {name} -> {local_path}")

    # === 3. MISSION IMAGES (hero/background) ===
    print("\n=== MISSION IMAGES ===")
    images_dir = CLIENT / "images"
    images_dir.mkdir(exist_ok=True)

    c.execute("SELECT id, slug, image_url, agency_logo_url FROM missions WHERE is_active = 1")
    missions = c.fetchall()

    for mid, slug, image_url, agency_logo_url in missions:
        # Hero image
        if image_url and image_url.startswith('http'):
            filename = f"{slug}-hero{ext_from_url(image_url)}"
            dest = images_dir / filename
            if download(image_url, dest):
                local_path = f"/assets/images/{filename}"
                c.execute("UPDATE missions SET image_url = ? WHERE id = ?", (local_path, mid))
                print(f"  DB updated: {slug} image_url -> {local_path}")

        # Agency logo in DB
        if agency_logo_url and agency_logo_url.startswith('http'):
            # Point to local NASA SVG or downloaded logo
            if 'NASA' in agency_logo_url or 'nasa' in agency_logo_url.lower():
                local_path = "/assets/logos/nasa-logo.svg"
            else:
                # Try to match to downloaded logo
                for agency in agency_logos:
                    if agency in agency_logo_url.lower():
                        local_path = f"/assets/logos/{agency}-logo{ext_from_url(agency_logos[agency])}"
                        break
                else:
                    # Download as mission-specific
                    filename = f"{slug}-agency-logo{ext_from_url(agency_logo_url)}"
                    dest = logos_dir / filename
                    download(agency_logo_url, dest)
                    local_path = f"/assets/logos/{filename}"

            c.execute("UPDATE missions SET agency_logo_url = ? WHERE id = ?", (local_path, mid))
            print(f"  DB updated: {slug} agency_logo_url -> {local_path}")

    conn.commit()
    conn.close()
    print("\n=== DONE ===")
    print("Next: update AGENCY_LOGOS in tabs/mission.html to use local paths")

if __name__ == '__main__':
    main()
