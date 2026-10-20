# Avaliação comparativa com e sem a skill

1. Escolha 8–12 briefs heterogêneos (SaaS, app com mascote, social impacto, B2B, brand film, motion typography, 3D, curta de 6 s, UI).
2. Congele assets/fontes/versões/modelos/créditos/seed disponíveis e budget por condição.
3. Condição A sem a skill; B com a skill; repetir ensaios em workspaces isolados. Guardar logs de leitura real de SKILL.md e referencias, sem segredos.
4. Julgadores externos cegos avaliam vídeos finais em escala 0–4 para verdade, clareza, distintividade, story, motion, cinema, sound, edição, legibilidade e eficácia presumida.
5. Checar tecnicamente com video_qc e inspecionar áudio/imagem. Os julgadores precisam ver o vídeo, não só um resumo.
6. Publicar vitórias, perdas, regressões e custo médio, sem alegar significância causal sem amostra.
7. Anúncio que gerou mais views NÃO prova mais vendas; teste comercial exige randomização/atribuição e métricas reais.

**Nenhuma comparação cega independente foi realizada nesta versão.** Testes de Python/GitHub Actions inspecionam integridade, não direção artística.

## Video OS Prime 4.0 experimental protocol

**Creative blinded test:**
1. Randomly assign matching briefs to agents with and without the skill in isolated environments. Freeze source footage/brand canon, AI model + credits, render tools, editing effort, and deadline.
2. Preserve final MP4, audio, frame sheet, source assets and technical preflight from both arms, with anonymous IDs that do not expose condition.
3. Invite at least two reviewers unaware of the condition. Ask them to observe whole videos WITH audio and independently submit rubric across brand truth, memorable concept, original visual form, story middle, motion, cinema, sound, readability, emotional payoff and objective.
4. Submit their declared reports to `scripts/independent_review.py` for schema/critical issue checks. It **cannot verify they watched**: logs and custody must come from the actual study process.
5. Publish all pairs including failures, study size, confidence limitations and methodology. Do not collapse ordinal subjective scores into invented statistical certainty.

**Marketing creative test:**
1. Define primary metric and denominator BEFORE traffic begins; use matching audience, attribution, placement and verified offers.
2. Use `scripts/campaign_matrix.py` to isolate one change per A/B (hook, proof, CTA or offer), and keep brand/theme/landing locked.
3. Export actual platform counts to a separate JSON and run `scripts/campaign_results.py`. It returns descriptive rates and Wilson intervals, not a causal effect or a "winning" variant.
4. For a causal claim, require appropriate random assignment, power, confidence/multiple comparisons and real platform attribution analysis. Without those, report observation only.

**Decision to improve:** fix the worst reproducible deficiency in creative performance, not whichever edit had the loudest effects. Reduce giant docs if reading them lowers execution quality.
