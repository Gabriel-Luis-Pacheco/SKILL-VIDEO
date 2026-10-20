#!/usr/bin/env python3
"""Turn a semantic storyboard into a drift-free, integer-frame scene plan.

This validates scene ordering/duration only. It cannot prove visual quality.
No network, imports from third parties, files executed, or subprocesses.
"""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import sys

ALLOWED_ASPECTS = {"9:16", "4:5", "1:1", "16:9"}
ALLOWED_METHODS = {
    "SCREEN_CAPTURE", "LIVE_ACTION", "MOTION_2D", "MOTION_3D",
    "GENERATIVE_VIDEO", "HYBRID", "STILL", "DOCUMENTARY",
}
MIN_FIELDS = ("id", "seconds", "role", "visual", "sound", "render_method")

class PlanError(ValueError):
    pass

def decimal(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise PlanError(f"{name}: expected positive number")
    try:
        num = Decimal(str(value))
    except InvalidOperation as exc:
        raise PlanError(f"{name}: invalid number") from exc
    if not num.is_finite() or num <= 0:
        raise PlanError(f"{name}: number must be positive and finite")
    return num

def frame_round(value):
    return int(value.to_integral_value(rounding=ROUND_HALF_UP))

def compile_storyboard(doc):
    if not isinstance(doc, dict):
        raise PlanError("Root must be an object")
    if doc.get("aspect") not in ALLOWED_ASPECTS:
        raise PlanError("aspect must be one of " + ", ".join(sorted(ALLOWED_ASPECTS)))
    if not isinstance(doc.get("title"), str) or not doc["title"].strip():
        raise PlanError("title required")
    fps = decimal(doc.get("fps"), "fps")
    if fps > 240:
        raise PlanError("fps exceeds 240")
    scenes = doc.get("scenes")
    if not isinstance(scenes, list) or not scenes or len(scenes) > 500:
        raise PlanError("scenes must be 1–500 items")
    if "target_seconds" in doc:
        target = decimal(doc["target_seconds"], "target_seconds")
    else:
        target = None
    previous_end = 0
    elapsed = Decimal(0)
    compiled = []
    ids = set()
    for idx, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            raise PlanError(f"scene[{idx}] must be object")
        missing = [key for key in MIN_FIELDS if key not in scene]
        if missing:
            raise PlanError(f"scene[{idx}]: missing {', '.join(missing)}")
        ident = scene["id"]
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            raise PlanError(f"scene[{idx}]: id missing or duplicated")
        ids.add(ident)
        for field in ("role", "visual", "sound"):
            if not isinstance(scene[field], str) or not scene[field].strip():
                raise PlanError(f"scene[{idx}]: empty {field}")
        if scene["render_method"] not in ALLOWED_METHODS:
            raise PlanError(f"scene[{idx}]: unsupported render_method")
        if "source_assets" in scene and (not isinstance(scene["source_assets"], list) or
            any(not isinstance(v, str) or not v.strip() for v in scene["source_assets"])):
            raise PlanError(f"scene[{idx}]: source_assets must be list of IDs")
        duration = decimal(scene["seconds"], f"scene[{idx}].seconds")
        elapsed += duration
        end_frame = frame_round(elapsed * fps)
        if end_frame <= previous_end:
            raise PlanError(f"scene[{idx}]: duration under 1 frame at selected fps")
        length = end_frame - previous_end
        compiled.append({
            "id": ident, "role": scene["role"], "start_frame": previous_end,
            "end_frame_exclusive": end_frame, "duration_in_frames": length,
            "start_seconds_encoded": float(Decimal(previous_end) / fps),
            "end_seconds_encoded": float(Decimal(end_frame) / fps),
            "visual": scene["visual"], "sound": scene["sound"],
            "render_method": scene["render_method"],
            "source_assets": scene.get("source_assets", []),
            "overlay_text": scene.get("overlay_text", ""),
            "checkpoints": sorted({previous_end, previous_end + length // 2, end_frame - 1}),
        })
        previous_end = end_frame
    if target is not None and abs(elapsed - target) > Decimal("0.000001"):
        raise PlanError("scene durations do not sum to target_seconds")
    return {
        "schema": "video-os-compiled-v1", "title": doc["title"],
        "fps": float(fps), "aspect": doc["aspect"],
        "requested_seconds": float(elapsed), "duration_in_frames": previous_end,
        "encoded_seconds": float(Decimal(previous_end) / fps),
        "scenes": compiled,
        "warnings": ["Storyboard is structurally valid; assets, transitions, copy, visual craft and audio remain UNVERIFIED."],
    }

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("storyboard", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    args = ap.parse_args(argv)
    try:
        source = json.loads(args.storyboard.read_text(encoding="utf-8"))
        result = compile_storyboard(source)
    except (ValueError, OSError) as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    body = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
        print("PASS: " + str(args.output) + " (timing only)")
    else:
        print(body, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
