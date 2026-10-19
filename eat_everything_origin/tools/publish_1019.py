"""0.4.0 adapter. No PASS evidence is synthesized by this release gate."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import math
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

import publish_update as update

ROOT = update.ROOT
VERSION = "0.4.0"
EVIDENCE = ROOT / "docs/evidence/publication-0.4.0"
RUNTIME = ROOT / "docs/evidence/1019-requirements/final-result.json"
PROFILE = "eep-0.4.0-single-production-mod"
ENABLED_MODS = ["mod/ugc_eep-1019.mod"]
LANGUAGES = {"braz_por", "english", "french", "german", "japanese", "korean",
             "polish", "russian", "simp_chinese", "spanish"}
EVIDENCE_KINDS = {"native_save", "screenshot", "actions", "log", "analysis"}
STARTUP_CHECKS = {"single_homeworld", "correct_homeworld_type", "initial_energy_200", "first_month_generator_jobs",
                  "auto_devour_off", "population_preserved", "normal_upkeep"}
ECONOMY_CHECKS = {"baseline_12_months", "candidate_12_months", "all_net_energy_nonnegative",
                  "no_resource_injection", "no_trade_subsidy", "no_job_closure", "no_ship_disband"}
CASE_CHECKS = {
    **{f"{branch}_startup": STARTUP_CHECKS for branch in ("hive", "machine", "purifier")},
    **{f"{branch}_economy": ECONOMY_CHECKS for branch in ("hive", "machine", "purifier")},
    "lithoid_hive_first_month": STARTUP_CHECKS | {"first_month_energy_nonnegative"},
    "mothership_configuration": {"same_country_same_date_relic_reference", "native_design_matches",
        "power_nonnegative", "upkeep_observed", "actual_jump", "ten_mobile_shipyards",
        "no_empire_technology_grant", "other_juggernauts_unchanged", "twenty_two_large_defense_slots",
        "five_relic_auxiliary_components_preserved", "reference_stats_observed", "existing_advantages_preserved"},
    "unlimited_growth": {"count_level_samples", "four_stats_five_percent_per_level", "daily_regeneration",
        "single_scaled_modifier", "repeated_sync_idempotent", "same_day_reload_idempotent",
        "destroyed_mother_not_respawned", "jump_and_shipyards_preserved", "report_level_count_remainder",
        "invalid_or_cancelled_no_growth"},
    "colossus_enemy_fire": {"native_charge_and_fire", "enemy_colony_destroyed", "war_target",
        "no_army", "beneficiary_is_core_owner", "owned_noncore_colony_fire"},
    "colossus_guards": {"uncolonized_rejected", "artificial_rejected", "all_core_worlds_rejected",
        "colonizing_rejected", "ground_combat_rejected", "devouring_rejected", "neutral_friendly_rejected",
        "settled_rejected", "completion_revalidates_target", "completion_revalidates_core_owner"},
    "colossus_cancel_idempotence": {"queue_no_reward", "cancel_no_reward", "repeat_event_no_reward",
        "reload_no_reward", "crisis_objective_once"},
    "common_settlement": {"q_c_g_d_match", "native_devour_loss_deducted", "population_matches",
        "core_capacity_matches", "owned_main_species_return", "enemy_population_not_returned",
        "lithoid_native_branch", "settlement_and_destruction_once"},
    "normal_dismantle_regression": {"normal_duration_preserved", "normal_seed_preserved",
        "normal_completion", "normal_reload_idempotent"},
    "old_save_migration": {"original_031_save", "extra_world_preserved", "no_startup_reward",
        "native_design_migration", "identity_preserved", "name_preserved", "position_preserved",
        "queue_preserved", "damage_preserved", "migration_once", "layout_preserved", "civilian_queue_preserved"},
    "candidate_reload": {"native_restart", "native_reload", "ledger_preserved", "no_duplicate_reward"},
    "repeat_initialization": {"no_extra_world", "no_extra_ship", "no_extra_reward", "no_extra_civilian_queue"},
}
COMPONENT_CHECKS = {"real_component", "positive_effect_observed", "random_pool",
                    "every_five_levels", "threshold_idempotent", "reload_persistent",
                    "other_fleets_unchanged", "equipped_component_present_in_native_design",
                    "component_owns_dynamic_bonus", "no_external_reward_modifier",
                    "native_component_effects_source_attributed", "growth_component_contributions_separated",
                    "cross_threshold_catchup"}
COMPONENT_KINDS = ("shield", "armor", "hull", "damage", "tracking", "regen")
COMPONENT_MODIFIERS = {"ship_hull_add", "ship_hull_mult", "ship_armor_add", "ship_armor_mult",
                       "ship_shield_add", "ship_shield_mult", "ship_weapon_damage", "ship_tracking_add",
                       "ship_hull_regen_add_static", "ship_armor_regen_add_static"}
# Expectations were fixed before the RC4 RNG observations; they are source
# models, not inherited RC3 runtime acceptance or fitted future coefficients.
COMPONENT_SOURCE_MODELS = (
    "bd3b4d48eeb5de98b34a8ba104f55c23f17cb43a723a216934f2c2a1c4a2099f",
    "a191eea40464ef3fde5f7ec64f33ac2d7012ef74d6b6cdea900d441a16371bc8")
COMPONENT_ATTRIBUTION_CONTRACT = "source_separated_native_rng_v1"
GROWTH_SAMPLES = [(0, 0), (9, 0), (10, 1), (19, 1), (20, 2), (200, 20), (10000, 1000)]
COMPONENT_NODES = (0, 9, 10, 19, 20, 49, 50, 200, 10000)
PLANET_KILLER_CALLBACK_CONTRACT = "native_completed_queued_unqueued_v1"
PLANET_KILLER_NUMERIC_CONTRACT = "native_csv_or_literal_txt_v1"
WEAPON_CSV_LOADER_CONTRACT = "native_fixed_paths_v1"
WEAPON_CSV_PATHS = {"common/component_templates/weapon_components.csv",
                    "common/component_templates/mutation_weapon_components.csv"}
PLANET_KILLER_NUMERIC_FIELDS = {"windup_min", "windup_max", "total_fire_time", "power"}
DECLARATION_TOKEN = re.compile(r'#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}=]|[^\s{}="#]+')


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def project_evidence_path(name, root):
    """Resolve a portable project-relative path before reading any bytes."""
    if not isinstance(name, str):
        raise RuntimeError("evidence path missing")
    relative = PurePosixPath(name)
    if (not name or "\\" in name or relative.is_absolute() or PureWindowsPath(name).drive
            or ".." in relative.parts):
        raise RuntimeError("evidence must use a project-relative path")
    try:
        path = (root / Path(name)).resolve(strict=True)
        path.relative_to(root.resolve())
    except (ValueError, OSError) as error:
        raise RuntimeError("evidence outside project or missing: " + name) from error
    if not path.is_file():
        raise RuntimeError("evidence file missing: " + name)
    return path


def reference_path(entry, root):
    """Accept portable project-relative references, including on Windows hosts."""
    if (not isinstance(entry, dict) or not isinstance(entry.get("sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", entry["sha256"])):
        raise RuntimeError("evidence SHA256 missing")
    path = project_evidence_path(entry.get("path"), root)
    if update.digest(path.read_bytes()) != entry["sha256"]:
        name = entry["path"]
        raise RuntimeError("evidence changed: " + name)
    return path


def verify_references(entries, root, required_kinds=None):
    if not isinstance(entries, list) or not entries:
        raise RuntimeError("evidence references missing")
    paths = [reference_path(entry, root) for entry in entries]
    if len(paths) != len(set(paths)):
        raise RuntimeError("duplicate evidence references")
    if required_kinds and not required_kinds.issubset({entry.get("kind") for entry in entries}):
        raise RuntimeError("native save, screenshot, actions, log and analysis evidence required")
    return paths


def candidate_version(runtime):
    version = runtime.get("version", "")
    if not re.fullmatch(r"0\.4\.0-rc\.[1-9]\d*", version):
        raise RuntimeError("matching 0.4.0 release candidate required")
    return version


def candidate_descriptor(runtime):
    version = candidate_version(runtime)
    descriptor = runtime.get("candidate_descriptor")
    if not isinstance(descriptor, str):
        raise RuntimeError("candidate descriptor bytes missing")
    raw = descriptor.encode("utf-8")
    marker = f'version="{version}"'.encode()
    if (len(re.findall(rb'(?m)^version="[^"\r\n]+"\r?$', raw)) != 1
            or raw.count(marker) != 1 or b"remote_file_id" in raw
            or str(update.base.FORBIDDEN_ID).encode() in raw):
        raise RuntimeError("candidate descriptor version or upstream identity differs")
    return raw


def candidate_files(runtime):
    files = runtime.get("production_files")
    if not isinstance(files, dict) or "descriptor.mod" not in files:
        raise RuntimeError("candidate production manifest missing")
    for name, value in files.items():
        relative = PurePosixPath(name)
        if (not name or "\\" in name or relative.is_absolute() or ".." in relative.parts
                or PureWindowsPath(name).drive or not re.fullmatch(r"[0-9a-f]{64}", value)):
            raise RuntimeError("candidate production manifest malformed")
        if "eep_probe" in name or name.startswith("testing/"):
            raise RuntimeError("test fixture in production candidate")
    if update.digest(candidate_descriptor(runtime)) != files["descriptor.mod"]:
        raise RuntimeError("candidate descriptor hash differs")
    return files


def validate_candidate_files(files, runtime):
    candidate = candidate_files(runtime)
    descriptor = candidate_descriptor(runtime)
    normalized = {**candidate, "descriptor.mod": update.digest(descriptor.replace(
        f'version="{candidate_version(runtime)}"'.encode(), f'version="{VERSION}"'.encode(), 1))}
    if files != normalized:
        raise RuntimeError("formal content differs from tested candidate beyond descriptor version")


def candidate_tree(runtime, root):
    """Match stellaris_acceptance.tree_manifest's path-NUL-raw-bytes digest."""
    files = candidate_files(runtime)
    current = update.base.manifest(root / "mod")
    if current != files:
        validate_candidate_files(current, runtime)
    digest = hashlib.sha256()
    # Path ordering matches sorted(Path) in the Windows runtime harness.
    for path in sorted((root / "mod" / name) for name in files):
        name = path.relative_to(root / "mod").as_posix()
        raw = candidate_descriptor(runtime) if name == "descriptor.mod" else path.read_bytes()
        digest.update(name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
    return digest.hexdigest()


def declaration_literal(token):
    if token.startswith('"') and token.endswith('"') and "\\" not in token:
        return token[1:-1]
    if not token or '"' in token or token.startswith("@") or token in {"{", "}", "="}:
        return None
    return token


def root_declaration_blocks(path):
    """Project literal root declarations; Kaishek remains the mandatory P parser."""
    text = path.read_text(encoding="utf-8-sig")
    tokens = [match[0] for match in DECLARATION_TOKEN.finditer(text) if not match[0].startswith("#")]
    depth, start, name = 0, None, None
    for index, token in enumerate(tokens):
        if token == "{":
            if depth == 0 and index >= 2 and tokens[index - 1] == "=":
                name, start = declaration_literal(tokens[index - 2]), index + 1
            depth += 1
        elif token == "}":
            depth -= 1
            if depth == 0 and start is not None:
                yield name, tokens[start:index]
                name, start = None, None


def planet_killer_component_sources(component_root):
    keys = {}
    for path in component_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() != ".txt":
            continue
        for name, tokens in root_declaration_blocks(path):
            if name != "weapon_component_template":
                continue
            fields, depth = {"key": [], "type": []}, 0
            for index, token in enumerate(tokens):
                if token == "{":
                    depth += 1
                elif token == "}":
                    depth -= 1
                elif depth == 0 and token in fields and tokens[index + 1:index + 2] == ["="]:
                    fields[token].append(declaration_literal(tokens[index + 2]) if index + 2 < len(tokens) else None)
            if "planet_killer" in fields["type"]:
                if fields["type"] != ["planet_killer"] or len(fields["key"]) != 1 or not fields["key"][0]:
                    raise RuntimeError("literal planet-killer component key/type required")
                key = fields["key"][0]
                if key in keys:
                    raise RuntimeError("duplicate planet-killer component key")
                keys[key] = path
    return keys


def planet_killer_component_keys(component_root):
    return set(planet_killer_component_sources(component_root))


def validate_planet_killer_numeric_contract(report, mod, components):
    count = len(components)
    applicability = "checked" if count else "not_applicable_no_planet_killer_components"
    if (report.get("planet_killer_numeric_contract") != PLANET_KILLER_NUMERIC_CONTRACT
            or any(type(report.get(field)) is not int for field in (
                "planet_killer_numeric_components", "planet_killer_numeric_resolved"))
            or report.get("planet_killer_numeric_components") != count
            or report.get("planet_killer_numeric_resolved") != count
            or report.get("planet_killer_components") != count
            or report.get("planet_killer_numeric_applicability") != applicability):
        raise RuntimeError("matching checked planet-killer numeric loading contract required")
    sources = report.get("planet_killer_numeric_sources")
    if not isinstance(sources, list) or len(sources) != count:
        raise RuntimeError("planet-killer numeric sources must cover the actual component keys")
    seen = set()
    for row in sources:
        if (not isinstance(row, dict) or not isinstance(row.get("key"), str)
                or row.get("key") not in components or row["key"] in seen
                or not isinstance(row.get("kind"), str)
                or row.get("kind") not in {"literal_component_txt", "native_fixed_csv", "mod_fixed_csv"}
                or type(row.get("line")) is not int or row["line"] < 1
                or not isinstance(row.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", row["sha256"])
                or not isinstance(row.get("path"), str) or not Path(row["path"]).is_absolute()):
            raise RuntimeError("planet-killer numeric source identity malformed")
        values = row.get("values")
        if (not isinstance(values, dict) or set(values) != PLANET_KILLER_NUMERIC_FIELDS
                or any(type(value) not in (int, float) or not math.isfinite(value) for value in values.values())
                or any(values[key] < 0 for key in PLANET_KILLER_NUMERIC_FIELDS - {"power"})):
            raise RuntimeError("four finite literal planet-killer numeric values required")
        source = Path(row["path"])
        if row["kind"] == "literal_component_txt":
            actual = components[row["key"]]
            relative = actual.relative_to(mod)
            if source.parts[-len(relative.parts):] != relative.parts:
                raise RuntimeError("planet-killer TXT source path differs from its declaration")
        else:
            matches = [Path(name) for name in WEAPON_CSV_PATHS
                       if source.parts[-len(Path(name).parts):] == Path(name).parts]
            if len(matches) != 1:
                raise RuntimeError("planet-killer numeric CSV source uses an unsupported loader path")
            actual = mod / matches[0] if row["kind"] == "mod_fixed_csv" else source
        if not actual.is_file() or update.digest(actual.read_bytes()) != row["sha256"]:
            raise RuntimeError("planet-killer numeric source bytes differ from the checked source")
        seen.add(row["key"])
    if seen != set(components):
        raise RuntimeError("planet-killer numeric sources must cover the actual component keys")


def validate_planet_killer_contract(report, mod):
    components = planet_killer_component_sources(mod / "common/component_templates")
    expected = len(components) * 3
    if (not components or report.get("planet_killer_callback_contract") != PLANET_KILLER_CALLBACK_CONTRACT
            or any(type(report.get(field)) is not int for field in (
                "planet_killer_components", "planet_killer_callbacks_required", "planet_killer_callbacks_resolved"))
            or report.get("planet_killer_components") != len(components)
            or report.get("planet_killer_callbacks_required") != expected
            or report.get("planet_killer_callbacks_resolved") != expected
            or report.get("planet_killer_callback_applicability") != "checked"):
        raise RuntimeError("matching checked native planet-killer callback contract required")
    defined = set()
    for path in (mod / "common/on_actions").rglob("*"):
        if path.is_file() and path.suffix.lower() == ".txt":
            defined.update(name for name, _ in root_declaration_blocks(path))
    required = {f"on_destroy_planet_with_{key}{suffix}" for key in components for suffix in ("", "_queued", "_unqueued")}
    if not required.issubset(defined):
        raise RuntimeError("native planet-killer callback definitions missing from package: " + ", ".join(sorted(required - defined)))
    validate_planet_killer_numeric_contract(report, mod, components)


def validate_weapon_csv_contract(report, mod):
    component_root = mod / "common/component_templates"
    tables = sorted(path for path in component_root.rglob("*") if path.is_file() and path.suffix.lower() == ".csv")
    unsupported = [path for path in tables if path.relative_to(mod).as_posix() not in WEAPON_CSV_PATHS]
    if (report.get("weapon_csv_loader_contract") != WEAPON_CSV_LOADER_CONTRACT
            or type(report.get("weapon_csv_unsupported_files")) is not int
            or report.get("weapon_csv_unsupported_files") != len(unsupported) or unsupported):
        raise RuntimeError("matching supported native weapon CSV loader contract required")
    weapon_keys = []
    for table in tables:
        rows = [line.split(";") for line in table.read_text(encoding="utf-8-sig").splitlines()
                if line.strip() and not line.startswith("#")]
        if not rows or rows[0][0] != "key":
            raise RuntimeError("weapon CSV key header missing")
        weapon_keys.extend(row[0] for row in rows[1:])
    applicability = "checked" if tables else "not_applicable_no_weapon_csv_files"
    if (len(set(weapon_keys)) != len(weapon_keys) or any(not key for key in weapon_keys)
            or (tables and not weapon_keys)
            or any(type(report.get(field)) is not int for field in ("weapon_csv_files", "weapon_csv_keys"))
            or report.get("weapon_csv_files") != len(tables)
            or report.get("weapon_csv_keys") != len(set(weapon_keys))
            or report.get("weapon_csv_applicability") != applicability):
        raise RuntimeError("matching checked weapon CSV files and component keys required")


def validate_static_report(report, root):
    mod = root / "mod"
    scripts = [path for path in mod.rglob("*") if path.is_file()
               and (path.suffix.lower() in {".txt", ".gfx", ".gui", ".asset"} or path.name == "descriptor.mod")]
    locales = {}
    key_pattern = re.compile(r'^\s*([^#\s:]+):\d+\s+"', re.M)
    for language in LANGUAGES:
        keys = []
        for path in (mod / "localisation").rglob(f"*_l_{language}.yml"):
            raw = path.read_bytes()
            if not raw.startswith(b"\xef\xbb\xbf"):
                raise RuntimeError("localization BOM missing")
            text = raw.decode("utf-8-sig")
            if not text.startswith(f"l_{language}:"):
                raise RuntimeError("localization header differs")
            keys.extend(key_pattern.findall(text))
        if not keys or len(keys) != len(set(keys)):
            raise RuntimeError("localization keys missing or duplicated: " + language)
        locales[language] = set(keys)
    if any(keys != locales["simp_chinese"] for keys in locales.values()):
        raise RuntimeError("localization key coverage differs")
    validate_weapon_csv_contract(report, mod)
    validate_planet_killer_contract(report, mod)
    if (report.get("status") != "PASS" or report.get("game_exe_sha256") != update.EXE_SHA
            or not scripts or report.get("p_scripts") != len(scripts) or report.get("p_parsed") != len(scripts)
            or report.get("dds") != len(list(mod.rglob("*.dds")))
            or set(report.get("languages", [])) != LANGUAGES or len(report.get("languages", [])) != len(LANGUAGES)
            or report.get("localization_keys") != len(locales["simp_chinese"])
            or report.get("localization_applicability") != "checked" or report.get("errors") != []):
        raise RuntimeError("matching whole-package open_kaishek gate incomplete")


def validate_component_attribution(case, tree, root):
    """Require this candidate's six native RNG channels and fixed-source model.

    The independent report checks actual SAVs and source coefficients. This
    gate binds its bytes and required observations, without claiming that a
    changing-L observation was a fixed-L 0/1/2 hardware probe.
    """
    def require(condition, detail):
        if not condition:
            raise RuntimeError("random_components source attribution incomplete: " + detail)

    def scoped(value):
        return (isinstance(value, dict) and value.get("status") == "PASS_SCOPED"
                and isinstance(value.get("checks"), list) and bool(value["checks"])
                and all(isinstance(row, dict) and row.get("passed") is True for row in value["checks"]))

    def finite(value):
        return type(value) in (int, float) and math.isfinite(value)

    reference = case.get("component_attribution_report")
    require(isinstance(reference, dict), "native growth report reference")
    path = reference_path(reference, root)
    require(any(entry.get("kind") == "analysis" and entry.get("path") == reference["path"]
                and entry.get("sha256") == reference["sha256"] for entry in case["evidence"]),
            "growth report must be this case's analysis evidence")
    try:
        report = read_json(path)
    except (ValueError, OSError) as error:
        raise RuntimeError("random_components source attribution report unreadable") from error
    require(isinstance(report, dict), "native report object")
    require(report.get("schema") == "eep.six-core-growth-report.v1"
            and report.get("status") == "PASS_SCOPED"
            and report.get("component_attribution_contract") == COMPONENT_ATTRIBUTION_CONTRACT,
            "native source-separated RNG contract")
    require(report.get("run_id") in case["run_ids"] and report.get("production_tree_sha256") == tree,
            "current candidate run and source")
    require(type(report.get("absolute_tolerance")) in (int, float)
            and report["absolute_tolerance"] == .01
            and report.get("source_models_sha256") == list(COMPONENT_SOURCE_MODELS),
            "predetermined source models and tolerance")
    for name in ("matrix", "repeat", "reload", "budget", "ordinary_controls"):
        require(scoped(report.get(name)), name + " scoped native checks")
    controls = report["ordinary_controls"].get("ship_ids")
    require(isinstance(controls, list) and bool(controls)
            and all(isinstance(identity, str) and identity for identity in controls)
            and len(set(controls)) == len(controls), "nonempty ordinary native controls")
    coverage, tiers = report.get("nonzero_tier_coverage"), report.get("final_native_tiers")
    require(isinstance(coverage, dict) and set(coverage) == set(COMPONENT_KINDS)
            and all(value is True for value in coverage.values()), "six actual nonzero RNG channels")
    require(isinstance(tiers, dict) and set(tiers) == set(COMPONENT_KINDS)
            and all(type(value) is int and value > 0 for value in tiers.values())
            and sum(tiers.values()) == COMPONENT_NODES[-1] // 50, "six positive actual native tiers")
    baseline = report.get("C0_baseline")
    require(isinstance(baseline, dict) and type(baseline.get("C")) is int and baseline["C"] == 0
            and type(baseline.get("L")) is int and baseline["L"] == 0
            and baseline.get("actual_native_intercept") is True, "actual C0 intercept")
    initial_tiers = baseline.get("tiers")
    require(isinstance(initial_tiers, dict) and set(initial_tiers) == set(COMPONENT_KINDS)
            and all(type(value) is int and value == 0 for value in initial_tiers.values()), "zero C0 native tiers")
    exports, maximums = baseline.get("modifier_exports"), baseline.get("native_maximums")
    require(isinstance(exports, dict) and set(exports) == COMPONENT_MODIFIERS
            and all(finite(value) for value in exports.values()), "ten independent C0 native exports")
    require(isinstance(maximums, dict)
            and set(maximums) == {"max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints"}
            and all(finite(value) and value > 0 for value in maximums.values()), "three actual C0 native maximums")
    native = {entry["sha256"] for entry in case["evidence"] if entry.get("kind") == "native_save"}
    observations = report.get("native_evidence")
    require(isinstance(observations, list) and len(observations) == 2 * len(COMPONENT_NODES),
            "eighteen raw native observations")
    observed_shas = []
    for index, observation in enumerate(observations):
        require(isinstance(observation, dict), "native phase object")
        phase = observation.get("phase")
        require(isinstance(phase, dict) and type(phase.get("C")) is int
                and phase["C"] == COMPONENT_NODES[index // 2]
                and phase.get("phase") == ("refresh" if index % 2 == 0 else "final")
                and observation.get("sha256") in native, "native phase and case SAV binding")
        observed_shas.append(observation["sha256"])
    require(len(set(observed_shas)) == len(observed_shas)
            and baseline.get("save_sha256") == observed_shas[1], "distinct raw SAVs and actual C0 binding")


def validate_runtime_index(runtime, root):
    candidate_version(runtime)
    if (runtime.get("schema") != "eep-1019-acceptance-v1" or runtime.get("status") != "PASS_SCOPED"
            or runtime.get("formal_version") != VERSION or runtime.get("language") != "l_simp_chinese"
            or runtime.get("game_exe_sha256") != update.EXE_SHA
            or runtime.get("profile_id") != PROFILE or runtime.get("enabled_mods") != ENABLED_MODS
            or runtime.get("fully_accepted_civics") != []):
        raise RuntimeError("matching scoped Chinese single-production-mod acceptance required")
    files = candidate_files(runtime)
    tree = candidate_tree(runtime, root)
    if runtime.get("production_tree_sha256") != tree:
        raise RuntimeError("candidate production tree differs")
    static = runtime.get("static_gate", {})
    static_path = reference_path(static.get("report"), root)
    if static.get("production_files") != files or static.get("production_tree_sha256") != tree:
        raise RuntimeError("candidate static gate source differs")
    validate_static_report(read_json(static_path), root)
    manifests = verify_references(runtime.get("runs"), root)
    run_ids = set()
    for path in manifests:
        run = read_json(path)
        source = run.get("repository_mod_files", [])
        hashes = {entry["path"]: entry["sha256"] for entry in source}
        gate = run.get("static_gate", {})
        if (run.get("schema") != "xenoamess.stellaris.acceptance-run.v1"
                or run.get("profile_id") != PROFILE or run.get("enabled_mods") != ENABLED_MODS
                or run.get("language") != "l_simp_chinese" or run.get("game_exe_sha256") != update.EXE_SHA
                or run.get("repository_mod_tree_sha256") != tree or run.get("copied_mod_tree_sha256") != tree
                or len(hashes) != len(source) or hashes != files
                or gate.get("status") != "PASS" or gate.get("version") != runtime["version"]
                or gate.get("source_tree_sha256") != tree or gate.get("report_sha256") != static["report"]["sha256"]
                or not run.get("run_id") or run["run_id"] in run_ids):
            raise RuntimeError("native run does not bind the accepted final candidate: " + str(path))
        run_ids.add(run["run_id"])
    components = runtime.get("component_rewards", {})
    if (components.get("status") not in {"IMPLEMENTED", "DEFERRED"}
            or components.get("interval_levels") != 5 or not components.get("reason", "").strip()):
        raise RuntimeError("every-five-level component implementation scope must be explicit")
    verify_references(components.get("evidence"), root)
    if components["status"] == "DEFERRED":
        authorization = components.get("release_scope_authorization", {})
        if authorization.get("decision") != "USER_APPROVED_SCOPE_CHANGE":
            raise RuntimeError("deferred component release requires explicit user scope-change authorization")
        verify_references(authorization.get("evidence"), root)
    checks = {**CASE_CHECKS}
    if components["status"] == "IMPLEMENTED":
        checks["random_components"] = COMPONENT_CHECKS
    cases = runtime.get("cases", {})
    if set(cases) != set(checks):
        raise RuntimeError("required 1019 runtime case groups differ")
    for name, required in checks.items():
        case = cases[name]
        if (case.get("status") != "PASS_SCOPED" or case.get("production_tree_sha256") != tree
                or not isinstance(case.get("checks"), dict)
                or not required.issubset(case["checks"])
                or any(value is not True for value in case["checks"].values())
                or not case.get("run_ids") or not set(case["run_ids"]).issubset(run_ids)):
            raise RuntimeError("required runtime case incomplete: " + name)
        verify_references(case.get("evidence"), root, EVIDENCE_KINDS)
    if components["status"] == "IMPLEMENTED":
        validate_component_attribution(cases["random_components"], tree, root)
    for branch in ("hive", "machine", "purifier"):
        budget = runtime.get("economy", {}).get(branch, {})
        months = budget.get("candidate_months", [])
        baseline = budget.get("baseline_months", [])
        if (len(months) != 12 or len(baseline) != 12 or len({row.get("date") for row in months}) != 12
                or len({row.get("date") for row in baseline}) != 12):
            raise RuntimeError("twelve native baseline and final-candidate budget samples required: " + branch)
        for rows, candidate in ((months, True), (baseline, False)):
            for row in rows:
                value = row.get("net_energy")
                if (not re.fullmatch(r"\d{4}\.\d{2}\.01", row.get("date", ""))
                        or type(value) not in (int, float) or not math.isfinite(value)
                        or (candidate and value < 0)):
                    raise RuntimeError("invalid or negative native monthly budget: " + branch)
                reference_path(row.get("evidence"), root)
            dates = [(int(row["date"][:4]), int(row["date"][5:7])) for row in rows]
            if any(not 1 <= month <= 12 for _, month in dates):
                raise RuntimeError("invalid native budget month: " + branch)
            ordinals = [year * 12 + month for year, month in dates]
            if ordinals != list(range(ordinals[0], ordinals[0] + 12)):
                raise RuntimeError("native budget months must be consecutive and ordered: " + branch)
            if len({row["evidence"]["path"] for row in rows}) != 12:
                raise RuntimeError("twelve distinct native monthly saves required: " + branch)
        if {row["evidence"]["path"] for row in months} & {row["evidence"]["path"] for row in baseline}:
            raise RuntimeError("baseline saves must not be reused as final candidate: " + branch)
        native = {entry["path"] for entry in cases[f"{branch}_economy"]["evidence"]
                  if entry.get("kind") == "native_save"}
        if not {row["evidence"]["path"] for row in months}.issubset(native):
            raise RuntimeError("candidate budget samples must reference this economy case's native saves: " + branch)
    if runtime.get("growth_samples") != [{"C": count, "L": level} for count, level in GROWTH_SAMPLES]:
        raise RuntimeError("uncapped growth samples differ")
    verify_references(runtime.get("archives"), root)
    return runtime


def collect_reference(spec, root):
    """Hash existing bytes; never infer what an evidence file proves."""
    if isinstance(spec, str):
        spec = {"path": spec}
    if not isinstance(spec, dict) or set(spec) - {"path", "kind"}:
        raise RuntimeError("reference plan entries accept only path and optional kind")
    path = project_evidence_path(spec.get("path"), root)
    entry = {"path": path.relative_to(root.resolve()).as_posix(), "sha256": update.digest(path.read_bytes())}
    if "kind" in spec:
        if spec["kind"] not in EVIDENCE_KINDS:
            raise RuntimeError("unsupported planned evidence kind")
        entry["kind"] = spec["kind"]
    return entry


def scaffold_content_digest(data):
    content = {**data, "_scaffold": {**data.get("_scaffold", {})}}
    content["_scaffold"].pop("generated_content_sha256", None)
    return update.digest(json.dumps(content, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":"), allow_nan=False).encode("utf-8"))


def build_pending_index(root, plan=None):
    """Inventory and evidence references only; every acceptance result stays pending."""
    root = root.resolve()
    plan = {} if plan is None else plan
    if not isinstance(plan, dict) or set(plan) - {"static_report", "runs", "cases", "component_evidence", "archives"}:
        raise RuntimeError("reference plan cannot provide statuses, check results, budgets or growth observations")
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    data = {"schema": "eep-1019-acceptance-v1", "status": "PENDING", "version": version,
            "formal_version": VERSION, "language": "l_simp_chinese", "game_exe_sha256": update.EXE_SHA,
            "profile_id": PROFILE, "enabled_mods": list(ENABLED_MODS), "fully_accepted_civics": [],
            "production_files": update.base.manifest(root / "mod"),
            "candidate_descriptor": (root / "mod/descriptor.mod").read_bytes().decode("utf-8")}
    candidate_version(data)
    tree = candidate_tree(data, root)
    data["production_tree_sha256"] = tree
    data["static_gate"] = {"report": collect_reference(plan["static_report"], root) if plan.get("static_report") else None,
                           "production_files": dict(data["production_files"]), "production_tree_sha256": tree}
    if not isinstance(plan.get("runs", []), list) or not isinstance(plan.get("cases", {}), dict):
        raise RuntimeError("reference plan runs must be a list and cases must be a dictionary")
    data["runs"] = [collect_reference(spec, root) for spec in plan.get("runs", [])]
    planned_checks = {**CASE_CHECKS, "random_components": COMPONENT_CHECKS}
    if set(plan.get("cases", {})) - set(planned_checks):
        raise RuntimeError("unknown planned runtime case")
    data["cases"] = {}
    for name, checks in planned_checks.items():
        item = plan.get("cases", {}).get(name, {})
        if (not isinstance(item, dict) or set(item) - {"run_ids", "evidence"}
                or not isinstance(item.get("run_ids", []), list)
                or any(not isinstance(run_id, str) or not run_id for run_id in item.get("run_ids", []))
                or not isinstance(item.get("evidence", []), list)):
            raise RuntimeError("planned case accepts only run_ids and evidence references: " + name)
        evidence = [collect_reference(spec, root) for spec in item.get("evidence", [])]
        data["cases"][name] = {"status": "PENDING", "production_tree_sha256": tree,
                              "run_ids": list(item.get("run_ids", [])),
                              "checks": {check: None for check in sorted(checks)}, "evidence": evidence}
    data["economy"] = {branch: {"baseline_months": [], "candidate_months": []}
                       for branch in ("hive", "machine", "purifier")}
    data["growth_samples"] = []
    for field in ("component_evidence", "archives"):
        if not isinstance(plan.get(field, []), list):
            raise RuntimeError("reference plan evidence groups must be lists")
    data["component_rewards"] = {"status": "PENDING", "interval_levels": 5,
                                 "reason": "Await actual native component tests and implementation decision.",
                                 "evidence": [collect_reference(spec, root) for spec in plan.get("component_evidence", [])]}
    data["archives"] = [collect_reference(spec, root) for spec in plan.get("archives", [])]
    data["_scaffold"] = {"schema": "eep-1019-index-scaffold-v1", "acceptance_claims": False,
        "warning": "PENDING inventory and planned evidence only; no native action or acceptance is inferred.",
        "required_growth_samples": [{"C": count, "L": level} for count, level in GROWTH_SAMPLES],
        "required_evidence_kinds": sorted(EVIDENCE_KINDS), "required_months_per_budget": 12}
    return data


def write_pending_index(root, output=None, reference_plan=None):
    """Regenerate only an untouched scaffold; never replace manually reviewed evidence."""
    root = root.resolve()
    output = root / "docs/evidence/1019-requirements/final-result.pending.json" if output is None else Path(output)
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    try:
        output.relative_to(root)
        output.relative_to((root / "docs/evidence").resolve())
    except ValueError as error:
        raise RuntimeError("pending scaffold output must remain inside this project's docs/evidence") from error
    if output == (root / "docs/evidence/1019-requirements/final-result.json").resolve():
        raise RuntimeError("scaffold cannot write the final acceptance index")
    plan = None
    plan_reference = None
    if reference_plan is not None:
        path = Path(reference_plan)
        if path.is_absolute():
            try:
                path = path.resolve().relative_to(root)
            except ValueError as error:
                raise RuntimeError("reference plan must remain inside this project") from error
        plan_reference = collect_reference(path.as_posix(), root)
        plan = read_json(root / plan_reference["path"])
    data = build_pending_index(root, plan)
    if plan_reference:
        data["_scaffold"]["reference_plan"] = plan_reference
    data["_scaffold"]["generated_content_sha256"] = scaffold_content_digest(data)
    if output.exists():
        try:
            existing = read_json(output)
            untouched = (existing.get("status") == "PENDING"
                and existing.get("_scaffold", {}).get("schema") == "eep-1019-index-scaffold-v1"
                and existing.get("_scaffold", {}).get("acceptance_claims") is False
                and existing["_scaffold"].get("generated_content_sha256") == scaffold_content_digest(existing)
                and all(case.get("status") == "PENDING" and all(value is None for value in case.get("checks", {}).values())
                        for case in existing.get("cases", {}).values())
                and existing.get("component_rewards", {}).get("status") == "PENDING")
        except (KeyError, ValueError, TypeError, AttributeError):
            untouched = False
        if not untouched:
            raise RuntimeError("refuse to overwrite manual or accepted evidence; select a new pending output")
        if existing == data:
            return {"status": "PENDING", "output": output.relative_to(root).as_posix(), "changed": False,
                    "cases": len(data["cases"]), "production_tree_sha256": data["production_tree_sha256"]}
    update.base.write_json(output, data)
    return {"status": "PENDING", "output": output.relative_to(root).as_posix(), "changed": True,
            "cases": len(data["cases"]), "production_tree_sha256": data["production_tree_sha256"]}


def load_runtime():
    if not RUNTIME.is_file():
        raise RuntimeError("final 1019 runtime acceptance index missing: " + str(RUNTIME))
    return validate_runtime_index(read_json(RUNTIME), ROOT)


def prior_release():
    prior = read_json(ROOT / "docs/evidence/publication-0.3.1/workshop-verification.json")
    if prior.get("status") != "PASS" or prior.get("version") != "0.3.1" or prior.get("item_id") != update.ITEM:
        raise RuntimeError("previous verified 0.3.1 identity differs")
    return prior


def accepted_files():
    prior_release()
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise RuntimeError("formal VERSION required; release candidates cannot be published")
    runtime = load_runtime()
    files = update.base.manifest(ROOT / "mod")
    validate_candidate_files(files, runtime)
    static = EVIDENCE / "open-kaishek.json"
    validate_static_report(read_json(static), ROOT)
    binding = read_json(EVIDENCE / "static-source-manifest.json")
    if (binding.get("version") != VERSION or binding.get("production_files") != files
            or binding.get("report_sha256") != update.digest(static.read_bytes())):
        raise RuntimeError("formal static source or report changed")
    return {"status": "PASS_SCOPED", "version": VERSION, "candidate_version": runtime["version"],
            "previous_public_version": "0.3.1", "production_files": files,
            "runtime_index_sha256": update.digest(RUNTIME.read_bytes()),
            "static_sha256": update.digest(static.read_bytes()), "cases": sorted(runtime["cases"]),
            "component_rewards": runtime["component_rewards"], "fully_accepted_civics": [],
            "scope": "1019 final-candidate startup/economy, flagship growth, native colossus and migration cases only",
            "only_mod_change_from_candidate": "descriptor version metadata"}


def record_static():
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        raise RuntimeError("formal VERSION required before recording formal static gate")
    runtime = load_runtime()
    files = update.base.manifest(ROOT / "mod")
    validate_candidate_files(files, runtime)
    report = EVIDENCE / "open-kaishek.json"
    validate_static_report(read_json(report), ROOT)
    update.base.write_json(EVIDENCE / "static-source-manifest.json", {
        "version": VERSION, "production_files": files, "report_sha256": update.digest(report.read_bytes())})


def validate_gallery(images, runtime, prior, root):
    gallery = [image for image in images if image.get("role") == "gallery"]
    if len(gallery) != 6 or [image.get("id") for image in gallery] != [f"WS-{i:02}" for i in range(1, 7)]:
        raise RuntimeError("six ordered Workshop gallery slots required")
    old = prior.get("gallery", [])
    if len(old) != 6:
        raise RuntimeError("previous verified six-slot gallery missing")
    opening = gallery[-1]
    if (opening.get("sha256") == old[-1].get("sha256")
            or Path(opening.get("file", "")).name == old[-1].get("filename")
            or opening.get("evidence_kind") != "native_screenshot"
            or opening.get("run_id") not in runtime["cases"]["purifier_startup"]["run_ids"]):
        raise RuntimeError("WS-06 requires a new final-candidate single-homeworld startup screenshot and filename")
    evidence = runtime["cases"]["purifier_startup"]["evidence"]
    references = {reference_path(entry, root) for entry in evidence if entry.get("kind") == "screenshot"}
    native_saves = {reference_path(entry, root) for entry in evidence if entry.get("kind") == "native_save"}
    source = (root / "workshop" / opening["source"]).resolve()
    save = (root / "workshop" / opening["native_save"]).resolve()
    if source not in references or save not in native_saves:
        raise RuntimeError("WS-06 source and native save must be accepted purifier startup evidence")
    return gallery


_description_inputs = update.description_inputs
_preflight = update.preflight


def description_inputs():
    description, pictures = _description_inputs()
    runtime = load_runtime()
    if {picture["url"]: picture["sha256"] for picture in pictures} != {
            picture["source"]: picture["sha256"] for picture in prior_release().get("inline_images", [])}:
        raise RuntimeError("the four historical immutable inline images must be preserved")
    if runtime["component_rewards"]["status"] == "DEFERRED":
        disclosure = "每5级随机组件未实现"
        if disclosure not in description or disclosure not in update.release_entry():
            raise RuntimeError("deferred component rewards must be disclosed in description and formal changelog")
    return description, pictures


def preflight(require_clean=True):
    inputs = _preflight(require_clean=require_clean)
    validate_gallery(inputs["images"], load_runtime(), prior_release(), ROOT)
    return inputs


def tag_check():
    """Read-only local guard; the operator creates a tag only after this passes."""
    acceptance = accepted_files()
    state = read_json(EVIDENCE / "publish-state.json")
    verified = read_json(EVIDENCE / "workshop-verification.json")
    downloaded = read_json(EVIDENCE / "workshop-download.json")
    inputs = state.get("inputs", {})
    if (state.get("version") != VERSION or state.get("item_id") != update.ITEM
            or state.get("submit_result") != 1 or state.get("submit_item_id") != update.ITEM
            or state.get("submit_legal_required") is not False or inputs.get("acceptance") != acceptance
            or inputs.get("content") != acceptance["production_files"]
            or verified.get("status") != "PASS" or verified.get("version") != VERSION
            or verified.get("item_id") != update.ITEM or verified.get("production_files") != inputs["content"]
            or verified.get("download_files") != len(inputs["content"])
            or any(verified.get(field) is not True for field in (
                "public_metadata_exact", "change_note_exact", "gallery_exact", "inline_images_exact"))
            or downloaded.get("status") != "DOWNLOADED" or downloaded.get("version") != VERSION
            or downloaded.get("item_id") != update.ITEM or downloaded.get("content") != inputs["content"]
            or len(verified.get("gallery", [])) != 6 or len(verified.get("inline_images", [])) != 4):
        raise RuntimeError("exact successful upload, independent download and public media verification required before tag")
    installed = Path(downloaded["folder"]).resolve(strict=True)
    mod = (ROOT / "mod").resolve()
    if installed == mod or mod in installed.parents or not installed.is_dir():
        raise RuntimeError("independent installed Workshop directory required before tag")
    if update.base.manifest(installed) != inputs["content"]:
        raise RuntimeError("independently downloaded bytes changed after verification")
    description, pictures = description_inputs()
    current_images = update.workshop_images.local_images(ROOT, VERSION)
    if (description != inputs.get("description") or update.change_note() != inputs.get("note")
            or current_images != inputs.get("images")
            or json.loads(json.dumps(pictures)) != inputs.get("inline_images")):
        raise RuntimeError("public text or frozen images changed after verification")
    gallery = inputs.get("gallery", [])
    if len(gallery) != 6:
        raise RuntimeError("six frozen gallery slots required before tag")
    for index, (actual, expected) in enumerate(zip(verified["gallery"], gallery, strict=True)):
        if (actual.get("index") != index or actual.get("type") != 0
                or actual.get("filename") != Path(expected["file"]).name
                or actual.get("sha256") != expected["sha256"] or actual.get("bytes") != expected["bytes"]):
            raise RuntimeError("verified gallery differs from frozen inputs")
    if {entry.get("source"): entry.get("sha256") for entry in verified["inline_images"]} != {
            entry["url"]: entry["sha256"] for entry in pictures}:
        raise RuntimeError("verified inline images differ from frozen inputs")
    if update.git("status", "--porcelain"):
        raise RuntimeError("commit and push verification receipts before tag")
    head = update.git("rev-parse", "HEAD").decode().strip()
    if update.git("rev-parse", "@{upstream}").decode().strip() != head:
        raise RuntimeError("verification commit has not been pushed")
    return {"status": "READY_TO_TAG", "version": VERSION, "tag": "v" + VERSION, "head": head,
            "verification_sha256": update.digest((EVIDENCE / "workshop-verification.json").read_bytes())}


@contextmanager
def configured():
    """Restore old adapter globals so historical imports/tests stay independent."""
    values = {"VERSION": VERSION, "EVIDENCE": EVIDENCE, "accepted_files": accepted_files,
              "description_inputs": description_inputs, "preflight": preflight}
    for key, name in {"STATE": "publish-state.json", "ACCEPTANCE": "acceptance.json",
                      "STATIC": "open-kaishek.json", "DOWNLOAD": "workshop-download.json",
                      "VERIFIED": "workshop-verification.json", "INLINE": "inline-images.json"}.items():
        values[key] = EVIDENCE / name
    saved = {key: getattr(update, key) for key in values}
    try:
        for key, value in values.items():
            setattr(update, key, value)
        yield
    finally:
        for key, value in saved.items():
            setattr(update, key, value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("scaffold-index", "check-runtime", "record-static", "prepare", "preflight",
                                             "publish", "download", "verify", "tag-check"))
    parser.add_argument("--download", type=Path)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--output", type=Path, help="scaffold-index: project-relative pending output")
    parser.add_argument("--reference-plan", type=Path, help="scaffold-index: project-relative evidence reference plan")
    args = parser.parse_args()
    with configured():
        if args.command == "scaffold-index":
            print(json.dumps(write_pending_index(ROOT, args.output, args.reference_plan)))
        elif args.command == "check-runtime":
            runtime = load_runtime()
            print(json.dumps({"status": runtime["status"], "version": runtime["version"],
                              "cases": len(runtime["cases"])}))
        elif args.command == "record-static":
            record_static()
        elif args.command == "tag-check":
            print(json.dumps(tag_check()))
        elif args.command == "prepare":
            validate_gallery(update.workshop_images.local_images(ROOT, VERSION), load_runtime(), prior_release(), ROOT)
            update.prepare()
        elif args.command == "download":
            if args.timeout < 1:
                raise RuntimeError("positive download timeout required")
            update.base.STATE, update.base.DOWNLOAD_RECEIPT = update.STATE, update.DOWNLOAD
            update.base.download_item(args.timeout)
        elif args.command == "verify":
            if not args.download or not args.download.is_dir():
                raise RuntimeError("independent installed Workshop directory required")
            update.verify(args.download)
        else:
            inputs = preflight()
            if args.command == "publish":
                update.publish(inputs)
            else:
                print(json.dumps({"status": "PASS", "version": VERSION, "files": len(inputs["content"])}))


if __name__ == "__main__":
    main()
