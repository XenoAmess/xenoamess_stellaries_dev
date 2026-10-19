"""Reproduce the 1019 localization-only QA; no game or Steam operations."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CALLER = Path(r"D:\workspace\ck3_eternal_recurrence\tools")
GAME = Path(r"C:\SteamLibrary\steamapps\common\Stellaris")
sys.path.insert(0, str(CALLER))
import translate_localization_minimax as translator

COMPONENT_TOKEN = re.compile(r'#[^\r\n]*|"(?:\\.|[^"\\])*"|[{}=]|[^\s{}="#]+')
NATIVE_ORDER = "FLEETORDER_DESTROY_PLANET_WITH_PLANET_KILLER_CRACKER"


def planet_killer_components():
    """Project direct declaration fields for UI names; this is not P validation."""
    found = []
    for path in sorted((ROOT / "mod/common/component_templates").glob("*.txt")):
        tokens = [token for token in COMPONENT_TOKEN.findall(path.read_text(encoding="utf-8-sig"))
                  if not token.startswith("#")]
        depth = 0
        fields = {}
        for index, token in enumerate(tokens):
            if token == "{":
                depth += 1
            elif token == "}":
                depth -= 1
                if depth == 0 and fields.get("type") == "planet_killer":
                    if not fields.get("key"):
                        raise ValueError(f"Planet-killer declaration lacks key: {path}")
                    found.append({"key": fields["key"], "path": path.relative_to(ROOT).as_posix()})
                if depth == 0:
                    fields = {}
            elif depth == 1 and token in ("key", "type") and tokens[index + 1:index + 2] == ["="]:
                fields[token] = tokens[index + 2].strip('"')
    return found


def validate_planet_killer_ui(locales, components, native_tokens):
    errors = []
    for component in components:
        action = component["key"] + "_ACTION"
        order = "FLEETORDER_DESTROY_PLANET_WITH_" + component["key"]
        for language, entries in locales.items():
            for key in (action, order):
                if not entries.get(key):
                    errors.append({"language": language, "key": key,
                                   "issue": "planet_killer_derived_key_missing"})
            if order in entries and Counter(re.findall(r"\$([^$\r\n]+)\$", entries[order])) != native_tokens:
                errors.append({"language": language, "key": order,
                               "issue": "planet_killer_order_runtime_tokens"})
    return errors


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def decoded(value):
    return value.replace("\\n", "\n").replace('\\"', '"')


def rendered(value):
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def main():
    errors = []
    files = sorted((ROOT / "mod/localisation").glob("*/*.yml"))
    locales = {path.parent.name: translator.parse_ck3_localization(path) for path in files}
    english = locales["english"]
    components = planet_killer_components()
    native_file = GAME / "localisation/english/apocalypse_l_english.yml"
    native_order = re.search(r"^ " + NATIVE_ORDER + r':\d* "([^"\r\n]*)"',
                             native_file.read_text(encoding="utf-8-sig"), re.M).group(1)
    native_tokens = Counter(re.findall(r"\$([^$\r\n]+)\$", native_order))
    errors.extend(validate_planet_killer_ui(locales, components, native_tokens))
    derived_orders = {"FLEETORDER_DESTROY_PLANET_WITH_" + item["key"] for item in components}
    canonical = read_json(ROOT / "localization/source.json")
    canonical["german"] = read_json(ROOT / "localization/german-authored.json")
    candidates = sorted((ROOT / "localization/candidates").glob("*.json"))
    for path in candidates:
        if ".source-sha256." not in path.name:
            canonical[path.stem] = {key: decoded(value) for key, value in read_json(path).items()}
    source_hashes = {key: hashlib.sha256(value.encode("utf-8")).hexdigest()
                     for key, value in english.items()}
    report_languages = {}
    evolution_numbers = {}
    product_core_checks = {}
    aliases = re.compile(r"\$[^$\r\n]+\$|\[[^\[\]\r\n]+\]")
    for path in files:
        language = path.parent.name
        entries = locales[language]
        if path.read_text(encoding="utf-8-sig").splitlines()[0] != f"l_{language}:":
            errors.append({"language": language, "issue": "header"})
        if set(entries) != set(english):
            errors.append({"language": language, "issue": "key_set"})
        try:
            translator.assert_protected_tokens(english, entries)
        except translator.TranslationError as exc:
            errors.append({"language": language, "issue": str(exc)})
        evolution_numbers[language] = {}
        for evolution_key in ("eep_mothership_evolution_desc", "eep_evolution_report"):
            evolution_text = entries[evolution_key]
            checks = {"matter_per_level_10": bool(re.search(r"(?<!\d)10(?!\d)", evolution_text)),
                      "bonus_per_level_5_percent": bool(re.search(r"\+5\s*%", evolution_text)),
                      "no_deprecated_caps": not re.search(r"(?<!\d)(?:20|60|200)(?!\d)", evolution_text)}
            if evolution_key == "eep_mothership_evolution_desc":
                checks["daily_regeneration_0_1"] = bool(re.search(r"(?<!\d)0[.,]1(?!\d)", evolution_text))
            evolution_numbers[language][evolution_key] = {"checks": checks,
                "numeric_literals": re.findall(r"[+-]?\d+(?:[.,]\d+)?%?", evolution_text)}
            if not all(checks.values()):
                errors.append({"language": language, "key": evolution_key,
                               "issue": "evolution_text_number_drift", "checks": checks})
        if "eep_component_report" in entries:
            core_desc = [entries.get(f"EEP_ADAPTIVE_{kind}_CORE_DESC", "")
                         for kind in ("SHIELD", "ARMOR", "HULL", "DAMAGE", "TRACKING", "REGEN")]
            development_terms = (r"experimental|native checks|runtime checks|reload|refresh|probe|"
                r"Versuch|Prüfungen|Skalierung|rechargement|expérimental|実機|試験|"
                r"실제 게임|시험|실험|eksperymental|sprawdzenia w grze|эксперимент|проверки в игре|"
                r"pruebas en el juego|testes no jogo|待原生|待验|实验")
            component_report = entries["eep_component_report"]
            core_checks = {"six_descriptions_present": all(core_desc),
                "no_development_terms": not any(re.search(development_terms, value, re.I) for value in core_desc),
                "no_implementation_batch_limit": not re.search(r"(?<!\d)200(?!\d)|sync|synchron|同步|同期|동기화", component_report, re.I),
                "evolution_report_reference_once": entries["eep_evolution_report"].count("$eep_component_report$") == 1,
                "court_report_reference_present": "$eep_evolution_report$" in entries["eep.100.desc"],
                "nine_runtime_variables": component_report.count("[Root.") == 9,
                "five_raw_newlines": component_report.count("\\n") == 5 and "\\\\n" not in component_report,
                "section_labels_present": all(entries.get(name) and "1019" not in entries[name]
                    for name in ("eep_mothership_section", "eep_mothership_section_1019"))}
            product_core_checks[language] = core_checks
            if not all(core_checks.values()):
                errors.append({"language": language, "issue": "core_product_copy_contract", "checks": core_checks})
        for key, value in entries.items():
            if value != rendered(canonical[language][key]):
                errors.append({"language": language, "key": key, "issue": "render_drift"})
            if not value or "\ufffd" in value or re.search(r"\?{3,}", value):
                errors.append({"language": language, "key": key, "issue": "character_loss"})
            plain = aliases.sub("", value)
            if any(re.search(r"(?<![\w.])" + re.escape(candidate) + r"(?![\w.])", plain)
                   for candidate in english):
                errors.append({"language": language, "key": key, "issue": "bare_mod_key"})
            if language != "simp_chinese":
                if re.search(r"[\u3400-\u9fff]", value) and language != "japanese":
                    errors.append({"language": language, "key": key, "issue": "unexpected_cjk"})
                if value == locales["simp_chinese"][key] and re.search(r"[\u3400-\u9fff]", value):
                    errors.append({"language": language, "key": key, "issue": "chinese_fallback"})
                if language != "english" and value == english[key] and re.search(r"[A-Za-z]{4}", plain):
                    errors.append({"language": language, "key": key, "issue": "english_fallback"})
            for reference in re.findall(r"\$([^$\r\n]+)\$", value):
                if key in derived_orders and reference in native_tokens:
                    continue
                if reference in entries:
                    continue
                game_file = GAME / f"localisation/{language}/nemesis_content_l_{language}.yml"
                if not re.search(r"^ " + re.escape(reference) + r":\d* ",
                                 game_file.read_text(encoding="utf-8-sig"), re.M):
                    errors.append({"language": language, "key": key,
                                   "issue": "unresolved_reference", "reference": reference})
        report_languages[language] = {
            "keys": len(entries), "bom": path.read_bytes().startswith(b"\xef\xbb\xbf"),
            "status": "static_validation_passed", "runtime": "out_of_scope",
        }
    for path in (ROOT / "localization/candidates").glob("*.source-sha256.json"):
        if read_json(path) != source_hashes:
            errors.append({"path": path.name, "issue": "stale_english_raw_yml_fingerprint"})
    overlap_checks = 0
    for path in (ROOT / "localization").glob("*-authored.json"):
        data = read_json(path)
        if path.name == "german-authored.json":
            continue
        for language, entries in data.items():
            if language not in canonical:
                errors.append({"path": path.name, "issue": "unknown_author_locale", "language": language})
                continue
            for key, value in entries.items():
                overlap_checks += 1
                if decoded(value) != canonical[language].get(key):
                    errors.append({"path": path.name, "language": language, "key": key,
                                   "issue": "author_overlap_drift"})
    description = ROOT / "workshop/description.bbcode"
    old = subprocess.check_output(["git", "show", "HEAD:eat_everything_origin/workshop/description.bbcode"],
                                  cwd=ROOT.parent).decode("utf-8")
    extract = lambda text: re.findall(r"\[img\](.*?)\[/img\]", text)
    unchanged_images = extract(old) == extract(description.read_text(encoding="utf-8"))
    if len(extract(old)) != 4 or not unchanged_images:
        errors.append({"issue": "historical_inline_images_changed"})
    contracts = {}
    if components:
        component_key = components[0]["key"]
        for suffix, key in (("action", component_key + "_ACTION"),
                            ("order", "FLEETORDER_DESTROY_PLANET_WITH_" + component_key)):
            mutated = {"english": {name: value for name, value in english.items() if name != key}}
            contracts["reject_missing_" + suffix] = any(
                error["issue"] == "planet_killer_derived_key_missing" and error["key"] == key
                for error in validate_planet_killer_ui(mutated, components, native_tokens))
        order_key = "FLEETORDER_DESTROY_PLANET_WITH_" + component_key
        mutated = {"english": {**english, order_key: "Preparing to dismantle $PLANET$"}}
        contracts["reject_changed_planet_token"] = any(
            error["issue"] == "planet_killer_order_runtime_tokens"
            for error in validate_planet_killer_ui(mutated, components, native_tokens))
    if not contracts or not all(contracts.values()):
        errors.append({"issue": "planet_killer_qa_contract_failed", "checks": contracts})
    tracked = files + sorted((ROOT / "localization").rglob("*.json"))
    tracked += [ROOT / "README.md", description, Path(__file__)]
    tracked += sorted((ROOT / "mod/common/component_templates").glob("*.txt"))
    evidence = {
        "schema": "eep-1019-localization-static-v1",
        "status": "PASS" if not errors else "FAIL",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "version": (ROOT / "VERSION").read_text().strip(),
        "scope": "Localization and candidate copy only; no open_kaishek or runtime verdict",
        "non_chinese_result": "静态校验通过；运行时不在范围内" if not errors else "静态校验失败",
        "languages": report_languages,
        "author_overlap_checks": overlap_checks,
        "evolution_text_numbers": evolution_numbers,
        "core_product_copy": product_core_checks,
        "planet_killer_ui": {"components": components, "native_order": native_order,
                             "native_tokens": dict(native_tokens), "contracts": contracts,
                             "native_source": {"path": str(native_file),
                                               "sha256": hashlib.sha256(native_file.read_bytes()).hexdigest()}},
        "historical_inline_images": {"count": 4, "unchanged": unchanged_images},
        "protected_token_parser": {"path": str(CALLER / "translate_localization_minimax.py"),
                                   "sha256": hashlib.sha256((CALLER / "translate_localization_minimax.py").read_bytes()).hexdigest()},
        "files": [{"path": path.relative_to(ROOT).as_posix(),
                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in tracked],
        "notes": ["Japanese uses shared Han characters; its remaining Han-only labels were manually reviewed as Japanese.",
                  "Catches exact English/Chinese fallback, unexpected CJK outside Japanese, bare Mod keys, and character loss.",
                  "Does not certify linguistic fluency or any new gameplay semantics."],
        "errors": errors,
    }
    output = Path(__file__).with_name(f"static-qa-{len(english)}.json")
    output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": evidence["status"], "languages": len(locales),
                      "keys_per_language": len(english), "overlap_checks": overlap_checks,
                      "errors": errors}, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
