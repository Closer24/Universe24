"""The proper-time gate of covariant-readings-v1 without a root (the owner's
word, 2026-09-22, records 642 and 647): the whole-root gate against two
root-free counter gates, enumerated exactly in integers (a check, not a run;
the derivation mathematician; DERIVATIONS_BEAM 17.7).

The body's integers: m = Q S M its rest energy in the identity's units, W =
m^2 + 3 p . p the exact square (17.6 M3), E' = isqrt(W) its whole root, gamma
= sqrt(W) / m. The whole-root gate (17.6 M1, 18.1 (a)) puts the n-th
self-creation at the tick

    T_n = 1 + floor((n - 1) E' / m).

Two root-free gates on two counters since the reset, t the intervals (the
first interval after the reset is t = 1) and n the self-creations:

    (A) the owner's, as stated: the n-th self-creation at the first t with
        t^2 m^2 >= n^2 W,                        T'_n = ceil(n sqrt(W) / m);
    (B) the same comparison shifted to the whole-root gate's origin and made
        strict: the n-th at the first t with t^2 m^2 > (n - 1)^2 W,
                                                 T''_n = 1 + floor((n - 1) sqrt(W) / m).

Every comparison below is on integers (no float, no root); sqrt(W) never
appears, only t^2 m^2 against n^2 W.

Run from the repository root:

    python docs/designs/covariant_readings/root_free_gate.py > docs/designs/covariant_readings/root_free_gate.out
"""

from __future__ import annotations

from math import isqrt


def whole_root(w: int, m: int, count: int) -> list[int]:
    e = isqrt(w)
    return [1 + (n - 1) * e // m for n in range(1, count + 1)]


def gate_a(w: int, m: int, count: int) -> list[int]:
    ticks, t = [], 0
    for n in range(1, count + 1):
        t = max(t, 1)
        while t * t * m * m < n * n * w:
            t += 1
        ticks.append(t)
    return ticks


def gate_b(w: int, m: int, count: int) -> list[int]:
    ticks, t = [], 1
    for n in range(1, count + 1):
        k = n - 1
        while t * t * m * m <= k * k * w:
            t += 1
        ticks.append(t)
    return ticks


def domain_squares(m: int) -> set[int]:
    """Every p . p reachable with |p|_1 <= m (three non-negative components)."""
    out = set()
    for a in range(m + 1):
        for b in range(m + 1 - a):
            for c in range(m + 1 - a - b):
                out.add(a * a + b * b + c * c)
    return out


def survey(m: int, squares: set[int], count: int) -> None:
    worst_a = (0, None, None)
    worst_b = (0, None, None)
    exact_a = exact_b = 0
    for s in sorted(squares):
        w = m * m + 3 * s
        base = whole_root(w, m, count)
        a = gate_a(w, m, count)
        b = gate_b(w, m, count)
        da = max(x - y for x, y in zip(a, base, strict=True))
        db = max(x - y for x, y in zip(b, base, strict=True))
        assert (
            min(x - y for x, y in zip(a, base, strict=True)) >= 0
            and min(x - y for x, y in zip(b, base, strict=True)) >= 0
        )
        if da > worst_a[0]:
            worst_a = (
                da,
                s,
                [n + 1 for n, (x, y) in enumerate(zip(a, base, strict=True)) if x - y == da][:3],
            )
        if db > worst_b[0]:
            worst_b = (
                db,
                s,
                [n + 1 for n, (x, y) in enumerate(zip(b, base, strict=True)) if x - y == db][:3],
            )
        exact_a += a == base
        exact_b += b == base
    print(
        f"   m = {m}: {len(squares)} values of p . p on |p|_1 <= m, n = 1 .. {count}: "
        f"gate (A) later than the whole root by at most {worst_a[0]} (at p . p = {worst_a[1]}, n = {worst_a[2]}), "
        f"identical for {exact_a} of {len(squares)} values of W; "
        f"gate (B) later by at most {worst_b[0]} (at p . p = {worst_b[1]}, n = {worst_b[2]}), identical for {exact_b} of {len(squares)}; "
        "neither gate is ever earlier"
    )


def main() -> None:
    print(
        "1. THE THREE GATES ON THE DOMAIN |p|_1 <= m (exact integers; the difference in the n-th self-creation's tick, root-free minus whole-root)"
    )
    for m in (16, 64, 100, 128):
        survey(m, domain_squares(m), count=min(128, m + 1))
    print(
        "   the bound: (B) differs from the whole root by at most ceil((n - 1) / m), i.e. by at most 1 for n <= m + 1;"
    )
    print(
        "   (A) differs by ceil(n gamma) - 1 - floor((n - 1) E' / m): 0 at p = 0, exactly 1 at gamma = 2, at most 3 on the domain (gamma <= 2), as enumerated above"
    )
    print()
    print(
        "2. THE MUON OF SERIES S (m = Q S M = 64 x 1 x 207 = 13248; c^2 = [1, 3]); the 64th self-creation and the beta click"
    )
    m = 13248
    for p, click_run, flight in ((0, 392, 328), (3640, 369, 299), (12856, 345, 221)):
        w = m * m + 3 * p * p
        e = isqrt(w)
        base, a, b = whole_root(w, m, 64), gate_a(w, m, 64), gate_b(w, m, 64)
        print(
            f"   p = {p}: W = {w}, E' = {e}, W - E'^2 = {w - e * e} (a perfect square: {w == e * e}); "
            f"the 64th self-creation: whole root {base[63]} (the register's pin), gate (A) {a[63]}, gate (B) {b[63]}; "
            f"the beta click = decay + the product's flight ({flight} intervals as run): whole root {base[63] + flight} (run {click_run}), "
            f"(A) about {a[63] + flight} to {a[63] + flight - (1 if a[63] > base[63] else 0)}, (B) {b[63] + flight}; "
            f"the largest difference over n = 1 .. 64: (A) {max(x - y for x, y in zip(a, base, strict=True))}, (B) {max(x - y for x, y in zip(b, base, strict=True))}"
        )
    print()
    print("3. THE COUNTERS' BOUND (the working bound 2^63 - 1 on t^2 m^2 and n^2 W)")
    bound = 2**63 - 1
    for m_, w_max in (
        (13248, 13248 * 13248 * 4),
        (64, 64 * 64 * 4),
        (2**20, 2**40 * 4),
        (2**24, 2**48 * 4),
    ):
        t_max = isqrt(bound) // m_
        n_max = isqrt(bound // w_max)
        print(
            f"   m = {m_}: t^2 m^2 <= 2^63 - 1 up to t = {t_max} intervals; n^2 W <= 2^63 - 1 up to n = {n_max} self-creations at gamma = 2 (W = 4 m^2)"
        )
    print(
        "   the registered covariant worlds run 420 ticks (j4_muon_3640.json): the muon's products stay below 2^49 without any reset"
    )
    print()
    print(
        "4. THE RESET: the whole-root gate is periodic in n with period m and shift E' (T_(n + m) = T_n + E'), a check on the muon:"
    )
    for p in (3640, 12856):
        w = m * m + 3 * p * p
        e = isqrt(w)
        base = whole_root(w, m, 2 * m + 2)
        ok = all(base[n + m] - base[n] == e for n in range(m + 1))
        print(
            f"   p = {p}: T_(n + m) - T_n = E' = {e} for every n <= m + 1: {ok}; the shift is the elapsed ticks, read without a root"
        )
    print(
        "   gate (B) has no exact period (its shift per m self-creations is sqrt(W), not an integer); a reset of (t, n) to (0, 0) without a carried remainder"
    )
    print(
        "   changes the ticks: the next self-creation would fall at floor(gamma) + 1 = 2 intervals for every 1 < gamma < 2 (a rate 1/2 in place of 1/gamma)"
    )


if __name__ == "__main__":
    main()
