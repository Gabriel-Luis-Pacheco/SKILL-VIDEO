#!/usr/bin/env python3
"""Scaffold a video production without inventing product truth or source assets.

Creates a clean, editable project only. Never overwrites an existing directory.
The storyboard intentionally starts empty (cannot pass a release preflight).
"""
import argparse
import json
from pathlib import Path
import re
import sys

GOALS={"awareness","consideration","conversion","retention","education","art","launch"}
SURFACES={"reels","tiktok","shorts","youtube","landing","event","internal","cinema"}

def build(out,title,brand,goal,surface):
    out=Path(out)
    if not isinstance(title,str) or not title.strip() or not isinstance(brand,str) or not brand.strip():
        raise ValueError("nonempty title and brand required")
    if goal not in GOALS or surface not in SURFACES:
        raise ValueError("invalid goal/surface")
    if out.exists() or out.is_symlink():
        raise FileExistsError("Destination already exists: "+str(out))
    if not out.parent.is_dir():
        raise ValueError("Parent directory must already exist")
    out.mkdir()
    for sub in ("source-assets","captures","storyboards","animatics","renders","reviews","deliverables"):
        (out/sub).mkdir()
    brief={
        "schema":"video-os-production-v4",
        "project":title,"brand":brand,"goal":goal,"surface":surface,
        "audience":"UNKNOWN","product_truth":"unknown","truth_sources":[],
        "brand_assets":"NOT PROVIDED","canonical_character":"UNKNOWN",
        "offer":"NOT VERIFIED","cta_destination":"UNKNOWN",
        "visual_mechanism":"NOT DECIDED","first_frame":"NOT DESIGNED",
        "middle_scene":"NOT DESIGNED","payoff":"NOT DESIGNED",
        "motion_language":"NOT DESIGNED","sound_language":"NOT DESIGNED",
        "status":"DRAFT_NOT_RENDERED"
    }
    storyboard={
        "title":title,"fps":30,"aspect":"9:16" if surface in {"reels","tiktok","shorts"} else "16:9",
        "scenes":[],
        "_readme":"DRAFT. Fill real scenes before timeline_compile; no fabricated source assets."
    }
    assets={"schema":"video-os-assets-v1","assets":[]}
    for path,data in (
        ("brief.json",brief),("storyboard.json",storyboard),
        ("assets.json",assets)
    ):
        (out/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (out/"README.md").write_text(
        "# "+title+"\n\n"
        "**STATUS: DRAFT / NOT RENDERED.** This folder contains no filmed scenes, sound, claims or release rights.\n\n"
        "1. Verify product/brand/rights. Replace the unknown fields in brief.json.\n"
        "2. Explore creative treatments; choose one with a strong beginning, memorable middle, and payoff.\n"
        "3. Capture product UI or licensed real-world materials into source-assets/ and captures/.\n"
        "4. Write storyboard.json with real scene IDs, times, sounds and asset IDs. Register them in assets.json.\n"
        "5. Use timeline_compile.py and asset_preflight.py. Make a full-film animatic.\n"
        "6. Produce shots; assemble and mix the final video; export per-destination composition.\n"
        "7. Run video_qc.py, evidence_capture.py and production_gate.py with the **actual** MP4.\n"
        "8. Review the whole film including sound. Publish only after rights and human/creative checks.\n\n"
        "Never claim a fictitious script, project scaffold or metadata check is finished film.\n",
        encoding="utf-8"
    )
    return out

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,required=True)
    ap.add_argument("--title",required=True)
    ap.add_argument("--brand",required=True)
    ap.add_argument("--goal",choices=sorted(GOALS),required=True)
    ap.add_argument("--surface",choices=sorted(SURFACES),required=True)
    args=ap.parse_args(argv)
    try:out=build(args.out,args.title,args.brand,args.goal,args.surface)
    except (ValueError,OSError) as exc:
        print("FAIL:",str(exc),file=sys.stderr);return 1
    print("CREATED DRAFT (NOT RENDERED):",out)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
