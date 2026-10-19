"""Freeze only stopped RC6 final logs and three run identity receipts."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
USERDIR = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\runs\20261019T150008Z")
RUN_ID = "20261019T150008Z"
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
STOP_UTC = "2026-10-19T16:38:02.658777+00:00"
RUN_FILES = ("manifest.json", "process.json", "stop.json")
CANONICAL = (
    "1019-rc6-static/source-index.json",
    "1019-rc6-static/candidate-rc6-gate.json",
    "1019-rc6-static/candidate-rc6-open-kaishek.json",
    "1019-rc6-migration-checkpoint-v1/index.json",
    "1019-rc6-migration-checkpoint-v1/verify.json",
    "1019-rc6-migration-checkpoint-v1/run/manifest.json",
    "1019-rc6-migration-checkpoint-v1/run/process.json",
    "1019-rc4-phase-a-final-logs/review.json",
)


def fp(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": sha256(body).hexdigest()}


def write(name, value):
    path = OUT / name
    assert not path.exists(), "Sealed output already exists: " + name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def choose():
    files = {"run/" + name: RUN / name for name in RUN_FILES}
    files.update({"logs/" + p.relative_to(USERDIR / "logs").as_posix(): p
                  for p in (USERDIR / "logs").rglob("*") if p.is_file()})
    return dict(sorted(files.items()))


def main():
    assert not (OUT / "index.json").exists(), "Existing archive is immutable"
    manifest = json.loads((RUN / "manifest.json").read_bytes())
    process = json.loads((RUN / "process.json").read_bytes())
    stop = json.loads((RUN / "stop.json").read_bytes())
    assert process["pid"] == process["launcher_pid"] == stop["pid"] == 30812
    assert process["transport"] == "direct" and process["command"] == manifest["launch_args"]
    assert manifest["run_id"] == RUN_ID and Path(manifest["userdir"]) == USERDIR
    assert Path(manifest["artifact_dir"]) == RUN and manifest["language"] == "l_simp_chinese"
    assert manifest["repository_mod_tree_sha256"] == manifest["copied_mod_tree_sha256"] == TREE
    assert manifest["static_gate"]["version"] == "0.4.0-rc.6"
    assert stop["stopped_at_utc"] == STOP_UTC and stop["forced"] is False and stop["running_after"] is False
    assert datetime.fromisoformat(manifest["prepared_at_utc"]) < datetime.fromisoformat(process["started_at_utc"]) < datetime.fromisoformat(STOP_UTC)
    query = ["powershell", "-NoProfile", "-NonInteractive", "-Command",
             "ConvertTo-Json -InputObject @(Get-CimInstance Win32_Process -Filter 'ProcessId=30812' -ErrorAction Stop | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine,CreationDate) -Depth 4 -Compress"]
    began = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    ended = datetime.now(timezone.utc).isoformat()
    found = json.loads(result.stdout.decode("utf-8-sig"))
    assert found == [] and not result.stderr
    assert datetime.fromisoformat(ended) > datetime.fromisoformat(STOP_UTC)
    proof = {"schema": "eep.rc6.final-logs-independent-process-proof.v1", "status": "ABSENT",
             "run_id": RUN_ID, "expected_pid": 30812, "query_started_at_utc": began, "checked_at_utc": ended,
             "query": query, "query_exit_code": result.returncode, "query_stdout": result.stdout.decode("utf-8-sig"),
             "query_stdout_sha256": sha256(result.stdout).hexdigest(), "query_stderr": "", "matched_processes": found,
             "process_receipt": fp(RUN / "process.json"), "stop_receipt": fp(RUN / "stop.json"),
             "process_command_matches_manifest": True, "stop_was_normal": True,
             "limit": "Post-stop PID absence and existing identity receipts, not a new historical OS launch capture."}
    write("process-independent.json", proof)
    files = choose()
    rows = [{"path": name, "source": str(path.resolve()), **fp(path)} for name, path in files.items()]
    logs = [row for row in rows if row["path"].startswith("logs/")]
    assert len(rows) == 22 and len(logs) == 19
    assert len([row for row in logs if row["path"].startswith("logs/script_documentation/")]) == 5
    selection = {"schema": "eep.rc6.final-logs-selection.v1", "run_id": RUN_ID,
                 "created_at_utc": datetime.now(timezone.utc).isoformat(), "fixed_artifact_path": str(RUN),
                 "fixed_userdir": str(USERDIR), "all_stopped_log_files_recursive": True,
                 "run_metadata_whitelist": list(RUN_FILES), "files": rows,
                 "exclusions": ["SAV", "Mod payload", "growth actions and receipts", "current-run pointer", "RC7 and other runs", "UI and Steam", "production and tools code mutations"]}
    write("selection.json", selection)
    for row in rows:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert choose() == files
    refs = []
    for name in CANONICAL:
        source = OUT.parent / name
        refs.append({"path": str(source.resolve()), **fp(source)})
    checkpoint = OUT.parent / "1019-rc6-migration-checkpoint-v1/run"
    for name in ("manifest.json", "process.json"):
        assert fp(OUT / "run" / name) == fp(checkpoint / name)
    static = OUT.parent / "1019-rc6-static"
    gate = json.loads((static / "candidate-rc6-gate.json").read_bytes())
    inventory = json.loads((static / "source-index.json").read_bytes())
    assert inventory["tree"] == gate["source_tree_sha256"] == TREE and gate == manifest["static_gate"]
    assert gate["files"] == manifest["repository_mod_files"] and len(gate["files"]) == 59
    static_files = [{**row, "path": row["path"].removeprefix("candidate-rc6/mod/")}
                    for row in inventory["files"] if row["path"].startswith("candidate-rc6/mod/")]
    assert static_files == gate["files"]
    assert fp(static / "candidate-rc6-open-kaishek.json")["sha256"] == gate["report_sha256"]
    index = {"schema": "eep.rc6.final-logs-index.v1", "status": "BYTE_IDENTICAL_STOPPED_RC6_FINAL_LOGS",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": RUN_ID, "pid": 30812,
             "stop": stop, "source_tree_sha256": TREE, "version": "0.4.0-rc.6", "language": "l_simp_chinese",
             "payload_file_count": len(rows), "payload_bytes": sum(row["bytes"] for row in rows),
             "log_file_count": len(logs), "log_bytes": sum(row["bytes"] for row in logs),
             "script_documentation_file_count": 5, "run_metadata_file_count": 3,
             "selection_sha256": fp(OUT / "selection.json")["sha256"],
             "process_independent_sha256": fp(OUT / "process-independent.json")["sha256"],
             "archive_script_sha256": fp(Path(__file__))["sha256"],
             "canonical_references_not_copied": refs, "files": rows,
             "Mod_payload_copied": False, "SAV_payload_copied": False, "Mod_acceptance_pass": False,
             "limits": ["Complete final logs are retained without filtering or baseline exemptions.",
                        "Raw clock stamps contain no calendar date; stage attribution requires separate evidence.",
                        "Static canonical PASS is not runtime acceptance.",
                        "No prepare-time execution-source snapshot or in-memory source proof is created.",
                        "Historical nomads diagnostics remain unexplained even if absent in this run."]}
    write("index.json", index)
    (OUT / ".gitattributes").write_text("* -text\n", encoding="ascii")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "log_file_count", "log_bytes")}))


if __name__ == "__main__":
    main()
