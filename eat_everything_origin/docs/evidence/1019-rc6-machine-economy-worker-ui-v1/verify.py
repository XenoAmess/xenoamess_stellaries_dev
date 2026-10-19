"""Verify completed Machine worker bytes and recorded commands only."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def fp(path):
    raw = path.read_bytes(); return len(raw), sha256(raw).hexdigest()


def main():
    index = json.loads((OUT / "index.json").read_bytes())
    assert fp(OUT / "selection.json")[1] == index["selection_sha256"]
    for row in index["files"]:
        assert fp(OUT / row["path"]) == fp(Path(row["source"])) == (row["bytes"], row["sha256"])
        assert Path(row["path"]).suffix not in (".sav", ".log") and "r6mcinit2" not in row["path"] and "r6g" not in row["path"]
    for row in index["canonical_references_not_copied"]:
        assert fp(Path(row["path"])) == (row["bytes"], row["sha256"])
    commands = []
    for p in (OUT / "machine").glob("*-advance-command.action.json"):
        d=json.loads(p.read_bytes()); assert d["text"] == "fast_forward 30" and d["submitted"]; commands.append(p.name)
    assert len(commands) == 12 and all(value is None for value in index["four_checks_await_root_review"].values())
    images=[]
    for p in (OUT / "machine").glob("*.ocr.json"):
        d=json.loads(p.read_bytes()); assert fp(OUT / "machine" / Path(d["image"]).name)[1] == d["image_sha256"] and d["pid"] == 30812
        images.append({"stage":d["stage"],"image_sha256":d["image_sha256"]})
    result={"schema":"eep.rc6.machine-economy-worker-ui-verification.v1","status":"PASS_BYTES_AND_CONTROLLED_WORKER_COMMAND_BINDING_ONLY",
            "verified_at_utc":datetime.now(timezone.utc).isoformat(),"index_sha256":fp(OUT/'index.json')[1],"payload_files_rechecked":len(index['files']),
            "canonical_refs_rechecked":len(index['canonical_references_not_copied']),"image_ocr_bindings":images,"recorded_FF30_count":12,
            "four_checks_remain_null":True,"system_wide_input_audit":False,"init2_growth_logs_read":False,"UI_or_Git_operations":False}
    (OUT/'verify.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='image_ocr_bindings'},indent=2))


if __name__ == '__main__': main()
