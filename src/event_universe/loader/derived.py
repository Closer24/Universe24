"""The families from the rule (ALGEBRA.md, THE FAMILIES FROM THE RULE): every key of a family's entry that the rule and the geometry fix is derived from its rank and its pair where the file leaves it out, so the universe of record holds Gamma, T, the matter pair and the two divisors; a key the file declares stands as written (the fixtures in the older form, seeded as recorded)."""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.features.counts_line import PAIRS, PORTS, PRODUCTS

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


def clock_of(value: object, entries: tuple[dict[str, Any], ...], bound: int) -> tuple[int, int]:
    """THE NODE CLOCK, an integer or a pair (GAMMA IS NOT CONSTANT, the owner's word of 2026-09-28, 15:44 Israel, a hypothesis under its own name; the Closer's order of 15:55): `node_clock` is Gamma, an integer from 1 (a constant clock, as before, bit for bit), or [Gamma_0, step], the clock at the start and its growth per interval (the step 0 a constant clock); with a step every family's pair must step with Gamma in integers (`clock_at` at the first interval), refused by name otherwise."""
    pair = [value, 0] if type(value) is int else value
    if not isinstance(pair, (list, tuple)) or len(pair) != 2 or any(type(v) is not int for v in pair):
        raise ValueError("node_clock must be an integer from 1 or [Gamma_0, step], two integers")
    gamma, step = int(pair[0]), int(pair[1])
    if not 1 <= gamma <= bound or not 0 <= step <= bound:
        raise ValueError(
            f"node_clock must be an integer from 1 through {bound}, or [Gamma_0, step] with Gamma_0 "
            f"from 1 and the step from 0, each through {bound}"
        )
    if step:
        pairs = [e["pair"] for e in paired(entries, gamma) if isinstance(e["pair"], list)]
        clock_at([(int(m), int(den)) for m, den in pairs], gamma, step, 1)
    return gamma, step


def clock_at(
    pairs: Sequence[tuple[int, int]], gamma: int, step: int, interval: int
) -> tuple[int, list[tuple[int, int]]]:
    """Gamma at an interval and every pair over it (GAMMA IS NOT CONSTANT): Gamma_t = Gamma_0 + step t, and a pair [m, Gamma_0] becomes [m Gamma_t div Gamma_0, Gamma_t], exact (at the rule's universe light steps by the step, matter by two thirds of it, the third band by minus half of it); a pair not over Gamma_0, or one whose m x step is not a multiple of Gamma_0, is refused by name. The loop's use of the clock at every interval is its own line; the constant clock (the step 0) returns the pairs as written."""
    now = gamma + step * interval
    stepped = []
    for m, den in pairs:
        if den != gamma or (m * step) % gamma:
            raise ValueError(
                f"the pair [{m}, {den}] does not step with the clock [{gamma}, {step}]: a stepping Gamma "
                "needs every pair over Gamma_0 with m x step a multiple of Gamma_0 (GAMMA IS NOT CONSTANT)"
            )
        stepped.append((m * now // gamma, now))
    return now, stepped


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


def width_bound(obj: dict[str, Any], entries: Sequence[dict[str, Any]]) -> int:
    """THE WIDTH BOUNDS A BY THE LEAST OF THE THREE (Cheshbon's line, 2026-09-28, 15:27 Israel; the Closer's ruling of 15:26): beside Rule3's total (`world.derived_amplitude`) the count's line's total, 6 Ports x 2 products x 2 pairs x w A^2 + T (most + 2) with w the common wall of a body's family (the least common multiple of the numerators of its pair and its bodies' pairs, the loop's `kind_wall`) and most the largest count declared on its bodies, and the transport's total 3 d_1 d_0 (A + 1) with the largest d of the fine and the coarse table of the file, each inside the width, as the loop checks them at the step (`features/counts_line`, `loader/world._twist_table`); the least of the two here, the least of the three at the caller; the width itself where no body and no table bounds it."""
    bodies = [b for b in obj.get("measured", ()) if isinstance(b, dict)]
    numerators: dict[str, list[int]] = {}
    for entry in entries:
        pair = entry.get("pair")
        if isinstance(pair, (list, tuple)) and len(pair) == 2 and type(pair[0]) is int and pair[0] >= 1:
            numerators[str(entry.get("name"))] = [int(pair[0])]
    found = MAX_WORK_INT
    norm = max(int(obj.get("quantum_action", 1) or 1), 1)
    for body in bodies:
        name = str(body.get("family"))
        for key in ("pair", "kind"):
            pair = body.get(key)
            if (
                isinstance(pair, (list, tuple))
                and len(pair) == 2
                and type(pair[0]) is int
                and pair[0] >= 1
            ):
                numerators.setdefault(name, []).append(int(pair[0]))
        wall = 1
        for value in numerators.get(name, [1]):
            wall = wall * value // math.gcd(wall, value)
        nodes = body.get("nodes")
        counts = (
            [int(n["count"]) for n in nodes if isinstance(n, dict)] if isinstance(nodes, list) else []
        )
        most = max([*counts, int(body.get("amount", 0) or 0), 0])
        found = min(
            found,
            math.isqrt(max(MAX_WORK_INT - norm * (most + 2), 0) // (PORTS * PRODUCTS * PAIRS * wall)),
        )
    table = obj.get("twist_table")
    if isinstance(table, dict):
        largest = [
            max((int(row[2]) for row in table.get(part, ()) if len(row) == 3), default=1)
            for part in ("fine", "coarse")
        ]
        found = min(found, MAX_WORK_INT // (3 * largest[0] * largest[1]) - 1)
    return found
