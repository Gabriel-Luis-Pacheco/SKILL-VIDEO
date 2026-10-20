# Production runbook — do briefing ao master

## 0. Contra o overplanning
Se ferramentas e ativos são suficientes e a tarefa pede filme: criar **primeiro corte real** antes de dezenas de documentos. Um roteiro excelente não equivale a obra pronta.

## 1. Truth & direction
Inspecionar marca, produto, consumidor, restrição, canal, direitos e objetivo. Escolher mecanismo do atlas e compará-lo com um concorrente criativo realmente diferente. A decisão de produção depende da evidência: software → gravação real; explicação diagramática → motion determinístico; mundo imaginário → 3D ou I2V; filme humano → filmagem consentida.

## 2. Previz e timeline
Escrever logline e beat sheet. Escolher FPS, duração e versões. Anotar timing e source de cada plano no JSON de fixtures; rodar shotlist_lint. Gerar quadro-chave para abertura, meio, payoff, final. Montar animatic (mesmo com stills) e sonorização preliminar para observar ritmo e comprimento.

## 3. Production
Dividir asset por tipo: real footage / capture UI / SVG fonts / rig / 3D / approved generated shot. Travar identidade por source e exportar stems. Prompt de I2V fala de movimento; T2V de cena + movimento. Depois do take, inspecionar 0%,25%,50%,75%,100% da duração, bordas e continuidade; descartar take que deforma pessoa, logo ou UI. Produzir camadas de typography determinística por cima, e não confiar em lettering do gerador.

## 4. Post
Organizar montagem por ação, não efeitos. Controlar coloração, sem overgrading, de cada fonte. Foley, ambiência, voz e música em stems. Audição mono/celular/fones, e revisão mute. Exportar master e layouts redimensionados **por nova composição**, não crop automático sem QA.

## 5. Gates
- P0: false claims/licença/consentimento/PII.
- P1: não há filme inteiro, identidade errada, falha de narrativa, texto ilegível, áudio ininteligível.
- P2: sombra/timing/kerning/pequena polidez.
Reparar o problema mais importante e rerenderizar. Só declarar dimensões técnicas PASS após ffprobe; declarar craft PASS apenas após revisão efetiva. Para anúncios, decidir experimentos posteriores isolando hook/prova/oferta e sem fabricar ROI.

## 6. Checklist de entrega
MP4/MOV verificado, master, derivativos, legendas, fonte editável, assets canônicos, manifest e direitos, frame de thumb, notes de fontes, report PASS/FAIL/UNKNOWN e hipótese de melhoria restante. Se alguma ferramenta ausente, separar claramente o que ficou NOT RENDERED.

## Version 3.0 — release evidence required

For `PRODUCE` and `EXPORT`, separate **conceptual pre-production**, **real rendered cut**, **technical checks** and **creative sign-off**. The reproducible sample in `examples/rendered-proof/` proves that image and generated audio can be muxed. That example is intentionally fictional; never reuse it as a real customer testimonial, product feature or brand asset.

**Preflight:** exact offer/product behavior, brand assets, target surface, medium decision per shot, timeline and asset rights. **Creative proof:** opening + middle + climax + end, sound and material signature. **Technical proof:** original compiled timeline, actual encoded output, measured fps/duration/aspect, caption structure, source assets. **Visual evidence:** use `scripts/evidence_capture.py` to see real frames. **Final review:** watch and listen to the film; a contact sheet or ffprobe alone never certifies smoothness or artistic intent.

On model-generated shots use `references/59-generative-shot-supervision.md` to decide accept/reshoot/rig replacement, not unlimited regenerate. On poor results change the weakest causal layer, reexport, inspect the new master and report remaining unknowns.

In CI, install FFmpeg and Pillow for the demonstration render. For actual user deliveries, preserve readable source, license information, canonical fonts/assets, and a non-fabricated QA ledger.
