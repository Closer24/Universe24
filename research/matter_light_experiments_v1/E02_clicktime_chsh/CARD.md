# E02 — CHSH with light approvals: board-time S = 2, click-time S = 4 (a PR box, not quantum)

## On the event board
- board: side 256, coupling +++ (reference), quiet vacuum (0,0,2)
- prepared at t = 0: two guided fibres F_A (y = 40) and F_B (y = 56) at z = 64, unit pulses (1,0,−1) on them,
  and two phase gates (all-48 period-4 dark clocks two sites beside a fibre node): G_A at x = 96 with its phase
  set by the setting x, G_B at x = 56
- runs: 16 = 2 arrangements × settings x, y × hidden λ; y = 1 adds B's setting pulse on F_A, λ shifts both
  source pulses by 2 updates (equal weights, independent of the settings); 80 updates each
- "separated": A's source pulse reaches G_A at 16/18, before B's setting pulse can (board-time separation);
  "signal": the setting pulse reaches G_A at 36, inside the same approval interval, before A's source at 56/58
- after t = 0 only Rule3 acts; nothing is injected or read back

## In the clicks (click_decoder_v1 1.0, frozen 2026-11-09 01:29 UTC; official click logs only)
- detectors (detectors.json, r08's rule fixed 00:35): a station clicks if the decoder's detector region (Chebyshev
  ≤ 3 around its gate, the fibre line's channel 0 excluded) has a click in the station's window [t+1, t+8] after
  its own source pulse arrives (t = tA or tB); outcome +1 if it clicks, −1 if not
- `derive: chsh` (decoder `chsh`, all four labellings): E per setting over λ, S, marginals; decoded: separated
  E = (+1, +1, −1, −1), S = 2; signal E00 = +1, E01 = E10 = E11 = −1, S = 4; every marginal 1/2
- board-local mechanism read from the clicks: with x = 0, y = 1 the setting pulse is absorbed at G_A between
  approvals (clicks in [37, 48]); with x = 1 it passes

## Claim
- the gate law [THEOREM, r08]: an all-48 period-4 dark clock two sites beside a fibre node absorbs a unit
  pulse whose head passes at t ≡ 1, 2 (mod 4) if it is (−1,−1,0), at t ≡ 3, 0 if it is (1,1,0), and is
  exactly transparent otherwise; an absorption flips its window (a 1-bit record)
- [SIMULATION] 16 native runs: board-time separated stations give
  E = (+1, +1, −1, −1) and S = 2, the local bound. Registering outcomes only at the approvals, while a board signal
  crosses inside one approval interval, gives E00 = +1, E01 = E10 = E11 = −1 and S = 4 in click-time: a PR box,
  beyond Tsirelson's 2√2, with uniform marginals 1/2 for every setting.
- This is **not** a quantum result: it shows that click-time can hide board-local signalling. The assumption
  that changes is the locality proof's assumption 3 (the remote setting outside the readout's backward cone in
  board-time). A principle that limits board signalling within one approval interval is still missing.
- referee: r10e R10E-39 CONFIRMED
- limits: 8 deterministic trials per arrangement with a two-valued hidden variable; prepared fibres and gates;
  single approvals only (approval streams lose exclusivity through the gates' 1-bit records, r08 W9)

Reproduce: python -m research.matter_light_experiments_v1.verify E02_clicktime_chsh
