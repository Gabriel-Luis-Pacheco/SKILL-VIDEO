#!/usr/bin/env python3
"""Check internal references and minimal structure of the installed skill."""
import argparse
import re
from pathlib import Path

def validate_skill(root):
    root = Path(root)
    errors = []
    skill = root / "SKILL.md"
    vault = root / "examples" / "original-script-vault.md"
    atlas = root / "references" / "30-campaign-atlas.md"
    if not skill.is_file():
        return ["missing SKILL.md"]
    content = skill.read_text(encoding="utf-8")
    for field in ("name: ai-video-director", "version: \"4.0.0\""):
        if field not in content:
            errors.append("missing metadata: " + field)
    for link in sorted(set(re.findall(r"(?:references|examples)/[A-Za-z0-9._-]+\.(?:md|tsx)", content))):
        if not (root / link).is_file():
            errors.append("broken SKILL.md link: " + link)
    if not vault.is_file():
        errors.append("missing example vault")
    else:
        count = len(re.findall(r"(?m)^## [0-9]{2}\. ", vault.read_text(encoding="utf-8")))
        if count < 24:
            errors.append("expected >=24 distinct example scripts, got " + str(count))
    for needed in ("62-brand-memory-and-direct-response.md","63-world-class-editing-sound-playbook.md",
                   "64-motion-3d-and-character-craft.md","65-creative-quality-control-and-learning-loop.md",
                   "57-observed-visual-review.md","58-studio-creative-brain.md","59-generative-shot-supervision.md",
                   "60-directors-cut-review.md","61-creative-budget-router.md",
                   "44-top-10-skills-comparison.md", "45-production-pipeline.md",
                   "46-type-color-and-sound.md", "47-attention-and-experiments.md",
                   "48-postproduction-and-media-qa.md", "49-frame-evidence.md",
                   "50-motion-language-contract.md"):
        if not (root / "references" / needed).is_file():
            errors.append("missing specialist reference: " + needed)
    for tool in ("timeline_compile.py", "campaign_matrix.py", "asset_preflight.py",
                 "captions_lint.py", "production_gate.py", "evidence_capture.py", "campaign_results.py",
                 "independent_review.py", "brief_router.py"):
        if not (root / "scripts" / tool).is_file():
            errors.append("missing production validator: " + tool)
    if not (root / "examples/rendered-proof/render.py").is_file():
        errors.append("missing real motion render example")
    if not atlas.is_file():
        errors.append("missing atlas")
    else:
        count = len(re.findall(r"(?m)^## [^\n]+", atlas.read_text(encoding="utf-8")))
        if count < 16:
            errors.append("expected >=16 case studies, got " + str(count))
    for file in (root / "references").glob("*.md"):
        if not file.read_text(encoding="utf-8").strip():
            errors.append("empty reference: " + file.name)
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_skill(args.root)
    for issue in errors:
        print("FAIL:", issue)
    if errors:
        return 1
    print("PASS: references, metadata and minimum library coverage. Not creative validation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
