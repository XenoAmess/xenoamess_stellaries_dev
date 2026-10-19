"""Review complete legacy-run logs, preserved fixture states and EEP05 evidence."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import re

OUT = Path(__file__).resolve().parent
DOCS = OUT.parent.parent
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]")


def metadata(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "sha256": sha256(data).hexdigest()}


def records(path):
    lines = path.read_bytes().decode("utf-8-sig").splitlines()
    result = []
    for number, line in enumerate(lines, 1):
        if STAMP.match(line) or not result:
            result.append({"line_start": number, "line_end": number, "lines": [line]})
        else:
            result[-1]["lines"].append(line)
            result[-1]["line_end"] = number
    return lines, result


def main():
    error, er = records(OUT / "logs/error.log")
    game, gr = records(OUT / "logs/game.log")
    debug, dr = records(OUT / "logs/debug.log")
    baseline = DOCS / "evidence/1019-baseline/logs-final/error.log"
    native_baseline = baseline.read_text(encoding="utf-8-sig").splitlines()
    assert len(error) == 23
    assert [STAMP.sub("", s) for s in error] == [STAMP.sub("", s) for s in native_baseline[:23]]
    debug_baseline = DOCS / "evidence/1019-baseline/logs-final/debug.log"
    assert [STAMP.sub("", s) for s in debug] == [STAMP.sub("", s) for s in debug_baseline.read_text(encoding="utf-8-sig").splitlines()]
    for row in er:
        text = row["lines"][0]
        category = ("baseline_missing_workshop_discovery" if "Could not find files for mod:" in text else
                    "baseline_native_consume_override" if "decision_lithoid_swarm_consume_world already exists" in text else
                    "baseline_native_picker_portrait_container_warning" if "portrait_container" in text else
                    "unknown_retained")
        row.update(category=category, reason="Preserved; exact baseline match after timestamp removal is not proof of harmlessness or loaded missing Workshop mods.")
    for row in gr:
        row.update(category="native_version_information" if "Game Version:" in row["lines"][0] else "native_defines_information" if "defines loaded" in row["lines"][0] else "unknown_retained")
    for row in dr:
        row.update(category="baseline_native_building_category_warning_unidentified_object",
                   reason="Same baseline message without building key; object identity and impact remain unresolved.")
    reports = []
    final = {}
    for path in sorted((OUT / "analysis").glob("*-report-v1.json")):
        d = json.loads(path.read_bytes())
        checks = d.get("checks", {})
        row = {**metadata(path), "status": d["status"], "scope": d["scope"],
               "check_count": len(checks), "true_checks": sum(x is True for x in checks.values())}
        if "strict_comparison" in d:
            row.update(strict_status=d["strict_comparison"]["status"], strict_difference_count=len(d["strict_comparison"]["differences"]))
        if "-partial-fixture-" in path.name:
            damage = d["snapshot"]["damage"]
            assert all(0 < x["current_absolute"] < x["maximum"] for x in damage.values())
            assert d["status"] == "PASS_SCOPED" and all(checks.values())
            row.update(damage=damage, original_fixture_version=d["original_fixture"]["version"],
                       original_fixture_sha256=d["original_fixture"]["save_sha256"], actual_damage_run_mod_version="0.3.1")
            final[path.name] = row
        reports.append(row)
    assert len(reports) == 5 and len(final) == 2
    ocr_failure_frames = []
    for name in ("ld031-hurt-reload-load-window.ocr.json", "ld031-hurt-reload-initial-page-0.ocr.json"):
        path = OUT / "run" / name
        d = json.loads(path.read_bytes())
        matched = [x for x in d["rows"] if "Id031hurt" in x["text"]]
        assert matched, name
        ocr_failure_frames.append({**metadata(path), "image": metadata(OUT / "run" / Path(d["image"]).name), "relevant_rows": matched})
    assert not (OUT / "run/ld031-hurt-reload.load.json").exists()
    tooltip_path = OUT / "run/eep05-error-tooltip.ocr.json"
    tooltip = json.loads(tooltip_path.read_bytes())
    exact = "\u7edf\u6cbb\u8005\u6027\u522b\u672a\u9009\u5b9a\u3002"
    rows = [x for x in tooltip["rows"] if x["text"] == exact]
    assert len(rows) == 1
    migration_templates = []
    for path in sorted((OUT / "analysis").glob("*-case-template-v2.json")):
        d = json.loads(path.read_bytes())
        assert all(d[x] is None for x in ("loaded_before_sync", "after", "reload"))
        migration_templates.append({**metadata(path), "status": d["status"], "loaded_before_sync": None, "after": None, "reload": None})
    report = {"schema": "eep.legacy-damage.final-run-review.v1", "status": "REVIEWED_FIXTURE_PROVENANCE_ONLY",
              "reviewed_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T130448Z",
              "index_sha256": sha256((OUT / "index.json").read_bytes()).hexdigest(),
              "logs": {"error.log": {**metadata(OUT / "logs/error.log"), "physical_lines": len(error), "records": er, "categories": dict(Counter(x["category"] for x in er))},
                       "game.log": {**metadata(OUT / "logs/game.log"), "physical_lines": len(game), "records": gr, "categories": dict(Counter(x["category"] for x in gr))},
                       "debug.log": {**metadata(OUT / "logs/debug.log"), "physical_lines": len(debug), "records": dr, "categories": dict(Counter(x["category"] for x in dr))}},
              "baseline_sources": [metadata(baseline), metadata(debug_baseline)],
              "nomads_error_seen_in_this_run": False, "nomads_causal_status_elsewhere": "UNRESOLVED_UNCHANGED",
              "fixture_reports_preserved": reports,
              "caller_lookup_failure": {"stage": "ld031-hurt-reload", "target_label": "ld031hurt", "ocr_read_initial_letter": "Id031hurt (capital I)",
                    "ocr_engine_failure": False, "native_load_success_claimed_for_failed_attempt": False,
                    "frames": ocr_failure_frames, "independent_failure_receipt_exists": False,
                    "limit": "Caller exception was reported in root worker61189 session; no invented on-disk failure JSON. Existing failed-attempt screenshots/OCR/actions are preserved.",
                    "recovery": "raw aliases src031hurt/srcpaidarmor with partial-source-aliases.json; not extra native saves; no ld031armor"},
              "eep05": {"specific_reason_observed": exact, "tooltip_ocr": metadata(tooltip_path),
                    "tooltip_image": metadata(OUT / "run/eep05-error-tooltip.jpg"), "row": rows[0],
                    "unmodified_editor_evidence": metadata(OUT / "run/eep05-editor-unmodified.ocr.json"),
                    "hover_basis": metadata(OUT / "run/eep05-completion-hover-basis.json"),
                    "old_runtime_input_sha256": metadata(OUT / "runtime-input/user_empire_designs_v3.4.txt")["sha256"],
                    "repaired_candidate_sha256": metadata(OUT / "eep05-fixture/fixture-after-gender-repair.txt")["sha256"],
                    "single_field_repair_proof": metadata(OUT / "eep05-fixture/fixture-gender-repair-v1.json"),
                    "native_repaired_selection_acceptance": "PENDING"},
              "future_migration_templates": migration_templates,
              "limitations": ["Final partial fixtures are qualified only; RC4 load/sync/reload and full Mod acceptance are not assigned.",
                   "Initial two three-layer setup FAIL reports and armor-only OBSERVATION remain intact; raw omitted shield is not silently turned into zero.",
                   "Public final strict26/paid strict20 differences remain FAIL in copied reports; no ignored paths.",
                   "Paid source is0.3.0-rc.1 while this actual damage run is public0.3.1; original provenance is not rewritten.",
                   "No new semantic error records does not prove harmlessness or repaired-fixture runtime success; native building identity remains unresolved.",
                   "All19 logs retained; semantic review here covers complete error/game/debug only; no UI, game, Steam, Mod/SAV mutation or commit performed."]}
    (OUT / "review.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "error_categories": report["logs"]["error.log"]["categories"],
                      "reports": [{"name": Path(x["path"]).name, "status": x["status"], "checks": x["check_count"], "true": x["true_checks"]} for x in reports],
                      "eep05_specific_reason_verified": True, "helper_lookup_failure_preserved": True}, indent=2))


if __name__ == "__main__":
    main()
