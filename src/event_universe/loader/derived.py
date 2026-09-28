"""The families from the rule (ALGEBRA.md, THE FAMILIES FROM THE RULE): every key of a family's entry that the rule and the geometry fix is derived from its rank and its pair where the file leaves it out, so the universe of record holds Gamma, T, the matter pair and the two divisors; a key the file declares stands as written (the fixtures in the older form, seeded as recorded)."""

from __future__ import annotations

from typing import Any

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
    if count == "content" and tuple(entry["pair"]) == VACUUM_PAIR:
        return (1, 3, 6)
    return (1,)


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
