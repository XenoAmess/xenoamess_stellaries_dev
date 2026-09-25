"""Bind the shared isolated Stellaris harness to the Synthetic Queen portrait mod."""

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
    "5b11638e90815b7487335f272ec1540fd4fa07057d818275803483edb41811ba"
)
acceptance.WORKSHOP_ID = "xenoamess_synthetic_queen_beautification"
acceptance.PROFILE_ID = "stellaris-4.4.6-cetana-static-portrait"
acceptance.RUNTIME_ROOT = DIST_ROOT / "evidence" / "runtime"
acceptance.CURRENT_RUN = acceptance.RUNTIME_ROOT / "current-run.json"
acceptance.DIRECTX_REDIST_CAB = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Steamworks Shared"
    r"\_CommonRedist\DirectX\Jun2010\Jun2010_d3dx9_43_x64.cab"
)


if __name__ == "__main__":
    raise SystemExit(acceptance.main())
