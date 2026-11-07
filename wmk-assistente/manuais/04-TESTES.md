# Testes e evidências

**Walney Moreira Klein — walneyk@hotmail.com**

| Item | Resultado | Evidência |
|---|---|---|
| GET / | OK | Interface atualizada retornada |
| GET /api/avatares | OK | Resposta `{"avatares":[]}` |
| Upload real de imagem | PENDENTE | Ainda sem teste ponta a ponta |
| Chat Ollama | OK anterior | Resposta HTTP 200 com modelo local |
| Gerar WAV | OK anterior | Arquivo WAV RIFF válido |
| BasicSR/GFPGAN | INSTALADOS | Instalação terminou com código 0 |
| inference.py --help | FALHOU | Falta `pooch` |
| MP4 do SadTalker | PENDENTE | Não existe geração comprovada |
| Publicação desta revisão | PENDENTE | Requer commit e push |

## Critérios de conclusão

1. `inference.py --help` deve sair com código 0.
2. Rodar foto frontal + WAV usando CPU e modelo 256.
3. Verificar MP4 não vazio com FFprobe.
4. Reproduzir e avaliar a sincronização.
5. Integrar a geração na interface com progresso, erros e download.

Não confundir biblioteca instalada com pipeline validado.
