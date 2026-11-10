# E11 — Moving light clocks: the beat of two exact diagonal light waves ticks at Ω = ω′√(1 − u²/c_s²), c_s = 1/√3, an identity of exact linear dispersion

## On the event board
- coupling +++ (reference), quiet vacuum (0,0,2); one triple on all 48 channels per site (A1 light; main: one
  plane_light@1 placement, control: all48_site@1 placements); data only, nothing acts after t = 0 except Rule3
- main_diagonal_L6 (24 updates): four light clocks, one per body-diagonal family n = s·x. Each clock is a forward wave
  f(n − t) plus a backward wave g(n + t) with exact integer profiles 2cos(2πjn/6). The (j_f, j_b) pairs are (2,1) on
  (1,1,1), (1,1) on (1,1,−1), (1,2) on (1,−1,1) and (2,2) on (−1,1,1)
- on these families u is a multiple of 3, so r never changes and Rule3 is exactly the d'Alembert equation. These
  waves move at exactly c_s = 1/√3, at every amplitude and wavelength [THEOREM, r03 L4; r25]
- control_generic_L5 (24 updates): a light clock along z under a transverse standing wave cos(2πx/5), lattice-scale k,
  not a diagonal family (rounding active)
- the light clock is transversely extended (plane waves); the linear layer has no localized light clock

## In the clicks
- decoder (click_decoder_v1 1.0): main: all 185,856 clicks are C0, and the whole record is exactly periodic with
  period 6 = L. Control: C1 and C2 occur (46,800 and 47,520 clicks)
- decoder layer beat_clock_v1 (click_decoder_v1 release 1.0.3, frozen; it reads step, address and quotient of the
  official log and the phases of the channel-0 quotients on declared wavevectors):
  - d1: u = +c_s/3; the clock rate at the in-phase point is Ω = 1.396263 = ω′√(1 − u²/c_s²) (ratio 1 to 2e-16).
    d3: u = −c_s/3, the same rate (two diagonals agree)
  - rest clocks d2, d4: u = 0, Ω = ω′ = π/3 and 2π/3
  - control: Ω/Ω_SR = 1.41 (no SR at the lattice scale)
- ratio 1 is an algebraic identity of exact linear dispersion (R10G-36): the run tests the d'Alembert law on the
  diagonals, not an independent γ; the decoder itself sees only C0 clicks and one period-6 source

## Claim
- [THEOREM + SIMULATION] A light clock (the beat of two light waves) ticks at Ω = ω′√(1 − u²/c_s²), with ω′ the pair's
  invariant rest frequency, exactly on the body diagonals at every k. The γ(c_s) rate holds for clocks made of light;
  band matter has its own c_b (r25 T8).
- band matter dilates with its own c_b, never exactly c_s at cone-free Γ/R or isolated nondegenerate extrema (r25 T8,
  Lindemann); the best isotropic band in r25's scan reaches 0.969 c_s
- no Lorentz-covariant vertex exists (r25 V: Rule3's rounding is amplitude-independent), so this is **free kinematics
  in the lattice frame, not interacting Lorentz invariance**; the board is not boosted
- limits: the exact core consists of 1+1D clocks along the diagonals, with lattice-scale rates (Ω ≈ 1–2 rad/update).
  The generic-direction (isotropy) supplement, L = 96, is not part of this experiment and was not checked by the
  referee (R10G-37). The clock is transversely extended
- referee: r10g R10G-35 CONFIRMED (the package); R10G-36 CONFIRMED as measured, an identity of linear dispersion

Reproduce: python -m research.matter_light_experiments_v1.verify E11_light_clock_dilation
