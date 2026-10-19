"""Load through the observed Chinese title menu; retain the original load receipt."""
import argparse
import json
from pathlib import Path
import re
import time

import runtime_1019 as runtime

b, h = runtime.base, runtime.base.h
EXIT = "\u9000\u51fa\u5230\u83dc\u5355"
CONFIRM = "\u653e\u5f03\u6e38\u620f\u5e76\u8fd4\u56de\u4e3b\u83dc\u5355"


def labels(frame):
    return {row["text"] for row in frame["rows"] if row["score"] >= .8}


def title_visible(frame):
    text = labels(frame)
    return ({"\u65b0\u6e38\u620f", "\u8f7d\u5165\u6e38\u620f", "\u591a\u4eba\u6e38\u620f"} <= text
            and not any(re.fullmatch(r"\d{4}\.\d{2}\.\d{2}", value) for value in text))


def return_to_title(stage):
    frame = h.capture(stage + "-start")
    for attempt in range(5):
        if title_visible(frame):
            return frame
        text = labels(frame)
        if EXIT in text and "\u4fdd\u5b58\u6e38\u620f" in text:
            h.click_text(EXIT, stage + "-exit-choice")
            confirmation = h.capture(stage + "-confirmation")
            if not title_visible(confirmation):
                if not any(CONFIRM in value for value in labels(confirmation)):
                    raise RuntimeError("expected native return-to-title confirmation is missing")
                h.click_text(EXIT, stage + "-exit-confirm")
            for index in range(4):
                frame = h.capture(stage + f"-title-{index}")
                if title_visible(frame):
                    return frame
                time.sleep(1)
            raise RuntimeError("native title menu not observed after confirmed exit")
        if attempt == 4:
            break
        h.press_scan_code(0x01, stage + f"-esc-{attempt}", 1)
        frame = h.capture(stage + f"-menu-{attempt}")
    raise RuntimeError("native game/title menu not visible; no load attempted")


def load(save_name, stage):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", stage):
        raise ValueError("unique ASCII stage of at most 40 characters required")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", save_name):
        raise ValueError("explicit ASCII native save name required")
    artifacts, _, _ = h.load_run()
    receipt = artifacts / (stage + ".title-workflow.json")
    if receipt.exists() or (artifacts / (stage + ".load.json")).exists():
        raise FileExistsError("refusing to overwrite an existing load workflow")
    frame = return_to_title(stage)
    result = b.r.native_load(save_name, stage)
    original = artifacts / (stage + ".load.json")
    record = {"schema": "eep.1020.native-title-load-workflow.v1",
              "status": "TITLE_AND_UI_DATE_VERIFIED_STATE_REQUIRES_NEW_NATIVE_SAVE",
              "source_name": save_name,
              "title_frame": {"path": frame["image"], "sha256": frame["image_sha256"]},
              "original_load_receipt": {"path": str(original), "sha256": h.sha256(original)},
              "native_load": result,
              "followup": "Verify identity/date/state with a newly saved native file."}
    h.write_json(receipt, record)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save_name")
    parser.add_argument("stage")
    args = parser.parse_args()
    print(json.dumps(load(args.save_name, args.stage), ensure_ascii=False))


if __name__ == "__main__":
    main()
