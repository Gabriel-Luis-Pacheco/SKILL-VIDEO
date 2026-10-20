#!/usr/bin/env python3
"""Check asset provenance, local integrity and declared release rights.

A declared license or hash is not legal verification; human approval required.
Never follows symlinks outside the project root or fetches remote assets.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ALLOWED_KINDS = {"logo","mascot","screen_capture","footage","audio","font","vector","image","3d","other"}
RIGHTS = {"cleared","pending","unknown"}
KINDS_REQUIRING_CANON = {"logo","mascot","screen_capture"}

def check_manifest(doc, project_root=None, release=False):
    errors, warnings = [], []
    if not isinstance(doc, dict) or not isinstance(doc.get("assets"), list):
        return ["assets must be an array"], warnings
    assets = doc["assets"]
    if not assets:
        return ["assets cannot be empty"], warnings
    root = Path(project_root).resolve() if project_root else None
    seen = set()
    for index, asset in enumerate(assets):
        mark = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(mark + ": must be object")
            continue
        ident = asset.get("id")
        if not isinstance(ident, str) or not ident.strip() or ident in seen:
            errors.append(mark + ": id missing or duplicate")
        else:
            seen.add(ident)
        if asset.get("kind") not in ALLOWED_KINDS:
            errors.append(mark + ": invalid kind")
        if asset.get("rights") not in RIGHTS:
            errors.append(mark + ": invalid rights")
        if not isinstance(asset.get("source"), str) or not asset["source"].strip():
            errors.append(mark + ": source required")
        if asset.get("kind") in KINDS_REQUIRING_CANON and not asset.get("canonical"):
            (errors if release else warnings).append(mark + ": canonical origin unverified")
        if release and asset.get("rights") != "cleared":
            errors.append(mark + ": rights not cleared")
        if release and asset.get("kind") == "screen_capture" and asset.get("truth") != "verified":
            errors.append(mark + ": screen capture product truth not verified")
        relpath = asset.get("path")
        if not isinstance(relpath, str) or not relpath.strip():
            (errors if release else warnings).append(mark + ": local path missing; content unavailable for review")
            continue
        pp = Path(relpath)
        if pp.is_absolute() or ".." in pp.parts:
            errors.append(mark + ": local path must be relative and cannot traverse")
            continue
        if root is None:
            warnings.append(mark + ": no --project-root, file existence/hash NOT CHECKED")
            continue
        target = (root / pp).resolve()
        if not target.is_relative_to(root):
            errors.append(mark + ": path escapes project root")
            continue
        if not target.is_file() or target.stat().st_size == 0:
            (errors if release else warnings).append(mark + ": asset missing or empty")
            continue
        wanted = asset.get("sha256")
        if wanted:
            if not isinstance(wanted, str) or len(wanted) != 64 or any(c not in "0123456789abcdefABCDEF" for c in wanted):
                errors.append(mark + ": sha256 must be 64 hexadecimal characters")
            else:
                sha = hashlib.file_digest(target.open("rb"), "sha256").hexdigest()
                if sha.lower() != wanted.lower():
                    errors.append(mark + ": sha256 mismatch")
        elif release:
            warnings.append(mark + ": no hash; not automatically verifiable across machines")
    warnings.append("Declared rights cannot prove consent, license scope, official brand canon or product authenticity.")
    return errors, warnings

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--project-root", type=Path)
    ap.add_argument("--release", action="store_true")
    args = ap.parse_args(argv)
    try:
        doc = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors, warnings = check_manifest(doc, args.project_root, args.release)
    except (OSError, ValueError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        return 2
    for w in warnings: print("WARN:", w)
    for e in errors: print("FAIL:", e)
    if errors: return 1
    print("PASS: asset manifest declared fields; actual rights/visuals UNKNOWN")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
