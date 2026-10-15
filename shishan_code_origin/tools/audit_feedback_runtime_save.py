"""Read native Stellaris saves without launching or modifying the game.

This inspects saved data and independently recomputes weighted trait counts.
It does not emulate script execution, generate a fixture save, or certify UI.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile


class AuditError(ValueError):
    """A native save cannot be interpreted unambiguously."""


@dataclass(frozen=True)
class Block:
    start: int
    end: int


@dataclass(frozen=True)
class Entry:
    key: str | None
    value: str | Block


class Document:
    """A shallow P-data reader: nested blocks retain offsets into one string.

    Anonymous blocks and bare list values are preserved. Strings and comments
    are scanned before braces; nested occurrences cannot impersonate fields.
    """

    def __init__(self, text: str):
        self.text = text
        self.root = Block(0, len(text))
        self.cache: dict[Block, list[Entry]] = {}

    def whitespace(self, position: int, end: int) -> int:
        while position < end:
            if self.text[position].isspace():
                position += 1
            elif self.text[position] == "#":
                newline = self.text.find("\n", position, end)
                position = end if newline < 0 else newline + 1
            else:
                break
        return position

    def quoted_end(self, position: int, end: int) -> int:
        start = position
        position += 1
        while position < end:
            if self.text[position] == "\\":
                position += 2
            elif self.text[position] == '"':
                return position + 1
            else:
                position += 1
        raise AuditError(f"unclosed quoted string at offset {start}")

    def block_end(self, position: int, end: int) -> int:
        start, depth = position, 0
        while position < end:
            char = self.text[position]
            if char == '"':
                position = self.quoted_end(position, end)
            elif char == "#":
                newline = self.text.find("\n", position, end)
                position = end if newline < 0 else newline + 1
            else:
                depth += (char == "{") - (char == "}")
                position += 1
                if depth == 0:
                    return position
        raise AuditError(f"unclosed block at offset {start}")

    def token(self, position: int, end: int) -> tuple[str | Block, int]:
        position = self.whitespace(position, end)
        if position == end:
            raise AuditError("missing token at end of block")
        char = self.text[position]
        if char == "{":
            after = self.block_end(position, end)
            return Block(position + 1, after - 1), after
        if char == '"':
            after = self.quoted_end(position, end)
            raw = self.text[position + 1:after - 1]
            return re.sub(r'\\(["\\])', r"\1", raw), after
        if char in "}=":
            raise AuditError(f"unexpected {char!r} at offset {position}")
        after = position
        while after < end and not self.text[after].isspace() and self.text[after] not in '{}=#"':
            after += 1
        if after == position:
            raise AuditError(f"invalid token at offset {position}")
        return self.text[position:after], after

    def entries(self, source: Block | None = None) -> list[Entry]:
        source = self.root if source is None else source
        if source in self.cache:
            return self.cache[source]
        result, position = [], source.start
        while True:
            position = self.whitespace(position, source.end)
            if position == source.end:
                break
            first, position = self.token(position, source.end)
            position = self.whitespace(position, source.end)
            if isinstance(first, str) and position < source.end and self.text[position] == "=":
                value, position = self.token(position + 1, source.end)
                result.append(Entry(first, value))
            else:
                result.append(Entry(None, first))
        self.cache[source] = result
        return result

    def values(self, source: Block, key: str) -> list[str | Block]:
        return [entry.value for entry in self.entries(source) if entry.key == key]

    def field(self, source: Block, key: str, required: bool = True):
        found = self.values(source, key)
        if len(found) > 1:
            raise AuditError(f"duplicate {key} at offset {source.start}")
        if not found:
            if required:
                raise AuditError(f"missing {key} at offset {source.start}")
            return None
        return found[0]

    def section(self, source: Block, key: str, required: bool = True) -> Block | None:
        value = self.field(source, key, required)
        if value is None:
            return None
        if not isinstance(value, Block):
            raise AuditError(f"expected block {key}, got {value!r}")
        return value

    def scalar(self, source: Block, key: str, required: bool = True) -> str | None:
        value = self.field(source, key, required)
        if isinstance(value, Block):
            raise AuditError(f"expected scalar {key}")
        return value

    def native(self, value: str | Block):
        if isinstance(value, str):
            return value
        entries = self.entries(value)
        if all(entry.key is None for entry in entries):
            return [self.native(entry.value) for entry in entries]
        result = []
        # A list of pairs retains duplicate native keys and mixed bare entries.
        for entry in entries:
            result.append({"key": entry.key, "value": self.native(entry.value)})
        return result


def decimal(text: str | None, context: str) -> Decimal:
    try:
        result = Decimal(text)
    except (InvalidOperation, TypeError) as error:
        raise AuditError(f"non-numeric {context}: {text!r}") from error
    if not result.is_finite():
        raise AuditError(f"non-finite {context}: {text!r}")
    return result


def integer(text: str | None, context: str) -> int:
    result = decimal(text, context)
    if result != result.to_integral_value() or result < 0:
        raise AuditError(f"nonnegative integer required for {context}: {text!r}")
    return int(result)


def numeric_database(doc: Document, source: Block, context: str) -> dict[int, Block]:
    result = {}
    for entry in doc.entries(source):
        if entry.key is None:
            raise AuditError(f"unexpected bare member in {context}")
        index = integer(entry.key, context + " ID")
        if index in result:
            raise AuditError(f"duplicate {context} ID {index}")
        if isinstance(entry.value, Block):
            result[index] = entry.value
        elif entry.value != "none":
            raise AuditError(f"unrecognized {context} entry {index}={entry.value}")
    return result


def integer_list(doc: Document, source: Block, context: str) -> list[int]:
    result = []
    for entry in doc.entries(source):
        if entry.key is not None or not isinstance(entry.value, str):
            raise AuditError(f"expected bare ID list for {context}")
        result.append(integer(entry.value, context))
    if len(result) != len(set(result)):
        raise AuditError(f"duplicate IDs in {context}")
    return result


def required_record(database: dict[int, Block], index: int, context: str) -> Block:
    if index not in database:
        raise AuditError(f"missing {context} record {index}")
    return database[index]


def mod_fields(doc: Document, source: Block | None) -> dict:
    result = {}
    if source is None:
        return result
    for entry in doc.entries(source):
        if entry.key and entry.key.startswith("shishan_code_"):
            if entry.key in result:
                raise AuditError(f"duplicate Mod field {entry.key}")
            result[entry.key] = doc.native(entry.value)
    return result


def locate_player(doc: Document) -> tuple[int, Block, dict]:
    players = doc.section(doc.root, "player")
    ids = []
    for entry in doc.entries(players):
        if entry.key is not None or not isinstance(entry.value, Block):
            raise AuditError("unsupported player record layout")
        country = integer(doc.scalar(entry.value, "country"), "player country")
        ids.append(country)
    if len(ids) != 1:
        raise AuditError(f"expected one unambiguous player country, got {ids}")
    countries = numeric_database(doc, doc.section(doc.root, "country"), "country")
    actor = required_record(countries, ids[0], "country")
    return ids[0], actor, {"source": "player[].country", "country_id": ids[0]}


def locate_main_species(doc: Document, actor: Block) -> tuple[int, str]:
    # The rights primary row can retain the old template after the engine
    # changes dominant species. Never substitute it for this country pointer.
    index = integer(doc.scalar(actor, "founder_species_ref"), "country founder species reference")
    return index, "country.founder_species_ref"


def main_species_evidence(doc: Document, actor: Block) -> dict:
    modules = doc.section(actor, "modules", False)
    rights = doc.section(modules, "standard_species_rights_module", False) if modules else None
    primary = doc.section(rights, "primary", False) if rights else None
    defaults = doc.section(actor, "default_species", False)
    owned = doc.section(actor, "owned_species_refs", False)
    return {
        "founder_species_ref": doc.scalar(actor, "founder_species_ref"),
        "rights_primary_species_index": doc.scalar(primary, "species_index", False) if primary else None,
        "rights_primary_raw": doc.native(primary) if primary else None,
        "default_species_raw": doc.native(defaults) if defaults else None,
        "owned_species_refs_raw": doc.native(owned) if owned else None,
        "interpretation": "main template uses country.founder_species_ref; rights primary and cached species references are independent saved fields, not resolved rights or substitute main pointers",
    }


def species_records(doc: Document) -> dict[int, dict]:
    database = numeric_database(doc, doc.section(doc.root, "species_db"), "species")
    records = {}
    for index, source in database.items():
        traits_source = doc.section(source, "traits")
        traits = []
        for entry in doc.entries(traits_source):
            if entry.key != "trait" or not isinstance(entry.value, str):
                raise AuditError(f"unknown formal trait layout in species {index}")
            traits.append(entry.value)
        identity = {entry.key: doc.native(entry.value) for entry in doc.entries(source) if entry.key and "identity" in entry.key}
        if identity:
            raise AuditError(f"species {index} uses unsupported explicit identity fields: {identity}")
        parent = doc.scalar(source, "base_ref", False)
        records[index] = {
            "id": index, "base_ref": integer(parent, f"species {index} base_ref") if parent is not None else None,
            "raw_trait_keys": traits, "distinct_trait_keys": sorted(set(traits)),
            "distinct_trait_count": len(set(traits)), "duplicate_trait_keys": sorted({key for key in traits if traits.count(key) > 1}),
        }
    for index in records:
        current, chain = index, []
        while True:
            if current in chain:
                raise AuditError(f"cyclic species base_ref chain {chain + [current]}")
            if current not in records:
                raise AuditError(f"species {index} base_ref chain references missing species {current}")
            chain.append(current)
            parent = records[current]["base_ref"]
            if parent is None or parent == current:
                break
            current = parent
        records[index]["base_ref_chain"] = chain
        records[index]["lineage_root"] = chain[-1]
    return records


def native_modifiers(doc: Document, actor: Block) -> list[dict]:
    timed = doc.section(actor, "timed_modifier", False)
    if timed is None:
        return []
    items = doc.section(timed, "items")
    result = []
    for entry in doc.entries(items):
        if entry.key is not None or not isinstance(entry.value, Block):
            raise AuditError("unsupported timed_modifier.items layout")
        name = doc.scalar(entry.value, "modifier")
        if name.startswith("shishan_code_"):
            multiplier = doc.scalar(entry.value, "multiplier", False)
            result.append({
                "modifier": name, "multiplier_raw": multiplier,
                "effective_multiplier": str(decimal(multiplier, "modifier multiplier")) if multiplier is not None else "1",
                "days": doc.scalar(entry.value, "days", False),
                "native_fields": doc.native(entry.value),
            })
    return result


def native_projects(doc: Document, actor: Block) -> list[dict]:
    events = doc.section(actor, "events", False)
    if events is None:
        return []
    result = []
    for source in doc.values(events, "special_project"):
        if not isinstance(source, Block):
            raise AuditError("unsupported country special project layout")
        name = doc.scalar(source, "special_project")
        if name.startswith("SHISHAN_CODE_"):
            result.append({
                "key": name, "id": integer(doc.scalar(source, "id"), "special project ID"),
                "status": doc.scalar(source, "status", False),
                "native_fields": doc.native(source),
            })
    return result


def inspect_populations(doc: Document, actor: Block, actor_id: int, species: dict, main_species: int) -> dict:
    owned = integer_list(doc, doc.section(actor, "owned_planets"), "owned colony IDs")
    colonies = numeric_database(doc, doc.section(doc.root, "colony"), "colony")
    planets_wrapper = doc.section(doc.root, "planets")
    planets = numeric_database(doc, doc.section(planets_wrapper, "planet"), "physical planet")
    groups = numeric_database(doc, doc.section(doc.root, "pop_groups"), "pop group")
    if main_species not in species:
        raise AuditError(f"primary species {main_species} missing from species_db")
    main_root = species[main_species]["lineage_root"]
    ownership = []
    listed_groups = set()
    for colony_id in owned:
        colony = required_record(colonies, colony_id, "owned colony")
        carrier = doc.section(colony, "carrier")
        kind = doc.scalar(carrier, "type")
        reference = integer(doc.scalar(carrier, "reference"), "colony carrier reference")
        if kind != "planet":
            raise AuditError(f"owned colony {colony_id} uses unsupported carrier type {kind!r}; cannot infer domestic ownership")
        physical = required_record(planets, reference, "carrier planet")
        owner = integer(doc.scalar(physical, "owner"), "physical carrier owner")
        if owner != actor_id:
            raise AuditError(f"owned colony {colony_id} carrier planet {reference} belongs to country {owner}, expected {actor_id}")
        if integer(doc.scalar(physical, "colony"), "physical planet colony") != colony_id:
            raise AuditError(f"colony {colony_id} / physical planet {reference} reverse link mismatch")
        group_ids = integer_list(doc, doc.section(colony, "pop_groups"), f"colony {colony_id} population group list")
        if listed_groups.intersection(group_ids):
            raise AuditError("one population group appears in multiple owned colonies")
        listed_groups.update(group_ids)
        ownership.append({"colony_id": colony_id, "carrier_type": kind, "carrier_reference": reference, "carrier_owner": owner, "listed_pop_groups": group_ids})
    included, excluded, by_species = [], [], {}
    found_groups, denominator, numerator = set(), 0, 0
    foreign_count = 0
    for group_id, source in groups.items():
        colony_id = integer(doc.scalar(source, "planet"), f"pop group {group_id} colony pointer")
        if colony_id not in colonies:
            raise AuditError(f"pop group {group_id} references unknown colony {colony_id}")
        if colony_id not in owned:
            foreign_count += 1
            if group_id in listed_groups:
                raise AuditError(f"listed owned group {group_id} points to foreign colony {colony_id}")
            continue
        found_groups.add(group_id)
        if group_id not in listed_groups:
            raise AuditError(f"domestic group {group_id} missing from colony population list")
        key = doc.section(source, "key")
        species_id = integer(doc.scalar(key, "species"), f"pop group {group_id} species")
        if species_id not in species:
            raise AuditError(f"pop group {group_id} references missing species {species_id}")
        size = integer(doc.scalar(source, "size"), f"pop group {group_id} size")
        same_lineage = species[species_id]["lineage_root"] == main_root
        row = {"id": group_id, "colony_id": colony_id, "species_id": species_id, "category": doc.scalar(key, "category", False), "size": size, "lineage_root": species[species_id]["lineage_root"], "same_main_lineage": same_lineage, "formal_trait_count": species[species_id]["distinct_trait_count"]}
        if size > 0 and same_lineage:
            included.append(row)
            denominator += size
            numerator += size * row["formal_trait_count"]
            summary = by_species.setdefault(species_id, {**species[species_id], "population": 0, "group_ids": []})
            summary["population"] += size
            summary["group_ids"].append(group_id)
        else:
            row["exclusion_reason"] = "zero population" if size == 0 else "foreign species lineage within actor country"
            excluded.append(row)
    if found_groups != listed_groups:
        raise AuditError(f"owned colony group list contains missing groups: {sorted(listed_groups - found_groups)}")
    fraction = Fraction(numerator, denominator) if denominator else Fraction(0)
    with localcontext() as context:
        context.prec = 35
        average = Decimal(fraction.numerator) / Decimal(fraction.denominator)
    return {
        "owned_colony_ids": owned, "ownership_links": ownership, "main_species_id": main_species,
        "main_lineage_root": main_root, "included_groups": included, "excluded_domestic_groups": excluded,
        "foreign_colony_groups_excluded": foreign_count, "populated_templates": sorted(by_species.values(), key=lambda item: item["id"]),
        "population": denominator, "trait_weight": numerator, "trait_average_exact": f"{fraction.numerator}/{fraction.denominator}",
        "trait_average_expression": f"{numerator}/{denominator}" if denominator else "0/0 (no domestic main-lineage population)",
        "trait_average_decimal": str(average), "trait_exclusion_keys": [],
        "lineage_method": "species_db base_ref chains; unsupported explicit identity fields fail closed",
    }


def expected_and_observed(populations: dict, variables: dict, flags: dict, modifiers: list[dict]) -> tuple[dict, list[dict]]:
    diagnostics = []
    legacy = {}
    legacy_extra = Decimal(0)
    for suffix in ("output", "energy", "assembly", "experience"):
        key = "shishan_code_iteration_" + suffix
        raw = variables.get(key)
        value = decimal(raw, key) if raw is not None else Decimal(0)
        legacy[key] = {"observed": raw, "missing_counter_extra_is_zero": raw is None, "extra_repeats": str(max(value - 1, Decimal(0)))}
        legacy_extra += max(value - 1, Decimal(0))
        if value < 0 or value != value.to_integral_value():
            diagnostics.append({"severity": "warning", "code": "LEGACY_COUNTER_INVALID", "key": key, "observed": raw})
    repeat_key = "shishan_code_architecture_repeat_count"
    observed_repeat = variables.get(repeat_key)
    migrated = "shishan_code_architecture_migrated" in flags
    u = decimal(populations["trait_average_decimal"], "independent U")
    expected = {"population": populations["population"], "trait_weight": populations["trait_weight"], "trait_average_exact": populations["trait_average_exact"], "trait_average": str(u), "legacy_counter_details": legacy, "legacy_extra_repeat_migration": str(legacy_extra), "migration_flag_observed": migrated}
    # R is a persisted reward history; it cannot be inferred from current traits.
    # If missing, retain null and do not invent T/M observations or post-migration R.
    repeated = decimal(observed_repeat, repeat_key) if observed_repeat is not None else None
    expected["repeat_count_basis"] = "observed persisted R" if repeated is not None else "unknown; legacy extra migration is only a historical expectation"
    t = u + repeated if repeated is not None and populations["population"] > 0 else (Decimal(0) if populations["population"] == 0 else None)
    expected["total"] = str(t) if t is not None else None
    expected["bonus"] = str(t * Decimal(".05")) if t is not None else None
    expected["diagnostic_multiplier"] = str(1 + t * Decimal(".05")) if t is not None else None
    expected["economic_route"] = "current rc additive native job-output bonus; diagnostic M is not final-output multiplication"
    targets = {
        "shishan_code_architecture_population": Decimal(populations["population"]),
        "shishan_code_architecture_trait_weight": Decimal(populations["trait_weight"]),
        "shishan_code_architecture_trait_average": u,
        "shishan_code_architecture_total": t,
        "shishan_code_architecture_bonus": t * Decimal(".05") if t is not None else None,
        "shishan_code_architecture_multiplier": 1 + t * Decimal(".05") if t is not None else None,
    }
    comparisons = {}
    for key, target in targets.items():
        observed = variables.get(key)
        status = "MISSING" if observed is None else ("EXPECTED_UNAVAILABLE" if target is None else ("MATCH" if abs(decimal(observed, key) - target) <= Decimal(".0001") else "MISMATCH"))
        comparisons[key] = {"observed": observed, "expected": str(target) if target is not None else None, "status": status}
        if status == "MISMATCH":
            diagnostics.append({"severity": "error", "code": "ARCHITECTURE_OBSERVATION_MISMATCH", "key": key, **comparisons[key]})
    jobs = [item for item in modifiers if item["modifier"] == "shishan_code_architecture_jobs"]
    if len(jobs) > 1:
        diagnostics.append({"severity": "error", "code": "DUPLICATE_ARCHITECTURE_MODIFIER", "count": len(jobs)})
    if jobs and t is not None and abs(decimal(jobs[0]["effective_multiplier"], "architecture modifier") - t) > Decimal(".0001"):
        diagnostics.append({"severity": "error", "code": "ARCHITECTURE_MODIFIER_SCALE_MISMATCH", "expected": str(t), "observed": jobs[0]["effective_multiplier"]})
    if not migrated:
        diagnostics.append({"severity": "info", "code": "MIGRATION_NOT_OBSERVED", "message": "Legacy migration expectation is not proof that the redesigned script ran."})
    expected["comparisons"] = comparisons
    return expected, diagnostics


def inspect_text(meta_text: str, game_text: str) -> dict:
    meta, doc = Document(meta_text), Document(game_text)
    version = doc.scalar(doc.root, "version")
    meta_version = meta.scalar(meta.root, "version")
    date, meta_date = doc.scalar(doc.root, "date"), meta.scalar(meta.root, "date")
    if version != meta_version or date != meta_date:
        raise AuditError(f"meta/gamestate version or date mismatch: {meta_version}/{version}, {meta_date}/{date}")
    actor_id, actor, actor_source = locate_player(doc)
    main_species, main_source = locate_main_species(doc, actor)
    species = species_records(doc)
    populations = inspect_populations(doc, actor, actor_id, species, main_species)
    variables = mod_fields(doc, doc.section(actor, "variables", False))
    flags = mod_fields(doc, doc.section(actor, "flags", False))
    modifiers = native_modifiers(doc, actor)
    expected, diagnostics = expected_and_observed(populations, variables, flags, modifiers)
    modules = doc.section(actor, "government", False)
    origin = doc.scalar(modules, "origin", False) if modules else None
    return {
        "status": "FAIL" if any(item["severity"] == "error" for item in diagnostics) else "PASS",
        "semantic_scope": "read-only native saved-data audit; no script emulation or runtime/UI certification",
        "native_version": version, "native_date": date, "meta_version": meta_version, "meta_date": meta_date,
        "redesign_observation_status": "NOT OBSERVED" if not any(key.startswith("shishan_code_architecture_") for key in variables) else "OBSERVED; see per-field comparisons",
        "actor": {**actor_source, "origin": origin, "main_species_source": main_source, "main_species_id": main_species,
                  "main_species_evidence": main_species_evidence(doc, actor)},
        "observed": {"variables": variables, "flags": flags, "modifiers": modifiers, "special_projects": native_projects(doc, actor)},
        "population": populations, "independent_expected": expected, "diagnostics": diagnostics,
        "not_run": ["game launch", "UI/OCR", "save reload", "economic independent multiplication", "natural playthrough"],
    }


def audit_save(path: Path) -> dict:
    raw = path.read_bytes()
    identity = {"save": str(path.resolve()), "save_sha256": hashlib.sha256(raw).hexdigest(), "save_bytes": len(raw)}
    try:
        if path.suffix.lower() != ".sav":
            raise AuditError("input must be a native .sav file")
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)):
                raise AuditError("save archive contains duplicate members")
            if "meta" not in names or "gamestate" not in names:
                raise AuditError("save archive must contain meta and gamestate")
            meta = archive.read("meta")
            game = archive.read("gamestate")
        result = inspect_text(meta.decode("utf-8-sig"), game.decode("utf-8-sig"))
        return {**identity, "zip_members": names, "gamestate_sha256": hashlib.sha256(game).hexdigest(), "gamestate_bytes": len(game), **result}
    except (AuditError, UnicodeError, zipfile.BadZipFile, KeyError) as error:
        return {**identity, "status": "FAIL", "semantic_scope": "read-only native saved-data audit", "diagnostics": [{"severity": "error", "code": "SAVE_UNINTERPRETABLE", "message": str(error)}]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = audit_save(args.save)
    except OSError as error:
        result = {"status": "FAIL", "save": str(args.save), "diagnostics": [{"severity": "error", "code": "SAVE_READ_FAILED", "message": str(error)}]}
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
