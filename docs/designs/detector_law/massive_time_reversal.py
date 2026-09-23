"""COMPUTATION in integers (not an engine run): the direction of time in the Inside
(MASSIVE_RECORD.md section 14, the owner's question of record 1439).

The light rule 3 a_next + r' = S_6 - 3 a_before + r (0 <= r' < 3) and the massive kind's
stable form 3 den (a_next + a_before) + r' = num S_6 + r (0 <= r' < 3 den), on a chain
with the two absent axes folded (S_6 = a_left + a_right + 4 a_now), the faces zero.
Three things are checked to the bit: (i) the forward step is a BIJECTION of the row's
state (a_now, a_before, r) given the neighbours, so an exact inverse exists: N = 3 den
a_next + r' is exact, M = num S_6 - N = 3 den a_before - r has one solution with 0 <= r
< 3 den, a_before = ceil(M / (3 den)), r = 3 den a_before - M; (ii) running the SAME
formula backward (the swap (a_next, r') <-> (a_before, r) with the floor division kept)
is a different map and does not return to the start; (iii) a click, the deletion of the
record's rows at a detector, cannot be inverted: the run with a click does not return.

    PYTHONPATH=src python docs/designs/detector_law/massive_time_reversal.py
"""

import numpy as np

RNG = np.random.default_rng(7)


def forward(a_now, a_before, r, num, den):
    """One interval of the pair's rule in integers (numpy int64), the floor division."""
    s6 = np.roll(a_now, 1) + np.roll(a_now, -1) + 4 * a_now
    s6[0] = s6[-1] = 0
    n_int = num * s6 + r - 3 * den * a_before
    a_next = n_int // (3 * den)
    r_next = n_int - 3 * den * a_next
    return a_next, a_now, r_next


def exact_inverse(a_now, a_before, r, num, den):
    """The inverse of `forward`: given (a_next, a_now, r') recover (a_now, a_before, r)."""
    a_next, a_mid, r_next = a_now, a_before, r  # the state after a forward step, renamed
    s6 = np.roll(a_mid, 1) + np.roll(a_mid, -1) + 4 * a_mid
    s6[0] = s6[-1] = 0
    m_int = num * s6 - (3 * den * a_next + r_next)
    a_prev = -((-m_int) // (3 * den))  # the ceiling division
    r_prev = 3 * den * a_prev - m_int
    return a_mid, a_prev, r_prev


def same_formula_backward(a_now, a_before, r, num, den):
    """The swap (a_next, r') <-> (a_before, r) with the floor division kept: the same
    formula run backward, which is NOT the inverse."""
    a_next, a_mid, r_next = a_now, a_before, r
    s6 = np.roll(a_mid, 1) + np.roll(a_mid, -1) + 4 * a_mid
    s6[0] = s6[-1] = 0
    n_int = num * s6 + r_next - 3 * den * a_next
    a_prev = n_int // (3 * den)
    r_prev = n_int - 3 * den * a_prev
    return a_mid, a_prev, r_prev


def run(num, den, steps, click_at=None, click_cells=None):
    n = 400
    x = np.arange(n)
    env = np.exp(-(((x - 120) / 20.0) ** 2))
    a_before = (2**20 * env * np.cos(0.2 * x)).astype(np.int64)
    a_now = (2**20 * env * np.cos(0.2 * x - 0.115)).astype(np.int64)
    r = RNG.integers(0, 3 * den, n, dtype=np.int64)
    start = (a_now.copy(), a_before.copy(), r.copy())
    st = start
    for t in range(steps):
        st = forward(*st, num, den)
        if click_at is not None and t == click_at:
            a, b, rr = st
            a = a.copy()
            b = b.copy()
            a[click_cells] = (
                0  # the click: the record's rows at the detector's cells deleted (the content handed over)
            )
            b[click_cells] = 0
            st = (a, b, rr)
    end = st
    back_exact = end
    back_same = end
    for _t in range(steps):
        back_exact = exact_inverse(*back_exact, num, den)
        back_same = same_formula_backward(*back_same, num, den)

    def dev(st):
        return max(
            int(np.abs(st[0] - start[0]).max()),
            int(np.abs(st[1] - start[1]).max()),
            int(np.abs(st[2] - start[2]).max()),
        )

    return dev(back_exact), dev(back_same), int(np.abs(start[0]).max())


def main():
    for label, num, den in (
        ("light [1, 1]", 1, 1),
        ("the massive kind [128, 129]", 128, 129),
        ("the massive kind [2, 3]", 2, 3),
    ):
        e, s, amp = run(num, den, 600)
        print(
            f"{label}, 600 intervals forward then back, no click: the exact inverse returns to the start with the maximal deviation {e} (of the amplitude {amp}); the same formula run backward deviates by {s}"
        )
    e, s, amp = run(1, 1, 600, click_at=300, click_cells=slice(200, 212))
    print(
        f"light [1, 1] with a CLICK at interval 300 (the rows on 12 cells deleted): the exact inverse deviates by {e} (of {amp}), the same formula by {s}: the click is not undone"
    )


if __name__ == "__main__":
    main()
