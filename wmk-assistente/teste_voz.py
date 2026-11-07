import json
from urllib.request import Request, urlopen
from pathlib import Path
root=Path(__file__).resolve().parent
with urlopen('http://127.0.0.1:18765/') as r:
    html=r.read().decode('utf-8')
    print('HTML:',r.status,'Gerar WAV:', 'gerarVoz' in html)
req=Request('http://127.0.0.1:18765/api/voz',data=json.dumps({'texto':'Ola! Eu sou o assistente WMK. Este e o primeiro teste de voz.'}).encode(),headers={'Content-Type':'application/json'})
with urlopen(req,timeout=120) as r:
    result=json.load(r)
    print('Resposta:',result)
with urlopen('http://127.0.0.1:18765'+result['url']) as r:
    wav=r.read()
    print('WAV:',r.status,'bytes:',len(wav),'RIFF:',wav[:4])
assert wav[:4]==b'RIFF'
