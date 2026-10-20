"""v4 constraints: truthful creative routing and honest independent outcome reporting."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/"skills"/"ai-video-director"

def load(name):
    path=SKILL/"scripts"/(name+".py")
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

metrics=load("campaign_results")
review=load("independent_review")
router=load("brief_router")

def fixture(name):
    return json.loads((SKILL/"fixtures"/name).read_text(encoding="utf-8"))

class MetricsTest(unittest.TestCase):
    def test_descriptive_only_no_winner(self):
        report=metrics.analyze(fixture("campaign_results_synthetic.json"))
        self.assertEqual(report["status"],"PASS")
        self.assertEqual(report["winner"],"NOT_DETERMINED")
        self.assertEqual(report["data_provenance"],"SYNTHETIC_SAMPLE")
        self.assertEqual(report["causal_effect"],"UNKNOWN")
        self.assertEqual(report["variants"][0]["click_through_pct"],10.0)
    def test_uncertainty_bounds_are_finite(self):
        self.assertEqual(metrics.wilson(0,0),None)
        low,high=metrics.wilson(0,10)
        self.assertEqual(low,0)
        self.assertGreater(high,0)
        low,high=metrics.wilson(10,10)
        self.assertLess(low,100)
        self.assertEqual(high,100)
    def test_invalid_count_or_nan_fails(self):
        d=fixture("campaign_results_synthetic.json")
        d["variants"][0]["clicks"]=-1
        self.assertEqual(metrics.analyze(d)["status"],"FAIL")
        d["variants"][0]["clicks"]=100
        d["variants"][1]["spend"]=float("nan")
        self.assertEqual(metrics.analyze(d)["status"],"FAIL")
    def test_views_above_impressions_rejected(self):
        d=fixture("campaign_results_synthetic.json")
        d["variants"][0]["views_3s"]=9999
        self.assertEqual(metrics.analyze(d)["status"],"FAIL")
    def test_zero_impressions_no_spend(self):
        d=fixture("campaign_results_synthetic.json")
        d["variants"][0].update({k:0 for k in ("impressions","views_3s","clicks","leads","purchases")})
        d["variants"][0]["spend"]=0
        report=metrics.analyze(d)
        self.assertEqual(report["status"],"PASS")
        self.assertIsNone(report["variants"][0]["click_through_pct"])

class ReviewTest(unittest.TestCase):
    def test_synthetic_reviews_are_never_called_blind(self):
        r=review.evaluate(fixture("review_synthetic.json"))
        self.assertEqual(r["status"],"PASS")
        self.assertEqual(r["blind_quality_claim"],"NOT_SUPPORTED")
        self.assertEqual(r["creative_release_recommendation"],"BLOCK")
        self.assertEqual(r["review_claim"],"DECLARED_ONLY_NOT_IDENTITY_VERIFIED")
    def test_bool_score_and_missing_evidence_fail(self):
        d=fixture("review_synthetic.json")
        d["reviewers"][0]["ratings"]["art"]=True
        self.assertEqual(review.evaluate(d)["status"],"FAIL")
        d=fixture("review_synthetic.json")
        d["reviewers"][0]["observations"]=[]
        self.assertEqual(review.evaluate(d)["status"],"FAIL")
    def test_critical_observation_blocks(self):
        d=fixture("review_synthetic.json")
        d["reviewers"][1]["observations"][0]["severity"]="NONE"
        r=review.evaluate(d)
        self.assertEqual(r["creative_release_recommendation"],"MANUAL_SIGNOFF_REQUIRED")

class RouterTest(unittest.TestCase):
    def test_verified_ui_still_only_plan(self):
        r=router.route(fixture("brief_synthetic.json"))
        self.assertEqual(r["status"],"PASS")
        self.assertFalse(r["blockers"])
        self.assertEqual(r["ready_for_commercial_publish"],"NOT_DETERMINED")
        self.assertEqual(r["output_status"],"PLAN_ONLY_NOT_RENDERED")
    def test_invalid_json_types_fail_gracefully(self):
        d=fixture("brief_synthetic.json")
        d["goal"]=["conversion"]
        self.assertEqual(router.route(d)["status"],"FAIL")
        d=fixture("brief_synthetic.json")
        d["available_tools"]=[{"tool":"malicious"}]
        self.assertEqual(router.route(d)["status"],"FAIL")
    def test_no_real_ui_blocks(self):
        d=fixture("brief_synthetic.json")
        d["available_tools"].remove("screen_capture")
        self.assertTrue(router.route(d)["blockers"])
    def test_missing_cta_blocks_conversion(self):
        d=fixture("brief_synthetic.json")
        d.pop("cta_destination")
        self.assertIn("No verified CTA destination",router.route(d)["blockers"][0])
    def test_art_does_not_require_cta(self):
        d=fixture("brief_synthetic.json")
        d.update({"goal":"art","central_visual":"imaginary_world","product_truth":"unknown","available_tools":["blender"]})
        d.pop("cta_destination")
        r=router.route(d)
        self.assertFalse(r["blockers"])
        self.assertIn("poetically",r["creative_priorities"][1].lower())
    def test_character_canon_missing_blocks(self):
        d=fixture("brief_synthetic.json")
        d.update({"central_visual":"brand_character","available_tools":["rive"]})
        self.assertTrue(any("character" in s for s in router.route(d)["blockers"]))

if __name__=="__main__":
    unittest.main()
