# WMK Avatar AI — Plataforma de Avatares Inteligentes (base SadTalker)

**Repositorio oficial WMK:** https://github.com/WalneyNF/WMK-Avatar-AI

**Guia público de instalação e hardware:** [Instalar, configurar e entender parâmetros (HTML)](wmk-assistente/manuais/instalacao-publica.html). **Central de manuais:** [Índice HTML](wmk-assistente/manuais/index.html). **Histórico técnico:** [Índice Markdown](wmk-assistente/manuais/INDICE.md). A plataforma WMK utiliza o motor SadTalker original, com os creditos e licencas preservados.

> **Projeto original:** [OpenTalker/SadTalker](https://github.com/OpenTalker/SadTalker)  
> **Fork e integracao WMK:** [WalneyNF/WMK-Avatar-AI](https://github.com/WalneyNF/WMK-Avatar-AI)  
> **Integracao, traducao e documentacao:** Walney Moreira Klein — walneyk@hotmail.com  
> **README original em ingles:** [README.original.en.md](README.original.en.md)

![Demonstracao do SadTalker](https://user-images.githubusercontent.com/4397546/222490039-b1f6156b-bf00-405b-9fda-0c9a9156f991.gif)

**Em poucas palavras:** uma fotografia ou imagem de rosto + um arquivo de audio = um video com o rosto falando.

O SadTalker gera movimentos faciais e de cabeca a partir de uma imagem e um audio. Foi apresentado na CVPR 2023. Leia o [artigo cientifico](https://arxiv.org/abs/2211.12194) e visite a [pagina do projeto](https://sadtalker.github.io).

## 1. Destaques

- Licenca do codigo atualizada para **Apache 2.0**, conforme README original. Confira separadamente as licencas dos modelos, arquivos e dependencias.
- Animacao de retratos, imagens inteiras e personagens, sujeita a deteccao facial.
- Modos de imagem parada (`--still`), referencia e redimensionamento.
- Opcao de aprimoramento de rosto com GFPGAN (requer pesos adicionais).
- Demonstracoes: [Hugging Face](https://huggingface.co/spaces/vinthony/SadTalker), [Google Colab](https://colab.research.google.com/github/Winfredy/SadTalker/blob/main/quick_demo.ipynb) e [Discord](https://discord.gg/rrayYqZ4tf).
- Integracao comunitaria com [Stable Diffusion WebUI](docs/webui_extension.md).

## 2. O que existe neste fork WMK

Este fork esta sendo preparado para um **assistente com rosto**:

1. O usuario escreve uma pergunta.
2. O Ollama gera a resposta.
3. O Windows sintetiza um arquivo WAV em portugues.
4. O SadTalker recebe uma imagem e esse WAV para gerar um MP4 animado.
5. Futuramente, a interface podera exibir o avatar e reproduzir o video.

**Estado verificado em 07/11/2026:** Ollama e WAV funcionando; pesos de 256 px instalados; MP4 real gerado com 105 quadros (Face Renderer 1h07min32s em CPU). Estúdio, monitor e biblioteca implementados; nove testes automatizados passaram. Instalação limpa em outra máquina e CUDA ainda não foram validadas.

Acesse a documentacao de instalacao especifica desta maquina em [wmk-assistente/README-PTBR.md](wmk-assistente/README-PTBR.md).

## 3. Instalacao no Windows

### Requisitos

- Windows 10/11;
- Git;
- Python 3.8 (a versao usada neste ambiente e 3.8.20);
- FFmpeg para codificacao e manipulacao de audio/video;
- Dependencias Python do projeto;
- Pesos dos modelos na pasta `checkpoints/`.

O projeto original sugere instalar Python 3.8, Git e FFmpeg, clonar o repositorio, baixar os modelos e executar a interface Gradio com `start.bat` ou `webui.bat`, conforme a versao.

### Instalacao classica (referencia do projeto original)

```bat
git clone https://github.com/WalneyNF/WMK-Avatar-AI.git
cd SadTalker
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Atencao:** o arquivo `requirements.txt` original pode exigir ajustes de versoes e pacotes no Windows. O procedimento acima e de referencia, NAO foi validado integralmente nesta maquina. Para o historico real de instalacao no disco D:, use o [manual WMK](wmk-assistente/README-PTBR.md).

### Instalacao realizada no computador WMK

Diretorio: `D:\Ferramentas\SadTalker`

Ambiente Python: `.venv\Scripts\python.exe`

PyTorch instalado e testado: `2.0.1+cpu`. Esta configuracao evita depender da GPU de 2 GB.

Para inspecionar a instalacao:

```bat
cd /d D:\Ferramentas\SadTalker
.venv\Scripts\python.exe -c "import torch; print(torch.__version__)"
uv pip freeze --python .venv\Scripts\python.exe
.venv\Scripts\python.exe inference.py --help
```

Se `inference.py --help` falhar, consulte o manual WMK para o diagnostico das dependencias.

## 4. Instalacao no Linux / Unix

Procedimento historico do projeto original:

```bash
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
conda create -n sadtalker python=3.8
conda activate sadtalker
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
conda install ffmpeg
pip install -r requirements.txt
```

Esse comando PyTorch usa CUDA 11.3 e **nao** e apropriado para todas as GPUs ou maquinas sem NVIDIA. Adapte ao hardware. O Coqui TTS era opcional na demonstracao Gradio (`pip install TTS`).

Para macOS, Docker e WSL, consulte [docs/install.md](docs/install.md). Esses ambientes nao foram testados neste fork.

## 5. Download dos modelos

No Linux/macOS, o projeto original oferece:

```bash
bash scripts/download_models.sh
```

Downloads oficiais: [GitHub Releases](https://github.com/OpenTalker/SadTalker/releases) | [Google Drive](https://drive.google.com/file/d/1gwWh45pF7aelNP_P78uDJL8Sycep-K7j/view?usp=sharing) | [Baidu](https://pan.baidu.com/s/1kb1BCPaLOWX1JJb9Czbn6w?pwd=sadt) (senha `sadt`).

### Pesos atuais

| Arquivo | Funcao |
|---|---|
| `checkpoints/SadTalker_V0.0.2_256.safetensors` | Pesos agrupados para animacao em 256 px |
| `checkpoints/SadTalker_V0.0.2_512.safetensors` | Modelo alternativo de 512 px |
| `checkpoints/mapping_00109-model.pth.tar` | Rede de mapeamento de movimentos |
| `checkpoints/mapping_00229-model.pth.tar` | Rede de mapeamento de movimentos |
| `gfpgan/weights/` | Pesos de deteccao, alinhamento e aprimoramento facial |

**Baixados e verificados neste computador:** modelo 256 e ambos os mapeamentos. O modelo 512 e os pesos opcionais do GFPGAN nao foram confirmados como instalados.

### Modelos legados

A versao antiga utilizava arquivos separados: `auido2exp_00300-model.pth`, `auido2pose_00140-model.pth`, `facevid2vid_00189-model.pth.tar`, `epoch_20.pth`, `wav2lip.pth`, `shape_predictor_68_face_landmarks.dat`, alem das pastas `BFM` e `hub`. Normalmente, prefira os pesos agrupados da versao atual, salvo quando `--old_version` for necessario.

## 6. Primeiro uso

### Interface grafica do projeto original

```bat
python app_sadtalker.py
```

Ou execute `webui.bat` no Windows, quando as dependencias da interface estiverem instaladas. No Linux/macOS: `bash webui.sh`. A interface original usa Gradio.

### Linha de comando: animar um rosto

Exemplo simples, sem aprimoramento adicional:

```bat
cd /d D:\Ferramentas\SadTalker
.venv\Scripts\python.exe inference.py --driven_audio examples\driven_audio\bus_chinese.wav --source_image examples\source_image\full_body_1.png --cpu --size 256
```

**Este e um comando de teste sugerido; ainda nao foi confirmado que ele gera MP4 nesta instalacao.** A pasta de resultados e normalmente `results/`, com subpastas por execucao.

Com aprimoramento facial, depois de instalar os modelos adicionais:

```bash
python inference.py --driven_audio audio.wav --source_image rosto.png --enhancer gfpgan
```

Para animar uma imagem completa:

```bash
python inference.py --driven_audio audio.wav --source_image personagem.png --still --preprocess full
```

Use `python inference.py --help` para consultar todos os parametros. Veja [boas praticas](docs/best_practice.md).

## 7. Assistente WMK — gerar voz

Abra a interface local em [http://127.0.0.1:18765/](http://127.0.0.1:18765/) **com o servidor em execucao**.

O painel permite escrever texto, gerar um WAV, ouvir e salvar o arquivo. Os WAVs sao armazenados em `wmk-assistente/resultados/`. O servidor escuta apenas em `127.0.0.1`, nao e um servico publico.

A integracao completa WAV → SadTalker → MP4 permanece em desenvolvimento. O primeiro teste real em CPU falhou em `np.float` removido do NumPy moderno; consulte [testes](wmk-assistente/manuais/04-TESTES.md).

## 8. Solucao de problemas

| Sintoma | Verificacao ou correcao |
|---|---|
| `No module named 'librosa'` | Instalar a versao compativel com Python 3.8 (neste ambiente: 0.9.2) |
| `No module named 'cv2'` | Instalar `opencv-python` (testado: 4.8.1.78) |
| `No module named 'tqdm'` | Instalar `tqdm` e demais dependencias de processamento |
| `No module named 'facexlib'` | Instalar `facexlib` (testado: 0.3.0) |
| Download de dependencias sem progresso | Verificar rede, cache, espaco livre e processos concorrentes |
| Rosto nao detectado | Testar primeiro uma fotografia frontal realista e boa iluminacao |
| GPU sem memoria | Utilizar `--cpu --size 256`; o processamento pode ser lento |
| FFmpeg nao encontrado | Instalar FFmpeg e verificar `ffmpeg -version` |
| Falta de pesos | Conferir `checkpoints/` e os arquivos auxiliares exigidos |

Consulte tambem a [FAQ original](docs/FAQ.md) e o [registro de alteracoes](docs/changlelog.md).

## 9. Historico do projeto original

- **12/06/2023:** melhorias na extensao WebUI.
- **05/06/2023:** modelo facial experimental de 512 × 512 px e correcoes.
- **15/04/2023:** novo notebook Colab para WebUI.
- **12/04/2023:** documentacao de instalacao WebUI, seguranca e melhorias de caminhos.
- **08/04/2023:** recursos de animacao de imagem completa e aprimoramento facial. Uma marca d'agua adicionada nessa versao foi removida posteriormente.

Acompanhe as [discussoes](https://github.com/OpenTalker/SadTalker/discussions/386) e [pendencias](https://github.com/OpenTalker/SadTalker/issues/280) originais.

## 10. Referencia cientifica

Se utilizar o SadTalker em pesquisa, cite o trabalho original:

```bibtex
@article{zhang2022sadtalker,
  title={SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation},
  author={Zhang, Wenxuan and Cun, Xiaodong and Wang, Xuan and Zhang, Yong and Shen, Xi and Guo, Yu and Shan, Ying and Wang, Fei},
  journal={arXiv preprint arXiv:2211.12194},
  year={2022}
}
```

Autores originais: Wenxuan Zhang, Xiaodong Cun, Xuan Wang, Yong Zhang, Xi Shen, Yu Guo, Ying Shan e Fei Wang. Instituicoes mencionadas na publicacao incluem Xi'an Jiaotong University, Tencent AI Lab e Ant Group.

## 11. Agradecimentos e projetos relacionados

A implementacao original aproveita trabalhos de [face-vid2vid](https://github.com/zhanglonghao1992/One-Shot_Free-View_Neural_Talking_Head_Synthesis), [PIRender](https://github.com/RenYurui/PIRender), [Deep3DFaceReconstruction](https://github.com/microsoft/Deep3DFaceReconstruction) e [Wav2Lip](https://github.com/Rudrabha/Wav2Lip).

Bibliotecas relacionadas: [facexlib](https://github.com/xinntao/facexlib), [GFPGAN](https://github.com/TencentARC/GFPGAN) e [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN).

Extensao comunitaria: [SadTalker-Video-Lip-Sync](https://github.com/Zz-ww/SadTalker-Video-Lip-Sync).

Outras pesquisas relacionadas: [StyleHEAT](https://github.com/FeiiYin/StyleHEAT), [CodeTalker](https://github.com/Doubiiu/CodeTalker), [VideoReTalking](https://github.com/vinthony/video-retalking), [DPE](https://github.com/Carlyx/DPE), [3D GAN Inversion](https://github.com/FeiiYin/SPI/) e [T2M-GPT](https://github.com/Mael-zys/T2M-GPT).

## 12. Licencas, privacidade e uso responsavel

**O SadTalker nao e um produto oficial da Tencent.**

Antes de usar ou distribuir, leia a licenca do codigo e as declaracoes de propriedade intelectual dos modelos e recursos. A licenca do codigo nao implica necessariamente licenca irrestrita sobre todos os modelos, imagens e audios.

O projeto original informa que seu codigo aberto pode funcionar offline e nao coleta dados pessoais por conta propria. **Essa declaracao nao abrange automaticamente integracoes adicionadas ao fork**, como Ollama, APIs, interfaces web ou servicos de terceiros. Se um produto coletar dados, o responsavel devera observar a legislacao aplicavel, inclusive a LGPD no Brasil, publicar informacoes de privacidade e obter consentimentos quando exigidos.

Nao use imagens ou vozes de pessoas sem autorizacao adequada. Sao proibidos usos para fraude, personificacao enganosa, violacao de direitos de imagem, reputacao, disseminacao ilegal de conteudo ou outras condutas ilicitas. Nao utilize marcas ou logotipos de terceiros como se houvesse endosso oficial.

Os direitos das imagens e dos audios de demonstracao pertencem aos respectivos titulares, conforme informado pelo projeto original.

---

**Creditos da integracao e documentacao em portugues:** Walney Moreira Klein — walneyk@hotmail.com.

**Preservacao de autoria:** o SadTalker foi criado pelos autores originais citados acima. Este fork acrescenta integracoes, testes e documentacao; nao reivindica a autoria do modelo original.
