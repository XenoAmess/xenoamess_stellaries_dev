from __future__ import annotations

import hashlib
import json
import re
import struct
import unittest
from pathlib import Path

from PIL import Image


REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_ROOT = REPO_ROOT / "gray_wind_beautification"
MOD_ROOT = DIST_ROOT / "mod"
CONTRACT_PATH = REPO_ROOT / "fixtures/gray-wind/mod-contract.json"
GAME_ROOT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def read_dds(path: Path) -> tuple[dict[str, int], bytes]:
    data = path.read_bytes()
    if data[:4] != b"DDS ":
        raise AssertionError(f"Not a DDS file: {path}")
    header = struct.unpack("<31I", data[4:128])
    info = {
        "header_size": header[0],
        "flags": header[1],
        "height": header[2],
        "width": header[3],
        "pitch": header[4],
        "mipmap_count": header[6],
        "pf_size": header[18],
        "pf_flags": header[19],
        "fourcc": header[20],
        "rgb_bits": header[21],
        "r_mask": header[22],
        "g_mask": header[23],
        "b_mask": header[24],
        "a_mask": header[25],
        "caps": header[26],
    }
    return info, data[128:]


def dds_rgba(path: Path) -> Image.Image:
    info, pixels = read_dds(path)
    size = (info["width"], info["height"])
    bgra = Image.frombytes("RGBA", size, pixels)
    blue, green, red, alpha = bgra.split()
    return Image.merge("RGBA", (red, green, blue, alpha))


class GrayWindPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_identity_and_version_are_independent(self) -> None:
        version = (DIST_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        descriptor = (MOD_ROOT / "descriptor.mod").read_text(encoding="utf-8-sig")
        self.assertIn(f'version="{version}"', descriptor)
        self.assertIn('name="[XenoAmess的灰风美化]"', descriptor)
        self.assertIn('supported_version="4.4.*"', descriptor)
        self.assertIn('picture="thumbnail.png"', descriptor)
        self.assertNotIn("remote_file_id", descriptor)
        self.assertEqual("xenoamess_gray_wind_beautification", self.contract["local_mod_id"])

        mod_bytes = b"".join(
            path.read_bytes() for path in MOD_ROOT.rglob("*") if path.is_file()
        )
        for forbidden_id in self.contract["forbidden_workshop_ids"]:
            self.assertNotIn(forbidden_id.encode("ascii"), mod_bytes)

    def test_art_files_have_exact_contract(self) -> None:
        expected = {
            "gfx/models/portraits/xenoamess_gray_wind_portrait.dds": (
                (800, 350),
                "99CBA6A4221AD9D9BC76D7153619913709518F19BD60ACA3B3F9B6BD67F22E27",
            ),
            "gfx/event_pictures/xenoamess_gray_wind_first_contact.dds": (
                (450, 150),
                "08A19EB5641606F505D1492981A31A1EAB9CF672D7ED286773B2564ECB499E07",
            ),
            "gfx/event_pictures/xenoamess_gray_wind_defeated.dds": (
                (450, 150),
                "49D007CA03491C0F5FD564ACCB5F26CD104557A96436E946A8D88060CF54261D",
            ),
            "gfx/event_pictures/xenoamess_gray_wind_return.dds": (
                (450, 150),
                "D82A715B719B5B2C7EBDF8DAACAED69904B65225484ECC3D305FBC74CEBC443C",
            ),
        }
        for relative, (size, expected_hash) in expected.items():
            path = MOD_ROOT / relative
            info, pixels = read_dds(path)
            self.assertEqual(size, (info["width"], info["height"]), relative)
            self.assertEqual(124, info["header_size"], relative)
            self.assertEqual(size[0] * 4, info["pitch"], relative)
            self.assertEqual(0, info["mipmap_count"], relative)
            self.assertEqual(32, info["pf_size"], relative)
            self.assertEqual(0x41, info["pf_flags"], relative)
            self.assertEqual(0, info["fourcc"], relative)
            self.assertEqual(32, info["rgb_bits"], relative)
            self.assertEqual(0x00FF0000, info["r_mask"], relative)
            self.assertEqual(0x0000FF00, info["g_mask"], relative)
            self.assertEqual(0x000000FF, info["b_mask"], relative)
            self.assertEqual(0xFF000000, info["a_mask"], relative)
            self.assertEqual(size[0] * size[1] * 4, len(pixels), relative)
            self.assertEqual(expected_hash, sha256(path), relative)

        thumbnail = MOD_ROOT / "thumbnail.png"
        with Image.open(thumbnail) as image:
            self.assertEqual((351, 313), image.size)
        self.assertEqual(
            "BAACCACA753870319B003A1ED86E733A935EEA3BD4D3C5B7EDA21D6B25902A2C",
            sha256(thumbnail),
        )

    def test_portrait_alpha_and_event_opacity(self) -> None:
        portrait = dds_rgba(
            MOD_ROOT / "gfx/models/portraits/xenoamess_gray_wind_portrait.dds"
        )
        alpha = portrait.getchannel("A")
        self.assertEqual([0, 0, 0, 0], [
            alpha.getpixel((0, 0)),
            alpha.getpixel((799, 0)),
            alpha.getpixel((0, 349)),
            alpha.getpixel((799, 349)),
        ])
        extrema = alpha.getextrema()
        self.assertEqual((0, 255), extrema)
        histogram = alpha.histogram()
        self.assertGreater(sum(histogram[1:255]), 0, "portrait needs antialiased alpha")
        self.assertGreater(sum(histogram[1:]), 10_000, "portrait visible area is too small")

        for filename in (
            "xenoamess_gray_wind_first_contact.dds",
            "xenoamess_gray_wind_defeated.dds",
            "xenoamess_gray_wind_return.dds",
        ):
            alpha = dds_rgba(MOD_ROOT / "gfx/event_pictures" / filename).getchannel("A")
            self.assertEqual((255, 255), alpha.getextrema(), filename)

    def test_visual_references_are_unique_and_resolvable(self) -> None:
        scripts = "\n".join(
            path.read_text(encoding="utf-8-sig")
            for path in MOD_ROOT.rglob("*")
            if path.suffix in {".txt", ".gfx", ".mod"}
        )
        # One sprite definition plus the anomaly and graygoo.400 references.
        self.assertEqual(3, scripts.count("GFX_evt_xenoamess_gray_wind_first_contact"))
        self.assertEqual(3, scripts.count('name = "GFX_evt_xenoamess_gray_wind_'))
        # Three sprite definitions plus four event/anomaly references.
        self.assertEqual(7, scripts.count("GFX_evt_xenoamess_gray_wind_"))
        self.assertNotRegex(scripts, r'name\s*=\s*"GFX_evt_ship_in_orbit_2"')
        self.assertEqual(1, scripts.count("xenoamess_gray_wind_portrait = {"))
        self.assertEqual(1, scripts.count("namespace = xenoamess_gray_wind"))
        self.assertEqual(1, scripts.count("id = xenoamess_gray_wind.100"))

        texture_refs = re.findall(r'texturefile\s*=\s*"([^"]+)"', scripts)
        for texture_ref in texture_refs:
            self.assertTrue((MOD_ROOT / texture_ref).is_file(), texture_ref)

    @unittest.skipUnless(GAME_ROOT.is_dir(), "Stellaris 4.4.6 base files not installed")
    def test_overridden_files_are_minimal_patches_of_current_base(self) -> None:
        event_mod = (MOD_ROOT / "events/gray_goo_events.txt").read_text(encoding="utf-8-sig")
        event_base = (GAME_ROOT / "events/gray_goo_events.txt").read_text(encoding="utf-8-sig")
        restored = event_mod
        restored = restored.replace(
            "picture = GFX_evt_xenoamess_gray_wind_first_contact",
            "picture = GFX_evt_ship_in_orbit_2",
            1,
        )
        restored = restored.replace(
            "portrait = xenoamess_gray_wind_portrait", "portrait = root.species", 6
        )
        restored = restored.replace(
            "\t\t\tlast_created_leader = {\n"
            "\t\t\t\tchange_leader_portrait = xenoamess_gray_wind_portrait\n"
            "\t\t\t\tset_leader_flag = gray_leader\n"
            "\t\t\t}\n",
            "",
            1,
        )
        restored = restored.replace(
            "picture = GFX_evt_xenoamess_gray_wind_defeated",
            "picture = GFX_evt_circuitry_modification",
            1,
        )
        restored = restored.replace(
            "picture = GFX_evt_xenoamess_gray_wind_return",
            "picture = GFX_evt_gray_gooed_planet",
            1,
        )
        self.assertEqual(event_base, restored)

        anomaly_mod = (
            MOD_ROOT / "common/anomalies/95_anomaly_categories_distant_stars.txt"
        ).read_text(encoding="utf-8-sig")
        anomaly_base = (
            GAME_ROOT / "common/anomalies/95_anomaly_categories_distant_stars.txt"
        ).read_text(encoding="utf-8-sig")
        anomaly_restored = anomaly_mod.replace(
            'picture = "GFX_evt_xenoamess_gray_wind_first_contact"',
            'picture = "GFX_evt_ship_in_orbit_2"',
            1,
        )
        self.assertEqual(anomaly_base, anomaly_restored)

        effects_mod = (
            MOD_ROOT / "common/scripted_effects/gray_goo_effects.txt"
        ).read_text(encoding="utf-8-sig")
        effects_base = (
            GAME_ROOT / "common/scripted_effects/gray_goo_effects.txt"
        ).read_text(encoding="utf-8-sig")
        effects_restored = effects_mod.replace(
            "\t\tchange_leader_portrait = xenoamess_gray_wind_portrait\n", "", 1
        )
        self.assertEqual(effects_base, effects_restored)

    def test_upload_folder_is_clean(self) -> None:
        forbidden_names = {
            ".idea",
            "__pycache__",
            "evidence",
            "tools",
            ".git",
            "workspace.xml",
        }
        for path in MOD_ROOT.rglob("*"):
            self.assertFalse(any(part in forbidden_names for part in path.parts), path)
            self.assertNotIn(path.suffix.lower(), {".py", ".pyc", ".zip"}, path)

        self.assertLess((MOD_ROOT / "thumbnail.png").stat().st_size, 1_000_000)


if __name__ == "__main__":
    unittest.main()
