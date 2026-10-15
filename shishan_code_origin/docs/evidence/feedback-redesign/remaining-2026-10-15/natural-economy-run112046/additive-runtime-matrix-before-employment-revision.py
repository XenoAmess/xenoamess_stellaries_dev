"""Read-only, finite-profile audit of seven native economy experiment branches.

No save or game file is written. Synthetic development snapshots are not native
acceptance evidence. A missing matrix is NOT RUN, never a zero-valued oracle.
"""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "additive_native_save_reader", ROOT / "shishan_code_origin/tools/audit_feedback_runtime_save.py")
native = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = native
_SPEC.loader.exec_module(native)
D = Decimal
BRANCHES = ("F00", "F10", "F01", "F11", "FP", "FN", "FH")
PHASES = ("input", "warm", "measured")
TRAITS = dict(zip(("FP", "FN", "FH"), (
    "trait_external_econ_probe_positive", "trait_external_econ_probe_negative", "trait_external_econ_probe_hidden")))
ARCH = "shishan_code_architecture_jobs"
COUNTER = "shishan_econ_probe_counter"
OTHER = "shishan_econ_probe_other_output"
PREFIX = "shishan_code_architecture_"
JOBS = ("biologist", "shishan_code_maintainer")
FINITE_BASE_TRAITS = sorted(("trait_machine_unit", "trait_shishan_code", "trait_robot_luxurious",
    "trait_robot_high_bandwidth", "trait_robot_high_maintenance", "trait_wet_planet_preference", "trait_robot_power_drills"))
ABS_EPS = D(".0001")
REL_EPS = D(".000001")


def number(value, context="number"):
    return native.decimal(str(value) if value is not None else None, context)


def epsilon(*values):
    return max(ABS_EPS, REL_EPS * max((abs(number(v)) for v in values), default=D(0)))


def close(left, right):
    return abs(number(left) - number(right)) <= epsilon(left, right)


def equivalent(left, right):
    """Only saved numeric precision gets tolerance; shapes and names are exact."""
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(equivalent(left[k], right[k]) for k in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(equivalent(a, b) for a, b in zip(left, right))
    if left is None or right is None:
        return left is right
    try:
        return close(left, right)
    except native.AuditError:
        return left == right


def issue(status, code, **details):
    return {"status": status, "code": code, **details}


def status_of(items, fallback="PASS"):
    for status in ("NOT RUN", "INVALID", "FAIL", "NOT COVERED"):
        if any(i["status"] == status for i in items):
            return status
    return fallback


def native_field(doc, block, key):
    value = doc.field(block, key, False)
    return None if value is None else doc.native(value)


def all_modifiers(doc, country):
    timed = doc.section(country, "timed_modifier", False)
    items = doc.section(timed, "items") if timed else None
    result = []
    for entry in doc.entries(items) if items else []:
        if entry.key is not None or not isinstance(entry.value, native.Block):
            raise native.AuditError("unknown timed_modifier layout")
        block = entry.value
        result.append({"modifier": doc.scalar(block, "modifier"),
                       "multiplier": str(number(doc.scalar(block, "multiplier", False) or "1")),
                       "days": doc.scalar(block, "days", False)})
    return sorted(result, key=lambda r: (r["modifier"], r["multiplier"]))


def resource_table(doc, block):
    if block is None:
        return None
    result = {}
    for entry in doc.entries(block):
        if entry.key is None or isinstance(entry.value, native.Block) or entry.key in result:
            raise native.AuditError("unknown or duplicate native resource row")
        result[entry.key] = str(number(entry.value, entry.key))
    return result


def budget_snapshot(doc, country):
    budget = doc.section(country, "budget", False)
    result = {}
    for period in ("current_month", "last_month"):
        block = doc.section(budget, period, False) if budget else None
        result[period] = {}
        for kind in ("income", "expenses"):
            rows = doc.section(block, kind, False) if block else None
            categories = {}
            for entry in doc.entries(rows) if rows else []:
                if entry.key is None or not isinstance(entry.value, native.Block) or entry.key in categories:
                    raise native.AuditError("unknown or duplicate native budget category")
                categories[entry.key] = resource_table(doc, entry.value)
            result[period][kind] = categories
    return result


def compact_jobs(doc, population, species):
    colonies = set(population["owned_colony_ids"])
    database = native.numeric_database(doc, doc.section(doc.root, "pop_jobs"), "pop jobs")
    groups = native.numeric_database(doc, doc.section(doc.root, "pop_groups"), "pop groups")
    result = []
    for index, block in database.items():
        colony = native.integer(doc.scalar(block, "planet"), "job colony")
        if colony not in colonies:
            continue
        row = {"id": index, "colony_id": colony, "type": doc.scalar(block, "type")}
        for field in ("workforce", "bonus_workforce", "automated_workforce", "max_workforce", "workforce_limit", "automated_workforce_limit"):
            value = doc.scalar(block, field, False)
            # A missing field is not silently interpreted as zero.
            row[field] = str(number(value, field)) if value is not None else None
        allocations = doc.section(block, "pop_groups", False)
        row["allocations"] = []
        for entry in doc.entries(allocations) if allocations else []:
            if entry.key is not None or not isinstance(entry.value, native.Block):
                raise native.AuditError("unknown job population allocation")
            group_id = native.integer(doc.scalar(entry.value, "pop_group"), "job pop group")
            group = native.required_record(groups, group_id, "job pop group")
            if native.integer(doc.scalar(group, "planet"), "job pop colony") != colony:
                raise native.AuditError("job allocation crosses colony")
            sid = native.integer(doc.scalar(doc.section(group, "key"), "species"), "job species")
            row["allocations"].append({"group_id": group_id, "species_id": sid,
                "category": doc.scalar(doc.section(group, "key"), "category", False),
                "amount": str(number(doc.scalar(entry.value, "amount"), "allocated workforce")),
                "base_traits": sorted(set(species[sid]["distinct_trait_keys"]) - set(TRAITS.values()))})
        result.append(row)
    return sorted(result, key=lambda r: (r["colony_id"], r["type"], r["id"]))


def economy_context(doc, actor, population, modifiers):
    """Observed finite context; does not pretend to solve every native modifier."""
    government = doc.section(actor, "government")
    tech = doc.section(actor, "tech_status", False)
    completed = [{"key": e.key, "value": doc.native(e.value)} for e in doc.entries(tech) if e.key in ("technology", "level")] if tech else None
    contexts = []
    colonies = native.numeric_database(doc, doc.section(doc.root, "colony"), "colony")
    planets = native.numeric_database(doc, doc.section(doc.section(doc.root, "planets"), "planet"), "planet")
    for link in population["ownership_links"]:
        colony = colonies[link["colony_id"]]
        planet = planets[link["carrier_reference"]]
        contexts.append({"colony_id": link["colony_id"],
            **{k: native_field(doc, colony, k) for k in ("stability", "final_designation", "ascension_tier", "buildings_cache", "districts", "binary_flags")},
            "deposits": native_field(doc, planet, "deposits"),
            "carrier_flags": native_field(doc, planet, "carrier_binary_flags")})
    situations = doc.section(doc.section(doc.root, "situations"), "situations")
    own_id, _, _ = native.locate_player(doc)
    own_situations = []
    for index, block in native.numeric_database(doc, situations, "situations").items():
        if native.integer(doc.scalar(block, "country"), "situation country") == own_id:
            own_situations.append({"id": index, **{k: native_field(doc, block, k) for k in ("type", "stage", "approach")}})
    fixed_modifiers = [{"modifier": m["modifier"], "multiplier": m["multiplier"]}
                       for m in modifiers if m["modifier"] not in (ARCH, COUNTER, OTHER)]
    leader_database = doc.section(doc.root, "leaders", False)
    leader_ids = doc.section(actor, "owned_leaders", False)
    leaders = None
    if leader_database is not None and leader_ids is not None:
        records = native.numeric_database(doc, leader_database, "leader")
        leaders = []
        for index in native.integer_list(doc, leader_ids, "owned leaders"):
            block = native.required_record(records, index, "owned leader")
            leaders.append({"id": index,
                **{key: native_field(doc, block, key) for key in ("class", "tier", "level", "bonus_skill_level", "job", "location", "council_location")},
                "traits": [doc.native(v) for v in doc.values(block, "traits")]})
    modules = doc.section(actor, "modules", False)
    economy = doc.section(modules, "standard_economy_module", False) if modules else None
    stocks = resource_table(doc, doc.section(economy, "resources", False)) if economy else None
    # Stockpiles may grow normally; only zero/negative availability is a guard.
    depleted = sorted(k for k, v in (stocks or {}).items() if number(v) <= 0)
    return {"government": [{"key": e.key, "value": doc.native(e.value)} for e in doc.entries(government) if e.key != "council_agenda_progress"],
            "completed_technologies": completed, "policies": native_field(doc, actor, "active_policies"),
            "ethos": native_field(doc, actor, "ethos"), "colonies": contexts,
            "situations": own_situations, "other_country_modifiers": fixed_modifiers,
            "owned_leader_economic_state": leaders, "depleted_resource_keys": depleted}


def extract_snapshot(path: Path):
    """One ZIP/Document lifetime per call; result has no parser block or text."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    with zipfile.ZipFile(path) as archive:
        if len(archive.namelist()) != len(set(archive.namelist())):
            raise native.AuditError("duplicate ZIP member")
        meta = native.Document(archive.read("meta").decode("utf-8-sig"))
        doc = native.Document(archive.read("gamestate").decode("utf-8-sig"))
    version, date = doc.scalar(doc.root, "version"), doc.scalar(doc.root, "date")
    if version != meta.scalar(meta.root, "version") or date != meta.scalar(meta.root, "date"):
        raise native.AuditError("meta/gamestate identity mismatch")
    actor_id, actor, _ = native.locate_player(doc)
    main, _ = native.locate_main_species(doc, actor)
    species = native.species_records(doc)
    population = native.inspect_populations(doc, actor, actor_id, species, main)
    variables_block = doc.section(actor, "variables", False)
    variables = {e.key: doc.native(e.value) for e in doc.entries(variables_block)
                 if e.key and (e.key.startswith("shishan_code_") or e.key.startswith("shishan_econ_probe_"))} if variables_block else {}
    flags = native.mod_fields(doc, doc.section(actor, "flags", False))
    modifiers = all_modifiers(doc, actor)
    native_mods = native.native_modifiers(doc, actor)
    expected, diagnostics = native.expected_and_observed(population, variables, flags, native_mods)
    comparisons = expected["comparisons"]
    strict = [issue("FAIL", "STRICT_CACHE_" + row["status"], key=key, observation=row)
              for key, row in comparisons.items() if row["status"] != "MATCH"]
    strict += [issue("FAIL", d["code"], native_diagnostic=d) for d in diagnostics if d["severity"] == "error" and d["code"] != "ARCHITECTURE_OBSERVATION_MISMATCH"]
    return {"save": str(path.resolve()), "sha256": digest.hexdigest(), "bytes": path.stat().st_size,
            "version": version, "date": date, "actor_id": actor_id,
            "origin": doc.scalar(doc.section(actor, "government"), "origin", False),
            "mods": native_field(meta, meta.root, "mods"),
            "population": population, "variables": variables, "modifiers": modifiers,
            "projects": native.native_projects(doc, actor),
            "strict_cache": {"status": status_of(strict), "checks": strict, "comparisons": comparisons},
            "jobs": compact_jobs(doc, population, species),
            "budget": budget_snapshot(doc, actor),
            "context": economy_context(doc, actor, population, modifiers)}


def source_profile(game_root: Path | None, mod_root: Path | None):
    """Resolve active job resource categories from declared game + isolated pack.

    This is a narrow source inspection, not an evaluator of all scripted native
    triggers. Unknown conditional/inline output is retained as NOT COVERED.
    """
    if game_root is None or mod_root is None:
        return {"status": "NOT COVERED", "reason": "sources.game_root and sources.mod_root are required"}
    definitions, files = {}, []
    for root in (game_root, mod_root):
        for path in sorted((root / "common/pop_jobs").glob("*.txt")):
            raw = path.read_bytes()
            doc = native.Document(raw.decode("utf-8-sig"))
            for entry in doc.entries():
                if entry.key and isinstance(entry.value, native.Block):
                    rows = []
                    for resources in doc.values(entry.value, "resources"):
                        if isinstance(resources, native.Block):
                            rows.append({"category": doc.scalar(resources, "category", False),
                                         "raw": doc.native(resources)})
                    definitions[entry.key] = rows
            files.append({"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest()})
    categories = sorted(k for k, rows in definitions.items() if any(r["category"] == "planet_biologists" for r in rows))
    expected_maintainer = [{"key": "category", "value": "planet_biologists"},
        {"key": "produces", "value": [{"key": "society_research", "value": "3"}, {"key": "unity", "value": "1"}]},
        {"key": "upkeep", "value": [{"key": "consumer_goods", "value": "1.5"}]},
        {"key": "inline_script", "value": "output/researcher_output"}]
    maintainer = definitions.get("shishan_code_maintainer", [])
    biologist = definitions.get("biologist", [])
    researcher_inline = []
    for root in (game_root, mod_root):
        path = root / "common/inline_scripts/output/researcher_output.txt"
        if path.is_file():
            raw = path.read_bytes()
            researcher_inline = native.Document(raw.decode("utf-8-sig")).entries()
            files.append({"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest()})
    unity_safe = (len(maintainer) == 1 and maintainer[0]["raw"] == expected_maintainer and
                  len(biologist) == 1 and biologist[0]["category"] == "planet_biologists" and not researcher_inline)
    if unity_safe:
        # Every direct/conditional produces block must contain only society.
        for entry in biologist[0]["raw"]:
            if entry["key"] == "produces":
                if any(row["key"] not in ("society_research", "trigger") for row in entry["value"]):
                    unity_safe = False
            elif entry["key"] not in ("category", "upkeep", "inline_script"):
                unity_safe = False
        inline = [e["value"] for e in biologist[0]["raw"] if e["key"] == "inline_script"]
        unity_safe = unity_safe and inline == ["output/researcher_output"]
    return {"status": "PASS" if unity_safe else "NOT COVERED", "unity_source_isolated": unity_safe,
            "planet_biologists_job_types": categories, "files": files,
            "permitted_base_trait_keys": FINITE_BASE_TRAITS,
            "scope": "declared isolated game+pack job resource tables; unknown additional loaded Mods or dynamic resource-add channels require independent source review",
            "society_source_status": "CONDITIONAL: Q derived from same four-grid; combined workforce; zookeeper/other source drift invalidates interpretation"}


def date_tuple(date):
    match = re.fullmatch(r"(\d+)\.(\d{2})\.(\d{2})", date)
    if not match:
        raise native.AuditError(f"unrecognized native date {date!r}")
    year, month, day = map(int, match.groups())
    if not 1 <= month <= 12 or not 1 <= day <= 30:
        raise native.AuditError(f"unsupported native date {date!r}")
    return year * 360 + (month - 1) * 30 + day - 1


def observed_modifier(snapshot, name):
    return [m for m in snapshot["modifiers"] if m["modifier"] == name]


def employment_signature(snapshot):
    rows = []
    for job in snapshot["jobs"]:
        # IDs can change after clone/merge; workload and contributing traits cannot.
        row = {k: job[k] for k in ("colony_id", "type", "workforce", "bonus_workforce", "automated_workforce", "max_workforce", "workforce_limit", "automated_workforce_limit")}
        allocation_totals = {}
        for allocation in job["allocations"]:
            key = (allocation["category"], tuple(allocation["base_traits"]))
            allocation_totals[key] = allocation_totals.get(key, D(0)) + number(allocation["amount"])
        row["allocations"] = sorted(({"category": key[0], "base_traits": list(key[1]), "amount": str(amount)}
                                     for key, amount in allocation_totals.items()), key=lambda r: json.dumps(r, sort_keys=True))
        rows.append(row)
    return rows


def effective_workforce(snapshot, types):
    return sum((number(j["workforce"]) + number(j["bonus_workforce"]) for j in snapshot["jobs"] if j["type"] in types), D(0)) / 100


def core_guards(branch, phase, snapshot):
    result = []
    expected_u = D(8 if branch in TRAITS else 7)
    pop, variables = snapshot["population"], snapshot["variables"]
    wanted_dummy = {TRAITS[branch]} if branch in TRAITS else set()
    for template in pop["populated_templates"]:
        actual = set(template["distinct_trait_keys"])
        if actual & set(TRAITS.values()) != wanted_dummy or template["distinct_trait_count"] != expected_u or template["duplicate_trait_keys"]:
            result.append(issue("FAIL", "ACTUAL_TEMPLATE_INPUT", species_id=template["id"], traits=sorted(actual), expected_dummy=sorted(wanted_dummy)))
    if pop["population"] <= 0 or not close(pop["trait_average_decimal"], expected_u):
        result.append(issue("FAIL", "ACTUAL_U", observed=pop["trait_average_decimal"], expected=str(expected_u)))
    targets = {PREFIX + "repeat_count": D(0), PREFIX + "trait_average": expected_u,
               PREFIX + "total": expected_u, PREFIX + "bonus": expected_u * D(".05"),
               PREFIX + "multiplier": 1 + expected_u * D(".05"), "shishan_code_maintenance_count": D(1)}
    if snapshot["origin"] != "origin_shishan_code":
        result.append(issue("INVALID", "WRONG_ORIGIN"))
    if "v4.5.2" not in snapshot["version"]:
        result.append(issue("NOT COVERED", "UNREVIEWED_NATIVE_VERSION", observed=snapshot["version"]))
    if not isinstance(snapshot["mods"], list) or len(snapshot["mods"]) != 1:
        result.append(issue("NOT COVERED", "UNREVIEWED_LOADED_MOD_SET", observed=snapshot["mods"]))
    for key, target in targets.items():
        raw = variables.get(key)
        if raw is None or not close(raw, target):
            result.append(issue("FAIL", "CORE_VARIABLE", key=key, observed=raw, expected=str(target)))
    for name, count, multiplier in ((ARCH, 1, expected_u), (COUNTER, int(branch in ("F00", "F10")), expected_u), (OTHER, int(branch in ("F10", "F11", "FP", "FN", "FH")), D(1))):
        rows = observed_modifier(snapshot, name)
        if len(rows) != count or (rows and (not close(rows[0]["multiplier"], multiplier) or rows[0]["days"] != "-1")):
            result.append(issue("FAIL", "CONTROL_MODIFIER", modifier=name, observed=rows, expected_count=count, expected_multiplier=str(multiplier)))
    if branch in ("F00", "F10"):
        raw = variables.get("shishan_econ_probe_counter_t")
        if raw is None or not close(raw, expected_u):
            result.append(issue("FAIL", "COUNTER_T", observed=raw, expected=str(expected_u)))
    # P/W stale caches are deliberately NOT a guard on fixed-U differences.
    for key, row in snapshot["strict_cache"]["comparisons"].items():
        if key not in (PREFIX + "population", PREFIX + "trait_weight") and row["status"] != "MATCH":
            result.append(issue("FAIL", "CORE_CACHE", key=key, observed=row))
    if any(p["status"] == "active" for p in snapshot["projects"]):
        result.append(issue("INVALID", "ACTIVE_PROJECT_DURING_MEASUREMENT"))
    measured_jobs = [j for j in snapshot["jobs"] if j["type"] in JOBS]
    if not measured_jobs or any(j[k] is None for j in measured_jobs for k in ("workforce", "bonus_workforce", "automated_workforce", "max_workforce", "workforce_limit", "automated_workforce_limit")):
        result.append(issue("NOT COVERED", "MISSING_JOB_FIELDS"))
    else:
        actual_j = sum((number(j["workforce"]) for j in measured_jobs if j["type"] == "shishan_code_maintainer"), D(0))
        if not close(actual_j, 100):
            result.append(issue("INVALID", "ACTUAL_J_NOT_100", observed=str(actual_j)))
        if any(number(j["automated_workforce"]) != 0 for j in measured_jobs):
            result.append(issue("NOT COVERED", "AUTOMATED_WORKFORCE_UNRESOLVED"))
        if effective_workforce(snapshot, ("shishan_code_maintainer",)) <= 0:
            result.append(issue("INVALID", "NO_EFFECTIVE_MAINTAINERS"))
        for j in measured_jobs:
            if not close(sum((number(a["amount"]) for a in j["allocations"]), D(0)), j["workforce"]):
                result.append(issue("INVALID", "JOB_ALLOCATION_MISMATCH", job=j["id"]))
    return [{"branch": branch, "phase": phase, **row} for row in result]


def comparison(code, observed, expected):
    return issue("PASS" if close(observed, expected) else "FAIL", code,
                 observed=str(observed), expected=str(expected), epsilon=str(epsilon(observed, expected)))


def resource_matrix(snapshots, resource, types):
    normalized = {}
    for branch in BRANCHES:
        snapshot = snapshots[branch]["measured"]
        value = snapshot["budget"]["last_month"]["income"].get("planet_biologists", {}).get(resource)
        weight = effective_workforce(snapshot, types)
        if value is None or number(value) <= 0 or weight <= 0:
            return {"status": "NOT COVERED", "checks": [issue("NOT COVERED", "RESOURCE_SOURCE_MISSING_OR_ZERO", branch=branch, resource=resource)]}
        normalized[branch] = number(value) / weight
    y = normalized
    q0, q1 = (y["F10"] - y["F00"]) / D(".4"), (y["F11"] - y["F01"]) / D(".4")
    checks = [comparison("A40_RESPONSE_EQUAL", q1, q0)]
    if q0 <= epsilon(q0) or q1 <= epsilon(q1):
        checks.append(issue("INVALID", "NONPOSITIVE_A40_RESPONSE", q0=str(q0), q1=str(q1)))
    checks += [comparison("ARCHITECTURE_AT_A0", y["F01"] - y["F00"], D(".35") * q0),
               comparison("ARCHITECTURE_AT_A40", y["F11"] - y["F10"], D(".35") * q0),
               comparison("INTERACTION", (y["F11"] - y["F10"]) - (y["F01"] - y["F00"]), 0)]
    checks += [comparison("DUMMY_INCREMENT_" + b, y[b] - y["F11"], D(".05") * q0) for b in TRAITS]
    return {"status": status_of(checks), "resource": resource, "normalized": {k: str(v) for k, v in y.items()},
            "Q0": str(q0), "Q1": str(q1), "checks": checks,
            "denominator": "sum(actual workforce + bonus_workforce)/100 for " + ",".join(types)}


def negative_controls(snapshots):
    base = snapshots["F11"]["measured"]
    maintenance = base["budget"]["last_month"]["expenses"].get("planet_biologists")
    country = base["budget"]["last_month"]["income"].get("country_base")
    checks = []
    if not maintenance or not any(number(v) > 0 for v in maintenance.values()):
        checks.append(issue("NOT COVERED", "MAINTENANCE_SOURCE_MISSING_OR_ZERO"))
    else:
        for branch in BRANCHES:
            current = snapshots[branch]["measured"]
            expenses = current["budget"]["last_month"]["expenses"].get("planet_biologists")
            if expenses is None or expenses.keys() != maintenance.keys():
                checks.append(issue("NOT COVERED", "MAINTENANCE_SOURCE_SHAPE", branch=branch))
                continue
            for resource, value in maintenance.items():
                checks.append(comparison("MAINTENANCE_" + branch + "_" + resource,
                    number(expenses[resource]) / effective_workforce(current, JOBS), number(value) / effective_workforce(base, JOBS)))
    if not country or not any(number(v) != 0 for v in country.values()):
        checks.append(issue("NOT COVERED", "COUNTRY_BASE_MISSING_OR_ZERO"))
    else:
        for branch in BRANCHES:
            table = snapshots[branch]["measured"]["budget"]["last_month"]["income"].get("country_base")
            if table is None or table.keys() != country.keys():
                checks.append(issue("NOT COVERED", "COUNTRY_BASE_SOURCE_SHAPE", branch=branch))
                continue
            for resource, value in country.items():
                if number(value) == 0:
                    checks.append(issue("NOT COVERED", "ZERO_COUNTRY_BASE_RESOURCE", resource=resource))
                else:
                    checks.append(comparison("COUNTRY_BASE_" + branch + "_" + resource, table[resource], value))
    return {"status": status_of(checks), "checks": checks,
            "foreign_economy": {"status": "NOT COVERED", "reason": "no independently fixed foreign job/budget window in this finite domestic matrix"},
            "station_deposit_building_income": {"status": "NOT COVERED", "reason": "country_base only; these sources need their own stable source/workforce audit"}}


def audit_matrix(snapshots, profile):
    guards, strict, timing = [], [], []
    reference = snapshots["F00"]
    ref_measured = reference["measured"]
    baseline_templates = sorted({tuple(sorted(set(t["distinct_trait_keys"]) - set(TRAITS.values())))
                                 for t in ref_measured["population"]["populated_templates"]})
    for branch in BRANCHES:
        rows = snapshots[branch]
        for phase in PHASES:
            snap = rows[phase]
            guards += core_guards(branch, phase, snap)
            actual_base = sorted({tuple(sorted(set(t["distinct_trait_keys"]) - set(TRAITS.values())))
                                  for t in snap["population"]["populated_templates"]})
            if actual_base != baseline_templates:
                guards.append(issue("INVALID", "BASE_TEMPLATE_TRAITS_CHANGED", branch=branch, phase=phase))
            strict += [{"branch": branch, "phase": phase, **i} for i in snap["strict_cache"]["checks"]]
            if snap["version"] != ref_measured["version"] or snap["actor_id"] != ref_measured["actor_id"] or snap["mods"] != ref_measured["mods"]:
                guards.append(issue("INVALID", "NATIVE_IDENTITY_CHANGED", branch=branch, phase=phase))
            if snap["date"] != reference[phase]["date"]:
                timing.append(issue("INVALID", "BRANCH_CALENDAR_MISMATCH", branch=branch, phase=phase, observed=snap["date"], reference=reference[phase]["date"]))
            if not equivalent(employment_signature(snap), employment_signature(ref_measured)):
                guards.append(issue("INVALID", "EMPLOYMENT_OR_CAPACITY_CHANGED", branch=branch, phase=phase))
            # Warmup may settle a common transient before the complete measured
            # month. Input contexts must match one another, then warm/measured
            # contexts must remain stable throughout the measurement window.
            context_reference = reference["input"] if phase == "input" else ref_measured
            if not equivalent(snap["context"], context_reference["context"]):
                guards.append(issue("INVALID", "ECONOMIC_CONTEXT_CHANGED", branch=branch, phase=phase))
        start, warm, end = (date_tuple(rows[p]["date"]) for p in PHASES)
        # At least one entire native 30-day month after warm, with common day.
        if not start < warm < end or warm // 30 + 1 != end // 30 or warm % 30 != end % 30:
            timing.append(issue("INVALID", "INSUFFICIENT_OR_AMBIGUOUS_FULL_MONTH", branch=branch))
        if warm % 30 > 2:
            timing.append(issue("INVALID", "WARM_NOT_AT_MEASUREMENT_MONTH_START", branch=branch, day=warm % 30 + 1))
        if start // 30 >= warm // 30:
            timing.append(issue("INVALID", "NO_PRECEDING_WARMUP_MONTH", branch=branch))
        for phase in ("warm", "measured"):
            for modifier in rows[phase]["modifiers"]:
                days = modifier["days"]
                if days is not None and number(days) >= 0 and number(days) <= 30:
                    guards.append(issue("INVALID", "EXPIRING_COUNTRY_MODIFIER", branch=branch, phase=phase, modifier=modifier))
    guards += timing
    known = set(profile.get("planet_biologists_job_types", []))
    active = {j["type"] for j in ref_measured["jobs"] if j["workforce"] is not None and number(j["workforce"]) > 0}
    unisolated = sorted((known & active) - set(JOBS))
    if profile.get("status") != "PASS" or unisolated:
        guards.append(issue("NOT COVERED", "UNITY_SOURCE_NOT_ISOLATED", source_profile_status=profile.get("status"), other_category_jobs=unisolated))
    permitted = profile.get("permitted_base_trait_keys")
    if permitted is not None:
        for branch in BRANCHES:
            for phase in PHASES:
                templates = snapshots[branch][phase]["population"]["populated_templates"]
                if any(sorted(set(t["distinct_trait_keys"]) - set(TRAITS.values())) != permitted for t in templates):
                    guards.append(issue("NOT COVERED", "UNREVIEWED_MAIN_TEMPLATE_TRAIT_INPUT", branch=branch, phase=phase))
                for job in snapshots[branch][phase]["jobs"]:
                    if job["type"] in JOBS:
                        for allocation in job["allocations"]:
                            if number(allocation["amount"]) > 0 and allocation["base_traits"] != permitted:
                                guards.append(issue("NOT COVERED", "UNREVIEWED_CATEGORY_TRAIT_INPUT", branch=branch, phase=phase, job=job["id"], observed=allocation["base_traits"]))
    def attempt(call):
        try:
            return call()
        except native.AuditError as error:
            return {"status": "NOT COVERED", "checks": [issue("NOT COVERED", "RESOURCE_DENOMINATOR_UNAVAILABLE", message=str(error))]}
    unity = attempt(lambda: resource_matrix(snapshots, "unity", ("shishan_code_maintainer",)))
    society = attempt(lambda: resource_matrix(snapshots, "society_research", JOBS))
    controls = attempt(lambda: negative_controls(snapshots))
    guarded_status = status_of(guards)
    limited_checks = guards + unity["checks"] + controls["checks"]
    limited_status = status_of(limited_checks)
    for result in (unity, society, controls):
        result["arithmetic_status"] = result["status"]
        if guarded_status != "PASS":
            result["status"] = guarded_status
            result["interpretation"] = "arithmetic retained; sample guards do not permit acceptance"
    strict_status = status_of(strict)
    final = status_of([issue(limited_status, "LIMITED_ECONOMY"), issue(strict_status, "STRICT_CACHE")])
    return {"status": final, "strict_cache_audit": {"status": strict_status, "checks": strict},
            "limited_economy": {"status": limited_status, "guards": guards, "unity": unity, "society_secondary": society, "negative_controls": controls},
            "source_profile": profile,
            "scope": "native finite additive response; fixed U7/U8, R0, n1, J100, no automated workforce; endpoint stability does not prove all intervening native ticks",
            "epsilon_rule": "max(0.0001,0.000001*max(abs(compared values)))"}


def audit_manifest(path: Path, loader=extract_snapshot):
    base = {"manifest": str(path.resolve()), "status": "NOT RUN", "native_execution": "NOT RUN", "snapshots": {}}
    if not path.is_file():
        return {**base, "diagnostics": [issue("NOT RUN", "MANIFEST_MISSING")]}
    raw = path.read_bytes()
    base["manifest_sha256"] = hashlib.sha256(raw).hexdigest()
    try:
        manifest = json.loads(raw)
        if not isinstance(manifest, dict):
            raise native.AuditError("manifest must be an object")
        mapping = manifest.get("branches", manifest)
        if not isinstance(mapping, dict):
            raise native.AuditError("branches must be an object")
        missing = []
        paths = {}
        for branch in BRANCHES:
            paths[branch] = {}
            if branch in mapping and not isinstance(mapping[branch], dict):
                raise native.AuditError(f"branch {branch} must map input/warm/measured")
            for phase in PHASES:
                value = mapping.get(branch, {}).get(phase)
                target = Path(value) if isinstance(value, str) and value else None
                if target is not None and not target.is_absolute():
                    target = path.parent / target
                if target is None or not target.is_file():
                    missing.append(issue("NOT RUN", "SNAPSHOT_MISSING", branch=branch, phase=phase, path=str(target) if target else None))
                else:
                    paths[branch][phase] = target
        if missing:
            return {**base, "diagnostics": missing}
        snapshots = {}
        base["native_execution"] = "ATTEMPTED NATIVE SAVE READ; no game launch"
        # Never parallelize these reads: extract_snapshot owns the only full
        # gamestate Document, and releases it before the next loader call.
        for branch in BRANCHES:
            snapshots[branch] = {}
            for phase in PHASES:
                snapshots[branch][phase] = loader(paths[branch][phase])
        source_args = manifest.get("sources", {})
        if not isinstance(source_args, dict):
            raise native.AuditError("sources must be an object")
        roots = []
        for key in ("game_root", "mod_root"):
            value = source_args.get(key)
            target = Path(value) if value else None
            roots.append((path.parent / target).resolve() if target and not target.is_absolute() else target)
        result = audit_matrix(snapshots, source_profile(*roots))
        return {**base, **result, "native_execution": "READ NATIVE SAVES; no game launch or UI certification", "snapshots": snapshots}
    except (native.AuditError, OSError, zipfile.BadZipFile, KeyError, TypeError, ValueError) as error:
        return {**base, "status": "INVALID", "diagnostics": [issue("INVALID", "MATRIX_UNINTERPRETABLE", message=str(error))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = audit_manifest(args.manifest)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status": result["status"], "native_execution": result["native_execution"], "report": str(args.report) if args.report else None}, ensure_ascii=False) if args.report else rendered, end="\n" if args.report else "")
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
