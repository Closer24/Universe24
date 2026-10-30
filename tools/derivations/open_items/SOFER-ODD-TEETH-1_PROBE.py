"""Sofer's check of the owner's ruling on the teeth counts (2026-10-28, 10:5x UTC): no restriction of even or odd.

  python3 -I tools/derivations/open_items/SOFER-ODD-TEETH-1_PROBE.py

Integers only (no float, no division but the floor). A gear has w fine teeth, r in [0, w), and mid(w) = w div 2. Each claim
is run for every teeth count from 2 to 40 and then again on a mutated formula that must fail (the mutation proof).
  the one mirror        r to (2 mid - r) mod w, the carry dropped (acts.mirror)
  the flip              r to w - 1 - r (acts.carry at -1)
  the carry's rounding  q(p) = (p + mid) div w, which should give q(-p) = -q(p)
  the fold's digits     min(r, w - 1 - r)
  the stride            P = w d + r - mid, d the notch now less the notch before
"""

from __future__ import annotations

COUNTS = range(2, 41)


def mid(w: int) -> int:
    return w // 2


def mirror(r: int, w: int) -> int:
    return (2 * mid(w) - r) % w


def flip(r: int, w: int) -> int:
    return w - 1 - r


def q(p: int, w: int) -> int:
    return (p + mid(w)) // w


def other_mirror(r: int, w: int) -> int:
    """The two's complement w - r mod w, the other mirror of the law's history."""
    return (w - r) % w


def retrace(w: int, d: int, turn) -> int:
    """The mathematician's one-gear toy: images hit twice by the step and the turnover at the weak top."""
    images: dict[tuple[int, int, int], int] = {}
    for before in range(-25, 26):
        for now in range(-25, 26):
            for r in range(w):
                u = 2 * w * now - w * before - d * now + r
                after = u // w
                top = before <= now and after <= now and (before < now or after < now)
                image = (now, before, turn(r, w)) if top else (now, u // w, u % w)
                images[image] = images.get(image, 0) + 1
    return sum(1 for n in images.values() if n > 1)


def parity(w: int) -> str:
    return "even" if w % 2 == 0 else "odd"


def main() -> int:
    bad = 0

    def report(label: str, ok: bool, detail: str = "") -> None:
        nonlocal bad
        if not ok:
            bad += 1
        print(f"  {label}: {'ok' if ok else 'FAILS'}{(' (' + detail + ')') if detail else ''}")

    print("1. The one mirror and the flip, at every teeth count from 2 to 40")
    report(
        "the mirror is an involution at every count",
        all(mirror(mirror(r, w), w) == r for w in COUNTS for r in range(w)),
    )
    report(
        "the flip is an involution at every count",
        all(flip(flip(r, w), w) == r for w in COUNTS for r in range(w)),
    )
    report(
        "the mirror fixes the tooth 0 and the tooth w / 2 at an even w, the mid tooth alone at an odd w",
        all(
            [r for r in range(w) if mirror(r, w) == r] == ([0, w // 2] if w % 2 == 0 else [mid(w)])
            for w in COUNTS
        ),
    )
    report(
        "the flip fixes no tooth at an even w, the mid tooth alone at an odd w",
        all(
            [r for r in range(w) if flip(r, w) == r] == ([] if w % 2 == 0 else [mid(w)]) for w in COUNTS
        ),
    )
    report(
        "the mirror is the flip at every odd w and differs from it at every even w",
        all(all(mirror(r, w) == flip(r, w) for r in range(w)) == (w % 2 == 1) for w in COUNTS),
    )

    print("2. The carry's rounding at the mid tooth")
    window = {w: range(-4 * w, 4 * w + 1) for w in COUNTS}
    ties = {w: [p for p in window[w] if q(-p, w) != -q(p, w)] for w in COUNTS}
    report(
        "no tie at an odd w: q(-p) = -q(p) for every p in -4 w to 4 w",
        all(ties[w] == [] for w in COUNTS if w % 2 == 1),
    )
    report(
        "at an even w the failures are exactly the ties p = w / 2 mod w",
        all(ties[w] == [p for p in window[w] if (p - w // 2) % w == 0] for w in COUNTS if w % 2 == 0),
    )
    print(
        "  failures in -4 w to 4 w at w = 8, 9, 10, 11: "
        + ", ".join(f"{len(ties[w])}" for w in (8, 9, 10, 11))
    )

    print("3. The fold's digit classes min(r, w - 1 - r)")
    report(
        "their number is (w + 1) div 2 at every count",
        all(len({min(r, w - 1 - r) for r in range(w)}) == (w + 1) // 2 for w in COUNTS),
    )
    report(
        "w div 2 is that number at an even w only",
        all((len({min(r, w - 1 - r) for r in range(w)}) == w // 2) == (w % 2 == 0) for w in COUNTS),
    )

    print("4. The stride P = w d + r - mid under the exchange of the two slots (d to -d)")
    flip_to = {}
    mirror_miss = {}
    for w in COUNTS:
        flip_to[w] = {
            (w * -d + flip(r, w) - mid(w)) + (w * d + r - mid(w)) for d in range(-3, 4) for r in range(w)
        }
        mirror_miss[w] = {
            (w * -d + mirror(r, w) - mid(w)) + (w * d + r - mid(w))
            for d in range(-3, 4)
            for r in range(w)
        }
    report(
        "the flip sends P to -P - 1 at an even w and to -P at an odd w",
        all(flip_to[w] == ({-1} if w % 2 == 0 else {0}) for w in COUNTS),
    )
    report(
        "the mirror, its carry dropped, sends P to -P at an odd w and misses by -w at the tooth 0 at an even w",
        all(mirror_miss[w] == ({-w, 0} if w % 2 == 0 else {0}) for w in COUNTS),
    )

    print("5. The mean teeth count (w / 2)(X0 + X1) of the riders' ride")
    sums = range(-10, 11)
    report(
        "w (X0 + X1) is even for every pair of notches at an even w",
        all((w * s) % 2 == 0 for w in COUNTS if w % 2 == 0 for s in sums),
    )
    report(
        "w (X0 + X1) is odd where the notches' sum is odd at an odd w: the half is no integer there",
        all((w * s) % 2 == 1 for w in COUNTS if w % 2 == 1 for s in sums if s % 2 == 1),
    )

    print(
        "6. The one-gear retrace of a turnover at the weak top (the mathematician's toy, rewritten), w = 8 to 15"
    )
    rows = []
    for w in range(8, 16):
        for d in (3, 5):
            rows.append((w, d, retrace(w, d, mirror), retrace(w, d, flip)))
    for w, d, m, f in rows:
        print(
            f"  w {w:2d} ({parity(w):4s}) D {d}: images hit twice with the mirror {m:3d}, with the flip {f:3d}"
        )
    report(
        "the mirror collides at every even w and at no odd w",
        all((m > 0) == (w % 2 == 0) for w, _, m, _ in rows),
    )
    report("the flip collides at no count", all(f == 0 for _, _, _, f in rows))
    toy = {w: retrace(w, 3, mirror) for w in (10, 11)}
    report(
        "the Boss's reading, 25 images hit twice at w = 10 and none at w = 11",
        toy == {10: 25, 11: 0},
        str(toy),
    )

    print("7. The mutation proof: each formula with one term changed must fail")
    other_ok = all(
        all(other_mirror(r, w) == flip(r, w) for r in range(w)) == (w % 2 == 1) for w in COUNTS
    )
    print(
        f"  the other mirror w - r mod w for the mirror: equals the flip at every odd w: {other_ok} (must be False)"
    )
    if other_ok:
        bad += 1
    wrong_classes = all(len({min(r, w - 1 - r) for r in range(w)}) == w // 2 for w in COUNTS)
    print(
        f"  w div 2 for the number of the fold's classes at every count: {wrong_classes} (must be False)"
    )
    if wrong_classes:
        bad += 1
    shifted = all(
        all(((p + w // 2 + 1) // w) == -((-p + w // 2 + 1) // w) for p in window[w])
        for w in COUNTS
        if w % 2 == 1
    )
    print(f"  the rounding at the tooth mid + 1 has no tie at every odd w: {shifted} (must be False)")
    if shifted:
        bad += 1
    print(f"result: {bad} failures of the claims (the mutants fail as they must)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
