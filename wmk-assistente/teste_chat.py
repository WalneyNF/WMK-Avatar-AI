import json
from urllib.request import Request, urlopen
payload = json.dumps({'modelo':'qwen2.5-coder:3b','mensagem':'Responda apenas: Ola, sou o assistente WMK.'}).encode('utf-8')
req = Request('http://127.0.0.1:18765/api/chat', data=payload, headers={'Content-Type':'application/json'})
with urlopen(req, timeout=180) as r:
    print(r.status, r.read().decode('utf-8'))
