# Draft F: roots II, III, V and VI by the symmetries of the families, the tensor and the 24

For Tensor24's section 18 (roots II, III, V and VI; root IV read for context only), with sections 19 (laws 1 to 11), 26 to 30 and 30's "What goes back to the owner". On the owner's word of 2026-10-28, 11:4x UTC (Hebrew, translated): "All the removal must come from operations of the families, the tensor, the 24; understand how the clocks solve it and how it was solved in the past ... from their symmetries." With the owner's question of 13:1x UTC, through the coordinator: "Is there a solution for what dark matter is? In fact it does not click, does it?" (section 6.3).

Drafted under derive/PROTOCOL.md and derive/TEMPLATE.md. Read on: the t24 worktree (TENSOR24.md at ee35a7c16; the head's src, imported read-only by two probes); scribe-5's docs/ALGEBRA.md at 25027b4f6 (every law line below is quoted by its number there; the copy is ref_ALGEBRA_scribe5_now.md in this folder); scribe-5's docs/CLOCK_WORDS.md; toys-5's DAVID-TEMPERATURE.md (536d7ea9b) and DAVID-FOUR-PHENOMENA.md; the physicist's and the mathematician's probes and reports (derive/physicist, derive/mathematician); drafts C and D. The probes and their outputs are in this folder (section 7). Every claim is marked **PROVED** (with its proof), **CHECKED** (with the probe and its count) or **OPEN** (with what blocks it and whose it is). Steps 5 and 6 of the protocol (a second hand; Sofer's check and David's sign-off) are not this draft's.

The words: the clock words of docs/CLOCK_WORDS.md. Three code words stand beside them, as the head names them: the hold (2 w - D - SUM_j R_j, the weight of a Node-clock's own notch in its next, core/rule3.py), the sweep (Im(conj(z-) z), a hand's area swept between its two notches) and the lead (Im(conj(z_x) z_y), the link's bilinear across a Mesh).

## 0. The answer in short

| item | the symmetry, the theorem or the operation | verdict | status |
| --- | --- | --- | --- |
| II.3 the cube against the continuum | Schur on T1: the 24 keep one quadratic form in k, \|k\|^2; the first form the 24 add to the sphere's is SUM k_a^4 (rank 4) | removed at O(k^2) for every scalar, hand and twin train; the rank-4 slowing stays; for E, T1 and T2 trains the 24 allow 2, 3 and 3 long-wave constants, and only a gauge makes them isotropic | PROVED; CHECKED (F1) |
| II.21 no Lorentz invariance | no linear map keeps both the stencil of one tick and light's cone but {+-1} x the 48; the asynchronous board makes the tick a gauge, not the Mesh's rest | the preferred frame stays (theorem); every train's long waves are a Lorentz form; one limiting speed is impossible on any finite tick, and the law of the grips makes it a function of the rest beat alone | PROVED; CHECKED (F1, F2) |
| II.23 the Courant bound | CFL: the act's cone is the L1 ball, light's long-wave sphere its inscribed sphere | permanent; in integers a strong pulse's precursor stands beyond light's sphere | PROVED; CHECKED (F2) |
| II.16 doubling | the staggered map SIGMA = the torus's character at (pi, pi, pi) times the tick's parity, exact where the hold is 0 | the one term of the stencil that lifts it is the hold, an A1 term; it is > 0 at every loaded Node-clock and 0 at the full rate by the teeth count's edge, which no symmetry fixes | PROVED; CHECKED (F3); the vacuum's choice OPEN (David, the owner) |
| II.26 CPT | C = the kinds' conjugation (Frobenius-Schur: every kind of 2O is real or quaternionic); CPT = C P (C R) = P R on every bilinear | "C undefined on the twin hands" removed; the plan's S . J is CPT-odd; the two-time spin SW . J is CPT-even with V - A's pattern | PROVED; CHECKED (F4); SW . J's rewind OPEN |
| III.17 single quanta | law 7's two ways: per M and det M; the hand's phase gives the sweep, the action per mode | HOM, antibunching and the partition from the one click; Grangier's anticorrelation stands for a spread quantum (a semiclassical engine); the quantum per mode is the sweep | CHECKED (F5); a token OPEN |
| III.18 Born for position | the sweep's exact continuity, the Mesh's lead its flux | a token per quantum hopping by the flux keeps Born's law exactly where the sizes are non-negative | CHECKED (F5); the discrete tick's validity OPEN |
| III.19 many quanta, the vacuum | the board's state is a point of a product, not a vector of a tensor product | the n-quantum click gives Fock's symmetrized products; entanglement of many, zero-point fluctuations and running couplings stay absent | PROVED (theorem, with root IV) |
| III.7 temperature | the exact T (detailed balance) and the exchange sign's 1 +- n | candidate route to Bose-Einstein and Fermi-Dirac | OPEN (David) |
| III.24 recurrence | a bijection's bounded orbit is a cycle | a theorem; law 10's two sentences meet at the circle's closing bang | PROVED; CHECKED (F5); for the owner |
| V.20, V.22 the light's kind and its gauge | the Mesh's odd gear is T1; its A1 gauge leaves two transverse gears per wave number; Maxwell = the one formula's pull less grad div | the light as the offset's T1 on the Meshes, Gauss kept by the sweep's continuity | CHECKED (F6); the hands' turn by a fine phase OPEN (David) |
| VI.25 the course | T^3 carries no metric of non-negative scalar curvature but the flat (Gromov and Lawson; Schoen and Yau): no turnaround with matter on the torus | permanent in general relativity; the bounce is law 4, the exact T used once, a decision | PROVED (cited theorem); the engine's constraint OPEN |
| VI.25 dark matter | a one-gear train is a real kind: no sweep, no lead, no phase; C, under which the offset is odd | dark to the light's current by its kind, and to the offset's linear terms by C and the gauge; to the light's quadratic forms only under its own Z2 with a coupling 0; the remainders refuted as a candidate | PROVED; CHECKED (F7); the head measured; halos and amount OPEN |

## 1. Root II: the lattice and its one tick

### 1.1 Item 3, the cube against the continuum

**The contradiction (TENSOR24.md 18, item 3):** "At the Mesh's scale a wave's speed depends on its direction; nature's isotropy holds for long waves alone."

**In the clocks.** A Node-clock's next notch reads its six Meshes alike. A long wave turns its six neighbours by nearly the same small step, so at the first order the clock cannot tell an axis from a diagonal: the 24 permute its Spokes, and one sum over six Spokes is the same however the wave runs. At a short wave the neighbours along an axis stand at other phases than along a diagonal: the cube's corners show, as the fourth power of the wave's step per Mesh.

**In the tensors.**
- The wave vector k is T1. A train's long-wave operator is M_ab(k) = C_ab,cd k_c k_d on the train's own components, a 24-invariant element of Sym2(K) x Sym2(T1).
- **The scalar case.** Sym2(T1) = A1 + E + T2 holds A1 once, so a scalar's dispersion is c^2 \|k\|^2 at O(k^2), whatever the stencil. **PROVED** (Schur: T1 is irreducible); **CHECKED** (F1 B1: one invariant of degree 2 under the 24).
- **The first anisotropy.** At degree 4 the 24 keep two invariants, \|k\|^4 and SUM k_a^4, where SO(3) keeps one. **CHECKED** (F1 B2 to B4: the invariants of degree 0 to 9 number 1, 0, 1, 0, 2, 0, 3, 0, 4, 1 under the 24 and 1, 0, 1, 0, 2, 0, 3, 0, 4, 0 under the 48).
- **Its size on the engine's band.** For cos w = 1 - lambda SUM_a (1 - cos k_a), with the hold h = 2 - 6 lambda, the group speed along the unit direction d is v = sqrt(lambda) (1 - kappa p^2 + ...), with kappa = (S4 - lambda) / 8 and S4 = SUM d_a^4. **PROVED** (series); **CHECKED** (F1 E1 to E3, exact rational series to p^8):
  - at the edge, lambda = 1/3: kappa is 1/12 on an axis, 1/48 on a face diagonal, 1/48 along (1, 2, 3), and 0 on a body diagonal;
  - below the edge (lambda = 1/6, the hold 1) the body diagonal slows too: kappa = 1/48.

  This is scribe-5's own line 713, "The cube's slowing and the tick's bound": "c (1 - ((3 SUM_a d_a^4 - 1) / 24) p^2 + ...), 1 / 12 along an axis, 1 / 48 along a face diagonal, 0 along a body diagonal ... 1 / 30 averaged over directions; the cubic group's first invariant beyond the sphere's, SUM d_a^4, carries the cube". It is the same number: (3 S4 - 1)/24 = (S4 - 1/3)/8.
- **A finding beyond the plan's big law** ("isotropy and one light cone hold for waves long against the Mesh, as on every lattice of physics"). For a train of kind E, T1 or T2 the 24 allow 2, 3 and 3 long-wave constants: a cubic crystal's elastic constants (C11, C12, C44). **CHECKED** (F1 C2, by characters). So the offset's T1 gears and the regulator's tensions and shears are not isotropic by the 24 alone. For T1 the three are alpha \|k\|^2 delta_ab + beta k_a k_b + gamma k_a^2 delta_ab. A gauge, M(k) k = 0 for every k (a pure gradient wave carries nothing), leaves one: |k|^2 delta - k k^T, Maxwell's, which a rational rotation (3/5, 4/5) about z keeps and gamma's term breaks. **CHECKED** (F1 D1 to D5). For the metric the diffeomorphisms play that part: OPEN (David's general relativity items, section 25 item 3).

**The history.**
- Lattice waves are anisotropic at short wavelengths in every crystal; in lattice field theory the departure from rotation symmetry is the order a^2 operator SUM_mu p_mu^4, removed order by order by Symanzik's improvement (K. Symanzik, Nucl. Phys. B 226 (1983) 187), which adds terms beyond the nearest neighbours.
- Nature bounds the cube's slowing: scribe-5 line 713 reads the three gamma-ray bursts (MAGIC GRB 190114C, Fermi GRB 090510, LHAASO GRB 221009A) as a Mesh under 1.3 x 10^-26 m along an axis.

**The project's earlier handling.** scribe-5 line 713 (2026-10-20): the form derived, the bound nature's. A derivation, with nature's bound as a reading.

**The removal.** The 24 remove the O(k^2) anisotropy for every scalar, hand and twin train (PROVED). The rank-4 slowing stays: the 24 allow SUM k_a^4, and an improvement would read beyond one Mesh, which Postulate 1 (line 29) forbids. **Theorem, permanent:** the cube's slowing at O((k Mesh)^2). For vector and tensor trains the gauge (root V; the diffeomorphisms for the metric) is what removes the O(k^2) anisotropy.

### 1.2 Item 21, Lorentz invariance

**The contradiction (item 21):** "a preferred frame; limiting speeds that differ by train; the cubic anisotropy at the nucleons' scale; no dilation of a moving clock."

**In the clocks.** Every Node-clock keeps its own tick at its own rate, the lapse (the owner's ruling for the new engine; the law's own clause, line 98: "The Node-clock steps on its own clock; the great clock at equal ticks is one"). A bob's chimes are its ticks and light's clicks its signals (section 25, item 3). Two bobs that read each other by light out and back read Einstein's numbers, because the Mesh's rest cancels from a round trip. The Meshes themselves never move: the great clock has one rest, and a one-way reading or a short wave can find it.

**In the tensors.**
- **No boost keeps the one act.** Light's long-wave cone is t^2 = 3 \|x\|^2. Its integral form t^2 - 3 x^2 has an infinite group of integer boosts, Pell's unit 2 + sqrt 3: (t, x) -> (2t + 3x, t + 2x), of determinant 1. But the stencil of one tick holds two time steps of Q4 = t^2 - 3 \|x\|^2 = 1 and six Spokes of Q4 = -3, so a linear map that keeps both the stencil and Q4 keeps the time steps and the Spokes apart: it is in {+-1} x the 48. The boost maps (1; 0, 0, 0) to (2; 1, 0, 0). **PROVED; CHECKED** (F2 D1 to D4).
- **The asynchronous board.** Each Node-clock steps when its six neighbours' arrivals stand (line 98: "whenever every Node-clock has reached the same count of ticks the great clock is one and the same bit for bit, whatever the order was"). So the great clock's tick is a gauge, the lapse's slicing, and no act reads it (line 695: "The great clock's tick is no observable"). It removes the preferred simultaneity, and not the Mesh's rest, which no relabelling of ticks moves. **PROVED** (from the clauses' content).
- **The long-wave Lorentz form.** The 24 make each train's k^2 term isotropic (1.1); the exact T (the rewind) makes the band a function of cos w; the torus's translations give plane waves. So each train's long waves obey w^2 = w0^2 + c_K^2 \|k\|^2 + O(k^4, w0^2 k^2). **PROVED.**
- **One limiting speed.** For cos w = r (1/3) SUM_a cos k_a (every train at the vacuum's hold 0, r = cos w0 = pinion / rim):
  - in the lattice's own variable 2 sin(w/2), (2 sin(w/2))^2 = (2 - 2r) + (r/3) p^2 + ...: c_K^2 = r/3. **CHECKED** (F1 E4, exact for r = 1, 4/5, 3/5, 1/2);
  - in w, c_K^2 = w0 cot(w0) / 3 = (1/3)(1 - w0^2/3 + ...). **PROVED** (first-order expansion).

  So the speeds differ by train at O(w0^2), the square of the rest beat per tick. The law of the grips (the grip proportional to the pinion, the spring to rim - pinion, the hold 0) makes c_K a function of w0 alone, equal to light's as w0 -> 0. Exact universality is impossible on any tick stencil of finite reach in time: it needs a dispersion F(w) = w^2 on an interval, and a trigonometric polynomial that equals w^2 on an interval is w^2 everywhere, which is not periodic. **PROVED.**
- **A moving clock's dilation.** On the band w^2 = w0^2 + c^2 k^2 a packet's phase along its own path runs at w - k . v_g = w0^2 / w = w0 / gamma. A moving bob chimes at its band's phase rate, so the dilation is the band's at long waves, with lattice corrections of O(k^2, w0^2). **PROVED** (at long waves). The plan's item 21 reads the head, whose rate is the typed exponential (E8).
- **The nucleons at the cutoff.** The one big bang's heavy rows have r = 2458210083751875/15162856759112389 and 2580388913625285/15162856759112389, about one sixth: w0 near 1.4, so c_K^2 = r/3 is about a sixth of light's in the variable 2 sin(w/2). That is the calibre's choice of masses in lattice units (A12), and the theorem says the anisotropy and the speed's spread both vanish as w0 and k Mesh go to 0.

**The history.**
- **Clocks and signals.** A. Einstein, Ann. Phys. 17 (1905) 891, section 1, "Definition der Gleichzeitigkeit": clocks at A and B are synchronous when t_B - t_A = t'_A - t_B for light out and back. The round trip is the observable; the one-way speed rests on that convention (R. Mansouri and R. U. Sexl, Gen. Rel. Grav. 8 (1977) 497, the test theory with an arbitrary synchronization).
- **Emergent Lorentz invariance.** S. Chadha and H. B. Nielsen, Nucl. Phys. B 217 (1983) 125: different metrics for different species flow to one in the infrared. J. Collins, A. Perez, D. Sudarsky, L. Urrutia and H. Vucetich, Phys. Rev. Lett. 93 (2004) 191301: with interactions, a preferred frame at the cutoff feeds percent-level differences into the low-energy limiting speeds unless the bare parameters are fine-tuned.
- **No regular discretization is Lorentz invariant.** L. Bombelli, J. Henson and R. D. Sorkin, Mod. Phys. Lett. A 24 (2009) 2579 (gr-qc/0605006): no equivariant map from Poisson sprinklings to directions exists, so only random discreteness keeps Lorentz invariance; a lattice picks a frame.

**The project's earlier handling** (scribe-5, each with its status):
- line 711, "The two-way reading" (derived): a bob reads another's speed by light out and back as (v_B - v_A) / (1 - v_A v_B / c^2), "exact for long flashes on the empty great clock, at light's c and not at the pattern's c_m";
- line 693, "The same clock and the same ruler for every act" (the law, decided): "its content one assumption, the Mesh clocked twice by its reading Node-clock"; it calls the unimodular dilation of the Node-clock's cell "the one remnant of the light cone's invariance the law holds", and names matter's own limiting speed, c_m = 0.867 c at [2, 3];
- line 695, "The great clock's tick is no observable" (a hypothesis under its own name, 2026-10-22): the relabelling of ticks the second remnant;
- line 98 (the owner's word of 2026-10-25, 07:2x UTC): the asynchronous board, the great clock's tick the reader's;
- line 1507, "Einstein lives in the clicks of bound bobs, and the great clock is never measured" (the owner's organizing principle, 2026-10-21): "every train's band is a Lorentz form at long wavelength ... matter's own limiting speed c_m stands below light's by omega_0^2 / 6".

So the earlier law derived the two-way exactness and the long-wave form, and named the preferred frame and the speeds' spread. The one assumption (the ruler tied to the rate, h N = 1) the physicist calls gamma = 1 put in (TENSOR24.md 16).

**The removal.** The asynchronous board removes the preferred simultaneity (PROVED). The 24, T and the translations give every train a long-wave Lorentz form (PROVED). One law of the grips gives one limiting speed as a function of the rest beat (CHECKED). **Theorems, permanent:** no boost keeps the stencil (F2 D), so the Mesh's rest stays; the speeds' spread at O(w0^2) and the cube's slowing at O(k^2). **OPEN:** whether the one formula's sources (J) feed differences into the speeds at the order the couplings set, Collins and others' fine-tuning (David).

### 1.3 Item 23, the Courant bound (with item 2 read for context)

**The contradiction (item 23):** "no stencil reaches as far as its own light (the Courant bound), so section 25's item 7 is a permanent artifact". The precise statement is the converse: every stable explicit stencil reaches at least as far as its light.

**In the clocks.** In one tick a Node-clock's word crosses one Mesh along an axis. Light's long waves cross a Mesh in the root of 3 ticks along an axis, and along the body diagonal exactly as far as the word: there light touches the act's reach.

**In the tensors.**
- The act's cone after t ticks is the L1 ball \|x\|_1 <= t; light's long-wave sphere at the edge has radius^2 t^2/3, the L1 ball's inradius^2. (\|x\|_1)^2 <= 3 \|x\|^2 holds with equality on the 8 body diagonals alone. **PROVED** (Cauchy-Schwarz); **CHECKED** (F2 A1 to A3, a box of side 13).
- The rational Green's function of a+ = (1/3) SUM_j a_j - a- fills the L1 ball with the checkerboard's parity and reaches every point of its surface; the axis tip carries exactly 3^-t of the pulse. **CHECKED** (F2 B1 to B4, 9 ticks on a torus of side 21).
- **In integers the act's extra reach is real.** The one formula with Rule3's carry (W = 999, g = 333, the hold 0) from a one-site pulse: the axis tip carries the rounded thirds and goes dark after tick 6 (10^3 notches) and tick 13 (10^6); yet nonzero notches stand on the L1 surface at every tick to 24, near the body diagonals, and the farthest one stands beyond light's long-wave sphere, 3\|x\|^2 - t^2 = 186 and 624 at tick 24. **CHECKED** (F2 C1 to C3, on the octant). So a signal can outrun light's long waves on the integer engine, with an amplitude that grows with the pulse: item 2 stands for any strong source, not only for a carriage.

**The history.** R. Courant, K. Friedrichs and H. Lewy, Math. Ann. 100 (1928) 32: an explicit scheme converges only where its domain of dependence holds the equation's. On quantum lattices with local terms, E. H. Lieb and D. W. Robinson, Commun. Math. Phys. 28 (1972) 251: a finite group velocity with leakage outside the cone.

**The project's earlier handling.** Postulate 3 (line 33): the causal speed one Mesh a tick built in, light "1 / sqrt 3 of a Mesh per tick, c, the largest sphere that fits in what one tick reaches"; "no click of nature's measures it, and what a bob measures of another by clicks never exceeds c". A postulate and a derived dispersion; the precursor's amplitude was not read.

**The removal.** None by symmetry: a sphere is no polytope, and every stencil's cone is a polytope. **Theorem, permanent** (CFL). The integer precursor (F2 C) is the measured size of item 2's contradiction.

### 1.4 Item 16, doubling

**The contradiction (item 16):** "at the vacuum the hold 2 w - D - sum R is 0 for every train, so the checkerboard's two sublattices step apart, and every species has an exact doubler of the opposite charge."

**In the clocks.** At the full rate a Node-clock's own notch has no weight in its next notch: the next is its six neighbours' pull less its own notch before. Every Mesh joins the two colours of the checkerboard, so the two colours drive each other and never themselves, and a pattern with every other Node-clock's sign flipped, and flipped again every tick, runs as well as the pattern itself. A loaded Node-clock, running below the full rate, gives its own notch a weight, the hold, and the colours are tied.

**In the tensors.**
- **The map.** SIGMA: a(x, t) -> e(x, t) a(x, t), e = (-1)^(x + y + z + t): the torus's character at the wave number (pi, pi, pi) times the tick's parity. It sends k to k + (pi, pi, pi) and w to w + pi.
- **Exact where the hold is 0.** Under SIGMA the neighbours' sum takes -e and the Node-clock's own term +e; the step's a+ + a- takes -e. So SIGMA maps the step to itself exactly when the hold is 0. **PROVED; CHECKED** (F3 A1: 12 ticks bit for bit in exact rationals, for light and for a massive train r = 3/5; A2: off the edge, at a hold of 1/5, it fails at the first tick; C1, C2: the two terms' signs).
- **Same wind, opposite charge.** At the hold 0 the conserved form is SIGMA-even and the sweep SIGMA-odd. **CHECKED** (F3 B1: wind 423968/3 kept, sweep -5002 -> 5002; massive: 725934/5 kept, 957 -> -957; B2: off the edge the wind is not kept).
- **The hold on the head.** core/rule3.gearing at the one big bang's calibre (den 15162856759112389, Gamma 1000, G = 16): the hold is 0 at the full rate for the light, the three rows, the held field and the regulator; at a load (p0 = 999, 900, 500, pm = p0^2 div Gamma) it is 12 G^2 (rim (Gamma^2 - p0^2) + pinion (p0^2 - pm^2)) > 0; a tension on one Mesh raises it too. **CHECKED** (F3 D1 to D4, against the head's own function).
- **The carry.** With Rule3's carry (W odd) SIGMA is not exact (the image and the step part at the first tick in 5 of 5 random starts), and from a setting with no content at (pi, pi, pi) in either slot the rounding feeds the massless staggered mode: SUM e a = -2, -232, -1946, -4547, -11247, -30256 at ticks 1, 10, 50, 100, 200, 400; a massive train at the edge stays bounded (between -20 and 29). **CHECKED** (F3 E1, E2). This is scribe-5 line 1419's "Rule3's own rounding ... walks the staggered mode as t^(3/2)".
- **What fixes the hold.** SIGMA commutes with the 24 (each rotation keeps x + y + z mod 2), with the rewind (t -> -t keeps (-1)^t), with the mirror, and with the translations up to the global sign a -> -a, itself a symmetry of the linear step. So no symmetry of the list forces the hold or forbids it. At the vacuum it is set by the teeth count's definition, T = 6 rim Gamma^2 G^2 = (D + SUM_j g_j) / 2 at s = 1: the Courant edge (1.3). **PROVED.**

**The history.**
- **Nielsen and Ninomiya:** H. B. Nielsen and M. Ninomiya, Nucl. Phys. B 185 (1981) 20 and B 193 (1981) 173: a local, translation-invariant, Hermitian lattice action with exact chiral symmetry has as many left- as right-handed species. It concerns first-order (Dirac and Weyl) operators.
- **Wilson's way:** K. G. Wilson, "Quarks and strings on a lattice", in New Phenomena in Subnuclear Physics (Erice 1975), ed. A. Zichichi (Plenum, New York, 1977) p. 69: a Laplacian term times the spacing gives the doublers masses of the cutoff's order and breaks chiral symmetry.
- **Kogut and Susskind's way:** J. Kogut and L. Susskind, Phys. Rev. D 11 (1975) 395; L. Susskind, Phys. Rev. D 16 (1977) 3031: the staggered field spreads the doublers over the sublattices as tastes.
- **A remnant symmetry:** P. H. Ginsparg and K. G. Wilson, Phys. Rev. D 25 (1982) 2649; H. Neuberger, Phys. Lett. B 417 (1998) 141 (the overlap); M. Luscher, Phys. Lett. B 428 (1998) 342 (exact lattice chiral symmetry). No such operator is ultralocal: I. Horvath, Phys. Rev. Lett. 81 (1998) 4063.
- **An extra dimension:** D. B. Kaplan, Phys. Lett. B 288 (1992) 342: domain-wall fermions.

  Of the ways out, the overlap needs reads beyond one Mesh (Postulate 1 forbids it) and the domain wall a fifth index; within one Mesh only Wilson's (an explicit term) and Kogut and Susskind's (tastes) remain.

**The project's earlier handling** (scribe-5):
- line 1419, "No drive from outside Rule3 wakes either double root of the massless train" (the decision): the two double roots named (k = 0 and the staggered mode), "each carries neither form nor wind", and "the loader refuses such a great clock for a massless train by name". The refusal of even boards was a declaration: it struck the exact staggered mode and left the near-pi band. The owner's ruling of 11:1x UTC (no condition typed on the board) strikes it.
- line 1562, "Spin, closed for the paper as a route" (2026-10-19): "the staggering (-1)^(t + x + y + z) an exact Z_2 of every train's band and no doubling of components, not of hands ... two tastes, never a spinor", and Kogut and Susskind's half-spacing operator needing sixteen components.
- line 1641: the stability edge ("the edge admitted, a repeated root growing linearly, light's checkerboard"), the mathematician's finding again (TENSOR24.md 30).

**The removal: a term from the kinds.** The hold is the A1 term of the stencil, generic, the same formula for every train: hold = 2 W - s (D + SUM_j g_j). It is the one SIGMA-odd term within one Mesh, so it is the one lifting term the kinds allow (PROVED). It is already > 0 at every loaded or tensed Node-clock (CHECKED), so the doubler is exact only where the clock runs at the full rate. Two candidates for the vacuum, both generic, neither forced by a symmetry:
- **(a) the vacuum below the edge.** The teeth count from another lattice count, for example T = 12 rim Gamma^2 G^2 (the sides times the Spokes): the vacuum's hold is then T, the light's c^2 is 1/6, and the doubler sits at the band's middle, cos w = 0 at (pi, pi, pi). The cost: light's speed 1/sqrt 6, the body diagonal's exactness lost (F1 E3), and the act's cone strictly beyond light's in every direction; the pairs' beats move with T, so the calibre's pinions are re-derived.
- **(b) the edge kept, the doubler a taste.** Kogut and Susskind's reading: the doubler of every species is a second species of the opposite charge and the same wind, at frequencies near pi.

**OPEN** (David, then the owner, since (a) changes light's speed): (a) or (b). **Theorem that stays:** Nielsen and Ninomiya, for any first-order chiral form the plan may give the twin hands.

### 1.5 Item 26, CPT

**The contradiction (item 26):** "No CPT theorem without Lorentz invariance, and C is undefined on the twin hands."

**In the clocks.** The rewind runs every gear back, with the offset's time gear turned over (it is the four-vector's time part). The mirror turns the board inside out through a Node-clock and turns each Mesh's odd gear with its Mesh. The conjugation turns every hand's twelve-o'clock gear over, and on the twin hands it exchanges the two hands with one sign (the Kramers turn, the plan's phase reversal T). Their product runs the great clock back and inside out.

**In the tensors.** The three exact operations of F4:
- R, the rewind's involution: now and before exchanged on every gear, the offset's time gear negated;
- P, the inversion of the 48: site gears moved x -> -x, and a Mesh's odd gear A_a(x) -> -A_a(-x - e_a);
- C, the kinds' conjugation: z -> conj z on the hands; psi -> (-conj psi2, conj psi1) on the twin hands; the offset negated.

The findings:
- **C exists on every train.** The Frobenius-Schur indicator (1/\|G\|) SUM chi(g^2) is +1 for A1, A2, E, T1 and T2 of O and -1 for E1/2, E5/2 and G3/2 of 2O. For the spinor kinds, chi(h^2) = 2 cos(phi) = tr(g) - 1 at both preimages h of each g, so the 24's integer traces give the indicator exactly. So no kind of 2O is complex: each kind's conjugate is itself, and C acts within each train, as the plain conjugation (C C = +1) on O's kinds and as eps K (C C = -1) on the spinor kinds. No twin pair but 0 is its own conjugate, so no twin train can be self-conjugate (a Majorana train). **PROVED; CHECKED** (F4 F1 to F3: the indicators, and 0 fixed pairs in a box of 7^4). This removes "C undefined on the twin hands". Unlike the Lorentz group's Weyl spinor (whose conjugate is the other chirality), the cube's spinor is pseudoreal.
- **CPT = C P (C R) = P R** on every bilinear, since C C = -1 drops out of them. **CHECKED** (F4 T1). Here T = C R, the plan's phase reversal composed with the rewind (the charge-keeping time reversal: scribe-5 line 1602's "The swap keeps the charge": "the fifth act on a plane is C T_0, the conjugation composed with the exchange of the two notches").
- **Every reading has nature's parities** (C, P, T): the charge (-, +, +), the current (-, -, -), the momentum (+, -, -), the middle-slot twin spin S (-, +, -) like nature's tensor density, the two-time density W (-, +, +), the two-time spin SW (+, +, -) like nature's axial current, E (-, -, +) and B (-, +, -). **CHECKED** (F4's table, exact on 6 random states of the torus of side 3).
- **The electromagnetic couplings** Q A0 and J . A and the spin term S . B are even under C, P and T separately. **CHECKED** (F4 T4).
- **The plan's one-hand coupling S . J** (section 24, item 5: "the twin hands' spin S ... contracted with a current ... into A1") is P-odd, C-even, T-even, CP-odd and **CPT-odd**. **CHECKED** (F4 T7). So the CPT check of section 18's root II fails on the plan as written.
- **The two-time spin's coupling SW . J**, with SW = (2 Re D_ud, 2 Im D_ud, D_uu - D_dd) and D_ac = i (conj(b_a) n_c - conj(n_a) b_c) (draft D's two-time reading), is P-odd, C-odd, CP-even, T-even and **CPT-even**: nature's V - A pattern. S . Pm (spin with momentum) is the same, and S . E (spin with the electric field) is P-odd, T-odd and CPT-even (an electric dipole's). **CHECKED** (F4 T8).
- **A sign in draft D's two-time spin.** SW turns as S does under the 24's three-fold turn only with +2 Im D_ud; draft D's -2 Im D_ud is the conjugate basis, so its contraction with a current is not kept by the 24. **CHECKED** (F4 R1, R2, exact with the spinor turn (1 - i (s_x + s_y + s_z))/2 on 40 random pairs). For David and draft D's verifier.

**The history.** G. Luders, Kgl. Danske Vid. Selsk. Mat.-fys. Medd. 28, no. 5 (1954); W. Pauli, in Niels Bohr and the Development of Physics (Pergamon, 1955); R. Jost, Helv. Phys. Acta 30 (1957) 409: CPT from Lorentz invariance, locality and Hermiticity, through the complex Lorentz group's identity component, which holds the total reflection. O. W. Greenberg, Phys. Rev. Lett. 89 (2002) 231602: an interacting theory that violates CPT violates Lorentz invariance. So a lattice (no Lorentz group) may violate CPT, and the check must be made term by term, as F4 does. Frobenius-Schur's indicator: G. Frobenius and I. Schur, Sitzungsber. Preuss. Akad. Wiss. (1906) 186.

**The project's earlier handling** (scribe-5):
- line 344, "The conversion" (2026-10-23, the owner's word "support CPT; in nature it holds after the clicks"): "for a plane parent the click's CPT is an identity of the law" (derived);
- line 1181, "CR-S1 and CR-S2": "the step, the drives and the whole tick without the click covariant under C, P, T and all their compositions (the group of order 192 measured) ... no composition of C, P and T is an exact symmetry of the clicks on this head" (a finding);
- line 126, OL-S1: "the odd gears' current J is odd under the conjugation while the shape-4 train's K is the identity ... the letter that would mend it reads the sign train as a four-vector under time's reversal" (a finding and not a sentence). F4's R, with the offset's time gear negated, is that mend; its mutant (the rewind without the sign) breaks E's parity and the charge's coupling (F4 mutant a0);
- line 1562 (2026-10-24, derived): "W . k is CPT-odd and Phi . k CPT-even ... the law stays CPT-even".

**The removal.** C from the kinds' conjugation (PROVED), CPT = P R (CHECKED), and the check made term by term (CHECKED). **Candidate:** the one-hand coupling as the twin train's integer times SW . J, products and sums of the twin hands' two slots and the lead, no other number. **OPEN** (David): SW reads the before slot, so the step's exact rewind needs the twin train stepped after the trains it reads (the architect's two-stage schedule, TENSOR24.md 31) or a midpoint form; and CPT on the clicks (the draw, law 9).

## 2. Root III: one field per train, its quanta booked by the clicks

### 2.1 Item 17, single quanta, and the quantum per mode

**The contradiction (item 17):** "a quantum spread over several Node-clocks never clicks whole, against Grangier's anticorrelation; weak light would click late, while the photoelectric effect is prompt ... no threshold by frequency alone ...; no partition noise and no Hong-Ou-Mandel bunching."

**In the clocks.** A hand's sweep is the area its hand sweeps between its two notches: its turning, its action. A click of a whole that reads the sweep at the key takes one quantum of turning, and the wind that quantum carries is the key times the hand's own beat, 2 sin w: a faster hand's quantum carries more wind. At a splitter two equal quanta reach two bobs two ways, and the click adds the two ways' amplitudes with the family's sign.

**In the tensors.**
- **The n-quantum click** (law 7's form, sigma_ab = N(M_a1 M_b2 + eps M_b1 M_a2)) at a balanced splitter M = [[1, i], [i, 1]]: two light quanta, one per input, have the coincidence amplitude per M = 1 + i i = 0, and the odds (two in one output, one in each, two in the other) are (1/2, 0, 1/2): the Hong-Ou-Mandel dip. Two twin quanta have det M = 2, the coincidence certain. One quantum splits 1 : 1, the binomial partition. **CHECKED** (F5 C1 to C3, exact).
- **The quantum per mode is the sweep.** On the torus of side 4, two exact one-signed waves of the train r = 3/5 (k = 0 with cos w = 3/5, and k = (pi/2, pi/2, pi/2) with cos w = 0) solve the one formula exactly; each wave's wind is 2 sin(w) times its sweep (1064.96 = 2 (4/5) 665.6, written exactly 26624/25 = 2 (4/5) (3328/5); and 2176 = 2 x 1 x 1088); the waves' winds and sweeps add with no cross terms; no single frequency reads the sum; a standing wave has wind and no sweep. **CHECKED** (F5 B1 to B5). So the sweep is the hand's exact local integer whose content per one-signed mode is E / (2 sin w), the action: the plan's "wind over the frequency" (section 30) with the lattice's frequency variable 2 sin w.
- **The sweep is the exact charge** of the linear step at any hold, with the continuity equation at every Node-clock and tick and the Mesh's lead at the middle slot as its flux. **CHECKED** (F5 A1, A2: 10 ticks, light at the edge and a train below it; the centred lead fails, F5 mutant).

**The history.**
- **The quantum per mode:** M. Planck, Ann. Phys. 4 (1901) 553; A. Einstein, Ann. Phys. 17 (1905) 132 (light quanta). The adiabatic invariant E / nu: Einstein's answer to Lorentz's slowly shortened pendulum at the 1911 Solvay council; P. Ehrenfest, Ann. Phys. 51 (1916) 327 (the adiabatic hypothesis).
- **The photoelectric effect without quantized light:** W. E. Lamb and M. O. Scully, in Polarisation, Matiere et Rayonnement (Presses Universitaires de France, 1969): a classical field on a quantized detector gives the threshold by frequency and prompt emission with odds proportional to the intensity.
- **What refutes the semiclassical picture:** J. F. Clauser, Phys. Rev. D 9 (1974) 853; P. Grangier, G. Roger and A. Aspect, Europhys. Lett. 1 (1986) 173: one photon at a beam splitter gives coincidences far below any classical wave's bound.
- **Two-photon interference:** C. K. Hong, Z. Y. Ou and L. Mandel, Phys. Rev. Lett. 59 (1987) 2044. Detection odds from field correlations: R. J. Glauber, Phys. Rev. 130 (1963) 2529.

**The project's earlier handling** (scribe-5):
- line 915, "The click's unit: the whole of a click is the detector's own transition" (restored on 2026-10-28, 02:4x UTC; the declaration of the detector, its consequences derived): "Planck's relation holds on the lattice, wind = I sin omega with I = A^2 sin omega / T the adiabatic invariant ... a plane's invariant is its Wronskian, I T = A^2 sin omega = W, an integer bilinear of the hand's own notches that the law already counts as charge; a real gear's (light, dimension 1) is not a local integer". The quantum per mode as the sweep was the earlier law's, and Tensor24's w_c = 3 key s lost it.
- (h2), "One photon on two bobs: the anticoincidence" (line 1744): alpha = 0 for one quantum, against Grangier's alpha = 0.18 +- 0.06.
- item 4, "The lone quantum's detection" (line 1839): "two far detectors both rising on one quantum with the chance f_1 f_2, a quarter at an even split, where nature gives never both".
- item 49 (line 1885): "a single quantum cannot travel as a spherical wave beyond r of about 0.28 A Meshes" (a finding by name).

**The removal.**
- The bunching, the antibunching and the partition come from law 7's one click (CHECKED).
- **Candidate** for the quantum per mode, generic for every hand train: the click of a whole reads the sweep at the key, q = (S + r_S) div key, Rule3 of the local sweep, every hand alike and the light included, with no division by a sine (the light's winding w_c = 3 key s is 0 at s = 0). The energy one click books is then key times 2 sin w, Planck's relation in the lattice's variable. **OPEN** (David): the sweep counts the two senses' difference, so a standing wave has none; and for the light as a real transverse field (root V) no local number exists (T. D. Newton and E. P. Wigner, Rev. Mod. Phys. 21 (1949) 400), so its click is the absorber's own transition, as scribe-5 line 915 has it.
- **The spread single quantum** (Grangier): an engine of classical fields with quantized clicks is a semiclassical theory, and Clauser's and Grangier's measurements refute every such theory. So item 17's anticorrelation stands, unless each quantum is a local token (2.2). **Theorem** (with the token OPEN).

### 2.2 Item 18, Born's rule for position

**The contradiction (item 18):** "a split across Node-clocks would need a draw that reads beyond one Mesh (row 55)."

**In the clocks.** A quantum as a tooth riding a hand: at each tick the tooth stays at its Node-clock or crosses one Mesh, drawn by the sizes of the hand's flux out across each of the six Meshes and of what stays. The draw reads the Node-clock and its six Meshes alone.

**In the tensors.**
- The global phase (the hand's quarter turn) and the real symmetric pull make the sweep's continuity exact, the Mesh's lead at the middle slot its flux (2.1). A token with the hop sizes (max(0, flux out on Spoke j) on each Spoke, the density less their sum to stay) carries the law of position P(x) = sweep(x) / Q exactly from tick to tick wherever all sizes are non-negative: P_next(y) = (rho_y - SUM_out + SUM_in) / Q = rho_y(t + 1) / Q, by the flux's antisymmetry. **PROVED; CHECKED** (F5 D1: exact on the 2 of 8 ticks of the two-wave test where every size is non-negative; the other 6 ticks have a negative size or density; the centred lead breaks it, F5 mutant).
- In the three operations: the positive part is the flux times section 26's sign quotient [x >= 0] = 1 + x div (x x + 1), and the hop is a click of a split among seven parts. Whether that positive part is a clamp is Sofer's to rule.

**The history.** J. S. Bell, Phys. Rep. 137 (1986) 49, "Beables for quantum field theory": a lattice with the fermion number as the local beable, jumping at rates set by the current, reproduces quantum field theory's statistics. D. Durr, S. Goldstein, R. Tumulka and N. Zanghi, "Bell-type quantum field theories" (quant-ph/0407116, J. Phys. A, 2005).

**The project's earlier handling.** scribe-5 line 1053: "the Node-clocks' notches carry the winds and never the count (... a count in the notches would let a far detector credit twice from one photon before the hole reached it, against Grangier, Roger and Aspect 1986 ...)". The count as state was refused (a decision).

**The removal. Candidate:** a token per quantum, every train alike, hopping by its own train's flux, its draw local (law 9). It gives Born's rule for position and Grangier's anticorrelation for one quantum locally, since the token stands at one Node-clock. **OPEN** (David):
- the sizes go negative at the discrete tick (F5 D1: 6 of 8 ticks), so the rule needs a tick fine against the flux or another size form;
- the token is state the plan does not hold (a count per train and Node-clock);
- two or more quanta need the joint amplitude, not one flux each (2.3);
- a single photon split over two paths and read with local phase references violates a Bell inequality (S. M. Tan, D. F. Walls and M. J. Collett, Phys. Rev. Lett. 66 (1991) 252; B. Hessmo, P. Usachev, H. Heydari and G. Bjork, Phys. Rev. Lett. 92 (2004) 180401), which no local token reproduces: that part of item 18 is root IV's.

### 2.3 Item 19, many quanta and the vacuum

**The contradiction (item 19):** "no entanglement of many, no exchange forces, no Casimir effect, Lamb shift, Hawking radiation or running alpha; the calibre's integers are not renormalized couplings; confinement needs link variables the engine lacks."

**In the tensors.**
- **The theorem.** The board's state is a point of the product of the Node-clocks' integer sets, so its size adds over the Node-clocks, while an n-quantum state is a vector of the tensor product, whose size multiplies. One field per train holds a one-quantum amplitude or a coherent field, and law 7's click builds from them the symmetrized products, the permanents and determinants of Fock space's product states (F5 C). A state that is no such product cannot be held. **PROVED.** So entanglement of many quanta is absent, and the exchange forces stand only for product states. Root IV's theorem (Bell) is the same fact read at a distance.
- **The vacuum.** A board at rest with every fine tooth at its mid tooth has no zero-point motion; a classical zero-point field of random phases (T. H. Boyer, Phys. Rev. 182 (1969) 1374) would be a declared setting. So Casimir's force, Lamb's shift, Hawking's radiation and the running of couplings stay absent. **PROVED** (absent by construction).
- **Confinement.** The pawls are a Z2 link sign: F. J. Wegner, J. Math. Phys. 12 (1971) 2259, the Z2 lattice gauge theory, has an area-law phase. Colour confinement needs non-abelian links: K. G. Wilson, Phys. Rev. D 10 (1974) 2445. **OPEN** (David; root V).

**The history.** P. Jordan and E. Wigner, Z. Phys. 47 (1928) 631: lattice fermions from two-state systems. V. Fock, Z. Phys. 75 (1932) 622: the space of a variable number of identical quanta.

**The project's earlier handling.** scribe-5 line 458, "The atom is a bound bob of the holder of the sign": "nature's Coulomb operator is normal-ordered and counts pairs of quanta, N (N - 1) / 2, while the great clock's drive counts products of winds, N^2 / 2"; and line 1550, helium's 1.4 percent "the two-position amplitude no great clock of one-position hands holds". A finding by name.

**The removal.** The n-quantum click removes the bunching and the exclusion's absence (draft E). **Theorem, permanent:** no entangled many-quantum state and no zero-point vacuum on one classical field per train.

### 2.4 Item 7, temperature

**The contradiction (item 7):** "There is no common temperature (row 75): the unsprung hand's wind stands 10^7 above matter's."

**In the clocks.** Bobs and light trade whole windings at the chimes. At the balance the chimes up and the chimes down come equally often, by the rewind's symmetry; a light chime is helped by the windings already there (the bunching, law 7's permanent), and a matter chime is blocked by the twin already there (Pauli, law 7's determinant).

**The route.** Detailed balance follows from the exact T (C R, 1.5): every click and its time-reversed click have equal odds in balance. With law 7's two-quantum odds, the chimes' rates carry 1 + n on light and 1 - n on twin matter. Einstein's argument then gives Planck's spectrum and Fermi-Dirac occupation (A. Einstein, Phys. Z. 18 (1917) 121). **PROVED** (Einstein's argument, given its two inputs).

**The obstacle, measured.** DAVID-TEMPERATURE.md (toys-5 536d7ea9b, 2026-10-28, 01:2x UTC): "The close moves 1,766 light windings in 250 ticks ... against a sea of about 2.6 x 10^8 windings ... 7 parts in a million", so "the light's black body (row 48) would take about 10^5 times the run". A nearly linear lattice need not share its wind: E. Fermi, J. Pasta and S. Ulam, Los Alamos report LA-1940 (1955), found almost no tendency toward equipartition and a near-recurrence.

**The project's earlier handling.** scribe-5 line 1905 (2026-10-27, David): "temperature and equipartition need no new law but the books to close first"; line 1913, "The held field": "temperature and equipartition NOT SHOWN (the largest family's wind per mode, the light's, stands 31,888,184 times the least's at the last bang ...)".

**OPEN** (David): the chimes' factor 1 + n is not derived (a chime reads a hand's own wind at its winding); and the exchange rate.

### 2.5 Item 24, recurrence, and law 10

**The contradiction (item 24), as TENSOR24.md now words it:** "Under law 10 this is no contradiction but the circle itself ... every bang shows more along it, and it closes at the recurrence".

**In the clocks.** A great clock of whole numbers whose integers stay bounded has finitely many settings, and a clock that runs back exactly has no setting with two pasts, so it returns to its setting.

**In the tensors.**
- A bijection's bounded orbit is a cycle: the first repeated state has one past, so it is the start. **PROVED; CHECKED** (F5 E1: the integer one formula on a ring of 3, W = 9, a hold of 11, returns exactly to its setting at period 6).
- Unbounded orbits exist: the massless uniform mode at the hold 0 drifts one notch a tick for ever (F5 E2), and Rule3's rounding feeds the staggered mode (F3 E2). So the board's integers need not stay bounded, and on such an orbit there is no return.
- **Law 10's two sentences.** "Every bang shows more than the one before" and "time on the board is a circle": a reading of the board that grows at every bang cannot do so on a closed circle of bangs, since on a cycle B1, ..., Bn, B1 the step from Bn back to B1 must fall. **PROVED.** So along the circle every bang shows more except the one that closes it, or the integers grow without bound and there is no circle. For the owner (TENSOR24.md 30, item 11, "Where a derivation meets one of the owner's earlier laws").

**The history.** H. Poincare, Acta Math. 13 (1890) 1; E. Zermelo, Ann. Phys. 57 (1896) 485 (the recurrence objection to Boltzmann's H-theorem), with Boltzmann's reply that the recurrence time is astronomically long.

**The project's earlier handling.** Postulate 4 (line 35): "the great clock returns, the swing recurs ... no integer of its state is lost at any act". A postulate.

## 3. Root V: the light's kind

### 3.1 Items 20 and 22: the light as the Mesh's link

**The contradictions:** item 20, "The light is a complex scalar, not a transverse field of spin one; the offset, the potential, never clicks"; item 22, "No gauge invariance without link variables: the offset's U(1) holds only for gauge functions linear in the site, and the offset carries four components."

**In the clocks.** Light as the Mesh's own turning. Each Mesh's odd gear says how far its two Node-clocks' twelve-o'clock zeros are set apart. A Node-clock may reset its own zero, the gauge, and its six Meshes' gears take the difference, as Einstein's clocks may be reset and only a round trip is read. Only the turning around a plaquette, the curl, is physical, and it waves in the two directions across its travel.

**In the tensors.**
- **The link's kind.** The six Spokes are A1 + E + T1 under the 24; a gear on the Mesh, odd under the Mesh's reversal (A_(-j)(x + e_j) = -A_j(x)), is the T1 part. **CHECKED** (F6 A1, A2). So a Node-clock holding its three forward Meshes' gears holds a T1: the offset's three odd gears read on the Meshes.
- **The gauge.** The A1 function lambda at the Node-clocks acts as A_j(x) -> A_j(x) + lambda(x + e_j) - lambda(x). On the torus of side 3 and of side 4, curl grad = 0 exactly, rank grad = N - 1 and rank curl = 2N - 2. So the 3N link gears are N - 1 pure gauge, 2N - 2 transverse (two per wave number k != 0: the light's two polarizations) and 3 harmonic (the torus's three loops). **CHECKED** (F6 B1 to B3).
- **Maxwell is the one formula's pull.** curl^T curl + grad grad^T = -LAPLACIAN on the Meshes, exactly. So -curl^T curl A = LAPLACIAN A - grad(div A): the one formula's own pull less the gradient of the divergence, a T1 from the A1 divergence of a T1 (the product table's route), read as two one-Mesh reads. On transverse gears it is the one formula's pull, and the light's band stays cos w = (1/3) SUM cos k_a at the edge. **CHECKED** (F6 B4).
- **The 24** commute with the gauge's gradient and with curl^T curl on the Meshes. **CHECKED** (F6 C1, C2, all 24).
- **Gauss's law kept.** Hands on the one formula and the link gears in the temporal gauge, A+ = 2A - A- - (1/3) curl^T curl A + J, with J the Mesh's flux of the sweep: div E - rho is the same at every Node-clock over 10 ticks. **CHECKED** (F6 D1; with the centred lead as the source it fails, F6 mutant). The constraint is local, kept by the sweep's continuity.
- **The isotropy the gauge gives.** The T1 light's long waves are isotropic only through the gauge (1.1, F1 D).
- **The hands' turn.** The Gaussian integers of norm 1 are 1, i, -1 and -i. **CHECKED** (F6 E1). So a hand's exact turn across a Mesh by one Gaussian integer is a Z4 link. M. Creutz, L. Jacobs and C. Rebbi, Phys. Rev. D 20 (1979) 1915: four-dimensional Z_N lattice gauge theories have one first-order transition for N <= 4 and two for N >= 5, the massless phase between them (with S. Elitzur, R. B. Pearson and J. Shigemitsu, Phys. Rev. D 19 (1979) 3698). A fine phase on a hand has no exact unitary integer form.

**The history.** K. G. Wilson, Phys. Rev. D 10 (1974) 2445: the gauge field as link variables, the gauge transformation at the sites. J. Kogut and L. Susskind, Phys. Rev. D 11 (1975) 395: the Hamiltonian form, the temporal gauge and Gauss's law at each site. K. S. Yee, IEEE Trans. Antennas Propag. 14 (1966) 302: Maxwell on a staggered cubic lattice, E on the links and B on the plaquettes. The light's two helicities as the phase of E + iB: M. G. Calkin, Am. J. Phys. 33 (1965) 958; S. Deser and C. Teitelboim, Phys. Rev. D 13 (1976) 1592; I. Bialynicki-Birula, Acta Phys. Pol. A 86 (1994) 97 (the photon's wave function).

**The project's earlier handling.**
- scribe-5 line 1905 (2026-10-27, David, DAVID-FOUR-PHENOMENA.md): "the polarization of light is in the calibre and needs no new law (it lives on the offset, the transverse potential following the emitter's current 10 to 20 times over)". Measured, with "no setting form lays a wave on the offset itself".
- line 458 lists, among "what would solve everything", "transverse light (non-local, a constraint over space)". F6 D refutes the non-locality: on the Meshes the constraint is Gauss's, kept locally by the continuity.
- line 1537, "A static sign train is the electric potential in the temporal gauge", and line 1541, "The Lorentz form on the sign holder's four gears" (a hypothesis under its own name, the declaration `form: lorentz`, 2026-10-21).

**The removal. Candidate:** the light is the offset's T1 read on the forward Meshes, stepped by the one formula's pull less grad div (generic: every T1 link train alike), in the temporal gauge, sourced by the Mesh's flux of every hand's sweep, its gauge the A1 function at the Node-clocks. It removes item 22 (gauge invariance with link variables, four components down to two) and item 20's spin (two transverse helicities, T1). **OPEN** (David):
- the hands' transport by the link's fine phase: the Z4 links (no massless phase), three lifting shears (reversible, not exact in the norm; the architect's note, TENSOR24.md 31), or a Pythagorean turn with a carry;
- the light's click: a real transverse field has no local number (Newton and Wigner), so the click is the absorber's transition (scribe-5 line 915); or the Riemann-Silberstein hand E + iB of kind T1, whose sweep is the light's helicity (Calkin);
- the shears and the metric's own gauge (section 24, item 4) on the same plan.

## 4. Root VI: the course of the one big bang

### 4.1 Item 25, the flat torus

**The contradiction (item 25):** "T^3 is flat, and a flat Friedmann universe does not recollapse: the head's cycle is F1 and law 4, the time reversal put in."

**In the clocks.** The great clock's time gears climb together. On a torus nothing pulls the stretch back but its own spring (the metric's mass, item 14) or the rate chain's last notch. The turnover is the clock's own rewind at the top.

**In the tensors.**
- **No turnaround on the torus, homogeneous or not.** M. Gromov and H. B. Lawson, Ann. of Math. 111 (1980) 209, Corollary A: every metric of non-negative scalar curvature on the torus T^n is flat (R. Schoen and S.-T. Yau, Manuscripta Math. 28 (1979) 159, for T^3). At a turnaround (a maximal slice, mean curvature 0) general relativity's constraint reads R = 16 pi G rho + K_ij K^ij + 2 Lambda >= 0 for rho >= 0 and Lambda >= 0, so the slice is flat with rho = 0 and K_ij = 0. A torus with matter has no turnaround. **PROVED** (from the cited theorem). It extends draft C's C1 ("The flat torus never turns", the A1 course) to every inhomogeneous course. For the engine it holds where its metric half reaches general relativity's constraint, which the physicist found unstated: **OPEN** (David's six items, section 25 item 3).
- **The two brakes that remain**, each a declared number on the torus: Lambda < 0, which in the one formula is exactly the time gear's own spring (draft C's C5: Lambda = -(1/2)(s_R / rim)); or the rate chain's zero, the one turn found with no declared number (draft C (a)), which stands on BH-S1's restore (R10).
- **The bounce by symmetry.** Law 4's turnover is the exact T (1.5's C R with the kinds' signs) used once at the top: an involution, decided and not derived (the owner's word of 2026-10-23, "if the time reversal works and produces repeated bangs, enter it"; scribe-5 line 1602). Its trigger can come from no curvature on the torus.

**The history.** A. Friedmann, Z. Phys. 10 (1922) 377 and Z. Phys. 21 (1924) 326: the closed (positively curved) universe recollapses, the flat one does not. T. Gold, Am. J. Phys. 30 (1962) 403: the thermodynamic arrow follows the cosmological one, reversed in a contracting universe. Spatial topology and recollapse: J. D. Barrow, G. J. Galloway and F. J. Tipler, Mon. Not. R. Astron. Soc. 223 (1986) 835 (the closed-universe recollapse conjecture); D. M. Witt, arXiv:0908.3205 (a maximal slice needs a metric of non-negative scalar curvature on the Cauchy slice).

**The project's earlier handling.** scribe-5 line 448, "The clusters' cosmology": "the algebra as written derives no expansion of space", "the law has no dark energy, the finding of its own lines, standing by name with no mend"; line 695: "nature's Friedmann constraint in form, its coefficient 1 / n_f per train where nature's has 1 / 3"; line 1602, "The turnover" (the owner's decision of 2026-10-23). Draft C (derive/C, verified): C1 to C6.

**The removal.** None by curvature (theorem). The turnover by T is a decision (law 4), and law 10 makes the circle a law not to be crossed. **OPEN** (draft C, David): the turn's trigger without a declared number.

### 4.2 Items 15 and 24

Item 15 (the course's runaway below the cap) is draft C's. Item 24 is 2.5.

## 5. Root IV, read for context

Root IV is not mapped here. Two of this draft's checks bear on it: the integer precursor beyond light's cone (1.3, F2 C), and the many-quantum theorem (2.3), which is Bell's theorem read on one board.

## 6. Dark matter (item 25's second part; the owner's question of 13:1x UTC)

"Is there a solution for what dark matter is? In fact it does not click, does it?" Every wind pulls the great clock (the forms, the regulator's source, sum every driven train alike), and only a wind that completes a whole winding clicks and is seen.

### 6.1 Candidate 1: a massive train with no charge

**In the clocks.** A one-gear train holds a single gear per Node-clock, with no twelve-o'clock shadow: no hand. The Mesh's quarter turn moves only hands, so it cannot turn it; it has no hand to sweep, so it neither winds the offset nor is wound by it; no bob's chime takes its winding. Its notch beats on its own spring, and its wind loads the regulator's drive like every gear's, so the time gears slow where it gathers. It is seen only by the slowing it causes in the clocks around it.

**In the tensors.**
- **No current by its kind.** A one-gear train is a real field, its own conjugate (Frobenius-Schur +1 with a real own part). Its sweep Im(conj(a-) a) and its lead Im(conj(a) a_j) are 0 identically, so it sources neither the offset's time gear nor its odd gears, and the light's couplings Q A0 and J . A vanish on it. **PROVED; CHECKED** (F7 A1, A2, 20 random boards; with an imaginary part both fail, F7 mutant). Of the hand's four exact turns only 1 and -1 keep it real: no phase can act on it. **CHECKED** (F7 B1).
- **It gravitates.** The regulator's source, the forms, is the sum over every driven train of u_in u_out + (-a F) div w, the one-gear trains among them (the head's tick.impulse). **CHECKED** on the head (F7_dark_head: the forms split train by train sum to the head's own at every Node-clock at 250 of 250 ticks at 500 quanta and 60 of 60 at 5,000,000).
- **It is dust.** The homogeneous beat a+ + a- = 2c a has the discrete Lagrangian (a_t - a_(t-1))^2 / 2 - (1 - c)(a_t^2 + a_(t-1)^2) / 2, the homogeneous pressure, and its average over each exact period (c = 1/2, 0, -1/2: periods 6, 4, 3) is 0, while the wind stays constant and positive. **CHECKED** (F7 C1, C2; with the spring's term doubled it fails). M. S. Turner, Phys. Rev. D 28 (1983) 1243: a coherent oscillation in a quadratic potential has zero mean pressure and dilutes as matter.
- **Not a fermion.** No twin pair but 0 is its own conjugate (F4 F3), so a twin train cannot be its own antiparticle; a neutral twin train is a coupling of 0, not its kind (its two-time density is kept by the common quarter turn, F7 E1). So in the kinds of 2O a train dark by its kind is a boson: a real field.
- **The linear terms, closed by C and the gauge.** The 24's table also allows the gear's own A1 terms with the offset, a A0 and a div A (A1 x A1, and A1 x the divergence of a T1). C closes them, not the 24: the offset is C-odd and a real gear C-even (F4's table: Q A0 is C-even with Q C-odd), so both terms are C-odd; a A0, R-odd and P-even, is CPT-odd too (CPT = P R). Both also move under the gauge (A0 by lambda's change over a tick, div A by lambda's LAPLACIAN, F6 B). **PROVED** (from F4's table and F6's gauge). So the plan's "its contraction with the offset (A1 + T1) is 0" (section 18, item 25) holds for the current by the kind, and for the gear itself by C and the gauge.
- **The door the kinds still open.** The 24's table gives a one-gear train A1 contractions with the light's quadratic forms: with the plan's light (a complex A1 hand) its density \|z\|^2; with the link light E . E - B . B (kept by all 48) and E . B (kept by the 24, reversed by every mirror: the axion's coupling). **CHECKED** (F7 D1, D2). So "a one-gear train never couples to the light" (TENSOR24.md 19, "A coupling in two parts") holds for the current, not for these. They vanish under one more symmetry of the families' own: the dark gear's negation a -> -a, which keeps every term even in it. Then only pairs couple (a^2 times a light form), the dark quanta are made and unmade in pairs, and the lightest odd train is stable. With the pair coupling's integer 0 the train couples by gravity alone.

**The history.**
- F. Zwicky, Helv. Phys. Acta 6 (1933) 110 (the Coma cluster's missing mass).
- B. W. Lee and S. Weinberg, Phys. Rev. Lett. 39 (1977) 165 (a heavy neutral lepton's relic density: the WIMP's argument).
- A real scalar odd under its own Z2: V. Silveira and A. Zee, Phys. Lett. B 161 (1985) 136; J. McDonald, Phys. Rev. D 50 (1994) 3637.
- The axion as a classical field: J. Preskill, M. B. Wise and F. Wilczek, Phys. Lett. B 120 (1983) 127; L. F. Abbott and P. Sikivie, Phys. Lett. B 120 (1983) 133; M. Dine and W. Fischler, Phys. Lett. B 120 (1983) 137. Its photon coupling read in a magnetic field: P. Sikivie, Phys. Rev. Lett. 51 (1983) 1415.
- Fuzzy dark matter, a classical wave below the quantum's scale: W. Hu, R. Barkana and A. Gruzinov, Phys. Rev. Lett. 85 (2000) 1158. A scalar field's Jeans instability: M. Yu. Khlopov, B. A. Malomed and Ya. B. Zeldovich, Mon. Not. R. Astron. Soc. 215 (1985) 575.

**The project's earlier handling.** scribe-5 line 1606, "Dark matter in kind is a theorem of the gears" (a derived line, standing at the alignment of 2026-10-25): "a free quantum of a gapped train of dimension 1 ... has W = 0 and reads no sign holder ... the invisibility rests on W = 0, derived from the table's shapes, and on no declared transition for the scalar train in any declared bob, a declaration of the universe's files ... it gravitates and is invisible, dark matter in kind ... Status: derived in kind under the table, open in amount". And line 448's second candidate, the frozen Node-clock, a hypothesis by name. The candidate is the earlier law's, and the plan's coupling in two parts restates it.

**Refined.**
- Dark to the light's current by its kind: **PROVED**.
- Dark to the offset's linear terms by C and the gauge: **PROVED**.
- Dark to the light's quadratic forms only under its own Z2 with the pair coupling 0. **PROVED** (by the 24's table); the Z2 is a statement about the calibre's rows, every term even in the dark gear.
- On the plan as written the coupling of the clicks is the spring itself after R4 (TENSOR24.md 28), so every massive train would couple; the darkness needs the coupling in two parts (section 19) and the light as root V's link.

### 6.2 Candidate 2: the remainders

Wind spread below one winding at every Node-clock never clicks and gravitates. **Refuted as dark matter:** darkness by dilution is blind to the kind. It would hide dilute light and dilute charged matter alike, which nature detects quantum by quantum (Grangier; the prompt photoelectric effect). It is item 17's defect, and it goes with item 17. **PROVED** (by the clicking rule's train-blindness).

### 6.3 Measured on the head's one big bang

F7_dark_head.py runs world_bang.json on the t24 worktree's own src, read-only. A copy of the head's impulse loop splits the forms train by train before the head's impulse runs, with no write, and asserts after it that the trains' forms sum to the head's at every Node-clock (the split's second reading). **CHECKED** (250 of 250 and 60 of 60 ticks).

| the one big bang | the forms of the trains that never click (the held field, the offset) | of all the forms | the clicks |
| --- | --- | --- | --- |
| 500 quanta, ticks 1 to 250 (one bang, at tick 12) | 372,465,988 | 7,089,831,832 (5.3 percent) | 80 births, 2,560 chimes; births name the hands 1 to 4, chimes the matter hands |
| the same, ticks 13 to 250 (after the bang) | 372,460,676 | 4,473,160,208 (8.3 percent) | |
| the same, tick 250 alone | 2,262,184 (the offset 2,262,160, the held field 24) | 2,268,564 (99.7 percent) | |
| 5,000,000 quanta, ticks 1 to 60 (bangs every 5 ticks from tick 3) | 455,936 | 396,023,783,583,584 (about 1.2 x 10^-9) | 64 births, 5,632 chimes |

- The never-clicking wind on the head is almost all the offset, the potential: a dark electromagnetism, item 20's contradiction, and not nature's dark matter.
- The held field, the head's one real massive train, carries 24 of 2,268,564 at tick 250 and follows the masses that source it (its range per Node-clock 28..58 at tick 50, 0..4 at tick 200). It forms no halo of its own. At 5,000,000 quanta every Node-clock holds it alike (34..34): no structure at all.
- **CHECKED** (F7_dark_head_500.txt, F7_dark_head_5M.txt).

**The probe the new engine should run**, with two readings that can fail: the ledger's wind per train (the gravitating; TENSOR24.md 31) against the click record's windings per train (the clicking), per bang; and the dark train's contrast (its wind's spread over the board) against the bright matter's, per bang, from a setting that sets a dark displacement (data, as the axion's initial displacement) and breaks the seed once. Halos: the dark contrast grows about the bright wells.

**OPEN** (David): the halos (the regulator's Jeans growth, draft C); the dark amount (the setting's integer; nature's ratio, about 5.4, is not derived); whether the pair coupling 0 is the calibre's integer or follows from a symmetry not listed here.

## 7. The probes

Every probe is integer or Fraction arithmetic only (python3 -I), with a pass criterion per check and mutants that must fail; each output is kept beside it.

| probe | what it checks | its result | its mutants (each fails) |
| --- | --- | --- | --- |
| F1_kinds.py | the 24 and the 48; the kinds' characters; invariant polynomials of degree 0 to 9; long-wave operators by kind; the T1 gauge reduction; the band's long-wave series | 21 checks pass (F1_kinds.txt) | sign_E, hold, gauge (F1_kinds_mutants.txt) |
| F2_cone.py | Cauchy-Schwarz on a box of side 13; the rational Green's function (9 ticks, side 21); the integer front on the octant (24 ticks, 10^3 and 10^6 notches); Pell's boost and the stencil | 16 checks pass (F2_cone.txt) | edge, pell, parity (F2_cone_mutants.txt) |
| F3_doubler.py | SIGMA on the rational leapfrog (12 ticks, light and r = 3/5); its parities; the head's gearing at the bang's calibre; SIGMA with Rule3's carry and the staggered mode's feed (400 ticks) | 15 checks pass (F3_doubler.txt) | hold, neighbour, head (F3_doubler_mutants.txt) |
| F4_cpt.py | the parity table of 15 readings under R, P, C and their products (6 random states); the three-fold turn on the twin readings (40 pairs); the Frobenius-Schur indicators; the twin pairs fixed by C (a box of 7^4) | 13 checks pass (F4_cpt.txt) | lead_now, kramers, a0 (F4_cpt_mutants.txt) |
| F5_quanta.py | the sweep's conservation and continuity (10 ticks); the exact waves and the action per mode; the splitter's per and det; the token's equivariance; the ring's recurrence and the uniform drift | 15 checks pass (F5_quanta.txt) | centred, permanent, token, hold (F5_quanta_mutants.txt) |
| F6_link.py | the Spokes' kinds; the lattice's complex on the torus of side 3 and 4 (ranks exact); the 24 on the links; Gauss's law over 10 ticks; the norm-1 Gaussian integers | 14 checks pass (F6_link.txt) | current, curl, unit (F6_link_mutants.txt) |
| F7_dark.py | a one-gear train's sweep and lead; its turns; dust on exact periods; E . B and E . E - B . B under the 48; the twin charge's phase | 8 checks pass (F7_dark.txt) | complex, pressure, axion (F7_dark_mutants.txt) |
| F7_dark_head.py | the one big bang on the head's src (read-only): the forms train by train, the split's second reading, the clicks by train | 250 of 250 and 60 of 60 ticks (F7_dark_head_500.txt, F7_dark_head_5M.txt) | the split's assertion (the second reading) |

The explorations behind F2 C and F4 R2 are in explore/ (front_octant.py, threefold.py, log_keys.py). lawgrep.py is a reading tool for the law's long lines. The two-run head probe used the repository's venv314 interpreter with -I.

## 8. What it replaces and what moves

- **Section 18, root II:** the big law's "isotropy ... for waves long against the Mesh" holds for scalar, hand and twin trains by the 24, and for vector and tensor trains only through a gauge (1.1). "One limiting speed for every train" becomes one law of the grips with speeds a function of the rest beat (1.2). "A term from the kinds that lifts the doublers" is the hold, and the vacuum's edge is the choice left (1.4). "C from the kinds' conjugation" stands, and the CPT check fails on S . J (1.5).
- **Section 24, item 5 (the one-hand coupling):** S . J is CPT-odd; SW . J is the CPT-even form with V - A's pattern (1.5).
- **Section 30, what goes back to the owner:** law 10's two sentences at the circle's closing bang (2.5); the doubler's vacuum (1.4), since (a) changes light's speed.
- **Draft D:** the two-time spin's y sign (1.5).
- **Rows:** 40 (the photoelectric threshold) and 48 (the black body) through the quantum per mode (2.1) and the temperature route (2.4); 55 (the two slits' clicks) through the token (2.2); 67 (CPT) through the term-by-term check (1.5); no row is benched here.
- **The law's text:** scribe-5 line 1419's refusal of even boards is a declaration the owner's ruling of 11:1x UTC strikes (1.4); line 915's quantum per mode is the earlier law's derivation that the plan's w_c = 3 key s lost (2.1); line 458's "transverse light (non-local)" is refuted by F6 D (3.1); line 1606 is the dark-matter candidate's earlier form (6.1).
- **Contradictions that stay, named:** the cube's slowing (1.1); the Mesh's rest frame and the speeds' spread at O(w0^2) (1.2); the Courant bound and the integer precursor (1.3); Nielsen and Ninomiya for any first-order chiral form (1.4); entanglement of many and the zero-point vacuum (2.3); Grangier's anticorrelation without a token (2.1); no turnaround with matter on the torus (4.1).

## 9. OPEN

| what | what blocks it | whose |
| --- | --- | --- |
| the doubler at the vacuum: the teeth count off the edge, or the doubler a taste | no symmetry fixes the hold at the full rate; (a) changes light's speed | David, then the owner |
| the one-hand coupling as SW . J | its exact rewind (SW reads the before slot); CPT on the clicks | David |
| the limiting speeds under the sources | J's couplings may feed differences (Collins and others) | David |
| the quantum per mode as the sweep at the key | a standing wave has no sweep; a real light has no local number | David |
| a token per quantum for Born and Grangier | negative sizes at the discrete tick; the token as state; many quanta | David, Sofer (the positive part) |
| the chimes' factor 1 + n; the exchange's rate | not derived; 7 ppm in 250 ticks | David |
| law 10 at the circle's closing bang | a cycle has no strictly growing reading | the owner |
| the light as the Mesh's T1 | the hands' turn by a fine phase (Z4 or a carry); the light's click | David |
| the metric's isotropy and constraints | the diffeomorphism gauge on the lattice | David (section 25, item 3) |
| the course's turn on the torus | no curvature can give it; the rate chain's zero stands on R10 | draft C, David |
| dark matter's halos and amount | the regulator's Jeans growth; the setting's integer | David |
| the second hand for every claim here | protocol step 5 | a verifier who did not write it |
