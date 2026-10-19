"""Independent byte/image/command verification; does not accept economy checks."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
MOD = OUT.parents[2]


def fp(path):
    body = path.read_bytes(); return len(body), sha256(body).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    selection = json.loads((OUT / "selection.json").read_bytes())
    assert selection["files"] == index["files"] and fp(OUT / "selection.json")[1] == index["selection_sha256"]
    images = []
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"])
        assert Path(row["path"]).suffix not in (".sav", ".log") and "r6mc" not in row["path"]
        assert Path(row["path"]).name not in selection["excluded_post_UI_filenames"]
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"])
    for branch, data in index["branches"].items():
        receipt = json.loads((MOD / data["receipt"]["path"]).read_bytes())
        assert fp(OUT / "source/runtime_economy_1019.py")[1] == receipt["collector_sha256"]
        assert len(receipt["commands"]) == 12 and all(command["command"] == "fast_forward 30" for command in receipt["commands"])
        assert all(value is None for value in data["four_checks_await_root_review"].values())
        for path in (OUT / branch).glob("*.ocr.json"):
            ocr = json.loads(path.read_bytes()); image = OUT / branch / Path(ocr["image"]).name
            assert fp(image)[1] == ocr["image_sha256"] and ocr["pid"] == 30812
            images.append({"branch": branch, "stage": ocr["stage"], "image_sha256": ocr["image_sha256"]})
    result = {"schema": "eep.rc6.economy-worker-ui-verification.v1", "status": "PASS_BYTES_AND_CONTROLLED_WORKER_COMMAND_BINDING_ONLY",
              "verified_at_utc": datetime.now(timezone.utc).isoformat(), "index_sha256": fp(OUT / "index.json")[1],
              "payload_files_rechecked": len(index["files"]), "canonical_refs_rechecked": len(index["canonical_references_not_copied"]),
              "image_ocr_bindings": images, "each_branch_exactly_12_recorded_FF30": True,
              "four_checks_remain_null_for_root_review": True, "system_wide_input_audit": False,
              "Machine_or_logs_read": False, "UI_or_Git_operations": False}
    (OUT / "verify.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "image_ocr_bindings"}, indent=2))


if __name__ == "__main__": main()
