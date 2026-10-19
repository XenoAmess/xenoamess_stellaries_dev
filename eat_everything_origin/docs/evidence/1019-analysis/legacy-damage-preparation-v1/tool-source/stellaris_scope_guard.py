"""Finite, build-bound population-scope preflight; never a full P validator."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re


PROFILE = "stellaris-4.5.2-population-scopes-v2"
VALUE_PROFILE = "stellaris-4.5.2-referenced-script-value-shapes-v1"
BUILDS = {("v4.5.2", "400df27c82ddc845aa9dce79bd468d81f18f060d299cd263e3afa93aef4f7a83")}
POPULATION_SCOPES = {
    "pop_amount": frozenset({"planet", "country", "ship", "galactic_object", "pop_faction", "sector", "colony"}),
    "pop_group_size": frozenset({"pop_group"}),
}
ITERATORS = {
    **{f"{mode}_{kind}_pop_group": "pop_group" for mode in ("every", "any", "random", "count") for kind in ("owned", "species")},
    **{f"{mode}_owned_species": "species" for mode in ("every", "any", "random", "count")},
    "every_trait_of_species": "trait",
}
SCOPES = {"owner": "country", "controller": "country", "species": "species", "owner_main_species": "species", "planet": "planet", "capital_scope": "colony"}
EVENTS = {"country_event": "country", "planet_event": "planet", "ship_event": "ship", "fleet_event": "fleet", "leader_event": "leader", "pop_event": "pop"}
# These contain expressions/effects in the current scope, not new objects.
TRANSPARENT = frozenset({
    "if", "else_if", "else", "limit", "trigger", "potential", "allow", "AND", "OR", "NOT", "NOR", "NAND",
    "hidden_trigger", "hidden_effect", "immediate", "after", "option", "on_success", "on_cancel", "on_fail",
    "set_variable", "change_variable", "multiply_variable", "divide_variable", "subtract_variable", "check_variable",
    "min_variable", "max_variable", "modulo_variable", "round_variable", "export_trigger_value_to_variable",
    "modifier", "weights", "random_list", "random", "while", "switch", "case", "default", "custom_tooltip",
})


@dataclass(frozen=True)
class Token:
    text: str
    line: int
    column: int
    quoted: bool = False


@dataclass(frozen=True)
class Entry:
    key: Token
    op: str | None
    value: Token | list["Entry"] | None


def tokens(source: str) -> list[Token]:
    """Ignore comments and retain quotedness; not a replacement for Kaishek CST."""
    result = []
    offset, line, column = 0, 1, 1
    while offset < len(source):
        char = source[offset]
        if char.isspace():
            offset += 1
            line, column = (line + 1, 1) if char == "\n" else (line, column + 1)
            continue
        if char == "#":
            end = source.find("\n", offset)
            offset = len(source) if end < 0 else end
            continue
        start, start_column = offset, column
        if char == '"':
            offset += 1
            while offset < len(source):
                if source[offset] == "\\":
                    offset += 2
                elif source[offset] == '"':
                    offset += 1
                    break
                else:
                    offset += 1
            else:
                raise ValueError(f"unterminated string at {line}:{column}")
            text = source[start:offset]
            result.append(Token(text, line, column, True))
        elif char in "{}=<>!":
            offset += 1
            if offset < len(source) and source[offset] == "=" and char != "{" and char != "}":
                offset += 1
            text = source[start:offset]
            result.append(Token(text, line, column))
        else:
            while offset < len(source) and not source[offset].isspace() and source[offset] not in '#{}"=<>!':
                offset += 1
            text = source[start:offset]
            result.append(Token(text, line, column))
        if "\n" in text:
            line += text.count("\n")
            column = len(text.rsplit("\n", 1)[1]) + 1
        else:
            column = start_column + len(text)
    return result


def tree(source: str) -> list[Entry]:
    stream = tokens(source)
    index = 0

    def block(nested: bool = False) -> list[Entry]:
        nonlocal index
        result = []
        while index < len(stream):
            key = stream[index]
            index += 1
            if key.text == "}" and not key.quoted:
                if not nested:
                    raise ValueError("unmatched closing brace")
                return result
            if key.text == "{" and not key.quoted:
                result.append(Entry(key, None, block(True)))
                continue
            op = None
            value = None
            if index < len(stream) and not stream[index].quoted and stream[index].text in {"=", "==", "!=", ">", "<", ">=", "<="}:
                op = stream[index].text
                index += 1
                if index == len(stream) or stream[index].text == "}":
                    raise ValueError("missing assignment value")
                value = stream[index]
                index += 1
                if value.text == "{" and not value.quoted:
                    value = block(True)
            result.append(Entry(key, op, value))
        if nested:
            raise ValueError("unclosed brace")
        return result

    return block()


def target_exports(token: Token) -> list[tuple[list[str], str]]:
    if token.quoted:
        return []
    # Match complete exports only, not variables such as my_trigger:pop_amount.
    match = re.fullmatch(r"(?:(?P<scopes>.+)\.)?trigger:(pop_amount|pop_group_size)", token.text)
    return [(match.group("scopes").split(".") if match.group("scopes") else [], match.group(2))] if match else []


def target_comparison(token: Token) -> tuple[list[str], str] | None:
    if token.quoted:
        return None
    parts = token.text.split(".")
    return (parts[:-1], parts[-1]) if parts[-1] in POPULATION_SCOPES else None


def targets(entries: list[Entry]) -> bool:
    for entry in entries:
        if target_comparison(entry.key) and isinstance(entry.value, Token):
            return True
        if isinstance(entry.value, list):
            if targets(entry.value):
                return True
        elif isinstance(entry.value, Token) and target_exports(entry.value):
            return True
    return False


def saved_target_name(value: Token | list[Entry] | None) -> str | None:
    if isinstance(value, Token):
        name = value.text[1:-1] if value.quoted else value.text
        if re.fullmatch(r"[A-Za-z_]\w*", name):
            return name
    return None


def declared_saved_targets(entries: list[Entry]) -> set[str]:
    result = set()
    for entry in entries:
        if not entry.key.quoted and entry.key.text in {"save_event_target_as", "save_global_event_target_as"}:
            name = saved_target_name(entry.value)
            if name:
                result.add(name)
        if isinstance(entry.value, list):
            result.update(declared_saved_targets(entry.value))
    return result


def check_population_scopes(source: str, path: str, blocked_targets: set[str] | None = None) -> dict:
    """Check the registered slice only; callers must establish profile identity."""
    diagnostics = []
    checked = 0
    saved_targets: dict[str, str] = {}
    saved_points: dict[str, set[str | None]] = {}
    try:
        document = tree(source)
    except (ValueError, RecursionError) as error:
        return {"status": "UNKNOWN", "checked": 0, "diagnostics": [{"code": "STELLARIS_SCOPE_UNKNOWN", "path": path, "reason": f"finite reader cannot classify syntax: {error}"}]}

    def promote(parts: list[str], chain: tuple[str | None, ...], root: str | None) -> tuple[str | None, ...]:
        for part in parts:
            original = part
            part = part.lower()
            if part == "this":
                target = chain[-1]
            elif part == "root":
                target = root
            elif re.fullmatch(r"(?:prev)+", part):
                distance = len(part) // 4
                target = chain[-1 - distance] if len(chain) > distance else None
            elif part.startswith("event_target:"):
                target = saved_targets.get(original.split(":", 1)[1])
            else:
                target = SCOPES.get(part)
            chain = (*chain, target)
        return chain

    def inspect(token: Token, opcode: str, chain: tuple[str | None, ...]) -> None:
        nonlocal checked
        checked += 1
        actual = chain[-1]
        if actual not in POPULATION_SCOPES[opcode]:
            diagnostics.append({"code": "STELLARIS_SCOPE_UNKNOWN" if actual is None else "STELLARIS_SCOPE_MISMATCH", "path": path, "line": token.line, "column": token.column, "opcode": opcode, "scope": actual or "UNKNOWN", "allowed_scopes": sorted(POPULATION_SCOPES[opcode]), "profile": PROFILE})

    def walk(entries: list[Entry], chain: tuple[str | None, ...], root: str | None, depth: int = 0, collect: bool = False) -> None:
        for entry in entries:
            key = entry.key.text
            if isinstance(entry.value, Token):
                if collect:
                    if not entry.key.quoted and key in {"save_event_target_as", "save_global_event_target_as"}:
                        name = saved_target_name(entry.value)
                        if name:
                            saved_points.setdefault(name, set()).add(chain[-1])
                else:
                    comparison = target_comparison(entry.key)
                    if comparison:
                        parts, opcode = comparison
                        inspect(entry.key, opcode, promote(parts, chain, root))
                    for parts, opcode in target_exports(entry.value):
                        inspect(entry.value, opcode, promote(parts, chain, root))
            elif isinstance(entry.value, list):
                if not collect and not targets(entry.value):
                    continue
                if entry.key.quoted:
                    next_chain, next_root = (*chain, None), root
                elif depth == 0 and key in EVENTS and path.replace("\\", "/").startswith("events/"):
                    next_root = EVENTS[key]
                    next_chain = (next_root,)
                elif key in ITERATORS:
                    next_chain, next_root = (*chain, ITERATORS[key]), root
                elif key.lower() in {"root", "this"} or re.fullmatch(r"(?:prev)+", key.lower()) or key.lower() in SCOPES or (key.startswith("event_target:") and "." not in key):
                    next_chain, next_root = promote([key], chain, root), root
                elif "." in key and all(part.lower() in SCOPES or part.lower() in {"this", "root"} or part.startswith("event_target:") or re.fullmatch(r"(?:prev)+", part.lower()) for part in key.split(".")):
                    next_chain, next_root = promote(key.split("."), chain, root), root
                elif key in TRANSPARENT or (chain[-1] is not None and re.fullmatch(r"\d+(?:\.\d+)?", key)):
                    next_chain, next_root = chain, root
                else:
                    # Unknown containers/scope changes cannot inherit certainty.
                    next_chain, next_root = (*chain, None), root
                walk(entry.value, next_chain, next_root, depth + 1, collect)

    # Collect with an empty target environment. Unknown/alias/cyclic save points
    # remain unknown; a later known save must not silently erase them.
    walk(document, (None,), None, collect=True)
    saved_targets.update({name: next(iter(types)) for name, types in saved_points.items() if len(types) == 1 and None not in types and name not in (blocked_targets or set())})
    walk(document, (None,), None)
    status = "FAIL" if any(item["code"] == "STELLARIS_SCOPE_MISMATCH" for item in diagnostics) else "UNKNOWN" if diagnostics else "PASS" if checked else "NOT_APPLICABLE"
    return {"status": status, "checked": checked, "saved_target_scopes": saved_targets, "diagnostics": diagnostics}


def population_scope_preflight(package: Path, game: Path, scripts: list[tuple[Path, str]], game_sha: str | None) -> dict:
    """Bind the finite rules to the installed build and untouched alias."""
    relevant = []
    declaration_paths: dict[str, set[Path]] = {}
    for path, source in scripts:
        try:
            document = tree(source)
            needed = targets(document)
            for name in declared_saved_targets(document):
                declaration_paths.setdefault(name, set()).add(path)
        except (ValueError, RecursionError):
            # The main parser diagnoses syntax; the finite layer is conservative.
            needed = True
        if needed:
            relevant.append((path, source))
    if not relevant:
        return {"status": "NOT_APPLICABLE", "profile": PROFILE, "checked": 0, "diagnostics": []}
    reason = None
    settings = game / "launcher-settings.json"
    try:
        version = json.loads(settings.read_text(encoding="utf-8-sig")).get("rawVersion")
    except (OSError, ValueError):
        version = None
    if (version, game_sha) not in BUILDS:
        reason = "population scope rules are not registered for this exact game build"
    alias_relative = Path("common/scripted_triggers/00_scripted_triggers_pop.txt")
    try:
        alias = tree((game / alias_relative).read_text(encoding="utf-8-sig"))
        definitions = [entry for entry in alias if entry.key.text == "pop_amount"]
        valid = len(definitions) == 1 and isinstance(definitions[0].value, list) and len(definitions[0].value) == 1
        body = definitions[0].value[0] if valid else None
        if not body or body.key.text != "count_owned_pop_amount" or body.op != "=" or body.value != []:
            reason = "installed pop_amount alias differs from the registered rule"
    except (OSError, ValueError, RecursionError):
        reason = "installed pop_amount alias is missing or unreadable"
    # Either overriding the source file or redefining the alias changes semantics.
    for path, source in scripts:
        relative = path.relative_to(package).as_posix()
        if relative == "descriptor.mod":
            try:
                replaced = [entry.value.text.strip('"').strip("/") for entry in tree(source) if entry.key.text == "replace_path" and isinstance(entry.value, Token)]
            except (ValueError, RecursionError):
                replaced = ["common/scripted_triggers"]
            if any(str(alias_relative).replace("\\", "/").startswith(prefix + "/") for prefix in replaced):
                reason = "Mod replace_path removes the registered pop_amount alias"
        if relative.startswith("common/scripted_triggers/"):
            try:
                overridden = any(entry.key.text.strip('"') == "pop_amount" for entry in tree(source))
            except (ValueError, RecursionError):
                overridden = True
            if overridden or path.relative_to(package) == alias_relative:
                reason = "Mod overrides the registered pop_amount alias or its source file"
    diagnostics, checked = [], 0
    blocked_targets = {name for name, paths in declaration_paths.items() if len(paths) > 1}
    for path, source in relevant:
        relative = path.relative_to(package).as_posix()
        if reason:
            diagnostics.append({"code": "STELLARIS_SCOPE_UNKNOWN", "path": str(path), "reason": reason, "profile": PROFILE})
        else:
            result = check_population_scopes(source, relative, blocked_targets)
            checked += result["checked"]
            diagnostics.extend({**item, "path": str(path)} for item in result["diagnostics"])
    status = "FAIL" if any(item["code"] == "STELLARIS_SCOPE_MISMATCH" for item in diagnostics) else "UNKNOWN" if diagnostics else "PASS"
    return {"status": status, "profile": PROFILE, "checked": checked, "relevant_files": len(relevant), "diagnostics": diagnostics}


def script_value_shape_preflight(package: Path, game: Path, scripts: list[tuple[Path, str]], game_sha: str | None) -> dict:
    """Reject referenced ordinary numeric scalar definitions, not @ constants.

    This does not execute values, resolve missing third-party definitions, or
    certify post-init macro expansion depth.
    """
    definitions: dict[str, list[tuple[Path, Entry]]] = {}
    references: dict[str, list[dict]] = {}
    diagnostics = []

    def exports(entries: list[Entry], path: Path) -> None:
        for entry in entries:
            if isinstance(entry.value, list):
                exports(entry.value, path)
            elif isinstance(entry.value, Token) and not entry.value.quoted:
                match = re.fullmatch(r"(?:[A-Za-z_][\w:@?]*\.)*value:([A-Za-z_]\w*)(?:\|[^\r\n]*)?", entry.value.text)
                if match:
                    references.setdefault(match.group(1), []).append({"path": str(path), "line": entry.value.line, "column": entry.value.column})

    for path, source in scripts:
        try:
            document = tree(source)
        except (ValueError, RecursionError):
            # Syntax diagnostics remain the Kaishek parser's responsibility.
            continue
        exports(document, path)
        if path.relative_to(package).as_posix().startswith("common/script_values/"):
            for entry in document:
                name = entry.key.text.strip('"')
                if entry.op == "=" and re.fullmatch(r"[A-Za-z_]\w*", name):
                    definitions.setdefault(name, []).append((path, entry))
    candidates = {name: entries for name, entries in definitions.items() if name in references and any(isinstance(entry.value, Token) for _, entry in entries)}
    if not candidates:
        return {"status": "NOT_APPLICABLE", "profile": VALUE_PROFILE, "checked": 0, "diagnostics": []}
    try:
        version = json.loads((game / "launcher-settings.json").read_text(encoding="utf-8-sig")).get("rawVersion")
    except (OSError, ValueError):
        version = None
    for name, entries in candidates.items():
        path, definition = entries[0]
        numeric_scalar = isinstance(definition.value, Token) and not definition.value.quoted and re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", definition.value.text)
        known = (version, game_sha) in BUILDS and len(entries) == 1 and numeric_scalar
        reason = "ordinary named script values referenced with value: require a block definition; @ constants are separate" if known else "unregistered build, duplicate definitions or unregistered scalar form; value shape is UNKNOWN"
        diagnostics.append({"code": "STELLARIS_SCRIPT_VALUE_SCALAR_DEFINITION" if known else "STELLARIS_SCRIPT_VALUE_UNKNOWN", "path": str(path), "line": definition.key.line, "column": definition.key.column, "name": name, "references": references[name], "profile": VALUE_PROFILE, "reason": reason})
    status = "FAIL" if any(item["code"] == "STELLARIS_SCRIPT_VALUE_SCALAR_DEFINITION" for item in diagnostics) else "UNKNOWN"
    return {"status": status, "profile": VALUE_PROFILE, "checked": len(candidates), "diagnostics": diagnostics}
