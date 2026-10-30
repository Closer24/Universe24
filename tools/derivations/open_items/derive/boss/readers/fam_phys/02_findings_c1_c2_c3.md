# Findings from c1, c2, c3 (outputs beside them)

## c1_pairhand.txt
1. The board holds phi + chi up to the carry's rounding (1666 of 2160 gears differ by up to 10 notches on hands of
   ~10^3 over ten rounds). The "pair hand" is epsilon of two SEPARATELY RUN boards' hands: no Node-clock holds it.
2. Three splits of one board (phi at 0, 5 J phi at 13 = 2 J phi + 3 J phi): pair hands 833, 415, 270 thousandths.
   (Redo at 10x the size, c1b: the small lays are rounding-dominated.) Algebraically the splits differ by the factor
   |L phi|^2 / (|L phi|^2 + |L (2 or 3) J phi|^2): the number depends on how the prober divides one field in two.
3. Light's own kind (T1 at part 2, the engine's epsilon channel made bilinear over the part's i): one state 39
   thousandths, an orthogonal state 944. The text's "exclusion reading" holds for light.
4. I is four signed 2-cycles (four planes). The free act keeps each lay in its own plane (phi0, I phi0) to 22
   thousandths: scalar propagation of eight alike rows; the "same state 0" is kinematics of the lay.
5. The symmetric T1-valued pair hand (the text's own table) of two hands in one state: not 0 at 228 of 228, and
   larger than the partner's (768 : 430). "No pair hand" = "no A1 pair hand".

## c2_light.txt
- Free act: same state 10 / partner 921 (text reproduced).
- Generic table + random light: 144 / 634; w_I 12000 -> 28664 (text reproduced); SUM |h|^2 240000 -> 172146
  against the free act's 40370: light PUMPS the half-speed hand (4x) with no partner: winding made from light.
- Generic table + uniform light (100, -70, 40): runaway: SUM |h|^2 -> 48,369,655 (200x the lay), w_J -> 3,019,320;
  (37, 37, 37): SUM |h|^2 -> 268,327, w_J, w_K ~ 10^5. The generic table conserves no winding and amplifies.
- I-averaged table + random light: 44 / 825 (text); w_I 12000 -> 13003 (the free act's wander is 12223; the drift
  is the rounding at pumped size, SUM |h|^2 64671); w_J, w_K ~ 10^5 (not charges of the vertex: Sp(1) -> U(1)).
- I-averaged + uniform light: 40 / 670 and 22 / 922: the one-state pair hand rises above the free act's 10 even for
  uniform light, because the vertex pushes light at the matter's sites (every leg pushed) and the light is no longer
  uniform after one round; the control is contaminated by the back-reaction, which the law requires. In every
  I-averaged run SUM w_I stays within rounding: NO quantum is made; "a pair appears" is the two lays' inner states
  (the quartet's four complex components, mixed C_I-linearly by light) turned differently at different places.
- No beat, no spring (massless), static light: no threshold is askable.

## c3_doublers.txt
- Commutant of the 24-gear train: rank 24; the right-regular 48 are signed permutations commuting with the left 48,
  -1 = -I: an internal group of 48 on the "electron" (the doublers' symmetry).
- Whole pieces: Q_E (E1/2 + E5/2) rank 8, Q_G (G3/2 twice) rank 16; E1/2 alone is no whole sub-train.
- T1 in (E1/2 + E5/2) x G3/2 = 2; the text's own 24-gear table has 1728 nonzero entries in the E-G blocks: light
  converts doublet content into quartet content at no cost (one train). A click (term 11) sums the rows: blind.
- The eight-gear G3/2 holds no doublet (SUM chi_E trace M8 = 0).
