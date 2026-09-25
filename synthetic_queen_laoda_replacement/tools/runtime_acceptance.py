"""Bind the shared isolated Stellaris harness to the Laoda portrait replacement."""

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
acceptance.EXPECTED_EXE_SHA256 = (
    "6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4"
)
acceptance.EXPECTED_MOD_TREE_SHA256 = (
    "3570b2e5a721b44f9e3f86e77e0a9cef09a625daff173481be96ee91ac5d4b1d"
)
acceptance.WORKSHOP_ID = "xenoamess_synthetic_queen_laoda_replacement"
acceptance.PROFILE_ID = "stellaris-4.5.1-cetana-static-portrait"
acceptance.RUNTIME_ROOT = DIST_ROOT / "evidence" / "runtime"
acceptance.CURRENT_RUN = acceptance.RUNTIME_ROOT / "current-run.json"
acceptance.DIRECTX_REDIST_CAB = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common\Steamworks Shared"
    r"\_CommonRedist\DirectX\Jun2010\Jun2010_d3dx9_43_x64.cab"
)


if __name__ == "__main__":
    raise SystemExit(acceptance.main())
