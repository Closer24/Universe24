# E04 — Two-way Einstein synchronisation with created atom-clock candidates: t_B = (t1 + t2)/2 exactly

## On the event board
- board: side 240 (and 2L = 480), coupling (−,+,+) (reference), quiet vacuum (0,0,2)
- prepared at t = 0 (main run = published block `einstein_created_instruments_L240`): the seed's matter line A0,
  light lines B_A (y = 0) and B_B (y = −20), both gauge phase 1, a light-line link along y at x = −32, two traps
  (cores (−1,0,0) at x = −3 and 5, d = 8) on B_A and B_B, one SLOW seed glider (start ≡ 20 mod 4)
- runs: main L240, size check L480, controls no link / no seed / no cores (L240); 230 updates (size check 400)
- after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- two periodic sources of period 20 (the created atom-clock candidates A and B)
- stations (detectors.json, r08's rule fixed 23:14): the B-line nodes 6 (inner) and 7 (outer) sites outside each
  trap's link-side core; a passage = click-run onsets at the two nodes one update apart (outward: inner then
  outer; inward: outer then inner), read as the decoder's first click in declared windows
- decoded: two periodic sources of period 20; station onsets exactly as declared: A outward 66/67, B inward
  137/138, B outward 152/153, A inward 223/224, all eight the same on 2L = 480; no link: no inward click at B;
  no seed: 0 clicks; no cores: no periodic source; the two sources are born 60 updates apart (57 and 117)

## Claim
- [SIMULATION] native, r08 wave 8 (pre-registered 23:14): the seed creates atom clocks A (t = 62) and B (t = 122);
  A's formation packet leaves A's station at t1 = 66, is reflected at B at t_B = (138 + 152)/2 = 145 and is back at
  t2 = 224. So t_B = (t1 + t2)/2 exactly, and the Einstein offset −60 equals the true dial offset on the board's
  simultaneity. Each leg crosses one counter-propagating packet and is delayed by exactly 4, so the delays cancel.
- referee: r10e R10E-40 CONFIRMED
- limits: prepared lines, link and traps (structured vacuum); one clean round trip per run; the board's synchronous
  update is the simultaneity that the light exchange reproduces (no relativity beyond that); the station rule is
  r08's, read here through first clicks in declared windows

Reproduce: python -m research.matter_light_experiments_v1.verify E04_einstein_created
