"""Request targeted MiniMax repairs for untranslated localization values.

Candidates and API responses stay in _runtime; only validated improvements are
added to the curated override file. The API key remains in the environment.
"""

from __future__ import annotations

from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from promote_translations import LOCALIZATION, OVERRIDES, ROOT, source_entries, TOKEN
from request_minimax_translations import CALLER, TARGETS


OUTPUT = ROOT / "_runtime/shishan_code/translation_repair"
HAN = re.compile(r"[\u4e00-\u9fff]")


def entries(language: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted((LOCALIZATION / language).glob("*.yml")):
        result.update(source_entries(path))
    return result


def needs_repair(key: str, current: str, english: str, language: str) -> bool:
    if language != "japanese" and HAN.search(current):
        return True
    if current == english and (len(current) >= 20 or key.endswith("_warning")):
        return True
    return False


def request(language: str, chosen: list[str], source_files: list[Path]) -> dict[str, str]:
    context = (
        "Stellaris 4.5.1 game localization. Translate every supplied English string "
        f"fully into {TARGETS[language]}. The prior model left these strings in English, "
        "so a copied English sentence is invalid. Preserve all $KEY$ and formatting "
        "tokens exactly, and never include Chinese text. Vivhite is a proper name. "
        "This story is about mechanical beings maintaining dangerous legacy code. "
        "Keep the UI succinct and the dialogue sombre. Return JSON only."
    )
    result: dict[str, str] = {}
    for source in source_files:
        available = source_entries(source)
        subset = [key for key in chosen if key in available]
        for start in range(0, len(subset), 4):
            batch = subset[start:start + 4]
            args = [sys.executable, str(CALLER), "--source", str(source),
                    "--source-language", "English", "--context", context,
                    "--workers", "1", "--max-completion-tokens", "5000",
                    "--target", f"{language}={TARGETS[language]}"]
            for key in batch:
                args.extend(["--key", key])
            run = subprocess.run(args, capture_output=True, text=True,
                                 encoding="utf-8", timeout=600)
            if run.returncode:
                raise RuntimeError(f"MiniMax repair failed for {language} {batch}: {run.stderr[-1200:]}")
            candidate = json.loads(run.stdout)[language]
            result.update(candidate)
            print(f"{language}: repaired candidate {len(result)}/{len(chosen)}", flush=True)
    return result


def main() -> None:
    if not os.environ.get("MINIMAX_API_KEY"):
        raise RuntimeError("MINIMAX_API_KEY is not configured")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    english = entries("english")
    source_files = sorted((LOCALIZATION / "english").glob("*.yml"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    for language in TARGETS:
        if language == "english":
            continue
        current = entries(language)
        chosen = [key for key in english if needs_repair(key, current[key], english[key], language)]
        if not chosen:
            continue
        cache = OUTPUT / f"{language}.json"
        if cache.is_file():
            candidate = json.loads(cache.read_text(encoding="utf-8"))
        else:
            print(f"{language}: requesting {len(chosen)} repairs", flush=True)
            candidate = request(language, chosen, source_files)
            cache.write_text(json.dumps(candidate, ensure_ascii=False, indent=2), encoding="utf-8")
        for key in chosen:
            value = candidate[key]
            if '"' in value or "\n" in value or not value:
                raise ValueError(f"invalid quote or newline: {language} {key}")
            if Counter(TOKEN.findall(value)) != Counter(TOKEN.findall(english[key])):
                raise ValueError(f"token drift: {language} {key}")
            if needs_repair(key, value, english[key], language):
                print(f"still needs review: {language} {key}", flush=True)
                continue
            overrides.setdefault(language, {})[key] = value
        OVERRIDES.write_text(json.dumps(overrides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("MiniMax targeted pass complete", flush=True)


if __name__ == "__main__":
    main()
