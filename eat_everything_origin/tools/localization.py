"""Build authored baselines and protected, auditable MiniMax translations."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import sys
import winreg
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parents[1]
CALLER = Path(r"D:\workspace\ck3_eternal_recurrence\tools")
sys.path.insert(0, str(CALLER))
import translate_localization_minimax as translator

TARGETS = {
    "french": "French (France)",
    "japanese": "Japanese (Japan)", "korean": "Korean (South Korea)",
    "polish": "Polish (Poland)", "russian": "Russian (Russia)",
    "spanish": "Spanish (Spain)", "braz_por": "Portuguese (Brazil)",
}
CONTEXT = (
    "Stellaris 4.5.2 Heart of Devouring origin. Queen Vivhite is the English name of 女王·白绮. "
    "Icy, ruthless, arrogant evil ruler; aliens and planets are food. Preserve every dynamic "
    "bracket expression, dollar reference, color code and escaped newline exactly. "
    "Use native game UI terms, leave no untranslated source text, add no ASCII double quotes. "
    "C/G/D are ledger variable labels. A population amount of 100 is literal, not 100 old pops."
)


def render(language, entries):
    target = ROOT / f"mod/localisation/{language}/eep_l_{language}.yml"
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"l_{language}:"]
    for key, value in entries.items():
        raw = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        lines.append(f' {key}:0 "{raw}"')
    target.write_text("\n".join(lines) + "\n", encoding="utf-8-sig", newline="\n")
    return target


def baseline():
    data = json.loads((ROOT / "localization/source.json").read_text(encoding="utf-8"))
    assert set(data["english"]) == set(data["simp_chinese"])
    for language, entries in data.items():
        render(language, entries)
    german = json.loads((ROOT / "localization/german-authored.json").read_text(encoding="utf-8"))
    assert set(german) == set(data["english"])
    render("german", german)
    return data


def translate(language, source, reference):
    output = ROOT / f"localization/candidates/{language}.json"
    fingerprints = output.with_name(language + ".source-sha256.json")
    current_hashes = {key: hashlib.sha256(value.encode("utf-8")).hexdigest() for key, value in source.items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    candidate = {}
    if output.exists():
        old_hashes = json.loads(fingerprints.read_text(encoding="utf-8"))
        previous = json.loads(output.read_text(encoding="utf-8"))
        candidate = {k: previous[k] for k in source if k in previous and old_hashes.get(k) == current_hashes[k]}
    keys = [key for key in source if key not in candidate]
    for start in range(0, len(keys), 8):
        batch = {key: source[key] for key in keys[start:start + 8]}
        ref = {key: reference[key] for key in batch}
        prompt = translator.make_prompt("English", ("Simplified Chinese",), TARGETS[language], CONTEXT, batch, (ref,))
        _, translated = translator.request_candidate(language, TARGETS[language], prompt, batch, os.environ["MINIMAX_API_KEY"], 8000)
        candidate.update(translated)
    translator.assert_protected_tokens(source, candidate)
    output.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fingerprints.write_text(json.dumps(current_hashes, indent=2) + "\n", encoding="utf-8")
    # Caller returns raw YML escapes; render accepts decoded text.
    decoded = {key: value.replace("\\n", "\n").replace('\\"', '"') for key, value in candidate.items()}
    render(language, decoded)
    return language, len(candidate)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["baseline", "translate"])
    args = parser.parse_args()
    baseline()
    if args.command == "baseline":
        print("authored Chinese/English baselines written")
        return
    if not os.getenv("MINIMAX_API_KEY"):
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as registry:
            os.environ["MINIMAX_API_KEY"] = winreg.QueryValueEx(registry, "MINIMAX_API_KEY")[0]
    source = translator.parse_ck3_localization(ROOT / "mod/localisation/english/eep_l_english.yml")
    reference = translator.parse_ck3_localization(ROOT / "mod/localisation/simp_chinese/eep_l_simp_chinese.yml")
    with ThreadPoolExecutor(max_workers=3) as pool:
        pending = {pool.submit(translate, language, source, reference): language for language in TARGETS}
        for future in as_completed(pending):
            language, count = future.result()
            print(f"{language}: {count} protected keys", flush=True)
    evidence = {"caller": str(CALLER / "translate_localization_minimax.py"), "caller_sha256": hashlib.sha256((CALLER / "translate_localization_minimax.py").read_bytes()).hexdigest(), "languages": list(TARGETS), "runtime_scope": "l_simp_chinese only"}
    (ROOT / "docs/evidence/translation-provenance.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
