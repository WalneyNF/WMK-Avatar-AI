"""Exportacao nao destrutiva de MP4 existente com FFmpeg."""
from pathlib import Path
import subprocess

RESOLUCOES = {'original': None, '480p': 480, '720p': 720, '1080p': 1080}
CRFS = (18, 20, 23, 26, 28)
PRESETS = ('ultrafast', 'fast', 'medium', 'slow')
FPS = (15, 25, 30)
NITIDEZ = ('desligada', 'suave', 'media')
AUDIO = (128, 192, 256)


def validar(opcoes):
    if not isinstance(opcoes, dict):
        raise ValueError('Opcoes de exportacao invalidas')
    cfg = {'resolucao': 'original', 'crf': 20, 'preset': 'fast', 'fps': 25, 'nitidez': 'desligada', 'audio_kbps': 192}
    cfg.update(opcoes)
    limites = {'resolucao': RESOLUCOES, 'crf': CRFS, 'preset': PRESETS, 'fps': FPS, 'nitidez': NITIDEZ, 'audio_kbps': AUDIO}
    for k, valores in limites.items():
        if type(cfg[k]) not in (int, str) or cfg[k] not in valores:
            raise ValueError('Valor invalido para ' + k)
    return cfg


def exportar(origem, destino, opcoes, ffmpeg='ffmpeg', timeout=1200):
    cfg = validar(opcoes)
    origem, destino = Path(origem).resolve(), Path(destino).resolve()
    if not origem.is_file() or origem.suffix.lower() != '.mp4':
        raise ValueError('MP4 original nao encontrado')
    if origem == destino or destino.suffix.lower() != '.mp4':
        raise ValueError('Destino deve ser outro arquivo MP4')
    filtros = []
    altura = RESOLUCOES[cfg['resolucao']]
    if altura:
        # Lanczos amplia sem recuperar detalhes ausentes do modelo neural.
        filtros.append('scale=-2:%d:flags=lanczos' % altura)
    if cfg['nitidez'] == 'suave':
        filtros.append('unsharp=5:5:0.35:5:5:0.0')
    elif cfg['nitidez'] == 'media':
        filtros.append('unsharp=5:5:0.65:5:5:0.0')
    command = [str(ffmpeg), '-hide_banner', '-loglevel', 'error', '-nostdin', '-y', '-i', str(origem)]
    if filtros:
        command += ['-vf', ','.join(filtros)]
    command += ['-r', str(cfg['fps']), '-c:v', 'libx264', '-preset', cfg['preset'], '-crf', str(cfg['crf']), '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', str(cfg['audio_kbps'])+'k', '-movflags', '+faststart', str(destino)]
    destino.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(command, check=True, timeout=timeout, capture_output=True, text=True)
    except Exception:
        destino.unlink(missing_ok=True)
        raise
    if not destino.is_file() or destino.stat().st_size == 0:
        raise RuntimeError('Exportacao nao produziu MP4')
    return destino


if __name__ == '__main__':
    import argparse, json
    p = argparse.ArgumentParser(description='Exportar MP4 com qualidade configuravel')
    p.add_argument('origem'); p.add_argument('destino'); p.add_argument('--opcoes', default='{}'); p.add_argument('--ffmpeg', default='ffmpeg')
    args = p.parse_args()
    print(exportar(args.origem, args.destino, json.loads(args.opcoes), args.ffmpeg))
