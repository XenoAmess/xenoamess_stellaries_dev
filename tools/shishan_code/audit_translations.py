"""Print semantic-review candidates after the structural localization gate."""

from pathlib import Path
import re

from promote_translations import LOCALIZATION, source_entries

ENGLISH = {}
for path in (LOCALIZATION / "english").glob("*.yml"):
    ENGLISH.update(source_entries(path))

findings = 0
for directory in sorted(LOCALIZATION.iterdir()):
    if not directory.is_dir() or directory.name in {"simp_chinese", "english"}:
        continue
    entries = {}
    for path in directory.glob("*.yml"):
        entries.update(source_entries(path))
    english = [key for key, value in entries.items()
               if value == ENGLISH.get(key) and len(value) >= 20 and len(value.split()) >= 3]
    han = [key for key, value in entries.items()
           if directory.name != "japanese" and re.search(r"[\u4e00-\u9fff]", value)]
    findings += len(english) + len(han)
    print(f"{directory.name}: {len(english)} unchanged English entries, {len(han)} Han-script entries")
    if english:
        print("  English:", ", ".join(english))
    if han:
        print("  Han:", ", ".join(han))
if findings:
    raise SystemExit(1)
