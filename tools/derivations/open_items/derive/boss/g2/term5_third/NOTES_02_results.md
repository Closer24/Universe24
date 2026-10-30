# Working notes 02: the three blocking items' measures (out_e.txt, out_g.txt, out_w.txt)

## Item 3 (M-1, hypothesis (e)): CLOSED
- The swap identity on the edge: the mirrored round reads (sigma_in, sigma_out) = (-sigma_out, -sigma_in) of the
  forward round: 0 mismatches of 1,296 reads (12 rounds, 54 matter gears, strides up to 30, W moving).
- Cases built to pass rule (b) and still break: si^2 alone -> 00, so^2 alone, si(r0) so(r1) alone, si D_x alone ->
  0x: each (b) 1, (e) 0, holds 0 of 12, departs at round back 1 (the metric moved 1.6e7-3.4e7 counts by each
  case's push, so the push was live). Their swap-symmetric pairs: (b) 1, (e) 1, hold 12 of 12. si so alone is
  self-symmetric and holds. A (b)-breaking case departs; a (d)-breaking case departs.
- The shipped plan (76 terms at factor not 0) passes (b) and (e) by the predicate and runs back 12 of 12.

## Item 1 (P-1, M-5, the sign and gamma): CLOSED with a second-order note
- Derivation of -1/12 = -c^2/2 per slot: S = Spokes x senses = 12 read from the star (load.pushing: scale = n *
  senses). The 00 slot is pushed by +S J00 in its unit (the teeth: rest = 6 grips, load.geared: len(spokes) * grip,
  so c^2 = grip/rest = 1/6); each ii slot by -J_ii in its unit (the grips, at both ends of the Mesh: 2 per count).
  Dust: J00 = J_ii = T00; delta W / rest = 12 J / (6 grip) = 2 J / grip; delta grip / grip = -2 J / grip: equal and
  opposite -> grip = grip_rest (1 - u), W = rest (1 + u), gamma = 1 at first order. The slot ratio -1/12 =
  -(1/6)/2 = -c^2/2: the six Spokes give c^2 = 1/6, the two ends give the 2. The ratio is the star's, not CHOSEN;
  the overall strength stays CHOSEN ("push" in the universe file).
- Dust measured (G1), 30 rounds, slots read: at u = 1, 10, 20, 50, 100, 200 permille: -12 ii / c00 = 999, 995, 990,
  975, 953, 911 permille; gamma_slot = 1001, 1015, 1030, 1077, 1158, 1337 (the ideal (1+u)/(1-u): 1002, 1020,
  1040, 1105, 1222, 1500). gamma -> 1 as u -> 0. The second order is NOT the sign's: the ii gears' teeth read the
  00 slot (every row but the 00 row), so under a rising clock the ii count accumulates dc00 / (12 W):
  ii = -(rest/12) ln(1 + u), grip/grip_rest = 1 - ln(1 + u): ln(1.2)/0.2 = 0.912 against 911 measured; the
  momenta stay at 12 : -1 exactly (shipped probe). In a STATIC well no teeth enter (force balance), so there the
  ratio is -1/12 up to the stresses' share.
- Light against the clock on the pushed metric, frozen (G3; the clock's period^2 ratio W/rest by P1, SOUND to
  both readers): 1 + gamma = 2050, 2100, 2370 permille at u = 20, 50, 200 permille (2/(1-u) = 2040, 2105, 2500;
  at u = 0.2 the grip was 817 permille = 1 - ln 1.2, so light's period^2 ratio 1.2/0.817 = 1.468 against 1474).
- A free lump of one site (G2): gamma_slot at its centre 555-1111 permille by rounds 1-6: below the Mesh's scale
  the centre's six grips read their other ends (ii there ~ 0), so the local ratio is about half; a one-site lump
  is no place to read gamma; the hand radiates (|a| far 1714 against 67 at the centre by round 6).
- gamma on the lump's static well (W): -12 ii / 00 by class = 955 (centre), 810, 792, 667, 756, 980, 871, 857,
  848, 843 permille: the far classes about 0.85. The held lump's stresses: the six neighbours' gradient pushes
  have a +2 A^2 monopole per ii slot against -36 A^2 at the centre (-> 0.81); a lump bound by its own forces has
  sum J_ii = 0 over the body (von Laue) and the far ratio -1/12 exactly. That lump is G3's: OPEN, as before.

## Item 2 (P-2, the Newtonian well): CLOSED
- Cube of 5, the lump held at the centre turning a quarter a round (A = 30), strength grip/9: 52,799 grips of
  push on the board a round (S/grip >> 1); the push at the centre 6.55e26 counts a round, steady (period 4); the
  mean after 600 rounds 12.7e6 counts (the zero mode), u = 0 permille: linear.
- The well (mean subtracted) at the centre: by 200-round windows 9425, 9415, 9389 counts; by 50-round windows
  9166-9713; the per-round swing 2761-16145 over the run (undamped waves of the sudden start on the torus, width
  not growing: 50-round windows' min/max 3538-15978 early, 4131-14270 late).
- Poisson residual grip Delta <w> + <P> - mean<P>, over sum |P - mean|: 70-143 permille by 50-round windows,
  38-58 by 100, 16-26 by 200: falls as 1/T (the residual is the momentum's change over the window / 4).
- Shape against the torus's exact Green's function (Bareiss, by 10 distance classes): measured/predicted = 1000,
  997, 992, 981, 988, 1011, 990, 1001, 988, 997 permille; centre 9402 against 9400; far class (2,2,2) -685 against
  -687.
