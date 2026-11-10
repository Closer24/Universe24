# E17 — an exact bounce: one JR-fixed state s*, whose contraction and expansion are mirror images in the clicks

## On the event board
- board: L = 640 and 2L = 1280; coupling (−,+,+) (reference); quiet vacuum (0,0,2); compositions/*.json of registered
  blocks: E16's board reduced to zero-counter hardware (matter and light lines, the hz and h1 rings, tap fibre, bridge),
  the two all-48 phase gates at phases 3 and 1, and one 20-cell literal patch with the bang cell set to the vacuum
  triple; no analysers, trap cores or recorders
- [THEOREM + check] JR(s*) = s* on the whole board, JR(a, b, r) = (−b, −a, r); since JR∘F∘JR = F⁻¹, the past of s* is
  the JR image of its future, X₋ₜ = JR(Xₜ) (checked natively for t ≤ 240 by the source researcher); the composed s*
  equals that researcher's init file and is JR-fixed, and its 240-step rewind equals the recorded bounce start
- runs: forward from s* (240 updates, L and 2L); bounce: 240 exact rewinds of s* before t = 0 (a preparation, not a
  stage of the run), then 480 updates (L and 2L), ending in the forward run's final state (same SHA-256); control: the
  unsymmetrized bang (the A0 node at O at (−1,−1,4); not JR-fixed; 17,407 click records differ from s* over 240
  updates on L = 320), its bounce on L; after t = 0 only Rule3 acts, nothing is injected or read back

## In the clicks (official click logs; decoder 1.0 and its released layer log_symmetry_v1)
- forward from s* (decoder 1.0): the h1 ring clock and the hz ring are created sources of period 22 and 36, born at 48;
  lamp light tracks at exact +1 born at 60 + 18k; probe tracks at exact −7/11 against the stream (T81 born 154, T107);
  exact speeds 1, 1/3 and 7/11; the z-ring reader passes at 58 + 18k (k = 0..6); the same on 2L, 24,915 records each
- the period-10 source at the single site (0,12,3) over [166, 207] in forward_L640 is used by no claim
- the bounce (log_symmetry_v1 1.0.3): a mirror about τ = 240, every record
  (t, x, k, q) paired with (481 − t, x, −k mod 3, −q): 49,830 records, 0 unpaired, 480/480 updates mirrored, on L
  and 2L; the best moment read from the log alone is τ = 240, unique
- control: the unsymmetrized bounce is no mirror: 78,572 of 97,636 records unpaired about 240,
  0/480 updates mirrored; its best moment (τ = 72) leaves 73,914 unpaired

## Claim
- [THEOREM + SIMULATION] (r27b, declared 2026-11-09 03:54 UTC): a JR-fixed state bounces exactly: the board's click
  record before t = 0 (light converging, rings un-lighting) is the mirror of its record after t = 0, up to C1 ↔ C2
  and q → −q, so the record after t = 0 determines the whole two-sided record
- inside the bounce the forward half keeps a matched α_in = 1 instrument pair whose moving parts are all created: the
  probe (tap fibre, slowed by the lamp stream to 7/11) and the h1 ring clock (slowed by its own counter packet from a
  free 14, E16's calibration, to 22) are separate devices equal by design (s − 4 = R), not N(x) and v(x) of one medium
- referee: remote fresh-machine referee FRESH4-A1..A3 CONFIRMED (report 4); its addendum confirms the forward readouts
- limits: lost against E16: the common-cause pair (no analysers), the twin trap atoms (no cores, so no gate approval
  and no radar twins) and the recorder clicks; v1.0 reads the halves asymmetrically (one periodic run per site; the
  contracting probe at +7/11 is not an exact track although its clicks are mirrored); one bounce, not a cycle (the
  one-way hz ring has no second moment)

Reproduce: python -m research.matter_light_experiments_v1.verify E17_exact_bounce_v6
