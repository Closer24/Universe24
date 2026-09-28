"""The families from the rule (ALGEBRA.md, THE FAMILIES FROM THE RULE): every key of a family's entry that the rule and the geometry fix is derived from its rank and its pair where the file leaves it out, so the universe of record holds Gamma, T, the matter pair and the two divisors; a key the file declares stands as written (the fixtures in the older form, seeded as recorded)."""

from __future__ import annotations

import math
from typing import Any

from event_universe.core.integer import MAX_WORK_INT
from event_universe.features.counts_line import PAIRS, PORTS, PRODUCTS

VACUUM_PAIR = (1, 1)  # the rule's own massless band, the band of the one real field of the highest rank


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


def filled(entry: dict[str, Any], entries: tuple[dict[str, Any], ...]) -> dict[str, Any]:
    """The entry with every absent key the rule fixes filled: the parts from the rank, the phase 2 where it carries quanta and 1 for a real field, the quantum 1, the sign 0, the self-source off, the held factors 1, and the reads: a family of quanta reads every real field (a holder of the content, at any rank, the bound band's well among them) and the clicking families of a higher rank (the holders of the sign), at the weight 1, by its own twist, by the sign where the read family holds the sign; in the rule's form (no `parts` declared) also the clicks on a family of quanta and the dipole (the spin on the content's real field, the moment on the sign's holder) with the divisor equal to the phase, where the older form's absence meant none; a declared key stands."""
    found = dict(entry)
    rule_form = "parts" not in entry
    parts = list(found.get("parts", rank_of(entry)))
    found["parts"] = parts
    quanta = carries_quanta(entry)
    found.setdefault("phase", 2 if quanta else 1)
    found.setdefault("quantum", 1)
    found.setdefault("sign", 0)
    found.setdefault("self_source", {"unit": 0})
    if rule_form and quanta and "clicks" not in found:
        found["clicks"] = {"gives": True, "takes": True, "quantum": found["quantum"]}
    if isinstance(found.get("held"), dict):
        held = dict(found["held"])
        held.setdefault("factors", [1] * len(parts))
        if rule_form and len(parts) > 1:
            held.setdefault("dipole", "spin" if held["count"] == "content" else "moment")
            held.setdefault("dipole_div", found["phase"])
        found["held"] = held
    reads: list[dict[str, Any]] = []
    if "reads" in found:
        reads = [dict(read) for read in found["reads"]]
    elif quanta:
        reads = [
            {"family": other["name"]}
            for other in entries
            if held_count(other) == "content"
            or (held_count(other) == "sign" and len(rank_of(other)) > len(parts))
        ]
    by_name = {str(other["name"]): other for other in entries}
    for read in reads:
        read.setdefault("weight", 1)
        read.setdefault("twist", "own")
        read.setdefault("by", "q" if held_count(by_name[str(read["family"])]) == "sign" else 1)
    found["reads"] = reads
    return found


def width_bound(obj: dict[str, Any], entries: tuple[dict[str, Any], ...]) -> int:
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
