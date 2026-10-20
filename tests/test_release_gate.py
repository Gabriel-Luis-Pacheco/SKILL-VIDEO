"""Integration tests for asset/storyboard cross-file and release semantics."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills"/"ai-video-director"
sys.path.insert(0,str(SKILL/"scripts"))
from production_gate import run_gate

def fixture(n):
    return json.loads((SKILL/"fixtures"/n).read_text())

class ReleaseGateTests(unittest.TestCase):
    def test_preview_never_claims_media_or_creative_quality(self):
        r=run_gate(fixture("storyboard.json"),fixture("assets.json"),project_root=SKILL)
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["checks"]["media"],"UNKNOWN")
        self.assertEqual(r["checks"]["creative_quality"],"UNKNOWN")
        self.assertTrue(any("absent from manifest" in w for w in r["warnings"]))
    def test_release_without_video_fails(self):
        r=run_gate(fixture("storyboard.json"),fixture("assets.json"),project_root=SKILL,release=True)
        self.assertEqual(r["status"],"FAIL")
        self.assertTrue(any("no rendered video" in e for e in r["errors"]))
    def test_release_with_missing_asset_reference_fails(self):
        d=fixture("assets.json")
        r=run_gate(fixture("storyboard.json"),d,project_root=SKILL,release=True)
        self.assertTrue(any("absent from manifest" in e for e in r["errors"]))
    def test_subtitle_overlap_blocks_preview(self):
        s="1\n00:00:00,000 --> 00:00:02,000\nX\n\n2\n00:00:01,000 --> 00:00:03,000\nY\n"
        r=run_gate(fixture("storyboard.json"),fixture("assets.json"),captions_text=s)
        self.assertEqual(r["status"],"FAIL")
        self.assertEqual(r["checks"]["captions"],"FAIL")

if __name__=="__main__":
    unittest.main()
