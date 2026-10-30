# t11_math: hostile reading of CLICK25.md sections 0, 2, 3, 6 (term 11's count)
Started 2026-10-30. Findings saved in numbered small files as they come.

Plan:
1. Read CLICK25.md (done), NOTES.md, probe_wind.py/.txt, probe_count.py/.txt, halftooth.py, common.py, plan.py
2. Read TERM11.md + readers; EDGE.md "Owner's word"
3. Read engine: carry, step, state, mirror/untick, runner (click writing)
4. Rerun probes; check the per-gear identity W D = W q v - a J - a (r - r+) symbolically and numerically
5. Check mirror-evenness of D (a_t^2 - a_{t-1} a_{t+1}) -- exact or only in this world?
6. Check count's carry: k_0 = (key-1) div 2; birth; books; the two misses
7. Check run-back claim ("no hold survives")
8. Key parity: CLICK25 (births sum 2 key - 1, odd key) vs EDGE (born 0, mirrored by negation) -- measure
9. Build adversarial cases
10. REPORT.md

## Rerun (done)
probe_count.py -> rerun/probe_count.txt: byte for byte with click25/probe_count.txt (3.6 s)
probe_wind.py  -> rerun/probe_wind.txt:  byte for byte with click25/probe_wind.txt (5.7 s)

## First algebra notes (by hand, to be measured)
- Per gear: W q + r+ = W v + push + r (v = a - b), a+ = a + q. D = a^2 - a+ b = a(v - q) + q v;
  W(v - q) = r+ - r - push  =>  W D = W q v - a push - a (r - r+). EXACT; the text writes J for push,
  which is the special case s = T_k = T_d = 1 and no Mesh force (Animate's world). General: push.
- SUM(W q v - a J) = W v+.v- + 2V = 2 E_shadow (E_shadow = (W/2) v+ v- + V is the exact invariant of
  the EXACT leapfrog for quadratic V). The act's drift is rounded, so E_shadow is NOT an invariant of
  the act; W(D_L + D_M) = 2 E_shadow - SUM a (r - r+): two Rule3 terms, not one.
- D even under the mirror: mirror(s_{t+1}) = (a_t, a_{t+1}); its tick gives a_{t-1} iff untick exact;
  then D_back = a_t^2 - a_{t-1} a_{t+1} = D(t). A consequence of the exact run back, not a measurement.
- Count n = floor((x + k0)/key), x = D - D_lay. Odd key 2m+1, k0 = m: n = nearest integer to x/key, no ties.
  Even key 2m, k0 = m - 1: x in [n key - m + 1, n key + m] -> n (rounds half up).
- Pair with x_L + x_M = 0 exactly: odd key -> n_L + n_M = 0 always; even key -> -1 when x_L = n key + m.
  With x_L + x_M = delta (the wobble): a miss whenever x_L lies within |delta| of a cell boundary.
- Half-tooth form (sec 3 Algebra): n = floor((2x + key)/(2 key)); even key rounds half DOWN; pair sum
  = +1 when 2x + key = 0 mod 2 key. The text's statement is right for the stated rule.

## Probe A (probe_a.txt), first run: identity exact 72,000/72,000; D even 6000/6000 (theorem); count: -6/+6, 0..7,
35 click rounds, 2 misses = ONE event (t=216: giver -1 while x_L = -0.500432 key, x_M = +0.499655 key, delta = -776
millionths; t=217 taker +1, books closed again): the books open for exactly 1 round. The wobble delta in
[-1855, +1712] millionths, per-round change up to 3351 (it alternates sign fast). My first n_half_even was wrong
(dial 2 key on x not 2x) -> fixed; rerun.
## Key insight for probe C: in EXACT arithmetic the hand's wind change per round is
2 dE_M = g (M_{t-1}.L_t - M_t.L_{t-1}) = g (b_M.a_L - a_M.b_L) =: X_M, and X_L = -X_M by construction (same g,
symmetric dot). X reads now and before only (no next), is odd under the mirror (a <-> b), whole. A tooth-carry on
X_h closes the pair's books EXACTLY (TERM11's pair theorem) and runs back exactly with the tooth KEPT (not flipped):
-X + k+ = -q key + k. This contradicts "no hold survives the run back" / "no third dial" and gives a wind count
with exact books and a free hand that never clicks at any swing. To measure.
