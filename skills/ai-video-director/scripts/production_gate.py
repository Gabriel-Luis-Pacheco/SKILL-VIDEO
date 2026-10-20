#!/usr/bin/env python3
"""Cross-file production preflight.

PREVIEW validates declared dependencies. RELEASE additionally demands
cleared local assets, consistent references and an actual verified MP4.
No command or untrusted media is executed except ffprobe on local files.
"""
import argparse
import json
from pathlib import Path
import sys
from timeline_compile import compile_storyboard, PlanError
from asset_preflight import check_manifest
from captions_lint import lint_srt
from video_qc import inspect as inspect_media

def run_gate(storyboard, manifest, *, project_root=None, release=False,
             captions_text=None, video_path=None, require_audio=False):
    errors, warnings = [], []
    try:
        timeline = compile_storyboard(storyboard)
    except (PlanError, ValueError) as exc:
        return {"status":"FAIL","errors":["timeline: " + str(exc)],"warnings":[],"checks":{"timeline":"FAIL"}}
    asset_errors, asset_warnings = check_manifest(manifest, project_root=project_root, release=release)
    errors.extend(asset_errors)
    warnings.extend(asset_warnings)
    registered = {a.get("id") for a in manifest.get("assets", []) if isinstance(a, dict)} if isinstance(manifest, dict) else set()
    for shot in timeline["scenes"]:
        for asset_id in shot.get("source_assets", []):
            if asset_id not in registered:
                entry = f"scene {shot['id']}: source asset {asset_id!r} absent from manifest"
                (errors if release else warnings).append(entry)
    if captions_text is not None:
        e, w = lint_srt(captions_text)
        errors.extend("subtitle: " + x for x in e)
        warnings.extend("subtitle: " + x for x in w)
    media_status = "UNKNOWN"
    media_detail = None
    if video_path is not None:
        media_detail = inspect_media(video_path, duration=timeline["encoded_seconds"], aspect=timeline["aspect"], require_audio=require_audio)
        media_status = media_detail.get("status","UNKNOWN")
        if media_status == "FAIL":
            errors.extend("media: " + x for x in media_detail.get("issues",[]))
        elif media_status != "PASS" and release:
            errors.append("media cannot be verified for RELEASE")
    elif release:
        errors.append("release requested but no rendered video file supplied")
    else:
        warnings.append("No rendered video provided; visual/sound/master checks UNKNOWN")
    checks = {"timeline":"PASS","assets":"FAIL" if asset_errors else "DECLARED",
              "captions":"NOT_PROVIDED" if captions_text is None else "FAIL" if any(x.startswith("subtitle: ") for x in errors) else "STRUCTURAL_PASS",
              "media":media_status,"creative_quality":"UNKNOWN","commercial_effectiveness":"UNKNOWN","real_rights":"UNKNOWN"}
    if release and errors:
        checks["release"]="FAIL"
    elif release and not errors:
        checks["release"]="TECHNICAL_PASS_ONLY"
    else:
        checks["release"]="NOT_REQUESTED"
    return {"status":"FAIL" if errors else "PASS", "errors":errors, "warnings":warnings,
            "checks":checks, "timeline_frames":timeline["duration_in_frames"],
            "encoded_seconds":timeline["encoded_seconds"],"media":media_detail}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("storyboard",type=Path)
    p.add_argument("asset_manifest",type=Path)
    p.add_argument("--project-root",type=Path)
    p.add_argument("--release",action="store_true")
    p.add_argument("--video",type=Path)
    p.add_argument("--captions",type=Path)
    p.add_argument("--require-audio",action="store_true")
    p.add_argument("--report",type=Path)
    args=p.parse_args(argv)
    try:
        sb=json.loads(args.storyboard.read_text(encoding="utf-8"))
        manifest=json.loads(args.asset_manifest.read_text(encoding="utf-8"))
        srt=args.captions.read_text(encoding="utf-8-sig") if args.captions else None
        result=run_gate(sb,manifest,project_root=args.project_root,release=args.release,
                        captions_text=srt,video_path=args.video,require_audio=args.require_audio)
    except (OSError, ValueError) as exc:
        print("FAIL:",exc,file=sys.stderr);return 2
    result_json=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.report:
        args.report.write_text(result_json,encoding="utf-8")
    print(result_json,end="")
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
