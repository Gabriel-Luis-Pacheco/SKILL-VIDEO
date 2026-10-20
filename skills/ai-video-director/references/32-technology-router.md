# Tecnologia — escolher o meio, não seguir hype

## Árvore de decisão
**Texto exato, gráficos, logo, UI, data, precisão de pixel:** preferir Remotion/After Effects/Motion Canvas/Cavalry/Fusion. **Captura de aplicativo:** gravar fluxo real com dados fictícios autorizados e editar (não simular telas). **Personagens e props sob continuidade rígida:** rig 2D/3D, Rive, Blender, composição controlada; geradores só em passes com QA. **Atmosfera, locais impossíveis, mood, cenas abertas:** considerar T2V/I2V após preparar stills e art bible. **Filme humano documental:** filmagem/licenciamento/consentimento. **Cor, sound mix, edição longa:** Resolve e Fairlight, Premiere/AE quando existente. **Composição 3D fotorrealista:** Blender e render adequado.

## Ferramenta / força / limitação / validação
| Ferramenta | Excelente para | Falha típica | Evidência |
|---|---|---|---|
| Remotion (React) | Vídeos programáticos, layout e render determinístico, variações, captions | Misturar efeitos CSS assíncronos ou fontes instáveis | Preview/render frame-by-frame e export |
| Motion Canvas (TS) | 2D procedural, diagrama e narrativa matemática | Deixar timing preso a exemplos genéricos | Reprodução e export real |
| After Effects | 2D/comp, keyframes, efeitos, retiming | Preset-driven, projeto difícil de reproduzir | Arquivo fonte + render |
| Cavalry | Motion procedural, layouts, repeaters | Render dependente de plugins/versão | Teste de saída |
| Blender | 3D, física, Grease Pencil, Geometry Nodes | Pesado, overengineering, render caro | Playblast + amostras finais |
| Rive | Animações de marca e interação stateful reutilizável | Runtime não é timeline de filme longo por padrão | Gravação/export comprovado |
| Resolve/Fusion | Edit, color management, node compositing | Configurações de espaço de cor inconsistentes | A/B scopes + master |
| FFmpeg/ffprobe | Transcode, concat, QC, formatos | Não avalia direção artística | Metadados + análise |
| IA T2V/I2V | Movimento/cenas não determinísticos com textura/atmosfera | Drift, personagem mutável, texto errado | Decupar take e inspecionar frames |

Não fixar modelo, preços, dimensões, duração ou codecs se a documentação atual não foi checada. Verificar fontes oficiais no momento da execução. Não assumir que biblioteca instalada está disponível. Se a combinação de ferramentas for inviável, escolher o fallback mais controlável e reportar trade-off.

## Render pipeline de nível profissional
1. Preflight: assets com licença, dimensões, canal alpha, fontes, sample rate, fps, lineages.
2. Animatic de baixa resolução de todo o arco, com placeholders explicitamente rotulados.
3. Motion/comp refinado: pass de silhueta, pass de cor, pass de material/luz, pass de timing/mix.
4. Render de frames amostrados incluindo extremos e momentos de transição.
5. Master edit: color transform coerente, primárias/secundárias com scopes, sound mix, legendas e final action.
6. Export: master de qualidade + derivativos por canal; nunca esticar vídeo para outra proporção.
7. QC metadata + reprodução efetiva com inspeção de som e imagem; preservar editável, assets e fontes.

## Fontes oficiais (consultadas em outubro/2026)
- https://www.remotion.dev/docs/render
- https://www.remotion.dev/docs/parameterized-rendering
- https://www.remotion.dev/docs/captions/displaying
- https://rive.app/features
- https://docs.blender.org/manual/en/4.5/grease_pencil/index.html
- https://www.blackmagicdesign.com/br/products/davinciresolve
- https://academy.runwayml.com/guides/prompting-guide

A fonte que comprova recurso não certifica que o workflow foi testado neste repositório.
