"""Review exact vanilla sky-dragon text errors and one native L-Gate popup."""
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
before = "terravore-kira39-scout-month03-native-22890401"
after = "terravore-kira39-scout-month04-native-22890501"
prior = "terravore-kira39-scout-month03-guard-22890401"
ui_stage = "terravore-kira39-apoc3-postsave-capture-22890501"
stage = "terravore-kira39-apoc3-vanilla-error-review-22890501"
out = run / (stage + "-proof.json")
assert not out.exists()
load = lambda n: json.loads((run / n).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
prior_proof = load(prior + "-proof.json")
review = load("terravore-kira39-scout-month04-review-22890401-review.json")
calendar = load(after + "-calendar-receipt.json")
failed_execution = load(after + "-execution.json")
capture = load(ui_stage + "-observation.json")
capture_execution = load(ui_stage + "-execution.json")
ui_ocr = load(ui_stage + "-native-ui.ocr.json")
error_before = (run / (after + "-error-before.log")).read_bytes()
error_after = (run / (after + "-error-after.log")).read_bytes()
suffix = error_after[len(error_before):].decode("utf-8-sig") if error_after.startswith(error_before) else ""
new_lines = suffix.splitlines()
official_l10n = Path("C:/SteamLibrary/steamapps/common/Stellaris/localisation/simp_chinese/grand_archive_specimens_l_simp_chinese.yml")
official_event = Path("C:/SteamLibrary/steamapps/common/Stellaris/events/apocalypse_events.txt")
l10n = official_l10n.read_text("utf-8-sig")
event_source = official_event.read_text("utf-8-sig")
dlc = json.loads((user / "dlc_load.json").read_text("utf-8-sig"))
text_sources = [p for root in [Path("eat_everything_origin/mod"), Path("eat_everything_origin/localization")]
                for p in root.rglob("*") if p.is_file() and p.suffix in {".txt", ".yml", ".mod"}]
own_keys = [p.as_posix() for p in text_sources
            if any(key in p.read_text("utf-8-sig") for key in
                   ["sky_dragon_desc_short", "sky_dragon_desc_details", "apoc.3"])]
bc, ac = (s["audit"]["countries"]["0"] for s in (b, a))
cur = ac["budget_categories"]["current_month"]
cash = ["energy", "minerals", "alloys", "unity", "rare_crystals"]
actual = {k: D(str(ac["effective_stockpile"].get(k, 0)))
          - D(str(bc["effective_stockpile"].get(k, 0))) for k in cash}
net = {k: sum((D(str(v.get(k, 0))) for v in cur["income"].values()), D(0))
       - sum((D(str(v.get(k, 0))) for v in cur["expenses"].values()), D(0))
       for k in cash}
residual = {k: actual[k] - net[k] for k in cash}
pending = q.scalars(a["pending"][0]) if len(a["pending"]) == 1 else {}
message = q.scalars(a["messages"][0]) if len(a["messages"]) == 1 else {}
science = a["fleets"]["166"]
move = q.block(science, "movement_manager")
checks = {
    "prior_pass_review_one_calendar_confirmed_but_original_execution_failed_after_save":
        prior_proof["status"] == "PASS_NATIVE_KIRA39_SCOUT_TRAVEL_MONTH"
        and all(prior_proof["checks"].values())
        and review["status"] == "PASS_REVIEWED_NATIVE_BOUNDARY"
        and all(review["checks"].values())
        and failed_execution["returncode"] == 1
        and failed_execution["helper_sha256"] == h.sha256(Path(failed_execution["command"][1]))
        and calendar["status"] == "CALENDAR_CONFIRMED"
        and calendar["start_date"] == "2289.04.01"
        and calendar["date"] == "2289.05.01"
        and calendar["days"] == 30
        and prior_proof["after_sha256"] == review["after_sha256"]
            == b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav"))
        and a["audit"]["save_sha256"] == h.sha256(run / (after + ".sav")),
    "exact_three_new_vanilla_sky_dragon_text_error_lines_only":
        error_after.startswith(error_before)
        and len(new_lines) == 3
        and all("[game_text.cpp:1287]: Unknown property" in line for line in new_lines)
        and "GetHomeWorldName" in new_lines[0]
        and "天龙" in new_lines[0]
        and all("GetAdjective" in line and "幼崽" in line for line in new_lines[1:])
        and (user / "logs/error.log").read_bytes() == error_after
        and capture["error_before_sha256"] == capture["error_after_sha256"]
            == h.sha256(run / (after + "-error-after.log")),
    "exact_official_localization_event_sources_single_active_mod_no_override":
        h.sha256(official_l10n) == "c1f029f76a933508a566c35ef9b605a33766bd862f95fea71090db38ee149f33"
        and h.sha256(official_event) == "0bd0b3a338e462a1a8f87c1f12abe62645efa2b3144a82ed38b6acbdc8931f1f"
        and "sky_dragon_desc_short:" in l10n
        and "[EVENT_TARGET_0.GetHomeWorldName]" in l10n
        and l10n.count("[EVENT_TARGET_0.GetAdjective]") >= 2
        and "id = apoc.3" in event_source
        and "start_lcluster_chain = yes" in event_source
        and own_keys == []
        and dlc["enabled_mods"] == ["mod/ugc_eep-local.mod"],
    "single_native_apoc3_popup_and_one_chinese_option_recorded":
        pending.get("event") == "apoc.3"
        and pending.get("id") == 307
        and message.get("event") == 307
        and "遗弃星门" in message.get("text", "")
        and capture_execution["returncode"] == 0
        and capture["status"] == "OBSERVED_NATIVE_APOC3_POSTSAVE_UI"
        and capture["image_sha256"] == ui_ocr["image_sha256"]
        and all(any(x["text"] == label for x in ui_ocr["rows"])
                for label in ["2289.05.01", "暂停", "遗弃星门", "有意思。"]),
    "cash_monthly_net_scout_mia_original_ships_eep_stable":
        all(abs(v) <= D("0.00002") for v in residual.values())
        and q.scalars(q.block(move, "coordinate"))["origin"] == 164
        and q.scalars(q.block(move, "target_coordinate"))["origin"] == 39
        and "can_reach=yes" in q.block(science, "current_order")
        and set(a["ships"]) == set(b["ships"])
        and set(a["fleets"]) == set(b["fleets"])
        and len(a["ships"]) == 75
        and all(q.ids(q.block(b["fleets"][k], "ships"))
                == q.ids(q.block(a["fleets"][k], "ships"))
                for k in b["fleets"])
        and q.scalars(a["fleets"]["50331731"])["mia_type"] == "mia_reinforce"
        and len(q.ids(q.block(a["fleets"]["917"], "ships"))) == 8
        and all(ac["variables"].get(k) == bc["variables"].get(k)
                for k in ["eep_c", "eep_d", "eep_stage", "eep_crisis"]),
}
proof = {
    "status": "PASS_REVIEWED_VANILLA_APOC3_SKY_DRAGON_LOC_BOUNDARY" if all(checks.values()) else "FAIL",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "new_error_lines": new_lines,
    "cash_residuals": {k: str(v) for k, v in residual.items()},
    "option_text": "有意思。",
    "scope": "Exact official localization fault and one unrelated native L-Gate popup; only reviewed ACK is allowed next.",
}
h.write_json(out, proof)
print(json.dumps({k: v for k, v in proof.items() if k != "new_error_lines"},
                 ensure_ascii=False), flush=True)
assert all(checks.values())
