# AI Shot Supervisor — gerar menos tomadas ruins e preservar continuidade

## A decisão que precede o prompt
O take exige consistência perfeita de marca/personagem, texto exato, UI real, dados, cálculo, lipsync, uma ação humana simples, mundo imaginário ou câmera complexa? **Não escolher o modelo pela propaganda do fornecedor.** Determinístico quando precisão é central; T2V/I2V quando movimento atmosférico ou ação específica beneficia o filme; filmagem licenciada para verdade documental; Blender/Rive/AE/Remotion para controle rigoroso. Consultar fontes oficiais na data do trabalho e testar limites de FPS, tempo, referências e áudio antes de assumir capacidade.

## 1. Shot contract
Uma linha por take:
- `shot_id`, intenção narrativa, duração-alvo, orientação, tamanho do sujeito e eixo de ação.
- Referência canônica: imagens aprovadas, faixa de variação, cores, escala, anatomia, logo (ou nenhum).
- Ação física observável no começo, no meio e no fim; ao menos um ponto de continuidade com cena vizinha.
- Regras de câmera: parada, pan/dolly/orbit, altura, lente/perspectiva e velocidade motivada.
- Luz, textura, época/contexto, figurino e materiais.
- Som esperado/sons a produzir em pós (não assumir que o gerador produz áudio).
- Zona de texto: deixar livre para lettering exato feito em pós quando necessário.
- Falhas graves e método alternativo de reshoot.

## 2. Prompt por modo
**T2V:** descrição sucinta do sujeito, ambiente, composição e uma ação principal com progressão temporal. Acrescentar movimento de câmera somente se ajuda o gesto. Ex.: "Em uma bancada de madeira, uma fita de papel se desenrola, encosta numa pedra e altera a direção; tomada média fixa, luz lateral, câmera imóvel até o contato; depois dolly lento para revelar consequência." Não adicionar promessa de precisão inexistente.
**I2V:** imagem de referência estabelece aparência; prompt enfatiza apenas como sujeito, objetos, câmera e luz mudam no tempo. Evitar redescrever o frame com adjetivos redundantes. Ex.: "A personagem segura pose durante um instante, vira a cabeça à esquerda e aponta para o cartão; câmera mantém enquadramento, o cartão permanece imóvel." Texto/rostos canônicos exigem inspeção.
**Extend:** usar último frame canônico da tomada anterior, mesma direção de ação, luz, eixo e escala; revisar raccord no corte.
**Restyle:** direitos do material original, sem alterar anatomia/identidade e sem simular evento factual enganoso.

## 3. Ficha de prova antes de gastar
Testar dois desafios do filme: (A) consistência de personagem/objeto em cinco frames críticos; (B) câmera/ação/oclusão. Gerar somente candidatos suficientes para estimar falha sem queimar orçamento. Documentar modelo, versão, entradas, seed quando suportada, time, custo/créditos, referência, status e motivo de descarte. "Melhor modelo" é relativo a este take, não a benchmark inventado.

## 4. Rejeição e reshoot por falha
- UI, texto, marca ou número alterado → sempre preferir overlay vetorial/captura verdadeira, não retocar glitch.
- Rosto/mascote irreconhecível ou múltiplos membros → voltar para rig, vídeo real ou referência mais rígida.
- Objeto atravessa parede, muda de escala ou posição sem causa → dividir plano, reduzir movimentos, criar cenário controlável.
- Tempo/continuidade errados → animatic e pontos de entrada/saída antes de regenerar.
- Só atmosférico e não revela produto → reescrever papel narrativo da tomada, não repetir prompt com 30 adjetivos.
- Cor/foco flutuando entre takes → match color com source, atualizar chave visual ou trocar clipe.
- Gerador não dispõe de áudio confiável → criar foley/VO em pós com licença apropriada.

## 5. Produção híbrida
Compor resultado generativo como **placa** de cinema: mascarar, color-match, tracking, grain controlado e som coerente. Adicionar tipografia, CTA, preço, dado, logo e UI como elementos autorais determinísticos sobre a cena. O "primeiro/último frame" real pode ser uma decisão de direção mais importante que a imagem mais bonita do meio. Limites da ferramenta mudam: docs oficiais atuais governam.

## 6. Política de tempo
Takes complexos divididos em ações compreensíveis. Duração por cena é determinada por timing/ritmo e condições do modelo, não cortes automáticos de 2 ou 4 segundos. Não aumentar velocidade arbitrariamente e falsear demonstração técnica.

Fontes oficiais de princípio: https://academy.runwayml.com/guides/prompting-guide ; https://help.runwayml.com/hc/en-us/articles/42460036199443-Text-to-Video-Prompting-Guide ; https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide ; https://motion-canvas.io/docs/rendering/video/
