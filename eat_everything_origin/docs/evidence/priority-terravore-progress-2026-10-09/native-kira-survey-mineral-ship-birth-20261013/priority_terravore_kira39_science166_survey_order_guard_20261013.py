"""Read-only proof of the paid-game native survey order and its side effects."""
import json
import logging
import re
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
before = "terravore-kira39-fleet917-reinforce-paid-native-22881115"
after = "terravore-kira39-science166-survey-ordered-native-v2-22881115"
menu = "terravore-kira39-science166-context-revealed-22881115"
click = "terravore-kira39-science166-survey-click-22881115"
stage = "terravore-kira39-science166-survey-order-guard-22881115"
assert not (run / (stage + "-proof.json")).exists()
load = lambda name: json.loads((run / name).read_text("utf-8-sig"))
b, a = (read_state(run, s) for s in (before, after))
obs = load(after + "-observation.json")
menu_obs = load(menu + "-observation.json")
menu_ocr = load(menu + "-menu.ocr.json")
click_act = load(click + ".action.json")
click_exec = load(click + "-execution.json")
save_exec = load(after + "-execution.json")
f0, f1 = b["fleets"]["166"], a["fleets"]["166"]
movement = q.block(f1, "movement_manager")
path = q.block(movement, "path")
path_origins = [int(x) for x in re.findall(r"\borigin=(\d+)", path)]
path_systems = []
for x in path_origins:
    if not path_systems or path_systems[-1] != x:
        path_systems.append(x)
current = q.block(q.block(f1, "current_order"), "survey_planet_order")
queued = [v for k, v, obj in q.fields(q.block(f1, "order"))
          if k == "survey_planet_order" and obj]
queued_ids = [q.scalars(q.block(v, "deposit_holder"))["id"] for v in queued]
pb, pa = (q.block(s["roots"]["planets"], "planet") for s in (b, a))
planets_b = {k: v for k, v, obj in q.fields(pb) if obj}
planets_a = {k: v for k, v, obj in q.fields(pa) if obj}
planet523_b, planet523_a = planets_b["523"], planets_a["523"]
unchanged_523 = lambda x: [(k, v, obj) for k, v, obj in q.fields(x)
                           if k != "planet_orbitals"]
other_maps = ["country", "ships", "queues", "items", "designs",
              "templates", "messages", "pending"]
checks = {
    "original_menu_one_click_native_save_actual0_source_hashes":
        meta["language"] == "l_simp_chinese"
        and menu_obs["status"] == "OBSERVED_NATIVE_SCIENCE166_KIRA_CONTEXT_MENU"
        and menu_obs["image_sha256"] == menu_ocr["image_sha256"]
        and any(x["text"] == "调查恒星系" for x in menu_ocr["rows"])
        and click_act["action"] == "left-click"
        and click_act["client_point"] == [500, 538]
        and click_exec["returncode"] == save_exec["returncode"] == 0
        and click_exec["helper_sha256"] == h.sha256(Path(click_exec["command"][1]))
        and save_exec["helper_sha256"] == h.sha256(Path(save_exec["command"][1]))
        and obs["status"] == "OBSERVED_NATIVE_SCIENCE166_SURVEY_CHOICE_AND_SAVE"
        and obs["menu_image_sha256"] == menu_obs["image_sha256"]
        and obs["save_sha256"] == a["audit"]["save_sha256"]
            == h.sha256(run / (after + ".sav"))
        and b["audit"]["save_sha256"] == h.sha256(run / (before + ".sav")),
    "same_paused_date_no_new_resources_ships_or_other_fleet_orders":
        b["audit"]["date"] == a["audit"]["date"] == "2288.11.15"
        and len(b["ships"]) == len(a["ships"]) == 74
        and len(b["fleets"]) == len(a["fleets"]) == 35
        and all(b[k] == a[k] for k in other_maps)
        and b["audit"]["countries"]["0"] == a["audit"]["countries"]["0"]
        and all(b["fleets"][k] == a["fleets"][k]
                for k in b["fleets"] if k != "166"),
    "science166_from37_to39_via_real_reachable_hyperlane_path":
        f0 != f1
        and path_systems == [37, 97, 80, 71, 164, 39]
        and q.scalars(q.block(movement, "target_coordinate"))["origin"] == 39
        and q.scalars(movement)["state"] == "move_idle"
        and q.ids(q.block(f1, "ships")) == [1049],
    "full_survey_queue_contains_volcanic_planet544_no_completion_yet":
        q.scalars(q.block(current, "deposit_holder"))["id"] == 550
        and q.scalars(current)["progress"] == 0
        and q.scalars(current)["can_reach"] == "yes"
        and queued_ids == [555, 554, 549, 548, 547, 553, 552, 545,
                           544, 546, 543, 551]
        and all(q.scalars(v)["can_reach"] == "yes" for v in queued)
        and q.scalars(planets_a["544"])["planet_class"] == "pc_volcanic"
        and q.scalars(planets_a["544"])["planet_size"] == 20
        and planets_b["544"] == planets_a["544"],
    "only_native_planet_orbit_release_at_old_location":
        set(planets_b) == set(planets_a)
        and [k for k in planets_a if planets_b[k] != planets_a[k]] == ["523"]
        and unchanged_523(planet523_b) == unchanged_523(planet523_a)
        and q.scalars(q.block(planet523_b, "planet_orbitals")).get("5") == 166
        and q.scalars(q.block(planet523_a, "planet_orbitals")) == {},
    "galaxy_war_leaders_and_error_unchanged":
        all(b["roots"][k] == a["roots"][k]
            for k in ["galactic_object", "war", "leaders"])
        and obs["error_unchanged"]
        and (run / (after + "-error-before.log")).read_bytes()
            == (run / (after + "-error-after.log")).read_bytes(),
}
proof = {
    "status": "PASS_NATIVE_KIRA39_SCIENCE166_SURVEY_ORDER" if all(checks.values())
              else "FAIL_NATIVE_KIRA39_SCIENCE166_SURVEY_ORDER",
    "checks": checks,
    "before_sha256": b["audit"]["save_sha256"],
    "after_sha256": a["audit"]["save_sha256"],
    "date": a["audit"]["date"],
    "path_systems": path_systems,
    "queued_survey_planet_ids": queued_ids,
    "scope": "Paused native order only; neither arrival nor survey completion nor devour.",
}
h.write_json(run / (stage + "-proof.json"), proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values()), "Survey order proof failed; keep original output"
