"""Generate only the two documented 4.5.2 native adapters, with pinned sources."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")


def definition(path: Path, key: str) -> tuple[str, str]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    start = text.index(key + " = {")
    opening = text.index("{", start)
    depth = 0
    quoted = False
    comment = False
    escaped = False
    for i in range(opening, len(text)):
        char = text[i]
        if char == "\n":
            comment = False
        if comment:
            continue
        if char == '"' and not escaped:
            quoted = not quoted
        if char == "#" and not quoted:
            comment = True
        if not quoted:
            depth += (char == "{") - (char == "}")
            if depth == 0:
                return text[start:i + 1], hashlib.sha256(raw).hexdigest()
        escaped = char == "\\" and not escaped
    raise ValueError("unbalanced native definition")


def main():
    effect_path = GAME / "common/scripted_effects/00_scripted_effects.txt"
    decision_path = GAME / "common/decisions/02_special_decisions.txt"
    native, effect_hash = definition(effect_path, "consume_world")
    assert native.count("PLANET = owner.capital_scope") == 1
    adapted = native.replace("consume_world = {", "eep_native_consume = {", 1).replace(
        "PLANET = owner.capital_scope", "PLANET = event_target:eep_core@event_target:eep_actor"
    )
    (ROOT / "mod/common/scripted_effects/eep_native_consume.txt").write_text(
        "# 4.5.2 consume_world: only AI destination changed to the bound core.\n" + adapted + "\n",
        encoding="utf-8", newline="\n",
    )
    decision, decision_hash = definition(decision_path, "decision_lithoid_swarm_consume_world")
    original_effect, _ = definition(decision_path, "decision_lithoid_swarm_consume_world")
    # Reuse the balanced scanner on a small temporary-free view of the full block.
    effect_start = decision.index("\teffect = {")
    ai_start = decision.index("\tai_weight = {", effect_start)
    original_effect = decision[effect_start:ai_start].strip()
    body = original_effect[original_effect.index("{") + 1:original_effect.rfind("}")]
    replacement = """\tallow = {
        if = {
            limit = { owner = { has_origin = origin_heart_of_devouring } }
            custom_tooltip = { fail_text = eep_source_required eep_source_valid = yes }
            custom_tooltip = { fail_text = eep_seed_required eep_seed_available = yes }
            custom_tooltip = { fail_text = eep_material_required planet_size > value:eep_damage_count }
        }
    }
    effect = {
        if = {
            limit = { owner = { has_origin = origin_heart_of_devouring } }
            custom_tooltip = eep_devour_effect
            hidden_effect = { eep_begin = yes }
        }
        else = {""" + body + "\n        }\n    }\n\n"
    decision = decision[:effect_start] + replacement + decision[ai_start:]
    assert decision.count("\t\tis_capital = no") == 1
    decision = decision.replace("\t\tis_capital = no", """        OR = {
            AND = { owner = { has_origin = origin_heart_of_devouring } NOT = { has_carrier_flag = eep_core } }
            AND = { owner = { NOT = { has_origin = origin_heart_of_devouring } } is_capital = no }
        }""", 1)
    (ROOT / "mod/common/decisions/zz_eep_native_decision.txt").write_text(
        "# Single-key adapter; non-EEP economic effects and AI weights are native.\n" + decision + "\n",
        encoding="utf-8", newline="\n",
    )
    evidence = {
        "game": "Cygnus v4.5.2 (9776)",
        "sources": {str(effect_path): effect_hash, str(decision_path): decision_hash},
        "consume_world_changes": ["name", "AI relocation destination"],
        "decision_changes": ["origin-specific allow", "origin-specific effect routing", "bound core exclusion"],
        "non_origin_effect_body_preserved": body in decision,
    }
    output = ROOT / "docs/evidence/native-adapter-build.json"
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, ensure_ascii=False))


if __name__ == "__main__":
    main()
