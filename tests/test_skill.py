"""No network calls; standard-library structural tests."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-video-director"
SCRIPTS = SKILL / "scripts"

def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

linter, validator, qc = load("shotlist_lint"), load("validate"), load("video_qc")

class VideoOSPrimeTests(unittest.TestCase):
    def test_skill_structure(self):
        self.assertEqual(validator.validate_skill(SKILL), [])
    def test_valid_shotlist(self):
        doc = json.loads((SKILL/"fixtures/valid_shotlist.json").read_text())
        self.assertEqual(linter.lint(doc), [])
        self.assertEqual(linter.lint(doc, release=True), [])
    def test_invalid_shotlist(self):
        doc = json.loads((SKILL/"fixtures/invalid_shotlist.json").read_text())
        self.assertGreater(len(linter.lint(doc)), 1)
        self.assertGreater(len(linter.lint(doc, release=True)), 2)
    def test_bool_is_not_number(self):
        doc = {"fps": True, "duration_s": 3, "shots": []}
        self.assertTrue(any("fps" in s for s in linter.lint(doc)))
    def test_gap_and_overlap(self):
        doc = json.loads((SKILL/"fixtures/valid_shotlist.json").read_text())
        doc["shots"][1]["start_s"] = 4
        self.assertTrue(any("gap/overlap" in s for s in linter.lint(doc)))
    def test_incomplete_release(self):
        doc = json.loads((SKILL/"fixtures/valid_shotlist.json").read_text())
        doc["shots"][0]["asset_status"] = "placeholder"
        self.assertTrue(any("placeholder" in s for s in linter.lint(doc, release=True)))
    def test_missing_media(self):
        result = qc.inspect(ROOT / "file-that-does-not-exist.mp4")
        self.assertEqual(result["status"], "FAIL")
    def test_script_library_covers_24(self):
        contents = (SKILL/"examples/original-script-vault.md").read_text()
        self.assertIn("## 24. As cores têm memória", contents)

if __name__ == "__main__":
    unittest.main()
