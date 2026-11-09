# E23 — Prescribed flat FLRW in clicks: on r70's static fibre-light lattice with a(η) written into its tape clocks, radar echoes return exactly 2χ later and O's dial keeps the prescribed schedule

## On the event board
- coupling +++, vacuum (0,0,2), L = 4096 (EdS also on 2L, same sites), T = 1,200; r70's rung-E9 boards as ONE
  guide_net@1 placement per hardware version (registry wave 13; r70's init files byte for byte): fibre light, one-way
  A-pulses (1,0,−1), speed 1, on a static, comoving relay lattice; board time = conformal time η; no action after t = 0
- standard clocks are TAPES: per station a +x fibre whose A-pulses pass its tick node J0 at prescribed updates η_k, so
  a(η) = dτ/dη is written into the packet positions (prescribed, as E10's node counts): EdS (dust, 48 ticks), RAD
  (radiation, 50), STATIC2 (every 36), CYC (a = 0.06(1 − cos 2πη/600), 600-node tape rings), DARK (none)
- stations on +y: O with four radar U-paths (χ = 40, 80, 120, 160), S100, S300, S600 (one A-pulse per tick to O), S160
  (clock only); two 16-node rings. Projection layers declared before decoding: O's plane y = 600 (O's dial, radar nodes,
  receivers); for E9-2 the dial line x = 1310, z = 100

## In the clicks (decoder 1.0 checks; log_symmetry_v1)
- O's dial keeps the prescribed schedule in EdS, RAD, STATIC2 and CYC: one head passage at each scheduled update
- exact light times (E9-1) in every run: every radar echo exactly 2χ after a departure (χ = 40, 80, 120, 160); every
  reception at O exactly h + χ after a tick of O's dial (χ = 100, 300, 600)
- in EdS every station's dial ticks with O's (E9-2); CYC: O's dial, and the echo and receiver records of updates 1–600,
  recur 600 later; DARK: no click; STATIC2 likewise exact; L = 2L: the same click records on the whole board (0 differ)

## Claim
- [SIMULATION] the decoded times. [THEOREM, by construction] the exact FLRW light laws "hold BY CONSTRUCTION: light time
  is the node count, and a(η) is written into the tape clocks" (E9-1..E9-4, r70 §10; PROOF CHECKED, r68 D31)
- reported, not computed by this package's checks (r70; R10ZF-5..7; GR-F8, GR-F10), from the decoded times: radar R =
  ½∫a dη, read at the radar midpoint τ_mid = (τ_dep + τ_echo)/2 and interpolated linearly; R/χ = a(1 − (5/3)x) is first
  order in x = χ²/η² at fixed τ_mid; 1 + z = ∫_rec a / ∫_em a, = a_r/a_e in 177/177 constant-rate intervals, an identity
  of the piecewise-linear dial once E9-1 holds, finite intervals within −7 to +8 % of the continuum; Hubble: "v/R spread
  3–9 %; board within ±7 % of the same estimator on the continuum (EdS ±6 %, RAD up to +6.6 % at τ = 30, χ = 40)";
  Einstein-synchronisation defect, EdS: "always > 0; its continuum value is 3η_Rχ²/C³; board values are 0.58–1.47× that
  at χ = 40, 0.94–1.05 at χ = 80, within ±3 % at χ ≥ 120"
- CYC, reported (R10ZF-8, GR-F8; no ring detector declared): "every station dial is exactly periodic with period 600;
  every light record repeats 600 updates later; the second cycle also receives light emitted in the first, so the first
  cycle is a start-up transient; the board's own 16-node rings are not 600-periodic (600 = 37·16 + 8); the big clock is
  the prescribed ring tapes, not the board"
- prescribed a(η) in the tape clocks, not caused by matter; the board's own ring clocks see no expansion; not claimed:
  the board expanding, FLRW shown by the board, isotropy, curvature; Olbers (a sourced optical analogue)
- referee: R10ZF-1..6, 9, 11 CONFIRMED, R10ZF-7, 8 PARTLY (W1–W8); fresh machine 1 GR-F8 (8/8 CONFIRMED; fixes 1–3
  applied); fresh machine 2 GR-F10 (runs, dials, redshift and radar rows CONFIRMED; its two band refinements applied)

Reproduce: python -m research.matter_light_experiments_v1.verify E23_flrw_in_clicks
