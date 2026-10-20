#!/usr/bin/env python3
"""Structural and release-risk lint. Not an artistic review."""
import argparse
import json
import math
from pathlib import Path

REQUIRED = ("id", "start_s", "end_s", "intent", "visual", "audio", "method", "rights", "asset_status")
ASSET_STATUSES = {"ready", "placeholder", "unconfirmed", "generated"}
RIGHTS = {"cleared", "pending", "unknown"}

def valid_number(x):
    return type(x) in (int, float) and math.isfinite(x)

def lint(document, release=False):
    errors = []
    if not isinstance(document, dict):
        return ["Root must be a JSON object"]
    fps, duration, shots = document.get("fps"), document.get("duration_s"), document.get("shots")
    if not valid_number(fps) or fps <= 0 or fps > 240:
        errors.append("fps must be a positive finite number <= 240")
    if not valid_number(duration) or duration <= 0 or duration > 86400:
        errors.append("duration_s must be between 0 and 86400")
    if not isinstance(shots, list) or not shots:
        return errors + ["shots must be a nonempty array"]
    tolerance = 1 / fps + 0.000001 if valid_number(fps) and fps > 0 else 0.034
    seen, prior_end = set(), 0.0
    for index, shot in enumerate(shots):
        mark = "shots[{}]".format(index)
        if not isinstance(shot, dict):
            errors.append(mark + ": not an object")
            continue
        for key in REQUIRED:
            if key not in shot:
                errors.append(mark + ": missing " + key)
        ident = shot.get("id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append(mark + ": nonempty id required")
        elif ident in seen:
            errors.append(mark + ": duplicated id " + ident)
        else:
            seen.add(ident)
        start, end = shot.get("start_s"), shot.get("end_s")
        if not valid_number(start) or not valid_number(end) or start < 0 or end <= start:
            errors.append(mark + ": invalid start_s/end_s")
        else:
            if abs(start - prior_end) > tolerance:
                errors.append(mark + ": gap/overlap from previous shot")
            if valid_number(duration) and end > duration + tolerance:
                errors.append(mark + ": exceeds duration")
            prior_end = end
        for key in ("intent", "visual", "audio", "method"):
            if key in shot and (not isinstance(shot[key], str) or not shot[key].strip()):
                errors.append(mark + ": " + key + " must be nonempty text")
        if shot.get("rights") not in RIGHTS:
            errors.append(mark + ": rights must be cleared/pending/unknown")
        if shot.get("asset_status") not in ASSET_STATUSES:
            errors.append(mark + ": invalid asset_status")
        if release and shot.get("rights") != "cleared":
            errors.append(mark + ": unreleased rights")
        if release and shot.get("asset_status") in {"placeholder", "unconfirmed"}:
            errors.append(mark + ": placeholder or unconfirmed asset in release")
    if valid_number(duration) and abs(prior_end - duration) > tolerance:
        errors.append("Last shot does not end at duration_s")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shotlist", type=Path)
    parser.add_argument("--release", action="store_true", help="Block pending rights and placeholders")
    args = parser.parse_args()
    try:
        doc = json.loads(args.shotlist.read_text(encoding="utf-8"))
        issues = lint(doc, args.release)
    except (OSError, ValueError, UnicodeError) as exc:
        print("FAIL:", exc)
        return 2
    if issues:
        for issue in issues:
            print("FAIL:", issue)
        return 1
    print("PASS: structural timeline/rights fields only; artistic QA is UNKNOWN")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
