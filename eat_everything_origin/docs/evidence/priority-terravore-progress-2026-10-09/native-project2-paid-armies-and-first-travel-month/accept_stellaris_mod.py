#!/usr/bin/env python3
"""Validate a Stellaris Mod package with Kaishek syntax and static contracts.

This check deliberately makes no opcode or runtime-semantic claim for paths not
registered by a game-version profile. A passing report must be paired with a
separate Stellaris runtime test for behavioral acceptance.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "kaishek-cli/target/kaishek-cli-0.1.0-SNAPSHOT.jar"
CYGNUS_451_SHA256 = "6fe06709f265e726722dc23f617c5fc4e5557629e2d43fe312016aba547c83e4"
LOCALIZATION = re.compile(r'^ ([^:\s]+):\d* "((?:[^"\\]|\\.)*)"$')
TOKEN = re.compile(r"\$[^$\r\n]+\$|§.|\\.")
ASSET = re.compile(r'"(gfx/[^"\r\n]+\.dds)"', re.IGNORECASE)
VERSION = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_localization(path: Path, language: str, errors: list[dict]) -> dict[str, str]:
    data = path.read_bytes()
    if not data.startswith(b"\xef\xbb\xbf"):
        errors.append({"code": "LOCALIZATION_BOM", "path": str(path)})
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        errors.append({"code": "LOCALIZATION_ENCODING", "path": str(path)})
        return {}
    if not lines or lines[0] != f"l_{language}:":
        errors.append({"code": "LOCALIZATION_HEADER", "path": str(path)})
    entries: dict[str, str] = {}
    for number, line in enumerate(lines[1:], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = LOCALIZATION.fullmatch(line)
        if not match:
            errors.append({"code": "LOCALIZATION_SYNTAX", "path": str(path), "line": number})
            continue
        key, value = match.groups()
        if key in entries:
            errors.append({"code": "LOCALIZATION_DUPLICATE_KEY", "path": str(path), "key": key})
        if not value:
            errors.append({"code": "LOCALIZATION_EMPTY_VALUE", "path": str(path), "key": key})
        entries[key] = value
    return entries


def check(mod: Path, game: Path, expected_sha: str, cli: Path, version_source: Path | None = None) -> dict:
    errors: list[dict] = []
    package = mod / "mod" if (mod / "mod/descriptor.mod").is_file() else mod
    descriptor = package / "descriptor.mod"
    exe = game / "stellaris.exe"
    if not exe.is_file() or sha256(exe).lower() != expected_sha.lower():
        errors.append({"code": "GAME_EXE_IDENTITY", "path": str(exe)})
    if not cli.is_file():
        errors.append({"code": "KAISHEK_CLI_MISSING", "path": str(cli)})
    version_file = version_source or (mod / "VERSION" if (mod / "VERSION").is_file() else package / "VERSION")
    if not version_file.is_file() or not descriptor.is_file():
        errors.append({"code": "MOD_METADATA_MISSING", "path": str(mod)})
    else:
        version = version_file.read_text(encoding="utf-8-sig").strip()
        text = descriptor.read_text(encoding="utf-8-sig")
        match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        supported = re.search(r'^supported_version\s*=\s*"([^"]+)"', text, re.MULTILINE)
        if not VERSION.fullmatch(version) or not match or match.group(1) != version or not supported:
            errors.append({"code": "MOD_VERSION_CONTRACT", "path": str(descriptor)})
        settings_file = game / "launcher-settings.json"
        if supported and settings_file.is_file():
            settings = json.loads(settings_file.read_text(encoding="utf-8-sig"))
            actual = settings.get("rawVersion", "").removeprefix("v").split(".")
            declared = supported.group(1).split(".")
            if not actual or not all(part == "*" or (index < len(actual) and part == actual[index])
                                     for index, part in enumerate(declared)):
                errors.append({"code": "MOD_SUPPORTED_VERSION", "path": str(descriptor),
                               "declared": supported.group(1), "game": settings.get("rawVersion")})
    script_files = sorted(
        path for path in package.rglob("*")
        if path.is_file() and (path.suffix.lower() in {".txt", ".gfx", ".gui"} or path.name == "descriptor.mod")
    )
    parsed = 0
    if not script_files:
        errors.append({"code": "NO_P_SCRIPTS", "path": str(package)})
    for path in script_files:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append({"code": "P_SCRIPT_BOM", "path": str(path)})
            continue
        try:
            data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append({"code": "P_SCRIPT_ENCODING", "path": str(path)})
            continue
        if cli.is_file():
            command = ["java", "-jar", str(cli), "parse", "--file", str(path)]
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
            try:
                payload = json.loads(result.stdout)
            except json.JSONDecodeError:
                errors.append({"code": "KAISHEK_RESPONSE", "path": str(path)})
                continue
            if result.returncode or payload.get("status") != "PARSED" or payload.get("diagnostics") or not payload.get("roundTrip"):
                errors.append({"code": "P_SCRIPT_PARSE", "path": str(path), "diagnostics": payload.get("diagnostics", [])})
            else:
                parsed += 1
        for asset in ASSET.findall(data.decode("utf-8")):
            relative = Path(asset)
            if not (package / relative).is_file() and not (game / relative).is_file():
                errors.append({"code": "ASSET_REFERENCE_MISSING", "path": str(path), "asset": asset})
    dds = sorted(package.rglob("*.dds"))
    for path in dds:
        if len(path.read_bytes()) < 128 or not path.read_bytes().startswith(b"DDS "):
            errors.append({"code": "DDS_HEADER", "path": str(path)})
    game_languages = sorted(path.name for path in (game / "localisation").iterdir() if path.is_dir()) if (game / "localisation").is_dir() else []
    if not game_languages:
        errors.append({"code": "GAME_LANGUAGES_MISSING", "path": str(game / "localisation")})
    locales: dict[str, dict[str, str]] = {}
    localization_root = package / "localisation"
    has_localization = any(localization_root.rglob("*.yml"))
    for language in game_languages if has_localization else []:
        files = sorted(localization_root.rglob(f"*_l_{language}.yml"))
        if not files:
            errors.append({"code": "LOCALIZATION_LANGUAGE_MISSING", "language": language})
            continue
        values: dict[str, str] = {}
        for path in files:
            for key, value in read_localization(path, language, errors).items():
                if key in values:
                    errors.append({"code": "LOCALIZATION_DUPLICATE_KEY", "language": language, "key": key})
                values[key] = value
        locales[language] = values
    if "simp_chinese" in locales:
        reference = locales["simp_chinese"]
        for language, values in locales.items():
            missing = sorted(set(reference) - set(values))
            extra = sorted(set(values) - set(reference))
            if missing or extra:
                errors.append({"code": "LOCALIZATION_KEY_SET", "language": language, "missing": missing, "extra": extra})
            for key in set(values) & set(reference):
                if Counter(TOKEN.findall(values[key])) != Counter(TOKEN.findall(reference[key])):
                    errors.append({"code": "LOCALIZATION_TOKEN_DRIFT", "language": language, "key": key})
                if language != "simp_chinese" and values[key] == reference[key] and re.search(r"[\u4e00-\u9fff]", values[key]):
                    errors.append({"code": "LOCALIZATION_CHINESE_PLACEHOLDER", "language": language, "key": key})
    return {
        "status": "PASS" if not errors else "FAIL",
        "game_exe_sha256": sha256(exe) if exe.is_file() else None,
        "p_scripts": len(script_files), "p_parsed": parsed, "dds": len(dds),
        "languages": game_languages,
        "localization_keys": len(locales.get("simp_chinese", {})),
        "localization_applicability": "checked" if has_localization else "not_applicable_no_localization_files",
        "semantic_scope": "syntax/package only; runtime and unregistered opcodes require Stellaris tests",
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod", required=True, type=Path)
    parser.add_argument("--game", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--expected-exe-sha256", default=CYGNUS_451_SHA256)
    parser.add_argument("--cli", type=Path, default=CLI)
    parser.add_argument("--version-file", type=Path, help="explicit VERSION source for a package in a multi-Mod repository")
    args = parser.parse_args()
    result = check(args.mod.resolve(), args.game.resolve(), args.expected_exe_sha256, args.cli.resolve(),
                   args.version_file.resolve() if args.version_file else None)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "p_scripts", "p_parsed", "dds", "localization_keys")}, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
