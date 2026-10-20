"""Real frame-rendering tests. Technical verification, not aesthetic judgment."""
import importlib.util
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
MOVIE=ROOT/"skills"/"ai-video-director"/"examples"/"rendered-proof"/"render.py"
spec=importlib.util.spec_from_file_location("motion_study",MOVIE)
motion=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=motion
spec.loader.exec_module(motion)

class RealRenderLab(unittest.TestCase):
    def test_frames_progress_through_story(self):
        first=motion.draw_frame(0,270,480)
        middle=motion.draw_frame(3.25,270,480)
        final=motion.draw_frame(6.7,270,480)
        self.assertEqual(first.size,(270,480))
        self.assertNotEqual(first.tobytes(),middle.tobytes())
        self.assertNotEqual(middle.tobytes(),final.tobytes())
    def test_original_audio_has_samples(self):
        import wave
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"original.wav"
            motion.sound(path,2)
            with wave.open(str(path),"rb") as reader:
                self.assertEqual(reader.getnframes(),48000)
                self.assertEqual(reader.getnchannels(),1)
    @unittest.skipUnless(shutil.which("ffmpeg"),"FFmpeg missing")
    def test_supported_four_by_five_aspect(self):
        import importlib.util
        qc_path=ROOT/"skills"/"ai-video-director"/"scripts"/"video_qc.py"
        spec=importlib.util.spec_from_file_location("qc_4x5",qc_path)
        qc=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qc)
        with tempfile.TemporaryDirectory() as tmp:
            sample=Path(tmp)/"four-by-five.mp4"
            motion.render(sample,240,300,6,7)
            self.assertEqual(qc.inspect(sample,7,"4:5",True)["status"],"PASS")
    def test_parameter_guardrails(self):
        with self.assertRaises(ValueError):
            motion.render("unused.mp4",width:=161,h:=480,fps:=30,seconds:=7)
    @unittest.skipUnless(shutil.which("ffmpeg"),"FFmpeg missing")
    def test_real_video_has_image_and_audio(self):
        from pathlib import Path
        import importlib.util
        qc_path=ROOT/"skills"/"ai-video-director"/"scripts"/"video_qc.py"
        s=importlib.util.spec_from_file_location("qc",qc_path)
        qc=importlib.util.module_from_spec(s)
        s.loader.exec_module(qc)
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"sample.mp4"
            stills=Path(tmp)/"stills"
            result=motion.render(out,270,480,6,7,stills=stills)
            self.assertEqual(result["frames"],42)
            self.assertTrue(out.is_file() and out.stat().st_size>0)
            self.assertEqual(len(list(stills.glob("*.png"))),5)
            report=qc.inspect(out,7,"9:16",True)
            self.assertEqual(report["status"],"PASS",report)
            self.assertEqual(report["metadata"]["audio_streams"],1)

if __name__=="__main__":
    unittest.main()
