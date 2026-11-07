# Instalação e dependências — Windows

**Walney Moreira Klein — walneyk@hotmail.com**

Projeto: `D:\Ferramentas\SadTalker`. Python 3.8.20 isolado em `.python/`, virtualenv `.venv/`, PyTorch 2.0.1+cpu, FFmpeg em `D:\ffmpeg\bin\ffmpeg.exe`. Pesos 256 em `checkpoints/`.

## Problemas diagnosticados

- `gfpgan==1.3.8` requer `basicsr>=1.4.2`; modo somente wheel falhou por BasicSR sem wheel.
- BasicSR tentou compilar `lmdb==2.1.1`; falhou por ausência de Microsoft Visual C++ 14+.
- Contorno aplicado com sucesso: `lmdb==1.4.1` (wheel), `basicsr==1.4.2 --no-deps`, `gfpgan==1.3.8 --no-deps`.
- `decorator==5.1.1` instalado após erro de importação no librosa.
- **Resolvido em 07/11/2026:** `pooch==1.8.2`, `audioread==3.0.1` e `resampy==0.4.3` instalados. `inference.py --help` executou com codigo 0. O teste de MP4 baixou pesos auxiliares, mas falhou na extracao facial: `AttributeError: module 'numpy' has no attribute 'float'` em `src/face3d/util/my_awing_arch.py`. Corrigir compatibilidade e repetir o teste.

## Comandos comprovados

```bat
set UV_CACHE_DIR=D:\Ferramentas\SadTalker\.cache\uv
set UV_LINK_MODE=copy
uv pip install --python D:\Ferramentas\SadTalker\.venv\Scripts\python.exe lmdb==1.4.1
uv pip install --python D:\Ferramentas\SadTalker\.venv\Scripts\python.exe --no-deps basicsr==1.4.2
uv pip install --python D:\Ferramentas\SadTalker\.venv\Scripts\python.exe --no-deps gfpgan==1.3.8
uv pip install --python D:\Ferramentas\SadTalker\.venv\Scripts\python.exe decorator==5.1.1
```

`--no-deps` instala sem verificar dependências transitivas: **não garante compatibilidade em execução**. Não instalar pacotes globais nem usar C: para cache.

## Diagnóstico

```bat
cd /d D:\Ferramentas\SadTalker
.venv\Scripts\python.exe inference.py --help
uv pip check --python .venv\Scripts\python.exe
```
