# E03 — Exclusive single-click detection: with one light approval exactly one of two detectors clicks

## On the event board
- board: side 200, coupling +++ (reference), quiet vacuum (0,0,2), device in the plane z = 100
- prepared at t = 0: an input fibre (channel 0 along +x) into a degree-3 junction at x = 70 (r04) with two arms A
  (+x) and B (+y); one quantum = one unit packet (1,0,−1) on the input; detectors = all-48 dark clocks (r08
  absorbers) two sites beside arm node 20 of each arm, D_A at (90,100,98), D_B at (70,120,98); the approval = one
  packet already on arm A that writes D_A before the quantum arrives (r03's D1)
- runs (5 of r13's declared families): approval with t_q = 24 and 25; no approval with t_q = 25; independent
  complementary detector phases (2, 0) with t_q = 23; no quantum (control); horizon t_q + 70
- the quantum's arrival phase t_q is a hidden, deterministic parameter; after t = 0 only Rule3 acts

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- detectors (detectors.json, r13's detector_click_v1 fixed 00:47/00:49): a detector fires if its clock site or
  the site between clock and fibre (all 48 channels) clicks in W = [t_q, t_q + 20]
- per run (decoder `correlations` on the declared detectors and windows), decoded: approval t_q = 24 → only A;
  t_q = 25 → only B; no approval t_q = 25 → both; complementary phases (2, 0) → only A; no quantum → none

## Claim
- the gate law [THEOREM, r08]: an all-48 period-4 dark clock two sites beside a fibre node absorbs a unit
  pulse whose head passes at t ≡ 1, 2 (mod 4) if it is (−1,−1,0), at t ≡ 3, 0 if it is (1,1,0), and is
  exactly transparent otherwise; an absorption flips its window (a 1-bit record)
- [SIMULATION] the five shipped runs, decoded: with the approval exactly one detector clicks (A at t_q = 24,
  B at t_q = 25); without it both click (t_q = 25); complementary independent detectors give exactly one; no
  quantum, none. r13's family statistics (α = 0 / 2 / 1 over 8 / 8 / 64 runs) stay in the program record until the
  families ship as a registry composition.
- The selection is set by the hidden arrival phase and the gates' clock phases: a deterministic, local overflow,
  counted over a declared family of hidden phases, not random draws. "One click selects one path" holds for one
  approval; the selection is a burst of clicks, and the unselected packet is not stopped.
- referee: r10e R10E-53 CONFIRMED
- limits: prepared fibres, junction and clocks; repeatability with a second detector pair failed on arm A
  (approval cross-talk) and the R_delta = 2 prediction failed (r13 E2, kept); the families need a composition with t_q
  and the detector phases as parameters before α can be read by the decoder

Reproduce: python -m research.matter_light_experiments_v1.verify E03_exclusive_detection
