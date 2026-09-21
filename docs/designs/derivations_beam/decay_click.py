"""Section 18 (b) of DERIVATIONS_BEAM.md: a decay read as a click at a
rate, and a passage read as a click per Node of depth. Host arithmetic;
no run.

(A) The memoryless reference: a geometric survival at the rate p per
    interval, its 10th-to-90th-percentile width over its median (3.17 in
    the limit of small p).
(B) A decay decided on the body's own record: the wheel u advanced by the
    golden rate r on Z_W (record 155), the body decaying at the first
    interval with u < b; over every birth phase u_0 the first-passage
    times, their width over the median and their maximum (bounded, by
    the three-distance theorem).
(C) The same with the bit-reversed wheel of record 156.
(D) A passage per Node of depth decided the same way: the depth at which
    a row is absorbed, against the exponential (1 - p)^n.
"""

from __future__ import annotations

import math
from pathlib import Path

W = 4096
R = 2531  # the golden rate on Z_4096: 4096 / phi = 2531.4


def quantiles(times: list[int]) -> tuple[float, float, float, int]:
    s = sorted(times)
    n = len(s)
    q = lambda f: s[min(n - 1, int(f * n))]  # noqa: E731
    return q(0.1), q(0.5), q(0.9), s[-1]


def geometric(p: float) -> tuple[float, float, float]:
    q = lambda f: math.ceil(math.log(1 - f) / math.log(1 - p))  # noqa: E731
    return q(0.1), q(0.5), q(0.9)


def bitrev(n: int, bits: int = 12) -> int:
    return int(format(n, f"0{bits}b")[::-1], 2)


def first_passage(step, b: int, u0: int, n_max: int = 10**6) -> int:
    for n in range(1, n_max):
        if step(u0, n) < b:
            return n
    return n_max


def main() -> None:
    out = []
    out.append(
        "(A) The memoryless survival: the geometric law's 10th, 50th, 90th percentiles and (90 - 10) / 50"
    )
    for b in (64, 16, 4):
        p = b / W
        q10, q50, q90 = geometric(p)
        out.append(
            f"  p = {b} / {W}: {q10}, {q50}, {q90}; width over median {(q90 - q10) / q50:.3f} (the limit ln 9 / ln 2 = {math.log(9) / math.log(2):.3f})"
        )

    out.append("")
    out.append(
        "(B) The golden wheel on the body's record, u_n = (u_0 + n r) mod W, the decay at the first u_n < b"
    )
    golden = lambda u0, n: (u0 + n * R) % W  # noqa: E731
    for b in (64, 16, 4):
        times = [first_passage(golden, b, u0) for u0 in range(W)]
        q10, q50, q90, mx = quantiles(times)
        out.append(
            f"  b = {b} (p = 1 / {W // b}): percentiles {q10}, {q50}, {q90}, the maximum {mx} (1 / p = {W // b}); width over median {(q90 - q10) / q50:.3f}"
        )

    out.append("")
    out.append("(C) The bit-reversed wheel, u_n = (u_0 + bitrev(n)) mod W")
    rev = lambda u0, n: (u0 + bitrev(n % W)) % W  # noqa: E731
    for b in (64, 16):
        times = [first_passage(rev, b, u0) for u0 in range(W)]
        q10, q50, q90, mx = quantiles(times)
        out.append(
            f"  b = {b}: percentiles {q10}, {q50}, {q90}, the maximum {mx}; width over median {(q90 - q10) / q50:.3f}"
        )

    out.append("")
    out.append(
        "(D) A passage per Node of depth at the absorption p = 1 / 64: the count behind n Nodes over the first's"
    )
    p = 1 / 64
    out.append(
        f"  memoryless: (1 - p)^n = {1 - p:.4f}, {(1 - p) ** 10:.4f}, {(1 - p) ** 100:.4f} at n = 1, 10, 100 (nature: 1 to a part in 10^16 per metre)"
    )
    times = [first_passage(golden, 64, u0) for u0 in range(W)]
    surv = lambda n: sum(1 for t in times if t > n) / W  # noqa: E731
    out.append(
        f"  the golden wheel per Link: {surv(1):.4f}, {surv(10):.4f}, {surv(100):.4f}, {surv(150):.4f} at n = 1, 10, 100, 150: a ramp to zero, not an exponential"
    )
    out.append(
        "  the register's filter (J2): the same u at every Node, all or nothing: 16 of 1024 at the first reader, 0 behind"
    )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
