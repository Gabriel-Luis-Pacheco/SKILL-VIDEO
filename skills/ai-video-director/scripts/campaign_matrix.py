#!/usr/bin/env python3
"""Validate one-variable-at-a-time ad experiments with locked visual/target fields.

Cannot validate semantic hook/CTA message match, statistical power or conversion.
"""
import argparse
import json
from pathlib import Path
import sys

FIELDS = ("hook", "benefit", "proof", "cta", "offer")
LOCKED = ("brand_id", "asset_ids", "theme", "layout_id", "motion_id", "landing_url", "audience_id")
NEEDED = FIELDS + LOCKED

def check_matrix(data):
    errors, warnings = [], []
    if not isinstance(data, dict):
        return ["root must be an object"], []
    base, variants = data.get("baseline"), data.get("variants")
    if not isinstance(base, dict):
        return ["baseline must be an object"], []
    if not isinstance(variants, list) or not variants or len(variants) > 1000:
        return ["variants must be a nonempty array of <=1000 entries"], []
    for key in NEEDED:
        if key not in base:
            errors.append(f"baseline: missing {key}")
        elif base[key] in (None, "", [], {}):
            errors.append(f"baseline: empty {key}")
    ids = set()
    for i, v in enumerate(variants):
        pos = f"variants[{i}]"
        if not isinstance(v, dict):
            errors.append(pos + ": must be object")
            continue
        ident = v.get("id")
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            errors.append(pos + ": missing or duplicate id")
        else:
            ids.add(ident)
        field = v.get("changed_field")
        if field not in FIELDS:
            errors.append(pos + ": changed_field must be one of " + ", ".join(FIELDS))
            continue
        for required in NEEDED:
            if required not in v:
                errors.append(pos + ": missing " + required)
        if any(k not in v or k not in base for k in NEEDED):
            continue
        changed = [k for k in FIELDS if v[k] != base[k]]
        if changed != [field]:
            errors.append(pos + ": actual changes " + str(changed) + " do not match " + field)
        if any(v[k] != base[k] for k in LOCKED):
            errors.append(pos + ": brand, assets, animation, target or audience changed")
        if any(not isinstance(v[k], str) or not v[k].strip() for k in FIELDS):
            errors.append(pos + ": copy fields must be nonempty text")
        if not isinstance(v.get("hypothesis"), str) or not v["hypothesis"].strip():
            errors.append(pos + ": missing hypothesis")
        if field in ("proof", "offer") and (not isinstance(v.get("evidence"), str) or not v["evidence"].strip()):
            errors.append(pos + ": proof/offer change needs evidence reference")
        if field == "hook":
            warnings.append(pos + ": review hook/CTA/landing message match manually")
        if field == "cta":
            warnings.append(pos + ": review CTA destination and user expectation manually")
    warnings.append("No real campaign metrics or creative quality can be inferred from this matrix.")
    return errors, warnings

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("matrix", type=Path)
    args = ap.parse_args(argv)
    try:
        errors, warnings = check_matrix(json.loads(args.matrix.read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        print("FAIL:", exc, file=sys.stderr)
        return 2
    for warning in warnings:
        print("WARN:", warning)
    for error in errors:
        print("FAIL:", error)
    if errors:
        return 1
    print("PASS: controlled fields only; creative/causal validity UNKNOWN")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
