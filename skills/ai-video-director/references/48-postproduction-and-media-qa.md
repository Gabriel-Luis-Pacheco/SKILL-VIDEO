# Pós-produção e conformação técnica — ferramenta não substitui revisão de filme

## Edição determinística
FFmpeg aplica cortes, filtros, composições, grade simples, overlays, conversão, concatenção e análise; Resolve/Fusion ou editor adequado tratam decisões criativas complexas. Prefira comandos em arrays via subprocess, sem shell com conteúdo do briefing. Inspecionar streams com ffprobe ANTES de escolher transcode e mapear vídeo/áudio explicitamente.

### Cortes precisos
Para corte exato em tempo não-keyframe, reencode apropriado ou fluxo intermediário lossless; `-c copy` com seek rápido pode não cortar na exata borda solicitada. O áudio precisa acompanhar alterações temporais: mudar `setpts` sozinho deixa trilha fora de sync.

### Concatenar
Verificar codec, resolução, fps, timebase, pix_fmt, áudio, sample rate e canal de cada entrada antes de concat demuxer com `-c copy`; incompatíveis pedem normalizar para intermediários antes. Crossfade com `xfade` exige compatibilidade de streams/timescale e áudio equivalente se necessário; conferir sobreposição na timeline compilada.

### Exports
H.264 MP4 para uso amplo, opções configuradas por plataforma, `-movflags +faststart` para progressive playback quando aplicável; ProRes/DNxHR/intermediários de alta fidelidade para edição, alpha somente quando pipeline suporta; codec e bit depth escolhidos pelo destino real. Não fixar CRF/preset/LUFS como dogma universal.
Gradear no espaço de trabalho e converter corretamente; metadados colorimétricos NÃO representam color management por si.

### Diagnóstico automatizável
```bash
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,avg_frame_rate,pix_fmt,color_range,color_space,color_transfer,color_primaries,sample_rate,channels -show_entries format=duration -of json output.mp4
ffmpeg -hide_banner -i output.mp4 -vf "blackdetect=d=0.15:pix_th=0.05" -an -f null -
ffmpeg -hide_banner -i output.mp4 -af "silencedetect=noise=-45dB:d=0.5" -vn -f null -
```
Esses thresholds são *sondas* e precisam ser ajustados ao filme: um fade-to-black planejado ou silêncio dramático não é erro. Analisar relatório junto à timeline/roteiro. Não executar os exemplos sem confirmar arquivo e ferramentas.

## QA visual final
Montar contact sheet com momentos narrativos representativos incluindo corte, clímax, CTA, caption, texto pequeno e transição em overlap. Conferir RGB/banding/material/identidade humana, não só se o MP4 abre. Sondar áudio isolado, em celular e mono. Reexportar depois de corrigir e verificar novamente o arquivo **final**, não renders intermediários.

Fontes: https://ffmpeg.org/ffmpeg.html ; https://ffmpeg.org/ffprobe.html ; https://github.com/bryanwhl/ffmpeg-video-editor
