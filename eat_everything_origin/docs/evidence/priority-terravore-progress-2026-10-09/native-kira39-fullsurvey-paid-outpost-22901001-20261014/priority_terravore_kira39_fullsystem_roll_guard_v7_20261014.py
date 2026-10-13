"""Validate one bounded native Kira full-system survey interval."""
import json
import hashlib
import logging
import re
import sys
from decimal import Decimal as D
from pathlib import Path

before, after, stage, prior_proof_file, review_stage = sys.argv[1:]
sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import audit_save as q
import runtime as r
from priority_terravore_native_state import read_state
import priority_terravore_vanilla_survey_message_20261014 as survey

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
out = run / (stage + "-proof.json")
assert not out.exists()
frozen = run / Path(survey.__file__).name
raw = Path(survey.__file__).read_bytes()
if frozen.exists(): assert frozen.read_bytes() == raw
else: frozen.write_bytes(raw)
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
prior, review = load(prior_proof_file), load(review_stage + "-review.json")
calendar, execution = load(after + "-calendar-receipt.json"), load(after + "-execution.json")
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
old, new = (s["fleets"]["166"] for s in (b, a))
old_order, new_order = (q.block(f, "current_order") for f in (old, new))
target = lambda f: list(map(int, re.findall(r"\bid=(\d+)", q.block(f, "current_order"))))
queue = lambda f: list(map(int, re.findall(r"\bid=(\d+)", q.block(f, "order"))))
old_targets, new_targets = target(old) + queue(old), target(new) + queue(new)
consumed = len(old_targets) - len(new_targets)
original = [546, 545, 552, 553, 547, 543, 549, 554, 555, 550, 551, 548]
crossed = b["audit"]["date"][:7] != a["audit"]["date"][:7]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
budget = ac["budget_categories"]["current_month"]
net = {k: sum((D(str(v.get(k, 0))) for v in budget["income"].values()), D(0))
       - sum((D(str(v.get(k, 0))) for v in budget["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
stable_cash = ["energy", "minerals", "food", "influence", "unity", "trade", "alloys", "rare_crystals", "menace"]
reinforcement = a["fleets"]["50331731"]
checks = {
    "prior_review_calendar_actual0_exact_sav_chain":
        prior["status"].startswith("PASS") and all(prior["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and review["remaining_targets"] == old_targets
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["days"] == review["days"]
        and (calendar["start_date"], calendar["date"])
        == (b["audit"]["date"], a["audit"]["date"])
        and execution["returncode"] == 0
        and execution["helper_sha256"] == h.sha256(Path(execution["command"][1]))
        and prior["after_sha256"] == review["after_sha256"] == b["audit"]["save_sha256"]
        == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "survey_keeps_original_ordered_suffix_and_consumes_at_most_one":
        old_targets and old_targets == original[original.index(old_targets[0]):]
        and 0 <= consumed <= 1
        and new_targets == old_targets[consumed:]
        and (not new_targets or
             (len(target(new)) == 1
              and "survey_planet_order" in new_order
              and "can_reach=yes" in new_order))
        and (consumed > 0 or
             D(str(q.scalars(q.block(new_order, "survey_planet_order")).get("progress", 0)))
             >= D(str(q.scalars(q.block(old_order, "survey_planet_order")).get("progress", 0))))
        and q.scalars(q.block(q.block(new, "movement_manager"), "coordinate"))["origin"] == 39
        and q.ids(q.block(new, "ships")) == [1049]
        and q.block(q.block(b["roots"]["planets"], "planet"), "544")
        == q.block(q.block(a["roots"]["planets"], "planet"), "544"),
    "same_month_cash_or_one_exact_monthly_budget":
        ((not crossed
          and all(ac["effective_stockpile"].get(k) == bc["effective_stockpile"].get(k)
                  for k in stable_cash)
          and ac["budget_categories"]["current_month"]
              == bc["budget_categories"]["current_month"])
         or (crossed and a["audit"]["date"].endswith(".01")
             and all(abs(v) <= D("0.00002") for v in residual.values())
             and ac["budget_categories"]["last_month"]
             == bc["budget_categories"]["current_month"])),
    "paid_reinforcement_all_ship_memberships_stable":
        q.scalars(reinforcement)["mia_type"] == "mia_reinforce"
        and q.scalars(reinforcement)["return_date"] == "2290.12.02"
        and q.ids(q.block(reinforcement, "ships")) == [50332133]
        and q.scalars(q.block(q.block(reinforcement, "current_order"), "merge_fleet_order"))["target"] == 917
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships")) for k in b["fleets"]),
    "eep_reviewed_kira39_crystal_battle_error_stable":
        all(ac["variables"].get(k) == bc["variables"].get(k)
            for k in ("eep_c", "eep_d", "eep_stage", "eep_crisis"))
        and a["pending"] == b["pending"] == []
        and survey.is_one_surveyed(b["messages"])
        and len(a["messages"]) == 2 and a["messages"][0] == b["messages"][0]
        and hashlib.sha256(a["messages"][1].encode("utf-8")).hexdigest()
            == "91f16b30095bb3e7d34967680bd4c5e5a6149bfd46598a7571769a5b84a50852"
        and q.scalars(a["messages"][1]) == {
            "type": "COMBAT_STATS", "receiver": 0, "end": "2290.06.24",
            "date": "2290.05.09", "notification": 322,
            "message_type": "combat_stats"}
        and q.scalars(q.block(a["messages"][1], "coordinate"))["origin"] == 39
        and all(("fleet=" + fid) in q.block(a["messages"][1], "combat_stats")
                for fid in ("50332250", "83886903", "917", "33555324"))
        and bool(q.block(b["roots"]["fleet"], "33555324"))
        and not q.block(a["roots"]["fleet"], "33555324")
        and bool(q.block(b["roots"]["ships"], "16777760"))
        and not q.block(a["roots"]["ships"], "16777760")
        and 33555324 in q.ids(q.block(q.block(b["roots"]["galactic_object"], "39"), "fleet_presence"))
        and 33555324 not in q.ids(q.block(q.block(a["roots"]["galactic_object"], "39"), "fleet_presence"))
        and D(str(ac["effective_stockpile"]["menace"]))
            - D(str(bc["effective_stockpile"]["menace"])) == D(15)
        and {k for k in b["ships"] if any(q.scalars(b["ships"][k]).get(z)
            != q.scalars(a["ships"][k]).get(z)
            for z in ("hitpoints", "shield_hitpoints", "armor_hitpoints"))}
            == {"67110414", "100665013", "33556327"}
        and hashlib.sha256(Path("C:/SteamLibrary/steamapps/common/Stellaris/common/message_types/00_message_types.txt").read_bytes()).hexdigest()
            == "b9457c4434ef69ac407c0850a34b80a66ed93b70ec1140858045caba406a7904"
        and hashlib.sha256(Path("C:/SteamLibrary/steamapps/common/Stellaris/localisation/simp_chinese/messages_l_simp_chinese.yml").read_bytes()).hexdigest()
            == "7b3d8417034fe50d626cb90cc5f02d9500407338558d5c9304c718924199f8b5"
        and (run / (after + "-error-before.log")).read_bytes()
        == (run / (after + "-error-after.log")).read_bytes(),
}
original_fail = json.loads((run / "terravore-kira39-fullsystem-roll10-v6guard-22900601-proof.json").read_text("utf-8-sig"))
checks["v6_fail_preserved_only_battle_message_check_failed"] = (
    original_fail["status"] == "FAIL"
    and original_fail["after_sha256"] == a["audit"]["save_sha256"]
    and list(original_fail["checks"].values()) == [True, True, True, True, False]
)
proof = {
    "status": "PASS_NATIVE_KIRA39_FULLSYSTEM_SURVEY_ROLL" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "old_targets": old_targets,
    "new_targets": new_targets,
    "consumed_targets": old_targets[:consumed] if 0 <= consumed <= len(old_targets) else [],
    "current_progress": q.scalars(q.block(new_order, "survey_planet_order")).get("progress"),
    "crossed_month": crossed,
    "cash_residuals": {k: str(v) for k, v in residual.items()} if crossed else None,
    "scope": "One bounded native full-system survey window; at most one queued body consumed and one monthly settlement. Outpost still needs UI acceptance.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
