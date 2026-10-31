"""The floor's balance on the click world's triangle: an equal own spring s on the giver and the taker, at a fraction of
half their hands' tie, read on Big Pic's own equil.py (bigpic-3clicks 9771a49a4) and nothing else.

Clock: the giver and the taker on one two-leg band t, each with its own spring s (its mass); the held hand lends each
c h^2 through its four-leg tie. Swinging opposite, the pair holds s - t/2 + c h^2, so the floor at every h asks s >= t/2.
Algebra: the pair's form [[s + c h^2, t/2], [t/2, s + c h^2]]; the lend adds to the diagonal only.
Board: Big Pic's World and round, unchanged, run from his file's text above his first reading; his grain recipe
(README.md of his miracle folder): the counts times lam; W, the spring and the hands' tie times lam^4; the tie's factor
times lam^2. Every division here is the carry's.
Clicks: none read here; the identity (E32's change = the teeth's share) is checked every round, as in his read().

Usage: python3 -I floor_balance.py <src of node-all 9d75a4904> <equil.py of 9771a49a4> <lam> <num> <den> <rounds>
       <fall bits> [held lay a/b of the shipped one] [window]
  s = num/den of half the hands' tie; a fall is a count wider than the giver's lay by <fall bits> bits; with a window,
  the largest held square in counts^2 per window of rounds is printed (divide by lam^2 for the unit's terms).
"""

import sys

src, path = sys.argv[1], sys.argv[2]
lam, num, den, rounds, fall_bits = (int(x) for x in sys.argv[3:8])
held_part = sys.argv[8] if len(sys.argv) > 8 else "1/1"
window = int(sys.argv[9]) if len(sys.argv) > 9 else 0

text = open(path).read()
body = text.split('print(f"three clocks at W')[0]  # his module above his first reading: constants, World, run
sys.argv = [path, src, str(rounds)]
g = {"__name__": "equil_copy"}
exec(compile(body, path, "exec"), g)
carry = g["carry"]

l2, l4 = lam * lam, lam * lam * lam * lam
g["W"], g["S"], g["TIE2"], g["TIE4"] = g["W"] * l4, g["S"] * l4, g["TIE2"] * l4, g["TIE4"] * l2
g["D"] = g["W"] + g["W"]
half, _ = carry(g["TIE2"], 2, 0)
s, _ = carry(half * num, den, 0)
world = g["World"]({(0, 2): "four", (1, 2): "four", (0, 1): "two"}, [s, s, g["S"]], [2])

a, b = (int(x) for x in held_part.split("/"))
giver, taker, held = (x * lam for x in g["LAY"])
held, _ = carry(held * a, b, 0)
lay = [giver, taker, held]
st0 = (list(lay), list(lay), [0, 0, 0])
lay_bits = giver.bit_length()

st, kept, widest, fell, giver_top, taker_top, peak, peaks = st0, 0, 0, None, 0, 0, 0, []
for r in range(1, rounds + 1):
    try:
        st1 = world.round_(st)
    except ZeroDivisionError:
        fell = f"stopped at round {r}: a dial of 0"
        break
    kept += 1 if world.e32(st1) - world.e32(st) == world.share(st, st1) else 0
    widest = max([widest] + [abs(x).bit_length() for x in st1[0]])
    giver_top, taker_top = max(giver_top, abs(st1[0][0])), max(taker_top, abs(st1[0][1]))
    peak = max(peak, st1[0][2] * st1[0][2])
    st = st1
    if window and carry(r, window, 0)[1] == 0:
        peaks.append((r, peak))
        peak = 0
    if widest > lay_bits + fall_bits:
        fell = f"falls at round {r} (a count {fall_bits} bits past the giver's lay)"
        break

back = "not read (fallen)"
if fell is None:
    back = str(g["mirror"](g["run"](world, g["mirror"](st), rounds)) == st0)
print(f"lam {lam}; s = {num}/{den} of t/2 = {s} (t = {g['TIE2']}); held lay {held_part} of the shipped one ({held} counts):"
      f" identity {kept} of {r}; widest {widest} bits (the giver's lay {lay_bits}); {fell or 'no fall over the run'};"
      f" run back exact: {back}; largest swing in the unit: giver {carry(giver_top, lam, 0)[0]},"
      f" taker {carry(taker_top, lam, 0)[0]}", flush=True)
if window:
    print(f"  the largest held square in counts^2 per {window} rounds (lam^2 = {l2}): {peaks[:8]}", flush=True)
