import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from publish_artificial_1023 import promoted_manifest


class CandidatePromotionTests(unittest.TestCase):
    def setUp(self):
        self.descriptor = b'version="0.5.0-rc.5"\nsupported_version="4.5.2"\n'
        self.candidate = {"descriptor.mod": hashlib.sha256(self.descriptor).hexdigest(), "events/a.txt": "tested"}
        self.formal = {**self.candidate, "descriptor.mod": hashlib.sha256(self.descriptor.replace(b'0.5.0-rc.5', b'0.5.0')).hexdigest()}

    def test_version_only_promotion(self):
        self.assertEqual(promoted_manifest(self.candidate, self.descriptor, self.formal), self.formal)

    def test_script_drift_rejected(self):
        self.formal["events/a.txt"] = "untested"
        with self.assertRaises(RuntimeError):
            promoted_manifest(self.candidate, self.descriptor, self.formal)

    def test_extra_file_rejected(self):
        self.formal["testing.txt"] = "fixture"
        with self.assertRaises(RuntimeError):
            promoted_manifest(self.candidate, self.descriptor, self.formal)

    def test_wrong_candidate_version_rejected(self):
        with self.assertRaises(RuntimeError):
            promoted_manifest(self.candidate, b'version="0.4.0"', self.formal)


if __name__ == "__main__":
    unittest.main()
