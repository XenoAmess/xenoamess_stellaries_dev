"""Freeze fixed Purifier post-economy UI and sealed source-derived analysis."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
RUN = Path(r"C:\Users\1\AppData\Local\xenoamess_stellaries_dev\artifacts\1019-implementation\runs\20261019T150008Z")
ECON = OUT.parent / "1019-rc6-economy/purifier"
PREFIXES = ("r6pu-after-queen", "r6pu-mother", "r6pu-queen-ack", "r6pu-contact-ack", "r6pu-crisis-ack",
            "r6pu-merc-tutorial-ack", "r6pu-tutorial-ack-observed", "r6pu-advisor", "r6pu-open-actual-designer",
            "r6pu-actual-designer", "r6pu-details-clean", "r6pu-designer", "r6pu-posttutorial", "r6pu-verified-designer",
            "r6pu-close-details-maintenance", "r6pu-ship-maintenance", "r6pu-exit-console", "r6pu-exit-debug")
YEAR_SHA = "79c49aaae6660f341c7f3e08751a415405e44c4d139d465367a8b07870b393b0"


def fp(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": sha256(body).hexdigest()}


def role(path):
    if path.suffix == ".sav": return "native_save"
    if path.suffix in (".jpg", ".png"): return "screenshot"
    if path.name.endswith((".action.json", ".native-save.json")): return "actions"
    return "analysis"


def source_refs(value, refs):
    if isinstance(value, list):
        for row in value: source_refs(row, refs)
    elif isinstance(value, dict):
        for key, hashkey in (("path", "sha256"), ("save", "save_sha256"), ("audit", "audit_sha256"), ("manifest", "manifest_sha256")):
            name, checksum = value.get(key), value.get(hashkey)
            if isinstance(name, str) and isinstance(checksum, str) and len(checksum) == 64:
                source = Path(name)
                if not source.is_absolute(): source = REPO / source
                assert "r6hvc" not in str(source).lower() and source.suffix != ".log" and "logs" not in source.parts
                assert fp(source)["sha256"] == checksum
                refs[str(source.resolve())] = {"path": str(source.resolve()), **fp(source)}
        for row in value.values(): source_refs(row, refs)


def choose():
    files = {}
    for path in RUN.glob("r6pu-*"):
        if path.is_file() and any(path.name.startswith(x + "-") or path.name.startswith(x + ".") for x in PREFIXES):
            assert path.suffix in (".json", ".jpg", ".png")
            files["raw/" + path.name] = path
    author = json.loads((OUT / "author-selection.json").read_bytes())
    for row in author["files"]:
        path = REPO / row["source"]
        assert fp(path) == {"bytes": row["bytes"], "sha256": row["sha256"]}
        assert row["destination"] not in files
        assert not Path(row["destination"]).is_absolute() and ".." not in Path(row["destination"]).parts
        files[row["destination"]] = path
    return dict(sorted(files.items())), author


def main():
    assert not (OUT / "index.json").exists(), "Existing UI checkpoint is immutable"
    files, author = choose()
    ui = [name for name in files if name.startswith("raw/")]
    assert len(ui) == 85
    assert fp(ECON / "r6puyearui.sav")["sha256"] == YEAR_SHA == fp(ECON / "r6pum12.sav")["sha256"]
    m12 = json.loads((ECON / "r6pum12-receipt.json").read_bytes())
    boundary = datetime.fromisoformat(m12["observed_at_utc"])
    assert m12["sha256"] == YEAR_SHA
    before = [{"path": name, "source": str(path.resolve()), **fp(path)} for name, path in files.items()]
    selection = {"schema": "eep.rc6.purifier-post-economy-ui-selection.v1", "run_id": "20261019T150008Z",
                 "status": "COMPLETED_PURIFIER_UI_ONLY_NOT_FINAL_RUN", "created_at_utc": datetime.now(timezone.utc).isoformat(),
                 "fixed_artifact_directory": str(RUN), "prefixes": PREFIXES, "post_m12_observed_at_utc": m12["observed_at_utc"],
                 "boundary_limit": "M12 actual observation is the lower bound; later rewritten collector receipt mtime is not worker-return time",
                 "author_selection_sha256": fp(OUT / "author-selection.json")["sha256"], "files": before,
                 "exclusions": ["r6hvc/Hive files", "active/final logs", "economy mNN/yearUI SAV or duplicate collector payload", "old-game/new-game/startup UI", "other runs", "production or tool mutation"]}
    (OUT / "selection.json").write_text(json.dumps(selection, indent=2) + "\n", encoding="utf-8")
    for row in before:
        target = OUT / row["path"]
        assert not target.exists()
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(row["source"], target)
        assert fp(target) == fp(Path(row["source"])) == {"bytes": row["bytes"], "sha256": row["sha256"]}
    assert files == choose()[0]
    for path in (OUT / "raw").glob("*.ocr.json"):
        ocr = json.loads(path.read_bytes())
        assert datetime.fromisoformat(ocr["captured_at_utc"]) > boundary
    refs = {}
    canonical_names = ("archive-index.json", "archive-supplement-v2.json", "byte-verification-v1.json", "manifest.json",
                       "native-branch-report-v2.json", "r6pu-economy-receipt.json", "r6pu-auto-ui-comparison-m12.json",
                       "r6pum12.sav", "r6pum12.audit.json", "r6pum12-receipt.json",
                       "r6puyearui.sav", "r6puyearui.audit.json", "r6puyearui.native-save.json")
    for name in canonical_names:
        path = ECON / name
        refs[str(path.resolve())] = {"path": str(path.resolve()), **fp(path)}
    for row in author.get("canonical_references", []):
        path = REPO / row["path"]
        assert fp(path) == {"bytes": row["bytes"], "sha256": row["sha256"]}
        generated_catalog = row.get("source_class") == "sealed_generated_static_documentation" and path.name == "modifiers.log" and path.is_relative_to(REPO)
        assert (generated_catalog or (path.suffix != ".log" and "logs" not in path.parts)) and "r6hvc" not in str(path).lower()
        refs[str(path.resolve())] = {"path": str(path.resolve()), **fp(path)}
    for row in author["files"]:
        path = OUT / row["destination"]
        if path.suffix == ".json": source_refs(json.loads(path.read_bytes()), refs)
    typed = []
    for row in before:
        path = OUT / row["path"]
        typed.append({"kind": role(path), "path": path.relative_to(REPO).as_posix(), "bytes": row["bytes"], "sha256": row["sha256"], "role": row["path"]})
    for name in canonical_names:
        path = ECON / name
        typed.append({"kind": role(path), "path": path.relative_to(REPO).as_posix(), **fp(path), "role": "canonical-economy/" + name})
    for row in author.get("canonical_references", []):
        path = REPO / row["path"]
        typed.append({"kind": "analysis", "path": path.relative_to(REPO).as_posix(), **fp(path), "role": "canonical-power/" + row["path"], "source_class": row.get("source_class", "sealed_power_source_or_report")})
    typed_doc = {"schema": "eep.rc6.purifier-ui-typed-references.v1", "status": "RAW_PROJECT_RELATIVE_REFERENCES_ONLY",
                 "scope": "Native UI observations and separate source-derived power calculation; no final configuration or release PASS", "references": typed}
    (OUT / "typed-references.json").write_text(json.dumps(typed_doc, indent=2) + "\n", encoding="utf-8")
    index = {"schema": "eep.rc6.purifier-mothership-ui-index.v1", "status": "BYTE_IDENTICAL_UI_ATTEMPTS_AND_SOURCE_CALCULATION",
             "created_at_utc": datetime.now(timezone.utc).isoformat(), "run_id": "20261019T150008Z", "game_pid": 30812,
             "selection_sha256": fp(OUT / "selection.json")["sha256"], "author_selection_sha256": fp(OUT / "author-selection.json")["sha256"],
             "typed_references_sha256": fp(OUT / "typed-references.json")["sha256"], "payload_file_count": len(before),
             "payload_bytes": sum(x["bytes"] for x in before), "raw_UI_file_count": 85, "yearUI_sha256": YEAR_SHA,
             "mother": {"fleet_id": 150, "ship_id": 1077, "actual_design_id": 1918, "C": 0, "date": "2201.01.01"},
             "canonical_power_bundle_not_duplicated": author.get("power_bundle"),
             "canonical_references_not_copied": sorted(refs.values(), key=lambda x: x["path"]), "files": before,
             "final_run_freeze": False, "logs_or_Hive_read_or_copied": False, "Mod_acceptance_pass": False,
             "limits": ["Maintenance 10.07 energy/2.88 alloys is the observed date and empire state with naval use115/cap66", "Early designer attempts were tutorial-obscured; later unobscured hover/click still showed details, no editor opened", "Power+9743 is source-derived, not a UI power readout", "Economy raw reused through canonical references; no duplicate SAV copied", "No UI/Git/Steam/production/tool operation"]}
    (OUT / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    (OUT / ".gitattributes").write_text("raw/** -text\nanalysis/** -text\nplans/** -text\nsource-primary/** -text\n", encoding="ascii")
    print(json.dumps({k: index[k] for k in ("status", "payload_file_count", "payload_bytes", "raw_UI_file_count")}))


if __name__ == "__main__":
    main()
