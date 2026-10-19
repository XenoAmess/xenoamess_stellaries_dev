"""Independent read pass: verify the frozen payload against its index and source."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess

OUT = Path(__file__).resolve().parent


def check_file(path, record):
    data = path.read_bytes()
    return len(data) == record["bytes"] and sha256(data).hexdigest() == record["sha256"]


def main():
    index_bytes = (OUT / "index.json").read_bytes()
    index = json.loads(index_bytes)
    errors = []
    expected_logs = {x["path"] for x in index["files"] if x["path"].startswith("logs/")}
    copied_logs = {"logs/" + p.relative_to(OUT / "logs").as_posix()
                   for p in (OUT / "logs").rglob("*") if p.is_file()}
    source_logs_root = Path(index["source_userdir"]) / "logs"
    source_logs = {"logs/" + p.relative_to(source_logs_root).as_posix()
                   for p in source_logs_root.rglob("*") if p.is_file()}
    if expected_logs != copied_logs or expected_logs != source_logs:
        errors.append("Log file sets differ")
    for record in index["files"]:
        if not check_file(OUT / record["path"], record):
            errors.append("Frozen bytes differ: " + record["path"])
        if not check_file(Path(record["source"]), record):
            errors.append("Source bytes differ: " + record["path"])
    for name in ("manifest.json", "process.json", "stop.json"):
        if sum(x["path"] == name for x in index["files"]) != 1:
            errors.append("Missing/duplicate proof: " + name)
    stop = json.loads((OUT / "stop.json").read_text(encoding="utf-8"))
    process = json.loads((OUT / "process.json").read_text(encoding="utf-8"))
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    if (stop["pid"] != 34832 or process["pid"] != 34832 or stop["forced"] is not False
            or stop["running_after"] is not False or manifest["run_id"] != "20261019T092935Z"):
        errors.append("Run identity/stop proof mismatch")
    command = ("$taskProcess = Get-Process -Id 34832 -ErrorAction SilentlyContinue; "
               "if ($null -ne $taskProcess) { exit 1 }; Write-Output 'ABSENT'; exit 0")
    probe = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                           capture_output=True, text=True, check=False)
    if probe.returncode != 0 or probe.stdout.strip() != "ABSENT" or probe.stderr.strip():
        errors.append("PID no longer independently confirmed absent")
    if any(p.suffix.lower() == ".sav" for p in OUT.rglob("*")):
        errors.append("Unexpected savegame in archive")
    report = {"schema": "eep.rc3.final-log-verify.v1", "status": "PASS" if not errors else "FAIL",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(),
              "index_sha256": sha256(index_bytes).hexdigest(), "run_id": manifest["run_id"],
              "payload_files_verified": len(index["files"]), "source_files_verified": len(index["files"]),
              "log_file_count": len(copied_logs), "script_documentation_file_count": sum(
                  x.startswith("logs/script_documentation/") for x in copied_logs),
              "all_source_and_copy_bytes_match": not errors,
              "pid_probe": {"pid": 34832, "returncode": probe.returncode,
                            "stdout": probe.stdout.strip(), "stderr": probe.stderr.strip()},
              "errors": errors}
    (OUT / "verify.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))


if __name__ == "__main__":
    main()
