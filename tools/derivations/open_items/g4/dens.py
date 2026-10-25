"""Hand g4, brief m, part (b): the den from its Gaussian primes. A lift of the prime p = a^2 + b^2 (a > b > 0) of den
is the point (num, s, den) with cos omega_0 = (a^2 - b^2) / p and sin omega_0 = 2 a b / p, so its gap is
g = 2 b^2 / p and its mass T sin omega_0 is T x 2 a b / p, both set by the prime alone (loader/circle.lift_points:
s = 2 a b den / p). The search: every prime 1 mod 4 below the bound with its two squares (loader/circle.two_squares),
the heavy lifts with g inside the window of window.py (g_low from the localised packet, g_high from the beat's
fraction), the light lifts with a Compton length 1 / (sqrt 3 omega_0) of 10 to 100 Links (omega_0 near sin omega_0
there), the dens their products (two primes, and three with a second heavy lift) within the bit bound measured
through the loader (the width, the amplitude bound and Rule3's flux total at the bound). Integer readings:
g, sin and the Compton length as quotients with remainders at the scale 1000, the mass ratio sin_h / sin_l as a
quotient with its remainder.

    python tools/derivations/g4/dens.py [--g-low 616/1000] [--g-high 821/1000] [--bits 128]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from event_universe import world_files  # noqa: E402
from event_universe.core.ports import LINK_UNIT  # noqa: E402
from event_universe.core.rule3 import coefficients, mass, partial_rooms, wall_of  # noqa: E402
from event_universe.features.read import edge_of  # noqa: E402
from event_universe.loader.circle import two_squares  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

GAMMA, ACTION = 1000, 36000
SQRT3_MILLI = isqrt(3 * 10**6)  # 1732: sqrt 3 to the thousandth, for the Compton length 1 / (sqrt 3 omega_0)


def quot(x: Fraction, scale: int = 1000) -> str:
    q, r = divmod(x.numerator * scale, x.denominator)
    return f"{q} rem {r}/{x.denominator}" if r else str(q)


def primes_1_mod_4(bound: int) -> list[int]:
    sieve = bytearray([1]) * (bound + 1)
    sieve[0] = sieve[1] = 0
    for n in range(2, isqrt(bound) + 1):
        if sieve[n]:
            sieve[n * n :: n] = bytearray(len(sieve[n * n :: n]))
    return [p for p in range(5, bound + 1, 4) if sieve[p]]


def lift_of(p: int) -> dict:
    """A prime's lift: its two squares a > b, g = 2 b^2 / p, sin = 2 a b / p, cos = (a^2 - b^2) / p, the Compton length 1000 / (sqrt 3 omega_0) in milli Links with omega_0 read as sin omega_0 (the light lifts, where the two agree to sin^2 / 6)."""
    legs = two_squares(p)
    a, b = max(legs), min(legs)
    g = Fraction(2 * b * b, p)
    s = Fraction(2 * a * b, p)
    compton_milli = (10**6 * p) // (2 * a * b * SQRT3_MILLI)  # 1000 / (sqrt 3 sin omega_0)
    return {"p": p, "a": a, "b": b, "g": g, "sin": s, "compton_milli": compton_milli}


def bits_at(den: int, folder: Path) -> dict:
    """The bit lengths at a den through the loader: the derived width, the amplitude bound A, the wall 6 den Gamma^2 G^2 (the remainders' room) and the largest total of Rule3's flux line at A over every family at the vacuum's paces, at a frozen clock and at the hill's edge (rule3.partial_rooms, the loader's own three extremes), the one transient the brief's bound names."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps({"integers": {"den": den, "node_clock": GAMMA, "quantum_action": ACTION}}))
    (folder / "w.json").write_text(json.dumps({"universe": "u.json", "shape": [3, 3, 3], "intervals": 1}))
    world_files.REPOSITORY_ROOT = folder
    t0 = time.time()
    world = load_world(folder / "w.json")
    a_bound = world.amplitude_bound
    unit = LINK_UNIT
    largest_total, largest_name = 0, ""
    for family in world.families:
        num, d = family.pair
        edge = edge_of(family.pair, GAMMA)
        for clock, pace in ((GAMMA, GAMMA), (0, 0), (edge, edge)):
            reads, self_coefficient, wall = coefficients(num, d, GAMMA, clock, pace, None, unit)
            plain = sum(abs(r) for r in reads)
            own = mass(num, d, clock, unit)
            *_partials, total = partial_rooms(self_coefficient, wall, own, plain + plain, plain)
            value = a_bound * total + wall - 1
            if value > largest_total:
                largest_total, largest_name = value, f"{family.name} at paces ({clock}, {pace})"
    return {
        "den": den,
        "den_bits": den.bit_length(),
        "width_bits": world.width.bit_length() if hasattr(world.width, "bit_length") else int(world.width),
        "amplitude_bound": a_bound,
        "wall_bits": wall_of(den, GAMMA, unit).bit_length(),
        "flux_total_bits": largest_total.bit_length(),
        "flux_total_at": largest_name,
        "families": len(world.families),
        "load_seconds": round(time.time() - t0, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--g-low", default="616/1000")
    parser.add_argument("--g-high", default="821/1000")
    parser.add_argument("--bits", type=int, default=128)
    parser.add_argument("--den-bits", type=int, default=59)
    parser.add_argument("--prime-bound", type=int, default=400000)
    parser.add_argument("--compton", default="10,100")
    args = parser.parse_args()
    g_low, g_high = Fraction(args.g_low), Fraction(args.g_high)
    c_lo, c_hi = (int(x) for x in args.compton.split(","))
    folder = Path("/dev/shm/tmp/g4_dens")
    out = Path(__file__).resolve().parent / "dens.out"
    lines: list[str] = []

    out.write_text("", encoding="utf-8")

    def say(text: str) -> None:
        print(text, flush=True)
        lines.append(text)
        with out.open("a", encoding="utf-8") as f:
            f.write(text + "\n")

    primes = primes_1_mod_4(args.prime_bound)
    lifts = [lift_of(p) for p in primes]
    heavy = [l for l in lifts if g_low <= l["g"] <= g_high]
    light = [l for l in lifts if c_lo * 1000 <= l["compton_milli"] <= c_hi * 1000]
    say(f"# dens (hand g4): primes 1 mod 4 below {args.prime_bound}: {len(primes)}; heavy lifts with g in [{g_low}, {g_high}]: {len(heavy)}; light lifts with the Compton length in [{c_lo}, {c_hi}] Links: {len(light)}; den within {args.den_bits} bits")
    say("# the heavy lifts below 2000 (p = a^2 + b^2, g = 2 b^2 / p, sin = 2 a b / p; milli):")
    for l in heavy:
        if l["p"] < 2000:
            say(f"  p {l['p']} = {l['a']}^2 + {l['b']}^2: g {quot(l['g'])}, sin {quot(l['sin'])}, Compton milli {l['compton_milli']}")
    say("# the control den 15,162,856,759,112,389 = 617 x 196,613 x 124,992,409, its three lifts:")
    for p in (617, 196613, 124992409):
        l = lift_of(p)
        inside = "INSIDE the window" if g_low <= l["g"] <= g_high else ("ABOVE the window (the pixel's side)" if l["g"] > g_high else "BELOW the window")
        say(f"  p {p} = {l['a']}^2 + {l['b']}^2: g {quot(l['g'])} milli ({inside}), sin {quot(l['sin'])} milli, Compton {quot(Fraction(l['compton_milli'], 1000))} Links")
    e_lift, p_lift = lift_of(124992409), lift_of(617)
    ratio = p_lift["sin"] / e_lift["sin"]
    say(f"  the control's mass ratio sin(617 lift) / sin(124,992,409 lift) = {quot(ratio, 1)} (nature's 1,836); its light lift's Compton length {quot(Fraction(e_lift['compton_milli'], 1000), 1)} Links, far beyond a 9-cube: a cloud over the board")
    # two-prime dens: the heavy times the light, within the bit bound, ranked by the mass ratio
    bound = 2**args.den_bits
    two = []
    for h in heavy:
        for l in light:
            den = h["p"] * l["p"]
            if den < bound:
                two.append((h["sin"] / l["sin"], den, h, l))
    two.sort(key=lambda row: (-row[0], row[1]))
    say(f"# two-prime dens within {args.den_bits} bits: {len(two)}; the three with the largest mass ratio sin_h / sin_l (nature's order 1,836, the integers' and the board's allowance here):")
    best = []
    for ratio, den, h, l in two[:3]:
        say(f"  den {den} ({den.bit_length()} bits) = {h['p']} x {l['p']}: heavy lift ({h['a']},{h['b']}) g {quot(h['g'])} milli sin {quot(h['sin'])} milli Compton {quot(Fraction(h['compton_milli'], 1000))} milli-Links; light lift ({l['a']},{l['b']}) g {quot(l['g'], 10**6)} micro, sin {quot(l['sin'], 10**6)} micro, Compton {quot(Fraction(l['compton_milli'], 1000))} milli-Links; mass ratio {quot(ratio, 1)} (x1000: {quot(ratio)})")
        best.append(den)
    # the compact choice: the smallest den with the heavy g nearest the window's centre and the light lift's Compton in range, ratio at least 20
    centre = (g_low + g_high) / 2
    compact = sorted(two, key=lambda row: (abs(row[2]["g"] - centre) > Fraction(1, 20), row[1]))
    say("# the three smallest dens with the heavy g within 0.05 of the window's centre " + quot(centre) + " milli:")
    for ratio, den, h, l in compact[:3]:
        say(f"  den {den} ({den.bit_length()} bits) = {h['p']} x {l['p']}: heavy ({h['a']},{h['b']}) g {quot(h['g'])} sin {quot(h['sin'])}; light ({l['a']},{l['b']}) sin {quot(l['sin'], 10**6)} micro Compton {quot(Fraction(l['compton_milli'], 1000))} milli-Links; ratio {quot(ratio, 1)}")
        if den not in best:
            best.append(den)
    # three-prime dens: heavy x neutron-like (a second lift in the window, sin above the heavy's by the least) x light, within the bound
    three = []
    small_heavy = [h for h in heavy if h["p"] < 3000]  # the three-prime search over the small heavy lifts alone (the product of three primes within 59 bits leaves the light lift its room)
    for i, h in enumerate(small_heavy):
        for n in small_heavy:
            if n["sin"] <= h["sin"]:
                continue
            r_n = n["sin"] / h["sin"]
            if r_n > Fraction(11, 10):
                continue
            for l in light:
                den = h["p"] * n["p"] * l["p"]
                if den < bound:
                    three.append((r_n, -(h["sin"] / l["sin"]), den, h, n, l))
    three.sort(key=lambda row: (row[0], row[1]))
    say(f"# three-prime dens within {args.den_bits} bits with a second heavy lift (neutron-like) whose sin exceeds the heavy's by the least (nature's 1.0013784): {len(three)}; the three nearest:")
    for r_n, neg_ratio, den, h, n, l in three[:3]:
        say(f"  den {den} ({den.bit_length()} bits) = {h['p']} x {n['p']} x {l['p']}: heavy ({h['a']},{h['b']}) g {quot(h['g'])} sin {quot(h['sin'])}; second ({n['a']},{n['b']}) g {quot(n['g'])} sin {quot(n['sin'])}, sin_n / sin_h x 10^6 = {quot(r_n, 10**6)}; light ({l['a']},{l['b']}) Compton {quot(Fraction(l['compton_milli'], 1000))} milli-Links; ratio heavy/light {quot(-neg_ratio, 1)}")
        if den not in best:
            best.append(den)
    say("# the bit lengths through the loader (the width derived, A, the wall's bits, Rule3's flux total at A over the three paces; the bound every integer must stand within is " + str(args.bits) + "):")
    for den in best + [15162856759112389, 1021, 1166991900949580266237]:
        try:
            found = bits_at(den, folder)
            verdict = "within" if found["flux_total_bits"] <= args.bits and found["wall_bits"] <= args.bits else "BEYOND"
            say(f"  den {den}: {json.dumps(found)} -> {verdict} {args.bits} bits")
        except Exception as named:  # a refusal by name is a reading too
            say(f"  den {den}: refused: {named}")
    # the den's bit bound: the largest den bits whose flux total stays within the bound, scanned on dens of the form 2^k - small prime products is not needed: the total is A x 3 w to the bit, so the scan is on the loader's A at a den of each bit length (the heavy x light products above, by bits)
    say("# the flux total's bits against den's bits on two-prime dens of rising size (one per bit length among the candidates):")
    seen = set()
    for ratio, den, h, l in sorted(two, key=lambda row: row[1]):
        b = den.bit_length()
        if b in seen or b % 4:
            continue
        seen.add(b)
        found = bits_at(den, folder)
        say(f"  den bits {b}: den {den}: width {found['width_bits']} A {found['amplitude_bound']} wall bits {found['wall_bits']} flux total bits {found['flux_total_bits']}")


if __name__ == "__main__":
    main()
