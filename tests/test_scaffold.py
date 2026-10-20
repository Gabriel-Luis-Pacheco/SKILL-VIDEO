"""Scaffold is a fail-closed starting point, not a rendered film."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
p=ROOT/"skills"/"ai-video-director"/"scripts"/"new_video_project.py"
spec=importlib.util.spec_from_file_location("new_video_project",p)
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

class ProjectScaffoldTest(unittest.TestCase):
    def test_create_draft_and_do_not_invent_truth(self):
        with tempfile.TemporaryDirectory() as folder:
            dst=Path(folder)/"commercial"
            mod.build(dst,"Commercial","Example Studio","conversion","reels")
            data=json.loads((dst/"brief.json").read_text())
            self.assertEqual(data["status"],"DRAFT_NOT_RENDERED")
            self.assertEqual(data["product_truth"],"unknown")
            self.assertEqual(json.loads((dst/"storyboard.json").read_text())["scenes"],[])
            self.assertEqual(json.loads((dst/"assets.json").read_text())["assets"],[])
            self.assertTrue((dst/"deliverables").is_dir())
    def test_never_overwrite_user_files(self):
        with tempfile.TemporaryDirectory() as folder:
            dst=Path(folder)/"creative"
            mod.build(dst,"Art","Art","art","cinema")
            (dst/"README.md").write_text("MANUAL CONTENT")
            with self.assertRaises(FileExistsError):
                mod.build(dst,"Other","Brand","awareness","reels")
            self.assertEqual((dst/"README.md").read_text(),"MANUAL CONTENT")
    def test_unrecognized_goal_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                mod.build(Path(folder)/"bad","Film","B","unknown","reels")

if __name__=="__main__":
    unittest.main()
