"""Gerenciador local de tarefas de video do WMK Avatar AI."""
import json
import re
import subprocess
import sys
import threading
import time
import uuid
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUT = ROOT / "resultados"
VIDEOS = OUT / "videos"
AVATARS = ROOT / "avatares"
JOBS = {}
LOCK = threading.RLock()
PHASES = ("Aguardando", "Deteccao facial", "Reconstrucao 3D", "Analise do audio", "Expressoes faciais", "Renderizacao", "Montagem MP4", "Concluido")
PROGRESS = re.compile(r"(\d{1,3})%\|.*?\|\s*(\d+)\/(\d+)")
MAX_JOBS = 30

def snapshot(job):
    with LOCK:
        return {k: (list(v) if k == 'logs' else v) for k, v in job.items() if k not in ("process", "thread", "folder_before")}

def get(job_id):
    with LOCK:
        job = JOBS.get(job_id)
        return snapshot(job) if job else None

def _update(job, **fields):
    with LOCK:
        job.update(fields)
        job["atualizado"] = time.time()

def _parse(job, line):
    line = line.strip()
    if not line:
        return
    with LOCK:
        job["logs"].append(line[-350:])
    labels = (("landmark Det", 1), ("3DMM Extraction", 2), ("mel:", 3), ("audio2exp", 4), ("Face Renderer", 5))
    for label, phase in labels:
        if label in line:
            m = PROGRESS.search(line)
            values = {"etapa": PHASES[phase], "etapa_indice": phase}
            if m:
                values.update({"percentual_etapa": min(100, int(m.group(1))), "quadros_feitos": int(m.group(2)) if phase == 5 else job["quadros_feitos"], "quadros_total": int(m.group(3)) if phase == 5 else job["quadros_total"]})
            _update(job, **values)
            return
    if "video is saved" in line.lower() or "saving video" in line.lower():
        _update(job, etapa=PHASES[6], etapa_indice=6, percentual_etapa=0)

def _run(job, command):
    try:
        kwargs = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "text": True, "bufsize": 1, "cwd": str(PROJECT), "errors": "replace"}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        p = subprocess.Popen(command, **kwargs)
        with LOCK:
            job["process"] = p
        buffer = ""
        while True:
            ch = p.stdout.read(1)
            if not ch:
                break
            if ch in "\r\n":
                if buffer:
                    _parse(job, buffer)
                    buffer = ""
            else:
                buffer = (buffer + ch)[-1500:]
        if buffer:
            _parse(job, buffer)
        rc = p.wait()
        with LOCK:
            cancelled = job["estado"] == "cancelado"
        if cancelled:
            return
        if rc:
            _update(job, estado="erro", erro="Processo terminou com codigo " + str(rc))
            return
        # O arquivo final pode estar na pasta raiz ou numa subpasta da tarefa.
        files = [f for f in VIDEOS.rglob("*.mp4") if f.is_file() and f.stat().st_mtime >= job["inicio"] - 2]
        if not files:
            _update(job, estado="erro", erro="Processo terminou sem MP4 verificavel")
            return
        result = max(files, key=lambda f: f.stat().st_mtime)
        _update(job, estado="concluido", etapa=PHASES[7], etapa_indice=7, percentual_etapa=100, arquivo=str(result.relative_to(VIDEOS)).replace("\\", "/"))
    except Exception as exc:
        _update(job, estado="erro", erro=str(exc))
    finally:
        with LOCK:
            job.pop("process", None)

def start(audio_name, avatar_name, options=None):
    options = options or {}
    if not isinstance(options, dict):
        raise ValueError('Configuracoes invalidas')
    batch_size = options.get('batch_size', 2)
    preprocess = options.get('preprocess', 'crop')
    still = options.get('still', False)
    if type(batch_size) is not int or batch_size not in (1, 2, 4):
        raise ValueError('Lote permitido: 1, 2 ou 4')
    if preprocess not in ('crop', 'resize'):
        raise ValueError('Preprocessamento invalido')
    if type(still) is not bool:
        raise ValueError('Modo estatico invalido')
    if not re.fullmatch(r"wmk-[a-f0-9-]{36}\.wav", audio_name):
        raise ValueError("Arquivo WAV invalido")
    if not re.fullmatch(r"avatar-[a-f0-9]{12}\.(png|jpg|jpeg|webp)", avatar_name):
        raise ValueError("Avatar invalido")
    audio, avatar = OUT / audio_name, AVATARS / avatar_name
    if not audio.is_file() or not avatar.is_file():
        raise ValueError("Avatar ou WAV nao encontrado")
    with LOCK:
        if any(j["estado"] in ("aguardando", "executando") for j in JOBS.values()):
            raise ValueError("Ja existe uma renderizacao em andamento")
        if len(JOBS) >= MAX_JOBS:
            for key in list(JOBS):
                if JOBS[key]["estado"] not in ("aguardando", "executando"):
                    JOBS.pop(key)
                    break
        job_id = uuid.uuid4().hex
        job = {"id": job_id, "estado": "aguardando", "etapa": PHASES[0], "etapa_indice": 0, "percentual_etapa": 0, "quadros_feitos": 0, "quadros_total": 0, "logs": deque(maxlen=60), "erro": None, "arquivo": None, "inicio": time.time(), "atualizado": time.time()}
        JOBS[job_id] = job
    VIDEOS.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, "-u", str(PROJECT / "inference.py"), "--driven_audio", str(audio), "--source_image", str(avatar), "--cpu", "--size", "256", "--result_dir", str(VIDEOS)]
    command.extend(['--batch_size', str(batch_size), '--preprocess', preprocess])
    if still:
        command.append('--still')
    _update(job, estado="executando")
    t = threading.Thread(target=_run, args=(job, command), daemon=True)
    t.start()
    return snapshot(job)

def cancel(job_id):
    with LOCK:
        job = JOBS.get(job_id)
        if not job:
            return None
        if job["estado"] not in ("aguardando", "executando"):
            return snapshot(job)
        job["estado"] = "cancelado"
        job["etapa"] = "Cancelado pelo usuario"
        proc = job.get("process")
    if proc and proc.poll() is None:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=15)
        else:
            proc.terminate()
    return snapshot(job)
