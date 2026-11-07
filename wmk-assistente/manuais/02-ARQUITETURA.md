# Arquitetura do WMK

**Walney Moreira Klein — walneyk@hotmail.com**

```text
Navegador/index.html
 |-- /api/chat --> server.py --> Ollama:11434
 |-- /api/voz --> server.py --> voz.ps1 --> Windows SAPI --> WAV
 |-- /api/avatares --> server.py --> pasta avatares/
 |-- /api/avatar/* --> imagem cadastrada
 +-- FUTURO: avatar + WAV --> inference.py/SadTalker --> MP4
```

`server.py` é API HTTP local (127.0.0.1:18765); `index.html` é a interface; `voz.ps1` gera áudio; `resultados/` contém WAV; `avatares/` contém imagens; `checkpoints/` contém pesos; `.venv/` contém bibliotecas; `inference.py` é o pipeline original SadTalker.

**Segurança:** servidor local, não exposto publicamente; upload limita tamanho e confere assinaturas básicas, mas isso não substitui análise completa de arquivo. Não publicar fotos pessoais, pesos, WAV, vídeos nem ambiente virtual. Preservar atribuições e licenças originais do SadTalker.
