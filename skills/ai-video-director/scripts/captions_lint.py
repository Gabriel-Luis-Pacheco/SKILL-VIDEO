#!/usr/bin/env python3
"""Read SRT blocks and detect invalid timing/overlaps with legibility warnings.

Checks are heuristic; must listen to the actual dialogue and watch subtitles.
"""
import argparse
import re
from pathlib import Path
import sys

STAMP = re.compile(r"^(\d{2,}):(\d{2}):(\d{2})[,\.](\d{3})$")
TIMELINE = re.compile(r"^\s*(\S+)\s+-->\s+(\S+)(?:\s+.*)?$")
TAGS = re.compile(r"<[^>]*>")

def stamp_ms(s):
    m = STAMP.match(s)
    if not m:
        raise ValueError("timestamp must be HH:MM:SS,mmm")
    hh, mm, ss, ms = map(int, m.groups())
    if mm >= 60 or ss >= 60:
        raise ValueError("minutes/seconds out of range")
    return (((hh * 60 + mm) * 60) + ss) * 1000 + ms

def lint_srt(content, max_cps=25, max_line=48):
    issues, warnings = [], []
    if not isinstance(content, str) or not content.strip():
        return ["no subtitle content"], []
    chunks = re.split(r"\n\s*\n", content.replace("\r\n","\n").replace("\r","\n").strip())
    last_end = -1
    cues = []
    for i, chunk in enumerate(chunks):
        lines = [ln.rstrip() for ln in chunk.split("\n")]
        if lines and lines[0].isdigit():
            lines = lines[1:]
        if len(lines) < 2:
            issues.append(f"cue {i+1}: missing time or text")
            continue
        match = TIMELINE.match(lines[0])
        if not match:
            issues.append(f"cue {i+1}: malformed time line")
            continue
        try:
            start,end = stamp_ms(match.group(1)),stamp_ms(match.group(2))
        except ValueError as exc:
            issues.append(f"cue {i+1}: {exc}")
            continue
        if end <= start:
            issues.append(f"cue {i+1}: negative or zero duration")
        if start < last_end:
            issues.append(f"cue {i+1}: overlaps previous cue")
        last_end = max(last_end, end)
        visible = [TAGS.sub("", s).strip() for s in lines[1:]]
        if not any(visible):
            issues.append(f"cue {i+1}: empty text")
        max_actual = max(map(len, visible), default=0)
        if max_actual > max_line:
            warnings.append(f"cue {i+1}: {max_actual} characters on one line (> {max_line}); inspect in layout")
        chars = sum(len(t) for t in visible)
        seconds = (end-start)/1000
        if seconds > 0 and chars/seconds > max_cps:
            warnings.append(f"cue {i+1}: reading speed {chars/seconds:.1f} cps > {max_cps}; review manually")
        cues.append({"start_ms":start,"end_ms":end,"text":" ".join(visible)})
    if not cues: issues.append("no parsed cues")
    return issues, warnings

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("srt", type=Path)
    ap.add_argument("--max-cps",type=float,default=25)
    ap.add_argument("--max-line",type=int,default=48)
    ap.add_argument("--strict",action="store_true",help="Fail on legibility warnings, not just structure errors")
    args=ap.parse_args(argv)
    if args.max_cps <= 0 or args.max_line <= 0:
        print("FAIL: positive limits required",file=sys.stderr);return 2
    try:
        errs, warns = lint_srt(args.srt.read_text(encoding="utf-8-sig"),args.max_cps,args.max_line)
    except OSError as exc:
        print("FAIL:",exc,file=sys.stderr);return 2
    for w in warns: print("WARN:",w)
    for e in errs: print("FAIL:",e)
    if errs or (args.strict and warns):return 1
    print("PASS: SRT syntax/timing; actual audio sync and visual legibility UNKNOWN")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
