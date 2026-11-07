# Próximas etapas

**Walney Moreira Klein — walneyk@hotmail.com**

## P0 — Motor de vídeo

- [x] Instalar `pooch`, `audioread`, `resampy` e confirmar inicializacao do `inference.py --help`.
- [ ] Conferir `uv pip check`.
- [ ] Corrigir incompatibilidade `np.float` em `src/face3d/util/my_awing_arch.py`.
- [ ] Repetir teste SadTalker CPU 256 com WAV e foto; tentativa anterior falhou na extracao facial.
- [ ] Validar MP4 e sincronização.

## P1 — WMK

- [x] Interface de chat, WAV e seleção de avatar.
- [x] Cadastro de avatar implementado (falta teste com imagem real).
- [x] Créditos no cabeçalho.
- [ ] Renomear/excluir avatares com confirmação.
- [ ] Gerar vídeo com avatar escolhido, fila, progresso, logs e download.
- [ ] Enquadramento/zoom do rosto sem alterar original.

## P2 — Qualidade e publicação

- [ ] Testar rosto humano e robô WMK (detector pode falhar no robô).
- [ ] Melhorar naturalidade e sincronia labial.
- [ ] Criar testes automatizados.
- [ ] Revisar `.gitignore`, licenças e README.
- [ ] Commit, push e conferência do GitHub.
