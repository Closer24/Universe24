> **Historical research record.** This text describes its original configuration and contains superseded paths, defaults and interpretations. For the executable current construction and evidence boundaries, use the [system map](../../docs/SYSTEM_MAP.md) and its linked algebra. Claims marked THEOREM or DERIVED below retain their original stated assumptions; they are not a certificate that the current default derives physical laws.

# FULL PICTURE — Universe24 through its clocks (final synthesis, Study 36)

Writer: SYN (Study 36). Skeleton written Tue Nov 10 16:29 UTC 2026 (`date -u`); final: Tue Nov 10 17:43:11 UTC 2026 (`date -u`).
Request (the owner, relayed by the manager): one last attempt at the full picture, through the clocks, the tensor and the
Einstein approximation.
Scope: ONE story, from the node to the outlook. This document adds NO new physical claim. Every content line repeats,
combines or labels a signed record; anything without a signed source or an exact check is OPEN.
Labels: every content line below carries exactly one label. Headings, this front matter and the two keys are structure.

| label | meaning |
|---|---|
| THEOREM | proved from the law; the proof is in the cited signed record |
| NUMERIC | an exact integer computation in a cited record |
| DERIVED | a short argument from the lines above it; not separately signed |
| CHOSEN | an input, a convention or an owner decision; it could have been otherwise |
| NEW LAW | an extension that changes the law's content (approved, or proposed and not adopted) |
| DATA | a number the law does not produce; it sits in the tensor's integers or in the seed |
| OPEN | not established |
| IMPOSSIBLE | excluded by a theorem under the stated rules |

Source key. Every citation names a Study (research record) and a row or section of it. Study 24 (research record) is
THE_ALGEBRA.md in this folder; Study 26 (research record) is summarised in CHANNELS.md in this folder. Only records signed by
both of their researchers are used, except Study 30, a single-researcher run record cited for NUMERIC results only, and the
study briefs, cited only for the owner's rules as relayed. The records and their sha256 prefixes are listed at the end.

---------------------------------------------------------------------------------------------------------------------
## §0 The story in seventeen lines
0. [DERIVED] The thread: every object below is a clock (a gear's rate), a click (a carry of a clock's remainder) or a reading of clocks; the law makes the clocks, the tensor sets their rates and their couplings, and gravity and the cosmic hand act by changing rates.
1. [CHOSEN] Space is the periodic cube (Z/LZ)³; every node holds the same gears (a, b, r); a gear reads only its own node and its six face neighbours.
2. [THEOREM] One update, Rule3, is an exact bijection: the past is recovered from the present, stage by stage.
3. [THEOREM] Every gear is a clock: b(t+1) + b(t−1) = 2u/D + ε with |ε| < 1, and a mode with eigenvalue μ ticks at cos w = μ/2.
4. [THEOREM] A click is a carry of the remainder, and the ledger D·Σℓ = ΣK + r(0) − r(T) is exact for every gear.
5. [THEOREM] For the reciprocal part, Rule3 is the discrete Euler–Lagrange equation of one integer potential Φ per block, and rank = degree of Φ.
6. [CHOSEN] Rank 4 (a quartic Φ, a cubic force) is final; the seven-step recipe of §3 builds every tensor.
7. [THEOREM] A mass is a rest click rate; the cube fixes multiplets, pairings and lattice-scale ladders, not the values (§4).
8. [DERIVED] Gravity is the lapse slowing clocks by 1 − 2U and links by 1 − 4U; in the weak-field continuum limit this is the metric of general relativity with γ = 1 (§5).
9. [IMPOSSIBLE] An exactly conserved reciprocal gravity source and an exact Bianchi identity, at any rank: the full Einstein equations are not on the board (§5).
10. [CHOSEN] Owner rule: the cosmic clock (the WIND hand) reads no matter and no matter reads it; ONE v1, the default, obeys it for every package gear (§6).
11. [DERIVED] Through time alone a cosmic turn reaches matter only as a redshift of the clocks that read the lapse; an opt-in clock law (CG2, default OFF) holds the uniform lapse at L = 6 but not on larger boards (§6.4).
12. [THEOREM] There is one exact bang (THEOREM D); the board's information is law + seed + log t (THEOREM K); the choices time the turns and never cause a bang (THEOREM N).
13. [THEOREM] Born counts are exact; with no freeze and free choosers the board obeys Bell's bound S ≤ 2 (§7).
14. [NUMERIC] One quantum works exactly as the owner's path rule says, with no freeze: one emission click, one absorption click, Born exact (§7).
15. [CHOSEN] The owner's addition: the click has a choice, so the universe is not deterministic (§8).
16. [NUMERIC] On the board that choice is free data: re-drawing it changes 98 % of the outcomes and not one bit of the history (§8).

---------------------------------------------------------------------------------------------------------------------
## §1 The node: strictly local; the links make the geometry
### 1.1 Where a gear may look
- [CHOSEN] Space is the periodic cube Λ = (Z/LZ)³ with one side length L ≥ 3 and six face neighbours x ± e_d; the neighbour graph itself is a choice (the cube), not an output. — Study 24 (research record) §1.1.
- [CHOSEN] Every node holds the same list of gear types; a gear holds (a, b, r) with a, b integers and r ∈ {0, …, D − 1}; ONE divisor D = 6Q for every gear, Q = 2^33 + 1. — Study 24 (research record) §1.1.
- [CHOSEN] B3 locality: every monomial of the tensor lives on ONE node or ONE face link (all its offsets in {0, e} for a single face direction e). — Study 24 (research record) §3.4.
- [THEOREM] The package builder enforces B3: an edge, diagonal or long offset, or a monomial touching both +e and −e, is rejected (LocalityError), so in every composed tensor the inputs of a gear come only from its node and its six faces. — Study 24 (research record) §3.0, §3.4.
- [THEOREM] Cone theorem: one update moves influence by at most one face, so the state at x after t updates depends only on the seed inside the taxicab ball of radius t; board-causal no-signalling is a theorem of the law. — Study 24 (research record) §3.4 (X36).
- [DERIVED] That hard cone is wider than the wave cone c_Q ≈ 0.577, so the law alone is board-causal, not c_Q-causal. — Study 24 (research record) §5.1a.

### 1.2 What sits on a node
- [THEOREM] The dark board L0 carries the 48 labels of the binary octahedral group 2O; the LEFT action is frame and spin, the RIGHT action is internal (an exact Q8 isospin skeleton); mirrors act as the outer automorphism; spin ½ is exact (z = −1 is the 2π turn). — Study 24 (research record) §2.1, §2.2, §2.5.
- [THEOREM] As a real algebra the node gives real and quaternionic blocks only: it makes SU(2)s natively, never U(1) or SU(3). — Study 24 (research record) §2.1.
- [THEOREM] The cube has exactly one orientation bit; given massive Dirac matter (a CHOSEN content) there are exactly two hands, Γ5 = −PxPyPz, and Γ5·V is the unique chiral, CPT-even, clock- and charge-keeping split. — Study 24 (research record) §2.4, §7.1.
- [THEOREM] Block sizes: the Dirac pair 16, the links V⊗V* (SU(2) 4, SU(3) 18, U(1) 2, U(2) 8) and the metric 10 = Sym²R⁴ are minimal real modules; L0 = 48 is the regular module of 2O, fixed by the contract, not by minimality; the content and the total are chosen. — Study 26 (research record) A9; Study 24 (research record) §3.9.
- [CHOSEN] The inputs of the node: d = 3, L, the 2O labels, the body actions (0, 1, 3), the axis signs (1, −1, 1) and the value of Q. — Study 24 (research record) §10.0.

### 1.3 The links (face terms) make the geometry
- [CHOSEN] One common stencil for the ten metric gears, the E1 photon's potential and (in magnitude) every L0 channel: on-site 6 and six face weights Q − 1 (the exceptions are the β gear and the E1 accumulator). — Study 24 (research record) §5.1a.
- [THEOREM] With that stencil the plane-wave law is exact: cos w = 1 − c_Q²·Σ_d (1 − cos k_d) with c_Q² = (Q − 1)/(3Q), so there is ONE cone, c_Q = 0.5773502691560 at the package Q. — Study 24 (research record) §5.1a.
- [THEOREM] Forces are links: at rank 3 one link per face per irreducible multiplet spans its whole matrix algebra (Burnside), and three link factors on one hop would be degree 5 > 4, so the rank bound forces ONE unified link per face per multiplet. — Study 24 (research record) §3.2, §7.2.
- [NUMERIC] Gauss = Noether + remainder on the links: local Z4 / Q8 / Δ96 covariance bit-exact, with 0/1,280, 0/32,400 and 0/92,160 failures (U(1), SU(2), SU(3)). — Study 24 (research record) §7.2.
- [CHOSEN] A link reads the lapse at BOTH of its end nodes: 1 − (F(x) + F(x + e))/P = (1 − 2U(x))(1 − 2U(x + e)) + O(U²) ≈ 1 − 4U, while a site term reads it once, 1 − 2U (c_link = 1; the average of the two ends, c_link = ½, is equally B3-legal). — Study 24 (research record) §5.1c.
- [DERIVED] So at first order the link factor is the square of the clock factor: this one fact is the γ = 1 geometry of §5 (in the linearised layer of §5.2 the field equation forces it). — Study 24 (research record) §5.1c.

---------------------------------------------------------------------------------------------------------------------
## §2 The law and its inverse: every gear is a clock
### 2.1 The law
- [CHOSEN] Rule3, for every gear of every node at once, from the SAME complete previous snapshot: (ℓ, r′) = divmod(K + r, D), a′ = b, b′ = ℓ − a, with K = 2u (always even) and floor division. — Study 24 (research record) §1.2.
- [CHOSEN] u is the fixed integer tensor evaluated on v = (1, b, a) of the node and one face; no monomial reads a remainder; r enters only its own gear's divmod. — Study 24 (research record) §1.1, §1.8.
- [THEOREM] At a = b = 0 every monomial vanishes (the default has no constant term), so every vacuum (0, 0, r) is fixed; a vacuum remainder fixed by the exact mirror exists exactly when Q is odd, and then the fixed pair is {3Q − 1, 3Q}. — Study 24 (research record) §1.5, §1.6.
- [CHOSEN] The package puts every gear at r = 3Q − 1, one member of that pair. — Study 24 (research record) §1.5 (X39).

### 2.2 The inverse (audit and recovery, never a stage of evolution)
- [THEOREM] From the new snapshot: old b = a′; then K is known, r = (r′ − K) mod D, ℓ = (K + r − r′)/D and old a = ℓ − b′; a gear that reads other gears' a is undone after them, which needs an acyclic a-read graph (the builder rejects a cycle). — Study 24 (research record) §1.3, §3.6.
- [THEOREM] The inverse uses neither the sign nor the time-independence of the coefficients, so the bijection survives any coefficient and any runaway. — Study 24 (research record) §1.3.
- [NUMERIC] Rewinds are exact on the full package default (L = 3, data ±2^10), across all six turns of ONE v1 (1,200 updates), and across the rejected coupling's runaway (1,554 updates at L = 6, 667 at L = 4). — Study 24 (research record) §1.3; Study 22 (research record) R18; Study 30 (research record) R1, L4c.

### 2.3 Every gear is a clock
- [THEOREM] Because a(t+1) = b(t), Rule3 gives ℓ(t) = b(t+1) + b(t−1), hence b(t+1) + b(t−1) = 2u(t)/D + ε(t) with ε = (r(t) − r(t+1))/D and |ε| < 1. — Study 24 (research record) §1.2, §4.1.
- [THEOREM] About the vacuum, u = Hb + O(b²) gives the leapfrog b(t+1) + b(t−1) = M b(t) + ε with M = 2H/D and ONE kinetic coefficient D for every gear. — Study 24 (research record) §4.1.
- [THEOREM] A mode with M e = μ e ticks at cos w = μ/2: |μ| < 2 is a clock, μ = 2 is massless, μ = −2 is the doubler, |μ| > 2 grows; translation invariance gives every momentum k its own clock, cos w(k) = μ(k)/2. — Study 24 (research record) §4.2.
- [NUMERIC] Two coupled gears at D = 6006 predicted at 0.16676 and 0.20156 ticks per update are measured at 0.16675 and 0.20155 (20,000 updates, amplitude 10⁷). — Study 24 (research record) §4.2.
- [NUMERIC] A gear shows its eigen-rate only at amplitude ≫ 1: at amplitude 1 the orbit locks to a rational period (6 instead of 5.42). — Study 24 (research record) §4.3, X38.

### 2.4 A click is a carry; the ledger is exact
- [THEOREM] r′ = (r + K) mod D: the remainder is a phase register on the circle Z_D, advanced by K every update, and ℓ counts its passes through 0; a CLICK is ℓ ≠ 0 together with a change of the gear's triple. — Study 24 (research record) §4.4.
- [THEOREM] Nothing is rounded away: ε is exactly what the integers cannot hold, and the remainder carries it to the next update; this is why Rule3 is a bijection. — Study 24 (research record) §4.4.
- [NUMERIC] The smallest clock, u = 12b at Q = 5 (D = 30) from (0, 1, 14): r walks 14 → 8 → 2 → 2 → 8 → 14, the carries are 1, 1, 0, −1, −1, 0, the period is 6, and every carry becomes the next b. — Study 24 (research record) §1.4.
- [THEOREM] The ledger: D·Σ_{t<T} ℓ(t) = Σ_{t<T} K(t) + r(0) − r(T) for every gear (a telescoping sum). — Study 24 (research record) §4.5.
- [NUMERIC] Ledger failures: 0 of 4,950,720 sampled gear-updates in ONE v1 (L = 6, 1,200 updates) and 0 of 6,435,936 in the runaway run of the rejected coupling. — Study 22 (research record) R8; Study 30 (research record) R1.
- [THEOREM] The two-time energy E = D|b|² + D|a|² − 2aᵀHb of a linear symmetric part (an algebraic account, not established physical energy) changes ONLY by remainder kicks: E(t+1) − E(t) = Σ (r − r′)(b′ − a). — Study 24 (research record) §4.8.

### 2.5 No freeze, by the law itself
- [THEOREM] An oscillator cannot be paused by its own input (a pause needs ℓ = a + b of the gear itself, a self-a-read, which breaks the bijection), and no b-only rule of any degree generates a hold. — Study 24 (research record) §3.6, §8; Study 23 (research record) B1, C4.
- [THEOREM] A bounded orbit of the bijection is exactly periodic (THEOREM P). — Study 24 (research record) §4.9.
- [CHOSEN] Board time t = the number of Rule3 updates, the same for every gear; a clock's own tick is read by the read-only rule R2 (one sign cycle of its click sizes in its own rotating frame). — Study 24 (research record) §4.7.

---------------------------------------------------------------------------------------------------------------------
## §3 The tensor: the rank-4 recipe (rank = degree of Φ)
### 3.1 What a tensor is
- [CHOSEN] A tensor is an ordered list of gear types plus a list of monomials (target, integer coefficient, at most three factors); a factor is (gear type, offset in {0, ±e_x, ±e_y, ±e_z}, field a or b). — Study 24 (research record) §3.0.
- [CHOSEN] Rank = 1 + the largest number of factors, so rank 4 means at most three factors; rank 4 is final by owner decision. — Study 24 (research record) §1.1, §3.11.
- [THEOREM] For the reciprocal part Rule3 is the discrete Euler–Lagrange equation of L(x, y) = Φ(x) + Φ(y) − D·x·y, with the integer rounding carried by the remainder; reciprocity itself is a design rule, not forced by Rule3. — Study 24 (research record) §1.7.

### 3.2 The seven steps
1. [CHOSEN] Blocks: gear types, terms, vacuum remainders, parameters and one Q; compose() merges the blocks and enforces ONE Q. — Study 24 (research record) §3.1.
2. [THEOREM] One integer potential Φ per reciprocal block: if Φ has degree n, each force ∂Φ/∂b has degree n − 1, so rank = degree of Φ. Quadratic Φ (rank 2) gives inertia, masses and ports; cubic Φ (rank 3) a hop through a dynamic link or a lapse dressing; quartic Φ (rank 4) the link spring −(λ/4)(|U|² − A²)². — Study 24 (research record) §3.2.
3. [THEOREM] Deviation form about the vacuum: subtracting D·X0·X̃ makes the vacuum a fixed point; the builder refuses a surviving linear term or a non-integer coefficient. — Study 24 (research record) §3.3.
4. [CHOSEN] B3 locality: node plus one face, the link gear stored at its base node, enforced by the builder (§1.1). — Study 24 (research record) §3.4.
5. [CHOSEN] Reciprocal versus designated: a reciprocal block passes the exact checker (one Φ, symmetric Jacobian, action = reaction); a one-way entry must be designated with a written reason, and Newton III fails for it. — Study 24 (research record) §3.5.
6. [THEOREM] Staging: a gear may read the a of earlier stages only, or the inverse fails. — Study 24 (research record) §3.6.
7. [CHOSEN] Compose, then run the ten checks: one Q; rank ≤ 4; B3; acyclic a-reads; reciprocity; vacuum fixed; rewind; the reversor R*; an all-k Bloch scan; integrality. — Study 24 (research record) §3.7.

### 3.3 What the recipe gives
- [THEOREM] Checks 1–8 are kinematic and do not imply a bounded history; the all-k scan (check 9) is what separated the runaways from the bounded runs. — Study 24 (research record) §3.7.
- [NUMERIC] A worked block (compact U(1), Q = 5): 8 gear types, 77 monomials, rank 4, 0 reciprocity violations; the radial link's coefficient 22 = D − 2λA² is inertia minus spring stiffness, and its rank-4 part is −1·W_re³ (a quartic Φ gives a cubic force). — Study 24 (research record) §3.10.
- [NUMERIC] The package default (FIX-i): 375 gear types, 18,553 monomials, rank 4, 706 designated one-way entries, 3 inverse stages. — Study 24 (research record) §3.9.
- [NUMERIC] ONE v1 adds the seven-gear cosmic block: 382 gear types, 18,592 monomials, 736 designations, rank 4. — Study 22 (research record) R1; Study 26 (research record) A1, A2.
- [NUMERIC] Rank 5 was tested and rejected: it lifts one wall only to an approximate echo (0.0033), cannot generate a hold, brings an unbounded-below term and cuts the usable amplitude about 19-fold (6,553 → 350). — Study 23 (research record) A1, B1, C2, C3.

---------------------------------------------------------------------------------------------------------------------
## §4 Masses = rest click rates
### 4.1 What the clock law fixes
- [THEOREM] A mass is a clock's rest rate: cos w0 = μ(0)/2; a lone gear u = m·b has cos w0 = m/D. — Study 24 (research record) §4.3; Study 21 (research record) Part III.1.
- [THEOREM] Symmetry fixes equal rates within a multiplet and never ratios between blocks (Schur); irrational rates come in Galois pairs (a light one has a heavy partner); the doubler ladder is 1:2:3 at the lattice scale. — Study 21 (research record) B2, B3, B4.
- [THEOREM] THEOREM S: on the handed dark board every L0 mode is massive, cos w ≤ 0.911 and w ≥ 0.4255. — Study 24 (research record) §2.3.
- [THEOREM] The board's own rates span about one decade at the lattice scale; nature's masses span about twelve decades far below, so no forced rate can be an observed mass ratio. — Study 21 (research record) A14.
- [DATA] The light masses are Yukawa integers in the tensor: about 39 bits for the lepton ratios alone. — Study 21 (research record) B6.
- [NUMERIC] The package's Dirac pair: m = 4915·2^22 at D = 6(2^33 + 1), m/D = 0.39998; board rate 1.159 rad per update (with the π/2 carrier), own-frame rest rate arcsin(m/D) = 0.4115 rad. — Study 24 (research record) §4.3.
- [DERIVED] Koide's Q = 2/3 holds to 2·10⁻⁶ but is not derived: the √2 is available in 2O, its use is accommodation, and QED dressing would spoil any bare law 170–250-fold; δ = 2/9 is numerology. — Study 21 (research record) Part III.4, III.5.

### 4.2 Masses out of the clicks (Study 35)
- [THEOREM] Out of the clicks, a mass is the sign-cycle rate of a large-amplitude rest state in its click record, and it equals the k = 0 eigenvalue divided by D; the literal clicks per update of a single quantum is a rounding lock, not the mass. — Study 35 (research record) B1, B18, Part III.1.
- [THEOREM] With nothing put in (six signed unit ports, the body actions, no on-site term, no mass entry anywhere) the handed dark board has exactly nine rest levels, fixed by 2O and the signs, eight of them visible in the clicks; their mean is fixed by the trace (cos w = 1/3), and the lightest is 0.068 per update: all at the lattice scale, nothing light. — Study 35 (research record) B2, A1, A4, Part III.2 (EDIT E1).
- [NUMERIC] Every clicking level was measured from the click record, never read from a parameter: within 6.9·10⁻⁸ per update of arccos(λ/6)/2π, and within 1.7·10⁻¹⁰ (cosine) in the package's own form at Q = 2^33 + 1. — Study 35 (research record) A2 (EDIT), B3.
- [THEOREM] The 90° level (λ = 0) is click-silent exactly in the reference cube; in the default form it is silent only below the amplitude 12·max|b| ≤ 3Q − 1 and clicks at a rate near 1/4 above it. — Study 35 (research record) B4, A3.
- [THEOREM] THEOREM E: identical clocks with symmetric tensor and seed stay identical bit for bit forever, so they cannot split themselves at any order. — Study 35 (research record) A6, B6.
- [THEOREM] Couplings and seeds do split a rate, but they never force a ratio: the mean is fixed (Σ_j cos w_j = N·cos w_bare), the degeneracy pattern is fixed by symmetry, and the spread is the coupling integer that was written or the seed that was chosen. — Study 35 (research record) B7, A8, B11, Part III.3 (EDIT E2).
- [THEOREM] At the vacuum every term of degree ≥ 2 has zero Jacobian, so any dressing of a rest rate needs seed amplitude: its size and pattern are seed data. — Study 35 (research record) B8, A7, B11.
- [THEOREM] No relaxation: a bijection with a fixed vacuum never reaches a state (a vev, a fixed point, a cycle) that it does not start on. — Study 35 (research record) B9, A11.
- [DATA] The doublet's mass is the tensor integer 2yv = 4915·2^22: the clicks show it exactly, they follow the integer when it is changed (4916·2^22 and 4000·2^22), and the cosmic hand does not touch it. — Study 35 (research record) A9, A10, B14.
- [NUMERIC] From the symmetric point Φ = 0 the Higgs runs away instead of settling (beyond 2^40 by update 44–46), so the doublet's mass exists only because the seed starts at the built-in Φ = v. — Study 35 (research record) B17.
- [NUMERIC] The lapse slows every clock that reads it by the same factor (L0 levels at U = 1/16, 0.05 and 0.2: ratios kept within 6·10⁻⁹); the default visible doublet does not read it, so the doublet : L0 ratio moves by the declared EP debt, not by a law; and on the periodic cube a resting dark clock drives the uniform lapse secularly, so there is no static self-gravity mass. — Study 35 (research record) A13, B13, B21, B12.
- [NUMERIC] A light mass can appear with NO mass entry: a massless clock riding a condensate in the seed ticks at a light rate proportional to the condensate (7.12·10⁻⁴ per update at amplitude 2^10, within 1 % of the formula, 95 times below the zero-input gap); its value is (the chosen coupling g = 1) × (the seed amplitude)²: data. — Study 35 (research record) A15 (EDIT), Part III.5.
- [IMPOSSIBLE] The light mass values and their ratios (the leptons, Koide's Q, δ) out of the clicks with no input: the board cannot create the ≈ 39 bits they carry (THEOREM K); they must be written once, as tensor integers or as seed amplitudes. — Study 35 (research record) A16, Part III.6.
- [IMPOSSIBLE] A forced Koide relation among identical clocks (THEOREM E); it can only be written in as data. — Study 35 (research record) Part III.7.
- [DATA] The Higgs radial rate equals the dark λ = 2 level exactly only because 2λ_H·v² = 4(Q − 1) was chosen: a coincidence of chosen integers, not a zero-input Higgs mass. — Study 35 (research record) B15, Part III.4 (EDIT E4).
- [IMPOSSIBLE] A mass value selected by the dynamics independently of the tensor and the seed. — Study 35 (research record) joint verdict M4.
- [NUMERIC] The doublet's self-dressing runs about 89 % through its own weak current and about 11 % through the Higgs (diagnostic variants with those couplings removed); its size stays seed and coupling data. — Study 35 (research record) MASS2-B post-signature T8.
- [NUMERIC] A naive flat-Higgs variant fails: the doublet's own density drives the flat Higgs (to 1.57 v in 400 updates), so its mass does not even stay at the tensor value; the board holds a vev only where the tensor pins it. — Study 35 (research record) AM-6 (one case).
- [OPEN] The click reading of the silent level and a stabilised flat-Higgs variant. — Study 35 (research record) MASS2-A final signature.
- [DERIVED] Verdict, in the joint wording of both researchers: "Every mass is MEASURED as a rest click rate. Its VALUE is a tensor integer or seed DATA, except the zero-input dark levels and 0, which the 2O node fixes by itself at the lattice scale (8 of 9 visible in clicks)." Every ratio among visible or light masses is data too. — Study 35 (research record) row A-§0.10 (conceded), Part III FINAL point 8.

---------------------------------------------------------------------------------------------------------------------
## §5 Gravity: the lapse slows clocks and links; the Einstein approximation
### 5.1 The lapse
- [CHOSEN] The lapse F is the b-counter of the gear metric.h00, and U := F/(2P) with P = 2^20. — Study 24 (research record) §5.0.
- [CHOSEN] A clock that reads the lapse gets the factor 1 − 2U on its mass (site) entries and 1 − 4U on its link (transport) entries; a first-order clock takes 1 − U and 1 − 2U; both come from one potential Φ_int. — Study 24 (research record) §5.0.
- [THEOREM] Feels ⇔ sources: the action (metric → matter) and the source (matter → metric) are the two derivatives of the same Φ_int, so Newton III is exact for every undesignated lapse term. — Study 24 (research record) §5.0.
- [THEOREM] The half-angle law (L0 form C, exact symbol): sin(w/2) = √(1 − 2U)·sin(w0/2), so a clock deeper in the potential ticks slower per board update: time dilation is a rate change. — Study 24 (research record) §4.7, §5.1b.
- [NUMERIC] The live tensor carries the form-C factors, clock 1 − 2U on the mass and link 1 − 4U on the transport, at every k: 147,456 entries at 64 k-points, 0 failures. — Study 24 (research record) §5.1b.
- [DERIVED] Continuum, weak field: w² = (1 − 2U)m² + (1 − 4U)c_Q²k², which is the eikonal of g00 = −(1 − 2U), g_ij = (1 + 2U)δ_ij: Newtonian potential Φ = −U and PPN γ = 1, while the 1911 control gives γ = 0. — Study 24 (research record) §5.1c.
- [DERIVED] Newtonian limit: a static field obeys the lattice Poisson law (Q − 1)ΔF = −s, and a slow body feels V = −mU, the same for every lapse reader. — Study 24 (research record) §5.3d.
- [NUMERIC] A field built by the board from F = 0 falls as 1/r (slope −1.0018), with Gauss ratio 1.0002–1.0008. — Study 24 (research record) §5.3d.
- [DERIVED] Redshift: a static lapse keeps every mode's board frequency, so a clock at x ticks at N(x) in its own frame and z = U_e − U_r + O(U²). — Study 24 (research record) §5.3a.
- [NUMERIC] The clicks read that slowing: |N_click/N_lapse − 1| ≤ 2.9·10⁻⁵ with a sourced field and 3.8·10⁻¹¹ with a frozen lapse. — Study 24 (research record) §5.3a.
- [THEOREM] The equivalence principle of the factor: every lapse-reading clock of a given order gets the same factor, as an integer identity. — Study 24 (research record) §5.2.
- [NUMERIC] In the live default only the dark L0 reads the lapse at rest; the visible Dirac doublet's rest clock neither feels nor sources it (its input changes by exactly 0 under a uniform U): the declared FIX-i EP debt, first order in U. — Study 24 (research record) §4.7, §5.2.
- [THEOREM] The k = 0 identity: summing Rule3 over the closed board, any net source drives the uniform lapse as t² (no restoring force; finding F4). — Study 24 (research record) §5.5e.
- [NUMERIC] On ONE v1 (L = 6, J-pure seed, 9,869 updates) the uniform lapse first rises as ≈ 1.8·10⁻⁹·t² (0.96 of the rate the exact summed-Rule3 identity predicts from the measured net source), reaches U = +0.024 at t = 4,000, comes back through 0 at t ≈ 6,050, and then falls ever faster: −0.070 at 8,000, −0.123 at 9,000, −0.186 at 9,869, still accelerating. — Study 30 (research record) LV6.
- [NUMERIC] The identity explains all of it: the net source is positive until t ≈ 3,000, then turns negative and grows; the predicted t² coefficient matches the fit (0.96 on the rise, 1.07 over the whole run), with 0 identity failures in 99 checks. — Study 30 (research record) LV6.
- [NUMERIC] From the other package bang (S2*) the same law drifts the other way: U = −0.0368 at t = 1,200 (about −2.6·10⁻⁸·t², 29 bits, bounded), as found before for the FIX-i package. — Study 30 (research record) V1S.
- [DERIVED] Extrapolated, not run: U would reach −0.25 near t ≈ 10,500. — Study 30 (research record) LV6 (post hoc).
- [OPEN] The cause is exact (the k = 0 lapse has no restoring force), but its cure is not: this uniform-lapse drift is the main open stability problem of ONE v1. — Study 24 (research record) §5.5e; Study 30 (research record) LV6, V1S.
- [DERIVED] The strong field departs from GR: the Dirac clock stops at U = 1 (GR: ½), and L0's link factor flips sign at U = ¼. — Study 24 (research record) §5.1c.

### 5.2 The Einstein approximation (Study 28)
- [CHOSEN] The Einstein layer is opt-in and DEFAULT OFF: einstein_system(base) returns its base unchanged unless it is switched on, and after the push the base is ONE v1. — Study 28 (research record) EINF-A signature block, V1.
- [NUMERIC] It is built with NO new gear: the nine idle metric gears take the roles of an integer DeWitt basis (field sign −1 on a3 and on h0i), and two new blocks couple them to L0, einL0 (4,032 terms, rank 3, reciprocal) and einbeta (1,296 terms, rank 3, designated one-way); rank 4, 0 reciprocity violations, no new degree-1 monomial. — Study 28 (research record) A1, A2, A5, A11, A17, B15.
- [THEOREM] The law it adds is the harmonic-gauge (de Donder) wave operator for all ten components on the one cone, with the exact lattice dispersion; the gauge-invariant Fierz–Pauli operator cannot be the law, because it needs edge offsets and an a-read cycle. — Study 28 (research record) A3, A24.
- [THEOREM] Two polarisations hold on constraint-satisfying data, six in general: the board does not impose the harmonic constraint (Box C = 2·div s + ledger, exactly), so sourced waves carry up to six polarisations (two in GR), the extra ones in proportion to the source defect. — Study 28 (research record) A4, A4b, B4, EINF-B verdict.
- [DERIVED] γ = 1 is now derived, given the board reader (h_00 on sites, h_00 + h_dd on links, a CHOSEN board form of ½hT): dust sources only F, so P·h_dd = F = P·h_00, and the link factor 1 − 4U follows from the field equation; inside that form the 1911 value is excluded. — Study 28 (research record) A6, A6′.
- [DERIVED] The DeWitt (ghost) sign makes stressed sources GR-like and isotropic, h_dd/h_00 = (ρ − p)/(ρ + 3p) on every axis; with that sign flipped the response would be anisotropic. — Study 28 (research record) B10, A6′.
- [NUMERIC] Bending and Shapiro delay on the board (pre-registered PASS; L = 56; field built by the board from a static load; test lights reading the full metric against an h_00-only control): delay ratio 2.02–2.06 and bending ratio 2.08–2.16; the excess over 2 is the predicted O(U) term of the built factors. — Study 28 (research record) A8, A8c, B7.
- [NUMERIC] The scope of that test: one-way test lights and a mechanism load; no light of the ONE content reads the metric (E1 is not coupled). — Study 28 (research record) A8 (EINF-B EDIT).
- [DERIVED] β = 1 for L0, for static fields: L0 reads G = F²/(2P) one-way, so −g00 = 1 − 2U + 2U², and the perihelion advance is GR's (ratio 1.0000007), against 4/3 of GR without that read. — Study 28 (research record) A11, A11b, A11′, B6.
- [DERIVED] The diagonal linearised equations: □h̄_μν = −16πG·T_μν holds in the diagonal sector (h̄_00, h̄_dd) on time average, for the dark board L0, with a source that is not conserved. — Study 28 (research record) A21, B13.
- [NUMERIC] A real board source (an L0 lump) gives γ_eff between 0.97 and 1.00 once the uniform modes are removed (reported only; not a far-field test). — Study 28 (research record) A9b.
- [IMPOSSIBLE] A conserved reciprocal source and an exact Bianchi identity stay impossible at any rank (G-NOGO-a; §5.3). — Study 28 (research record) A16.
- [NUMERIC] The measured source defect: the time part is 44–82 % of the source per update and the space part 0.4–1.9 %. — Study 28 (research record) A10.
- [IMPOSSIBLE] Gravitomagnetism felt by second-order matter (h_0i: an a-read cycle) and any off-diagonal h_ij for second-order matter (three nodes in one monomial), at any rank: L0 and light feel no frame dragging. — Study 28 (research record) A13, A14′.
- [CHOSEN] A one-way source of h_0i would be legal; it is simply not built. — Study 28 (research record) A14′.
- [IMPOSSIBLE] The visible doublet at rest reading the lapse covariantly: a rank-5 wall (degree 5 with Θ) in the coupled opt-in; in ONE v1 the covariant composite is rank 4 but grain-blocked at today's integers (6451/2^15 ≈ 0.197 per unit Higgs), and the integral bare-mass dressing breaks SU(2). — Study 28 (research record) A15, V3.
- [IMPOSSIBLE] Spring and plaquette energy as sources (rank 5) and gravitating gauge fields (edge-mode lemma, F-4). — Study 28 (research record) A16, A23.
- [NUMERIC] Universality is L0 only: the visible doublet, E1, the gauge fields, the Higgs and the cosmic block do not read the metric. — Study 28 (research record) A21 (EINF-B EDIT).
- [NUMERIC] Where the layer acts (L = 6, the J-pure seed plus an L0 lump, 400 updates, on both bases) the board stays bounded (24–25 bits) and the rewind is exact; on ONE v1 at L = 4 the J-pure seed stays bounded for 700 updates with the layer idle. — Study 28 (research record) A27, A-V1R-a, A-V1R-c.
- [OPEN] The layer adds two uncompensated uniform drifts (a2, a3), like F4; its ghost-sign gears propagate, with no ghost-specific growth in the verifier's Krein test; lattice-scale resonances stay open. — Study 28 (research record) A20, A22, B5, B12.
- [NUMERIC] The binding long-run limit of any run with L0 matter, with or without the layer, is the base's uniform lapse: in the verifier's test the base without the layer fails first (t = 180, against 487 and 589), the difference being 99.8 % the k = 0 mode before the U > ¼ flip. — Study 28 (research record) B5, EINF-B finding (i).
- [DERIVED] A board prediction that differs from GR: with h̄_0i walled off, two parallel co-moving light beams attract (exchange 2EE′) where GR gives 0, and antiparallel beams get 2EE′ where GR gives 4EE′ (not run). — Study 28 (research record) B14, EINF-B finding (ii).
- [DERIVED] Verdict, signed by both researchers: the board holds Einstein's LINEARISED equations (harmonic gauge, diagonal sector, the dark board L0 only, a non-conserved source); it does NOT hold the full Einstein equations at rank 4, and the missing parts are theorem walls (some at any rank) plus one grain wall. — Study 28 (research record) EINF-A item 8, EINF-B verdict (signed 16:35:57 UTC).

### 5.3 What forbids more (theorems of Rule3 itself)
- [IMPOSSIBLE] G-NOGO-a: no reciprocal (one-potential, b-only) gravity coupling of ANY rank has an exactly conserved source, because Rule3's map a → b′ is onto and no function of b alone is conserved on all orbits; "Newton III exact" and "source conserved" exclude each other. — Study 24 (research record) §5.5a.
- [IMPOSSIBLE] An exact Bianchi identity and an exact Hamiltonian constraint: Rule3's fixed kinetic coefficient D admits no time-dependent gauge symmetry. — Study 24 (research record) §5.5b.
- [THEOREM] What is exact instead: the per-update Gauss/flux identity of the lapse, the k = 0 identity, the Newtonian Bianchi (carrier-number continuity with its ledger), the exchange identity and the shift law. — Study 24 (research record) §5.5c, §6.1.
- [IMPOSSIBLE] Exact rotations SO(3) and exact boosts (the node has 2O, the lattice is cubic); Lorentz symmetry emerges at O(k²) only. — Study 24 (research record) §5.4.

---------------------------------------------------------------------------------------------------------------------
## §6 The cosmic clock and the bangs
### 6.1 The rule and the default
- [CHOSEN] Owner rule (relayed by the manager at about 16:13 UTC): the WIND hand reads no matter, and no matter reads it. — briefs of Study 34 and Study 35 (research records).
- [CHOSEN] The default is ONE v1 = one_system(couple_doublet=False), dynamics fingerprint 77f6d251…: the FIX-i package plus the seven-gear cosmic block; the coupled build (593753fa…) stays an explicit opt-in. — Study 22 (research record) R23; Study 28 (research record) A-addendum 3.
- [THEOREM] ONE v1 is block-diagonal: 0 monomials cross the package/cosmic boundary, so the hand reads no package gear and no package gear reads the hand. — Study 22 (research record) R2, OB2.
- [NUMERIC] The package evolves bit-identically with and without the cosmic block: 20/20 updates at L = 4, and 721/721 bit traces to t = 720 on the J-pure seed. — Study 22 (research record) R2; Study 30 (research record) L4a, L4b.
- [NUMERIC] The cosmic block is its own component of the coupling graph: the hand Θ, two Θ-reading clocks (M1, M2; called "cosmic matter" in the records), two static Born loads and the matched choice pair (dp, dm). — Study 22 (research record) R1, R3; Study 26 (research record) A4.
- [OPEN] Those two Θ-reading clocks belong to the clock itself (the light whose intensity drives the choice pair); whether the owner's rule is meant to cover them is for the owner to say. — Study 22 (research record) R3, OB10.
- [DERIVED] Why the hand is separate: gravity's uniform (k = 0) mode has no restoring force, and a spring on it would screen gravity beyond about five sites, so the cosmic clock needs its own γ = 0 hand. — Study 24 (research record) §9.3.
- [NEW LAW] WIND (approved, in ONE v1): a per-node hand Θ with no bare spring, whose stiffness comes from the matched-pair choice record Δ, Δ(t+1) + Δ(t−1) = ℓ+ − ℓ−; a turn comes when ∫Ω_eff dt = π/2. — Study 24 (research record) §9.3.
- [THEOREM] The hand reads b-values (Δ), never a remainder: legal and not circular. — Study 24 (research record) §9.3 (X20).

### 6.2 The cosmic clock, measured
- [NUMERIC] ONE v1 at L = 6 from the J-pure seed: turns (hand zeros) at t = 96, 289, 481, 672, 863, 1054; bounded for 1,200 updates (25 bits); the rewind of all 1,200 updates is exact across the six turns. — Study 22 (research record) R8, R9, R18, R19.
- [CHOSEN] The ~192-update aeon is an input: g_w = 1310 was chosen for a quarter period of 100 at L = 6; the runs check the period, they do not predict it. — Study 22 (research record) A-1 (declaration 1 of the package notes NOTES_one.md).
- [NUMERIC] The period scales as √(number of nodes), as derived before the runs: the first zero (a quarter period) comes at 52.35 for L = 4 (ONE v1) and at 148.6 for L = 8 (coupled run), against 52.42 and 148.3 predicted; the L = 4 intervals are 104.7–105.6 against 104.67. — Study 30 (research record) A1.
- [NUMERIC] ONE v1 has no runaway in what could be run (9,869 updates at L = 6 from J-pure, 1,200 at L = 6 from S2*, 1,998 at L = 8), far past the coupled build's runaway at t ≈ 1,554; but it is not quiet: E1, β and the metric grow slowly (pre-registered 4-bit onsets at t = 2,621, 2,931 and 6,752), E1 reaches the 32-bit bound by t ≈ 8,000, and the uniform lapse is not small (§5.1). — Study 30 (research record) LV6, V1S, LV8.
- [NUMERIC] The hand keeps turning on ONE v1: 33 turns to t = 6,300 at L = 6, intervals 186–193. — Study 30 (research record) R4.
- [NUMERIC] The rewinds of the two long ONE v1 runs (6,300 and 1,200 updates on Python integers) were stopped before they finished, so their exactness is not determined; every rewind that did finish was exact (ONE v1 for 1,200 updates at L = 6 and 720 at L = 4; the coupled build across its runaways). — Study 30 (research record) R4, V1S, L4b; Study 22 (research record) R18.

### 6.3 The rejected coupling runs away
- [NUMERIC] The coupling in which the doublet reads the hand (C1, fingerprint 593753fa…) runs away: at L = 6 it stays at 24 bits to t = 1530, then the Higgs (chiral) sector grows first and the board reaches 433 bits at t = 1554; at L = 4 it runs away at t = 662–667. — Study 30 (research record) R1, D1, L4c.
- [NUMERIC] On the same L = 4 seed, the package alone and ONE v1 stay at 29 bits to t = 720: the runaway is caused by the coupling. — Study 30 (research record) L4a, L4b.
- [NUMERIC] Across the runaway the rewind is exact (1,554 updates) and every ledger is 0: an exact bijection can still run away. — Study 30 (research record) R1.
- [DERIVED] The mechanism, identified after the runs (post hoc): a forced, non-resonant 1:1 pumping of the Higgs by the sign-changing Θ factor on the Yukawa and doublet terms, against the unscaled Higgs spring, ending in the quartic blow-up (not a 2:1 parametric resonance); in ONE v1 the Higgs level instead saturates. — Study 30 (research record) PC.
- [DERIVED] So "exact" is not "bounded": the ten checks are kinematic, and only the all-k scan and long runs speak about stability. — Study 24 (research record) §3.7 (X22).

### 6.4 A generic clock law (Study 34)
- [CHOSEN] The question: can a cosmic turn reach all matter through time itself, one universal rule acting on every clock as the lapse does, with no matter gear reading the hand? — brief of Study 34 (research record).
- [NEW LAW] CG1, built and default OFF: the hand drives the uniform lapse additively, through ONE designated one-way monomial per node, u[h00] += κ·Θ (rank 2, on-site); no package matter gear reads Θ (the clock's own M1, M2 still do). — Study 34 (research record) A1 and its CLK-B mark.
- [THEOREM] Such a coupling must be one-way: a reciprocal Θ–F coupling would put an additive source into the hand's input, which THEOREM O forbids. — Study 34 (research record) A2.
- [THEOREM] Through the lapse a turn reaches matter only as a common clock-rate (redshift) modulation, never as an echo or a bang of matter: the lapse factors are affine and keep their sign for U < ¼. — Study 34 (research record) A3, B4.
- [NUMERIC] "Every clock feels each turn" is false: su2, su3, u1, bgk, the choice observers and nine metric gears are not downstream of the hand; under a uniform lapse only L0's own rest clock changes (48 of 48), the doublets' rest clocks do not (0 of 16, hop rows only), and the Higgs, the weak links, E1 and β change by 0. — Study 34 (research record) B4, A6, A13.
- [NUMERIC] CG1 is lawful and exact (2,000-update rewinds at L = 4 for both drive sizes; the cosmic block bit-identical to ONE v1 at every update), but it cures nothing: it adds a bounded swing and no restoring force, and the uniform lapse keeps growing (L = 6: 5.94·10⁻³ against 7.15·10⁻³ at t = 2,000). — Study 34 (research record) A4, A5, A7, A8, B2, B3.
- [IMPOSSIBLE] The multiplicative law CG2 (u[h00] += Θ·F, rank 3) at today's hand scale 2^24, for every integer κ ≥ 1: the k = 0 mode is Mathieu-unstable (|U| grows about 8-fold per hand period), and the board runs away (Higgs first, t ≈ 1,124 at L = 4). — Study 34 (research record) A10, B5.
- [DERIVED] A Θ·F term pumps or holds only the k = 0 mode (a Kapitza spring; every k ≠ 0 lapse mode is adiabatic), so it screens no gravity. — Study 34 (research record) A11.
- [CHOSEN] The owner approved (17:00 UTC) a hand scale of 2^21 instead of 2^24, picked to put CG2 inside its stability window at L = 6; the M1/M2 hop h = 2^10 then follows. — Study 34 (research record) A18, B8.
- [NUMERIC] That constant change alters the cosmic clock itself: the 2^21 hand's turn intervals drift from 193 to 178 updates by t ≈ 8,800, with or without CG2, while the 2^24 hand stays at 186–193. — Study 34 (research record) A19′, B8, CLK-B L6LONG.
- [NUMERIC] Inside that window CG2 holds the uniform lapse at L = 6 (J-pure): max U ≈ 7.6·10⁻⁴ near t = 955 with a slow period of about 1,600, against ONE v1's monotone 7.1·10⁻³ by t = 2,000; reproduced in two codes and at two grains, with exact rewinds of 400 updates (L = 6) and 1,000 (L = 4). — Study 34 (research record) A12, B6.
- [NUMERIC] The composed law (one_system_clock, CG2 at 2^21) at L = 6 (J-pure, run to t = 8,900): bits 29–31 and 0 identity failures, and the uniform lapse stays within |U| ≤ 4.1·10⁻³ while ONE v1 goes to +0.024 and later to −0.070; the hold lasts into v1's sign-changed phase as far as the run goes (beyond t = 8,900: OPEN), but the pre-registered bounds (1.5·10⁻³ and 3·10⁻³) fail as worded. — Study 34 (research record) A19, A21′, CLK-B L6LONG.
- [NUMERIC] Its rewinds are exact wherever they were run: 400 and 1,200 updates at L = 6, 1,000 and 2,000 at L = 4. — Study 34 (research record) A23, A24, B6.
- [NUMERIC] Inside that window every lapse READER feels each turn as a common clock-rate (redshift) pulse: L0's own rate, the doublet's hop (not its rest clock), and E1's source dressing and β only through products with other excited fields; the non-readers never feel it (su2, su3, u1, the choice observers, bgk, the free metric gears: 239 package gear types) — "everything" was withdrawn as an overclaim. — Study 34 (research record) A21′, B4.
- [NUMERIC] From the S2* bang, where ONE v1 drifts fastest (U = −0.0368 at t = 1,200, accelerating), CG2 at 2^21 turns the lapse around (largest |U| = 0.0197 near t = 1,004, then −0.0136 at 1,200); the pre-registered bound fails as registered, "bounded" is shown only to t = 1,200 on one seed, and the rewind of all 1,200 updates is exact. — Study 34 (research record) A23, A24 and their CLK-B marks.
- [NUMERIC] At L = 4 the same law is a weak spring: it halves the excursion of the uniform lapse (−0.0295 against ONE v1's −0.0627 at t = 2,000) but has not yet turned it, so "bounded" is not shown there; the rewind of all 2,000 updates is exact. — Study 34 (research record) A24.
- [NUMERIC] The window closes with size: q_M grows with the number of nodes, and at L = 8 the same law PUMPS the uniform lapse (extrema of alternating sign growing 6–7-fold per hand period); each hand scale has a largest safe board (2^21: L ≤ 6; 2^20: L ≤ 8; 2^19: L ≤ 10). — Study 34 (research record) B7, A20.
- [CHOSEN] Safe as the default: NO, in both researchers' words (size wall, seed dependence, weak sources only, bounds not met as registered, a changed cosmic clock, and M1/M2 left to the owner). ONE v1 stays the default (manager decision, 17:15 UTC); CG2 at 2^21 is an explicit opt-in NEW LAW candidate, default OFF, used only inside its stated validity window (L ≤ 6, A_c ≥ 840, Θ0 = 2^21). — Study 34 (research record) A20, CLK-B SAFE AS DEFAULT.
- [NUMERIC] It does not hold an L0 lump either: that board still blows up (t ≈ 330, against 274 without the law). — Study 34 (research record) A17.
- [IMPOSSIBLE] "Every clock reads the lapse" at rank 4: lapse-dressing a quartic potential is rank 5, and an exact dressing of most coefficients is also grain-blocked at P = 2^20; the doublet's rest clock is degree-legal but costs SU(2) at O(U) (OPEN, not built). — Study 34 (research record) A13 and its CLK-B mark.
- [IMPOSSIBLE] The GR second-order completion of the lapse factors, which would make the k = 0 source self-limiting, at today's P and Q (it needs P ≤ 2^16 or Q − 1 ≥ 2^41). — Study 34 (research record) A15.
- [CHOSEN] The clock's own Θ readers M1 and M2 are acceptable only if the owner classifies them as clock parts; driving the choice pair by an existing clock's intensity is a NEW LAW candidate, not built; turning the hand by the lapse, or by direct reads of remainders or clicks, is impossible. — Study 34 (research record) A14 and its CLK-B mark.
- [DERIVED] Verdict, signed by both researchers (no DISAGREE): a generic clock law that reaches EVERY clock does not exist at rank 4; through time a cosmic turn is only a universal change of clock rate (a redshift pulse) for the clocks that read the lapse, and it never folds or echoes matter. What exists is an opt-in NEW LAW, CG2 at the owner-chosen hand scale 2^21 (one designated monomial per node, no matter gear reading the clock): it holds the uniform lapse at L = 6 (one seed per bang, to t = 8,900), only halves its excursion at L = 4 within 2,000 updates, pumps it at L = 8, and does not hold an L0 lump; ONE v1 stays the default. — Study 34 (research record) A20, A21′, A24, both signature blocks (CLK-B 17:41:44, CLK-A 17:42:27 UTC).

### 6.5 One exact bang, information, and the turns
- [THEOREM] THEOREM D: two exact symmetric moments make a history periodic, so a growing history has at most ONE exact bang. — Study 24 (research record) §4.9, §9.2.
- [NUMERIC] The one exact bang: the CPT reversor R* is exact along the ONE seed (0 mismatches for t = 1…10 at L = 4 and 6, on both package bangs); the past is the CPT image of the future. — Study 22 (research record) R6; Study 24 (research record) §9.2.
- [THEOREM] THEOREM N: the choices time the turns and never cause a bang. — Study 24 (research record) §9.3 (X11).
- [THEOREM] THEOREM O: an interacting composition never folds exactly, so every later turn is at best an approximate echo. — Study 24 (research record) §9.4.
- [NUMERIC] Echo distances are kept as data, not as a target (cosmic matter 0.016–0.047 near twice the turn time). — Study 22 (research record) R9.
- [CHOSEN] No new seed is injected: each later turn simply starts from the state at the turn, with all its records; nothing is reset, posted or tuned. — Study 24 (research record) §9.3 (owner decision O2).
- [THEOREM] THEOREM K: |K(X_t) − K(X_0)| ≤ 2·log2 t + O(1), so the board's information is law + seed + log t. — Study 24 (research record) §9.5.
- [NUMERIC] What grows is the click record: each aeon adds about 80 kB of new zlib-incompressible pair-outcome record (80.1–81.6 kB), at least 99.4 % of its entries new, flat per aeon, with all turn states distinct. — Study 22 (research record) R12, R20; Study 30 (research record) R1, R2a.
- [DERIVED] That record is written by Rule3 from data already in the seed: it is new to a reader without the seed, not new to the board (THEOREM K). — Study 24 (research record) §9.3, §9.5.

---------------------------------------------------------------------------------------------------------------------
## §7 Quanta and Bell
### 7.1 One click per quantum, Born exact
- [THEOREM] The Born count: for 0 ≤ K < D, #{r ∈ Z_D : K + r ≥ D} = K, so a uniform remainder carries with probability exactly K/D; with inputs proportional to |ψ|² this is the Born rule. — Study 24 (research record) §4.6.
- [THEOREM] The link chooses: one shared remainder overflows exactly once, so P(both) = 0. — Study 24 (research record) §4.6, §8.
- [NUMERIC] In ONE v1 the Born ledger is exact for every pair, with maximal deviation 3.2·10⁻⁷ over 216 nodes and 2.66·10⁹ events. — Study 22 (research record) R12.
- [THEOREM] Odd-Q parity: no carry event has probability exactly 1/2. — Study 24 (research record) §4.6.
- [OPEN] Freshness: Born is exact only for a fresh uniform remainder; re-reading one circle gives Fréchet joints and Sturmian noise. — Study 24 (research record) §4.6 (X10).

### 7.2 The owner's rule for the path, and Bell (Study 27)
- [CHOSEN] The owner's rule: all paths exist on the board; the receiving click closes the path back to the emitting click; only the confirmed path clicks; there is no freeze. — brief of Study 27 (research record).
- [DERIVED] The rule as a law with no freeze (LAW O): the quantum is an exact wave on every path with total intensity ΣK = D, carrying the emitting click's token (a common-past datum loaded into the detectors' vacuum remainders and never read); a detector carries when its loaded remainder plus its input reaches D; the exact inverse is the backward trace. — Study 27 (research record) X1.
- [THEOREM] Every reading of "the path goes back from the receiving click to the emitting click" is one of four types: a re-description (rewind, retrodiction), a selection of seeds by future clicks, a forward signal inside the cone, or a hidden time; the last needs a freeze or a second board and is excluded. — Study 27 (research record) Y1, X1 (EDIT).
- [THEOREM] The backward trace exists for every history and selects nothing; it runs from the final FULL state, since the clicks alone do not fix the seed (r mod 2 is inert). — Study 27 (research record) X2 (EDIT), Y3.
- [NUMERIC] One quantum, exact, with no freeze: one emission click and exactly one absorption click for each of 15 token values (left 3, right 12, none 0, double 0), so Born gives 1/5 and 4/5 exactly; the rewind is exact in 15 of 15. — Study 27 (research record) X3.
- [NUMERIC] Each click depends only on its own path back to the emitting click (936 single-entry seed perturbations per token, 0 cone violations); "the light chooses the path that is going to be" is the emitting click's token, a local hidden variable, enough for one quantum. — Study 27 (research record) X4, X5.
- [NUMERIC] The Bell pair with no freeze, exact over all 1,296 analyser choices and over the whole seed class (about 1.3 million full-board runs): independent path tokens give S = 5/4; one shared path token gives at most 2 (Clauser–Horne J_max = 0); the dynamical one-click router ("only the confirmed path clicks" built into the dynamics) gives exactly 2; δ = 0 and the far-setting marginal shift is 0 in every design. — Study 27 (research record) X7, joint answer.
- [THEOREM] With no freeze and a typical seed, Bell holds: click time = board time keeps each record inside its own past cone, and fresh chooser remainders give measurement independence (δ = 0), so S ≤ 2 at spacelike separation. — Study 27 (research record) X8 (1), (2), Y5.
- [NUMERIC] S > 2 appears only by selection. If the observer discards unconfirmed single clicks (the detection loophole) the board gives 22/9, or 2.4677 on the verifier's board, under the tight frontier S ≤ 2/p; scored over all pairs, as loophole-free experiments score them, it gives J ≤ 0 exactly. — Study 27 (research record) X10, X8 (4), joint answer.
- [NEW LAW] The owner's rule taken as a law on seeds ("only histories whose clicks are confirmed under their actual settings exist") gives S = 271800/110143 = 2.4677 at D = 30 (2.514 in the continuum) with every trial confirmed and no click discarded. — Study 27 (research record) X8 (EDIT), Y7.
- [DERIVED] Its price: measurement independence breaks (δ = 0.28 on that board, 4/9 on the builder's; at least 0.138 for 2√2), the allowed seeds weigh 0.544^N over N trials, the correlation curve is wrong (E(0) ≈ 0.83 instead of 1 on the verifier's board; −1/9 instead of −1 at 90° on the builder's), detectors must be 100 % efficient (no miss can exist under that law), and no-signalling holds only by detector symmetry (asymmetric exits signal 0.147, faster than light under that law). — Study 27 (research record) X11, Y7, Y10, joint answer.
- [THEOREM] On this bijective board a two-time boundary, a retrocausal selection and a superdeterministic seed are one object (pullback), so the lawful door to S > 2 is a seed law, i.e. superdeterminism. — Study 27 (research record) X14, Y2.
- [THEOREM] It is fine-tuned: any seed law reaching 2√2 over N trials has natural measure ≤ e^(−0.0214·N) (Azuma–Hoeffding); i.i.d. Tsirelson records need ≥ 0.046 bits per trial of seed–setting information; an all-or-nothing confirmation with fair rate p has S ≤ 2/p, so 2√2 needs ≤ 2^(−N/2) of the seeds. — Study 27 (research record) X12 (EDIT), Y8.
- [THEOREM] Tsirelson's 2√2 is derived in NO reading (selection reaches 4; the natural rule gives 2.514 with the wrong curve), and no-signalling is a theorem of the law in no reading with S > 2. — Study 27 (research record) X13, Y9.
- [IMPOSSIBLE] A forward confirmation without a freeze cannot give a spacelike violation: confirmed records wait, visibly, and are timelike to the far setting; it fails against tests whose timing margin exceeds the board cone's 1.73. — Study 27 (research record) X15 (EDIT), X17, Y6.
- [DERIVED] Verdict, signed by both researchers: one quantum works exactly as the owner says, with no freeze; but with no freeze and a typical seed Bell's quantum violation does NOT stand on the board (S ≤ 2 exactly); the only lawful door is a fine-tuned seed law (superdeterminism) with no no-signalling theorem and no Tsirelson; the push gate "Bell stands" is not met. — Study 27 (research record) joint answer (BELL-X 17:08:24, BELL-Y confirmed 17:09:03 UTC).

### 7.3 What is fixed independently of Study 27
- [THEOREM] Tsirelson's 2√2 follows from four declared reader laws (one-way, amplitude-only, fresh Born, setting-free average); breaking one gives a PR box or signalling, so 2√2 is not a board theorem. — Study 20 (research record) ZB9 (T4).
- [THEOREM] Over ALL seeds S = 4 is reachable (choose a final full state with the wanted records and rewind it to its seed), so a law on seed data predicts nothing by itself. — Study 24 (research record) §8 (X25); Study 14 (research record) B4.
- [IMPOSSIBLE] True entanglement and the exchange sign (Pauli) on one board: they need configuration space (×1.26·10⁷ per added quantum at L = 64) or orbital copies, both NEW LAW. — Study 24 (research record) §7.6; Study 16 (research record) Z8.

---------------------------------------------------------------------------------------------------------------------
## §8 The owner's addition: a choice for every click
- [CHOSEN] The owner's addition, recorded as his: "there is a choice for the click, so the universe is not deterministic"; this is where he parts from 't Hooft's deterministic cellular automaton.
- [THEOREM] Board fact 1: no monomial reads a remainder, so a choice pair's remainder (its token) enters only its own divmod: no other gear depends on it, and its starting value is seed data that nothing on the board fixes. — Study 24 (research record) §1.8.
- [THEOREM] Board fact 2: a matched pair obeys Δ(t+1) + Δ(t−1) = ℓ+ − ℓ− = I, so the history reads how many choices were made, never which way they went. — Study 22 (research record) R13; Study 24 (research record) §6.2.
- [NUMERIC] Board fact 3: re-drawing the free data (tokens and Born loads) changes 98.2 % of the outcomes and leaves the hand, the cosmic matter, Δ and every package gear bit-identical for 1,200 of 1,200 updates. — Study 22 (research record) R13.
- [NUMERIC] The same in the coupled run: 98.25 % of the lit outcome entries differ, and the hand, the matter, the package and Δ are identical at every one of 1,200 updates. — Study 30 (research record) R2a.
- [THEOREM] Board fact 4: given those data, Rule3 is an exact bijection, so law + seed fix every outcome (THEOREM K). — Study 24 (research record) §1.3, §9.5.
- [THEOREM] Precisely which way the bijection runs: the final FULL STATE (a, b, r) ↔ the seed (exact bijection); the click record alone does not determine the seed, because K is even, so r mod 2 never changes and never moves a carry: a seed and its parity-flipped copy give identical a, b and clicks. — Study 24 (research record) §1.3, §1.6; Study 27 (research record) Y3, X2.
- [DERIVED] So the board's "choice" is exactly this: the outcome data are free (nothing else on the board fixes them and nothing else depends on them), and once they are given nothing is left undetermined.
- [DERIVED] The board cannot tell the two readings apart: every final full state comes from exactly one seed, and the clicks do not even fix that seed, so "chosen at the click" versus "written in the seed" is a reading, not an observable.
- [DERIVED] The difference from 't Hooft (literature, from memory): in his automaton everything, settings included, is fixed by the initial state, and Bell violations come from correlations in that state (superdeterminism); here the choice data are free and uncorrelated with the settings, which keeps measurement independence, and that is exactly why the board obeys Bell's bound (§7); Study 27 maps his automaton onto the seed-law reading. — Study 27 (research record) Y11.
- [NEW LAW] The 't Hooft route on this board would be a seed law correlating the emission data with the future settings; its price is given in §7.2.

---------------------------------------------------------------------------------------------------------------------
## §9 Solved, approximate, impossible, open: one table
| # | item | where it stands | label | § |
|---|---|---|---|---|
| T1 | Exact reversibility: Rule3 is a bijection with a staged inverse; rewinds exact across every turn and through a runaway | SOLVED, exact | THEOREM | §2.2 |
| T2 | Every gear is a clock (cos w = μ/2); a click is a carry; the per-gear ledger | SOLVED, exact | THEOREM | §2.3, §2.4 |
| T3 | Strict locality (node + six faces) and the board cone; board-causal no-signalling | SOLVED, exact | THEOREM | §1.1 |
| T4 | The rank-4 recipe; rank = degree of Φ; one unified link per face per multiplet | SOLVED | THEOREM | §1.3, §3 |
| T5 | One cone, c_Q² = (Q − 1)/(3Q), for metric, E1 and L0 transport (given the common stencil) | SOLVED, exact | THEOREM | §1.3 |
| T6 | Exact lapse factors in the tensor (clock 1 − 2U, link 1 − 4U); EP of the factor; Newton III for the reciprocal lapse terms | SOLVED, exact | THEOREM | §5.1 |
| T7 | The Born count K/D; one click per shared remainder | SOLVED, exact (given a fresh remainder) | THEOREM | §7.1 |
| T8 | One quantum along the owner's path rule, with no freeze: one emission click, one absorption click, Born exact, the click depending only on its own path back to the emitting click | SOLVED on the board | NUMERIC | §7.2 |
| T9 | One exact CPT bang; information = law + seed + log t; the choices time the turns and never cause a bang | SOLVED, exact | THEOREM | §6.5 |
| T10 | The history does not depend on the click outcomes (the owner's "choice" as free data) | SOLVED on the board | NUMERIC | §8 |
| T11 | Weak-field metric with γ = 1; Newtonian limit (Poisson, V = −mU); redshift z = ΔU | APPROXIMATE: continuum, first order in U | DERIVED | §5.1, §5.2 |
| T12 | Bending and Shapiro delay at twice the Newtonian value | APPROXIMATE: measured on the board with test lights; the excess over 2 is the predicted O(U) term | NUMERIC | §5.2 |
| T13 | PPN β = 1 (L0, static fields, one-way U² read) | APPROXIMATE: second order, static only | DERIVED | §5.2 |
| T14 | Linearised Einstein equations: harmonic gauge, diagonal sector, dark board L0, time average | APPROXIMATE: opt-in layer, default OFF | DERIVED | §5.2 |
| T15 | Lorentz symmetry; EP of observed tick rates | APPROXIMATE: O(k²); first order in U and w0 → 0 | DERIVED | §5.1, §5.3 |
| T16 | Later bangs | APPROXIMATE echoes only, kept as data | NUMERIC | §6.5 |
| T17 | Masses: forms (multiplets, pairings, lattice ladders) forced; values put in | values are DATA | DATA | §4 |
| T18 | An exactly conserved reciprocal gravity source (G-NOGO-a), at any rank | IMPOSSIBLE | IMPOSSIBLE | §5.3 |
| T19 | An exact Bianchi identity or Hamiltonian constraint, at any rank; hence the full Einstein equations | IMPOSSIBLE | IMPOSSIBLE | §5.3 |
| T20 | Felt gravitomagnetism (h_0i) and off-diagonal stress (h_ij, i ≠ j) for second-order matter | IMPOSSIBLE | IMPOSSIBLE | §5.2 |
| T21 | The visible doublet at rest reading the lapse covariantly | IMPOSSIBLE: a rank-5 wall in the coupled opt-in, a grain wall at today's integers in ONE v1 | IMPOSSIBLE | §5.2 |
| T22 | Exact SO(3) and exact boosts | IMPOSSIBLE (emerge at O(k²)) | IMPOSSIBLE | §5.3 |
| T23 | A freeze or hold generated by the tensor, at any rank | IMPOSSIBLE (as the owner requires) | IMPOSSIBLE | §2.5 |
| T24 | An exact later bang (a second exact symmetric moment) | IMPOSSIBLE in a growing history | IMPOSSIBLE | §6.5 |
| T25 | Spacelike S > 2 with free choosers and no freeze | IMPOSSIBLE without a seed law | IMPOSSIBLE | §7.2 |
| T26 | Tsirelson's 2√2 as a board theorem | IMPOSSIBLE: it follows only from declared reader laws | IMPOSSIBLE | §7.3 |
| T27 | True entanglement and the Pauli sign on one board | IMPOSSIBLE (NEW LAW needed) | IMPOSSIBLE | §7.3 |
| T28 | Freshness of the remainder (Born exact only for a fresh one) | OPEN | OPEN | §7.1 |
| T29 | The long-time fate of the uniform lapse (on the longest ONE v1 run it rose to U = +0.024, crossed 0 and fell to −0.186 by t = 9,869, still accelerating; the exact identity explains every step) | OPEN | OPEN | §5.1, §6.2 |
| T30 | The doublet's EP debt under FIX-i (it neither feels nor sources the lapse) | OPEN | OPEN | §5.1 |
| T31 | Radiative gravity (emission by the board's own matter, back-reaction); the layer's two new uniform drifts; lattice-k Krein resonances | OPEN | OPEN | §5.2 |
| T32 | A generic clock law reaching all matter without matter reading the hand (Study 34) | IMPOSSIBLE at rank 4 (a turn reaches only the lapse readers, and only as a redshift); an opt-in law (CG2 at the owner-chosen 2^21) holds the uniform lapse at L = 6, halves it at L = 4 and pumps it at L = 8 | IMPOSSIBLE | §6.4 |
| T33 | Masses out of the clicks with no mass put in (Study 35) | by itself only the nine dark lattice-scale levels (eight visible) and 0; every visible or light mass value and every ratio is data | DATA | §4.2 |
| T34 | The lattice scale in physical units (it sets the size of every lattice-scale prediction) | an input | DATA | §10 |

---------------------------------------------------------------------------------------------------------------------
## §10 Outlook
- [DERIVED] Told through its clocks, Universe24 is one exactly reversible clockwork: one integer law, one fixed rank-4 tensor and one seed give the clocks, the clicks, the ledgers, the Born counts, one cone, the weak-field metric with γ = 1 and one exact bang, with nothing posted, tuned or frozen.
- [CHOSEN] Its numbers are put in: d = 3, L, Q, the integer weights, the Yukawa integers, the seed and the time scale of the cosmic clock; what comes out are forms.
- [IMPOSSIBLE] "Exactly nature" is blocked within today's framework by theorems: Rule3's fixed kinetic coefficient forbids a conserved reciprocal gravity source and an exact Bianchi identity, so the full Einstein equations are absent; and with free choosers and no freeze the board keeps Bell's bound, so the measured quantum violations are absent unless a fine-tuned seed law is added.
- [OPEN] "Nature could work like this" needs one confirmed new prediction: an effect the board makes without tuning and standard physics does not make.
- [DERIVED] Candidate 1, subluminal high-energy dispersion: every one-cone wave has group velocity below c_Q (the k⁴ term is negative in every direction), the shortfall largest along the cube axes and almost zero along the body diagonals; its clock analogue is the lattice-scale redshift departure δ/U → −w0²/12 (L0) or −w0²/3 (Dirac). — Study 24 (research record) §5.1a, §5.3e.
- [DERIVED] Candidate 2, no force-mediated proton decay: matter and antimatter counts are separately exact at the linear level, and the Pati–Salam ceiling (keeping J′, a choice) has no gauge-mediated proton decay. — Study 11 (research record) row 13; Study 12 (research record) A7; Study 24 (research record) §7.3.
- [DERIVED] Candidate 3, a forced right-handed neutrino: every first-order matter field is a Dirac pair carrying both hands, so ν_R exists; its realistic masses still need a Majorana NEW LAW (Pati–Salam gives M_νD = M_u). — Study 26 (research record) T7; Study 12 (research record) A6; Study 16 (research record) B19 (families).
- [DERIVED] Candidate 4, gravitational action = reaction is not exact together with a conserved source (G-NOGO-a): either a gravity coupling is one-way or its source is not conserved (the one-time source swings at twice the clock frequency), so some active gravitational mass must differ from its passive mass or vary in time. — Study 24 (research record) §5.5a; Study 28 (research record) A10.
- [DERIVED] Candidate 5, in principle only: co-moving parallel light beams attract on the board and not in GR (exchange 2EE′ against 0); the effect is far below any foreseeable measurement (an order-of-magnitude remark, not a record). — Study 28 (research record) B14.
- [DATA] The size of every candidate in physical units needs the lattice scale, which is an input: the records fix signs and forms, not sizes.
- [OPEN] None of the candidates is confirmed; until one is, the board is a model that reproduces much of physics in form, by exact integer identities, and it should be read as that.

---------------------------------------------------------------------------------------------------------------------
## Records used
| record | what it holds | sha256 prefix (as read) | label |
|---|---|---|---|
| Study 24 (research record): THE_ALGEBRA | the law, the node, the recipe, the clocks, §5 Einstein, conservation, quanta, bangs, audit (frozen 15:45:34 UTC; section numbers as in this folder's copy) | 4923e1fdce440796 | NUMERIC |
| Study 22 (research record): AGREE_ONE | ONE v1 and the coupling option, runs T1–T4, C1, C2 (signed 15:30–15:31 UTC) | 7c28128baf0ae381 | NUMERIC |
| Study 23 (research record): AGREE_R5 | rank 5 considered and rejected; no hold at any rank (signed 15:22 UTC) | 2affbb05cb9e028e | NUMERIC |
| Study 26 (research record): AGREE_CH | channels, census of ONE v1, forced block sizes, ν_R (signed 15:20 UTC) | 90b3e30ec3bf0c9f | NUMERIC |
| Study 21 (research record): AGREE_MASS | masses as clock rates; forms forced, values data; Koide (signed 14:27 UTC) | 04b4c89298660b19 | NUMERIC |
| Study 20 (research record): AGREE_ZT | the zero-time hold; Tsirelson from four reader laws (signed 14:36 UTC) | 49336fa86e253d12 | NUMERIC |
| Study 14 (research record): AGREE_BELL | the cosmic clock and Bell; the superdeterminism door (signed 13:48 UTC) | bb860211f6467cda | NUMERIC |
| Study 16 (research record): AGREE_EN, AGREE_FA | entanglement on one board; families and the Pati–Salam mass relations | 4cff35a08a654487, 161b21f413f19bcf | NUMERIC |
| Study 11 (research record): AGREE_CL3; Study 12 (research record): AGREE_GU1 | matter/antimatter counts, no gauge proton decay, ν_R forced (conditional on the chosen framework) | 14a17bd3c4e59f3b, b5c064a4c4518d03 | NUMERIC |
| Study 30 (research record): ONE-LONG notes, results and run files | long runs of the coupled build and of ONE v1 (single researcher; NUMERIC only) | 05db243d845d440f (notes), c634656955bd0983 (results, final 17:07 UTC) (results) | NUMERIC |
| Study 27 (research record): AGREE_B27 | Bell on the board, the owner's way, no freeze | 511b2670bec12dcf (final: BELL-X 17:08:24, BELL-Y 17:09:03 UTC; note 17:09:45) | NUMERIC |
| Study 28 (research record): AGREE_EINF | the linearised Einstein layer, default OFF | 05aa85746baa7871 (signed 16:35:57 UTC) | NUMERIC |
| Study 34 (research record): AGREE_CLK | a generic clock law | 583d3a49acf7063c (signed: CLK-B 17:41:44, CLK-A 17:42:27 UTC) | NUMERIC |
| Study 35 (research record): AGREE_MASS2 | masses out of the clicks | 714e7643be34834e (closed on both sides 17:06:16 UTC) | NUMERIC |
| briefs of Study 27, Study 34, Study 35 (research records) | the owner's rules as relayed (path rule; matter never reads the hand) | c4792428d76880e7, 20f3f57f9cf403f8, 0cce63a23369db6a | CHOSEN |
