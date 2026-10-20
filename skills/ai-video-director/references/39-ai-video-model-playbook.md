# Geradores de vídeo com IA — prompting por tomada e calibração

## Regras que sobrevivem à troca de modelo
T2V: descrever sujeito, contexto, ação física observável, composição, câmera, luz, progressão temporal e acabamento; uma tomada com ideia clara tende a ser mais controlável que roteiro de 30s num único prompt. I2V: **imagem ancora aparência**, texto descreve mudança/movimento; não recitar toda imagem. Para um personagem recorrente, usar ativos canônicos (reference/keyframes) e avaliar drift quadro a quadro. Para textos/números/logos, compor em pós com vetor/fonte verdadeira. Para áudio, verificar que modelo e modo suportam o pedido — nunca assumir.

## Estrutura por modo
**TEXT TO VIDEO:** "Um [sujeito] [ação física principal] num [ambiente]. Enquadramento [plano], câmera [trajetória motivada], iluminação [origem/coerência]. A ação evolui [início → evento → final]. [aspect, duração e áudio] apenas se interface documentar."
**IMAGE TO VIDEO:** "Preserve a composição e os traços canônicos da imagem de referência. [Parte] executa [movimento observável] enquanto [câmera] acompanha. Final em [estado/posição]." Alguns modelos ignoram restrições de identidade; validar e rerrolar/reshoot.
**SHOT-EXTENSION:** iniciar com frame final canônico, mesma linha de ação, luz e orientação; checar continuidade de objeto e música antes de colar.
**STYLE TRANSFER/RESTYLE:** direitos de origem, consistência da marca, teste de bordas/expressões/texto.

## Calibração antes de gastar orçamento
Gerar 2 microprovas difíceis: (A) identidade/continuidade, (B) movimento de câmera/oclusão. Avaliar taxa de tomadas utilizáveis, custo, duração, assets exigidos e áudio, com output real; não declarar “melhor gerador do mundo” por marketing da ferramenta. Comparar gerador vs rig/Blender/Remotion para a cena específica.

## Falhas comuns e correções na ordem
Texto mutante → layer determinística em pós; mãos deformadas → reenquadramento/reshoot, menos interação manual complexa; rosto/mascote drift → img reference/rig; objeto atravessando parede → reconstruir plano em 3D ou cortar; câmera sem motivação → prompt simples locked/dolly; fundo pulsando → trocar plano, estabilizar/comp controlada; dificuldade de ação múltipla → dividir em takes; vídeo com história inexistente → consertar storyboard antes de prompt.

## Fontes oficiais para consultar na data da tarefa
- Runway Gen-4.5: https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5
- Runway prompting: https://academy.runwayml.com/guides/prompting-guide
- Runway I2V: https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide
- Google Veo: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
Outros modelos (Sora, Kling, Luma etc.): pesquisar documentações oficiais no momento de usar. Evitar especificações de versão obsoletas, falsos limites e comandos API imaginários.
