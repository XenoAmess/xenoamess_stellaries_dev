"""Archive completed Machine worker UI only; exclude init2, growth and logs."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
MOD = OUT.parents[2]
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
CANONICAL = OUT.parent / "1019-rc6-economy/machine"
PRIOR = OUT.parent / "1019-rc6-economy-worker-ui-v1"


def fp(path):
    raw = path.read_bytes(); return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def main():
    assert not (OUT / "index.json").exists()
    receipt = json.loads((CANONICAL / "r6mc-economy-receipt.json").read_bytes())
    assert receipt["state"] == "COLLECTED_NOT_ACCEPTED" and len(receipt["commands"]) == len(receipt["snapshots"]) == 12
    files = {}
    for prefix in ["r6mc-"] + [f"r6mcm{i:02d}-" for i in range(13)] + ["r6mcyearui-"]:
        for p in RUN.glob(prefix + "*"):
            if p.is_file() and (p.suffix in (".jpg", ".png") or p.name.endswith((".action.json", ".ocr.json", ".wait.json"))):
                assert "r6mcinit2" not in p.name and not p.name.startswith("r6g")
                files["machine/" + p.name] = p
    for name in ("runtime_economy_1019.py", "runtime_growth_1019.py", "runtime_single_homeworld.py"):
        files["source/" + name] = PRIOR / "source" / name
    assert fp(files["source/runtime_economy_1019.py"])["sha256"] == receipt["collector_sha256"]
    for command in receipt["commands"]:
        actual = json.loads((RUN / (command["input_action"]["stage"] + ".action.json")).read_bytes())
        assert actual == command["input_action"] and actual["text"] == command["command"] == "fast_forward 30" and actual["submitted"]
    rows = [{"path": name, "source": str(p.resolve()), **fp(p)} for name, p in sorted(files.items())]
    selection = {"schema": "eep.rc6.machine-economy-worker-ui-selection.v1", "status": "COMPLETED_WORKER_ONLY",
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "files": rows,
                 "exclusions": ["r6mcinit2 separate repeat probe", "r6g active growth", "all logs", "SAV/audit copies already in thin archive"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        p = OUT / row["path"]; assert not p.exists(); p.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(row["source"], p)
        assert fp(p) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    refs = [{"path": str(p.resolve()), **fp(p)} for p in sorted(CANONICAL.iterdir()) if p.is_file()]
    result = {"schema": "eep.rc6.machine-economy-worker-ui-index.v1", "status": "OBSERVATION_ONLY_FOUR_CHECKS_AWAIT_ROOT_REVIEW",
              "run_id": "20261019T150008Z", "created_at_utc": datetime.now(timezone.utc).isoformat(), "files": rows,
              "payload_files": len(rows), "payload_bytes": sum(row["bytes"] for row in rows), "canonical_references_not_copied": refs,
              "selection_sha256": fp(OUT / "selection.json")["sha256"], "recorded_FF30_count": 12,
              "four_checks_await_root_review": {key: None for key in ("no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband")},
              "root_handoff": "Root exclusive native new_game + existing collect until total receipt; not system-wide input audit",
              "source_scope": "Exact collector SHA matches receipt; reused prior on-disk review snapshots do not prove historical process memory",
              "init2_growth_logs_read": False, "UI_or_Git_operations": False}
    (OUT / "index.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("machine/** -text\nsource/** -text\n", encoding="ascii")
    print(json.dumps({key: result[key] for key in ("status", "payload_files", "payload_bytes")}))


if __name__ == "__main__": main()
