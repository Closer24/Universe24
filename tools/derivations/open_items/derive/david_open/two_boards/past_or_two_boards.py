"""The past alone, or two boards: which keeps the clicks going and the clocks growing, in exact fractions.

David's probe for the owner's word to David of 2026-10-29, 08:52 UTC ("The future must be rich by the clicks... the
clicks' continuity must be shown, and the two kinds explained... check whether the past makes ever more complex
clocks because of the big bang, the old theory, or the two boards, where looking back one also sees one bang in the
clicks, but they swing and so advance in complexity").

usage: python3 -I past_or_two_boards.py

A toy of the logic, not the act. The depth k = 0 to K is how deep the board's composite clocks are bound, K the room
(the cap). Each step is one split click among three parts, with forward sizes from the past:
  bind  (k to k + 1): (K - k)(H - h), free room on a cool board;
  break (k to k - 1): k h, the heat breaking the weakly bound;
  stay  (k to k):     K H.
h is the heat: the swing's (H at each bang, 0 at the top), or the old theory's (one bang, then cooling for ever).
The whole clicks of composites that each step writes, the interesting clicks, number k f, with f = h (H - h) the flow
between hot and cold: a board at one temperature carries none.
Four histories, each from the same first bang (k = 0, h = H):
  A, the old theory: one bang, then cooling for ever, forward only;
  B1, the swing, forward only (a silent future);
  B2, the swing with two boards: at the last bang the future weighs each depth by the clicks it will make, 1 + c k,
      the backward board carries that weight back step by step, and each split is drawn by its forward size times the
      backward weight of the side it leads to (the product draw of two_boards.py, part 1);
  B3, the swing on one board with records: the depth M a composite has reached is kept in the record and passes
      every bang, and binding again below M is REBIND + 1 times as easy (heredity, forward only).
Each history's law is computed exactly: the forward weights from the past, the backward weights from the future, and
the step's law their product (Aharonov, Bergmann and Lebowitz's rule, a Markov chain weighed by its far end).
"""

from fractions import Fraction

K, H, T, C = (
    10,
    4,
    8,
    8,
)  # the room, the heat's top, the steps of one swing (its bang at step 0), the swings
GENTLE = 2  # a gentler bang's heat, for the memory that passes it


def swing_heat(step: int) -> int:
    """The swing: H at its bang (step 0 of each swing), falling to 0 at the top, rising toward the next bang."""
    t = step % T
    return abs(H - t)


def gentle_heat(step: int) -> int:
    """The same swing with a gentler bang: the heat held at most GENTLE, so more of the bound passes each bang."""
    return min(GENTLE, swing_heat(step))


def cooling_heat(step: int) -> int:
    """The old theory: one bang at step 0, then the board cools and stays cold."""
    return max(0, H - step)


def sizes(k: int, h: int) -> dict[int, int]:
    """The split's forward sizes from depth k at heat h: the depth each part leads to, and its size."""
    out = {k: K * H}
    if k < K:
        out[k + 1] = (K - k) * (H - h)
    if k > 0:
        out[k - 1] = k * h
    return out


def forward(heat, steps: int) -> list[list[Fraction]]:
    """The past's law at every step: the first bang at depth 0, each split drawn by its forward sizes."""
    law = [[Fraction(0)] * (K + 1) for _ in range(steps + 1)]
    law[0][0] = Fraction(1)
    for s in range(steps):
        h = heat(s)
        for k, p in enumerate(law[s]):
            if p:
                parts = sizes(k, h)
                total = sum(parts.values())
                for k2, size in parts.items():
                    law[s + 1][k2] += p * Fraction(size, total)
    return law


def backward(heat, steps: int, weight: list[int]) -> list[list[Fraction]]:
    """The future's weight at every step: at the last bang the given weight, carried back through the forward sizes."""
    back = [[Fraction(0)] * (K + 1) for _ in range(steps + 1)]
    back[steps] = [Fraction(w) for w in weight]
    for s in range(steps - 1, -1, -1):
        h = heat(s)
        for k in range(K + 1):
            parts = sizes(k, h)
            total = sum(parts.values())
            back[s][k] = sum(Fraction(size, total) * back[s + 1][k2] for k2, size in parts.items())
    return back


def met(fwd: list[list[Fraction]], bwd: list[list[Fraction]]) -> list[list[Fraction]]:
    """The two boards' law at every step: the past's law times the future's weight, normalized."""
    out = []
    for a, b in zip(fwd, bwd, strict=True):
        prod = [x * y for x, y in zip(a, b, strict=True)]
        total = sum(prod)
        out.append([x / total for x in prod])
    return out


def mean(law: list[Fraction]) -> Fraction:
    return sum(k * p for k, p in enumerate(law))


def flow(h: int) -> int:
    return h * (H - h)


def per_swing(law: list[list[Fraction]], heat) -> list[Fraction]:
    """The interesting clicks each swing writes."""
    return [sum(mean(law[s]) * flow(heat(s)) for s in range(n * T, (n + 1) * T)) for n in range(C)]


def report(name: str, law: list[list[Fraction]], heat) -> list[str]:
    """Per swing: the interesting clicks it writes and the depth at its top."""
    out = [name]
    clicks_per_swing, tops = [], []
    for n in range(C):
        steps = range(n * T, (n + 1) * T)
        clicks = sum(mean(law[s]) * flow(heat(s)) for s in steps)
        clicks_per_swing.append(clicks)
        tops.append(mean(law[n * T + T // 2]))
    out.append(
        "  interesting clicks per swing: " + ", ".join(f"{float(c):.2f}" for c in clicks_per_swing)
    )
    out.append("  depth at each swing's top:    " + ", ".join(f"{float(t):.2f}" for t in tops))
    return out


REBIND = 3  # a remembered bond rebinds REBIND + 1 times as easily


def heredity(heat, steps: int) -> list[list[Fraction]]:
    """One board with records: the depth M a composite has reached is kept in the record and passes every bang,
    and binding again below M is REBIND + 1 times as easy; the law over (k, M), read as the law of k."""
    law = {(0, 0): Fraction(1)}
    marginals = []
    for s in range(steps + 1):
        row = [Fraction(0)] * (K + 1)
        for (k, _m), p in law.items():
            row[k] += p
        marginals.append(row)
        if s == steps:
            break
        h = heat(s)
        nxt: dict[tuple[int, int], Fraction] = {}
        for (k, m), p in law.items():
            parts = sizes(k, h)
            if k < K:
                remembered = 1 - nonneg_less(k, m)
                parts[k + 1] = parts[k + 1] * (1 + REBIND * remembered)
            total = sum(parts.values())
            for k2, size in parts.items():
                key = (k2, max(m, k2))
                nxt[key] = nxt.get(key, Fraction(0)) + p * Fraction(size, total)
        law = nxt
    return marginals


def nonneg_less(k: int, m: int) -> int:
    """1 where k is at least m, 0 where k is below m: the one whether on m - k - 1."""
    n = m - k - 1
    return 1 - (n // (n * n + 1) + 1)


def main() -> None:
    steps = C * T
    lines = [
        "The past alone, or two boards (David, 2026-10-29): a toy of the logic in exact fractions",
        "",
    ]
    lines.append(
        f"room K = {K}, heat's top H = {H}, steps per swing T = {T}, swings C = {C}; decimals printed"
    )
    lines.append("")
    lines.extend(
        report(
            "A, the old theory: one bang, then cooling for ever, forward only",
            forward(cooling_heat, steps),
            cooling_heat,
        )
    )
    lines.append("")
    b1 = forward(swing_heat, steps)
    lines.extend(report("B1, the swing, forward only (a silent future)", b1, swing_heat))
    for c in (1, 3):
        lines.append("")
        bwd = backward(swing_heat, steps, [1 + c * k for k in range(K + 1)])
        lines.extend(
            report(
                f"B2, the swing with two boards, the future at the last bang weighing depth k by 1 + {c} k",
                met(b1, bwd),
                swing_heat,
            )
        )
    lines.append("")
    g1 = forward(gentle_heat, steps)
    lines.extend(
        report(f"B1 with a gentler bang (heat at most {GENTLE}), forward only", g1, gentle_heat)
    )
    lines.append("")
    g2 = met(g1, backward(gentle_heat, steps, [1 + 3 * k for k in range(K + 1)]))
    lines.extend(
        report("B2 with the gentler bang, the future weighing depth k by 1 + 3 k", g2, gentle_heat)
    )
    lines.append("")
    strong = [
        b - a
        for a, b in zip(
            per_swing(b1, swing_heat),
            per_swing(
                met(b1, backward(swing_heat, steps, [1 + 3 * k for k in range(K + 1)])), swing_heat
            ),
            strict=True,
        )
    ]
    gentle = [b - a for a, b in zip(per_swing(g1, gentle_heat), per_swing(g2, gentle_heat), strict=True)]
    b3 = heredity(swing_heat, steps)
    lines.extend(
        report(
            f"B3, the swing on one board with records: a remembered bond rebinds {REBIND + 1} times as easily",
            b3,
            swing_heat,
        )
    )
    lines.append("")
    lines.append("the two boards' lean, B2 less B1, in interesting clicks per swing (weight 1 + 3 k):")
    lines.append("  the full bang:   " + ", ".join(f"{float(x):.2f}" for x in strong))
    lines.append("  the gentle bang: " + ", ".join(f"{float(x):.2f}" for x in gentle))
    lines.append("")
    silent = met(b1, backward(swing_heat, steps, [1] * (K + 1)))
    same = all(x == y for a, b in zip(silent, b1, strict=True) for x, y in zip(a, b, strict=True))
    lines.append(f"B2 with a silent future (weight 1 at every depth) equals B1 exactly: {same}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
