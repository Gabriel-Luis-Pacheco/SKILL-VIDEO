# Video OS Prime · Film, Motion & Ads with AI

**AI-assisted audiovisual direction system, not a prompt collection.** Built for original ads, cinematic brand films, motion graphics, product demos, 2D/3D, trailers, social campaigns and hybrid films.

> Version 2.0.0 · 2026-10-20 · Based on the [Best Designer in the World](https://github.com/Gabriel-Luis-Pacheco/Best-Designer-in-the-World.-) philosophy, expanded with specialized cinema/advertising/motion workflows.

## Promise and limits

The goal is to raise the standard of creative *decisions*, technical production and final work. It cannot guarantee virality, ROAS, artistic superiority, awards or parity with the production teams of OpenAI, Anthropic and Duolingo. Technical and artistic evaluations are separate; neither may be fabricated.

## Install

```bash
npx skills add Gabriel-Luis-Pacheco/SKILL-VIDEO --skill ai-video-director
```

Or copy `skills/ai-video-director` to your agent's skills directory. Begin at [SKILL.md](skills/ai-video-director/SKILL.md). The script library, documented case studies, production recipes, capability router and tests live alongside it.

## The standard

**Truth of product → creative insight → multiple defensible treatments → storyboard → per-shot medium selection → animatic → produce the full film → inspect visuals AND audio → repair weakest link → render/export → performance learnings.**

- Keep canonical brand assets and genuine product screens. Do not invent features, reviews or client results.
- Use Remotion / After Effects / Fusion / Blender / Rive / procedural 2D when controllability matters; generative video where its unique strengths actually improve the film.
- Build a memorable visual action rather than text slides, stock b-roll, default gradient or generic AI cinematics.
- Ads use a relevant hook and proof; brand film and art may earn attention differently.
- Every film has a complete beginning, middle and payoff. One polished opener is not a finished film.
- Validate technical assets with repeatable checks. Only real human or independent review can establish artistic perception.

## Reading paths

| Task | Start |
|---|---|
| Quick new project | [SKILL.md](skills/ai-video-director/SKILL.md) |
| Learn from world-class work | [Brand campaigns atlas](skills/ai-video-director/references/30-campaign-atlas.md) |
| Original scripts ready to adapt | [Script vault](skills/ai-video-director/examples/original-script-vault.md) |
| Motion engineering | [Motion art direction](skills/ai-video-director/references/31-motion-masterclass.md) and [technical router](skills/ai-video-director/references/32-technology-router.md) |
| OpenAI / Anthropic / Duolingo principles | [High-craft brand patterns](skills/ai-video-director/references/33-high-craft-brand-cases.md) |
| Quality control | [Film review](skills/ai-video-director/references/34-qa-scorecards.md) |
| Evaluation | [Head-to-head protocol](skills/ai-video-director/references/35-benchmark-protocol.md) |

## Verification

```bash
python skills/ai-video-director/scripts/validate.py
python -m unittest discover -s tests -v
python skills/ai-video-director/scripts/shotlist_lint.py skills/ai-video-director/fixtures/valid_shotlist.json
```

Full source links appear in the references. The atlas analyzes concepts and techniques; it does **not** reproduce copyrighted commercials or claim to contain production scripts of the brands.

License: MIT.