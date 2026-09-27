"""Review gate and file writer for MiniMax localization candidates.

The MiniMax caller only produces JSON in _runtime. This deterministic local
step verifies keys/tokens, applies curated corrections, and writes game YML.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LOCALIZATION = ROOT / "shishan_code_origin/mod/localisation"
CANDIDATES = ROOT / "_runtime/shishan_code/translation_candidates"
CANDIDATES_EN = ROOT / "_runtime/shishan_code/translation_candidates_english"
CANDIDATES_EN_OTHER = ROOT / "_runtime/shishan_code/translation_candidates_english_other"
OVERRIDES = ROOT / "tools/shishan_code/translation_overrides.json"
ENTRY = re.compile(r'^ ([^:\s]+):\d+ "((?:[^"\\]|\\.)*)"$')
TOKEN = re.compile(r"\$[^$\r\n]+\$|§.|\\.")


def source_entries(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines()[1:]:
        match = ENTRY.fullmatch(line)
        if match:
            result[match.group(1)] = match.group(2)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", required=True)
    args = parser.parse_args()
    corrections = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.is_file() else {}
    for source in sorted((LOCALIZATION / "simp_chinese").glob("*.yml")):
        reference = source_entries(source)
        if not reference:
            raise ValueError(f"no source entries: {source}")
        merged: dict[str, str] = {}
        use_english = args.language != "english"
        candidate_dir = (
            CANDIDATES_EN_OTHER if args.language in {"korean", "russian", "braz_por"}
            else CANDIDATES_EN if use_english else CANDIDATES
        )
        candidate_stem = source.stem.replace("_l_simp_chinese", "_l_english") if use_english else source.stem
        for batch in sorted(candidate_dir.glob(candidate_stem + "-*.json")):
            payload = json.loads(batch.read_text(encoding="utf-8"))
            values = payload.get(args.language)
            if not isinstance(values, dict):
                raise ValueError(f"missing language in {batch}: {args.language}")
            duplicate = set(values) & set(merged)
            if duplicate:
                raise ValueError(f"duplicate keys: {sorted(duplicate)}")
            merged.update(values)
        if set(merged) != set(reference):
            raise ValueError(f"key mismatch {source.name}: missing={sorted(set(reference)-set(merged))}")
        merged.update({key: value for key, value in corrections.get(args.language, {}).items() if key in reference})
        for key, value in merged.items():
            if not isinstance(value, str) or not value or '"' in value or "\n" in value:
                raise ValueError(f"invalid value {args.language} {key}")
            if Counter(TOKEN.findall(value)) != Counter(TOKEN.findall(reference[key])):
                raise ValueError(f"token drift {args.language} {key}")
            if value == reference[key] and re.search(r"[\u4e00-\u9fff]", value):
                raise ValueError(f"untranslated Chinese value {args.language} {key}")
        target_dir = LOCALIZATION / args.language
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / source.name.replace("_l_simp_chinese.yml", f"_l_{args.language}.yml")
        lines = [f"l_{args.language}:"] + [f' {key}:0 "{merged[key]}"' for key in reference]
        target.write_text("\ufeff" + "\n".join(lines) + "\n", encoding="utf-8")
        print(f"{args.language}: {target.name}: {len(reference)} keys")


if __name__ == "__main__":
    main()
