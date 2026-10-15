"""Build an isolated, reversible computation-OFF package; never launch a game."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil


ROOT = Path(__file__).resolve().parents[3]
MOD_ROOT = ROOT / "shishan_code_origin"
ALLOWED_OUTPUT_ROOT = ROOT / "_runtime/shishan_code/20261015-remaining"
OVERRIDE = "common/scripted_effects/shishan_code_architecture_effects.txt"
EVENT = "events/shishan_perf_probe_events.txt"
EFFECT = b"shishan_code_architecture_refresh_effect"
OFF_FLAG = "shishan_perf_probe_compute_off"
REVIEWED_EVENT_SHA256 = "e661e936b09e03fa3a9742c8f318e41323c10596a3b5bef338ce372d410e0d71"
PREFIX = b"""
	# PERF_FIXTURE_COMPUTATION_GATE_BEGIN: preserve the enclosed production bytes.
	if = {
		limit = {
			OR = {
				NOT = { has_origin = origin_shishan_code }
				NOT = { has_country_flag = shishan_perf_probe_compute_off }
			}
		}
"""
SUFFIX = b"""
	}
	# PERF_FIXTURE_COMPUTATION_GATE_END
"""


class FixtureError(ValueError):
    """Refuse any ambiguous source, output, or computation-gate package."""


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def content(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p.read_bytes())}
            for p in sorted(root.rglob("*")) if p.is_file()}


def body_span(raw: bytes) -> tuple[int, int]:
    """Locate one top-level named effect; preserve comments/strings verbatim."""
    matches = list(re.finditer(rb"(?m)^" + re.escape(EFFECT) + rb"\s*=\s*\{", raw))
    if len(matches) != 1:
        raise FixtureError("expected exactly one refresh definition")
    opening = matches[0].end() - 1
    depth, quoted, escaped, comment = 0, False, False, False
    for index in range(opening, len(raw)):
        char = raw[index]
        if comment:
            comment = char != 10
            continue
        if quoted:
            if escaped:
                escaped = False
            elif char == 92:
                escaped = True
            elif char == 34:
                quoted = False
            continue
        if char == 35:
            comment = True
        elif char == 34:
            quoted = True
        elif char == 123:
            depth += 1
        elif char == 125:
            depth -= 1
            if depth == 0:
                return opening + 1, index
    raise FixtureError("unclosed refresh body")


def wrap_refresh(raw: bytes) -> bytes:
    if OFF_FLAG.encode() in raw or b"PERF_FIXTURE_COMPUTATION_GATE" in raw:
        raise FixtureError("source already contains fixture control")
    begin, end = body_span(raw)
    wrapped = raw[:begin] + PREFIX + raw[begin:end] + SUFFIX + raw[end:]
    if unwrap_refresh(wrapped) != raw:
        raise FixtureError("production bytes are not reversibly preserved")
    return wrapped


def unwrap_refresh(raw: bytes) -> bytes:
    begin, end = body_span(raw)
    body = raw[begin:end]
    if not body.startswith(PREFIX) or not body.endswith(SUFFIX):
        raise FixtureError("wrapper differs from the fixed computation gate")
    original_body = body[len(PREFIX):-len(SUFFIX)]
    return raw[:begin] + original_body + raw[end:]


def validate_source(source: Path, identity: dict, version: str) -> dict:
    actual = content(source)
    if identity.get("status") != "PASS" or identity.get("version") != "0.2.1" or version != "0.2.1":
        raise FixtureError("requires the accepted formal 0.2.1 identity")
    if len(actual) != 90 or actual != identity.get("content"):
        raise FixtureError("source does not match all 90 released production files")
    if any(b"shishan_perf_probe" in (source / path).read_bytes() for path in actual):
        raise FixtureError("fixture prefix is occupied by source content")
    body_span((source / OVERRIDE).read_bytes())
    return actual


def validate_output_path(output: Path, source: Path) -> Path:
    output, source = output.resolve(), source.resolve()
    if output.exists():
        raise FixtureError("output already exists; never overwrite a possible active package")
    if not output.is_relative_to(ALLOWED_OUTPUT_ROOT.resolve()):
        raise FixtureError("output must be a new directory under the dedicated remaining-runtime root")
    if output.is_relative_to(source) or source.is_relative_to(output):
        raise FixtureError("output intersects production source")
    for parent in output.parents:
        if parent.is_relative_to(ALLOWED_OUTPUT_ROOT.resolve()) and (
            (parent / "descriptor.mod").is_file() or (parent / "mod/descriptor.mod").is_file()
        ):
            raise FixtureError("output is inside an existing possible active package")
    return output


def validate_fixture(source: Path, package: Path, event_bytes: bytes) -> dict:
    validate_event_asset(event_bytes)
    original, actual = content(source), content(package)
    if set(actual) - set(original) != {EVENT} or set(original) - set(actual):
        raise FixtureError("unexpected added or missing package files")
    changed = [name for name in original if original[name] != actual[name]]
    if changed != [OVERRIDE]:
        raise FixtureError("exactly the architecture effects path may differ")
    if unwrap_refresh((package / OVERRIDE).read_bytes()) != (source / OVERRIDE).read_bytes():
        raise FixtureError("restored architecture source differs from production")
    if (package / EVENT).read_bytes() != event_bytes:
        raise FixtureError("event asset differs from the reviewed fixture source")
    return {"production_files": 90, "unchanged_production_files": 89, "changed": changed,
            "added": [EVENT], "removed": [], "file_count": len(actual), "content": actual,
            "restores_exact_production_bytes": True}


def validate_event_asset(raw: bytes) -> None:
    # Exact reviewed input controller: unexpected APIs/guards fail closed.
    # Separate actual-AST tests check its behavior; this is an identity gate.
    if sha(raw) != REVIEWED_EVENT_SHA256:
        raise FixtureError("event controller differs from the reviewed, guarded input-only asset")


def write_json(path: Path, value: dict):
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def build(source: Path, output: Path, identity_path: Path, version_path: Path) -> dict:
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    version = version_path.read_text(encoding="utf-8").strip()
    validate_source(source, identity, version)
    output = validate_output_path(output, source)
    raw = (source / OVERRIDE).read_bytes()
    wrapped = wrap_refresh(raw)
    event_source = MOD_ROOT / "testing/performance/mod" / EVENT
    event_bytes = event_source.read_bytes()
    validate_event_asset(event_bytes)
    output.mkdir(parents=True)
    shutil.copytree(source, output / "mod")
    (output / "mod" / OVERRIDE).write_bytes(wrapped)
    event_path = output / "mod" / EVENT
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_bytes(event_bytes)
    (output / "VERSION").write_bytes(version_path.read_bytes())
    # Kept outside mod/ so it cannot become a second script definition.
    (output / "architecture-effects.production-original.txt").write_bytes(raw)
    details = validate_fixture(source, output / "mod", event_bytes)
    begin, end = body_span(raw)
    report = {"status": "PREPARED_NOT_RUNTIME_TESTED", "created_at_utc": datetime.now(timezone.utc).isoformat(),
              "source": str(source.resolve()), "output": str(output), "version": version,
              "source_identity_sha256": sha(identity_path.read_bytes()),
              "source_mod_tree_sha256": identity["mod_tree_sha256"],
              "override": {"path": OVERRIDE, "original_sha256": sha(raw), "wrapped_sha256": sha(wrapped),
                           "original_body_offsets": [begin, end], "original_body_sha256": sha(raw[begin:end]),
                           "roundtrip_sha256": sha(unwrap_refresh(wrapped))},
              "event_source": str(event_source.resolve()), "event_sha256": sha(event_bytes),
              "computation_off_flag": OFF_FLAG,
              "semantics": "Origin + OFF skips actual refresh and retains existing B; other states execute the original body. Not economic OFF.",
              "native_timing": "NOT RUN", **details}
    write_json(output / "source-manifest.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-mod", type=Path, default=MOD_ROOT / "mod")
    parser.add_argument("--identity", type=Path, default=MOD_ROOT / "evidence/v0.2.1/acceptance/release-identity.json")
    parser.add_argument("--version-file", type=Path, default=MOD_ROOT / "VERSION")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = build(args.source_mod, args.output, args.identity, args.version_file)
    except (FixtureError, OSError, ValueError) as error:
        parser.exit(1, f"performance fixture refused: {error}\n")
    print(json.dumps({k: report[k] for k in ("status", "output", "file_count", "unchanged_production_files", "restores_exact_production_bytes")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
