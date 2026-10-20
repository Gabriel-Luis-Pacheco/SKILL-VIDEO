#!/usr/bin/env python3
"""Production-medium and objective routing from a factual brief.

The output is an explicit, conservative production plan — not a creative
director, a model benchmark, a claim verifier or an actual film render.
"""
import argparse
import json
from pathlib import Path
import sys

GOALS={
    "awareness":"Memória de marca, experiência, personagem e prova suficiente para atribuição.",
    "consideration":"Demonstrar diferença real e responder à dúvida dominante.",
    "conversion":"Provar benefício e oferecer próximo passo verdadeiramente disponível.",
    "retention":"Mostrar progresso/função real e reforçar hábito útil, não anúncio de aquisição.",
    "education":"Ensinar com sequência inteligível e prova/dados verificáveis, sem CTA de venda obrigatório.",
    "art":"Criar experiência visual/emocional; não exigir funil de marketing.",
    "launch":"Introduzir produto verdadeiro com momento memorável, uma prova e destino real.",
}
SURFACES={"reels","tiktok","shorts","youtube","landing","event","internal","cinema"}
TRUTH={"verified","declared","unknown"}
AVAILABLE={"remotion","blender","ae","rive","camera","screen_capture","t2v","i2v","ffmpeg"}
ASSET_KINDS={"ui","chart","brand_character","real_human","physical_product","imaginary_world","typography","mixed"}

def route(brief):
    errors=[]
    if not isinstance(brief,dict):
        return {"status":"FAIL","errors":["brief must be an object"]}
    goal=brief.get("goal")
    if not isinstance(goal,str) or goal not in GOALS:errors.append("goal must be one of "+", ".join(sorted(GOALS)))
    surface=brief.get("surface")
    if not isinstance(surface,str) or surface not in SURFACES:errors.append("surface must be one of "+", ".join(sorted(SURFACES)))
    kind=brief.get("central_visual")
    if not isinstance(kind,str) or kind not in ASSET_KINDS:errors.append("central_visual must be one of "+", ".join(sorted(ASSET_KINDS)))
    tools=brief.get("available_tools",[])
    if not isinstance(tools,list) or any(not isinstance(t,str) or t not in AVAILABLE for t in tools):
        errors.append("available_tools must be a list of named supported tools")
        tools=[]
    truth=brief.get("product_truth","unknown")
    if not isinstance(truth,str) or truth not in TRUTH:errors.append("product_truth must be verified, declared or unknown")
    if not isinstance(brief.get("brand"),str) or not brief["brand"].strip():
        errors.append("brand/subject must be nonempty")
    if errors:return {"status":"FAIL","errors":errors}
    warnings,blockers=[],[]
    if goal in {"conversion","launch"} and not brief.get("cta_destination"):
        blockers.append("No verified CTA destination; do not publish an invented landing or checkout.")
    if goal in {"conversion","launch","consideration","retention"} and truth != "verified":
        blockers.append("Product/feature truth not verified for commercial demonstration.")
    if kind=="ui":
        pipeline=["real product screen capture","deterministic overlays","edit and mix"]
        if "screen_capture" not in tools:
            blockers.append("Real screen capture unavailable; do not generate an official-looking fake UI.")
    elif kind=="chart":
        pipeline=["audited numeric source","deterministic data visualization","edit and sound"]
        if "remotion" not in tools and "ae" not in tools:
            blockers.append("Exact chart animation needs a deterministic graphics tool or comparable available pipeline.")
        if not brief.get("data_source"):
            blockers.append("Charts require real or explicitly labeled synthetic source data.")
    elif kind=="brand_character":
        pipeline=["canonical character bible","controlled rig","editorial sound"]
        if not brief.get("canonical_assets"):
            blockers.append("Official character references absent; do not invent mascot anatomy.")
        if not any(t in tools for t in ("rive","blender","ae")):
            warnings.append("No controlled rig tool available; generated character continuity remains high risk.")
    elif kind=="real_human":
        pipeline=["consented live-action","edit and dialogue","color and mix"]
        if not brief.get("consent_confirmed"):
            blockers.append("Human footage/voice requires relevant consent and rights before commercial use.")
        if "camera" not in tools:
            warnings.append("No camera production tool listed; licensed stock or approved existing footage needed.")
    elif kind=="physical_product":
        pipeline=["real product proof / macro","3D only where faithful","composition and sound"]
        if not brief.get("product_assets"):
            blockers.append("No real product reference/footage for accurate claims or packshot.")
    elif kind=="imaginary_world":
        pipeline=["original art bible","storyboard/previz","controlled or generated cinematography"]
        if not any(t in tools for t in ("blender","t2v","i2v","camera")):
            warnings.append("No capture, 3D or generative video tool available for the intended imaginary world.")
    elif kind=="typography":
        pipeline=["licensed exact font and copy","deterministic motion type","sound-design"]
        if not any(t in tools for t in ("remotion","ae")):
            warnings.append("No deterministic typography animation tool listed.")
    else:
        pipeline=["shot-by-shot truth contract","select most controllable medium per shot","edit and sound"]
    if "ffmpeg" not in tools and surface in {"reels","tiktok","shorts","youtube","event","cinema"}:
        warnings.append("FFmpeg not listed; another export pipeline must actually be available.")
    creative_focus=[GOALS[goal]]
    if goal=="awareness":
        creative_focus+=["Recognizable distinctiveness and showmanship; no automatic hard-sell CTA."]
    elif goal=="conversion":
        creative_focus+=["True offer, concrete proof, dominant objection and message-matched CTA."]
    elif goal=="art":
        creative_focus+=["Image and sound can resolve poetically without product cards or conversion metrics."]
    else:
        creative_focus+=["Story, visual action, progression, payoff and context-appropriate brand identity."]
    aspect_hint={"reels":"9:16","tiktok":"9:16","shorts":"9:16",
                 "youtube":"depends on placement","landing":"responsive/crop-safe or bespoke",
                 "event":"real display specs","internal":"needs destination specs","cinema":"delivery specs"}.get(surface)
    return {
        "status":"PASS","creative_goal":goal,"surface":surface,
        "central_visual":kind,"suggested_aspect":aspect_hint,
        "creative_priorities":creative_focus,"medium_pipeline":pipeline,
        "blockers":blockers,"warnings":warnings,
        "ready_for_commercial_publish":"NO" if blockers else "NOT_DETERMINED",
        "output_status":"PLAN_ONLY_NOT_RENDERED",
        "next_action":"Resolve P0 truth/rights/asset blockers, create storyboards with a strong middle, then render and inspect a real cut.",
        "note":"Rules route constraints; final creative direction must be judged in context, not by this router.",
    }

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("brief",type=Path)
    args=ap.parse_args(argv)
    try:
        result=route(json.loads(args.brief.read_text(encoding="utf-8")))
    except (OSError,ValueError) as exc:
        print("FAIL:",str(exc),file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())

