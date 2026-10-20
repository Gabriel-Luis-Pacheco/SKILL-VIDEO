# QA adversarial — técnica, arte, narrativa e resultado são dimensões distintas

## Gates de lançamento
- **P0:** funcionalidade, cliente, citação, review ou depoimento fabricado; direito ausente; pessoa real simulada sem consentimento; divulgação sintética exigida ausente; interface fictícia apresentada como verdadeira.
- **P1:** entendimento central falha; hook promete outro vídeo; branding errado; mascote fora de anatomia; peça inacabada; erro de som/legenda/contraste/crop; payoff faltando.
- **P2:** polish de timing, kerning, texturas, curvas, pequenas variações de áudio/edição.

## Avaliar separadamente (0–4, com justificativa por evidência/timecode)
1. Precisão e verdade da marca.
2. Particularidade da ideia — imagem que só este produto faria.
3. Qualidade e pertinência do hook.
4. Progressão de narrativa/prova.
5. Aderência do payoff.
6. Direção de arte, forma e identidade.
7. Motion: peso, spacing, ritmo, coordenação e pausas.
8. Câmera/luz/profundidade/continuidade.
9. Montagem/transições e ritmo do filme inteiro.
10. Som: mix, espaço, pausas, SFX/voz.
11. Legibilidade, safe zone e acessibilidade.
12. Excelência técnica da entrega / consistência de formatos.

**Regras de honestidade:** nenhum vídeo acessível → tudo que depende de observar mídia é UNKNOWN; um MP4 gerado não prova alta qualidade; score próprio é *autoavaliação*, não avaliação humana. Conteúdo proibido ou P0 impede aprovação independentemente da média. Marca/conversão também não podem ser inferidas de métrica de export.

## Métodos de review
Passo 1 assistir sem tomar nota; contar o filme que entendeu sem reler o script. Passo 2 rever com som mudo; consegue identificar contexto e payoff? Passo 3 só áudio; ambiência/voz/ritmo fazem sentido? Passo 4 inspecionar timecodes de frame 1, mudança de cena, meio e final; procurar drift, flicker, pequenas deformações. Passo 5 rever em telefone e sem legendas forçadas do player. Passo 6 anotar três falhas mais sérias, raiz causal e teste da correção. Passo 7 reexportar e rever **o novo MP4**.

## QC automatizável
FFprobe: duração, streams, codec, dimensions, fps. FFmpeg: blackdetect/silencedetect/ebur128 quando configurados, e montage de frames. Captions: alinhamento, caracteres/linha, tempo suficiente. Automação não reconhece se frame é bonito, se voz soa humana ou se anúncio vende — declarar não verificado.
