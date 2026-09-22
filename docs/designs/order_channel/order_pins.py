"""The pins of the order channel, computed from the law's algebra before any
run (docs/designs/order_channel/PINS.md; the third referee read, record 938
(2) of docs/LOG_2026-09-20.md). No engine run: the click of a record is the
ladder of the registered design (the generator's `joint` and the rungs of
BEAM_LAW note 46, imported from examples/events/amplitude/make_worlds.py),
so every number here is a COMPUTATION. Integers and Fractions only.

The law under the pair form: a record of birth ordinal t has the wheel
value u = (t - 1) mod N (the wheel [1, N]); its one click lands in the first
cell k of the ladder with u < b_k, the rungs b_k = (2 N C_k + T) // (2 T)
over the cells (++, +-, -+, --) in the layer's order, C_k the cumulative
weight, T the total. The first party's outcome is + exactly for u < N / 2
(Theorem 5 of the paper). The serial correlation at lag 1 of a sequence
x_0 .. x_{L-1} of +-1 is the cyclic mean (1 / L) sum_t x_t x_{(t+1) mod L}
(the referee's definition: 15 / 16 over 192 births at a = 0), and the open
mean over the L - 1 adjacent pairs is printed beside it, unpinned.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GENERATOR = ROOT / "examples" / "events" / "amplitude" / "make_worlds.py"


def load_generator():
    sys.path.insert(0, str(ROOT / "src"))
    spec = importlib.util.spec_from_file_location("amplitude_make_worlds", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


GEN = load_generator()
N = GEN.N
PAIR = GEN.BELL_PAIR
BIRTHS = 192


def cell_of_u(a: int, b: int) -> list[tuple[str, str]]:
    """The cell (oA, oB) of every u = 0 .. N - 1 at the settings (a, b): the
    ladder's first k with u < b_k over the cells in the layer's order."""
    weights = GEN.joint([(a, 0), (b, 0)], [tuple(p) for p in PAIR], N)
    order = GEN.outcomes(2)
    total = sum(weights[o] for o in order)
    rungs = []
    cumulative = 0
    for outcome in order:
        cumulative += weights[outcome]
        rungs.append((2 * N * cumulative + total) // (2 * total))
    assert rungs[-1] == N
    cells = []
    for u in range(N):
        k = next(i for i, rung in enumerate(rungs) if u < rung)
        cells.append((order[k][0], order[k][1]))
    return cells


def sign(o: str) -> int:
    return 1 if o == "+" else -1


def serial(xs: list[int]) -> tuple[Fraction, Fraction]:
    """(cyclic, open) serial correlation at lag 1."""
    L = len(xs)
    cyclic = Fraction(sum(xs[t] * xs[(t + 1) % L] for t in range(L)), L)
    open_ = Fraction(sum(xs[t] * xs[t + 1] for t in range(L - 1)), L - 1)
    return cyclic, open_


def protocol(settings: list[int], shift: int, b: int = 0) -> dict[str, object]:
    """Alice's setting at the analysed birth number t (t = 0 .. 191, the
    wheel u = (t + u0) mod N for any start u0: one joint period of the wheel
    and the setting cycle, so the cyclic values do not depend on u0; u0 = 0
    here) is settings[(t + shift) mod period]; Bob's at b."""
    tables = {a: cell_of_u(a, b) for a in set(settings)}
    period = len(settings)
    A: list[int] = []
    B: list[int] = []
    for t in range(BIRTHS):
        a = settings[(t + shift) % period]
        oa, ob = tables[a][t % N]
        A.append(sign(oa))
        B.append(sign(ob))
    return {
        "alice_plus": A.count(1),
        "alice_minus": A.count(-1),
        "bob_plus": B.count(1),
        "bob_minus": B.count(-1),
        "bob_serial": serial(B),
        "alice_serial": serial(A),
        "same": sum(1 for x, y in zip(A, B, strict=True) if x == y),
    }


def main() -> int:
    print(
        f"N = {N}, births analysed L = {BIRTHS} (three turns of the wheel, one joint period with a period-3 cycle), b = 0"
    )
    print("COMPUTATION: the cells of the ladder at (a, 0), Bob's + set over u:")
    for a in (0, 32, 21, 42):
        cells = cell_of_u(a, 0)
        alice_plus = [u for u in range(N) if cells[u][0] == "+"]
        bob_plus = [u for u in range(N) if cells[u][1] == "+"]
        assert alice_plus == list(range(N // 2)), a
        print(
            f"  a = {a:2d}: Alice + for u < 32 (Theorem 5); Bob + at {len(bob_plus)} of 64 u: {bob_plus}"
        )
    print()
    protocols = [
        ("P1 Alice constant a = 0 (the referee's 'send 0': the world order_a0_b0.json)", [0]),
        (
            "P2 Alice a = 32, 0 with period 2 (a chooser at the stride 32: REFUSED by the loader, 2 x content must stay below K x N; no world)",
            [32, 0],
        ),
        (
            "P3 Alice a = 0, 21, 42 with period 3 (the register's chooser at the stride 64 / 3: the world order_a0_21_42_b0.json)",
            [0, 21, 42],
        ),
        (
            "P0 the referee's a = 32, 0, 0 with period 3 (not expressible by the register's keys; the check of record 938 (2))",
            [32, 0, 0],
        ),
    ]
    for title, settings in protocols:
        print(title)
        for shift in range(len(settings)):
            r = protocol(settings, shift)
            cyc, opn = r["bob_serial"]
            acyc, aopn = r["alice_serial"]
            print(
                f"  shift {shift} (Alice's setting at the analysed birth t is {settings}[(t + {shift}) mod {len(settings)}]):"
                f" Bob's serial correlation at lag 1 = {cyc} cyclic ({opn} open, unpinned);"
                f" Bob's marginal {r['bob_plus']} / {r['bob_minus']}; Alice's marginal {r['alice_plus']} / {r['alice_minus']},"
                f" Alice's serial {acyc} cyclic; same-sign pairs {r['same']} of {BIRTHS}"
            )
    print()
    print(
        "nature: 0 on Bob's serial correlation under any setting sequence of Alice's (the comparison value, record 817's rule: the thing compared with)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
