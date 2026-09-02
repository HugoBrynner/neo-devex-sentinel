import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from neo_sentinel.core import scan, write_report

ROOT = Path(__file__).resolve().parents[1]

class SentinelTests(unittest.TestCase):
    def test_runtime_drift_maps_to_docs(self):
        f = ROOT / "fixtures/runtime"
        r = scan(f/"old", f/"new", f/"docs", "v3.7.4", "v3.8.1")
        hits = [c for c in r["changes"] if c["kind"] == "target_framework_changed"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["before"], "net8.0")
        self.assertEqual(hits[0]["after"], "net9.0")
        self.assertIn("develop.md", hits[0]["docs_exact"])
        self.assertEqual(hits[0]["severity"], "high")

    def test_new_public_types_are_detected(self):
        f = ROOT / "fixtures/api"
        r = scan(f/"old", f/"new", f/"docs", "v3.10.0", "v3.10.1")
        added = {c["symbol"]: c for c in r["changes"] if c["kind"] == "public_type_added"}
        for name in ("AccessControl", "Ownable2Step", "PausableOwnable", "RoyaltyNep11Token"):
            self.assertIn(name, added)
        self.assertFalse(added["AccessControl"]["docs_exact"])
        self.assertIn("nep11.md", added["RoyaltyNep11Token"]["docs_related"])

    def test_multi_release_runtime_drift(self):
        f = ROOT / "fixtures/runtime-next"
        r = scan(f/"old", f/"new", f/"docs", "v3.8.1", "v3.9.0")
        hit = next(c for c in r["changes"] if c["kind"] == "target_framework_changed")
        self.assertEqual(hit["before"], "net9.0")
        self.assertEqual(hit["after"], "net10.0")
        self.assertIn("develop.md", hit["docs_exact"])

    def test_signature_change_is_paired(self):
        f = ROOT / "fixtures/signature"
        r = scan(f/"old", f/"new", f/"docs", "a", "b")
        hits = [c for c in r["changes"] if c["kind"] == "public_method_signature_changed"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["symbol"], "Update")
        self.assertIn("api.md", hits[0]["docs_exact"])

    def test_outputs(self):
        f = ROOT / "fixtures/runtime"
        r = scan(f/"old", f/"new", f/"docs", "a", "b")
        with TemporaryDirectory() as td:
            jp, mp = write_report(r, Path(td))
            self.assertTrue(jp.exists())
            self.assertTrue(mp.exists())
            self.assertEqual(json.loads(jp.read_text())["version"], "0.1.0")

if __name__ == "__main__":
    unittest.main()
