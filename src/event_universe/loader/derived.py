"""The families from the rule (ALGEBRA.md, THE FAMILIES FROM THE RULE): every key of a family's entry that the rule and the geometry fix is derived from its rank and its pair where the file leaves it out, so the universe of record holds Gamma, T, the matter pair and the two divisors; a key the file declares stands as written (the fixtures in the older form, seeded as recorded)."""

from __future__ import annotations

import json
import math
from typing import Any

VACUUM_PAIR = (1, 1)  # the rule's own massless band, the band of the one real field of the highest rank


def pair_of(entry: dict[str, Any], gamma: int, label: str) -> list[int] | str:
    """THE MASS IS ONE INTEGER (the owner, 2026-09-28): a family's pair is written over the lattice's denominator Gamma, the file holding the numerator `m` alone, cos omega_0 = m / Gamma, and the loader writes the pair [m, Gamma] as it stands (THE WALL IS ONE: the wall 6 Gamma^3 for every family, the pair in the coefficients as written; light m = Gamma, the exact band m = Gamma div 2, the band read by `reduced`); a row declaring both `m` and `pair` is refused by name, and a row with neither lacks its pair."""
    if "m" in entry and "pair" in entry:
        raise ValueError(
            f"{label} declares both m and pair: the pair is [m, Gamma] as it stands, one form"
        )
    if "m" not in entry:
        if "pair" not in entry:
            raise ValueError(
                f"{label} lacks keys: m (the family's numerator over Gamma; THE MASS IS ONE INTEGER)"
            )
        pair = entry["pair"]
        return "body" if pair == "body" else [int(pair[0]), int(pair[1])]
    m = int(entry["m"])
    if not 1 <= m <= gamma:
        raise ValueError(
            f"{label}.m {m} is not from 1 to Gamma = {gamma}: cos omega_0 = m / Gamma lies in (0, 1]"
        )
    return [m, gamma]


def paired(entries: tuple[dict[str, Any], ...], gamma: int) -> list[dict[str, Any]]:
    """Every entry with its pair filled from `m` where the file wrote the numerator alone (the amplitude bound reads the pairs)."""
    return [
        {**entry, "pair": pair_of(entry, gamma, f"the family {entry.get('name')!r}")}
        for entry in entries
    ]


def held_count(entry: dict[str, Any]) -> str | None:
    """The count a family holds ("content" or "sign"), None where it holds none."""
    held = entry.get("held")
    return None if not isinstance(held, dict) else str(held["count"])


def rank_of(entry: dict[str, Any]) -> tuple[int, ...]:
    """The parts of a family from what writes it: the count, the current and the current's tensor for the real field of the vacuum's band holding the content; the count and the current for the holder of the sign; the count alone otherwise (the bound band [1, 2] holding the content, and every family of quanta)."""
    count = held_count(entry)
    if count == "sign":
        return (1, 3)
    if count == "content" and reduced(entry["pair"]) == VACUUM_PAIR:
        return (1, 3, 6)
    return (1,)


def reduced(pair: object) -> tuple[int, ...]:
    """A pair in lowest terms, the band it names (THE MASS IS ONE INTEGER: [m, Gamma] is the band [m div g, Gamma div g]); the word "body" as it is; the coefficients stay on the pair as written, whose wall sets the amplitude unit."""
    if not isinstance(pair, (list, tuple)):
        return (0,)
    num, den = int(pair[0]), int(pair[1])
    divisor = math.gcd(num, den) or 1
    return (num // divisor, den // divisor)


def carries_quanta(entry: dict[str, Any]) -> bool:
    """Whether the family carries quanta (a pair of levels, the clicks): every family but the real fields, the holders of the content."""
    return held_count(entry) != "content"


RULED = (
    "parts",
    "phase",
    "quantum",
    "clicks",
    "reads",
)  # the keys the rule fixes; declared against it, refused
HELD_RULED = ("factors", "dipole", "dipole_div")  # the held row's keys the rule fixes
CLICKS = {"gives": True, "takes": True, "quantum": 1}  # a family of quanta gives and takes one quantum


def contradiction(label: str, key: str, declared: object, fixed: object) -> ValueError:
    """The refusal by name of a key declared against the rule (THE FAMILIES FROM THE RULE): the key leaves the files, the rule fixes it."""
    shown = (
        json.loads(json.dumps(declared)),
        json.loads(json.dumps(fixed)),
    )  # the frame's tuples as lists
    return ValueError(
        f"{label}.{key} {shown[0]!r} contradicts the rule, which fixes {shown[1]!r} from the rank and "
        "the pair (THE FAMILIES FROM THE RULE: the key leaves the files)"
    )


def reads_of(parts: list[int], entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The reads of a family of quanta of rank `parts`: every real field (a holder of the content, at any rank) and the clicking families of a higher rank (the holders of the sign, by q), at the weight 1, by its own twist, in the file's order."""
    return [
        {
            "family": other["name"],
            "weight": 1,
            "twist": "own",
            "by": "q" if held_count(other) == "sign" else 1,
        }
        for other in entries
        if held_count(other) == "content"
        or (held_count(other) == "sign" and len(rank_of(other)) > len(parts))
    ]


def filled(
    entry: dict[str, Any], entries: tuple[dict[str, Any], ...], gamma: int, label: str = "the family"
) -> dict[str, Any]:
    """The entry with every key the rule fixes filled from its rank and its pair: the parts from the rank, the phase 2 where it carries quanta and 1 for a real field, the quantum 1, the clicks on a family of quanta and none on a real field, the reads (`reads_of`), the held factors 1 and the dipole (the spin on the content's real field, the moment on the sign's holder) with the divisor equal to the phase; a key declared at another value is refused by name (`contradiction`), a key declared at the rule's value stands; the sign (0) and the self-source (off) are filled where absent and stand where declared until the owner's word on a body's charge and on the slot."""
    found = {k: v for k, v in entry.items() if k not in RULED}
    found["pair"] = pair_of(entry, gamma, label)
    found.pop("m", None)
    with_pairs = paired(entries, gamma)
    parts = list(rank_of(found))
    quanta = carries_quanta(found)
    rule: dict[str, Any] = {"parts": parts, "phase": 2 if quanta else 1, "quantum": 1}
    rule["reads"] = reads_of(parts, with_pairs) if quanta else []
    if quanta:
        rule["clicks"] = CLICKS
    elif "clicks" in entry:
        raise contradiction(label, "clicks", entry["clicks"], None)
    declared = dict(entry)
    if "reads" in declared:
        by_name = {str(other["name"]): other for other in with_pairs}
        declared["reads"] = [
            {
                "weight": 1,
                "twist": "own",
                "by": "q" if held_count(by_name.get(str(r["family"]), {})) == "sign" else 1,
                **r,
            }
            for r in declared["reads"]
        ]
    for key, value in rule.items():
        if key in declared and declared[key] != value:
            raise contradiction(label, key, entry[key], value)
    found.update(rule)
    found.setdefault("sign", 0)
    found.setdefault("self_source", {"unit": 0})
    if isinstance(found.get("held"), dict):
        held = {k: v for k, v in found["held"].items() if k not in HELD_RULED}
        held["factors"] = [1] * len(parts)
        if len(parts) > 1:
            held["dipole"] = "spin" if held["count"] == "content" else "moment"
            held["dipole_div"] = rule["phase"]
        for key in HELD_RULED:
            if key in entry["held"] and entry["held"][key] != held.get(key):
                raise contradiction(f"{label}.held", key, entry["held"][key], held.get(key))
        found["held"] = held
    return found
