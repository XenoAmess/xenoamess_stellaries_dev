"""Bind the shared Stellaris desktop harness to the standalone Gray Wind mod."""

from __future__ import annotations

import sys
from pathlib import Path


DIST_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = DIST_ROOT.parent
sys.path.insert(0, str(REPO_ROOT))

from tools import stellaris_acceptance as acceptance  # noqa: E402


acceptance.MOD_ROOT = DIST_ROOT / "mod"
acceptance.GAME_EXE = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe"
)
acceptance.EXPECTED_MOD_TREE_SHA256 = (
    "214007f79e5d9ed12d08b04f19ac7df09b27ba8c78e36b514f9112d3adcbceb5"
)
acceptance.WORKSHOP_ID = "xenoamess_gray_wind_beautification"
acceptance.PROFILE_ID = "stellaris-4.4.6-gray-wind"
acceptance.RUNTIME_ROOT = DIST_ROOT / "evidence" / "runtime"
acceptance.CURRENT_RUN = acceptance.RUNTIME_ROOT / "current-run.json"
acceptance.DIRECTX_REDIST_CAB = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Steamworks Shared"
    r"\_CommonRedist\DirectX\Jun2010\Jun2010_d3dx9_43_x64.cab"
)


if __name__ == "__main__":
    raise SystemExit(acceptance.main())
