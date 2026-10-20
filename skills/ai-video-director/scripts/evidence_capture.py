#!/usr/bin/env python3
"""Sample actual encoded frames and create a visual-review contact sheet + provenance.

This script captures images for human inspection. It NEVER declares that the
images look beautiful, text is legible, an ad converts, or rights are cleared.
Requires Pillow, ffmpeg and ffprobe; no network, shell or untrusted code runs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

def metadata(path):
    if shutil.which("ffprobe") is None or shutil.which("ffmpeg") is None:
        raise RuntimeError("FFmpeg and ffprobe must be installed")
    cmd=["ffprobe","-v","error","-show_entries","format=duration:stream=width,height,codec_type,avg_frame_rate","-of","json",str(path)]
    result=subprocess.run(cmd,capture_output=True,text=True,check=True,timeout=25)
    data=json.loads(result.stdout)
    video=next((s for s in data.get("streams",[]) if s.get("codec_type")=="video"),None)
    if not video:
        raise ValueError("no video stream")
    seconds=float(data["format"]["duration"])
    if not 0<seconds<=3600:
        raise ValueError("sample time limit is 1 hour")
    return seconds,video

def make_samples(duration,timeline=None,max_frames=24):
    if not 3<=max_frames<=48:
        raise ValueError("max_frames must be between 3 and 48")
    points=set()
    if timeline:
        scenes=timeline.get("scenes",[])
        fps=timeline.get("fps")
        if not isinstance(fps,(int,float)) or fps<=0 or not isinstance(scenes,list):
            raise ValueError("invalid compiled timeline for sample schedule")
        for s in scenes:
            for f in s.get("checkpoints",[]):
                if not isinstance(f,int) or f<0:
                    raise ValueError("invalid checkpoint frame")
                points.add(f/fps)
    # Always check the physical opening, midpoint and end: clip max slightly.
    for x in (0,duration*.25,duration*.5,duration*.75,max(0,duration-.085)):
        points.add(x)
    ordered=sorted(max(0,min(duration-.001,t)) for t in points)
    if len(ordered)<=max_frames:
        return ordered
    # Keep start/end and spread samples across timeline. Prefer not to oversample short scenes.
    picks=sorted(set(round(i*(len(ordered)-1)/(max_frames-1)) for i in range(max_frames)))
    return [ordered[i] for i in picks]

def capture(source,output_dir,timeline=None,max_frames=24,thumb_width=320):
    source=Path(source).resolve()
    if not source.is_file() or source.stat().st_size==0:
        raise ValueError("missing or empty media file")
    out=Path(output_dir)
    out.mkdir(parents=True,exist_ok=True)
    duration,stream=metadata(source)
    samples=make_samples(duration,timeline,max_frames)
    thumbs=[]
    frames=[]
    for i,t in enumerate(samples):
        frame=out/f"review-{i:02d}.png"
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",f"{t:.5f}","-i",str(source),"-frames:v","1",str(frame)]
        subprocess.run(cmd,check=True,timeout=35,capture_output=True)
        if not frame.is_file() or frame.stat().st_size==0:
            raise RuntimeError("frame extraction failed at time "+str(t))
        with Image.open(frame) as raw:
            raw.load()
            w=max(80,min(thumb_width,raw.width))
            h=round(raw.height*w/raw.width)
            thumbs.append(raw.convert("RGB").resize((w,h),Image.Resampling.LANCZOS))
        frames.append({"time_s":round(t,5),"file":frame.name,"observed_by_human":False})
    # Aspect-independent grid: each cell has sufficient border and a timecode.
    ncol=4 if len(thumbs)>8 else 3
    cell_w=max(im.width for im in thumbs)+18
    cell_h=max(im.height for im in thumbs)+48
    nrow=(len(thumbs)+ncol-1)//ncol
    board=Image.new("RGB",(ncol*cell_w,nrow*cell_h),(18,20,23))
    d=ImageDraw.Draw(board)
    for k,im in enumerate(thumbs):
        x=(k%ncol)*cell_w+9;y=(k//ncol)*cell_h+9
        board.paste(im,(x,y))
        d.text((x,y+cell_h-32),f"{k:02d}  {samples[k]:.2f}s",fill=(240,243,240))
    sheet=out/"contact-sheet.jpg"
    board.save(sheet,quality=90)
    # Preserve SHA for reconstruction; never save secrets or the original's absolute path.
    digest=hashlib.sha256()
    with source.open("rb") as handle:
        while chunk:=handle.read(1024*1024):digest.update(chunk)
    report={
        "schema":"video-os-review-evidence-v1",
        "input_name":source.name,"input_sha256":digest.hexdigest(),
        "duration_s":duration,"size":[stream.get("width"),stream.get("height")],
        "captured_frames":frames,"contact_sheet":sheet.name,
        "visual_qa":"NOT_PERFORMED","audio_qa":"NOT_PERFORMED",
        "note":"A contact sheet and successful extraction do not prove content, craft, motion, captions or sound."
    }
    (out/"evidence.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video",type=Path)
    ap.add_argument("--timeline",type=Path)
    ap.add_argument("--out",type=Path,default=Path("out/review"))
    ap.add_argument("--max-frames",type=int,default=24)
    ap.add_argument("--thumb-width",type=int,default=320)
    args=ap.parse_args(argv)
    try:
        timeline=json.loads(args.timeline.read_text(encoding="utf-8")) if args.timeline else None
        report=capture(args.video,args.out,timeline,args.max_frames,args.thumb_width)
        print(json.dumps(report,indent=2,ensure_ascii=False))
        return 0
    except (OSError,ValueError,RuntimeError,subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        print("FAIL:",str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
