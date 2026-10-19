"""Collect twelve separate native monthly observations; default is an offline plan."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
import zipfile
import zlib

import audit_save as a
import check_growth_1019 as growth
import runtime_growth_1019 as common

TREE = "06485dc540a88b30cef15c27c323ff21cd88f04ad57b79e4f5bc0590937ef468"
VERSION = "0.4.0-rc.4"
CIVICS = {"machine": "civic_machine_terminator", "hive": "civic_hive_devouring_swarm",
          "purifier": "civic_fanatic_purifiers"}


def validate_package(manifest_path, expected_tree=TREE, expected_version=VERSION):
    if (not isinstance(expected_tree, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_tree)
            or not isinstance(expected_version, str)
            or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?", expected_version)):
        raise ValueError("explicit expected tree/version must be a SHA256 and semantic version")
    import publish_1019 as gates
    manifest = common.read_json(Path(manifest_path))
    mod = Path(manifest["copied_mod"])
    actual, tree = [], hashlib.sha256()
    for path in sorted(p for p in mod.rglob("*") if p.is_file()):
        raw, name = path.read_bytes(), path.relative_to(mod).as_posix()
        actual.append({"path": name, "bytes": len(raw), "sha256": common.digest(raw)})
        tree.update(name.encode("utf-8"))
        tree.update(b"\0")
        tree.update(raw)
    gate = manifest["static_gate"]
    if (len(actual) != 59 or actual != sorted(manifest["repository_mod_files"], key=lambda x: x["path"])
            or actual != sorted(gate["files"], key=lambda x: x["path"])
            or tree.hexdigest() != expected_tree
            or manifest["repository_mod_tree_sha256"] != expected_tree
            or manifest["copied_mod_tree_sha256"] != expected_tree
            or manifest.get("profile_id") != "eep-0.4.0-single-production-mod"
            or manifest.get("enabled_mods") != ["mod/ugc_eep-1019.mod"]
            or manifest.get("language") != "l_simp_chinese"
            or manifest.get("game_exe_sha256") != common.EXE
            or common.digest(Path(manifest["game_exe"]).read_bytes()) != common.EXE
            or gate.get("source_tree_sha256") != expected_tree or gate.get("version") != expected_version
            or gate.get("status") != "PASS"):
        raise ValueError("economy collection requires the explicit single-Mod Chinese package tree/version and full file binding")
    versions = [a.unquote(value) for key, value, block in a.fields((mod / "descriptor.mod").read_text(encoding="utf-8-sig"))
                if key == "version" and not block]
    if versions != [expected_version]:
        raise ValueError("actual descriptor version differs from explicit expected version")
    report_path = Path(gate["report"])
    if common.digest(report_path.read_bytes()) != gate["report_sha256"]:
        raise ValueError("original package report bytes differ from the bound static gate")
    report = common.read_json(report_path)
    if report.get("status") != "PASS" or report.get("game_exe_sha256") != common.EXE:
        raise ValueError("the bound whole-package report did not pass for this executable")
    gates.validate_weapon_csv_contract(report, mod)
    gates.validate_planet_killer_contract(report, mod)
    user = Path(manifest["userdir"])
    if common.read_json(user / "dlc_load.json").get("enabled_mods") != ["mod/ugc_eep-1019.mod"]:
        raise ValueError("actual enabled Mod list differs from the explicit single candidate")
    settings = (user / "settings.txt").read_text(encoding="utf-8-sig")
    if (not re.search(r'(?m)^language\s*=\s*"l_simp_chinese"\s*$', settings)
            or not re.search(r"(?m)^autosave\s*=\s*2\s*$", settings)):
        raise ValueError("actual simplified-Chinese/monthly-autosave settings differ")
    return manifest


def require_pristine(state, government):
    if government not in CIVICS:
        raise ValueError("government must be explicit: machine, hive or purifier")
    native_government = state.get("government_raw", state.get("government", ""))
    if not re.search(r'(?<![A-Za-z0-9_])"?' + CIVICS[government] + r'"?(?![A-Za-z0-9_])', native_government):
        raise ValueError("actual native government differs from the requested economy branch")
    cv, fv = state["country_variables"], state["fleet_variables"]
    if (cv.get("eep_c") != 0 or cv.get("eep_mothership_level") != 0
            or fv.get("eep_applied_level") != 0
            or any(cv.get(key, 0) != 0 or fv.get(key, 0) != 0
                   for key in (*common.TIERS, "eep_component_rewards"))
            or cv.get("eep_component_entitled", 0) != 0 or cv.get("eep_component_pending", 0) != 0
            or cv.get("eep_component_snapshot_state", 0) != 0
            or "eep_component_work_budget" in fv):
        raise ValueError("economy branch has C/L/R/tier growth contamination")
    cores = state.get("core_counts")
    if cores is None:
        installed = [(item.get("slot"), item.get("template")) for stage in state["layout"]
                     for section in stage["sections"] for item in section["components"]]
        cores = {core: sum(template == core for _, template in installed) for core in growth.CORE_SLOTS.values()}
        if any([(slot, template) for slot, template in installed if template == core] != [(expected, core)]
               for expected, core in growth.CORE_SLOTS.items()):
            raise ValueError("actual RC4 core slots differ from AUX6 through AUX11")
    if any(cores.get(core) != 1 for core in growth.CORE_SLOTS.values()):
        raise ValueError("the existing Mother must carry its six actual RC4 cores")


def require_new_outputs(plan):
    artifacts = Path(plan["artifacts"])
    for stage in [month["stage"] for month in plan["months"]] + [plan["prefix"] + "yearui"]:
        if list(artifacts.glob(stage + "*")):
            raise FileExistsError("refusing to overwrite a future economy stage: " + stage)
    for name in (plan["prefix"] + "-economy-receipt.json", plan["prefix"] + "-auto-ui-comparison-m12.json"):
        if (artifacts / name).exists():
            raise FileExistsError("refusing to overwrite an economy receipt or comparison")


def make_plan(anchor_receipt, prefix, government, autosave_dir=None, expected_tree=TREE, expected_version=VERSION):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,20}", prefix):
        raise ValueError("prefix must be 1-20 safe ASCII characters")
    receipt_path = Path(anchor_receipt).resolve(strict=True)
    manifest_path = receipt_path.parent / "manifest.json"
    manifest = validate_package(manifest_path, expected_tree, expected_version)
    receipt = common.read_json(receipt_path)
    state = growth.receipt_save(receipt_path)
    if state["date"] != "2200.01.01":
        raise ValueError("economy anchor must be a fresh native 2200.01.01 new-game save")
    history = Path(receipt["history"]).resolve(strict=True)
    if common.digest(history.read_bytes()) != receipt["sha256"]:
        raise ValueError("original native history anchor bytes differ")
    require_pristine(state, government)
    user = Path(manifest["userdir"]).resolve(strict=True)
    folder = (Path(autosave_dir) if autosave_dir else Path(receipt["written_at"]).parent).resolve(strict=True)
    folder.relative_to((user / "save games").resolve(strict=True))
    date, months = state["date"], []
    for index in range(1, 13):
        date = common.next_month(date)
        months.append({"index": index, "stage": prefix + f"m{index:02}", "date": date,
                       "command": "fast_forward 30"})
    plan = {"status": "OBSERVATION_ONLY", "mode": "PLAN_ONLY", "prefix": prefix, "government": government,
            "run_id": manifest["run_id"], "artifacts": str(receipt_path.parent), "userdir": str(user),
            "manifest": str(manifest_path), "manifest_sha256": common.digest(manifest_path.read_bytes()),
            "anchor_receipt": str(receipt_path), "anchor_receipt_sha256": common.digest(receipt_path.read_bytes()),
            "anchor_sha256": state["sha256"], "anchor_date": state["date"], "autosave_dir": str(folder),
            "expected_tree_sha256": expected_tree, "expected_version": expected_version,
            "country": 0, "fleet": state["fleet"], "ship": state["ship"],
            "months": months, "final_ui_stage": prefix + "yearui"}
    require_new_outputs(plan)
    return plan


def monthly_summary(audit):
    country = audit["countries"]["0"]
    return {"status": "OBSERVATION_ONLY", "date": audit["date"], "save_sha256": audit["save_sha256"],
            "energy": {period: {direction: sum(row.get("energy", 0) for row in categories.values())
                                for direction, categories in values.items()}
                       for period, values in country["budget_categories"].items()},
            "stock": country["stockpile"].get("energy"),
            "used_naval_capacity": country["native"].get("used_naval_capacity")}


def compare_economy(auto, ui):
    country_keys = ("budget_categories", "stockpile", "variables", "flags", "owned_colonies")
    checks = {"country." + key: auto["countries"]["0"][key] == ui["countries"]["0"][key] for key in country_keys}
    checks.update({key: auto[key] == ui[key] for key in
                   ("districts", "pop_jobs", "pop_groups", "planets", "colonies")})
    checks["same_native_date"] = auto["date"] == ui["date"]
    return {"status": "OBSERVATION_ONLY", "scope": "Same-date original native automatic/UI economic fields",
            "all_fields_equal": all(checks.values()), "checks": checks,
            "auto_sha256": auto["save_sha256"], "ui_sha256": ui["save_sha256"]}


class LiveBackend(common.LiveBackend):
    def __init__(self, plan):
        validate_package(plan["manifest"], plan.get("expected_tree_sha256", TREE), plan.get("expected_version", VERSION))
        super().__init__(plan)

    def final_save(self, stage, date):
        errors = self.cleanup()
        if errors:
            raise RuntimeError("could not close console/debug before native UI save: " + "; ".join(errors))
        return self.base.r.native_save(stage, date, (0,))


def collect(plan, backend_factory=LiveBackend, autosave_timeout=25):
    require_new_outputs(plan)
    artifacts = Path(plan["artifacts"])
    result = {"status": "OBSERVATION_ONLY", "state": "STARTING", "plan": plan,
              "collector_sha256": common.digest(Path(__file__).read_bytes()), "snapshots": [], "commands": []}
    backend = None
    try:
        # Revalidate package bytes when execution actually begins, not just during an earlier plan.
        validate_package(plan["manifest"], plan.get("expected_tree_sha256", TREE), plan.get("expected_version", VERSION))
        if common.digest(Path(plan["manifest"]).read_bytes()) != plan["manifest_sha256"]:
            raise ValueError("native run manifest changed after economy planning")
        backend = backend_factory(plan)
        backend.initial()
        for month in plan["months"]:
            stage, expected = month["stage"], month["date"]
            source = Path(plan["autosave_dir"]) / ("autosave_" + expected + ".sav")
            prior_mtime = source.stat().st_mtime_ns if source.exists() else 0
            started = time.time_ns()
            command = backend.command("fast_forward 30", stage + "-advance")
            result["commands"].append(command)
            print(json.dumps({"status": "OBSERVATION_ONLY", "month": month["index"], "awaiting_hud": expected}), flush=True)
            hud = backend.wait_date(expected, stage + "-hud")
            deadline, last_error = time.monotonic() + autosave_timeout, None
            while time.monotonic() < deadline:
                try:
                    raw, state, binding = common.fresh_native(source, prior_mtime, started, expected,
                                                               (0, plan["fleet"], plan["ship"]))
                    break
                except (OSError, ValueError, KeyError, EOFError, zipfile.BadZipFile, zlib.error) as error:
                    last_error = str(error)
                    time.sleep(.2)
            else:
                raise RuntimeError("fresh complete monthly native autosave unavailable: " + str(last_error))
            archived = artifacts / (stage + ".sav")
            with archived.open("xb") as stream:
                stream.write(raw)
            audit = a.audit(archived, (0,))
            if audit["save_sha256"] != binding["sha256"] or audit["date"] != expected:
                raise RuntimeError("archived economy audit differs from original native ZIP")
            common.write_new(artifacts / (stage + ".audit.json"), audit)
            common.write_new(artifacts / (stage + ".economy.json"), monthly_summary(audit))
            binding.update(archived=str(archived), hud=hud, command=command,
                           month=month["index"], government=plan["government"],
                           observed_at_utc=datetime.now(timezone.utc).isoformat(),
                           method="separate native fast_forward 30 and monthly automatic save",
                           manifest_sha256=plan["manifest_sha256"], run_id=plan["run_id"],
                           audit_sha256=common.digest((artifacts / (stage + ".audit.json")).read_bytes()))
            month_receipt = artifacts / (stage + "-receipt.json")
            common.write_new(month_receipt, binding)
            result["snapshots"].append({**binding, "receipt": str(month_receipt),
                                         "receipt_sha256": common.digest(month_receipt.read_bytes())})
            print(json.dumps({"status": "OBSERVATION_ONLY", "month": month["index"], "date": expected,
                              "sha256": binding["sha256"], "archived": str(archived),
                              "receipt": str(month_receipt)}, ensure_ascii=False), flush=True)
            # Decode actual equipped slots independently after preserving the native observation.
            require_pristine(growth.read_save(archived), plan["government"])
        final = backend.final_save(plan["final_ui_stage"], plan["months"][-1]["date"])
        comparison = compare_economy(audit, final)
        comparison_path = artifacts / (plan["prefix"] + "-auto-ui-comparison-m12.json")
        common.write_new(comparison_path, comparison)
        result["auto_ui_comparison"] = {"path": str(comparison_path),
                                        "sha256": common.digest(comparison_path.read_bytes()), **comparison}
        if not comparison["all_fields_equal"]:
            raise RuntimeError("same-date native automatic/UI economic fields differ")
        final_receipt = artifacts / (plan["final_ui_stage"] + ".native-save.json")
        final_state = growth.receipt_save(final_receipt)
        if final_state["date"] != plan["months"][-1]["date"]:
            raise ValueError("final year UI native receipt date differs")
        require_pristine(final_state, plan["government"])
        result["year_ui"] = {"receipt": str(final_receipt), "receipt_sha256": common.digest(final_receipt.read_bytes()),
                             "date": final_state["date"], "sha256": final_state["sha256"]}
        result["state"] = "COLLECTED_NOT_ACCEPTED"
    except Exception as error:
        result.update(state="ABORTED", error_type=type(error).__name__, error=str(error))
        raise
    finally:
        result["cleanup_errors"] = backend.cleanup() if backend else []
        if result["cleanup_errors"]:
            result["state"] = "CLEANUP_REQUIRED"
        receipt_path = artifacts / (plan["prefix"] + "-economy-receipt.json")
        common.write_new(receipt_path, result)
    if result["cleanup_errors"]:
        raise RuntimeError("economy console/debug cleanup requires inspection")
    return {"status": "OBSERVATION_ONLY", "receipt": str(receipt_path), "monthly_snapshots": len(result["snapshots"]),
            "year_ui": result["year_ui"], "acceptance": "NOT_PERFORMED"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--anchor-receipt", required=True, type=Path)
    parser.add_argument("--prefix", required=True)
    parser.add_argument("--government", choices=tuple(CIVICS), required=True)
    parser.add_argument("--autosave-dir", type=Path)
    parser.add_argument("--expected-tree", default=TREE)
    parser.add_argument("--expected-version", default=VERSION)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true")
    modes.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    plan = make_plan(args.anchor_receipt, args.prefix, args.government, args.autosave_dir,
                     args.expected_tree, args.expected_version)
    output = collect(plan) if args.execute else plan
    print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
