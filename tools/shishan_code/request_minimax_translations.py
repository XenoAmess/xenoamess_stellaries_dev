"""Collect MiniMax translation candidates; never edit Mod localization.

Reuses the read-only CK3 localization caller at its pinned workspace path. Each
request carries only a small set of strings and structural validation remains
the responsibility of the local acceptance scripts.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
LOCALIZATION = ROOT / "shishan_code_origin/mod/localisation"
CALLER = Path(r"C:\workspace\ck3_eternal_recurrence\tools\translate_localization_minimax.py")
ENTRY = re.compile(r'^ ([^:\s]+):\d+ "((?:[^"\\]|\\.)*)"$')
TARGETS = {
    "english": "English (United States)",
    "french": "French (France)",
    "german": "German (Germany)",
    "japanese": "Japanese (Japan)",
    "korean": "Korean (South Korea)",
    "polish": "Polish (Poland)",
    "russian": "Russian (Russia)",
    "spanish": "Spanish (Spain)",
    "braz_por": "Portuguese (Brazil)",
}


def keys(path: Path) -> list[str]:
    if not path.read_bytes().startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"missing BOM: {path}")
    return [match.group(1) for line in path.read_text(encoding="utf-8-sig").splitlines()
            if (match := ENTRY.fullmatch(line))]


def request_batch(source: Path, chosen: list[str], context: str,
                  targets: dict[str, str], source_language: str,
                  reference: Path | None) -> dict[str, dict[str, str]]:
    args = [sys.executable, str(CALLER), "--source", str(source),
            "--source-language", source_language, "--context", context,
            "--workers", "3", "--max-completion-tokens", "8000"]
    if reference is not None:
        args.extend(["--reference", str(reference), "--reference-language", "Simplified Chinese"])
    for target, name in targets.items():
        args.extend(["--target", f"{target}={name}"])
    for key in chosen:
        args.extend(["--key", key])
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", timeout=900)
    if result.returncode:
        if len(chosen) == 1:
            print(result.stderr.strip(), file=sys.stderr, flush=True)
            raise RuntimeError(f"MiniMax candidate key failed: {chosen[0]}")
        midpoint = len(chosen) // 2
        print(f"retrying in groups of {midpoint} and {len(chosen) - midpoint}", flush=True)
        left = request_batch(source, chosen[:midpoint], context, targets, source_language, reference)
        right = request_batch(source, chosen[midpoint:], context, targets, source_language, reference)
        return {language: {**left[language], **right[language]} for language in targets}
    data = json.loads(result.stdout)
    if set(data) != set(targets):
        raise ValueError("target set differs")
    for language, entries in data.items():
        if set(entries) != set(chosen):
            raise ValueError(f"key set differs: {language}")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-language", choices=("simp_chinese", "english"), default="simp_chinese")
    parser.add_argument("--targets", default="all", help="comma-separated Stellaris language codes")
    options = parser.parse_args()
    targets = TARGETS if options.targets == "all" else {
        key: TARGETS[key] for key in options.targets.split(",")
    }
    source_dir = LOCALIZATION / options.source_language
    output_name = "translation_candidates"
    if options.source_language == "english":
        output_name = (
            "translation_candidates_english_other"
            if set(targets) == {"korean", "russian", "braz_por"}
            else "translation_candidates_english"
        )
    output_dir = ROOT / "_runtime/shishan_code" / output_name
    if not os.environ.get("MINIMAX_API_KEY"):
        raise RuntimeError("MINIMAX_API_KEY is not configured")
    if not CALLER.is_file():
        raise FileNotFoundError(CALLER)
    output_dir.mkdir(parents=True, exist_ok=True)
    context = (
        "Stellaris 4.5.1 science-fiction Mod. Mechanical civilization with legacy spaghetti code; "
        "Vivhite is the given English name of the female immortal machine leader 白绮. "
        "Translate 屎山代码 idiomatically as Spaghetti Code; 大厦将倾 is an imminent system collapse. "
        "Maintain a somber, restrained voice. Keep Paradox localization markup exactly. "
        "Use contemporary game UI language, never archaic literary diction. "
        "Do not leave source-language words or Chinese passages in the output. "
        "Do not enclose dialogue in quotation marks or add ASCII double quotes inside any value."
    )
    for source in sorted(source_dir.glob("*.yml")):
        reference = (LOCALIZATION / "simp_chinese" / source.name.replace("_l_english.yml", "_l_simp_chinese.yml")) if options.source_language == "english" else None
        all_keys = keys(source)
        for start in range(0, len(all_keys), 12):
            chosen = all_keys[start:start + 12]
            output = output_dir / f"{source.stem}-{start // 12:02}.json"
            if output.exists():
                print(f"cached {output.name}", flush=True)
                continue
            print(f"requesting {source.name} batch {start // 12:02}: {len(chosen)} keys", flush=True)
            data = request_batch(source, chosen, context, targets,
                                 "English" if options.source_language == "english" else "Simplified Chinese",
                                 reference)
            output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"saved {output.name}", flush=True)


if __name__ == "__main__":
    main()
