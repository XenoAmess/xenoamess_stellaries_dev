"""Bind existing public/paid load frames; preserve prior audit as history."""
from hashlib import sha256
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import publish_1019 as release
import runtime_index_1019 as helper

OUT = ROOT / "docs/evidence/1019-requirements/rc6-runtime-progress-v1.json"
AUDIT = OUT.with_name("rc6-runtime-progress-v1-byte-audit.json")
PRIOR = OUT.with_name("rc6-runtime-progress-v1-machine-stage-audit.json")


def main():
    assert not PRIOR.exists()
    shutil.copyfile(AUDIT, PRIOR)
    audit = release.read_json(AUDIT)
    previous_sha = sha256(OUT.read_bytes()).hexdigest()
    paths = []
    for prefix in ("r6pautoload-native-load2-loaded", "r6paidauto-native-load2-loaded"):
        for suffix, kind in ((".jpg", "screenshot"), (".ocr.json", "analysis"), ("-f12.action.json", "actions")):
            paths.append(("docs/evidence/1019-rc6-migration-checkpoint-v1/run/" + prefix + suffix, kind))
    def mutate(data):
        for path, kind in paths:
            helper.attach(data, "old_save_migration", "20261019T150008Z", kind, path, ROOT)
    result = helper.update_progress(OUT, ROOT, {"command": "attach_existing_public_and_paid_native_load_frames", "scope": "References only; no new UI or case/check promotion"}, mutate)
    _, data = helper.load_progress(OUT, ROOT)
    refs = {row["path"]: row for row in audit["references"]}
    for path, kind in paths:
        row = release.collect_reference({"path": path, "kind": kind}, ROOT)
        refs[path] = {"path": path, "sha256": row["sha256"], "bytes": (ROOT / path).stat().st_size}
    missing = helper.missing(data)
    OUT.with_name("rc6-runtime-progress-v1-missing.json").write_text(json.dumps(missing, indent=2) + "\n", encoding="utf-8")
    audit["machine_append_stage_index_sha256"] = previous_sha
    audit["prior_machine_stage_audit"] = {"path": PRIOR.relative_to(ROOT).as_posix(), "sha256": sha256(PRIOR.read_bytes()).hexdigest()}
    audit["index_sha256"] = sha256(OUT.read_bytes()).hexdigest()
    audit["additional_existing_UI_refs_verified"] = len(paths)
    audit["reference_objects_verified"] += len(paths)
    audit["unique_references_verified"] = len(refs)
    audit["references"] = sorted(refs.values(), key=lambda row: row["path"])
    audit["final_reference_attach_helper_result"] = result
    AUDIT.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    md = OUT.with_name("rc6-runtime-progress-v1-missing.md")
    body = md.read_text(encoding="utf-8")
    body = body.replace("| old_save_migration | 1 | 1 | 11 | log, screenshot |", "| old_save_migration | 1 | 1 | 11 | log |")
    md.write_text(body + "\n公开／paid原生loaded代表图、原OCR与F12动作已从既有migration checkpoint绑定，无重新操作UI；完整失败／重试链仍由原checkpoint index引用。\n", encoding="utf-8")
    print(json.dumps({"status": "PENDING", "index_sha256": audit["index_sha256"], "unique_references_verified": len(refs), "attached_existing_UI_refs": len(paths)}))


if __name__ == "__main__": main()
