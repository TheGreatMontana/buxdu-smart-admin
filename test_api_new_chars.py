import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/tools/transliterate/',
    data=json.dumps({'text': "G' g', O' o', Sh sh, Ch ch, Is'hoq."}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

# Start server if not running, or test if running
try:
    with urllib.request.urlopen(req, timeout=3) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print("API output:", data['result'])
except Exception as e:
    print("Server not responding yet:", e)
