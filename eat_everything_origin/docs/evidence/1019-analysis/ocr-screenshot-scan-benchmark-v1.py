"""Compare complete Steam screenshot metadata without desktop/game operations."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import time

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tools/runtime.py"
SCREENSHOTS = Path(r"D:\program files (x86)\steam\userdata")
OUTPUT = Path(__file__).with_suffix(".json")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mapping_sha(mapping):
    return hashlib.sha256(json.dumps(sorted(mapping.items()), separators=(",", ":")).encode()).hexdigest()


def main():
    if OUTPUT.exists():
        raise FileExistsError("refusing to overwrite scan evidence")
    tree = ast.parse(SOURCE.read_text(encoding="utf-8-sig"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "screenshot_mtimes")
    namespace = {"os": os, "Path": Path, "STEAM_SCREENSHOTS": SCREENSHOTS}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(SOURCE), "exec"), namespace)
    rounds = []
    for index in range(3):
        started = time.perf_counter()
        reference = {str(path): path.stat().st_mtime_ns
                     for path in SCREENSHOTS.glob("*/760/remote/281990/screenshots/*.jpg")}
        old_finished = time.perf_counter()
        observed = namespace["screenshot_mtimes"]()
        new_finished = time.perf_counter()
        row = {"round": index + 1, "glob_path_stat_seconds": old_finished - started,
               "scandir_seconds": new_finished - old_finished,
               "reference_count": len(reference), "observed_count": len(observed),
               "all_path_mtimes_exactly_equal": reference == observed,
               "reference_mapping_sha256": mapping_sha(reference),
               "observed_mapping_sha256": mapping_sha(observed),
               "missing_path_count": len(reference.keys() - observed.keys()),
               "extra_path_count": len(observed.keys() - reference.keys()),
               "changed_mtime_count": sum(reference[key] != observed[key] for key in reference.keys() & observed.keys())}
        rounds.append(row)
        print(json.dumps(row), flush=True)
    equal = all(row["all_path_mtimes_exactly_equal"] for row in rounds)
    stable = len({row["reference_mapping_sha256"] for row in rounds}) == 1
    old_median = statistics.median(row["glob_path_stat_seconds"] for row in rounds)
    new_median = statistics.median(row["scandir_seconds"] for row in rounds)
    result = {"schema": "eep.ocr-screenshot-scan.offline.v1",
              "status": "PASS_SCOPED" if equal and stable and new_median < old_median else "FAIL",
              "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "All current fixed Steam screenshot leaves, complete path/mtime mappings; no screenshot, focus or input operation.",
              "runtime_tool_sha256": sha(SOURCE), "benchmark_sha256": sha(Path(__file__)),
              "python": platform.python_version(), "rounds": rounds,
              "all_rounds_file_mapping_stable": stable,
              "glob_path_stat_median_seconds": old_median, "scandir_median_seconds": new_median,
              "median_speedup_ratio": old_median / new_median,
              "estimated_two_scan_seconds_saved": 2 * (old_median - new_median),
              "limits": ["Offline metadata speed only; full live F12/probe duration was not measured.",
                         "Images, OCR models/settings, full directory scope, before/fresh mtime test and failure contract are unchanged."]}
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "output": str(OUTPUT), "sha256": sha(OUTPUT),
                      "median_speedup_ratio": result["median_speedup_ratio"]}), flush=True)
    return 0 if result["status"] == "PASS_SCOPED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
