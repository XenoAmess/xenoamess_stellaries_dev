"""Bounded, byte-verified documentary checkpoint; no live-game actions."""
import hashlib
import json
import shutil
from pathlib import Path

repo = Path.cwd().resolve()
pointer = json.loads((repo / "_runtime/heart-of-devouring/runs/current-run.json").read_text("utf-8"))
run = Path(pointer["artifact_dir"])
dest = repo / "eat_everything_origin/docs/evidence/terravore-march-victory-2026-10-14"
assert dest.resolve().is_relative_to(repo) and not dest.exists()
names = set()
stages = ["hope-route-mar15-native-22940315", "hope-route-mar22-native-22940322",
          "hope-route-mar22-market5000-native-22940322", "hope-route-mar22-return2-native-22940322"]
for stage in stages:
    names.update(stage + suffix for suffix in (".sav", ".audit.json", ".native-save.json", "-error-before.log", "-error-after.log"))
names.update([
    "terravore-resume-20261014-package-check.json",
    "hope-route-mar15-battle-return-guard-22940315-proof.json",
    "hope-route-mar22-observed-22940322-proof.json",
    "hope-route-mar22-victory-guard-22940322-proof.json",
    "hope-route-mar22-market5000-guard-22940322-proof.json",
    "hope-route-mar22-return-guard-22940322-proof.json",
    "hope-route-mar22-battle-result-inspection-20261014.json",
    "hope-route-mar22-source-scan-20261014.json",
    "hope-route-mar22-native-22940322-preflight.json",
    "hope-route-mar22-native-22940322-calendar-receipt.json",
    "hope-route-mar22-market5000-native-22940322-action-proof.json",
    "hope-route-mar22-market5000-native-22940322-buy.action.json",
    "hope-route-mar22-return-native-22940322-return-fleet3.action.json",
    "hope-route-mar22-return2-native-22940322-return-fleet2.action.json",
    "hope-route-mar22-market-quote5000-ui-proof.json",
    "hope-route-mar22-market-quote5000-after.ocr.json",
    "hope-route-mar22-market-quote5000-after.jpg",
    "hope-route-mar22-clean-combat-report-ui-proof.json",
    "hope-route-mar22-clean-combat-report-after.ocr.json",
    "hope-route-mar22-clean-combat-report-after.jpg",
    "hope-route-mar22-return-native-22940322-fleet2-selection.ocr.json",
    "hope-route-mar22-return-native-22940322-fleet2-selection.jpg",
    "hope-route-mar22-fleet2-return-tooltip-ui-proof.json",
    "hope-route-mar22-fleet2-return-tooltip-after.jpg",
])
executions = ["hope-route-mar15-battle-return-guard-20261014", "hope-route-mar22-battle-calendar-20261014",
              "hope-route-mar22-battle-observer-20261014", "hope-route-mar22-battle-result-inspection-20261014",
              "hope-route-mar22-victory-guard-20261014", "hope-route-mar22-market5000-20261014",
              "hope-route-mar22-market5000-guard-20261014", "hope-route-mar22-return-fleets-20261014",
              "hope-route-mar22-return-resume-20261014", "hope-route-mar22-return-guard-20261014",
              "hope-route-mar22-market-quote5000-20261014", "hope-route-mar22-clean-combat-report-20261014"]
for stage in executions:
    names.update(stage + suffix for suffix in ("-execution.json", "-stdout.txt", "-stderr.txt"))
    execution = json.loads((run / (stage + "-execution.json")).read_text("utf-8"))
    helper = Path(execution["command"][1]).name
    assert hashlib.sha256((run / helper).read_bytes()).hexdigest() == execution["helper_sha256"]
    names.add(helper)
names.add("record_current_helper.py")
sources = {name: run / name for name in names}
sources.update({"support-runtime.py": repo / "eat_everything_origin/tools/runtime.py",
                "support-audit_save.py": repo / "eat_everything_origin/tools/audit_save.py",
                "priority_terravore_native_state.py": repo / "_runtime/heart-of-devouring/priority_terravore_native_state.py",
                "archive-helper.py": Path(__file__).resolve()})
assert all(path.is_file() for path in sources.values())
size = sum(path.stat().st_size for path in sources.values())
assert shutil.disk_usage(repo).free > size * 3 + 20_000_000
dest.mkdir(parents=True)
(dest / ".gitattributes").write_bytes(b"* binary\n")
manifest = []
for name, src in sorted(sources.items()):
    data = src.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    target = dest / name
    assert target.resolve().is_relative_to(dest.resolve())
    target.write_bytes(data)
    assert hashlib.sha256(target.read_bytes()).hexdigest() == sha
    manifest.append({"file": name, "source": str(src), "bytes": len(data), "sha256": sha})
report = {"scope": "Bounded live paused March22 checkpoint; not exit/reload/full-route acceptance.",
          "source_run": pointer, "files": len(manifest), "bytes": size, "manifest": manifest,
          "support_scope": "support-runtime.py/audit_save.py captured at checkpoint; executed helper sources match recorded hashes."}
(dest / "source-snapshot.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"files": len(manifest), "bytes": size, "dest": str(dest), "status": "PASS_RAW_BYTE_CHECKPOINT"}), flush=True)
