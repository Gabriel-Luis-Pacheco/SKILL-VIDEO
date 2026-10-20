#!/usr/bin/env python3
"""FFprobe-based technical QC; never claims to have watched/heard a video."""
import argparse
import json
import math
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

def inspect(path, duration=None, aspect=None, require_audio=False):
    path = Path(path)
    if not path.is_file() or not path.stat().st_size:
        return {"status": "FAIL", "issues": ["missing or empty file"], "unknown": ["creative quality"]}
    if shutil.which("ffprobe") is None:
        return {"status": "UNKNOWN", "issues": ["ffprobe unavailable"], "unknown": ["all media checks"]}
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate,pix_fmt,color_range,color_space,color_transfer,color_primaries,sample_rate,channels,sample_aspect_ratio", "-of", "json", str(path)]
    try:
        run = subprocess.run(command, check=True, text=True, capture_output=True, timeout=45)
        info = json.loads(run.stdout)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError) as exc:
        return {"status": "FAIL", "issues": [str(exc)], "unknown": ["creative quality"]}
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    issues = []
    if not videos:
        issues.append("video stream missing")
    if require_audio and not audios:
        issues.append("audio stream required but missing")
    actual = float(info.get("format", {}).get("duration", 0) or 0)
    if not math.isfinite(actual) or actual <= 0:
        issues.append("invalid duration")
    if duration is not None and abs(actual - duration) > max(.2, duration * .015):
        issues.append("duration differs from target")
    fps = 0.
    if videos:
        v = videos[0]
        if aspect:
            w,h = v.get("width"),v.get("height")
            expected = {"9:16":9/16,"4:5":4/5,"16:9":16/9,"1:1":1}.get(aspect)
            if expected is None:
                issues.append("unsupported requested aspect")
            elif not w or not h or abs(w/h - expected) > .03:
                issues.append("aspect ratio differs from target")
        try:
            fps = float(Fraction(v.get("avg_frame_rate", "0/1")))
        except (TypeError, ValueError, ZeroDivisionError):
            issues.append("invalid fps")
        if fps <= 0:
            issues.append("fps nonpositive")
    return {"status": "FAIL" if issues else "PASS", "issues": issues, "metadata": {"duration_s":actual,"fps":fps,"video_streams":len(videos),"audio_streams":len(audios),"codec":videos[0].get("codec_name") if videos else None,
        "pixel_format":videos[0].get("pix_fmt") if videos else None,
        "color_range":videos[0].get("color_range") if videos else None,
        "color_primaries":videos[0].get("color_primaries") if videos else None,
        "color_transfer":videos[0].get("color_transfer") if videos else None,
        "color_space":videos[0].get("color_space") if videos else None,
        "audio_sample_rate":audios[0].get("sample_rate") if audios else None,
        "audio_channels":audios[0].get("channels") if audios else None}, "unknown": ["visual craft", "sound intelligibility", "rights", "conversion", "brand fidelity"]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file",type=Path)
    ap.add_argument("--duration",type=float)
    ap.add_argument("--aspect",choices=["9:16","4:5","16:9","1:1"])
    ap.add_argument("--require-audio",action="store_true")
    args = ap.parse_args()
    result = inspect(args.file,args.duration,args.aspect,args.require_audio)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result["status"] == "FAIL" else 2 if result["status"] == "UNKNOWN" else 0

if __name__ == "__main__":
    raise SystemExit(main())
