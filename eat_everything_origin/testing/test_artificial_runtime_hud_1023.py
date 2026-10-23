from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from runtime_artificial_1023 import hud_date_visible


def row(text, x, y):
    return {"text": text, "score": .99, "box": [[x, y], [x+65, y], [x+65, y+12], [x, y+12]]}


class HudDateTests(unittest.TestCase):
    def test_real_top_hud(self):
        self.assertTrue(hud_date_visible({"rows": [row("2200.01.03", 900, 2), row("暂停", 930, 17)]}, "2200.01.03"))

    def test_save_list_metadata_is_not_gameplay(self):
        self.assertFalse(hud_date_visible({"rows": [row("2200.01.03", 720, 440), row("读取存档", 720, 600)]}, "2200.01.03"))

    def test_wrong_game_date(self):
        self.assertFalse(hud_date_visible({"rows": [row("2201.05.01", 900, 2), row("暂停", 930, 17)]}, "2200.01.03"))

    def test_date_without_hud_pause_marker(self):
        self.assertFalse(hud_date_visible({"rows": [row("2200.01.03", 900, 2)]}, "2200.01.03"))

    def test_real_resource_bar_when_tiny_pause_text_is_not_recognized(self):
        rows = [row("2201.04.30", 915, 0), row("284+8", 45, 10), row("862+0", 115, 10), row("879+45", 260, 10)]
        self.assertTrue(hud_date_visible({"rows": rows}, "2201.04.30"))

    def test_resource_like_metadata_outside_top_bar_rejected(self):
        rows = [row("2201.04.30", 915, 0), row("284+8", 45, 300), row("862+0", 115, 300), row("879+45", 260, 300)]
        self.assertFalse(hud_date_visible({"rows": rows}, "2201.04.30"))


if __name__ == "__main__":
    unittest.main()
