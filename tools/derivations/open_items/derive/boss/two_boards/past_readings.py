"""Three readings on David's past_or_two_boards toy (toys-5 7168f77c9), in exact fractions, the toy's own laws.

usage: git show 7168f77c9:tools/derivations/open_items/derive/david_open/two_boards/past_or_two_boards.py > toy.py
       python3 -I past_readings.py toy.py

1. The fade: the same weighted future (1 + 3 k) placed 8 swings or 16 swings ahead; the lean per swing against
   the swings left before that future.
2. The act's own count as the future's weight, nothing typed: each history weighed by the product of its own sizes
   (the backward board's weight the count of the future's paths, unnormalized; the chain run from the first
   bang through its own split chances), against the forward law.
3. The lean is a departure from the forward draw (law 9): per swing, the largest change of one split's chance
   between B2 (1 + 3 k) and B1, as a fraction of the forward chance.
"""

import importlib.util
import sys
from fractions import Fraction


def load(path: str):
    spec = importlib.util.spec_from_file_location("toy", path)
    toy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(toy)
    return toy


def steps_law(toy, heat, steps: int, back: list[list[Fraction]]):
    """The product draw's chance of each split at every step: forward size times the backward weight it leads to."""
    out = []
    for s in range(steps):
        h = heat(s)
        row = {}
        for k in range(toy.K + 1):
            parts = toy.sizes(k, h)
            weights = {k2: size * back[s + 1][k2] for k2, size in parts.items()}
            total = sum(weights.values())
            row[k] = {k2: w / total for k2, w in weights.items()}
        out.append(row)
    return out


def forward_chances(toy, heat, steps: int):
    out = []
    for s in range(steps):
        h = heat(s)
        row = {}
        for k in range(toy.K + 1):
            parts = toy.sizes(k, h)
            total = sum(parts.values())
            row[k] = {k2: Fraction(size, total) for k2, size in parts.items()}
        out.append(row)
    return out


def path_count_back(toy, heat, steps: int) -> list[list[Fraction]]:
    """The future's own count: Z(s, k) = sum over the splits of size times Z(s + 1, k2), Z = 1 at the end."""
    back = [[Fraction(0)] * (toy.K + 1) for _ in range(steps + 1)]
    back[steps] = [Fraction(1)] * (toy.K + 1)
    for s in range(steps - 1, -1, -1):
        h = heat(s)
        for k in range(toy.K + 1):
            back[s][k] = sum(size * back[s + 1][k2] for k2, size in toy.sizes(k, h).items())
    # Normalize each step's row so the numbers stay small; the draw reads ratios alone.
    for s in range(steps + 1):
        top = max(back[s])
        back[s] = [x / top for x in back[s]]
    return back


def propagate(toy, law, steps: int) -> list[list[Fraction]]:
    """The marginal of a chain from the first bang at depth 0, step by step through its split chances."""
    out = [[Fraction(0)] * (toy.K + 1) for _ in range(steps + 1)]
    out[0][0] = Fraction(1)
    for s in range(steps):
        for k, p in enumerate(out[s]):
            if p:
                for k2, q in law[s][k].items():
                    out[s + 1][k2] += p * q
    return out


def main() -> None:
    toy = load(sys.argv[1])
    T, C = toy.T, toy.C
    heat = toy.swing_heat
    weight = [1 + 3 * k for k in range(toy.K + 1)]
    lines = ["Three readings on David's past_or_two_boards toy (the Boss, 2026-10-29)", ""]

    # 1. The fade.
    lines.append("1. The fade: the lean B2 less B1 in interesting clicks per swing, weight 1 + 3 k")
    for swings in (C, 2 * C):
        steps = swings * T
        b1 = toy.forward(heat, steps)
        b2 = toy.met(b1, toy.backward(heat, steps, weight))
        lean = [
            sum(
                (toy.mean(b2[s]) - toy.mean(b1[s])) * toy.flow(heat(s))
                for s in range(n * T, (n + 1) * T)
            )
            for n in range(swings)
        ]
        lines.append(f"  the weighted future {swings} swings ahead:")
        lines.append("    swing  1 to " + f"{swings}: " + ", ".join(f"{float(x):.3g}" for x in lean))
        ratios = [lean[n] / lean[n + 1] for n in range(swings - 1)]
        lines.append(
            "    each swing's lean over the next's: " + ", ".join(f"{float(r):.3f}" for r in ratios)
        )
    lines.append("")

    # 2. The act's own count.
    steps = C * T
    b1 = toy.forward(heat, steps)
    counted = propagate(toy, steps_law(toy, heat, steps, path_count_back(toy, heat, steps)), steps)
    lines.append(
        "2. The future weighed by its own count of paths (nothing typed), against the forward law:"
    )
    lines.append(
        "  depth at each swing's top, forward:  "
        + ", ".join(f"{float(toy.mean(b1[n * T + T // 2])):.3f}" for n in range(C))
    )
    lines.append(
        "  depth at each swing's top, counted:  "
        + ", ".join(f"{float(toy.mean(counted[n * T + T // 2])):.3f}" for n in range(C))
    )
    lean = [
        sum(
            (toy.mean(counted[s]) - toy.mean(b1[s])) * toy.flow(heat(s))
            for s in range(n * T, (n + 1) * T)
        )
        for n in range(C)
    ]
    lines.append(
        "  the lean in interesting clicks per swing: " + ", ".join(f"{float(x):+.3f}" for x in lean)
    )

    check = propagate(toy, steps_law(toy, heat, steps, toy.backward(heat, steps, weight)), steps)
    same_b2 = check == toy.met(b1, toy.backward(heat, steps, weight))
    lines.append(f"  (the chain's own marginal reproduces David's B2 marginal exactly: {same_b2})")
    lines.append("")

    # 3. The lean as a departure from the forward draw.
    back = toy.backward(heat, steps, weight)
    drawn = steps_law(toy, heat, steps, back)
    born = forward_chances(toy, heat, steps)
    lines.append(
        "3. The lean is a departure from the forward draw: per swing, the largest relative change of one"
    )
    lines.append(
        "   split's chance, B2 (1 + 3 k) against B1, over the depths and the steps of the swing"
    )
    worst = []
    for n in range(C):
        top = Fraction(0)
        for s in range(n * T, (n + 1) * T):
            for k in range(toy.K + 1):
                for k2, p in born[s][k].items():
                    if p:  # a split of size 0 has chance 0 under both
                        top = max(top, abs(drawn[s][k][k2] - p) / p)
        worst.append(top)
    lines.append("  " + ", ".join(f"{float(x):.3g}" for x in worst))
    silent = steps_law(toy, heat, steps, toy.backward(heat, steps, [1] * (toy.K + 1)))
    same = all(silent[s][k] == born[s][k] for s in range(steps) for k in range(toy.K + 1))
    lines.append(f"  a silent future's draw equals the forward draw at every split: {same}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
