"""0.3.2 release adapter: require this version's actual startup/economy evidence."""
import json
from pathlib import Path
import sys

import publish_update as update

ROOT = update.ROOT
VERSION = "0.3.2"
CANDIDATE_VERSION = "0.3.2-rc.2"
EVIDENCE = ROOT / "docs/evidence/publication-0.3.2"
RUNTIME = ROOT / "docs/evidence/single-homeworld-20261019/final-result.json"
CASES = {f"{branch}_{kind}" for branch in ("hive", "machine", "purifier")
         for kind in ("startup", "economy")} | {"candidate_reload", "repeat_initialization", "old_save_compatibility"}


def verify_references(entries, root):
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("runtime evidence references missing")
    for entry in entries:
        relative = Path(entry["path"])
        if relative.is_absolute():
            raise RuntimeError("runtime evidence must be project-relative")
        path = (root / relative).resolve(strict=True)
        path.relative_to(root.resolve())
        if update.digest(path.read_bytes()) != entry.get("sha256"):
            raise RuntimeError("runtime evidence changed: " + str(relative))


def validate_runtime_index(runtime, root):
    if (runtime.get("schema") != "eep-single-homeworld-acceptance-v1"
            or runtime.get("status") != "PASS_SCOPED"
            or runtime.get("version") != CANDIDATE_VERSION
            or runtime.get("language") != "l_simp_chinese"
            or runtime.get("game_exe_sha256") != update.EXE_SHA
            or runtime.get("fully_accepted_civics") != []):
        raise RuntimeError("matching scoped runtime acceptance missing")
    if set(runtime.get("cases", {})) != CASES:
        raise RuntimeError("runtime must cover all nine required case groups")
    for name, case in runtime["cases"].items():
        if case.get("status") != "PASS_SCOPED":
            raise RuntimeError("required runtime case incomplete: " + name)
        verify_references(case.get("evidence"), root)
    for branch in ("hive", "machine", "purifier"):
        budget = runtime.get("economy", {}).get(branch, {})
        if (budget.get("baseline_months") != 12 or budget.get("candidate_months") != 12
                or budget.get("candidate_energy_nonnegative_all_months") is not True):
            raise RuntimeError("twelve-month economy evidence incomplete: " + branch)
    variant = runtime.get("additional_checks", {}).get("lithoid_startup_first_month", {})
    if variant.get("status") != "PASS_SCOPED":
        raise RuntimeError("lithoid hive startup and first-month smoke evidence missing")
    verify_references(variant.get("evidence"), root)
    verify_references(runtime.get("archives"), root)


def validate_candidate_files(files, runtime):
    candidate = runtime.get("production_files", {})
    if set(files) != set(candidate) or "descriptor.mod" not in files:
        raise RuntimeError("formal file set differs from tested production candidate")
    descriptor = runtime.get("candidate_descriptor", "").encode("utf-8")
    marker = f'version="{CANDIDATE_VERSION}"'.encode()
    if (update.digest(descriptor) != candidate["descriptor.mod"]
            or descriptor.count(marker) != 1):
        raise RuntimeError("tested candidate descriptor missing or different")
    normalized = {**candidate, "descriptor.mod": update.digest(
        descriptor.replace(marker, f'version="{VERSION}"'.encode()))}
    if files != normalized:
        raise RuntimeError("formal content differs from tested candidate beyond version")


def accepted_files():
    prior = json.loads((ROOT / "docs/evidence/publication-0.3.1/workshop-verification.json").read_text(encoding="utf-8"))
    if (prior.get("status") != "PASS" or prior.get("version") != "0.3.1"
            or prior.get("item_id") != update.ITEM):
        raise RuntimeError("previous verified 0.3.1 identity differs")
    if (ROOT / "VERSION").read_text().strip() != VERSION:
        raise RuntimeError("formal VERSION is required; candidates cannot be published")
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    validate_runtime_index(runtime, ROOT)
    files = update.base.manifest(ROOT / "mod")
    validate_candidate_files(files, runtime)
    static = EVIDENCE / "open-kaishek.json"
    package = json.loads(static.read_text(encoding="utf-8"))
    if (package.get("status") != "PASS" or package.get("game_exe_sha256") != update.EXE_SHA
            or package.get("p_scripts") != 24 or package.get("p_parsed") != 24
            or len(package.get("languages", [])) != 10 or package.get("localization_keys") != 101):
        raise RuntimeError("formal open_kaishek check incomplete")
    binding = json.loads((EVIDENCE / "static-source-manifest.json").read_text(encoding="utf-8"))
    if (binding.get("production_files") != files
            or binding.get("report_sha256") != update.digest(static.read_bytes())):
        raise RuntimeError("formal static check source or report changed")
    return {"status": "PASS_SCOPED", "version": VERSION, "previous_public_version": "0.3.1",
            "production_files": files, "runtime_index_sha256": update.digest(RUNTIME.read_bytes()),
            "static_sha256": update.digest(static.read_bytes()),
            "scope": "three startup branches, twelve-month economy, reload and old-save compatibility",
            "only_mod_change_from_candidate": "descriptor version metadata"}


def record_static():
    if (ROOT / "VERSION").read_text().strip() != VERSION:
        raise RuntimeError("only record a formal static gate after candidate acceptance")
    report = EVIDENCE / "open-kaishek.json"
    if json.loads(report.read_text(encoding="utf-8")).get("status") != "PASS":
        raise RuntimeError("formal static check did not pass")
    update.base.write_json(EVIDENCE / "static-source-manifest.json", {
        "version": VERSION, "production_files": update.base.manifest(ROOT / "mod"),
        "report_sha256": update.digest(report.read_bytes())})


def configure():
    update.VERSION = VERSION
    update.EVIDENCE = EVIDENCE
    for key, name in {"STATE": "publish-state.json", "ACCEPTANCE": "acceptance.json",
                      "STATIC": "open-kaishek.json", "DOWNLOAD": "workshop-download.json",
                      "VERIFIED": "workshop-verification.json", "INLINE": "inline-images.json"}.items():
        setattr(update, key, EVIDENCE / name)
    update.accepted_files = accepted_files


if __name__ == "__main__":
    configure()
    if len(sys.argv) == 2 and sys.argv[1] == "record-static":
        record_static()
    else:
        update.main()
