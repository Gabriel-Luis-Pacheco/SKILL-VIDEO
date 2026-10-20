# Video OS Prime 4.0

**Direção criativa, motion, cinema, publicidade e engenharia de vídeo com IA — em uma skill.**

Criada para desenvolver **vídeos originais completos**, não apenas roteiros ou slides animados: anúncios de performance, filmes emocionais de marca, lançamentos de SaaS, demonstrações reais, motion graphics 2D/3D, personagens, trailers, conteúdo social, explainer e filmes experimentais.

> Objetivo: aplicar o rigor de grandes diretores criativos, motion studios, editores, estrategistas de marca e profissionais de marketing/vendas, sem copiar trabalhos alheios. Uma skill ou ferramenta não substitui talento, ativos reais, julgamento humano nem recursos de produção.

## Instalar

```bash
npx skills add Gabriel-Luis-Pacheco/SKILL-VIDEO --skill ai-video-director
```

Ou copie `skills/ai-video-director` para o diretório de skills do seu agente. **Ponto de entrada:** [SKILL.md](skills/ai-video-director/SKILL.md). Os módulos de apoio são carregados somente quando a tarefa os exige.

## O princípio que guia tudo

**Entender a marca → descobrir uma ideia única → criar um acontecimento visual → dirigir a progressão → escolher ferramenta por cena → fazer animatic → produzir o filme inteiro → montar e sonorizar → exportar → assistir/escutar → corrigir a falha principal → medir resultados reais.**

Uma grande abertura não salva uma parte central vazia. Um vídeo tecnicamente perfeito não é automaticamente memorável. Um anúncio que ganhou cliques não é necessariamente uma campanha de marca eficaz. E uma ideia excelente não precisa de todos os efeitos ou de um modelo generativo para cada cena.

## O que mudou na versão 4.0

| Frente | Implementação |
|---|---|
| **Brand + growth** | [62 — Memória de marca e resposta direta](skills/ai-video-director/references/62-brand-memory-and-direct-response.md): emoção, personagens, demonstração, objeções e CTA, conforme objetivo |
| **Montagem e som** | [63 — Edição, som e acabamento](skills/ai-video-director/references/63-world-class-editing-sound-playbook.md): roteiro de assembly → narrative → motion → sound → polish |
| **Motion/3D/personagens** | [64 — Direção de animação](skills/ai-video-director/references/64-motion-3d-and-character-craft.md): massa, gestos, rig, câmera, luz, material e acting |
| **Avaliação e aprendizado** | [65 — Creative Learning Loop](skills/ai-video-director/references/65-creative-quality-control-and-learning-loop.md): defeitos P0/P1/P2, correção causal e testes comparativos |
| **Decisão de produção** | [brief_router.py](skills/ai-video-director/scripts/brief_router.py): objetivos, ferramentas apropriadas, bloqueios de verdade/rights |
| **Métricas comerciais** | [campaign_results.py](skills/ai-video-director/scripts/campaign_results.py): relatório descritivo, taxas/custos e intervalos informativos, sem vitória causal inventada |
| **Revisão criativa** | [independent_review.py](skills/ai-video-director/scripts/independent_review.py): observações cronometradas, distinção entre agente e avaliador humano e bloqueios críticos |
| **Projetos editáveis** | [new_video_project.py](skills/ai-video-director/scripts/new_video_project.py): inicia projeto seguro, com pastas, brief, storyboard e manifesto vazios em vez de dados inventados |
| **Diagnóstico de mídia** | [signal_qc.py](skills/ai-video-director/scripts/signal_qc.py) analisa quadros pretos, holds e trechos silenciosos reais sem confundir arte com erro técnico |
| **Entregas nativas** | Verificador de mídia agora aceita 9:16, 4:5, 1:1 e 16:9 e expõe metadata de cor/áudio |
| **Tecnologias atuais** | [66 — Modelos e ferramentas disponíveis](skills/ai-video-director/references/66-current-tool-capabilities.md), incluindo a descontinuação do Sora como produto em abril/2026 |
| **Pesquisa de referência** | Google ABCD + System1/Aardman + pesquisa 2026 de Orlando Wood e identidade de marca; ver [fontes](docs/SOURCE_MATRIX.md) |

Tudo é **original**, inspirado em princípios verificáveis e trabalho de referência, sem copiar roteiros completos, cenas exatas, marcas ou trilhas.

## Biblioteca

- [24 roteiros originais com 102 beats cronometrados](skills/ai-video-director/examples/original-script-vault.md)
- [Atlas crítico de 16 campanhas](skills/ai-video-director/references/30-campaign-atlas.md), incluindo Volvo, Nike, Dove, Old Spice, OpenAI e Duolingo
- [Comparação técnica de 10 skills externas](skills/ai-video-director/references/44-top-10-skills-comparison.md)
- [Motion system, timing e cinematografia](skills/ai-video-director/references/INDEX.md)
- [Roteiro de produção e QA](docs/PRODUCTION_RUNBOOK.md)
- [Prompts prontos para produção](docs/AGENT_PROMPTS.md)

## Começar um vídeo novo

```bash
python skills/ai-video-director/scripts/new_video_project.py \
  --out ./meu-video --title "Meu Comercial" --brand "Minha Marca" \
  --goal conversion --surface reels

python skills/ai-video-director/scripts/brief_router.py \
  skills/ai-video-director/fixtures/brief_synthetic.json

python skills/ai-video-director/scripts/timeline_compile.py \
  skills/ai-video-director/fixtures/storyboard.json

python skills/ai-video-director/scripts/campaign_results.py \
  skills/ai-video-director/fixtures/campaign_results_synthetic.json
```

**Atenção:** os exemplos de métricas e revisões são **fictícios para testes**, não prova de resultado comercial. O scaffold é um projeto vazio, **não** um filme pronto.

## Renderização real e testes

A pasta [Motion Film Lab](skills/ai-video-director/examples/rendered-proof/README.md) contém um gerador autoral de vídeo de sete segundos com som procedural. O GitHub Actions renderiza MP4 real, testa metadados, captura frames, produz contact sheet e guarda um artefato de prova de engenharia temporário.

```bash
python -m unittest discover -s tests -v
python skills/ai-video-director/scripts/validate.py
python skills/ai-video-director/examples/rendered-proof/render.py \
  --output /tmp/motion-os.mp4 --width 540 --height 960 --fps 30
python skills/ai-video-director/scripts/video_qc.py \
  /tmp/motion-os.mp4 --duration 7 --aspect 9:16 --require-audio
python skills/ai-video-director/scripts/evidence_capture.py \
  /tmp/motion-os.mp4 --out /tmp/motion-review
```

Requisitos do laboratório: Python, Pillow e FFmpeg instalado. As ferramentas de revisão não geram qualidade artística automaticamente: assistir e escutar o arquivo final continua indispensável.

## O que NÃO está comprovado

Não executamos uma bateria independente e cega de vídeos produzidos **com e sem** a skill. Não há evidência de que este sistema seja literalmente "o melhor do mundo", gere vendas superiores ou atinja o nível de produção de grandes estúdios em qualquer orçamento. [Limitações e próximos critérios de prova](docs/KNOWN_LIMITATIONS.md).

**Licença:** MIT. Faça bom uso, preserve a marca real e deixe o filme falar por si.
