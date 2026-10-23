"""Publish the accepted 0.5.0 habitat regression through the existing updater."""
import hashlib
import json
from pathlib import Path

import publish_update as update

ROOT = update.ROOT
VERSION = "0.5.0"
CANDIDATE_VERSION = "0.5.0-rc.5"
PROOFS = ROOT / "docs/evidence/artificial-worlds-2026-10-23"
EVIDENCE = ROOT / "docs/evidence/publication-0.5.0"
REQUIRED_CASES = {"A01", "H01", "H02", "H03", "H04", "H05", "H06"}


def promoted_manifest(candidate, candidate_descriptor, actual):
    expected = dict(candidate)
    before = f'version="{CANDIDATE_VERSION}"'.encode()
    after = f'version="{VERSION}"'.encode()
    if candidate_descriptor.count(before) != 1:
        raise RuntimeError("accepted candidate descriptor identity differs")
    expected["descriptor.mod"] = hashlib.sha256(candidate_descriptor.replace(before, after)).hexdigest()
    if actual != expected:
        raise RuntimeError("formal package differs from the tested candidate beyond version metadata")
    return expected


def accepted_files():
    index_path = PROOFS / "result.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if (index.get("status") != "PASS_SCOPED" or index.get("candidate_version") != CANDIDATE_VERSION
            or index.get("language") != "l_simp_chinese" or set(index.get("cases", {})) != REQUIRED_CASES
            or not index.get("final_log_reviewed")
            or any(case.get("status") != "PASS_SCOPED" for case in index["cases"].values())):
        raise RuntimeError("habitat runtime acceptance is incomplete")
    for entry in index["references"]:
        path = (ROOT / entry["path"]).resolve()
        path.relative_to(ROOT.resolve())
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise RuntimeError("accepted evidence changed: " + entry["path"])
    descriptor_path = PROOFS / "candidate-descriptor.mod"
    candidate_descriptor = descriptor_path.read_bytes()
    if hashlib.sha256(candidate_descriptor).hexdigest() != index["production_files"]["descriptor.mod"]:
        raise RuntimeError("candidate descriptor certificate changed")
    files = promoted_manifest(index["production_files"], candidate_descriptor, update.base.manifest(update.MOD))
    report = json.loads(update.STATIC.read_text(encoding="utf-8"))
    if (report.get("status") != "PASS" or report.get("game_exe_sha256") != update.EXE_SHA
            or report.get("p_scripts") != report.get("p_parsed") or report.get("errors")):
        raise RuntimeError("formal open_kaishek gate missing")
    prior_path = ROOT / "docs/evidence/publication-0.4.0/workshop-verification.json"
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    if prior.get("status") != "PASS" or prior.get("item_id") != update.ITEM or prior.get("version") != "0.4.0":
        raise RuntimeError("previous verified release differs")
    return {"status": "PASS_SCOPED", "version": VERSION, "candidate_version": CANDIDATE_VERSION,
            "previous_public_version": "0.4.0", "item_id": update.ITEM,
            "production_files": files, "runtime_index_sha256": hashlib.sha256(index_path.read_bytes()).hexdigest(),
            "static_report_sha256": hashlib.sha256(update.STATIC.read_bytes()).hexdigest(),
            "runtime_scope": "Chinese habitat regression only; other artificial types static only",
            "previous_verification_sha256": hashlib.sha256(prior_path.read_bytes()).hexdigest()}


def configure():
    update.VERSION = VERSION
    update.EVIDENCE = EVIDENCE
    update.STATE = EVIDENCE / "publish-state.json"
    update.ACCEPTANCE = EVIDENCE / "acceptance.json"
    update.STATIC = EVIDENCE / "open-kaishek.json"
    update.DOWNLOAD = EVIDENCE / "workshop-download.json"
    update.VERIFIED = EVIDENCE / "workshop-verification.json"
    update.INLINE = EVIDENCE / "inline-images.json"
    update.accepted_files = accepted_files


if __name__ == "__main__":
    configure()
    update.main()
