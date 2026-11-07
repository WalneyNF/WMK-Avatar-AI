# WMK Avatar AI — Assistente com Rosto, instalacao e diagnostico (Windows)

**Repositorio:** https://github.com/WalneyNF/WMK-Avatar-AI

**Atualização de 07/11/2026:** um MP4 real foi gerado com sucesso; as afirmações abaixo de que o MP4 ainda não foi validado são histórico anterior. Para instalar em outro computador, consulte primeiro o [manual público atualizado de instalação, hardware e parâmetros](manuais/instalacao-publica.html).

**Documentacao organizada:** [abrir indice dos manuais](manuais/INDICE.md). O indice e os cinco guias separados sao a referencia atualizada; este arquivo preserva o historico de instalacao e diagnostico.

**Integracao e documentacao:** Walney Moreira Klein — walneyk@hotmail.com

Projeto derivado do SadTalker (OpenTalker); manter creditos e licencas do projeto original.

## Estado verificado em 07/11/2026

- Ollama local: API em http://127.0.0.1:11434, modelo qwen2.5-coder:3b testado com HTTP 200.
- Interface WMK: http://127.0.0.1:18765/ (servidor local em server.py).
- Texto para WAV: POST /api/voz testado, arquivo RIFF/WAV reproduzivel via GET /api/audio/arquivo.wav.
- PyTorch 2.0.1+cpu testado; execucao prevista em CPU (GPU de 2 GB).
- Modelos SadTalker 256 e dois mapeamentos baixados com sucesso.
- **Geracao de MP4 ainda NAO validada.** Nao anunciar como concluida antes de verificar o arquivo e o audio.

## Diretorios

- Codigo: D:\\Ferramentas\\SadTalker
- Python 3.8.20: .python\\cpython-3.8.20-windows-x86_64-none\\python.exe
- Ambiente: .venv\\Scripts\\python.exe
- Interface: wmk-assistente\\index.html
- Servidor: wmk-assistente\\server.py
- Voz Windows: wmk-assistente\\voz.ps1
- WAV: wmk-assistente\\resultados
- Pesos: checkpoints\\
- Cache uv: .cache\\uv (disco D:)

## Dependencias comprovadamente instaladas

| Biblioteca | Versao |
|---|---|
| Python | 3.8.20 |
| torch CPU | 2.0.1+cpu |
| torchvision CPU | 0.15.2+cpu |
| torchaudio CPU | 2.0.2+cpu |
| face-alignment | 1.3.5 |
| librosa | 0.9.2 |
| scipy | 1.10.1 |
| kornia | 0.6.8 |
| safetensors | 0.4.5 |
| opencv-python | 4.8.1.78 |
| facexlib | 0.3.0 |
| av | 12.3.0 |
| imageio-ffmpeg | 0.5.1 |
| numba | 0.58.1 |
| scikit-image | 0.21.0 |
| scikit-learn | 1.3.2 |
| tqdm | 4.70.1 |
| matplotlib | 3.7.5 |

Outras dependencias transitivas foram instaladas. Para obter a lista EXATA do ambiente, execute:

```bat
D:\\Ferramentas\\SadTalker\\.venv\\Scripts\\python.exe -m pip freeze
```

ATENCAO: pip nao foi instalado nesse venv criado pelo uv. Use `uv pip freeze --python D:\\Ferramentas\\SadTalker\\.venv\\Scripts\\python.exe` em seu lugar.

## Instalacao incremental no D:

```bat
cd /d D:\\Ferramentas\\SadTalker
set UV_CACHE_DIR=D:\\Ferramentas\\SadTalker\\.cache\\uv
set UV_LINK_MODE=copy
uv pip install --python .venv\\Scripts\\python.exe --only-binary :all: --no-deps librosa==0.9.2 face_alignment==1.3.5 safetensors==0.4.5 scipy==1.10.1 kornia==0.6.8
uv pip install --python .venv\\Scripts\\python.exe --only-binary :all: --no-deps opencv-python==4.8.1.78
uv pip install --python .venv\\Scripts\\python.exe --only-binary :all: tqdm imageio imageio-ffmpeg scikit-image scikit-learn numba soundfile pyyaml yacs einops av
uv pip install --python .venv\\Scripts\\python.exe facexlib==0.3.0
```

**Importante:** esses comandos documentam as correcoes realizadas, nao substituem a instalacao completa do projeto; usar ambiente virtual isolado e validar versoes antes de distribuir.

## Pesos baixados (origem: releases oficiais OpenTalker/SadTalker v0.0.2-rc)

- `SadTalker_V0.0.2_256.safetensors` — 725066984 bytes
- `mapping_00109-model.pth.tar` — 155779231 bytes
- `mapping_00229-model.pth.tar` — 155521183 bytes

Base: https://github.com/OpenTalker/SadTalker/releases/tag/v0.0.2-rc

## Erros diagnosticados e solucoes

1. `ModuleNotFoundError: librosa`: instalar librosa 0.9.2 e dependencias.
2. `ModuleNotFoundError: cv2`: instalar opencv-python 4.8.1.78.
3. `ModuleNotFoundError: tqdm`: instalar lote de processamento de imagem/video.
4. `ModuleNotFoundError: facexlib`: instalar facexlib 0.3.0.
5. Instalacao `uv pip install -r requirements.txt` sem progresso: foi encerrada e substituida por lotes menores; nao considerar o requirements original validado.
6. Porta 8765 ocupada: interface WMK passou a usar 18765.

## Verificacao

```bat
cd /d D:\\Ferramentas\\SadTalker
.venv\\Scripts\\python.exe inference.py --help
```

Para primeiro video, usar imagem facial REALISTA de exemplo, WAV curto e `--cpu --size 256`. Somente depois testar o robo WMK: detectores de rostos podem falhar em rostos metalicos ou estilizados.

## Pendencias

- Confirmar importacao completa do inference.py e resolver dependencias remanescentes.
- Confirmar modelos auxiliares de deteccao e reconstrução facial, se exigidos em execucao.
- Gerar e verificar MP4 real, duracao, sincronismo e reproducao.
- Integrar upload de avatar e botao de animacao na interface WMK.
- Criar manifesto completo do ambiente (`uv pip freeze`) e procedimento de instalacao automatizada apos primeiro teste bem-sucedido.
- Documentar licencas de modelos, software e componentes antes de publicar/distribuir.

**Regra de qualidade:** diferenciar 'baixado', 'instalado', 'testado' e 'funcionando'.
