import urllib.request
import json

endpoints = [
    'materials', 'xodimlar', 'books', 'kategoriyalar',
    'lavozimlar', 'materialturlari', 'menus', 'photos'
]

for ep in endpoints:
    url = f'http://127.0.0.1:8000/api/{ep}/'
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Endpoint /{ep}/ -> OK ({len(data.get('items', []))} items)")
    except Exception as e:
        print(f"Endpoint /{ep}/ -> FAILED: {e}")
