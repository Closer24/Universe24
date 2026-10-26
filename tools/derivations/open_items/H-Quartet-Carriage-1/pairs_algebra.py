"""The pairs of den's circle in the law's integers (a reader of the two universe files, no engine import): per candidate quartet pair num over den, the sine s on the circle (s^2 = den^2 - num^2, exact), the row's unit 3 T s, the mass D = 12 (den - num) Gamma^2 G^2 and the six reaches' sum 6 R = 12 num Gamma^2 G^2 at the vacuum, the step's own coefficient S = 2 w - D - 6 R, the carriage inequality D > 6 R (den > 2 num), and the fraction of a one-Node level handed to the six Links per interval, 2 num over den as [quotient, remainder] per 1000. Integers only.
Usage: python pairs_algebra.py <out.json>"""
import json, sys
def isqrt(n):
    lo, hi = 0, 1
    while hi * hi <= n: hi += hi
    while hi - lo > 1:
        m = (lo + hi) // 2
        if m * m <= n: lo = m
        else: hi = m
    return lo
def unit_of(gamma):
    u = 1
    while (u + u) * u * (gamma + gamma - 1) <= gamma * gamma: u += 1
    return u
T, gamma = 36000, 1000
G = unit_of(gamma)
A, B = 125, 144
rows = []
for name, num, den in (("first lift", 15162854575528411, 15162856759112389), ("second leg", 2458210083751875, 15162856759112389), ("third lift", 2580388913625285, 15162856759112389), ("middle first", 1655880909, 1655909141), ("middle heavy", 506298091, 1655909141)):
    s = isqrt(den * den - num * num)
    assert s * s + num * num == den * den
    w = 6 * den * gamma * gamma * G * G
    D = 12 * (den - num) * gamma * gamma * G * G
    R6 = 12 * num * gamma * gamma * G * G
    unit = 3 * T * s
    share_node = 3 * den * (A * A + B * B)  # a one-Node child of v.G.v = 1 at S = 0: 2 w (A^2 + B^2) X / (4 Gamma^3 G^2)
    rows.append({"pair": name, "num": num, "den": den, "s": s, "gap den-num": den - num, "g per 1000": [(den - num) * 1000 // den, (den - num) * 1000 % den], "cos per 1000": [num * 1000 // den, num * 1000 % den],
        "unit 3Ts": unit, "D": D, "6R": R6, "S = 2w - D - 6R": 2 * w - D - R6, "carries D > 6R": D > R6, "handed per interval 2num/den per 1000": [2 * num * 1000 // den, 2 * num * 1000 % den],
        "child share at the Node over the unit (v.G.v 1)": [share_node // unit, share_node % unit], "quartet child (v.G.v 4) quanta": [4 * share_node // unit, 4 * share_node % unit]})
json.dump({"T": T, "gamma": gamma, "G": G, "A": A, "B": B, "rows": rows}, open(sys.argv[1], "w"), indent=1)
for r in rows: print(r)
