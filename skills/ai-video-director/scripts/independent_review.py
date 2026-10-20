#!/usr/bin/env python3
"""Audit declared HUMAN film reviews without fabricating artistic scores.

Requires evidence paths/timecodes. Does not certify that named humans
actually watched/listened; identity and independence remain DECLARED.
"""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import sys

DIMENSIONS=("truth","brand","concept","story","art","motion","editing","sound","clarity","payoff")
GATES=("P0","P1","P2","NONE")

def evaluate(data):
    if not isinstance(data,dict):return {"status":"FAIL","errors":["root must be object"]}
    errors=[]
    film=data.get("film")
    if not isinstance(film,dict) or not isinstance(film.get("file"),str) or not film["file"].strip():
        errors.append("film.file required")
    reviewers=data.get("reviewers")
    if not isinstance(reviewers,list) or not reviewers or len(reviewers)>30:
        errors.append("reviewers must be 1–30")
        return {"status":"FAIL","errors":errors}
    ids=set()
    observations=defaultdict(list)
    critical=[]
    for i,rev in enumerate(reviewers):
        p=f"reviewers[{i}]"
        if not isinstance(rev,dict):
            errors.append(p+" must be object");continue
        rid=rev.get("id")
        if not isinstance(rid,str) or not rid.strip() or rid in ids:
            errors.append(p+" unique id required")
        else:ids.add(rid)
        if rev.get("review_scope")!="full_video_and_audio":
            errors.append(p+" must have watched full video and listened to audio")
        if rev.get("reviewer_type") not in ("independent_human","internal_human","agent_self_review"):
            errors.append(p+" reviewer_type must disclose independence")
        grades=rev.get("ratings")
        if not isinstance(grades,dict) or set(grades)!=set(DIMENSIONS):
            errors.append(p+" ratings must cover all dimensions")
            continue
        for key,value in grades.items():
            if isinstance(value,bool) or not isinstance(value,int) or not 0<=value<=4:
                errors.append(p+" invalid rating "+key)
            else:observations[key].append(value)
        evidence=rev.get("observations")
        if not isinstance(evidence,list) or not evidence:
            errors.append(p+" needs timecoded observations")
            continue
        for j,item in enumerate(evidence):
            q=p+f".observations[{j}]"
            if not isinstance(item,dict):
                errors.append(q+" must be object");continue
            time_s=item.get("time_s")
            if isinstance(time_s,bool) or not isinstance(time_s,(int,float)) or not math.isfinite(time_s) or time_s<0:
                errors.append(q+" invalid time_s")
            if not isinstance(item.get("note"),str) or not item["note"].strip():
                errors.append(q+" note required")
            if item.get("severity") not in GATES:
                errors.append(q+" invalid severity")
            elif item["severity"] in ("P0","P1"):
                critical.append({"reviewer":rid,"time_s":time_s,"severity":item["severity"],"note":item.get("note")})
    if errors:return {"status":"FAIL","errors":errors}
    independent=[r for r in reviewers if r["reviewer_type"]=="independent_human"]
    means={k:round(sum(v)/len(v),3) for k,v in observations.items()}
    ranges={k:(max(v)-min(v)) for k,v in observations.items()}
    return {
        "status":"PASS",
        "review_claim":"DECLARED_ONLY_NOT_IDENTITY_VERIFIED",
        "independent_reviewer_count":len(independent),
        "blind_quality_claim":"NOT_SUPPORTED" if len(independent)<2 else "POTENTIALLY_ELIGIBLE_REQUIRES_PROTOCOL_AUDIT",
        "average_ordinal_ratings_descriptive":means,
        "inter_reviewer_range":ranges,
        "critical_observations":critical,
        "creative_release_recommendation":"BLOCK" if critical else "MANUAL_SIGNOFF_REQUIRED",
        "limits":[
            "Ratings are declared opinions, not ground truth or statistical proof of creative excellence.",
            "Independent identity, blinding and actual playback are not verified by this tool.",
            "An apparently high score without P0/P1 does not replace legal, brand, market or accessibility review.",
            "Compare two films only under the same brief/assets/tools, with truly blind human review.",
        ],
    }

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("review",type=Path)
    args=ap.parse_args(argv)
    try:res=evaluate(json.loads(args.review.read_text(encoding="utf-8")))
    except (OSError,ValueError) as exc:
        print("FAIL:",str(exc),file=sys.stderr);return 2
    print(json.dumps(res,indent=2,ensure_ascii=False))
    return 0 if res["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
