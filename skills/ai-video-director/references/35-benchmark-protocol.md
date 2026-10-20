# Benchmarks — como verificar se a skill melhora vídeos

Não dizer "vence todas as skills" sem uma comparação válida. Preparar ensaios com mesmo brief, assets canônicos, modelo, versões de geradores, créditos de geração, hardware, tempo, ferramentas, fontes, orçamento e direitos. Idealmente 2 ou mais repetições independentes por condição (com vs sem skill), em workspaces separados e prompts que não vazem a condição. Guardar hash de entradas e render outputs.

## Testes adversariais obrigatórios
- SaaS (UI real): remover tela falsa e preservar feature.
- App com mascote: testar consistência entre 6 planos, sem inventar redesenho.
- Motion tipográfico PT-BR: testar acentos, kerning, legibilidade mobile, pausa e gesto próprio.
- Filme de marca emotivo: verificar virada e associação de marca, não só trilha bonita.
- Ad de 6s: provar oferta com clareza e sem clickbait.
- Social 9:16 e master 16:9: redesenho nativo, não crop.
- AI T2V: continuidade temporal mãos/objetos/telas, falhas e plano de reshoot.
- Vídeo médico/fintech: alegações e direitos elevados, precisão antes de espetáculo.
- Documentário com humanos: consentimento e não falsificar depoimentos.
- Revisão de vídeo ruim: capacidade de consertar a raiz causal, não apenas adicionar efeitos.

## Avaliação
Painel de profissionais convidados, com condição cega e rubrica de 34-qa-scorecards.md. Separar métricas técnicas automáticas, compreensão de usuários, preferência artística, aderência à marca e medidas de marketing em campanha real. Para marketing, atribuição só com experimento viável, consentimento, períodos e amostras. Registrar **derrotas e casos mistos**, porque indicam defeitos reais na skill. Revisão feita pelo próprio agente é útil mas não é evidência independente.

## Stop condition
A versão é candidata a melhor se melhora média e pior caso, não introduz regressões P0/P1 e mantém custo/tempo viáveis. Uma prova estatística requer amostra suficiente; não inventar número de superioridade. Uma coleção de guias não substitui renderização de peças reais.
