"""Isolated Chinese production runs for the 0.3.2 single-homeworld regression."""
import json
from functools import lru_cache
import io
from pathlib import Path
import re
import shutil
import sys
import time
import zipfile

import runtime_1015 as previous

r, h = previous.r, previous.h
ROOT = r.ROOT
ARTIFACTS = Path.home() / "AppData/Local/xenoamess_stellaries_dev/artifacts/single-homeworld-20261019"
h.RUNTIME_ROOT = ARTIFACTS / "runs"
h.CURRENT_RUN = ARTIFACTS / "current-run.json"
h.WORKSHOP_ID = "eep-single-homeworld"
h.PROFILE_ID = "eep-0.3.2-single-homeworld"
original_focus = h.focus_pid


def focus_current_window(pid):
    foreground = h.win32gui.GetForegroundWindow()
    if foreground in h.windows_for_pid(pid):
        return foreground
    return original_focus(pid)


h.focus_pid = focus_current_window
# Bound inference threads avoid CPU oversubscription beside the live game.
# Keep the same models, score threshold, and full-frame GPU input.
original_ocr = h.RapidOCR


@lru_cache(maxsize=1)
def bounded_ocr():
    return original_ocr(params={"EngineConfig.onnxruntime.intra_op_num_threads": 1,
                                "EngineConfig.onnxruntime.inter_op_num_threads": 1})


h.RapidOCR = bounded_ocr


def snapshot_baseline():
    destination = ARTIFACTS / "baseline"
    if destination.exists():
        raise RuntimeError("baseline snapshot already exists")
    report = ARTIFACTS / "baseline-open-kaishek.json"
    if json.loads(report.read_text(encoding="utf-8"))["status"] != "PASS":
        raise RuntimeError("baseline package gate missing")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if version != "0.3.1":
        raise RuntimeError("baseline must be the unchanged 0.3.1 package")
    shutil.copytree(ROOT / "mod", destination / "mod")
    shutil.copyfile(ROOT / "VERSION", destination / "VERSION")
    before = h.tree_manifest(ROOT / "mod")
    if before != h.tree_manifest(destination / "mod"):
        raise RuntimeError("baseline snapshot bytes differ")
    h.write_json(ARTIFACTS / "baseline-gate.json", {
        "status": "PASS", "version": version, "mod": str(destination / "mod"),
        "source_tree_sha256": before[1], "report": str(report),
        "report_sha256": h.sha256(report), "files": before[0],
    })
    return {"status": "SNAPSHOTTED", "version": version, "tree": before[1]}


def gate_candidate():
    report = ARTIFACTS / "candidate-open-kaishek.json"
    data = json.loads(report.read_text(encoding="utf-8"))
    if data["status"] != "PASS" or data["game_exe_sha256"] != h.EXPECTED_EXE_SHA256:
        raise RuntimeError("candidate package gate missing or wrong game")
    files, tree = h.tree_manifest(ROOT / "mod")
    result = {"status": "PASS", "version": (ROOT / "VERSION").read_text().strip(),
              "mod": str(ROOT / "mod"), "source_tree_sha256": tree, "files": files,
              "report": str(report), "report_sha256": h.sha256(report)}
    h.write_json(ARTIFACTS / "candidate-gate.json", result)
    return {"status": "GATED", "tree": tree}


def prepare(role, seed=None):
    gate = json.loads((ARTIFACTS / f"{role}-gate.json").read_text(encoding="utf-8"))
    report = Path(gate["report"])
    if (gate["status"] != "PASS" or h.sha256(report) != gate["report_sha256"]
            or json.loads(report.read_text(encoding="utf-8"))["status"] != "PASS"):
        raise RuntimeError("static gate changed")
    h.MOD_ROOT = Path(gate["mod"])
    if h.tree_manifest(h.MOD_ROOT)[1] != gate["source_tree_sha256"]:
        raise RuntimeError("source package changed after check")
    h.EXPECTED_MOD_TREE_SHA256 = gate["source_tree_sha256"]
    data = h.prepare("l_simp_chinese", [], Path(seed) if seed else None)
    user = Path(data["userdir"])
    settings = Path.home() / "AppData/Local/xenoamess_stellaries_dev/runs/20261014T163036Z/settings.txt"
    # The Chinese native settings UI verified autosave=2 means 每月.
    text = re.sub(r"(?m)^autosave=4$", "autosave=2", settings.read_text(encoding="utf-8"))
    if not re.search(r"(?m)^autosave=2$", text):
        raise RuntimeError("monthly native autosave configuration missing")
    (user / "settings.txt").write_text(text, encoding="utf-8")
    designs = ROOT / "testing/single-homeworld-user-empires.txt"
    (user / "user_empire_designs_v3.4.txt").write_bytes(designs.read_bytes())
    data.update(role=role, static_gate=gate, test_empire_designs_sha256=h.sha256(designs),
                window_settings_sha256=h.sha256(user / "settings.txt"),
                scope="0.3.2 startup and monthly economy only; stopped Terravore campaign untouched")
    h.write_json(Path(data["artifact_dir"]) / "manifest.json", data)
    return {"run_id": data["run_id"], "role": role, "artifact_dir": data["artifact_dir"], "userdir": data["userdir"]}


def observe(save):
    sys.path.insert(0, str(ROOT / "testing"))
    import inspect_1015
    artifacts, _, _ = h.load_run()
    path = artifacts / f"{save}.sav"
    result = inspect_1015.observe(path, artifacts / "manifest.json")
    output = artifacts / f"{save}.observation.json"
    h.write_json(output, result)
    country = result["country"]
    energy = {period: {direction: sum(resources.get("energy", 0) for resources in rows.values())
                       for direction, rows in categories.items()}
              for period, categories in country["budget_categories"].items()}
    return {"status": "OBSERVATION_ONLY", "date": result["date"], "worlds": len(result["worlds"]),
            "energy": energy, "stock": country["stockpile"].get("energy"),
            "output": str(output)}


def monthly_summary(audit):
    country = audit["countries"]["0"]
    energy = {period: {direction: sum(resources.get("energy", 0) for resources in rows.values())
                       for direction, rows in categories.items()}
              for period, categories in country["budget_categories"].items()}
    return {"status": "OBSERVATION_ONLY", "date": audit["date"],
            "save_sha256": audit["save_sha256"], "energy": energy,
            "stock": country["stockpile"].get("energy"),
            "used_naval_capacity": country["native"].get("used_naval_capacity")}


def expected_autosave_dates():
    return {f"{2200 + month // 12:04}.{month % 12 + 1:02}.01": month
            for month in range(1, 13)}


def autosave_date(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        # Reading the complete member checks its CRC before a copy is accepted.
        text = archive.read("gamestate").decode("utf-8-sig")
        if archive.testzip() is not None:
            raise ValueError("incomplete native autosave ZIP")
    match = re.search(r'^date\s*=\s*"?(\d{4}\.\d{2}\.\d{2})', text, re.M)
    if not match:
        raise ValueError("native autosave has no root date")
    return match.group(1)


def console_visible(captured):
    return any("使用任何调试命令" in row["text"]
               or re.fullmatch(r"Fast Forwarded \d+ Days", row["text"])
               for row in captured["rows"])


def close_console(stage):
    if console_visible(h.capture(stage + "-before")):
        h.press_scan_code(0x29, stage + "-close", 1)
        if console_visible(h.capture(stage + "-after")):
            raise RuntimeError("native console did not close")


def console(command, stage):
    ready = h.capture(stage + "-console-state")
    if not console_visible(ready):
        h.press_scan_code(0x29, stage + "-open", 1)
        ready = h.capture(stage + "-console-ready")
    if not console_visible(ready):
        raise RuntimeError("native console is not visibly open; refusing to type")
    if ready["resolution"] != [1024, 768]:
        raise RuntimeError("console input geometry requires the tested 1024x768 layout")
    # Native console.gui: (30+3, 100+310), 700x40 at gui_scale .75.
    # F12 can focus Debug View, so explicitly focus the observed console edit.
    h.click_point(120, 322, stage + "-focus-console-input")
    h.type_text(command, True, stage + "-command")
    if not command.startswith("fast_forward "):
        close_console(stage)


def frame(stage):
    result = h.capture(stage)
    return {"image": result["image"], "texts": [row["text"] for row in result["rows"]]}


def close_debug_overlay(stage):
    captured = h.capture(stage)
    titles = [row for row in captured["rows"] if row["text"] == "Debug View"]
    if not titles:
        return
    if len(titles) != 1:
        raise RuntimeError("ambiguous native debug window")
    title = titles[0]["box"]
    title_x = sum(point[0] for point in title) / 4
    title_y = sum(point[1] for point in title) / 4
    closes = []
    for row in captured["rows"]:
        if row["text"] not in ("×", "X", "x"):
            continue
        x = sum(point[0] for point in row["box"]) / 4
        y = sum(point[1] for point in row["box"]) / 4
        if x > title_x and abs(y - title_y) < 12:
            closes.append((round(x), round(y)))
    if (not closes and captured["resolution"] == [1024, 768]
            and abs(title_y - 347) < 6 and 35 < title_x < 130):
        # This tiny X is sometimes omitted by OCR. Its native position was
        # visually verified in this fixed-size window and retained GPU frames.
        closes = [(540, 347)]
    if len(closes) != 1:
        raise RuntimeError("native debug close control missing or ambiguous")
    h.click_point(*closes[0], stage + "-close")


def monthly(prefix, first_month, count):
    # The caller starts paused at the first of the month. Each fast_forward runs
    # the actual game calendar; native_save checks the resulting date on disk.
    for index in range(first_month, first_month + count):
        year, month = 2200 + index // 12, index % 12 + 1
        expected = f"{year:04}.{month:02}.01"
        stage = f"{prefix}m{index:02}"
        console("fast_forward 30", stage)
        previous.wait_for_native_date(expected, stage + "-date", 180)
        close_console(stage + "-console-finished")
        close_debug_overlay(stage + "-debug-overlay")
        labels = ARTIFACTS / "observed-notification-labels.json"
        if labels.exists():
            previous.acknowledge_notifications(json.loads(labels.read_text(encoding="utf-8")), stage + "-notifications")
        saved = r.native_save(stage, expected, (0,))
        summary = monthly_summary(saved)
        artifacts, _, _ = h.load_run()
        h.write_json(artifacts / (stage + ".economy.json"), summary)
        print(json.dumps(summary, ensure_ascii=False), flush=True)


def monthly_autosaves(prefix, first_month, count, anchor):
    """One actual 30-day step per snapshot; annual fast_forward skips months."""
    import audit_save
    if (not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", prefix)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", anchor)
            or first_month < 1 or count < 1 or first_month + count > 13):
        raise ValueError("unsafe scenario label or months outside the first year")
    artifacts, user, manifest = h.load_run()
    receipt = json.loads((artifacts / (anchor + ".native-save.json")).read_text(encoding="utf-8"))
    if h.sha256(Path(receipt["archived"])) != receipt["sha256"]:
        raise RuntimeError("native anchor changed")
    folder = Path(receipt["written_at"]).parent.resolve(strict=True)
    folder.relative_to((user / "save games").resolve())
    receipt_path = artifacts / (prefix + "-monthly-autosave-receipt.json")
    records = []
    if receipt_path.exists():
        prior = json.loads(receipt_path.read_text(encoding="utf-8"))
        if prior["anchor"] != anchor or prior["role"] != manifest["role"]:
            raise RuntimeError("monthly continuation anchor differs")
        records = prior["snapshots"]
        dates = expected_autosave_dates()
        for record in records:
            index = dates[record["date"]]
            if index >= first_month or h.sha256(artifacts / f"{prefix}m{index:02}.sav") != record["sha256"]:
                raise RuntimeError("monthly continuation evidence differs")
    for index in range(first_month, first_month + count):
        expected = f"{2200 + index // 12:04}.{index % 12 + 1:02}.01"
        stage = f"{prefix}m{index:02}"
        target = artifacts / (stage + ".sav")
        if target.exists():
            raise RuntimeError("refusing to overwrite monthly evidence")
        source = folder / ("autosave_" + expected + ".sav")
        old_mtime = source.stat().st_mtime_ns if source.exists() else 0
        console("fast_forward 30", stage + "-auto")
        previous.wait_for_native_date(expected, stage + "-auto-date", 180)
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            try:
                raw = source.read_bytes()
                if source.stat().st_mtime_ns > old_mtime and autosave_date(raw) == expected:
                    break
            except (OSError, ValueError, KeyError, zipfile.BadZipFile):
                pass
            time.sleep(.2)
        else:
            raise RuntimeError("fresh monthly native autosave missing: " + expected)
        target.write_bytes(raw)
        audit = audit_save.audit(target, (0,))
        if audit["date"] != expected:
            raise RuntimeError("actual monthly snapshot date differs")
        h.write_json(target.with_suffix(".audit.json"), audit)
        summary = monthly_summary(audit)
        h.write_json(target.with_suffix(".economy.json"), summary)
        records.append({"date": expected, "source": str(source), "sha256": audit["save_sha256"],
                        "source_mtime_ns": source.stat().st_mtime_ns, "bytes": len(raw)})
        h.write_json(receipt_path, {
            "status": "OBSERVATION_ONLY", "role": manifest["role"], "anchor": anchor,
            "snapshots": records, "method": "separate native fast_forward 30 per month"})
        print(json.dumps(summary), flush=True)
    close_console(prefix + "-monthly-auto-console-close")
    close_debug_overlay(prefix + "-monthly-auto-debug-close")
    previous.acknowledge_notifications(["王座之外，皆可吞噬。"], prefix + "-monthly-auto-queen")
    previous.acknowledge_notifications(["确认"], prefix + "-monthly-auto-tutorial")
    final_stage = prefix + ("yearui" if index == 12 else f"m{index:02}ui")
    final = r.native_save(final_stage, expected, (0,))
    keys = ("budget_categories", "stockpile", "variables", "flags", "owned_colonies")
    checks = {key: audit["countries"]["0"][key] == final["countries"]["0"][key] for key in keys}
    checks.update({key: audit[key] == final[key]
                   for key in ("districts", "pop_jobs", "pop_groups", "planets", "colonies")})
    h.write_json(artifacts / (prefix + f"-auto-ui-comparison-m{index:02}.json"), {
        "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
        "auto_sha256": audit["save_sha256"], "ui_sha256": final["save_sha256"]})
    if not all(checks.values()):
        raise RuntimeError("same-date native automatic/UI saves differ in gameplay fields")
    return {"status": "OBSERVATION_ONLY", "monthly_snapshots": count, "native_auto_ui": "PASS"}


def new_game(empire, prefix):
    """Use observed Chinese controls; verify the actual galaxy configuration."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", prefix):
        raise ValueError("unsafe scenario label")
    initial = h.capture(prefix + "-before-newgame")
    labels = {row["text"] for row in initial["rows"]}
    at_picker = "选择帝国" in labels and "选择" in labels
    if not at_picker and "新游戏" not in labels:
        close_debug_overlay(prefix + "-old-debug")
        previous.acknowledge_notifications(["王座之外，皆可吞噬。"], prefix + "-old-queen")
        previous.acknowledge_notifications(["确认"], prefix + "-old-tutorial")
        h.press_scan_code(0x01, prefix + "-old-menu", 1)
        h.click_text("退出到菜单", prefix + "-exit-menu")
        h.click_text("退出到菜单", prefix + "-exit-confirm")
        time.sleep(5)
    if not at_picker:
        h.click_text("新游戏", prefix + "-newgame")
    picker = h.capture(prefix + "-empire")
    rows = [row for row in picker["rows"] if h.normalized(row["text"]) == h.normalized(empire)
            and row["score"] >= .8 and max(point[0] for point in row["box"]) < 180]
    if picker["resolution"] != [1024, 768] or len(rows) != 1:
        raise RuntimeError("native empire list label missing or ambiguous")
    box = rows[0]["box"]
    h.click_point(round(sum(p[0] for p in box) / 4), round(sum(p[1] for p in box) / 4), prefix + "-empire-click")
    h.click_text("选择", prefix + "-select")
    galaxy = h.capture(prefix + "-galaxy-settings")
    if not any("200恒星" in h.normalized(row["text"]) for row in galaxy["rows"]):
        if galaxy["resolution"] != [1024, 768]:
            raise RuntimeError("unverified galaxy spinner geometry")
        h.click_point(740, 340, prefix + "-galaxy-smaller-1")
        h.click_point(740, 340, prefix + "-galaxy-smaller-2")
        galaxy = h.capture(prefix + "-galaxy-settings-tiny")
    labels = {h.normalized(row["text"]) for row in galaxy["rows"]}
    if not any("200恒星" in text for text in labels) or "尉官" not in labels or "3" not in labels:
        raise RuntimeError("actual galaxy settings differ from the 200-star/3-AI control")
    h.click_text("开始征程", prefix + "-start")
    deadline = time.monotonic() + 120
    poll = 0
    while time.monotonic() < deadline:
        time.sleep(3)
        frame = h.capture(prefix + f"-start-scene-{poll}")
        poll += 1
        if any(row["text"] == "我们的征途是星辰大海！" for row in frame["rows"]):
            break
    else:
        raise RuntimeError("new-game intro was not observed")
    h.click_text("我们的征途是星辰大海！", prefix + "-intro-ack")
    close_debug_overlay(prefix + "-initial-debug")
    saved = r.native_save(prefix + "m00", "2200.01.01", (0,))
    print(json.dumps(observe(prefix + "m00"), ensure_ascii=False), flush=True)
    return {"status": "OBSERVATION_ONLY", "date": saved["date"], "save_sha256": saved["save_sha256"]}


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ("snapshot-baseline", "gate-candidate", "prepare-single", "observe", "monthly", "console", "frame", "monthly-autosaves", "new-game"):
        command = sys.argv[1]
        if command == "snapshot-baseline":
            result = snapshot_baseline()
        elif command == "gate-candidate":
            result = gate_candidate()
        elif command == "prepare-single":
            result = prepare(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
        elif command == "observe":
            result = observe(sys.argv[2])
        elif command == "console":
            result = console(sys.argv[2], sys.argv[3])
        elif command == "frame":
            result = frame(sys.argv[2])
        elif command == "monthly-autosaves":
            result = monthly_autosaves(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
        elif command == "new-game":
            result = new_game(sys.argv[2], sys.argv[3])
        else:
            result = monthly(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
        print(json.dumps(result, ensure_ascii=False))
    elif sys.argv[1] == "native-save":
        saved = r.native_save(sys.argv[2], sys.argv[3], (0,))
        print(json.dumps({key: saved[key] for key in ("date", "save_sha256")}, ensure_ascii=False))
    elif sys.argv[1] == "native-load":
        print(json.dumps(r.native_load(sys.argv[2], sys.argv[3]), ensure_ascii=False))
    else:
        h.main()


if __name__ == "__main__":
    main()
