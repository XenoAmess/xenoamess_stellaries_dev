"""Freeze completed purifier/hive worker UI; no Machine, SAV copies or logs."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
MOD = REPO / "eat_everything_origin"
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
BRANCHES = {"purifier": "r6pu", "hive": "r6hvc"}
SOURCES = ("runtime_economy_1019.py", "runtime_growth_1019.py", "runtime_single_homeworld.py")
FOUR = ("no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband")


def fp(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def main():
    assert not (OUT / "index.json").exists()
    previous = OUT.parent / "1019-rc6-purifier-mothership-ui-v1"
    post = {Path(row["path"]).name for row in json.loads((previous / "index.json").read_bytes())["files"]}
    files, refs, branches = {}, {}, {}
    for branch, prefix in BRANCHES.items():
        canonical = OUT.parent / "1019-rc6-economy" / branch
        receipt = json.loads((canonical / (prefix + "-economy-receipt.json")).read_bytes())
        assert len(receipt["commands"]) == len(receipt["snapshots"]) == 12
        assert receipt["state"] == "COLLECTED_NOT_ACCEPTED"
        assert fp(MOD / "tools/runtime_economy_1019.py")["sha256"] == receipt["collector_sha256"]
        for number, command in enumerate(receipt["commands"], 1):
            assert command["command"] == command["input_action"]["text"] == "fast_forward 30"
            stage = prefix + f"m{number:02d}"
            action = RUN / (stage + "-advance-command.action.json")
            actual = json.loads(action.read_bytes())
            assert actual == command["input_action"] and actual["submitted"] is True
        for path in canonical.iterdir():
            if path.is_file():
                refs[str(path.resolve())] = {"path": str(path.resolve()), **fp(path)}
        prefixes = [prefix + "-"] + [prefix + f"m{i:02d}-" for i in range(13)] + [prefix + "yearui-"]
        for start in prefixes:
            for path in RUN.glob(start + "*"):
                if not path.is_file() or path.name in post: continue
                if (path.suffix in (".jpg", ".png") or path.name.endswith((".action.json", ".ocr.json", ".wait.json"))):
                    files[branch + "/" + path.name] = path
        for snapshot in receipt["snapshots"]:
            image = Path(snapshot["hud"]["image"])
            assert branch + "/" + image.name in files and fp(image)["sha256"] == snapshot["hud"]["image_sha256"]
        branches[branch] = {"receipt": {"path": (canonical / (prefix + "-economy-receipt.json")).relative_to(MOD).as_posix(), **fp(canonical / (prefix + "-economy-receipt.json"))},
                            "scope": "Native new_game plus existing collect worker only; root-exclusive execution handoff; not system-wide input audit",
                            "recorded_FF30_count": 12, "four_checks_await_root_review": {key: None for key in FOUR},
                            "root_handoff": "No other UI/console until total receipt completed; post-Purifier maintenance UI is separate",
                            "memory_loaded_source_proof": False}
    for name in SOURCES: files["source/" + name] = MOD / "tools" / name
    rows = [{"path": rel, "source": str(path.resolve()), **fp(path)} for rel, path in sorted(files.items())]
    selection = {"schema": "eep.rc6.economy-worker-ui-selection.v1", "created_at_utc": datetime.now(timezone.utc).isoformat(),
                 "run_id": "20261019T150008Z", "branches": BRANCHES, "excluded_post_UI_filenames": sorted(post), "files": rows,
                 "exclusions": ["Machine r6mc", "all logs", "all SAV copies and economic collector duplicates", "85 post-Purifier UI files", "other live branches"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists() and Path(row["path"]).suffix not in (".sav", ".log") and "r6mc" not in row["path"]
        target.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    index = {"schema": "eep.rc6.economy-worker-ui-index.v1", "status": "OBSERVATION_ONLY_FOUR_CHECKS_AWAIT_ROOT_REVIEW",
             "run_id": "20261019T150008Z", "created_at_utc": datetime.now(timezone.utc).isoformat(),
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "payload_files": len(rows), "payload_bytes": sum(row["bytes"] for row in rows),
             "branches": branches, "files": rows, "canonical_references_not_copied": sorted(refs.values(), key=lambda row: row["path"]),
             "source_scope": "Collector exact SHA matches both original receipts; other source files are posthoc on-disk review copies, no historical-memory claim; indirect changing publish/check dependencies not backfilled",
             "system_wide_input_audit": False, "case_status_promoted": False, "active_logs_or_Machine_read": False, "UI_or_Git_operations": False}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("purifier/** -text\nhive/** -text\nsource/** -text\n", encoding="ascii")
    print(json.dumps({key: index[key] for key in ("status", "payload_files", "payload_bytes")}))


if __name__ == "__main__": main()
