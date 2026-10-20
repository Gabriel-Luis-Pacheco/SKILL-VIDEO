#!/usr/bin/env python3
"""Descriptive campaign reporting with input checks and uncertainty intervals.

This does NOT infer causality, calculate statistical significance, or crown a
"winning" creative. Non-random, repeat viewers and platform attribution
invalidate simple binomial assumptions; interpret intervals as descriptive.
All metrics must come from a supplied real data export.
"""
import argparse
import json
import math
from pathlib import Path
import sys

COUNTS = ("impressions", "views_3s", "clicks", "leads", "purchases")
MONEY = ("spend",)

def nonnegative(value, integer=False):
    if isinstance(value, bool) or not isinstance(value, (float, int)):
        return False
    if not math.isfinite(value) or value < 0:
        return False
    return not integer or isinstance(value, int)

def percent(num, denom):
    return round(100.0 * num / denom, 3) if denom else None

def wilson(k, n, z=1.959963984540054):
    """Wilson 95% interval for a binomial proportion; return percentages."""
    if not n:
        return None
    p=k/n
    q=z*z
    center=(p+q/(2*n))/(1+q/n)
    radius=z*math.sqrt(p*(1-p)/n+q/(4*n*n))/(1+q/n)
    return [round(100*(center-radius),3), round(100*(center+radius),3)]

def money_per(spend, conversions):
    return round(spend/conversions, 4) if conversions else None

def analyze(data):
    errors=[]
    if not isinstance(data, dict):
        return {"status":"FAIL","errors":["root must be object"]}
    platform=data.get("platform")
    period=data.get("period")
    variants=data.get("variants")
    currency=data.get("currency","BRL")
    if not isinstance(platform,str) or not platform.strip():
        errors.append("platform is required")
    if not isinstance(period,str) or not period.strip():
        errors.append("period is required; use ISO date range or source export period")
    if not isinstance(currency,str) or not currency.isalpha() or len(currency)!=3:
        errors.append("currency must be a three-character currency code")
    if not isinstance(variants,list) or not 2<=len(variants)<=100:
        errors.append("variants must be an array of 2–100 entries")
        return {"status":"FAIL","errors":errors}
    seen=set()
    rows=[]
    for index,v in enumerate(variants):
        prefix=f"variants[{index}]"
        if not isinstance(v,dict):
            errors.append(prefix+" must be object")
            continue
        ident=v.get("id")
        if not isinstance(ident,str) or not ident.strip() or ident in seen:
            errors.append(prefix+" id missing or duplicated")
        else: seen.add(ident)
        for field in COUNTS:
            if not nonnegative(v.get(field),integer=True):
                errors.append(prefix+" "+field+" must be nonnegative integer")
        if not nonnegative(v.get("spend")):
            errors.append(prefix+" spend must be nonnegative finite number")
        if any(not nonnegative(v.get(field),integer=True) for field in COUNTS) or not nonnegative(v.get("spend")):
            continue
        impressions, views, clicks, leads, purchases = (v[k] for k in COUNTS)
        if any(n>impressions for n in (views,clicks,leads,purchases)):
            errors.append(prefix+" an event count exceeds impressions")
        if purchases>leads:
            # Not necessarily impossible: some stores attribute purchases without lead event.
            pass
        if not impressions and v["spend"]>0:
            errors.append(prefix+" has spend without impressions")
        if not impressions and any((views,clicks,leads,purchases)):
            errors.append(prefix+" has event counts without impressions")
        rows.append({
            "id":ident,
            "impressions":impressions,"views_3s":views,"clicks":clicks,
            "leads":leads,"purchases":purchases,"spend":v["spend"],
            "view_3s_pct":percent(views,impressions),
            "click_through_pct":percent(clicks,impressions),
            "lead_per_click_pct":percent(leads,clicks) if leads<=clicks else None,
            "purchase_per_click_pct":percent(purchases,clicks) if purchases<=clicks else None,
            "click_through_wilson_95_pct":wilson(clicks,impressions),
            "cost_per_click":money_per(v["spend"],clicks),
            "cost_per_lead":money_per(v["spend"],leads),
            "cost_per_purchase":money_per(v["spend"],purchases),
        })
    if errors: return {"status":"FAIL","errors":errors}
    cautions=[
        "DESCRIPTIVE ONLY: No causal lift, statistically significant winner, ROI or ROAS inferred.",
        "Wilson intervals assume independent binomial impressions; they may be misleading with repeat viewers/auction interference.",
        "Purchase and lead attribution windows, targeting, bids, placements, creative fatigue and spend can confound comparisons.",
        "Verify exported source, date range, funnel event semantics, attribution, sample size and experimental design.",
        "Costs are in the reported currency; do not interpret them as profit or customer lifetime value.",
    ]
    if any(r["lead_per_click_pct"] is None and r["leads"]>0 for r in rows):
        cautions.append("Lead counts may not be a subset of clicks; lead/click rate withheld.")
    if any(r["purchase_per_click_pct"] is None and r["purchases"]>0 for r in rows):
        cautions.append("Purchase counts may not be a subset of clicks; purchase/click rate withheld.")
    return {"status":"PASS","platform":platform,"period":period,"currency":currency,
        "analysis_type":"descriptive_only","variants":rows,"limitations":cautions,
        "winner":"NOT_DETERMINED","causal_effect":"UNKNOWN"}

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("data",type=Path)
    ap.add_argument("-o","--output",type=Path)
    args=ap.parse_args(argv)
    try:
        data=json.loads(args.data.read_text(encoding="utf-8"))
        result=analyze(data)
    except (ValueError,OSError) as exc:
        print("FAIL:",str(exc),file=sys.stderr)
        return 2
    payload=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:print(payload,end="")
    return 0 if result["status"]=="PASS" else 1

if __name__=="__main__":
    raise SystemExit(main())
