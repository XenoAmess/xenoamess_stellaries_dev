"""Read a completed native monthly receipt set; never imports desktop modules."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(PROJECT / "tools"), str(PROJECT / "testing")]
import audit_save as a
import inspect_1019 as native
import runtime_economy_1019 as economy

RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
TREE = "cc181c8a27ede295e9fcebeffc5e10bb75e9cd643edec1d194b928993ffab33a"
VERSION = "0.4.0-rc.6"
BASE_MAP = PROJECT / "docs/evidence/1019-baseline-reference-map/baseline-031-economy-map-v1.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ref(path, kind="analysis"):
    path = Path(path).resolve()
    return {"path": path.relative_to(PROJECT).as_posix() if path.is_relative_to(PROJECT) else str(path),
            "sha256": sha(path), "kind": kind}


def stable(path):
    first = path.stat()
    data, again = path.read_bytes(), path.read_bytes()
    last = path.stat()
    if data != again or (first.st_size, first.st_mtime_ns) != (last.st_size, last.st_mtime_ns):
        raise ValueError("source bytes still changing: " + str(path))
    return data


def decimal(value):
    return Decimal(str(value))


def net(country, resource="energy"):
    categories = country["budget_categories"]["current_month"]
    income, expenses = (sum((decimal(row.get(resource, 0)) for row in categories[key].values()), Decimal(0))
                        for key in ["income", "expenses"])
    return {"income": float(income), "expenses": float(expenses), "net": float(income - expenses),
            "net_exact": str(income - expenses)}


def projection(path, branch, pristine=True):
    raw = stable(path)
    audit = load(path.with_suffix(".audit.json"))
    assert audit["audit_tool_sha256"] == sha(Path(a.__file__))
    assert hashlib.sha256(raw).hexdigest() == audit["save_sha256"]
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        gamestate = archive.read("gamestate")
    assert hashlib.sha256(gamestate).hexdigest() == audit["gamestate_sha256"]
    fields = list(a.fields(gamestate.decode("utf-8-sig")))
    roots = {k: v for k, v, block in fields if block}
    fleets = {k: v for k, v, block in a.fields(roots["fleet"]) if block}
    ships = {k: v for k, v, block in a.fields(roots["ships"]) if block}
    date = next(a.unquote(v) for k, v, b in fields if k == "date" and not b)
    assert date == audit["date"]
    country_raw = a.block(roots["country"], "0")
    country = audit["countries"]["0"]
    founder_id = str(country["native"]["founder_species_ref"])
    founder = audit["species"][founder_id]
    founder_raw = a.block(roots["species_db"], founder_id)
    assert [a.unquote(value) for key, value, block in a.fields(a.block(founder_raw, "traits")) if key == "trait" and not block] == founder["traits"]
    if pristine:
        if branch == "hive" and set(founder["traits"]) & {"trait_lithoid", "trait_machine_unit", "trait_mechanical"}:
            raise ValueError("requested organic Hive is actually a lithoid or machine founder")
        if branch == "machine" and "trait_machine_unit" not in founder["traits"]:
            raise ValueError("requested Machine branch lacks native machine founder trait")
    native_country_scalars = a.scalars(country_raw)
    assert all(native_country_scalars[key] == value for key, value in country["native"].items())
    assert {k: v for k, v in a.scalars(a.block(country_raw, "flags")).items() if k.startswith("eep")} == country["flags"]
    # Re-extract every recorded budget scalar directly from the bound native block.
    budget = {}
    for period in ["current_month", "last_month"]:
        budget[period] = {direction: {name: a.scalars(values) for name, values, block in a.fields(
            a.block(a.block(a.block(country_raw, "budget"), period), direction)) if block}
            for direction in ["income", "expenses", "balance"]}
    assert budget == country["budget_categories"]
    assert a.scalars(a.block(a.block(a.block(country_raw, "modules"), "standard_economy_module"), "resources")) == country["stockpile"]
    assert a.ids(a.block(country_raw, "owned_planets")) == country["owned_colonies"]
    targets = [a.scalars(v) for k, v, b in fields if k == "saved_event_target" and b]
    core_targets = [t for t in targets if t.get("name") == "eep_core0" and t.get("type") == "planet"]
    assert len(core_targets) == 1
    core_id = str(core_targets[0]["id"])
    core = audit["planets"][core_id]
    colony = audit["colonies"][str(core["colony"])]
    native_core = a.scalars(a.block(a.block(roots["planets"], "planet"), core_id))
    assert all(native_core.get(key) == core.get(key) for key in ["planet_class", "owner", "colony"])
    native_colony = a.block(roots["colony"], str(core["colony"]))
    assert a.ids(a.block(native_colony, "pop_groups")) == colony["pop_groups"]
    assert sum(a.scalars(a.block(roots["pop_groups"], str(i)))["size"] for i in colony["pop_groups"]) == colony["actual_pop_sum"]
    mother_targets = [t for t in targets if t.get("name") == "eep_mothership0" and t.get("type") == "fleet"]
    assert len(mother_targets) == 1
    fleet_id = str(mother_targets[0]["id"])
    fleet = fleets[fleet_id]
    members = a.ids(a.block(fleet, "ships"))
    assert len(members) == 1
    ship_id = str(members[0])
    ship = ships[ship_id]
    design_id = str(a.scalars(a.block(ship, "ship_design_implementation"))["design"])
    design = native.design(a.block(roots["ship_design"], design_id))
    layout = [{"ship_size": stage["native"].get("ship_size"), "required_components": stage["required_components"],
               "sections": [{"native": section["native"], "components": section["components"]} for section in stage["sections"]]}
              for stage in design["stages"]]
    state = {"country_variables": a.scalars(a.block(country_raw, "variables")),
             "fleet_variables": a.scalars(a.block(fleet, "variables")), "government": a.block(country_raw, "government"), "layout": layout}
    if pristine:
        economy.require_pristine(state, branch)
    owned = set(re.findall(r"\bfleet\s*=\s*(\d+)", a.block(a.block(country_raw, "fleets_manager"), "owned_fleets")))
    assert fleet_id in owned and a.scalars(ship)["fleet"] == int(fleet_id)
    owned_ships = {}
    fleet_modifiers = {}
    for identity in owned:
        body = fleets[identity]
        fleet_modifiers[identity] = native.modifiers(body)["items"]
        for sid in a.ids(a.block(body, "ships")):
            body = ships[str(sid)]
            owned_ships[str(sid)] = {"fleet": identity, "name_raw": a.block(body, "name"), "original_owner": a.scalars(body).get("original_owner")}
    jobs = {str(i): audit["pop_jobs"][str(i)] for i in colony["pop_jobs"]}
    for identity, record in jobs.items():
        assert record == a.scalars(a.block(roots["pop_jobs"], identity))
    return {"source": ref(path, "native_save"), "audit": ref(path.with_suffix(".audit.json")), "date": date,
            "gamestate_sha256": audit["gamestate_sha256"], "country": country,
            "founder_species_id": founder_id, "founder_species": founder, "core_id": core_id,
            "core": core, "colony": colony, "core_population": colony["actual_pop_sum"], "jobs": jobs,
            "districts": {str(i): audit["districts"][str(i)] for i in colony["districts"]},
            "mother": {"fleet": fleet_id, "ship": ship_id, "design_name": design["name"], "layout": layout,
                       "country_variables": state["country_variables"], "fleet_variables": state["fleet_variables"]},
            "owned_ships": owned_ships, "country_modifiers": native.modifiers(country_raw)["items"],
            "fleet_modifiers": fleet_modifiers, "event_targets": targets, "energy": net(country),
            "auto_devour_off": "eep_auto_devour_enabled" not in country["flags"],
            "_audit": audit}


def upkeep_costs(states):
    source = Path(r"C:\SteamLibrary\steamapps\common\Stellaris\common\economic_categories\00_common_categories.txt")
    assert sha(source) == "b3da494d1889bf79a361840f4e9705995e8cd2bbee09d65629d7e182cf46f01b"
    parents = {key: a.scalars(body).get("parent") for key, body, block in a.fields(source.read_text(encoding="utf-8-sig")) if block}
    family = {"planet_districts"}
    while True:
        expanded = family | {key for key, parent in parents.items() if parent in family}
        if expanded == family:
            break
        family = expanded
    assert {"planet_districts_farming", "planet_districts_mining", "planet_districts_generator", "planet_districts_cities"} <= family
    rows = []
    for state in states:
        expenses = state["country"]["budget_categories"]["current_month"]["expenses"]
        groups = {name: {category: values for category, values in expenses.items() if category in categories}
                  for name, categories in {"ships": {"ships"}, "ship_components": {"ship_components"},
                                           "planet_buildings": {"planet_buildings"}, "planet_districts_family": family}.items()}
        present = {name: any(decimal(v) > 0 for values in categories.values() for v in values.values()) for name, categories in groups.items()}
        rows.append({"date": state["date"], "native_categories": groups, "nonzero_groups": present})
    return all(all(row["nonzero_groups"].values()) for row in rows), rows, ref(source)


def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def analyze(branch, prefix):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,20}", prefix):
        raise ValueError("explicit safe prefix required")
    total_path = RUN / (prefix + "-economy-receipt.json")
    final_path = RUN / (prefix + "yearui.native-save.json")
    if not total_path.exists() or not final_path.exists():
        return {"status": "PENDING", "branch": branch, "prefix": prefix, "reason": "complete twelve-month total receipt and yearUI not yet available"}
    total = json.loads(stable(total_path))
    if total.get("state") != "COLLECTED_NOT_ACCEPTED" or total.get("cleanup_errors"):
        return {"status": "PENDING_OR_ABORTED", "branch": branch, "collector_state": total.get("state"), "error": total.get("error")}
    plan = total["plan"]
    assert plan["prefix"] == prefix and plan["government"] == branch and plan["run_id"] == "20261019T150008Z"
    assert plan["expected_tree_sha256"] == TREE and plan["expected_version"] == VERSION
    manifest = economy.validate_package(RUN / "manifest.json", TREE, VERSION)
    assert sha(RUN / "manifest.json") == plan["manifest_sha256"]
    anchor_receipt = RUN / (prefix + "m00.native-save.json")
    anchor = load(anchor_receipt)
    assert sha(anchor_receipt) == plan["anchor_receipt_sha256"]
    assert sha(RUN / (prefix + "m00.sav")) == anchor["sha256"] == plan["anchor_sha256"]
    assert anchor["date"] == plan["anchor_date"] == "2200.01.01"
    assert len(total["snapshots"]) == len(total["commands"]) == len(plan["months"]) == 12
    assert all(row["command"] == "fast_forward 30" for row in total["commands"])
    assert sha(Path(economy.__file__)) == total["collector_sha256"]
    for index, row in enumerate(total["snapshots"], 1):
        receipt = RUN / f"{prefix}m{index:02}-receipt.json"
        assert sha(receipt) == row["receipt_sha256"]
        entry = load(receipt)
        assert entry["sha256"] == row["sha256"] and entry["month"] == index and entry["government"] == branch
        assert entry["date"] == f"{2200 + index // 12:04}.{index % 12 + 1:02}.01"
        assert entry["manifest_sha256"] == plan["manifest_sha256"] and entry["run_id"] == plan["run_id"]
        assert entry["command"]["command"] == "fast_forward 30"
        assert entry["source_mtime_ns"] > entry["source_prior_mtime_ns"] and entry["source_mtime_ns"] >= entry["command_started_ns"]
        assert sha(RUN / f"{prefix}m{index:02}.sav") == entry["sha256"]
        assert sha(RUN / f"{prefix}m{index:02}.audit.json") == entry["audit_sha256"]
    assert sha(final_path) == total["year_ui"]["receipt_sha256"]
    final_receipt = load(final_path)
    assert final_receipt["sha256"] == total["year_ui"]["sha256"] == sha(RUN / (prefix + "yearui.sav"))
    assert final_receipt["date"] == total["year_ui"]["date"] == "2201.01.01"
    comparison_path = RUN / (prefix + "-auto-ui-comparison-m12.json")
    assert sha(comparison_path) == total["auto_ui_comparison"]["sha256"]
    assert load(comparison_path)["all_fields_equal"] is True
    mapping = load(BASE_MAP)
    assert sha(BASE_MAP) == "07e2c61203d350d40c5ef1b4600622a1b4d3d135ed5c27624ad2a6342cced847"
    baseline_rows = mapping["economy_baseline_payload"][branch]["baseline_months"]
    assert len(baseline_rows) == 12
    for row in baseline_rows:
        assert sha(PROJECT / row["evidence"]["path"]) == row["evidence"]["sha256"]
    baseline_prefix = mapping["branches"][branch]["prefix"]
    baseline_initial = projection(PROJECT / "docs/evidence/1019-baseline" / (baseline_prefix + "00.sav"), branch, False)
    states = [projection(RUN / f"{prefix}m{i:02}.sav", branch) for i in range(13)]
    final = projection(RUN / (prefix + "yearui.sav"), branch)
    for i, state in enumerate(states):
        assert state["date"] == f"{2200 + i // 12:04}.{i % 12 + 1:02}.01"
    assert final["date"] == "2201.01.01"
    comparison = economy.compare_economy(states[-1]["_audit"], final["_audit"])
    assert comparison["all_fields_equal"]
    baseline_verified = []
    for row in baseline_rows:
        audit = load((PROJECT / row["evidence"]["path"]).with_suffix(".audit.json"))
        with zipfile.ZipFile(PROJECT / row["evidence"]["path"]) as archive:
            assert archive.testzip() is None
            raw = archive.read("gamestate")
            assert hashlib.sha256(raw).hexdigest() == audit["gamestate_sha256"]
        native_country = a.block(a.block(raw.decode("utf-8-sig"), "country"), "0")
        current = a.block(a.block(native_country, "budget"), "current_month")
        categories = {direction: {name: a.scalars(values) for name, values, block in a.fields(a.block(current, direction)) if block}
                      for direction in ["income", "expenses", "balance"]}
        assert categories == audit["countries"]["0"]["budget_categories"]["current_month"]
        actual = net(audit["countries"]["0"])
        assert actual["net"] == row["net_energy"] and audit["date"] == row["date"]
        baseline_verified.append({**row, "native_energy": actual})
    # All reports remain absent until every original source has been checked above.
    folder = PROJECT / "docs/evidence/1019-rc6-economy" / branch
    folder.mkdir(parents=True, exist_ok=False)
    (folder / ".gitattributes").write_bytes(b"* -text\n")
    files = []
    paths = [RUN / "manifest.json", total_path, comparison_path]
    for i in range(13):
        paths.extend([RUN / f"{prefix}m{i:02}.sav", RUN / f"{prefix}m{i:02}.audit.json",
                      RUN / (f"{prefix}m{i:02}.native-save.json" if i == 0 else f"{prefix}m{i:02}-receipt.json")])
        if i:
            paths.append(RUN / f"{prefix}m{i:02}.economy.json")
    paths.extend(RUN / (prefix + "yearui" + suffix) for suffix in [".sav", ".audit.json", ".native-save.json"])
    for path in paths:
        data = stable(path)
        target = folder / path.name
        with target.open("xb") as stream:
            stream.write(data)
        assert target.read_bytes() == path.read_bytes() == data
        files.append({"source": str(path), "path": path.name, "bytes": len(data), "sha256": sha(path)})
    first, month1 = states[0], states[1]
    expected_type = {"purifier": "pc_relic", "hive": "pc_hive", "machine": "pc_machine"}[branch]
    generator_jobs = [j for j in month1["jobs"].values() if j["type"] in ["technician", "technician_drone"]]
    all_states = states + [final]
    ledgers = []
    for before, after in zip(states, states[1:]):
        resources = sorted(set(before["country"]["stockpile"]) | set(after["country"]["stockpile"]))
        row = {"date": after["date"], "resources": {}}
        for resource in resources:
            native_net = net(after["country"], resource)
            old, new = before["country"]["stockpile"].get(resource, 0), after["country"]["stockpile"].get(resource, 0)
            residual = decimal(new) - decimal(old) - decimal(native_net["net_exact"])
            row["resources"][resource] = {"before": old, "after": new, "native_net": native_net, "residual": str(residual)}
        ledgers.append(row)
    resource_closure = all(abs(decimal(r["residual"])) <= Decimal("0.00001") for row in ledgers for r in row["resources"].values())
    initial_ids = set(first["owned_ships"])
    ships_held = all(set(s["owned_ships"]) == initial_ids and s["owned_ships"] == first["owned_ships"] for s in all_states)
    job_limits = all(j.get("max_workforce", -1) < 0 or j.get("workforce_limit") == j.get("max_workforce")
                     for state in all_states for j in state["jobs"].values())
    normal_costs, upkeep_rows, upkeep_source = upkeep_costs(states[1:])
    source_new = Path(manifest["copied_mod"]) / "common/static_modifiers/eep_modifiers.txt"
    old_manifest = load(PROJECT / "docs/evidence/1019-baseline/manifest.json")
    source_old = Path(old_manifest["copied_mod"]) / "common/static_modifiers/eep_modifiers.txt"
    assert sha(source_old) == next(row["sha256"] for row in old_manifest["repository_mod_files"]
                                   if row["path"] == "common/static_modifiers/eep_modifiers.txt")
    old_upkeep = {k: v for k, v in a.scalars(a.block(source_old.read_text(encoding="utf-8-sig"), "eep_mothership")).items() if "upkeep" in k or "maintenance" in k}
    new_upkeep = {k: v for k, v in a.scalars(a.block(source_new.read_text(encoding="utf-8-sig"), "eep_mothership")).items() if "upkeep" in k or "maintenance" in k}
    normal_upkeep = normal_costs and old_upkeep == new_upkeep and all(
        "eep_mothership" not in [m["modifier"] for m in s["country_modifiers"]] and all(
            ("eep_mothership" in [m["modifier"] for m in mods]) == (fid == s["mother"]["fleet"])
            for fid, mods in s["fleet_modifiers"].items()) for s in all_states)
    startup_checks = {"single_homeworld": all(len(s["country"]["owned_colonies"]) == 1 for s in [first, month1]),
        "correct_homeworld_type": all(s["core"]["planet_class"] == expected_type for s in [first, month1]),
        "initial_energy_200": first["country"]["stockpile"].get("energy") == 200,
        "first_month_generator_jobs": any(j["workforce"] > 0 for j in generator_jobs),
        "auto_devour_off": all(s["auto_devour_off"] for s in all_states),
        "population_preserved": first["core_population"] == baseline_initial["core_population"],
        "normal_upkeep": normal_upkeep}
    economy_checks = {"baseline_12_months": True, "candidate_12_months": True,
        "all_net_energy_nonnegative": all(s["energy"]["net"] >= 0 for s in states[1:]),
        "no_resource_injection": None, "no_trade_subsidy": None, "no_job_closure": None, "no_ship_disband": None}
    candidate_rows = [{"date": s["date"], "net_energy": s["energy"]["net"],
                       "evidence": ref(folder / Path(s["source"]["path"]).name, "native_save")} for s in states[1:]]
    for s in all_states:
        s.pop("_audit")
    report = {"schema": "eep.rc6.economy_startup_native_branch.v1", "status": "PASS_SCOPED" if all(startup_checks.values()) and economy_checks["all_net_energy_nonnegative"] else "FAIL",
        "scope": "Completed native branch startup, monthly budgets and same-date auto/UI save fields only; operation constraints require separate recorded input review",
        "branch": branch, "prefix": prefix, "run_id": plan["run_id"], "version": VERSION, "production_tree_sha256": TREE,
        "manifest": ref(folder / "manifest.json"), "collector_receipt": ref(folder / total_path.name), "baseline_map": ref(BASE_MAP),
        "startup_checks": startup_checks, "economy_checks": economy_checks, "baseline_verified": baseline_verified,
        "candidate_months": candidate_rows, "monthly_baseline_delta": [{"date": s["date"], "candidate_net": s["energy"]["net"],
            "baseline_net": b["net_energy"], "difference": float(decimal(s["energy"]["net_exact"]) - decimal(b["net_energy"]))}
            for s, b in zip(states[1:], baseline_rows)], "native_states": all_states,
        "baseline_initial_population": {"source": baseline_initial["source"], "core": baseline_initial["core_id"], "population": baseline_initial["core_population"]},
        "first_month_generator_jobs": generator_jobs, "auto_ui_comparison": comparison,
        "monthly_stock_ledger": ledgers, "observed_constraints": {"all_stocked_resources_close": resource_closure,
            "native_finite_job_limits_at_max": job_limits, "initial_owned_ship_ids_names_fleets_preserved": ships_held,
            "receipt_commands_exactly12_FF30": True}, "upkeep": {"normal_costs_present": normal_costs,
            "old_source": ref(source_old), "new_source": ref(source_new), "old_mother_discount": old_upkeep, "new_mother_discount": new_upkeep,
            "normal_cost_category_rows": upkeep_rows, "native_district_family_source": upkeep_source},
        "analysis_source": ref(Path(__file__)), "parser_sources": {name: sha(PROJECT / folder_name / name)
            for folder_name, name in [("tools", "audit_save.py"), ("testing", "inspect_1019.py"), ("tools", "runtime_economy_1019.py")]},
        "limitations": ["No UI/OCR, action-chain or log review; final case evidence kinds remain incomplete.",
            "Operation-constraint check values remain null until root separately reviews recorded inputs; native checkpoints are limited observations.",
            "Population comparison is same-preset historical Mod core, excluding gift colony; not pure-vanilla control.",
            "Only energy>=0 is asserted, other resources and native maintenance remain in raw records.",
            "No whole-Mod or public release PASS."], "created_at_utc": datetime.now(timezone.utc).isoformat()}
    write(folder / "native-branch-report.json", report)
    evidence = [ref(folder / "native-branch-report.json"), ref(folder / (prefix + "m00.sav"), "native_save"),
                ref(folder / (prefix + "m01.sav"), "native_save"), ref(folder / (prefix + "m12.sav"), "native_save"),
                ref(folder / (prefix + "yearui.sav"), "native_save"), ref(folder / total_path.name)]
    payload = {"schema": "eep.rc6.startup_economy_payload_proposal.v1", "status": "PENDING_CASE_EVIDENCE_ASSEMBLY",
        "cases": {branch + "_startup": {"status": "PENDING", "production_tree_sha256": TREE, "run_ids": [plan["run_id"]], "checks": startup_checks, "evidence": evidence},
                  branch + "_economy": {"status": "PENDING", "production_tree_sha256": TREE, "run_ids": [plan["run_id"]], "checks": economy_checks, "evidence": evidence}},
        "economy": {branch: {"baseline_months": baseline_rows, "candidate_months": candidate_rows}},
        "assembly_gaps": ["startup/economy screenshot, action-chain and final-log evidence must be assembled by root", "four operational economy flags remain null"]}
    write(folder / "payload-proposal.json", payload)
    assert all(sha(Path(f["source"])) == f["sha256"] == sha(folder / f["path"]) for f in files)
    write(folder / "archive-index.json", {"schema": "eep.rc6.economy_thin_archive.v1", "status": "BYTE_IDENTICAL_NATIVE_RECEIPTS_ONLY", "files": files,
        "file_count": len(files), "total_bytes": sum(f["bytes"] for f in files), "report": ref(folder / "native-branch-report.json"),
        "payload": ref(folder / "payload-proposal.json"), "baseline_map": ref(BASE_MAP), "scope": "No Mod, UI images, actions or log payloads"})
    return {"status": report["status"], "branch": branch, "minimum_net_energy": min(s["energy"]["net"] for s in states[1:]),
            "startup_failures": [k for k, v in startup_checks.items() if not v], "native_constraints": report["observed_constraints"],
            "report": ref(folder / "native-branch-report.json"), "payload": ref(folder / "payload-proposal.json"), "files": len(files)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", choices=["purifier", "hive", "machine"], required=True)
    parser.add_argument("--prefix", required=True)
    args = parser.parse_args()
    print(json.dumps(analyze(args.branch, args.prefix), ensure_ascii=False, indent=2))
