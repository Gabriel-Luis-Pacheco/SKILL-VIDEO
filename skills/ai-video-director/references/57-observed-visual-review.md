# Evidence capture — real frames, not imaginary QA

This script extracts up to 48 actual frames from an existing MP4, forms a contact sheet, and records an SHA256 plus precise sample times. With `--timeline compiled.json`, it prioritizes meaningful scene checkpoints; otherwise it samples the clip uniformly.

```bash
python -m pip install Pillow
python skills/ai-video-director/scripts/evidence_capture.py out/video.mp4 --timeline out/timeline.json --out out/review
```

Outputs: `review-00.png` etc, `contact-sheet.jpg` and `evidence.json` with `visual_qa=NOT_PERFORMED`. Review those frames and **watch and listen to the entire MP4**. Write actual observations separately as evidence with timecode; the renderer must not fill in a fictional human evaluation.

Limitations: screenshots do not reveal motion smoothness, sonic timing, flicker between sampled frames, stereophony, emotional impact or commercial conversion. The source video is not copied or uploaded elsewhere by the script.
