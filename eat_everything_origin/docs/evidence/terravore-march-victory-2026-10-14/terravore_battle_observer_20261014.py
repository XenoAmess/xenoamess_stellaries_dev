"""Read-only bounded battle contract; report natural combat, guard Mod state."""
import json
import logging
import math
import sys
from pathlib import Path

start, stage, calendar_execution = sys.argv[1:]
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
a, b = read_state(run, start), read_state(run, stage)
pre = json.loads((run / (stage + "-preflight.json")).read_text("utf-8"))
receipt = json.loads((run / (stage + "-calendar-receipt.json")).read_text("utf-8"))
execution = json.loads((run / calendar_execution).read_text("utf-8"))
prior = json.loads((run / pre["prior_proof"]).read_text("utf-8"))
ac, bc = a["audit"]["countries"]["0"], b["audit"]["countries"]["0"]
fleet_ids = ("50332250", "917", "50332411", "69")

def fleet(state, fid):
    return q.block(state["roots"]["fleet"], fid)

def members(state, fid):
    return [str(sid) for sid in q.ids(q.block(fleet(state, fid), "ships"))]

ids_a = {fid: members(a, fid) for fid in fleet_ids}
ids_b = {fid: members(b, fid) for fid in fleet_ids}
wanted = {sid for ids in ids_a.values() for sid in ids} | {sid for ids in ids_b.values() for sid in ids}
raw_a = {k: v for k, v, nested in q.fields(a["roots"]["ships"]) if nested and k in wanted}
raw_b = {k: v for k, v, nested in q.fields(b["roots"]["ships"]) if nested and k in wanted}
values_a = {sid: q.scalars(raw) for sid, raw in raw_a.items()}
values_b = {sid: q.scalars(raw) for sid, raw in raw_b.items()}
destroyed = {fid: [sid for sid in ids_a[fid] if sid not in raw_b] for fid in fleet_ids}
detached = {fid: [sid for sid in ids_a[fid] if sid not in ids_b[fid] and sid in raw_b] for fid in fleet_ids}
new_members = {fid: [sid for sid in ids_b[fid] if sid not in ids_a[fid]] for fid in fleet_ids}
identity_fields = ("fleet", "design", "ship_design", "name", "ship_size", "original_owner",
                   "max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints")
hp_fields = ("hitpoints", "armor_hitpoints", "shield_hitpoints")
changes = {fid: {sid: {field: [values_a[sid].get(field), values_b[sid].get(field)]
                      for field in hp_fields if values_a[sid].get(field) != values_b[sid].get(field)}
                 for sid in ids_b[fid] if sid in values_a
                 and any(values_a[sid].get(field) != values_b[sid].get(field) for field in hp_fields)}
           for fid in fleet_ids}

def ship_valid(sid):
    x, y = values_a[sid], values_b[sid]
    if any(x.get(field) != y.get(field) for field in identity_fields):
        return False
    for field, max_field in zip(hp_fields, ("max_hitpoints", "max_armor_hitpoints", "max_shield_hitpoints")):
        value, cap = y.get(field), y.get(max_field)
        if value is not None and (not isinstance(value, (int, float)) or not math.isfinite(value)
                                  or value < 0 or cap is not None and value > cap + 0.00001):
            return False
    return True

def crisis(state):
    raw = q.block(state["country"], "crisis_progression")
    return {"path": q.scalars(raw).get("path"),
            "levels": [v for k, v, nested in q.fields(raw) if not nested and k == "level"],
            "objectives": {q.scalars(v).get("objective"): q.scalars(v).get("progress")
                           for k, v, nested in q.fields(raw) if nested and k == "objective"}}

crisis_a, crisis_b = crisis(a), crisis(b)
enemy = fleet(b, "50332411")
enemy_move = q.block(enemy, "movement_manager")
enemy_summary = {"present": bool(enemy), "ships": len(ids_b["50332411"]),
                 "position": q.scalars(q.block(enemy_move, "coordinate")),
                 "state": q.scalars(enemy_move).get("state"),
                 "power": q.scalars(enemy).get("military_power"),
                 "order": q.block(enemy, "current_order")}
cash = ("energy", "minerals", "alloys", "trade", "unity", "astral_threads")
pa = q.scalars(q.block(q.block(a["roots"]["planets"], "planet"), "544"))
pb = q.scalars(q.block(q.block(b["roots"]["planets"], "planet"), "544"))
checks = {
    "bound_native_calendar_and_package": meta["language"] == "l_simp_chinese"
    and meta["version"] == "0.2.0" and prior["pass"]
    and a["audit"]["save_sha256"] == prior["after_save_sha256"] == pre["start_sha256"]
    and h.sha256(run / (start + ".sav")) == a["audit"]["save_sha256"]
    and h.sha256(run / (stage + ".sav")) == b["audit"]["save_sha256"]
    and pre["status"] == "PASS_BOUND_SAME_MONTH_BATTLE_PREFLIGHT"
    and pre["start_date"] == a["audit"]["date"] and pre["end_date"] == b["audit"]["date"]
    and receipt["status"] == "CALENDAR_CONFIRMED" and receipt["days"] == pre["days"]
    and receipt["start_date"] == a["audit"]["date"] and receipt["date"] == b["audit"]["date"]
    and execution["returncode"] == 0
    and h.sha256(Path(execution["command"][1])) == execution["helper_sha256"]
    and h.tree_manifest(Path(meta["copied_mod"]))[1] == meta["copied_mod_tree_sha256"],
    "no_new_ship_and_valid_survivors": not any(new_members.values())
    and not any(detached.values()) and all(ship_valid(sid) for sid in raw_b if sid in values_a)
    and set(a["ships"]) - set(b["ships"]) == set(destroyed["50332250"] + destroyed["917"])
    and not (set(b["ships"]) - set(a["ships"])),
    "neutral_and_reserve_held": ids_a["69"] == ids_b["69"] == ["282"]
    and raw_a["282"] == raw_b["282"]
    and a["fleets"]["83886903"] == b["fleets"]["83886903"],
    "mod_colonies_and_same_month_cash_held": ac["variables"] == bc["variables"]
    and ac["owned_colonies"] == bc["owned_colonies"] == [0, 40]
    and pa.get("owner") == pb.get("owner") == pa.get("controller") == pb.get("controller") == 0
    and pa.get("colony") == pb.get("colony") == 40
    and pb.get("bombardment_damage") == 0
    and all(a["audit"]["colonies"][cid]["actual_pop_sum"]
            == b["audit"]["colonies"][cid]["actual_pop_sum"] for cid in ("0", "40"))
    and all(ac["effective_stockpile"][resource] == bc["effective_stockpile"][resource] for resource in cash),
    "native_crisis_levels_and_ship_menace": crisis_a["path"] == crisis_b["path"] == "nemesis_path"
    and crisis_a["levels"] == crisis_b["levels"]
    and bc["effective_stockpile"]["menace"] - ac["effective_stockpile"]["menace"]
    == 15 * len(destroyed["50332411"])
    and crisis_b["objectives"].get("crisobj_destroy_enemy_ships", 0)
    - crisis_a["objectives"].get("crisobj_destroy_enemy_ships", 0) == 15 * len(destroyed["50332411"]),
    "no_unknown_event_or_error": not b["pending"] and not b["messages"]
    and (run / (stage + "-error-before.log")).read_bytes()
    == (run / (stage + "-error-after.log")).read_bytes()
    == (user / "logs" / "error.log").read_bytes(),
}
war_changed = a["roots"]["war"] != b["roots"]["war"]
calendar_ready = all(checks.values()) and bool(enemy) and enemy_summary["position"].get("origin") == 30 and not war_changed
proof = {"stage": stage.replace("-native-", "-observed-"), "pass": all(checks.values()),
         "calendar_ready": calendar_ready,
         "status": "PASS_BOUNDED_BATTLE" if all(checks.values()) else "REVIEW_REQUIRED",
         "before_save_sha256": a["audit"]["save_sha256"],
         "after_save_sha256": b["audit"]["save_sha256"],
         "date": b["audit"]["date"], "days": pre["days"], "checks": checks,
         "members_before": ids_a, "members_after": ids_b, "destroyed": destroyed,
         "detached": detached, "new_members": new_members, "hp_changes": changes,
         "menace_before": ac["effective_stockpile"]["menace"],
         "menace_after": bc["effective_stockpile"]["menace"],
         "native_crisis_before": crisis_a, "native_crisis_after": crisis_b,
         "enemy": enemy_summary, "war_changed": war_changed,
         "messages": [q.scalars(m) for m in b["messages"]],
         "pending": [q.scalars(m) for m in b["pending"]]}
out = run / (proof["stage"] + "-proof.json")
assert not out.exists()
out.write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({k: proof[k] for k in ("status", "pass", "calendar_ready", "date", "days", "checks", "destroyed", "menace_before", "menace_after")}), flush=True)
sys.exit(0 if proof["pass"] else 1)
