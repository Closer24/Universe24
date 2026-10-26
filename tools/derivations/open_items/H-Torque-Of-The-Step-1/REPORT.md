# H-Torque-Of-The-Step-1: where in the step's letter the torque is born (2026-10-26, 03:0x to 03:4x UTC; engine 38655ef18; project NatureFirst, item A1)

**Verdict: A FINDING.** The torque on the board's L is located to its acts by name and to the integer, by an identity exact on every interval of every record read (hole 60, chiral 60, ga2 450, bodies 300): the step's change of 2 L across the riding lines' divisions is the sum of seven local terms, each a function of a Link's two ends and their six Links. The largest terms are the Link coupling's symmetric part at a non-uniform content (the well's gradient, read alike from both ends: 164 x 10^21 of the hole's 176 x 10^21 per component, 38 of 60 intervals the largest term) and the swap (226 x 10^21, larger than every division term on 27 of 60). The term a symmetrisation would remove, the coupling's asymmetric part (the pace not shared by the Link's two ends), is 21 x 10^21 on the hole, one eighth of the step's change; the rounding's term is 2 x 10^21, under one per cent of its bound. No local form of the step reaches the conservation of the records' L: the torque is the well's own (the Node's content in the record's coefficients, the same at both ends), which is nature's torque of a non-central potential on a body; what nature conserves is the body's L with the source's recoil, and the source here, the carrier's row, has no Links and so no momentum density MV-S1 to carry a moment. Named missing: a moment of the carrier's recoil. No form was built; the uniform boards, the 48 and the run back were not rerun (nothing changed under src/).

## 1. The algebra (THE_WAY step 1)

The reading (am1/am2, kept): 2 L_c = SUM over Links (i, i+a) of eps_cba d_b(i) p_a(i), p_a(i) = 2 num SUM_lines (now_(i+a) before_i - now_i before_(i+a)), d = 2 x - (c - 1) the doubled offset from the cube's centre.

**The step's letter as built** (interval.kick, interval.division): a riding line's momentum is read at the carrier's mean wall before the carrier's act, Wb = scale (w div 2)(X_before + X_now), p = Wb (now - before) + rem - Wb div 2 + X F, and divided at the mean wall after it, W = scale (w div 2)(X_now + X_next): W v + rem' = p + W div 2, next = now + v. So exactly, at every Node and line,

  2 W (next - 2 now + before) = 2 (X F + rem - rem') + (Wb - W)(2 (now - before) - 1),

the force F = SUM_j R_ij (m_j - now) - D now + curl term, m_j the arrival turned by the Link's record. Write g_i = next_i - 2 now_i + before_i (a rational). The Wronskian's identity gives, per Link, delta p_a(i) = 2 num SUM_lines (g_(i+a) now_i - g_i now_(i+a)): the 2 now - before part conserves every p_a(i) line by line, and the whole of the step's change of L is a sum over Links of local terms, one per term of g:

| term | g_i | the act | where it lives |
|---|---|---|---|
| ride | (Wb - W)(now - before - 1/2) / W | the content's own motion within the interval (the carrier's act between the kick and the division) | the Node |
| rounding (b) | (rem - rem') / W | the dropped remainder of the division | the Node |
| mass | -(X D / W) now | the Node's clock p_0 in the record's mass | the Node |
| link sym | SUM_j Ks_ij (now_j - now_i), Ks = (K_ij + K_ji)/2, K_ij = X_i R_ij / W_i | the coupling read alike from both ends: the content's gradient | the Link |
| link asym (c) | SUM_j Ka_ij (now_j - now_i), Ka = (K_ij - K_ji)/2 | the pace the two ends do not share (p_i^2, X_i, W_i the Node's own) | the Link |
| curl | (X / W) term_i | the potential's odd lines rotating the row | the Node |
| turn | (X / W)(arrivals turned - plain) | the Link's record turning the arrival | the Link |

Then the lays' write (the emission on the emitter's line, the current on the potential), the swap (d) and the close (a), each the integer difference of the reading before and after the act.

**What vanishes by the letter.** (i) The 2 now - before part: exactly, line by line (the Wronskian). (ii) Every term with a uniform coefficient: at a uniform content K_ij = K_ji and K, D, W, X the same at every Node, so Ka = 0, the mass term's torque is 2 num m SUM_rings now_i now_(i+a)(1 - 1) = 0, and the link_sym and ride terms telescope along every closed ring of the torus with the arm d_b fixed along the ring (ga2 450: every term 0 at 450 of 450; the bodies 300 of 300). (iii) The curl term: 0 at every interval of every record (a plane row has no axis matrices). (iv) The lays: 0 on the hole 60 of 60, on ga2 450 of 450, on the chiral 54 of 60 (the emission laid on the emitter's line moves its current where the emitter row has a current). A Link's current lies along its own axis, so a change along the Link has no moment about the Link's own line; the torque is born where a Node's g_i differs between a Link's two ends with an arm d_b transverse to the Link: every term above does that at a non-uniform content, and none of them moves momentum across axes by itself; the cross-axis move is the swap's (the turned Node's lines exchanged and conjugated: its six currents negated at once) and the click's take.

**What carries a remainder and its bound.** The rounding's g lies in (-1, 1) in level units, so |delta 2 L_c| <= SUM over Links |d_b| 2 num (|now_i| + |now_(i+a)|) per line; measured 2.0 x 10^21 against the bound 4.1 x 10^24 on the hole, 3.8 x 10^21 against 3.6 x 10^24 on the chiral: under one per cent of the wall's room. The other six terms are exact rationals of the paces, not remainders.

## 2. The measurement (step 2; tq1_torque.py; the records of 2ab32b518; about the doubled centre; integers and Fractions of integers, no float)

The identity (the divisions' integer change of 2 L = the sum of the seven rational terms) holds at 60 of 60 intervals on the hole and 480 of 480 lines, 60 of 60 and 480 of 480 on the chiral, 450 of 450 on ga2, 300 of 300 on the bodies. The sums of the absolute per-interval values per component (x, y, z), the integers in out/summary.txt:

- **hole 60**: step (the divisions) [7.7e21, 176.2e21, 176.2e21]; ride [2.9e21, 52.6e21, 52.6e21]; rounding [1.3e21, 2.0e21, 2.0e21]; mass [0.14e21, 0.50e21, 0.50e21]; link_sym [6.7e21, 164.4e21, 164.4e21]; link_asym [1.2e21, 21.1e21, 21.1e21]; curl 0; turn [8.4e21, 3.3e21, 3.3e21]; lays 0; swap [4.7e21, 226.0e21, 226.0e21]; click [2.1e21, 1.8e21, 1.8e21]. The largest division term: link_sym on 38 intervals, ride on 12, turn on 10; the swap exceeds every division term on 27 of 60. L_y = -L_z at every interval (the hole's transposition, the board hands' finding, reproduced).
- **chiral 60**: step [202e21, 194e21, 186e21]; ride [66e21, 68e21, 81e21]; rounding [2.4e21, 2.7e21, 3.8e21]; mass [0.55e21, 0.79e21, 0.75e21]; link_sym [165e21, 189e21, 134e21]; link_asym [39e21, 47e21, 43e21]; curl 0; turn [33e21, 46e21, 41e21]; lays [0.08e21, 0.16e21, 0.14e21]; swap [319e21, 244e21, 224e21]; click [5.9e21, 7.2e21, 7.3e21]. The largest division term: link_sym 31, turn 24, ride 5; the swap exceeds every division term on 35 of 60.
- **ga2 450**: every term 0 at 450 of 450 (2 L = 0 to the bit through the 64 births and the returns), the clicks' moment 0, P_z the births' net recoil 8.87e22 unreturned (ac2's reading reproduced).
- **bodies 300**: 2 L = 0 to the bit at 300 of 300 intervals and every term 0 (the two packets mirrored about the centre; 197 clicking intervals, 238 with a swap, 4,229 turns), the identity 300 of 300.

Exact integers (one sample, the hole, interval 6, component y): the divisions' change 18,2xx x 10^18 = ride 5.56e20 + rounding -4.27e19 + mass 0 + link_sym 1.79e22 + link_asym -2.08e20 + curl 0 + turn 0, the integers in out/hole_60.json under per_interval[5].terms. The term that carries the torque, named: the Link coupling's symmetric part at a non-uniform content (the well's gradient), and the swap.

## 3. A local form (step 3)

The task's two candidates: (i) a rounding whose dropped remainder is kept on the same axis: the rounding's term is 1 per cent of the step's change and under one per cent of its bound; removing it leaves 99 per cent. (ii) a pace read from both ends alike (Ka = 0): removes link_asym, 12 per cent of the hole's and 22 per cent of the chiral's step change; it leaves link_sym, the ride and the turn, which are read alike from both ends already. The ride is the carrier's own motion; link_sym is the content's gradient entering both ends' reaches alike (the law's gravity: a body's clock and Link pace from the content it stands in). These are what nature's non-central potential does to a body's L: the torque is physical and the law's, not a defect of the step's rounding or of a one-sided read. So no local form of the step's rounding or paces reaches conservation of the records' L on a seed without the symmetry, by the letter: the term that cannot be removed by a local change of the step is the content's gradient in the coefficients (link_sym with the ride), and the swap's exchange at the turned Nodes (a Node's own act negating its six currents; 226e21 on the hole, the largest mover). Nothing built, nothing flagged.

What conservation would need, by name: the moment of the source's recoil. The carrier's write (held_numerator, the traceless stress on its axis lines) is the recoil of the content under the records, local at the Node, but the carrier's row has no Links (rule_of: its own wall, no reaches) and so no MV-S1 density and no moment. Whether a reading of the carrier's recoil as a momentum on the Links exists in the letter is the next derivation; it is a reading, not a form of the step, and it is not proposed here.

## 4. The laws with a number (step 4)

The one-Link reach: every term is a function of a Link's two ends and their six Links (K_ji read across the Link back, K[port ^ 1] across port). Integers only: the reader holds Fractions of Python integers, no float; the identity is checked as integers (2 W (next - 2 now + before) against 2 (X F + rem - rem') + (Wb - W)(2 (now - before) - 1)). 128 bits: unchanged, no state written. The fixed count: unchanged. The run back: untouched (no act). No commit, no push, nothing under src/ or tests/.

## 5. The sentence and the row (step 5)

**TQ-S1, 2026-10-26 (a reading's clause, no act; for the Scribe under the clicks' and the board's clauses; not for approval here):** the step conserves the moment of the lattice momentum density MV-S1 exactly where its coefficients are uniform along every ring of the torus (the 2 now - before part line by line; the reaches, the mass, the mean wall and the content telescoping with the arm fixed along the ring) and on every seed with the cube's symmetry (ga2 450 of 450, the bodies, the uniform boards: 0 to the bit); where the content is not uniform the step's change of the moment is the sum over Links of seven local terms, each a function of the Link's two ends and their six Links (the ride, the rounding, the mass, the coupling's symmetric and asymmetric parts, the curl, the turn), the identity exact at every interval; the torque is the content's gradient read alike from both ends (the well's) and the swap's exchange at a turned Node, not the rounding (under one per cent of its bound) and not the one-sided read of the pace alone (one eighth); the clicks change the moment by their take alone (AJ-S1). The conservation of the records' moment alone is not in the letter and no local form of the rounding or the paces puts it there; the source's recoil carries no moment, the carrier's row having no Links.

The row for the gates of the phenomena, "the conservation of angular momentum": NOT SHOWN; the torque located to its acts (TQ-S1), the identity SHOWN at 60 of 60 (hole), 60 of 60 (chiral), 450 of 450 (ga2); reader tools/derivations/open_items/H-Torque-Of-The-Step-1/tq1_torque.py; test test_tq1_torque.py (1 test, 1.1 s).

## 6. The ledger row and what is missing (step 6)

| item | derived | one-Node test | toy | gates | spec | missing by name |
|---|---|---|---|---|---|---|
| the torque of the step (tq1) | a finding: the step's torque the sum of seven local terms, exact; the well's gradient (link_sym with the ride) and the swap the carriers; the rounding under 1 per cent of its bound; no local form reaching conservation | 1 test, 1.1 s | hole 60, chiral 60, ga2 450, bodies 300 | a row NOT SHOWN, the identity SHOWN | TQ-S1, a reading | the moment of the carrier's recoil (the source has no Links); the swap's torque as a form; the second blind hand's reading |

Runs cut short: none; the bodies 300 ended at 300 of 300 (121 s). No form built: the uniform boards bit for bit, the 48 on the chiral 3-cube, ga2's 64 births and the run back 10 of 10 were not rerun, the head being unchanged.

Files: tq1_torque.py (the reader), tq1_summary.py, test_tq1_torque.py, out/*.json (the per-interval integers), out/summary.txt, out/*.log.
