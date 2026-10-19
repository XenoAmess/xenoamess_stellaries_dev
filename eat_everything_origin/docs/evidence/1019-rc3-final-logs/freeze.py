"""Freeze only the stopped RC3 run's logs and three run proofs, byte for byte."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess

RUN_ID = "20261019T092935Z"
PID = 34832
BASE = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev")
USERDIR = BASE / "runs" / RUN_ID
ARTIFACT = BASE / "artifacts/1019-implementation/runs" / RUN_ID
OUT = Path(__file__).resolve().parent


def stamp():
    return datetime.now(timezone.utc).isoformat()


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def pid_probe():
    command = ("$taskProcess = Get-Process -Id 34832 -ErrorAction SilentlyContinue; "
               "if ($null -ne $taskProcess) { $taskProcess | Select-Object Id,ProcessName,StartTime | "
               "ConvertTo-Json -Compress; exit 1 }; Write-Output 'ABSENT'; exit 0")
    result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                            capture_output=True, text=True, check=False)
    probe = {"checked_at_utc": stamp(), "pid": PID, "returncode": result.returncode,
             "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    assert result.returncode == 0 and probe["stdout"] == "ABSENT" and not probe["stderr"], probe
    return probe


def sources():
    entries = {"logs/" + p.relative_to(USERDIR / "logs").as_posix(): p
               for p in sorted((USERDIR / "logs").rglob("*")) if p.is_file()}
    assert entries and not any(p.suffix.lower() == ".sav" for p in entries.values())
    for name in ("manifest.json", "process.json", "stop.json"):
        entries[name] = ARTIFACT / name
    return dict(sorted(entries.items()))


def main():
    assert not (OUT / "index.json").exists(), "Refuse to replace an existing freeze"
    manifest = json.loads((ARTIFACT / "manifest.json").read_text(encoding="utf-8"))
    process = json.loads((ARTIFACT / "process.json").read_text(encoding="utf-8"))
    stop = json.loads((ARTIFACT / "stop.json").read_text(encoding="utf-8"))
    assert manifest["run_id"] == RUN_ID and Path(manifest["userdir"]) == USERDIR
    assert process["pid"] == stop["pid"] == PID
    assert stop["forced"] is False and stop["running_after"] is False
    assert datetime.fromisoformat(stop["stopped_at_utc"]) < datetime.now(timezone.utc)
    probe_before = pid_probe()
    started = stamp()
    before_paths = sources()
    before = {name: fingerprint(path) for name, path in before_paths.items()}
    for name, path in before_paths.items():
        target = OUT / name
        assert not target.exists(), target
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    after_paths = sources()
    assert before_paths == after_paths, "Source file set changed during copy"
    records = []
    for name, path in after_paths.items():
        after = fingerprint(path)
        copied = fingerprint(OUT / name)
        assert before[name] == after == copied, name
        records.append({"path": name, "source": str(path), **before[name],
                        "source_after_sha256": after["sha256"], "copy_sha256": copied["sha256"]})
    probe_after = pid_probe()
    doc_names = [r["path"] for r in records if r["path"].startswith("logs/script_documentation/")]
    assert len(doc_names) == 5, doc_names
    index = {"schema": "eep.rc3.final-log-freeze.v1", "status": "FROZEN_BYTE_EXACT",
             "run_id": RUN_ID, "source_userdir": str(USERDIR), "source_artifact_dir": str(ARTIFACT),
             "copy_started_at_utc": started, "copy_finished_at_utc": stamp(),
             "stop_proof": stop, "pid_probe_before": probe_before, "pid_probe_after": probe_after,
             "scope": "All files under this run's logs plus manifest/process/stop only; no savegames or other runs",
             "log_file_count": sum(r["path"].startswith("logs/") for r in records),
             "script_documentation_file_count": len(doc_names), "proof_file_count": 3,
             "total_bytes": sum(r["bytes"] for r in records), "files": records}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: index[k] for k in ("status", "log_file_count", "script_documentation_file_count",
                                           "proof_file_count", "total_bytes")}, indent=2))


if __name__ == "__main__":
    main()
