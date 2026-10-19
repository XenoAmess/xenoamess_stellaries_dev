#!/usr/bin/env python3
"""Validate a Stellaris Mod package with Kaishek syntax and static contracts.

This check deliberately makes no opcode or runtime-semantic claim for paths not
registered by a game-version profile. A passing report must be paired with a
separate Stellaris runtime test for behavioral acceptance.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

if __package__:
    from tools.stellaris_scope_guard import population_scope_preflight, script_value_shape_preflight
else:
    from stellaris_scope_guard import population_scope_preflight, script_value_shape_preflight


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "kaishek-cli/target/kaishek-cli-0.1.0-SNAPSHOT.jar"
CYGNUS_451_SHA256 = "6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4"
LOCALIZATION = re.compile(r'^ ([^:\s]+):\d* "((?:[^"\\]|\\.)*)"$')
TOKEN = re.compile(r"\$[^$\r\n]+\$|§.|\\.")
ASSET = re.compile(r'"(gfx/[^"\r\n]+\.dds)"', re.IGNORECASE)
VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?")
WEAPON_COLUMNS = tuple((
    "key;cost;power;min_damage;max_damage;hull_damage;shield_damage;shield_penetration;"
    "armor_damage;armor_penetration;min_windup;max_windup;cooldown;range;accuracy;tracking;"
    "size_damage_factor;military_power_multiplier;missile_speed;missile_evasion;"
    "missile_shield;missile_armor;missile_health;missile_retarget_range;end"
).split(";"))
WEAPON_NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)")
# This is a declaration projection, not a second P parser. Kaishek still parses P.
COMPONENT_TOKEN = re.compile(r'#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}=]|[^\s{}="#]+')
WEAPON_CSV_PATHS = frozenset("common/component_templates/" + name for name in (
    "weapon_components.csv", "mutation_weapon_components.csv"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_localization(path: Path, language: str, errors: list[dict]) -> dict[str, str]:
    data = path.read_bytes()
    if not data.startswith(b"\xef\xbb\xbf"):
        errors.append({"code": "LOCALIZATION_BOM", "path": str(path)})
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        errors.append({"code": "LOCALIZATION_ENCODING", "path": str(path)})
        return {}
    if not lines or lines[0] != f"l_{language}:":
        errors.append({"code": "LOCALIZATION_HEADER", "path": str(path)})
    entries: dict[str, str] = {}
    for number, line in enumerate(lines[1:], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = LOCALIZATION.fullmatch(line)
        if not match:
            errors.append({"code": "LOCALIZATION_SYNTAX", "path": str(path), "line": number})
            continue
        key, value = match.groups()
        if key in entries:
            errors.append({"code": "LOCALIZATION_DUPLICATE_KEY", "path": str(path), "key": key})
        if not value:
            errors.append({"code": "LOCALIZATION_EMPTY_VALUE", "path": str(path), "key": key})
        if "\ufffd" in value or re.search(r"\?{4,}", value):
            errors.append({"code": "LOCALIZATION_CHARACTER_LOSS", "path": str(path),
                           "key": key, "line": number,
                           "reason": "replacement_character" if "\ufffd" in value else "consecutive_question_marks"})
        entries[key] = value
    return entries


def read_weapon_csv(path: Path, errors: list[dict], *, native: bool = False,
                    records: dict | None = None) -> dict[str, int]:
    """Read the observed unquoted, semicolon-delimited native weapon table."""
    data = path.read_bytes()
    if not native and data.startswith(b"\xef\xbb\xbf"):
        errors.append({"code": "WEAPON_CSV_BOM", "path": str(path)})
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        errors.append({"code": "WEAPON_CSV_ENCODING", "path": str(path)})
        return {}
    rows = [(number, line.split(";")) for number, line in enumerate(lines, 1)
            if line.strip() and not line.startswith("#")]
    if not rows or tuple(rows[0][1]) != WEAPON_COLUMNS:
        errors.append({"code": "WEAPON_CSV_HEADER", "path": str(path),
                       "line": rows[0][0] if rows else 1})
        return {}
    keys: dict[str, int] = {}
    for number, row in rows[1:]:
        location = {"path": str(path), "line": number}
        if len(row) != len(WEAPON_COLUMNS):
            errors.append({"code": "WEAPON_CSV_COLUMNS", **location,
                           "expected": len(WEAPON_COLUMNS), "actual": len(row)})
            continue
        key = row[0]
        if not key or '"' in key or any(char.isspace() for char in key):
            errors.append({"code": "WEAPON_CSV_KEY", **location, "key": key})
            continue
        if key in keys:
            errors.append({"code": "WEAPON_CSV_DUPLICATE_KEY", **location,
                           "key": key, "first_line": keys[key]})
        keys[key] = number
        if records is not None:
            records[key] = {"line": number, "values": dict(zip(WEAPON_COLUMNS, row))}
        if row[-1]:
            errors.append({"code": "WEAPON_CSV_END", **location, "key": key})
        if native:
            continue  # Native tables supply reference keys, not Mod numeric acceptance.
        for column, value in zip(WEAPON_COLUMNS[1:-1], row[1:-1]):
            if value and (not WEAPON_NUMBER.fullmatch(value) or not math.isfinite(float(value))):
                errors.append({"code": "WEAPON_CSV_NUMBER", **location,
                               "key": key, "column": column, "value": value})
    return keys


def weapon_component_keys(path: Path, errors: list[dict], *, type_filter: str | None = None) -> list[tuple[str, int]]:
    """Project direct literal keys from root weapon_component_template blocks."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        # The package's existing P encoding check diagnoses Mod scripts separately.
        errors.append({"code": "WEAPON_COMPONENT_ENCODING", "path": str(path)})
        return []
    matches = [match for match in COMPONENT_TOKEN.finditer(text) if not match[0].startswith("#")]
    tokens = [match[0] for match in matches]
    result: list[tuple[str, int]] = []
    depth = 0
    active = False
    keys: list[str | None] = []
    types: list[str | None] = []
    block_line = 1
    for index, token in enumerate(tokens):
        if token == "{":
            if depth == 0 and tokens[max(0, index - 2):index] == ["weapon_component_template", "="]:
                active = True
                keys = []
                types = []
                block_line = text.count("\n", 0, matches[index].start()) + 1
            depth += 1
        elif token == "}":
            depth -= 1
            if depth == 0 and active:
                if type_filter is not None and type_filter not in types:
                    active = False
                    continue
                if len(keys) != 1 or keys[0] is None:
                    errors.append({"code": "WEAPON_COMPONENT_KEY_UNSUPPORTED", "path": str(path),
                                   "line": block_line,
                                   "reason": "requires one direct literal key; variables are not evaluated"})
                else:
                    result.append((keys[0], block_line))
                active = False
        elif active and depth == 1 and token in {"key", "type"} and tokens[index + 1:index + 2] == ["="]:
            value = tokens[index + 2] if index + 2 < len(tokens) else ""
            if value.startswith('"') and value.endswith('"') and "\\" not in value:
                value = value[1:-1]
            elif '"' in value or value.startswith("@") or value in {"{", "}", "="}:
                value = ""
            (keys if token == "key" else types).append(value or None)
    return result


def direct_component_fields(tokens: list[str]) -> dict[str, list[list[str]]]:
    """Retain direct field values, skipping each nested value as a whole."""
    fields: dict[str, list[list[str]]] = {}
    index = 0
    while index < len(tokens):
        if index + 2 >= len(tokens) or tokens[index + 1] != "=":
            index += 1
            continue
        name, start = tokens[index], index + 2
        end = start + 1
        if tokens[start] == "{":
            depth = 1
            while end < len(tokens) and depth:
                depth += (tokens[end] == "{") - (tokens[end] == "}")
                end += 1
        fields.setdefault(name, []).append(tokens[start:end])
        index = end
    return fields


def planet_killer_numeric_declarations(path: Path, errors: list[dict]) -> list[dict]:
    """Project literal PK declarations and direct values; no variables or expansion."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        errors.append({"code": "PLANET_KILLER_NUMERIC_ENCODING", "path": str(path)})
        return []
    matches = [m for m in COMPONENT_TOKEN.finditer(text) if not m[0].startswith("#")]
    tokens = [m[0] for m in matches]
    depth, start = 0, None
    records = []
    for index, token in enumerate(tokens):
        if token == "{":
            if depth == 0 and tokens[max(0, index - 2):index] == ["weapon_component_template", "="]:
                start = index
            depth += 1
        elif token == "}":
            depth -= 1
            if depth == 0 and start is not None:
                fields = direct_component_fields(tokens[start + 1:index])
                types = fields.get("type", [])
                if any(value in (["planet_killer"], ['"planet_killer"']) for value in types):
                    keys = fields.get("key", [])
                    key = keys[0][0] if len(keys) == 1 and len(keys[0]) == 1 else ""
                    if key.startswith('"') and key.endswith('"') and "\\" not in key:
                        key = key[1:-1]
                    location = {"path": str(path.resolve()), "line": text.count("\n", 0, matches[start].start()) + 1}
                    if not key or key.startswith("@") or any(c in key for c in '\\"{}=') or len(types) != 1:
                        errors.append({"code": "PLANET_KILLER_NUMERIC_DECLARATION", **location,
                                       "reason": "requires one literal key and one direct planet_killer type"})
                    else:
                        records.append({"key": key, **location, "fields": fields})
                start = None
    return records


def check_planet_killer_numeric(package: Path, game: Path, errors: list[dict]) -> dict:
    """Resolve only four literal PK values from supported static source shapes."""
    components: dict[str, dict] = {}
    duplicates: set[str] = set()
    for path in sorted((package / "common/component_templates").rglob("*")):
        if path.is_file() and path.suffix.lower() == ".txt":
            for record in planet_killer_numeric_declarations(path, errors):
                key = record["key"]
                if key in components:
                    duplicates.add(key)
                    errors.append({"code": "PLANET_KILLER_NUMERIC_DUPLICATE_KEY", "key": key,
                                   "path": record["path"], "line": record["line"]})
                components[key] = record
    summary = {"planet_killer_numeric_contract": "native_csv_or_literal_txt_v1",
               "planet_killer_numeric_components": len(components), "planet_killer_numeric_resolved": 0,
               "planet_killer_numeric_applicability": "checked" if components else "not_applicable_no_planet_killer_components",
               "planet_killer_numeric_sources": []}
    if not components:
        return summary
    tables: dict[str, list[dict]] = {}
    mod_tables = {p.relative_to(package).as_posix().casefold(): p
                  for p in (package / "common/component_templates").rglob("*") if p.is_file() and p.suffix.lower() == ".csv"}
    native_tables = {p.relative_to(game).as_posix().casefold(): p
                     for p in (game / "common/component_templates").rglob("*") if p.is_file() and p.suffix.lower() == ".csv"}
    for relative in sorted(WEAPON_CSV_PATHS):
        path = mod_tables.get(relative, native_tables.get(relative))
        if path is None:
            continue
        kind = "mod_fixed_csv" if relative in mod_tables else "native_fixed_csv"
        rows: dict = {}
        reference_errors: list[dict] = []
        read_weapon_csv(path, reference_errors, native=kind == "native_fixed_csv", records=rows)
        if reference_errors:
            for error in reference_errors:
                errors.append({**error, "code": "PLANET_KILLER_NUMERIC_CSV_REFERENCE", "cause": error["code"]})
            continue
        for key, row in rows.items():
            if key in components:
                tables.setdefault(key, []).append({"kind": kind, "path": str(path.resolve()),
                                                   "line": row["line"], "values": row["values"]})
    def number(value: list[str]) -> float | None:
        if len(value) != 1 or not WEAPON_NUMBER.fullmatch(value[0]):
            return None
        parsed = float(value[0])
        return parsed if math.isfinite(parsed) else None
    for key, component in sorted(components.items()):
        if key in duplicates:
            continue
        sources = tables.get(key, [])
        if len(sources) > 1:
            errors.append({"code": "PLANET_KILLER_NUMERIC_AMBIGUOUS", "key": key,
                           "paths": [source["path"] for source in sources]})
            continue
        if sources:
            source = sources[0]
            cells = source["values"]
            values = {name: number([cells[column]]) for name, column in (
                ("windup_min", "min_windup"), ("windup_max", "max_windup"),
                ("total_fire_time", "cooldown"), ("power", "power"))}
        else:
            source = {name: component[name] for name in ("path", "line")}
            source["kind"] = "literal_component_txt"
            fields = component["fields"]
            windups = fields.get("windup", [])
            windup = windups[0] if len(windups) == 1 else []
            bounds = direct_component_fields(windup[1:-1]) if windup[:1] == ["{"] and windup[-1:] == ["}"] else {}
            values = {}
            for name, candidates in (("windup_min", bounds.get("min", [])), ("windup_max", bounds.get("max", [])),
                                     ("total_fire_time", fields.get("total_fire_time", [])), ("power", fields.get("power", []))):
                values[name] = number(candidates[0]) if len(candidates) == 1 else None
            if set(bounds) != {"min", "max"} or len(windup) != 8:
                values["windup_min"] = values["windup_max"] = None
        invalid = False
        for field, value in values.items():
            if value is None or (field != "power" and value < 0):
                errors.append({"code": "PLANET_KILLER_NUMERIC_FIELD", "key": key, "field": field,
                               "path": source["path"], "line": source["line"],
                               "reason": "requires one finite direct decimal; timing values must be nonnegative"})
                invalid = True
        if not invalid:
            summary["planet_killer_numeric_sources"].append({"key": key, "kind": source["kind"],
                "path": source["path"], "line": source["line"], "sha256": sha256(Path(source["path"])), "values": values})
    summary["planet_killer_numeric_resolved"] = len(summary["planet_killer_numeric_sources"])
    return summary


def on_action_block_names(path: Path, errors: list[dict]) -> set[str]:
    """Project root block names only; comments, strings and nested names are not callbacks."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        errors.append({"code": "PLANET_KILLER_CALLBACK_ENCODING", "path": str(path)})
        return set()
    tokens = [match[0] for match in COMPONENT_TOKEN.finditer(text) if not match[0].startswith("#")]
    names: set[str] = set()
    depth = 0
    for index, token in enumerate(tokens):
        if token == "{":
            if depth == 0 and index >= 2 and tokens[index - 1] == "=":
                name = tokens[index - 2]
                if name.startswith('"') and name.endswith('"') and "\\" not in name:
                    name = name[1:-1]
                names.add(name)
            depth += 1
        elif token == "}":
            depth -= 1
    return names


def check_planet_killer_callbacks(package: Path, game: Path, errors: list[dict]) -> dict:
    """Require only the three observed native callbacks for literal planet-killer keys."""
    components: dict[str, dict] = {}
    for path in sorted((package / "common/component_templates").rglob("*")):
        if path.is_file() and path.suffix.lower() == ".txt":
            for key, line in weapon_component_keys(path, errors, type_filter="planet_killer"):
                components[key] = {"path": str(path), "line": line}
    summary = {
        "planet_killer_callback_contract": "native_completed_queued_unqueued_v1",
        "planet_killer_components": len(components),
        "planet_killer_callbacks_required": len(components) * 3,
        "planet_killer_callbacks_resolved": 0,
        "planet_killer_callback_applicability": "checked" if components else "not_applicable_no_planet_killer_components",
    }
    if not components:
        return summary
    action_root = Path("common/on_actions")
    mod_files = sorted(path for path in (package / action_root).rglob("*")
                       if path.is_file() and path.suffix.lower() == ".txt")
    hidden = {path.relative_to(package).as_posix().casefold() for path in mod_files}
    native_files = sorted(path for path in (game / action_root).rglob("*")
                          if path.is_file() and path.suffix.lower() == ".txt"
                          and path.relative_to(game).as_posix().casefold() not in hidden)
    defined: set[str] = set()
    for path in [*mod_files, *native_files]:
        defined.update(on_action_block_names(path, errors))
    for key, location in sorted(components.items()):
        for suffix in ("", "_queued", "_unqueued"):
            callback = f"on_destroy_planet_with_{key}{suffix}"
            if callback in defined:
                summary["planet_killer_callbacks_resolved"] += 1
            else:
                errors.append({"code": "PLANET_KILLER_CALLBACK_MISSING", **location,
                               "key": key, "callback": callback})
    return summary


def check_planet_killer_message_localization(package: Path, game: Path, locales: dict,
                                             languages: list[str], errors: list[dict]) -> dict:
    """Resolve the observed native destruction-description key, not message execution."""
    components = {}
    for path in sorted((package / "common/component_templates").rglob("*")):
        if not path.is_file() or path.suffix.lower() != ".txt":
            continue
        for key, line in weapon_component_keys(path, errors, type_filter="planet_killer"):
            components[key] = {"path": str(path), "line": line}
    resolved = []
    for language in languages:
        values = locales.get(language, {})
        needed = {"MESSAGE_DESC_FOR_" + key for key in components} - set(values)
        native = {}
        for path in sorted((game / "localisation" / language).rglob("*.yml")) if needed else []:
            text = path.read_text(encoding="utf-8-sig")
            for name in list(needed):
                match = re.search(r'^\s*' + re.escape(name) + r':\d*\s+"((?:[^"\\]|\\.)*)"', text, re.M)
                if match:
                    native[name] = (match[1], str(path))
                    needed.remove(name)
            if not needed:
                break
        for key, location in sorted(components.items()):
            name = "MESSAGE_DESC_FOR_" + key
            value = values.get(name) if name in values else native.get(name, (None, None))[0]
            if value is None:
                errors.append({"code": "PLANET_KILLER_MESSAGE_LOCALIZATION_MISSING", **location,
                               "key": key, "localization_key": name, "language": language})
            elif not value.strip() or value.strip() in {name, "$" + name + "$"}:
                errors.append({"code": "PLANET_KILLER_MESSAGE_LOCALIZATION_INVALID", **location,
                               "key": key, "localization_key": name, "language": language})
            else:
                resolved.append({"key": key, "localization_key": name, "language": language,
                                 "source": "mod" if name in values else "native",
                                 **({"native_path": native[name][1]} if name not in values else {})})
    return {"planet_killer_message_localization_contract": "native_destroy_description_v1",
            "planet_killer_message_localization_applicability": "checked" if components else "not_applicable_no_planet_killer_components",
            "planet_killer_message_localization_required": len(components) * len(languages),
            "planet_killer_message_localization_resolved": len(resolved),
            "planet_killer_message_localization_sources": resolved}


def check_weapon_csv(package: Path, game: Path, errors: list[dict], *, literal_stat_keys: set[str] | None = None) -> dict:
    """Check Mod tables and literal key associations; do not execute weapon semantics."""
    component_root = Path("common/component_templates")
    def files(root: Path, suffix: str) -> list[Path]:
        return sorted(path for path in (root / component_root).rglob("*")
                      if path.is_file() and path.suffix.lower() == suffix)

    tables = files(package, ".csv")
    summary = {"weapon_csv_files": len(tables), "weapon_csv_keys": 0,
               "weapon_csv_applicability": "checked" if tables else "not_applicable_no_weapon_csv_files",
               "weapon_csv_loader_contract": "native_fixed_paths_v1", "weapon_csv_unsupported_files": 0}
    if not tables:
        return summary
    mod_keys: dict[str, dict] = {}
    for path in tables:
        if path.relative_to(package).as_posix().casefold() not in WEAPON_CSV_PATHS:
            summary["weapon_csv_unsupported_files"] += 1
            errors.append({"code": "WEAPON_CSV_UNSUPPORTED_PATH", "path": str(path),
                           "reason": "only the two fixed native weapon CSV paths are supported; syntax is still checked"})
        for key, line in read_weapon_csv(path, errors).items():
            location = {"path": str(path), "line": line}
            if key in mod_keys:
                errors.append({"code": "WEAPON_CSV_DUPLICATE_KEY", **location,
                               "key": key, "first_path": mod_keys[key]["path"]})
            mod_keys[key] = location
    summary["weapon_csv_keys"] = len(mod_keys)
    mod_scripts = files(package, ".txt")
    hidden = {path.relative_to(package).as_posix().casefold() for path in [*tables, *mod_scripts]}
    native_keys: set[str] = set()
    native_definitions: set[str] = set()
    native_errors: list[dict] = []
    for path in files(game, ".csv"):
        if path.relative_to(game).as_posix().casefold() in WEAPON_CSV_PATHS and path.relative_to(game).as_posix().casefold() not in hidden:
            native_keys.update(read_weapon_csv(path, native_errors, native=True))
    for path in files(game, ".txt"):
        if path.relative_to(game).as_posix().casefold() not in hidden:
            native_definitions.update(key for key, _ in weapon_component_keys(path, native_errors))
    summary["weapon_csv_native_unexpanded_templates"] = sum(
        error["code"] == "WEAPON_COMPONENT_KEY_UNSUPPORTED" for error in native_errors)
    for error in native_errors:
        if error["code"] != "WEAPON_COMPONENT_KEY_UNSUPPORTED":
            errors.append({**error, "code": "WEAPON_CSV_GAME_REFERENCE", "cause": error["code"]})
    mod_definitions: dict[str, dict] = {}
    for path in mod_scripts:
        for key, line in weapon_component_keys(path, errors):
            location = {"path": str(path), "line": line}
            if key in mod_definitions:
                errors.append({"code": "WEAPON_COMPONENT_DUPLICATE_KEY", **location, "key": key})
            mod_definitions[key] = location
    for key in sorted(mod_keys.keys() - mod_definitions.keys() - native_definitions):
        errors.append({"code": "WEAPON_CSV_COMPONENT_MISSING", **mod_keys[key], "key": key})
    for key in sorted(mod_definitions.keys() - mod_keys.keys() - native_keys - (literal_stat_keys or set())):
        errors.append({"code": "WEAPON_COMPONENT_STATS_MISSING", **mod_definitions[key], "key": key})
    return summary


def check(mod: Path, game: Path, expected_sha: str, cli: Path, version_source: Path | None = None) -> dict:
    errors: list[dict] = []
    package = mod / "mod" if (mod / "mod/descriptor.mod").is_file() else mod
    descriptor = package / "descriptor.mod"
    exe = game / "stellaris.exe"
    game_sha = sha256(exe) if exe.is_file() else None
    if game_sha is None or game_sha.lower() != expected_sha.lower():
        errors.append({"code": "GAME_EXE_IDENTITY", "path": str(exe)})
    if not cli.is_file():
        errors.append({"code": "KAISHEK_CLI_MISSING", "path": str(cli)})
    version_file = version_source or (mod / "VERSION" if (mod / "VERSION").is_file() else package / "VERSION")
    if not version_file.is_file() or not descriptor.is_file():
        errors.append({"code": "MOD_METADATA_MISSING", "path": str(mod)})
    else:
        version = version_file.read_text(encoding="utf-8-sig").strip()
        text = descriptor.read_text(encoding="utf-8-sig")
        match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        supported = re.search(r'^supported_version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        if not VERSION.fullmatch(version) or not match or match.group(1) != version or not supported:
            errors.append({"code": "MOD_VERSION_CONTRACT", "path": str(descriptor)})
        settings_file = game / "launcher-settings.json"
        if supported and settings_file.is_file():
            settings = json.loads(settings_file.read_text(encoding="utf-8-sig"))
            actual = settings.get("rawVersion", "").removeprefix("v").split(".")
            declared = supported.group(1).split(".")
            if not actual or not all(part == "*" or (index < len(actual) and part == actual[index])
                                     for index, part in enumerate(declared)):
                errors.append({"code": "MOD_SUPPORTED_VERSION", "path": str(descriptor),
                               "declared": supported.group(1), "game": settings.get("rawVersion")})
    script_files = sorted(
        path for path in package.rglob("*")
        if path.is_file() and (path.suffix.lower() in {".txt", ".gfx", ".gui", ".asset"} or path.name == "descriptor.mod")
    )
    parsed = 0
    scope_sources: list[tuple[Path, str]] = []
    if not script_files:
        errors.append({"code": "NO_P_SCRIPTS", "path": str(package)})
    for path in script_files:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append({"code": "P_SCRIPT_BOM", "path": str(path)})
            continue
        try:
            source = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append({"code": "P_SCRIPT_ENCODING", "path": str(path)})
            continue
        scope_sources.append((path, source))
        if cli.is_file():
            command = ["java", "-jar", str(cli), "parse", "--file", str(path)]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
            try:
                payload = json.loads(result.stdout)
            except json.JSONDecodeError:
                errors.append({"code": "KAISHEK_RESPONSE", "path": str(path)})
                continue
            if result.returncode or payload.get("status") != "PARSED" or payload.get("diagnostics") or not payload.get("roundTrip"):
                errors.append({"code": "P_SCRIPT_PARSE", "path": str(path), "diagnostics": payload.get("diagnostics", [])})
            else:
                parsed += 1
        for asset in ASSET.findall(source):
            relative = Path(asset)
            if not (package / relative).is_file() and not (game / relative).is_file():
                errors.append({"code": "ASSET_REFERENCE_MISSING", "path": str(path), "asset": asset})
    finite_scope = population_scope_preflight(package, game, scope_sources, game_sha)
    errors.extend(finite_scope["diagnostics"])
    finite_values = script_value_shape_preflight(package, game, scope_sources, game_sha)
    errors.extend(finite_values["diagnostics"])
    dds = sorted(package.rglob("*.dds"))
    for path in dds:
        if len(path.read_bytes()) < 128 or not path.read_bytes().startswith(b"DDS "):
            errors.append({"code": "DDS_HEADER", "path": str(path)})
    game_languages = sorted(path.name for path in (game / "localisation").iterdir() if path.is_dir()) if (game / "localisation").is_dir() else []
    if not game_languages:
        errors.append({"code": "GAME_LANGUAGES_MISSING", "path": str(game / "localisation")})
    locales: dict[str, dict[str, str]] = {}
    localization_root = package / "localisation"
    has_localization = any(localization_root.rglob("*.yml"))
    for language in game_languages if has_localization else []:
        files = sorted(localization_root.rglob(f"*_l_{language}.yml"))
        if not files:
            errors.append({"code": "LOCALIZATION_LANGUAGE_MISSING", "language": language})
            continue
        values: dict[str, str] = {}
        for path in files:
            for key, value in read_localization(path, language, errors).items():
                if key in values:
                    errors.append({"code": "LOCALIZATION_DUPLICATE_KEY", "language": language, "key": key})
                values[key] = value
        locales[language] = values
    if "simp_chinese" in locales:
        reference = locales["simp_chinese"]
        for language, values in locales.items():
            missing = sorted(set(reference) - set(values))
            extra = sorted(set(values) - set(reference))
            if missing or extra:
                errors.append({"code": "LOCALIZATION_KEY_SET", "language": language, "missing": missing, "extra": extra})
            for key in set(values) & set(reference):
                if Counter(TOKEN.findall(values[key])) != Counter(TOKEN.findall(reference[key])):
                    errors.append({"code": "LOCALIZATION_TOKEN_DRIFT", "language": language, "key": key})
                if language != "simp_chinese" and values[key] == reference[key] and re.search(r"[\u4e00-\u9fff]", values[key]):
                    errors.append({"code": "LOCALIZATION_CHINESE_PLACEHOLDER", "language": language, "key": key})
    planet_killer_numeric = check_planet_killer_numeric(package, game, errors)
    literal_stat_keys = {source["key"] for source in planet_killer_numeric["planet_killer_numeric_sources"]
                         if source["kind"] == "literal_component_txt"}
    weapon_csv = check_weapon_csv(package, game, errors, literal_stat_keys=literal_stat_keys)
    planet_killer_callbacks = check_planet_killer_callbacks(package, game, errors)
    planet_killer_messages = check_planet_killer_message_localization(package, game, locales, game_languages, errors)
    return {
        "status": "PASS" if not errors else "FAIL",
        "game_exe_sha256": game_sha,
        "p_scripts": len(script_files), "p_parsed": parsed, "dds": len(dds),
        "languages": game_languages,
        "localization_keys": len(locales.get("simp_chinese", {})),
        "localization_applicability": "checked" if has_localization else "not_applicable_no_localization_files",
        **weapon_csv,
        **planet_killer_callbacks,
        **planet_killer_messages,
        **planet_killer_numeric,
        "finite_scope_preflight": finite_scope,
        "finite_script_value_preflight": finite_values,
        "semantic_scope": "syntax/package including supported fixed weapon CSV paths, literal planet-killer numeric sources, callback existence and derived destruction-description localization plus explicitly registered finite population scopes and referenced script-value shapes only; native loading, phase timing, runtime, recursive expansion and other opcodes require Stellaris tests",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod", required=True, type=Path)
    parser.add_argument("--game", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expected-exe-sha256", default=CYGNUS_451_SHA256)
    parser.add_argument("--cli", type=Path, default=CLI)
    parser.add_argument("--version-file", type=Path, help="explicit VERSION source for a package in a multi-Mod repository")
    args = parser.parse_args()
    result = check(args.mod.resolve(), args.game.resolve(), args.expected_exe_sha256, args.cli.resolve(),
                   args.version_file.resolve() if args.version_file else None)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "p_scripts", "p_parsed", "dds", "localization_keys")}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
