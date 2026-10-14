"""Independent native/UI battle victory and survival contract."""
import json
import logging
import sys
from pathlib import Path

sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
a = read_state(run, "hope-route-mar15-native-22940315")
b = read_state(run, "hope-route-mar22-native-22940322")
observed = json.loads((run / "hope-route-mar22-observed-22940322-proof.json").read_text("utf-8"))
inspection = json.loads((run / "hope-route-mar22-battle-result-inspection-20261014.json").read_text("utf-8"))
ui = json.loads((run / "hope-route-mar22-clean-combat-report-ui-proof.json").read_text("utf-8"))
ui_execution = json.loads((run / "hope-route-mar22-clean-combat-report-20261014-execution.json").read_text("utf-8"))
diagnostic_execution = json.loads((run / "hope-route-mar22-battle-result-inspection-20261014-execution.json").read_text("utf-8"))
ids = {sid for members in observed["members_after"].values() for sid in members}
ships_a = {k: v for k, v, nested in q.fields(a["roots"]["ships"]) if nested and k in ids}
ships_b = {k: v for k, v, nested in q.fields(b["roots"]["ships"]) if nested and k in ids}
max_changes = {"33556357": (1560, 1620), "16778219": (280, 290), "16778216": (280, 290)}
survivors_ok = all(
    q.block(ships_a[sid], "ship_design_implementation")
    == q.block(ships_b[sid], "ship_design_implementation")
    and q.scalars(ships_a[sid]).get("max_armor_hitpoints")
    == q.scalars(ships_b[sid]).get("max_armor_hitpoints")
    and q.scalars(ships_a[sid]).get("max_shield_hitpoints")
    == q.scalars(ships_b[sid]).get("max_shield_hitpoints")
    and (q.scalars(ships_a[sid]).get("max_hitpoints"),
         q.scalars(ships_b[sid]).get("max_hitpoints"))
    == max_changes.get(sid, (q.scalars(ships_a[sid]).get("max_hitpoints"),
                             q.scalars(ships_a[sid]).get("max_hitpoints")))
    for sid in ids)
veterans_ok = all(q.scalars(ships_a[sid]).get("experience") == 980
                  and q.scalars(ships_b[sid]).get("experience") == 1005 for sid in max_changes)
defines = Path(meta["game_exe"]).parent / "common/defines/00_defines.txt"
modifiers = Path(meta["game_exe"]).parent / "common/static_modifiers/00_static_modifiers.txt"
enemy = q.block(b["roots"]["fleet"], "50332411")
movement = q.block(enemy, "movement_manager")
combat = q.block(b["messages"][0], "combat_stats") if len(b["messages"]) == 1 else ""
checks = {
    "source_binding": observed["checks"]["bound_native_calendar_and_package"]
    and diagnostic_execution["returncode"] == ui_execution["returncode"] == 0
    and h.sha256(Path(diagnostic_execution["command"][1])) == diagnostic_execution["helper_sha256"]
    and h.sha256(Path(ui_execution["command"][1])) == ui_execution["helper_sha256"]
    and observed["before_save_sha256"] == a["audit"]["save_sha256"]
    and observed["after_save_sha256"] == b["audit"]["save_sha256"],
    "own_survival_and_native_enemy_losses": inspection["own_removed"] == inspection["own_added"] == []
    and observed["members_before"]["50332250"] == observed["members_after"]["50332250"]
    and observed["members_before"]["917"] == observed["members_after"]["917"]
    and observed["destroyed"]["50332411"] == ["67109347", "50333348", "33556150", "67110711"]
    and len(observed["members_after"]["50332411"]) == 13
    and not any(observed["detached"].values()) and not any(observed["new_members"].values()),
    "survivor_design_and_veteran_changes": survivors_ok and veterans_ok
    and inspection["health_violations"] == []
    and "SHIP_EXP_VETERAN" in defines.read_text("utf-8-sig")
    and q.scalars(q.block(modifiers.read_text("utf-8-sig"), "ship_rank_veteran")).get("ship_hull_mult") == 0.05,
    "native_and_chinese_victory": len(b["messages"]) == 1 and not b["pending"]
    and q.scalars(b["messages"][0]).get("type") == "COMBAT_STATS"
    and q.scalars(b["messages"][0]).get("date") == "2294.03.20"
    and q.scalars(combat).get("reason") == "no_more_enemies"
    and ui["pass"] and "战斗胜利" in ui["labels"]
    and ui["image_sha256"] == h.sha256(run / "hope-route-mar22-clean-combat-report-after.jpg")
    and q.scalars(q.block(movement, "coordinate")).get("origin") == 4294967295
    and not q.block(enemy, "current_order"),
    "mod_colony_cash_native_crisis_held": observed["checks"]["mod_colonies_and_same_month_cash_held"]
    and observed["checks"]["native_crisis_levels_and_ship_menace"]
    and observed["menace_before"] == 3365 and observed["menace_after"] == 3425,
    "neutral_reserve_error_held": observed["checks"]["neutral_and_reserve_held"]
    and (run / "hope-route-mar22-native-22940322-error-before.log").read_bytes()
    == (run / "hope-route-mar22-native-22940322-error-after.log").read_bytes()
    == (user / "logs/error.log").read_bytes(),
}
proof = {"stage": "hope-route-mar22-victory-guard-22940322", "pass": all(checks.values()),
         "calendar_ready": False, "checks": checks,
         "before_save_sha256": a["audit"]["save_sha256"],
         "after_save_sha256": b["audit"]["save_sha256"],
         "battle_ended": "2294.03.20", "ui_image_sha256": ui["image_sha256"],
         "defines_sha256": h.sha256(defines), "modifiers_sha256": h.sha256(modifiers),
         "scope": "Native battle victory, enemy MIA, protected colony; not full route acceptance."}
out = run / (proof["stage"] + "-proof.json")
assert not out.exists()
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
sys.exit(0 if proof["pass"] else 1)
