"""Offline failures/retries for Workshop images; never initialize Steam."""
import ctypes as C
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import workshop_images as gallery


class SimulatedSteam:
    def __init__(self, previews=(), completed=None, fail=None):
        self.previews = list(previews)
        self.completed = completed or gallery.QueryCompleted(77, 1, 1, 1, False)
        self.fail = fail
        self.calls = []
        self.bound = []

    def fn(self, name, arguments, result):
        self.bound.append(name)

    def call(self, method, *arguments):
        self.calls.append((method, arguments))
        if method == self.fail:
            return False
        if method == "CreateQueryUGCDetailsRequest":
            return 77
        if method == "SendQueryUGCRequest":
            return 88
        if method == "GetQueryUGCNumAdditionalPreviews":
            return len(self.previews)
        if method == "GetQueryUGCAdditionalPreview":
            preview = self.previews[arguments[2]]
            arguments[3].value = preview["url"].encode()
            arguments[5].value = preview["filename"].encode()
            C.cast(arguments[7], C.POINTER(C.c_int32)).contents.value = preview["type"]
        return True

    def wait(self, handle, result_type, callback):
        if self.fail == "wait":
            raise TimeoutError("simulated query timeout")
        assert handle == 88 and result_type == gallery.QueryCompleted and callback == 3401
        return self.completed


class GalleryProtocolTests(unittest.TestCase):
    item = 9999999999
    preview = {"index": 0, "url": "https://example.invalid/original.jpg",
               "filename": "01.jpg", "type": 0}

    def test_uncached_query_reads_previews_and_releases_handle(self):
        steam = SimulatedSteam([self.preview])
        self.assertEqual(gallery.remote_previews(steam, self.item), [self.preview])
        self.assertIn(("SetAllowCachedResponse", (77, 0)), steam.calls)
        self.assertEqual(steam.calls[-1], ("ReleaseQueryUGCRequest", (77,)))

    def test_wrong_callback_cached_and_failed_results_reject_and_release(self):
        for result in (gallery.QueryCompleted(78, 1, 1, 1, False),
                       gallery.QueryCompleted(77, 2, 1, 1, False),
                       gallery.QueryCompleted(77, 1, 0, 0, False),
                       gallery.QueryCompleted(77, 1, 1, 1, True)):
            with self.subTest(result=(result.handle, result.result, result.returned, result.cached)):
                steam = SimulatedSteam(completed=result)
                with self.assertRaisesRegex(RuntimeError, "query result"):
                    gallery.remote_previews(steam, self.item)
                self.assertEqual(steam.calls[-1][0], "ReleaseQueryUGCRequest")

    def test_failed_configuration_read_and_timeout_release_handle(self):
        for method in ("SetReturnAdditionalPreviews", "SetAllowCachedResponse",
                       "GetQueryUGCAdditionalPreview", "wait"):
            with self.subTest(method=method):
                steam = SimulatedSteam([self.preview], fail=method)
                with self.assertRaises((RuntimeError, TimeoutError)):
                    gallery.remote_previews(steam, self.item)
                self.assertEqual(steam.calls[-1][0], "ReleaseQueryUGCRequest")

    def test_upstream_and_invalid_item_rejected_before_any_call(self):
        for item in (0, -1, gallery.FORBIDDEN_ID):
            steam = SimulatedSteam()
            with self.assertRaisesRegex(RuntimeError, "read-only"):
                gallery.remote_previews(steam, item)
            self.assertFalse(steam.calls)

    def test_retry_replaces_old_gallery_instead_of_adding_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "01.jpg"
            raw = b"frozen-image-payload"
            path.write_bytes(raw)
            images = [{"file": path.name, "sha256": hashlib.sha256(raw).hexdigest()}]
            steam = SimulatedSteam()
            gallery.replace_previews(steam, 99, [{}, {}, {}], images, folder)
            self.assertEqual([(name, args[:2]) for name, args in steam.calls], [
                ("RemoveItemPreview", (99, 2)), ("RemoveItemPreview", (99, 1)),
                ("RemoveItemPreview", (99, 0)), ("AddItemPreviewFile", (99, str(path).encode()))])

    def test_failed_removal_or_changed_image_does_not_add_new_previews(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "01.jpg"
            path.write_bytes(b"changed")
            images = [{"file": path.name, "sha256": hashlib.sha256(b"original").hexdigest()}]
            for fail in (None, "RemoveItemPreview"):
                steam = SimulatedSteam(fail=fail)
                with self.assertRaises(RuntimeError):
                    gallery.replace_previews(steam, 99, [{}], images, folder)
                self.assertFalse(any(name == "AddItemPreviewFile" for name, _ in steam.calls))

    def test_remote_count_order_type_filename_and_bytes_mismatches_fail(self):
        raw = b"actual-remote-payload"
        expected = [{"file": "workshop/images/01.jpg", "bytes": len(raw),
                     "sha256": hashlib.sha256(raw).hexdigest()}]
        self.assertEqual(gallery.verify_previews([self.preview], expected, lambda _: raw)[0]["sha256"],
                         expected[0]["sha256"])
        for actual, data in (([], raw), ([{**self.preview, "index": 1}], raw),
                             ([{**self.preview, "type": 1}], raw),
                             ([{**self.preview, "filename": "wrong.jpg"}], raw),
                             ([self.preview], b"tampered-remote-payload")):
            with self.subTest(actual=actual, data=data):
                with self.assertRaises(RuntimeError):
                    gallery.verify_previews(actual, expected, lambda _: data)

    def test_selected_gallery_is_valid_and_draft_cannot_publish(self):
        root = Path(__file__).resolve().parents[1]
        # Validate the selected historical gallery independently of a newer
        # gameplay candidate whose screenshots have not been selected yet.
        version = json.loads((root / "workshop/images-manifest.json").read_text(encoding="utf-8"))["version"]
        self.assertGreaterEqual(len(gallery.local_images(root, version, require_frozen=False)), 3)
        # Exercise a draft independently of the final release's real status.
        with tempfile.TemporaryDirectory() as folder:
            workshop = Path(folder) / "workshop"
            workshop.mkdir()
            draft = json.loads((root / "workshop/images-manifest.json").read_text(encoding="utf-8"))
            draft.update(status="COLLECTING", final_release_selection=False)
            (workshop / "images-manifest.json").write_text(json.dumps(draft), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "frozen"):
                gallery.local_images(folder, version)

    def test_in_place_preserves_correct_slot_and_replaces_only_changed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            images = []
            for name in ("01.jpg", "new02.jpg"):
                (root / name).write_bytes(name.encode())
                images.append({"file": name, "sha256": hashlib.sha256(name.encode()).hexdigest()})
            existing = [self.preview, {**self.preview, "index": 1, "filename": "old02.jpg"}]
            steam = SimulatedSteam()
            actions = gallery.update_previews_in_place(steam, 99, existing, images, root, lambda _: b"01.jpg")
            self.assertEqual([a["action"] for a in actions], ["KEEP", "REPLACE"])
            self.assertEqual(steam.calls, [("UpdateItemPreviewFile", (99, 1, str(root / "new02.jpg").encode()))])

    def test_in_place_missing_or_drifted_retained_image_prevents_all_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "01.jpg").write_bytes(b"original")
            images = [{"file": "01.jpg", "sha256": hashlib.sha256(b"original").hexdigest()}]
            def missing(_):
                raise OSError("HTTP404")
            for fetch in (missing, lambda _: b"drift"):
                steam = SimulatedSteam()
                with self.assertRaises((OSError, RuntimeError)):
                    gallery.update_previews_in_place(steam, 99, [self.preview], images, root, fetch)
                self.assertFalse(steam.calls)

    def test_in_place_wrong_count_or_position_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "01.jpg").write_bytes(b"original")
            images = [{"file": "01.jpg", "sha256": hashlib.sha256(b"original").hexdigest()}]
            for existing in ([], [{**self.preview, "index": 2}], [{**self.preview, "type": 1}]):
                steam = SimulatedSteam()
                with self.assertRaises(RuntimeError):
                    gallery.update_previews_in_place(steam, 99, existing, images, root, lambda _: b"original")
                self.assertFalse(steam.calls)

    def test_in_place_update_failure_does_not_delete_or_append(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "new.jpg").write_bytes(b"original")
            images = [{"file": "new.jpg", "sha256": hashlib.sha256(b"original").hexdigest()}]
            steam = SimulatedSteam(fail="UpdateItemPreviewFile")
            with self.assertRaisesRegex(RuntimeError, "in-place gallery update failed"):
                gallery.update_previews_in_place(steam, 99, [self.preview], images, root)
            self.assertEqual([name for name, _ in steam.calls], ["UpdateItemPreviewFile"])


if __name__ == "__main__":
    unittest.main()
