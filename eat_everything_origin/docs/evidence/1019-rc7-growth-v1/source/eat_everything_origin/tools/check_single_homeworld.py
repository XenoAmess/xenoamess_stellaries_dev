"""Scoped acceptance derived from immutable native SAVs, never edited saves."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

import audit_save as a

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "testing"))
import inspect_1015

EXE_SHA = "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


CHECKER_SHA256 = digest(Path(__file__))


def read_run(run):
    path = run / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if (manifest["language"] != "l_simp_chinese" or manifest["game_exe_sha256"] != EXE_SHA
            or len(manifest["enabled_mods"]) != 1 or manifest["scheduled_commands"]):
        raise ValueError("wrong runtime scope or scheduled commands")
    if manifest["repository_mod_tree_sha256"] != manifest["static_gate"]["source_tree_sha256"]:
        raise ValueError("run source differs from its static gate")
    copied = Path(manifest["copied_mod"])
    actual = {p.relative_to(copied).as_posix(): digest(p) for p in copied.rglob("*") if p.is_file()}
    expected = {entry["path"]: entry["sha256"] for entry in manifest["repository_mod_files"]}
    if actual != expected:
        raise ValueError("copied runtime Mod differs from the manifest")
    return manifest


def observed(run, stage):
    read_run(run)
    return inspect_1015.observe(run / (stage + ".sav"), run / "manifest.json")


def energy(country, period="current_month"):
    categories = country["budget_categories"][period]
    totals = {key: sum(row.get("energy", 0) for row in categories[key].values())
              for key in ("income", "expenses")}
    return {**totals, "balance": totals["income"] - totals["expenses"]}


def startup(run, prefix, kind):
    initial, first = observed(run, prefix + "m00"), observed(run, prefix + "m01")
    country = first["country"]
    cores = [(key, world) for key, world in first["worlds"].items() if "eep_core" in world["flags"]]
    checks = {"initial_date": initial["date"] == "2200.01.01", "first_month_date": first["date"] == "2200.02.01",
              "one_colony": len(country["owned_colonies"]) == 1,
              "one_initial_colony": len(initial["country"]["owned_colonies"]) == 1,
              "one_bound_core": len(cores) == 1,
              "no_extra_grant_flag": "eep_extra_world_granted" not in country["flags"],
              "no_extra_target": not any(t["name"].startswith("eep_extra_world") for t in first["event_targets"]),
              "no_extra_world_flag": all("eep_startup_world" not in p["flags"] for p in first["worlds"].values()),
              "crisis_perk": "ap_become_the_crisis" in country["ascension_perks"],
              "automatic_devouring_off": "eep_auto_devour_enabled" not in country["flags"],
              "startup_flags": all(key in country["flags"] for key in
                                   ("eep_startup_granted", "eep_mothership_granted", "eep_parallel_construction_granted")),
              "no_startup_subsidy": initial["country"]["stockpile"].get("energy") == 200,
              "initial_energy_nonnegative": energy(initial["country"])["balance"] >= 0,
              "first_month_energy_nonnegative": energy(country)["balance"] >= 0}
    expected_class = {"hive": "pc_hive", "lithoid": "pc_hive", "machine": "pc_machine", "purifier": "pc_relic"}[kind]
    details = {"initial_sha256": initial["save_sha256"], "first_month_sha256": first["save_sha256"]}
    if cores:
        core_id, core = cores[0]
        colony_id = str(core["colony"])
        colony = first["colonies"][colony_id]
        districts = {first["districts"][str(i)]["type"]: first["districts"][str(i)]["level"] for i in colony["districts"]}
        core_jobs = [first["pop_jobs"][str(i)] for i in colony["pop_jobs"]]
        technicians = [j for j in core_jobs if j["type"] in ("technician", "technician_drone")]
        checks.update(correct_homeworld=core["planet_class"] == expected_class,
                      correct_capital=country["native"]["capital"] == core["colony"],
                      core_target=any(t["name"] == "eep_core0" and str(t["id"]) == core_id for t in first["event_targets"]),
                      court="eep_court" in core["modifiers"],
                      two_core_queues=any(q["type"] == "planet" and str(q["location"]["id"]) == core_id
                                          and q["simultaneous"] == 2 for q in first["queues"].values()),
                      power_jobs_staffed=any(j["workforce"] > 0 for j in technicians))
        if kind == "hive":
            checks["food_layout"] = districts.get("district_hive_3") == 2
        elif kind == "machine":
            checks["mineral_layout"] = districts.get("district_nexus_2") == 2
        elif kind == "lithoid":
            checks["lithoid_layout"] = districts.get("district_hive_2") == 4 and not districts.get("district_hive_3", 0)
        details.update(core=core_id, districts=districts, technicians=technicians,
                       core_pop=colony["actual_pop_sum"], first_month_energy=energy(country))
    mothers = [f for f in first["fleets"].values() if f["name"] == "NAME_EEP_Baiqi_Mothership"]
    checks["unique_mothership"] = len(mothers) == 1 and sum(len(f["ships"]) for f in mothers) == 1
    if mothers:
        ship_ids = {int(key) for f in mothers for key in f["ships"]}
        yards = [s for s in first["starbases"].values() if s["station"] in ship_ids]
        checks["ten_mobile_shipyards"] = (len(yards) == 1 and
            first["queues"].get(str(yards[0]["shipyard_build_queue"]), {}).get("simultaneous") == 10)
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL", "scope": "new-game startup and first month only",
            "kind": kind, "checks": checks, "details": details, "fully_accepted_civics": []}


def monthly_run(run, prefix):
    read_run(run)
    rows = []
    for month in range(13):
        path = run / f"{prefix}m{month:02}.sav"
        native = a.audit(path, (0,))
        expected = f"{2200 + month // 12:04}.{month % 12 + 1:02}.01"
        if native["date"] != expected:
            raise ValueError("actual native monthly date differs: " + str(path))
        country = native["countries"]["0"]
        rows.append({"date": expected, "sha256": native["save_sha256"],
                     "energy": energy(country), "last_month_energy": energy(country, "last_month"),
                     "stockpile": country["stockpile"], "native_budget": country["budget_categories"],
                     "used_naval_capacity": country["native"].get("used_naval_capacity")})
    return rows


def economy(baseline, baseline_prefix, candidate, candidate_prefix):
    before, after = monthly_run(baseline, baseline_prefix), monthly_run(candidate, candidate_prefix)
    checks = {"twelve_baseline_months": len(before[1:]) == 12, "twelve_candidate_months": len(after[1:]) == 12,
              "candidate_energy_nonnegative_all_months": all(row["energy"]["balance"] >= 0 for row in after[1:]),
              "candidate_energy_stock_never_decreases": all(
                  right["stockpile"].get("energy", 0) >= left["stockpile"].get("energy", 0) - .0001
                  for left, right in zip(after, after[1:])),
              "same_initial_energy_stock": before[0]["stockpile"].get("energy") == after[0]["stockpile"].get("energy") == 200}
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL", "checks": checks,
            "baseline_months": 12, "candidate_months": 12, "baseline": before, "candidate": after,
            "scope": "twelve actual monthly energy balances; other resource budgets retained, no full campaign claim"}


def differences(before, after, path="$"):
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(before.keys() | after.keys()):
            result.extend(differences(before.get(key), after.get(key), path + "." + key))
        return result
    if before != after:
        return [{"path": path, "before": before, "after": after}]
    return []


def gameplay_fields(observation):
    fields = ("worlds", "colonies", "districts", "pop_groups", "pop_jobs", "situations", "event_targets",
              "zones", "queues", "construction_items", "fleets", "starbases")
    result = {key: observation[key] for key in fields}
    for key in ("stockpile", "variables", "flags", "owned_colonies", "ascension_perks", "native"):
        result["country." + key] = observation["country"][key]
    return result


def same_day(run, before_stage, after_stage):
    before, after = observed(run, before_stage), observed(run, after_stage)
    delta = differences(gameplay_fields(before), gameplay_fields(after))
    same_date = before["date"] == after["date"]
    return {"status": "PASS_SCOPED" if same_date and not delta else "FAIL", "same_date": same_date,
            "before_sha256": before["save_sha256"], "after_sha256": after["save_sha256"], "differences": delta,
            "scope": "strict same-day gameplay fields; all differences retained for separate review"}


def review_same_day(run, before_stage, after_stage, strict_path):
    """Only verified index/owner metadata, with the original strict FAIL retained."""
    strict = json.loads(strict_path.read_text(encoding="utf-8"))
    before_path, after_path = (run / (stage + ".sav") for stage in (before_stage, after_stage))
    if (strict["before_sha256"] != digest(before_path) or strict["after_sha256"] != digest(after_path)
            or not strict["same_date"] or strict["status"] != "FAIL"):
        raise ValueError("strict native reload evidence missing or changed")
    texts = []
    inventories = []
    for path in (before_path, after_path):
        with zipfile.ZipFile(path) as archive:
            text = archive.read("gamestate").decode("utf-8-sig")
        texts.append(text)
        country = a.block(a.block(text, "country"), "0")
        owned = a.block(a.block(country, "fleets_manager"), "owned_fleets")
        fleet_ids = {int(value) for value in re.findall(r"\bfleet\s*=\s*(\d+)", owned)}
        fleets = a.block(text, "fleet")
        inventories.append({identity: a.ids(a.block(a.block(fleets, str(identity)), "ships")) for identity in fleet_ids})
    checks = {"all_owned_fleets_and_members_preserved": inventories[0] == inventories[1]}
    approved, rejected = [], []
    observations = [observed(run, stage) for stage in (before_stage, after_stage)]
    if (observations[0]["date"] != observations[1]["date"] or
            differences(*[gameplay_fields(o) for o in observations]) != strict["differences"]):
        raise ValueError("strict report omitted or changed actual native differences")
    for delta in strict["differences"]:
        path = delta["path"]
        design = re.fullmatch(r"\$\.fleets\.(\d+)\.ships\.(\d+)\.design_id", path)
        owner = re.fullmatch(r"\$\.fleets\.(\d+)\.ships\.(\d+)\.native\.original_owner", path)
        station = re.fullmatch(r"\$\.starbases\.(\d+)\.station_native\.original_owner", path)
        proof = None
        if design and int(design[1]) in inventories[0] and int(design[2]) in inventories[0][int(design[1])]:
            bodies = [a.block(a.block(text, "ship_design"), str(delta[key]))
                      for text, key in zip(texts, ("before", "after"))]
            if bodies[0] and bodies[0] == bodies[1]:
                proof = {"reason": "native design index changed; complete design body identical",
                         "design_body_sha256": hashlib.sha256(bodies[0].encode()).hexdigest(),
                         "design_body_bytes": len(bodies[0].encode())}
        elif delta["before"] is None and delta["after"] == 0:
            if owner:
                fleet, ship = int(owner[1]), int(owner[2])
                if all(fleet in inv and ship in inv[fleet] for inv in inventories):
                    proof = {"reason": "previously owned ship records its original country0 owner on load"}
            elif station:
                pair = [o["starbases"].get(station[1]) for o in observations]
                if all(pair) and pair[0]["station"] == pair[1]["station"]:
                    if all(p["station_native"]["fleet"] in inv and p["station"] in inv[p["station_native"]["fleet"]]
                           for p, inv in zip(pair, inventories)):
                        proof = {"reason": "previously owned station records its original country0 owner on load"}
        if proof:
            approved.append({**delta, **proof})
        else:
            rejected.append(delta)
    checks["every_strict_difference_independently_explained"] = bool(approved) and not rejected
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL", "checks": checks,
            "strict_report": str(strict_path), "strict_report_sha256": digest(strict_path),
            "before_sha256": digest(before_path), "after_sha256": digest(after_path),
            "approved_metadata_differences": approved, "unexplained_differences": rejected,
            "scope": "this exact same-day pair only; original strict FAIL remains unchanged"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("startup")
    start.add_argument("run", type=Path)
    start.add_argument("prefix")
    start.add_argument("kind", choices=("hive", "machine", "purifier", "lithoid"))
    budget = sub.add_parser("economy")
    budget.add_argument("baseline", type=Path)
    budget.add_argument("baseline_prefix")
    budget.add_argument("candidate", type=Path)
    budget.add_argument("candidate_prefix")
    compare = sub.add_parser("same-day")
    compare.add_argument("run", type=Path)
    compare.add_argument("before")
    compare.add_argument("after")
    review = sub.add_parser("review-same-day")
    review.add_argument("run", type=Path)
    review.add_argument("before")
    review.add_argument("after")
    review.add_argument("strict_report", type=Path)
    args = parser.parse_args()
    if args.command == "startup":
        result = startup(args.run, args.prefix, args.kind)
    elif args.command == "economy":
        result = economy(args.baseline, args.baseline_prefix, args.candidate, args.candidate_prefix)
    elif args.command == "same-day":
        result = same_day(args.run, args.before, args.after)
    else:
        result = review_same_day(args.run, args.before, args.after, args.strict_report)
    result["checker_sha256"] = CHECKER_SHA256
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "output": str(args.output), "checks": result.get("checks")}, ensure_ascii=False))
    return 0 if result["status"] == "PASS_SCOPED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
