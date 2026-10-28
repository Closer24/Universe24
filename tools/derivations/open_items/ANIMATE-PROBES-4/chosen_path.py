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
  half         as choice, with the child laid half along the lead: shares (2 +- s . m) / 4.
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


def run(rule):
    bits = digits()
    record = None
    same_line, reversed_choice, drawn = 0, 0, 0
    last = None
    for _ in range(BANGS):
        # the detector: the record where one stands, else the bang's own frame, the light's lead axis there, which
        # turns from bang to bang (drawn from the same stream: one of the three axes)
        if record is not None:
            m = record
        else:
            pick = 3
            while pick == 3:
                pick = 2 * next(bits) + next(bits)
            m = AXES[pick]
        if rule in ("choice", "half") and record is not None:
            s = record  # the child laid along the lead the record bent
        else:
            s = (0, 0, 0)  # a singlet's child
        weight = 2 if rule != "half" else 4
        up_share = (weight // 2) * (1 + dot(s, m)) if rule != "half" else 2 + dot(s, m)
        # the click: up with up_share of weight, by the draw where both shares are not 0
        if 0 < up_share < weight:
            drawn += 1
            # a fair draw of up_share out of weight from the bits (weight 2 or 4)
            value = next(bits) if weight == 2 else 2 * next(bits) + next(bits)
            up = value < up_share
        else:
            up = up_share == weight
        choice = m if up else neg(m)
        if last is not None:
            same_line += abs(dot(choice, last)) == 1
            reversed_choice += choice == neg(last)
        last = choice
        record = choice
        # the turnover: T reverses every gear's spin; the rewound rule undoes the click from its log
        record = None if rule == "rewound" else neg(record)
    pairs = BANGS - 1
    return same_line, reversed_choice, drawn, pairs


def main():
    print(
        f"one Node-clock over {BANGS} bangs; the detector the last record, or the bang's own lead axis"
    )
    for rule in ("rewound", "axis", "choice", "half"):
        same_line, reversed_choice, drawn, pairs = run(rule)
        print(
            f"  {rule:8s}: the next choice on the last choice's line {same_line} of {pairs}; "
            f"the last choice reversed {reversed_choice} of {pairs}; fresh draws {drawn} of {BANGS}"
        )


if __name__ == "__main__":
    main()
