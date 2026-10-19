"""Exact RC7 mechanics plus the pinned, separately tested RC8 notification repair."""
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import re
import zipfile

import publish_1019 as original
import check_1019 as native_checker

CERTIFICATE_SHA = "7a3c237354fef7b65ab7c9f8e8d93219c2b4a40a5632d65bb66e6587d2e4ad40"
PARENT_TREE = "61b34f6dbdc277c44364889d5f1e1cd2773a4624786bbf0d538079fc6ba4feb0"
CHILD_TREE = "537f1f95ce33ac44e7825c7374e15c3a8b62092a2df25d152570bd685fe86390"
KEY = "MESSAGE_DESC_FOR_EEP_PLANET_KILLER_DEVOURER"
TOOL_SHA = "149bb31c7c566319c313114c9796fa697453c7df804ec6f29572a8fb5e945335"
PARENT_STATIC_SHA = "b48b6160c234ba77f6b18a5ce7b6b7987b0cfc47fd98ebe5675455f917f61fb9"
PATCH_CHECKS = {"actual_rc8_run_and_source", "native_prefire_loaded", "native_last_day_completed",
                "original_settlement_math", "source_global_liveness", "actual_chinese_destroyed_message",
                "no_raw_description_key", "native_reward_message_separate", "duplicate_and_reload_no_rewards",
                "all_other_languages_static_only", "stopped_complete_logs_reviewed"}
digest = original.update.digest


def require(value, reason):
    if not value:
        raise RuntimeError("notification localization patch: " + reason)


def source_contract(runtime, root):
    """Verify original byte prefixes and every non-localization byte, not just keys."""
    scope = runtime.get("notification_localization_patch", {})
    entry = scope.get("source_certificate", {})
    require(entry.get("sha256") == CERTIFICATE_SHA, "unknown source certificate")
    certificate = original.read_json(original.reference_path(entry, root))
    require(certificate.get("schema") == "eep.1020.notification-localization-source-patch.v1"
            and certificate.get("key") == KEY
            and certificate.get("parent_tree_sha256") == PARENT_TREE
            and certificate.get("child_tree_sha256") == CHILD_TREE
            and certificate.get("parent_version") == "0.4.0-rc.7"
            and certificate.get("child_version") == "0.4.0-rc.8", "exact reviewed revision pair")
    parent = original.candidate_files(runtime)
    require(runtime["production_tree_sha256"] == PARENT_TREE and runtime["version"] == "0.4.0-rc.7",
            "original mechanics identity retained")
    rows = certificate["parent_files"]
    require(len(rows) == len(parent) == 59 and {r["path"]: r["sha256"] for r in rows} == parent,
            "all 59 original source identities")
    child_rows = certificate["child_files"]
    child = {r["path"]: r["sha256"] for r in child_rows}
    require(len(child_rows) == len(child) == 59 and set(child) == set(parent), "unchanged file set")
    changes = certificate["changes"]
    require(len(changes) == 10 and {r["language"] for r in changes} == original.LANGUAGES,
            "all ten distinct languages")
    originals = {"descriptor.mod": original.candidate_descriptor(runtime)}
    for row in changes:
        name = f"localisation/{row['language']}/eep_l_{row['language']}.yml"
        require(row["path"] == name, "only the existing localization files")
        before = original.reference_path(row["before"], root).read_bytes()
        after = original.reference_path(row["after"], root).read_bytes()
        require(digest(before) == parent[name] and digest(after) == child[name]
                and after.startswith(before) and before.startswith(b"\xef\xbb\xbf"), "unchanged original byte prefix")
        newline = b"\r\n" if b"\r\n" in before else b"\n"
        addition = (b"" if before.endswith(b"\n") else newline) + (
            f' {KEY}:0 "{row["value"]}"'.encode("utf-8")) + newline
        require(after == before + addition and KEY.encode() not in before
                and row["value"].strip() and row["value"] != KEY, "exact one appended description key")
        originals[name] = before
    old_descriptor = original.reference_path(certificate["before_descriptor"], root).read_bytes()
    descriptor = original.reference_path(certificate["after_descriptor"], root).read_bytes()
    require(old_descriptor == originals["descriptor.mod"]
            and descriptor == old_descriptor.replace(b'0.4.0-rc.7', b'0.4.0-rc.8')
            and digest(descriptor) == child["descriptor.mod"], "descriptor version only")
    allowed = {"descriptor.mod", *(r["path"] for r in changes)}
    require({n for n in parent if parent[n] != child[n]} == allowed, "no script, component, asset or other change")
    current = original.update.base.manifest(root / "mod")
    formal = {**child, "descriptor.mod": digest(descriptor.replace(b'0.4.0-rc.8', b'0.4.0'))}
    require(current in (child, formal), "current package equals exact RC8 or its formal version")
    reconstructed = hashlib.sha256()
    for path in sorted(root / "mod" / n for n in parent):
        name = path.relative_to(root / "mod").as_posix()
        raw = originals.get(name, path.read_bytes())
        require(digest(raw) == parent[name], "original mechanics bytes: " + name)
        reconstructed.update(name.encode()); reconstructed.update(b"\0"); reconstructed.update(raw)
    require(reconstructed.hexdigest() == PARENT_TREE, "reconstructed original tree")
    return certificate, child, formal


def runtime_contract(runtime, root, certificate, child):
    scope = runtime["notification_localization_patch"]
    proof = original.read_json(original.reference_path(scope.get("runtime_report"), root))
    require(proof.get("schema") == "eep.1020.notification-localization-runtime.v1"
            and proof.get("status") == "PASS_SCOPED"
            and proof.get("source_certificate_sha256") == CERTIFICATE_SHA
            and isinstance(proof.get("checks"), dict) and PATCH_CHECKS.issubset(proof["checks"])
            and all(v is True for v in proof["checks"].values()), "completed native patch review")
    static = original.read_json(original.reference_path(proof["static_report"], root))
    original.validate_static_report(static, root)
    require(static.get("planet_killer_message_localization_contract") == "native_destroy_description_v1"
            and static.get("planet_killer_message_localization_required") == 10
            and static.get("planet_killer_message_localization_resolved") == 10
            and static.get("localization_keys") == 132
            and {r["language"] for r in static["planet_killer_message_localization_sources"]} == original.LANGUAGES
            and all(r["source"] == "mod" and r["localization_key"] == KEY
                    for r in static["planet_killer_message_localization_sources"]), "new ten-language static contract")
    tool = original.reference_path(proof["static_checker"], root)
    require(digest(tool.read_bytes()) == TOOL_SHA, "reviewed repaired acceptance tool")
    manifest_ref = proof["manifest"]
    manifest = original.read_json(original.reference_path(manifest_ref, root))
    require(manifest["repository_mod_tree_sha256"] == manifest["copied_mod_tree_sha256"] == CHILD_TREE
            and manifest["static_gate"]["version"] == "0.4.0-rc.8"
            and manifest["static_gate"]["report_sha256"] == proof["static_report"]["sha256"]
            and manifest["profile_id"] == original.PROFILE and manifest["enabled_mods"] == original.ENABLED_MODS
            and manifest["language"] == "l_simp_chinese" and manifest["game_exe_sha256"] == original.update.EXE_SHA
            and len(manifest["repository_mod_files"]) == 59
            and {r["path"]:r["sha256"] for r in manifest["repository_mod_files"]} == child,
            "independent full RC8 native source identity")
    process = original.read_json(original.reference_path(proof["process"], root))
    stop = original.read_json(original.reference_path(proof["stop"], root))
    require(process["pid"] == stop["pid"] and stop["forced"] is False and stop["running_after"] is False,
            "actual normally stopped child process")
    observations, saves = {}, {}
    for role in ("before", "after", "duplicate", "reloaded"):
        native = proof["native_" + role]
        save = original.reference_path(native["save"], root)
        observation = original.read_json(original.reference_path(native["observation"], root))
        audit = original.read_json(original.reference_path(native["audit"], root))
        receipt = original.read_json(original.reference_path(native["receipt"], root))
        provenance = observation["provenance_1019"]
        require(native["save"]["sha256"] == observation["save_sha256"] == audit["save_sha256"] == receipt["sha256"]
                and provenance["manifest_sha256"] == manifest_ref["sha256"]
                and provenance["run_id"] == manifest["run_id"] and provenance["version"] == "0.4.0-rc.8"
                and provenance["production_tree_sha256"] == CHILD_TREE, "actual native " + role)
        observations[role] = observation
        saves[role] = save
    settlement = original.read_json(original.reference_path(proof["settlement_report"], root))
    case = settlement["case"]
    require(observations["before"]["date"] == "2200.06.03" and observations["after"]["date"] == "2200.06.04"
            and case["native"] is True and case["expected_q"] == 2 and case["expected_return"] == 302,
            "actual same prefire fixture and one final natural day")
    mothers = native_checker.mother_records(observations["before"])
    require(len(mothers) == 1, "one actual Mother before replay")
    fleet = next(iter(mothers.values()))
    order = native_checker.a.block(native_checker.a.block(fleet["raw"], "current_order"), "destroy_planet_order")
    phase = native_checker.a.scalars(native_checker.a.block(native_checker.a.block(order, "sub_order"),
                                                           "planet_killer_weapon_fire_order"))
    require(native_checker.a.scalars(order).get("planet") == case["source_world"]
            and phase.get("fire") == 29 and phase.get("fire_time") == 30, "actual native fire29 input")
    with zipfile.ZipFile(saves["after"]) as archive:
        text = archive.read("gamestate").decode("utf-8-sig")
    messages = re.findall(r'localization\s*=\s*"(MESSAGE_TERRAVORE_CONSUME_WORLD_(?:POP|MINERALS|ALLOYS)_TEXT)"', text)
    require(len(messages) == 1 and case["expected_other_core_pop_delta"] == (
        100 if messages[0].endswith("_POP_TEXT") else 0), "native saved reward selects predeclared population branch")
    require(settlement["before"]["save_sha256"] == proof["native_before"]["save"]["sha256"]
            and settlement["after"]["save_sha256"] == proof["native_after"]["save"]["sha256"]
            and all(v is True for k,v in settlement["checks"].items() if k != "source_colony_destroyed"),
            "original settlement invariants")
    if settlement["checks"]["source_colony_destroyed"] is not True:
        supplement = original.read_json(original.reference_path(proof["liveness_supplement"], root))
        require(supplement.get("status") == "PASS_SCOPED"
                and supplement["sources"]["before"]["sha256"] == proof["native_before"]["save"]["sha256"]
                and supplement["sources"]["after"]["sha256"] == proof["native_after"]["save"]["sha256"],
                "independent bound global liveness supplement")
    for label, left, right in (("duplicate", "after", "duplicate"), ("reload", "duplicate", "reloaded")):
        report = original.read_json(original.reference_path(proof[label + "_report"], root))
        require(report["status"] == "PASS_SCOPED" and len(report["checks"]) == 9
                and all(v is True for v in report["checks"].values())
                and report["before"]["save_sha256"] == proof["native_" + left]["save"]["sha256"]
                and report["after"]["save_sha256"] == proof["native_" + right]["save"]["sha256"]
                and observations[left]["country"]["stockpile"] == observations[right]["country"]["stockpile"],
                "actual " + label + " preserves all rewards and stockpiles")
    value = next(r["value"] for r in certificate["changes"] if r["language"] == "simp_chinese")
    for name in ("destruction", "reward"):
        picture = proof[name + "_screenshot"]
        original.reference_path(picture, root)
        ocr = original.read_json(original.reference_path(proof[name + "_ocr"], root))
        labels = "".join(r["text"] for r in ocr["rows"])
        require(ocr["image_sha256"] == picture["sha256"] and ocr["pid"] == process["pid"]
                and ocr["resolution"] == [1024,768] and KEY not in labels
                and "2200.06.04" in labels, "actual localized " + name + " GPU/OCR")
        if name == "destruction":
            require(value in re.sub(r"\s+", "", labels), "translated destruction fragment actually displayed")
        else:
            word = "人口" if messages[0].endswith("_POP_TEXT") else "矿物" if messages[0].endswith("_MINERALS_TEXT") else "合金"
            require("吞噬星球" in labels and word in labels, "native reward tooltip matches saved message")
    return proof


@contextmanager
def adapted():
    saved = (original.validate_candidate_files, original.candidate_tree, original.accepted_files,
             original.validate_static_report)
    def static(report, root):
        path = root / "docs/evidence/1019-rc7-static/candidate-rc7-open-kaishek.json"
        if path.is_file() and digest(path.read_bytes()) == PARENT_STATIC_SHA and report == original.read_json(path):
            parent = root / "docs/evidence/1020-notification-localization-patch-v1/mechanics-parent"
            certificate_path = root / "docs/evidence/1020-notification-localization-patch-v1/source-certificate-v1.json"
            require(digest(certificate_path.read_bytes()) == CERTIFICATE_SHA, "pinned historical source view")
            cert = original.read_json(certificate_path)
            require(original.update.base.manifest(parent / "mod") == {
                r["path"]:r["sha256"] for r in cert["parent_files"]}, "complete historical static input bytes")
            return saved[3](report, parent)
        return saved[3](report, root)
    def validate(files, runtime):
        if "notification_localization_patch" not in runtime:
            return saved[0](files, runtime)
        cert, child, formal = source_contract(runtime, original.ROOT)
        runtime_contract(runtime, original.ROOT, cert, child)
        require(files == formal, "formal descriptor version required")
    def tree(runtime, root):
        if "notification_localization_patch" not in runtime:
            return saved[1](runtime, root)
        cert, child, formal = source_contract(runtime, root)
        runtime_contract(runtime, root, cert, child)
        return PARENT_TREE
    def accepted():
        result = saved[2]()
        runtime = original.read_json(original.RUNTIME)
        require("notification_localization_patch" in runtime, "explicit patch proof required for this adapter")
        result["only_mod_change_from_candidate"] = "descriptor version and pinned ten-language notification key addition; mechanics unchanged"
        result["notification_localization_patch"] = runtime["notification_localization_patch"]
        return result
    original.validate_candidate_files, original.candidate_tree, original.accepted_files = validate, tree, accepted
    original.validate_static_report = static
    try:
        yield
    finally:
        (original.validate_candidate_files, original.candidate_tree, original.accepted_files,
         original.validate_static_report) = saved


if __name__ == "__main__":
    with adapted():
        original.main()
