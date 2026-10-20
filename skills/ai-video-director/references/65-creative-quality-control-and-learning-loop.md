# Creative Learning Loop — melhor resultado com evidência, não com aprovação automática

## 1. Quatro vozes para a crítica
**Diretor de cinema**: atenção, mise-en-scène, arco, tensão e payoff.
**Motion supervisor**: massa, spacing, composição, hierarquia, preservação de shape/character.
**Sound designer/editor**: cortes, silêncios, material, mix, continuidade.
**Brand / growth / sales**: veracidade, distintividade, desejo, objeção, caminho de ação e compatibilidade da landing.
Isso NÃO significa fingir quatro avaliadores externos: são perspectivas de uma revisão do agente. Avaliação independente requer pessoas diferentes, método cego e arquivos observados.

## 2. Ordem de reparo
P0: direito/consentimento/identidade/fato falso; bloquear.
P1: ideia errada, falta cena central, som importante incompreensível, versão errada, produto impossível de reconhecer; refazer.
P2: timing local, acabamento, fonte, grade, som de detalhe; polir.
Uma cena inteira de "text animation" quando precisava demonstrar a experiência é problema de conceito, não ajuste de easing.

## 3. Evidence ledger
Após render, cada observação inclui `file_sha256`, timecode, expected/observed, audio listened?, screenshots do frame, severidade, owner, correção e estado. `scripts/evidence_capture.py` prepara quadros reais, mas a qualidade visual permanece UNKNOWN sem observação. A crítica deve reconhecer limitações de voz, cor e movimentos impossíveis de perceber no still.

## 4. Provar eficácia criativa sem cair em estatística de marketing
`scripts/independent_review.py` organiza notas declaradas e bloqueios P0/P1. A validação não prova que os avaliadores são independentes; usar procedimentos e convite externo.
`scripts/campaign_results.py` calcula métricas descritivas reais, com checagens, mas não declara significância/causalidade. Visualizações de impressões e CTR sem randomização são exploratórias. Qualidade criativa percebida, memória de marca e venda não são intercambiáveis.

## 5. Ensaios comparativos
Condição A com skill e B sem skill, mesmo briefing, ativos, modelos, créditos, pessoas, hardware, budget, duração de trabalho e regras de direitos. Realizar múltiplas produções por gênero (SaaS/UI, marca humana, social, produto 3D, motion 2D, 9:16 social, educativo, evento). Avaliadores cegos veem arquivo completo com áudio — não screenshots do hero. Publicar onde a skill perde, e mudar o **método que causou a derrota**.
**O objetivo é melhorar o pior filme**, não escolher o trailer mais bonito de um lote.

## 6. Não usar evidências erradas
GitHub Actions green = scripts e render técnico funcionam.
MP4 com áudio = vídeo existe; não diz se voz está inteligível.
Contact sheet = quadros são extraíveis; não significa motion fluido.
Notas de uma IA = autoavaliação, não avaliação independente.
CTR maior = resultado observado; não prova vídeo superior sem experimento apropriado.
WARC/System1/Google = referências de boas práticas e pesquisa, não validação da Video OS Prime.

## 7. Condição de parada da produção
Entrega corresponde à solicitação, fonte editável preservada, filme assistido/ouvido quando possível, P0/P1 conhecidos resolvidos, MP4/QC real, legibilidade por plataforma e relato de UNKNOWN preciso. Se era só roteiro, entregar roteiro. Se houver impedimento real de render, avisar; nunca inventar que trabalho está feito.
