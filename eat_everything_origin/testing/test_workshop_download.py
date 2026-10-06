"""Offline protocol checks. These never initialize Steam or prove a download."""
import ctypes as C
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import publish


class ManualCallbacks:
    def __init__(self, entries):
        self.entries = list(entries)
        self.released = 0
        self.buffers = []

    def SteamAPI_ManualDispatch_RunFrame(self, pipe):
        pass

    def SteamAPI_ManualDispatch_GetNextCallback(self, pipe, destination):
        if not self.entries:
            return False
        callback, app, item, result, size = self.entries.pop(0)
        data = publish.DownloadResult(app, item, result)
        self.buffers.append(data)
        message = C.cast(destination, C.POINTER(publish.CallbackMessage)).contents
        message.callback = callback
        message.data = C.addressof(data)
        message.size = C.sizeof(data) if size is None else size
        return True

    def SteamAPI_ManualDispatch_FreeLastCallback(self, pipe):
        self.released += 1


class DownloadProtocolTests(unittest.TestCase):
    item = 9999999999

    def run_entries(self, entries):
        callbacks = ManualCallbacks(entries)
        steam = type("SimulatedSteam", (), {"dll": callbacks})()
        return callbacks, steam

    def test_ignores_other_app_item_and_callback_and_releases_all(self):
        callbacks, steam = self.run_entries([
            (3405, publish.APP_ID, self.item, 1, None),
            (3406, 480, self.item, 1, None),
            (3406, publish.APP_ID, self.item + 1, 1, None),
            (3406, publish.APP_ID, self.item, 1, None),
        ])
        result = publish.wait_download(steam, 1, self.item, 1)
        self.assertEqual(result["item_id"], self.item)
        self.assertEqual(callbacks.released, 4)

    def test_failed_result_is_rejected_and_released(self):
        callbacks, steam = self.run_entries([(3406, publish.APP_ID, self.item, 2, None)])
        with self.assertRaisesRegex(RuntimeError, "EResult 2"):
            publish.wait_download(steam, 1, self.item, 1)
        self.assertEqual(callbacks.released, 1)

    def test_short_structure_is_rejected_before_read_and_released(self):
        callbacks, steam = self.run_entries([(3406, publish.APP_ID, self.item, 1, 1)])
        with self.assertRaisesRegex(RuntimeError, "structure differs"):
            publish.wait_download(steam, 1, self.item, 1)
        self.assertEqual(callbacks.released, 1)

    def test_absent_callback_times_out(self):
        callbacks, steam = self.run_entries([])
        with self.assertRaisesRegex(RuntimeError, "timed out"):
            publish.wait_download(steam, 1, self.item, .01)
        self.assertEqual(callbacks.released, 0)


if __name__ == "__main__":
    unittest.main()
