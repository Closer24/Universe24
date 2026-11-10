# beat_clock_v1 as a frozen layer of click_decoder_v1: pre-registration (r17)

Written 2026-11-09 04:24 UTC, before the layer copy, its tests and its validation logs exist. Ruling: r16b on E11
(coordinator 04:06): r25's observer `beat_clock_v1` becomes a separately frozen layer of click_decoder_v1, like
the sign layer, with its own pre-registration, validation cases that are not E11's own logs, FROZEN file and tests.
Developed in `research/matter_light_v1/r17/layers_dev/`, outside the released package.

## The layer
* Code: `layers_dev/beat_clock_v1.py`, a byte-identical copy of r25's observer
  (research/matter_light_v1/r25/experiments_proposal/beat_clock_v1.py, SHA-256 05d9d495...; r01c's
  observers/ copy is the same file). The algorithm is not changed, so E11's pin (code_sha256) names the same
  bytes. It reads from each record only step, address and quotient; a declaration gives side, steps, channel,
  optional detector sites and per clock K1, K2, axis e and c; it reports omega_1, omega_2, the chord speed u,
  Omega, the rest frequency w', Omega_SR and the ratio Omega / Omega_SR.
* Reporting: separate from the decoder report, as r01c's mechanics do (pointer into `/clocks/<i>/<field>`, the
  `approx` and `not_approx` operators with a declared tolerance).

## Validation cases (none of them is an E11 log; made with r25's own data-only builders and the official CLI)
Preparations: r25's `preparations_e11.main_diagonal(side, clocks)` and `generic_clock(side, n1, n2, M)`, reference
coupling +++, 24 updates, `python -m universe24 --audit --events`, under runs/matter_light_v1/r17/beat_clock/.
* B1 main_diagonal at L = 12 with every wavenumber doubled (d1 (4, 2), d2 (2, 2), d3 (2, 4), d4 (4, 4)): the same
  wavelengths as E11's L = 6 board, four times the sites per family line. Declarations as E11's main run (K in
  radians per site unchanged). Expected (tolerance 1e-9): d1 u/c = +1/3 and ratio = 1; d3 u/c = -1/3 and ratio = 1;
  d2 Omega = pi/3; d4 Omega = 2 pi/3.
* B2 main_diagonal at L = 6 with the forward and backward wavenumbers of d1 and d3 swapped (d1 (1, 2), d2 (1, 1),
  d3 (2, 1), d4 (2, 2)): d1 u/c = -1/3 and ratio = 1; d3 u/c = +1/3 and ratio = 1; d2 Omega = pi/3; d4
  Omega = 2 pi/3 (tolerance 1e-9).
* B3 generic clock control at L = 7, (n1, n2) = (1, 2), M = 1000 (rounding active), detector sites (0, 0, z),
  K1 = (0, 0, 2 pi/7), K2 = (0, 0, 4 pi/7), axis z, c = 1/sqrt(3): |ratio - 1| > 0.01 (not_approx 1.0, tol 0.01).
* B4 synthetic (tests): a relativistic pair gives ratio 1 (1e-6); a standing wave gives u = 0 and Omega = omega;
  a Galilean dispersion is detected (|ratio - 1| > 1e-3); an empty log gives "no clock"; dict and tuple records
  agree; the layer copy is byte-identical to r25's file.
Failures are recorded; the layer is frozen before B1-B3 are run with it.
