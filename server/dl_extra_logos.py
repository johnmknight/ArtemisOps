import urllib.request

# Direct SVG URLs (not thumbnails)
logos = {
    'csa-logo.svg': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Canadian_Space_Agency_logo.svg',
    'roscosmos-logo.svg': 'https://upload.wikimedia.org/wikipedia/commons/d/da/Roscosmos_logo_en.svg',
}

for filename, url in logos.items():
    dest = f'client/assets/logos/{filename}'
    print(f'Downloading {filename}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f'  OK: {len(data)} bytes')
    except Exception as e:
        print(f'  FAIL: {e}')
