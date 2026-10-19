"""Validate an explicit full or Scorched Hive first-release acceptance scope."""
import hashlib
from pathlib import Path

EXE_SHA256 = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"
SCOPED_MODE = "scorched-hive-first-release"
FOCUS_SCOPE = "scorched_hive_and_shared_mechanisms"
FOCUS_CIVIC = "civic_hive_scorched_earth"
OPEN_CIVICS = {
    "civic_hive_devouring_swarm", "civic_machine_terminator",
    "civic_fanatic_purifiers", "civic_scorched_earth", FOCUS_CIVIC,
}
CASES = {f"EAT-{number:02}" for number in range(1, 34)}
NOT_APPLICABLE = {"EAT-05", "EAT-08"}
DISCLOSURES = (
    "完整实机验收仅焦土蜂巢", "首发推荐焦土蜂巢",
    "其它路线开放但未完成完整实机验收",
)


def _evidence(entries, root, label):
    if not isinstance(entries, list) or not entries:
        raise RuntimeError(f"{label}: evidence is missing")
    root = root.resolve()
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise RuntimeError(f"{label}: invalid evidence reference")
        relative = Path(entry["path"])
        if relative.is_absolute():
            raise RuntimeError(f"{label}: evidence must use a project-relative path")
        try:
            path = (root / relative).resolve(strict=True)
            path.relative_to(root)
        except (OSError, ValueError) as error:
            raise RuntimeError(f"{label}: evidence is missing or outside the project") from error
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry.get("sha256"):
            raise RuntimeError(f"{label}: evidence bytes differ from the acceptance receipt")


def validate_runtime(runtime, production_files, version, description, note, changelog_entry, root):
    if runtime.get("production_files") != production_files:
        raise RuntimeError("acceptance production files drifted")
    if runtime.get("version") != version or runtime.get("game_exe_sha256") != EXE_SHA256:
        raise RuntimeError("acceptance version or game executable differs")
    if runtime.get("language") != "l_simp_chinese":
        raise RuntimeError("runtime must be Simplified Chinese")
    mode = runtime.get("acceptance_mode", "full")
    cases = runtime.get("cases", {})
    if not isinstance(cases, dict) or set(cases) != CASES:
        raise RuntimeError("acceptance must account for all 33 original case IDs")
    if mode == "full":
        if runtime.get("status") != "PASS" or any(
            not isinstance(case, dict) or case.get("status") != "PASS" for case in cases.values()
        ):
            raise RuntimeError("full acceptance is incomplete")
        return {"mode": "full", "status": "PASS"}
    if mode != SCOPED_MODE or runtime.get("status") != "PASS_SCOPED":
        raise RuntimeError("unknown or incomplete acceptance scope")
    if runtime.get("scope") != FOCUS_SCOPE or runtime.get("fully_accepted_civics") != [FOCUS_CIVIC]:
        raise RuntimeError("first release must claim full acceptance only for Scorched Hive")
    open_civics = runtime.get("open_civics", [])
    if not isinstance(open_civics, list) or len(open_civics) != len(OPEN_CIVICS) or set(open_civics) != OPEN_CIVICS:
        raise RuntimeError("first release must retain all five civic entrances")
    deferred = runtime.get("deferred_civics", {})
    if not isinstance(deferred, dict) or set(deferred) != OPEN_CIVICS - {FOCUS_CIVIC}:
        raise RuntimeError("other open civics must be explicitly deferred")
    for civic, case in deferred.items():
        if (not isinstance(case, dict) or case.get("status") != "NOT_COMPLETE"
                or not isinstance(case.get("remaining"), str) or not case["remaining"].strip()):
            raise RuntimeError(f"{civic}: unfinished route must disclose its remaining acceptance")
    for identity, case in cases.items():
        if not isinstance(case, dict) or case.get("scope") != FOCUS_SCOPE:
            raise RuntimeError(f"{identity}: case scope differs")
        if identity in NOT_APPLICABLE:
            if (case.get("status") != "NOT_APPLICABLE" or not isinstance(case.get("reason"), str)
                    or not case["reason"].strip()):
                raise RuntimeError(f"{identity}: explicit non-applicability reason is required")
            continue
        if case.get("status") != "PASS_SCOPED":
            raise RuntimeError(f"{identity}: required first-release acceptance is incomplete")
        _evidence(case.get("evidence"), root, identity)
    smoke = runtime.get("production_smoke", {})
    if (not isinstance(smoke, dict) or smoke.get("status") != "PASS"
            or smoke.get("production_files") != production_files):
        raise RuntimeError("a matching final production-package smoke test is required")
    _evidence(smoke.get("evidence"), root, "production smoke")
    for label, text in (("Workshop description", description), ("Change Note", note),
                        ("formal changelog", changelog_entry)):
        if any(phrase not in text for phrase in DISCLOSURES):
            raise RuntimeError(f"{label}: first-release acceptance disclosure is missing")
    return {"mode": mode, "status": "PASS_SCOPED", "fully_accepted_civics": [FOCUS_CIVIC],
            "open_civics": sorted(OPEN_CIVICS), "deferred_civics": sorted(deferred)}
