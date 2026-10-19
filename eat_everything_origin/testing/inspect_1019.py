"""Read-only 1019 native SAV observations; extraction never implies acceptance."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import audit_save as a
import check_single_homeworld as old
import inspect_1015


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def blocks(text, key):
    return [value for name, value, obj in a.fields(text) if obj and name == key]


def anonymous_blocks(text):
    """Extract native unnamed objects (growth_stages and timed_modifier.items)."""
    result, depth, start = [], 0, None
    for token, before, after in a.tokens(text):
        if token == "{":
            if depth == 0:
                start = after
            depth += 1
        elif token == "}":
            depth -= 1
            if depth < 0:
                raise ValueError("unexpected anonymous-list closing brace")
            if depth == 0:
                result.append(text[start:before])
        elif depth == 0:
            raise ValueError("expected anonymous object list")
    if depth:
        raise ValueError("unclosed anonymous object")
    return result


def modifiers(body):
    raw = a.block(body, "timed_modifier")
    return {"raw": raw, "items": [a.scalars(item) for item in
                                      anonymous_blocks(a.block(raw, "items"))]}


def sections(body):
    return [{"native": a.scalars(section),
             "components": [a.scalars(c) for c in blocks(section, "component")],
             "raw": section} for section in blocks(body, "section")]


def design(body):
    stages = anonymous_blocks(a.block(body, "growth_stages"))
    if not stages:  # Script definitions have no growth_stages wrapper.
        stages = [body]
    return {"native": a.scalars(body),
            "name": a.scalars(a.block(body, "name")).get("key", a.scalars(body).get("name")),
            "stages": [{"native": a.scalars(stage), "sections": sections(stage),
                        "required_components": [a.unquote(v) for k, v, b in a.fields(stage)
                                                if k == "required_component" and not b],
                        "raw": stage} for stage in stages],
            "raw": body, "body_sha256": hashlib.sha256(body.encode()).hexdigest()}


def shield_basis(observation, ship):
    """Resolve installed base shield from source, never from actual shield HP.

    Sources are read from the manifest's native installation and immutable
    copied_mod. Unsupported expressions/conflicting symbols fail explicitly.
    """
    manifest = json.loads(Path(observation["manifest"]).read_text(encoding="utf-8"))
    exe = Path(manifest["game_exe"])
    if digest(exe) != manifest["game_exe_sha256"]:
        raise ValueError("current native executable differs from runtime manifest")
    native, mod = exe.parent, Path(manifest["copied_mod"])
    cache = {}

    def source(path):
        path = Path(path)
        if path not in cache:
            cache[path] = {"path": str(path), "sha256": digest(path),
                           "text": path.read_text(encoding="utf-8-sig")}
        return cache[path]

    def effective_files(relative):
        # A copied file at the same relative path replaces that native file.
        files = {p.name: p for p in (native / relative).glob("*.txt")}
        files.update({p.name: p for p in (mod / relative).glob("*.txt")})
        return [files[key] for key in sorted(files)]

    variable_pattern = re.compile(r"(?m)^[ \t]*(@[A-Za-z0-9_]+)[ \t]*=[ \t]*([^#\r\n]+)")
    globals_ = {}
    for path in effective_files("common/scripted_variables"):
        record = source(path)
        for match in variable_pattern.finditer(record["text"]):
            globals_.setdefault(match[1], []).append({"path": str(path), "sha256": record["sha256"],
                "line": record["text"].count("\n", 0, match.start()) + 1, "token": match[2].strip()})
    resolutions = []

    def number(token, path, seen=()):
        if isinstance(token, (int, float)):
            return token
        if isinstance(token, str) and re.fullmatch(r"-?\d+(?:\.\d+)?", token):
            return a.unquote(token)
        if not isinstance(token, str) or not re.fullmatch(r"@[A-Za-z0-9_]+", token):
            raise ValueError("unsupported native shield expression: " + str(token))
        if token in seen:
            raise ValueError("cyclic native shield variable: " + token)
        record = source(path)
        local = [{"path": str(path), "sha256": record["sha256"],
                  "line": record["text"].count("\n", 0, m.start()) + 1, "token": m[2].strip()}
                 for m in variable_pattern.finditer(record["text"]) if m[1] == token]
        definitions = local or globals_.get(token, [])
        if not definitions:
            raise ValueError("unresolved native shield variable: " + token)
        values = [number(d["token"], Path(d["path"]), (*seen, token)) for d in definitions]
        if any(value != values[0] for value in values):
            raise ValueError("conflicting native shield variable: " + token)
        resolutions.append({"variable": token, "resolved": values[0], "definitions": definitions})
        return values[0]

    library = {}
    for path in effective_files("common/component_templates"):
        record = source(path)
        for kind, body, obj in a.fields(record["text"]):
            if obj and kind.endswith("component_template"):
                # Some unrelated native components use @[ arithmetic ] later
                # in their body. Index the direct key without evaluating it.
                key = next((a.unquote(value) for name, value, nested in a.fields(body)
                            if name == "key" and not nested), None)
                if key is not None:
                    library.setdefault(key, []).append((path, body, kind))

    def context(body, path):
        records = []
        for key, raw, obj in a.fields(body):
            if obj and ("modifier" in key):
                shield = {k: {"raw": v, "resolved": number(v, path)}
                          for k, v, nested in a.fields(raw) if not nested and "shield" in k}
                if shield:
                    records.append({"scope": key, "fields": shield, "raw": raw})
        return records

    counts = {}
    if len(ship["design"]["stages"]) != 1:
        raise ValueError("shield hardware basis requires one fixed native design stage")
    for stage in ship["design"]["stages"]:
        for section in stage["sections"]:
            for component in section["components"]:
                key = component["template"]
                counts[key] = counts.get(key, 0) + 1
        for key in stage["required_components"]:
            counts[key] = counts.get(key, 0) + 1
    records, total, design_mult_contributions = [], 0, []
    for key, count in sorted(counts.items()):
        found = library.get(key, [])
        if len(found) != 1:
            raise ValueError("expected one effective source for installed component: " + key)
        path, body, kind = found[0]
        contexts = context(body, path)
        additive = 0
        for entry in contexts:
            if "ship_shield_add" in entry["fields"]:
                if entry["scope"] != "modifier":
                    raise ValueError("unsupported non-design additive shield source: " + key)
                additive += entry["fields"]["ship_shield_add"]["resolved"]
            if "ship_shield_mult" in entry["fields"]:
                if entry["scope"] == "modifier":
                    each = entry["fields"]["ship_shield_mult"]["resolved"]
                    design_mult_contributions.append({"component": key, "count": count,
                        "scope": "component.modifier", "per_component": each, "total": count * each,
                        "path": str(path), "sha256": source(path)["sha256"]})
                elif entry["scope"] == "triggered_ship_design_modifier":
                    raise ValueError("conditional design shield multiplier requires explicit evaluation: " + key)
        total += count * additive
        records.append({"key": key, "count": count, "kind": kind, "source": str(path),
                        "source_sha256": source(path)["sha256"], "base_shield_each": additive,
                        "shield_context": contexts, "definition_raw": body})
    ship_size = ship["design"]["stages"][0]["native"]["ship_size"]
    sizes = []
    for path in effective_files("common/ship_sizes"):
        for key, body, obj in a.fields(source(path)["text"]):
            if obj and key == ship_size:
                sizes.append((path, body))
    if len(sizes) != 1:
        raise ValueError("expected one effective native ship-size source")
    path, body = sizes[0]
    size_context = context(body, path)
    size_native = a.scalars(body)
    native_shield = {k: {"raw": v, "resolved": number(v, path)}
                     for k, v in size_native.items() if "shield" in k}
    if native_shield or any(any(key in item["fields"] for key in ("ship_shield_add", "ship_shield_mult"))
                            for item in size_context):
        raise ValueError("ship-size additive shield requires explicit supported derivation")
    section_context = []
    for stage in ship["design"]["stages"]:
        for section in stage["sections"]:
            key = section["native"]["template"]
            found = []
            for section_path in effective_files("common/section_templates"):
                for name, section_body, obj in a.fields(source(section_path)["text"]):
                    template_key = next((a.unquote(value) for field, value, nested in a.fields(section_body)
                                         if field == "key" and not nested), None) if obj and name == "ship_section_template" else None
                    if template_key == key:
                        found.append((section_path, section_body))
            if len(found) != 1:
                raise ValueError("expected one effective source for installed section: " + key)
            section_path, section_body = found[0]
            contexts = context(section_body, section_path)
            if any(any(field in item["fields"] for field in ("ship_shield_add", "ship_shield_mult"))
                   for item in contexts):
                raise ValueError("section additive shield requires explicit supported derivation")
            section_context.append({"key": key, "path": str(section_path),
                                    "sha256": source(section_path)["sha256"], "shield_context": contexts})
    design_mult = sum(item["total"] for item in design_mult_contributions)
    if 1 + design_mult <= 0:
        raise ValueError("nonpositive native design shield multiplier")
    documentation = native / "common/component_templates/000_documentation.txt"
    return {"base_shield": total,
            "design_shield_multiplier_add": design_mult,
            "design_shield_multiplier_factor": 1 + design_mult,
            "design_shield_multiplier_contributions": design_mult_contributions,
            "design_shield_before_ship_modifiers": total * (1 + design_mult),
            "source_layer_documentation": {"path": str(documentation), "sha256": digest(documentation),
                "design_modifier_line": 12, "triggered_ship_scope_line": 18, "triggered_design_scope_line": 24,
                "interpretation": "Design modifier and ship modifier are separate source scopes; the layered numerical model is checked against native readings, not claimed as closed-source engine code."},
            "installed_components_including_required": records,
            "ship_size": {"key": ship_size, "path": str(path), "sha256": source(path)["sha256"],
                          "native_shield_fields": native_shield, "shield_context": size_context,
                          "definition_raw": body}, "sections": section_context,
            "variable_resolutions": resolutions,
            "native_exe": {"path": str(exe), "sha256": digest(exe)},
            "source_read_scope": "current native files plus verified frozen copied_mod; source-derived expectation only"}


def provenance(save):
    save = Path(save).resolve(strict=True)
    run = save.parent
    manifest = old.read_run(run)
    if manifest["static_gate"].get("status") != "PASS":
        raise ValueError("native run did not pass its static gate")
    archive_sha = digest(save)
    audit_path = save.with_suffix(".audit.json")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    if audit.get("save_sha256") != archive_sha:
        raise ValueError("native audit SHA does not match SAV")
    matches, unsupported_receipts = [], []
    receipt_paths = set(run.glob("*.native-save.json")) | set(run.glob("*-receipt.json"))
    for path in sorted(receipt_paths):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            unsupported_receipts.append({"path": str(path), "sha256": digest(path), "shape": type(receipt).__name__})
            continue
        entries = receipt.get("snapshots", [receipt])
        if not isinstance(entries, list):
            unsupported_receipts.append({"path": str(path), "sha256": digest(path),
                                         "snapshots_shape": type(entries).__name__})
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                unsupported_receipts.append({"path": str(path), "sha256": digest(path),
                                             "entry_shape": type(entry).__name__})
                continue
            if entry.get("sha256") == archive_sha and entry.get("date") == audit["date"]:
                matches.append({"path": str(path), "sha256": digest(path), "entry": entry})
    if not matches:
        raise ValueError("no matching original native-save/monthly receipt")
    descriptor = Path(manifest["copied_mod"]) / "descriptor.mod"
    descriptor_version = a.scalars(descriptor.read_text(encoding="utf-8-sig")).get("version")
    version = manifest["static_gate"].get("version", descriptor_version)
    if version != descriptor_version:
        raise ValueError("static gate version differs from verified copied descriptor")
    return manifest, {"save": str(save), "save_sha256": archive_sha,
                      "run_id": manifest["run_id"], "version": version,
                      "version_source": "static_gate_and_copied_descriptor" if "version" in manifest["static_gate"]
                                        else "verified_copied_descriptor_only",
                      "production_tree_sha256": manifest["repository_mod_tree_sha256"],
                      "manifest_sha256": digest(run / "manifest.json"),
                      "audit": str(audit_path), "audit_sha256": digest(audit_path),
                      "receipts": matches, "unsupported_receipt_shapes": unsupported_receipts}


def observe(save, world_ids=()):
    save = Path(save)
    manifest, proof = provenance(save)
    result = inspect_1015.observe(save, save.parent / "manifest.json")
    with zipfile.ZipFile(save) as archive:
        native = archive.read("gamestate")
    text = native.decode("utf-8-sig")
    roots = {key: value for key, value, obj in a.fields(text) if obj}
    country = a.block(roots["country"], "0")
    ships = inspect_1015.objects(roots["ships"])
    fleets = inspect_1015.objects(roots["fleet"])
    designs = inspect_1015.objects(roots["ship_design"])
    owned = a.block(a.block(country, "fleets_manager"), "owned_fleets")
    owned_fleets = {str(v) for v in re.findall(r"\bfleet\s*=\s*(\d+)", owned)}
    mother_targets = [t for t in result["event_targets"] if t["name"] == "eep_mothership0"]
    mother_ids = {str(t["id"]) for t in mother_targets}
    result["fleets_1019"] = {}
    for identity, body in fleets.items():
        name = a.scalars(a.block(body, "name")).get("key")
        if identity not in owned_fleets and identity not in mother_ids and name != "NAME_Relic":
            continue
        record = {"native": a.scalars(body), "name": name, "variables": a.scalars(a.block(body, "variables")),
                  "timed_modifier": modifiers(body), "ships": {}, "raw": body}
        movement = a.block(body, "movement_manager")
        record["movement"] = {"native": a.scalars(movement),
                              "coordinate": a.scalars(a.block(movement, "coordinate")),
                              "target_coordinate": a.scalars(a.block(movement, "target_coordinate")),
                              "orbit_raw": a.block(movement, "orbit"), "raw": movement}
        for ship_id in a.ids(a.block(body, "ships")):
            ship_body = ships[str(ship_id)]
            implementation = a.scalars(a.block(ship_body, "ship_design_implementation"))
            design_id = str(implementation["design"])
            record["ships"][str(ship_id)] = {
                "native": a.scalars(ship_body), "implementation": implementation,
                "design_id": design_id, "design": design(designs[design_id]),
                "timed_modifier": modifiers(ship_body), "variables": a.scalars(a.block(ship_body, "variables")),
                "flags": a.scalars(a.block(ship_body, "flags")),
                "name": a.scalars(a.block(ship_body, "name")),
                "coordinate": a.scalars(a.block(ship_body, "coordinate")),
                "target_coordinate": a.scalars(a.block(ship_body, "target_coordinate")), "raw": ship_body}
        result["fleets_1019"][identity] = record
    result["starbases_1019"] = {}
    for identity, body in inspect_1015.objects(a.block(roots["starbase_mgr"], "starbases")).items():
        record = a.scalars(body)
        station = ships.get(str(record.get("station")), "")
        if str(a.scalars(station).get("fleet")) not in result["fleets_1019"]:
            continue
        result["starbases_1019"][identity] = {
            "native": record,
            "standalone_components": [a.unquote(v) for v, _, _ in a.tokens(a.block(body, "standalone_components"))],
            "timed_modifier": modifiers(body), "variables": a.scalars(a.block(body, "variables")), "raw": body}
    construction = roots.get("construction", "")
    queue_bodies = inspect_1015.objects(a.block(a.block(construction, "queue_mgr"), "queues"))
    result["queues_1019"] = {identity: {**record, "raw": queue_bodies[identity]}
                             for identity, record in result["queues"].items()}
    item_bodies = inspect_1015.objects(a.block(a.block(construction, "item_mgr"), "items"))
    result["construction_items_1019"] = {}
    for identity, record in result["construction_items"].items():
        body = item_bodies[identity]
        ship = a.block(body, "buildable_ship")
        implementation = a.scalars(a.block(ship, "ship_design_implementation"))
        design_id = str(implementation.get("design"))
        result["construction_items_1019"][identity] = {
            **record, "ship_implementation": implementation,
            "orbitable": a.scalars(a.block(ship, "orbitable")),
            "queued_ship_design": design(designs[design_id]) if design_id in designs else None}
    all_worlds = inspect_1015.objects(a.block(roots["planets"], "planet"))
    selected_worlds = result["worlds"].keys() | {str(i) for i in world_ids}
    result["worlds_1019"] = {}
    pop_groups = inspect_1015.objects(roots.get("pop_groups", ""))
    for identity in sorted(selected_worlds):
        body = all_worlds.get(identity)
        if body is None:
            raise ValueError("requested planet absent from native save: " + identity)
        record = a.scalars(body)
        colony = a.block(roots.get("colony", ""), str(record.get("colony")))
        groups = {str(i): {"native": a.scalars(pop_groups[str(i)]),
                          "key": a.scalars(a.block(pop_groups[str(i)], "key"))}
                  for i in a.ids(a.block(colony, "pop_groups"))}
        result["worlds_1019"][identity] = {
            "native": record, "variables": a.scalars(a.block(body, "variables")),
            "flags_raw": a.block(body, "flags"),
            "flags": [k for k, _, _ in a.fields(a.block(body, "flags"))],
            "timed_modifier": modifiers(body), "colony_native": a.scalars(colony),
            "deposits": {str(i): a.scalars(a.block(roots.get("deposit", ""), str(i)))
                         for i in a.ids(a.block(body, "deposits"))},
            "pop_groups": groups, "actual_pop_sum": sum(g["native"]["size"] for g in groups.values()),
            "raw": body, "colony_raw": colony}
    result["provenance_1019"] = proof
    result["gamestate_sha256"] = hashlib.sha256(native).hexdigest()
    original_audit = json.loads(save.with_suffix(".audit.json").read_text(encoding="utf-8"))
    if (original_audit.get("gamestate_sha256") != result["gamestate_sha256"]
            or original_audit["date"] != result["date"]):
        raise ValueError("audit gamestate SHA/date differs from native SAV")
    result["country_variables_all"] = a.scalars(a.block(country, "variables"))
    result["country_timed_modifier"] = modifiers(country)
    result["crisis_progression_raw"] = a.block(country, "crisis_progression")
    result["crisis_progression_native"] = a.scalars(result["crisis_progression_raw"])
    result["crisis_objectives"] = [a.scalars(body) for body in
                                  blocks(result["crisis_progression_raw"], "objective")]
    result["crisis_levels"] = [a.unquote(v) for k, v, obj in a.fields(result["crisis_progression_raw"])
                               if not obj and k == "level"]
    result["galaxy_native"] = a.scalars(roots.get("galaxy", ""))
    result["galaxy_system_count"] = len(inspect_1015.objects(roots.get("galactic_object", "")))
    result["inspector_sha256"] = digest(Path(__file__))
    return result
