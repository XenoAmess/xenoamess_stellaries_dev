"""Verify one normal L-Gate event acknowledgement after reviewed vanilla errors."""
import json
import logging
import sys
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
before = "terravore-kira39-scout-month04-native-22890501"
after = "terravore-kira39-apoc3-ack-native-22890501"
review_stage = "terravore-kira39-apoc3-vanilla-error-review-22890501"
stage = "terravore-kira39-apoc3-ack-guard-22890501"
out = run / (stage + "-proof.json")
assert not out.exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
review = load(review_stage + "-proof.json")
observation = load(after + "-observation.json")
receipt = load(after + "-execution.json")
old_events, new_events = (q.block(s["country"], "events") for s in (b, a))
old_chains = [v for k, v, obj in q.fields(old_events) if k == "event_chain" and obj]
new_chains = [v for k, v, obj in q.fields(new_events) if k == "event_chain" and obj]
old_variables, new_variables = (q.scalars(q.block(s["country"], "variables"))
                                for s in (b, a))
omit = lambda raw, keys: [(k, v, obj) for k, v, obj in q.fields(raw) if k not in keys]
other_roots = (set(b["roots"]) | set(a["roots"])) - {
    "country", "message", "player_event", "open_player_event_selection_history"}
checks = {
    "review_five_pass_one_chinese_click_same_day_original_sav_sha":
        review["status"] == "PASS_REVIEWED_VANILLA_APOC3_SKY_DRAGON_LOC_BOUNDARY"
        and all(review["checks"].values())
        and receipt["returncode"] == 0
        and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
        and observation["status"] == "OBSERVED_ONE_NATIVE_APOC3_OPTION_AND_SAME_DAY_SAVE"
        and observation["option"] == "有意思。"
        and observation["client_point"] == [510, 545]
        and review["after_sha256"] == observation["before_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and observation["after_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav"))
        and b["audit"]["date"] == a["audit"]["date"] == "2289.05.01",
    "one_apoc3_pending_and_lgate_message_consumed":
        len(b["pending"]) == len(b["messages"]) == 1
        and q.scalars(b["pending"][0])["event"] == "apoc.3"
        and q.scalars(b["messages"][0])["event"] == 307
        and a["pending"] == a["messages"] == [],
    "exact_one_official_lcluster_chain_and_counter_zero":
        len(new_chains) == len(old_chains) + 1
        and new_chains[:len(old_chains)] == old_chains
        and q.scalars(new_chains[-1])["event_chain"] == "l_cluster_chain"
        and new_variables.get("num_lcluster_clues") == 0
        and {k: v for k, v in new_variables.items() if k != "num_lcluster_clues"}
            == old_variables
        and omit(old_events, {"event_chain"}) == omit(new_events, {"event_chain"})
        and omit(b["country"], {"events", "variables"})
            == omit(a["country"], {"events", "variables"}),
    "all_other_native_objects_eep_cash_fleets_ships_unchanged":
        all(b["roots"].get(k) == a["roots"].get(k) for k in other_roots)
        and b["ships"] == a["ships"]
        and b["fleets"] == a["fleets"]
        and b["queues"] == a["queues"]
        and b["items"] == a["items"]
        and b["audit"]["countries"]["0"]["effective_stockpile"]
            == a["audit"]["countries"]["0"]["effective_stockpile"]
        and b["audit"]["countries"]["0"]["variables"]
            == a["audit"]["countries"]["0"]["variables"],
    "previous_reviewed_error_persisted_no_new_error":
        observation["error_unchanged"]
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes()
            == (run / (before + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_APOC3_ACK_AFTER_REVIEWED_VANILLA_LOC_ERROR" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "event_chain": "l_cluster_chain",
    "scope": "One official apoc.3 option only; old vanilla localization errors retained, no new error or EEP change.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
