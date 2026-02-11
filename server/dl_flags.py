import urllib.request
import os

flags = {
    'us.png': 'https://flagcdn.com/w320/us.png',
    'eu.png': 'https://flagcdn.com/w320/eu.png',
    'jp.png': 'https://flagcdn.com/w320/jp.png',
    'ru.png': 'https://flagcdn.com/w320/ru.png',
}

dest_dir = 'client/assets/flags'

for filename, url in flags.items():
    dest = os.path.join(dest_dir, filename)
    print(f'Downloading {filename}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'ArtemisOps/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f'  OK: {len(data)} bytes')
    except Exception as e:
        print(f'  FAIL: {e}')
