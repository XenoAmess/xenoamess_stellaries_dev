"""Read-only native combat-result and survivor-field diagnosis."""
import difflib
import json
import logging
import math
import sys

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
run, user, meta = r.harness.load_run()
a = read_state(run, "hope-route-mar15-native-22940315")
b = read_state(run, "hope-route-mar22-native-22940322")
proof = json.loads((run / "hope-route-mar22-observed-22940322-proof.json").read_text("utf-8"))
ids = {sid for members in proof["members_after"].values() for sid in members}
ships_a = {k: q.scalars(v) for k, v, nested in q.fields(a["roots"]["ships"]) if nested and k in ids}
ships_b = {k: q.scalars(v) for k, v, nested in q.fields(b["roots"]["ships"]) if nested and k in ids}
identity = ("fleet", "design", "ship_design", "name", "ship_size", "original_owner",
            "max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints")
changes = {sid: {field: [ships_a[sid].get(field), ships_b[sid].get(field)] for field in identity
                if ships_a[sid].get(field) != ships_b[sid].get(field)} for sid in ids
           if any(ships_a[sid].get(field) != ships_b[sid].get(field) for field in identity)}
violations = []
for sid in ids:
    for field, maximum in (("hitpoints", "max_hitpoints"), ("armor_hitpoints", "max_armor_hitpoints"),
                           ("shield_hitpoints", "max_shield_hitpoints")):
        value, cap = ships_b[sid].get(field), ships_b[sid].get(maximum)
        if value is not None and (not math.isfinite(value) or value < 0 or cap is not None and value > cap + 0.00001):
            violations.append({"ship": sid, "field": field, "value": value, "cap": cap})
report = {
    "identity_changes": changes, "health_violations": violations,
    "own_removed": sorted(set(a["ships"]) - set(b["ships"])),
    "own_added": sorted(set(b["ships"]) - set(a["ships"])),
    "combat_message_raw": b["messages"],
    "war_diff": list(difflib.unified_diff(a["roots"]["war"].splitlines(),
                                         b["roots"]["war"].splitlines(), n=2)),
    "enemy_raw": q.block(b["roots"]["fleet"], "50332411"),
}
out = run / "hope-route-mar22-battle-result-inspection-20261014.json"
assert not out.exists()
out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: report[k] for k in ("identity_changes", "health_violations", "own_removed", "own_added", "combat_message_raw", "war_diff")}, ensure_ascii=False), flush=True)
