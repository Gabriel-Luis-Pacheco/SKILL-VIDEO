#!/usr/bin/env python3
"""Video signal QC: actual decoded black/freeze/silence intervals, for review.

Alerts are NOT objective artistic defects: long holds, black fades and
silence can be intentional. Requires ffmpeg/ffprobe; checks at most first N
seconds (default 120), never evaluates visual craft or audio perception.
"""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

BLACK=re.compile(r"black_start:([-\d.]+)\s+black_end:([-\d.]+)\s+black_duration:([-\d.]+)")
FREEZE_START=re.compile(r"freeze_start:\s*([-\d.]+)")
FREEZE_END=re.compile(r"freeze_end:\s*([-\d.]+)\s*\|\s*freeze_duration:\s*([-\d.]+)")
SILENCE_START=re.compile(r"silence_start:\s*([-\d.]+)")
SILENCE_END=re.compile(r"silence_end:\s*([-\d.]+)\s*\|\s*silence_duration:\s*([-\d.]+)")

def parse_intervals(log, kind):
    if kind=="black":
        return [
            {"start_s":float(start),"end_s":float(end),"duration_s":float(duration)}
            for start,end,duration in BLACK.findall(log)
        ]
    start_pattern,end_pattern=(FREEZE_START,FREEZE_END) if kind=="freeze" else (SILENCE_START,SILENCE_END)
    starts=[float(n) for n in start_pattern.findall(log)]
    ends=[(float(end),float(duration)) for end,duration in end_pattern.findall(log)]
    out=[]
    # The FFmpeg detector writes events in order. Closed intervals paired with starts.
    for i,(end,duration) in enumerate(ends):
        start=end-duration
        if i<len(starts) and abs(starts[i]-start)<.25:
            start=starts[i]
        out.append({"start_s":round(start,4),"end_s":round(end,4),"duration_s":round(duration,4)})
    if len(starts)>len(ends):
        for start in starts[len(ends):]:
            out.append({"start_s":start,"end_s":None,"duration_s":None,"note":"continues beyond analyzed interval"})
    return out

def process(cmd,timeout):
    proc=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout,check=False)
    if proc.returncode:
        raise RuntimeError("FFmpeg analysis failed: "+proc.stderr[-800:])
    return proc.stderr

def analyze(path,max_seconds=120,black_min=.20,freeze_min=.55,silence_min=.40):
    path=Path(path)
    if not path.is_file() or path.stat().st_size==0:
        return {"status":"FAIL","issues":["missing or empty input file"]}
    if any(not isinstance(x,(float,int)) or isinstance(x,bool) or not math.isfinite(x) or x<=0
           for x in (max_seconds,black_min,freeze_min,silence_min)):
        return {"status":"FAIL","issues":["limits/thresholds must be positive finite numbers"]}
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        return {"status":"UNKNOWN","issues":["ffmpeg and ffprobe required"]}
    try:
        probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type",
            "-of","json",str(path)],capture_output=True,text=True,check=True,timeout=30)
        info=json.loads(probe.stdout)
        duration=float(info.get("format",{}).get("duration","0"))
        streams=info.get("streams",[])
        if not any(s.get("codec_type")=="video" for s in streams) or not 0<duration<86400:
            return {"status":"FAIL","issues":["valid video stream and duration required"]}
        has_audio=any(s.get("codec_type")=="audio" for s in streams)
        bounded=min(float(max_seconds),duration)
        cmd=["ffmpeg","-hide_banner","-nostdin","-i",str(path),"-t",str(bounded),
             "-vf",f"blackdetect=d={black_min}:pix_th=0.055,freezedetect=n=-58dB:d={freeze_min}",
             "-an","-f","null","-"]
        visual_log=process(cmd,120)
        audio_log=""
        if has_audio:
            cmd=["ffmpeg","-hide_banner","-nostdin","-i",str(path),"-t",str(bounded),
                 "-af",f"silencedetect=noise=-43dB:d={silence_min}","-vn","-f","null","-"]
            audio_log=process(cmd,120)
    except (ValueError,OSError,subprocess.TimeoutExpired,subprocess.CalledProcessError,RuntimeError) as exc:
        return {"status":"FAIL","issues":[str(exc)]}
    black=parse_intervals(visual_log,"black")
    freeze=parse_intervals(visual_log,"freeze")
    silence=parse_intervals(audio_log,"silence") if has_audio else []
    alerts=[]
    if black:alerts.append(f"{len(black)} possibly black interval(s): check if intentional")
    if freeze:alerts.append(f"{len(freeze)} possibly frozen interval(s): can be a deliberate hold")
    if silence:alerts.append(f"{len(silence)} possibly silent interval(s): may be intentional")
    if not has_audio:alerts.append("No audio stream detected; verify whether silent output was intended")
    if duration>bounded:alerts.append("Only part of the film analyzed: raise --max-seconds for full duration")
    return {
        "status":"PASS_WITH_WARNINGS" if alerts else "PASS",
        "analysis_type":"AUTOMATED_SIGNAL_DIAGNOSTICS_ONLY",
        "analyzed_seconds":bounded,"total_duration_s":duration,
        "audio_stream_present":has_audio,
        "black_intervals":black,"freeze_intervals":freeze,"silence_intervals":silence,
        "review_flags":alerts,
        "creative_quality":"UNKNOWN","sound_intelligibility":"UNKNOWN","brand_fidelity":"UNKNOWN",
        "interpretation":"Black/freeze/silence can be deliberate. Watch/listen to video, especially flagged timecodes."
    }

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video",type=Path)
    ap.add_argument("--max-seconds",type=float,default=120)
    ap.add_argument("--report",type=Path)
    args=ap.parse_args(argv)
    result=analyze(args.video,args.max_seconds)
    payload=json.dumps(result,indent=2,ensure_ascii=False)+"\n"
    if args.report:args.report.write_text(payload,encoding="utf-8")
    else:print(payload,end="")
    return 1 if result["status"]=="FAIL" else 2 if result["status"]=="UNKNOWN" else 0

if __name__=="__main__":
    raise SystemExit(main())
