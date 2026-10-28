"""Toy: the chosen path carried into the next bang (Animate; the owner's word of 2026-10-28, 15:4x UTC: "a detector's
click chooses one path for the future; in the next bang I want it to influence it; that the path it chose does not
disappear, that it influences it").

One Node-clock across many bangs, in clocks:
  - each bang a fresh twin child comes to the clock (a fitting's child);
  - the detector's click (law 6) picks its direction along the detector's axis m, with the shares (1 + s . m) / 2 and
    (1 - s . m) / 2, s the child's own spin (0 for a singlet's child), by the board's draw (here a fixed stream of fair
    digits, the vernier's stand-in);
  - what the click wrote is a twin pair with a definite direction: the record;
  - the turnover is T on every gear: the record's direction reverses (S to -S);
  - law 6's detector is "a second twin pair at the Node-clock": where a record stands, it is the next click's detector,
    its axis m; where none stands, the bang's own frame, the light's lead axis there, one of the three axes by the draw.
The directions are the 24's six axis directions, integers. Four rules for what crosses into the next bang:
  rewound      the exact rewind undoes every click: each bang starts with no record (law 3 as the board's own act);
  axis         way 2: the record stands through the turnover, reversed, and is the next detector; the child a singlet's
               (s = 0): the axis carries, the sign is drawn afresh;
  choice       as axis, and the record bends the light's lead through the spin's coupling to the current (S . J,
               item 5), so the next child is laid along the lead (law C, the kind kept): s = the reversed record;
  half         as choice, with the child laid half along the lead: shares (2 +- s . m) / 4;
  mutant       as half, with the contraction read on the z parts alone (an axis typed), which must part the 24.
The 24: the same draws with every frame turned by each of the 24 turns; a generic law turns every choice with them.
Read over 4,096 bangs: how often the next bang's axis is the last record's line, how often its choice is the last
choice reversed, and the share of fresh draws.
"""

BANGS = 4096
AXES = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]


def digits():
    """A fixed stream of fair bits: the binary digits of a linear congruential walk (the vernier's stand-in)."""
    x = 2026
    while True:
        x = (1103515245 * x + 12345) % (1 << 31)
        yield (x >> 16) & 1


def dot(a, b):
    return sum(p * q for p, q in zip(a, b, strict=True))


def neg(a):
    return tuple(-p for p in a)


def share_up(s, m, rule):
    """The up share of the click along m, out of its weight: the A1 contraction of the child's spin s with the detector's
    axis m (law 6: (rho rho_d + S . S_d) / (2 rho rho_d) at rho = rho_d = 1), the child's spin whole (out of 2) or at
    half its length (out of 4); the mutant reads the z parts alone, an axis typed."""
    contraction = s[2] * m[2] if rule == "mutant" else dot(s, m)
    weight = 4 if rule in ("half", "mutant") else 2
    return weight, weight // 2 + contraction


def run(rule, turn=None):
    """The run under a rule; with `turn`, every frame the draw gives is turned by it (a 3 x 3 signed permutation of
    determinant 1, one of the 24), and the choices are returned for the covariance check."""
    bits = digits()
    record = None
    same_line, reversed_choice, drawn = 0, 0, 0
    last, choices = None, []
    for _ in range(BANGS):
        # the detector: the record where one stands, else the bang's own frame, the light's lead axis there, which
        # turns from bang to bang (drawn from the same stream: one of the three axes)
        if record is not None:
            m = record
        else:
            pick = 3
            while pick == 3:
                pick = 2 * next(bits) + next(bits)
            m = AXES[pick] if turn is None else apply(turn, AXES[pick])
        if rule in ("choice", "half", "mutant") and record is not None:
            s = record  # the child laid along the lead the record bent (S . J and law C)
        else:
            s = (0, 0, 0)  # a singlet's child
        weight, up_share = share_up(s, m, rule)
        if 0 < up_share < weight:
            drawn += 1
            value = next(bits) if weight == 2 else 2 * next(bits) + next(bits)
            up = value < up_share
        else:
            up = up_share == weight
        choice = m if up else neg(m)
        if last is not None:
            same_line += abs(dot(choice, last)) == 1
            reversed_choice += choice == neg(last)
        last = choice
        choices.append(choice)
        # the turnover: T reverses every gear's spin; the rewound rule undoes the click from its log
        record = None if rule == "rewound" else neg(choice)
    pairs = BANGS - 1
    return same_line, reversed_choice, drawn, pairs, choices


def apply(turn, v):
    return tuple(sum(turn[i][j] * v[j] for j in range(3)) for i in range(3))


def turns():
    """The 24 turns of the cube as 3 x 3 signed permutation matrices of determinant 1."""
    from itertools import permutations, product

    found = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i, j in enumerate(perm):
                m[i][j] = signs[i]
            det = (
                m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
            )
            if det == 1:
                found.append(m)
    return found


def main():
    print(
        f"one Node-clock over {BANGS} bangs; the detector the last record, or the bang's own lead axis"
    )
    for rule in ("rewound", "axis", "choice", "half"):
        same_line, reversed_choice, drawn, pairs, _ = run(rule)
        print(
            f"  {rule:8s}: the next choice on the last choice's line {same_line} of {pairs}; "
            f"the last choice reversed {reversed_choice} of {pairs}; fresh draws {drawn} of {BANGS}"
        )
    print(
        "the 24: every frame the draw gives turned by each turn R; the law keeps the 24 where the choices turn by R"
    )
    every = turns()
    for rule in ("rewound", "axis", "choice", "half", "mutant"):
        base = run(rule)[4]
        parted = [turn for turn in every if run(rule, turn)[4] != [apply(turn, c) for c in base]]
        print(
            f"  {rule:8s}: the choices turned by R under {len(every) - len(parted)} of {len(every)} turns"
        )
        if parted:
            line = tuple(abs(p) for p in base[0])
            moved = sum(abs(apply(turn, line)[2]) != line[2] for turn in parted)
            print(
                f"            it parts at {len(parted)} turns; {moved} of them carry the run's line {line} onto the z "
                "line or off it"
            )


if __name__ == "__main__":
    main()
