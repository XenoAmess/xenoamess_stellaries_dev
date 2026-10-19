"""Independent second-process byte and closure verification of this archive."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    output = HERE / "verification.json"
    if output.exists():
        raise FileExistsError(output)
    index_path = HERE / "archive-index.json"
    index = load(index_path)
    assert sha(index_path.read_bytes()) == "2b984e60d900b13127628ec438885a4d0ee8cbb7b2ad01f9d195db2a4d396438"
    checks = {}
    checks["payloads_unique"] = len({f["path"] for f in index["files"]}) == len(index["files"]) == index["file_count"]
    checks["payload_sources_and_archives_byte_identical"] = all(
        len((HERE / f["path"]).read_bytes()) == f["bytes"] and
        sha((HERE / f["path"]).read_bytes()) == f["sha256"] == sha(Path(f["source"]).read_bytes())
        for f in index["files"])
    metadata = {"archive.py", "verify.py", "archive-index.json", "README.md", ".gitattributes"}
    expected = {f["path"] for f in index["files"]} | metadata
    actual = {p.relative_to(HERE).as_posix() for p in HERE.rglob("*") if p.is_file()}
    checks["exact_archive_file_set_before_verification_output"] = actual == expected
    run = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
    checks["exact_requested_prefix_set"] = {p.name for p in run.iterdir() if p.is_file() and p.name.startswith(tuple(index["prefixes"]))} == {
        Path(f["path"]).name for f in index["files"] if f["kind"] == "completed_phase_a_named_prefix"}
    canonical_path = Path(index["canonical_index"]["path"])
    canonical = load(canonical_path)
    checks["original_v3_index_unchanged"] = sha(canonical_path.read_bytes()) == index["canonical_index"]["sha256"]
    checks["all_v3_canonical_payloads_unchanged"] = all(
        len((canonical_path.parent / f["path"]).read_bytes()) == f["bytes"] and
        sha((canonical_path.parent / f["path"]).read_bytes()) == f["sha256"] for f in canonical["files"])
    checks["reused_source_bindings_exact"] = all(
        sha(Path(f["requested_source"]).read_bytes()) == f["sha256"] == sha(Path(f["canonical_path"]).read_bytes())
        for f in index["canonical_exact_byte_source_bindings"])
    manifest_path = Path(index["canonical_manifest"]["path"])
    manifest = load(manifest_path)
    checks["same_canonical_manifest_and_run_language"] = sha(manifest_path.read_bytes()) == index["canonical_manifest"]["sha256"] and (
        manifest["run_id"], manifest["language"], manifest["game_exe_sha256"]) == (
        index["run_id"], "l_simp_chinese", "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83")
    copied = Path(manifest["copied_mod"])
    checks["exact_59_copied_mod_files_unchanged_not_copied"] = len(manifest["repository_mod_files"]) == 59 and all(
        sha((copied / f["path"]).read_bytes()) == f["sha256"] for f in manifest["repository_mod_files"])
    log_path = Path(index["phase_a_final_logs"]["path"])
    logs = load(log_path)
    checks["independent_phase_a_log_archive_unchanged"] = sha(log_path.read_bytes()) == index["phase_a_final_logs"]["sha256"] and all(
        sha((log_path.parent / f["path"]).read_bytes()) == f["sha256"] for f in logs["files"])
    stop = load(log_path.parent / "stop.json")
    checks["normal_exit_proven"] = stop["forced"] is False and stop["running_after"] is False
    save_rows, ocr_rows = [], []
    for f in index["files"]:
        path = HERE / f["path"]
        if path.suffix == ".sav":
            audit, receipt = load(path.with_suffix(".audit.json")), load(path.with_suffix(".native-save.json"))
            with zipfile.ZipFile(path) as archive:
                crc_ok = archive.testzip() is None
                data = archive.read("gamestate")
            save_rows.append({"path": f["path"], "crc_ok": crc_ok,
                              "bound": sha(path.read_bytes()) == audit["save_sha256"] == receipt["sha256"] and
                              sha(data) == audit["gamestate_sha256"] and audit["date"] == receipt["date"]})
        elif path.name.endswith(".ocr.json"):
            ocr = load(path)
            image = path.with_name(path.name.replace(".ocr.json", ".jpg"))
            ocr_rows.append({"path": f["path"], "bound": sha(image.read_bytes()) == ocr["image_sha256"]})
    checks["five_complete_native_save_sets"] = len(save_rows) == 5 and all(r["bound"] and r["crc_ok"] for r in save_rows)
    checks["all89_original_ocr_gpu_pairs"] = len(ocr_rows) == 89 and all(r["bound"] for r in ocr_rows)
    checks["failed_probes_and_raw_delta_retained"] = all((HERE / p).exists() for p in [
        "raw/r4mother13-details.jpg", "raw/r4jump-vapob-search-result.jpg", "raw/r4jump-vapob-pasted-result.jpg",
        "analysis/rc4-relic-reference-raw-delta-v1.json"])
    checks["19_scoped_jump_assertions_all_true"] = all(load(HERE / "analysis/rc4-relic-ui-jump-v1.json")["checks"].values())
    checks["raw_delta_strict_failure_not_rewritten"] = load(HERE / "analysis/rc4-relic-reference-raw-delta-v1.json")["strict_existing_ship_raw_equal"] is False
    paths = sorted(p for p in HERE.rglob("*") if p.is_file())
    relative = [p.relative_to(REPO).as_posix() for p in paths]
    attrs = subprocess.run(["git", "check-attr", "text", "--stdin"], input="\n".join(relative) + "\n",
                           cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    checks["all_git_text_attributes_unset"] = len(attrs) == len(paths) and all(line.endswith(": text: unset") for line in attrs)
    blob_ids = subprocess.run(["git", "hash-object", "--stdin-paths"], input="\n".join(relative) + "\n",
                              cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    expected_blobs = [hashlib.sha1(b"blob " + str(p.stat().st_size).encode() + b"\0" + p.read_bytes()).hexdigest() for p in paths]
    checks["all_git_filtered_blobs_equal_raw_bytes"] = blob_ids == expected_blobs
    result = {"schema": "eep.rc4_relic_jump_native_control_archive_verify.v1", "status": "PASS_BYTES_AND_SCOPED_BINDINGS" if all(checks.values()) else "FAIL",
              "created_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": sha(index_path.read_bytes()),
              "checks": checks, "save_sets": save_rows, "ocr_pairs": ocr_rows,
              "files_checked_before_output": len(paths), "payloads": index["file_count"], "payload_bytes": index["total_bytes"],
              "verifier_sha256": sha(Path(__file__).read_bytes()), "release_acceptance": "PENDING_NOT_CLAIMED"}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "checks": len(checks), "failures": [k for k, v in checks.items() if not v], "sha256": sha(output.read_bytes())}))


if __name__ == "__main__":
    main()
