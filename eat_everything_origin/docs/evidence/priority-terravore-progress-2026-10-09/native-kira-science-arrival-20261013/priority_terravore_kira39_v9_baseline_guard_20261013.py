"""Prove revised calendar error baseline accepts only exact reviewed bytes."""
import json
import logging
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path[:0] = ["eat_everything_origin/tools", "_runtime/heart-of-devouring"]
sys.argv = ["runtime"]
import runtime as r
import priority_native_uplift_error_baseline_v2_20261013 as baseline

logging.disable(logging.INFO)
h = r.harness
run, user, meta = h.load_run()
stage = "terravore-kira39-v9-baseline-guard-22890501"
out = run / (stage + "-proof.json")
assert not out.exists()
current = (user / "logs/error.log").read_bytes()
ack_stage = "terravore-kira39-apoc3-ack-guard-22890501"
ack = json.loads((run / (ack_stage + "-proof.json")).read_text("utf-8-sig"))
receipt = json.loads((run / (ack_stage + "-execution.json")).read_text("utf-8-sig"))
v8 = Path("_runtime/heart-of-devouring/priority_terravore_labs_completion_calendar_v8_20261013.py").read_text("utf-8")
v9_file = Path("_runtime/heart-of-devouring/priority_terravore_labs_completion_calendar_v9_20261013.py")
v9 = v9_file.read_text("utf-8")
expected = v8.replace(
    "from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair",
    "import priority_native_uplift_error_baseline_v2_20261013 as reviewed_baseline\n"
    "reviewed_error_pair=reviewed_baseline.reviewed_error_pair")
expected = expected.replace(
    " else:shutil.copyfile(__file__,dest)\n",
    " else:shutil.copyfile(__file__,dest)\n"
    " source=Path(reviewed_baseline.__file__);frozen=run/source.name\n"
    " if frozen.exists():assert frozen.read_bytes()==source.read_bytes()\n"
    " else:shutil.copyfile(source,frozen)\n")
checks = {
    "reviewed_apoc3_ack_five_pass_actual0_original_source":
        ack["status"] == "PASS_NATIVE_APOC3_ACK_AFTER_REVIEWED_VANILLA_LOC_ERROR"
        and len(ack["checks"]) == 5 and all(ack["checks"].values())
        and receipt["returncode"] == 0
        and receipt["helper_sha256"] == h.sha256(Path(receipt["command"][1]))
        and ack["after_sha256"] == h.sha256(run / "terravore-kira39-apoc3-ack-native-22890501.sav"),
    "v9_only_uses_revised_exact_error_module_and_freezes_it":
        v9 == expected
        and baseline.reviewed_error_pair(current, current, run),
    "any_new_error_byte_or_unreviewed_start_rejected":
        not baseline.reviewed_error_pair(current, current + b"new_error", run)
        and not baseline.reviewed_error_pair(current + b"new_error", current + b"new_error", run)
        and not baseline.reviewed_error_pair(current, current[:-1], run),
    "current_bytes_exact_official_reviewed_baseline":
        h.sha256(user / "logs/error.log") == baseline.CURRENT
        and (run / "terravore-kira39-apoc3-ack-native-22890501-error-after.log").read_bytes()
            == current,
}
proof = {
    "status": "PASS_REVISED_EXACT_VANILLA_ERROR_BASELINE" if all(checks.values()) else "FAIL",
    "checks": checks,
    "after_sha256": ack["after_sha256"],
    "baseline_sha256": baseline.CURRENT,
    "calendar_v9_source_sha256": h.sha256(v9_file),
    "baseline_v2_source_sha256": h.sha256(Path(baseline.__file__)),
    "scope": "Read-only fixture self-test; no GUI or calendar. Any additional error still fails.",
}
h.write_json(out, proof)
print(json.dumps(proof, ensure_ascii=False), flush=True)
assert all(checks.values())
