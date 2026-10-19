"""Exclusive byte archive of five completed phase-A evidence prefixes; no UI."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
DOCS = HERE.parents[1]
PROJECT = DOCS.parent
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T112808Z")
CANON = DOCS / "evidence/1019-rc4-pk2-duration"
PREFIXES = ("pk2nativecontrol", "r4relic", "r4mother13", "r4ref13", "r4jump")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def stable(path):
    first = path.stat()
    data, again = path.read_bytes(), path.read_bytes()
    last = path.stat()
    assert (first.st_size, first.st_mtime_ns) == (last.st_size, last.st_mtime_ns)
    assert data == again
    return data, first


def main():
    assert not (HERE / "archive-index.json").exists()
    assert {p.name for p in HERE.iterdir()} == {"archive.py", ".gitattributes"}
    canonical_path = CANON / "archive-index-v3.json"
    canonical_data = canonical_path.read_bytes()
    assert sha(canonical_data) == "1b371ae6e6c33bc1841af895bb94bb7e037d0a7b7da20bd689045d70e7afaf64"
    canonical = json.loads(canonical_data)
    for item in canonical["files"]:
        data = (CANON / item["path"]).read_bytes()
        assert len(data) == item["bytes"] and sha(data) == item["sha256"]
    files, reused, source_to_dest = [], [], {}
    canonical_by_sha = {}
    for item in canonical["files"]:
        canonical_by_sha.setdefault(item["sha256"], item)

    def copy(path, relative, kind):
        path = path.resolve()
        data, stat = stable(path)
        if str(path) in source_to_dest:
            assert source_to_dest[str(path)]["sha256"] == sha(data)
            return
        dest = HERE / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("xb") as stream:
            stream.write(data)
        assert dest.read_bytes() == path.read_bytes() == data
        record = {"source": str(path), "path": relative, "kind": kind, "bytes": len(data),
                  "sha256": sha(data), "source_mtime_ns": stat.st_mtime_ns}
        files.append(record)
        source_to_dest[str(path)] = record

    def bind_existing(path, expected=None):
        path = path.resolve()
        data, _ = stable(path)
        digest = sha(data)
        if expected:
            assert digest == expected
        if str(path) in source_to_dest:
            return
        if digest in canonical_by_sha:
            item = canonical_by_sha[digest]
            reused.append({"requested_source": str(path), "canonical_path": str(CANON / item["path"]),
                           "bytes": len(data), "sha256": digest, "binding": "exact_bytes"})
        else:
            game = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")
            if path.is_relative_to(game):
                relative = "primary/" + path.relative_to(game).as_posix()
            elif path.is_relative_to(PROJECT):
                relative = "sources/" + path.relative_to(PROJECT).as_posix()
            else:
                raise ValueError("unplanned source outside canonical or named prefixes: " + str(path))
            copy(path, relative, "explicit_report_source")

    selected = sorted(p for p in RUN.iterdir() if p.is_file() and p.name.startswith(PREFIXES))
    for path in selected:
        copy(path, "raw/" + path.name, "completed_phase_a_named_prefix")
    analysis = DOCS / "evidence/1019-analysis"
    for name in ["rc4-relic-reference-v1.py", "rc4-relic-reference-v1.json", "rc4-relic-reference-raw-delta-v1.json",
                 "rc4-relic-six-day-refresh-v1.json", "rc4-relic-ui-jump-v1.py", "rc4-relic-ui-jump-v1.json"]:
        copy(analysis / name, "analysis/" + name, "readonly_observation_snapshot")
    control = DOCS / "evidence/1019-native-cracker-control"
    for path in sorted(control.iterdir()):
        if path.is_file():
            copy(path, "native-control-analysis/" + path.name, "original_native_callback_analysis")
    for name in ["juggernaut-native-jump-probe-1019.md", "rc4-native-cracker-control-analysis-2026-10-19.md"]:
        copy(DOCS / name, "notes/" + name, "scope_and_findings_snapshot")
    for record in load(control / "analysis.json")["sources"]:
        bind_existing(Path(record["source"]), record["sha256"])
    for record in load(analysis / "rc4-relic-reference-v1.json")["sources"].values():
        bind_existing(Path(record["path"]), record["sha256"])
    for tool in [PROJECT / "tools/audit_save.py", PROJECT / "testing/inspect_1015.py", PROJECT / "testing/inspect_1019.py"]:
        bind_existing(tool)
    game = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")
    note = (DOCS / "juggernaut-native-jump-probe-1019.md").read_text(encoding="utf-8")
    for path, digest in re.findall(r"^\| ([^|]+?) \| ([0-9a-f]{64}) \|$", note, re.MULTILINE):
        bind_existing(game / path, digest)
    manifest = load(CANON / "manifest.json")
    copied = Path(manifest["copied_mod"])
    assert len(manifest["repository_mod_files"]) == 59
    for item in manifest["repository_mod_files"]:
        data = (copied / item["path"]).read_bytes()
        assert len(data) == item["bytes"] and sha(data) == item["sha256"]
    final_logs = DOCS / "evidence/1019-rc4-phase-a-final-logs"
    log_index = load(final_logs / "index.json")
    for item in log_index["files"]:
        data = (final_logs / item["path"]).read_bytes()
        assert len(data) == item["bytes"] and sha(data) == item["sha256"]
    stop = load(final_logs / "stop.json")
    assert stop["forced"] is False and stop["running_after"] is False
    assert {p.name for p in selected} == {p.name for p in RUN.iterdir() if p.is_file() and p.name.startswith(PREFIXES)}
    saves, ocr_count = [], 0
    for item in files:
        path = HERE / item["path"]
        if path.suffix == ".sav":
            audit, receipt = load(path.with_suffix(".audit.json")), load(path.with_suffix(".native-save.json"))
            with zipfile.ZipFile(path) as archive:
                assert archive.testzip() is None
                gamestate = archive.read("gamestate")
            assert sha(gamestate) == audit["gamestate_sha256"]
            assert item["sha256"] == audit["save_sha256"] == receipt["sha256"]
            assert audit["date"] == receipt["date"]
            saves.append({"path": item["path"], "sha256": item["sha256"], "date": audit["date"], "gamestate_sha256": sha(gamestate)})
        elif path.name.endswith(".ocr.json"):
            ocr = load(path)
            image = path.with_name(path.name.replace(".ocr.json", ".jpg"))
            assert sha(image.read_bytes()) == ocr["image_sha256"]
            ocr_count += 1
    for item in files:
        data, _ = stable(Path(item["source"]))
        assert len(data) == item["bytes"] and sha(data) == item["sha256"] == sha((HERE / item["path"]).read_bytes())
    index = {"schema": "eep.rc4_relic_jump_native_control_archive.v1", "status": "BYTE_IDENTICAL_SCOPED_OBSERVATIONS",
             "run_id": "20261019T112808Z", "created_at_utc": datetime.now(timezone.utc).isoformat(),
             "prefixes": PREFIXES, "file_count": len(files), "total_bytes": sum(x["bytes"] for x in files),
             "raw_prefix_file_count": len(selected), "files": files, "native_saves": saves, "ocr_gpu_pairs": ocr_count,
             "canonical_index": {"path": str(canonical_path), "sha256": sha(canonical_data), "verified_payloads": len(canonical["files"])},
             "canonical_manifest": {"path": str(CANON / "manifest.json"), "sha256": sha((CANON / "manifest.json").read_bytes())},
             "canonical_exact_byte_source_bindings": reused,
             "phase_a_final_logs": {"path": str(final_logs / "index.json"), "sha256": sha((final_logs / "index.json").read_bytes()), "verified_payloads": len(log_index["files"])},
             "copied_mod_files_reverified_not_copied": 59, "mod_tree_sha256": manifest["copied_mod_tree_sha256"],
             "builder": {"path": "archive.py", "sha256": sha(Path(__file__).read_bytes())},
             "limitations": ["Only scoped reference configuration and one actual jump are verified; maintenance and power remain absent.",
                 "Native CRACKER is a manually dispatched completion callback control, not an actual weapon shot or90-day test.",
                 "Preserves failed Unicode search, unopened Mother detail and rawdelta; no whole-Mod or release PASS.",
                 "No native in_ftl transient or200-day cooldown expiry sample. Relic fixture is not new-game economy."]}
    write_json(HERE / "archive-index.json", index)
    summary = "# RC4 phase-A Relic、跃迁与原版回调对照原字节归档\n\n"
    summary += f"已排他复制{len(files)}份载荷／{index['total_bytes']:,}字节，含{len(saves)}套真实SAV与{ocr_count}对GPU／OCR。\n\n"
    summary += "范围、逐源路径及SHA见archive-index.json；复用并复核v3 canonical798份载荷和59份copied Mod，未复制Mod树。最终日志单独引用原冻结归档。\n\n"
    summary += "Relic／UI／jump报告19项限定存档断言通过；真实Mar13→Mar27 Mother8→196及200天原生冷却成立。维护、供电、独立in_ftl瞬态和冷却到期未验。原版CRACKER仅手动完成回调对照，保留原生nomads错误与worlds750／empires0；不声称实际武器发射。\n\n"
    summary += "失败Unicode空框、未打开Mother详情和rawdelta原文全部保留。此归档字节核验与限定观察不能扩大为整个Mod、经济、迁移或发布PASS。由主线程统一提交，本任务未操作UI或生产代码。\n"
    with (HERE / "README.md").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(summary)
    print(json.dumps({"status": index["status"], "files": len(files), "bytes": index["total_bytes"], "saves": len(saves), "ocr": ocr_count,
                      "index_sha256": sha((HERE / "archive-index.json").read_bytes())}))


if __name__ == "__main__":
    main()
