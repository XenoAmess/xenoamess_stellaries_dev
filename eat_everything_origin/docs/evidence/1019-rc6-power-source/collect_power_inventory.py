"""Read the bound RC6 native save and component sources; never operate the game.

This is a report reproduction script, not a Mod validator or a runtime power getter.
It writes only its own evidence directory. No acceptance Boolean is assigned.
"""
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

OUT = Path(__file__).resolve().parent
EAT = OUT.parents[2]
NATIVE = Path("C:/SteamLibrary/steamapps/common/Stellaris")
RUN = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/runs/20261019T150008Z")
ART = Path("C:/Users/1/AppData/Local/xenoamess_stellaries_dev/artifacts/1019-implementation/runs/20261019T150008Z")
sys.path.insert(0, str(EAT / "tools"))
import audit_save as audit


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ref(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "sha256": sha(raw), "bytes": len(raw)}


def direct(body, key):
    return [(value, block) for name, value, block in audit.fields(body) if name == key]


def scalar(body, key):
    values = direct(body, key)
    if len(values) != 1 or values[0][1]:
        raise ValueError("expected unique scalar: " + key)
    return values[0][0].strip('"')


def line(text, pattern):
    match = re.search(pattern, text, re.MULTILINE)
    if match is None:
        raise ValueError("missing source line: " + pattern)
    return text.count("\n", 0, match.start()) + 1


sources = {}


def source(path):
    if path.is_relative_to(NATIVE):
        rel = Path("native") / path.relative_to(NATIVE)
    elif path.is_relative_to(RUN / "mod/eep-1019"):
        rel = Path("mod") / path.relative_to(RUN / "mod/eep-1019")
    elif path.is_relative_to(RUN):
        rel = Path("run") / path.relative_to(RUN)
    else:
        rel = Path("project") / path.relative_to(EAT)
    key = rel.as_posix()
    if key not in sources:
        raw = path.read_bytes()
        target = OUT / "source" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        sources[key] = {**ref(path), "archived": target.relative_to(EAT).as_posix()}
    return key


save_path = ART / "r6puyearui.sav"
save_raw = save_path.read_bytes()
gamestate_raw = zipfile.ZipFile(io.BytesIO(save_raw)).read("gamestate")
gamestate = gamestate_raw.decode("utf-8-sig")
roots = {key: value for key, value, block in audit.fields(gamestate)}
manifest_path = ART / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
mod = Path(manifest["copied_mod"])
assert mod == RUN / "mod/eep-1019"
receipt_path = ART / "r6puyearui.native-save.json"
receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
assert receipt["sha256"] == sha(save_raw)
assert manifest["language"] == "l_simp_chinese"
mod_hash_mismatches = [row["path"] for row in manifest["repository_mod_files"]
                       if sha((mod / row["path"]).read_bytes()) != row["sha256"]]
assert not mod_hash_mismatches
fleets = [(key, body) for key, body, block in audit.fields(roots["fleet"])
          if block and 'modifier="eep_mothership"' in body]
assert len(fleets) == 1
fleet_id, fleet = fleets[0]
ship_ids = audit.ids(audit.block(fleet, "ships"))
assert len(ship_ids) == 1
ship_id = str(ship_ids[0])
ship = audit.block(roots["ships"], ship_id)
design_id = scalar(audit.block(ship, "ship_design_implementation"), "design")
design = audit.block(roots["ship_design"], design_id)
stages = list(audit.tokens(audit.block(design, "growth_stages")))
# The native list is unnamed; take its sole outer brace pair without rewriting it.
assert stages[0][0] == "{" and stages[-1][0] == "}"
growth_stage = audit.block(design, "growth_stages")[stages[0][2]:stages[-1][1]]
assert scalar(growth_stage, "ship_size") == "juggernaut"
inventory = []
for section, block in direct(growth_stage, "section"):
    assert block
    for component, block in direct(section, "component"):
        assert block
        inventory.append({"kind": "slot", "slot": scalar(component, "slot"),
                          "component": scalar(component, "template")})
for component, block in direct(growth_stage, "required_component"):
    assert not block
    inventory.append({"kind": "required", "slot": None, "component": component.strip('"')})
assert Counter(row["kind"] for row in inventory) == {"slot": 50, "required": 6}
assert len({row["slot"] for row in inventory if row["kind"] == "slot"}) == 50

component_files = {path.relative_to(NATIVE).as_posix(): path
                   for path in (NATIVE / "common/component_templates").glob("*.txt")}
suppressed_native_files = [path.relative_to(mod).as_posix()
                          for path in (mod / "common/component_templates").glob("*.txt")
                          if path.relative_to(mod).as_posix() in component_files]
component_files.update({path.relative_to(mod).as_posix(): path
                        for path in (mod / "common/component_templates").glob("*.txt")})
definitions = defaultdict(list)
actual_keys = {row["component"] for row in inventory}
for path in component_files.values():
    text = path.read_text(encoding="utf-8-sig")
    local_vars = {key: value for key, value, block in audit.fields(text)
                  if key.startswith("@") and not block}
    for kind, body, block in audit.fields(text):
        if block and kind.endswith("_component_template"):
            # Ignore unrelated example-template dialect; fully parse actual keys below.
            match = re.search(r'^\s*key\s*=\s*"([^"\n]+)"', body, re.MULTILINE)
            if match and match.group(1) in actual_keys:
                key = scalar(body, "key")
                definitions[key].append((path, text, body, kind, local_vars))
globals_index = defaultdict(list)
global_files = {path.name: path for path in (NATIVE / "common/scripted_variables").glob("*.txt")}
global_files.update({path.name: path for path in (mod / "common/scripted_variables").glob("*.txt")})
for path in global_files.values():
    text = path.read_text(encoding="utf-8-sig")
    for key, value, block in audit.fields(text):
        if key.startswith("@") and not block:
            globals_index[key].append((path, text, value))

csv_index = defaultdict(list)
for filename in ("weapon_components.csv", "mutation_weapon_components.csv"):
    path = NATIVE / "common/component_templates" / filename
    if (mod / path.relative_to(NATIVE)).exists():
        path = mod / path.relative_to(NATIVE)
    text = path.read_text(encoding="utf-8-sig")
    rows = [(number, row) for number, row in enumerate(text.splitlines(), 1)
            if row.strip() and not row.lstrip().startswith("#")]
    header = next(csv.reader([rows[0][1]], delimiter=";"))
    assert header[0] == "key" and header[2] == "power"
    for number, row in rows[1:]:
        cells = next(csv.reader([row], delimiter=";"))
        csv_index[cells[0]].append((path, number, cells[2], header, row))

component_details = {}
for key in sorted({row["component"] for row in inventory}):
    assert len(definitions[key]) == 1, (key, len(definitions[key]))
    path, text, body, kind, local_vars = definitions[key][0]
    detail = {"template_kind": kind, "source": source(path),
              "key_line": line(text, r'^\s*key\s*=\s*"?' + re.escape(key) + r'"?\s*$')}
    power_fields = direct(body, "power")
    if power_fields:
        assert len(power_fields) == 1 and not power_fields[0][1]
        raw = power_fields[0][0]
        detail.update({"power_source_kind": "explicit_TXT", "power_expression": raw})
        power_match = re.search(r'^\s*power\s*=', body, re.MULTILINE)
        assert power_match is not None
        detail["power_line"] = text.count("\n", 0, text.find(body) + power_match.start()) + 1
        if raw.startswith("@"):
            if raw in local_vars:
                value = local_vars[raw]
                detail["variable_source"] = {"source": source(path),
                    "line": line(text, r'^\s*' + re.escape(raw) + r'\s*='), "value": value}
            else:
                assert len(globals_index[raw]) == 1, (raw, globals_index[raw])
                var_path, var_text, value = globals_index[raw][0]
                detail["variable_source"] = {"source": source(var_path),
                    "line": line(var_text, r'^\s*' + re.escape(raw) + r'\s*='), "value": value}
        else:
            value = raw
    else:
        assert kind == "weapon_component_template" and len(csv_index[key]) == 1
        csv_path, number, value, header, raw_row = csv_index[key][0]
        detail.update({"power_source_kind": "native_fixed_filename_CSV",
                       "csv_source": source(csv_path), "csv_line": number,
                       "csv_column_name": "power", "csv_column_zero_based": 2,
                       "csv_header": header, "raw_csv_row": raw_row})
    detail["signed_power"] = int(Decimal(value))
    assert Decimal(value) == detail["signed_power"]
    component_details[key] = detail
for row in inventory:
    row["signed_power"] = component_details[row["component"]]["signed_power"]
produced = sum(max(0, row["signed_power"]) for row in inventory)
consumed = sum(max(0, -row["signed_power"]) for row in inventory)
grouped = [{"component": key, "count": count,
            "signed_power_each": component_details[key]["signed_power"],
            "signed_power_total": count * component_details[key]["signed_power"]}
           for key, count in sorted(Counter(row["component"] for row in inventory).items())]

power_pattern = re.compile(r"\b(ship_reactor_power_(?:add|mult))\s*=\s*([^\s#}]+)")
scan = subprocess.run(["rg", "-l", "-g", "*.txt", r"ship_reactor_power_(add|mult)",
                       str(NATIVE), str(mod)], capture_output=True, text=True, encoding="utf-8", check=True)
occurrences = []
for name in scan.stdout.splitlines():
    path = Path(name)
    text = path.read_text(encoding="utf-8-sig")
    for name, body, block in audit.fields(text):
        if not block:
            continue
        for match in power_pattern.finditer(body):
            parent = scalar(body, "key") if direct(body, "key") else name
            active = (parent in component_details if "component_templates" in path.parts
                      else parent == "juggernaut")
            occurrences.append({"source": source(path), "definition": parent,
                "line": text.count("\n", 0, text.find(body) + match.start()) + 1,
                "modifier": match.group(1),
                "value": match.group(2), "applicability": "actual" if active else "other_component_or_hull"})
assert all(row["applicability"] != "actual" for row in occurrences)
assert all(Decimal(row["value"]) > 0 for row in occurrences)

country = audit.block(roots["country"], "0")
state = {}
for name, body in (("country0", country), ("fleet" + fleet_id, fleet), ("ship" + ship_id, ship),
                   ("system1", audit.block(roots["galactic_object"], "1"))):
    state[name] = [{"key": key, "block": block, "raw": value}
                  for key, value, block in audit.fields(body)
                  if key in ("timed_modifier", "modifier", "aura_modifier", "auras", "storm", "variables",
                             "government", "ethos", "tech_status", "ascension_perks", "active_policies")]
state_path = OUT / "actual-native-state-excerpts.txt"
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
design_path = OUT / "actual-design-1918.txt"
design_path.write_text(design, encoding="utf-8", newline="\n")
for path in (NATIVE / "common/component_templates/000_documentation.txt",
             NATIVE / "common/ship_sizes/18_juggernauts.txt",
             mod / "common/section_templates/eep_mothership.txt",
             mod / "common/static_modifiers/eep_modifiers.txt",
             RUN / "logs/script_documentation/modifiers.log", EAT / "tools/audit_save.py"):
    source(path)
exe_raw = (NATIVE / "stellaris.exe").read_bytes()
assert sha(exe_raw) == manifest["game_exe_sha256"]
fixed_csv_path = b"common/component_templates/weapon_components.csv"
binary_offset = exe_raw.find(fixed_csv_path)
assert binary_offset >= 0
image = ART / "r6pu-ship-maintenance-hover.jpg"
ocr_path = ART / "r6pu-ship-maintenance-hover.ocr.json"
ocr = json.loads(ocr_path.read_text(encoding="utf-8-sig"))
assert ocr["image_sha256"] == ref(image)["sha256"]
report = {
    "schema": "eep.1019.actual-native-component-power-source.v1",
    "status": "SOURCE_DERIVED_NOT_UI_MEASURED",
    "run_id": manifest["run_id"], "manifest": ref(manifest_path),
    "game_exe": {"path": manifest["game_exe"], "sha256": sha(exe_raw)},
    "mod_tree_sha256": manifest["copied_mod_tree_sha256"],
    "bound_mod_file_count": len(manifest["repository_mod_files"]),
    "bound_mod_hash_mismatches": mod_hash_mismatches,
    "language": manifest["language"], "enabled_mods": manifest["enabled_mods"],
    "native_save": ref(save_path), "native_receipt": ref(receipt_path),
    "gamestate_sha256": sha(gamestate_raw), "date": roots["date"].strip('"'),
    "actual_identity": {"country": 0, "fleet": int(fleet_id), "ship": int(ship_id),
                        "actual_design": int(design_id), "growth_stage": 0,
                        "ship_size": "juggernaut", "slots": 50, "required": 6},
    "actual_design_excerpt": ref(design_path), "actual_state_excerpts": ref(state_path),
    "source_loading": {"component_TXT_files_scanned": len(component_files),
                       "suppressed_native_component_TXT_files": suppressed_native_files,
                       "mod_CSV_files": [p.relative_to(mod).as_posix() for p in mod.rglob("*.csv")],
                       "weapon_CSV_EXE_literal_path_offset": binary_offset,
                       "boundary": "Fixed original CSV is documented and named in this exact EXE; no arbitrary new CSV is assumed loaded. This is source binding, not disassembly or a runtime getter."},
    "signed_power_semantics": "Native 000_documentation.txt:10: negative consumes; positive produces. The fixed weapon CSV header also explicitly names column index 2 power.",
    "inventory": inventory, "grouped_inventory": grouped, "component_details": component_details,
    "power_modifier_review": {
        "generated_public_ship_power_channels": ["ship_reactor_power_add", "ship_reactor_power_mult"],
        "scan_scope": "All *.txt under this native installation and the bound copied Mod, using rg; every declaration archived below.",
        "source_occurrences": occurrences,
        "actual_power_declaration_count": 0,
        "actual_state": "Country has only game_start timed modifier, no reactor research modifier; fleet only eep_mothership; ship has no timed modifier and its actual aura cache is ship_fire_rate_mult=.05 and ships_logistics_mult=-.75; system1 has no storm. Other native power declarations belong only to unequipped reactor boosters and other hulls. No technology, trait, tradition, civic, policy, aura or timed-modifier declaration contains these power channels in the full scanned source.",
        "formula_boundary": "No active additive or multiplicative reactor-power source applies, so no nontrivial modifier stacking formula is needed; signed component powers add directly. Source-derived conclusion assumes the published component contract, not unexposed engine internals."},
    "arithmetic": {"produced": produced, "consumed": consumed, "source_derived_balance": produced - consumed,
                   "unresolved_component_power_fields": [],
                   "conclusion": "The complete actual 56-component configuration has a strictly positive source-derived power balance; this is not an observed UI power number."},
    "maintenance_UI": {"image": ref(image), "ocr": ref(ocr_path),
        "hover_action": ref(ART / "r6pu-ship-maintenance-hover.action.json"),
        "evidence_type": "root visually confirmed Fresh Steam F12 GPU tooltip; same-date native-save binding",
        "pid": ocr["pid"], "resolution": ocr["resolution"], "date": "2201.01.01",
        "country": 0, "fleet": int(fleet_id), "ship": int(ship_id),
        "energy_per_month_displayed": "10.07", "alloys_per_month_displayed": "2.88",
        "naval_capacity_context": "115/66", "scope": "Only this actual Purifier date/state; not generalized to other governments or to base component upkeep."},
    "limitations": ["Actual designer hover/click after tutorial dismissal remained in detail and exposed no power number; this report is an explicit source-derived alternative, never UI power measurement.",
                    "No public ship excess-power or individual ship actual-upkeep export getter was found; maintenance is the independent visual tooltip observation, not calculated from this component-power sum.",
                    "No unexposed engine caches, executable control flow, DLC archive-only code or hypothetical future changes are asserted. The exact native source, copied Mod, save and EXE are bound by SHA.",
                    "No Mod, save, UI, game process, validator or acceptance Boolean was modified."],
    "sources": sources, "reproduction_script": ref(Path(__file__).resolve())}
out_path = OUT / "power-inventory-report-v1.json"
out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"report": str(out_path), "sha256": sha(out_path.read_bytes()),
                  "arithmetic": report["arithmetic"], "actual_identity": report["actual_identity"],
                  "modifier_declarations": len(occurrences), "sources": len(sources)}, indent=2))
