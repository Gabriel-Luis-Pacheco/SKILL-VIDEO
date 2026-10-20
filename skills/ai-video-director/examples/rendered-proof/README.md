# Motion Film Lab — a genuinely rendered and testable video (v3)

A complete original 7-second vertical 9:16 specimen: graphic trajectory → transformation → typographic payoff → restrained end frame, with procedurally authored synced sound. **No borrowed stock, no fake app screen, no commercial claims.** This is an engineering reference, NOT a claim that a world-class commercial has been created.

**Requirements:** Python 3.11+, `pip install Pillow`, FFmpeg with libx264/AAC available and a system font (DejaVu Sans or Liberation Sans). The renderer needs no model API and creates no secret-bearing files.

```bash
python -m pip install Pillow
python skills/ai-video-director/examples/rendered-proof/render.py --output /tmp/motion-specimen.mp4 --width 540 --height 960 --fps 30 --stills /tmp/motion-frames
python skills/ai-video-director/scripts/video_qc.py /tmp/motion-specimen.mp4 --duration 7 --aspect 9:16 --require-audio
```

**Creative review:** examine the five saved frames, actually watch all 7 seconds, listen to the synced original audio, reject cheap easing, assess beginning/middle/end and revise source. Technical rendering only shows a functioning pipeline. No automatic test can verify artistic superiority or user retention.

**CI:** Github Actions renders a lower-resolution specimen for smoke verification and checks media metadata. That proves a portable, fully reproducible path from source to real MP4. Rendered sample is ephemeral unless deliberately attached to a run. For editable design direction, use the Remotion source study alongside this pipeline.

**Why this matters:** A lot of video skills only describe a process or show a snippet of JSX without an executable build. This laboratory tests that actual frame generation, encoder, soundtrack, storyboard and metadata travel through to an inspectable video, without mistaking technical success for artistic greatness.
