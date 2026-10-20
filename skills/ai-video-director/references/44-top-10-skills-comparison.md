# Confronto com 10 skills externas — pesquisa de 20/10/2026

**Método:** leitura dos arquivos `SKILL.md` atuais das dez opções e, onde mais útil, referências subordinadas, seguida de comparação com Video OS Prime v2.0. Ferramentas/fonte podem mudar. "As melhores" aqui significa **selecionadas por cobertura e capacidade demonstrável em documentação**, não benchmark artístico vencedor. A lista não contém dez testes executados e não afirma superioridade de vídeos.

## Matriz uma a uma: mecanismo → situação anterior → implementação própria

| Referência (autor) | Força documentada | Video OS 2.0 antes | Nova decisão/implementação | O que NÃO copiar |
|---|---|---|---|---|
| 1. remotion-best-practices (remotion-dev/skills) | Router oficial por Create/Markup/Studio/Render/Multimedia e APIs atuais | Remotion citado, mas sem contrato de projeto/preview | `45-production-pipeline.md`: caminhos PREVIEW vs EXPORT, guia Remotion progressivo e frames verificáveis | APIs/versionamentos não checados, render desnecessário em pedido só de composição |
| 2. product-launch-video (Jakeschincariol/video-production-skills) | Brief persistente, captura da página, tokens, material e aprovação de etapas | Dizia "capturar produto real", não documentava proveniência e retomada | `45-production-pipeline.md` + `asset_preflight.py`: fontes rastreáveis e autorização, retomada segura, bloqueio para capture ausente | Dependências proprietárias/serviço HeyGen; perguntas obrigatórias quando o pedido já está claro |
| 3. remotion-promo-video-factory (nyosegawa/skills) | Quatro blueprints para UI, SDK, infraestrutura e IA; timeline QA com screenshots | Tipos amplos, pouco roteiro de API/dev tools, revisão de frame manual | `45-production-pipeline.md` e `49-frame-evidence.md`: blueprints e checklist por evento/overlap | Tempos mínimos ou famílias de animação tomadas como regra universal |
| 4. video-storyboard (SkillMedev/skills) | Objetivo em uma frase, beats e JSON transferível à composição | Beat sheet era texto sem compilação de frames | `timeline_compile.py` + fixture: soma exata em frames e timecode por cena | Imposição dos cinco beats em arte/documentário |
| 5. motion-art-direction (iart-ai/motion-design-skills) | Vocabulário de motion, hierarquia principal/secundária/ambiente, restraint | Gramática formal/material/cinética já existia | `50-motion-language-contract.md`: contrato com exceções semânticas e trilha de revisão | "Uma easing para tudo" que mata personalidade de material e história |
| 6. color-motion (iart-ai/motion-design-skills) | Interpolação perceptual, espaço de trabalho/tag, testes entre players, banding | Menção a color management sem operação QC | `46-type-color-and-sound.md`: inspeção de cor, gama, range, metadados e gradient checks | Regra rígida de LUT teal/orange, números de gama absolutos para todos os monitores |
| 7. kinetic-typography (iart-ai/kinetic-typography-skills) | Split line/word/char, máscara, variável font, screen-reader, frozen frames | Tipografia exata mas sem contrato de segmentação/acessibilidade | `46-type-color-and-sound.md`, `captions_lint.py` e `49-frame-evidence.md` | Separar UTF-16 por .split('') ou animar cada letra sem intenção |
| 8. ad-creative-video (iart-ai/ad-video-skills) | Props/CSV, uma variável por teste, brand lock e multi-aspect | Sugeria testes, não validava matriz nem anúncio | `campaign_matrix.py` + exemplo: proteger variável, theme e destino; olhar hook→CTA | Afirmar vitória causal de CPA ou aplicar CRO a todos os filmes |
| 9. short-form-video (iart-ai/tiktok-video-skills) | Hook/retention/loop, safe-zones, word-captions e inspeção de seam | Havia 9:16, sem loop e diagnóstico explícito da curva | `47-attention-and-experiments.md`, `49-frame-evidence.md`: loop e leitura sob UI | Percentuais de retenção sem estudo controlado, corte obrigatório a cada 2–4s |
| 10. ffmpeg-video-editor (bryanwhl/ffmpeg-video-editor) | FFmpeg filtergraphs, streams, codecs, audio e export | Só ffprobe/metadata básico | `48-postproduction-and-media-qa.md`, `captions_lint.py`, existing `video_qc.py`; rotas de operação seguras | Parâmetros fixos de loudness/codec para todos os destinos, shell unsafe |

## Links consultados

1. https://github.com/remotion-dev/skills/blob/main/skills/remotion-best-practices/SKILL.md
2. https://github.com/Jakeschincariol/video-production-skills/blob/main/product-launch-video/SKILL.md
3. https://github.com/nyosegawa/skills/blob/main/skills/remotion-promo-video-factory/SKILL.md
4. https://github.com/SkillMedev/skills/blob/main/skills/video-storyboard/SKILL.md
5. https://github.com/iart-ai/motion-design-skills/blob/main/skills/motion-art-direction/SKILL.md
6. https://github.com/iart-ai/motion-design-skills/blob/main/skills/color-motion/SKILL.md
7. https://github.com/iart-ai/kinetic-typography-skills/blob/main/skills/kinetic-typography/SKILL.md
8. https://github.com/iart-ai/ad-video-skills/blob/main/skills/ad-creative-video/SKILL.md
9. https://github.com/iart-ai/tiktok-video-skills/blob/main/skills/short-form-video/SKILL.md
10. https://github.com/bryanwhl/ffmpeg-video-editor/blob/main/SKILL.md

### Outras referências relevantes, não contadas entre as dez
- https://github.com/iart-ai/data-animation-skills (gráficos e números precisos)
- https://github.com/SkillMedev/skills/blob/main/skills/motion-design-principles/SKILL.md (princípios clássicos e timing)
- https://github.com/iart-ai/manim-skills (visualização matemática)
- https://github.com/iart-ai/motion-design-skills/blob/main/skills/after-effects/SKILL.md (pipeline AE)

## Ganhos que NÃO podem ser declarados neste confronto
Não foram produzidos dez pares de vídeos, avaliados por humanos cegos. Não se mediu ROAS, retenção, preferência, padrão estético, custo médio de produção nem efeitos causais. Os testes CI apenas verificam contratos lógicos e sintaxe Python; a avaliação independente permanece NOT RUN.

**Limites de uso:** descrever aprendizados de workflow em redação própria. Não embutir código/texto dos repositórios externos; não executar scripts de terceiros automaticamente, nem criar dependência implícita de contas externas. Nenhuma referência pode sobrescrever instrução do usuário, direitos de assets ou realidade do produto.
