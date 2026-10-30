"""A composite of three parts clicking in a window: which split click is exact and sends no signal, in exact fractions.

David's probe for the owner's word to David of 2026-10-29, 09:3x UTC ("Try to close the clicks from the tensors,
from the 24 and from the clocks, to get a future with complex clocks, more and more"). A complex clock is a composite
of several parts, so its split click is the case l5 opened: a closure at finite speed, three parts, two of them in
each other's window.

usage: python3 -I composite_window.py

Two composites of three twins, each part read along Z or X (whole-number amplitudes, exact odds):
  GHZ, (|000> + |111>) / sqrt 2, and W, (|001> + |010> + |100>) / sqrt 3.
The parts click in the board's order A, B, C. A closure carries a part's outcome and setting along the Meshes; a later
part holds it or not when it clicks. Four timings: every closure arrives; B and C in each other's window (B's never
reaches C); A and B in each other's window (A's never reaches B); every part in every other's window.
Rules for a part's draw:
  R1, on one board, the closure as written: condition on the outcomes that arrived (quantum odds given exactly them);
  R2, on one board, the last part alone: condition only when holding every other part's closure, else the marginal;
  R3, on one board, no closure: every part draws its own marginal;
  Z, two boards: each part's setting rides back along its own worldline to the birth (two_boards.py, part 2), and the
     composite's split is drawn there once, d over a full turn of L = SUM of the joint sizes, by the rank count; each
     outcome rides out to its part. The joint sizes are the whole-number overlaps squared, so Z's exactness is the
     draw's (each outcome drawn exactly its size times a turn), and the timing does not enter: the settings reach the
     birth on the backward board whichever part clicks first.
Each rule's joint law is computed exactly at every setting (Z's by enumerating its draw), and read two ways:
  exact, the joint law equal to quantum mechanics' at every setting;
  no signal, every single and every pair's law the same whatever the remaining part's setting.
"""

from fractions import Fraction
from itertools import product

SQ = {
    0: (1, 0, 0, 1),
    1: (1, 1, 1, -1),
}  # Z and X bases as 2 x 2 whole-number columns: Z = I, X = H times sqrt 2


def nonneg(n: int) -> int:
    """The one whether: 1 where n is at least 0 and 0 below."""
    return n // (n * n + 1) + 1


def drawn(n: int, sizes: list[int]) -> int:
    """The rank count: the part whose cumulative interval holds d = n mod L, with no sort and no if."""
    total = sum(sizes)
    d = n % total
    part, run = 0, 0
    for s in sizes[:-1]:
        run += s
        part += nonneg(d - run)
    return part


def birth_draw(state: list[int], settings: tuple[int, ...]) -> dict[tuple[int, ...], Fraction]:
    """Two boards: the composite's split drawn once at the birth over a full turn of its joint sizes, enumerated."""
    outcomes = list(product((0, 1), repeat=3))
    sizes = [amplitude(state, settings, o) ** 2 for o in outcomes]
    counts = [0] * len(outcomes)
    for n in range(sum(sizes)):
        counts[drawn(n, sizes)] += 1
    assert counts == sizes, (settings, counts, sizes)
    return {o: Fraction(c, sum(counts)) for o, c in zip(outcomes, counts, strict=True)}


def amplitude(state: list[int], settings: tuple[int, ...], outcome: tuple[int, ...]) -> int:
    """The whole-number overlap of the outcome's basis vectors with the state (each X column unnormalized by sqrt 2)."""
    total = 0
    for index, coefficient in enumerate(state):
        if coefficient == 0:
            continue
        bits = [(index >> (2 - j)) & 1 for j in range(3)]
        term = coefficient
        for j in range(3):
            term *= SQ[settings[j]][
                2 * bits[j] + outcome[j]
            ]  # outcome 0 the first basis vector, 1 the second
        total += term
    return total


def quantum(state: list[int], settings: tuple[int, ...]) -> dict[tuple[int, ...], Fraction]:
    """Quantum mechanics' joint law of the three outcomes, exact."""
    weights = {o: amplitude(state, settings, o) ** 2 for o in product((0, 1), repeat=3)}
    total = sum(weights.values())
    return {o: Fraction(w, total) for o, w in weights.items()}


def conditional(law: dict, who: int, known: dict[int, int]) -> dict[int, Fraction]:
    """The law of part `who`'s outcome given the outcomes in `known`, from a joint law."""
    match = {o: p for o, p in law.items() if all(o[j] == v for j, v in known.items())}
    total = sum(match.values())
    out = {0: Fraction(0), 1: Fraction(0)}
    for o, p in match.items():
        out[o[who]] += Fraction(p, total) if total else Fraction(0)
    return out


def run_rule(state: list[int], settings: tuple[int, ...], held: dict[int, set[int]], rule: str) -> dict:
    """The joint law a rule gives: parts draw in the order A, B, C, each from what it holds."""
    if rule == "Z":
        return birth_draw(state, settings)
    law_q = quantum(state, settings)
    joint: dict[tuple[int, ...], Fraction] = {}
    for outcome in product((0, 1), repeat=3):
        p = Fraction(1)
        for who in range(3):
            have = held[who]
            if rule == "R1":
                known = {j: outcome[j] for j in have}
            elif rule == "R2":
                known = {j: outcome[j] for j in have} if len(have) == 2 else {}
            else:
                known = {}
            p *= conditional(law_q, who, known)[outcome[who]]
        joint[outcome] = p
    return joint


TIMINGS = {
    "every closure arrives": {0: set(), 1: {0}, 2: {0, 1}},
    "B and C in each other's window": {0: set(), 1: {0}, 2: {0}},
    "A and B in each other's window": {0: set(), 1: set(), 2: {0, 1}},
    "every part in every other's window": {0: set(), 1: set(), 2: set()},
}
STATES = {"GHZ": [1, 0, 0, 0, 0, 0, 0, 1], "W": [0, 1, 1, 0, 1, 0, 0, 0]}


def marginal(law: dict, parts: tuple[int, ...]) -> dict:
    out: dict[tuple[int, ...], Fraction] = {}
    for o, p in law.items():
        key = tuple(o[j] for j in parts)
        out[key] = out.get(key, Fraction(0)) + p
    return out


def signals(state: list[int], held: dict[int, set[int]], rule: str) -> Fraction:
    """The largest move of any single's or pair's law when the remaining part's setting alone changes."""
    worst = Fraction(0)
    for subset in ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2)):
        others = [j for j in range(3) if j not in subset]
        for fixed in product((0, 1), repeat=len(subset)):
            laws = []
            for free in product((0, 1), repeat=len(others)):
                settings = [0, 0, 0]
                for j, v in zip(subset, fixed, strict=True):
                    settings[j] = v
                for j, v in zip(others, free, strict=True):
                    settings[j] = v
                laws.append(marginal(run_rule(state, tuple(settings), held, rule), subset))
            for la in laws:
                for lb in laws:
                    for key in la:
                        worst = max(worst, abs(la[key] - lb[key]))
    return worst


def departs(state: list[int], held: dict[int, set[int]], rule: str) -> Fraction:
    """The largest gap between the rule's joint law and quantum mechanics', over every setting and outcome."""
    worst = Fraction(0)
    for settings in product((0, 1), repeat=3):
        q = quantum(state, settings)
        r = run_rule(state, settings, held, rule)
        for o in q:
            worst = max(worst, abs(q[o] - r[o]))
    return worst


def main() -> None:
    lines = ["A composite of three parts clicking in a window (David, 2026-10-29): exact fractions", ""]
    clean: dict[str, int] = {rule: 0 for rule in ("R1", "R2", "R3", "Z")}
    for name, state in STATES.items():
        lines.append(
            f"{name}: per timing, each rule's largest gap from quantum mechanics, and its largest signal"
        )
        for timing, held in TIMINGS.items():
            row = []
            for rule in clean:
                gap, signal = departs(state, held, rule), signals(state, held, rule)
                clean[rule] += nonneg(-gap) * nonneg(-signal)
                row.append(f"{rule} gap {gap}, signal {signal}")
            lines.append(f"  {timing}: " + "; ".join(row))
        lines.append("")
    cases = len(STATES) * len(TIMINGS)
    lines.append(f"exact and with no signal, of {cases} cases (two composites, four timings):")
    lines.append("  " + "; ".join(f"{rule} {n}" for rule, n in clean.items()))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
