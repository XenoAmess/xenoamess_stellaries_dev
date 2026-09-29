"""Read-only audit of reward selection, guards, weights, and vanilla candidates."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from audit_compat_traits import block
from generate_rewards import OTHER, OUTPUT, ROBOTIC, compatible_name, condition


Pair = tuple[str, str | list["Pair"]]
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=#]+')


def parse(source: str) -> list[Pair]:
    tokens = [token for token in TOKENS.findall(source) if not token.startswith("#")]
    position = 0

    def entries(nested: bool = False) -> list[Pair]:
        nonlocal position
        result: list[Pair] = []
        while position < len(tokens):
            if tokens[position] == "}":
                if not nested:
                    raise ValueError("unexpected closing brace")
                position += 1
                return result
            key = tokens[position]
            if position + 1 >= len(tokens) or tokens[position + 1] != "=":
                raise ValueError(f"expected assignment after {key!r}")
            position += 2
            if position >= len(tokens):
                raise ValueError(f"missing value for {key!r}")
            if tokens[position] == "{":
                position += 1
                value: str | list[Pair] = entries(True)
            else:
                value = tokens[position]
                position += 1
            result.append((key, value))
        if nested:
            raise ValueError("unclosed block")
        return result

    return entries()


def exactly(pairs: list[Pair], key: str) -> str | list[Pair]:
    values = [value for name, value in pairs if name == key]
    if len(values) != 1:
        raise AssertionError(f"expected exactly one {key}, got {len(values)}")
    return values[0]


def obj(value: str | list[Pair]) -> list[Pair]:
    if not isinstance(value, list):
        raise AssertionError(f"expected block, got {value!r}")
    return value


def reward_trait(item: list[Pair], expected: str) -> None:
    assert [key for key, _ in item] == ["owner_main_species"], item
    species = obj(exactly(item, "owner_main_species"))
    assert [key for key, _ in species] == ["change_species_characteristics"]
    changes = obj(exactly(species, "change_species_characteristics"))
    assert changes == [("add_trait", expected)], (expected, changes)


def audit_pool(branch: list[Pair], items: list[tuple[str, list[str], bool, bool]], compatible: bool) -> None:
    assert [key for key, _ in branch] == ["limit", "random_list"]
    limits = obj(exactly(obj(exactly(branch, "limit")), "OR"))
    draws = obj(exactly(branch, "random_list"))
    assert len(limits) == len(draws) == len(items), (len(limits), len(draws), len(items))
    expected_names = [compatible_name(item[0]) if compatible else item[0] for item in items]
    assert len(expected_names) == len(set(expected_names))
    for index, (entry, limit, draw) in enumerate(zip(items, limits, draws, strict=True)):
        expected_guard = parse(condition(entry, compatible))
        assert limit == ("AND", expected_guard), (index, limit)
        assert draw[0] == "1", (index, draw[0])
        draw_body = obj(draw[1])
        assert [key for key, _ in draw_body] == ["modifier", "owner_main_species"]
        modifier = obj(exactly(draw_body, "modifier"))
        assert modifier == [("factor", "0"), ("NOT", expected_guard)], (index, modifier)
        reward_trait(draw_body[1:], expected_names[index])


def audit_iteration(branch: list[Pair]) -> None:
    assert [key for key, _ in branch] == ["random_list"]
    draws = obj(exactly(branch, "random_list"))
    suffixes = ("output", "energy", "assembly", "experience")
    assert len(draws) == len(suffixes)
    for (weight, value), suffix in zip(draws, suffixes, strict=True):
        assert weight == "1"
        body = obj(value)
        assert [key for key, _ in body] == ["change_variable", "owner_main_species"]
        assert obj(exactly(body, "change_variable")) == [
            ("which", f"shishan_code_iteration_{suffix}"),
            ("value", "1"),
        ]
        reward_trait(body[1:], f"trait_shishan_iteration_{suffix}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", required=True, type=Path)
    args = parser.parse_args()
    effects = parse(OUTPUT.read_text(encoding="utf-8"))
    reward = obj(exactly(effects, "shishan_code_award_reward"))
    assert [key for key, _ in reward] == ["if", "else_if", "else"]
    audit_pool(obj(reward[0][1]), ROBOTIC, False)
    audit_pool(obj(reward[1][1]), OTHER, True)
    audit_iteration(obj(reward[2][1]))
    vanilla = (args.game / "common/traits/05_species_traits_robotic.txt").read_text(encoding="utf-8-sig")
    for name, *_ in ROBOTIC:
        definition = block(vanilla, name)
        # Vanilla archetypes and tags are bare tokens, unlike effect assignments.
        assert re.search(r"allowed_archetypes\s*=\s*\{\s*ROBOT\s+MACHINE\s*\}", definition), name
        assert re.search(r"tags\s*=\s*\{[^}]*\bpositive\b", definition), name
    print(f"reward contract: PASS ({len(ROBOTIC)} robotic, {len(OTHER)} compatible, 4 iterative)")


if __name__ == "__main__":
    main()
