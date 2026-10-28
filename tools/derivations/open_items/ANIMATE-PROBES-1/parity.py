"""Probe: the one mirror and Rule3's rounding at even and odd teeth counts (pure integers, no engine).

The mirror is the engine's (acts.mirror): the fine tooth r to (mid + mid - r) mod w, the carry dropped,
with the gear's two slots exchanged, so the stride P = w (now - before) + r - mid should turn to -P.
The rounding is the carry at the mid tooth: q(p) = (p + mid) div w, which should give q(-p) = -q(p).
"""


def mirror(r: int, w: int) -> int:
    mid = w // 2
    return (mid + mid - r) % w


def row(w: int) -> str:
    mid = w // 2
    involution = sum(1 for r in range(w) if mirror(mirror(r, w), w) != r)
    stride = [(d, r) for d in range(-2, 3) for r in range(w)
              if (-w * d + mirror(r, w) - mid) != -(w * d + r - mid)]
    off = sorted({(-w * d + mirror(r, w) - mid) + (w * d + r - mid) for d, r in stride})
    ties = sum(1 for p in range(-50, 51) if (-p + mid) // w != -((p + mid) // w))
    return (f"w {w:2d} ({'even' if w % 2 == 0 else 'odd '}): mirror an involution, failures {involution}; "
            f"P to -P, failures {len(stride)} of {5 * w} (fine teeth {sorted({r for _, r in stride})}, "
            f"off by {off}); rounding q(-p) = -q(p), failures {ties} of 101")


for w in range(8, 16):
    print(row(w))


def carried_mirror(d: int, r: int, w: int) -> tuple[int, int]:
    """A candidate for any teeth count: the mirror with its carry kept in the stride (the slots exchanged, d to -d + c)."""
    mid = w // 2
    c, r2 = divmod(mid + mid - r, w)
    return -d + c, r2


def half_even(p: int, w: int) -> int:
    """A candidate for any divisor: the carry at the mid tooth with an exact tie sent to the even quotient."""
    mid = w // 2
    q, s = divmod(p + mid, w)
    tie = 1 if (w % 2 == 0 and s == 0) else 0
    return q - tie * (q % 2)


print("candidates for any teeth count:")
for w in range(8, 16):
    mid = w // 2
    inv = sum(1 for d in range(-2, 3) for r in range(w)
              if carried_mirror(*carried_mirror(d, r, w), w) != (d, r))
    neg = sum(1 for d in range(-2, 3) for r in range(w)
              if (lambda d2, r2: w * d2 + r2 - mid)(*carried_mirror(d, r, w)) != -(w * d + r - mid))
    sym = sum(1 for p in range(-50, 51) if half_even(-p, w) != -half_even(p, w))
    print(f"w {w:2d}: the carried mirror an involution, failures {inv} of {5 * w}; P to -P, failures {neg}; "
          f"ties to even, q(-p) = -q(p), failures {sym} of 101")
