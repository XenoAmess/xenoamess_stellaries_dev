"""Exclusive byte archive of the completed RC4 PK2 shot, excluding later work."""
import datetime
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT / "tools"))
import check_1019 as c

RUN_ID = "20261019T112808Z"
TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs") / RUN_ID
ANALYSIS = PROJECT / "docs/evidence/1019-analysis"
DEST = PROJECT / "docs/evidence/1019-rc4-pk2-duration"
NATIVE_DOCS = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs") / RUN_ID / "logs/script_documentation"
STAGES = ("pk2base", "pk2queued", "pk2day1", "pk2charge1", "pk2cancel", "pk2requeued",
          "pk2windapr", "pk2windmay", "pk2windjun", "pk2fire0", "pk2prefire", "pk2fired",
          "pk2dupe", "pk2dupevalid", "pk2dupereload")
MANUAL_NEW = ("pk2requeued", "pk2fire0", "pk2prefire", "pk2fired", "pk2dupe", "pk2dupevalid", "pk2dupereload")


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, value):
    with Path(path).open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    index_path = DEST / "archive-index-v3.json"
    verify_path = DEST / "archive-verification-v3.json"
    if index_path.exists() or verify_path.exists():
        raise FileExistsError("v3 already exists; no archive bytes may be overwritten")
    parent = DEST / "archive-index-v2.json"
    assert digest(parent) == "3c60b1cc7f85131071a110a87dcfb2f96dbe3f6dfca89f15c234b26621104d13"
    previous = read(parent)
    old_files = previous["files"]
    assert len(old_files) == 348
    assert all(digest(DEST / f["path"]) == f["sha256"] for f in old_files)
    preserved = {str(p.relative_to(DEST)).replace("\\", "/"): digest(p)
                 for p in DEST.rglob("*") if p.is_file()}
    old_sources = {str(Path(f["source"]).resolve()).casefold() for f in old_files}
    final_files = sorted(RUN.glob("pk2-complete-final-state*"))
    assert {p.suffix for p in final_files} >= {".jpg", ".json"}
    assert (RUN / "pk2-complete-final-state.ocr.json").exists()
    cutoff = max(p.stat().st_mtime_ns for p in final_files)
    additions = {}

    def add(source, relative, kind):
        source = Path(source).resolve()
        if str(source).casefold() in old_sources:
            return
        key = str(source).casefold()
        entry = (source, relative, kind)
        if key in additions:
            assert additions[key] == entry
        additions[key] = entry

    for source in sorted(RUN.iterdir()):
        if (source.is_file() and source.name.startswith("pk2")
                and not source.name.startswith("pk2nativecontrol")
                and source.stat().st_mtime_ns <= cutoff):
            add(source, "phase3/" + source.name, "completed_native_pk2_shot_payload")
    press_bindings = []
    for stage in MANUAL_NEW:
        field = RUN / (stage + "-name-field.action.json")
        name = RUN / (stage + "-name.action.json")
        typed = datetime.datetime.fromisoformat(read(name)["typed_at_utc"]).timestamp()
        low = field.stat().st_mtime_ns / 1e9
        matching = []
        for source in RUN.glob("press-*.json"):
            record = read(source)
            at = datetime.datetime.fromisoformat(record["at_utc"]).timestamp()
            if record.get("keys") == ["ctrl", "a"] and low <= at <= typed:
                matching.append(source)
        assert len(matching) == 1, (stage, matching)
        add(matching[0], "phase3/" + matching[0].name, "native_save_name_edit_ctrl_a")
        press_bindings.append({"stage": stage, "name_field": str(field), "typed_name": str(name),
                               "ctrl_a": str(matching[0]), "sha256": digest(matching[0])})
    for source in sorted(ANALYSIS.iterdir()):
        if (source.is_file() and (source.name.startswith("rc4-pk2") or source.name.startswith("pk2-")
                or source.name in ("rc4-native-owned-colony-scope-source-v1.json", Path(__file__).name))
                and "nativecontrol" not in source.name.lower()):
            add(source, "phase3/analysis/" + source.name, "independent_readonly_analysis_or_recorded_failure")
    for name in ("triggers.log", "scopes.log"):
        add(NATIVE_DOCS / name, "phase3/native-documentation/" + name, "completed_native_generated_documentation")

    planned = list(additions.values())
    assert len({relative for _, relative, _ in planned}) == len(planned)
    assert not any((DEST / relative).exists() for _, relative, _ in planned)
    new_files = []
    for source, relative, kind in planned:
        first = source.stat()
        data = source.read_bytes()
        second = source.stat()
        assert (first.st_size, first.st_mtime_ns) == (second.st_size, second.st_mtime_ns)
        assert data == source.read_bytes()
        target = DEST / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        sha = hashlib.sha256(data).hexdigest()
        assert digest(target) == sha
        new_files.append({"source": str(source), "path": relative, "kind": kind,
                          "bytes": len(data), "sha256": sha, "source_mtime_ns": first.st_mtime_ns,
                          "read_utc": now()})
    files = old_files + new_files
    sources = {str(Path(f["source"]).resolve()).casefold(): f for f in files}
    saves = []
    for stage in STAGES:
        save = RUN / (stage + ".sav")
        _, proof = c.n.provenance(save)
        audit = read(save.with_suffix(".audit.json"))
        with zipfile.ZipFile(save) as archive:
            assert archive.testzip() is None
            game_hash = hashlib.sha256(archive.read("gamestate")).hexdigest()
        assert audit["gamestate_sha256"] == game_hash and audit["date"] == proof["receipts"][0]["entry"]["date"]
        assert str(save.resolve()).casefold() in sources
        assert sources[str(save.resolve()).casefold()]["sha256"] == proof["save_sha256"]
        saves.append({"stage": stage, "date": audit["date"], "sha256": proof["save_sha256"],
                      "gamestate_sha256": game_hash, "receipts": proof["receipts"]})
    ocr_count = 0
    for f in files:
        if f["source"].endswith(".ocr.json"):
            record = read(DEST / f["path"])
            image = record.get("image")
            if image and record.get("image_sha256"):
                match = sources.get(str(Path(image).resolve()).casefold())
                assert match and match["sha256"] == record["image_sha256"]
                ocr_count += 1
    after = {str(p.relative_to(DEST)).replace("\\", "/") for p in DEST.rglob("*") if p.is_file()}
    expected = set(preserved) | {f["path"] for f in new_files}
    checks = {"parent348_payloads_preserved": all(digest(DEST / f["path"]) == f["sha256"] for f in old_files),
              "all_existing_archive_metadata_preserved": all(digest(DEST / rel) == sha for rel, sha in preserved.items()),
              "exact_payload_file_set_before_index": after == expected,
              "all_source_and_archive_payload_bytes_equal": all(digest(f["source"]) == digest(DEST / f["path"]) == f["sha256"] for f in files),
              "fifteen_native_sav_provenance_audit_receipt_verified": len(saves) == 15,
              "seven_new_ctrl_a_inputs_bound": len(press_bindings) == 7,
              "all_archive_payload_paths_unique": len({f["path"] for f in files}) == len(files),
              "all_archive_source_paths_unique": len(sources) == len(files),
              "ocr_gpu_byte_bindings_verified": ocr_count > 0,
              "complete_final_frame_included": all(str(p.resolve()).casefold() in sources for p in final_files),
              "later_nativecontrol_excluded": not any("pk2nativecontrol" in f["path"] for f in files),
              "no_active_logs_directory_copied": not any("/logs/" in f["path"].replace("\\", "/") for f in files),
              "original_immediate_settlement_fail_retained": read(ANALYSIS / "rc4-pk2-prefire-fired-settlement-report-v1.json")["status"] == "FAIL",
              "unchanged_checker_stable_settlement25_pass": read(ANALYSIS / "rc4-pk2-prefire-stable-settlement-report-v2.json")["status"] == "PASS_SCOPED",
              "correct_callback_reload_scoped_pass": read(ANALYSIS / "rc4-pk2-valid-callback-reload-dedup-report-v1.json")["status"] == "PASS_SCOPED",
              "missing_jul1_not_fabricated": read(ANALYSIS / "rc4-pk2-jul1-autosave-missing-v1.json")["created_jul1_save"] is False}
    assert all(checks.values()), checks
    index = {"schema": "eep.1019.rc4-pk2-phase-archive.v3", "status": "BYTE_IDENTICAL_COMPLETED_ENEMY_SHOT_SCOPED",
             "run_id": RUN_ID, "production_tree_sha256": TREE, "parent_index": {"path": parent.name, "sha256": digest(parent)},
             "files": files, "file_count": len(files), "new_file_count": len(new_files),
             "total_bytes": sum(f["bytes"] for f in files), "preserved_archive_files": preserved,
             "cutoff": {"prefix": "pk2-complete-final-state", "maximum_source_mtime_ns": cutoff},
             "canonical_manifest": previous["canonical_manifest"], "native_saves": saves, "new_ctrl_a_bindings": press_bindings,
             "historical_unit_calibration_archive": {"path": "../1019-analysis/pk1-objective-calibration-v1/archive-index-v1.json",
                 "sha256": digest(ANALYSIS / "pk1-objective-calibration-v1/archive-index-v1.json")},
             "active_logs_copied": False, "complete_run_freeze": False, "release_status": "PENDING",
             "scope": "Single enemy shot 90+30 native timing, stable settlement, callback/reload dedup only; known native and operator errors retained",
             "excluded_prefixes": ["pk2nativecontrol", "future_growth", "future_guard_cases"], "checks": checks}
    write(index_path, index)
    verification = {"schema": "eep.1019.rc4-pk2-phase-byte-verification.v3", "status": "PASS_SCOPED",
                    "scope": "Byte preservation and completed-stage provenance only; not a Mod release gate",
                    "index": {"path": index_path.name, "sha256": digest(index_path)}, "checked_at_utc": now(),
                    "file_count": len(files), "new_file_count": len(new_files), "ocr_gpu_bindings": ocr_count,
                    "checks": checks, "all_payload_sha_rechecked": all(digest(DEST / f["path"]) == f["sha256"] for f in files)}
    write(verify_path, verification)
    print(json.dumps({"index_sha256": digest(index_path), "verification_sha256": digest(verify_path),
                      "files": len(files), "new_files": len(new_files), "bytes": index["total_bytes"], "checks": len(checks)}))


if __name__ == "__main__":
    main()
