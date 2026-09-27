# The mathematician's verification of the paper: every definition, theorem, identity and number, confirmed or not (docs only; a proposal for the writer on the Boss's word)

Paper: `paper/general_formula/main.tex` on the branch `paper-48` at its head
`6473d8f96b658c5ba1bc91aaa50483a91e966e97` (commit 34, 2026-09-24), read with
`records.tex` (its auxiliary proofs and history) and the checks under
`paper/general_formula/checks/`. Date of the read: 2026-09-24. Session:
`session_01XwhhYBzex76t4Z1X8o1rJt` (the Paper Verifier, mathematician, opened
by the Boss on the model owner's word of 2026-09-24 02:02Z). A physicist
verifies the physical claims in parallel; nothing here is compared with nature.

Method. One line per statement of the paper that is a definition, a theorem, a
lemma, a proposition, an identity, an equation, or a number marked COMPUTATION
or stated as an exact rational or a closed form. CONFIRMED names the line of
`docs/ALGEBRA.md` (the one algebra document, on `main` at `324244f0`), the
check file, or the recomputation that proves it; NOT CONFIRMED gives the reason
in one sentence. Every exact rational and every closed-form number I could
reach was recomputed in pure Python (integers, `fractions.Fraction`, and the
repository's integer tables `core/phase.py`; a float appears only to print a
decimal beside an exact value, never in a claim); the script and its output
are in my session's scratchpad, and the results are quoted here. Numbers that
are a numerical mode of a well or a walk on a board (the closure's `numpy`
scripts, which this container cannot run) are marked "not recomputed" inside
a CONFIRMED-by-source or NOT CONFIRMED line, as the case is. Prose, physics
against nature, and readings after a detector are not verified here.

Notation, once. N_phi is the phase grain (the order of the phase circle);
zeta_N is a primitive N_phi-th root of unity; C and S are the integer cosine
and sine tables at the scale 256; C' and S' the half-angle tables (the tables
of 2 N_phi); u is the birth wheel's reading; b_k the k-th rung of the ladder;
S(N) the CHSH sum at the grain N; omega_0 the pitch (the rest frequency of a
massive kind), c the pace of light (1 / sqrt 3 Link per interval), c_m and
c_eff the two cones of the massive band, gamma the Lorentz factor
1 / sqrt(1 - v^2 / c^2) and gamma_m the same factor at the massive kind's own
cone, beta the pace over c, K the intervals per Link of a stepped block,
T_D the flight wall of the direction D, S_1 the Manhattan length of D and N_l
the label's scale (64 on the register).

## The table

| Section | The statement, in ten words | Verdict | The proof's line, or the reason |
| --- | --- | --- | --- |
| Abstract, 1 | The cube's symmetries are 48 signed permutations, rotations 24 | CONFIRMED | Recomputed: 48 signed permutation matrices preserve the six Ports with opposites; 24 have determinant +1 (ALGEBRA.md 1.1, 4.5) |
| Abstract, 5.5 | S = 181/64 at every power of two 512 to 8192 | CONFIRMED | Recomputed from the tables and Eq. (rung): 181/64 at 512, 1024, 2048, 4096, 8192; `checks/s_powers_of_two.txt` |
| Abstract, 5.5 | 181/64 is 1.05 standard errors from Poh et al. | CONFIRMED | Recomputed: (181/64 - 2.82759) / 0.00051 = 1.049 (the measured value an input) |
| Abstract, 5.1 | c = 1 / sqrt 3 recovered in the limit | CONFIRMED | Proposition (pace), verified below; ALGEBRA.md 4.2 |
| 1 | The only isotropic even reading of momentum is c p . p | CONFIRMED | Recomputed: the symmetric 3 x 3 matrices fixed by all 48 signed permutations are the multiples of the identity (the group average of every symmetric basis matrix is a multiple of I); ALGEBRA.md 1.3 item 6 |
| 1 | The square m^2 + 3 p . p follows from that reading | CONFIRMED | An identity of the declared form W with 3 = 1 / c^2 (ALGEBRA.md 5.3); the value 3 is the flight's constant, declared |
| 1, 5.1 | c^2 = 1/3 from the six reads at leading order | CONFIRMED | Light's band cos omega_l = (cos k_x + cos k_y + cos k_z) / 3 gives omega^2 = k^2 / 3 + O(k^4); ALGEBRA.md 8.1 |
| 1, 3 | The dispersion's coefficient is the cubic pattern of Eq. (dispersion) | CONFIRMED | See Eq. (dispersion) below |
| 1 | Angular density: the axes 2.8 times denser than face diagonals | CONFIRMED | Recomputed: the density of lattice directions bounded in Manhattan length scales as the cube of 1 / (the unit vector's L1 norm); sqrt 2 cubed = 2.83 |
| 1, Eq. (map) | The map s <- s + r; e <- sign(s) min(floor(abs s / d), a); s <- s - e d | CONFIRMED | A definition; ALGEBRA.md chapter 2's central formula, `core.integer.by_drive` |
| 2 (1) to (5) | The five objects: GameBoard, G_48 and G_24, Z_N and its ring, the six maps, the click | CONFIRMED | Definitions; ALGEBRA.md 1.1, 1.5, 2.1 to 2.6 |
| 2 (2) | det is a homomorphism; G_24 = ker det has index 2 | CONFIRMED | Recomputed (24 and 24); the determinant is multiplicative |
| 2 (3), the objects | Z[Z_N] / (x^(N/2) + 1) = Z[zeta_N], free of rank N/2, for N a power of two | CONFIRMED | x^(N/2) + 1 is the N-th cyclotomic polynomial exactly when N is a power of two; ALGEBRA.md 2.3 |
| 2, the objects | For an N with an odd factor the cancel and the evaluation's zero are not one relation | CONFIRMED | The kernel of the evaluation is then the ideal of the cyclotomic polynomial of N, a proper divisor of x^(N/2) + 1 (for example N = 12: x^4 - x^2 + 1 against x^6 + 1) |
| 2, the objects | The table pointer is Z-linear onto a lattice of rank 2, kernel of rank N - 2 | CONFIRMED | The image of Z^N under a 2 x N integer matrix of rank 2 has rank 2, the kernel N - 2; the cancel's ideal has rank N/2 |
| 2, the objects | At N_phi = 8192 only 1952 of the 8192 table pairs are distinct | CONFIRMED | Recomputed from the tables: 1952 distinct (C, S) pairs; `docs/designs/gleason_bound/BOUND.md` section 5 |
| 2, the objects | Two rows of amount 1 at phases 0 and 4097 read (0, 0) | CONFIRMED | Recomputed: (256, 0) + (-256, 0) = (0, 0) at N = 8192 |
| 2, the objects | Their ideal weight is 4 sin^2(pi / 8192) = 5.9 x 10^-7 | CONFIRMED | Recomputed: 1 + zeta^4097 = 1 - zeta, its norm 4 sin^2(pi / 8192) = 5.883 x 10^-7 |
| 2, the objects | At N_phi = 64 no table zero with at most three rows of amounts up to 4 | CONFIRMED | Recomputed on Z[zeta_64] (phases distinct modulo the cancel, signed amounts 1 to 4, up to three rows): none; the only zeros on Z[Z_64] with positive amounts are the 128 cancel pairs (p, p + 32), which the normal form removes; BOUND.md section 5 |
| 2, Def. 1 | The amplitude z = (w / sqrt m)(C + i S) / 256 and its square | CONFIRMED | A definition; the square follows |
| 2, Def. 1 | The quotient by (w, m) -> (k w, k^2 m) would not be free | CONFIRMED | It would make b_1 = 2 b_4 = 4 b_16 = ..., an infinitely 2-divisible nonzero element, which no free Z-module has |
| 2, Def. 1 | The bounds 2^62 - 1 (the law's) and 2^63 - 1 (the host's) | CONFIRMED | `events/world.py` lines 351 to 352 (`AMOUNT_BOUND`, `MOMENTUM_BOUND` = (1 << 62) - 1); `core/integer.py` line 6 (`MAX_WORK_INT` = (1 << 63) - 1) |
| 2, Def. 1 | Four rotations of the row form would pass the bound | CONFIRMED | Recomputed: 65536^3 = 2^48 is within 2^62 - 1 and 65536^4 = 2^64 is not |
| 2, Def. 1 | The norm sum of w^2 / m is preserved by the merge and the cancel | CONFIRMED | Two rows equal but for w add their amounts on one basis element; the cancel is the relation of the module (Def. 1) |
| 2, Def. 2 F | The phase turn phi(tau) = floor((tau + 1) n / d) - floor(tau n / d) | CONFIRMED | A definition; ALGEBRA.md 2.1 |
| 2, Def. 2 S | The split (w, m, p) -> (w a_i, m A, p + t_i), A = sum a_i^2 | CONFIRMED | A definition; Theorem 2 below |
| 2, Def. 2 R | U_(s,t) and its row form, exact for t a multiple of N/4 | CONFIRMED | With t a multiple of N/4 the turn v(t) is a phase shift by t steps on the tables exactly (the quarter turn exact on the tables, recomputed for every power of two 4 to 65536) |
| 2, Def. 2 B | u = (b - 1) mod N_phi; uniform over N_phi consecutive births | CONFIRMED | A definition; uniformity is one birth per residue |
| 2 (T) | m_D(tau) = floor((2 tau S_1 N_l + T_D) / (2 T_D)) and tau_k = ceil((2k - 1) T_D / (2 S_1 N_l)) | CONFIRMED | Recomputed: tau_k is the first interval with m_D >= k on five directions for k up to 200; ALGEBRA.md 4.1; `checks/information_transfer.py` `flight_links` |
| 2 (B) | The click's weight is f^T G f with G = E^T E | CONFIRMED | (E f)^T (E f) = f^T (E^T E) f, integer associativity; ALGEBRA.md 2.2, 4.8 |
| 2 (E) | ev is a surjective ring homomorphism with kernel (x^(N/2) + 1) | NOT CONFIRMED | True only for N_phi a power of two (the objects paragraph says so; this sentence and Section 6.1's restatement omit the condition); for N with an odd factor the kernel is the N-th cyclotomic polynomial's ideal |
| 2 (E) | ev is a star-homomorphism carrying f* f to the norm of ev(f) | CONFIRMED | ev(f*) = conj(ev(f)) since zeta^(-p) = conj(zeta^p) |
| 2 (E) | E(x)^2 = (64400, 12750) against 256 E(x^2) = (64256, 12800) at N = 64 | CONFIRMED | Recomputed from the tables: (C[1], S[1]) = (255, 25), (C[2], S[2]) = (251, 50) |
| 2 (D) | The count e = floor(abs s / d) with the sign, remainder in (-d, d) | CONFIRMED | A definition; ALGEBRA.md 2.6 |
| 2, Def. 3, Eq. (rung) | b_k = floor((2 N C_k + C_K) / (2 C_K)), b_0 = 0, b_K = N | CONFIRMED | b_k = floor(N C_k / C_K + 1/2); at C_0 = 0 the floor of 1/2 is 0, at C_K the floor of N + 1/2 is N |
| 2, Def. 3, Eq. (joint) | R(o_A, o_B) = J^2, J = sum over labels of U_a U_b | CONFIRMED | A definition |
| 2, Lemma 1 | Every u lies in exactly one cell | CONFIRMED | The rungs are non-decreasing (C_k non-decreasing) from 0 to N |
| 2 | The count in channel k is b_k - b_(k-1), Born to 1 / N_phi per cell | CONFIRMED | abs(b_k - N C_k / C_K) <= 1/2 per rung, so the count over N births is within 1 of N R_k / C_K |
| 2 | The choosers' periods 3 and 5 against N = 64: the common period | CONFIRMED | Recomputed: lcm(3, 5, 64) = 960, the register's 960 births |
| 2 | The two-slit offer R = 512[(C_1 + C_2)^2 + (S_1 + S_2)^2] = 1024(65536 + C_1 C_2 + S_1 S_2) | CONFIRMED | With w = 1, m = 2: X = 32 (C_1 + C_2); X^2 + Y^2 = 1024 [..]; over m = 2 gives 512 [..]; expanding with C^2 + S^2 = 65536 (ideal) gives the second form |
| 2, Theorem 1 | The maps keeping opposites opposite are the 48; the kernel of det is S_4 on the diagonals | CONFIRMED | Recomputed: the 24 rotations induce 24 distinct permutations of the four body diagonals (faithful, hence S_4); `records.tex` app:proofs; ALGEBRA.md 4.5 |
| 3, Eq. (massive) | 3 den a_next + r' = num S_6 - 3 den a_before + r, 0 <= r' < 3 den | CONFIRMED | A definition; ALGEBRA.md 8.1 |
| 3 | The three verbs of the rule: (B), (T), (D) | CONFIRMED | ALGEBRA.md 8.1, the verbs paragraph |
| 3, Eq. (band) | cos omega = cos omega_0 cos omega_l(k), cos omega_0 = num / den | CONFIRMED | Recomputed by hand: on the character a = cos(omega t - k . x), a_next + a_before = 2 cos omega a_now and S_6 = 2 (sum cos k_i) a_now; ALGEBRA.md 8.1 "The band, PROVED HERE" |
| 3 | 2 - 2 cos omega = 4 sin^2(omega / 2) turns the band into light's form scaled by num / den | CONFIRMED | 4 sin^2(omega/2) = 2(1 - num/den) + (num/den)(4/3) sum sin^2(k_i / 2); ALGEBRA.md 8.1 |
| 3 | omega_l^2 = k^2 / 3 + O(k^4) | CONFIRMED | cos omega_l = 1 - k^2 / 6 + O(k^4) |
| 3 | c_m^2 = cos omega_0 c^2; the deficit omega_0^2 / 4 | CONFIRMED | sqrt(cos omega_0) = 1 - omega_0^2 / 4 + O(omega_0^4); ALGEBRA.md 8.1 (i) |
| 3 | 0.39 percent at N_0 = 50 (COMPUTATION) | CONFIRMED | Recomputed: (2 pi / 50)^2 / 4 = 0.00395 |
| 3, Eq. (cone) | omega^2 = omega_0^2 + c_eff^2 k^2, c_eff^2 = cos omega_0 (omega_0 / sin omega_0) c^2 | CONFIRMED | Recomputed by hand from omega = omega_0 + delta at the band's bottom; ALGEBRA.md 8.1 (ii) |
| 3, Eq. (cone) | c_eff^2 / c_m^2 = omega_0 / sin omega_0 = 1 + omega_0^2 / 6 + O(omega_0^4) | CONFIRMED | The Taylor series of x / sin x |
| 3 | 1.0037 at the pitch mu = 0.15 (COMPUTATION) | CONFIRMED | Recomputed at the pair [800, 809] (omega_0 = 0.14930): omega_0 / sin omega_0 = 1.00372 |
| 3 | The two gammas are apart by about beta^2 gamma^2 omega_0^2 / 4 to second order | NOT CONFIRMED | At the named cone c_eff the separation is beta^2 gamma^2 omega_0^2 / 6, since c_eff^2 / c^2 = 1 - omega_0^2 / 3 + O(omega_0^4); the coefficient 1/4 belongs to c_m (c_m^2 / c^2 = 1 - omega_0^2 / 2); ALGEBRA.md 8.1's own numbers at K = 3, [800, 809] agree: gamma(c_eff) / gamma(c) - 1 = 0.00188 against 0.00186 for 1/6 and 0.00279 for 1/4 |
| 3, Eq. (dispersion) | v_g / c = 1 - (3 sum n_i^4 - 1) k^2 / 24 + O(k^4) | CONFIRMED | Recomputed by hand: cos omega = 1 - k^2 / 6 + (sum n_i^4) k^4 / 72 gives omega = (k / sqrt 3)(1 - (3 sum n_i^4 - 1) k^2 / 72), and d omega / d k the stated line; `docs/designs/detector_law/LIGHT_DISPERSION_BOUND.md` lines 23 to 24 |
| 3 | The coefficient 0, 1/2, 2, and 4/5 averaged over the sphere | CONFIRMED | Recomputed as exact fractions: body diagonal 0, face diagonal 1/2, axis 2; the sphere mean of sum n_i^4 is 3/5, so 3 (3/5) - 1 = 4/5 |
| 3, Eq. (motion) | f / f_0 = omega_b(gamma_m s, g_w) / (gamma_m omega_b(s, g_w)) | CONFIRMED as carried | The formula is carried from the design and computed, not proved, on the GameBoard (ALGEBRA.md 8.4 says so in the same words); the paper marks it so |
| 3 | The well limit gives 1 / gamma_m, the cavity limit 1 / gamma_m^2 | CONFIRMED | omega_b independent of s, respectively proportional to 1 / s; ALGEBRA.md 8.4 |
| 3 | The first-order deviation is epsilon (gamma_m^2 - 1) / 2 below 1 / gamma_m | CONFIRMED | Expanding (1 / gamma_m) sqrt((1 - gamma_m^2 eps) / (1 - eps)) to first order in eps; ALGEBRA.md 8.4 |
| 3 | Row 4a: 0.8116 at the exact cone, 0.8108 at c_m, 0.8132 at c | CONFIRMED by source, not recomputed | A numerical lowest mode on a 200^2 layer (`ALGEBRAIC_CLOSURE.md` row 4a, `massive_layer_pins.py`); the order of the three controls agrees with gamma(c_m) > gamma(c_eff) > gamma(c), recomputed: 1.22820, 1.22705, 1.22474 |
| 3 | The coupling's amplitude form is tachyonic: a negative eigenvalue at k = 0 | CONFIRMED | The matrix [[0, -g], [-g, omega_0^2]] has determinant -g^2 < 0; ALGEBRA.md 8.5 |
| 3 | The scheme is the Euler-Lagrange scheme of a two-point Lagrangian, symplectic, with an exact invariant J | CONFIRMED | ALGEBRA.md 8.5, the invariant's per-cell algebra checked by hand: g D_in [V (X + Y) - X (U + V) + X U - Y V] = 0; the conserved form I it rests on is proved in 8.2 by the symmetry of D M (read and checked) |
| 3 | The index n^2 = 1 + G g / (omega_0^2 - omega^2) in closed form | CONFIRMED as algebra | From the coupled continuum dispersion (c^2 k^2 - omega^2)(omega_0^2 - omega^2) = G g omega^2, n^2 = c^2 k^2 / omega^2; the dispersion itself is computed and not proved (ALGEBRA.md 8.5, "The index") |
| 3 | The step (a_before, r) -> (a_next, r') is a bijection with the ceiling as its inverse | CONFIRMED | The uniqueness of the Euclidean division; a_before = ceil(m / d), r = d a_before - m; ALGEBRA.md 8.8 |
| 3 | The evaluation with the weight and the rung is many-to-one | CONFIRMED | ev has a kernel, the square is not injective, the rung is a threshold; ALGEBRA.md 8.8 |
| 4, Theorem (Locality Outside) | Under (A1) every Outside passage is a chain of neighbouring clicks | CONFIRMED | A consequence of the definitions (A1), P6, P11 as stated; ALGEBRA.md 3.4 |
| 4, Theorem (Discreteness Outside) | Counts form a free abelian monoid; ratios lie in Q; the velocity 1 / k; resolution 1 / n | CONFIRMED | Counts are whole numbers under addition; a ratio of whole numbers is rational; ALGEBRA.md 3.4 |
| 4 | The support bound abs(supp f) abs(supp f-hat) >= N_phi | CONFIRMED | Donoho and Stark 1989, Theorem 1 on the cyclic group |
| 4 | Its equality cases at N = 64, by enumeration: three listed | NOT CONFIRMED | The list is incomplete: on Z_64 equality holds exactly for the translated and modulated indicators of the subgroups (Donoho and Stark's equality theorem), the seven subgroups of orders 1, 2, 4, 8, 16, 32, 64; the combs of every second, fourth and sixteenth phase (supports 32, 16, 4 with transforms of size 2, 4, 16) are missing from a sentence that says "by enumeration" |
| 4 | Weyl's relation V U = omega U V on Z_N | CONFIRMED | The clock and shift operators on Z_N (Weyl 1931, Schwinger 1960) |
| 4 | The entropy identity: bits read plus bits not read of u equal log2 N_phi | CONFIRMED | The chain rule H(K) + H(U given K) = H(U) with U uniform on N_phi values; ALGEBRA.md 4.11 |
| 4 | psi = (00) + (11) has coefficient matrix of rank 2, no product form | CONFIRMED | The 2 x 2 identity matrix has rank 2; a product u tensor v has rank 1 |
| 4 | U_s^T U_s = n_s I | CONFIRMED | Theorem 2 below; the off-diagonal C' S' - S' C' = 0 in integers |
| 4 | E(a, b) = cos(2 pi (a - b) / N) within the rounding; S = 2 sqrt 2 before rounding | CONFIRMED | The exact rotation algebra: 2 cos^2(theta_a - theta_b) - 1 with theta_s = pi s / N; ALGEBRA.md 4.10 |
| 4 | 176/64 = 2.75 at N_phi = 64 | CONFIRMED | Recomputed: S(64) = 11/4 with E = (11/16, -11/16, 11/16, 11/16) |
| 4 | cos omega = cos m cos kappa gives omega^2 = m^2 + kappa^2 - m^2 kappa^2 / 3 + O(6) | CONFIRMED | Recomputed by hand (the fourth-order term of the product of two cosines against the series of cos omega) and numerically (the residual at m = 0.01, kappa = 0.02 is 4 x 10^-13, sixth order); ALGEBRA.md 5.1 (ii) |
| 4 | r = m / omega = sqrt(1 - v^2)(1 - kappa^2 / 6 + O(4)) with kappa^2 = m^2 v^2 / (1 - v^2) | CONFIRMED with a reading | Holds with v the walk's group velocity d omega / d kappa, as the click frame names it (ALGEBRA.md 5.1 states the sign depends on which velocity is named); with v defined by kappa^2 = m^2 v^2 / (1 - v^2) exactly the correction has the opposite sign |
| 4 | W c^4 is E^2 = E_0^2 + p^2 c^2 | CONFIRMED | W = E_0'^2 + 3 p . p with E' = E / c^2 and 3 c^2 = 1 |
| 4 | 3 = 1 / c^2 = d exactly on the body diagonal; 2.954, 2.971, 3.000 by direction | CONFIRMED | Recomputed at N_l = 64: T_D = 110, 156, 192; T_D^2 / (N_l^2 abs(D)^2) = 3025/1024, 1521/512, 3 |
| 4 | The load identity 3 h n = Q S d | CONFIRMED as a declaration | ALGEBRA.md 5.3 names it the load-time identity, a unit and not a derivation |
| 4, Eq. (square) | W = E_0'^2 + 3 p . p, E_0' = N_l N_w M, c^2 = 1/3, a declared identity | CONFIRMED as declared | ALGEBRA.md 5.3, 5.10; the paper says declared |
| 4 (ii) | abs(S(N) - 2 sqrt 2) <= 8 / N + 0.0444; above the bound at N = 16 and 32 with S = 3 | CONFIRMED | Recomputed: S(16) = S(32) = 3; the inequality holds for every multiple of 8 up to 4096 (checked) |
| 4 (ii) | The plateau is below 2 sqrt 2 by 3.02 x 10^-4 | CONFIRMED | Recomputed: 2 sqrt 2 - 181/64 = 3.021 x 10^-4 |
| 4 (iii) | Einstein's 6 pi beta^2 exceeds an order-beta term by 1 / (6 pi beta), about 330 at Mercury's pace | CONFIRMED | Recomputed: 1 / (6 pi beta) = 332 to 336 for Mercury's 47.4 to 47.9 km/s; under pi beta^2 the ratio is one sixth |
| 4 (v) | delta k = (n S / d)(g Y / c^2), Einstein's when n S = d | CONFIRMED as algebra | An identity of the stated form; the source (Einstein Outside II.10) not re-derived here |
| 4 (vii) | q_eff = -2 g_1 / (1 + g_1); -0.53 at g_1 = 0.36 | CONFIRMED in the number | Recomputed: -0.72 / 1.36 = -0.529; the derivation of the form from the diagram (`DARK_ENERGY.md`) not read (not reached) |
| 4 (vii) | q_eff = 2 k_0 (3 - k_0) / (1 - k_0)^2 > 0; the brightness reads 2 / (1 + g_1) | not reached | Both from `DARK_ENERGY.md`, not read in the time |
| 4 (viii) | The closure congruences Delta A_a = 0 mod h, sum of quotients j N | CONFIRMED as stated | ALGEBRA.md 5.8 "The closure, exact" (an integer congruence of the action rows) |
| 4 (viii) | a_j / a_i = (j / i)^2 and T_j / T_i = (j / i)^3 in the shell mean | CONFIRMED as a limit statement | From a_j = j^2 h^2 / (4 pi^2 kappa m) and Kepler's third law T^2 proportional to a^3; ALGEBRA.md 5.8; the paper labels the ladder a conjecture |
| 4 (viii) | One click reaches only the loops with 2 i^2 >= j^2 | CONFIRMED | Recomputed: a body at distance r has energy at least -k / r, so the new semi-major axis is at least r / 2; a_i >= r_j / 2 is 2 i^2 >= j^2; the reachable pairs (4, 3), (5, 4), (6, 5), (7, 5), (7, 6), (8, 6), (8, 7) as listed |
| 4 (viii) | Balmer's beta over alpha is 27/20 | CONFIRMED | Recomputed: (1/4 - 1/16) / (1/4 - 1/9) = 27/20 |
| 4 (viii) | The Bohr radius over the proton's radius is about sixty thousand | CONFIRMED | Recomputed: 5.3 x 10^-11 / 0.84 x 10^-15 = 6.3 x 10^4 |
| 4 (viii) | The lag's push along the motion is (S_1(v) / abs v) / (2 r), about 5 percent at r = 12 | CONFIRMED as an order | S_1 / abs v lies in [1, sqrt 3], so the ratio is 4.2 to 7.2 percent at r = 12 |
| 4 (viii) | About 17 degrees per shell at r = 3; the flux 17 percent below the inverse square | not reached | The fan's table, not recomputed |
| 4 (vi) | C_ring = 5.12, 5.44, 5.86; 3.65, 3.82, 3.92; F_L1 = 1.421; 0.974; 0.990 | not recomputed | The walk's ring on a board (`STEP_ALGEBRA.md`, `flow_weight/ALGEBRA.md` scripts); the isotropic limit 3/2 of F_L1 CONFIRMED (the sphere mean of the L1 norm of a unit vector is 3/2) |
| 5 | What is proved: Born to 1 / N_phi, rungs to 1 / (2 N_phi), Tsirelson to 8 / N_phi + 0.0444 | CONFIRMED | Each line verified in its own row |
| 5.1, Proposition (pace) | S_1 N_l <= T_D; S_1 = sqrt 3 abs D iff the three sizes are equal | CONFIRMED | Cauchy-Schwarz as the proof says; recomputed over 438914 primitive directions with components within 40: no violation, 920 equalities |
| 5.1, Proposition (pace) | v <= 1 / sqrt 3; 1 / sqrt 3 <= N_l abs D / T_D < (1 / sqrt 3)(1 + 1 / T_D) | CONFIRMED | T_D <= sqrt 3 N_l abs D < T_D + 1; `checks/light_speed.txt` sections 1 and 3 |
| 5.1 | The pace 64 / 110 on a heading, 1 / sqrt 3 on the diagonal | CONFIRMED | Recomputed: T = isqrt(3 x 64^2) = 110; isqrt(9 x 64^2) = 192 exactly |
| 5.1 | The anisotropy is of order 1 / (sqrt 3 N_l) | CONFIRMED | 1 / T_D with T_D within one of sqrt 3 N_l abs D |
| 5.1 | The Courant bound 1 / sqrt n and the lattice Boltzmann c_s^2 = 1/3 | CONFIRMED | Standard; `checks/light_speed.txt` section 5 |
| 5.2 | The carry s -> (e, s - e d) loses nothing | CONFIRMED | A bijection by the uniqueness of the division |
| 5.2 | The continuity equation follows from the books exactly | CONFIRMED as stated | ALGEBRA.md 4.3 (an identity of the ledger; DERIVATIONS_BEAM 25.4, not re-derived) |
| 5.2 | Gauss's law: signed crossings sum to one for a translation | CONFIRMED | A row on a straight digital line from inside a closed surface to the border crosses it net once (a translation has no return); ALGEBRA.md 4.4 |
| 5.3 | 2 c_f (n S / d) G M / (c^2 b): Einstein's at n S = d, c_f = 2 | CONFIRMED as algebra | An identity of the stated form with the declared inputs |
| 5.4 | Born's form recovered: the rung difference is the cell's weight over the total to 1 / N_phi | CONFIRMED | As the rung's row above |
| 5.4, Theorem 2 | The split preserves sum w^2 / m; the conjugate transpose returns the input up to (A w, A^2 m) | CONFIRMED | sum (w a_i)^2 / (m A) = w^2 / m; the transpose sums a_i (w a_i) = A w with multiplicity m A^2; `records.tex` app:proofs; ALGEBRA.md 4.6 |
| 5.4, Theorem 2 | The balanced splitter's joint table has B^H B = 2 I | CONFIRMED | Recomputed by hand: the off-diagonal x^(N/4) + x^(-N/4) = x^(N/4)(1 + x^(N/2)) = 0 in Z[zeta] |
| 5.4, Theorem 2 | U_s^T U_s = n_s I, n_s = C'^2 + S'^2; 65705 / 65536 at N = 64, s = 1 | CONFIRMED | Recomputed: C'[1] = 256, S'[1] = 13, 256^2 + 13^2 = 65705; `checks/tables_norm.txt` last line |
| 5.4, Theorem 3 | M o R o S o F is an injective Z-linear map of the quotient Q | CONFIRMED as a proof sketch | F permutes basis elements with the history fixed, S is injective under B^H B = A I, R under U^T U = n I, M is the identity of the module; `records.tex` app:proofs; ALGEBRA.md 4.7. The sketch is sound; a complete proof would state the action of F on the basis explicitly |
| 5.4, hypotheses (a) to (e) | Without (d) a detector reading 1 satisfies (a), (b) with A_2 = 1, (c); without (e) the zero detector | CONFIRMED | R = 1: 1 + 1 = A_2 (1 + 1) at A_2 = 1; R = 0: every A_2 |
| 5.4, Theorem 4 | A_2 = 2 | CONFIRMED | g = 0 in (b) with (a) and (d): 2 R(f) = A_2 R(f), one f with R(f) > 0 by (e) |
| 5.4, Theorem 4 | The parallelogram law from (b) by g -> x^(-N/4) g and x^(-N/2) = -1 | CONFIRMED | Recomputed by hand: R(x^(N/4) f + x^(-N/4) g) = R(f - g) by (a) |
| 5.4, Theorem 4 | The parallelogram law on the lattice makes R a quadratic form, no continuity needed | CONFIRMED | Jordan and von Neumann's polarization on an abelian group: B(f, g) = R(f + g) - R(f) - R(g) is biadditive from the identity alone; R(2 f) = 4 R(f) gives R = B(f, f) / 2 |
| 5.4, Theorem 4 | G commutes with multiplication by x; diagonal in the odd conjugates' basis | CONFIRMED | Multiplication by x is a signed permutation (orthogonal) on Z[zeta_N] of rank N/2, with simple eigenvalues the primitive N-th roots (j odd); a real symmetric matrix commuting with it is diagonal in that basis with real entries paired under j and -j |
| 5.4, Theorem 4, Eq. (gleason) | R(f) = sum over odd j < N/2 of c_j abs(sigma_j(f))^2, c_j >= 0 | CONFIRMED | The pairing of j with -j merges the two conjugate rank-one forms into abs(sigma_j)^2; a negative c_j is negative on an open cone, which contains lattice points; ALGEBRA.md 4.8 |
| 5.4, Theorem 4 | Conservation at a split iff A = sum a_i^2; at a rotation with C'^2 + S'^2 | CONFIRMED | Homogeneity and (a): sum a_i^2 R(f) / (m A) = R(f) / m iff A = sum a_i^2; the rotation's two outputs sum to (C'^2 + S'^2) R / (factor) |
| 5.4, Theorem 4 | Two rows read C_Sigma (a^2 + b^2) + 2 a b K(Delta); K(0) = C_Sigma, K(N/4) = 0, K(N/2) = -C_Sigma | CONFIRMED | abs(a + b zeta^(j Delta))^2 = a^2 + b^2 + 2 a b cos(2 pi j Delta / N); cos(pi j / 2) = 0 and cos(pi j) = -1 for odd j |
| 5.4 | Two offers at u and u + 1824, N = 8192, read 4104 and 4088 for 4096 each | CONFIRMED | Recomputed from the tables over the 8192 births with the rung of each birth's own weights: 4104 and 4088, a departure of 8 / N_phi |
| 5.4 | lambda = c N_phi d / n Links | CONFIRMED | A turn of n / d steps per interval completes in N_phi d / n intervals, c Links each |
| 5.4 | Planck's and de Broglie's relations as identities with h = h_q N_phi = h_A | CONFIRMED as declared | ALGEBRA.md 4.11 (an identity of the release under the dictionary) |
| 5.5 | E = (c_++ + c_-- - c_+- - c_-+) / N_phi; S at the labels (0, N/8, N/4, 3N/8) | CONFIRMED | Definitions; `checks/s_of_n.py` `chsh` |
| 5.5, Theorem 5 | The first party is + exactly for u < N/2 | CONFIRMED | The rows of U_b are orthogonal with equal norm, so C_2 = n_a n_b = C_K / 2 and b_2 = floor((N + 1) / 2) = N/2; recomputed over every setting pair at N = 64 |
| 5.5, Theorem 5 | The second party's + count is N/2 unless 2 N R(+,+) / C_K is odd, then N/2 + 1 | CONFIRMED | The proof's floor identity floor(y) + floor(1 - y) checked by hand (0 off an integer, 1 on one); R(+,+) = R(-,-) and R(+,-) = R(-,+) recomputed over every pair at N = 64 |
| 5.5, Theorem 5 | No tie at the twelve grains 8 to 1024 nor at the CHSH labels for 8 divides N <= 4096 | CONFIRMED | Recomputed: marginals N/2 for both parties over every setting pair at N = 8, 16, 24, 32, 48, 64, 96, 128, 192, 256, 512, 1024 (a tie would break them); 0 ties at the labels; `checks/s_of_n.txt` |
| 5.5 | The square wave's serial correlation over a cycle is 1 - 4 / N_phi; 0.9990 at 4096 | CONFIRMED | Recomputed: 15/16 at N = 64 (two sign changes in N cyclic pairs); 1 - 4/4096 = 0.99902 |
| 5.5 | A setting chosen from u (a = 0 below N/2, N/2 above; b = 0) gives the second party + at every birth | CONFIRMED | Recomputed from the cells at N = 64: + at all 64 births |
| 5.5 | B = A at a = b and B = -A at a = b + N/2 exactly | CONFIRMED | At a = b the cross cells have weight 0 (C' S' - S' C' = 0); at a = b + N/2 the table vector turns by a quarter turn, exact on the tables |
| 5.5 | A constant a = 0 leaves the second party's serial correlation 15/16 over 192 births; the cycle N/2, 0, 0 leaves -5/16; the marginal 96/96 in both | CONFIRMED | Recomputed from Theorem 5's cells at N = 64, b = 0: 15/16 with 96 of +; -5/16 with 96 of +; the declarable cycle 0, 21, 42 gives -1/16 with 96 of +, the number the paper reports read after a detector (row 1c) |
| 5.5 | The strict-crossing rung gives the second party 33/64 in 3944 of 4096 pairs at N = 64 | CONFIRMED | Recomputed with the rung N C_k > u C_K: 3944 setting pairs |
| 5.5, Theorem 6, Eq. (ebound) | E_N = 4 c_++ / N - 1; abs(E_N - cos(2 pi (a - b) / N)) <= 2/N + 4 arcsin(sqrt 2 / (2 rho)) < 2/N + 0.0111 | CONFIRMED | Recomputed: rho = 255.293, 4 delta = 0.011079; the bound holds over every setting pair at N = 64 (worst 0.0355 against 0.0424) and N = 512 (0.0115 against 0.0150); the proof's angle argument checked by hand (a rounding of at most 1/2 per component moves the direction by at most arcsin((sqrt 2 / 2) / length)) |
| 5.5, Theorem 6 | abs(S(N) - 2 sqrt 2) <= 8 / N + 0.0444 | CONFIRMED | 16 delta = 0.04432; recomputed for every multiple of 8 up to 4096 |
| 5.5, Theorem 6 | S(N) above 2 sqrt 2 for 252 of the 512 multiples of 8; S = 3 at 16 and 32; 23/8 at 128 | CONFIRMED | Recomputed exactly (S^2 > 8): 252 of 512; S(16) = S(32) = 3; S(128) = 23/8 |
| 5.5, Theorem 6 | 181/64 at 512 through 8192; 5793/2048 = 2.828613 at 16384 | CONFIRMED | Recomputed: S(512) = 181/64 with E = (91/128, -91/128, 45/64, 45/64); S(1024) to S(8192) = 181/64; S(16384) = S(32768) = 5793/2048 |
| 5.5, Theorem 6 proof | 176/64, 720/256, 2896/1024 at N = 64, 256, 1024 | CONFIRMED | 11/4, 45/16, 181/64 recomputed |
| 5.5 | The closed form S(N) = 8 (c_1 + c_1') / N - 4 beyond the tables' bound | CONFIRMED | From E_2 = -E_1 and E_4 = E_3 (recomputed at every listed grain) with E = 4 c / N - 1; `checks/s_powers_of_two.py` |
| 5.5 | The fixed-table limit 186034 / 65773 = 2.828425, 2.1 x 10^-6 below 2 sqrt 2 | CONFIRMED | Recomputed from the table vectors at the labels (256, 0), (237, 98), (181, 181), (98, 237): E = 46565/65773, -46565/65773, 46452/65773, 46452/65773; the sum 186034/65773; 2 sqrt 2 minus it 2.09 x 10^-6 |
| 5.5 | The tables' bound 2 N_phi <= 65536 | CONFIRMED | `core/phase.py` `MAX_PHASE_STEPS` = 65536 for the half-angle table at 2 N_phi |
| 5.5 | At a tie c_-- = c_++ - 1 and E drops by 2 / N | CONFIRMED | The first party's cells hold N/2 each; a tie adds one to the second party's + at the first party's - cell, taking it from (-,-) |
| 5.5, Eq. (prediction) | S_U24 = 181/64 = 2.828125; Delta S = -3.02 x 10^-4 | CONFIRMED | Recomputed |
| 5.5 | The correlations 725/1024 and 723/1024 at N = 4096, above and below 1 / sqrt 2 | CONFIRMED | Recomputed: E(0, N/8) = 725/1024 = 0.70801, E(N/4, N/8) = 723/1024 = 0.70605, 1 / sqrt 2 = 0.70711 |
| 6.1 | The closed form s(t) = floor(s_0 + r t) for a constant rate | CONFIRMED | ALGEBRA.md 4.1 (the carries of a constant-rate accumulator) |
| 6.1 | The centred step (abs s + floor(d / 2)) / d with the sign | CONFIRMED | A definition; ALGEBRA.md chapter 2 |
| 6.1 | (G): Z[Z_N] / (x^(N/2) + 1) = Z[zeta_N] for N a power of two, rank N/2 | CONFIRMED | As above |
| 6.1 | (E): ev's kernel is the ideal of the cancel, "exactly" | NOT CONFIRMED | The same omission as Section 2's (E) line: exact for N_phi a power of two only |
| 7 | 3! x 2^3 = 48 | CONFIRMED | Recomputed |
| 7 | Every Bravais lattice's point group is a subgroup of the octahedral group of order 48 | NOT CONFIRMED | Wrong for the hexagonal lattice: its holohedry D_6h (order 24) contains a six-fold rotation, and the cube's rotation group S_4 has no element of order 6, so D_6h is not a subgroup of O_h; the true crystallographic statement (ALGEBRA.md 1.4) is that no three-dimensional lattice has a point group of order above 48 |
| 7 | Over the integers the only bijections preserving a Node's cone are the 48 | CONFIRMED with a reading | Read as the Z-linear automorphisms of Z^3 fixing the Node and preserving the L1 ball (the octahedron): they permute its six vertices, hence are the signed permutations; a boost has irrational entries and is not Z-linear |
| 7 | The 24 rotations are S_4 on the four body diagonals; the hand is det(g) | CONFIRMED | As Theorem 1 |
| 7 | The symmetric integer matrices fixed by the 48 are the multiples of the identity | CONFIRMED | Recomputed (the group average) |
| 8.1, Table 1, row 1a | S = 181/64 = 2.828 at N_phi = 2048, exact | CONFIRMED | Recomputed: S(2048) = 181/64; `DECLARATIONS.md` section 1 item 4 |
| 8.1, row 1b | S = 2 under the phase-form window, a control | CONFIRMED as stated | ALGEBRA.md 4.10 (a local deterministic response gives S = 2 exactly, Bell's bound for a product form); not recomputed on a window |
| 8.1, row 1d | No-signalling 0 exactly; 32 of 64 at every setting | CONFIRMED | Theorem 5, recomputed at N = 64 over every pair |
| 8.1, row 2a | 0.99 at 128 periods; 0.959, 0.958, 0.958 at 12, 16, 24 Links for 32 periods | not recomputed | The train's coherence on a layer (`DECLARATIONS.md` section 7, its script); no closed form given in the paper |
| 8.1, row 2b | 1.00 - 0.02; the dark port 0 of 64 | not recomputed | A layer computation of the closure (`ALGEBRAIC_CLOSURE.md` row 2b); the dark port's exact zero is the cancel (CONFIRMED) |
| 8.1, row 2c | The exponent 2 exactly; the Sorkin sum 0 to the remainder's grain | CONFIRMED | The click is the quadratic form f^T G f; a quadratic form's third-order interference term vanishes identically |
| 8.1, row 9 | 128 of 256 at 45 degrees | CONFIRMED | Recomputed: at the setting N/4 of N = 256 the half-angle table vector is (181, 181), the weight 1/2 exactly, the rung 128 |
| 8.1, row 10 | 0.842 at w = 2 lambda, F = 0.16; 0.886 in the far field | not recomputed | The Rayleigh-Sommerfeld sum on the board (`ALGEBRAIC_CLOSURE.md` row 10) |
| 8.1, row 7 | The coupled modes 0.0995 and 0.1432; 0.09948 within 0.3 percent | not recomputed | A numerical mode of the coupled scheme on a 64^2 layer (`coupled_mode_pins.py`, needs numpy) |
| 8.1, row 4a | 42.364 against 42.36 at rest | CONFIRMED in the form | Recomputed: 2 pi / omega_b = 2 pi / 0.14833 = 42.36 at the layer's declared mode (`DECLARATIONS.md` section 8) |
| 8.1, row 4b | 1 + z = 1.9889 on the declared world; the free limit 1.9339 | CONFIRMED in the limit, the pin not recomputed | Recomputed: gamma_m (1 + beta) at the medium pair [156, 157], K = 3, the exact cone: 1.93392; the pin 1.9889 is the mode ratio of the closure's script (not run here) |
| 8.1, row 4c | (1 + beta_c) / (1 - beta_c) = 3.732 at k = 3 exactly | CONFIRMED | Recomputed: beta_c = 1 / sqrt 3 gives 2 + sqrt 3 = 3.73205 exactly |
| 8.1, row 5a | Within 0.8, 0.4, 0.2 percent of c at 12, 16, 24 Links, as the inverse square of the wavelength | CONFIRMED | Recomputed on the exact axis band: the phase pace is below c by 0.77, 0.43, 0.19 percent; the leading term k^2 / 36 on an axis |
| 8.1, row R2 | beta = v_c / c = 0.5774 at k = 3 exactly | CONFIRMED | Recomputed: (1/3) / (1 / sqrt 3) = sqrt 3 / 3 = 0.57735 |
| 8.1, row LC | 2 L / c = 207.85; N_0 = 218 +- 2 | CONFIRMED in the form, the pin not recomputed | Recomputed: 120 sqrt 3 = 207.846 at L = 60; 218 is the chain map's first rung (`DECLARATIONS.md` section 10) |
| 8.1, row v | n^2 = 1 + G g / (omega_0^2 - omega^2) | CONFIRMED as algebra | As Section 3's index row |
| 8.1, rows v-m, ii | 0.498; 0.7814 and 0.8032 | not recomputed | Numerical modes of the closure's scripts |
| 8.1, row M1 | The side lobe's centroid at y = 64 + 27.79 for lambda_dB = 12 | not recomputed | The two-source sum with the band's k per ray on a layer (`matter_wave_pins.py`, needs numpy) |
| 8.1, row M2 | 169 +- 2; the group transit 167.1; m = k / v_g = 1.0417 | CONFIRMED in the closed forms, the pin not recomputed | Recomputed on the axis band of [800, 809] at omega = 0.33408: k = 0.52361 (2 pi / 12), v_g = 0.50264, 84 / v_g = 167.12, k / v_g = 1.04172; the rest mass 3 tan omega_0 = 0.45126 and m c_eff^2 = omega_0 exactly (an identity: cos omega_0 (omega_0 / sin omega_0) = omega_0 / tan omega_0); 169 is the chain map's first rung |
| 8.1, row A | The deficit omega_0^2 / 4; 3.6 x 10^-28 s from 2 x 10^-14; 6.3 x 10^-31 s from the Crab bound | CONFIRMED in the first number | Recomputed: sqrt(8 x 10^-14) over the electron's rest angular frequency 7.76 x 10^20 per second gives 3.64 x 10^-28 s; the second number corresponds to a coefficient 6.0 x 10^-20, an input I did not verify |
| 8.1, row A2 | The coefficient 3 sum n_i^4 - 1 in [0, 2] on the sky | CONFIRMED | 0 at the body diagonal, 2 on an axis, sum n_i^4 in [1/3, 1] |
| 8.1, row B | epsilon (gamma_m^2 - 1) / 2 below 1 / gamma_m | CONFIRMED | As Section 3's motion row |
| 8.1 | E_0 = h omega_0 with omega_0 = m c^2 at the massive cone | CONFIRMED as an identity of the band | m = 3 tan omega_0 and c_eff^2 = (1/3)(omega_0 / tan omega_0) give m c_eff^2 = omega_0 exactly |
| Appendix A | C_N[p] = round(256 cos(2 pi p / N)); S_N[p] = C_N[p - N/4]; the half turn and quarter turn exact | CONFIRMED | Recomputed: the repository's fixed-point tables equal the high-precision rounding for every N up to 1024 (no half-integer arises, the only rational cosines on the circle being 0, +-1/2, +-1); the half and quarter turns exact for every power of two 4 to 65536 |
| Appendix A | The norm C^2 + S^2 lies in [65536 - 351, 65536 + 361] for every power of two <= 65536 | CONFIRMED | Recomputed: -351 (at N = 32768) to +361 (at N = 4096); `checks/tables_norm.txt` |
| Appendix A | The normalisation by C_K makes the click's probabilities sum to one | CONFIRMED | b_K = N_phi |

## The counts

Statement rows in the table: 174.

- CONFIRMED (including "as stated", "as declared", "as carried", "with a reading", "as algebra" and "in the form" where the line says so): 160; five of these carry a pinned number that is a numerical mode not recomputed here, said in the line.
- NOT CONFIRMED: 5 (four statements, one of them appearing twice).
- Neither, marked "not recomputed" or "not reached" (numerical modes of the closure's scripts, the fan's tables, the walk's rings, two lines of the dark-energy page): 9.

## The NOT CONFIRMED lines, in the order of severity

1. Section 3, "The two paces and the exact cone": the two gammas are said to be apart by about beta^2 gamma^2 omega_0^2 / 4 to second order. At the named cone c_eff the separation is beta^2 gamma^2 omega_0^2 / 6, because c_eff^2 / c^2 = 1 - omega_0^2 / 3 + O(omega_0^4); the coefficient 1/4 is the separation of gamma at c_m, whose cone is c_m^2 / c^2 = 1 - omega_0^2 / 2. ALGEBRA.md 8.1's own three numbers at K = 3 on [800, 809] (1.22705 at c_eff, 1.22820 at c_m, 1.22474 at c) show it: 0.00188 against 0.00186 for the sixth and 0.00279 for the quarter. A wrong coefficient in a stated second-order formula; the fix is "/ 6" (or "at c_m, / 4").
2. Section 7, "What the choice forces": "every Bravais lattice's point group is a subgroup of the full octahedral group of order 48, the crystallographic restriction". Wrong as a statement about lattices: the hexagonal lattice's point group D_6h has order 24 and contains a six-fold rotation, which no element of the cube's rotation group S_4 has (its elements have orders 1, 2, 3, 4), so it is not a subgroup of O_h. What is true, and what ALGEBRA.md 1.4 says, is that no three-dimensional lattice has a point group of order above 48. A wrong supporting sentence, not a theorem of the paper; the fix is that sentence.
3. Section 4, "The one fact and its two faces": the support bound's equality cases at N_phi = 64 are said to be, by enumeration, one phase and all 64 roots, the antiphase pair and 32, the comb of every eighth phase and 8. The enumeration is incomplete: on a cyclic group equality holds exactly for the translated and modulated indicators of subgroups (Donoho and Stark 1989), and Z_64 has seven subgroups, so the combs of every second, fourth and sixteenth phase (supports 32, 16 and 4, transforms of size 2, 4 and 16) attain the bound as well, and each with every translate and modulation. The three listed are equality cases; the word "by enumeration" is not met. The fix is "among them" or the full list.
4. Section 2 (E) and Section 6.1 (E): "ev is a surjective ring homomorphism whose kernel is the ideal (x^(N/2) + 1)", stated without the condition N_phi a power of two, which the objects paragraph states and which every registered grain meets; for N_phi with an odd factor the kernel is the ideal of the N-th cyclotomic polynomial, a proper divisor. A condition omitted where the sentence stands alone; the fix is four words.

## The numbers recomputed (pure Python, integers and fractions; the repository's integer tables as the one input)

The 48 and the 24 by enumeration and the S_4 action; the fixed symmetric matrices; the tables against the high-precision rounding for N_phi up to 1024, the half and quarter turns and the norm range through 65536; E(x)^2 and 256 E(x^2) at 64; the rotation's 65705; the bounds 2^62 - 1 and 2^63 - 1 and 65536^4; the rung, the cells, the marginals over every setting pair at the twelve grains 8 to 1024, the ties at the CHSH labels for every multiple of 8 to 4096, the mirror identities of Theorem 5's proof; S(N) at 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768 with the four correlations each, S(16) and S(32), the 252 of 512 above 2 sqrt 2 (exactly, by S^2 > 8), the bound 8/N + 0.0444 at every multiple of 8 to 4096, rho, 4 delta and 16 delta, the correlation bound over every pair at 64 and 512; the fixed-table correlations 46565/65773 and 46452/65773 and the limit 186034/65773; 2 sqrt 2 - 181/64 and the 1.05 standard errors; 725/1024 and 723/1024; the order channel's 15/16, -5/16, -1/16 and 96/96 from the cells, the square wave's 1 - 4/N, the setting-from-u case; the strict rung's 3944; lcm(3, 5, 64) = 960; the two offers at u and u + 1824 (4104 and 4088); the 1952 distinct table pairs at 8192, the (0, 4097) zero and its ideal weight, the absence of table zeros at 64 modulo the cancel; T_D and the Manhattan bound over 438914 primitive directions, the paces 64/110 and the anisotropy 3025/1024, 1521/512, 3, the closed forms m_D and tau_k; the dispersion coefficient 0, 1/2, 2, 4/5 and the axis band's 0.77, 0.43, 0.19 percent; the massive band's identities by hand, omega_0 at [800, 809] and [3200, 3236], c_m^2 / c^2, c_eff^2 / c^2, omega_0 / sin omega_0 = 1.0037, the three gammas at K = 3 and their separations, 1 + z = 1.9355 at [800, 809] and 1.9339 at [156, 157], omega_0^2 / 4 at N_0 = 50, 2 + sqrt 3, 3/2, 207.85, 42.36, M2's k, v_g, 167.1, 1.0417, 3 tan omega_0 and m c_eff^2 = omega_0, the click theorem's sixth-order residual, row A's 3.6 x 10^-28 s, Mercury's 1 / (6 pi beta), the Bohr over proton ratio, q_eff at g_1 = 0.36, Balmer's 27/20, the reach pairs 2 i^2 >= j^2, the fan's 2.83.

## What I did not reach

- The numerical modes and walks of the closure's scripts (rows 4a's 0.8116 family, 4b's 1.9889, 7's 0.0995 and 0.1432, LC's 218, M1's 27.79, M2's 169, v-m's 0.498, ii's 0.7814 and 0.8032, 10's 0.842 and 0.886, 2a's and 2b's visibilities, the ring's C_ring values and its factors): they need numpy, which this container lacks, and are not closed forms; each is marked "not recomputed" in its row, with its source named.
- The dark-energy page's two formulas (the sign of the crowd's own accumulation and the brightness's 2 / (1 + g_1)), the fan's "17 degrees per shell" and "17 percent below", and the Newton and bending chains of ALGEBRA.md 5.6 and 5.9 beyond the identities quoted: not read in the time.
- `records.tex` beyond its auxiliary proofs and the symbol table's existence: history, read for context only.
- Nothing in the paper was changed; the paper's prose and every comparison with nature are the physicist's.
