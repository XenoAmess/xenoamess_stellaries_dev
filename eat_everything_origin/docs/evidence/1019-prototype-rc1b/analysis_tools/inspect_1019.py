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
    matches = []
    receipt_paths = set(run.glob("*.native-save.json")) | set(run.glob("*-receipt.json"))
    for path in sorted(receipt_paths):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        entries = receipt.get("snapshots", [receipt])
        for entry in entries:
            if entry.get("sha256") == archive_sha and entry.get("date") == audit["date"]:
                matches.append({"path": str(path), "sha256": digest(path), "entry": entry})
    if not matches:
        raise ValueError("no matching original native-save/monthly receipt")
    return manifest, {"save": str(save), "save_sha256": archive_sha,
                      "run_id": manifest["run_id"], "version": manifest["static_gate"].get("version"),
                      "production_tree_sha256": manifest["repository_mod_tree_sha256"],
                      "manifest_sha256": digest(run / "manifest.json"),
                      "audit": str(audit_path), "audit_sha256": digest(audit_path),
                      "receipts": matches}


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
        for ship_id in a.ids(a.block(body, "ships")):
            ship_body = ships[str(ship_id)]
            implementation = a.scalars(a.block(ship_body, "ship_design_implementation"))
            design_id = str(implementation["design"])
            record["ships"][str(ship_id)] = {
                "native": a.scalars(ship_body), "implementation": implementation,
                "design_id": design_id, "design": design(designs[design_id]),
                "timed_modifier": modifiers(ship_body), "variables": a.scalars(a.block(ship_body, "variables")),
                "flags": a.scalars(a.block(ship_body, "flags")),
                "coordinate": a.scalars(a.block(ship_body, "coordinate")), "raw": ship_body}
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
