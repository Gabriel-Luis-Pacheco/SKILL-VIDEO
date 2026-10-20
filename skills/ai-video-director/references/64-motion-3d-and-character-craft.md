# Motion craft — editor de referência / diretor de animação / supervisão 3D

## A diferença entre animação e movimento decorativo
Movimento expressa relação de causa, peso, tempo e significado. A palavra que "quebra" precisa sofrer uma força; uma interface que mostra ligação precisa evidenciar nós reais; um material molhado pode alterar brilho e som; a animação de um mascote precisa comunicar personalidade e manter anatomia canônica. Objetos que só "entram com easing e bounce" não têm uma ideia cinematográfica.

## High-end 2D editorial
1. Criar silhuetas/typography em frames-chave, com spacing óptico e grid real.
2. Definir hierarquia PRIMARY, SUPPORT, AMBIENT por quadro (nunca três protagonistas competindo).
3. Escolher famílias cinéticas: estrutural, elástica, orgânica, mecânica, tipográfica, recortada; exceções por material.
4. Definir momentum, contato, anticipation, overshoot, hold e amortecimento em frames, sem copiar números globais.
5. Revisar curva de velocidade e objetos relacionados; atrasos precisam ter significado causal.
6. Fazer reveal do texto apenas quando ele é parte da narrativa — use objetos, personagens, espaço, câmera, layout.
7. Evitar zoom/blur como substituto de ação. Reduzir layers concorrentes e usar espaço negativo.
8. Adaptar 9:16/1:1/16:9 como layouts próprios, revisando legibilidade de tipografia PT-BR.

## 3D com intenção cinematográfica
**Blockout e câmera primeiro:** silhueta e proporção do objeto, eixo e blocking, composições em 3 frames e playblast do gesto; fechar antes de texturizar. Não usar oito movimentos de câmera sobre um objeto de cinco segundos.
**Material:** refletância, rugosidade, normal/displacement adequados à escala física, PBR sem over-shading, sombras de contato; se objeto real, conferir com referência.
**Luz:** key/fill/practical/motivated e consistência em plano/contra-plano; não combinar neon de estúdio com publicidade orgânica sem motivo.
**Sombra e profundidade:** perspective, lens, oclusão, DOF para dirigir foco e não ocultar erros; separar espaço de marca e espaço diegético conscientemente.
**Render:** amostras e antialiasing reais, motion blur sem virar smear genérico, noise/flicker entre frames, color pipeline correto, passes para correção/composição.
**Composição:** integrar glow, AO, reflexos, materiais reais com chromatic discipline; vinheta/grain/bloom não devem mascarar elementos ruins.

## Character acting
Antes de modelo, uma bíblia aprovada: silhueta, olhos, membros, proportion, rig, range of motion, personalidade, formas de reação e gestos recorrentes. **Acting beat**: personagem quer algo; obstáculo muda intenção; gesto revela atitude. Animação excelente vem de pose e spacing, não aumento de frames. Animar overlap das partes, mas não tornar mascote amorfo. Para personagem que ensina idioma: hesitação, erro, humor, resposta devem ser relevantes à ação, nunca barulho aleatório.

## QA motion por takes
- Silhouette read, forma e foco no primeiro quadro.
- Peak frame legível sob movimento.
- Contact frame com força e reação.
- Seguinte plano preserva orientação e escala ou justifica quebra.
- Surpresa narrativa está no meio, não somente no início.
- Pausas existem e têm duração suficiente no destino.
- Texto é exato, inclusive números, acentos, CTA e marca.
- Áudio reforça sem mimetizar cada animação.

## Anti-clone
Estudar Aardman, Giant Ant, BUCK e outros por sistemas de atuação, composição e direção, não copiar personagens, identidade de campanha ou processo proprietário. Referência não substitui design canônico do produto.
