import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/tools/transliterate/',
    data=json.dumps({'text': "O' G' Sh Ch o' g' sh ch"}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("API Result:", data['result'])
