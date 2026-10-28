# One mass in the clicks: a train's pair, read exactly by its sine

David, 2026-10-28, 13:5x UTC, for the Boss (Sofer and Animate copied). This page answers the owner's word through Animate (6467743683, posted at 11:25 by the platform's clock; quoted in ALGEBRA.md line 440 on scribe-5): "From the tensor of the 24's rules, the complex numbers and the clock, it must get exactly what a mass is in the clicks." It answers the plan's section 30 row "The mass readings disagree" (TENSOR24.md line 1468 at 13af3fc82): the sines give 1,838.68 and 1,836.15, the rest beats 2,623 and 2,608, and the inertia about 11,000.

A helper drafted it (draft M), and I reran its four probes; the outputs are identical, apart from their run-time lines. They are in DAVID-TENSOR24-THE-MASS_CHECKS.txt, with the draft's proofs in full. The draft reads toys-5 b56643b0e (src, identical to engine-5.0-test 33d9ecaa3's) and scribe-5 f32b67cc3 (the law). It follows the owner's method: the clock first, then the tensor, then the 24. This page covers protocol steps 1 to 4. A second hand follows, then Sofer's check and my sign-off. No src is pushed.

**Units.** At the vacuum (the load 0 at the full rate, p_0 = p_i = Gamma, Q_j = G^2): the teeth w = 6 rim Gamma^2 G^2, each of the six grips R = 2 pinion Gamma^2 G^2, the spring D = 12 (rim - pinion) Gamma^2 G^2, and the hold S = 2 w - D - SUM_j R_j. One quantum is the sweep key / 2. hbar_L = 3 key rim is the light's winding. g = pinion + i s is the train's pair as one Gaussian integer, with N(g) = rim^2 (den's circle).

## 1. In the clock: what a mass is

1. **A hand at rest turns by its own pair.** Every tick, its three-o'clock shadow becomes pinion/rim of itself, less s/rim of its twelve-o'clock shadow. The rest turn is the Gaussian unit g/rim, since g^2 - 2 pinion g + rim^2 = 0. The hand is a small clock whose gear ratio is its pair. PROVED; CHECKED (C3: 63 of 63; the mutant g = pinion + i (s + 1) fails 60 of 63).
2. **A mass is the wind a hand must hold for each quantum it sweeps.** The least such wind is held by the hand standing at rest and turning by its own pair: the twelve-o'clock shadow of the pair, s, in the key's units. That is the click's winding w_c = 3 key s. PROVED (section 2).
3. **So one mass is one Gaussian integer, with three shadows:**
   - **the sine,** s / rim: the wind one quantum holds at rest;
   - **the beat,** arg g: the hand's turn per tick;
   - **the inertia,** 3 s / pinion: the band's curvature.

   The sine is the exact reading in the clicks. The beat misreads it through E = hbar w, and the inertia misreads it through light's c.

## 2. The formula and its proofs

1. **The dispersion.** The one formula's rational form, w (a+ - 2 a + a-) = SUM_j R_j (a_j - a) - D a, takes a plane wave exactly when w (2 - 2 cos w) = R SUM_j (2 - 2 cos k_j) + D. At the vacuum S = 0, so
   - rim cos w(k) = pinion (cos k_x + cos k_y + cos k_z) / 3.
   - In the clock's words: the rim's shadow of the beat is the pinion's shadow of the mean turn per Mesh.
   - PROVED; CHECKED (C1: the head's gearing for all 14 trains of the four universe files; C2: 896 of 896 exact plane waves on the 4^3 torus, through the head's own Spoke read).
2. **Per mode, the wind bounds the sweep.** For one mode, with alpha the amplitude now and beta the amplitude before, the wind is E_k = w (|alpha|^2 + |beta|^2) - 2 w cos w_k Re(conj(alpha) beta) and the sweep is sigma_k = Im(conj(alpha) beta). Then
   - E_k - 2 w sin w_k |sigma_k| = w |beta - alpha e^(i eps w_k)|^2 >= 0, with eps = sgn(sigma_k).
   - The draft's text writes e^(-i eps w_k); the sign is e^(+i eps w_k), as its probe has it (m4: "beta = alpha e^{i w}"). I checked the identity both ways: only the + sign holds. The bound itself is unchanged.
3. **(i) The lattice's Planck relation.** Per quantum, the wind of mode k is at least hbar_L sin w(k), with one hbar_L = 3 key rim for every train and mode. It is reached exactly when the hand turns as one circular wave. CHECKED (Q1: 448 of 448; the mutants fail 60 and 73).
4. **(ii) The least wind per quantum is the winding.** Since sin w(k) >= sin w0 for every k, every state of a train at the vacuum holds at least 3 key s per quantum. Only the rest wave and its doubler at the corner (pi, pi, pi) reach it. The light has s = 0 and no least wind: it is massless. CHECKED (C5: 225 states, 0 failures, exactly 18 equalities, the rest and corner modes).
5. **The exact law between the readings.** Differentiating the dispersion twice at k = 0 gives m2 (R / w) = sin w0, that is E0 = m2 c_T^2, with the train's own c_T^2 = R / w = c^2 cos w0. CHECKED (C4: exact for 3 of 3 trains).
6. **The three readings:**

   | reading | exact form | electron | heavier nucleon | lighter nucleon | ratios to the electron |
   | --- | --- | --- | --- | --- | --- |
   | the sine | Im g / rim | 5.366726e-4 | 0.98677 | 0.98541 | 1,838.68 and 1,836.15 |
   | the beat | arg g | 5.366726e-4 | 1.40796 | 1.39979 | 2,623.49 and 2,608.27 |
   | the inertia | 3 Im g / Re g | 1.6102e-3 | 18.2600 | 17.3714 | 11,341 and 10,790 |

   - The beat agrees with the sine to 5e-8 for the electron, and is off by 1.427 and 1.420 for the nucleons. Section 30's "effective quantum 0.70" (line 1431) is sin w0 / w0.
   - The inertia is off by rim / pinion: 6.17 and 5.88. Exactly, 11,341 = 1,838.68 x pinion_e / pinion_n.
7. **The same on the walk of the cap page** (my addition). For a step that is a turn U, the form (U^dagger - U) / (2i) commutes with U, and on a turning wave U psi = e^(-iw) psi it reads sin w per quantum. It is read from U's rational entries, while the angle w needs an arc. So on either step the integers read the sine of the turn, never its angle. PROVED (two lines).

## 3. The 24

1. The dispersion depends on k only through SUM cos k_j, so it is kept by the 24 and the inversion.
2. The inertia at k = 0 is delta_ab / m2: the six grips are one at the vacuum, and Sym^2 T1 = A1 + E + T2 holds one A1 (Schur).
3. The winding is a function of g alone, an A1 reading, and both spin states of the twin hands share one mass.
4. Beyond the inertia the band is the cube's: its k^4 term is cubic, not round.
5. CHECKED (C6): the head's wind and sweep are kept, and the rational step commutes, under the 24: 144 of 144 each. Anisotropic grips fail 96 of 144.

## 4. The second reading, from the clicks: the chimes

1. **A standing hand's bob crosses its reference at the sign changes of Re(g^n),** integers by the recurrence c_(t+1) = 2 pinion c_t - rim^2 c_(t-1). The mean half period is pi / arcsin(w_c / hbar_L). CHECKED (A3: the counts never part by more than 1 in 33,000 ticks; the beat read as E = hbar w fails at 1,985 to 1,989 of 2,000 ticks on the heavy trains).
2. **The chime's face shows the rest turn at the clock's rate,** cos w0(load) = 1 - (1 - pinion/rim)(p0(load)/Gamma)^2: the mass at the clock's rate, its dilated beat. PROVED; CHECKED (B2: 3,500 of 3,500 chimes on world_plasma and world_universe, within 4/|z|).
3. **The click count exceeds the sweep count by the teeth times the squared miss of the turn against g:**
   - rim^2 E_raw - 4 w rim s |sigma| = 2 w |rim z- - z (pinion + i sgn(sigma) s)|^2, exactly, on one Node-clock.
   - CHECKED (A2: 33,000 of 33,000 ticks; the mutants s + 1 and pinion + 1 fail all 33,000).
4. **Findings on the head** (for Sofer and me):
   - **(a)** the crossing rule CK-S1 counts a passage through exactly 0 twice. The electron's sea reads a beat of 1,964 ticks against the half period 5,890. A run of zeros should be read as one passage;
   - **(b)** the head's full engine turns a flat clock over at every tick (162 turnovers in 6 ticks over 27 clocks on the empty 3^3 board), against law 4's "the rest at the full rate does not turn". This is the vacuum's turnover of my lapse page;
   - **(c)** a fixed winding loses standing quanta on loaded clocks: on world_plasma the heavier nucleon's click count falls to 0 from tick 5, while its action count stays at 0.99 to 1.02;
   - **(d)** the recoil of a fitted pair reads no mass on the head, since every train is fitted as the same one-site child.

## 5. No E = 2 m c^2 at the fitting

1. **A child alone on one Node-clock holds at least one light winding per quantum, for every train.** The hold is 0 at the vacuum, so the spring drops out: E_1 = 3 rim (|z|^2 + |z-|^2) X / Gamma >= 6 rim |sigma| X / Gamma (AM-GM). PROVED; CHECKED (F2: 480 of 480; F3: 232 of 232 shapes, 5 equalities).
2. **The train's own pair as the shape is worse:** 1 / sin w0 light windings a quantum, about 1,863 for the electron and 1.013 for the heavier nucleon. The cost falls as the mass rises, the inverse of E = m c^2. CHECKED (F4).
3. **E = 2 m c^2 is the least cost of a pair,** reached only by rest waves wider than the train's Compton length, which no one-Mesh write lays. CHECKED (F5, F6: the nucleons' packets reach 1.0045 of it at half-width 3; the electron's stay above 5.7e5).
4. **On the head's records,** every single light fitting's booked due equals the train-free one-site formula: 25 of 25 births on world_hole and world_nature (F7).
5. **So section 27's sentence** "A pair is set where the wind reaches the pair's winding at both ends (E = mc^2)" (line 1221) is false for a one-Node-clock child. There the threshold is two light windings a pair, for every train. A fitting at 2 m c^2 must lay rest waves, or be a different click (OPEN).

## 6. The quantum per mode is the action

1. **The action of the hand's own turn:** Q = SUM_x Im(conj(a) P), with P = W (a - a-) + (r - mid W) the step's exact momentum. It is the area the hand sweeps in a tick, times its teeth: the hand's Noether charge.
2. **It is kept exactly by the rational step under any uniform change of the clock** (the teeth, the stretch, the spring and the grips at every tick), not only slowly. PROVED; CHECKED (Q3: 4 of 4 runs of 12 varying ticks; the plain sweep fails 4 of 4).
3. **A fixed winding overcounts mode k by sin w(k) / sin w0.** That is section 30's 54 (line 1428): 53.79 at k = 0.05 for the electron. On the 4^3 board's lowest moving mode the head counts 1,388.8469 electrons a quantum, exactly the formula's value (Q1).
4. **At rest the wind counts both senses and the action their difference** (Q4: 150 of 150 swings split exactly into their circular parts).
5. **On the head the integer carries leak the action** (draft A's verifier's identity; Q5). The integer carry that keeps Q exactly is OPEN; it joins the kept charge Q* (draft I, and my charge helper, still running).
6. **The light.** The head's drift holds no action (sweep 0), so it is no photon. The bang's quarter-turn lay holds exactly one light winding per quantum (Q6: 5,000,000 of 5,000,000).

## 7. The composite (a cross-check with my composite page)

The product of the parts' pairs adds the beats but not the windings. The composite books (p1 s2 + s1 p2) / (rim (s1 + s2)) of its parts' windings, short by exactly s1 (rim - p2) + s2 (rim - p1): 0.9999999 for two electrons, 0.99954 for an electron and a nucleon, 0.162 to 0.170 for two nucleons. CHECKED (C9: 9 of 9). OPEN, mine: the fusion's books for heavy parts.

## 8. A big law missing above? (the owner's 13:21 and 13:26 words)

1. **The candidate: a click counts the hand's action, one quantum a unit of swept area times the teeth.** The wind per quantum is then read (hbar_L sin w), never fixed per train.
2. **It does more than the mass:**
   - a moving hand clicks as its quanta: one electron, not 1,389;
   - a clock whose rate moves (the expansion, a well) keeps its standing hands' quanta;
   - light quanta exist only as turning hands;
   - the mass is the least wind per quantum, the sine, with no second definition.
3. **It contradicts a small law:** law 5's fixed winding w_c = 3 key s as the click's divisor (line 755). On the owner's word of 13:26, it goes to him through section 30, item 11.
4. **Gravity's source follows the same way.** The head's held field is sourced by the spring's density, D |a|^2 div w (tick.py:229), which reads a fourth shadow, key tan(w0/2) a quantum (C7: the wells' ratios 3,164 and 3,138). For one mass in gravity, inertia and the clicks, the source must be the wind, the time-time stress. OPEN, mine, with general relativity's six.

## 9. What it replaces, and what stays

1. **Replaces:**
   - section 19's mass reading ("read as the beat", line 803) and its row;
   - section 28's "a mass ratio is a ratio of two rest beats" (line 1314);
   - section 30's rows on the quantum (line 1428), on the masses (line 1431) and on the mass readings (line 1468);
   - the owed "quantum per mode, from an adiabatic invariant" (line 569): it is the action.
2. **The choice of one light speed for every train** (draft M, 1.6). With grips R = c_u^2 w for all, the sine and the inertia become one reading. The cost: the hold is no longer 0, and the corner's stability needs c_u^2 <= (1 + pinion_min / rim) / 6, light at 0.440 Mesh a tick against 0.577 now. CHECKED (C8: at c_u^2 = 1/3 the nucleons' corner mode grows about 3.4 times a tick). OPEN: mine, then the owner's.
3. **What stays a contradiction with nature** (the lattice's): the nucleons sit at the cutoff (w0 = 1.41 rad, a beat of 2.23 ticks). Nature one to one needs w0 much below 1 for every train. With the electron at 5.4e-4, the ratio 1,838 forces the nucleons to the cutoff, and the electron's Compton length is 1,076 Meshes.

## For Sofer and the Boss

1. **A sentence for Sofer to weigh:** "A train's mass is its pair's Gaussian integer g = pinion + i s on den's circle. In the clicks it is the winding 3 key Im g, the least wind a quantum of the train can hold, held only at rest. Its rest beat is arg g, read by the chimes through E = hbar_L sin(beat). Its inertia is 3 Im g / Re g, read through the train's own grip over its teeth."
2. **Line 440's** "nature's E = h nu being the hand's click rate" holds on the lattice only as E = hbar_L sin(pi / beat), with the beat the half period in ticks: the click rate reads the angle, and the books read its sine.
3. **The head's findings** of section 4, item 4: CK-S1's double count, and the flat clock's turnover against law 4's sentence.
4. **For the Boss:** the calibre's 1,838.68 and 1,836.15 are the click's mass ratios; the rest beats and the inertia are their shadows. A second hand is to re-derive the per-mode bound, attack the naming (the beat as a Floquet quasi-energy against the books' wind), and rerun F7 on more worlds.
