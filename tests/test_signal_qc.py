"""Signal detector flags are NOT automatic cinematic fail conditions."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
import shutil

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills"/"ai-video-director"
p=SKILL/"scripts"/"signal_qc.py"
spec=importlib.util.spec_from_file_location("signal_qc",p)
module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module
spec.loader.exec_module(module)

class SignalQCTest(unittest.TestCase):
    def test_parse_closed_and_open_events(self):
        text="[blackdetect] black_start:0 black_end:0.4 black_duration:0.4"
        self.assertEqual(module.parse_intervals(text,"black")[0]["duration_s"],.4)
        t="[freezedetect] freeze_start: 0.5\n[freezedetect] freeze_end: 2.0 | freeze_duration: 1.5"
        self.assertEqual(module.parse_intervals(t,"freeze")[0]["duration_s"],1.5)
        self.assertEqual(module.parse_intervals("[silencedetect] silence_start: 1.2","silence")[0]["end_s"],None)
    def test_invalid_input(self):
        r=module.analyze(ROOT/"missing-movie.mp4")
        self.assertEqual(r["status"],"FAIL")
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),"ffmpeg unavailable")
    def test_rendered_sample_can_be_inspected_without_quality_claim(self):
        # Generate a short 4s explicitly black/silent clip. No claim about good cinema.
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            video=Path(tmp)/"black.mp4"
            command=["ffmpeg","-hide_banner","-loglevel","error","-y",
                     "-f","lavfi","-i","color=c=black:s=160x160:r=12:d=4",
                     "-f","lavfi","-i","anullsrc=r=24000:cl=mono",
                     "-t","4","-c:v","libx264","-pix_fmt","yuv420p",
                     "-c:a","aac",str(video)]
            subprocess.run(command,check=True,capture_output=True,timeout=60)
            r=module.analyze(video,max_seconds=4,black_min=.2,freeze_min=.5,silence_min=.4)
            self.assertEqual(r["status"],"PASS_WITH_WARNINGS")
            self.assertGreater(len(r["black_intervals"]),0)
            self.assertGreater(len(r["freeze_intervals"]),0)
            self.assertGreater(len(r["silence_intervals"]),0)
            self.assertEqual(r["creative_quality"],"UNKNOWN")

if __name__=="__main__":
    unittest.main()
