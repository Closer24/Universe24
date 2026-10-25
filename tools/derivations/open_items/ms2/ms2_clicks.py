"""ms2: what a far reader has from the clicks alone of one engine record (the credit and birth lines), integers only.
Usage: python ms2_clicks.py <record.json>
Reads: every birth's two children's Wronskian W (the charge as laid), its plane, its amplitude; every credit's sense and its
species solved from the frame by the decoder (decoder.solve), as a rational num/den, per plane; the ratio of the decoded
points of any two gapped planes (the middle solve per plane) as an integer per 10^9; the senses' sums.
PREDICTION (written before the run, from lay_amplitude's algebra at the vacuum, 2D + SUM R = 12 Gamma^2 G^2 (2 den - num),
target = 3 T s 4 Gamma^2 G^2, so A = ceil sqrt(T s / (2 den - num)) and W_child = +-A^2):
  universe_toy (T 36,000): gapped 0 (the electron-like lift, s/den about 5.4e-4): A 5, |W| 25; the heavy lifts: A about 139 to 140,
  |W| about 19,300 to 19,600; the gap-0 plane: A 190, |W| 36,100. NOT T div 2 = 18,000 and NOT the same across the rows.
  The senses: every birth's two children at opposite signs, the sum 0."""
import json, sys
from functools import cmp_to_key
sys.set_int_max_str_digits(0)
from event_universe import decoder
from event_universe.core.paces import sine_den

BILLION = 10 ** 9

def main(path):
    run = json.load(open(path))
    rec = decoder.Record(run)
    den, T = rec.den, rec.T
    print("record", path, "den", den, "T", T, "Gamma", rec.gamma, "G", rec.G)
    print("planes (num) by file order:", rec.line_num)
    print("decoder names:", {k: v for k, v in rec.NAMES.items()})
    births = rec.births
    print("births", len(births), "credits", len(rec.credits))
    byplane = {}
    for b in births:
        s = b["line_pair"]
        byplane.setdefault(s, []).append((b["amplitude"], tuple(b["W_children"]), b["booked"], b["taken"]))
    for s in sorted(byplane):
        ws = sorted(set(w for a, wc, bo, ta in byplane[s] for w in wc))
        amps = sorted(set(a for a, wc, bo, ta in byplane[s]))
        opp = sum(1 for a, wc, bo, ta in byplane[s] if wc[0] * wc[1] < 0)
        print(f"  plane {s} num {rec.line_num[s]}: births {len(byplane[s])}, amplitudes {amps}, W_children values {ws}, "
              f"births with opposite signs {opp}, W div (T div 2) per 10^9: {[abs(w) * BILLION // (T // 2) for w in ws]}")
    signs = [(w > 0) - (w < 0) for b in births for w in b["W_children"]]
    print("  senses' sum over all children", sum(signs), "children with W = 0", signs.count(0))
    # the law's letter for each row: W per quantum = T div 2; the quarter-turn lay's A^2
    print("the law's W per quantum T div 2 =", T // 2)
    # credits
    decoded, right, within, floors = decoder.decoded_credits(rec)
    per = {}
    senses = {}
    for c, name, x in decoded:
        per.setdefault(c["line"], []).append(x)
        senses.setdefault(c["line"], []).append(c["sense"])
    print("credits decoded", len(decoded), "right", right, "within floor", within)
    mids = {}
    for line in sorted(per):
        xs = sorted(per[line], key=cmp_to_key(decoder.cmp_rat))
        m = decoder.middle(xs)
        mids[line] = m
        n, d = m
        num = rec.line_num[line]
        print(f"  plane {line} num {num}: credits {len(xs)}, senses sum {sum(senses[line])} (+{senses[line].count(1)} / -{senses[line].count(-1)}),"
              f" middle solve x per 10^9 = {n * BILLION // d}, typed num/den per 10^9 = {num * BILLION // den}")
    # the legs (sines) of the decoded middle points against the typed legs, ratios per 10^9
    gapped = [l for l in sorted(per) if rec.line_num[l] != den]
    if len(gapped) >= 2:
        legs_typed = {l: sine_den(rec.line_num[l], den) for l in gapped}
        legs_dec = {}
        for l in gapped:
            n, d = mids[l]
            # the decoded cosine n/d; the leg den sin = largest_below(den^2 - (n den / d)^2) in integers: scale by d
            x = min(n * den // d, den)  # a decoded cosine above 1 (within the floor) read at the circle's edge
            legs_dec[l] = sine_den(x, den)
        order = sorted(gapped, key=lambda l: legs_typed[l])
        a = order[0]
        for l in order[1:]:
            print(f"  ratio legs plane {l} / plane {a}: typed {legs_typed[l] * BILLION // legs_typed[a]} per 10^9,"
                  f" decoded (middle points) {legs_dec[l] * BILLION // legs_dec[a] if legs_dec[a] else None} per 10^9")
    print("run back", run.get("run_back"), "counts", run["counts"])

if __name__ == "__main__":
    main(sys.argv[1])
