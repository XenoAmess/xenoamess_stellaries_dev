"""Offline only: compare fresh RapidOCR with the existing cached factory."""
import ast
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import statistics
import time

from PIL import Image
from rapidocr import RapidOCR

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tools/runtime_single_homeworld.py"
SHARED = ROOT / "tools/runtime.py"
ARCHIVE = ROOT / "docs/evidence/1019-rc4-relic-jump-native-control-v1/raw"
OUTPUT = Path(__file__).with_suffix(".json")
PARAMS = {"EngineConfig.onnxruntime.intra_op_num_threads": 1,
          "EngineConfig.onnxruntime.inter_op_num_threads": 1}
IMAGES = ("r4mother13-verified-details.jpg", "r4relic-refresh-six-days-console-ready.jpg",
          "r4relic6-save-dialog.jpg")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload(output):
    boxes = output.boxes.tolist() if output.boxes is not None else []
    texts = list(output.txts) if output.txts is not None else []
    scores = [float(value) for value in output.scores] if output.scores is not None else []
    rows = [{"text": str(label), "score": round(score, 5),
             "box": [[round(float(x), 2), round(float(y), 2)] for x, y in box]}
            for box, label, score in zip(boxes, texts, scores, strict=True)]
    return {"boxes": boxes, "txts": texts, "scores": scores, "rows": rows}


def main():
    if OUTPUT.exists():
        raise FileExistsError("refusing to overwrite benchmark evidence")
    tree = ast.parse(SOURCE.read_text(encoding="utf-8-sig"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "bounded_ocr")
    namespace = {"original_ocr": RapidOCR, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(SOURCE), "exec"), namespace)
    cached = namespace["bounded_ocr"]
    frames = []
    for index, name in enumerate(IMAGES):
        path = ARCHIVE / name
        image = Image.open(path)
        image.load()
        started = time.perf_counter()
        fresh = RapidOCR(params=PARAMS)
        constructed = time.perf_counter()
        reference = payload(fresh(image))
        finished = time.perf_counter()
        del fresh
        cache_start = time.perf_counter()
        reused = cached()
        cache_ready = time.perf_counter()
        observed = payload(reused(image))
        cache_finish = time.perf_counter()
        equal = {key: reference[key] == observed[key] for key in reference}
        record = {"image": path.relative_to(ROOT).as_posix(), "sha256": sha(path),
                  "resolution": list(image.size), "fresh_construct_seconds": constructed - started,
                  "fresh_inference_seconds": finished - constructed, "fresh_total_seconds": finished - started,
                  "cached_factory_seconds": cache_ready - cache_start,
                  "cached_inference_seconds": cache_finish - cache_ready,
                  "cached_total_seconds": cache_finish - cache_start,
                  "cached_factory_cold": index == 0, "exact_equality": equal,
                  "fresh_output": reference, "cached_output": observed}
        if index == 0:
            repeat_start = time.perf_counter()
            repeated = payload(cached()(image))
            record.update(hot_repeat_seconds=time.perf_counter() - repeat_start,
                          hot_repeat_output=repeated,
                          hot_repeat_exact_equality={key: observed[key] == repeated[key] for key in observed})
        frames.append(record)
        print(json.dumps({"frame": name, "exact_equality": equal,
                          "fresh_total_seconds": record["fresh_total_seconds"],
                          "cached_total_seconds": record["cached_total_seconds"]}), flush=True)
    equal = all(all(frame["exact_equality"].values()) and
                all(frame.get("hot_repeat_exact_equality", {"unused": True}).values()) for frame in frames)
    info = cached.cache_info()
    result = {"schema": "eep.ocr-session-reuse.offline.v1", "status": "PASS_SCOPED" if equal else "FAIL",
              "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Three archived Simplified Chinese images; fresh factory versus already-existing sequential process cache, no desktop operation or Mod acceptance claim.",
              "runtime_tool_modified": False, "current_runtime_tool_sha256": sha(SOURCE),
              "shared_runtime_sha256": sha(SHARED), "benchmark_sha256": sha(Path(__file__)),
              "versions": {key: version(key) for key in ("rapidocr", "onnxruntime", "numpy", "pillow")},
              "python": platform.python_version(), "bounded_parameters": PARAMS,
              "cache_info": {"hits": info.hits, "misses": info.misses, "maxsize": info.maxsize, "currsize": info.currsize},
              "fresh_construct_median_seconds": statistics.median(frame["fresh_construct_seconds"] for frame in frames),
              "warm_cached_total_median_seconds": statistics.median(frame["cached_total_seconds"] for frame in frames[1:]),
              "frames": frames,
              "limits": ["Sequential calls only; no concurrent-session safety claim.",
                         "Cold initialization remains once per CLI process; already-existing cache was not introduced by this task.",
                         "Output elapsed metadata is intentionally excluded; full unrounded boxes and scores and harness-rounded rows are compared exactly."]}
    with OUTPUT.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"status": result["status"], "output": str(OUTPUT), "sha256": sha(OUTPUT),
                      "cache_info": result["cache_info"]}), flush=True)
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
