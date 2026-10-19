"""Supplement the frozen settlement checker with global native liveness evidence.

Historical job records are accepted only when unchanged and all of their real
population references are dead. The original diagnostic is never rewritten.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile

import audit_save as a
import check_1019 as original


def objects(body):
    return {key: value for key, value, nested in a.fields(body) if nested}


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def inspect_liveness(before_text, after_text, source_world):
    before, after = objects(before_text), objects(after_text)
    required = {"planets", "colony", "country", "pop_groups", "pop_jobs"}
    if not required <= before.keys() or not required <= after.keys():
        raise ValueError("complete native population, job and country tables required")
    bp = objects(a.block(before["planets"], "planet"))[str(source_world)]
    ap = objects(a.block(after["planets"], "planet"))[str(source_world)]
    bn, an = a.scalars(bp), a.scalars(ap)
    colony_id = bn.get("colony")
    if type(colony_id) is not int:
        raise ValueError("before source must have an explicit colony ID")
    bc = a.block(before["colony"], str(colony_id))
    ac = a.block(after["colony"], str(colony_id))
    cn = a.scalars(ac)
    groups = {key: a.scalars(value) for key, value in objects(after["pop_groups"]).items()}
    before_groups = set(a.ids(a.block(bc, "pop_groups")))
    before_jobs = objects(before["pop_jobs"])
    after_jobs = objects(after["pop_jobs"])
    prior_ids = set(a.ids(a.block(bc, "pop_jobs")))
    listed_ids = set(a.ids(a.block(ac, "pop_jobs")))
    global_source_jobs = {int(key) for key, value in after_jobs.items()
                          if a.scalars(value).get("planet") == colony_id}
    examined = sorted(listed_ids | global_source_jobs)
    job_evidence = {}
    for identity in examined:
        key = str(identity)
        body = after_jobs.get(key, "")
        native = a.scalars(body)
        refs = {int(value) for value in re.findall(r"\bpop_group\s*=\s*(\d+)", body)}
        refs.discard(4294967295)
        workforce = native.get("workforce", 0)
        auto = native.get("automated_workforce", 0)
        unchanged = bool(body) and identity in prior_ids and body == before_jobs.get(key)
        dead = all(str(ref) not in groups or
                   (finite(groups[str(ref)].get("size")) and groups[str(ref)]["size"] == 0)
                   for ref in refs)
        safe = (unchanged and native.get("planet") == colony_id
                and finite(workforce) and workforce >= -1
                and finite(auto) and -1 <= auto <= 0
                and refs <= before_groups and dead and (workforce <= 0 or bool(refs)))
        job_evidence[key] = {"native": native, "population_references": sorted(refs),
                             "unchanged_before_record": unchanged,
                             "all_population_references_dead": dead,
                             "historical_only": safe}
    live_groups = {key: record for key, record in groups.items()
                   if record.get("planet") == colony_id and
                   (not finite(record.get("size")) or record["size"] != 0)}
    country_refs = {}
    for key, body in objects(after["country"]).items():
        found = {field: a.ids(a.block(body, field)) for field in
                 ("owned_planets", "controlled_colonies", "controlled_planets")}
        if (colony_id in found["owned_planets"] or colony_id in found["controlled_colonies"]
                or source_world in found["controlled_planets"]):
            country_refs[key] = found
    checks = {
        "source_colony_reference_absent_or_original": an.get("colony") in (None, colony_id),
        "source_physically_shattered": an.get("planet_class") == "pc_shattered",
        "source_without_owner_or_controller": "owner" not in an and "controller" not in an,
        "colony_population_list_empty": not a.ids(a.block(ac, "pop_groups")),
        "live_population_counters_zero_or_absent": all(
            finite(cn.get(key, 0)) and cn.get(key, 0) == 0
            for key in ("num_sapient_pops", "employable_pops")),
        "no_global_population_at_source_colony": not live_groups,
        "no_country_ownership_or_control": not country_refs,
        "listed_job_ids_not_new": listed_ids <= prior_ids,
        "all_global_and_listed_jobs_historical_only": all(
            record["historical_only"] for record in job_evidence.values()),
    }
    return {"status": "PASS_SCOPED" if all(checks.values()) else "FAIL", "checks": checks,
            "source_world": source_world, "colony_id": colony_id,
            "retained_job_ids": examined, "jobs": job_evidence,
            "live_global_groups": live_groups, "country_references": country_refs,
            "limitation": "Proves absence of live colony/population/job allocations; historical storage may remain."}


def native_text(path):
    with zipfile.ZipFile(path) as archive:
        return archive.read("gamestate").decode("utf-8-sig")


def reference(path):
    path = Path(path).resolve()
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def check(case, before, after, reload_save=None):
    worlds = sorted({case["source_world"], case["core_world"]})
    b, f = original.n.observe(before, worlds), original.n.observe(after, worlds)
    reload_observation = original.n.observe(reload_save, worlds) if reload_save else None
    diagnostic = original.settlement(case, b, f, reload_observation)
    liveness = inspect_liveness(native_text(before), native_text(after), case["source_world"])
    checks = {"all_original_non_liveness_checks_pass": all(
                  value is True for key, value in diagnostic["checks"].items()
                  if key != "source_colony_destroyed"),
              "original_liveness_failure_only_job_list": all(
                  value is True for key, value in diagnostic["actual"]["source_colony_liveness"].items()
                  if key != "colony_pop_job_list_empty"),
              "global_native_liveness": liveness["status"] == "PASS_SCOPED"}
    return {"schema": "eep.1020.settlement-global-liveness.v1",
            "status": "PASS_SCOPED" if all(checks.values()) else "FAIL",
            "scope": "Original settlement math and receipts, plus strict global dead-job verification.",
            "checks": checks, "original_diagnostic_unchanged": diagnostic,
            "native_liveness": liveness,
            "sources": {"before": reference(before), "after": reference(after),
                        "reload": reference(reload_save) if reload_save else None,
                        "original_checker": reference(original.__file__),
                        "supplement": reference(__file__)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--reload", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("refusing to overwrite a prior diagnostic")
    result = check(json.loads(args.case.read_text(encoding="utf-8")), args.before, args.after, args.reload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write("\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}))
    return 0 if result["status"] == "PASS_SCOPED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
