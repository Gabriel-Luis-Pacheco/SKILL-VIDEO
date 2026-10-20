#!/usr/bin/env python3
"""A seven-second original motion-film laboratory. Render with Pillow + FFmpeg.

No external assets, generative media, fake product screens or commercial claims.
This proves an inspectable MP4 pipeline with synchronized self-produced audio;
it cannot prove great art, audience engagement or advertising effectiveness.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave

from PIL import Image, ImageDraw, ImageFont

INK=(11,20,25)
PAPER=(246,241,227)
CORAL=(255,111,81)
LILAC=(173,160,249)
MINT=(149,209,183)
FONT_PATHS=[
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

def get_font(size, override=None):
    for path in ([str(override)] if override else [])+FONT_PATHS:
        if Path(path).is_file():
            return ImageFont.truetype(path,max(8,round(size)))
    raise RuntimeError("Font unavailable; provide --font PATH")

def ease(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)

def enter(t,a,b):
    return ease((t-a)/(b-a))

def mix(c1,c2,amount):
    return tuple(round(p*(1-amount)+q*amount) for p,q in zip(c1,c2))

def write(draw,point,message,ft,fill=PAPER,anchor="mm"):
    draw.text(point,message,font=ft,fill=fill,anchor=anchor)

def draw_frame(t,w,h,font_override=None):
    image=Image.new("RGB",(w,h),INK)
    d=ImageDraw.Draw(image)
    u=min(w,h)/540
    cx,cy=w*.5,h*.43
    for x in range(round(w*.10),w,round(w*.20)):
        d.line((x,h*.12,x,h*.84),fill=(30,43,49),width=max(1,round(u)))
    d.line((w*.1,h*.84,w*.9,h*.84),fill=(60,73,76),width=max(1,round(u)))
    small=get_font(15*u,font_override)
    headline=get_font(61*u,font_override)
    medium=get_font(27*u,font_override)
    foot=get_font(13*u,font_override)
    write(d,(w*.1,h*.073),"VIDEO OS / MOTION STUDY",small,(179,189,189),"lm")
    write(d,(w*.9,h*.073),"01",small,CORAL,"rm")
    # Act I: material arrives, contacts its intended position and settles.
    move=1-(1-enter(t,.15,1.43))**3
    x=-w*.13+(cx+w*.13)*move
    compression=1-.15*math.exp(-((t-1.1)/.15)**2)
    radius=(24+17*enter(t,.82,1.52))*u*compression
    d.ellipse((x-radius,cy-radius-20*u,x+radius,cy+radius-20*u),fill=CORAL)
    # Act II: one event becomes an actual line of connection, not random particles.
    bloom=enter(t,1.2,2.45)*(1-enter(t,3.5,4.35))
    if bloom>0:
        for k,col in enumerate((PAPER,MINT,LILAC,CORAL)):
            progress=enter(t,1.27+k*.16,3.1+k*.12)
            if not progress:continue
            y=cy-20*u+(k-1.5)*30*u
            left=cx-174*u
            right=left+348*u*progress
            pts=[]
            for i in range(53):
                a=i/52
                pts.append((left+(right-left)*a,y+math.sin(a*math.pi*1.25+t*.62+k*.65)*(11+k*3)*u*progress))
            d.line(pts,fill=mix(INK,col,.28+.67*bloom),width=max(2,round((2+k%2)*u)))
    # Act III: theme becomes typography, preserving exact source text.
    a=enter(t,3.06,3.58)
    if a:
        write(d,(cx,h*.635+(1-a)*44*u),"UMA IDEIA",medium,mix(INK,PAPER,a))
    b=enter(t,3.85,4.65)
    if b:
        write(d,(cx,h*.711+(1-b)*40*u),"GANHA",headline,mix(INK,PAPER,b))
        write(d,(cx,h*.711+67*u+(1-b)*40*u),"FORMA.",headline,mix(INK,PAPER,b))
    # Act IV: resolve, hold, and let people read the finished composition.
    c=enter(t,4.72,5.35)
    if c:
        d.line((cx-64*u,h*.848,cx+64*u,h*.848),fill=mix(INK,PAPER,c*.40),width=max(1,round(2*u)))
        for k,xx in enumerate((cx-64*u,cx,cx+64*u)):
            r=8*u*c
            d.ellipse((xx-r,h*.848-r,xx+r,h*.848+r),fill=(CORAL,PAPER,MINT)[k])
    if t>5.1:
        write(d,(cx,h*.938),"A FORM IS A DECISION — NOT A PRESET",foot,mix(INK,PAPER,enter(t,5.1,5.65)*.7))
    return image

def sound(path,seconds,rate=24000):
    # Original synthesis: timed resonances, not stock or AI-generated music.
    notes=((1.17,110,.38,.17),(2.42,195,.30,.13),(3.68,380,.24,.09),(4.52,260,.22,.11),(5.25,390,.40,.09))
    with wave.open(str(path),"wb") as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate)
        for idx in range(round(rate*seconds)):
            t=idx/rate
            signal=.024*math.sin(2*math.pi*55*t)*min(1,t/.9,max(0,(seconds-t)/.55))
            for start,freq,decay,level in notes:
                tau=t-start
                if tau>=0:
                    signal+=level*math.exp(-tau*9/decay)*(math.sin(2*math.pi*freq*tau)+.33*math.sin(2*math.pi*freq*2.005*tau))
            signal*=min(1,t/.018,max(0,(seconds-t)/.018))
            value=round(max(-.93,min(.93,signal))*32767)
            wav.writeframesraw(value.to_bytes(2,"little",signed=True))

def render(output,w=540,h=960,fps=30,seconds=7.0,font=None,stills=None):
    if w<160 or h<256 or w%2 or h%2 or fps not in range(6,61) or not 5<=seconds<=30:
        raise ValueError("Use even dimensions >=160x256, 6–60fps and duration 5–30s")
    if shutil.which("ffmpeg") is None:raise RuntimeError("Install ffmpeg to render")
    output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    total=round(fps*seconds)
    samples=set([0,round(fps*1.4),round(fps*3.25),round(fps*4.5),total-1])
    saved=[]
    with tempfile.TemporaryDirectory(prefix="video-os-") as temp:
        wav=Path(temp)/"original-score.wav"
        sound(wav,seconds)
        cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(fps),"-i","pipe:0","-i",str(wav),"-c:v","libx264","-preset","fast","-crf","21","-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-movflags","+faststart","-t",str(seconds),str(output)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            for i in range(total):
                image=draw_frame(i/fps,w,h,font)
                if stills and i in samples:
                    target=Path(stills)
                    target.mkdir(parents=True,exist_ok=True)
                    still=target/f"frame-{i:04d}.png"
                    image.save(still)
                    saved.append(str(still))
                proc.stdin.write(image.tobytes())
            proc.stdin.close()
            log=proc.stderr.read().decode("utf-8",errors="replace")
            proc.stderr.close()
            rc=proc.wait()
        except (OSError,BrokenPipeError):
            proc.kill();proc.wait();raise
        finally:
            if proc.stdin and not proc.stdin.closed:proc.stdin.close()
            if proc.stderr and not proc.stderr.closed:proc.stderr.close()
        if rc:raise RuntimeError("ffmpeg failed: "+log[-1000:])
    if not output.is_file() or output.stat().st_size==0:
        raise RuntimeError("Render created no MP4")
    return {"path":str(output),"frames":total,"fps":fps,"duration_seconds":seconds,"resolution":[w,h],"audio":"original procedural music","stills":saved,"creative_review":"NOT_PERFORMED"}

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,default=Path("out/motion-specimen.mp4"))
    ap.add_argument("--width",type=int,default=540)
    ap.add_argument("--height",type=int,default=960)
    ap.add_argument("--fps",type=int,default=30)
    ap.add_argument("--duration",type=float,default=7)
    ap.add_argument("--font",type=Path)
    ap.add_argument("--stills",type=Path)
    args=ap.parse_args()
    print(json.dumps(render(args.output,args.width,args.height,args.fps,args.duration,args.font,args.stills),ensure_ascii=False,indent=2))
