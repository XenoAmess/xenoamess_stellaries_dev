"""No desktop imports: execute the real scanner/capture functions with fake input."""
import ast
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import unittest

from PIL import Image

SOURCE = Path(__file__).resolve().parents[1] / "tools/runtime.py"


class ScreenshotScanTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.leaf = self.root / "123/760/remote/281990/screenshots"
        self.leaf.mkdir(parents=True)
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.clock = 0.
        self.on_f12 = lambda: None
        self.saved = []
        def offline_ocr(frame):
            frame.load()
            return SimpleNamespace(boxes=None, txts=None, scores=None)
        harness = SimpleNamespace(
            load_run=lambda: (self.artifacts, None, None),
            process_record=lambda artifacts: {"pid": 123}, focus_pid=lambda pid: 1,
            press_scan_code=lambda *args: self.on_f12(),
            RapidOCR=lambda: offline_ocr,
            sha256=lambda path: hashlib.sha256(path.read_bytes()).hexdigest(),
            write_json=lambda path, value: self.saved.append((path, value)),
            win32gui=SimpleNamespace(GetWindowText=lambda hwnd: "fake offline window",
                ClientToScreen=lambda hwnd, point: point, GetClientRect=lambda hwnd: (0, 0, 10, 10)))
        self.namespace = {"os": os, "Path": Path, "STEAM_SCREENSHOTS": self.root,
            "harness": harness, "shutil": shutil, "datetime": datetime, "timezone": timezone,
            "time": SimpleNamespace(monotonic=lambda: self.clock, sleep=self.advance)}
        tree = ast.parse(SOURCE.read_text(encoding="utf-8-sig"))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                     and node.name in ("screenshot_mtimes", "gpu_capture")]
        self.assertEqual(len(functions), 2)
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), "exec"), self.namespace)

    def tearDown(self):
        self.temporary.cleanup()

    def advance(self, seconds):
        self.clock += seconds

    def image(self, path, color="red", stamp=1_700_000_000_000_000_000):
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (10, 10), color).save(path, format="JPEG")
        os.utime(path, ns=(stamp, stamp))
        return path

    def test_full_glob_mapping_preserves_profiles_suffixes_and_entry_kinds(self):
        self.image(self.leaf / "old.jpg")
        self.image(self.leaf / "upper.JPG")
        self.image(self.root / "987/760/remote/281990/screenshots/second.jpg")
        self.image(self.leaf / "excluded.png")
        self.image(self.root / "123/760/remote/other/screenshots/excluded.jpg")
        self.image(self.root / "123/760/remote/281990/screenshots/nested/excluded.jpg")
        (self.leaf / "directory.jpg").mkdir()
        reference = {str(path): path.stat().st_mtime_ns
                     for path in self.root.glob("*/760/remote/281990/screenshots/*.jpg")}
        self.assertEqual(self.namespace["screenshot_mtimes"](), reference)

    def test_missing_root_and_leaf_match_empty_glob(self):
        self.namespace["STEAM_SCREENSHOTS"] = self.root / "missing"
        self.assertEqual(self.namespace["screenshot_mtimes"](), {})
        self.namespace["STEAM_SCREENSHOTS"] = self.root
        (self.root / "empty-profile").mkdir()
        self.assertEqual(self.namespace["screenshot_mtimes"](), {})

    def test_capture_accepts_new_file_and_selects_latest_mtime(self):
        self.image(self.leaf / "old.jpg")
        def fresh():
            self.image(self.leaf / "new.jpg", "blue", 1_700_000_000_001_000_000)
            self.image(self.leaf / "latest.jpg", "green", 1_700_000_000_002_000_000)
        self.on_f12 = fresh
        result = self.namespace["gpu_capture"]("new-file")
        self.assertEqual(Path(result["image"]).read_bytes(), (self.leaf / "latest.jpg").read_bytes())
        self.assertEqual(result["rows"], [])
        self.assertEqual(self.clock, .2)
        self.assertEqual(len(self.saved), 1)

    def test_capture_accepts_modified_existing_path(self):
        path = self.image(self.leaf / "existing.jpg")
        self.on_f12 = lambda: self.image(path, "blue", 1_700_000_000_001_000_000)
        result = self.namespace["gpu_capture"]("modified")
        self.assertEqual(Path(result["image"]).read_bytes(), path.read_bytes())
        self.assertEqual(self.clock, .2)

    def test_capture_rejects_no_new_file_and_older_mtime(self):
        path = self.image(self.leaf / "old.jpg")
        self.on_f12 = lambda: os.utime(path, ns=(1, 1))
        with self.assertRaisesRegex(RuntimeError, "did not produce a fresh GPU screenshot"):
            self.namespace["gpu_capture"]("unchanged")
        self.assertGreaterEqual(self.clock, 12.)
        self.assertEqual(self.saved, [])
        self.assertFalse((self.artifacts / "unchanged.jpg").exists())

    def test_capture_rejects_unchanged_existing_file(self):
        self.image(self.leaf / "old.jpg")
        with self.assertRaisesRegex(RuntimeError, "did not produce a fresh GPU screenshot"):
            self.namespace["gpu_capture"]("same-mtime")
        self.assertGreaterEqual(self.clock, 12.)
        self.assertEqual(self.saved, [])


if __name__ == "__main__":
    unittest.main()
