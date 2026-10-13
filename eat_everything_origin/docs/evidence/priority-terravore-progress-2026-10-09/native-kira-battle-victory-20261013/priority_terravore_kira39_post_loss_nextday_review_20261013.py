"""Approve one real post-loss day while both original Kira enemies remain."""
import json
import logging
import sys
from pathlib import Path

before, end, stage, prior_file, prior_stage = sys.argv[1:]
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import audit_save as q
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
s = read_state(run, before)
audit = s["audit"]
country = audit["countries"]["0"]
proof = json.loads((run / prior_file).read_text("utf-8-sig"))
execution = json.loads((run / (prior_stage + "-execution.json")).read_text("utf-8-sig"))
own = ["83886903", "917", "50332250"]
enemy = ["33554515", "854"]
own_ids, enemy_ids = ({int(i) for i in group} for group in [own, enemy])

def ordinal(date):
    year, month, day = map(int, date.split("."))
    assert 1 <= month <= 12 and 1 <= day <= 30
    return year * 360 + (month - 1) * 30 + day - 1

def combat_ids(fleet):
    return set(q.ids(q.block(q.block(fleet, "combat"), "in_combat_with")))

def own_ok(fid):
    fleet = s["fleets"][fid]
    extra = combat_ids(fleet) - enemy_ids
    return (len(q.ids(q.block(fleet, "ships")))
                == {"83886903": 16, "917": 8, "50332250": 14}[fid]
            and enemy_ids <= combat_ids(fleet)
            and all(not q.block(s["roots"]["fleet"], str(i)) for i in extra)
            and q.scalars(q.block(q.block(fleet, "movement_manager"),
                                  "coordinate"))["origin"] == 39)

def enemy_ok(fid):
    fleet = q.block(s["roots"]["fleet"], fid)
    members = q.ids(q.block(fleet, "ships"))
    living = [sid for sid in members if
              q.scalars(q.block(s["roots"]["ships"], str(sid))).get("killed") != "yes"]
    return (bool(fleet) and 0 < len(living) <= 9
            and combat_ids(fleet) == own_ids
            and q.scalars(q.block(q.block(fleet, "movement_manager"),
                                  "coordinate"))["origin"] == 39)

head = q.scalars(s["items"]["117440553"])
objective_progress = [q.scalars(raw)["progress"]
                      for key, raw, obj in q.fields(q.block(s["country"],
                                                         "crisis_progression"))
                      if key == "objective" and obj]
source_ok = (execution["returncode"] == 0
             and execution["helper_sha256"] == h.sha256(Path(execution["command"][1])))
checks = {
    "prior_post_loss_PASS_actual0_source_original_SAV":
        proof["status"] in {
            "PASS_NATIVE_KIRA39_FIRST_PAID_CRISIS_DESTROYER_LOSS",
            "PASS_NATIVE_KIRA39_POST_LOSS_ACTIVE_BATTLE_DAY",
        }
        and proof["checks"] and all(v is True for v in proof["checks"].values())
        and source_ok
        and proof["after_sha256"] == audit["save_sha256"]
            == h.sha256(run / (before + ".sav")),
    "exactly_one_next_day_no_later_than_Nov15":
        "2288.11.08" <= audit["date"] < end <= "2288.11.15"
        and ordinal(end) - ordinal(audit["date"]) == 1
        and proof["boundaries"] == ["active_kira39_post_loss_single_day_review"]
        and head["progress"] + 1.4 < 480,
    "three_original_paid_fleets_all38_ships_and_in_combat":
        len(s["fleets"]) == 35 and len(s["ships"]) == 74
        and all(own_ok(fid) for fid in own),
    "both_original_hostile_fleets_alive_in_reciprocal_battle":
        all(enemy_ok(fid) for fid in enemy),
    "no_pending_message_and_cash_remains_sufficient":
        not s["pending"] and not s["messages"]
        and country["effective_stockpile"]["energy"] > 20000
        and country["effective_stockpile"]["minerals"] > 1000
        and country["effective_stockpile"]["alloys"] > 3000,
    "EEP_queen_crisis3_no_unreviewed_menace":
        all(country["variables"].get(k) == value for k, value in {
            "eep_c": 76, "eep_d": 21, "eep_crisis": 3,
            "eep_stage": 2, "eep_worlds": 5}.items())
        and country["effective_stockpile"]["menace"]
            == sum(objective_progress) >= 3200,
    "CN41_production_mod_and_live_error_same":
        meta["version"] == "0.2.0" and meta["language"] == "l_simp_chinese"
        and len(h.tree_manifest(h.MOD_ROOT)[0]) == 41
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7"
        and (user / "logs/error.log").read_bytes()
            == (run / (before + "-error-after.log")).read_bytes(),
}
passed = all(value is True for value in checks.values())
out = run / (stage + ".json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_REVIEWED_NATIVE_BOUNDARY" if passed else "FAIL",
    "checks": checks, "before_sha256": audit["save_sha256"],
    "after_sha256": audit["save_sha256"], "start_date": audit["date"],
    "end_date": end, "days": 1, "maximum_days": 1,
    "allowed_boundaries": proof["boundaries"], "execution_stage": stage,
    "scope": "One continuing post-loss two-enemy-fleet battle day only. No next outcome presumed.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [k for k, value in checks.items() if value is not True],
                  "start": audit["date"], "end": end}), flush=True)
assert passed
