"""Freeze only the stopped legacy public031 damage run's logs and three run proofs, byte for byte."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess

RUN_ID = "20261019T130448Z"
PID = 5216
BASE = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev")
USERDIR = BASE / "runs" / RUN_ID
ARTIFACT = BASE / "artifacts/1019-legacy-damage/runs" / RUN_ID
OUT = Path(__file__).resolve().parent


def stamp():
    return datetime.now(timezone.utc).isoformat()


def fingerprint(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def pid_probe():
    command = ("$taskProcess = Get-Process -Id 5216 -ErrorAction SilentlyContinue; "
               "if ($null -ne $taskProcess) { $taskProcess | Select-Object Id,ProcessName,StartTime | "
               "ConvertTo-Json -Compress; exit 1 }; Write-Output 'ABSENT'; exit 0")
    result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
                            capture_output=True, text=True, check=False)
    probe = {"checked_at_utc": stamp(), "pid": PID, "returncode": result.returncode,
             "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    assert result.returncode == 0 and probe["stdout"] == "ABSENT" and not probe["stderr"], probe
    return probe


SAVES = ("ld031clean", "ld031hurt", "ldpaidclean", "ldpaidhurt", "ldpaidarmor", "p031before", "ppaidbefore")
ANALYSIS_ROOT = OUT.parent / "1019-analysis"
FIX_ROOT = OUT.parent / "1019-eep05-design"
REPORTS = ("legacy-ld031-clean-hurt-report-v1.json", "legacy-ldpaid-clean-hurt-report-v1.json", "legacy-ldpaid-hurt-armor-report-v1.json", "legacy-p031before-partial-fixture-report-v1.json", "legacy-ppaidbefore-partial-fixture-report-v1.json")
ANALYSIS_NAMES = REPORTS + tuple("legacy-" + name + "-observation-v1.json" for name in SAVES) + ("legacy-public031-fraction-migration-case-template-v2.json", "legacy-paid-fraction-migration-case-template-v2.json")
FIX_NAMES = ("fixture-before-gender-repair.txt", "fixture-after-gender-repair.txt", "fixture-gender-repair-v1.json")


def sources():
    entries = {"logs/" + p.relative_to(USERDIR / "logs").as_posix(): p
               for p in sorted((USERDIR / "logs").rglob("*")) if p.is_file()}
    assert {p.stem for p in ARTIFACT.glob("*.sav")} == set(SAVES), "Unexpected native save set"
    assert not any(p.is_dir() for p in ARTIFACT.iterdir()), "New subdirectory requires explicit inventory review"
    for path in ARTIFACT.iterdir():
        if path.name in ("manifest.json", "process.json", "stop.json"):
            entries[path.name] = path
        else:
            assert path.suffix in (".json", ".jpg", ".png", ".sav"), path
            entries["run/" + path.name] = path
    for name in ANALYSIS_NAMES:
        entries["analysis/" + name] = ANALYSIS_ROOT / name
    for name in FIX_NAMES:
        entries["eep05-fixture/" + name] = FIX_ROOT / name
    entries["runtime-input/user_empire_designs_v3.4.txt"] = USERDIR / "user_empire_designs_v3.4.txt"
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
    assert manifest["copied_mod_tree_sha256"] == manifest["repository_mod_tree_sha256"] == "abca9b4195a991d98ca25336ed7807e0306d30e2c33021e4d307f78e1db864d8"
    assert manifest["language"] == "l_simp_chinese"
    assert process["command"][0] == manifest["game_exe"] and "-userdir=" + str(USERDIR) in process["command"]
    canonical = ANALYSIS_ROOT / "legacy-damage-preparation-v1"
    canonical_refs = [{"source": str((canonical / name).resolve()), **fingerprint(canonical / name)} for name in ("archive-index-v1.json", "archive-verification-v1.json", "public031-profile.json", "public031-gate.json", "public031-open-kaishek.json")]
    assert fingerprint(USERDIR / "user_empire_designs_v3.4.txt")["sha256"] == "b3cee1d3c3475ea6fa9b54cc09eb0f75e848f565a02326bf70c59db0c9ed0e90"
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
    index = {"schema": "eep.legacy-damage.final-run-freeze.v1", "status": "FROZEN_BYTE_EXACT_LEGACY_FIXTURE_RUN",
             "run_id": RUN_ID, "source_userdir": str(USERDIR), "source_artifact_dir": str(ARTIFACT),
             "copy_started_at_utc": started, "copy_finished_at_utc": stamp(),
             "stop_proof": stop, "pid_probe_before": probe_before, "pid_probe_after": probe_after,
             "scope": "Stopped legacy public031 run: all logs, 7 native saves, associated UI/actions/receipts and stable analysis plus EEP05 candidate repair evidence; no duplicate Mod tree or other runs",
             "log_file_count": sum(r["path"].startswith("logs/") for r in records),
             "script_documentation_file_count": len(doc_names), "proof_file_count": 3,
             "total_bytes": sum(r["bytes"] for r in records), "files": records,
             "native_saves": list(SAVES), "analysis_whitelist": list(ANALYSIS_NAMES),
             "canonical_refs_not_copied": canonical_refs,
             "runtime_mod_version": "0.3.1", "original_paid_fixture_version": "0.3.0-rc.1",
             "mod_tree_sha256": manifest["copied_mod_tree_sha256"], "mod_tree_copied": False,
             "scope_limit": "Fixture qualification and old EEP05 tooltip only; RC4 migration and repaired-fixture native validation remain pending"}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: index[k] for k in ("status", "log_file_count", "script_documentation_file_count",
                                           "proof_file_count", "total_bytes")}, indent=2))


if __name__ == "__main__":
    main()
