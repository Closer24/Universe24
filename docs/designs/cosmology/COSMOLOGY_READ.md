# The expansion of the universe, closed or open, dark energy and dark matter: what the world's data say, what the algebra of the law gives, and what it cannot decide (CLOSER24, a physicist and a mathematician in one agent, 2026-09-24; docs only, no run, no pin, nothing decided)

The model owner's word of 2026-09-24, 02:47Z (Hebrew, through the Boss, translated):
"Activate a physicist and a mathematician in one agent, who will say what can be
inferred about the expansion of the universe, a closed or an open universe, from the
data that exists in the world today and from our algebra and our physics: dark
matter, dark energy. It works on its own machine so it does not disturb us. Call it
CLOSER24." This page is that reading, on `origin/main` at `b96e6eea` (2026-09-24),
against [docs/ALGEBRA.md](../../ALGEBRA.md) chapters 1, 5 and 8,
[POSTULATES.md](../../../POSTULATES.md) sections 10 and 26,
[DARK_ENERGY.md](../light_outside/DARK_ENERGY.md), [Light
Outside](../light_outside/DERIVATION.md) II.8, [Einstein
Outside](../einstein_outside/DERIVATION.md) II.10 to IV,
[DARK_SECTOR.md](../far_lamp/DARK_SECTOR.md), [SCHEDULE.md](../detector_law/SCHEDULE.md)
and [DECLARATIONS.md](../detector_law/declarations/DECLARATIONS.md) section 4. It
changes no page, declares and moves no pin, runs nothing, and enters neither the
paper nor the GO. Its arithmetic is cosmology_read.py (`docs/designs/cosmology/cosmology_read.py`, deleted 2026-09-26) with its
output [cosmology_read.out](cosmology_read.out), pure integers and fractions.

**The rules and the kinds.** Every symbol is named in English at its first use; a
GameBoard reading is a diagnostic; only a detector's click is a measurement; every
match is "matches nature", never "is nature"; a number whose kind is not named is
not a result. The kinds of this page: DATA (a published number with its source, its
printed value and its printed uncertainty; the source's own abstract or table cited
where the reader can find it, else RECALLED, NOT VERIFIED; "(snippet)" marks a
number read today in a search excerpt of the paper's abstract, never in the paper,
the rule of [SOURCES_VERIFIED.md](../detector_law/SOURCES_VERIFIED.md)); DERIVATION
(it follows from the law's algebra as ALGEBRA.md states it); COMPUTATION (a closed
form on the repository's integers, or on DATA, made on the host); HYPOTHESIS (it
needs a rule or a declaration outside the law, named under its own identity); NOT
DECIDABLE BY THE ALGEBRA (the algebra says nothing); INPUT (a declared number of a
world). The symbols: H_0 the Hubble constant; Omega_m, Omega_Lambda, Omega_b,
Omega_c, Omega_K the density parameters of matter, the cosmological constant,
baryons, cold dark matter and curvature; h the reduced Hubble constant in Omega h^2
(here only, the action elsewhere); q_0 the deceleration parameter; w_0, w_a the dark
energy equation of state and its slope; A_L the lensing amplitude; z the redshift;
tau a flight time; beta the speed over c; gamma_m the Lorentz factor at the massive
kind's cone c_eff (ALGEBRA.md 8.1); K the intervals per hop; k_crowd the crowd's
stretch of a count; r_B a detector's own rate; g_1 the growth of the emitters' clock
stretch per Hubble length of flight time (DARK_ENERGY.md section 2).

## 1. The data of the world today (kind DATA)

| Quantity | Value as printed | Source | Mark |
| --- | --- | --- | --- |
| H_0, the CMB inference | 67.4 +- 0.5 km/s/Mpc (the paper's table 2: 67.36 +- 0.54, TT,TE,EE+lowE+lensing) | Planck 2018 results VI, Aghanim et al. 2020, A&A 641, A6, arXiv:1807.06209, the abstract | (snippet) the abstract's 67.4 +- 0.5; the two-decimal form RECALLED, NOT VERIFIED |
| Omega_m | 0.315 +- 0.007 (the table's 0.3153 +- 0.0073) | the same, the abstract | (snippet); the four-decimal form RECALLED |
| Omega_Lambda | 0.685 +- 0.007 (1 - Omega_m at fixed flatness; the table's 0.6847 +- 0.0073) | the same | COMPUTATION on the row above; the table's form RECALLED |
| Omega_c h^2, Omega_b h^2 | 0.120 +- 0.001, 0.0224 +- 0.0001 | the same, the abstract | (snippet) |
| The age | 13.797 +- 0.023 Gyr | the same, the table | RECALLED, NOT VERIFIED (not seen in an excerpt today) |
| Omega_K without BAO | -0.044 (+0.018, -0.015) at 68 percent (TT,TE,EE+lowE), a closed universe preferred at over 2.5 sigma, over 99 percent on the spectra alone | the same, its section on curvature; Di Valentino, Melchiorri and Silk 2020, Nature Astronomy 4, 196, arXiv:1911.02087, the abstract | (snippet) through the second paper's abstract |
| Omega_K with lensing, then with BAO | -0.0106 +- 0.0065 (with lensing); 0.001 +- 0.002 (with BAO) | the same, the abstract for the BAO value | (snippet) the 0.001 +- 0.002; the lensing-only value RECALLED, NOT VERIFIED |
| A_L, the lensing amplitude | 1.180 +- 0.065 (TT,TE,EE+lowE): "higher lensing amplitudes than predicted in base LCDM at over 2 sigma" | the same, the abstract for the sentence; the number from its section 6.2 | (snippet) the sentence; the number RECALLED, NOT VERIFIED |
| The sum of the neutrino masses | below 0.12 eV at 95 percent (Planck with BAO); below 0.072 eV at 95 percent (DESI 2024 with CMB, the prior sum above 0); below 0.064 eV (DESI DR2 2025 with CMB, flat LCDM) | Planck 2018 VI, the abstract; DESI 2024 VI, Adame et al. 2025, JCAP 02, 021, arXiv:2404.03002, the abstract; DESI DR2 II, Abdul Karim et al. 2025, Phys. Rev. D 112, 083515, arXiv:2503.14738, the abstract | (snippet) all three |
| The neutrino's mass, direct | below 0.45 eV at 90 percent (the effective electron neutrino mass, 259 days) | KATRIN, Aker et al. 2025, Science 388, 180, "Direct neutrino-mass measurement based on 259 days of KATRIN data" | (snippet) the number; the volume and page RECALLED |
| DESI 2024 BAO, the w_0 w_a hint | w_0 > -1 and w_a < 0 preferred; the departure from LCDM 2.6 sigma (DESI+CMB), 2.5, 3.5 and 3.9 sigma with Pantheon+, Union3 and DES-SN5YR; DESI alone flat LCDM Omega_m = 0.295 +- 0.015; H_0 = 68.52 +- 0.62 with the BBN prior and the CMB acoustic scale | DESI 2024 VI, the abstract | (snippet); the central values w_0 = -0.827 +- 0.063, w_a = -0.75 (+0.29, -0.25) with Pantheon+ from its table 3, RECALLED, NOT VERIFIED |
| DESI DR2 2025 | the BAO parameters in 2.3 sigma tension with the CMB's under flat LCDM; "dynamical dark energy offers a possible solution" | DESI DR2 II, the abstract | (snippet); its w_0 w_a significances 2.8 to 4.2 sigma RECALLED, NOT VERIFIED |
| Pantheon+ | 1701 light curves of 1550 supernovae, z from 0.001 to 2.26; flat LCDM Omega_m = 0.334 +- 0.018 from the supernovae alone | Brout et al. 2022, ApJ 938, 110, arXiv:2202.04077, the abstract; the sample Scolnic et al. 2022, ApJ 938, 113 | (snippet) |
| H_0, the local ladder | 73.04 +- 1.04 km/s/Mpc; "5 sigma" against Planck's | Riess et al. 2022, ApJL 934, L7, the abstract | (snippet) the number; the tension's 4.85 sigma this page's COMPUTATION (cosmology_read.out 2) |
| q_0 | -0.527 +- 0.011 (Planck's flat LCDM); -0.499 +- 0.027 (Pantheon+'s Omega_m); about -0.36 under DESI's w_0 at Omega_m 0.31 | COMPUTATION on the rows above, q_0 = Omega_m / 2 - Omega_DE (1 + 3 w_0) / 2 (cosmology_read.out 1) | a fitted parameter of a model, not one measurement ([NATURE.md](../../NATURE.md) row 3's note) |
| The CMB temperature | 2.7255 +- 0.0006 K | Fixsen 2009, ApJ 707, 916, the abstract | (snippet) |
| The CMB dipole | 3.36208 +- 0.00099 mK; v = 369.82 +- 0.11 km/s toward Galactic (l, b) = (263.998 +- 0.051, 48.265 +- 0.015) degrees | Planck 2018 results I, Akrami et al. 2020, A&A 641, A1, its dipole section | (snippet) |
| The Bullet cluster | 1E 0657-558 at z = 0.296: the total mass's centre offset from the baryonic mass's at 8 sigma; the lensing potential traces the galaxies, not the plasma | Clowe et al. 2006, ApJL 648, L109, the abstract | (snippet) |
| The rotation curves | 21 Sc galaxies, radii 4 to 122 kpc: "neither high nor low luminosity Sc galaxies have falling rotation curves" | Rubin, Ford and Thonnard 1980, ApJ 238, 471, the abstract | (snippet) |
| The radial acceleration relation | a_0 = 1.20 +- 0.02 (random) +- 0.24 (systematic) x 10^-10 m/s^2, 2693 points in 153 galaxies | McGaugh, Lelli and Schombert 2016, Phys. Rev. Lett. 117, 201101, the abstract | (snippet); the tree carries it in DARK_SECTOR.md section 1 |
| The baryonic Tully-Fisher slope | 3.9 +- 0.2 | McGaugh 2012, AJ 143, 40 | as the tree carries it (DARK_SECTOR.md section 1); RECALLED, NOT VERIFIED here |
| The baryon fraction | Omega_b / Omega_m = 0.157 | COMPUTATION on Planck's two densities (cosmology_read.out 3) | |
| BBN, the deuterium abundance | 10^5 D/H = 2.527 +- 0.030 (68 percent, seven systems); Omega_b h^2 from it 0.02166 +- 0.00015 +- 0.00011 (the paper's own), other pipelines 0.02189 to 0.02270 | Cooke, Pettini and Steidel 2018, ApJ 855, 102, arXiv:1710.11129, the abstract | (snippet) the D/H; the Omega_b h^2 values RECALLED, NOT VERIFIED (one excerpt gives 0.02189 to 0.02270 from three pipelines) |
| The topology bound | no matched circles of radius above 25 degrees in WMAP's first year; the fundamental domain larger than 24 Gpc | Cornish, Spergel, Starkman and Komatsu 2004, Phys. Rev. Lett. 92, 201302, the abstract | (snippet) the circles; the 24 Gpc RECALLED, NOT VERIFIED |
| Tolman's exponent | n = 2.28 +- 0.17 (R band) and 3.06 +- 0.13 (I band) before the galaxies' own evolution, against the expansion's 4 | Lubin and Sandage 2001, AJ 122, 1084, the abstract | (snippet); the tree's row 11c carries 2.3 to 3.1 |

What is not in this table: nothing here is a reading of the GameBoard; every number
is nature's, and the tree's own numbers enter only in section 2 by their kind.

## 2. What the algebra gives, by kind

The objects the questions are asked of (ALGEBRA.md 1.1, 1.6, 2): the GameBoard is
the cubic lattice with six Ports per Node and the translation group Z_X x Z_Y x Z_Z
of declared extents, each axis periodic or open (the world keys `shape` and
`boundary`); the law is one map **F** of the six verbs on the state vector at every
Node per interval; the six verbs act on the state (the levels, the counts, the
labels, the phases) and none of them acts on the set of Nodes, on the extents or on
the Links; the only output of the board is a click (3.1, 8.6); a measurement is a
count between clicks on a detector's own record or a ratio of such counts (3.2).
Everything below is read off these statements.

### 2 (a). Does the law have a notion of a global expansion at all

1. DERIVATION. The lattice has no scale factor. No verb changes the number of Nodes,
   the length of a Link or the extents (ALGEBRA.md 2.1 to 2.6: the translation, the
   bilinear form, the group-ring addition, the permutation, the evaluation and the
   division act on the state vector alone; 1.6: the extents are chosen per world).
   "The universe expands" as a statement about the GameBoard is therefore not a
   state the law can reach from any other state: a stretched lattice is not in the
   state space. The Inside has no a(t).
2. DERIVATION. A row's phase is never stretched in flight: the flight rule is blind
   (Light Outside I, L1 and L3, citing BEAM_LAW line 609: "a stretched phase per age
   would redshift light"; ALGEBRA.md 5.7, "the row's phase is never stretched").
   Under the massive record kind the light record's characters (omega, **k**) keep
   omega along a free flight on a periodic board (8.1, the band an identity of the
   linear recurrence). So a COSMOLOGICAL redshift, a wavelength stretched between
   emission and click with no motion of the emitter and no crowd, is not in the law:
   no verb makes it. The growing wall, `expansion-v1`, which puts H into the
   flight's wall, is a declared assumption with no key ([HYPOTHESES
   27](../../HYPOTHESES.md), the row "the expansion as a growing wall";
   STATUS_RULES.md step (1): a hypothesis's number).
3. DERIVATION. What "the universe expands" means as a detector's reading in this
   model, and the only thing it can mean: a Hubble diagram of RECEDING EMITTERS read
   at one detector in its own count. On the ray law the one count of one detector
   carries three factors, 1 + z_d = (1 + k_crowd,A)(1 + v / c) r_B (Light Outside
   II.8; ALGEBRA.md 5.7, SHOWN, rung 1; MET on series G, G2, T, X, DETECTOR, history
   since 2026-09-23); under the new law the same reading is row 4b's, 1 + z =
   gamma_m (1 + beta_c) for a free receding emitter and (1 + beta_c) / (f / f_0) for
   a bound block on its own well (ALGEBRA.md 8.1, 8.4; DECLARATIONS.md section 4,
   the pin 1.9889 at K = 3, COMPUTATION, not run). In both laws the redshift is the
   emitter's motion times the two clocks' crowd stretch and nothing else; a coasting
   throw read against the flight time is Milne's diagram, 1 + z = 1 / (1 - x), x = H
   tau, q = 0 exactly (DARK_ENERGY.md section 2; ALGEBRA.md 5.7).
4. INPUT. The Hubble constant of such a diagram is the throw's declared momenta over
   the world's age: a number of the world file, never of the law (STATUS_RULES.md
   step (3)(a)).
5. DERIVATION (the separating structure). A receding emitter and a stretched lattice
   differ Outside in two readable ways, both of which the law fixes: (i) a body in
   motion reads BLUE to a detector ahead of it and red to one behind, the product
   of the two one-way factors r-free (ALGEBRA.md 5.1; PUBLISHED_FORMS.md section B
   item 3), while a stretched lattice reads red on both sides; (ii) the click's
   content is the birth's (Light Outside L4), so the law's flux of a receding lamp
   falls by one factor 1 / (1 + z) where the expanding form falls by two, and its
   surface brightness by (1 + z)^-1 against the expansion's (1 + z)^-4 (NATURE
   rows 11a and 11c, pinned by derivation). Section 2 (f) builds (i) into one world.
6. NOT DECIDABLE BY THE ALGEBRA. Whether nature's redshift is a throw of emitters
   through a static lattice or an expansion is a question about which world file
   nature is, not about the law. The algebra fixes what each would read (item 5) and
   the data decide: Tolman's exponent (2.28 to 3.06 before evolution, DATA) sits on
   the expansion's side, three powers of 1 + z from the law's throw (row 11c, FAIL by
   derivation; at row 4b's 1 + z = 1.9889 the expansion's surface brightness is 0.127
   of the law's, cosmology_read.out 5).

### 2 (b). Closed or open

1. DERIVATION. The model has no curvature. The lattice is Z^3 with the L1
   neighbourhood; its point group is the 48 and no more (ALGEBRA.md 1.1, 1.4: "the
   crystallographic restriction"); a row's path is the Bresenham line of its
   direction (5.9) and a crowd bends nothing on the law as built (row 13, the flight
   blind; under `optical` the wall stretches the dwell, an index and not a geometry,
   and under the massive record kind the coupling gives an index at declared cells
   and "nothing about a crowd's field", MASSIVE_RECORD.md section 7). There is no
   metric, no connection and no Omega_K in the state space; Einstein's field
   equations are NEITHER beyond the weak static limit (Einstein Outside II.13 and
   IV).
2. DERIVATION. The topology is a declaration. A periodic axis is a circle of the
   translation group, an open axis a segment whose faces are detectors (1.6;
   POSTULATES.md, GameBoard topology: "the torus's unless a world declares a face
   open", record 1421). So a periodic GameBoard is a flat 3-torus, closed in the
   topologist's sense by declaration and of finite volume; an open GameBoard is a
   flat box bounded by detectors. Neither is the cosmologist's closed (positively
   curved, Omega_K < 0) or open (negatively curved, Omega_K > 0) space, and neither
   is infinite. "Closed or open" in the FRW sense is NOT DECIDABLE BY THE ALGEBRA:
   the model carries no object the question is about.
3. DERIVATION (what a periodic board would read). On a torus of extent L along an
   axis a lamp's row reaches a detector by the short way and the long way, so every
   source is read twice on that axis, L apart in flight age (DARK_SECTOR.md section
   3, "the sky repeats"). Nature's sky shows no such repeat: no matched circles
   above 25 degrees, the fundamental domain above 24 Gpc (Cornish et al. 2004, DATA,
   the 24 Gpc RECALLED). So a periodic GameBoard standing for nature must have L
   above that bound: a HYPOTHESIS about a declaration, with nature's number a lower
   bound on the extent and no test the model can run at scale.
4. DERIVATION (carried, the one algebraic statement about a closed board with
   eternal sources). On a static periodic board with a homogeneous crowd of eternal
   sources the presence at every Node grows linearly in the age and the age moment
   as its square (DERIVATIONS_BEAM 14.3 and 15.5 through DARK_ENERGY.md section 3
   (b): Seeliger's accumulation); no steady state exists without the growing wall.
   The law's closed board is not a static eternal universe: a board with a beginning
   whose crowd thickens forever, or a board under `expansion-v1`, a hypothesis;
   Olbers' and Seeliger's paradox in the law's own terms, a derivation and no match.
5. The honest statement, in one line: the model's space is flat and finite by
   declaration; it has no curvature to be closed or open by, and Planck's Omega_K
   (0.001 +- 0.002 with BAO; -0.044 on the spectra alone; DATA) measures a quantity
   the model does not have; what the model could share with a closed universe is a
   finite volume, and nature bounds that volume from below.

### 2 (c). Dark energy

The earlier page's verdict restated by kind, against today's numbers (DARK_ENERGY.md
sections 2 to 5; ALGEBRA.md 5.7, the apparent acceleration):

1. DERIVATION (the shape; the earlier "SHOWN IN FORM"). For a lamp thrown at v and
   read after the flight time tau, 1 + z_d(tau) = g(tau) (1 + z_throw(tau)) with g
   the ratio of the emitter's clock stretch at its birth to the detector's own at
   the click; with g(x) = 1 + g_1 x + g_2 x^2 + ..., x = H tau, a reader fits q_eff
   = 2 [(1 + g_1 + g_2) / (1 + g_1)^2 - 1], and q_eff = -2 g_1 / (1 + g_1) when g_2
   = 0: a stretch of the emitters' clocks growing linearly with the flight time reads
   as an acceleration with nothing accelerating (rung 2); a property of the
   conversion (3.5). The register read the shape once (series G, the nearest of
   three fixed forms in all six pushing windows, the fitted q_eff positive in five of
   six; GAMEBOARD by its denominator; history).
2. INPUT, and NOT DECIDABLE BY THE ALGEBRA (the size). Nature's q_0 needs g_1 = -q_0
   / (2 + q_0): 0.358 for Planck's -0.527, 0.332 for Pantheon+'s -0.499, 0.217 for
   DESI's w_0 = -0.827 at Omega_m 0.31 (cosmology_read.out 1, COMPUTATION on DATA).
   The clocks' stretch k_crowd = a_tau n / d is the crowd's age moment times the
   world's declared suspension pair; the law sets neither, and nature's known wells
   are 10^-6 to 10^-5 in k (DARK_ENERGY.md section 3 (a)), four orders below any of
   the three. The algebra does not give the size and does not forbid it; it says the
   size is a declaration of the crowd.
3. DERIVATION (the sign from the law's own crowd). Under Seeliger's accumulation the
   older light was born in a thinner crowd, k_A(tau) = k_0 (1 - x)^2, so q_eff = 2
   k_0 (3 - k_0) / (1 - k_0)^2 > 0 (cosmology_read.out 7: 0.061 at k_0 = 1/100,
   0.716 at 1/10): a deceleration. Under the growing wall the presence is steady and
   q = 0 (Milne). The law's own history of a crowd never gives nature's sign.
4. DERIVATION, FAIL (the brightness; the earlier "FAIL"). By nature's own method,
   the flux of a standard lamp, the law's click carries the birth's content, so d_L
   = D sqrt(1 + z_d) and q_eff (by brightness) = 2 / (1 + g_1): +2 for the pure
   throw, +1 under the growing wall (NATURE row 11a, pinned, FAIL against -0.53),
   never negative for any g_1. The paper's supernova diagram row and this line are
   one object (NATURE.md row 11a; STATUS_RULES.md row 11a: not predicted by the law
   as built, the hypothesis's number +1 printed as such; row 3, the coasting -0.108
   and the crowd's +0.35 to +0.92, disagrees). Nothing in today's numbers softens
   it: DESI moves q_0 from -0.53 toward -0.36 (COMPUTATION at Omega_m 0.31) and the
   law's brightness reading stays at +1 or above.
5. Does the massive record kind of chapter 8 change it? Two statements, apart.
   - COMPUTATION (the field): under chapter 8 light is the rule's record at [1, 1]
     and a block emits through the coupling's source term, the first difference of
     its own record (8.5). In that scheme's continuum the field of a monopole source
     moving at beta is the retarded scalar wave: behind a receding source the
     frequency is D f_0 with D = 1 / (1 + beta), and the amplitude of the level's
     first difference is D times the rest amplitude on a chain (the retarded time
     compressed by D) and D^2 in three dimensions (the Lienard-Wiechert denominator
     1 - **n** . **beta** times the compression); so the field's energy flux behind
     a receding emitter carries (1 + z)^-2 on a chain and (1 + z)^-4 in three
     dimensions, Tolman's exponent in the field, where the ray law's click carried
     one factor. This page's arithmetic on the continuum, not proved on the
     GameBoard, and a GAMEBOARD quantity (the form I of 8.2 at a probe), never a
     measurement.
   - NOT DECIDABLE BY THE ALGEBRA (the click): the click of chapter 8 is the rung 1
     / W of the receiver's own norm crossed by its pointer (8.6), scale-free in the
     received amplitude and one click per cycle of the driven record; it reads the
     frequency (row 4b's pin) and defines no brightness. SCHEDULE.md's rows 3 and
     11a to 11c are NOT PREDICTED under the new law for this reason ("no click
     definition of a brightness"). So chapter 8 changes the brightness in the FIELD
     and leaves it unread by any click: the FAIL of row 11a is neither confirmed nor
     reversed under the new law, and it stands as the ray law's derivation until a
     click reads a flux. FOR THE OWNER, below.
6. HYPOTHESIS (named, not proposed). DESI's w_0 w_a hint is, in item 1's shape, a
   nonzero g_2, a clock stretch not linear in the flight time. It is a DECLARED crowd
   profile (an initial state, kind 2 of Highlights item 5), not a rule, so the three
   tests do not apply to it; its identity, if ever ordered, `clock-gradient-hypothesis`
   (the crowd's age moment declared to grow outward from the detector). Its brightness
   still reads q_eff = 2 / (1 + g_1) > 0 by item 4: it can match the diagram's shape
   and never the supernova brightness. The paper should not carry it.
7. The receding emitter's field on the lattice itself, no continuum (the Boss's
   item 1 of 03:26Z). Three statements, each with its kind.
   - DERIVATION (exact on the lattice): the frequency behind. On a chain the rule at
     [1, 1] reads 3 (a_next + a_before) = a_E + a_W + 4 a_now before the remainder,
     whose characters obey cos omega = (cos k + 2) / 3 (8.1's band with two folded
     axes). A block stepping one Link per K intervals sources light at its own
     clock's angle omega_s per interval (omega_0 f / f_0, the one formula's) along
     its path, so the character behind it is the one whose phase advances omega_s
     per interval on that path: omega + k / K = omega_s with omega on the band.
     That is one equation in the integers of the world and the band, no continuum;
     the receiver's 1 + z is omega_0 over its root omega. At K = 3 on row 4b's
     world it gives 1.98904 against the continuum form's 1.98884, the band's
     dispersion 1.0 x 10^-4, inside the 0.3 percent band (cosmology_read.out 8,
     COMPUTATION of the root; the equation the DERIVATION).
   - COMPUTATION, no closed form (the amplitude behind). The field's level behind a
     hopping source is the sum of the chain's discrete retarded responses over the
     source's path, which the exact recurrence computes interval by interval (the
     Inside a bijection, 8.8) and no elementary closed form gives, the band being
     dispersive away from its bottom; its energy balance is exact, the source's
     work per interval entering J's identity (8.5). At the band's bottom (rung 2,
     lambda much longer than a Link) the sum is the continuum's, D on the first
     difference on a chain and D^2 in three dimensions, item 5. Nothing of the law
     is missing here: the amplitude is a number the recurrence gives, not a rule.
   - What a reading needs, and its identity. To pin the field's (1 + z)^-4 a click
     must read a FLUX: a detector whose click carries the received norm's size and
     not only its first rung (8.6's rung is scale-free). That is a declaration of
     the detector (kind 3), not a rule; if the owner admits it beside the law it is
     `flux-rung-hypothesis`, and until then the field's exponent stays GAMEBOARD.

### 2 (d). Dark matter

1. DERIVATION (the ray law, the law as built in the register's history). Every
   gravitational push is the bilinear form **r** = **C** **a**, the coupling matrix
   over the columns times the flow of the ARRIVING rows (ALGEBRA.md 1.2, the force
   row; 2.2); the rows of the gravity column are released by a body at its release
   rate eta per unit of content per direction (5.6 (e), G = K eta / (4 pi S_w)); a
   Node with no body releases nothing (the third test: nothing kept at a Node). So
   there is no source of a gravitational effect without a body of content. Whether
   that body CLICKS is a separate declaration: a family with the charge column 0 and
   no lamp pushes and is pushed by its content and releases no paid row a light
   detector reads (DARK_SECTOR.md section 6). Such a family is dark matter as an
   INPUT, the content per galaxy an initial state, exactly as nature's model
   declares it; nothing of the six derives it and nothing forbids it.
2. DERIVATION (the massive record kind, the law of the GO). Under chapter 8 the mass
   IS the pair [num, den] (8.1); the massive kind's rows do not push, a
   massive-to-massive force is not in the law, and the only force between blocks is
   light's stress at their outer Ports, 2 A^2 cos(k_0 L) with no 1 / r form (8.11;
   8.9, "the rows this kind does not reach: the crowd's field, rows 3, 11, 12, 13,
   14"). So under the new law there is no gravity at all yet, with or without a
   clicking body; "gravity as an index of the crowd's massive records" is
   `gravity-index-hypothesis`, named with no number (MASSIVE_RECORD.md section 7).
   The question "a gravitational effect without a clicking body" has no object under
   chapter 8 until a crowd's field is derived.
3. The four candidates the order names, one line each. The held mass (POSTULATES.md
   26.1) is the content of a body that clicks; it adds no unseen source. The block's
   self pair [p, q] is WITHDRAWN and maps onto [num, den], the block's rest frequency
   and no source of a push (8.1; MASSIVE_RECORD.md section 1). `newton-presence-v1`
   is an unordered alternative for WHICH count a body's push takes, the rows present
   in place of the rows met ([DIAGNOSIS.md](../newton_diagnosis/DIAGNOSIS.md) section
   6); it adds no source. `flow-link-v1`'s one constant makes the push's and the
   clock's constants one, q / (4 pi S_w) at n S_w = d ([the flow
   weight](../flow_weight/DESIGN.md) section 0), off by default; it rescales the push
   and adds no source. None is a gravitational effect without content.
4. DERIVATION (what a rotation curve reads as a detector's click). A lamp on an
   orbiting body hands the body's own count to every rest detector its rows reach;
   the click is the triple (the Node, the detector's count, what arrived) (5.6 (a)).
   The speed is the click train's Doppler, 1 + z = 1 + v / c on the ray law (5.7),
   gamma_m (1 + beta_c) under chapter 8; the radius the arrival Node and the row's
   age converted back (CONVERSION). A rotation curve is a list of (radius, z) pairs
   from the lamps' clicks at many radii, the flat curve a z constant in the radius.
   The detector adds nothing at a galaxy's speeds: the law's Doppler departs from
   the classical one by parts in 10^7 where the curves are read to parts in 100
   (DARK_SECTOR.md section 1). The curve then tests the field, Newton's in the shell
   mean on the ray law, a = -G M / r^2 with the ripple (5.6 (e), rung 2): the
   visible content gives the Keplerian fall, as in nature's model.
5. DERIVATION (the in-law routes to a flat curve, all refuted, carried). A short
   periodic dimension gives 1 / r beyond its thickness: the Tully-Fisher slope 2
   against nature's 3.9 +- 0.2, a departure at one radius against nature's one
   acceleration a_0, and a sky repeating at 1 to 10 kpc (DARK_SECTOR.md section 3);
   an acceleration floor from the push's rounding is zero, the remainder kept, and the
   width S cannot be derived ([S_AND_A0.md](../far_lamp/S_AND_A0.md)). The Bullet
   cluster (DATA, 8 sigma) is a lensing reading: on the law as built light is not
   bent (row 13, 0.000 pixel, DETECTOR, history); under `optical` the bending follows
   the content met, so a bending mass where the plasma is not is again a dark
   family's content, an INPUT (DARK_SECTOR.md section 4). The CMB's third peak, the
   hot gas and BBN have no object in the law (no plasma, no acoustic physics, no
   nucleus beyond binding-v1's give): NOT DECIDABLE BY THE ALGEBRA.
6. The answer to the owner's question in one line: no, the law contains no source of
   gravity without a body of content; it admits unseen content as an input family,
   and under the law of the GO it has no gravity yet at all.

### 2 (e). The Hubble tension

1. NOT DECIDABLE BY THE ALGEBRA. Nature's 67.4 is an inference through the acoustic
   scale of a plasma at z = 1100 and the expansion history since, and 73.0 a ladder
   of distances; the law has no plasma, no acoustic scale, no a(t) and no luminosity
   distance (2 (a) 1, 2 (c) 4). The algebra says nothing of the tension.
2. DERIVATION (the one thing it does say, a bound). A detector's own rate multiplies
   every Hubble rate it reads: a coasting throw reads H_d = r_B H, r_B = 1 / (1 +
   k_crowd,B) (Light Outside II.8, "the Hubble form"). So two detectors in two
   crowds read two Hubble constants in the ratio (1 + k_B') / (1 + k_B), and a local
   reader in a thinner crowd than the mean emitter's reads a larger H. For 73.04 /
   67.36 = 1.084 the crowds' stretch would differ by k = 0.084 (cosmology_read.out
   2, COMPUTATION), four orders above nature's known wells (10^-6 to 10^-5): the
   law's clock mechanism cannot make the tension at nature's crowds, and this page
   proposes nothing.

### 2 (f). The one detector experiment that separates the model from the standard cosmology on one question

The question: 2 (a), a receding emitter against a stretched lattice. The form: the
two-reader world of PUBLISHED_FORMS.md section B item 3, Ives and Stilwell's and
Botermann's arrangement, which the tree already names and no schedule row yet runs.

- THE WORLD, under the existing keys, DECLARATIONS.md section 4's chain: the light
  family [1, 1] and the massive kind [156, 157]; ONE emitter block A (side 12, the
  well [314, 315], `emits`, G = [1, 50], g = [1, 1000], W = 64) at x = 1000 on a
  chain of 2200, pushed to K = 3 toward -x over the declared `ramp` and held; TWO
  light detectors at rest, BEHIND at x = 1900 (section 4's) and AHEAD at x = 100,
  under `clock_stamp`; the control with A at rest. No new key; one detector more.
- THE READING, DETECTOR: at each detector the mean count between clicks over the
  hold, in the receding world over the control, is 1 + z_behind and 1 + z_ahead; the
  product is a CONVERSION of two ratios of one clock's counts.
- THE PIN IN FORM (COMPUTATION, proposed, FOR THE OWNER to declare, moved by no
  one): z_ahead < 0 (blue) and z_behind > 0 (red); the product (1 + z_behind)(1 +
  z_ahead) = (1 - beta_c^2) / (f / f_0)^2 on the declared well, 1.0599 at f / f_0 =
  0.7931 and K = 3 (cosmology_read.out 4); the free emitter's limit gamma_m^2 (1 -
  beta_c^2) = 1.0022 at the kind's own cone (1 exactly at light's gamma;
  PUBLISHED_FORMS.md's (P) reading of the two-pace world, its 0.9962 the inverse
  ratio of the two gammas at mu = 0.15's gamma_m 1.22705); the band the peak's grain
  over the hold, 0.3 percent, as row 4b's.
- WHAT SEPARATES: a stretched lattice (the standard cosmology's redshift, no motion
  of the emitter, no preferred side) reads red at BOTH detectors and a product (1 +
  z)^2 > 1 by twice the redshift; the law reads blue ahead and a product within a
  fraction of a percent of 1, a body in motion. The row decides between the two
  mechanisms by two clicks of one world; it does not compare with a cosmological
  observation, because nobody sits ahead of a receding galaxy, and it says so. Its
  falsifier on the model's side: a product off the pin beyond the band (the one
  formula wrong) or z_ahead > 0 (no motion read).
- THE THREE TESTS: the world adds no rule; the rules it runs (8.1, 8.5, 8.6, 8.11)
  passed all three in ALGEBRA.md 8.10. Generic, vector, local: nothing to add, a
  verdict of PASS by inheritance and no new verb.
- HOST: a chain of 2200, seconds to a minute (section 4's estimate). Not run by this
  page.

A second reading of the same world, named and NOT COMPUTED: the clicks behind over
ahead, the beaming of a receding emitter. The field's energy share behind over ahead
on a chain is ((1 - beta) / (1 + beta))^2 = 7 - 4 sqrt 3 = 0.0718 at K = 3
(COMPUTATION on the continuum, cosmology_read.out 4), where a photon count on a line
is one power, 2 - sqrt 3 = 0.268; what two receivers' clicks read of one record is
DESIGN.md section 5's rule, not derived here. FOR THE OWNER.

### 2 (g). A Hubble diagram of receding lamps read at one detector in its own count, in form (a proposal; the Boss's item 2 of 03:26Z; nothing declared in DECLARATIONS.md)

1. The objects. Four chain worlds of DECLARATIONS.md section 4's form, 2200 x 1 x
   1, x open for light (sponge faces), the massive kind's faces open on x; Z_N;
   `light` [1, 1] and the massive kind [156, 157]; in each world ONE emitter block
   A (side 12, the well [314, 315], `emits`, G = [1, 50], g = [1, 1000], the mode
   seed) starting at x = 113, pushed toward +x to K = 3, 4, 5 or 6 over the ramp
   and held at that momentum; ONE light detector of the ray law at x = 100, W = 64,
   `clock_stamp`, at rest in no crowd (r_B = 1); a fifth world the control, A at
   rest at x = 113. Why not one world with four lamps: the receiver's record is
   driven by the total field, so one detector reads the SUM of four lines and no
   click of it is one lamp's; a detector set reading one side only would need a
   key the engine lacks (a directional blind on a set), named and not proposed.
2. The declared integers: the pairs above; s = 12; G, g, W; the momenta [Q S M / K,
   0, 0] for K = 3, 4, 5, 6 (beta_c = sqrt 3 / K: 0.577, 0.433, 0.346, 0.289); the
   ramp 1500; the hold 8000; t_0 = 9500 the reading's count; nothing chosen from
   nature's numbers (DERIVED_BLIND: the pairs and the well are row 4b's, declared
   before this row; nature's q_0 nowhere in the inputs).
3. The verbs: 8.1 (the rule), 8.5 (the coupling and the emission), 8.11 (the step
   by the declared momentum), 8.6 (the click at W stamped with the detector's own
   count and the record's birth stamp). No new verb; the three tests inherited.
4. The readings, DETECTOR: per world the mean count between clicks over the hold
   against the control's, 1 + z_K; the flight age tau_K of the clicks, the click's
   count less the record's birth stamp; the diagram the four pairs (tau_K / t_0,
   z_K). GAMEBOARD beside: A's Node per interval, the probes' amplitude.
5. The pin in form, before any run (COMPUTATION from the DERIVATION; proposed, FOR
   THE OWNER to declare): (a) each 1 + z_K = (1 + beta_c) / (f / f_0)(K) by the
   one formula on this well at that K, the band 0.3 percent (the free emitter's
   limit (1 + beta_c) gamma_m: 1.934, 1.591, 1.436, 1.346 at K = 3, 4, 5, 6,
   cosmology_read.out 9); (b) each x_K = tau_K / t_0 = beta_c / (1 + beta_c) to the
   start's 13 Links over v t_0 (0.366, 0.302, 0.257, 0.224); (c) the curve through
   them, 1 + z = (1 + beta) gamma_m(beta) with beta = x / (1 - x), whose second
   order reads q_eff = c^2 / c_eff^2 = 1 + omega_0^2 / 3 + O(omega_0^4) = 1.0043 at
   omega_0 = 0.1129 (DERIVATION of the form, COMPUTATION of the number; the bound
   block's f / f_0 per K a per-point correction computed before its run); (d) the
   falsifier: any lamp's 1 + z off its pin beyond the band, or the four points'
   fitted second-order coefficient reading q_eff below 0, which no coasting throw
   of the law can give.
6. What separates. In the same variables (z against the light's flight age) the
   standard cosmology at Planck's q_0 = -0.53 has the second-order coefficient 1 +
   q_0 / 2 = 0.735, the far points BELOW the near slope's line, with no motion of
   any emitter; the law's throw has 3 / 2 (+ omega_0^2 / 6), the far points ABOVE
   it, every emitter a body in motion, and the offset from Milne's 1 (q = 0) the
   two-pace world's mark. The flight age is not one of nature's observables, so the
   row compares the diagram's FORM and says so; a run confirms the engine against
   the algebra (a (K) row in the number, the +omega_0^2 / 3 a (P) beside it).
7. The identity: `detector-law-v1` with `massive-record-v1`; every key section 4's
   (`emits` consuming nothing held, M1-2); HOST five chains, seconds to a minute
   each. Not run by this page.
8. The preliminary run's form (the owner's word of 03:29Z through the Boss: "without
   a preliminary experiment we run nothing"; a pin run only after an exploratory,
   unpinned run is approved; nothing here runs, not even that). What the
   exploratory run of the K = 3 world and its control would have to show, read
   against no pin: (a) clicks ARRIVE at the declared detector at x = 100 within the
   declared count: the first record born at the first cycle of A's clock after the
   seed's standing start, 13 Links of flight at c (23 intervals) plus the receiver's
   ring-up, so a first click within the first 500 intervals of the run in both
   worlds, and clicks throughout the hold; (b) the count over the hold of 8000 of
   the order the rest clock gives, 8000 x 0.10175 / (2 pi) = 130 clicks in the
   control (COMPUTATION on section 4's mode 0.10175) and fewer, not more, in the
   receding world, with no number of either read against a pin; (c) the mean
   interval between clicks steady over the hold, no beat (8.7's criterion; a beat
   sends the world back for a longer ramp, never to a pin); (d) A stepping one Link
   per 3 intervals by its `block` lines and its own clicks per cycle present
   (GAMEBOARD and DETECTOR beside), the books' J identity holding, no stop on the
   bound abs(**v**) < c; (e) every number of the run labelled EXPLORATORY, GAMEBOARD
   or DETECTOR, and none carried into item 5. Only on that showing, and on the
   owner's word, would the pin of item 5 be declared and the four worlds run.

### FOR THE OWNER (questions this page does not decide)

1. Whether a click that reads a FLUX is to be declared under the new law (a receiver
   whose rung is not scale-free, or a count of completed records per detector Node),
   so that rows 11a and 11c can be pinned under chapter 8; without it the brightness
   stays the ray law's derivation, FAIL, and the field's (1 + z)^-4 of 2 (c) 5 stays
   a GAMEBOARD number.
2. Whether the two-reader world of 2 (f) enters the schedule as a (K) row in the
   number with a (P) beside it (the two-pace world's product), and who declares its
   pin.
3. Whether the paper's statement on the dark sector should read, in one line, what 3
   below says: no dark energy and no dark matter are derived, none is forbidden, the
   acceleration's shape is the conversion's, and the brightness fails by derivation.

## 3. The honest summary

1. The law has no scale factor and no cosmological redshift: no verb acts on the
   lattice, and a row's phase is never stretched in flight (DERIVATION).
2. "The universe expands" can only mean, in this model, a Hubble diagram of receding
   emitters read at one detector in its own count, the throw's Doppler times two
   clocks' crowd stretch (DERIVATION); its H is a declared momentum (INPUT).
3. The model has no curvature and no Omega_K; its space is flat and finite by
   declaration, a torus or a box, closed only as a topology (DERIVATION); FRW's
   closed or open is NOT DECIDABLE BY THE ALGEBRA.
4. A static periodic board of eternal sources has no steady crowd, Seeliger's
   accumulation (DERIVATION); nature's absence of matched circles bounds a torus's
   extent from below, above 24 Gpc (DATA, RECALLED).
5. The accelerating shape of the redshift-against-time diagram follows from the
   clocks' stretch growing with the flight time, q_eff = -2 g_1 / (1 + g_1), with
   nothing accelerating (DERIVATION, rung 2); its size, 0.22 to 0.36 for today's
   q_0, is an INPUT four orders above nature's wells.
6. The law's own crowd history gives the wrong sign, q_eff > 0 (DERIVATION); by the
   brightness the ray law reads q_eff = +1 or +2 against -0.53, the paper's
   supernova FAIL (DERIVATION); today's DESI numbers move nature's q_0 toward -0.36
   and change nothing of that.
7. Chapter 8's receding emitter reads, exact on the lattice, the frequency behind it
   by one character equation on the band (DERIVATION, 1.98904 at K = 3 against the
   form's 1.98884); its field carries (1 + z)^-4, Tolman's exponent (COMPUTATION,
   rung 2, GAMEBOARD); its click reads no flux, so the brightness is NOT DECIDABLE
   BY THE ALGEBRA until a flux click is declared.
8. On the ray law every push reads rows a body of content released: no gravity
   without content (DERIVATION); under the new law there is no gravity at all yet,
   `gravity-index-hypothesis` named with no number (DERIVATION).
9. A rotation curve is a list of (radius, z) pairs from orbiting lamps' clicks; the
   detector adds parts in 10^7, the field is Newton's in the shell mean, and every
   in-law route to a flat curve is refuted by the Tully-Fisher slope, the a_0 scale,
   the repeating sky or the kept remainder (DERIVATION, carried).
10. Dark matter is admitted only as an INPUT family with charge 0 and no lamp, as
    nature's model has it; the Bullet cluster, the third peak and BBN have no object
    in the law (NOT DECIDABLE BY THE ALGEBRA).
11. The Hubble tension is NOT DECIDABLE BY THE ALGEBRA; the one line the law has,
    H_d = r_B H, would need a crowd difference k = 0.084 (COMPUTATION), four orders
    above nature's wells.
12. What would be a HYPOTHESIS and not the law: a declared crowd gradient
    (`clock-gradient-hypothesis`) for the shape and DESI's w_a, a dark family's
    content per galaxy, a periodic extent above 24 Gpc, a flux click; none is
    proposed, and none enters the paper on this page's word.

## 4. What this page did not reach

- The (1 + z)^-4 of 2 (c) 5 is the continuum's retarded solution; on the lattice
  the frequency is exact (2 (c) 7) and the amplitude a computation by the recurrence
  with no closed form, not run; the beaming count ratio of 2 (f)'s second reading is
  named and not computed (the click's rule between two receivers of one record not
  derived here).
- The DESI w_0 w_a central values, Planck's A_L, its age, its lensing-only Omega_K
  and Cornish's 24 Gpc were not seen in an excerpt today and stand RECALLED, NOT
  VERIFIED; every other number of section 1 was read in a search excerpt of the
  paper's abstract, never in the paper (the publisher hosts blocked from this
  machine, the Source Verifier's rule).
- The CMB's acoustic peaks, BBN's helium and lithium and the growth of structure
  were not read against the law, which has no object for them (2 (d) 5); the paper's
  own text on the dark sector was not read (paper-48 is the one writer's), and the
  third FOR THE OWNER line is an offer to the Boss, not a proposal into it.

> The scripts of this folder (`cosmology_read.py`, `receding_source_chain.py`) were deleted on 2026-09-26 (the model owner's word, record 2229: code not in use goes); git history keeps them at `6d2a92e2` (`git checkout 6d2a92e2 -- docs/designs/cosmology/<script>`).
