# Evidence-first frame review — screenshots que realmente testam o filme

## Por que 3 stills são insuficientes em produção real
Frame de abertura, meio e final não prova a continuidade, interações, legibilidade durante transformações, glitches de T2V, drifts faciais nem o timing das transições. Planejar captura por **eventos**, não só porcentagem.

## Matriz mínima de checkpoints para cada cena
- Início e fim do shot.
- Primeiro frame de entrada de texto e quadro após a entrada completar.
- Pico de velocidade / contato entre objetos / deformação máxima.
- Início, centro e fim de sobreposição/crossfade.
- Trechos que revelam a prova principal do anúncio, UI e números.
- Mudança de máscara, conteúdo do primeiro/último frame de loop, CTA legível.
- Pontos do filme onde a ação deve gerar som importante.

`timeline_compile.py` produz `checkpoints` provisórios (inícios, midpoints e últimos frames por cena). Especialista deve acrescentar key events reais. Comparar renders no frame exato, sempre com fontes e props usadas para a versão entregue.

## Registro de evidência
`frame | time | expected event | observed | PASS/FAIL/UNKNOWN | issue | correction | revisited_frame`. Sem screenshot/acesso a frame observável, status UNKNOWN; sem acesso ao vídeo não há verificação de continuidade. Após alteração relevante, recapturar eventos afetados e final completo.

## Arte/motion
Checar silhueta, foco, alinhamento, contraste, hierarquia, curva, direção, material e som com a mesma exigência do roteiro. Um frame lindo de uma sequência ruim não atende ao objetivo. Flashing excessivo ou cintilação podem ser problemas de conforto/acessibilidade.

## Fluxo barato de revisão
Renderizar 1 variante em todos os formatos antes de fazer dezenas de renderizações. Conferir variação real de texto e posição. Para dúvida de QA de color/exposição, usar chart e amostra sem afirmar que screenshots representam todos os monitores.

Referências: https://github.com/nyosegawa/skills/tree/main/skills/remotion-promo-video-factory ; https://github.com/iart-ai/tiktok-video-skills
