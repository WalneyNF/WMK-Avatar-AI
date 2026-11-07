"""WMK Assistente com Rosto - Ollama e texto para WAV local."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import json
import subprocess
import sys
import uuid
import tempfile
import base64
import re
import mimetypes
import job_manager
import qualidade_video

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUT = ROOT / 'resultados'
OUT.mkdir(exist_ok=True)
AVATARS = ROOT / 'avatares'
AVATARS.mkdir(exist_ok=True)
OLLAMA = 'http://127.0.0.1:11434'

class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_bytes(data, 'application/json; charset=utf-8', status)

    def send_bytes(self, data, mime, status=200, extra=None):
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        if extra:
            for k,v in extra.items(): self.send_header(k,v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/estudio':
            return self.send_bytes((ROOT/'estudio.html').read_bytes(), 'text/html; charset=utf-8')
        if path == '/biblioteca':
            return self.send_bytes((ROOT/'biblioteca.html').read_bytes(), 'text/html; charset=utf-8')
        if path == '/monitor':
            self.send_bytes((ROOT/'monitor.html').read_bytes(), 'text/html; charset=utf-8')
        elif path.startswith('/api/jobs/'):
            parts = path.strip('/').split('/')
            if len(parts) == 3 and re.fullmatch(r'[a-f0-9]{32}', parts[2]):
                job = job_manager.get(parts[2])
                return self.send_json(job) if job else self.send_error(404)
            return self.send_error(404)
        elif path.startswith('/api/video-resultado/'):
            parts = path.strip('/').split('/')
            if len(parts) == 3 and re.fullmatch(r'[a-f0-9]{32}', parts[2]):
                job = job_manager.get(parts[2])
                if not job or job['estado'] != 'concluido' or not job['arquivo']: return self.send_error(404)
                file = (job_manager.VIDEOS / job['arquivo']).resolve()
                if job_manager.VIDEOS.resolve() not in file.parents or not file.is_file(): return self.send_error(404)
                return self.send_bytes(file.read_bytes(), 'video/mp4')
            return self.send_error(404)
        elif re.fullmatch(r'/api/exportacao/[a-f0-9]{32}', path):
            job_id = path.rsplit('/', 1)[-1]
            file = job_manager.VIDEOS / ('export-' + job_id + '.mp4')
            if not file.is_file(): return self.send_error(404)
            return self.send_bytes(file.read_bytes(), 'video/mp4')
        elif path == '/':
            self.send_bytes((ROOT/'index.html').read_bytes(), 'text/html; charset=utf-8')
        elif path == '/api/videos':
            videos = [{'arquivo':f.name,'bytes':f.stat().st_size} for f in sorted(job_manager.VIDEOS.glob('*.mp4'), key=lambda x:x.stat().st_mtime, reverse=True) if f.is_file() and re.fullmatch(r'[0-9_.-]+\.mp4', f.name)]
            return self.send_json({'videos':videos})
        elif path.startswith('/api/video-biblioteca/'):
            name = path.rsplit('/',1)[-1]
            if not re.fullmatch(r'[0-9_.-]+\.mp4', name): return self.send_error(404)
            file = job_manager.VIDEOS / name
            if not file.is_file(): return self.send_error(404)
            return self.send_bytes(file.read_bytes(),'video/mp4')
        elif path == '/api/audios':
            self.send_json({'audios':[f.name for f in sorted(OUT.glob('wmk-*.wav')) if re.fullmatch(r'wmk-[a-f0-9-]{36}\.wav',f.name)]})
        elif path.startswith('/manuais/'):
            name = path.split('/')[-1]
            if not re.fullmatch(r'[a-z0-9-]+\.html', name): return self.send_error(404)
            file = ROOT / 'manuais' / name
            if not file.is_file(): return self.send_error(404)
            self.send_bytes(file.read_bytes(), 'text/html; charset=utf-8')
        elif path == '/api/avatares':
            self.send_json({'avatares':[{'arquivo':f.name,'url':'/api/avatar/'+f.name} for f in sorted(AVATARS.iterdir()) if f.is_file() and f.suffix.lower() in ('.png','.jpg','.jpeg','.webp')]})
        elif path.startswith('/api/avatar/'):
            name=path.split('/')[-1]
            if not re.fullmatch(r'[a-zA-Z0-9_-]+\.(png|jpg|jpeg|webp)',name): return self.send_error(404)
            file=AVATARS/name
            if not file.is_file(): return self.send_error(404)
            mime={'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg','webp':'image/webp'}[file.suffix[1:].lower()]
            self.send_bytes(file.read_bytes(),mime)
        elif path == '/api/status':
            try:
                with urlopen(OLLAMA+'/api/tags', timeout=15) as r:
                    models = [m['name'] for m in json.load(r).get('models', [])]
                self.send_json({'ollama':True,'modelos':models,'sad_models':(PROJECT/'checkpoints').exists(),'python':sys.version.split()[0]})
            except Exception as e:
                self.send_json({'ollama':False,'modelos':[],'sad_models':(PROJECT/'checkpoints').exists(),'erro':str(e)})
        elif path.startswith('/api/audio/') and path.endswith('.wav'):
            name=path.split('/')[-1]
            if not name.startswith('wmk-') or len(name)!=44:
                return self.send_error(404)
            file=OUT/name
            if not file.is_file(): return self.send_error(404)
            self.send_bytes(file.read_bytes(),'audio/wav',extra={'Content-Disposition':'inline; filename="'+name+'"'})
        else: self.send_error(404)

    def do_POST(self):
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>8000000: return self.send_json({'erro':'Tamanho invalido'},413)
            data=json.loads(self.rfile.read(size))
            if self.path=='/api/jobs':
                try:
                    job = job_manager.start(str(data.get('audio','')), str(data.get('avatar','')), data.get('opcoes'))
                    return self.send_json(job, 202)
                except ValueError as exc:
                    return self.send_json({'erro':str(exc)}, 400)
            elif self.path == '/api/videos/exportar':
                name = str(data.get('arquivo',''))
                if not re.fullmatch(r'[0-9_.-]+\.mp4', name):
                    return self.send_json({'erro':'Nome de video invalido'},400)
                origem = job_manager.VIDEOS / name
                if not origem.is_file(): return self.send_json({'erro':'Video nao encontrado'},404)
                export_id = uuid.uuid4().hex
                destino = job_manager.VIDEOS / ('export-' + export_id + '.mp4')
                qualidade_video.exportar(origem, destino, data.get('qualidade',{}), ffmpeg=r'D:\ffmpeg\bin\ffmpeg.exe')
                return self.send_json({'url':'/api/exportacao/'+export_id,'arquivo':destino.name})
            elif re.fullmatch(r'/api/jobs/[a-f0-9]{32}/exportar', self.path):
                job_id = self.path.split('/')[3]
                job = job_manager.get(job_id)
                if not job or job['estado'] != 'concluido' or not job['arquivo']:
                    return self.send_json({'erro':'Tarefa concluida nao encontrada'},404)
                origem = (job_manager.VIDEOS / job['arquivo']).resolve()
                if job_manager.VIDEOS.resolve() not in origem.parents:
                    return self.send_json({'erro':'Caminho invalido'},400)
                destino = job_manager.VIDEOS / ('export-' + job_id + '.mp4')
                qualidade_video.exportar(origem, destino, data.get('qualidade', {}), ffmpeg=r'D:\ffmpeg\bin\ffmpeg.exe')
                return self.send_json({'url':'/api/exportacao/' + job_id, 'arquivo':destino.name})
            elif re.fullmatch(r'/api/jobs/[a-f0-9]{32}/cancel', self.path):
                job = job_manager.cancel(self.path.split('/')[3])
                return self.send_json(job) if job else self.send_error(404)
            elif self.path=='/api/avatares':
                encoded=str(data.get('imagem',''))
                ext=str(data.get('extensao','')).lower()
                if ext not in ('png','jpg','jpeg','webp'): return self.send_json({'erro':'Formato nao permitido'},400)
                if len(encoded)>7000000: return self.send_json({'erro':'Imagem muito grande'},413)
                raw=base64.b64decode(encoded,validate=True)
                if len(raw)>5000000 or len(raw)<100: return self.send_json({'erro':'Arquivo invalido ou maior que 5 MB'},400)
                valid={'png':raw.startswith(bytes.fromhex('89504e470d0a1a0a')),'jpg':raw.startswith(bytes.fromhex('ffd8ff')),'jpeg':raw.startswith(bytes.fromhex('ffd8ff')),'webp':raw[:4]==b'RIFF' and raw[8:12]==b'WEBP'}
                if not valid[ext]: return self.send_json({'erro':'Conteudo nao corresponde ao formato'},400)
                name='avatar-'+uuid.uuid4().hex[:12]+'.'+ext
                (AVATARS/name).write_bytes(raw)
                self.send_json({'arquivo':name,'url':'/api/avatar/'+name})
            elif self.path=='/api/chat':
                msg=str(data.get('mensagem','')).strip()
                model=str(data.get('modelo','')).strip()
                if not msg or not model: return self.send_json({'erro':'Informe mensagem e modelo'},400)
                req=Request(OLLAMA+'/api/chat',data=json.dumps({'model':model,'stream':False,'messages':[{'role':'system','content':'Responda em portugues brasileiro, com clareza e objetividade.'},{'role':'user','content':msg}]}).encode(),headers={'Content-Type':'application/json'})
                with urlopen(req,timeout=180) as response: answer=json.load(response)['message']['content']
                self.send_json({'resposta':answer,'id':str(uuid.uuid4())})
            elif self.path=='/api/voz':
                texto=str(data.get('texto','')).strip()
                if not texto or len(texto)>3000: return self.send_json({'erro':'Digite de 1 a 3000 caracteres'},400)
                name='wmk-'+str(uuid.uuid4())+'.wav'
                target=OUT/name
                with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.txt',dir=str(OUT),delete=False) as f:
                    f.write(texto)
                    source=Path(f.name)
                try:
                    p=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'voz.ps1'),'-TextoArquivo',str(source),'-WavArquivo',str(target)],capture_output=True,text=True,timeout=120)
                    if p.returncode!=0 or not target.is_file() or target.stat().st_size<44:
                        target.unlink(missing_ok=True)
                        return self.send_json({'erro':'Falha no sintetizador: '+(p.stderr or p.stdout)[-700:]},502)
                    self.send_json({'arquivo':name,'url':'/api/audio/'+name,'bytes':target.stat().st_size})
                finally: source.unlink(missing_ok=True)
            else: self.send_error(404)
        except Exception as e:
            self.send_json({'erro':str(e)},502)

if __name__=='__main__':
    print('WMK Assistente: http://127.0.0.1:18765',flush=True)
    ThreadingHTTPServer(('127.0.0.1',18765),Handler).serve_forever()
