"""Read-only, non-GUI contract checks for the feedback redesign.

This deliberately small P-language interpreter checks emitted data against
independent design examples. It is not the Stellaris engine or Kaishek parser.
Unknown evaluated operations fail closed rather than silently becoming true.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR
import hashlib
import json
from pathlib import Path
import random
import re


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MOD = ROOT / "shishan_code_origin/mod"
FULL_NAME = "\u57fa\u4e8e\u4f4e\u5185\u805a\u9ad8\u8026\u5408\u7684\u65e7\u65f6\u4ee3\u96c6\u6210\u670d\u52a1\u67b6\u6784"
LANGUAGES = (
    "braz_por", "english", "french", "german", "japanese", "korean",
    "polish", "russian", "simp_chinese", "spanish",
)
PRODUCTION_RESOURCES = (
    "energy", "trade", "minerals", "food", "alloys", "consumer_goods",
    "physics_research", "society_research", "engineering_research", "unity",
    "influence", "volatile_motes", "exotic_gases", "rare_crystals",
    "sr_living_metal", "sr_zro", "sr_dark_matter", "nanites",
    "minor_artifacts", "astral_threads", "advanced_logic", "entropy_crystals",
)
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|>=|<=|!=|\?=|[{}=<>]|[^\s{}=<>!?#]+')
LOC_ENTRY = re.compile(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s+"((?:\\.|[^"\\])*)"\s*(?:#.*)?$')


class ContractError(ValueError):
    """The inspected artifact violates a static contract or unsupported scope."""


@dataclass(frozen=True)
class Entry:
    key: str
    op: str | None
    value: str | list["Entry"] | None


def parse(source: str) -> list[Entry]:
    """Parse assignments, comparisons, and bare list members without deduping."""
    tokens = [token for token in TOKEN.findall(source) if not token.startswith("#")]
    position = 0

    def entries(nested: bool = False) -> list[Entry]:
        nonlocal position
        result = []
        while position < len(tokens):
            key = tokens[position]
            position += 1
            if key == "}":
                if not nested:
                    raise ContractError("unexpected closing brace")
                return result
            if key in ("{", "=", ">", "<", ">=", "<=", "!=", "?="):
                raise ContractError(f"unexpected token {key!r}")
            if position == len(tokens) or tokens[position] not in ("=", ">", "<", ">=", "<=", "!=", "?="):
                result.append(Entry(key, None, None))
                continue
            op = tokens[position]
            position += 1
            if position == len(tokens) or tokens[position] == "}":
                raise ContractError(f"missing value for {key}")
            value = tokens[position]
            position += 1
            if value == "{":
                value = entries(True)
            result.append(Entry(key, op, value))
        if nested:
            raise ContractError("unclosed block")
        return result

    return entries()


def block(value: str | list[Entry] | None) -> list[Entry]:
    if not isinstance(value, list):
        raise ContractError(f"expected block, got {value!r}")
    return value


def one(entries: list[Entry], key: str) -> str | list[Entry]:
    found = [entry for entry in entries if entry.key == key]
    if len(found) != 1 or found[0].op != "=" or found[0].value is None:
        raise ContractError(f"expected exactly one assignment {key}, got {len(found)}")
    return found[0].value


def walk(entries: list[Entry]):
    for entry in entries:
        yield entry
        if isinstance(entry.value, list):
            yield from walk(entry.value)


def number(value: str | list[Entry] | None) -> Decimal:
    if not isinstance(value, str):
        raise ContractError(f"expected numeric scalar, got {value!r}")
    try:
        return Decimal(value)
    except Exception as error:
        raise ContractError(f"expected numeric scalar, got {value!r}") from error


def read_script(path: Path) -> list[Entry]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ContractError(f"P script has BOM: {path}")
    text = raw.decode("utf-8")
    if "\ufffd" in text:
        raise ContractError(f"replacement character: {path}")
    return parse(text)


class Values:
    """Interpret only script-value arithmetic required by these contracts."""

    def __init__(self, definitions: list[Entry], variables: dict[str, Decimal | int] | None = None, jobs: dict[str, int] | None = None):
        self.definitions = definitions
        self.variables = variables or {}
        self.jobs = jobs or {}
        self.depth = 0

    def scalar(self, value: str | list[Entry] | None) -> Decimal:
        if isinstance(value, list):
            return self.evaluate(value)
        if not isinstance(value, str):
            raise ContractError("missing scalar")
        if value.startswith("value:"):
            return self.named(value[6:])
        if value.startswith(("this.", "owner.", "root.", "prev.")):
            name = value.split(".", 1)[1]
            if name.startswith("value:"):
                return self.named(name[6:])
            if name.startswith("trigger:"):
                raise ContractError(f"unsupported trigger value {value}")
            return Decimal(self.variables.get(name, 0))
        if value in self.variables:
            return Decimal(self.variables[value])
        return number(value)

    def named(self, name: str) -> Decimal:
        if self.depth > 50:
            raise ContractError("recursive script value")
        self.depth += 1
        try:
            definition = one(self.definitions, name)
            return self.evaluate(definition) if isinstance(definition, list) else self.scalar(definition)
        finally:
            self.depth -= 1

    def evaluate(self, entries: list[Entry]) -> Decimal:
        result = Decimal(0)
        for entry in entries:
            key, value = entry.key, entry.value
            if entry.op != "=":
                raise ContractError(f"unsupported script value operator {entry.op}")
            if key == "base":
                result = self.scalar(value)
            elif key == "add":
                result += self.scalar(value)
            elif key == "subtract":
                result -= self.scalar(value)
            elif key == "mult":
                result *= self.scalar(value)
            elif key == "divide":
                result /= self.scalar(value)
            elif key == "min":
                # P script-value min constrains the LOWER bound; max the upper.
                result = max(result, self.scalar(value))
            elif key == "max":
                result = min(result, self.scalar(value))
            elif key == "floor" and value == "yes":
                result = result.to_integral_value(rounding=ROUND_FLOOR)
            elif key == "complex_trigger_modifier":
                body = block(value)
                if one(body, "trigger") != "num_assigned_jobs" or one(body, "mode") != "add" or one(body, "trigger_scope") != "owner":
                    raise ContractError("unsupported complex trigger modifier")
                job = one(block(one(body, "parameters")), "job")
                result += Decimal(self.jobs.get(str(job), 0))
            else:
                raise ContractError(f"unsupported script value operation {key}")
        return result


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def equal(actual, expected, context: str) -> None:
    require(actual == expected, f"{context}: expected {expected}, got {actual}")


@dataclass
class Scope:
    kind: str = "country"
    variables: dict | None = None
    flags: set | None = None
    traits: set | None = None
    groups: list | None = None
    modifiers: dict | None = None
    species_templates: list | None = None
    species: "Scope | None" = None
    projects: set | None = None
    leaders: list | None = None
    owner: "Scope | None" = None
    main_species: "Scope | None" = None
    lineage: str = "main"
    population: int = 0
    origin: str = "origin_shishan_code"
    food: bool = True
    gestalt: bool = False

    def __post_init__(self):
        self.variables = {} if self.variables is None else self.variables
        self.flags = set() if self.flags is None else self.flags
        self.traits = set() if self.traits is None else self.traits
        self.groups = [] if self.groups is None else self.groups
        self.modifiers = {} if self.modifiers is None else self.modifiers
        self.species_templates = [] if self.species_templates is None else self.species_templates
        self.projects = set() if self.projects is None else self.projects
        self.leaders = [] if self.leaders is None else self.leaders


class Effects:
    """Explicit, narrow offline semantics for emitted arithmetic and receipts.

    Scope/iterator mapping is a fixture model, not proof of engine scope rules.
    In particular lineage labels are supplied independently by test fixtures.
    """

    def __init__(self, definitions: list[Entry], values: list[Entry] | None = None, seed: int = 0, trigger_overrides: dict | None = None, effect_hooks: dict | None = None, opaque_effects: set | None = None):
        self.definitions = definitions
        self.values = values or []
        self.rng = random.Random(seed)
        self.root = None
        self.depth = 0
        self.events = []
        self.event_calls = []
        self.ancestors = []
        self.trigger_overrides = trigger_overrides or {}
        self.effect_hooks = effect_hooks or {}
        self.event_targets = {}
        self.opaque_effects = opaque_effects or set()
        self.opaque_calls = []

    def resolve_scope(self, name: str, current: Scope, previous: Scope | None) -> Scope:
        target = {"this": current, "prev": previous, "root": self.root,
                  "prevprev": self.ancestors[1] if len(self.ancestors) > 1 else None,
                  "owner": current.owner, "owner_main_species": (current.owner or current).main_species,
                  "species": current.species}.get(name)
        if name.startswith("event_target:"):
            target = self.event_targets.get(name[13:])
        if target is None:
            raise ContractError(f"unsupported/missing scope {name}")
        return target

    def scoped_trigger(self, entries, target, current):
        self.ancestors.insert(0, current)
        try:
            return self.trigger(entries, target, current)
        finally:
            self.ancestors.pop(0)

    def scoped_execute(self, entries, target, current):
        self.ancestors.insert(0, current)
        try:
            self.execute(entries, target, current)
        finally:
            self.ancestors.pop(0)

    def scalar(self, value, current: Scope, previous: Scope | None = None) -> Decimal:
        if not isinstance(value, str):
            raise ContractError(f"expected scalar, got {value!r}")
        if value.startswith("value:"):
            return Values(self.values, current.variables).named(value[6:])
        if value.startswith("trigger:"):
            require(value == "trigger:pop_amount", f"unsupported trigger export {value}")
            return Decimal(current.population)
        if "." in value:
            scope, key = value.split(".", 1)
            if scope in ("this", "prev", "root", "owner"):
                target = self.resolve_scope(scope, current, previous)
                if key.startswith("value:"):
                    return Values(self.values, target.variables).named(key[6:])
                if key == "trigger:pop_amount":
                    return Decimal(target.population)
                return Decimal(target.variables.get(key, 0))
        if value in current.variables:
            return Decimal(current.variables[value])
        return number(value)

    def compare(self, actual, op, expected) -> bool:
        if op == "=":
            return actual == expected
        if op == ">":
            return actual > expected
        if op == "<":
            return actual < expected
        if op == ">=":
            return actual >= expected
        if op == "<=":
            return actual <= expected
        if op == "!=":
            return actual != expected
        raise ContractError(f"unsupported comparison {op}")

    def trigger(self, entries: list[Entry], current: Scope, previous: Scope | None = None) -> bool:
        results = []
        for entry in entries:
            key, value = entry.key, entry.value
            if key in self.trigger_overrides:
                result = bool(self.trigger_overrides[key])
            elif key in ("AND", "limit"):
                result = self.trigger(block(value), current, previous)
            elif key == "OR":
                result = any(self.trigger([item], current, previous) for item in block(value))
            elif key in ("NOT", "NOR"):
                result = not (self.trigger(block(value), current, previous) if key == "NOT" else any(self.trigger([item], current, previous) for item in block(value)))
            elif key in ("this", "prev", "root", "owner", "owner_main_species", "species"):
                result = self.scoped_trigger(block(value), self.resolve_scope(key, current, previous), current)
            elif key == "has_origin":
                result = current.origin == value
            elif key in ("has_country_flag", "has_species_flag", "has_leader_flag"):
                result = value in current.flags
            elif key == "has_modifier":
                result = value in current.modifiers
            elif key == "has_special_project":
                result = value in current.projects
            elif key == "is_variable_set":
                result = value in current.variables
            elif key == "has_trait":
                result = value in current.traits
            elif key == "country_uses_food":
                result = current.food == (value == "yes")
            elif key == "has_ethic":
                require(value == "ethic_gestalt_consciousness", f"unsupported ethic {value}")
                result = current.gestalt
            elif key == "is_same_species":
                result = current.lineage == self.resolve_scope(str(value), current, previous).lineage
            elif key == "is_exact_same_species":
                target = self.resolve_scope(str(value), current, previous)
                result = (current.species or current) is (target.species or target)
            elif key == "any_owned_species":
                result = any(self.scoped_trigger(block(value), species, current) for species in current.species_templates if species.owner is current)
            elif key == "any_owned_pop_group":
                result = any(self.scoped_trigger(block(value), group, current) for group in current.groups if group.owner is current)
            elif key == "any_owned_leader":
                result = any(self.scoped_trigger(block(value), leader, current) for leader in current.leaders if leader.owner is current)
            elif key == "pop_amount":
                result = self.compare(Decimal(current.population), entry.op, self.scalar(value, current, previous))
            elif key == "check_variable":
                body = block(value)
                variable = one(body, "which")
                comparisons = [item for item in body if item.key == "value"]
                require(len(comparisons) == 1, "invalid variable comparison")
                comparison = comparisons[0]
                result = self.compare(Decimal(current.variables.get(variable, 0)), comparison.op, self.scalar(comparison.value, current, previous))
            elif key == "always":
                result = value == "yes"
            elif key.startswith("shishan_") and value == "yes":
                result = self.trigger(block(one(self.definitions, key)), current, previous)
            else:
                raise ContractError(f"unsupported offline trigger {key}")
            results.append(result)
        return all(results)

    def named(self, name: str, current: Scope, previous: Scope | None = None, parameters: dict | None = None) -> None:
        if self.root is None:
            self.root = current
        if self.depth > 100:
            raise ContractError("recursive scripted effect")
        body = block(one(self.definitions, name))
        if parameters:
            def substitute(entries):
                result = []
                for entry in entries:
                    key = entry.key
                    value = entry.value
                    for parameter, replacement in parameters.items():
                        key = key.replace(f"${parameter}$", str(replacement))
                    if isinstance(value, str):
                        for parameter, replacement in parameters.items():
                            value = value.replace(f"${parameter}$", str(replacement))
                    elif isinstance(value, list):
                        value = substitute(value)
                    result.append(Entry(key, entry.op, value))
                return result
            body = substitute(body)
        self.depth += 1
        try:
            self.execute(body, current, previous)
        finally:
            self.depth -= 1

    def execute(self, entries: list[Entry], current: Scope, previous: Scope | None = None) -> None:
        branch_taken = False
        for entry in entries:
            key, value = entry.key, entry.value
            if key in self.opaque_effects:
                self.opaque_calls.append(entry)
            elif key in ("if", "else_if", "else"):
                if key == "if":
                    branch_taken = False
                body = block(value)
                limits = [item for item in body if item.key == "limit"]
                require(len(limits) <= 1, "duplicate branch limit")
                qualifies = key == "else" or (bool(limits) and self.trigger(block(limits[0].value), current, previous))
                if not branch_taken and qualifies:
                    self.execute([item for item in body if item.key != "limit"], current, previous)
                    branch_taken = True
            elif key in ("set_variable", "change_variable", "multiply_variable", "divide_variable", "subtract_variable"):
                body = block(value)
                variable = str(one(body, "which"))
                amount = self.scalar(one(body, "value"), current, previous)
                before = Decimal(current.variables.get(variable, 0))
                if key == "set_variable":
                    after = amount
                elif key == "change_variable":
                    after = before + amount
                elif key == "multiply_variable":
                    after = before * amount
                elif key == "subtract_variable":
                    after = before - amount
                else:
                    after = before / amount
                current.variables[variable] = after
            elif key == "floor_variable":
                current.variables[str(value)] = Decimal(current.variables.get(str(value), 0)).to_integral_value(rounding=ROUND_FLOOR)
            elif key == "clear_variable":
                current.variables.pop(str(value), None)
            elif key == "remove_modifier":
                current.modifiers.pop(str(value), None)
            elif key == "add_modifier":
                body = block(value)
                modifier = str(one(body, "modifier"))
                multipliers = [item.value for item in body if item.key == "multiplier"]
                require(len(multipliers) <= 1, "duplicate modifier multiplier")
                require(not any(item.key == "mult" for item in body), "add_modifier must use documented multiplier field")
                current.modifiers[modifier] = self.scalar(multipliers[0], current, previous) if multipliers else Decimal(1)
            elif key in ("set_country_flag", "set_species_flag", "set_leader_flag"):
                current.flags.add(value)
            elif key in ("remove_country_flag", "remove_species_flag", "remove_leader_flag"):
                current.flags.discard(value)
            elif key == "save_event_target_as":
                self.event_targets[str(value)] = current
            elif key == "enable_special_project":
                current.projects.add(str(one(block(value), "name")))
            elif key == "abort_special_project":
                current.projects.discard(str(one(block(value), "type")))
            elif key in ("this", "prev", "root", "owner", "owner_main_species", "species") or key.startswith("event_target:"):
                self.scoped_execute(block(value), self.resolve_scope(key, current, previous), current)
            elif key == "every_owned_species":
                body = block(value)
                for species in list(current.species_templates):
                    if species.owner is current and all(self.scoped_trigger(block(item.value), species, current) for item in body if item.key == "limit"):
                        self.scoped_execute([item for item in body if item.key != "limit"], species, current)
            elif key == "every_owned_pop_group":
                body = block(value)
                for group in current.groups:
                    if group.owner is current and all(self.scoped_trigger(block(item.value), group, current) for item in body if item.key == "limit"):
                        self.scoped_execute([item for item in body if item.key != "limit"], group, current)
            elif key == "every_trait_of_species":
                for trait in sorted(current.traits):
                    target = Scope(kind="trait", traits={trait}, owner=current.owner)
                    self.scoped_execute(block(value), target, current)
            elif key == "change_species_characteristics":
                for change in block(value):
                    require(change.key in ("add_trait", "remove_trait"), f"unsupported species change {change.key}")
                    if change.key == "add_trait":
                        current.traits.add(change.value)
                    else:
                        current.traits.discard(change.value)
            elif key == "random_list":
                choices, weights = [], []
                for choice in block(value):
                    weight = number(choice.key)
                    body = block(choice.value)
                    for modifier in (item for item in body if item.key == "modifier"):
                        modifier_body = block(modifier.value)
                        conditions = [item for item in modifier_body if item.key not in ("factor", "add")]
                        if self.trigger(conditions, current, previous):
                            factors = [item.value for item in modifier_body if item.key == "factor"]
                            additions = [item.value for item in modifier_body if item.key == "add"]
                            for factor in factors:
                                weight *= self.scalar(factor, current, previous)
                            for addition in additions:
                                weight += self.scalar(addition, current, previous)
                    if weight > 0:
                        choices.append([item for item in body if item.key != "modifier"])
                        weights.append(float(weight))
                require(bool(choices), "random_list has no eligible choice")
                self.execute(self.rng.choices(choices, weights=weights, k=1)[0], current, previous)
            elif key == "country_event":
                body = block(value)
                event_id = str(one(body, "id"))
                days = [item.value for item in body if item.key == "days"]
                self.events.append(event_id)
                self.event_calls.append({"id": event_id, "days": int(number(days[0])) if days else 0})
            elif key in ("custom_tooltip", "hidden_effect"):
                if key == "hidden_effect":
                    self.execute(block(value), current, previous)
            elif key.startswith("shishan_"):
                parameters = {item.key: item.value for item in block(value)} if isinstance(value, list) else None
                require(value == "yes" or parameters is not None, f"invalid scripted effect invocation {key}")
                if key in self.effect_hooks:
                    self.effect_hooks[key](self, current, parameters or {})
                else:
                    self.named(key, current, previous, parameters)
            else:
                raise ContractError(f"unsupported offline effect {key}")


def load_definitions(mod: Path, directory: str) -> list[Entry]:
    definitions = []
    for path in sorted((mod / "common" / directory).glob("*.txt")):
        definitions.extend(read_script(path))
    return definitions


def check_domestic_templates(definitions: list[Entry]) -> dict:
    """Check scope structure; cloning engine semantics remain NOT RUN."""
    old = "event_target:shishan_code_reward_old_species"
    new = "event_target:shishan_code_reward_new_species"
    apply = block(one(definitions, "shishan_code_apply_domestic_template_effect"))
    for iterator in ("every_owned_pop_group", "every_owned_leader"):
        body = block(one(apply, iterator))
        limit = block(one(body, "limit"))
        equal(one(limit, "is_exact_same_species"), old, f"{iterator} exact template restriction")
        equal(one(body, "change_species"), new, f"{iterator} domestic new template")
        if iterator == "every_owned_pop_group":
            require(Entry("pop_amount", ">", "0") in limit, "template applies to empty group")
    condition = block(one(apply, "if"))
    equal(one(block(one(block(one(condition, "limit")), "owner_main_species")), "is_exact_same_species"), old, "main species only changes when it is the modified exact template")
    dominant = block(one(condition, "change_dominant_species"))
    equal(one(dominant, "species"), new, "main species replacement")
    equal(one(dominant, "change_all"), "no", "main species replacement cannot change foreign/shared species")
    helpers = ("shishan_code_modify_domestic_template_effect", "shishan_code_architecture_refactor_template_effect", "shishan_code_architecture_relapse_template_effect")
    for helper in helpers:
        body = block(one(definitions, helper))
        clone = block(one(body, "modify_species"))
        equal(one(clone, "species"), "this", "clone source")
        equal(one(clone, "change_scoped_species"), "no", "shared source template must not be mutated")
        equal(one(block(one(clone, "effect")), "save_event_target_as"), "shishan_code_reward_new_species", "clone target")
        equal(one(block(one(body, "event_target:shishan_code_reward_country")), "shishan_code_apply_domestic_template_effect"), "yes", "clone domestic application")
        require(not any(item.key == "change_species_characteristics" for item in walk(body)), "shared species mutation in domestic helper")
    for action in ("refactor", "relapse"):
        entry = block(one(definitions, f"shishan_code_architecture_{action}_species_effect"))
        branch = block(one(entry, "if"))
        equal(one(block(one(branch, "limit")), "has_origin"), "origin_shishan_code", "state species origin gate")
        population = block(one(branch, "every_owned_species"))
        limit = block(one(population, "limit"))
        equal(one(limit, "is_same_species"), "prev", "state only modifies main lineage")
        actual = block(one(block(one(limit, "prev")), "any_owned_pop_group"))
        equal(one(actual, "is_exact_same_species"), "prevprev", "owned template must be populated")
        require(Entry("pop_amount", ">", "0") in actual, "state modifies empty/unapplied template")
    return {"clone_helpers": 3, "country_state_entry_points": 2, "engine_clone_behavior": "NOT RUN"}


def check_architecture(mod: Path) -> dict:
    definitions = load_definitions(mod, "scripted_effects")
    values = load_definitions(mod, "script_values")
    equal(number(one(values, "shishan_code_architecture_per_trait")), Decimal(".05"), "architecture per trait")
    refresh = block(one(definitions, "shishan_code_architecture_refresh_effect"))
    modifier_definitions = load_definitions(mod, "static_modifiers")
    native_bonus = block(one(modifier_definitions, "shishan_code_architecture_jobs"))
    equal(native_bonus, [Entry("planet_jobs_produces_mult", "=", "0.05")], "explicit additive-only rc fallback")
    require(refresh and refresh[0] == Entry("remove_modifier", "=", "shishan_code_architecture_jobs"), "origin loss cannot leave a stale architecture modifier")
    iterators = [item for item in walk(refresh) if item.key == "every_trait_of_species"]
    require(bool(iterators), "all-trait native iterator missing")
    for iterator in iterators:
        require(not any(item.key == "limit" for item in block(iterator.value)), "trait iterator filters formal traits")
    require(any(item.key == "every_owned_pop_group" for item in walk(refresh)), "domestic population iterator missing")
    require(not any(item.key in ("add_trait", "remove_trait", "change_species_characteristics") for item in walk(refresh)), "counting mutates species")
    prefixes = "shishan_code_architecture_"
    country = Scope()
    ten = {"trait_positive", "trait_negative", "trait_zero", "trait_preference", "trait_hidden", "trait_event", "trait_third_party", "trait_vanilla_original", "trait_shishan_compat_original", "trait_status"}
    country.groups = [Scope(kind="pop_group", owner=country, population=800, traits=ten), Scope(kind="pop_group", owner=country, population=200, traits=set(list(sorted(ten))[:5])), Scope(kind="pop_group", owner=country, population=0, traits={f"empty_{n}" for n in range(50)}), Scope(kind="pop_group", owner=country, lineage="external", population=500, traits={f"foreign_{n}" for n in range(50)})]
    foreign_owner = Scope(origin="origin_default")
    # A foreign country can share the same raw trait/template object. Ownership
    # filtering is checked independently of the lineage filtering above.
    country.groups.append(Scope(kind="pop_group", owner=foreign_owner, population=10000, traits=ten))
    effects = Effects(definitions, values)
    effects.named("shishan_code_architecture_refresh_effect", country)
    equal(country.variables[prefixes + "trait_average"], Decimal(9), "population-weighted traits")
    equal(country.variables[prefixes + "multiplier"], Decimal("1.45"), "population-weighted multiplier")
    equal(country.modifiers, {"shishan_code_architecture_jobs": Decimal(9)}, "single additive modifier scales with total")
    require(all(not group.variables for group in country.groups), "temporary group bookkeeping leaked")
    country.groups[1].traits = set(ten)
    effects.named("shishan_code_architecture_refresh_effect", country)
    equal(country.variables[prefixes + "trait_average"], Decimal(10), "applied template change")
    country.groups[1].traits.add("trait_new_third_party_negative")
    effects.named("shishan_code_architecture_refresh_effect", country)
    equal(country.variables[prefixes + "trait_average"], Decimal("10.2"), "one trait on 20 percent of population")
    equal(country.variables[prefixes + "multiplier"], Decimal("1.51"), "weighted extra trait multiplier")
    for repeats, expected in ((0, "1.51"), (100, "6.51"), (1000, "51.51"), (10000, "501.51")):
        country.variables[prefixes + "repeat_count"] = Decimal(repeats)
        effects.named("shishan_code_architecture_refresh_effect", country)
        before = country.variables[prefixes + "multiplier"]
        equal(before, Decimal(expected), f"uncapped repeats {repeats}")
        effects.named("shishan_code_architecture_award_repeat_effect", country)
        equal(country.variables[prefixes + "multiplier"] - before, Decimal(".05"), "next layer independent delta")
        equal(country.variables[prefixes + "repeat_count"], Decimal(repeats + 1), "repeat award")
    country.groups = []
    effects.named("shishan_code_architecture_refresh_effect", country)
    equal(country.variables[prefixes + "multiplier"], Decimal(1), "zero lineage population no multiplier")
    equal(country.variables[prefixes + "repeat_count"], Decimal(10001), "zero population preserves repeats")
    equal(country.modifiers, {}, "zero population removes native modifier")
    legacy = Scope(variables=dict(zip(("shishan_code_iteration_output", "shishan_code_iteration_energy", "shishan_code_iteration_assembly", "shishan_code_iteration_experience"), (7, 5, 11, 4))))
    historical = legacy.variables.copy()
    effects = Effects(definitions, values)
    effects.named("shishan_code_architecture_migrate_effect", legacy)
    equal(legacy.variables[prefixes + "repeat_count"], Decimal(23), "legacy repetitions, first layers excluded")
    effects.named("shishan_code_architecture_migrate_effect", legacy)
    equal(legacy.variables[prefixes + "repeat_count"], Decimal(23), "migration replay")
    for key, value in historical.items():
        equal(legacy.variables[key], value, "frozen historical counter")
    legacy.groups = [Scope(kind="pop_group", owner=legacy, population=100, traits={f"trait_{index}" for index in range(43)})]
    effects.named("shishan_code_architecture_refresh_effect", legacy)
    equal(legacy.variables[prefixes + "total"], Decimal(66), "legacy first layers counted once as raw traits")
    equal(legacy.variables[prefixes + "multiplier"], Decimal("4.30"), "legacy 43 raw traits plus 23 repeats")
    for counter, expected, invalid in ((0, "0", False), (1, "0", False), (-2, "0", True), ("1.5", ".5", True)):
        edge = Scope(variables={"shishan_code_iteration_output": Decimal(counter)})
        Effects(definitions, values).named("shishan_code_architecture_migrate_effect", edge)
        equal(edge.variables[prefixes + "repeat_count"], Decimal(expected), "legacy edge arithmetic")
        equal(edge.variables["shishan_code_iteration_output"], Decimal(counter), "legacy abnormal history preserved")
        equal("shishan_code_architecture_legacy_invalid" in edge.flags, invalid, "legacy anomaly diagnostic")
    ordinary = Scope(origin="origin_default", variables={"shishan_code_iteration_output": 7})
    ordinary.modifiers["shishan_code_architecture_jobs"] = Decimal(50)
    Effects(definitions, values).named("shishan_code_architecture_refresh_effect", ordinary)
    equal(ordinary.variables, {"shishan_code_iteration_output": 7}, "origin scope")
    equal(ordinary.modifiers, {}, "origin loss removes stale native modifier")
    domestic = check_domestic_templates(definitions)
    return {"all_trait_keys_in_fixture": 10, "weighted_average": "9", "legacy_repeats": 23, "highest_repeats_checked": 10001, "domestic_template_scope": domestic, "economic_route": "explicit native additive rc fallback", "independent_multiplication": "NOT IMPLEMENTED", "engine_economic_effect": "NOT RUN"}


def reward_fixture(definitions, values, eligible_ids, seed=0):
    """Supply independent eligibility facts; execute emitted state machinery.

    The helper hook models an already-audited domestic clone as an abstract
    grant. It does not purport to implement or validate engine cloning.
    """
    country = Scope(variables={"shishan_code_maintenance_count": Decimal(7)}, flags={"shishan_code_reward_ticket_ready"})
    species = Scope(kind="species", owner=country, traits={"trait_shishan_code", "trait_robotic_1", "trait_pc_continental_preference"})
    country.main_species = species
    country.species_templates = [species]
    country.groups = [Scope(kind="pop_group", owner=country, species=species, population=100, traits=species.traits)]
    overrides = {f"shishan_code_reward_eligible_{index:02d}": index in eligible_ids for index in range(1, 40)}
    grants = []
    trait_ids = {}
    for index in range(1, 40):
        claim = block(one(definitions, f"shishan_code_reward_claim_{index:02d}_effect"))
        calls = [item for item in walk(claim) if item.key == "shishan_code_modify_domestic_template_effect"]
        equal(len(calls), 1, "one domestic grant invocation per candidate")
        trait_ids[str(one(block(calls[0].value), "ADD_TRAIT"))] = index

    def abstract_clone(interpreter, old, parameters):
        trait = str(parameters["ADD_TRAIT"])
        grants.append(trait)
        new = Scope(kind="species", owner=country, lineage=old.lineage, traits=old.traits | {trait})
        for group in country.groups:
            if group.owner is country and group.species is old and group.population > 0:
                group.species = new
                group.traits = new.traits
        country.species_templates = [new if template is old else template for template in country.species_templates]
        if country.main_species is old:
            country.main_species = new
        interpreter.trigger_overrides[f"shishan_code_reward_eligible_{trait_ids[trait]:02d}"] = False

    interpreter = Effects(definitions, values, seed, overrides, {"shishan_code_modify_domestic_template_effect": abstract_clone})
    interpreter.grants = grants
    return interpreter, country


def reward_slots(country: Scope) -> tuple[int, ...]:
    return tuple(int(country.variables.get(f"shishan_code_reward_slot_{slot}", 0)) for slot in (1, 2, 3))


def reward_snapshot(interpreter: Effects, country: Scope):
    return (dict(country.variables), set(country.flags), tuple(reward_slots(country)), tuple(interpreter.grants), frozenset(country.main_species.traits))


def reward_business_snapshot(interpreter: Effects, country: Scope):
    snapshot = list(reward_snapshot(interpreter, country))
    snapshot[1].discard("shishan_code_reward_window_open")
    return tuple(snapshot)


def country_events(mod: Path) -> list[Entry]:
    result = []
    for path in sorted((mod / "events").glob("*.txt")):
        result.extend(entry for entry in read_script(path) if entry.key == "country_event")
    return result


def find_country_event(events: list[Entry], event_id: str) -> list[Entry]:
    found = [block(entry.value) for entry in events if one(block(entry.value), "id") == event_id]
    require(len(found) == 1, f"expected one country event {event_id}, got {len(found)}")
    return found[0]


def run_country_event(interpreter: Effects, events: list[Entry], event_id: str, country: Scope) -> bool:
    body = find_country_event(events, event_id)
    conditions = [entry for entry in body if entry.key == "trigger"]
    if conditions and not interpreter.trigger(block(conditions[0].value), country):
        return False
    immediates = [entry for entry in body if entry.key == "immediate"]
    require(len(immediates) <= 1, f"duplicate immediate in {event_id}")
    if immediates:
        interpreter.execute(block(immediates[0].value), country)
    return True


def check_reward_windows(mod: Path, definitions: list[Entry], values: list[Entry]) -> dict:
    interpreter, country = reward_fixture(definitions, values, set(range(1, 7)), 3)
    interpreter.named("shishan_code_award_reward", country)
    equal(interpreter.events.count("shishan_code.1000"), 1, "first reward schedules one window")
    require("shishan_code_reward_window_open" in country.flags, "reward window lock not persisted")
    original = reward_snapshot(interpreter, country)
    for _ in range(3):
        interpreter.named("shishan_code_reward_open_window_effect", country)
    equal(interpreter.events.count("shishan_code.1000"), 1, "pending reward cannot schedule duplicate windows")
    equal(reward_snapshot(interpreter, country), original, "opening repeated window leaves ticket intact")
    event = find_country_event(country_events(mod), "shishan_code.1000")
    later = [block(entry.value) for entry in event if entry.key == "option" and one(block(entry.value), "name") == "shishan_code_reward_later"]
    require(len(later) == 1, "later option missing or duplicated")
    interpreter.execute([entry for entry in later[0] if entry.key not in ("name", "ai_chance", "trigger", "allow")], country)
    require("shishan_code_reward_window_open" not in country.flags, "later must release window lock")
    require("shishan_code_reward_pending" in country.flags, "later cannot consume reward")
    equal(reward_slots(country), original[2], "later preserves candidates")
    interpreter.named("shishan_code_reward_open_window_effect", country)
    interpreter.named("shishan_code_reward_open_window_effect", country)
    equal(interpreter.events.count("shishan_code.1000"), 2, "later allows one persisted-ticket reopen")
    interpreter.named("shishan_code_reward_reroll_effect", country)
    equal(interpreter.events.count("shishan_code.1000"), 3, "reroll replaces the window exactly once")
    require("shishan_code_reward_window_open" in country.flags, "rerolled window remains locked")
    selected = next(index for index in reward_slots(country) if index)
    interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
    require("shishan_code_reward_window_open" not in country.flags, "confirmation releases window lock")
    interpreter.named("shishan_code_reward_open_window_effect", country)
    equal(interpreter.events.count("shishan_code.1000"), 3, "consumed ticket cannot reopen")
    country.flags.add("shishan_code_reward_ticket_ready")
    interpreter.named("shishan_code_award_reward", country)
    equal(interpreter.events.count("shishan_code.1000"), 4, "new successful ticket opens one window")
    # A visible option may become invalid before it is clicked. The engine
    # closes that window after the click even when its internal guard rejects.
    # Only the lock may change; a capital reopen must repair the pending UI.
    decision = block(one(read_script(mod / "common/decisions/shishan_code_decisions.txt"), "decision_shishan_code_reward"))
    for rejection in ("claim", "reroll"):
        interpreter, country = reward_fixture(definitions, values, set(range(1, 7)), 5)
        interpreter.named("shishan_code_award_reward", country)
        selected = next(index for index in reward_slots(country) if index)
        if rejection == "claim":
            interpreter.trigger_overrides[f"shishan_code_reward_eligible_{selected:02d}"] = False
            country.variables["shishan_code_reroll_cooldown"] = Decimal(2)
            action = f"shishan_code_reward_claim_{selected:02d}_effect"
        else:
            country.variables["shishan_code_reroll_cooldown"] = Decimal(1)
            action = "shishan_code_reward_reroll_effect"
        before = reward_business_snapshot(interpreter, country)
        interpreter.named(action, country)
        require("shishan_code_reward_window_open" not in country.flags, f"rejected {rejection} must release window lock")
        equal(reward_business_snapshot(interpreter, country), before, f"rejected {rejection} preserves ticket/candidates/n/R/cooldown/grants")
        count_before = interpreter.events.count("shishan_code.1000")
        planet = Scope(kind="planet", owner=country)
        interpreter.execute(block(one(decision, "effect")), planet)
        equal(interpreter.events.count("shishan_code.1000"), count_before + 1, f"rejected {rejection} capital wrapper can reopen")
        require(run_country_event(interpreter, country_events(mod), "shishan_code.1000", country), "reopened reward UI event must run")
        if rejection == "claim":
            require(selected not in reward_slots(country), "reopened window must repair the invalid candidate")
        else:
            equal(reward_slots(country), before[2], "rejected reroll reopen preserves valid candidates")
        equal(country.variables["shishan_code_maintenance_count"], before[0]["shishan_code_maintenance_count"], "reopen cannot increment n")
        equal(country.variables["shishan_code_reroll_cooldown"], before[0]["shishan_code_reroll_cooldown"], "reopen cannot reduce cooldown")
        equal(country.variables.get("shishan_code_architecture_repeat_count", Decimal(0)), before[0].get("shishan_code_architecture_repeat_count", Decimal(0)), "reopen cannot award repeats")
        equal(interpreter.grants, [], "rejected action cannot grant a trait")
    return {"duplicate_open_requests": 3, "window_queue_counts": [1, 2, 3, 4], "rejected_option_unlock_and_reopen_cases": 2, "engine_window_lifecycle": "NOT RUN"}


def check_rewards(mod: Path) -> dict:
    definitions = load_definitions(mod, "scripted_effects") + load_definitions(mod, "scripted_triggers")
    values = load_definitions(mod, "script_values")
    # Fixed counts/tiers are a design baseline, independent of generator lists.
    eligibility = [entry for entry in definitions if re.fullmatch(r"shishan_code_reward_eligible_\d+", entry.key)]
    equal({entry.key for entry in eligibility}, {f"shishan_code_reward_eligible_{index:02d}" for index in range(1, 40)}, "39 eligibility triggers")
    for index in range(1, 40):
        guard = block(one(definitions, f"shishan_code_reward_eligible_{index:02d}"))
        domestic = block(one(guard, "any_owned_species"))
        equal(one(domestic, "is_same_species"), "prev", "reward eligibility main lineage")
        actual = block(one(block(one(domestic, "prev")), "any_owned_pop_group"))
        equal(one(actual, "is_exact_same_species"), "prevprev", "reward eligibility actual domestic template")
        require(Entry("pop_amount", ">", "0") in actual, "empty template makes reward eligible")
        claim = block(one(definitions, f"shishan_code_reward_claim_{index:02d}_effect"))
        require(claim and claim[0] == Entry("remove_country_flag", "=", "shishan_code_reward_window_open"), "rejected claim must release window lock before its guard")
        require(not any(entry.key == "change_species_characteristics" for entry in walk(claim)), "reward mutates shared species")
        branch = block(one(claim, "if"))
        grant_scope = block(one(branch, "every_owned_species"))
        grant_limit = block(one(grant_scope, "limit"))
        equal(one(grant_limit, "is_same_species"), "prev", "grant only modifies main lineage")
        populated = block(one(block(one(grant_limit, "prev")), "any_owned_pop_group"))
        equal(one(populated, "is_exact_same_species"), "prevprev", "grant requires actual domestic template")
        require(Entry("pop_amount", ">", "0") in populated, "grant modifies an empty/unapplied template")
    # N=0..6 and mixed tiers exercise the actual random_list / slot guards.
    draws = 0
    for seed in range(8):
        for count in range(7):
            ids = set(range(1, count + 1))
            interpreter, country = reward_fixture(definitions, values, ids, seed)
            interpreter.named("shishan_code_award_reward", country)
            slots = reward_slots(country)
            nonzero = [item for item in slots if item]
            equal(len(nonzero), min(count, 3), f"candidate count N={count}, seed={seed}")
            equal(len(nonzero), len(set(nonzero)), "candidate uniqueness")
            require(set(nonzero) <= ids, "candidate selected outside eligible pool")
            equal(country.variables["shishan_code_maintenance_count"], Decimal(7), "reward cannot independently increment maintenance count")
            if count == 0:
                equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "exhausted pool one repetition")
            else:
                before = reward_snapshot(interpreter, country)
                interpreter.named("shishan_code_award_reward", country)
                equal(reward_snapshot(interpreter, country), before, "opening/award replay keeps original ticket")
                old = set(nonzero)
                interpreter.named("shishan_code_reward_reroll_effect", country)
                if count <= 3:
                    expected = list(before)
                    expected[1].discard("shishan_code_reward_window_open")
                    equal(reward_business_snapshot(interpreter, country), tuple(expected), "no alternate means no reroll/cooldown cost")
                else:
                    new = set(reward_slots(country))
                    outside = ids - old
                    require(outside <= new, "reroll must prioritize all available outside-group candidates")
                    equal(len(new & old), max(0, 3 - len(outside)), "reroll only fills old candidates after outside ones")
                    equal(country.variables["shishan_code_reroll_cooldown"], Decimal(3), "reroll sets three-choice cooldown")
                    after = reward_snapshot(interpreter, country)
                    interpreter.named("shishan_code_reward_reroll_effect", country)
                    expected = list(after)
                    expected[1].discard("shishan_code_reward_window_open")
                    equal(reward_business_snapshot(interpreter, country), tuple(expected), "same ticket cannot reroll twice")
            draws += 1
    for ids, tier, expected_ids in (({1, 21, 22, 23, 24}, 1, {1}), ({21, 22, 23, 24, 25, 26}, 2, set(range(21, 27)))):
        interpreter, country = reward_fixture(definitions, values, ids, 11)
        interpreter.named("shishan_code_award_reward", country)
        equal(country.variables["shishan_code_reward_tier"], Decimal(tier), "tier priority")
        require({item for item in reward_slots(country) if item} <= expected_ids, "mixed tiers were filled together")
    interpreter, country = reward_fixture(definitions, values, set(range(1, 7)), 7)
    interpreter.named("shishan_code_award_reward", country)
    unselected = next(index for index in range(1, 7) if index not in reward_slots(country))
    before = reward_snapshot(interpreter, country)
    interpreter.named(f"shishan_code_reward_claim_{unselected:02d}_effect", country)
    expected = list(before)
    expected[1].discard("shishan_code_reward_window_open")
    equal(reward_business_snapshot(interpreter, country), tuple(expected), "unselected candidate cannot consume ticket")
    # Three actual claim confirmations, including the rerolled round itself.
    interpreter, country = reward_fixture(definitions, values, set(range(1, 11)), 9)
    interpreter.named("shishan_code_award_reward", country)
    interpreter.named("shishan_code_reward_reroll_effect", country)
    equal(country.variables["shishan_code_reroll_cooldown"], Decimal(3), "ready reroll")
    for expected in (2, 1, 0):
        selected = next(item for item in reward_slots(country) if item)
        interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
        equal(country.variables["shishan_code_reroll_cooldown"], Decimal(expected), "confirmation cooldown 3 -> 2 -> 1 -> 0")
        before = reward_snapshot(interpreter, country)
        interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
        equal(reward_snapshot(interpreter, country), before, "same candidate callback replay is idempotent")
        country.flags.add("shishan_code_reward_ticket_ready")
        interpreter.named("shishan_code_award_reward", country)
    equal(len(interpreter.grants), 3, "one grant per confirmed ticket")
    require(interpreter.trigger([Entry("shishan_code_reward_can_reroll", "=", "yes")], country), "round four reroll should be ready")
    # New exhausted tickets give R once, without progressing entity cooldown.
    interpreter, country = reward_fixture(definitions, values, set(), 0)
    country.variables["shishan_code_reroll_cooldown"] = Decimal(2)
    interpreter.named("shishan_code_award_reward", country)
    equal(country.variables["shishan_code_reroll_cooldown"], Decimal(2), "auto repetition cannot reduce entity cooldown")
    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "first exhausted ticket")
    interpreter.named("shishan_code_award_reward", country)
    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "exhausted ticket replay")
    country.flags.add("shishan_code_reward_ticket_ready")
    interpreter.named("shishan_code_award_reward", country)
    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(2), "next exhausted successful ticket")
    # Invalidation repairs only affected slots. Refreshes never count as choices.
    interpreter, country = reward_fixture(definitions, values, set(range(1, 7)), 2)
    interpreter.named("shishan_code_award_reward", country)
    before = reward_slots(country)
    interpreter.trigger_overrides[f"shishan_code_reward_eligible_{before[1]:02d}"] = False
    country.variables["shishan_code_reroll_cooldown"] = Decimal(2)
    interpreter.named("shishan_code_reward_refresh_effect", country)
    after = reward_slots(country)
    equal(after[0], before[0], "valid first slot kept on refresh")
    equal(after[2], before[2], "valid third slot kept on refresh")
    require(after[1] != before[1], "invalid second slot not repaired")
    equal(country.variables["shishan_code_reroll_cooldown"], Decimal(2), "invalid-option refresh is not a choice")
    equal(len(set(after)), 3, "refreshed candidates unique")
    for key in interpreter.trigger_overrides:
        interpreter.trigger_overrides[key] = False
    interpreter.named("shishan_code_reward_refresh_effect", country)
    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "all invalid and exhausted settles repetition once")
    interpreter.named("shishan_code_reward_refresh_effect", country)
    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "exhausted refresh replay")
    # No receipt or no origin must not create candidates/repetitions.
    for origin, ready in (("origin_default", True), ("origin_shishan_code", False)):
        interpreter, country = reward_fixture(definitions, values, {1, 2, 3, 4}, 0)
        country.origin = origin
        if not ready:
            country.flags.clear()
        before = reward_snapshot(interpreter, country)
        interpreter.named("shishan_code_award_reward", country)
        equal(reward_snapshot(interpreter, country), before, "reward requires origin and successful receipt")
    windows = check_reward_windows(mod, definitions, values)
    return {"seeded_candidate_cases": draws, "eligible_counts_checked": [0, 1, 2, 3, 4, 5, 6], "cooldown_sequence": [3, 2, 1, 0], "tier_priority": "robotic before compatible", "window_lock": windows, "eligibility_facts": "fixture overrides; actual guard scope checked structurally", "grant_clone_semantics": "abstract fixture hook, engine NOT RUN"}


def check_receipt_recovery(mod: Path) -> dict:
    definitions = load_definitions(mod, "scripted_effects") + load_definitions(mod, "scripted_triggers")
    values = load_definitions(mod, "script_values")
    events = country_events(mod)
    # Verify the source of the persisted receipt as well as consuming events.
    projects = read_script(mod / "common/special_projects/shishan_code_projects.txt")
    for suffix, event_id in (("MAINTAIN", "10"), ("CLEAN", "20"), ("OPTIMIZE", "30")):
        project = next(block(entry.value) for entry in projects if entry.key == "special_project" and one(block(entry.value), "key") == f'"SHISHAN_CODE_{suffix}"')
        success = block(one(project, "on_success"))
        equal(one(success, "set_country_flag"), f"shishan_code_{suffix.lower()}_success_pending", "successful project persists a receipt")
        equal(one(block(one(success, "country_event")), "id"), f"shishan_code.{event_id}", "successful project dispatches its guarded callback")

    def fixture(ids, seed=0):
        interpreter, country = reward_fixture(definitions, values, ids, seed)
        country.flags.clear()
        interpreter.opaque_effects = {"every_situation", "start_situation"}
        # These domains have separate structure/data checks and are outside
        # this receipt interpreter's runtime scope. The skips are explicit.
        interpreter.effect_hooks.update({name: (lambda *_: None) for name in (
            "shishan_code_refresh_vivhite_effect", "shishan_code_architecture_refactor_species_effect",
            "shishan_code_architecture_relapse_species_effect",
        )})
        return interpreter, country

    def recover(interpreter, country):
        offset = len(interpreter.event_calls)
        require(run_country_event(interpreter, events, "shishan_code.60", country), "receipt recovery event cannot run")
        calls = list(interpreter.event_calls[offset:])
        dispatched = []
        for call in calls:
            if call["days"] == 0 and call["id"] in {"shishan_code.10", "shishan_code.20", "shishan_code.30", "shishan_code.31"}:
                dispatched.append((call["id"], run_country_event(interpreter, events, call["id"], country)))
        return dispatched

    cases = 0
    for suffix, event_id in (("maintain", "10"), ("optimize", "30")):
        flag = f"shishan_code_{suffix}_success_pending"
        for refactored in (False, True):
            for ids in (set(), set(range(1, 7))):
                interpreter, country = fixture(ids)
                country.flags.add(flag)
                if refactored:
                    country.flags.add("shishan_code_refactored")
                dispatched = recover(interpreter, country)
                require((f"shishan_code.{event_id}", True) in dispatched, f"saved {suffix} receipt not recovered across current state")
                equal(country.variables["shishan_code_maintenance_count"], Decimal(8), "one recovered success increments n once")
                require(flag not in country.flags, "successful receipt was not consumed")
                if ids:
                    require("shishan_code_reward_pending" in country.flags, "recovered receipt must preserve a real choice ticket")
                else:
                    equal(country.variables["shishan_code_architecture_repeat_count"], Decimal(1), "recovered exhausted receipt gives one repeat")
                before = reward_snapshot(interpreter, country)
                require(not run_country_event(interpreter, events, f"shishan_code.{event_id}", country), "consumed receipt replay must fail trigger")
                equal(reward_snapshot(interpreter, country), before, "receipt callback replay cannot change n/R/cd/grants")
                if suffix == "optimize" and not refactored:
                    require("shishan_code.31" not in interpreter.events and "shishan_code.32" not in interpreter.events, "optimization receipt in a relapsed state cannot roll another relapse")
                cases += 1
    # A new successful receipt waits behind the old unconfirmed ticket.
    interpreter, country = fixture(set(range(1, 7)))
    country.flags.add("shishan_code_reward_ticket_ready")
    interpreter.named("shishan_code_award_reward", country)
    original_slots = reward_slots(country)
    country.flags.add("shishan_code_maintain_success_pending")
    equal(recover(interpreter, country), [], "unconfirmed ticket defers the next receipt")
    equal(country.variables["shishan_code_maintenance_count"], Decimal(7), "deferred receipt cannot increment n")
    equal(reward_slots(country), original_slots, "deferred receipt cannot replace candidates")
    run_country_event(interpreter, events, "shishan_code.11", country)
    require("SHISHAN_CODE_MAINTAIN" not in country.projects, "cannot start the next maintenance while receipt is unconsumed")
    selected = next(index for index in reward_slots(country) if index)
    interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
    require(("shishan_code.10", True) in recover(interpreter, country), "deferred receipt not resumed after old ticket confirmation")
    equal(country.variables["shishan_code_maintenance_count"], Decimal(8), "deferred receipt consumed once")
    cases += 1
    # Simultaneous receipts queue in order; the second callback's trigger
    # rechecks pending after the first has created its ticket.
    interpreter, country = fixture(set(range(1, 9)))
    country.flags.update({"shishan_code_maintain_success_pending", "shishan_code_optimize_success_pending"})
    dispatched = recover(interpreter, country)
    equal(dispatched, [("shishan_code.10", True), ("shishan_code.30", False)], "simultaneous receipts cannot overwrite first pending ticket")
    require("shishan_code_optimize_success_pending" in country.flags, "second successful receipt must remain pending")
    selected = next(index for index in reward_slots(country) if index)
    interpreter.named(f"shishan_code_reward_claim_{selected:02d}_effect", country)
    require(("shishan_code.30", True) in recover(interpreter, country), "second receipt not recovered after first choice")
    equal(country.variables["shishan_code_maintenance_count"], Decimal(9), "two successful receipts settle twice")
    cases += 1
    # A completed cleanup can precede the pending maintenance callback.
    interpreter, country = fixture(set(range(1, 7)))
    country.flags.update({"shishan_code_clean_success_pending", "shishan_code_maintain_success_pending"})
    equal(recover(interpreter, country), [("shishan_code.20", True), ("shishan_code.10", True)], "cleanup does not invalidate a prior earned maintenance receipt")
    require("shishan_code_refactored" in country.flags, "cleanup state persisted")
    equal(country.variables["shishan_code_maintenance_count"], Decimal(8), "maintenance reward after cleanup earned once")
    cases += 1
    for flag, refactored in (("shishan_code_clean_success_pending", True), ("shishan_code_relapse_pending", False)):
        interpreter, country = fixture(set(range(1, 7)))
        country.flags.add(flag)
        if refactored:
            country.flags.add("shishan_code_refactored")
        equal(recover(interpreter, country), [], "completed-state stale callback receipt does not replay")
        require(flag not in country.flags and "shishan_code_callback_state_invalid" in country.flags, "stale state receipt must leave a diagnostic and be cleared")
        equal(country.variables["shishan_code_maintenance_count"], Decimal(7), "stale state receipt has no maintenance reward")
        cases += 1
    return {
        "receipt_cases": cases, "saved_success_recovery": "offline queued-callback fixture",
        "opaque_engine_domains": ["situation mutation", "Vivhite refresh", "species state clone"],
        "runtime_reload": "NOT RUN",
    }


def check_numeric(mod: Path) -> dict:
    definitions = read_script(mod / "common/script_values/shishan_code_values.txt")
    # Fixed independent examples expose coefficient, floor, cross-job sum, and
    # lower-bound errors without reading generator constants as expectations.
    samples = (
        (0, 0, 0, "1"), (0, 99, 0, "1"), (0, 100, 0, ".75"),
        (0, 199, 0, ".75"), (0, 200, 0, ".5"), (0, 299, 0, ".5"),
        (0, 300, 0, ".25"), (0, 399, 0, ".25"), (0, 400, 0, ".2"),
        (0, 50, 50, ".75"), (0, 99, 1, ".75"), (0, 10000, 0, ".2"),
        (1, 0, 0, "1.25"), (1, 100, 0, "1"), (1, 300, 0, ".5"),
        (1, 400, 0, ".25"), (1, 500, 0, ".2"),
        (5, 0, 0, "2.25"), (5, 100, 0, "2"), (5, 700, 0, ".5"),
        (5, 800, 0, ".25"), (5, 900, 0, ".2"),
    )
    for n, individual, drone, expected in samples:
        evaluator = Values(definitions, {"shishan_code_maintenance_count": n}, {
            "shishan_code_maintainer": individual, "shishan_code_maintainer_drone": drone,
        })
        equal(evaluator.named("shishan_code_monthly_progress"), Decimal(expected), f"monthly n={n}, J={individual}+{drone}")
    for n, expected in ((0, (2000, 8000, 4000)), (1, (3000, 10000, 6000)), (5, (7000, 18000, 14000)), (1000, (1002000, 2008000, 2004000))):
        evaluator = Values(definitions, {"shishan_code_maintenance_count": n})
        for suffix, cost in zip(("maintenance", "clean", "optimization"), expected):
            equal(evaluator.named(f"shishan_code_{suffix}_cost"), Decimal(cost), f"{suffix} cost n={n}")
    origin = block(one(read_script(mod / "common/governments/civics/shishan_code_origin.txt"), "origin_shishan_code"))
    budget = block(one(origin, "modifier"))
    equal(number(one(budget, "MACHINE_species_trait_points_add")), Decimal(-6), "trait point budget")
    equal(number(one(budget, "MACHINE_species_trait_picks_add")), Decimal(3), "trait selection budget")
    jobs = read_script(mod / "common/pop_jobs/shishan_code_jobs.txt")
    for job in ("shishan_code_maintainer", "shishan_code_maintainer_drone"):
        resources = block(one(block(one(jobs, job)), "resources"))
        produces = block(one(resources, "produces"))
        equal(number(one(produces, "society_research")), Decimal(3), f"{job} society base")
        equal(number(one(produces, "unity")), Decimal(1), f"{job} unity base")
        upkeep = block(one(resources, "upkeep"))
        resource, cost = ("consumer_goods", "1.5") if job == "shishan_code_maintainer" else ("energy", "3")
        equal(number(one(upkeep, resource)), Decimal(cost), f"{job} upkeep retained")
    stages = read_script(mod / "common/static_modifiers/shishan_code_stages.txt")
    for stage, output, upkeep in ((1, ".25", "-.25"), (3, "-.125", ".125"), (4, "-.25", ".25"), (5, "-.375", ".375")):
        body = block(one(stages, f"shishan_code_stage_{stage}"))
        for resource in PRODUCTION_RESOURCES:
            equal(number(one(body, f"country_{resource}_produces_mult")), Decimal(output), f"stage {stage} {resource}")
        for key in ("ship_weapon_damage", "ship_speed_mult"):
            equal(number(one(body, key)), Decimal(output), f"stage {stage} {key}")
        equal(number(one(body, "planet_jobs_upkeep_mult")), Decimal(upkeep), f"stage {stage} upkeep")
    equal(number(one(block(one(stages, "shishan_code_refactored_jobs")), "planet_jobs_produces_mult")), Decimal(".25"), "refactor output")
    equal(number(one(block(one(stages, "shishan_code_vivhite_base")), "country_society_tech_research_speed")), Decimal(".05"), "Vivhite base society")
    equal(number(one(block(one(stages, "shishan_code_vivhite_society_step")), "country_society_tech_research_speed")), Decimal(".025"), "Vivhite society step")
    equal(number(one(block(one(stages, "shishan_code_vivhite_base")), "country_engineering_tech_research_speed")), Decimal(".10"), "Vivhite base engineering")
    equal(number(one(block(one(stages, "shishan_code_vivhite_engineering_step")), "country_engineering_tech_research_speed")), Decimal(".05"), "Vivhite engineering step")
    leader = block(one(read_script(mod / "common/traits/shishan_code_leader.txt"), "leader_trait_shishan_code_vivhite"))
    equal(block(one(leader, "self_modifier")), [Entry("leaders_unity_upkeep_mult", "=", "-1")], "Vivhite own unity upkeep only")
    situation = block(one(read_script(mod / "common/situations/shishan_code_situation.txt"), "situation_shishan_code"))
    ends = [number(one(block(entry.value), "end")) for entry in block(one(situation, "stages"))]
    equal(ends, [Decimal(v) for v in (250, 500, 750, 950, 1000)], "stage boundaries")
    projects = read_script(mod / "common/special_projects/shishan_code_projects.txt")
    for project in (entry for entry in projects if entry.key == "special_project"):
        department = one(block(project.value), "tech_department")
        equal(department, "society_technology", "project research department")
    return {"monthly_examples": len(samples), "cost_examples": 12, "stage_resources": len(PRODUCTION_RESOURCES)}


def localisation_entries(path: Path, language: str) -> dict[str, str]:
    raw = path.read_bytes()
    require(raw.startswith(b"\xef\xbb\xbf"), f"localisation missing UTF-8 BOM: {path}")
    text = raw.decode("utf-8-sig")
    require("\ufffd" not in text, f"replacement character: {path}")
    lines = text.splitlines()
    require(lines and lines[0].strip() == f"l_{language}:", f"wrong localisation header: {path}")
    result = {}
    for line_number, line in enumerate(lines[1:], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = LOC_ENTRY.fullmatch(line)
        require(match is not None, f"malformed localisation {path}:{line_number}")
        key, value = match.groups()
        require(key not in result, f"duplicate localisation key {key}: {path}")
        require(bool(value.strip()), f"empty localisation key {key}: {path}")
        result[key] = value
    return result


def game_localisation_keys(game: Path | None, language: str) -> set[str]:
    if game is None:
        return set()
    keys = set()
    for path in (game / "localisation").rglob(f"*_l_{language}.yml"):
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = re.match(r'^\s*([A-Za-z0-9_.-]+):', line)
            if match:
                keys.add(match[1])
    return keys


def check_localisation(mod: Path, game: Path | None = None) -> dict:
    dictionaries = {}
    files = 0
    for language in LANGUAGES:
        directory = mod / "localisation" / language
        require(directory.is_dir(), f"missing language directory: {language}")
        entries = {}
        paths = sorted(directory.glob("*.yml"))
        require(bool(paths), f"empty language directory: {language}")
        for path in paths:
            parsed = localisation_entries(path, language)
            require(not entries.keys() & parsed.keys(), f"duplicate keys across {language} files")
            entries.update(parsed)
            files += 1
        dictionaries[language] = entries
    chinese = dictionaries["simp_chinese"]
    full_name_keys = {key for key, value in chinese.items() if value == FULL_NAME}
    require(bool(full_name_keys), "full Chinese architecture name missing or truncated")
    equal(len(FULL_NAME), 18, "full name characters")
    equal(len(FULL_NAME.encode("utf-8")), 54, "full name UTF-8 bytes")
    reference_count = 0
    for language, entries in dictionaries.items():
        equal(set(entries), set(chinese), f"localisation key completeness {language}")
        vanilla = game_localisation_keys(game, language)
        for key, value in entries.items():
            if language != "simp_chinese":
                require(FULL_NAME not in value, f"Chinese placeholder in {language}:{key}")
                if language not in ("japanese", "korean"):
                    require(re.search(r"[\u3400-\u9fff]", value) is None, f"Chinese placeholder in {language}:{key}")
            require(value.count("$") % 2 == 0, f"unbalanced localisation reference {language}:{key}")
            for ref in re.findall(r"\$([^$]+)\$", value):
                reference_count += 1
                ref = ref.split("|", 1)[0]
                if ref.startswith(("shishan_", "trait_shishan_", "leader_trait_shishan_", "origin_shishan_", "situation_shishan_", "SHISHAN_")) or game is not None:
                    require(ref in entries or ref in vanilla, f"unresolved localisation reference {language}:{key} -> {ref}")
            require(value.count("\u00a3") % 2 == 0, f"unbalanced resource icon {language}:{key}")
            require(value.count("[") == value.count("]"), f"unbalanced dynamic localisation {language}:{key}")
            require(not re.search(r"\b(?:trait_shishan_|shishan_code_)[a-z0-9_]+\b", re.sub(r"\$[^$]+\$|\[[^]]*\]", "", value)), f"raw mod key in localisation {language}:{key}")
    # Reject accidental self-references and loops among the mod's local keys.
    for language, entries in dictionaries.items():
        active, complete = set(), set()

        def visit(key: str) -> None:
            require(key not in active, f"localisation reference cycle {language}:{key}")
            if key in complete:
                return
            active.add(key)
            for ref in re.findall(r"\$([^$|]+)(?:\|[^$]*)?\$", entries[key]):
                if ref in entries:
                    visit(ref)
            active.remove(key)
            complete.add(key)

        for key in entries:
            visit(key)
    def resolve_single_reference(key: str, entries: dict[str, str]) -> str:
        value = entries[key]
        match = re.fullmatch(r"\$([^$]+)\$", value)
        return resolve_single_reference(match[1], entries) if match and match[1] in entries else value
    if (mod / "common/static_modifiers/shishan_code_architecture_modifiers.txt").exists():
        require("shishan_code_architecture_jobs" in chinese, "architecture modifier display name missing")
        equal(resolve_single_reference("shishan_code_architecture_jobs", chinese), FULL_NAME, "architecture modifier complete display name")
    used_local_keys = set()
    for path in sorted((*((mod / "common").rglob("*.txt")), *((mod / "events").rglob("*.txt")))):
        for entry in walk(read_script(path)):
            if entry.key in ("title", "desc", "name", "custom_tooltip", "custom_description", "custom_catch_phrase") and isinstance(entry.value, str):
                name = entry.value.strip('"')
                if name.startswith(("shishan_", "trait_shishan_", "leader_trait_shishan_", "origin_shishan_", "NAME_shishan_")):
                    used_local_keys.add(name)
    for language, entries in dictionaries.items():
        missing = used_local_keys - entries.keys()
        require(not missing, f"script localisation keys missing in {language}: {sorted(missing)}")
    return {
        "languages": list(LANGUAGES), "files": files, "keys_per_language": len(chinese),
        "full_name_keys": sorted(full_name_keys), "full_name_characters": 18,
        "full_name_utf8_bytes": 54, "references": reference_count,
        "script_localisation_keys": len(used_local_keys),
        "vanilla_reference_scope": "checked" if game else "not checked without --game",
        "non_chinese_runtime": "out_of_scope",
    }


def validate_package(mod: Path, game: Path | None = None) -> dict:
    checks = []
    for name, check in (("numeric_contract", lambda: check_numeric(mod)), ("architecture_data_contract", lambda: check_architecture(mod)), ("reward_state_contract", lambda: check_rewards(mod)), ("receipt_recovery_contract", lambda: check_receipt_recovery(mod)), ("localisation_contract", lambda: check_localisation(mod, game))):
        try:
            details = check()
        except (ContractError, OSError, UnicodeError, ArithmeticError) as error:
            checks.append({"name": name, "status": "FAIL", "error": str(error)})
        else:
            checks.append({"name": name, "status": "PASS", "details": details})
    files = sorted(path for path in mod.rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in files:
        relative = path.relative_to(mod).as_posix()
        digest.update(relative.encode("utf-8") + b"\0" + hashlib.sha256(path.read_bytes()).digest())
    return {
        "status": "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL",
        "semantic_scope": "offline emitted-data contracts only; not engine acceptance",
        "mod": str(mod.resolve()), "mod_tree_sha256": digest.hexdigest(), "file_count": len(files),
        "checks": checks,
        "not_run": ["Stellaris", "UI/OCR/long-name layout", "save reload", "natural playthrough", "economic independent multiplication in engine", "performance"],
        "non_chinese_runtime": "out_of_scope",
        "required_package_validator": "open_kaishek/tools/accept_stellaris_mod.py",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod", type=Path, default=DEFAULT_MOD)
    parser.add_argument("--game", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = validate_package(args.mod, args.game)
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
