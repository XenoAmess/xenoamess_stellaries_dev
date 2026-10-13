"""Permit only the exact reviewed vanilla sky-dragon localization baseline."""
import hashlib
import json
from pathlib import Path

from priority_native_uplift_error_baseline_20261013 import reviewed_error_pair as prior_pair

CURRENT = "40c72b502b29278da2f2877994711b302b7265f0969dea9e6a656efa9be906c3"
OFFICIAL_L10N = "c1f029f76a933508a566c35ef9b605a33766bd862f95fea71090db38ee149f33"
OFFICIAL_EVENT = "0bd0b3a338e462a1a8f87c1f12abe62645efa2b3144a82ed38b6acbdc8931f1f"
sha = lambda data: hashlib.sha256(data).hexdigest()


def reviewed_error_pair(before, after, run):
    if prior_pair(before, after, run):
        return True
    if sha(before) != CURRENT or after != before:
        return False
    review_stage = "terravore-kira39-apoc3-vanilla-error-review-22890501"
    ack_stage = "terravore-kira39-apoc3-ack-guard-22890501"
    try:
        review = json.loads((run / (review_stage + "-proof.json")).read_text("utf-8-sig"))
        ack = json.loads((run / (ack_stage + "-proof.json")).read_text("utf-8-sig"))
        review_exec = json.loads((run / (review_stage + "-execution.json")).read_text("utf-8-sig"))
        ack_exec = json.loads((run / (ack_stage + "-execution.json")).read_text("utf-8-sig"))
        return (
            review["status"] == "PASS_REVIEWED_VANILLA_APOC3_SKY_DRAGON_LOC_BOUNDARY"
            and len(review["checks"]) == 5 and all(review["checks"].values())
            and ack["status"] == "PASS_NATIVE_APOC3_ACK_AFTER_REVIEWED_VANILLA_LOC_ERROR"
            and len(ack["checks"]) == 5 and all(ack["checks"].values())
            and review_exec["returncode"] == ack_exec["returncode"] == 0
            and review_exec["helper_sha256"] == sha(
                (run / "priority_terravore_kira39_apoc3_vanilla_error_review_20261013.py").read_bytes())
            and ack_exec["helper_sha256"] == sha(
                (run / "priority_terravore_kira39_apoc3_ack_guard_20261013.py").read_bytes())
            and sha((run / "terravore-kira39-scout-month04-native-22890501-error-after.log").read_bytes()) == CURRENT
            and sha((run / "terravore-kira39-apoc3-ack-native-22890501-error-after.log").read_bytes()) == CURRENT
            and sha(Path("C:/SteamLibrary/steamapps/common/Stellaris/localisation/simp_chinese/grand_archive_specimens_l_simp_chinese.yml").read_bytes()) == OFFICIAL_L10N
            and sha(Path("C:/SteamLibrary/steamapps/common/Stellaris/events/apocalypse_events.txt").read_bytes()) == OFFICIAL_EVENT
            and ack["after_sha256"] == sha((run / "terravore-kira39-apoc3-ack-native-22890501.sav").read_bytes())
        )
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return False
