"""Execute only extracted focus helpers with fake APIs; never import the desktop harness."""
import ast
import copy
import ctypes
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch


SOURCE = Path(__file__).resolve().parents[1] / "tools/runtime_single_homeworld.py"
OLD = SOURCE.parents[1] / "docs/evidence/1020-titlebar-focus-recovery/old-tool/runtime_single_homeworld.py"


class FocusError(Exception):
    def __init__(self, function="SetForegroundWindow"):
        super().__init__(0, function, "synthetic API denial")
        self.funcname = function


class TitlebarFocusTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.artifacts = Path(self.temporary.name)
        self.foreground = 77
        self.titlebar = {"rect": [108, 108, 1132, 130], "states": [0] * 6}
        self.gui = SimpleNamespace(
            GetForegroundWindow=Mock(side_effect=lambda: self.foreground),
            GetCursorPos=Mock(return_value=(42, 43)),
            IsWindow=Mock(return_value=True), IsWindowVisible=Mock(return_value=True),
            IsWindowEnabled=Mock(return_value=True), IsIconic=Mock(return_value=False),
            GetWindowText=Mock(return_value="Stellaris"),
            GetClientRect=Mock(return_value=(0, 0, 1024, 768)),
            ClientToScreen=Mock(return_value=(108, 131)),
            GetWindowRect=Mock(return_value=(100, 100, 1140, 907)),
            GetWindowLong=Mock(return_value=0x00c00000), SetWindowPos=Mock(),
            WindowFromPoint=Mock(return_value=100), GetAncestor=Mock(return_value=100))
        self.processes = {123: "stellaris.exe", 77: "ChatGPT.exe"}
        self.api = SimpleNamespace(
            win32gui=self.gui,
            win32con=SimpleNamespace(WM_NCHITTEST=0x84, HTCAPTION=2,
                GWL_STYLE=-16, WS_CAPTION=0x00c00000, HWND_TOP=0, GA_ROOT=2,
                SWP_NOMOVE=2, SWP_NOSIZE=1, SWP_NOACTIVATE=0x10),
            win32process=SimpleNamespace(GetWindowThreadProcessId=Mock(
                side_effect=lambda hwnd: (1, 123 if hwnd == 100 else 77))),
            psutil=SimpleNamespace(Process=Mock(side_effect=lambda pid:
                SimpleNamespace(name=lambda: self.processes[pid]))),
            windows_for_pid=Mock(return_value=[100]),
            process_record=Mock(return_value={"pid": 123}),
            load_run=Mock(return_value=(self.artifacts, None, {})),
            pyautogui=SimpleNamespace(click=Mock(side_effect=self.clicked), failSafeCheck=Mock()))
        self.original = Mock(side_effect=FocusError())
        self.tree = ast.parse(SOURCE.read_text(encoding="utf-8-sig"))
        functions = [node for node in self.tree.body if isinstance(node, ast.FunctionDef)
                     and (node.name.startswith("_focus_") or node.name == "focus_current_window")]
        self.namespace = {"h": self.api, "original_focus": self.original,
                          "json": json, "time": SimpleNamespace(sleep=Mock())}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(SOURCE), "exec"), self.namespace)
        self.real_titlebar = self.namespace["_focus_titlebar_info"]
        self.real_hit = self.namespace["_focus_caption_hit"]
        self.info = self.namespace["_focus_titlebar_info"] = Mock(
            side_effect=lambda hwnd: copy.deepcopy(self.titlebar))
        self.hit = self.namespace["_focus_caption_hit"] = Mock(return_value=2)
        self.addCleanup(patch.stopall)
        patch.dict(sys.modules, {"pywintypes": SimpleNamespace(error=FocusError)}).start()

    def clicked(self, *point):
        self.foreground = 100

    def focus(self, pid=123):
        return self.namespace["focus_current_window"](pid)

    def records(self):
        return [json.loads(p.read_text(encoding="utf-8"))
                for p in self.artifacts.glob("focus-titlebar-recovery-*.action.json")]

    def rejected(self, pattern):
        with self.assertRaisesRegex(Exception, pattern):
            self.focus()
        self.api.pyautogui.click.assert_not_called()
        records = self.records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["status"], "FAILED")
        self.assertIn("failure", records[0])

    def test_already_foreground_is_unchanged_without_fallback(self):
        self.foreground = 100
        self.assertEqual(self.focus(), 100)
        self.original.assert_not_called()
        self.api.load_run.assert_not_called()
        self.assertEqual(self.records(), [])

    def test_original_success_is_unchanged_without_fallback(self):
        self.original.side_effect = None
        self.original.return_value = 100
        self.assertEqual(self.focus(), 100)
        self.original.assert_called_once_with(123)
        self.api.load_run.assert_not_called()
        self.assertEqual(self.records(), [])

    def test_unrelated_exception_does_not_fallback(self):
        self.original.side_effect = RuntimeError("locked or no window")
        with self.assertRaisesRegex(RuntimeError, "locked or no window"):
            self.focus()
        self.api.load_run.assert_not_called()
        self.assertEqual(self.records(), [])

    def test_other_win32_function_does_not_fallback(self):
        self.original.side_effect = FocusError("ShowWindow")
        with self.assertRaises(FocusError):
            self.focus()
        self.api.load_run.assert_not_called()
        self.assertEqual(self.records(), [])

    def test_original_failsafe_exception_never_enters_recovery(self):
        class FailSafeException(Exception):
            pass
        self.original.side_effect = FailSafeException("corner stop")
        with self.assertRaisesRegex(FailSafeException, "corner stop"):
            self.focus()
        self.api.load_run.assert_not_called()
        self.gui.SetWindowPos.assert_not_called()
        self.api.pyautogui.click.assert_not_called()

    def test_direct_recovery_checks_failsafe_before_any_window_action(self):
        self.api.pyautogui.failSafeCheck.side_effect = RuntimeError("corner stop")
        with self.assertRaisesRegex(RuntimeError, "corner stop"):
            self.namespace["_focus_recover_titlebar"](123, FocusError())
        self.api.process_record.assert_not_called()
        self.gui.SetWindowPos.assert_not_called()
        self.api.pyautogui.click.assert_not_called()
        self.assertEqual(self.records()[0]["phase"], "failsafe_before_validation")

    def test_failsafe_before_raise_prevents_z_order_and_click(self):
        self.api.pyautogui.failSafeCheck.side_effect = [None, RuntimeError("corner stop")]
        self.rejected("corner stop")
        self.gui.SetWindowPos.assert_not_called()

    def test_failsafe_before_click_prevents_physical_input(self):
        self.api.pyautogui.failSafeCheck.side_effect = [None, None, RuntimeError("corner stop")]
        self.rejected("corner stop")
        self.gui.SetWindowPos.assert_called_once()

    def test_current_run_pid_must_match(self):
        self.api.process_record.return_value = {"pid": 456}
        self.rejected("not the current run")
        self.gui.SetWindowPos.assert_not_called()

    def test_process_must_be_stellaris(self):
        self.processes[123] = "other.exe"
        self.rejected("not stellaris.exe")

    def test_unreadable_cursor_is_not_recovered(self):
        self.gui.GetCursorPos.side_effect = OSError("desktop unavailable")
        self.rejected("desktop unavailable")
        self.gui.SetWindowPos.assert_not_called()

    def test_lockapp_is_not_recovered(self):
        self.processes[77] = "LockApp.exe"
        self.rejected("desktop is locked")
        self.gui.SetWindowPos.assert_not_called()

    def test_no_window_is_rejected(self):
        self.api.windows_for_pid.return_value = []
        self.rejected("one unique")

    def test_multiple_windows_are_rejected(self):
        self.api.windows_for_pid.return_value = [100, 101]
        self.rejected("one unique")

    def test_invalid_window_is_rejected(self):
        self.gui.IsWindow.return_value = False
        self.rejected("invalid, hidden")

    def test_hidden_window_is_rejected(self):
        self.gui.IsWindowVisible.return_value = False
        self.rejected("invalid, hidden")

    def test_disabled_window_is_rejected(self):
        self.gui.IsWindowEnabled.return_value = False
        self.rejected("disabled")

    def test_minimized_window_is_rejected(self):
        self.gui.IsIconic.return_value = True
        self.rejected("minimized")

    def test_window_pid_is_independently_rechecked(self):
        self.api.win32process.GetWindowThreadProcessId.side_effect = lambda hwnd: (1, 77)
        self.rejected("PID or title differs")

    def test_wrong_title_is_rejected(self):
        self.gui.GetWindowText.return_value = "Stellaris other window"
        self.rejected("PID or title differs")

    def test_wrong_client_size_is_rejected(self):
        self.gui.GetClientRect.return_value = (0, 0, 1600, 900)
        self.rejected("client size")

    def test_borderless_window_has_no_native_caption(self):
        self.gui.GetWindowLong.return_value = 0
        self.rejected("native caption")

    def test_titlebar_query_failure_is_rejected(self):
        self.info.side_effect = OSError("no real titlebar")
        self.rejected("no real titlebar")

    def test_unavailable_invisible_offscreen_titlebars_are_rejected(self):
        for state in (1, 0x8000, 0x10000):
            with self.subTest(state=state):
                self.titlebar["states"][0] = state
                with self.assertRaisesRegex(RuntimeError, "unavailable"):
                    self.focus()
        self.assertEqual(len(self.records()), 3)
        self.api.pyautogui.click.assert_not_called()
        self.gui.SetWindowPos.assert_not_called()

    def test_invalid_titlebar_rectangle_is_rejected(self):
        self.titlebar["rect"] = [108, 108, 108, 130]
        self.rejected("outside the nonclient")

    def test_titlebar_inside_client_viewport_is_rejected(self):
        self.titlebar["rect"] = [108, 150, 1132, 170]
        self.rejected("outside the nonclient")

    def test_caption_buttons_client_and_other_hits_are_rejected(self):
        for hit in (1, 8, 9, 20, 21, 0, 18):
            with self.subTest(hit=hit):
                self.hit.return_value = hit
                with self.assertRaisesRegex(RuntimeError, "not HTCAPTION"):
                    self.focus()
        self.assertEqual(len(self.records()), 7)
        self.api.pyautogui.click.assert_not_called()
        self.gui.SetWindowPos.assert_not_called()

    def test_z_order_raise_failure_is_recorded_without_click(self):
        self.gui.SetWindowPos.side_effect = OSError("raise refused")
        self.rejected("raise refused")
        self.assertEqual(self.records()[0]["phase"], "raise_without_activation")

    def test_handle_disappearing_after_raise_is_rejected(self):
        self.gui.IsWindow.side_effect = [True, False]
        self.rejected("invalid, hidden")
        self.gui.SetWindowPos.assert_called_once()

    def test_new_unique_handle_after_raise_is_rejected(self):
        self.api.windows_for_pid.side_effect = [[100], [100], [101]]
        self.api.win32process.GetWindowThreadProcessId.side_effect = (
            lambda hwnd: (1, 123 if hwnd in (100, 101) else 77))
        self.rejected("target or geometry changed")

    def test_geometry_change_after_raise_is_rejected(self):
        self.gui.ClientToScreen.side_effect = [(108, 131), (109, 131)]
        self.rejected("target or geometry changed")

    def test_titlebar_rectangle_change_after_raise_is_rejected(self):
        later = copy.deepcopy(self.titlebar)
        later["rect"][0] += 1
        self.info.side_effect = [self.titlebar, later]
        self.rejected("target or geometry changed")

    def test_window_covering_point_after_raise_is_rejected(self):
        self.gui.WindowFromPoint.return_value = 77
        self.rejected("covered by another window")

    def test_point_root_must_also_match(self):
        self.gui.GetAncestor.return_value = 77
        self.rejected("covered by another window")

    def test_late_hit_test_change_prevents_click(self):
        self.hit.side_effect = [2, 2, 1]
        self.rejected("changed before click")

    def test_late_cursor_failure_prevents_click(self):
        self.gui.GetCursorPos.side_effect = [(42, 43), OSError("cursor lost")]
        self.rejected("cursor lost")

    def test_success_raises_without_activation_then_clicks_only_titlebar(self):
        self.assertEqual(self.focus(), 100)
        self.gui.SetWindowPos.assert_called_once_with(100, 0, 0, 0, 0, 0, 0x13)
        self.gui.WindowFromPoint.assert_called_once_with((620, 119))
        self.gui.GetAncestor.assert_called_once_with(100, 2)
        self.api.pyautogui.click.assert_called_once_with(620, 119)
        record, = self.records()
        self.assertEqual(record["status"], "FOREGROUND_VERIFIED")
        self.assertEqual(record["after_click"]["foreground"], 100)
        self.assertEqual(record["clicked_point"], [620, 119])
        self.assertNotIn("failure", record)

    def test_click_without_foreground_is_failure(self):
        self.api.pyautogui.click.side_effect = None
        with self.assertRaisesRegex(RuntimeError, "did not establish"):
            self.focus()
        self.api.pyautogui.click.assert_called_once_with(620, 119)
        record, = self.records()
        self.assertEqual(record["status"], "FAILED")
        self.assertEqual(record["after_click"]["foreground"], 77)

    def test_click_exception_is_failure(self):
        self.api.pyautogui.click.side_effect = OSError("physical input failed")
        with self.assertRaisesRegex(OSError, "physical input failed"):
            self.focus()
        self.assertEqual(self.records()[0]["status"], "FAILED")

    def test_new_failure_record_does_not_overwrite_existing_actions(self):
        old = self.artifacts / "preexisting.action.json"
        old.write_bytes(b"original immutable action\r\n")
        for _ in range(2):
            self.foreground = 77
            self.assertEqual(self.focus(), 100)
        self.assertEqual(old.read_bytes(), b"original immutable action\r\n")
        self.assertEqual(len(self.records()), 2)

    def test_exclusive_record_collision_prevents_all_actions(self):
        name = "a" * 32
        old = self.artifacts / ("focus-titlebar-recovery-" + name + ".action.json")
        old.write_bytes(b"existing evidence")
        with patch("uuid.uuid4", return_value=SimpleNamespace(hex=name)):
            with self.assertRaises(FileExistsError):
                self.focus()
        self.assertEqual(old.read_bytes(), b"existing evidence")
        self.gui.SetWindowPos.assert_not_called()
        self.api.pyautogui.click.assert_not_called()

    def test_real_titlebar_wrapper_uses_sized_structure_and_pointer_safe_handle(self):
        def fill(hwnd, pointer):
            self.assertEqual(hwnd, 0x123456789)
            info = pointer._obj
            self.assertEqual(info.cbSize, ctypes.sizeof(info))
            info.rcTitleBar.left, info.rcTitleBar.top = 100, 101
            info.rcTitleBar.right, info.rcTitleBar.bottom = 900, 130
            info.rgstate[0] = 0x100000
            return 1
        query = Mock(side_effect=fill)
        with patch("ctypes.WinDLL", return_value=SimpleNamespace(GetTitleBarInfo=query)):
            self.assertEqual(self.real_titlebar(0x123456789),
                {"rect": [100, 101, 900, 130], "states": [0x100000, 0, 0, 0, 0, 0]})
        self.assertEqual(ctypes.sizeof(query.argtypes[0]), ctypes.sizeof(ctypes.c_void_p))

    def test_titlebar_native_query_false_raises(self):
        with patch("ctypes.WinDLL", return_value=SimpleNamespace(GetTitleBarInfo=Mock(return_value=0))):
            with self.assertRaises(OSError):
                self.real_titlebar(100)

    def test_hit_test_native_wrapper_is_bounded_and_packs_signed_coordinates(self):
        def hit(hwnd, message, wparam, packed, flags, timeout, result):
            self.assertEqual((hwnd, message, wparam, flags, timeout),
                             (0x123456789, 0x84, 0, 0x22, 2000))
            self.assertEqual(packed, ((-20 & 0xffff) | (119 << 16)))
            result._obj.value = 2
            return 1
        query = Mock(side_effect=hit)
        with patch("ctypes.WinDLL", return_value=SimpleNamespace(SendMessageTimeoutW=query)):
            self.assertEqual(self.real_hit(0x123456789, [-20, 119]), 2)
        self.assertEqual(ctypes.sizeof(query.argtypes[0]), ctypes.sizeof(ctypes.c_void_p))

    def test_native_hit_timeout_never_becomes_caption(self):
        with patch("ctypes.WinDLL", return_value=SimpleNamespace(SendMessageTimeoutW=Mock(return_value=0))):
            with self.assertRaisesRegex(RuntimeError, "failed or timed out"):
                self.real_hit(100, [620, 119])

    def test_unrepresentable_hit_coordinates_are_rejected(self):
        query = Mock()
        with patch("ctypes.WinDLL", return_value=SimpleNamespace(SendMessageTimeoutW=query)):
            with self.assertRaisesRegex(RuntimeError, "cannot be represented"):
                self.real_hit(100, [32768, 119])
        query.assert_not_called()

    def test_all_other_original_top_level_nodes_are_identical(self):
        old_tree = ast.parse(OLD.read_text(encoding="utf-8-sig"))
        def preserved(tree):
            return [ast.dump(node, include_attributes=False) for node in tree.body
                    if not (isinstance(node, ast.FunctionDef)
                            and (node.name.startswith("_focus_") or node.name == "focus_current_window"))]
        self.assertEqual(preserved(old_tree), preserved(self.tree))


if __name__ == "__main__":
    unittest.main()
