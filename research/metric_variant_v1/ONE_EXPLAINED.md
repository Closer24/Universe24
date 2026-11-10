# The ONE version explained: the local node, the full algebra, the clocks, the seed and the tensor

This page is the long version of the ONE-version sections of the [root README](../../README.md). It describes the
candidate variant `metric_variant_v1` as of 2026-11-10. It is a research record, not a physical claim. The reference
engine in [`universe24/`](../../universe24/) is unchanged; this package departs from [AGENTS.md](../../AGENTS.md) only in
its own declared layers (items 1, 2, 4, 5, 6 and 8; see [README_v1_draft.md](README_v1_draft.md)).

The final synthesis of the whole picture is
[full_picture_2026-11-10/FULL_PICTURE_FINAL.md](full_picture_2026-11-10/FULL_PICTURE_FINAL.md) (Study 36); start there.

Sources, all in this directory: the signed
[THE_ALGEBRA.md](full_picture_2026-11-10/THE_ALGEBRA.md) (Study 24), the signed
[CHANNELS.md](full_picture_2026-11-10/CHANNELS.md) (Study 26), [NOTES_one.md](NOTES_one.md) (Study 22), the stability
record [AGREE_STAB_2026-11-10.md](AGREE_STAB_2026-11-10.md) (Study 18), and [README_v1_draft.md](README_v1_draft.md).
Where they differ, README_v1_draft.md and the code govern.

Labels, one per claim: **THEOREM** (proved from the law), **NUMERIC** (an exact integer computation), **DERIVED** (a
short argument from those), **CHOSEN** (an input, a convention or data), **NEW LAW** (an extension that changes the law's
content and needs an explicit owner decision), **OPEN** (not established).

Names such as "light", "gravity", "matter", "Higgs" or "cosmic clock" are labels on tensor blocks and states, not
identifications with physical particles or fields. `Q` here is the divisor scale (`D = 6Q`); it is unrelated to the
signed account `Q` of AGENTS.md item 12, and neither is established physical energy.

## The local node

**Reference engine** ([AGENTS.md](../../AGENTS.md), [model](../../docs/MODEL.md)): one elementary node per site of the
periodic cube `(Z/LZ)^3`, `L >= 3`, with one board of 48 channels indexed by 2O. Every channel stores `(a, b, r)` with
`0 <= r < 6`, receives exactly six face inputs, and is coupled through the fixed 2O body actions `(0, 1, 3)` and three
preselected body-axis signs.

**ONE version.** Every site holds the same list of gears, each a triple `(a, b, r)` with `0 <= r < D`, `D = 6Q`
[CHOSEN]. The count is 382 gear types per node in ONE (375 in the package default, 444 with route B) [NUMERIC]:

| sector | gears | of which |
| --- | --- | --- |
| dark board L0 | 48 | one per element of 2O |
| Dirac matter pairs | 32 | matter 16 + matter2 16 (one lepton-like weak doublet) |
| Θ-reading cosmic gears | 2 | M1, M2: apart from the hand itself, the only readers of the hand |
| gauge-layer test scalars | 12 | su2 4, su3 6, u1 2 |
| Higgs | 4 | one quaternion |
| links (one per face, three faces per node) | 87 | su2 12, su3 54, u1 6, weak SU(2) 12, E1 3 |
| E1 scalar potential Φ | 1 | |
| two-path relays | 168 | su2 24, su3 108, u1 12, weak SU(2) 24 |
| lapse and metric gears | 12 | metric 10, β 1, background 1 |
| cosmic hand Θ, Born loads, choice pair | 5 | 1 + 2 + 2 |
| package choice readers | 11 | two rings of 3, router 2, gate 1, exit 2 |
| **total** | **382** | |

- **Sizes are forced, totals are chosen.** Given its content, each sector's size is the smallest exact real module of its
  algebra [THEOREM]: 16 per charged Dirac fermion, 4 for the Higgs, 2 / 4 / 8 / 18 per link (U(1) / SU(2) / U(2) /
  SU(3)), 10 for the metric (`Sym²R⁴`), 128 per family (8 Dirac fermions with ν_R), and 48 for the dark board, the
  regular module of 2O, given a sign-free frame. Which sectors exist, how many copies (colours, families) and the total
  are CHOSEN.
- **What talks to what** [NUMERIC]: only 127 of the 382 gears form the connected physical core (L0 48, the two Dirac
  pairs 32, the weak SU(2) links with their relays 36, E1 4, the Higgs 4, and the lapse, β and background gears). The
  su2, su3 and u1 gauge layers (228 gears) read nothing and are read by nothing, so today the SU(3) field acts on no
  quark; 9 of the 10 metric gears are uncoupled too. A full Standard-Model family would need about 820–1,060 gears per
  node or more, because the rank rule forces one merged link for the quark doublet, and that link is not built
  [DERIVED].
- **The groups of the cube** [THEOREM]: the rotations `O` (24) are the spatial symmetry; `O_h = O × {±1}` (48) is
  `Aut(2O)`, so the mirrors act on the node as its outer automorphism; the binary octahedral group 2O (48 unit
  quaternions) gives the 48 L0 labels [CHOSEN as labels], with one central involution `z = −1`, the 2π turn.
- **Left and right** [THEOREM]: the node is `Z[i][2O]` acted on from both sides. The left action is the frame and spin
  (exact only together with the spatial rotation); the right action is internal, and the ports' exact commutant is right
  `Q8 × {±1}`, an exact internal SU(2) skeleton. All characters of the cube groups are real, and `R[2O]` splits into
  real and quaternionic blocks only, so the node by itself makes SU(2)s, never U(1) or SU(3).
- **The ports** [CHOSEN]: channel `g` at `x` reads channel `g·B_u` at `x + d` with sign `s_u`, `u = R(g)⁻¹d`, body actions
  `(0, 1, 3)` and signs `(1, −1, 1)` (the "handed" class). In this class the largest port eigenvalue is `2 + 2√3 < 6`,
  so every L0 mode is massive [THEOREM]. With `K = 2u` and six unit ports, `D = 6` is the smallest divisor that keeps
  every mode stable [THEOREM, given those choices].
- **The hands** [THEOREM]: for the massive Dirac block the transports satisfy `P_d² = −1` and anticommute, and
  `ω = PxPyPz` is central with `ω² = +1`. So there are exactly two hands, with `Γ5 = −PxPyPz`. `Γ5·V` (with `V = JJ′`) is
  the only chiral split that keeps the clock, the charge and CPT; P and C are broken, CP is exact. That the weak force
  couples to one hand, and which one, is CHOSEN.
- **Locality, a binding rule of the law**: every gear's input is computed only from its own node and its six face
  neighbours [CHOSEN]; every monomial sits on one node or on the two ends of one face (B3), and the builder rejects
  anything else (edge, diagonal or two-step offsets, or a monomial touching both `+e` and `−e`) [CHOSEN; enforced by
  the builder, THEOREM]; every update reads only the complete previous snapshot [CHOSEN]; the cosmic clock is one hand
  per node, joined to its six face neighbours by a rigid face term, not a non-local variable [NEW LAW, approved]. So
  information moves at most one face per update, inside the board-causal (taxicab) cone [THEOREM]. The physical wave
  cone `c_Q ≈ 0.577` lies inside it; `c_Q` is the wave front of the common stencil, not a hard bound, so the law alone
  does not exclude influence between the two cones [THEOREM].
- **Links make the geometry, not the neighbour graph**: the neighbour graph (the periodic cube, six faces per site) is a
  CHOSEN input. What passes between neighbours is set by the face (link) terms of the tensor: the face weights `Q − 1`
  of the common stencil give the one cone `c_Q² = (Q − 1)/(3Q)` [THEOREM, given the CHOSEN common stencil]; the gauge
  links carry the forces, one link per face per multiplet [THEOREM, forced by rank ≤ 4]; and gravity's link factor
  `1 − 4U`, with the clock factor `1 − 2U`, gives `g_ij = (1 + 2U)δ_ij`, so γ = 1 comes through this CHOSEN factor
  [CHOSEN ⇒ DERIVED].
- **Constants** [CHOSEN unless stated]: `Q` odd is a THEOREM given a mirror-fixed vacuum; the 6 in `D = 6Q` is a THEOREM
  given `K = 2u` and six unit ports; the cone value `c² = (Q − 1)/(3Q)` is forced by the one stencil, while sharing that
  stencil is CHOSEN; γ = 1 is CHOSEN (encoded in the link factor). Every mass, α, θ_W at low energy, the number of
  colours and families, the gauge regime, the seed and `L` are CHOSEN or data.

## The full algebra

Every gear of every node keeps the primitive of the reference heart and reads the same complete previous snapshot:

```python
u = T(previous_snapshot)            # one fixed integer polynomial: rank <= 4, own node + one face link
ell, r_next = divmod(2 * u + r, D)  # one divisor D = 6Q for every gear, Q = 2**33 + 1 (odd)
a_next = b
b_next = ell - a
```

The ten-line summary of [THE_ALGEBRA.md](full_picture_2026-11-10/THE_ALGEBRA.md) (§0), with its labels:

1. [CHOSEN] Space is the periodic cube `(Z/LZ)³`, `L ≥ 3`; every site holds the same list of gears; a gear holds
   `(a, b, r)`.
2. [CHOSEN] One divisor `D = 6Q`; one integer tensor `u` of rank ≤ 4: at most three factors from `v = (1, b, a)`, on the
   node and one face.
3. [THEOREM] One update, Rule3: `ell, r' = divmod(2u + r, D)`; `a' = b`; `b' = ell − a`. It is an exact bijection.
4. [CHOSEN] One seed: the vacuum `(0, 0, 3Q − 1)` everywhere plus a few non-vacuum integers. Each later turn of the
   cosmic clock starts a new seed, the full state at the turn (owner decision).
5. [THEOREM] Every gear is a clock: `b(t+1) + b(t−1) = 2u/D + ε` exactly, `|ε| < 1`, i.e. `M b(t) + ε` for the linear
   part; a mode with eigenvalue μ of `M` ticks at `cos w = μ/2`.
6. [THEOREM] A click is a carry of the remainder: `ell(t) = b(t+1) + b(t−1)`, and `D·Σ ell = Σ K + r(0) − r(T)` exactly.
7. [THEOREM] For the reciprocal part of the tensor (17,729 of the 18,553 live monomials) Rule3 is the discrete
   Euler–Lagrange equation of `L(x, y) = Φ(x) + Φ(y) − D x·y`, and there rank = degree of Φ. Reciprocity itself is a
   CHOSEN design rule, checked by the package; the 706 designated and 118 two-time monomials are not gradients.
8. [THEOREM] The node is the group 2O (48 channels) over the Gaussian integers `Z[i]`: acting on the left it is the
   frame and spin, on the right it is internal; the mirrors are its outer automorphism.
9. [DERIVED] Einstein's kinematics is in the tensor as the continuum limit of exact integer identities: one cone, given
   the one CHOSEN stencil; an exact equivalence-principle factor for every clock that reads the lapse (in the live FIX-i
   default only the dark board L0 reads it at rest, while the visible Dirac pair's rest clock neither feels nor sources
   it: a declared first-order debt); a γ = 1 weak-field metric via the CHOSEN link factor `1 − 4U` (the 1911 control
   gives γ = 0); local rotations. The dynamics is a Newtonian-level sourced scalar lapse plus designated one-way parts.
   The full Einstein equations are NOT reproduced, because Rule3 forbids, by theorem, an exact Bianchi identity and an
   exactly conserved reciprocal source.
10. [CHOSEN] What the cube fixes are forms (groups, sectors, hands, splits, cones); 3, `L`, `Q`, the weights and the seed
    are inputs.

Four theorems are used throughout:

- **The exact inverse** [THEOREM]: from the new snapshot, the old `b` is the new `a`; once `K = 2u` is known,
  `r = (r' − K) mod D`, `ell = (K + r − r')/D` and `a = ell − b'`. Gears whose input reads the `a` of other gears are
  undone after them, which needs an acyclic order of these two-time reads. The proof uses neither the sign nor the time
  independence of the coefficients. The live default rewinds exactly [NUMERIC].
- **Why `Q` is odd** [THEOREM, given a CHOSEN demand]: the exact mirror flips the remainder by `R'(r) = D − 2 − r`
  (r even) or `D − r` (r odd); for even `K`, `divmod(−K + R'(r), D) = (−ell, R'(r'))`. `R'` fixes a remainder only when
  `Q` is odd (exactly `3Q − 1` and `3Q`), so a vacuum fixed by the exact mirror exists if and only if `Q` is odd. The
  plain flip `r ↦ D − 1 − r` fixes no remainder at all. Demanding the mirror-fixed vacuum is CHOSEN; so is `2^33 + 1`.
- **Forces are gradients** [THEOREM; reciprocity is a CHOSEN design rule]: for a reciprocal block with potential Φ,
  `D·(b(t+1) + b(t−1)) = 2∇Φ(b(t))` is the discrete Euler–Lagrange equation of `L(x, y) = Φ(x) + Φ(y) − D x·y`; Rule3
  carries the rounding in the remainder. The kinetic coefficient is the one number `D` for every gear.
- **Energy changes only by remainder kicks** [THEOREM]: for a linear symmetric part `H`, the two-time energy
  `E = D|b|² + D|a|² − 2aᵀHb` obeys `E(t+1) − E(t) = Σ (r − r')(b' − a)`. Checked with 0 failures in 12,000 updates on 40
  random boards [NUMERIC]. Neither `E` nor `Q` is established physical energy.

## The clocks

- **Every gear is a clock** [THEOREM]: because `a' = b`, `b(t+1) + b(t−1) = 2u/D + ε`, with `ε = (r − r')/D` and
  `|ε| < 1`. For the linear part `u = H b` this is a leapfrog step with `M = 2H/D`, and a mode with `M e = μ e` and
  `|μ| < 2` ticks at `cos w = μ/2`. One gear by hand [NUMERIC]: `u = 12b`, `Q = 5`, `D = 30`, start
  `(a, b, r) = (0, 1, 14)`:

  ```
  t   (a, b, r)      K + r = 30·ell + r'      click ell
  0   ( 0,  1, 14)    24 + 14 =  38 =  30 + 8      1
  1   ( 1,  1,  8)    24 +  8 =  32 =  30 + 2      1
  2   ( 1,  0,  2)     0 +  2 =   2                0
  3   ( 0, -1,  2)   -24 +  2 = -22 = -30 + 8     -1
  4   (-1, -1,  8)   -24 +  8 = -16 = -30 + 14    -1
  5   (-1,  0, 14)     0 + 14 =  14                0
  6   ( 0,  1, 14)   the start again: period 6
  ```

  The remainder walks 14, 8, 2, 2, 8, 14 around its circle of 30 positions; each time it wraps, a carry `ell = ±1` is
  emitted and becomes the next `b`. At this amplitude the rate locks to 1/6; with a large amplitude the gear ticks at
  `arccos(0.4)/2π ≈ 0.1845` per update [NUMERIC].
- **A click is a carry** [THEOREM]: `ell(t) = b(t+1) + b(t−1)`, and summing `D·ell = K + r − r'` gives every gear's
  exact ledger `D·Σ ell = Σ K + r(0) − r(T)`. With a fresh uniform remainder a carry fires with probability exactly
  `K/D`, which is the Born count [THEOREM]; whether the remainders are fresh is OPEN.
- **Mass is the rest clock rate** [THEOREM]: a mode's mass is its rate at `k = 0`, read from the click record; a lone
  gear `u = m·b` has `cos w0 = m/D`. The node fixes the shape: the 1 + 2 split and the lattice-scale 1:2:3 ladders of
  L0 are forced [THEOREM]. Study 35 (signed by both sides) asked whether masses come out of the clicks with nothing
  put in by hand:
  - with no mass entry the board makes 9 rest levels in the handed class, `cos w0 = λ/6` with λ ∈
    {0, 2, 4, 2 ± √2, 2 ± 2√2, 2 ± 2√3} (7 in the flat class), measured from the click record to within 7·10⁻⁸ of
    `arccos(λ/6)/2π`. They are the dark board's (L0) levels, all at the lattice scale: the lightest is 0.068 per
    update (THEOREM S), and the λ = 0 level is click-silent. Nothing light comes out by itself [THEOREM + NUMERIC];
  - identical clocks never split themselves (THEOREM E): a split needs a coupling integer or a seed amplitude, which
    are data, so a forced Koide relation among identical clocks is impossible [THEOREM];
  - the visible doublet's mass is the tensor integer `2yv = 4915·2^22` [DATA]. Its measured rest rate, 0.06548 per
    update, matches the formula's 0.06549, and changing the integer moves it [NUMERIC]. No vev is reached by the
    clocks: from `Φ = 0` the Higgs runs away, so the mass exists because the seed starts at `Φ = v`
    [THEOREM + NUMERIC];
  - the fairest form of "masses by themselves" [BUILT]: a massless clock riding a condensate in the seed gets a light
    rest rate with no mass entry, but its value is the coupling times the square of the seed amplitude [DATA];
  - verdict: the FORM of the masses comes out by itself; the light VALUES do not. They are information, about 39 bits
    for the leptons, which must be written in once, as tensor integers or as seed data [THEOREM K].
- **Gravity is a lapse that slows clocks and links**: the lapse is the counter `F` of one metric gear, `U = F/(2P)` with
  `P = 2^20`. A clock that reads it gets the factor `1 − 2U` on its mass (on-site) entries and `1 − 4U` on its link
  (transport) entries; a first-order clock takes half of each [CHOSEN, approved law]. Both factors come from one
  potential, so feeling the lapse and sourcing it are two derivatives of one term [THEOREM]. A clock deeper in the
  potential ticks slower per update; on the dark board L0, `sin(w/2) = √(1 − 2U)·sin(w0/2)` exactly [THEOREM]. What
  this gives and what it does not:
  - Kinematics [DERIVED, as the continuum limit of exact integer identities]: one cone `c_Q² = (Q − 1)/(3Q)` for the
    metric gears, the E1 "light" and L0, given the CHOSEN common stencil; a weak-field metric `g00 = −(1 − 2U)`,
    `g_ij = (1 + 2U)δ_ij` with PPN γ = 1, which follows from the CHOSEN link factor `1 − 4U` (the 1911 control, `1 − 2U`,
    gives γ = 0); an exact equivalence-principle factor for every clock that reads the lapse; local Lorentz symmetry at
    order k².
  - Dynamics [DERIVED]: a Newtonian-level sourced scalar lapse, which obeys a discrete Poisson law, plus designated
    one-way parts.
  - The full Einstein field equations are NOT reproduced [THEOREM]: no reciprocal gravity coupling of any rank has an
    exactly conserved source (G-NOGO-a), and Rule3's fixed kinetic coefficient admits no exact Bianchi identity.
  - The FIX-i debt [NUMERIC; OPEN]: in the live default the visible Dirac doublet's rest clock neither feels nor sources
    the lapse. This equivalence-principle debt is first order in `U`; at rest, only the dark board L0 reads the lapse.
  - The opt-in Einstein layer (Study 28, DEFAULT OFF, `layers/einstein.py`): with it, the board holds linearised Einstein
    in harmonic gauge for all ten metric components on the one cone, coupled to the diagonal sector of L0 only, with a
    non-conserved source. γ = 1 for dust is then DERIVED given the layer's board reader; β = 1 holds for L0 in static
    fields; on the board, test lights give bending 2.08–2.16× and Shapiro 2.02–2.06× the Newtonian value [NUMERIC]. The
    full equations remain impossible [THEOREM], and the visible doublet stays uncoupled. The root README lists the
    details.
- **The cosmic clock** [NEW LAW, approved: the WIND hand]: one hand Θ per node, with no bare spring. Its stiffness is
  the record Δ of the matched choice pairs, `Δ(t+1) + Δ(t−1) = ell+ − ell−`, so the choice events turn it; a turn
  comes when its accumulated phase reaches π/2. The hand reads no matter: its only inputs are its neighbours and Δ. In
  the default (ONE v1) no package gear reads the hand [NUMERIC]; apart from the hand's own face terms, its only
  readers are the cosmic block's two reader gears M1 and M2, whose intensity loads the choice pairs. The
  doublet-reads-the-hand coupling (Study 22) was rejected by the owner: matter must not read the clock; it also runs
  away (Study 30); it is kept as an explicit opt-in for the record. An opt-in clock law, Study 34's CG2 (default OFF,
  valid only for L ≤ 6), lets the hand act on the lapse alone, so that a turn reaches matter only as a common
  clock-rate pulse, never as an echo or a bang of matter [NEW LAW; THEOREM]. The bang at `t = 0` is the one exact CPT
  bang: the CPT reversor R\* is exact along the bang seed, so the past is the CPT image of the future [NUMERIC:
  checked over 200 updates with hands OFF and over 10 in the FIX-i default and in ONE]. Every later turn of the hand
  is a bang that starts a NEW seed, the complete state at the turn with all its records [CHOSEN, owner decision]. The
  spacing of the turns (about 192 updates) is an input, set through the hand's constant `g_w` [CHOSEN]. Three theorems
  fix what this means: a growing history has at most one exact bang, so later turns never return to the original seed
  (THEOREM D); the board's information is law + seed + ⌈log2 t⌉, and only the click record grows (THEOREM K); the
  choices time the turns and never cause a bang (THEOREM N).
- **The arrow of time is the record**: the click map is many-to-one, so collapse is conditioning on records and nothing
  is erased [THEOREM]. In the ONE run the outcome record grows by about 80 kB of new incompressible data per aeon
  [NUMERIC]. Rule3 is a bijection, so no information is ever lost [THEOREM].
- **No freeze** [THEOREM; owner decision]: an oscillator cannot be paused by any input, and no b-only rule of any degree
  generates a hold. The zero-time hold was dropped: it was put in by hand, and no tensor generates it. Only the chosen
  path clicks, because one shared remainder overflows once [THEOREM]. That light executes the clicks is the owner's
  reading [CHOSEN].
- **Choice and determinism.** The owner's position, in contrast with a deterministic cellular-automaton reading of
  physics such as 't Hooft's: there is a choice for each click, so the universe is not deterministic [CHOSEN, the
  owner's reading]. The board facts: the click outcomes are set by free seed data (the tokens), which nothing else on
  the board fixes [CHOSEN: seed data]; with different tokens and loads the history stays bit-identical while 98 % of
  the outcomes differ [NUMERIC]; and given those data, Rule3 is an exact bijection [THEOREM]. So the final full state
  `(a, b, r)` and the seed determine each other; the click record alone does not, because the parity of `r` is inert
  (`K = 2u` is even): a seed and its parity-flipped copy give the same `a`, `b` and clicks [THEOREM].
- **Reading a clock** [CHOSEN, a read-only observation rule]: one tick is one sign cycle of the click sizes in the
  clock's own rotating frame; the carrier is fixed by the law (π/2 for the Dirac pair, 0 for L0 in form C), never by a
  species label. Under a uniform lapse `U0 = 0.0100002` the measured tick ratios match the exact laws [NUMERIC]: an L0
  band with `μ = 0.536` gives 0.989797 against 0.989797 predicted, and the Dirac rest clock of the hands-OFF matter gives
  0.989391 against 0.989404; GR's slow-clock value is `√(1 − 2U0) = 0.989949`. In the live hands-ON default the Dirac
  rest clock carries no lapse factor (the FIX-i debt above).
- **A lattice-scale redshift** [DERIVED; NUMERIC in two codes]: the observed tick ratio departs from the slow-clock value
  by `δ ≈ −U·w0²/12` for L0 and `−U·w0²/3` for the Dirac pair, where `w0` is the clock's rest rate. GR's redshift is
  recovered for slow clocks; the `w0²` term is a falsifiable prediction.

## The initial conditions (seed) and the tensor

### The seed

The seed is data only: [`prepare/`](prepare/) writes initial states, as AGENTS.md item 9 requires [CHOSEN].

- **The vacuum**: every gear at `(0, 0, 3Q − 1)`. The tensor has no constant and, after step 3 below, no linear term, so
  the vacuum is a fixed point, and the mirror fixes it because `Q` is odd [THEOREM].
- **S2\***, the minimal bang seed: exactly two non-vacuum integers, `b(x0) = A·e_i` and `a(x0 + e_y) = A·Γe_i`, with
  `Γ = J′KW0`. It is fixed by the CPT reversor about the link midpoint and legal at `t = 0` (Lorenz and Gauss
  constraints zero everywhere) [CHOSEN].
- **J-pure**: amplitude `A_J = 2^12`, 6,912 nonzero integers on 216 nodes [CHOSEN]. The background datum, the R-a gear
  and the `k = 0` lapse offset are declared data.
- **The ONE seed** ([`prepare/one.py`](prepare/one.py)): a J-pure or S2\* package bang, plus the hand at rest at `Θ0`
  including the remainder `3Q − 1` (`Θ0 = 2^24` in the default ONE v1; the rejected coupled build used 64), a neutral
  packet of amplitude `2^10`, static Born loads and tokens. All of it is fixed by the CPT reversor about the bang
  centre [CHOSEN; NUMERIC: 0 mismatches over 10 updates].
- **Three declarations** (so that nothing reads as circular): the time scale is an input, because the hand's constant
  `g_w = 1310` was chosen for a target quarter period, so the turn times are checked, not predicted; no-signalling holds
  in the matched seed sector, where the law preserves it and the seed initiates it; the Born weights are seed data, put
  in by the loads, and the Born ledger (maximum deviation `3.2·10⁻⁷`) verifies the mechanism, not the probabilities.
- **New seeds**: each later bang starts a new seed, the complete state at the turn with all its records. Nothing is
  reset, posted or tuned [CHOSEN, owner decision].

### The tensor

The tensor is data: an ordered list of gear types and a list of monomials. A monomial adds
`integer coefficient × (at most three factors)` to one gear's input `u`; a factor is the `b` or the `a` of one gear at
the same node or at one face neighbour [CHOSEN]. The builder rejects more than three factors (rank above 4), a
non-integer coefficient, an illegal offset, a cycle of two-time reads, a one-way entry without a written reason, and
two different `Q` [THEOREM]. The recipe has seven steps:

1. **Blocks.** Split the content into blocks (gear types, terms, vacuum remainders, parameters, one `Q`).
2. **One potential per block; rank = degree.** For a reciprocal block write one integer potential Φ and take
   `u = ∂Φ/∂b`, so action = reaction. Then Rule3 is exactly the discrete Euler–Lagrange equation of
   `L(x, y) = Φ(x) + Φ(y) − D x·y`, with the rounding carried by the remainder [THEOREM]. A Φ of degree n gives a force of
   degree n − 1, so rank = degree of Φ: rank 2 is a quadratic Φ (masses, hops), rank 3 a cubic Φ (a hop through a dynamic
   link, a lapse dressing), rank 4 a quartic Φ (the link spring) [THEOREM]. Reciprocity is not forced by Rule3, which
   runs with any integer `u`; it is a CHOSEN design rule, checked by the package.
3. **Deviation form about the vacuum.** Store the deviation from the vacuum `(0, 0, 3Q − 1)` and remove the linear term,
   so that the vacuum is a fixed point [THEOREM]; the mirror fixes it because `Q` is odd (see above).
4. **B3 locality.** Every monomial lives on one node or one face link [CHOSEN]. Then one update moves influence by at
   most one face, so the board is causal inside this taxicab cone [THEOREM].
5. **Reciprocal or one-way.** Every term that is not a gradient of Φ is declared one-way, with a written reason. Its
   price: Newton III fails for that coupling, and it is never variational [CHOSEN].
6. **Staging.** A factor `a` reads `b(t−1)`. The exact inverse recovers the old snapshot stage by stage: the old `b` is
   the new `a`; once `K = 2u` is known, `r = (r' − K) mod D`, `ell = (K + r − r')/D` and `a = ell − b'`. So the two-time
   reads must form an acyclic order, and then Rule3 is an exact bijection for coefficients of any sign [THEOREM].
7. **Compose, then run the ten checks:** one `Q`; rank ≤ 4; B3; acyclic two-time reads; reciprocity; no constant and no
   linear term (a fixed vacuum); exact rewind; an exact CPT reversor on a seed; an all-`k` Bloch scan of the linear part;
   integrality. Checks 1–8 are kinematic and do not imply a bounded history [THEOREM]; the Bloch scan is the check that
   separated the runs that ran away from those that stayed bounded [NUMERIC].

**A worked block** [NUMERIC, with the coefficients DERIVED by hand]: the package builder turns a small U(1) block
(`Q = 5`, so `D = 30`; link vacuum `A = 2`, hop 1, mass 4, spring `λ = 1`) into 8 gear types and 77 monomials of rank 4,
with 0 reciprocity violations. Its potential is
`Φ = Σ_k ⟨ψ(x), U(x,k) ψ(x+e_k)⟩ + 2|ψ|² + (D/2) Σ_k |U_k|² − (1/4) Σ_k (|U_k|² − A²)²`. The radial link gear `U_x,re`
(deviation `W`) gets exactly seven monomials:

```
22·W_re                                       degree 1:  D − 2λA² = 30 − 8 (inertia minus spring stiffness)
1·ψ_re(0)·ψ_re(+e_x),  1·ψ_im(0)·ψ_im(+e_x)   the hop: ∂/∂W_re of Re(ψ̄ W ψ′)
−6·W_re²,  −2·W_im²                           degree 2:  −3λA and −λA
−1·W_re³,  −1·W_re·W_im²                      degree 3:  −λ, twice (the rank-4 part: a quartic Φ gives a cubic force)
```

So the radial link ticks at `cos w = 22/30`, i.e. `4 sin²(w/2) = 4λA²/D`, and the angular link (linear coefficient 30)
is a massless zero mode, the holonomy direction [DERIVED]. Reciprocity is visible by eye: the link reads
`ψ_re(0)·ψ_re(+e_x)` and the matter gear reads `ψ_re(+e_x)·W_re(0)`; both are derivatives of the one potential term
`ψ_re(x)·W_re(x)·ψ_re(x+e_x)` [THEOREM].

**The kinds of rank-4 terms**:

| kind | form | status |
| --- | --- | --- |
| OD4 spring | `−(λ/4)(|U|² − A²)²` on one link | the only reciprocal rank-4 kind in the package default: 1,528 monomials [NUMERIC] |
| narrow kind | an uncharged singlet × a gauge-covariant rank-3 composite; "link × composite" is excluded | approved design rule [NEW LAW]; in ONE, used by the choice pair |
| plaquette kind | the four links around one plaquette, with no matter factor | approved [NEW LAW]; used only by route B's opt-in plaquette option, by no default block |
| designated rank 4 | the E1 dressed source (384) and the gated exit (18) | the two allowed one-way places [NUMERIC] |

**The census** [NUMERIC]:

| system | gear types | monomials | designations (one-way) | rank |
| --- | --- | --- | --- | --- |
| package default `default_system()` (hands ON, FIX-i) | 375 | 18,553 (by degree 1 / 2 / 3: 2,329 / 14,294 / 1,930) | 706 | 4 |
| ONE default (v1), block-diagonal | 382 | 18,592 | 736 | 4 |
| rejected coupled build `couple_doublet=True`, kept for the record | 382 | 27,040 | 17,856 | 4 |

The package default has three inverse stages (358, 1 and 16 gear types), and 17,729 of its monomials pass the
reciprocity check with 0 violations. In the rejected coupled build, all 17,120 package terms that read the hand were
designated one-way [NUMERIC].

**Rank 4 is final** [CHOSEN, owner decision; NUMERIC evidence from Study 23]: a rank-5 term "hand × any approved rank-4
term" lifts only one wall, the hand × lapse × link × matter hop, and only to an approximate echo (0.0033, against no
echo at rank 4). Whether a fold of the cosmic clock is exact is decided by a parity law (THEOREM O), not by the rank, and the
zero-time hold cannot emerge at any rank. The costs would be a two-way term unbounded below (a quintic potential) and about 19× less usable amplitude at
the package's `Q`.

## Sources

- [full_picture_2026-11-10/THE_ALGEBRA.md](full_picture_2026-11-10/THE_ALGEBRA.md), signed (Study 24): §0 (the ten
  lines), §1 (the law and its inverse), §2 (the node), §3 (the tensor recipe, census and rank 5), §4 (the clocks), §5
  (Einstein: what the continuum limit gives and what it does not), §6 (conservation), §8 (quanta), §9 (the seed, the
  bang and the cosmic clock), §10 (the circularity audit).
- [full_picture_2026-11-10/CHANNELS.md](full_picture_2026-11-10/CHANNELS.md), signed (Study 26): channel counts, sizes
  and constants.
- [NOTES_one.md](NOTES_one.md) (Study 22): the ONE version, its tests, results and declarations.
- [README_v1_draft.md](README_v1_draft.md): the detailed package description, with the evidence index; it governs.
- [AGREE_STAB_2026-11-10.md](AGREE_STAB_2026-11-10.md) (Study 18): the stability record behind FIX-i.
- Code: [`layers/one.py`](layers/one.py), [`layers/system.py`](layers/system.py), [`prepare/one.py`](prepare/one.py),
  [`prepare/seed.py`](prepare/seed.py), [`observe/readout.py`](observe/readout.py), [`core/tensor.py`](core/tensor.py),
  [`core/engine.py`](core/engine.py), [`core/reciprocity.py`](core/reciprocity.py).
