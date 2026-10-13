"""Audit one actual mineral-only crisis destroyer reinforcement order."""
import json
import logging
import sys
from decimal import Decimal as D
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
before = "terravore-kira39-battle-day14-native-22881115"
after = "terravore-kira39-fleet917-reinforce-paid-native-22881115"
quote_stage = "terravore-kira39-postvictory-fleet917-reinforce-quote-v5-22881115"
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, stage) for stage in (before, after))
victory = load(before + "-kira39-final-battle-victory-proof.json")
quote = load(quote_stage + "-observation.json")
action = load(after + "-order-observation.json")
receipts = [load(stage + "-execution.json") for stage in [
    before + "-final-victory-guard", quote_stage + "-action", after + "-action"]]
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
new_id = "704643085"
item = a["items"][new_id]
item_data = q.scalars(item)
reinforcement = q.block(item, "buildable_ship_reinforcement")
template_before = q.block(b["roots"]["fleet_template"], "268435546")
template_after = q.block(a["roots"]["fleet_template"], "268435546")
other_templates_before = {key: raw for key, raw, obj in
                          q.fields(b["roots"]["fleet_template"])
                          if obj and key != "268435546"}
other_templates_after = {key: raw for key, raw, obj in
                         q.fields(a["roots"]["fleet_template"])
                         if obj and key != "268435546"}
checks = {
    "victory8_and_single_quote_click_actual0_sources_original_SAV":
        victory["status"] == "PASS_NATIVE_KIRA39_FINAL_BATTLE_VICTORY"
        and len(victory["checks"]) == 8
        and all(v is True for v in victory["checks"].values())
        and quote["status"] == "OBSERVED_NATIVE_FLEET917_REINFORCE_QUOTE"
        and quote["image_sha256"] == action["quote_ui_image_sha256"]
        and action["status"] == "OBSERVED_NATIVE_ONE_FLEET917_REINFORCEMENT_CLICK"
        and action["quote_ui_text"] == "补充舰队 412.50"
        and action["click_point"] == [583, 251]
        and [receipt["returncode"] for receipt in receipts] == [0, 0, 0]
        and all(receipt["helper_sha256"]
                == h.sha256(Path(receipt["command"][1])) for receipt in receipts)
        and victory["after_sha256"] == action["before_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and action["after_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav")),
    "same_paused_date_no_new_ship_fleet_or_paid_other_order":
        b["audit"]["date"] == a["audit"]["date"] == "2288.11.15"
        and len(b["ships"]) == len(a["ships"]) == 74
        and b["ships"] == a["ships"]
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and b["fleets"] == a["fleets"]
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8,
    "exactly_412point5_minerals_paid_and_zero_alloys":
        D(str(bc["effective_stockpile"]["minerals"]))
            - D(str(ac["effective_stockpile"]["minerals"])) == D("412.5")
        and D(str(bc["effective_stockpile"]["alloys"]))
            == D(str(ac["effective_stockpile"]["alloys"]))
        and {key: value for key, value in bc["effective_stockpile"].items()
             if key != "minerals"}
            == {key: value for key, value in ac["effective_stockpile"].items()
                if key != "minerals"}
        and q.scalars(q.block(item, "resources")) == {"minerals": 412.5},
    "one_new_paid_queue_item_at_mother_shipyard_work60":
        set(a["items"]) - set(b["items"]) == {new_id}
        and not (set(b["items"]) - set(a["items"]))
        and all(b["items"][key] == a["items"][key] for key in b["items"])
        and item_data["queue"] == 3
        and item_data["paying_country"] == 0
        and item_data["progress"] == 0
        and item_data["progress_needed"] == 60
        and q.ids(q.block(b["queues"]["3"], "items")) == []
        and q.ids(q.block(a["queues"]["3"], "items")) == [int(new_id)]
        and q.block(b["queues"]["3"], "location")
            == q.block(a["queues"]["3"], "location")
        and q.scalars(q.block(a["queues"]["3"], "location"))
            == {"type": 0, "id": 0}
        and {key: value for key, value in b["queues"].items() if key != "3"}
            == {key: value for key, value in a["queues"].items() if key != "3"},
    "new_item_exact_design_template_and_starbase0":
        q.scalars(reinforcement)["fleet_template"] == 268435546
        and q.scalars(q.block(reinforcement, "ship_design_implementation"))["design"]
            == 83887141
        and q.scalars(q.block(reinforcement, "orbitable"))["starbase"] == 0
        and 'ship_size="crisis_destroyer"' in b["designs"]["83887141"],
    "template_target9_still_eight_real_and_only_one_queued":
        "count=9" in template_before and "count=9" in template_after
        and "704643085" not in template_before
        and q.ids(q.block(q.block(template_after, "all_queued"),
                          "construction_queue_items")) == [int(new_id)]
        and template_after.count(new_id) == 2
        and other_templates_before == other_templates_after,
    "only_expected_native_roots_and_EEP_pop_research_held":
        {key for key in b["roots"] if b["roots"][key] != a["roots"].get(key)}
            == {"country", "construction", "fleet_template"}
        and bc["variables"] == ac["variables"]
        and bc["research_stockpile"] == ac["research_stockpile"]
        and b["audit"]["colonies"] == a["audit"]["colonies"]
        and b["messages"] == a["messages"]
        and b["pending"] == a["pending"] == [],
    "same_error_and_CN41_live_production":
        (run / (before + "-error-after.log")).read_bytes()
            == (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (user / "logs/error.log").read_bytes()
        and meta["language"] == "l_simp_chinese"
        and h.tree_manifest(h.MOD_ROOT)[1]
            == "ac802ed0b6226731b039458a472f46ed5c6f7f7de3e629751509cbb322f9eae7",
}
passed = all(v is True for v in checks.values())
out = run / (after + "-fleet917-mineral-payment-proof.json")
assert not out.exists()
h.write_json(out, {
    "status": "PASS_NATIVE_KIRA39_FLEET917_MINERAL_PAYMENT" if passed else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "minerals_paid": 412.5, "alloys_paid": 0,
    "queued_item_id": new_id, "work_needed": 60,
    "scope": "One paid mineral crisis destroyer ordered; no build completion or monthly upkeep yet.",
})
print(json.dumps({"status": "PASS" if passed else "FAIL", "checks": len(checks),
                  "failed": [key for key, value in checks.items() if value is not True]},
                 ensure_ascii=False), flush=True)
assert passed
