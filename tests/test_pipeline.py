"""Executable contract tests — not independent evidence of artistic quality."""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-video-director"

def load(name):
    path = SKILL / "scripts" / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

timeline = load("timeline_compile")
campaign = load("campaign_matrix")
assets = load("asset_preflight")
captions = load("captions_lint")

def fixture(name):
    return json.loads((SKILL/"fixtures"/name).read_text(encoding="utf-8"))

class TimelineTests(unittest.TestCase):
    def test_fractional_fps_total_and_no_drift(self):
        plan = timeline.compile_storyboard(fixture("storyboard.json"))
        self.assertEqual(plan["duration_in_frames"], 450)
        self.assertEqual(plan["scenes"][-1]["end_frame_exclusive"], 450)
        self.assertEqual(sum(s["duration_in_frames"] for s in plan["scenes"]), 450)
        self.assertEqual(plan["scenes"][0]["start_frame"], 0)
        self.assertEqual([s["end_frame_exclusive"] for s in plan["scenes"][:-1]],
                         [s["start_frame"] for s in plan["scenes"][1:]])
    def test_duplicate_scene(self):
        d=fixture("storyboard.json")
        d["scenes"][1]["id"] = d["scenes"][0]["id"]
        with self.assertRaises(timeline.PlanError):
            timeline.compile_storyboard(d)
    def test_zero_or_tiny_scene(self):
        d=fixture("storyboard.json")
        d.pop("target_seconds")
        d["scenes"][0]["seconds"] = .00001
        with self.assertRaises(timeline.PlanError):
            timeline.compile_storyboard(d)
    def test_mismatched_target(self):
        d=fixture("storyboard.json")
        d["target_seconds"] = 17
        with self.assertRaises(timeline.PlanError):
            timeline.compile_storyboard(d)
    def test_nonfinite_duration(self):
        d=fixture("storyboard.json")
        d["scenes"][0]["seconds"]="NaN"
        with self.assertRaises(timeline.PlanError):
            timeline.compile_storyboard(d)
    def test_invalid_method(self):
        d=fixture("storyboard.json")
        d["scenes"][0]["render_method"]="NOT_A_REAL_TOOL"
        with self.assertRaises(timeline.PlanError):
            timeline.compile_storyboard(d)

class CampaignTests(unittest.TestCase):
    def test_clean_one_variable_tests(self):
        errors, warnings = campaign.check_matrix(fixture("campaign_matrix.json"))
        self.assertEqual(errors, [])
        self.assertGreater(len(warnings), 0)
    def test_multiple_changes_and_brand_drift_fail(self):
        errs,_=campaign.check_matrix(fixture("campaign_matrix_invalid.json"))
        self.assertTrue(any("actual changes" in e for e in errs))
        self.assertTrue(any("brand" in e for e in errs))
    def test_missing_evidence_for_claim_change(self):
        d=fixture("campaign_matrix.json")
        d["variants"][0]["changed_field"]="proof"
        d["variants"][0]["hook"]=d["baseline"]["hook"]
        d["variants"][0]["proof"]="Resultado muito grande."
        errs,_=campaign.check_matrix(d)
        self.assertTrue(any("evidence" in e for e in errs))
    def test_changed_destination_is_disallowed(self):
        d=fixture("campaign_matrix.json")
        d["variants"][0]["landing_url"]="https://some-other-example.org"
        errs,_=campaign.check_matrix(d)
        self.assertTrue(any("target" in e for e in errs))

class AssetsTests(unittest.TestCase):
    def test_preview_may_warn_of_missing_assets(self):
        errors,warnings=assets.check_manifest(fixture("assets.json"),SKILL,False)
        self.assertEqual(errors,[])
        self.assertGreater(len(warnings),0)
    def test_release_fails_unknown_canon_and_rights(self):
        errors,_=assets.check_manifest(fixture("assets.json"),SKILL,True)
        self.assertTrue(any("rights" in e for e in errors))
        self.assertTrue(any("canonical" in e for e in errors))
    def test_path_traversal(self):
        doc={"assets":[{"id":"a","kind":"image","source":"test","rights":"cleared","path":"../../etc/passwd"}]}
        errors,_=assets.check_manifest(doc,SKILL,True)
        self.assertTrue(any("traverse" in e for e in errors))
    def test_duplicate_asset(self):
        d=fixture("assets.json")
        d["assets"][1]["id"]=d["assets"][0]["id"]
        errors,_=assets.check_manifest(d,SKILL,False)
        self.assertTrue(any("duplicate" in e for e in errors))

class CaptionsTests(unittest.TestCase):
    def test_srt_passes(self):
        e,w=captions.lint_srt((SKILL/"fixtures/sample.srt").read_text())
        self.assertEqual(e,[])
        self.assertEqual(w,[])
    def test_overlapping_cues_fail(self):
        s="1\n00:00:00,000 --> 00:00:03,000\nPrimeira\n\n2\n00:00:02,000 --> 00:00:04,000\nSegunda\n"
        errors,_=captions.lint_srt(s)
        self.assertTrue(any("overlaps" in e for e in errors))
    def test_bad_timestamp_fails(self):
        e,_=captions.lint_srt("1\n00:00:99,000 --> 00:00:01,000\nErro\n")
        self.assertTrue(e)
    def test_legibility_warning_only(self):
        s="1\n00:00:00,000 --> 00:00:00,050\nUma frase muito extensa para ler em menos de um segundo.\n"
        e,w=captions.lint_srt(s)
        self.assertEqual(e,[])
        self.assertTrue(w)

if __name__ == "__main__":
    unittest.main()
