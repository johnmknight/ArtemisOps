"""Check what CelesTrak returns for Dragon-related objects"""
import httpx
import asyncio

STATIONS_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"
ACTIVE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

DRAGON_PATTERNS = ["CREW DRAGON", "DRAGON", "CREW-", "FREEDOM", "ENDEAVOUR", "ENDURANCE", "RESILIENCE", "GRACE"]

def parse_tles(text):
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    sats = []
    i = 0
    while i < len(lines) - 2:
        name = lines[i]
        l1 = lines[i+1]
        l2 = lines[i+2]
        if l1.startswith("1 ") and l2.startswith("2 "):
            sats.append({"name": name, "norad": l1[2:7].strip(), "line1": l1, "line2": l2})
            i += 3
        else:
            i += 1
    return sats

async def main():
    async with httpx.AsyncClient(timeout=15) as client:
        for url, label in [(STATIONS_URL, "stations"), (ACTIVE_URL, "active")]:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                sats = parse_tles(resp.text)
                print(f"\n=== {label.upper()} ({len(sats)} total) ===")
                
                # Find anything Dragon-related
                for s in sats:
                    name_upper = s["name"].upper()
                    if any(p in name_upper for p in DRAGON_PATTERNS):
                        print(f"  NORAD {s['norad']:6s} | {s['name']}")
                
                # Also look for anything launched very recently (epoch in line1)
                # TLE epoch is columns 18-32 of line 1: YY DDD.fractional
                print(f"\n  Recent objects (epoch > 26044 = Feb 13, 2026):")
                for s in sats:
                    epoch_str = s["line1"][18:32].strip()
                    try:
                        epoch_year = int(epoch_str[:2])
                        epoch_day = float(epoch_str[2:])
                        if epoch_year == 26 and epoch_day >= 43:  # Feb 12+
                            print(f"  NORAD {s['norad']:6s} | epoch {epoch_str:14s} | {s['name']}")
                    except:
                        pass
                        
            except Exception as e:
                print(f"  Error fetching {label}: {e}")

asyncio.run(main())
