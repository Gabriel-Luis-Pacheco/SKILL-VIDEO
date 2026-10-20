# Ferramentas atuais de vídeo e motion — disponibilidade antes de hype

**Data de revisão editorial:** 20 de outubro de 2026. Este documento é um protocolo de consulta, NÃO uma tabela garantida de disponibilidade futura. Versões, assinaturas, países, créditos, limites e políticas mudam.

## O que foi verificado em fontes oficiais
| Sistema | Uso quando apropriado | Informação de disponibilidade / fonte oficial | Cuidados |
|---|---|---|---|
| **Remotion** | Motion exato com React, dados, tipografia, vídeo parametrizado | https://www.remotion.dev/docs/render — CLI, Studio, SSR e opções de render | Verificar APIs atuais e criar preview REAL antes de declarar MP4 |
| **DaVinci Resolve 21 / Fusion / Fairlight** | Montagem, conform, correção de cor, compositor, som e entrega | https://www.blackmagicdesign.com/br/products/davinciresolve/whatsnew/ — funções atuais Resolve 21 | Algumas funções dependem de Studio/hardware; não afirmar que está instalado |
| **Runway** | Gerar, transformar e explorar cenas onde IA acrescenta valor | https://help.runwayml.com/hc/en-us/articles/48649877897107-Available-Models-on-Runway — catálogo vivo | Variáveis: créditos, acesso, modo, duração, tipo de referência, áudio e região; conferir em tempo de execução |
| **Google Veo** | T2V, I2V e fluxos com keyframes de primeiro/último quando suportados pelo ID de modelo | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-1-generate — especificação de uma família de modelos | Não tratar função "suportada" num SKU como suporte universal em todos; verificar duração/aspecto/taxa de frame e disponibilidade |
| **Blender** | 3D, rig, Grease Pencil, câmera, física e geometry nodes | https://www.blender.org/ e https://docs.blender.org/manual/en/latest/ | Preview low-res antes de render pesado; GPU e materiais afetam resultado |
| **Rive** | Animação vetorial de personagem/estado reutilizável | https://rive.app/features | Verificar como exportar vídeo no projeto real; runtime de animação não equivale a pipeline de long-form automaticamente |
| **FFmpeg/ffprobe** | Conform técnico, encoding, sample de frames e metadata | https://ffmpeg.org/ffmpeg.html e https://ffmpeg.org/ffprobe.html | Não produz bom cinema sozinho; controlar shell e validar input |
| **Motion Canvas / After Effects / Cavalry** | Motion procedural e comp 2D, keyframes, precisão | https://motion-canvas.io/ ; https://helpx.adobe.com/after-effects.html ; https://cavalry.scenegroup.co/ | APIs/licenças/plugins/gestos variam, checar ferramentas reais |

## Descontinuações e contexto crítico
A OpenAI informa que **o produto Sora deixou de estar disponível em 26/04/2026**: https://openai.com/index/sora/ e https://openai.com/index/creating-with-sora-safely/ . Não recomendar seu aplicativo ou API como serviço pronto em um fluxo de produção atual sem confirmar outro produto ou disponibilidade oficial distinta. A existência histórica de um modelo não comprova serviço ativo.

## Capabilities ledger — exigido para produção que depende de provedor
Registrar estes campos em `capabilities.json` antes de escolher fornecedor:
- `provider`, `tool`, `model_id`, `version`, `verified_at`, `official_doc_url`.
- `access_verified` (teste real da conta ou UNKNOWN); `billing` e `quota` (com fonte atual).
- `text_to_video`, `image_to_video`, `first_last_frame`, `video_extension`, `audio_generation`, `reference_consistency`, `alpha`, `fps`, `durations`, `aspects`, `resolution`.
- `known_failure_modes`, `price_per_output`, `license_and_credits`, `privacy_and_retention`, `fallback_medium`.
Todos os campos desconhecidos ficam **UNKNOWN**, não false. Nunca transformar documentação de marketing em garantia de identidade ou qualidade.

## Seleção por tomadas em vez de ranking mágico
1. Precisão do material (UI, números, logo, mascote, direitos) é restrição, não score cosmético.
2. Entre opções tecnicamente viáveis, produzir **uma prova curta da tomada mais difícil**; comparar consistência de cinco pontos da timeline, câmera, material e custo de reexecução.
3. Calcular custo total do take aceito (incluindo tentativas descartadas), não apenas preço por geração.
4. Preferir meio mais reprodutível quando resultado exato é essencial; preferir gerar mundos com IA quando entrega originalidade controlável.
5. Preservar art bible/keyframes/seed quando disponível, fontes e timing para composição final.
6. Nenhuma tecnologia nova substitui direção, sound design, corte e performance real do anúncio.

## Estado de qualidade por etapa
**Documentação oficial consultada** ≠ acesso do usuário confirmado. **Acesso confirmado** ≠ take utilizável. **Take utilizável** ≠ filme terminado. **Filme terminado** ≠ conversão comprovada. A skill deve distinguir todos os quatro estados nas respostas.
