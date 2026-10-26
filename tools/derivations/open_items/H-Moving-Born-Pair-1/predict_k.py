"""The prediction before the runs: per birth of a head record, the born Link's axis, the recoil P the take books along it, each child's wall E (booked div 2), the half-angle sine h = den sin(k / 2) by born_phase's divisions, the circle's point (C, S), the child's levels under the phase against the rest levels (the plane's (sense A, 0, 0, B); the quartet's along its spin vector), and the first interval whose lay parts. Integers only.
Usage: python predict_k.py <record.json> [quartet]"""
import json, sys

sys.path.insert(0, "/dev/shm/tmp/mb1/src_mb1")
from event_universe.core.paces import sine_den
from event_universe.core.rule3 import quotient, signed_quotient, largest_below
from event_universe.seed import circle_point
from event_universe import gram

rec = json.load(open(sys.argv[1]))
den = int(rec["den"]) if "den" in rec else int(rec["universe"]["integers"]["den"])
uni = rec["universe"]
_den = int(rec["den"]) if "den" in rec else int(rec["universe"]["integers"]["den"])
_all = rec["universe"]["rows"]
rows = [r for r in _all if int(r["shape"]) in (2, 8) and int(r["pair"][0]) != _den] + [r for r in _all if int(r["shape"]) == 2 and int(r["pair"][0]) == _den]  # the records in the acts' order (rows.order_key): the gapped planes and the quartets in the file's order, then the emitter
T = int(uni["integers"]["quantum_action"])
births = [e for e in rec["log"] if e["event"] == "birth"]
first_part = None
out = []
for b in births:
    s = b["line_pair"]
    num = int(rows[s]["pair"][0])
    shape = int(rows[s]["shape"])
    A, B = b["amplitude"]
    minus, plus = b["minus"], b["plus"]
    axis = [a for a in range(3) if minus[a] != plus[a]][0]
    p = abs(int(b["dP_take"][axis]))
    e = quotient(int(b["booked"]), 2)
    sine = sine_den(num, den)
    h = min(quotient(3 * sine * quotient(den * p, num), 4 * e), den) if e > 0 else 0
    c, sn = circle_point(den, h)
    v_milli = quotient(1000 * p, e + e)
    if shape == 2:
        vec = [1, 0]
    else:
        vec = gram.spin_vector(shape, axis, 1)
    J = gram.rotation(shape)
    jv = gram.matvec(J, vec)
    rest = [x for v, j in zip(vec, jv) for x in (A * v, B * j)]
    moved = [x for v, j in zip(vec, jv) for x in (signed_quotient(A * (c * v + sn * j), den), signed_quotient(B * (c * j - sn * v), den))]
    parts = moved != rest
    if parts and first_part is None:
        first_part = b["i"]
    out.append({"i": b["i"], "row": s, "axis": axis, "P": p, "E": e, "v_milli": v_milli, "h": h, "h_bits": h.bit_length(), "den_minus_C": den - c, "S": sn, "rest": rest, "moved": moved, "parts": parts})
thr_re = largest_below(quotient(den, 4))
print(json.dumps({"record": sys.argv[1], "den": den, "T": T, "births": len(births), "parting births": sum(1 for o in out if o["parts"]), "first parting interval": first_part, "h at which C first falls below den (about)": thr_re, "h at which A S div den reaches 1 (about)": quotient(den, 2 * 125)}))
for o in out:
    print(json.dumps(o))
