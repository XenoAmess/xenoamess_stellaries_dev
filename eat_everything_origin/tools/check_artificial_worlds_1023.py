"""Inspect real SAV tables and check a predeclared habitat settlement contract."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import audit_save as p

LEDGER = ("eep_c", "eep_g", "eep_d", "eep_made", "eep_worlds")


def table(text):
    return {key: value for key, value, obj in p.fields(text) if obj}


def snapshot(path):
    path = Path(path)
    raw = path.read_bytes()
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError("corrupt SAV")
        state = archive.read("gamestate").decode("utf-8-sig")
    roots = list(p.fields(state))
    objects = {key: value for key, value, obj in roots if obj}
    targets = {v["name"]: v for key, value, obj in roots
               if key == "saved_event_target" and obj
               and (v := p.scalars(value)).get("name", "").startswith("eep")}
    countries = {}
    receipts = {}
    for identity, value in table(objects.get("country", "")).items():
        variables = p.scalars(p.block(value, "variables"))
        if "eep_c" in variables:
            countries[identity] = {key: variables.get(key, 0) for key in LEDGER}
            receipts[identity] = {key: variables.get(key, 0) for key in ("eep_last_return", "eep_last_manufactured", "eep_last_capacity")}
    groups = {key: {**p.scalars(v), "key": p.scalars(p.block(v, "key"))}
              for key, v in table(objects.get("pop_groups", "")).items()}
    colonies = {}
    for key, value in table(objects.get("colony", "")).items():
        record = p.scalars(value)
        group_ids = [str(i) for i in p.ids(p.block(value, "pop_groups"))]
        record.update(carrier=p.scalars(p.block(value, "carrier")), pop_groups=group_ids,
                      population=sum(groups[g]["size"] for g in group_ids))
        colonies[key] = record
    planets = {}
    for key, value in table(p.block(objects.get("planets", ""), "planet")).items():
        record = p.scalars(value)
        record.update(name=p.scalars(p.block(value, "name")).get("key"),
                      flags=p.block(value, "flags"),
                      variables=p.scalars(p.block(value, "variables")),
                      coordinate=p.scalars(p.block(value, "coordinate")))
        planets[key] = record
    fleets = {key: {**p.scalars(v), "coordinate": p.scalars(p.block(p.block(v, "movement_manager"), "coordinate")),
                    "current_order": p.block(v, "current_order"),
                    "variables": p.scalars(p.block(v, "variables"))}
              for key, v in table(objects.get("fleet", "")).items()}
    megastructures = {key: {**p.scalars(v), "coordinate": p.scalars(p.block(v, "coordinate"))}
                     for key, v in table(objects.get("megastructures", "")).items()}
    situations = {key: {**p.scalars(v), "target": p.scalars(p.block(v, "target"))}
                  for key, v in table(p.block(objects.get("situations", ""), "situations")).items()}
    return {"save": str(path), "save_sha256": hashlib.sha256(raw).hexdigest(),
            "date": next(p.unquote(v) for k, v, obj in roots if k == "date"),
            "targets": targets, "countries": countries, "receipts": receipts, "planets": planets,
            "colonies": colonies, "groups": groups, "fleets": fleets,
            "megastructures": megastructures, "situations": situations}


def compare(before, after, contract):
    """Expectations are supplied before reading after, never fitted from it."""
    actor = str(contract["actor"])
    source = str(contract["source"])
    colony = str(contract["colony"])
    expected = contract["expected_ledger"]
    checks = {
        "source_existed_as_habitat": before["planets"].get(source, {}).get("planet_class") == "pc_habitat",
        "source_colony_identity": str(before["planets"].get(source, {}).get("colony")) == colony,
        "source_had_live_population": before["colonies"].get(colony, {}).get("population", 0) > 0,
        "physical_source_removed": source not in after["planets"],
        "source_colony_not_live": colony not in after["colonies"] or (
            after["colonies"][colony].get("owner") in (None, "none", 4294967295)
            and not after["colonies"][colony].get("pop_groups")),
        "expected_ledger": after["countries"].get(actor) == expected,
        "no_live_situation_targeting_source": not any(
            s.get("killed") != "yes"
            and str(s.get("target", {}).get("id", s.get("target", {}).get("reference"))) == source
            for s in after["situations"].values()),
    }
    for identity in contract.get("removed_fleets", []):
        checks["fleet_removed_" + str(identity)] = str(identity) in before["fleets"] and str(identity) not in after["fleets"]
    for identity in contract.get("removed_megastructures", []):
        checks["orbital_removed_" + str(identity)] = str(identity) in before["megastructures"] and str(identity) not in after["megastructures"]
    anchor = str(contract["anchor"])
    # Indexed flags serialize as habitat2037, not the script spelling habitat@2037.
    link = "habitat" + source
    checks["anchor_link_existed"] = link in p.scalars(before["planets"].get(anchor, {}).get("flags", ""))
    checks["anchor_link_cleared"] = (anchor in after["planets"]
        and link not in p.scalars(after["planets"][anchor]["flags"]))
    checks["new_ruined_habitat_exists"] = any(
        identity not in before["megastructures"]
        and m.get("type") == "habitat_central_complex_ruined"
        and ("system" not in contract or m.get("coordinate", {}).get("origin") == contract["system"])
        for identity, m in after["megastructures"].items())
    if "expected_core_population" in contract:
        checks["actual_core_population"] = after["colonies"][str(contract["core_colony"])]["population"] == contract["expected_core_population"]
    if "core_population_interval" in contract:
        low, high = contract["core_population_interval"]
        actual = after["colonies"][str(contract["core_colony"])]["population"]
        checks["actual_core_population_within_predeclared_month_boundary"] = low <= actual <= high
        low, high = contract["source_return_interval"]
        checks["return_receipt_within_predeclared_source_population"] = low <= after["receipts"][actor]["eep_last_return"] <= high
        checks["manufactured_receipt_exact"] = after["receipts"][actor]["eep_last_manufactured"] == contract["expected_manufactured"]
    if "other_country" in contract:
        other = str(contract["other_country"])
        checks["other_country_not_rewarded"] = before["countries"].get(other) == after["countries"].get(other)
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL", "checks": checks,
            "before_sha256": before["save_sha256"], "after_sha256": after["save_sha256"],
            "before_date": before["date"], "after_date": after["date"], "contract": contract}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("contract", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    result = compare(snapshot(args.before), snapshot(args.after), contract)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "PASS_SCOPED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
