# Engenharia de tipografia, legendas, cor e som

## Tipografia não é efeito decorativo
Definir texto final, fonte autorizada, peso, tracking, limites de linha, divisões semânticas e zoom real ANTES de animar. Textos comerciais em vídeo precisam ser legíveis no player móvel e não podem competir com a prova. Em kinetic type, escolher linha, palavra ou grafema como granularidade, conforme intenção — não animar caractere a caractere por padrão.

**Unicode em português:** não usar `string.split('')` como método geral para grafemas. Quando houver JS moderno, `Intl.Segmenter('pt-BR',{granularity:'grapheme'})` mantém acentos combinados, emoji compostos e grafemas em unidades visuais. O resultado precisa ser inspecionado ao usar ligaturas ou variável font. `document.fonts.ready` antes de medir text boxes no browser; no Remotion, carregar fontes de modo suportado pela versão atual. Fonte variável: verificar eixos `wght`, `wdth`, `opsz` realmente contidos no arquivo antes de animar. Recalcular layout em cada aspect nativo.

### Legenda é semântica e tempo
Usar timestamps da transcrição revisados por pessoa quando necessário; um bloco curto deve permanecer tempo suficiente para leitura em celular. Em SRT, cue IDs e milissegundos crescentes, texto não vazio, ausência de overlaps acidentais, limites de largura configuráveis e não sobrepor UI do app. `captions_lint.py` checa erros estruturais e avisa quando velocidade de leitura parece alta; NÃO certifica sincronização voz→texto.

### Split text para web
Wrapper original possui full aria-label/accessible text, spans animados marcados aria-hidden, fallback reduced-motion. Animação não pode destruir copy/paste, ordem de leitura e grafemas. Evitar leitura de modelo generativo para tipografia, números, acentos e logos: usar SVG/HTML/AE editável.

## Color science no arquivo final
Decidir espaço de trabalho, primárias, transferência, matriz, range (limited/full) e alvo SDR/HDR; não presumir que "Rec.709" cobre TODAS as variáveis. Para SDR de distribuição típica verificar tags `color_primaries=bt709`, `color_transfer=bt709` quando adequado, `color_space=bt709`, faixa de níveis e display target; não copiar tags sem transformar pixels, porque declarar metadata não corrige grade incompatível.
- Gradientes devem preservar luminância/percepção intencional. Interpolação OKLCH/Lab pode evitar meio turvo quando a cor é expressiva; não é obrigação para uma cena dramática dessaturada.
- Teste de faixa/cor: render pequeno com patches (cinza, tons de pele, cor de marca), comparar interpretação em navegador/player/editor e verificar informações com ffprobe. Diferenças entre players são problema a investigar, não licença para aplicar LUT às cegas.
- Checar posterização/banding após compressão real, especialmente em áreas de gradiente e sombras. 10/16-bit intermediário se necessário, master de alta qualidade antes dos derivativos.
- Não adotar LUT teal-orange como sinal automático de cinema.

## Som e percepção
Trabalhar stems de voz, música, foley e ambiência com dinâmica de intenção. Analisar loudness conforme requisito real da plataforma/cliente, nunca assumir um valor LUFS universal. Testar inteligibilidade em telefone, fone e mono, transientes e trechos de silêncio; `ffprobe` identifica stream de áudio, mas não qualidade, clipping percebido ou adequação emocional.

## Checks práticos
- Ler frame com texto inteiro (e não só o momento em que ainda entra).
- Legenda não oclui prova/rosto nem CTA.
- Acentuação PT-BR e tipografia de logo são precisas.
- Comparar primeiro/final frame de loops quando a cena exige seam.
- Conferir tags colorimétricas com `ffprobe` e ver transcode nos destinos.
- Captar frames com **props reais** da variante, não só defaults.

Referências: https://github.com/iart-ai/kinetic-typography-skills ; https://github.com/iart-ai/motion-design-skills/tree/main/skills/color-motion
