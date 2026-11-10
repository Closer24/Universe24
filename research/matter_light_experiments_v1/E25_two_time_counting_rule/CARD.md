# E25 — Two-time counting rule: a second forward run from JR of a run's final state gives its click log in reverse order, kinds and quotients negated (C0 stays C0, C1 ↔ C2), on builder B's triple gate

## On the event board
- coupling (−,+,+) (reference), vacuum (0,0,2), L = 128; builder B's triple gate as ONE registered guide_net@1 placement
  (registry wave 12): x-, y- and z-fibres through one vacuum gap node X = (40, 40, 20), y and z in gauge sy, sz = ±1,
  the gate channel (X, 1) at gear g = 2 (vacuum), 3 or 4; on each line one separately prepared unit (1,−1) fibre
  packet (profile C; fibre light, r04 guide packets, speed 1), 12, 12 + Dy and 12 + Dz nodes before X
- run 1: 80 forward updates from x0. Mirrored run: a SECOND forward run of 80 updates from JR(x_T), the mirror image of
  run 1's complete final state ((a, b, r) → (−b, −a, r) on every channel, an official init file), not a rewind
- declared subset: (Dy, Dz, sy, sz) = (0, 0, +, +), (−4, 2, +, +), (−4, −3, +, −), (1, −1, −, +) × g = 2, 3, 4, all in
  the future condition B (+x exit occupied at T = 80): 24 runs; every mirrored run ends exactly at JR(x0) (tested)

## In the clicks (decoder 1.0 and log_symmetry_v1, official click logs; declared site: gate channel (40, 40, 20, 1))
- every member: run 1's first gate click (the statistic k) at update t1 with kind Ck, the mirrored run's last gate click
  at 81 − t1 with kind C(−k mod 3): k̄ = k in 12 of 12, with k = C0, C1 and C2 all present; the record totals agree, the
  C0 counts are equal and the C1 and C2 counts swap; gear 3 gives every click (t, x, k, q) of gear 2 (record_diff 0)
- builder B's picture, (0, 0, +, +), g = 4: run 1's gate word 12–15 C0, 58 C1, 59 C2, 62 C1, 63 C2, 78 C1, 79 C2; the
  mirrored run's 2 C1, 3 C2, 18 C1, 19 C2, 22 C1, 23 C2, 66–69 C0, nothing else: the word in reverse order, C1 ↔ C2

## Claim
- owner sentence (r10zc; UPDATE 46 item 22): "Universe24 runs backwards exactly in clicks. Prepare the mirror image (JR)
  of a run's final state and run the board forward again: it retraces the run, and its click log is the old log read
  backwards, with each click's kind and quotient negated (C0 stays C0, C1 and C2 swap). So click statistics conditioned
  on a past and a future equal the mirrored statistics with past and future exchanged. This is a theorem of the board's
  reversibility, confirmed on 972 + 485 runs. It is the time symmetry of any reversible deterministic system, classical
  mechanics included. It is not a quantum effect, no click acts backwards in time, and the quantum three-box two-time
  test (QX-4) fails on the board."
- [THEOREM M, R10ZC-9] JR∘F∘JR = F⁻¹: x0 ↦ JR F^T x0 maps A ∩ F^−T B one to one onto JR B ∩ F^−T JR A and each record
  (t, x, k, q) to (T + 1 − t, x, −k mod 3, −q), so P(k | A, B) = P(k̄ | JR B, JR A) for the counting measure, member by
  member; [SIMULATION] the 12 replayed members show it in their clicks
- reported, not replayed here (builder B QM-B8; R10ZC-7 on all 972 + 485 runs; QM-F5, 485/485, 48 CLI logs): A2 = A3:
  k = C0 36, C1 76, C2 33 of 145; A4: C0 15, C1 126, C2 54 of 195; the mirrored side equal in every table
- k is the first gate click; it is the click that records the outcome in only 270 of 318 g = 4 geometries (R10ZC-11);
  its C0 entries never reveal the gear (THEOREM G, R10ZC-2). A3 is the ε-twin of A2: every click (t, x, k, q) is
  identical; the gear cell's remainder differs by 1 (R10ZC-3, R10ZC-10)
- not claimed: a probability law or a selection (a counting measure on one finite prepared ensemble; C2 is an
  arithmetic class); a quantum effect; a click acting backwards in time; a backward run (both runs are forward)
- referee: r10zc R10ZC-7, 8, 9 CONFIRMED (9 is Theorem M); R10ZC-10, 11 wording applied; fresh machine 2 QM-F5 PASS

Reproduce: python -m research.matter_light_experiments_v1.verify E25_two_time_counting_rule
