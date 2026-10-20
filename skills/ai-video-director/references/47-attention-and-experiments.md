# Creative testing sem sacrificar direção artística

## Compreender a pergunta correta
Para uma peça de performance, separar hooks: resultado comprovável, tensão, surpresa relevante, prova primeiro, pergunta vivida. Todo hook cria expectativa que o filme e a oferta real devem satisfazer. Para brand film, arte ou educação, não aplicar mecânica de CTR/CTA por padrão.

## Short-form e retenção
Em social, assistir como alguém que ainda não conhece a marca: o primeiro quadro tem motivo, o meio progride, o final resolve a promessa (ou abre um loop narrativo honesto). Pattern interrupt deve nascer de mudança de informação/ação/som; intervalos fixos de corte podem piorar filme. **Não usar percentuais universais de swipe ou view-through sem fonte, amostra e plataforma atualizadas.**

Loops visuais: comparar primeiro/último frame sob o mesmo layout/movimento/contraste, mas distinguir *loop intencional* de encerramento ruim. Vídeo com CTA não deve desaparecer antes de a ação ser compreendida. Rewatch não equivale a intenção de compra.

## Variantes de publicidade como experimento
Uma rodada modifica só HOOK, PROOF, CTA ou OFFER. Os outros campos, footage, duração, sample, segmentação e budget devem ser equivalentes. Variar hook e CTA simultaneamente pode ser útil para explorar conceitos, mas não é um **teste causal de uma variável**; rotular como exploração multivariada. Mensagem de hook, corpo, CTA e landing deve combinar semanticamente — nenhum script automatizado certifica equivalência sem revisão humana.

### Contrato executável
Arquivo `campaign_matrix.json` com `baseline` e `variants`. `campaign_matrix.py` impede duas alterações entre baseline e variante e mudança de theme/URL sem hipótese correspondente; exige fonte para proof e offer. Ferramentas só fazem invariantes de campo, não reputação, copywriting, causalidade ou resultados.

## Métricas
Observações: plays, retenção segmentada, clicks, qualified signups, completed onboarding, vendas, brand lift são dimensões diferentes. Não inferir conversão pelo estilo nem validar hooks pela impressão subjetiva do próprio agente. Registar denominador, período, fonte do evento e consentimento. Testes experimentais devem ser desenhados com estatística adequada antes de declarar vencedor.

## Aspectos
Para 9:16, 4:5, 1:1, 16:9 gerar composições com escala e layout próprios. Especificação de safe zone depende do placement e do momento (botões/legendas UI mudam). Capturar overlay atual e conferir com o destino; um retângulo de segurança único não garante legibilidade em todos os apps.

Fontes: https://github.com/iart-ai/ad-video-skills ; https://github.com/iart-ai/tiktok-video-skills
