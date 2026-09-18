# Derivations of the known laws from the couplings

The model owner's question of 2026-09-18: from the simple laws and the
declared couplings alone, with limits and continuum arguments, which known
formulas can be reached, at least Newton's and Einstein's, and which
cannot? This document answers it on paper. No engine run was made for it,
no experiment, no edit to the engine. Every formula below is derived from a
Node rule of [Highlights](HIGHLIGHTS.md) or of the catalog entry that
implements it, cited at the point of use; the numbers of the runs and of
the mean-field computations already recorded ([A5s](EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest),
[A6](EXPERIMENTS.md#a6-light-bending-by-a-bound-group-and-g_eff-n²-over-n--28-to-216),
[E11](EXPERIMENTS.md#e11-the-fields-books-the-profile-of-a-point-source-shell-by-shell-and-the-momentum-between-release-and-meeting))
are cited only at the end of each section as checks, never as a starting
point. The method is the one the model owner set: one interval of the
engine written as an operator on the lattice, its exact identities, its
Fourier symbol, its continuum limit, and the place where integer rounding
enters. The small arithmetic checks were made in Python (sympy, mpmath,
numpy) on the formulas of this document alone, seconds each; they are not
engine runs and establish nothing about the engine. The dated register of
runs stays [EXPERIMENTS.md](EXPERIMENTS.md); the open questions stay
[HYPOTHESES.md](HYPOTHESES.md).

The verdict of each section uses three words. **Reached**: the known law
follows from the rules in the stated limit, exactly or up to a constant that
is named. **Different law**: the rules give a definite law of another form,
stated, with the run that would show the difference. **Not reached**: the
rules as declared do not determine the quantity, and what would is stated
plainly. **New** marks a formula the lattice gives that has no counterpart in
known physics. The summary table is [section 15](#15-the-verdicts-in-one-table-round-1-see-section-21-for-round-2); round 2 (sections 17 to 21, the model owner's points 16 to 21 of 2026-09-18) is summarized in [section 21](#21-round-2-the-verdicts-that-change-and-those-that-stand); round 3 (sections 22 to 25: Boss's vectorial steering rule and phase-reading push of 2026-09-18, verified, and the wait of point 23, PR #278) is summarized in [section 25](#25-round-3-the-verdicts); round 4 (sections 26 to 33: the model owner's point 24 of 2026-09-18, the Node mixes the six, derived as an operator and verified) is summarized in [section 33](#33-round-4-the-verdicts); round 5 (sections 34 to 38: the model owner's question of 2026-09-18, does the shadow pay the wait, the three options derived side by side against the gravitational tests, verified) is summarized in [section 38](#38-round-5-the-verdicts); round 6 (sections 39 to 44: the model owner's direction of 2026-09-18, the wait reads the amplitude, the coupling derived against the four gravitational tests, and whether any local reading falls as 1/r without the root, verified) is summarized in [section 43](#43-round-6-the-sizes-for-a6-the-separating-observable-and-the-verdicts); round 7 (sections 45 to 50: the model owner's decision of the evening of 2026-09-18, a thing emits and the stream leaves at the edge of an open board, derived as the fixed point of the emitting thing, its transient, its integer form and the tests, with the scratch script committed as `tools/derivations_round7.py`) is summarized in [section 50](#50-round-7-the-verdicts-and-the-run-plan); round 8 (sections 51 to 56: the model owner's decision of the same evening, the law of the shadow, only shadows and events, written as points in the mathematician's draft and derived on the fixed point of round 7, with the scratch script committed as `tools/derivations_round8.py`) is summarized in [section 56](#56-round-8-the-verdicts-the-smallest-engine-and-the-first-three-worlds).

## 0. Units, notation and the operator

**Lattice units.** The Link ℓ (the distance between neighbouring Nodes), the
interval δt (one tick), the quantum (one unit of amount; m₀ for a family of
rest rate 1, hypothesis 12). Everything moves one Link per interval
(Highlights 3.28, "there is no other speed in the engine"), so c = 1 Link
per interval. Momentum is amount × heading (catalog, `units.amount`), in
quanta·Link/interval; the invariant the couplings call energy is the amount
itself. A physical dictionary appears in each section.

**State.** Two kinds of content, distinguished by the bit alone (Highlights
3.3, 5.4, the law of the bit):

- Shadows (bit 0), the field: per Node x, per heading h ∈ {±e₁, ±e₂, ±e₃},
  the whole quanta a(x, h, t) that arrived at x during interval t on heading
  h (resident at x at the end of tick t), and per Node, family, sign and Port
  the remainder register ρ(x, h) ∈ {0, …, S − 1} in units of 1/S (Highlights
  3.17; [field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1),
  `field-remainder-v1`).
- Things (bit 1): each with a position x_i, a content m_i (its amount, its
  mass by Highlights 3.4 and 3.28), a momentum register p_i ∈ ℤ³ and three
  accumulators A_i ∈ ℤ³ ([a free ray turns by momentum](SPATIAL_FIELDS.md#a-free-ray-turns-by-momentum-ray-momentum-turn-v2);
  [the external body](SPATIAL_FIELDS.md#the-external-body-external-body-v1)),
  a phase φ_i on the circle of N = 2^phase_bits steps and a family rest rate
  r (Highlights 3.3).

**The rules, one interval.** Each rule names its source; nothing else is
used anywhere below.

- **R1, the split** (Highlights 3.5, "Light is the field, and the field
  spreads"; `field-spreading-v1`). The table w = [6, 1, 1, 1, 1, 1] with
  S = Σw = 11: content A that arrived on heading h is shared over the six
  headings h' with the weight W(h', h) = 6 if h' = h (forward), 1 if h' = −h
  (backward), 1 for each of the four transverse headings. Integer form: the
  whole quanta ⌊A·W(h', h)/S⌋ leave through h', the share A·W(h', h) mod S
  goes to the register ρ(x, h'), and a register that reaches S releases one
  whole quantum through its Port in the same interval. Mean-field form (the
  expectation of the integer form, since a register never destroys or
  creates a share): the linear map A → A·W(h', h)/S. Column sums:
  Σ_{h'} W(h', h) = S, so the split conserves amount exactly.
- **R2, the walk** (Highlights 3.3, 3.8, 3.9). What departs through Port h'
  at x in interval t + 1 is resident at x + h' at the end of tick t + 1 and
  is split there in interval t + 2.
- **R3, the source.** Two readings exist in the Highlights and both are used
  below, each named where it enters. The emitting reading (Highlights 3.5,
  "the release does not wait for the clock", superseded on 2026-09-18 but the
  reading under which every recorded run was made; `released-field-v1`,
  `external-body-v1`): a thing of content M releases ⌊M·n/d⌋ quanta per
  heading per interval on six headings, ρ = n/d its declared release ratio.
  The standing reading (Highlights 5.4, "A thing does not emit"): the
  shadows of a thing are a standing set of declared total X, given with the
  board as a declared profile or as the mean field's steady state, rounded to
  whole quanta with the fractions in the registers; a shadow that comes home
  leaves again.
- **R4, the push** (Highlights 5.4, the law of the bit, point 3;
  `ray-momentum-turn-v2`, `external-body-v1`, `momentum_table`). A thing at
  x whose table names the shadows' family takes, in one interval,
  Δp = σ·Σ_h a(x, h, t)·h, σ = ±1 the declared sign (−1 toward the source,
  +1 away), from every shadow at its Node; the engine's rule is one receiver
  per rule per Node per interval, which takes every shadow the table names.
- **R5, the return** (Highlights 5.4, point 3 and "Every action is a message
  that returns"). Each shadow that pushed turns back on its own steps with
  its amount and the opposite of the push it gave, arrives at its owner after
  as many intervals as it had walked (following the trace if the owner
  moved), and the owner's register changes by −Δp; a shadow that reaches its
  owner without having pushed is home and is absorbed back.
- **R6, the motion of a thing.** An external body: every interval each axis
  accumulator adds the register's component, and the body steps one Link
  through the Port of the first axis whose accumulator has reached the
  content M, subtracting M; at most one Link per interval
  (`external-body-v1`, "motion by fields only"). A free ray: the DDA, every
  interval the accumulators add the register, the axis furthest ahead steps
  one Link and loses the register's Manhattan length |p|₁
  (`ray-momentum-turn-v2`, "the DDA walks the register"). A bound group: the
  corner table on a ring (Highlights 3.4; [binding as a loop](SPATIAL_FIELDS.md#binding-as-a-loop-loop-binding-v1)).
- **R7, the phase** (Highlights 3.3; [loop binding](LOOP_BINDING.md#3-closure-as-integer-equalities)).
  A thing's phase advances by its family's rest rate r at every Link, modulo
  N; light's rate is 0; a shadow carries its owner's phase and no clock (law
  of the bit, point 9).

**Derived per-Node quantities** (definitions, no rule added):

```text
n(x, t)        = Σ_h a(x, h, t)                          content at the Node
φ(x → x + h')  = Σ_h W(h', h) a(x, h, t) / S              departure through Port h' (mean form)
Φ(x, x + h')   = φ(x → x + h') − φ(x + h' → x)           net Link current on the Link
J(x, t)        = Σ_h a(x, h, t) h                         net momentum arriving at x
```

J is what a thing at x takes per interval up to the sign σ (R4), and n is
what the record calls the content per Node.

**Where the integers enter.** The remainder register makes the integer split
equal to the mean-field split up to one bounded quantity per Node, family,
sign and Port: the whole quanta released through a heading over any window
equal the accumulated share of that heading to within one quantum. Every
mean-field formula below therefore holds for the engine's integers with a
bounded remainder per Node, which is what the dense-mode runs read
([A5s Run 2](EXPERIMENTS.md#a5s-coulombs-force-law-between-two-charges-at-rest):
a part in a thousand at r = 12, 16, 20; E11: a part in a thousand through
k = 16). What rounding changes qualitatively, the granularity of the far
field, is derived in [section 11](#11-gravity-on-a-quantum) and
[section 13](#13-what-the-lattice-says-that-the-textbooks-do-not).

## 1. Exact identities of the operator: continuity, Gauss's law, J = (11/8)·Φ

**Rules used.** R1, R2 and the definitions of section 0; nothing else.

**Continuity.** Everything resident at x in interval t leaves in interval
t + 1 (R1: the column sums are S, so Σ_{h'} φ(x → x + h') = n(x, t)), and
what is resident at x at the end of t + 1 is what arrived (R2):
n(x, t + 1) = Σ_{h'} φ(x − h' → x). Subtracting,

```text
n(x, t + 1) − n(x, t) = Σ_{h'} [φ(x − h' → x) − φ(x → x + h')]
                      = − Σ_{i=1..3} [Φ(x, x + eᵢ) − Φ(x − eᵢ, x)]  =  −(div Φ)(x).
```

This is the discrete continuity equation, exact. In the integer form n(x)
counts the in-flight quanta plus the registers' content (the ledger's
`current` line, [field spreading](SPATIAL_FIELDS.md#field-spreading-field-spreading-v1),
"the booking"), and the identity holds in integers because
Σ_{h'} ⌊A·W/S⌋ + Σ_{h'} (A·W mod S)/S = A.

**Gauss's law on the lattice.** Sum the identity over any set V of Nodes
that contains the source Node. Interior Links cancel in pairs (Φ on a Link
is counted once from each end with opposite signs); what remains is the
source's release less what it absorbs (its own shadows coming home, R5),
call it S_eff, and the Links crossing the boundary ∂V:

```text
Σ_{x∈V} [n(x, t + 1) − n(x, t)] = S_eff(t) − Σ_{Links crossing ∂V} Φ.
```

At a steady state the left side is 0, so the net current through every
closed surface of Ports enclosing the source is the same number S_eff, for
any shape and any size of V, at any r, exactly. This is Gauss's law as an
identity of the operator, with no continuum argument and no power law
assumed; it says nothing yet about the current per Node, which needs the
shape of the surface (section 5).

**The momentum a thing takes against the Link current.** On the axis e
through x write a₊ = a(x, +e), a₋ = a(x, −e), and Σ_t for the four transverse
arrivals. By R1 the departures on that axis are

```text
φ(x → x + e) = (6 a₊ + a₋ + Σ_t) / 11,     φ(x → x − e) = (a₊ + 6 a₋ + Σ_t) / 11,
```

so their difference is (5/11)(a₊ − a₋) = (5/11)·J_e(x). The arrivals are the
neighbours' departures toward x, a₊ = φ(x − e → x), a₋ = φ(x + e → x), so
J_e = φ(x − e → x) − φ(x + e → x). The net Link currents on the two Links of
that axis at x then sum to

```text
Φ(x − e, x) + Φ(x, x + e) = [φ(x − e → x) − φ(x + e → x)] + [φ(x → x + e) − φ(x → x − e)]
                          = J_e + (5/11) J_e = (16/11) J_e(x),
```

at a steady state (or with the departures read one interval after the
arrivals). The mean Link current on the axis through x is Φ̄_e = (8/11) J_e,
that is

```text
J(x) = (11/8) Φ̄(x)        exactly, at every Node, on every axis,
```

and for a general table J = 2Φ̄/(1 + c) with the persistence
c = (w_f − w_b)/S = 5/11 (2Φ̄ for the simple walk, c = 0). This is the
factor that turns Gauss's current into the push on a thing.

**Check.** The mean-field computation of A5s states J = 11/8 Φ at every Node
and the outflow through the cube of half-width r equal to S to 10⁻⁷ at
r = 2 to 64; E11's steady flux is the same number through every one of 22
shells, L1 and Euclidean alike, to one part in 10⁸.

**Verdict.** Gauss's law in flux form: **reached exactly** on the lattice,
as an identity. J = (11/8)Φ: **new** (the factor is the table's; it is 2 for
a memoryless walk and 1 + 5/11 = 16/11 over 2 here).

## 2. The Fourier symbol: diffusion, D = 4/9, and the cubic anisotropy

**Rules used.** R1, R2. The board is periodic or large (Highlights 3.1); the
source is left out here and put back in section 5.

**The symbol.** Writing R1 and R2 together, a(x, h', t + 1) = Σ_h T(h', h)
a(x − h', h, t) with T = W/S, and Fourier transforming in x
(â(k) = Σ_x a(x) e^{−ik·x}),

```text
â(k, h', t + 1) = e^{−ik·h'} Σ_h T(h', h) â(k, h, t)  =  [M(k) â(k, t)]_{h'},   M(k) = diag(e^{−ik·h}) T.
```

T is symmetric and doubly stochastic. Its eigenvalues at k = 0 are 1
(once, the eigenvector (1, …, 1), the content) and (w_f − w_b)/S = 5/11
(five times: the three vector modes a(+e) − a(−e) and the two traceless
tensor modes). Only one mode is undamped at k = 0, and by the symmetry
h → −h of the table the eigenvalue λ₀(k) that continues it is real and even
in k. Its expansion (computed exactly in rationals by fitting the symbol at
small k in the three directions and checked on the simple walk, whose
symbol is (cos k_x + cos k_y + cos k_z)/3 = 1 − k²/6 + Σkᵢ⁴/72 − …):

```text
1 − λ₀(k) = (4/9) k²  −  (58/81) Σᵢ kᵢ⁴  +  (95/243) (k²)²  +  O(k⁶).
```

**The diffusion constant.** The order-k² term is isotropic, as the cubic
group O_h requires (k² is its only quadratic invariant), and gives the
continuum equation of the content, n(x, t + 1) − n(x, t) = D ∇²n with

```text
D = (1/6)·(1 + c)/(1 − c) = (1/6)·(16/11)/(6/11) = 4/9   Link² per interval,
```

the persistent random walk's constant in three dimensions with persistence
c = 5/11 (D = 1/6 for the simple walk; the ratio D_simple/D = 3/8 is the
number the split table adds to Gauss's law and appears in every density
formula below). The correlation lengths of the damped modes are
1/ln(11/5) = 1.27 Links for the momentum mode and, for the unscattered
forward share on a line (the beam, ⌊6/11⌋ of it per Link), 1/ln(11/6) = 1.65
Links: beyond a few Links only the diffusive mode survives.

**The anisotropy at order k⁴.** O_h has two quartic invariants, (k²)² and
Σkᵢ⁴; the coefficient of Σkᵢ⁴ is the lattice's first departure from
rotational symmetry, a = −58/81 (the simple walk has −1/72). In real space
the density mode obeys

```text
n(t + 1) − n(t) = D ∇²n + (58/81) Σᵢ ∂ᵢ⁴ n − (95/243) ∇⁴ n + O(∂⁶).
```

Its effect on the far field of a point source is derived in section 5.

**Why not a wave.** The symbol of any non-negative split table is a
stochastic matrix; by Perron–Frobenius its eigenvalues other than 1 lie
inside the unit disc, so at k → 0 exactly one mode is undamped and it is
even and real: λ₀ = 1 − Dk² + …, diffusion. A wave equation needs a pair
λ± = e^{±iω(k)} with ω ≈ c_w k, two undamped modes of unit modulus, which
no table of non-negative amounts has. Section 6 states what a
phase-steered split would have to do.

**Verdict.** The continuum limit of the spread step is the diffusion
equation with D = 4/9: **reached exactly** as the k → 0 limit. The
anisotropy coefficients −58/81 and 95/243: **new**.

## 3. Newton's second law from the momentum register

**Rules used.** R4 (the push), R6 (the accumulator of an external body; the
DDA of a free ray), Highlights 3.14, 3.16, 3.28 ("speed is a clock
slowing" and "the velocity is its momentum over its amount, kept as an exact
accumulator that steps one Link when a full amount has accumulated on an
axis", Highlights 3.19).

**The force.** By R4 the register of a thing at x changes in one interval by
Δp = σ J(x, t), a bounded integer vector; nothing else changes it (Highlights
3.19: "nothing else moves it"). So dp/dt = F with F := σ J the momentum flux
of the shadows the thing absorbs per interval, exact in integers at every
tick. This is the first half of Newton's second law, in the form Newton
wrote it (the rate of change of the quantity of motion equals the impressed
force), with the force identified as the net momentum of the shadows met
per interval.

**The velocity of an external body (m = content).** Let the register be
constant, p. Per axis, the accumulator adds pᵢ every interval and gives
back M at every step, so after t intervals with xᵢ(t) steps taken,
Aᵢ(t) = pᵢ t − M xᵢ(t) with 0 ≤ Aᵢ < M (the step happens when the
accumulator reaches M and the accumulator never exceeds M when |pᵢ| ≤ M).
Hence

```text
xᵢ(t) = pᵢ t / M − Aᵢ(t)/M,      | xᵢ(t) − pᵢ t / M | < 1 Link,
```

the position is the integral of p/M to within one Link at every tick, and
the mean velocity is v = p/M exactly. With a force, p(t) = p₀ + Σ_{t'<t} F(t')
and

```text
x(t) = x₀ + (1/M) Σ_{t'<t} p(t') + O(1 Link)  =  x₀ + v₀ t + (F/2M) t² + O(1 Link) for constant F,
```

the parabola of a constant push, exact up to one Link. This is Newton's
second law F = M a with the inertial mass equal to the content, and Newton's
first law (constant p, uniform motion) as its special case. The limit
needed is only "many intervals": the O(1 Link) term is the only remainder.
The rule of one step per interval adds a bound with no Newtonian
counterpart: the accumulator rule needs |pᵢ| ≤ M per axis and admits at most
one Link per interval, so |v|₁ ≤ 1 = c; a register above M "fails the
cycle" (`external-body-v1`). The momentum is Newtonian, p = M v, and hard
capped, not γMv.

**A free ray (a thing of one register).** Under the DDA the axis furthest
ahead steps every interval and loses |p|₁: over t intervals the steps on
axis i are t·|pᵢ|/|p|₁ up to one Link, so the velocity is

```text
v = p / |p|₁      (Links per interval, |v|₁ = 1 always),
```

a direction, never a speed (Highlights 3.28). dp/dt = F still holds exactly
(R4), so a free ray obeys Newton's second law for its momentum and the
kinematics of a massless particle for its velocity (v = c p̂ in the L1
norm), whatever its rest rate: "slow" in the engine is a phase rate, not a
speed. Under a constant transverse push F = (0, 1, 0) per interval on a ray
of register (64, 0, 0), the y-position grows as Σ_t pᵧ(t)/|p(t)|₁ ≈ t²/(2·64)
for t ≪ 64: a parabola again, with the register's Manhattan length in the
place of the mass; the DDA takes its +Y Links at intervals 9, 15, 20 and 24
(my arithmetic of R6, reproducing the numbers stated for
`ray-momentum-turn-v2`).

**A bound group.** The motion of a loop as a whole is its corners shifting
(Highlights 3.4), a periodic orbit not yet established
([loop binding](LOOP_BINDING.md#8-motion-of-a-loop-as-a-whole)); no velocity
law for a loop can be derived today (section 9 gives what step counting
alone allows).

**Dictionary.** p ↔ momentum in quanta·Link/interval; M ↔ mass in quanta;
F = σJ ↔ force in quanta·Link/interval²; v ↔ Links per interval, c = 1.

**Check.** A5s and A6 read the register's change per interval as the push
and the body's accumulator as the motion (the bodies of A5s complete no
Link at 2²⁸, as the bound predicts: F t²/2 ≈ 6·10⁵ ≪ 2²⁸·1); A6's light of
2¹⁸ turned by 3423 quanta completes no transverse Link in 64 Links, as
v = p/|p|₁ predicts (3423/265567 × 64 = 0.82 < 1).

**Verdict.** Newton's second law: **reached exactly** for an external body
(dp/dt = F and v = p/M, to one Link), with the extra bound |v|₁ ≤ c; for a
free ray **reached** for the momentum and **different law** for the
velocity (v = c p/|p|₁, the massless form; the run that shows it is any
pushed ray, which never slows); for a bound group **not reached** (its
motion is open).

## 4. Newton's third law and the recoil

**Rules used.** R4, R5, Highlights 3.14 (no self-created force), 3.15
(exact accounting), 5.4 point 3 and "Every action is a message that
returns".

**At the meeting.** A shadow of amount a and heading h meeting a thing gives
it Δp = σ a h and turns back carrying −Δp along its own steps (R5). At the
meeting Node, Δp_thing + Δp_carried = 0 exactly, in integers. Nothing else
is created: the meeting is "a pair of opposite steps on one line whose sum
is zero" (Highlights 5.4).

**At the owner.** The shadow reaches its owner after s intervals, where s
is the number of Links it had walked from the owner to the meeting (R5), and
the owner's register changes by −Δp. So for every push,

```text
Δp_owner(t_meet + s)  =  − Δp_thing(t_meet):      action = − reaction, delayed by s intervals.
```

Summing over every push a thing i has taken (from others' shadows) and
every push its own shadows have given (to others), with the returns that
have arrived by tick t,

```text
p_i(t) = p_i(0) + Σ_{pushes taken by i, t_k ≤ t} Δp_k − Σ_{pushes given by i's shadows, t_j + s_j ≤ t} Δp_j,
```

an exact integer identity, and Σ_i p_i is constant once every return is
home: momentum is conserved among things (law of the bit, point 7), and
between the meeting and the return the difference is exactly the momentum
carried by the returning shadows in flight. This is Newton's third law with
a finite-speed delay, the form Highlights 3.5 states ("recoils when the
return arrives, at finite speed").

**The delay.** Here the diffusive spread (section 2) enters. A shadow that
arrives at distance r from its owner has walked s Links, and s is not r: the
shadows present at r at a steady state have the age distribution of the
diffusive field, and a shadow of age s walks back s Links. The fraction of
the recoil that has come home by s intervals after the push is the fraction
of the field at r younger than s, which for the diffusion equation with
D = 4/9 is

```text
returned(s) = erfc( r / (2 √(D s)) ):     half of the recoil is home after s₅₀ = 2.47 r² intervals,
                                            90 % after s₉₀ = 71 r², and the mean age is infinite,
```

the unreturned part falling as r/√(π D s) for s ≫ r². (For the fraction
1 − f that never returns, section 5, and the standing reading of R3 the
same schedule applies to what does come home.) So the third law holds
instantaneously at the meeting Node and in the sum over things and returns
at every tick, but the reaction reaches the owner on a diffusive schedule
of order r², not r: for two bodies at rest at distance r the sum of their
registers is not zero at any tick, the missing momentum being in flight in
returning shadows, and it approaches zero only as s^{−1/2}.

**What the recorded runs did instead.** The engine of A5s and E11 returned
the recoil as a fresh ray on the reversed line, spread from the next Node
(`field-spreading-v1`, "Consequences"), so most of it never reached the
source (E11: A receives about half in the spread world; A6: the star's
register 222 against the light's 3423 at b = 4). The identity above is the
law of the bit's, to be shown by E11 (a) repeated under it, which is the
run that reads the schedule s.

**Verdict.** Newton's third law: **reached exactly** as an integer identity
at the meeting and over the closed books; **different law** in time: the
reaction is delayed by the shadow's own path, whose distribution is the
diffusive age at r (median 2.47 r²), not r/c. The run: E11 (a) under the
law of the bit, reading the tick at which A's register moves against the
push tick.

## 5. Gauss's law, the inverse square, Coulomb's law and the lattice anisotropy

**Rules used.** R1, R2, R3 (both readings, named), R4, R5, and the
identities of sections 1 and 2.

**The steady state of a point source.** With a source of effective strength
S_eff at the origin, the continuum limit of section 2 at a steady state is
D ∇²n = −S_eff δ³(x), so at large r

```text
n(r) = S_eff / (4π D r) = 9 S_eff / (16π r)       quanta per Node,
Φ(r) = −D ∇n = S_eff / (4π r²) r̂                  Link current per Link,
J(r) = (11/8) Φ(r) = 11 S_eff / (32π r²) r̂        net momentum arriving per Node per interval.
```

The content per Node falls as 1/r with the coefficient 9S_eff/(16π); the
Link current is Gauss's S/(4πr²), as section 1 requires of any surface
once the current is isotropic; and the push a thing takes per interval,
σJ, falls as 1/r² with the coefficient 11 S_eff/(32π) = 0.1094 S_eff. The
limit taken is r ≫ 1.65 Links (the beam gone) and r ≫ the anisotropy
length (below), and a time ≫ r²/D (section 6).

**The effective source.** Under the emitting reading of R3 a thing of
content M releases 6⌊Mρ⌋ per interval, and a fraction f of it walks back to
its own Node and is home (R5: "a shadow meeting its owner is home"). f is a
property of the walk: the probability that the persistent walk started one
Link out on an outward heading ever returns to the origin, which for D = 4/9
in three dimensions is a transient walk's return probability, 0.176 after
1100 intervals in my 97³ iteration of R1–R2 and still rising (the recorded
mean field: 4444/24576 = 0.181 at its steady state). So

```text
S_eff = 6 ρ M (1 − f) ≈ 4.91 ρ M        (emitting reading),
```

and the force constant on the shadows' side is ρ(1 − f): ρ is the declared
input (Highlights 5.5, hypothesis 17), 1 − f ≈ 0.82 is derived. Under the
standing reading of R3 the flux S_eff through a shell is not fixed by X
alone: a diffusive profile has the residence time Σ_x n(x)/S_eff ≈ R²/(2D)
in a box of radius R, so a standing set of total X carries the flux
S_eff = 2DX/R² = (8/9)X/R², which depends on the extent of the declared
profile; and on a closed board a standing set that meets nothing spreads to
a uniform density, whose J is zero. What the force constant is under the
standing reading is therefore the flux its declared profile carries, which
the profile must state; every formula below is written in S_eff.

**Coulomb's law with the sign.** Two things A and B at rest at distance r,
each with shadows of its own family, each with a table of sign σ = sign of
the charge product (the catalog's `electron_field_turn` and its
`opposite_charge` entry; A5s). By R4, B takes per interval σ J_A(B) from A's
shadows, and by R5 B's register also changes by the returns of B's own
shadows that pushed A, −σ J_B(A), the two being opposite in direction
(r̂_AB against r̂_BA). With N_A and N_B the number of Nodes of each thing at
which a receiver stands (one receiver per Node per interval, R4) the net
push on B per interval is

```text
F_B = σ (11/(32π r²)) [ N_B S_A + N_A S_B ] r̂_AB,       F_A = −F_B,
```

equal and opposite once the returns are home (section 4), like charges
apart and opposite charges together by σ, inverse square by section 5's
J. The coefficient is the sum of the two fluxes weighted by the receivers,
not a product: for two external bodies of equal release the force is
σ·(11/(16π r²))·S, and for unequal releases (S_A ≠ S_B) it is proportional to
S_A + S_B, whereas Coulomb's is proportional to q_A q_B. With S = 6ρM(1 − f)
and g_i := N_i/M_i (receiver Nodes per unit of content),

```text
F_B = σ (33 ρ (1 − f) / (16π r²)) (g_A + g_B) M_A M_B r̂_AB.
```

The product law q_A q_B is recovered exactly when g_A + g_B is the same for
every pair, which holds if every thing is made of unit-amount rays each at
its own Node (g = 1) or, for charge, when the release ratio of each family
scales so that ρ_family·M is the charge magnitude; and it fails for an
external body (g = 1/M → 0) against matter. The catalog's charge (−3 for the
electron, +3 for the proton, in thirds of e) does not enter the magnitude:
the momentum table declares a sign only, so a thing of charge 2e takes the
same push per shadow quantum as a thing of charge e, and the proton's
Coulomb field, released from a content 1836 times the electron's at the same
ρ, would be 1836 times stronger. The model owner's option "a declared
amount" for the shadow set (Highlights 5.4) is the one under which the
strength is independent of content, that is, under which charge is not
mass.

**The lattice anisotropy.** Two terms make the field at a Node depend on the
direction to the source. (i) The beam: the share of a release that has never
scattered walks the axis line at one Link per interval and falls as
X_h (6/11)^{r−1} (R1's forward weight, one Link per interval by R2), an
exponential of length 1.65 Links that lives on the six axes only; it is
39 % of the push at b = 4 and 1 % at b = 16 in A6's construction and
explains the short-range axis-over-diagonal excess of both A5s (0.16 to
0.48 at Euclidean 4.2 to 11.3) and A6 (0.49, 0.59, 0.71 at 4.24, 5.66,
8.49). (ii) The order-k⁴ term of section 2. Writing 1 − λ₀ = Dk² + aΣkᵢ⁴ +
b(k²)² with a = −58/81, the steady state n̂ = S_eff/(1 − λ₀) expands as
S_eff/(Dk²) − S_eff (aΣkᵢ⁴ + bk⁴)/(D²k⁴) + …; the b term and the isotropic
part of the a term are constants in k, hence local (a δ-function at the
source), and the anisotropic part is the cubic harmonic K₄(k̂) = Σk̂ᵢ⁴ − 3/5,
whose Fourier transform in three dimensions is 15 K₄(r̂)/(8π r³) (checked:
Σᵢ∂ᵢ⁴ r = −15 K₄(r̂)/r³). Hence the far field is

```text
n(r, r̂) = (9 S_eff / 16π r) [ 1 + (145/12) K₄(r̂) / r² + O(1/r⁴) ],      K₄ = Σᵢ r̂ᵢ⁴ − 3/5,
Φ_r(r, r̂) = (S_eff / 4π r²) [ 1 + (145/4) K₄(r̂) / r² + O(1/r⁴) ],
```

with K₄ = +2/5 on an axis, −1/10 on a (110) diagonal and −4/15 on a (111)
diagonal. The force is stronger on the axes than on the diagonals at the
same distance by the relative amount (145/4)(2/5 + 1/10)/r² = 18.1/r² on
(110) and (145/4)(2/5 + 4/15)/r² = 24.2/r² on (111): 9 % and 12 % at
r = 14, 2 % and 2.6 % at r = 30, 0.5 % and 0.7 % at r = 60. The anisotropy
of the diffusive field decays as 1/r², it does not vanish at any finite r,
and off the axes and diagonals the force is not central: the tangential
component is −(145/12)(∂_θ K₄)/r² of the radial one. (The simple walk's
coefficient would be 15/(2·72)/(1/6) = 5/8 in place of 145/12: the persistent
table is nineteen times more anisotropic at the same r, the price of its
longer forward memory.)

**Dictionary.** S_eff ↔ 4π × (the source strength q/ε₀ or 4πGM); n ↔ field
energy density (∝ 1/r); Φ ↔ E (∝ 1/r²); σJ ↔ the force on a unit receiver;
11/(32π) ↔ the Coulomb constant per unit flux.

**Check.** The mean field of A5s: the current is 1.05, 1.03, 1.02 of Gauss
on the axis at r = 24, 32, 48 and 0.93, 0.97, 0.98 on the (111) diagonal at
13.9, 20.8, 27.7; the formula above gives the axis-over-(111) ratio
1 + 24.2/r² = 1.056 at r = 21 and 1.031 at r = 28 against the mean field's
1.06 and 1.04 (the same sign, the same order, the axis residue larger than
the k⁴ term alone by about a third at these r, where the k⁶ terms and the
box are not negligible). The density coefficient: my 97³ iteration gives
n·r = 0.68, 0.56, 0.39 at r = 12, 16, 24 for a unit release per heading,
against 9S_eff/(16π)·(1 − r/R) = 0.66, 0.59, 0.44 with the box's absorbing
wall at R = 48 (E11's per-Node profile has the exponent −1.13 to −1.17
near the source and its radial momentum per Node −2.0 from k = 2). The
local exponent of J in free space reaches −2.0 ± 0.1 from r ≈ 26; the
recorded runs' windows (r ≤ 16 in A5s Run 1, r ≤ 20 in Run 2) read the
beam and the approach, not the asymptote, as their entries state.

**Verdict.** The inverse square: **reached** at r ≫ 2 Links, with the
constant 11 S_eff/(32π) derived and S_eff = 6ρM(1 − f) with ρ an input.
Coulomb's sign: **reached** (σ). Coulomb's product law q_A q_B:
**different law** as the catalog stands, F ∝ (g_A + g_B) M_A M_B, a sum of
the two fluxes; the run that shows it is A5s with unequal releases (A at ρ,
B at ρ/4: Coulomb's product predicts 1/4 of the equal-release force, the
model (1 + 1/4)/2 = 5/8 of it after the returns, and 1 on B against 1/4 on A
before them). The anisotropy: **new**, K₄(r̂)(145/4)/r² of the force plus the
beam e^{−r/1.65} on the axes, testable by A5s in dense mode at r = 24 on
the axis against (110) at the same Euclidean r (predicted ratio 0.969).

## 6. The continuum limit of the spread step: diffusion, not waves

**Rules used.** R1, R2 and section 2.

**The equation.** Section 2 gives, for the content of shadows,

```text
∂n/∂t = D ∇²n,   D = 4/9 Link² per interval,
```

with the k⁴ corrections stated there, and not ∂²n/∂t² = c²∇²n. At the
scale of a few Links the six-component system is a telegraph equation: the
momentum mode relaxes at the rate ln(11/5) per interval (τ = 5/6 intervals
from 1 − 5/11), so a front travels at √(D/τ) = √(8/15) = 0.73 Links per
interval for about one interval and then diffuses; the beam alone keeps
the causal speed, on the axes, with the weight (6/11)^r. What physics
calls the propagation of light at c is, in the model, not the field's but
the thing's: a light thing moves whole on its line at one Link per interval
(law of the bit, point 2), and the wave equation is not needed for it.

**The time to establish the field.** For a source switched on at t = 0 the
diffusion equation gives n(r, t) = (S_eff/4πDr) erfc(r/2√(Dt)) and the
radial current Φ(r, t)/Φ(r, ∞) = erfc(z) + (2z/√π) e^{−z²}, z = r/(2√(Dt)).
The push on a thing at r (J = 11/8 Φ, the same ratio at every Node) reaches
90 % of its steady value when z = 0.5405, that is at

```text
t₉₀ = r² / (4 D z₉₀²) = 1.925 r²  intervals      (t₅₀ = 0.475 r²,  t₉₉ = 9.80 r²),
```

∝ r², the retardation of a diffusing field, against r/c = r for a wave. The
lattice approaches this from below because the first quanta arrive by the
beam at t = r and the walk is ballistic for its first 1.3 Links.

**What a phase-steered split would need.** The open item of Highlights 3.5
asks for a wave equation from a split steered by phase. From section 2: a
wave needs two undamped modes at k → 0 with symbol e^{±iω(k)}, ω ≈ c_w k.
(i) On amounts alone it is impossible: any table of non-negative weights
is stochastic and has one Perron mode; a second eigenvalue of modulus 1
means either a second conserved quantity per heading (w_f = S: no
scattering, the six axis lines of the E6 geometry, ballistic but not a wave)
or an eigenvalue −1 (a period-two flip, not propagation). (ii) With the
phase as a second variable, the linearised one-interval map on the twelve
numbers (amount, phase) per heading must have a conjugate pair on the unit
circle at k → 0; the coherent sum of Highlights 3.20 combines phases but
leaves the amounts' map stochastic, so a uniform static shadow set stays
diffusive under it. (iii) A steering that reads a phase difference can
drive amounts ballistically only where a phase gradient exists along the
path, and a family of rate 0 (light) whose emitter's clock is constant has
none: all its shadows carry one phase (R7). A wave equation for the field
of a static charge is therefore not reachable by steering as the phase is
declared; a source whose clock advances (rate r ≠ 0, or a time-varying
emitter) gives its shadows the phase r·(t − s) along paths of length s, the
gradient the steering could read. Whether such a steering yields ω = c_w k
is a computation on the declared table, not made here.

**Check.** The mean field of A5s: t₉₀/r² rising to 1.53 at r = 32 against
1.93; t₉₀ ∝ r^2.29 over r ≥ 12 (the near r the beam's); "the field is
diffusive, not ballistic". E11: the transient flux through the L1 shells
after 192 ticks, 99.7, 96, 86 and 68 % of S at k = 7, 12, 16, 22, against
erfc(z) + (2z/√π)e^{−z²} at D = 4/9 evaluated at the shells' mean Euclidean
radius 0.70 k: 0.99, 0.94, 0.86, 0.71.

**Verdict.** The diffusion equation with D = 4/9: **reached exactly** as the
continuum limit. Maxwell's wave equation for the field: **not reached**, and
not reachable from any non-negative split; what a phase-steered split must
do is stated. t₉₀ = 1.925 r²: **new** (a retardation law ∝ r², the run any
switched-on source read at two r; A5s Run 2 at r = 24 and 32 would read it
directly).

## 7. E = mc²

**Rules used.** Highlights 3.4 ("mass is the retained energy of a bound
group"), 3.28 ("its mass is its content"), the law of the bit point 9 ("a
thing's content is mass"), the invariant `energy` = amount of every
coupling (catalog `units.amount`; the `corner`, `absorb` and
`photofission` rules of examples/nature), c = 1 (R2).

**The identity.** The mass of a thing is its content m (an integer number
of quanta); the energy every meeting conserves is the amount; a light thing
born at an event carries an amount. So for every thing, at rest or moving,

```text
E = m       (quanta),     and in physical units E = m c²  since c = 1 Link per interval.
```

**What an emission converts.** A meeting whose table has a light output of
amount ΔE (E2's emission, E3's photofission) takes ΔE from the content of
the group and puts it on the light thing, the invariant `energy` exact:
Δm_group = −ΔE. The rate is one such conversion per meeting at which the
declared table fires, that is at most once per interval per corner of the
loop (Highlights 3.4, loop-binding); a free thing never emits (Highlights
3.26: no event without a meeting). The frequency the light carries is the
emitter's phase rate r at the emission (R7), an integer number of steps of
the N-circle per interval, so f = r/N cycles per interval; the amount ΔE and
the rate r are two independent declared numbers, and E = hf is not a
consequence of the rules (A8's "reported and not pinned" clause; section 14).

**Identity or law.** E = m is a units identity: with c = 1 the two names
denote one integer. The physical content of Einstein's relation, that rest
mass is convertible energy and that energy has inertia, splits in the model
into two statements of different standing. That content converts to light
quantum for quantum, exactly, is a law of the rules (the invariant at every
meeting): **reached exactly**. That the energy of motion has inertia is not
in the rules: a moving thing has the same content as at rest (nothing adds
to the amount, R4 changes p alone), its momentum is p = M v capped at M
(section 3), and its energy is m; so the model's energy–momentum relation
is

```text
E = m,   |p| = m v ≤ m,       not  E² = p² + m²  and not  E = m + ½ m v²:
```

a **different law**, with no kinetic energy anywhere in the books. The run
that shows it: a moving external body absorbed by a mark deposits m in the
mark's counter at any v (law of the bit, point 6), and two things colliding
head-on at equal v leave the invariant `energy` unchanged whatever v was.
For a free ray, |p| = m exactly (the default register is amount × heading),
which is the massless relation E = pc for every family, "slow" or not.

**Verdict.** E = mc²: **reached** as an exact units identity plus the law of
exact conversion at every meeting; the energy of motion: **different law**
(E = m for every v, p = mv capped at m).

## 8. Light bending by a mass (A6)

**Rules used.** R1–R5 with the mass field as the shadows' family (Highlights
3.28, "Gravity is bending by delay" as amended by the law of the bit, point
9: the shadow lays no delay; the bending is the push), the sign −1 (always
attraction, the catalog's `mass_field_turn` of A6), section 5's J.

**The push over a pass.** A ray of register p = (p, 0, 0) at speed 1 passes
the source at impact parameter b along x. Per interval it takes −J at its
Node; with the far-field J of section 5 and x = t,

```text
Δp_⊥ = ∫ (11 S_eff / 32π) · b / (b² + x²)^{3/2} dx = (11 S_eff / 32π) · (2/b) = 11 S_eff / (16π b),
```

toward the source, independent of the ray's content, since R4's push is the
shadows' amount times heading and reads nothing of the receiver
("the push reads the field's momentum and nothing of the ray's rate", A6).
Its deflection is the angle of its register (section 3's v = p/|p|₁; for
small angles the register's ratio):

```text
α = Δp_⊥ / p = 11 S_eff / (16π b p)  =  G_L M / (b p),      G_L := 33 ρ (1 − f) / (8π) ≈ 1.075 ρ,
```

with S_eff = 6ρM(1 − f). It is linear in M, inverse in b, and inverse in
the content p of the light thing.

**Against Newton and Einstein.** Newton's corpuscle: α_N = 2GM/(c²b);
Einstein: α_E = 4GM/(c²b), twice Newton's, the second half from the
spatial curvature, and neither depends on the photon's energy. The model's
α ∝ M/b has both forms' dependence on M and b and a coefficient that
depends on p: with the same G_L, a one-quantum photon (p = 1) is deflected
by G_L M/b, one of content p by G_L M/(bp). The model's bending is
chromatic (section 13); a run with the light's amount 2¹⁷ and 2¹⁹ at b = 8
in A6's construction would show α doubled and halved.

**The factor 2 and the light/slow ratio.** A6 measured the ratio 1 between
the light and the slow ray: derived above, since both move at one Link per
interval (the pass takes the same intervals), both take the same Δp, and
both have |p| = amount. Einstein's 2 against Newton comes from two equal
contributions, the time part of the metric (the force) and the space part
(the delay gradient, a refractive index n = 1 + 2GM/(c²r) bends a wavefront
by 2GM/(c²b)). The model has the first (R4) and, since point 9 of the law of
the bit, not the second: a shadow lays no delay. The second would be a
delay per shadow quantum met on the receiver's own axis, spent as a wait
(the `lag_bits` register of Highlights 3.28 in its wait form), and it would
add G_L M/b to α for a ray at speed 1 if the wait per quantum equalled the
push per quantum in the sense of section 11 (c); for a slow thing (an
external body at v ≪ 1) the push part is α = G_L g M/(b v²) (the pass lasts
1/v longer, p = Mv) while a delay part is v-independent, so the ratio
light/slow → 2 only in the limit v → 0 of the Newtonian part, exactly as in
general relativity's (1 + v²/c²) factor. None of this is in the rules
today: it is what a rule would have to be.

**Dictionary.** α in radians ↔ atan of the register's ratio; b in Links;
M in quanta; G_L in Link³/(quantum·interval²).

**Check.** The mean field of A6 in free space (an octant of half-width 96):
α = 0.001357 and 0.000981 at b = 24 and 32 for M = 2²⁸, ρ = 2⁻¹⁵, p = 2¹⁸;
the formula, 11 S_eff/(16π b p) with S_eff = 6·8192·(1 − 0.181) = 40 262,
gives 0.001401 and 0.001050, and with the octant's cut tails
(1 − 96/√(96² + b²) per side) 0.001359 and 0.000996: within 0.1 % and 1.6 %.
At b = 4, 8, 16 the mean field is 1.70, 1.25, 1.03 times the formula (the
beam and the anisotropy, section 5), which is the "approaches −1 from
below" of A6's entry. The engine's integers reproduced that mean field
within 1.4 % at every b (A6, measured).

**Verdict.** The form α ∝ M/b: **reached** at b ≫ 2 Links. The coefficient:
**different law**, α = G_L M/(b p), inverse in the photon's content and
equal to the Newtonian coefficient only for p = 1 with G = G_L/2 in the
convention of section 10; Einstein's 4GM/(c²b) **not reached** (no delay
gradient in the rules; what one would need is stated).

## 9. Time dilation and the clock of a moving loop

**Rules used.** Highlights 3.4 (a bound group is a periodic orbit on a
ring), 3.28 ("nothing slows a clock because of motion: there is no kinematic
rule"), 3.3 (the phase advances at the rest rate per Link), R6 for a loop
(the corner table, `loop-binding-v1`), R2 (one Link per interval, every
ray), hypothesis 15.

**The clock at rest.** On the unit square (L = 4 Links, 4 Nodes) the rest
orbit has period P₀ = 4 intervals: every ray walks the four Links of the
ring and is back; its phase has advanced 4r, so the state repeats after
T = L N/gcd(L r, N) intervals and the pattern of Nodes, headings and phase
differences after L. The clock of the group is the period of its loop
(Highlights 3.4).

**A moving loop, from step counting alone.** A loop moving at v = 1/k Links
per interval along +x is a pattern that repeats after P intervals shifted
by Pv Links (an integer). Every ray takes exactly one lattice step per
interval (R2), so over one period a ray takes P steps, of which
n₊ₓ − n₋ₓ = Pv are the net drift and the rest, P − Pv at least (more if it
ever steps −x), are the steps of its internal circuit. If the moving orbit's
internal circuit needs L_int steps per period (L_int = P₀ = 4 at rest),

```text
P (1 − v) ≥ L_int(v),     so the clock rate      P₀ / P  ≤  (1 − v) · P₀ / L_int(v).
```

The factor 1/(1 − v) is derived: it is the cost of the drift in a world
where every ray spends every interval on one Link. L_int(v) is not: the
moving orbit is a different periodic orbit of the corner table, not yet
constructed ([loop binding](LOOP_BINDING.md#8-motion-of-a-loop-as-a-whole)),
and it may need more steps than the rest orbit (extra −x steps, each
costing two) or, conceivably, fewer. With L_int = P₀ the rate is 1 − v,
hypothesis 15's curve.

**Against the Lorentz factor.** Nature's rate is √(1 − v²) =
(1 − v)·√((1 + v)/(1 − v)). To match it the lattice would need
L_int(v) = P₀ √((1 − v)/(1 + v)) = 2.31, 2.83, 3.10, 3.53 steps at
v = 1/2, 1/3, 1/4, 1/8 for P₀ = 4: not integers, and smaller than the
rest circuit. So no orbit with an integer internal circuit gives the
Lorentz factor exactly at these v; the model's own law is P₀(1 − v)/L_int(v)
with an integer L_int(v) ≥ some minimum, a staircase in v.

**The preferred frame.** v is counted in Links per interval against the
lattice, and the step count is absolute: a loop at rest on the lattice is
distinguishable from one that moves, the slowing is not reciprocal (the
moving loop sees the resting one's clock fast), and the drift cost is
|v|₁ = |vₓ| + |vᵧ| + |v_z|, not the Euclidean speed: a loop moving along a
(110) diagonal at Euclidean speed u pays 1 − √2·u. The lattice frame is a
preferred frame in the plain sense, and Lorentz invariance is not a symmetry
of the rules (section 14).

**Check.** A14 is planned and not run; E5's ring has period 4 and clock 2
per interval on the 8-step circle at r = 2 (T = 4 by L r = 0 mod N), as the
formula gives.

**Verdict.** Time dilation: **not reached** as the Lorentz factor; the
rules give the bound rate ≤ (1 − v)·P₀/L_int(v) with the drift factor 1 − v
derived and the moving orbit open. **Different law** if the moving orbit
keeps L_int = P₀: 1 − v, direction-dependent, in a preferred frame; the run
is A14 once a moving loop exists (v = 1/2: 0.500 against 0.866).

## 10. G and the units

**Rules used.** Hypothesis 12 (m₀ = h/(N δt c²), one phase step per interval
as the unit of mass), hypothesis 14 (G = ħc/(N m₀)²), the A6 status text,
Highlights 3.28 and 5.5. These are declared identifications, not Node rules;
this section derives their consequences only.

**Two choices of m₀.** In lattice units c = 1 (Link per interval) and
δt = 1.

- m₀ = h/(N δt c²) (one step of the N-circle per interval). Then the unit of
  action m₀c²δt is h/N, so h = N and ħ = N/(2π) in (m₀, Link, interval)
  units, and G = ħc/(N m₀)² = (N/2π)/N² = 1/(2πN): G_eff·N is constant
  (1/2π = 0.159), not G_eff·N².
- m₀ = ħ/(δt c²) (one radian per interval). Then ħ = 1 and G = 1/N²:
  G_eff·N² is constant (= 1).

So the model must choose m₀ = ħ/(δt c²) for the N² constancy of hypothesis
14 and m₀ = h/(N δt c²) for N constancy; the two differ by the factor 2π
between a step of the circle and a radian, and hypothesis 12's ladder is
written in steps. This is the identification A6's fail clause names.

**What the engine measured.** A6's register is the same at every N (a push
has no modulus, section 3), so G_eff is N-independent and neither product
is constant: the N² constancy of the earlier test came from scaling the mass
with N. In the derivation of section 8, G_L = 33ρ(1 − f)/(8π) contains ρ and
f and no N at all: N enters the strength of gravity only through the
declared identification of m₀, never through a Node rule. With the
convention G_eff := αb/(4M) of A6 and section 8's α, G_eff = G_L/(4p) =
33ρ(1 − f)/(32π p): a number of the release ratio and the test ray's
content.

**The Planck length under each choice.** Taking the identifications at
their word, ℓ_P² = ħG/c³ = (N/2π)(1/2πN) = 1/(4π²) under the first choice,
so the Planck length would be Link/(2π) for every N, and ℓ_P = Link/N under
the second; and m_P = √(ħc/G) = N m₀ under both, as hypothesis 14 says.
These are consequences of the hypotheses, stated so that a run at the real
N (A11) can read them; they are not derived from the operator.

**Verdict.** G's value: **not reached** (an input through ρ, Highlights 5.5,
hypothesis 17). G_eff·N² versus G_eff·N: **reached** as a statement about
units: N² needs m₀ = ħ/(δtc²), N needs m₀ = h/(Nδtc²), and the engine's
coupling depends on neither (G_eff constant, A6). ℓ_P = Link/(2π) or Link/N:
**new** as a consequence of the declared identifications.

## 11. Gravity on a quantum

**Rules used.** R1–R6 with the mass field as the shadows of every thing
(law of the bit, points 9 and 12: a thing's content is mass and its shadows
are of its own family; the mass field's coupling always attractive, σ = −1,
the catalog's `mass_field`), the integer form of R1 (the registers), and
sections 3, 5, 8.

**(a) The bending of one photon as a discrete process.** The field is the
same operator as Coulomb's with σ = −1 and no charge sign, so the mean push
over a pass is section 8's, Δp_⊥ = 11 S_eff/(16π b) = G_L M/b. The pushes
themselves are integers: at a Node a light thing takes −Σ_h a(x, h) h, the
whole quanta present. Far out, whole quanta are rare: the content per Node
is n(r) = 9S_eff/(16π r), below one quantum beyond

```text
r_γ = 9 S_eff / (16π)      (3605 Links for S_eff = 20 132, E11's source),
```

and there a Node holds a quantum in a fraction n(r) of the intervals, most
of them on one heading. The mean deflection is the sum of the pushes' means
(the register rule is exact on average): ⟨Δp_⊥⟩ = G_L M/b for any p. Its
variance is bounded by the two extremes of the register rule. If the quanta
arrived independently, the number met with a transverse heading over a pass
of length 2ℓ would be about (1/3)Σ_x n(x) = (3S_eff/(8π)) ln(2ℓ/b) and each
would push ±1, so Var(Δp_⊥) ≤ (3S_eff/8π) ln(2ℓ/b); since the registers
release whole quanta at regular intervals under a steady inflow (an
accumulator, not a lottery), the true variance is smaller, down to O(1) per
register along the line. For a one-quantum photon (p = 1) a single
transverse push turns the register from (1, 0, 0) to (1, ∓1, 0), a turn of
45° by the DDA (section 3), so its deflection is not small: at
b ≫ G_L M the photon is turned with probability about G_L M/b by 45° and
otherwise not at all, a mean angle of (π/4)·G_L M/b and a variance
(π/4)²·(G_L M/b)(1 − G_L M/b); at b < G_L M it takes more than one net
quantum and turns by more than 45°, that is, the capture radius of a
one-quantum photon is

```text
b_c = G_L M / p    (p = 1: b_c = G_L M, the model's "gravitational radius" for light),
```

against the 3√3 GM/c² = 5.2 GM/c² of general relativity, and inverse in the
photon's content. **New**: the bending of a photon is a Bernoulli-like
whole-Port event with probability G_L M/b, sub-Poissonian in its counts;
the run is A6's construction with light of amount 1 at b from 2 to 64 and
the deflection read as the register per pass over many passes (the mean
against G_L M/b, the fraction of passes turned, and the variance against
the two bounds).

**(b) Two things at rest and the escape velocity.** For two external bodies
(section 5, σ = −1) F = −(11/(32π r²))(N_B S_A + N_A S_B) r̂, and with R6
(v = p/M) the equations of motion in the limit of many Links and periods
long against r²/D (section 6, so the field is quasi-static) are Newton's:

```text
M_B d²x_B/dt² = − (G_L/2) (g_A + g_B) M_A M_B r̂ / r²,     g = N/M as in section 5,
```

with the derived first integral ½ μ v² − (G_L/2)(g_A + g_B) M_A M_B/r =
const (a constant of the trajectory, not a booked quantity: the books hold
no kinetic energy, section 7). Kepler's orbits follow in that limit with
G_N = (G_L/2)(g_A + g_B): for matter of g = 1 on both sides, G_N = G_L; for
an external body against unit-ray matter, G_L/2; and the equivalence
principle (the acceleration of B independent of M_B) holds iff g_B is the
same for all matter, which the rules do not fix (an external body has
g = 1/M, the E5 ring 4 receiver Nodes for content 8, unit rays at distinct
Nodes 1). The escape velocity in lattice units,

```text
v_esc = √( (G_L (g_A + g_B) M_A) / r )     Links per interval,   valid where v_esc < 1,
```

and the radius where it reaches the cap of section 3 (|v|₁ ≤ 1),
r_cap = G_L (g_A + g_B) M_A: inside it a thing at rest cannot be given the
momentum to leave, because the register is capped at its content; a
Michell–Laplace dark body, derived from the accumulator's cap and not from
curvature. The retardation of section 4 and 6 adds a condition no Newtonian
orbit has: the field and the recoil settle over r²/D intervals, so an orbit
of period P ≪ 2r² feels a field that lags, and the third law's reaction
arrives over s₅₀ = 2.47 r². **Reached** (Newton's two-body problem, with
G_N = (G_L/2)(g_A + g_B)); **different law** in the g's and in the
retardation; the runs: A7 with the bodies' contents and ring structures
varied, and any orbit with P comparable to 2r².

**(c) Gravitational time dilation.** Highlights 3.28 says content slows a
Node's output clock; point 9 of the law of the bit says a shadow "has no
mass, no clock and no delay". The shadows of a nearby mass at the Nodes of a
loop therefore delay nothing, and the loop's rays are pushed (R4) but not
slowed: as long as the ring holds (the pushes small against the rays'
registers so that the DDA keeps the ring's Ports), the period is P₀ and the
clock runs at its rest rate whatever the mass field's density n(r). **Not
reached**: no gravitational time dilation under the present rules; the
model gives zero, against 1 − GM/(rc²). What would give it, in the form of
the rules: a wait of w intervals per shadow quantum met on the ray's own
axis (the wait form of the lag register, Highlights 3.28, forbidden by point
9 as it stands). Then the period of a loop at distance r from a mass M would
be P = P₀(1 + w·n(r)) with n = 9S_eff/(16π r) = 27ρ(1 − f)M/(8π r), so

```text
P/P₀ − 1 = w · 27 ρ (1 − f) M / (8π r)  =  (9 w / 11) · G_L M / r,
```

the form 1 + GM/(rc²) of general relativity, with the same constant as the
force law (G_L) exactly when w = 11/9 intervals per quantum met: the
force's factor 11/8 (section 1) over the density's 9/8. A wait rule with
that coefficient would make the two faces of gravity, the push and the
clock, one table; nothing in the model fixes it. Once a loop falls, the
kinematic bound of section 9 applies with v = v_esc(r): a loop falling
from rest at infinity has its clock at most (1 − √(G_L (g_A + g_B) M/r)) of
the rest rate, a square root in M/r where nature has a linear term, and
nothing for a loop held at rest.

**(d) A gravitational atom.** A loop in the sense of Highlights 3.4 is
closed by the corner table, not by a field. What the mass field alone can
hold is an orbit of a thing around a mass: for a free ray (speed 1,
register of length p) a circle of radius R needs a turn of 1/R radians per
Link, that is |Δp| per interval = p/R, and with J(R) = 11 S_eff/(32π R²)
that gives one radius,

```text
R_c = 11 S_eff / (32π p) = G_L M / (2 p)       (the photon circle; 3GM/c² in general relativity),
```

a DDA staircase of a circle, which exists on the lattice only if
R_c ≥ 1 Link, that is M ≥ 2p/G_L (6.1·10⁴ quanta for p = 1 at ρ = 2⁻¹⁵), and
whose pushes must be integers, one quantum per interval at R_c = 1. For a
slow thing (v = p/M < 1, R6) the circle is Kepler's, v² = G_N M/R, at any R.
Nothing selects discrete radii: no rule reads a phase in the push, so the
orbits form a continuum and there is no level structure; the smallest
content that orbits is any content (Kepler's independence of the test mass,
given a common g). **Not reached**: a gravitational atom with levels; the
orbits themselves **reached** in the continuum limit, with the model's own
smallest circle R_c = G_L M/(2p) **new**; the run is E8's construction with
the mass field in place of the charge, a ray launched tangentially at R
from 1 to 8 Links from a body of M ≥ 2p/G_L.

## 12. The ladder of masses

**Rules used.** Highlights 3.4 (a bound group is a periodic orbit of the
meeting table on a ring; only the contents and phases that close a loop
exist); the `corner` rule of `examples/nature/ring.json`, the Port form
(each input's amount and phase leaving through the Port the other came in
by; [E5](EXPERIMENTS.md#e5-the-ring-an-electron-at-rest-as-a-loop)), and the
catalog's `born_steering` as the alternative corner table (the Born form,
T[d] = round(N cos²(πd/N)); [loop binding](LOOP_BINDING.md#3-closure-as-integer-equalities));
R2 and R7; hypothesis 12; experiment A10 (planned, not run).

**The corner map.** A ring is a rectangle a × b Links, L = 2(a + b), with
corners at arc positions 0, a, a + b, 2a + b; a ray's state is (sense
R or L, arc position, amount, phase). Each interval every ray moves one arc
step in its sense and its phase advances r (R2, R7). Where two rays of
opposite sense stand at one Node the table acts:

```text
Port form:  (a₀, φ₀), (a₁, φ₁)  →  (a₀, φ₀) out through the Port input 1 came in by,
                                    (a₁, φ₁) out through the Port input 0 came in by:
            the identity on (amount, phase); a quarter turn at a corner, straight on at a side Node.
Born form:  s = a₀ + a₁, d = φ₀ − φ₁ mod N;  ⌊s·T[d]/N⌋ continues in input 0's sense with φ₀,
            s − ⌊s·T[d]/N⌋ in input 1's sense with φ₁;  input 0 the lower heading index.
```

The loop's evolution over a period is the iterate of this map with the
walk. The exact condition for a bound group is that the state (all rays'
Nodes, headings, amounts and phases modulo N) repeats: a fixed point of the
iterate. Presence is required at every corner (a lone ray fires no rule and
crosses off the ring), so the ring a × b carries (a + b)/gcd(a, b) rays per
sense spaced 2 gcd(a, b) Links.

**Closure under the Port form.** The map is the identity on amounts and
phases and the geometry reproduces the headings, so the pattern repeats
after L intervals for every amount of every ray; the phase repeats when
L·r ≡ 0 (mod N), and otherwise the state period is T = L N/gcd(L r, N) with
the pattern of Nodes, headings and phase differences already periodic with
period L (nothing reads an absolute phase). So under the Port form every
content c ≥ the number of rays closes, at every rate r, on every ring:
**no ladder, mass free**, exactly hypothesis 12's negative case as the
design states.

**Closure under the Born form.** Equal amounts on the two senses are
reproduced at a corner iff ⌊2a·T[d]/N⌋ = a, that is T[d] = N/2, d = N/4 or
3N/4 (the senses in quadrature), for every a: the contents 2·(a + b)/g·a,
every multiple of the ray count, again no ladder in content. A zero output
at any meeting disperses the ring. What remains is whether unequal amounts
or other d close as longer periodic orbits (the amounts alternating between
the senses from corner to corner); that is what the enumeration below
reads.

**The enumeration.** My own iteration of the map above (not the engine),
over the rings 1 × 1 (L = 4, 4 rays), 1 × 2 (L = 6, 6 rays), 2 × 2 (L = 8,
4 rays) and 1 × 3 (L = 8, 8 rays), the amounts equal within a sense and
from 1 to 8 (Port form) or 1 to 24 (Born form), so contents up to 32 or 64
(Port) and 96 or 192 (Born) per ring, every phase difference d for N = 8, 16
and 64 and every 64th d with the quadratures for N = 4096, the rest rate
r = 1 for the Port form and r = N/L for the Born form (so that the phase
closes in one circuit and the amounts' period is read alone):

| Ring (L, rays) | Table | N | Closing phase differences d | Amounts that close | Period of the state |
| --- | --- | --- | --- | --- | --- |
| 1 × 1 (4, 4) | Port | 8, 16, 64, 4096 | every d (not read) | every (a_R, a_L), all c ≥ 4 | T = 4N/gcd(4r, N): 8, 16, 64, 4096 at r = 1 |
| 1 × 2 (6, 6) | Port | 8, 16, 64, 4096 | every d | every amount, all c ≥ 6 | 24, 48, 192, 12288 at r = 1 (gcd(6, N) = 2) |
| 2 × 2 (8, 4) | Port | 8, 16, 64, 4096 | every d | every amount, all c ≥ 4 | 8, 16, 64, 4096 at r = 1 |
| 1 × 3 (8, 8) | Port | 8, 16, 64, 4096 | every d | every amount, all c ≥ 8 | 8, 16, 64, 4096 at r = 1 |
| 1 × 1 (4, 4) | Born | 8 | 1, 2, 3, 5, 6, 7 (not 0, 4) | every (a_R, a_L) with 0 < ⌊s·T[d]/8⌋ < s, s = a_R + a_L: every even c from 4 to 96 | 4 |
| 1 × 1 (4, 4) | Born | 16 | 1 to 7, 9 to 15 (not 0, 8) | the same rule: every even c | 4 |
| 1 × 1 (4, 4) | Born | 64 | 2 to 28, 36 to 62 (not 0, 1, 63; not 29 to 35 at s ≤ 48) | every even c | 4 |
| 1 × 1 (4, 4) | Born | 4096 | every sampled d but 0 and 1920 to 2176 at s ≤ 48; 1023, 1024, 1025 among them | every even c | 4 |
| 2 × 2 (8, 4) | Born | 8, 16, 64, 4096 | as the 1 × 1 ring | every even c from 4 to 96 | 8 |
| 1 × 3 (8, 8) | Born | 8 | 1, 2, 6, 7 | every multiple of 4 from 8 to 192 | 8 |
| 1 × 3 (8, 8) | Born | 16 | 1 to 5, 11 to 15 | every multiple of 4 | 8 |
| 1 × 3 (8, 8) | Born | 64 | 2 to 23, 41 to 62 | every multiple of 4 | 8 |

What the Born rows show: at d = N/4 or 3N/4 equal amounts stay equal, as
the algebra says; at every other closing d the pair (a_R, a_L) becomes
(⌊s·T[d]/N⌋, s − ⌊s·T[d]/N⌋) at one corner and, since the input-0 role
alternates around the ring and T[d] = T[N − d], the same two amounts swap
senses at the next corner, so the amounts alternate with period 2 and the
state repeats after one circuit: a periodic orbit, hence a bound group by
Highlights 3.4, for every s at which the floor leaves both outputs nonzero
(d away from 0 and N/2 by more than the resolution of s·T/N). The ring
disperses only where ⌊s·T[d]/N⌋ is 0 or s. The 1 × 2 ring has no r with
6r = 0 mod N for these N and was read under the Port form only.

The contents c ≤ 4096 are not listed one by one because the sets have a
closed form: under the Port form every c from the ray count up, at every r
(the phase period T = L N/gcd(L r, N) listed above), and under the Born form
every multiple of the ray count at the quadratures, plus the alternating
orbits the table shows, whose contents are again every value the amounts
admit. The ratios of the members are therefore all rationals: no mass ratio
is predicted.

**Verdict.** The ladder: **not reached**. Under the catalog's tables as they
stand (the Port form of the corner, the Born form as the alternative) every
content closes: the ladder of hypothesis 12 needs a corner turn produced by
the group's own field with a table proportional to what is met
([loop binding](LOOP_BINDING.md#7-the-ladder-and-how-a10-counts-it)), which
is open. This is a derivation A10 would confirm by counting the same sets
on the same tables; the statement is exact, not sampled, for the Port form
and for the quadrature of the Born form, and enumerated for the rest.

## 13. What the lattice says that the textbooks do not

Each item is a formula derived above, with its limit and the run that would
test it; each is marked new: not in known physics.

1. **The force is not central and not isotropic, by a fixed harmonic.**
   δF/F = (145/4) K₄(r̂)/r² with K₄ = Σr̂ᵢ⁴ − 3/5, a tangential part
   −(145/12)(∂_θK₄)/r² (section 5); on top of it the axis beam
   X_h (6/11)^{r−1}. Limit: r ≫ 2 Links, the field steady. New: not in
   known physics, testable by A5s in dense mode at r = 24 axis against
   (110) (ratio 0.969) and (111) (0.958), and by the tangential push on a
   body placed at (r, r/2, 0).
2. **The retardation of the field is diffusive.** A source switched on
   establishes 90 % of its push at r after t₉₀ = 1.925 r² intervals
   (t₅₀ = 0.475 r²), not r (section 6). New: testable by A5s Run 2 with the
   push read at r = 24 and 32 tick by tick against erfc(z) + (2z/√π)e^{−z²}.
3. **The reaction is delayed by the shadow's own path.** After a push, the
   owner's recoil arrives on the schedule erfc(r/2√(Ds)): half after 2.47 r²
   intervals, a tail ∝ s^{−1/2} with infinite mean (section 4). New:
   testable by E11 (a) under the law of the bit.
4. **The far field is granular and sub-Poissonian.** Beyond r_γ =
   9S_eff/(16π) a Node holds a whole quantum in a fraction 9S_eff/(16πr) of
   its intervals; the quanta leave a register at regular intervals under a
   steady inflow, so their counts over a window deviate from the mean by
   O(1) per register, a Fano factor well below 1 where a photon field's is
   1 (sections 0, 11 (a)). New: testable by E11's point source read at a
   far Node over many intervals (the interarrival times and their variance).
5. **The momentum of a thing is an integer identity over its path.**
   p(t) = p(0) + Σ(pushes taken) − Σ(pushes given whose returns are home)
   (section 4), and over a straight pass of a static source at impact
   parameter b the total push is 11 S_eff/(16π b v) = G_L M/(b v), for any
   content of the receiver (section 8). New in the last clause: the push is
   independent of the receiver's content, so a heavier free ray bends less
   (α ∝ 1/p, chromatic bending); testable by A6 at amounts 2¹⁷ and 2¹⁹.
6. **The clock of a moving loop.** Rate ≤ (1 − |v|₁)·P₀/L_int(v), the drift
   factor derived, direction-dependent through the L1 norm, in the
   lattice's frame; a staircase in v with integer L_int; not the Lorentz
   factor for any integer L_int at v = 1/2, 1/3, 1/4, 1/8 (section 9). New:
   A14 once a moving loop exists.
7. **The force is a sum of the two shadow fluxes.** F ∝ (N_B S_A + N_A S_B)
   = (g_A + g_B) M_A M_B ρ(1 − f) (section 5), so the model's "charge" in
   lattice units is the flux S_eff = 6ρM(1 − f) (emitting reading) or the
   flux of the declared profile (standing reading), the receiver counts by
   Nodes, and the constant of the force is 11/(32π) per unit flux; two
   bodies of unequal release repel with a force proportional to their sum.
   New: A5s with unequal releases.
8. **The strength of gravity has no N in it.** G_L = 33ρ(1 − f)/(8π) ≈
   1.075ρ (section 8): the force constant is the release ratio times the
   derived 1 − f, and the phase circle enters only through the declared
   identification of m₀ (section 10), under which ℓ_P = Link/(2π) for every
   N (m₀ = h/(Nδtc²)) or Link/N (m₀ = ħ/(δtc²)). New: A6 at two ρ (the
   register ∝ ρ) and any N (the register unchanged), which A6 has already
   shown for N.
9. **A one-quantum photon is captured at b < G_L M and circles at
   R_c = G_L M/(2p)** (section 11): the model's photon sphere is inverse
   in the photon's content. New: A6's construction with amount-1 light.
10. **The energy of motion is nowhere.** E = m at any v, p = mv capped at
    m (section 7): a fast body absorbed by a mark deposits its rest content
    only. New: any absorption of a moving body at a mark.
11. **A speed that depends on direction.** A free ray with register p moves
    at Euclidean speed 1/|p̂|₁: 1 on an axis, 1/√2 along a (110) diagonal,
    1/√3 along (111) (section 3, R6). The light cone of a thing is the
    octahedron |x|₁ ≤ t. New: a pushed ray timed along a diagonal.

## 14. What cannot be reached from the present rules

- **Maxwell's wave equation** for the field: not from any non-negative
  split (section 6); the field diffuses with D = 4/9, and light in flight
  is a thing, not a field. A phase-steered split would need a conjugate pair
  on the unit circle at k → 0 and a phase gradient along the path, which a
  rate-0 family with a constant emitter clock does not carry.
- **Lorentz invariance**: the lattice frame is preferred (section 9), the
  speed of a thing is fixed at one Link per interval in the L1 norm
  (section 3), momentum is capped rather than γ-scaled, the energy of motion
  is absent (section 7), and no orbit with an integer circuit gives the
  Lorentz factor (section 9).
- **The Born rule** for a thing at two slits: Highlights 3.3 declares the
  cos²(δ/2) : sin²(δ/2) steering as a table; nothing in R1–R7 derives it,
  and under the law of the bit a thing has one path and the shadows carry
  the phases, so what the table steers at a meeting of shadows is amounts
  by declaration. Not derived here or anywhere in the rules.
- **The value of any constant**: G (through ρ and the identification of
  m₀; sections 8, 10), the fine-structure constant (through ρ and the
  table; hypothesis 17), h (E = hf is not a consequence: the amount and the
  rate of an emission are two independent numbers, section 7), the mass
  ratios (no ladder under the present tables, section 12), the lag width N
  (hypothesis 16). The model predicts forms: 1/r², M/b, r², 1 − v, and no
  values.
- **The equivalence principle**: the push is per receiver Node and the
  inertia is the content, so free fall is universal only for matter of one
  common g = N/M, which the rules do not fix (section 11 (b)).
- **Gravitational time dilation and Einstein's factor 2** in the bending:
  point 9 of the law of the bit removes the delay a shadow could lay
  (sections 8, 11 (c)); what a wait rule would need to give both with one
  constant is stated (w = 11/9 intervals per quantum).
- **Coulomb's product law and charge independent of mass**, as the tables
  stand (section 5): a sign table and a release per content give a sum of
  fluxes; the "declared amount" option of Highlights 5.4 is where charge
  would become independent of content.

## 15. The verdicts in one table (round 1; see section 21 for round 2)

| Law | Verdict | Constant or form derived | Run that decides |
| --- | --- | --- | --- |
| Gauss's law (flux) | reached exactly (lattice identity) | S_eff through every closed surface | E11 (done: same S through 22 shells) |
| Inverse square | reached at r ≫ 2 Links | J = 11 S_eff/(32π r²), n = 9 S_eff/(16π r) | A5s Run 2 (done to r = 20, the approach) |
| Coulomb's sign | reached | σ = sign(q_A q_B) | A5s (done) |
| Coulomb's product law | different law: F ∝ (g_A + g_B) M_A M_B | 33ρ(1 − f)/(16π) per unit g | A5s with unequal releases |
| Newton's 2nd law (external body) | reached exactly to one Link | v = p/M, the cap \|v\|₁ ≤ 1 | A5s/A6 accumulators (done) |
| Newton's 2nd law (free ray) | momentum reached; velocity different (v = p/\|p\|₁) | massless kinematics | any pushed ray |
| Newton's 3rd law | reached exactly in the books; delayed by the shadow's path | erfc(r/2√(Ds)), s₅₀ = 2.47 r² | E11 (a) under the law of the bit |
| Diffusion of the field | reached exactly | D = 4/9; k⁴: −58/81, 95/243 | A5s mean field (check) |
| Maxwell's wave equation | not reached, not reachable by a non-negative split | — | — |
| Retardation | new: t₉₀ = 1.925 r² | z₉₀ = 0.5405 | A5s Run 2 tick by tick |
| E = mc² | reached as identity + exact conversion; no kinetic energy | E = m, p = mv ≤ m | a moving body at a mark |
| Light bending ∝ M/b | reached | α = G_L M/(b p), G_L = 33ρ(1 − f)/(8π) | A6 (done) |
| Einstein's 4GM/(c²b) | not reached (no delay gradient) | needs a wait rule | — |
| Achromatic bending | different law: α ∝ 1/p | — | A6 at 2¹⁷, 2¹⁹ |
| Time dilation √(1 − v²) | not reached; bound rate ≤ (1 − v)P₀/L_int | drift factor 1 − v | A14 (needs a moving loop) |
| Preferred frame | different law (lattice frame, L1 speed) | — | a diagonal pass timed |
| G's value | not reached (input ρ) | G_eff N constant for m₀ = h/(Nδtc²), N² for ħ/(δtc²); engine: neither | A6 (done), A11 |
| Two-body problem, escape velocity | reached (Newton) with G_N = (G_L/2)(g_A + g_B) | v_esc = √(G_L(g_A + g_B)M/r) | A7 |
| Gravitational time dilation | not reached (zero) | w = 11/9 would give GR's form | — |
| Gravitational atom | not reached (no levels); orbits reached | R_c = G_L M/(2p) | E8 with the mass field |
| Mass ladder | not reached (every content closes) | T = L N/gcd(L r, N) | A10 |
| Born rule | not reached (declared) | — | A1 |

## 16. The checks, cited

All numbers used as checks come from the dated entries of
[EXPERIMENTS.md](EXPERIMENTS.md) and the computations recorded beside them
(`examples/nature/a5_static/mean_field_gauss.py`, `a6_bending/predict.py`,
`e11_field_books/profile.py`), read after the derivations were made:

- A5s, computed after the run: J = 11/8 Φ at every Node; the outflow equal
  to S to 10⁻⁷; D = 4/9; the density the lattice Green's function scaled by
  3/8; t₉₀/r² → 1.53 at r = 32 against 1.93; the axis and diagonal residues
  of the current; S = 20 132 with 4444 of 24 576 returning.
- A5s Run 2: the engine's push equal to the mean field to 0.08, 0.13 and
  0.18 % at r = 12, 16, 20.
- E11: the flux the same through every shell at the steady state; the
  radial momentum per Node −2.0 from k = 2; the content per Node −1.13 to
  −1.17 near the source; the books closing only with a source line under the
  emitting reading.
- A6: the register 3423, 1661, 862, 269, 93 at b = 4 to 16 (M = 2²⁸, ρ =
  2⁻¹⁵, p = 2¹⁸), the free-space mean field 0.001357 and 0.000981 at b = 24
  and 32; the ratio light/slow 1.0000; G_eff constant over N; the diagonal
  0.49, 0.59, 0.71.
- E5: the ring of period 4, clock 2 at N = 8, r = 2.

My own arithmetic (sympy, mpmath, numpy, seconds each, on the formulas of
this document): the symbol's expansion in exact rationals and its check on
the simple walk; the harmonic identity Σᵢ∂ᵢ⁴ r = −15K₄/r³; the return
fraction 0.176 and the density coefficient in a 97³ iteration of R1–R2; the
DDA staircase 9, 15, 20, 24; z₉₀ = 0.5405; the bending integral 2/b; the
closure enumeration of section 12. None of it ran the engine.

## 17. Round 2: the phase-steered spread as an operator

Round 2 (2026-09-18, after the model owner's decisions of Highlights 5.4
points 16 to 21, PR #273) derives from four amended rules. **R3′, one
shadow set per thing.** A thing of content M has one standing set of
shadows of size X = ξM (ξ declared once, for every family), each shadow
carrying its owner's id, its owner's charge q and content M; there is no
declared X for charge (point 18 restated). **R4′, the two readings**
(point 16): a thing B meeting a shadow of A takes, for the mass reading,
Δp = M_B · a h (σ = −1, always toward A), and for the charge reading
Δp = (q_A / M_A) · q_B · a h with the sign of q_A q_B (+ away). **R6′,
one Link per interval** (point 21): every thing moves one Link per
interval; its register sets the direction only (the DDA of section 3,
v = p/|p|₁, for every thing; the accumulator law v = p/M of section 3 is
superseded). **R7′, the clock** (point 19): a thing at rest advances its
phase by M/K turns of the circle per interval, K one universal constant
(N M/K steps per interval, an integer or a register); light and shadows
have no clock; a shadow carries its owner's phase at release. **R8, the
steered spread** (point 17): at a Node the shares of one owner that arrive
on two or more headings combine by the coherence rule (the amount A = Σ_h
a_h unchanged, the phase that of Σ_h a_h e^{iφ_h}); the phase difference δ
between the directions they came from steers the combined content by the
Born table of 3.3, cos²(δ/2) : sin²(δ/2) as ⌊A·T[δ]/N⌋ with the remainder
owned by the rest Port; shares arriving in one phase from behind continue
forward, shares of differing phase are sent apart; a share meeting no other
share of its owner keeps the fixed split R1. Sections 1 to 16 stand as
round 1; where a round-1 formula changes under these rules, section 21
says so.

**What R8 leaves to declare.** Four things, none derivable, each named
where it enters: (D1) the candidate Ports of a pair are its two
continuations (the words "continue forward" say so; the ring's corner of
section 12 uses the two entry Ports instead); (D2) for a pair of unequal
amounts the table splits the *sum* by δ alone, whereas the coherence rule's
own number, |√a₁e^{iφ₁} + √a₂e^{iφ₂}|², equals A cos²(δ/2) only for
a₁ = a₂ (derived: (2a + 2a cos δ)/(4a) = cos²(δ/2)); (D3) three or more
arrivals; (D4) where "apart" is. The completion used below, C1: the share
C² = |Σ_h a_h e^{iφ_h}|² / A² of every arrival continues on its own heading
(C² = cos²(δ/2) for an equal pair, the table's entry), and the rest
(1 − C²) a_h leaves through the four headings transverse to h, equally.
Every statement marked **(exact)** below holds for any completion that has
in-phase arrivals continue; the rest is C1's.

**The state.** As section 0, plus one phase per (Node, heading) and, for
the derivation, the age s of a share: the number of Links it has walked
since its release. Since a shadow's phase is its owner's at release and
does not advance (R7′), a share of age s at tick t carries φ = φ₀ + ρ(t − s)
with ρ = M/K the owner's rate; so at a Node **the phase difference between
two shares of one owner is ρ times their age difference (exact)**, and on
the lattice every step changes |x|₁ by ±1, so s ≡ |x|₁ − |x₀|₁ (mod 2): ages
at one Node differ by even numbers, δ ∈ {0, 2ρ, 4ρ, …} turns.

**Exact facts, before any completion.** (E1) Continuity and Gauss's law of
section 1 hold unchanged: they used only that the split conserves amount,
and R8 conserves it at every Node. (E2) For a single release every share
has the same age at every tick, so δ = 0 at every meeting: the steering is
the identity and only the lone split acts. (E3) On the light-cone edge
|x|₁ = t of any release, whatever the owner's rate, every arrival came by a
monotone path of length t, so all are in phase: the front is the identity's
front. (E4) An owner of rate 0 (a light thing's mass shadows; any set whose
profile was given with one phase) or of 2ρ ≡ 0 (mod 1) is steered as if
there were no steering. (E5) A thing meeting its own shadow is home (R5):
no push and no steering between a thing and its own field.

**(ii) A point release of one phase: the tube theorem (exact under "in
phase → continue").** Six lone shares X/6 leave the origin; the axis tip
(t, 0, 0) is reached at tick t by one path only, so it is lone at every
tick and keeps (6/11)^t of X/6 on the axis; of what it sheds, 4/11 goes to
(t, ±1, 0), (t, 0, ±1), Nodes of the edge |x|₁ = t + 1, where each share
meets the in-phase content of the line already there and continues, and
1/11 goes back into the interior. So the share of a release that stays on
the light-cone edge for ever is

```text
1 − (1/11) Σ_{t≥0} (6/11)^t = 1 − (1/11)/(1 − 6/11) = 4/5      (exact),
```

and it lives on lines parallel to the axes in the three coordinate planes
through the source: the line y = j (x ≥ 1, z = 0) carries (1/11)(6/11)^{j−1}
X/6 on heading +x, constant in x, and nothing leaves the planes (each tip
feeds only the four Nodes of its own coordinate planes). My iteration of C1
(45³, 20 ticks): the edge fraction 0.9091, 0.8595, 0.8325, …, 0.800002 at
t = 20; the coordinate planes 1.000000 at every tick; the line y = 1 at
1/66 = 0.015152 of X at every tick. The front moves at c on the
octahedron |x|₁ = t, but its content is six tubes of e-folding width
1/ln(11/6) = 1.65 Links in the coordinate planes, the flux through a
shell S_eff on a fixed set of lines: the field per Node on a tube does not
fall with r, and off the planes it is zero. The remaining 1/5 (the tips'
backward shares) is the diffusive residue: in the mean field it meets
in-phase content and continues; in the engine's integers it is lone
wherever fewer than two whole quanta arrive, and there it spreads by R1
with D = 4/9 as in section 2. This is E6's field on lines (Highlights 3.5,
rejected on 2026-09-17), returned by the identity at δ = 0.

**(i) A plane front of one phase.** Content on heading +x at every Node of
a plane: each share is lone at the next plane (6/11 forward, 1/11 back,
4/11 into the plane), and in the plane the four transverse arrivals at each
Node are in phase and continue sideways for ever. The transmitted front is
the lone beam (6/11)^x; the rest is left in planes of sideways streams. A
front of one phase has no phase gradient to read (k = 0), and the in-phase
rule carries content along the *arrival* headings, not along the front's
normal: Huygens' cancellation of the sideways wavelets needs signed
amplitudes, which amounts do not have. **Not a propagating front.**

**(iii) A continuous release from a thing with a clock.** Shares released
at successive ticks have ages that differ, so the field carries the
pattern φ(x, t) = φ₀ + ρ t − ρ s(x), and on the tubes and on every edge
s = |x|₁: the phase is constant on the L1 shells |x|₁ = const, with

```text
λ = 1/ρ = K/M Links   (N/r Links for a step rate r = N M/K),
```

the shell spacing along an axis, λ/√2 and λ/√3 in Euclidean distance
along the (110) and (111) diagonals. In the interior, shares of ages s and
s + 2m meet with δ = 2mρ turns. Under C1 an old share of amount ε at a Node
of young content A (phase difference δ) has 1 − C² = 2Aε(1 − cos 2πδ)/(A + ε)²
(derived from |A + εe^{iδ}|²), so it scatters about 2ε(1 − cos 2πδ) of the
young content per Node it passes; half of what is scattered moves inward
and is old at its next Node, so one old quantum walking home over s Links
breeds about (1 − cos 2πδ)·s old quanta. The pure transport state (all
shares outward, in phase) is therefore a fixed point of C1 that is stable
only out to

```text
r_coh ≈ 1/(1 − cos 2πδ) ≈ 2/(2π δ)² = λ² / (8π²) Links    (δ = 2ρ = 2/λ),
```

and beyond r_coh the field mixes. Under the declared table on the sum (D2)
one quantum of the wrong phase steers sin²(πδ) of the whole Node's content,
the gain is ∝ A/ε, and the transport state is unstable at every r. In the
mixing regime the steering acts as transverse scattering with a fraction p
per step (p = the steady mean of 1 − C², self-consistent, not derived
here), the effective table is [1 − p, 0, p/4, p/4, p/4, p/4], persistence
1 − p, and by section 2's formula

```text
D′(p) = (1/6)·(2 − p)/p Link² per interval     (D′ = 4/9 at p = 6/11; → ∞ as p → 0),
```

with the far field diffusive again. **The continuum limit** is therefore
not one equation: for r < r_coh (and for any single release, E2) it is the
transport equation ∂_t f_h + h·∇f_h = 0 on the six headings (symbol
e^{−ik·h}, six undamped modes with ω_h = k·h, dispersionless, anisotropic:
the content is carried on the axis families), fed by the lone split as a
source at the edges of the support; for r > r_coh it is the diffusion
equation with D′(p); and it is the wave equation in neither: no completion
of R8 on amounts gives ω = c|k| with an isotropic cone, since that needs
the amplitudes' signs (section 6's obstruction, now for the steered map: at
δ = 0 it is a non-negative map, and E3 puts every front at δ = 0). The
class of initial data that propagates ballistically: a release whose
shares meet only shares of their own age (single releases; the edge;
the coherent region of a slow clock).

**t₉₀ under R8.** On a tube, for a switched-on emitter, the content at a
Node is constant once the front has passed: t₉₀ = r + O(1) (exact). Off the
planes and for the residue: t₉₀ = 1.925 r² of the residue's own push
(section 6). In the mixing regime: t₉₀ = 0.856 r²/D′(p) = 5.13 p r²/(2 − p)
for r ≫ 1/p, and ≈ r for r ≪ 1/p. So the model owner's t₉₀ ∝ r is reached
on the tubes and within r_coh, and ∝ r² beyond. Run: A5s Run 2 under R8
with the push read at r = 24 and 32 on an axis, on a (110) diagonal in the
plane, and at (24, 12, 12) off the planes.

**Two slits.** Shadows of one owner through two slits at (0, ±d/2, 0) reach
the screen Node (L, y, 0) with ages L + |y ∓ d/2|, so δ(y) = ρ·(|y − d/2| −
|y + d/2|) = −2ρ y for |y| ≤ d/2 and ∓ρ d outside: the steering at the
screen Nodes sends cos²(2π ρ y) of the combined content forward and the
rest apart, a fringe pattern of period

```text
Δy = 1/(2ρ) = λ/2 Links,   in the strip |y| < d/2 only, independent of L and of d,
```

against optics' λL/d everywhere. A mark counts nothing of a field (law of
the bit, point 6): the fringes are read only as the push on a row of things
behind the slits. **Two slits for things:** a thing meets its own shadows
as home (E5), so one thing at a time shows the geometric shadow of its slit
and no fringes; the Born steering acts only where two things of one family
stand at one Node in one interval, so the fringes of things scale with the
coincidence rate. **Different law**; the run is A1 with one electron at a
time against many.

**Verdict.** The front at c: **reached** as the edge of the tubes (exact),
carrying 4/5 of a release on the coordinate planes; the wave equation:
**not reached** (transport inside r_coh, diffusion with D′(p) outside);
t₉₀ = r on the tubes: **new**; t₉₀ ∝ r² beyond r_coh: **stands**; the
fringe law λ/2 in the strip: **new**; no self-interference of a thing:
**different law** (A1).

## 18. Round 2: the field of a thing with a clock

**Rules used.** R7′ (rate = M/K), R8, R4′, R5, hypothesis 12, section 17.

**The pattern and its dictionary.** By section 17 (iii) the shadows of a
thing of content M carry φ = φ₀ + (M/K)(t − |x − x₀|₁): a pattern whose
spatial period is fixed, λ = K/M Links on L1 shells, and whose phase at a
fixed Node turns at the thing's rate. The energy–frequency identity: the
clock rate is ν = M/K turns per interval and the amount is E = M (section
7), so E = K ν for every thing at rest. **Planck's relation from an
emission.** A meeting whose table puts ΔE on a light thing takes ΔE from
the group (the invariant `energy`, section 7): the group's rate falls from
M/K to (M − ΔE)/K, and the beat between the emitter's clock before and after
is Δν = ΔE/K. The light thing has no clock (R7′); its frequency is read
only by interference between successive emissions (Highlights 3.3), that
is, against the emitter's clock, and what the emitter's clock lost is
exactly the light's amount over K:

```text
ΔE = K · Δν        (E = h ν with h = K quanta·interval, exact),
```

a consequence of conservation of amount plus rate ∝ content, not a new
rule; and E = m c² and E = h ν are the same identity, since ν = M/K. With
that h, the Compton wavelength is h/(m c) = K/M Links = λ: **the field's
wavelength is the Compton wavelength exactly**, for every K. What fixes K:
nothing in the rules; K = N makes one quantum advance one step per
interval, which is hypothesis 12's m₀ = h/(N δt c²) and round 1's first
choice in section 10 (h = N); in physical units K = h/(E₁ δt) with E₁ the
energy of one quantum. **Reached** (E = hν as an identity; λ = h/(mc)).

**What the steering does to the pattern.** On the tubes and on every edge
it holds exactly (E3); in the interior it is what steers: under C1 the
pattern is self-consistent (no scattering) out to r_coh = λ²/(8π²) Links
and self-scattering beyond, so a heavy thing (small λ) has a field that
mixes within a Link and a light thing (large λ) a coherent field far out;
under the sum table (D2) it scatters everywhere. Neither focuses.

**Two things with clocks.** R8 combines shares of one owner only; shares of
different owners cross. R4′ reads amount × heading × (M_B or q_A q_B/M_A)
and no phase. So A's phase pattern is invisible to B: no beat, no standing
pattern between them, no potential with a length scale; the Compton length
is present in every field and read by nothing that moves a thing. A beat at
|ρ_A − ρ_B| would appear only under a cross-owner steering, which point 17
does not declare. **Not reached** (no bound-state condition from this
alone; hypothesis 12 / A10 in the new form: none).

**Loops under rate ∝ content.** A ray of amount a on a ring of length L
advances a/K turns per Link; its phase returns after K/a intervals per
turn, the ring after L, the state after T = L N/gcd(L·N a/K, N) intervals;
nothing at a corner reads the absolute phase (section 12), so L a/K ∈ ℤ is
read by nothing. The Port form closes for every amount at every L. The Born
form reads d = φ_R − φ_L: for equal amounts the two senses have equal rates
and d is constant, so section 12's result stands (every even content at
d = N/4, 3N/4); for the alternating orbits (a₁, a₂) that swap senses at
every corner, d drifts by (a₁ − a₂)·g/K turns between corners g Links apart
and back by the same between the next two, so the orbit closes only if
T[d₀] = T[d₀ + Δ] with Δ = (a₁ − a₂) g N/K steps: Δ ≡ 0 or Δ ≡ N − 2d₀
(mod N), a discrete condition on the *difference* of the amounts, not on
the content. The ring size is constrained as before (presence: (a + b)/gcd
rays per sense) and by g N (a₁ − a₂)/K being an integer. **No ladder of
contents appears**: the members are every even content (Born, equal
senses) and every content (Port), whose ratios are all rationals, so none
of proton/electron 1836.153, neutron/proton 1.001378, muon/electron 206.768,
tau/electron 3477.2, π±/electron 273.13, π⁰/electron 264.14 is selected by
any K, N or ring; the alternating orbits' condition on a₁ − a₂ is the one
new integer equality and its enumeration with rates a/K (A10's count over
the corner tables, section 12's procedure) is open, not made here. The rule
a ladder needs: a meeting that reads a thing's absolute phase advance over
a closed path against a clock that did not walk it, e.g. a push that reads
a returning shadow's phase (age s) against its owner's, δ = M s/K; closure
M s/K ∈ ℤ gives s = m λ, the L1 length of the path a multiple of the
Compton wavelength (de Broglie's condition), and then A10 counts the (M, s)
pairs. **Not reached.**

**Verdict.** E = hν with h = K: **reached** as an identity of R7′. λ = h/(mc):
**reached** exactly. A length scale in the force: **not reached** (nothing
reads the phase in a push). Ladder: **not reached** (one new condition on
amount differences, enumeration open, A10).

## 19. Round 2: Coulomb and Newton from one shadow set and two readings

**Rules used.** R3′, R4′, R5, R6′, sections 1, 5 (the far field J = ζ Φ,
Φ = S/(4πr²), ζ = 11/8 for a diffusive field and 1 for a purely radial
transport field; the product and equivalence laws below hold for any ζ).

**The flux.** A's set has X_A = ξ M_A shadows; the flux its profile carries
is S_A = κ X_A = κ ξ M_A, κ the profile's flux per unit set (2D/R² for the
diffusive profile of section 5; X/(2R) for tubes returning from a wall at
R). Every force constant is written in κξ.

**Coulomb.** B at distance r reads A's shadows by the charge reading:
Δp_B = (q_A/M_A) q_B · J_A(B) = (q_A/M_A) q_B · ζ κ ξ M_A /(4π r²) r̂ =
ζ κ ξ q_A q_B/(4π r²) r̂: **M_A cancels**. B's own shadows push A by the
same law with A ↔ B, ζκξ q_B q_A/(4π r²), and return the recoil to B on the
schedule of section 4. Both halves are equal (the flux ∝ M_A, the reading
∝ 1/M_A), so, once the returns are home,

```text
F_B = k_C q_A q_B / r² r̂_AB,   F_A = −F_B,   k_C = ζ κ ξ /(2π),   a_B = F_B / M_B:
```

the product law, the sign rule (like charges apart), symmetric between the
two bodies at equal distance, independent of both masses in the force and
inverse in the pushed mass in the acceleration. **Reached exactly** (the
constant an input through ξ, κ). Note on the declared-X variant (the
superseded point 18): with X per family and a reading × q_B it would have
given F ∝ |q_B| X_A + |q_A| X_B, a product only if X ∝ |q| across families,
and a third law by halves only then.

**Newton.** The mass reading: Δp_B = M_B · ζ κ ξ M_A/(4π r²), and the return
of B's shadows the same, so

```text
F_B = −G M_A M_B / r² r̂_AB,   G = ζ κ ξ /(2π) = k_C,   a_B = −G M_A / r² r̂_AB   (any M_B, any structure):
```

**the equivalence principle exact** (round 1's g = N/M is gone: the reading
is per thing times its content). G and k_C are one number: the ratio of
the electric to the gravitational push between two things is q_A q_B/(M_A
M_B) in lattice units, exactly; for two electrons to have nature's
4.17·10⁴² the electron's content must be M_e = |q_e|·2.04·10²¹ quanta (6.1·10²¹
at q = 3 in thirds of e). **New**, testable by A5s and A7 on one board with
the same two bodies (the ratio of the registers is q²/M², no fit).

**Light bending.** A thing of content p at speed 1 (R6′: every thing)
passes at impact parameter b; the mass reading gives Δp_⊥ = p · ζ S_M/(2π b)
= p G M/b (section 8's integral 2/b), and its register has |p|₁ = p, so

```text
α = G M /(c² b)   on the pass, for every thing, achromatic;
```

the light thing's own mass shadows (ξ p of them) push M by the same law and
return the recoil along the trace (R5), up to another G M/b delivered late,
so α_total ∈ [GM/(c²b), 2GM/(c²b)]: at most Newton's 2GM/(c²b) and never
Einstein's 4GM/(c²b) (no delay gradient, section 8). The capture radius
b_c = G M and the circle R_c = G M/2 of section 11 are now the same for
every thing. **Achromatic: reached; coefficient: different law** (½ to 1 of
Newton, ¼ to ½ of Einstein; A6 with light of 2¹⁷ and 2¹⁹ reads the same
α, and the return part is read as the register after the pass).

**Motion (R6′).** dp/dt = F stands (section 3); every free thing moves at
one Link per interval on its DDA line, so Kepler's orbits (section 11 (b))
and v = p/M are **not reached** for a free thing: a free thing orbits only
on the circle R_c, and the slow motion of matter is a loop's drift, open
(section 9). E = m with no kinetic energy stands (section 7).

## 20. Round 2: what is new and testable under 16 to 21

1. **The front is six tubes.** 4/5 of a release stays on the light-cone
   edge on lines parallel to the axes in the coordinate planes, e-folding
   1.65 Links; off the planes the coherent field is zero and the push is
   the residue's (section 17). Run: E11's source under R8 read at (24, 0,
   0), (24, 1, 0), (17, 17, 0) and (14, 14, 14).
2. **The residual anisotropy.** In the mixing regime the field is the walk
   of table [1 − p, 0, p/4 ×4] with D′ = (2 − p)/(6p); in the coherent
   regime it is total (tubes). The k⁴ anisotropy coefficient of the
   effective table as a function of p: open (one symbol expansion, as
   section 2's).
3. **t₉₀ = r on a tube, 1.925 r² for the residue, 0.856 r²/D′(p) beyond
   r_coh = λ²/(8π²)** (section 17). Run: A5s Run 2 tick by tick.
4. **The wavelength of a massive thing's field is h/(mc) on L1 shells**,
   λ = K/M Links, spacing λ on an axis and λ/√2, λ/√3 in Euclidean distance
   on the diagonals (section 18). Run: E11 with a clocked source, the phase
   per Node from the dense mode read along an axis and a diagonal.
5. **No beat between two things** (per-owner steering, phase-blind push);
   a beat at |M_A − M_B|/K would mark a cross-owner steering (section 18).
6. **Fringes of shadows at λ/2 in the strip between the slits**,
   independent of L and d, against λL/d; **no fringes for one thing at a
   time** (section 17). Run: A1.
7. **k_C = G in lattice units**: F_e/F_g = q_A q_B/(M_A M_B); the electron's
   content follows from nature's ratio (section 19). Run: A5s and A7 on
   one board.
8. **Bending GM/(c²b) on the pass plus a late return**, achromatic (section
   19). Run: A6 at two amounts, the register read during and after.
9. **E = hν with h = K as an identity**, and the ladder's one new integer
   equality on amount differences (section 18). Run: A10 with rates a/K.

## 21. Round 2: the verdicts that change, and those that stand

| Law | Round 1 (section 15) | Under 16 to 21 | Run |
| --- | --- | --- | --- |
| Coulomb's product law | different (sum of fluxes) | **reached exactly**, k_C = ζκξ/(2π), mass-independent | A5s unequal contents |
| Equivalence principle | not reached (g = N/M) | **reached exactly** (reading × content) | A7 |
| Achromatic bending | different (α ∝ 1/p) | **reached** (α = GM/(c²b) for every thing) | A6 at 2¹⁷, 2¹⁹ |
| Einstein's 4GM/(c²b) | not reached | not reached (≤ 2GM/(c²b) with the return) | A6 after the pass |
| Diffusion of the field | reached, D = 4/9 | dichotomy: tubes/transport inside r_coh, D′(p) outside; D = 4/9 for lone quanta | A5s under R8 |
| Maxwell's wave equation | not reached | **not reached** (amounts have no sign) | — |
| Retardation t₉₀ | 1.925 r² | r on tubes and inside r_coh; r² beyond | A5s Run 2 |
| Newton's 2nd law, v = p/M | reached for a body | **superseded**: speed 1 for every thing, register = direction | any pushed body |
| Two-body orbits (Kepler) | reached | not reached for free things (speed 1); loops open | A7 |
| E = mc², no kinetic energy | reached / different | stands | a body at a mark |
| E = hν | not a consequence | **reached** as an identity, h = K | — |
| Compton wavelength | — | **reached**: λ = K/M = h/(mc), L1 shells | E11 clocked |
| Time dilation, Lorentz factor | not reached | stands (R6′ makes every thing's speed 1; the loop's drift open) | A14 |
| Gravitational time dilation | not reached | stands (16 changes the push, not a clock) | — |
| Mass ladder | not reached | stands; one new condition on amount differences, enumeration open | A10 |
| Born rule | declared | declared; no self-interference of a thing | A1 |
| G's value, α's value | inputs | inputs (ξ, κ); k_C = G new | A5s + A7 |

Open after 30 minutes, in one line each: the self-consistent p of the
mixing regime; the k⁴ coefficient of the effective table; the enumeration
of the alternating orbits with rates a/K; the field of a thing moving at
speed 1 (the return half of the bending).

## 22. Round 3: the vectorial steering rule, verified

Round 3 (2026-09-18, after PR #277) verifies two rules Boss proposed to the
model owner, A (this section) and B (section 23), and derives the wait of
Highlights 5.4 point 23 (section 24, PR #278). As before: no engine run, no
edit to the engine; the arithmetic is a mean-field iteration of the stated
rule on a board of 45³ or 61³ Nodes (seconds), cited as a check of the
derivation and never as its source.

**The rule, A (R8v).** At a Node, all shares of one owner that arrive on
two or more headings combine: the amount A = Σ_h a_h is summed, the phase
φ̄ is that of Σ_h a_h e^{iφ_h} (the coherence rule of Highlights 3.20, as
R8 of section 17). The steering is vectorial: with the weights
w_h = a_h cos²((φ_h − φ̄)/2) (the Born table read against the combined
phase) the vector V = Σ_h w_h h is formed over the arrival headings, and
the whole A leaves through the Port(s) nearest V with the remainder rule. A
share meeting no other share of its owner keeps the fixed split R1. Two
readings of "nearest" exist and both are derived: **(P)**, the DDA reading
(section 3, v = p/|p|₁): the content leaves through the Ports of the
nonzero components of V in the proportion |V_i|/|V|₁, the remainders owned
by the Node; **(M)**, the single-Port reading: all of A leaves through the
Port of the largest |V_i|, ties by Port order. Rules used besides: R1, R2,
R3 (both readings), R5, R7′; the state is section 17's (an amount and a
phase per Node and heading).

**Assumptions and limit.** One owner (R8v combines shares of one owner
only, as R8; shares of different owners cross). The mean field of the
integer rule (a register never destroys a share; every statement holds for
the integers up to one quantum per Node, heading and register). The board
large. Every statement marked **(exact)** holds for both readings and
without any completion.

**(i) The operator.** Write the one-phase case first (a single release, or
an owner of rate 0: E2 and E4 of section 17 make every meeting of one
release in phase, δ = 0, so w_h = a_h and V = Σ_h a_h h = J(x), the net
momentum arriving, section 0). Per axis i, V_i = a_{+i} − a_{−i} and
|V|₁ = Σ_i |a_{+i} − a_{−i}|, while A = Σ_i (a_{+i} + a_{−i}). Under (P)
the departure through +i is A·max(V_i, 0)/|V|₁. Hence the **identity
lemma (exact)**: if no axis carries arrivals of both signs, then
|V|₁ = A and the departure through h is A·a_h/A = a_h, the share continues
on its own heading, whatever the amounts. R8v differs from the transport
identity ("in phase → continue", the completion C1 of section 17 at δ = 0)
only at a Node where two shares of one owner meet head-on, and there it
collimates: the smaller is reversed and carried with the larger, the whole
A leaving along V/|V|₁, so the momentum of the field grows at that Node by

```text
|out|₁ − |V|₁ = A − |V|₁ = 2 Σ_i min(a_{+i}, a_{−i})      (exact; zero iff no head-on pair),
```

a non-conserving corner for momentum (amount is conserved exactly: all of
A leaves). At V = 0 (equal head-on arrivals, or a symmetric star of
arrivals) the rule names no Port. Under (M) the identity lemma fails
already at two orthogonal arrivals of equal amount (a tie, decided by Port
order) and of unequal amount (the whole A goes the larger way).

With phases, for a large share A of phase 0 meeting a small share ε of
phase δ: φ̄ = O(ε/A), w_A = A − O(ε), w_ε = ε cos²(δ/2) ≤ ε, so the sum
still leaves along A's heading for every δ: **the collimation of a small
opposing share does not depend on its phase (exact to O(ε/A))**. For two
equal shares a of phases φ₁, φ₂ (δ = φ₁ − φ₂, |δ| < π) the coherent sum is
2a cos(δ/2) e^{i(φ₁+φ₂)/2}, so φ_{1,2} − φ̄ = ±δ/2 and w₁ = w₂ = a cos²(δ/4):
V ∝ h₁ + h₂ **for every δ**, and at δ = π the sum is zero and φ̄ is
undefined. The steering of equal shares is blind to their phase difference;
only unequal amounts read it (below, (iv)).

**The Fourier symbol.** R8v is homogeneous of degree one (F(λa) = λF(a))
and piecewise linear, not linear: it has no symbol. Its linearisations do.
(a) About the empty background (a lone share) it is R1: section 2's
symbol, D = 4/9, the k⁴ coefficients −58/81 and 95/243. (b) About a
collimated background (a stream of amount A on +x at every Node of a line,
or any set of non-opposing arrivals) it is the transport map on the five
non-opposing headings, symbol e^{−ik·h}, five undamped modes ω = k·h with
no diffusion and total anisotropy (the group velocity is the axis heading),
and the annihilation of the opposing one (a perturbation ε on −x leaves on
+x with weight 1: eigenvalue 0). (c) About the isotropic background
a_h = ā on six headings (the local form of any diffusive field) it does
not exist: V = 0 there, and a perturbation ε on one heading sends all 6ā
through that Port, a gain 6ā/ε unbounded as ε → 0. The map is not
Lipschitz at V = 0, and the diffusive state of round 1 is not a fixed point
but a singular point of R8v. Nor does the rule's own direction, V/|V|₁,
carry an isotropic term with a small anisotropic correction: it is the
DDA's unit vector in the L1 norm, so a collimated stream steered toward
(cos θ, sin θ, 0) advances at Euclidean speed 1/(|cos θ| + |sin θ|) per
interval, 1/√2 on the diagonal, and the front of anything the rule
collimates is the octahedron |x|₁ = t, not a sphere and not a sphere plus
a k⁴ term. There is no order at which the shape becomes spherical.

**(ii) A point release of one phase: the tube theorem holds verbatim
(exact).** Section 17's theorem needs only that in-phase, non-opposing
arrivals continue; by the identity lemma R8v is that identity on the
light-cone edge (every arrival at a Node of |x|₁ = t at tick t came by a
monotone path, so all arrivals are outward and no axis carries both
signs). So the axis tip (t, 0, 0) is lone, keeps (6/11)^t of X/6 on the
axis and sheds 4/11 into the four lines (t, ±1, 0), (t, 0, ±1), where the
shed meets the line's in-phase stream at right angles and both continue;
the edge fraction is

```text
1 − (1/11) Σ_{t≥0} (6/11)^t = 4/5   (exact, both readings),
```

on lines parallel to the axes in the three coordinate planes through the
source, the line y = j carrying (1/11)(6/11)^{j−1} X/6, e-folding
1/ln(11/6) = 1.65 Links under (P). Under (M) the shed at (t, 1, 0) meets
the line's larger stream and all of it goes +x: the four lines at distance
1 absorb every tip's shed and the tubes are one Link wide; and at tick 2
the Node (1, 1, 0) holds X/66 on +x and X/66 on +y, a tie decided by Port
order, so the six crosses receive unequal shares and the release loses the
cubic symmetry of its source at its second step. My iteration (45³, 20
ticks, X = 1): under (P) the edge fraction 0.9091, 0.8595, 0.8325, …,
0.800002 at t = 20; the coordinate planes 1.000000 through t = 5 and
0.9834 at t = 20 (the residue's lone shares off the axes shed out of the
planes, 1.7 %, where C1 kept 1.000000); the axes 0.0011; home (the residue
absorbed at the owner's Node, R5) 0.1500 of X by t = 20, three quarters of
the 1/5 that is not on the edge, collimated inward by the head-on rule;
the tie content 1.3·10⁻⁶ X. Under (M): edge 0.7347, planes 0.9243, home
0.1596, Port-order ties 0.392 X (the second step), V = 0 ties 3·10⁻⁴ X.

**A switched-on source of one phase (the field of a thing).** This is the
case a force needs, and it is worse than the release. With the source
releasing X/6 per heading every tick, an axis Node x at tick t receives
the outward stream from x − 1 and, if the Node x + 1 was lone one tick
earlier, its backward 1/11; two opposing arrivals collimate (all forward,
nothing shed), one arrival is lone (R1: 4/11 shed sideways, 1/11 back).
So a Node is collimated exactly when the Node ahead of it was lone one
tick before, state(x, t) = ¬state(x + 1, t − 1), and with the tip lone this
gives on every axis Node the cycle lone, lone, collimated, collimated,
period 4 (derived; the iteration shows 0.1848, 0.1848, 0.0000, 0.0000 at
(16, 0, 0) from t = 18 on, and the same period on every line and diagonal).
The steady state (61³, 60 ticks, the mean over one period, ρ = 0): the
content per Node on the axis 0.0924 = 0.554 X/6 at r = 8, 12, 16, constant
in r; on the lines at distance 1, 2, 3 from an axis 0.00758, 0.00413,
0.00225, the ratio 0.545 = 6/11 per Link (e-folding 1.65 Links); on the
diagonal (r, r, 0) 0.00246, 0.00073, 0.00022 at r = 4, 6, 8 ((6/11)^{2r});
at (r, r, r) and at (r, 3, 3) exactly 0. Per L1 shell at r = 10 to 18:
58.1 % of the content on the six axes, 77.2 % within one Link of an axis,
87.5 % within two, **100.0 % on the three coordinate planes, 0 off them**;
the shell total 0.9546 X (the release X less the X/22 per tick that is
collimated home). The clock changes nothing: with ρ = 1/8 (λ = 8 Links)
every number above is the same to four digits, as the small-share lemma
says. The V = 0 ties: 0.64 X in 60 ticks, one per cent of the release,
decided by Port order. Under (M) the field is not steady in 60 ticks (the
axis 0.040, 0.024, 0.012 at r = 8, 16, 24 and drifting; 69 % on the
planes; the Port-order ties 2.0 X): the field of a point source under (M)
is a function of the Port order.

**(iii) Front speed and t₉₀.** The front is on |x|₁ = t at c (E3, exact,
any rule). On a tube the content is a pulse train of period 4, so the push
on a thing there is 0.185 X/6 for two ticks and 0 for two; its four-tick
mean is at its steady value from t = r + 4: **t₉₀ = r + O(4) on the tubes
(exact)**; off the three coordinate planes the field is 0 at every t
(t₉₀ = ∞: no push ever); on the diagonals of the planes it is
(6/11)^{2r} X/6, a push that at r = 8 is 2·10⁻⁴ of the axis value. The
model owner's t₉₀ ∝ r is reached where there is a field, and there is a
field on a set of measure zero.

**(iv) Two slits.** Section 17's geometry (slits at (0, ±d/2, 0), the
screen Node (L, y, 0), δ(y) = −2ρy in the strip |y| < d/2) gives at the
screen Node two shares of one owner on two headings h₁, h₂ with amounts
a₁, a₂ and phase difference δ. By the equal-share lemma the steering is
blind to δ when a₁ = a₂: the departures are (a₁, a₂) on (h₁, h₂) for every
δ < π and undefined at δ = π. For a₁ ≠ a₂ the fraction leaving on h₁ is
w₁/(w₁ + w₂), which moves from a₁/A at δ = 0 to 1 at δ = π (a₁ > a₂): a
modulation of the *direction* of the push behind the screen, of depth
|a₁ − a₂|/A, with the period λ/2 in y of section 17 and zero depth on the
symmetry line y = 0, where optics has its central maximum. The amount that
reaches the screen Node is A = a₁ + a₂ whatever δ, so a mark that absorbs
counts a₁(y) + a₂(y), the sum of the two single-slit patterns with no
cross term: **no fringes in the counts**; the cross term 2√(a₁a₂) cos δ of
the Born rule is what a rule on amounts cannot produce, and R8 of section
17 produced its stand-in (cos²(δ/2) of the sum forward, the rest apart)
only by steering equal shares apart, which R8v does not do. Things: as in
section 17, no self-interference (E5).

**(v) Pathologies.** (1) *V = 0 is not rare.* A mark returns a shadow as
at any thing (law of the bit, point 6), so in front of any mirror or wall
the incoming stream a on +h meets its own return a on −h at every tick,
V = 0 exactly, and the rule names no Port: the two-slit apparatus is made
of the configuration the rule cannot process; Port order decides, and the
first decision (2a through +h) makes the next tick's V = −a: the wall's
return then sweeps the incoming stream home, and the Node in front of the
wall alternates. In the switched-on source 1 % of the release meets V = 0
with no wall at all. (2) *The return is destroyed.* R5 sends a shadow that
pushed back on its own steps with amount ε against the outgoing stream A of
its owner; by the small-share lemma R8v collimates it outward again at the
first Node where A > ε cos²(δ/2), which is every Node of the path. The
recoil never comes home, B keeps Δp and A never receives −Δp: the third
law of section 4 and the closing of the books of things (point 7, "every
action is a message that returns") fail; exempting returning shares
contradicts "all shares of one owner that meet". (3) *Momentum is created*
at every head-on meeting, 2 Σ_i min(a_{+i}, a_{−i}) per Node per interval
(above); the field's J is no longer the source's momentum spread out, and
J = ζΦ of section 1 holds with ζ = 1 on the tubes and is meaningless
elsewhere. (4) *Port order:* every tie under (M), the V = 0 ties under (P);
the field of a symmetric source is asymmetric under (M) from tick 2. (5)
*The map is not Lipschitz:* the gain A/|V|₁ is unbounded, so the isotropic
state is an unstable singular point, and the engine's rounding (one
quantum) decides the direction of a whole Node's content wherever the
arrivals nearly balance. (6) *No trapping at a Node* (all of A leaves every
tick), but a cavity between two walls sloshes with period 2, the content
never diffusing out because equal head-on shares are the tie case.

**Formula.**

```text
R8v (P), one phase:   out_h = A · max(V·h, 0) / |V|₁,   V = Σ_h a_h h = J,   A = Σ_h a_h;
identity lemma:       no head-on pair  ⇒  out_h = a_h                            (exact);
head-on:              |out|₁ − |V|₁ = 2 Σ_i min(a_{+i}, a_{−i}) > 0,   V = 0 undefined;
point release:        4/5 on the light-cone edge, on axis-parallel lines of the coordinate planes  (exact);
switched-on source:   six tubes of period 4, 58 % on the axes, 100 % on the coordinate planes, 0 off them;
two slits:            counts a₁ + a₂ (no cross term); push direction modulated at λ/2 with depth |a₁ − a₂|/A.
```

**Dictionary.** A tube ↔ a ray of the E6 geometry (Highlights 3.5, the
"field on lines" the model owner rejected on 2026-09-17); the pulse train
↔ a field of period 4 intervals at every Node; V/|V|₁ ↔ the DDA direction;
the ties ↔ the standing wave in front of a mirror.

**Verdict.** Does R8v fix the tube artefact: **no.** It is the transport
identity wherever the artefact is made (the light-cone edge, the lines,
every Node without a head-on pair), so the tube theorem holds exactly:
4/5 of a release on the edge in the coordinate planes, and for a
switched-on source 58 % of the field on the six axes, 100 % on the three
coordinate planes and 0 off them, the six-line field of E6 with a period-4
pulse. Its Fourier symbol does not exist; its front is the octahedron at
every order. It loses what R8 had (the λ/2 fringes) and what R5 needs (the
return). **Different law** (six tubes; no fringes in counts; the third law
lost). The run: E11's source under R8v read at (24, 0, 0), (24, 1, 0),
(17, 17, 0) and (14, 14, 14) over eight ticks: 0.55 X/6 and 0.045 X/6 in a
period-4 pulse, 2·10⁻⁸ X/6, and exactly 0; and A5s Run 2 with the recoil
read at the source (none arrives).

## 23. Round 3: a push that reads the phase, verified

**The rule, B (R4″).** A shadow carries its owner's phase at release
(point 9: nothing advances it on the way; point 12: it is a ray of the
owner's family). When a shadow of A reaches a thing B, the push of R4′ is
multiplied by a declared function f of the difference between the
shadow's phase and B's own clock now: f(δ) = cos δ, or the Born table
cos²(δ/2) = (1 + cos δ)/2 (Highlights 3.3, T[d]/N). R5 stands: the return
carries the opposite of the push actually given. Rules used besides: R3′,
R7′ (rates ρ_A = M_A/K, ρ_B = M_B/K turns per interval), R6′, and the
phase pattern of sections 17 and 18, φ(x, t) = φ₀ + ρ(t − s) for a share
of age s.

**Assumptions and limit.** Two things at rest (loops, or the external
bodies of round 1) at L1 distance s, s ≫ 1. The phase of A's shadow at B
is a function of position only where the age of a share is: on the
coherent field (the tubes and edges of sections 17 and 22, where s = |x|₁
exactly), or within r < √(Dλ) = 0.67√λ Links of a diffusive source, beyond
which the ages at one Node spread over more than λ/ρ and the pattern is
washed out (section 17 (iii)). Everything below is on the coherent field.
The mean-field push of section 19 is written −G M_A M_B/s² r̂ for one
half (the direct push on B) and the same for the other (the recoil of B's
shadows' push on A, returned to B), G = ζκξ/(4π) per half.

**(i) The effective push on B.** The shadow that reaches B at tick t left
A at t − s with φ_A(t − s) = φ_A0 + ρ_A(t − s); B's clock reads
φ_B(t) = φ_B0 + ρ_B t. So B reads

```text
x(t) = φ_A(t − s) − φ_B(t) = Δ₀ + (ρ_A − ρ_B) t − ρ_A s,      Δ₀ = φ_A0 − φ_B0   (turns),
```

and A reads, of B's shadow, y(t) = −Δ₀ − (ρ_A − ρ_B) t − ρ_B s. The push on
B at tick t is the direct half f(x(t)) plus the returned half of what B's
shadow did at A at tick t − s (R5, delivered after s more Links),
f(y(t − s)); with x(t) + y(t − s) = −2ρ_B s (exact: the drift cancels, A's
lag ρ_A s cancels against its advance over the return) and
x(t) − y(t − s) = 2[Δ₀ + (ρ_A − ρ_B)(t − s)],

```text
f = cos:   F_B(s, t) = −(2 G M_A M_B / s²) · cos(2π M_B s / K) · cos(2π[Δ₀ + (M_A − M_B)(t − s)/K]) r̂,
f = cos²:  F_B(s, t) = −(G M_A M_B / s²) · [1 + cos(2π M_B s / K) · cos(2π[Δ₀ + (M_A − M_B)(t − s)/K])] r̂.
```

Boss's "round-trip phase s(rate_A + rate_B)" is what the two halves give
when both are read at the same tick, x(t) + y(t) = −(ρ_A + ρ_B) s; with
the return's own delay of s Links it is B's clock over the round trip,
2ρ_B s, and A's push has 2ρ_A s. Either way the standing factor is
multiplied by a **beat** at |M_A − M_B|/K turns per interval whenever the
rates differ, and the beat is a full cosine: under f = cos the push on B
changes sign every K/(2|M_A − M_B|) intervals and averages to **zero** over
a beat period; under cos² it averages to half the bare push of section 19
(cos² has mean ½) and the standing pattern survives only as a flicker of
depth cos(2πM_B s/K).
For equal rates (M_A = M_B = M) the beat factor is the constant
c₀ = cos(2πΔ₀), the relative setting of the two clocks, an initial
condition nothing fixes: two equal things with Δ₀ = 1/4 turn feel no force
at all under f = cos, and the standing pattern in s is

```text
F_B(s) = −(2 G M² c₀ / s²) cos(2π s/λ),   λ = K/M   (the Compton wavelength of section 18),
```

with sign changes at s = (n ± ¼)λ: attraction on |s − nλ| < λ/4 for
c₀ > 0, repulsion between (Coulomb's like charges attract there, gravity
repels), nodes at (n ± ¼)λ. Under cos² there is no sign change at any s.

**(ii) Orbits and preferred radii.** Under R6′ (point 21) a free thing
moves one Link per interval and its register sets its direction, so a
circle of L1 radius s (the DDA staircase of section 11 (d)) needs a turn of
1/s per Link, |F(s)| = |p_B|/s: for every s in an attractive band there is
a register length |p_B| = |F(s)| s that orbits, and none in a repulsive
band. Preferred radii in the sense of a discrete set: **none**; bands of
width λ/2 about s = nλ (equal rates, c₀ > 0), and for unequal rates no
band that lasts longer than a quarter beat, K/(4|M_A − M_B|) intervals. The
other sense, the minima of the standing potential U(s) = ∫_s^∞ F ds′ (a
constant of the trajectory, not a booked quantity, section 7): with
F = −C cos(ks)/s², C = 2GM²c₀, k = 2π/λ, the zeros of F with F′ < 0 are
at cos(ks) = 0, sin(ks) = −1 exactly,

```text
s_n = (n − ¼) λ,   n = 1, 2, …;    U_n = −C ∫_{s_n}^∞ cos(ks′)/s′² ds′  →  −C/(k s_n²) = −C/(2π λ (n − ¼)²) for large n.
```

The exact values (mpmath, in units C = λ = 1): U₁ = −0.23610 at s = 0.75,
and U_n/U₁ = 0.2106, 0.0875, 0.0474, 0.0297 at n = 2 to 5 (the asymptotic
law (¾)²/(n − ¼)² gives 0.184, 0.074, 0.040, 0.025); at the attraction
maxima s = nλ instead U = −0.0409, −0.0059, −0.0018, falling as 1/n³. The
model's own law: **r_n ∝ n, U_n ∝ 1/(n − ¼)²**, against Bohr's r_n ∝ n²,
E_n ∝ 1/n², because the wavelength here is the Compton length K/M, fixed,
and not de Broglie's h/(mv), which shrinks with the momentum: the condition
of section 18 (s = mλ) meets a 1/s² force with a fixed λ, and that gives a
linear ladder of radii. And no thing can sit at s_n: under R6′ nothing is
at rest but a loop, and a loop's rays read the pattern at their own Nodes.

**(iii) The ladder of A10.** Unchanged. A10 counts the closing orbits of
the corner table on a ring, a thing meeting a thing (point 4), and R4″
changes what a thing does with a *shadow*. What changes is which pairs
bind: under f = cos a pair of unequal contents has a force that averages to
zero, so **only equal contents bind** (for the proton and the electron the
sign flips every K/(2(M_p − M_e)) ≈ λ_p/2 Links of travel: hydrogen does
not bind); under cos² every pair binds as in section 19, on half the bare force
with a flicker. Neither is a ladder of contents.

**(iv) The measured ratios.** The level ratios of the model's law are
numbers, 0.2106 and 0.0875 against hydrogen's 1/4 and 1/9 (16 % and 21 %
low), independent of K (which sets λ, a scale) and of N (which sets the
resolution of the table, a rounding of order λ/N in s_n); no K, N
reproduces them, and the ratio E₂/E₁ = 1/4 needs minima at s = nλ exactly
(the form (n + c)⁻² has E₂/E₁ = 1/4 iff c = 0), which a cosine force gives
at no phase offset (c = −¼ for c₀ > 0, +¼ for c₀ < 0, ratios 0.184 or
0.309). The six mass ratios do not enter: the ladder is untouched, and the
one condition R4″ adds, M_A = M_B for binding, selects no ratio but 1.

**(v) The integer rule.** The phases are on the circle of N steps; B reads
d = (φ_shadow − φ_B) mod N, an integer, and the table T[d] ∈ {0, …, N}
(T[d] = round(N cos²(πd/N)) for the Born form, or a declared cos table with
sign). The push Δp_i on axis i (an integer, the whole quanta met times
their heading times M_B or q_Aq_B/M_A) becomes ⌊(Δp_i T[d] + R_i)/N⌋ with
R_i the thing's remainder register per family and axis, bounded by N − 1
in units of 1/N, so the mean push is exact and the remainder is one push
unit per register (section 0's rule, now on a thing). The clock advances
N M_B/K steps per interval, an integer or a register (R7′). The standing
pattern is resolved to 1/N of a turn and, since the age of a coherent
share is its L1 distance, lies on the octahedra |x − x_A|₁ = s, not on
spheres: the nodes of the force are at L1 radii (n ± ¼)K/M_B.

**A consequence to name.** Under f = cos the force between two equal things
is modulated to full depth at the pushed thing's Compton wavelength:
Coulomb's law between two electrons would reverse sign every 1.2 pm and
vanish at λ_e/4; under cos² it would flicker at the beat. Møller scattering
agrees with the unmodulated law to 10⁻¹⁸ m. **Different law.**

**Formula.**

```text
x(t) + y(t − s) = −2 M_B s / K  (delayed return; Boss's simultaneous reading: −(M_A + M_B) s / K);
F_B = −(2GM_AM_B/s²) cos(2πM_B s/K) · cos(2π[Δ₀ + (M_A − M_B)(t − s)/K])          (cos);
F_B = −(GM_AM_B/s²) [1 + the same product]                                          (cos²);
equal rates: bands |s − nλ| < λ/4 attract (c₀ > 0), λ = K/M; potential minima s_n = (n − ¼)λ, U_n/U₁ = 0.2106, 0.0875, 0.0474.
```

**Dictionary.** λ = K/M ↔ h/(mc) (section 18); the beat ↔ (M_A − M_B)c²/h,
the difference of the two Compton frequencies; Δ₀ ↔ the relative phase of
two clocks, unobservable in physics and load-bearing here; U_n ↔ a level
only as a constant of the trajectory.

**Verdict.** Does R4″ give levels: **no.** It gives a standing modulation of
the 1/s² force at the pushed thing's Compton wavelength, F ∝
cos(2πM_B s/K)/s², which for unequal contents beats at |M_A − M_B|/K and
averages to zero (cos) or to half the bare force (cos²), and for equal contents
depends on the clocks' relative setting Δ₀; the radii it prefers are bands
of width λ/2 about nλ, and the minima of its potential lie at (n − ¼)λ
with U_n ∝ 1/(n − ¼)² (r_n ∝ n): E₂/E₁ = 0.211 and E₃/E₁ = 0.087 against
1/4 and 1/9, for every K and N. The ladder of A10 is unchanged; hydrogen
does not bind under cos. **Different law.** The run: A5s Run 2 with two
clocked bodies of equal content M at s = 8 to 32 on an axis, K = 8M (λ = 8):
the register's change per interval ∝ cos(2πs/8)/s², zero at s = 10, 14,
18, …, sign reversed at s = 12, 20, 28; then with contents M and 2M: the
change oscillating at M/K per interval with zero mean.

## 24. Round 3: the wait, a tick per whole quantum read (point 23)

**The rule, R9 (Highlights 5.4 point 23, PR #278).** A thing that reads a
whole quantum of shadow does not step and does not advance its phase in
that interval; w intervals per quantum, w = 1 the natural value, kept
symbolic. A shadow pays nothing. Rules used besides: R4′, R6′, R7′, and the
standing field of round 1 (section 5: n(r) = 9S_eff/(16πr) quanta per Node
per interval, S_eff = 6ρM(1 − f), G_L = 33ρ(1 − f)/(8π)) or of round 2
(section 19: S = κξM, G = ζκξ/(2π)); in both

```text
n(r) = (9/11) · G M / r   quanta per Node per interval   (G = G_L in round 1, G = ζκξ/(2π) in round 2),
```

the ratio of the density coefficient 9/(16π) to the push coefficient
11/(16π) of section 5 (the same number that made w = 11/9 in section 11
(c)). This is the diffusive field; on the tubes of sections 17 and 22 n
does not fall with r and is zero off the planes, and everything below is
then true on a tube at its own n.

**Assumptions and limit.** n(r) ≪ 1/w (far field; the quanta arrive whole
in a fraction n of the intervals, section 11 (a), the registers making the
arrivals regular). Two readings agree there: the strict one (the interval
of a reading is the wait; several quanta in one interval cost one
interval) and the queued one (w per quantum, always): the fraction of
intervals lost is w n + O(n²) in both. Where w n ≥ 1 the thing never steps
and never ticks under either reading: a **horizon** at

```text
r_h = (9 w / 11) · G M     (w = 11/9: r_h = G M, the capture radius b_c of section 19; GR: 2GM).
```

Note the scale: A6's source (S_eff = 40 262) has n ≥ 1 out to
r = 9S_eff/(16π) = 7208 Links, so at w = 1 every clock within 7208 Links
of it stops; the weakness of gravity must sit in n ≪ 1 at every r of
interest, that is in ξκ, and the wait then inherits it, since one number
(9w/11) G sets both the push and the wait.

**(i) The clock of a thing at rest.** Its phase advances ρ per interval in
the intervals it does not wait, so the mean rate is

```text
ρ_eff(r) / ρ = 1 − w n(r) = 1 − (9 w / 11) · G M / r    (w n < 1; 0 beyond r_h),
```

against general relativity's √(1 − 2GM/(rc²)) = 1 − GM/(rc²) − ½(GM/(rc²))²
− …: the same form at first order, GR's coefficient exactly at **w = 11/9**
(w = 1 gives 9/11 of it), and a different second order (linear here,
−½(GM/r)² there; under the queued reading with the thing still reading
while it waits, 1/(1 + wn) = 1 − wn + (wn)², also different). A loop's
clock is its period (Highlights 3.4), and each ray of the ring loses the
same fraction of its steps, so P/P₀ = 1/(1 − wn) ≈ 1 + wn: the same factor
for the phase clock and the loop clock, section 11 (c)'s form with its
coefficient now derived from a rule rather than posited. Local and in
integers, as point 23 says. **Reached** in form; the coefficient is the
choice of w.

**(ii) Light passing at b.** A light thing reads the mass shadows like any
thing (point 16, times its content) and waits like any thing, so its speed
along its line is 1 − wn(r): an effective index n_eff = 1 + wn(r) =
1 + (9w/11)GM/r. A front (many light things abreast, or the phase pattern
of one emitter's successive things) is delayed more on the near side and
tilts by the standard integral of section 8 (∫ b/(b² + x²)^{3/2} dx = 2/b):

```text
α_front = (18 w / 11) · G M / b     (w = 1: 1.636 GM/b;   w = 11/9: 2 GM/b, Einstein's space half exactly).
```

But a thing moves on its line and turns only by a push (points 10 and 21;
rule (i) of the five settled rules): the wait delays it and does not turn
it. So the **image** (where each light thing lands) is turned by the push
alone, GM/b on the pass and up to another GM/b by the late return (section
19), while the **front** (the phase pattern, read by an interferometer or a
two-slit behind the mass) is turned by push and wait together:

```text
w = 1:     image 1 to 2 GM/b,   front 2.64 to 3.64 GM/b;
w = 11/9:  image 1 to 2 GM/b,   front 3 to 4 GM/b  (4 GM/b with the full return, Einstein's number, in the front only).
```

The delay itself is Shapiro's: Δt = w ∫ n dx = (9w/11) GM [asinh(x_A/b) +
asinh(x_B/b)] ≈ (9w/11) GM ln(4x_Ax_B/b²), half of GR's 2GM ln(4x_Ax_B/b²)
at w = 11/9 and GR's at w = 22/9, where the clock would run at 1 − 2GM/r,
twice GR's slowing. One w cannot serve both, because in GR light's index
carries two metric parts and a clock one (the ratio 2, γ = 1), and here the
same wait serves both (the ratio 1). The push half is changed only at
second order: a slower pass reads (1 + wn) quanta per Link, O((GM/b)²).
**Reached** (the space half of the front's bending, at w = 11/9);
**different law** (the image and the front disagree; Shapiro at half).

**(iii) The redshift.** A clock at r₁ runs at ρ(1 − wn₁), one at r₂ at
ρ(1 − wn₂); the light things between them carry no clock (R7′) and a
static field delays every emission alike, so the received rate against the
receiver's clock is

```text
ν₂/ν₁ = (1 − w n₁)/(1 − w n₂),    z = ν₁/ν₂ − 1 ≈ (9 w / 11) · G M (1/r₁ − 1/r₂),
```

GR's GM(1/r₁ − 1/r₂)/c² at w = 11/9. **Reached** in form.

**(iv) A free thing and a loop.** A push along a thing's own heading
changes its register and never its speed (point 21); the wait changes its
speed and never its register. So in the field of M every thing, whatever
the push's direction, moves at

```text
v(r) = 1 − w n(r) = 1 − (9 w / 11) · G M / r   Links per interval    (0 at r_h),
```

a thing falling in slows and stops at r_h in the lattice frame, the
frozen-star form of the Schwarzschild coordinate speed 1 − 2GM/r (with
w = 22/9 the two are equal, and then the clock is off by 2). Its momentum
still integrates the push exactly, dp/dt = F (section 3): a thing pushed
along its heading gains register at the full rate while moving slower. A
loop of side a at distance r: its period P₀/(1 − wn) as in (i), and a new
thing, a **tidal desynchronisation**: the near-side rays wait
w a |dn/dr| = (9w/11) a GM/r² intervals per interval more than the far
side, and since a corner fires only with both rays present (section 12) the
ring misses a corner after (11/9) r²/(w a G M) intervals unless the corner
table tolerates a lag: the loop is not pulled by the wait, it is sheared by
it. **New** (the slowing, the shear).

**Dictionary.** w ↔ intervals of proper time per quantum of field read;
9w/11 ↔ the ratio of the clock's coupling to the push's; r_h ↔ a horizon
where things freeze; n_eff ↔ a refractive index of the vacuum near mass.

**Verdict.** Gravitational time dilation: **reached** in form, 1 − (9w/11)GM/r,
GR's coefficient at w = 11/9, with a horizon at (9w/11)GM against 2GM and no
second-order term of GR's. The redshift: **reached** with the same w. The
bending: the front gains (18w/11)GM/b, Einstein's second half exactly at
w = 11/9, but the image does not: **different law** (image 1 to 2 GM/b,
front 3 to 4). Shapiro: half of GR's at the w that fixes the clock:
**different law**. The slowing of a free thing in a field and the shearing
of a loop: **new**. The runs: A6 repeated with the wait, reading the
register (unchanged to O((GM/b)²)) and the arrival tick; not with A6's
source, whose S_eff = 40 262 puts every Node of its board inside
r_h = 7208 Links at w = 1 (the light thing never steps: the first thing the
repeated run shows), but with S_eff = 10 (G_L M = 33 S_eff/(48π) = 2.19,
n(8) = 0.22): the register turns by one quantum in about a quarter of the
passes at b = 8 (section 11 (a)) and the arrival is late by
(9w/11) G_L M ln(4x_Ax_B/b²) = 11.4 w intervals for x_A = x_B = 96; and a
two-slit behind the mass for the front; E5's ring placed at
r = 8, 16, 32 from a body of content M for P/P₀ − 1 = (9w/11)G M/r; two
rings at two radii for z.

## 25. Round 3: the verdicts

| Law | Round 2 (section 21) | Round 3: A (R8v), B (R4″), C (R9) | Run |
| --- | --- | --- | --- |
| The front of a release | 4/5 on tubes (R8) | A: **the same, exact** (R8v is the transport identity off head-on pairs); switched-on source: 58 % on the axes, 100 % in the coordinate planes, 0 off, period-4 pulse | E11 under R8v at (24,0,0), (24,1,0), (17,17,0), (14,14,14) |
| Isotropy of the field | anisotropic (tubes) | A: **not reached**; no symbol; the front an octahedron at every order | — |
| Retardation t₉₀ | r on tubes | A: r + O(4) on tubes, ∞ off the planes | A5s Run 2 tick by tick |
| Two-slit fringes of shadows | λ/2 in the strip (R8) | A: **lost** in counts (a₁ + a₂), a push-direction modulation of depth \|a₁ − a₂\|/A | A1 |
| Newton's third law | reached with the return | A: **lost** (the return is collimated outward) | A5s Run 2, the recoil at the source |
| Port-order independence | — | A: **lost** under (M) at every tie; under (P) at V = 0 (every mirror, 1 % of a source) | E11 with a wall |
| A length scale in the force | not reached | B: **reached** as cos(2πM_B s/K)/s², beating at \|M_A − M_B\|/K | A5s with two clocked bodies |
| Bohr's levels | not reached | B: **not reached**: bands about nλ; potential minima (n − ¼)λ, E₂/E₁ = 0.211, E₃/E₁ = 0.087 vs 1/4, 1/9; r_n ∝ n | — |
| Mass ladder | stands, one new condition | B: unchanged; under cos only equal contents bind (no hydrogen) | A10 |
| Coulomb's law at short range | reached | B: **different law**, modulated at λ_e (cos) or flickering (cos²) | A5s at s < λ |
| Gravitational time dilation | not reached | C: **reached** in form, 1 − (9w/11)GM/r; GR's coefficient at w = 11/9; horizon (9w/11)GM vs 2GM | a ring beside a body |
| Gravitational redshift | — | C: **reached**, z = (9w/11)GM(1/r₁ − 1/r₂) | two rings at two radii |
| Einstein's 4GM/(c²b) | not reached (≤ 2) | C: front 3 to 4 GM/b at w = 11/9 (**reached** in the front), image 1 to 2 (**different law**) | A6 with the wait; a two-slit behind the mass |
| Shapiro delay | — | C: (9w/11)GM ln(4x_Ax_B/b²), half of GR's at w = 11/9 | A6 arrival tick |
| Speed of a thing in a field | 1 | C: **new**, 1 − wn(r), frozen at r_h; a loop sheared, period P₀/(1 − wn) | any pushed thing near a body |

Open after this round, one line each: the self-consistent tie rule of R8v
at a wall (the standing pattern in front of a mirror); the age distribution
of a diffusive field (the wash-out radius of B's pattern beyond √(Dλ));
the second order of the wait (strict against queued reading, and what the
thing reads while it waits); the corner table's tolerance to a lag (whether
a sheared loop breaks or drifts).

## 26. Round 4: the Node mixes the six, as an operator

Round 4 (2026-09-18, after PR #281) derives what the rule of Highlights 5.4
point 24 gives, bottom-up from the stated operator, with no physics assumed.
As before: no engine run, no edit to the engine; every number is checked by
an iteration of the stated operator on a box of 41³ to 81³ Nodes (seconds),
in floating point for the linear part and with the integer rule for section
30, cited after each derivation and never used as its source. The scripts
are the scratch files of this round, not committed.

**The rule, R10 (point 24).** Per Node and per owner, the six arrivals of an
interval are amplitudes A_p = √(amount_p)·e^{iφ_p}, p the Port they came in
through (from the neighbour x + e_p, so their heading is −e_p), the phase on
the circle of N steps. Each Port sends out

```text
B_p = (1/3) Σ_q A_q − A_p        (S = (1/3)J − I on the six Ports),
```

toward x + e_p; the amounts leaving are the total arriving shared in
proportion to |B_p|² in whole quanta, the remainders owned by the Node
(section 3.17's registers, now parked shadows by point 22), each share
carrying the phase of B_p; every share then moves one Link (R2). The return
of a pushed shadow (point 3) walks the trace and is not mixed. The prefilled
standing set, the pushes and the marks are as in points 1 to 23. Rules used
besides: R2, R3 (standing reading), R4′, R5, R6′, R7′, R9.

**Assumptions and limit.** One owner (the mixing is per owner; shadows of
different owners cross). The mean field of the integer rule is the linear
map on amplitudes (below); section 30 says where the integers break it. The
board large.

**(i) The matrix.** S = 2P − I with P = J/6 the projector on the uniform
vector: S is real, symmetric, S² = I, so S is orthogonal (unitary on
complex amplitudes), a Householder reflection. Its eigenvalues are +1 (once,
the uniform vector: six equal arrivals leave unchanged) and −1 (five times:
any six arrivals of zero sum are sent back with the sign reversed). A lone
arrival A on one Port leaves as −(2/3)A through its own Port and (1/3)A
through the five others: the amounts 4/9 back, 1/9 on each other heading,
point 24's numbers; its signed flux Σ amount·heading is reversed and cut to
a third (in: A² on +x; out: −A²/3 on +x). Nothing is declared: (2/n)J − I
is the only matrix that is symmetric under the Port permutations, orthogonal
and not ±I or a permutation. In the heading basis (W_h = A_{−h}) the same
matrix reads (1/3)J − Π with Π the flip h → −h: the Grover coin of the six
Ports composed with the reflection, which is the transmission-line node.

**(ii) The exact identities.**

- *Amount (unitarity).* Σ_p |B_p|² = Σ_p |A_p|² at every Node, so the
  amount leaving equals the amount arriving in the mean field, and the
  integer rule's shares sum to the arriving whole quanta by construction.
  Continuity holds exactly with the Link current Φ(x, x + e_p) = |B_p(x)|² −
  |B_{−p}(x + e_p)|²: n(x, t + 1) − n(x, t) = −Σ_p Φ(x, x + e_p), and
  Gauss's law in flux form (section 1) follows as before, an identity of
  the operator. The remainder rule adds a bounded parked amount per Node
  and Port, as in section 0.
- *Amplitude (Kirchhoff).* Σ_p B_p = 2Σ_p A_p − Σ_p A_p = Σ_p A_p: the
  Node conserves the amplitude sum as well as the amount. Hence, with
  u(x, t) = (1/3) Σ_p A_p(x, t) (the Node's common part; B_p = u − A_p),
  the total Σ_x u is conserved exactly, and the real and the imaginary
  part separately, since S is real.
- *The wave equation.* From B_p = u − A_p and R2, A_p(x, t + 1) =
  u(x + e_p, t) − A_{−p}(x + e_p, t) and A_{−p}(x + e_p, t) = u(x, t − 1) −
  A_p(x, t − 1); summing over p,

```text
u(x, t + 1) + u(x, t − 1) = (1/3) Σ_p u(x + e_p, t),        i.e.
u(t + 1) − 2u(t) + u(t − 1) = (1/3) Δ_lattice u(t),
```

  the lattice wave equation of the transmission-line matrix (Johns and
  Beurle 1971), exact at every Node and tick, for the real and the
  imaginary part alike. The amounts are the six |A_p|², not u², and are
  recovered from u by the two relations above.
- *The signed flux is not conserved by the Node.* J = Σ_h amount_h h
  changes at every Node (the lone share: −1/3 of itself); no local law of
  the form "J in = J out" exists, and the momentum the field carries is not
  Σ amount·heading. What a thing reads is J at its Node (R4′), so what J is
  in a wave is the question, answered in (iii).

**(iii) The dispersion relation and the plane wave.** With u = ū e^{i(k·x − ωt)}
the wave equation gives

```text
cos ω = (1/3)(cos k_x + cos k_y + cos k_z),
```

real ω for every k (the right side lies in [−1, 1]: no growing mode, the
scheme is stable, as unitarity demands). The Port amplitudes of the plane
wave are A_p = ū (e^{iω} − e^{ik·e_p})/(2i sin ω), and from them, exactly
at every k,

```text
n = Σ_p |A_p|² = 3|ū|²,        J = n · v_g,   v_g = ∇_k ω = (sin k_x, sin k_y, sin k_z)/(3 sin ω),
```

with the amount per Port |A_p|²/n = (1 − cos(ω − k·e_p))/(6 sin²ω). The
push a thing takes per interval from a plane wave is the amount per Node
times the group velocity, the energy flux of the wave, constant in time
although every amplitude oscillates; and the Link current on the axis
equals it, Φ_i = J_i (ζ = 1 in section 19's notation, against 11/8 for the
diffusive field). Two opposite waves of equal amount give J = 0 with n = 6|ū|²
passing through: the model owner's "a cancellation is a zero flux with the
amounts passing through, nothing destroyed" is this identity. Expanding,

```text
ω² = k²/3 − Σᵢkᵢ⁴/36 + (k²)²/108 + O(k⁶),
```

so the phase speed is (1/√3)(1 − k²(K₄/24 + 1/90)) with K₄ = Σk̂ᵢ⁴ − 3/5:
(1/√3)(1 − k²/36) on an axis, (1/√3)(1 − k²/144) on (110), and exactly
1/√3 at every k on (111), where cos ω = cos(k/√3). On an axis ω rises to
arccos(1/3) = 1.231 at k = π with v_g = 0 there: a stop band, the lattice
carries no axis wave shorter than two Links. Over the whole zone
|v_g|² = Σsin²kᵢ/(9 − (Σcos kᵢ)²) ≤ 1/3 (by Σcos²kᵢ ≥ (Σcos kᵢ)²/3), with
equality only for k ∥ (111): **no signal of the mixed field outruns 1/√3 in
any direction, at any wavelength (exact)**, and the octahedron |x|₁ = t of
the walk's support carries only an exponentially small precursor.

**Check.** A random complex state on 16³: unitarity per Node to 1.4·10⁻¹⁴,
the amplitude sum to 3.6·10⁻¹⁵, S² = I to 10⁻¹⁵, the wave-equation residual
9·10⁻¹⁶, the continuity residual 1.2·10⁻¹⁴. Plane waves on 32³ at six k
(axis, (110), (111), up to k = 0.98): ω measured from one step equals
arccos((1/3)Σcos kᵢ) to six digits, n/|ū|² = 3.0000, J = n·v_g to five
digits (1.72648 at k = 2π/32 on the axis, (1, 1, 1) exactly at k ∥ (111)).
The maximum of |v_g| on a 121³ grid of the zone: 0.57735 = 1/√3. The lone
share: (0.1111, 0.4444, 0.1111 ×4) and J out = −1/3.

**Verdict.** Unitarity and continuity: **reached exactly**. The lattice
wave equation of TLM with cos ω = (1/3)Σcos kᵢ: **reached exactly**, for the
amplitude's common part u. J = n·v_g and Φ = J for a wave: **new** (the push
is the energy flux; ζ = 1). A conservation law for the signed flux:
**not reached** (none exists; the Node reverses a lone share's flux).

## 27. Round 4: the continuum limit, the front, the far field and the standing part

**Rules used.** R10, R2, R3 (standing reading), section 26.

**(i) The wave speed and the equation.** At k → 0, ω = k/√3: the field
propagates at

```text
c_w = 1/√3 = 0.577 Links per interval    (the TLM speed on a cubic mesh, 1/√d in d dimensions),
```

isotropic at leading order, with the continuum equation of the common part

```text
∂²u/∂t² = (1/3) ∇²u + (1/36) Σᵢ ∂ᵢ⁴u − (1/108) ∇⁴u + O(∂⁶),
```

the anisotropic term at order k⁴ (the cubic invariant Σkᵢ⁴, as section 2's
for the diffusive symbol). It is a wave equation, which no rule on amounts
gave (section 6's obstruction): the reflected share −(2/3)A carries the
sign, and the sign is the heading, as point 24 says.

**(ii) The tube theorem overturned (against section 17).** Under R8 and R8v
a one-phase release stayed on the coordinate planes for ever (4/5 on the
light-cone edge, 0 off the planes, section 22). Under R10 the six lone
shares X/6 leave the origin, and at the first Node each is reflected
(4/9) and scattered (1/9 ×5): from the second tick on there is content off
the axes, from the third off the planes, and the backward shares of
neighbouring Nodes cancel by sign, which is what makes the spherical wave.
The share off the three coordinate planes at t = 3, 5, 10, 20, 30 is
0.198, 0.678, 0.693, 0.828, 0.890 (a uniform shell at r = 17 would have
0.91 off the planes: the field fills every direction); on the six axes
0.004 at t = 30; on the light-cone edge |x|₁ = t, 0.178, 0.086, 0.057 at
t = 10, 20, 30, falling as 1/t, and that content sits at the face centres
(t/3, t/3, t/3) of the octahedron, Euclidean t/√3, which is the wave front
itself and not a tube. The shell of maximal amount is at r = 5, 10, 16 at
t = 10, 20, 30 (0.53 t; the peak lags the front at t/√3 = 5.8, 11.5, 17.3).
**A one-phase release is not confined to axis lines or planes (exact
from the second tick; measured 89 % off the planes at t = 30).**

**(iii) The front's sharpness and anisotropy.** The front of a pulse moves
at the maximal group speed, 1/√3 in every direction (section 26 (iii)),
but it is sharp only where the dispersion vanishes: along (111) the pulse
keeps its shape (ω = k/√3 exactly), along an axis it is dispersive (the
short waves lag, the shortest stop), so the edge there is an Airy-type
smear whose width grows as t^{1/3}, and it is weak, since a point release
is broadband and the axis carries only its long waves. Measured (the
amount at the Node and its six neighbours per tick, 61³, one-phase
release): at r = 12.1 on (111) the passing pulse peaks at tick 24 (√3 r =
21) with its 10–90 % width 6 ticks and a peak amount 1.0·10⁻²; at r = 17.3
on (111) it peaks at 33 (30), width 6; on (110) at r = 12.7 and 17: peaks
at 29 and 39 (22, 29), widths 11 and 12; on the axis at r = 12 and 18:
peaks at 39 and 35 (21, 31), widths 20 and 14, peak amounts 3.2·10⁻⁴ and
6.9·10⁻⁵, thirty times below (111) at the same r. So **the front is at
√3 r in every direction, sharp (6 ticks) on the body diagonals and smeared
(14 to 20 ticks) on the axes, and a short pulse favours the diagonals by a
factor 30 in amount at r = 12**; a long wave (a clocked thing's field, (v))
is nearly isotropic, with the first-order anisotropy of (v). The
retardation of a switched-on clocked source (period 16; the period-mean
of J_r at the Node and its six neighbours, 61³, 120 ticks) reaches 90 % of
its steady value at t₉₀ = 22, 27, 31 for r = 12.1 on (111), 12.7 on (110)
and 12 on an axis (√3 r = 21.0, 22.0, 20.8), and at 32 and 45 for r = 17.3
on (111) and 16 on an axis (30.0, 27.7):

```text
t₉₀ = √3 r + 1 to 2 on the body diagonals,  + 5 on (110),  + 10 to 17 on the axes   (r = 12 to 17),
```

∝ r, against 1.925 r² of section 6 and r on the tubes only of sections 17
and 22.

**(iv) The standing part: the flat bands.** The one-step map on the six
amplitudes at wavevector k, U(k) = D(k)·Π·S, has the eigenvalues e^{±iω(k)}
once each (the wave) and +1 twice and −1 twice, independent of k (computed
at three generic k; the trace of the mean flat projector over the zone
3.99999). Four of the six bands are flat: their content does not move,
it stands (+1) or flips sign every tick (−1) where it was put. The
standing fraction of an initial state at one Node is its projection on the
flat bands, integrated over the zone:

```text
a lone share on one heading:            2/3 stands, 1/3 radiates         (exact, the zone integral 0.66667);
six equal shares in one phase:          0 stands, all radiates            (exact, 2·10⁻¹⁹);
a plane wave:                            0 stands                          (exact).
```

The iteration (61³, a lone share of amount 1 at the origin): the amount
within r ≤ 3 is 0.966, 0.748, 0.678, 0.669, 0.6648 at t = 4, 8, 12, 16, 40
(the two-tick mean; the origin Node itself holds 0.535), converging to
2/3. This is "what stays standing beside a thing" (point 24's third thing
to measure): a shadow re-released alone on the heading it came home on
(the orchestrator's re-release rule) leaves two thirds of itself standing
at the owner's Node for ever and sends one third out as a pulse; six
re-released together in one phase send everything out. The standing set of
point 11 is, under R10, this flat-band content: exact eigenstates of the
operator, localized, costing nothing and never leaving.

**(v) The far field of a source.** Three sources, each with its result.

*A constant one-phase source* (a clockless thing re-releasing every tick
what came home, or the emitting reading of R3 at rate 0: amplitude a on six
Ports every tick). The source in the u equation is −2a at the Node and
+a/3 at each of its six neighbours, of zero sum: **no monopole**, no 1/r
potential, no far field. The iteration (41³, 80 ticks): the source Node's
own standing set settles at A_p = −0.50 a on its six Ports (u = −1.0 a),
so that what leaves is 0.50 a per Port and is sent back by the neighbours'
standing pattern; the amount at (8, 0, 0), (12, 0, 0) and (7, 7, 7) is
0.000 at t = 20 to 60, the total amount 9.5 a² of which 4.1 within r ≤ 3
and the rest in the single switch-on shell that left once. **A clockless
thing at rest has no far field under R10: its constant release is cancelled
by the standing set it builds.**

*A switched-on clocked source* (a thing of rate ρ = M/K turns per interval
re-releasing at its current phase: amplitude a e^{−2πiρt} on six Ports
every tick). This is a monochromatic source of the wave equation at
ω₀ = 2πρ, and by section 26 (iii) its far field is a spherical wave of
wavenumber k₀ = √3 ω₀(1 + ω₀²(K₄(r̂)/8 + 1/30)), that is of wavelength

```text
λ_w = 2π/k₀ ≈ 1/(√3 ρ) = K/(√3 M) Links   (the Compton length of section 18 over √3),
```

with the amount n(r) = 3|u|² ∝ 1/r² and the push J = n v_g ∝ 1/r² outward
at every angle. The lattice's first-order anisotropy, from the stationary
phase on the dispersion surface (|G|² ∝ 1/(|∇_k D|² 𝒦 r²), 𝒦 the Gaussian
curvature of cos ω₀ = (1/3)Σcos kᵢ, computed with Δ_S K₄ = −20 K₄):

```text
n(r, r̂)  = (√3 S / 4π r²) [1 − (3/2) ω₀² K₄(r̂) + O(ω₀⁴)],
J_r(r, r̂) = (S / 4π r²) [1 − (15/8) ω₀² K₄(r̂) + O(ω₀⁴)],     v_g(r̂) = (1/√3)[1 − (3/8) ω₀² K₄(r̂)],
```

S the flux (amount per interval) the source sends out; the field is
weaker on the axes (K₄ = 2/5) than on the diagonals (−1/10, −4/15), by the
fixed fraction (15/8)(2/5 + 4/15) ω₀² = 1.25 ω₀² between an axis and (111),
**independent of r**: the anisotropy of the wave field does not decay with
distance, as the diffusive field's (145/4)K₄/r² did, and for a thing of
content M it is 1.25 (2πM/K)² = 49 (M/K)². **1/r² at every angle: reached
for a clocked thing**, with a fixed angular modulation of relative size
(15/8) ω₀² K₄.

*A finite standing set.* Under the standing reading a clocked thing's set of
total X is the wave above cut at the radius R its profile declares, and it
flows out at S = X/(√3 R) per interval for √3 R intervals and is gone
unless the board returns it: like section 5's, the force constant is the
profile's flux and must be declared with the profile (κ = 1/(√3 R) in
section 19's notation); unlike section 5's, what is not returned leaves
at 1/√3 instead of spreading to a uniform density.

**Check.** The switched-on clocked source on 81³ with a sponge, averaged
over one period after 150 ticks: at period 16 (ω₀ = 0.393, λ_w = 9.2)
J_r/n = 0.632, 0.603, 0.592, 0.589 on the axis at r = 8 to 20 and
0.567 to 0.578 on (110) and (111) (→ 1/√3 = 0.577); 4πr²J_r/S with S the
flux of J through the cube of half-width 8: axis 0.909, 0.852, 0.848, 0.811
at r = 8, 12, 16, 20; (110) 0.916, 0.915, 0.916, 0.914; (111) 0.928, 0.929,
0.946, 0.948; the flux of J through cubes of half-width 4, 8, 12, 16 is
1.039, 0.907, 0.864, 0.843 of the reference (J differs from the Link
current by the forward difference of the outward amount, ∝ 2/r, so J's
flux converges to Gauss's as 1/r). The ratio axis/(111) at r = 16 to 20 is
0.90 to 0.86 against the first-order 0.884/1.077 = 0.82. The steady state
by the lattice resolvent (256³ FFT of 1/(2cos ω₀ − (2/3)Σcos kᵢ + iη)) at
period 32 (ω₀ = 0.196, λ_w = 18.5): r²n relative to the directional mean at
r = 24, 36, 48, 60 is 0.962, 0.954, 0.948, 0.959 on the axis, 1.007 to
1.014 on (110), 1.022 to 1.041 on (111), constant in r, against the
first-order 0.977, 1.006, 1.016: the same sign and order (the first order
underestimates by about half at this ω₀; at period 16 the ordering holds
with 0.83, 1.03, 1.12 at r = 24 to 48). The constant source, the release
and the lone share: the numbers quoted in (ii), (iv), (v).

**Verdict.** The wave equation with c_w = 1/√3: **reached exactly** as the
continuum limit. The front fills every direction: **reached** (the tube
theorem of sections 17 and 22 does not hold under R10; 89 % off the planes
at t = 30). A sharp isotropic front: **different law** (sharp on (111),
Airy-smeared on the axes, a short pulse thirty times weaker on an axis).
t₉₀ ∝ r: **reached** (√3 r + 1 to 17 by direction). The far field 1/r² at every angle:
**reached** for a clocked thing, with a fixed first-order anisotropy
(15/8)ω₀²K₄; **not reached** for a clockless thing (no far field at all).
The standing part: **new** (2/3 of a lone re-release; 0 of a symmetric
one; four flat bands of six).

## 28. Round 4: the wave against the causal speed

**Rules used.** R10, R6′ (a thing moves one Link per interval), R9 (the
wait), section 26.

**What an observer measures.** A thing of light from A reaches B at
distance r after |x_B − x_A|₁ intervals, between r and √3 r; a change in
A's field (a wave front) reaches B after √3 r in every direction (section
26 (iii): nothing in the mixed field outruns 1/√3). So an observer at B
sees the light of A's move before the field of A's move, by (√3 − 1) r =
0.73 r intervals on an axis and by 0 to 0.73 r on a diagonal (light on the
L1 path takes √3 r on (111), the same as the wave). The retardation of
the force is √3 r, the delay of light r to √3 r. Every free thing moves
at speed 1 > 1/√3: **every thing outruns its own field**, and the field
of a moving thing is a Mach cone behind it of half-angle arcsin(1/√3) =
35.3° (in the continuum limit; on the lattice the cone is dressed by the
front's anisotropy), not the contracted Coulomb field of a moving charge.
A pushed shadow returning on the trace at one Link per interval (section
32) arrives before the field change that follows it.

**Is there an identification that makes the two speeds equal?** No, on
three counts. (a) The lattice unit: things and shadows walk the same
Links in the same intervals, and c_w = 1/√3 is a number of the mesh, the
TLM speed 1/√d for six Ports, not of any unit; a two-dimensional board
would give 1/√2 and a line 1. (b) N: the phase circle enters only the
rounding of the phase (section 30), not the linear map; the dispersion
relation has no N in it. (c) The wait of point 23: it slows things and
never shadows (a shadow pays nothing), so it moves light toward 1/√3
rather than the field toward 1: a light thing runs at 1 − w n (section 24
(ii)), equal to 1/√3 only where w n = 1 − 1/√3 = 0.423 quanta read per
interval, a dense field with the clock at 0.58; in the far field of
anything, light is at 1 and the field at 1/√3. A speed-1 field would need
a different node (in TLM the speed is set by the number of Ports and their
impedances; equal Ports on the cubic mesh give 1/√3 and nothing else), that
is, a different declaration, not a parameter of this one.

**Prediction.** Under R10, the field of a thing propagates at 1/√3 of the
causal speed: the recoil of a source pushed by a thing that moves (E11 (a)
repeated with a moving pusher) arrives r√3 intervals after the move, the
light of the move r to √3 r; a two-thing run with A displaced by one Link
at tick t₀ reads B's register change at t₀ + √3 r + 2 (on (111)) to
t₀ + √3 r + 17 (on an axis), never at t₀ + r; and a thing moving on a line
leaves its field in a cone of 35° behind it. **Different law** (c_w = c/√3;
the retardation of the force √3 r against r; the Mach cone).

## 29. Round 4: two slits and a mirror

**Rules used.** R10, the wave equation of section 26 (linear in the
amplitudes, so superposition holds), R4′ (a thing reads J), point 6 (a mark
counts nothing of a field), E5 (a thing meets its own shadows as home).

**Two slits.** A clocked owner's field (section 27 (v)) is a monochromatic
wave of wavelength λ_w = K/(√3 M); behind a wall with two slits at
(0, ±d/2, 0) the common part at the screen Node (L, y, 0) is the sum of
two spherical waves, u = u₁ + u₂ with u_{1,2} ∝ e^{ik₀ r_{1,2}}/r_{1,2},
and the amount is n = 3|u|² locally (section 26 (iii)): the cross term
2√(n₁n₂) cos(k₀(r₁ − r₂)) is real, since the amplitudes have signs, which
R8 and R8v could not produce (sections 17 and 22). For L ≫ d the pattern is

```text
n(y) = n₁ + n₂ + 2√(n₁n₂) cos(2π d y/(λ_w L)),    fringe spacing λ_w L/d,   depth 2√(n₁n₂)/(n₁ + n₂) (1 for equal slits),
```

optics' law, and the push on a row of things behind the slits is
J = n v_g (radial), modulated with the same fringes: **fringes in the
push**, of the optical spacing λ_w L/d everywhere on the screen, against
λ/2 in the strip only (R8) and none (R8v). In counts: a mark counts nothing
of a field (point 6), so the fringes of shadows are read only as pushes;
a thing meets its own shadows as home (E5) and one thing at a time shows
no self-interference, as in sections 17 and 22, so the fringes of things
scale with the coincidence rate, unchanged (A1). (In the exact lattice
form n is Σ_p|A_p|² of the six Port amplitudes, which for two crossing
plane waves of headings k₁, k₂ is n₁ + n₂ + 2Re Σ_p A_{1p}A*_{2p}, a cross
term whose weight against 2√(n₁n₂) is the overlap of the two Port vectors,
1 at small angle and cos-like at large angle: the fringe depth on the
lattice is that overlap, 1 at k₁ = k₂ and (1 + cos θ)/2 at long wavelength
for waves at angle θ, derived from section 26's A_p; at the two-slit
angles d/L ≪ 1 it is 1.)

**A mirror.** A wall that returns (a mark, or a thing's table: a shadow
that arrives turns back with its amount and its phase, point 6) is the Port
rule B_p = A_p at the wall Node in place of u − A_p: reflection coefficient
+1 on the amplitude. In front of it the incident and the returned waves
form a standing wave of the common part, u = 2ū cos(k₀x + θ) e^{−iω₀t} for
normal incidence, of period λ_w/2 = π/k₀ in the amounts. Two things
distinguish the lattice from a scalar field. First, the net flow is zero
but the push is not: the Link current Φ (what continuity conserves)
vanishes in the time mean at every Link, while J at a Node, which is what
a thing reads, differs from Φ by the forward difference of the outward
amount (section 26 (ii)) and oscillates with x:

```text
Φ = 0,    J_x(x) = ±(k₀/3) n · sin(2k₀x + θ′) + O(k₀³),    n(x) = 2n₀ [1 + (k₀²/6) cos(2k₀x + θ″) + O(k₀⁴)],
```

n₀ the amount of one wave (derived from the Port amplitudes A_p of section
26 (iii) for the two waves ±k₀; the coefficients are exact expansions of
the six-Port sums). So a thing at rest in front of a mirror is pushed
toward or away from the wall by up to (k₀/3) of the amount at its Node,
with the sign changing every λ_w/4, a standing ladder of force of period
λ_w/2 whose mean over a period is zero; and the amount itself is nearly
flat, modulated at depth k₀²/6 only (0.08 at λ_w = 9.2, 0.007 at
λ_w = 31), not the full cos² of a scalar standing wave: the amounts of the
two waves pass through each other almost uniformly while the push
alternates. **Reached** (a standing wave of period λ_w/2, zero net flow);
**new** (the push oscillates at (k₀/3) n and the amount at k₀²/6: the
lattice's Port structure, which no scalar field has).

**Check.** *Two slits* (R10 iterated on 97 × 97 × 17 with a plane source
at x = 6 of period 16, a returning wall at x = 30 with two slit lines
d = 16 apart, the screen at L = 48 behind it, a sponge on the x and y
edges, 420 ticks, the mean over the last period): the push J_x along the
screen has its maximum at y = 0 (109·10⁻⁴), minima at y = ±15
(0.7·10⁻⁴) and the next maxima at ±31 (91·10⁻⁴), against the first
minimum at y = 14.7 from the exact path difference √(L² + (y + d/2)²) −
√(L² + (y − d/2)²) = λ_w/2 (λ_w = 9.24; the small-angle spacing λ_w L/d =
27.7): the optical fringes, with the depth (109 − 0.7)/(109 + 0.7) = 0.99
in the push and 0.96 in the amount (193 against 4.0). *The mirror* (R10
iterated on 129 × 5 × 5 with a plane source of period 16 at x = 10, the
returning wall at x = 110, 900 ticks): the field in front of the wall is
two waves of equal weight at ±k₀ (the spectrum of the +x-moving Port
amplitude: 26.0 at +k₀ and 7.5 at −k₀, mirrored for the −x-moving one,
nothing else); the amount n(x) runs between 2.27 and 2.67, depth 0.081
against k₀²/6 = 0.079 at k₀ = 0.689; J_x(x) runs between −0.53 and +0.54,
amplitude 0.22 of the mean amount 2.46 against the exact two-wave value
0.220 (k₀/3 = 0.230), with its mean +0.005; the period of both 4.5 Links
against π/k₀ = 4.56. The exact two-wave state built from the Port
amplitudes gives the depth 0.0790 and the J amplitude 0.2204 for every
relative phase θ.

**Verdict.** Two-slit fringes of shadows in the push: **reached**, the
optical law λ_w L/d at full depth (0.99); in counts: none (point 6), and
no self-interference of a thing (E5). A mirror: **reached** as a standing
wave of period λ_w/2 with zero net flow; the push in front of it
oscillating at (k₀/3) n with zero mean and the amount nearly flat: **new**.

## 30. Round 4: the integer rule

**Rules used.** R10 in its integer form: at each Node the whole quanta
arriving, n_in = Σ_p amount_p, are shared over the Ports as ⌊n_in|B_p|²/Σ|B|²
+ ρ_p⌋ with ρ_p the Node's remainder register for that Port (a parked
shadow, point 22), the register keeping what is not whole; the leaving
share carries the phase of B_p, rounded to the circle of N steps; the
prefill rounds the declared profile to whole quanta per Node and heading
with the fractions in the registers (Highlights 5.4, "A thing does not
emit", the second rule).

**(i) What a wave needs in whole quanta.** By section 26 (iii) a plane wave
of amount n per Node has, at long wavelength, (1 + √3)²/12 = 0.622 n on
the Port moving with it, (1 − √3)²/12 = 0.0447 n on the Port moving against
it, and 1/12 = 0.0833 n on each of the four transverse Ports (at
λ = 16 Links: 0.616, 0.046, 0.084 ×4, exact). The wave is the cancellation
of the backward and transverse shares between neighbours; a rounding that
moves one quantum on a Port whose share is a few quanta destroys that
cancellation at that Node. So n must be large against 1/0.045 = 22 for the
smallest share to be whole at all, and larger for the cancellation to
hold: **the wave is a many-quanta phenomenon per Node.** A prefill with
fewer than 6 quanta per Node has no whole quantum on any Port and goes
entirely into the registers, where nothing moves it: the wave does not
start.

**(ii) Where the rounding puts what it takes.** The linear map has no
diffusive mode (its six bands are two waves and four flat bands, section
27 (iv)), so the rounding error, a perturbation of one quantum at a Node,
becomes standing flat-band content (2/3 of a lone perturbation) and
incoherent waves (1/3): **the rounding creates no diffusive part; it
creates standing content and noise**, and the amount it takes from the
wave stays where it was taken. The coherent push J of the wave is what
decays.

**(iii) The survival table.** A plane wave along an axis in a periodic 16³
box, N = 64, registers, the push ⟨J_x⟩ over the box against the linear
value n v_g, averaged over the 16 ticks ending at t = 32, 64, 128, 256,
512:

```text
quanta per Node     λ = 16 Links                              λ = 8 Links
      32            0.85  0.85  0.42  0.54  0.37               0.83  0.59  0.45  0.49  0.02
      64            0.94  0.89  0.86  0.75  −0.01              0.93  0.88  0.66  0.23  0.01
     128            0.97  0.97  0.98  0.97  0.92               0.97  0.97  0.90  0.79  0.74
     256            0.99  0.99  0.99  0.99  0.99               0.98  0.99  0.98  0.98  0.99
    1024            1.00  1.00  1.00  1.00  1.00               0.99  0.99  0.99  0.99  0.99
    4096            1.00  1.00  1.00  1.00  1.00               1.00  1.00  1.00  1.00  1.00
```

and at 8, 16 and 24 quanta per Node the push is 0.00 ± 0.1 from t = 16 on
(dead within a wavelength of travel). At 256 quanta per Node the wave
holds over 500 intervals at 99 % of its push; at 128 it loses 8 % (λ = 16)
to 26 % (λ = 8) in 500 intervals; at 64 it is gone by 500; at 32 by 100.
The phase circle: N = 64 changes nothing against unquantized phases; N = 8
caps the push at 0.93 of the linear value at every amount (0.925 at 256,
0.933 at 1024: the coherent fraction of a phase rounded to ±π/8 is
(sin(π/8)/(π/8))² = 0.95, less the register's part), so N = 8 is a 7 %
loss of force and N ≥ 64 none. Where the wave dies, its amount is 30 to
50 % in the flat bands (the projector of section 27 (iv) applied to the
state at t = 128: 0.32 to 0.52 at 8 to 32 quanta per Node, 0.02 at 64,
0.00 at 256), the rest incoherent waves; the registers hold 2 to 5 quanta
per Node throughout. The largest-remainder (Hamilton) variant, which parks
nothing and gives the leftover quanta to the largest fractions, behaves
the same to the digits shown at 64 and 256 quanta per Node.

**The smallest amount for the wave to survive:** about **256 quanta per
Node** for a field that keeps its push over hundreds of intervals (128 for
tens, 64 for a few wavelengths of travel). In the far field of a clocked
thing, n(r) = √3 S/(4πr²) ≥ 256 requires r ≤ 0.023 √S: a source of
S = 10⁶ quanta per interval carries a wave to r = 23 Links and a standing,
incoherent field beyond; the wave of a shadow set is, in whole quanta, a
near-field object unless X is enormous, and the 1/r² push of section 27 (v)
is read in the engine only inside that radius.

**Check.** The table above (16³, 512 ticks, seconds each); the linear
plane wave's flat-band fraction 0.000000 and its Port shares 0.0463,
0.6161, 0.0844 ×4 at λ = 16; the prefill at 1, 2 and 4 quanta per Node
giving n = 0.00 after rounding.

**Verdict.** The wave survives the integer rule: **reached** above about
256 quanta per Node (N ≥ 64), **not reached** below 64. A spurious
diffusive part: **none** (the rounding makes standing content and noise;
the operator has no diffusive mode). The phase circle: N = 8 costs 7 % of
the push, N ≥ 64 nothing. **New**: the radius 0.023 √S inside which the
engine's field is a wave.

## 31. Round 4: Coulomb and Newton under the mixed field

**Rules used.** R3′ (one shadow set, X = ξM), R4′ (the two readings of
points 16 and 18), R5, R7′ (rate M/K), R10, sections 19, 26, 27.

**The push.** A thing B at distance r from a clocked thing A reads, per
interval, J_A(B) = n v_g = S_A/(4π r²)[1 − (15/8)ω_A²K₄(r̂)] (section 27 (v);
ω_A = 2πM_A/K), constant in time for the monochromatic wave although the
amplitudes oscillate; the reading multiplies it by M_B (mass) or by
(q_A/M_A) q_B (charge), and B's own wave pushes A by the same law with
A ↔ B, the recoil returning on the trace (section 32). With S_A = κ ξ M_A
(κ = 1/(√3 R) for a set of extent R, section 27 (v)) section 19's algebra
goes through with ζ = 1:

```text
F_B = k_C q_A q_B / r² r̂_AB [1 − (15/8) ω² K₄(r̂)],   F_B = −G M_A M_B / r² r̂_AB [the same bracket],   k_C = G = κ ξ /(2π),
```

the product laws, the sign rule, the equivalence principle and k_C = G as
in round 2, **reached**, with three modifications. (1) **The angular
factor**: a fixed anisotropy of relative size (15/8)ω²K₄(r̂), ω the
*owner's* rate 2πM/K (so the bracket in F_B carries ω_A² for A's wave on B
and ω_B² for B's wave returned to B), 1.25(2πM/K)² between an axis and a
body diagonal, not decaying with r; for ω ≤ 0.1 (a content below K/63) it
is below 1.3 %, and the wave equation's own condition on the clock (point
19: the phase step per interval below half the circle, M/K < 1/2) allows
ω up to π where it is total. (2) **The retardation**: a change of either
thing's field reaches the other after √3 r, not r (section 28). (3)
**The source**: only a clocked thing has a far field (section 27 (v)),
and the flux S = X/(√3 R) of a finite standing set lasts √3 R intervals
unless returned; a clockless thing (light) pushes nothing at a distance,
which is consistent with light having no rest. Under the rounding of
section 30 the law holds where n(r) ≥ 256 quanta per Node, r ≤ 0.023 √S.

**No length scale in the force from the phase.** J reads amounts and no
phase, and for a monochromatic wave the amounts per Port are constant in
time (section 26 (iii)): the Compton pattern of section 18 is present in
the amplitudes and read by nothing; section 23's standing modulation
cos(2πM_B s/K)/s² appears only under R4″, which point 24 does not adopt.

**Check.** J = n v_g and Φ = J of section 26 (five digits); the 1/r² and
the angular numbers of section 27's check; the algebra of section 19.

**Verdict.** Coulomb's product law and Newton's, with k_C = G: **reached**
(ζ = 1), **modified** by a fixed lattice anisotropy of first order
(15/8)(2πM/K)²K₄(r̂), a retardation √3 r, and the requirement of a clock on
the source and of 256 quanta per Node at the receiver.

## 32. Round 4: the return on the trace inside a mixed field

**Rules used.** R5 (the return), point 24's exemption ("the return of point
3 stays a walk back on the trace, never a spread"), R10 for everything
else, section 4.

**The return is exempt, so the third law is exact.** A shadow that pushed
B turns back carrying its amount and −Δp and walks the trace home at one
Link per interval, unmixed: it crosses the mixed field of its owner (and of
everyone) without combining, so nothing of the −Δp is scattered, reversed
or collimated on the way, the failure of R8v (section 22 (v)) does not
occur, and the identity of section 4 holds in integers: Δp_owner(t_meet +
s) = −Δp_thing(t_meet), Σ p over things constant once the returns are home.
The number of steps s: under R10 a share at B is a sum over paths of many
lengths and has no step count of its own; what the rule gives it is the
trace, that is the Link path to where the owner is, s = |x_B − x_A|₁ for an
owner at rest (r on an axis, √3 r on (111)), and the trace of the owner's
moves otherwise. So the recoil arrives after |x|₁ ≤ √3 r intervals, **at or
before the field's own retardation** (section 28): the reaction reaches
the owner no later than any change of its field reaches the pushed thing.
**Reached exactly** (the third law in the books, delayed by |x|₁).

**What the return does at home.** By R5 a returning shadow is absorbed
and, under the standing reading, leaves again "back out along the line it
came home on" (the orchestrator's elaboration): a lone share on one
heading, of which 2/3 stands at the owner's Node in the flat bands and 1/3
radiates (section 27 (iv)). So in a steady circulation A → B → A, two
thirds of every returned amount joins A's standing set and one third goes
back out, and the flux S_A the far field carries is fed by one third of
the returns unless the re-release is six-fold and in phase (then all
radiates, 0 stands). The recoil momentum is unaffected (it is booked at
absorption, whole); the amount's fate depends on the re-release rule,
which is the owner's to fix (flagged in Highlights 5.4). **New**.

**Check.** Section 27 (iv)'s flat-band fractions (2/3 exact for a lone
share; the iteration 0.6648 at t = 40).

**Verdict.** The returning shadow's momentum comes home whole and the
third law is kept exactly, delayed by the L1 path: **reached**. The
returned amount's re-release: two thirds standing per lone re-release,
**new** and the owner's rule to fix.

## 33. Round 4: the verdicts

| Law | Round 3 (section 25) | Round 4: R10 (the Node mixes the six) | Run |
| --- | --- | --- | --- |
| Continuity, Gauss's law (flux) | reached | **reached exactly** (unitarity of S; Link current) | E11 under 16c |
| A conservation law for the signed flux J | — | **not reached** (the Node reverses a lone share's J to −1/3) | — |
| Maxwell's wave equation | not reached (amounts have no sign) | **reached exactly**: u(t+1) + u(t−1) = (1/3)Σ_nb u, cos ω = (1/3)Σcos kᵢ (TLM) | — |
| Wave speed | — | **1/√3 Link per interval** in the bulk; no signal faster in any direction | A5s Run 2 tick by tick |
| The push in a wave | J = 11/8 Φ (diffusive) | **new**: J = n·v_g = Φ exactly (ζ = 1); two opposite waves J = 0 with the amounts passing | — |
| The front of a release | 4/5 on tubes, 0 off the planes | **tube theorem overturned**: 89 % off the planes at t = 30; front at √3 r everywhere, sharp on (111) (6 ticks), smeared on the axes (14 to 20), a short pulse 30× weaker on an axis | E11's release read at (12,0,0), (7,7,7) |
| Retardation t₉₀ | r on tubes, ∞ off | **√3 r + 1 to 17** by direction (1 to 2 on (111), 10 to 17 on an axis) | A5s Run 2 |
| Far field of a thing at rest | six tubes | **1/r² at every angle** for a clocked thing, with a fixed anisotropy (15/8)ω²K₄ (1.25 ω² axis vs (111)); **no far field** for a clockless one (the constant source cancels itself) | E11 with a clocked source, at (24,0,0) and (14,14,14) |
| The standing set | — | **new**: four flat bands of six; 2/3 of a lone re-release stands, 0 of a symmetric release | a lone shadow re-released at a thing |
| Field speed against light | — | **different law**: the force lags light by (√3 − 1) r; every thing outruns its field; Mach cone 35.3°; no identification (unit, N, wait) closes the gap | E11 (a) with a moved pusher |
| Two-slit fringes of shadows | lost (R8v) | **reached** in the push: the optical spacing λ_w L/d, λ_w = K/(√3 M), depth 0.99 measured; none in counts (point 6); no self-interference of a thing | A1 |
| A mirror | ties, Port order (R8v) | **reached**: standing wave of period λ_w/2, zero net flow; **new**: the push oscillates at (k₀/3) n with zero mean, the amount at depth k₀²/6 (0.081 measured, 0.079 derived) | E11 with a wall |
| The integer rule | — | **reached** above ≈ 256 quanta per Node (N ≥ 64), dead below 64; no diffusive part (standing content and noise instead); N = 8 costs 7 % | A5s dense mode at two X |
| Coulomb's product law, Newton's, k_C = G | reached (R4′) | **reached** with ζ = 1, modified: anisotropy (15/8)(2πM/K)²K₄, retardation √3 r, a clock required on the source, 256 quanta per Node at the receiver | A5s, A7 |
| A length scale in the force | reached under R4″ | **not reached** (J is phase-blind and time-constant in a wave) | — |
| Newton's third law | lost (R8v) | **reached exactly**, delayed by \|x\|₁ ≤ √3 r (the return is exempt from mixing) | E11 (a) |
| Port-order independence | lost (R8v) | **reached** (S is a fixed linear map; the register order is the only tie, bounded) | — |

Open after this round, one line each: the
second-order (ω⁴) anisotropy and the first-order coefficient's excess
(measured ≈ 1.5 to 2 × 3/2 at ω₀ = 0.2); the re-release rule at the owner
(lone versus six-fold in phase decides whether the returns stand or
radiate); the time-averaged Gauss flux of J against Φ near a source
(the 2/r correction); a rounding-survival law in closed form (the measured
loss ∝ 1/n^{1.5 to 2} per interval).

## 34. Round 5: does the shadow pay the wait? The question, the reading rate under R10, and the three options as rules

Round 5 (2026-09-18, after PR #299) answers the model owner's question of
the same day: is the shadow (bit 0) affected by the wait of point 23, the
tick a thing pays per whole quantum it reads, and how, and what does each
answer give against the gravitational tests. As before: bottom-up from the
stated operator, no physics assumed, no engine run, no edit to the engine;
every number checked by an iteration of the operator on a box of 41³ to
81³ Nodes (seconds each), cited after the derivation and never used as its
source; the scripts are the scratch files of this round, not committed.

**The rules as they stand.** R10 (point 24, section 26) for the shadows;
R9 (point 23, section 24) for the wait: a thing that reads a whole quantum
of shadow does not step and does not advance its phase for w intervals, w
the model's constant (one the natural value), and a shadow pays nothing
(point 9: no mass, no clock, the causal speed). The return of a pushed
shadow is a field (point 3 as amended on 2026-09-18: the same shadow with
its heading reversed, mixing at every Node from then on, absorbed wherever
it reaches its owner), which supersedes the exemption section 32 derived
under ("the return walks the trace, unmixed"); everything below uses the
amended point 3. R4′ (the two readings), R6′ (one Link per interval), R7′
(the clock M/K), R3 in its standing reading (a clocked thing's set, flux
S = κξM, G = κξ/(2π), section 31).

**The three options, as local rules.** Each is stated as what a Node does
in one interval, since nothing else is a rule of this model.

- **I, the law as it stands (R9).** Only a real ray pays: w intervals per
  whole quantum of shadow it reads. A shadow never.
- **II, the shadow pays too.** Two readings, which differ, and both are
  derived; they are the two readings of the declared option `shadow_wait`
  of Highlights 5.4 ("The shadow's wait, a declared option to confront",
  model owner, 2026-09-18, PR #303, feature 16e): II-a is its `thing`,
  II-b its `field`. **II-a (R9a), at the thing:** the shadow a thing reads waits the
  same w intervals per quantum at the thing's Node before it turns back;
  the meeting is one computation and both parties pay. Local: the thing is
  at the Node, the shadow is parked there (point 22), the count is the
  thing's own. **II-b (R9b), in the field:** a share of owner A that
  arrives at a Node where whole quanta of another owner M are present waits
  w intervals per quantum of M present, then mixes with the arrivals of the
  interval in which it is released. Local per Node and interval, but it
  asks a shadow to count another owner's quanta, a reading, which point 16
  gives to things only ("how a thing reads a shadow is the coupling"), and
  it amends point 9 (a shadow moves at the causal speed) and point 21 (the
  only exception is a thing's). II-b is the reading under which "the field
  near a mass is slowed and piled up" (the model owner's phrase) means
  anything: under II-a the vacuum beside a mass has no index, since shadows
  wait only where a thing is.
- **III, the opposite.** Four rules could mean "sped up or thinned", and
  each is judged by the books. **III-1**: a share moves more than one Link
  per interval where M's quanta are present: impossible, not merely
  unlawful; R2 and the lane of point 25 hold one shadow per owner per lane
  per interval, and a ray is at one Node. **III-2 (R9c)**: at a Node where
  another owner's whole quantum is present the share passes straight,
  unmixed (B_p = A_{opp(p)} for those shares, the identity on the Ports in
  place of S): a switch between two orthogonal maps, so amount and
  amplitude are conserved exactly, nothing parked, nothing destroyed;
  lawful in the books, and it raises the field's speed from 1/√3 toward 1,
  never beyond (a share still crosses one Link per interval), so "sped up"
  is bounded by the causal speed. **III-3**: a share loses amount per
  quantum of M present ("thinned"): unlawful, point 7 (amount is never
  destroyed) and the unitarity of section 26 (ii). **III-4 (R9d)**: the
  thing gains rather than loses, its phase advancing by an extra content/K
  per quantum read (a tick bonus): lawful in the books of amount, momentum
  and charge, since the phase is not booked, but against point 11
  (computation is the things' content, nothing else) and point 19 (the
  clock is content/K); it touches only clocks, not motion, since a thing
  cannot move faster than one Link per interval. The lawful "opposite" is
  therefore III-2 for the shadow and III-4 for the thing; III-1 and III-3
  are not rules of this lattice.

**What every option reads: the reading rate under R10.** The wait, in
every option, counts quanta at a Node per interval. Under R10 the field of
a clocked thing of flux S is the spherical wave of section 27 (v), and the
arrivals per interval at a Node at distance r, which is what a thing there
reads (R4′: every shadow at its Node), are

```text
n(r) = √3 · J(r) = √3 S / (4π r²) [1 − (3/2) ω₀² K₄(r̂)],      J(r) = S / (4π r²) [1 − (15/8) ω₀² K₄(r̂)],
```

J = n v_g with v_g = 1/√3 (section 26 (iii)). With S = 2πGM (section 31:
S = κξM, G = κξ/(2π); the direct push per unit content of the receiver is
J = GM/(2r²), the other half of Newton's GM/r² being the returned recoil
of the receiver's own shadows),

```text
n(r) = (√3 / 2) · G M / r²    quanta per Node per interval:    the wait reads the field strength, not the potential.
```

This is the fact of the round. In rounds 1 to 3 the field was diffusive
and its amount fell as 1/r (section 5: n = 9S/(16πr); section 24:
n = (9/11)GM/r), which is why the wait gave the potential's form
1 − (9w/11)GM/r and w = 11/9 fixed GR's coefficient. Under R10 the amount
falls as 1/r², since the shadows pass at v_g and do not linger: n = J/v_g.
The potential 1/r is present in R10's field, as the amplitude of the
common part u ∝ e^{ik₀r}/r (section 27 (v)), and it is read by nothing: a
thing reads amounts, which are the squares. (As the Compton pattern of
section 18 and the phase of section 31: present in the amplitudes, read by
no push.) So every consequence of the wait below is a law in
g = GM/r², the acceleration, and none is a law in GM/r. In physical units
the reading rate is (√3/2) g ℓ/c² per interval, ℓ the Link, so the
wait's effects carry a factor ℓ/r against GR's.

**Assumptions and limit.** Mean field (the integer form is the register
rule on the thing's side, section 24; where it breaks is section 37).
Far field, k₀r ≫ 1, and w n ≪ 1. The self-reading excluded: a thing
meeting its own shadow is a round trip of length zero computed as zero
(point 3), so the home absorption is no reading; if it were, every thing
would pay w × (its standing amount at its Node) per interval, a constant
of the thing that cancels in every ratio below but stops every thing whose
own set exceeds 1/w at its Node. Light: a thing of the light family at
speed 1 (R6′), clockless (R7′); its own field is the Mach cone of section
28 and pushes M behind it, but the return is a field at group speed 1/√3
(section 26 (iii)) and a thing moving on an axis or a (110) line at
Euclidean speed 1 or 0.71 is never caught by it (only on a (111) line,
Euclidean 1/√3, does the sharp front keep pace); what would have been the
"late return" half of sections 19 and 24 stays in flight until the light
thing is absorbed at a mark, which then becomes the home of its shadows
(Highlights 5.4, "A thing does not emit"): the recoil goes to the screen.

**Check** (81³, a clocked source at period 16 and 32, the period mean
after 150 and 200 ticks, S the flux of J through the cube of half-width
16). The ratio n/J at r = 8 to 24: 1.72 to 1.76 on (110) and (111) at
period 16 (1.73 to 1.84 at period 32), 1.58 to 1.74 on the axis, rising
toward √3 = 1.732 with r (the axis's near-field term); 4πr²n/S = 1.67 to
1.78 on the diagonals, 1.45 to 1.55 on the axis at period 16 (the (15/8)ω₀²K₄
deficit of section 27 (v) with ω₀ = 0.39), against √3. The path sums of
the next section (Σ_x n along a line at impact parameter b = 8, 12, 16,
x ∈ [−28, 28]): 0.943, 0.943, 0.945 of (√3S/(4π))(2/b)atan(28/b) at
period 16 and 0.978, 0.966, 0.963 at period 32; Σ_x J_⊥: 0.978, 0.955,
0.947 and 1.017, 0.988, 0.976 of (S/(4π))(2/b)·28/√(b² + 28²).

**Verdict.** The reading rate under R10: n = √3 J = (√3/2)GM/r², **reached
exactly** in the mean field (n/J = 1.72 to 1.74 measured). A law of the
wait in the potential GM/r: **not reached** by any option, because the
amount of R10's field is 1/r² and its 1/r is an amplitude, which no rule
reads.

## 35. Round 5: the four gravitational tests under each option

**Rules used.** Section 34's rules and reading rate; the integrals of
section 8 (∫ b/(b² + x²)^{3/2} dx = 2/b) and two more, ∫ dx/(b² + x²) =
(1/b)[atan(x_A/b) + atan(x_B/b)] → π/b and ∫ ∂_b[1/(b² + x²)] dx → −π/b².
Everything is first order in w n and in GM/b; the second order (strict
against queued reading, and what a thing reads while it waits) is as in
section 24 and open.

**(i) The clock of a thing at rest at r.** The thing reads n(r) quanta per
interval and loses w intervals per quantum:

```text
I, II-a, II-b, III-2:   ρ_eff / ρ = 1 − w n(r) = 1 − (√3 w / 2) · G M / r²     (0 at the horizon r_h = √((√3/2) w G M) = 0.93 √(w G M));
III-4:                  ρ_eff / ρ = 1 + (√3 w / 2) · G M / r².
```

Against general relativity's 1 − GM/(rc²): there is no GM/r term to give
a coefficient against GR's 1; the law is in the acceleration, a clock
slows (III-4: quickens) by (√3 w/2) times the local g in Links per
interval², and by the anisotropy (3/2)ω₀²K₄ of n it slows more on a body
diagonal of the mass than on an axis at the same r. A loop's period,
P/P₀ = 1/(1 − wn), the same factor. The options do not differ here except
III-4, whose sign is the wrong one: near a mass a clock runs fast. II-a
and II-b change nothing in what the thing reads, since a shadow that waits
is read once, at its arrival, and the arrivals per interval in a steady
state equal the departures (continuity, section 26 (ii)). **Different
law** (I, II-a, II-b, III-2: 1/r² in place of 1/r; III-4: 1/r² and the
opposite sign).

**(ii) The gravitational redshift.** A clock at r₁ runs at ρ(1 − wn₁), at
r₂ at ρ(1 − wn₂); the light things between them carry no clock, and a
static field delays every emission alike (the Shapiro delay of (iv) is the
same for every thing of the stream), so

```text
z = ν₁/ν₂ − 1 ≈ (√3 w / 2) · G M · (1/r₁² − 1/r₂²)     (I, II-a, II-b, III-2;   III-4: the negative of it),
```

against GR's GM(1/r₁ − 1/r₂)/c². A photon climbing out of a well loses
frequency by the difference of the accelerations at the two ends times
one Link, not by the difference of the potentials. **Different law**.

**(iii) The bending.** Three things are bent, and each option bends them
differently.

*The image of light* (where a light thing lands): a thing turns only by a
push (points 10 and 21); over a pass at b it takes Δp_⊥ = p ∫ J_⊥ dx =
p (S/(4π))(2/b) = p GM/b, so

```text
α_image = G M / b     (every option; achromatic; a quarter of Einstein's 4GM/(c²b), half of Newton's corpuscle),
```

the direct push alone: the recoil half of Newton's force never reaches a
thing at speed 1 (section 34), and the wait turns nothing. The wait
changes the push at second order only (a slower pass reads (1 + wn) quanta
per Link).

*The front of light* (the phase pattern of successive light things from a
clocked emitter, read by an interferometer or a two-slit behind the mass):
each thing is late by w per quantum read, the phase it carries is its
emitter's and does not advance, so the surfaces of equal phase tilt by the
gradient of the delay,

```text
α_front(light) = α_image + w ∫ ∂_b n dx = G M / b + (√3 π w / 2) · G M / b²      (I, II-a, II-b, III-2;   III-4: α_image alone),
```

toward the mass (the near side waits more), 2.72 w GM/b². The added term
is 1/b², not 1/b: it is not Einstein's space half (2GM/b) at any w, it is
smaller than it by the factor 1.36 w/b, and the front and the image still
disagree.

*The front of the field* (a change in a thing A's field crossing M's field
at impact parameter b, read by the register of a thing B behind M): a
shadow of A is turned by no push (a shadow meeting a shadow is a sum of
phases, point 5; shadows of different owners cross, point 25), so under I,
II-a and III-4 its front is straight: α = 0. Under II-b the shadows of A
have the index 1 + w n_M(r) relative to 1/√3, since each Node crossing
costs w n_M intervals in the mean; under III-2 they have 1 − (1 − 1/√3) w
n_M, since a fraction w n_M of the crossings is ballistic (one interval
per Link in place of √3). The tilt of a front is the gradient of its
delay times its speed, so

```text
II-b:   α_front(field) = + (√3 π w / 2) · G M / b² = +2.72 w G M / b²   toward M;
III-2:  α_front(field) = − (1 − 1/√3)(√3 π w / 2) · G M / b² = −1.15 w G M / b²   away from M;
I, II-a, III-4:  0.
```

The field of a thing is focused behind a mass under II-b and defocused
under III-2; light is neither.

*Against Einstein's 4GM/(c²b)*, which needs the time half (2GM/b, Newton's
corpuscle) and the space half (2GM/b, the index): the image has one
quarter, the front of light one quarter plus a 1/b² term. **Not reached**
in every option; **different law** (image GM/b, front GM/b + 2.72 w
GM/b²; the field's front 0, +2.72 w GM/b² or −1.15 w GM/b² by option).

**(iv) The Shapiro delay.** *Light*: Δt = w ∫ n dx along the pass,

```text
Δt(light) = (√3 w / 2) · G M · (1/b) [atan(x_A/b) + atan(x_B/b)]  →  (√3 π w / 2) · G M / b = 2.72 w · G M / b     (I, II-a, II-b, III-2;   III-4: 0),
```

against GR's 2GM ln(4x_Ax_B/b²): a delay that saturates with the path
length and falls as 1/b, no logarithm, smaller than GR's by the factor
1.36 w/(b ln(4x_Ax_B/b²)), b in Links. A relation follows that no w can
change: the delay of a light thing over a pass and its deflection over the
same pass are the same integral up to the constant of the operator,

```text
Δt(light) / α_image = √3 · atan(X/b) / (X/√(b² + X²))  →  (√3 π / 2) w = 2.72 w   intervals per radian   (X the half-length of the pass),
```

so a light thing that is turned by α is late by 2.72 w α ticks, at every b
and every S: a one-tick delay needs a deflection of 0.37/w radians, and a
thing that is not captured (b > b_c = GM, section 19) is never late by more
than 2.72 w ticks over its whole pass. *The field*: its own time per Link
is √3 (section 28) and the extra is √3 w ∫ n_M dx under II-b, so

```text
II-b:   Δt(field) = + (3π / 2) w · G M / b = +4.71 w · G M / b;     III-2:  Δt(field) = − (1 − 1/√3) · 4.71 w · G M / b = −1.99 w · G M / b;     I, II-a, III-4:  0,
```

on top of the √3 r retardation of section 28 (which is unchanged in every
option and is not GR's). Under II-a the field is not delayed in the vacuum
but the return of every pushed shadow leaves the thing w intervals per
quantum later, so the recoil of section 32 arrives at the owner late by w
per quantum on top of |x|₁. **Different law** in every option (light's
delay ∝ 1/b, no logarithm; the field's delay 0, +4.71 or −1.99 w GM/b).

**Dictionary.** g = GM/r² ↔ the Newtonian acceleration in Links per
interval²; w n ↔ the fraction of intervals lost; 1 + w n_M ↔ a refractive
index of the vacuum for fields (II-b), 1 − 0.42 w n_M (III-2); the front
of the field ↔ the retardation of a force, read as the tick a register
first moves.

**Check.** *The index of II-b and III-2* (a plane wave of period 16 along
x in a thin periodic box, the exact one-dimensional reduction of R10, a
slab of 80 Nodes in which a static random fraction f of the Nodes applies
the modified rule, six masks, k_in fitted on the phase of the +x-moving
Port amplitude's time-harmonic component over the slab interior). II-b
with a first-in-first-out hold of w = 1 at the masked Nodes: k_in/k₀ =
2.102 at f = 1, exactly the lattice dispersion's arccos(3cos 2ω − 2)/k₀ =
2.102 (every Node delayed is the same operator with time doubled); at the
masked fractions 0.485, 0.217, 0.090, 0.042: 1.538 ± 0.067, 1.240 ± 0.039,
1.100 ± 0.042, 1.045 ± 0.038 against 1 + f = 1.485, 1.217, 1.090, 1.042
(1.512, 1.225, 1.092, 1.043 with the dispersion): **n_eff = 1 + w n_M to
first order**, with a transmitted amplitude 0.74 to 0.94 (the masks
scatter). III-2 with the straight pass at the masked Nodes: k_in/k₀ =
0.570 at f = 1 (ballistic: k_in = ω, ω/k₀ = 0.5696), and 0.816 ± 0.024,
0.921 ± 0.016, 0.969 ± 0.012, 0.988 ± 0.010 at the four fractions against
1 − f(1 − 1/√3) = 0.795, 0.908, 0.962, 0.982: **n_eff = 1 − 0.42 w n_M**
to first order, with a transmitted amplitude 0.39 at f = 0.485 (a
straight-passing Node in a wave scatters strongly) and 0.84 to 0.96 below.
*The path integrals of light* (section 34's check): Σ_x n / Σ_x J_⊥ along
the line at b = 8, 12, 16 with X = 28: 2.245, 2.170, 2.093 at period 16
and 2.239, 2.149, 2.070 at period 32, against √3 atan(X/b)/(X/√(b² + X²))
= 2.328, 2.197, 2.098 (the asymptote 2.721); the tilt d(Σ_x n)/db: 0.970,
0.948, 0.949 of the formula at period 16 and 1.051, 0.980, 1.016 at period
32.

**Verdict.** The clock: **different law** in every option, 1 − (√3w/2)GM/r²
(III-4 with the opposite sign); no coefficient of GM/r exists to set
against GR's 1. The redshift: **different law**, in the accelerations.
The bending: the image GM/b in every option (**different law**, a quarter
of Einstein's); the front of light GM/b + 2.72 w GM/b² (**not reached**:
the added term is 1/b²); the field's front 0 (I, II-a, III-4), focused
(II-b) or defocused (III-2) by a 1/b² term. Shapiro: **different law** in
every option, 2.72 w GM/b for light with no logarithm and the fixed ratio
2.72 w ticks per radian of deflection; the field late by 4.71 w GM/b under
II-b and early by 1.99 w GM/b under III-2. **New**: Δt = 2.72 w α for every
pass, and the focusing of fields, not of light, behind a mass under II-b.

## 36. Round 5: Coulomb near a mass, the far field of a thing near a mass, and the books

**Rules used.** Section 34's rules and reading rate, section 31 (Coulomb
and Newton under R10, ζ = 1), section 26 (ii) (continuity), section 28
(the retardation √3 r), point 7 (the books per bit), point 3 as amended.

**(v) Coulomb's law between two things at rest near a mass.** A and B at
separation s, both at distance r from a mass M (r ≫ s). Under R10 the push
B takes from A is J_A(B) = S_A/(4π s²), the flux of A's wave through the
sphere of radius s, and with the returned recoil the force is
k_C q_A q_B/s² (section 31). Near M three things could change it, and the
options differ only in the third.

- *The potential*: nothing. R10's amounts carry no potential (section
  34), and the flux S_A is what A's set declares (X/(√3 R)), which no wait
  changes; the pile-up of II-b raises the amount resident at B's Node to
  n_A(1 + w n_M) but a held share is read once, at its arrival, and in a
  steady state the arrivals per interval equal the departures
  (continuity), so J_A(B) is unchanged. The force between two things at
  rest is the same at every r from the mass, in lattice time, in every
  option. **Reached** (the product law, its constant and its independence
  of the place).
- *The clocks*: each thing's rate is ρ(1 − w n_M(r)) (section 35 (i)), so
  the same force per lattice interval is, per tick of the local clock,
  F/(1 − w n_M) = F [1 + (√3 w/2) GM/r²]. Physics says the local force is
  unchanged in the freely falling frame and the coordinate force carries
  the metric's √g₀₀ ≈ 1 − GM/r; here the coordinate force is unchanged and
  the proper force is larger, by the clock's factor, which is a law in
  g ℓ/c² and not in the potential. A second-order companion: A's wave has
  the frequency of A's slowed clock, ω_A(1 − w n_M), so the fixed
  anisotropy (15/8)ω_A²K₄ of section 31 shrinks by (1 − w n_M)². Under
  III-4 the signs reverse. **Different law** in the local observer's
  measure, by 1/(1 − (√3w/2)GM/r²) (all options but III-4, which gives the
  inverse).
- *The path* (II-b and III-2 only): A's shadows crossing M's field to B
  are late by √3 w ∫ n_M dx (II-b) or early by 0.42 of it (III-2), so a
  change of A's field reaches B later or sooner than section 28's √3 s,
  and the force lags or leads accordingly; the steady force is untouched.
  With whole quanta arriving at random the index would also scatter (the
  transmitted amplitude of section 35's check, 0.74 to 0.96 over a slab of
  80 Nodes at masked fractions 0.04 to 0.49), a screening of one thing's
  field by another's presence; with the registers' regular arrivals the
  medium is uniform in the mean and scatters only at index gradients, at
  second order. Whether M's own shadows count as "present" for M's own
  shares (II-b, III-2 applied per owner or to others only) changes the
  wavelength of M's near field by 1 + w n_M and nothing of (i) to (vi).

**(vi) The far field of a thing near a mass.** B's flux S_B is declared
and conserved through every shell (section 26 (ii)), so J = S_B/(4πr²)
holds in every option: **1/r² kept**. Modified in three ways. The
wavelength: B's clock is slowed, so λ_w = K/(√3 M_B (1 − w n_M)), longer
by 1 + w n_M near the mass, and its fixed anisotropy (15/8)ω_B²K₄ smaller
by (1 − w n_M)² (III-4: the reverse). The lens (II-b, III-2): B's wave
passing M is refracted by 1 + w n_M(r) (or 1 − 0.42 w n_M), the flux per
solid angle behind M raised (II-b) or lowered (III-2) at O(w GM/b²)
(section 35 (iii)) while the flux through a closed surface is exact.
The pile-up (II-b): the amount resident near M is n(1 + w n_M), which no
thing reads and only a count of parked shadows would show. Under I, II-a
and III-4 the far field of B is the far field of B with a slower clock,
nothing else.

**(vii) Conservation.** Point 7 asks that things conserve amount,
momentum and charge exactly among themselves at every interval, with the
momentum in flight in the returning shadows, and that every push comes
home through the field (the third law, global, section 32 as amended by
point 3). Option by option:

- **I**: the wait is a counter on the thing, its own time; nothing is
  parked, nothing is created; the return is a field at 1/√3 and the recoil
  reaches a thing at rest after √3 r + 1 to 17 (section 27 (iii)); a
  thing at speed 1 is not reached and its recoil is delivered to the mark
  that absorbs it (section 34). **Exact**, with momentum in flight for as
  long as the light flies.
- **II-a**: the pushed shadow is parked at the thing's Node with its
  amount and its −Δp for w intervals per quantum, a parked shadow of point
  22 with a countdown (a counter per parked share, or the thing's own
  counter, since the thing is there); the books close per interval with the
  parked momentum counted as in flight; the third law's delay is
  √3 r + w per quantum. **Exact**, one counter on the shadow.
- **II-b**: a first-in-first-out of held shares per Node, owner and Port,
  a delay line the Node holds beyond its six Ports (point 22 admits parked
  shadows; this adds their order and their countdown); unitary at every
  Node (each share leaves after w with its amplitude; at f = 1 it is the
  same operator with time stretched, the check of section 35), Kirchhoff's
  sum conserved, amount exact, the momentum in flight held longer near
  every mass (the third law late by 4.71 w GM/b over a pass at b). **Exact**
  in the books; new Node state; a reading by a shadow, which points 9, 16
  and 21 do not have.
- **III-2**: a switch between S and the Port identity in an interval,
  both orthogonal, both conserving Kirchhoff's sum; no state; the wave
  equation of section 26 (ii) fails at the switched Nodes (each is a
  scatterer, section 35's check), the returns pass straight near masses
  and arrive early. **Exact** in the books; a declared switch, which
  point 24's "nothing here is declared" does not have.
- **III-4**: amount, momentum and charge exact (the phase is not booked);
  the world's computation per interval exceeds the things' content by the
  bonus steps, against point 11, and the clock is no longer content/K,
  against point 19. **Exact** in the books, unlawful in the clock.
- **III-1, III-3**: not rules (III-1) or amount destroyed (III-3, against
  point 7 and unitarity).

**Check.** Section 35's slab check (unitarity at f = 1: transmitted
amplitude 0.993 for II-b, 1.000 for III-2; the scattering at random
masks); section 26's identities for the switched maps (Π is orthogonal
and 1ᵀΠ = 1ᵀ, so ΣB = ΣA under both S and Π); section 31's algebra.

**Verdict.** Coulomb near a mass: **reached** in lattice time in every
option (no potential in the amounts to change it); **different law** in
local time by the clock's 1/r² factor. The far field of a thing near a
mass: **1/r² kept** in every option, the wavelength longer by 1 + w n_M,
and under II-b and III-2 a lens of order w GM/b². The books: **exact** in
I, II-a, II-b, III-2 and III-4; II-a and II-b need a counter on a shadow,
II-b a reading by a shadow, III-2 a declared switch, III-4 breaks the
clock's law; III-3 is unlawful and III-1 is not a rule.

## 37. Round 5: one w for the four tests, the standing profile, and what A6 repeated can read

**Rules used.** Sections 34 to 36; section 27 (iv) (the flat bands);
section 30 (the integer rule); section 19 (the capture radius b_c = GM);
the A6 entry of [EXPERIMENTS.md](EXPERIMENTS.md#a6-light-bending-by-a-bound-group-and-g_eff-n²-over-n--28-to-216).

**(viii) Which option reaches GR's coefficients for (i) to (iv) with one
w.** None, and with no w: there is no term in GM/r to carry a coefficient.
Under R10 every effect of the wait is (√3 w/2) GM/r² or its integral, a
law in the acceleration, in every option (section 35); the options differ
only in what happens to fields, which GR's four tests do not read. The
reason is the reading rate (section 34): the amount of the wave field is
√3 J ∝ 1/r². Two ways to a 1/r amount exist on paper, and neither is
lawful under R10.

*The diffusive field* of rounds 1 to 3 had n ∝ 1/r because its shadows
lingered (the residence time r²/D), and there one w fixed the clock, the
redshift and the front's space half (w = 11/9) with Shapiro at half
(section 24). R10 replaced it (point 24), and its shadows pass.

*A standing profile.* R10 has content that does not move: the four flat
bands of section 27 (iv). Derived here: the −1 band is the set of scalar
Link fields with zero sum at every Node (A_p(x) = A_{−p}(x + e_p), Σ_p
A_p(x) = 0: 3N − N = 2N dimensions, two bands), the +1 band the set of
divergence-free directed Link currents (A_p(x) = −A_{−p}(x + e_p), zero
Node sum: two bands); on either, every Node sends every arrival back
(B_p = −A_p) and the amounts never change. A profile with the amount
f(x) per Link on the −1 band (the checkerboard (−1)^{|x|₁} σ_i √f on the
Link (x, x + e_i)) has, exactly on the lattice differences,

```text
n(x) = Σ_p f(x + e_p/2) ≈ 6 f(x),       J(x) = −Σ_i [f(x + e_i/2) − f(x − e_i/2)] e_i ≈ −∇f:
```

with f = γM/r a thing at r would read 6γM/r quanta per interval and be
pushed by γM/r² outward in J, that is toward M with σ = −1: the potential
in the wait and the inverse square in the push from one profile, the
clock 1 − 6wγM/r = 1 − 3w GM/r with G = 2γ (the recoil half counted; 6w
GM/r without it), GR's coefficient at w = 1/3 (1/6), the front of light
turned by 6wGM/b (2GM/b at w = 1/3, Einstein's space half), Shapiro
3wGM ln(4x_Ax_B/b²) (GM ln at w = 1/3, half of GR's): section 24's
structure with 1/3 in place of 11/9. Three things stop it. (1) No source
makes it: a clocked thing's re-release is a wave (section 27 (v)), a
clockless thing's cancels itself; the profile would be a declared prefill,
an input like G itself. (2) It does not stand: a smooth envelope breaks
the zero sum at every Node by (1/3)σ·∇√f, and with f = γM/r two thirds of
the profile radiates away within 20 intervals and one third stays (the
check). (3) Decisive: a thing at rest empties it. The thing's Node
returns every arrival with its amplitude (B_p = +A_p, point 3: the same
shadow, heading reversed, its phase a shadow's phase) where the band
needs −A_p; the sign defect empties the six Links at the thing's Node in
two intervals, after which the thing reads a tenth and then a hundredth
of 6f and a push that alternates in sign about zero: a standing profile
pushes and slows a thing at rest for two ticks and never again (the
check). And had the return carried the sign −1 instead, the thing's Node
would be one more Node of the band, the thing read 6f and took J for ever,
and nothing would ever leave toward the owner: a push with no reply,
against point 7's closed round trip. A standing profile is therefore not a
field of a thing under the law of the bit, on either sign, and the
potential stays unread. **Not reached** by any option and any w: no
local rule on amounts reads the potential under R10.

**(ix) What A6 repeated can read.** The sizes, under R10 with the star a
clocked thing of flux S (a declared set X of extent R, S = X/(√3R),
GM = S/(2π)):

```text
b_c = G M = S/(2π)   (capture, section 19),      r_h = 0.93 √(w G M) = 0.37 √(w S)   (the horizon, wn = 1),
```

so r_h < b_c whenever GM > 0.87 w: for every mass that bends light by a
measurable angle the horizon sits inside the capture radius and no ray
that passes ever sees it. A6's board (65 × 65 × 9, b = 4 to 16) is
outside both for S < 25 (GM < 4 = the smallest b). At S = 10 (GM = 1.59):
b_c = 1.6, r_h = 1.2 (w = 1) and 1.3 (w = 11/9); the image α = GM/b =
0.199 rad at b = 8 and 0.099 at 16 (a register turn of 5·10⁴ quanta at
A6's p = 2¹⁸); the delay 2.72 w α = 0.54 w ticks at b = 8 and 1.1 w at
b = 4, that is 0 or 1 tick per pass under the integer rule, with the 1/b
law readable only as the fraction of passes delayed over many passes; the
front of light tilted by 2.72 w GM/b² = 0.068 w rad at b = 8 (a two-slit
behind the mass); a ring at r = 8 slowed by (√3w/2)GM/r² = 2.2 % w. At
S = 25 (GM = 4): b_c = 4, r_h = 1.9 and 2.0, α(8) = 0.5 rad, the delay
1.4 w ticks at b = 8, the ring at r = 8 slowed by 5.4 % w (86 w ticks
over 100 periods of 16: w to 1 %). **The ring is the instrument for w**;
the pass reads at most 2.72 w ticks at any S, since a delay beyond that
needs b < b_c.

*The integer rule against the wait.* Section 30: the field is a wave in
whole quanta only where n ≥ 64 to 256 per Node, r ≤ 0.023 √S. Point 23:
a thing that reads n ≥ 1/w quanta per interval never steps. Hence
r_h = 0.37 √(wS) = 16 √w · r_wave: **wherever the integer field is a wave,
every thing in it is frozen, for every w ≥ 1/256**, and where things
move (n < 1) the integer field is the dead residue of section 30 (standing
content and noise, J ≈ 0). At S = 25, n(8) = 0.054 quanta per Node: no
wave in whole quanta. The wait as declared can therefore be read only in
the dense layer (point 13's second layer, the field as a formula or one
mean-field step), where the thing accumulates the fractional amount it
reads and waits w per whole quantum accumulated, the register rule on the
thing's side; the integer layer with the wait at w = 1 has no moving thing
inside any wave.

*The one run that separates the options.* A source thing A and a
receiver thing B on a body-diagonal line (the field's front is sharp
there, section 27 (iii): t₉₀ = √3 r + 1 to 2), the mass M beside the
line at impact parameter b = 8, S = 40 (GM = 6.4: b_c = 6.4 < 8,
r_h = 2.4), a ring at r = 8 from M, in the dense layer; A displaced by
one Link at t₀. Read: (a) the tick B's register first moves, against the
same board without M: I, II-a, III-4: unchanged (√3 r_AB + 1 to 2);
II-b: later by 4.71 w GM/b = 3.8 w ticks; III-2: earlier by 1.6 w ticks;
(b) the tick A's register takes the recoil of B's push: II-a: later than
(a)'s mirror by w per quantum read at B; (c) the ring's period: 1 +
(√3w/2)GM/r² = 1 + 0.087 w in I, II-a, II-b and III-2, 1 − 0.087 w in
III-4; (d) a light thing along the same line: late by 2.72 w GM/b = 2.2 w
ticks and turned by 0.8 rad in every option but III-4 (not late). (a)
separates I and II-a from II-b from III-2; (b) separates II-a from I; (c)
separates III-4; (d) confirms the wait of the thing and reads w coarsely.
Nothing in A6's own geometry (a light ray at b, the register after the
pass) separates the three: the image is GM/b in every option.

**Check.** *The standing profile* (61³, the −1-band checkerboard with the
amount f = 1/max(r, 2) per Link, tapered smoothly to zero between r = 12
and 18 so that no sponge touches it). At t = 0: n = 1.0000, 0.6000, 0.4286
at r = 6, 10, 14 against 6/r; J_r = +0.02797, +0.01003, +0.00511 against
the lattice differences 1/5.5 − 1/6.5 = 0.02797, 0.01003, 0.00511 (exact).
The amount within r ≤ 10 relative to t = 0: 0.998, 0.993, 0.964, 0.834,
0.404, 0.362, 0.366, 0.332, 0.319 at t = 1, 2, 5, 10, 20, 40, 80, 160,
400; within r ≤ 6: 0.994, 0.981, 0.904, 0.706, 0.413, 0.443, 0.380,
0.353, 0.343; on the board 0.513 at t = 400 (the rest left through the
sponge): a third stands, two thirds radiate by t = 20. J_r at r = 6 while
it radiates: +0.048, +0.070, +0.139, +0.111, +0.124 at t = 1, 2, 5, 10, 20
(the leaving waves carry J = n v_g, forty times the profile's own), then
±0.01 to 0.02. *A thing at rest* at (10, 0, 0) in the untapered profile,
its Node returning every arrival (B_p = +A_p): the arrivals it reads
0.6000, 0.6000, 0.0680, 0.0692, 0.0243, 0.0370, 0.0138, 0.0204, 0.0033,
0.0176, 0.0033 at t = 0, 1, 2, 3, 4, 6, 8, 12, 20, 40, 80 (6f = 0.6); the
push J_x it reads +0.0100, +0.0169, −0.0048, −0.0070, −0.0048, +0.0113,
−0.0022, +0.0052, −0.0013, +0.0005, −0.0006 (the profile's +0.0100); the
amount within 3 Links of it 73.8 through t = 12 (the content is there and
does not arrive), 54.5 at t = 20, 15.4 at t = 80. *The sizes*: algebra on
section 34's n(r), section 19's b_c and section 30's radius.

**Verdict.** One w for (i) to (iv): **not reached** in any option; under
R10 no local rule on amounts reads the potential, the standing profile
that would is unsourced, leaks by two thirds and is emptied by a thing at
rest in two ticks. What A6 repeated reads: the image GM/b in every option
(**different law**, unchanged by the wait), a delay of at most 2.72 w
ticks per pass, the ring's period for w; the one run that separates the
options is the arrival tick of a field's front through the mass's field
on a body diagonal. **New**: the horizon hides inside the capture radius
(r_h < b_c for GM > 0.87 w); the integer wave field and a moving thing
cannot coexist at w ≥ 1/256 (r_h = 16 √w r_wave).

## 38. Round 5: the verdicts

| Law | Round 3 / 4 (sections 25, 33) | Round 5: I (R9 as it stands) | II-a (the shadow waits at the thing) | II-b (the shadow waits in the field) | III-2 (the straight pass) / III-4 (the tick bonus) | Run |
| --- | --- | --- | --- | --- | --- | --- |
| The reading rate at a thing | n = (9/11)GM/r (diffusive) | **n = √3 J = (√3/2)GM/r²** (measured 1.72 to 1.76) | the same | the same (a held share is read once) | the same | a thing's wait count beside a body |
| Gravitational time dilation | 1 − (9w/11)GM/r, GR at w = 11/9 | **different law**: 1 − (√3w/2)GM/r² | the same | the same | III-2 the same; III-4 **1 + (√3w/2)GM/r²** (the wrong sign) | a ring at r = 8, 16 from a body, dense layer |
| Gravitational redshift | (9w/11)GM(1/r₁ − 1/r₂) | **different law**: (√3w/2)GM(1/r₁² − 1/r₂²) | the same | the same | III-4 negative | two rings |
| Light bending, the image | 1 to 2 GM/b | **GM/b** (a quarter of Einstein; the return never catches a thing at speed 1) | GM/b | GM/b | GM/b | A6 with the wait: the register after the pass |
| Light bending, the front | 3 to 4 GM/b at w = 11/9 | **not reached**: GM/b + 2.72 w GM/b² (1/b²) | the same | the same | III-2 the same; III-4 GM/b | a two-slit behind the mass |
| The field's front through a mass's field | — | 0 | 0 | **+2.72 w GM/b²** toward M (focused) | III-2 **−1.15 w GM/b²** (defocused); III-4 0 | B's register behind M |
| Shapiro delay of light | (9w/11)GM ln(4x_Ax_B/b²), half of GR at w = 11/9 | **different law**: 2.72 w GM/b, no logarithm; Δt = 2.72 w α for every pass | the same | the same | III-2 the same; III-4 0 | A6 arrival tick |
| Shapiro delay of the field | — | 0 (beyond √3 r) | 0; the recoil late by w per quantum at the thing | **+4.71 w GM/b** | III-2 **−1.99 w GM/b**; III-4 0 | the one run of section 37 |
| The index of the vacuum for fields | — | 1 | 1 | **1 + w n_M** (measured 1 + f w, exact at f = 1) | III-2 **1 − 0.42 w n_M** (measured); III-4 1 | — |
| Coulomb near a mass | reached (ζ = 1) | **reached** in lattice time; ×1/(1 − wn_M) in local time | the same | the same; the force lags by the field's delay | III-2 the same, leads; III-4 the inverse clock factor | A5s beside a body |
| Far field of a thing near a mass | 1/r², fixed anisotropy | **1/r² kept**; λ_w longer by 1 + wn_M | the same | the same, a converging lens, a pile-up no thing reads | III-2 a diverging lens; III-4 λ_w shorter | E11 beside a body |
| The books (point 7) | exact | **exact**; the counter on the thing | **exact**; a counter on the parked shadow | **exact**; a delay line per Node, a reading by a shadow (points 9, 16, 21 amended) | III-2 **exact**, a declared switch; III-4 exact in the books, against points 11 and 19; III-1 not a rule, III-3 unlawful | E11 (a) |
| Newton's third law | exact, delayed \|x\|₁ | **exact**, through the field at 1/√3; light's recoil goes to the mark | exact, + w per quantum | exact, + 4.71 w GM/b near masses | III-2 exact, early | E11 (a) with a moved pusher |
| One w for the four tests | w = 11/9 (clock, redshift, front), Shapiro at half | **not reached**: no GM/r term in any option | — | — | — | — |
| A standing 1/r profile | — | **not a field of a thing**: unsourced, leaks 2/3 in 20 ticks, emptied by a thing at rest in 2 ticks (or pushes with no reply) | — | — | — | — |
| The horizon | r_h = (9w/11)GM | **r_h = 0.93 √(wGM) < b_c = GM** for GM > 0.87 w | the same | the same | the same | — |
| The integer wave and the wait | — | **incompatible** at w ≥ 1/256: r_h = 16 √w r_wave; the wait is read in the dense layer only | the same | the same | the same | A6 in the dense layer |

Open after this round, one line each: the second order of the wait
(strict against queued reading; what a thing reads while it waits); the
time-random form of II-b (a held share merged with the next interval's
arrivals is not a unitary map on amplitudes, only the first-in-first-out
form is) and whether the registers' regular arrivals make the two agree;
the scattering of a field by whole quanta arriving at random against the
registers' regularity (the 0.74 to 0.96 transmission of the random-mask
slabs); the fraction of a smooth-envelope flat-band profile that stands
(a third measured for 1/r, its closed form not derived); the recoil of
light delivered at the mark, and what E9's screen reads of it; a rule
that would read the amplitude u ∝ 1/r rather than the amount, which
nothing in the law of the bit provides.

## 39. Round 6: the wait reads the amplitude; what a thing at rest reads at distance r

Round 6 (2026-09-18, after PR #304) derives the model owner's direction of
the same day (Highlights 5.4, "The wait reads the amplitude, a coupling to
derive"): the coupling names which face of the field each reading takes, the
push the amount (the count of quanta, 1/r²), the wait the size of the
coherent sum the Node already forms for the mixing (the amplitude, 1/r), each
multiplied by the content as point 16 says. As before: bottom-up from the
stated operator, no physics assumed, no engine run, no edit to the engine;
every number checked by an iteration of the operator on a box of 41³ to 81³
Nodes (seconds each), cited after the derivation and never used as its
source; the scripts are the scratch files of this round, not committed.

**The rule, R11 (the amplitude reading).** At the Node of a thing, for each
owner j whose shadows arrive in an interval, the Node's common part is
u_j = (1/3) Σ_p A_{j,p}, A_{j,p} = √(amount_{j,p}) e^{iφ_{j,p}} (section 26;
in the engine the integer square root of amount × 32² in 32nds,
`node-mixing-v1`, and the sum (Σx, Σy) at the phase tables' scale, formed
before the six B_h). The thing reads Σ_j |u_j|, multiplied by its content,
and owes w intervals per whole unit of what it reads; the push stays R4′
(the amount times heading, times the content). The unit: the reading
M_thing · Σ|u_j| is compared with the thing's content, as the step of point
21 compares the push M_thing × (amount) with the content, so that a thing of
any content steps per whole quantum of net flux read; hence the wait's whole
unit is M_thing × 1 quantum^{1/2}, the count per interval is Σ|u_j| in
quanta^{1/2}, and the content cancels: every thing at a Node waits alike
(the equivalence of clocks). Were the unit one quantum^{1/2} of M_thing|u|
itself, a thing of content M would wait M times more than one of content 1:
a clock's slowing proportional to its own mass, which no clock test allows;
stated, not adopted below. The engine of the same day (wait-reads-v1,
feature 16f, PR #308, merged while this round was written; a declared option
`wait_reads: amplitude`, `amount` the default) reads, once per group at the
thing's Node, ⌊|Σ_p A_p|/32⌋, the whole units of the size of the sum, 3|u|,
in quanta^{1/2} (`arrival_amplitude`), multiplies it by the thing's content
through the push's reading (`push_of`, sign × amount × content) and counts w
per quantum of that product (`pushed_ray`); so its w is this document's w/3,
and its unit is the quantum of push, the non-cancelling one, for the
amplitude and the count alike (clock-readings-v1 counts the push's quanta,
content × amount, where rounds 3 and 5 wrote 1 − wn per unit content). Which
unit the wait has is the model owner's; the run that reads it is two rings of
different content at one r from a body (the same slowing here, 32 : 1 for
contents 32 and 1 in the engine as it stands). Rules used besides: R10, R2, R3 (standing
reading), R4′, R6′, R7′, point 3 as amended, sections 26, 27, 34.

**Assumptions and limit.** Mean field first (the integer form is (iv)); far
field k₀r ≫ 1; w|u| ≪ 1; the self-reading excluded as in section 34 (a
round trip of length zero is computed as zero), and, new here, standing
content reads zero anyway ((ii) below).

**(i) The amplitude of a clocked source's far field.** By section 26 (iii),
n = 3|u|² for a wave, and by section 27 (v) the far field of a clocked
thing of flux S has n = √3 S/(4πr²)[1 − (3/2)ω₀²K₄(r̂)]. So

```text
|u|(r, r̂) = √(S / (4√3 π)) / r · [1 − (3/4) ω₀² K₄(r̂) + O(ω₀⁴)] = 0.2143 √S / r,
|u|(r)    = √(G M / (2√3)) / r = 0.5373 √(G M) / r       (S = 2π G M, section 34),
```

constant in time for a monochromatic source (|u|² = n/3 while the six
amplitudes oscillate), with half the count's anisotropy, weaker on the axes.
Two facts of the round. **The amplitude is 1/r, the potential's form.** And
**the amplitude is the square root of the flux**: √S, √(GM), not GM. For
one owner of content M the reading grows as √M. For a body of N owners of
content m each, the mixing and the common part are per owner (shadows of
different owners cross, section 26), the thing reads each owner's message
(point 16), and the sizes add:

```text
Σ_j |u_j| = N · 0.5373 √(G m) / r = (0.5373 / √(G m)) · G M / r,      M = N m,
```

linear in the total content when every owner has the same content m, and
otherwise √(κξ) Σ_j √(m_j), which is not a function of Σ_j m_j: 96 quanta
read 9.8 √(G/(2√3))/r as one owner, 13.7 as a 64 and a 32, 17.0 as three of
32, 96 as ninety-six of 1 (the same push in every case). The gravitational
mass a clock reads is Σ_j √m_j, the mass a push reads Σ_j m_j.

**(ii) The prefilled standing set.** Two parts. A clocked thing's finite set
of total X and extent R is the same wave cut at R: |u| as in (i) with
S = X/(√3R) for √3R intervals, then gone unless returned (section 27 (v)).
The flat-band content (the 2/3 of a lone re-release, the −1 and +1 bands of
section 27 (iv)) has u ≡ 0 at every Node, exactly: the −1 band is the scalar
Link fields with zero Node sum, the +1 band the divergence-free directed
currents with zero Node sum (section 37), so Σ_p A_p = 0 on both. **The
standing set is invisible to the amplitude reading, while the count reads
it in full**, and 3 Σ_x |u|² is exactly the amount in the two wave bands, a
conserved quantity (a lone share: 1/3 at every tick). A thing's own standing
content at its Node therefore costs it nothing under R11 without the
exclusion section 34 needed, and a clockless thing's constant release,
which cancels itself (section 27 (v)), has no far amplitude as it has no
far amount: light's content has no potential in this reading, as it has no
far push.

**(iii) A thing's Node.** By point 3 the thing's Node returns every share of
another owner through the Port it came in (B_p = A_p). The Port sum is
conserved by that rule as by the mixing, so u at the thing's Node obeys the
same equation u(t+1) + u(t−1) = (1/3)Σ_nb u as every other Node: the
amplitude a thing reads is the free field's (measured to four digits). The
count at the thing's Node is not: in a monochromatic field the arrivals at
a returning Node are, exactly, A_p(x) = u(x + e_p)/(2 cos ω) (from
A_p(x, t+1) = u(x+e_p, t) − A_{−p}(x+e_p, t) with A_{−p}(x+e_p, t) =
B_p(x, t−1) = A_p(x, t−1)), so n_thing = Σ_p |u(x+e_p)|²/(4cos²ω) → (3/2)|u|²
= n_free/2 at long wavelength (0.65 to 0.67 of the free n measured at
period 16, the neighbours' |u| raised by 2 to 16 %). A correction to round
5: the count a thing at rest reads is half to two thirds of section 34's n,
which scales round 5's coefficients by that factor and changes none of its
laws.

**(iv) The integer rule.** The engine's amplitude per Port is
isqrt(amount × 32²)/32, exact at perfect squares and below √(amount) by less
than 1/32 otherwise (1.406 for 2, 1.719 for 3, 3.156 for 10), so u is formed
to within 1/16 quantum^{1/2} at worst; the coherent sum 3u = (Σx, Σy) sits
at the scale 32 × 256 of the phase tables, and its size is one integer root
more, |3u| in units of 1/8192: the whole unit of the reading is 3 × 8192 =
24 576 in that scale. The smallest amplitude a Node forms is one quantum on
one Port, |u| = 1/3 quantum^{1/2} exactly (32/96). Three exact bounds on
what the Node forms in one interval from whole quanta a_p:

```text
|u| ≤ (1/3) Σ_p √a_p ≤ √(2n/3)     always (Cauchy–Schwarz);      |u| = √(n/3)  for the plane wave;
|u| ≤ n/3                          where every Port carries 0 or 1 quantum (√a = a).
```

Hence in the sparse field, n < 1 quantum per interval at the Node, the
interval-by-interval amplitude is at most a third of the count and its time
mean at most n/3 ∝ 1/r² (with the registers' regular arrivals, one quantum
every 1/n intervals on the forward Port, exactly n/3): **the potential's
1/r is formed by the Node only where the six Ports carry many whole quanta
at once**, the wave's regime of section 30 (n ≥ 64 to 256 per Node,
r ≤ 0.023 √S to 0.046 √S), where |u| = √(n/3) ≥ 4.6 to 9.2 and w|u| ≥ 1 for
every w ≥ 0.22. A thing moves under R11 where w √(n/3) < 1, n < 3/w²; the
window in which the whole-quanta field is a wave and the thing moves,
r_h < r < r_wave, exists only for w < 0.11 (256 quanta) or w < 0.22 (64
quanta): at w = 1 none, as in section 37; at the engine's rational
w = 1/32 a wave of 256 to 3000 quanta per Node slows a thing by 29 to 100 %
and reads 1/r. Elsewhere the 1/r law is read in the formula layer (point
13's second layer as a formula, section 37), where the thing accumulates
w|u| with the mean-field amplitude and waits per whole unit.

**Dictionary.** |u| ↔ the potential, in quanta^{1/2}; √S ↔ the charge of the
potential is the root of the flux; Σ_j √m_j ↔ the mass a clock reads; the
flat bands ↔ bound (standing) field, potential-free; 1/(2cos ω) ↔ a point
mirror's arrivals.

**Check.** *The far field* (81³ with a sponge, a clocked source at period 16
and 32, the period mean after 150 and 200 ticks, S the flux of J through the
cube of half-width 16): 3|u|²/n = 0.96 to 1.03 at r = 8 to 24 on (110) and
(111), 0.92 to 1.05 on the axis; |u| r/(0.2143 √S) = 0.96 to 1.02 on the
diagonals and 0.90 to 0.95 on the axis at period 16 (the first order gives
0.954, 1.012, 1.031 on axis, (110), (111)), 0.96 to 1.03 everywhere at
period 32; |u| over a period varies by 5 to 12 % of its mean at r ≤ 12 (the
box's reflections), more near the sponge. *The flat bands* (the one-step map
U(k) at three random k): the eigenvectors of eigenvalue +1 and −1 have
|Σ_p v_p|/|v| < 10⁻¹⁵, those of e^{±iω} have √3 = 1.732 (the identity
|Σ_p A_p|² = 3n of a wave); a lone share of amount 1 on 61³: the amount
within r ≤ 3 is 0.966, 0.748, 0.669, 0.664 at t = 4, 8, 16, 60 (→ 2/3)
while max|u| there falls 9.9·10⁻², 4.0·10⁻², 1.0·10⁻², 1.2·10⁻³ and
3Σ_x|u|² over the board is 0.3333 at every tick. *The thing's Node* (81³,
period 16, a returning Node at (12, 0, 0), (7, 7, 7), (16, 0, 0)): |u| at
the Node 1.000 of the free run's, n 0.652, 0.654, 0.667; the six neighbours'
|u| 1.02 to 1.16, n 0.81 to 1.14; on the axis between source and mirror n
within 1 % of the free run. *The integers*: the isqrt table above; the
bounds are algebra.

**Verdict.** The amplitude a thing reads: **reached exactly** in the mean
field, |u| = √(S/(4√3π))/r = 0.5373 √(GM)/r, the potential's 1/r with the
count's anisotropy halved. Its scaling with the source: **different law**,
√M for one owner, Σ_j √m_j for a body (linear in M only for owners of one
content): a clock and a push read two different masses of the same body.
The standing set: **new**, u = 0 on the flat bands, invisible to the wait.
A thing's Node: the amplitude the free field's (**exact** in the equation
for u), the count half to two thirds of it. The integer rule: the amplitude
is a many-quanta reading, **not reached** in whole quanta where things move
at w ≥ 0.22 (the mean at most n/3, the count over three); **reached** in the
formula layer, and in whole quanta at w ≤ 1/10 inside r_h < r < r_wave.

## 40. Round 6: the clock of a thing at rest, and the redshift

**Rules used.** R11 and section 39; R7′ (the clock M/K); R9's two readings
of the second order (section 24); section 31 (G = κξ/(2π), S = κξM per
owner, κ = 1/(√3R) the flux per unit set, ξ the set per content).

**(i) The clock.** A thing at rest at r reads |u|(r) per interval, in
quanta^{1/2}, its content cancelling (section 39), and owes w|u| intervals
per interval; its phase advances ρ = M/K in the intervals it does not wait,
so

```text
ρ_eff / ρ = 1 − w |u|(r) = 1 − w · 0.5373 √(G M) / r                       (one owner of content M),
          = 1 − w c₁ · G M / r,     c₁ = 1/√(2√3 G m) = 0.5373/√(G m)      (a body of owners of content m),
```

against general relativity's 1 − GM/(rc²): the potential's form, local and
in integers, GR's coefficient exactly at

```text
w = 1/c₁ = √(2√3 G m) = 1.861 √(G m) = 0.7425 √(S_m) = √(ξ m / (π R))     intervals per unit of amplitude,
```

S_m = 2πGm the flux of one elementary owner, ξm its set and R its extent.
Round 3's w = 11/9 was a pure number because the diffusive field's amount
carried the coupling; here the amplitude carries its root, and w is set by
the elementary set: w_GR² = 2√3 G m, the model's wait constant reads the
strength of gravity times the content of the smallest owner. For one owner
the same w gives 1 − √(Gm/(GM))·GM/r: a single thing of content M ≠ m slows a
clock by √(m/M) of GR's; the star of A6, one owner of flux S, needs
w = 0.7425 √S for its own coefficient. A loop's period P/P₀ = 1/(1 − w|u|),
the same factor; a ring of any content, a free thing of any content, the
same slowing (the unit of section 39). At the engine's unit (wait-reads-v1,
w_e per quantum of content × ⌊3|u|⌋) the rate is 1 − 3 w_e M_thing |u| and
GR's coefficient sits at w_e = 0.620 √(Gm)/M_thing, one w per content: no
one w serves two clocks of different content, which is the case for the
content-cancelling unit adopted here. The anisotropy (3/4)ω₀²K₄, half the
count's: the clock slower on the body diagonals of the mass than on its
axes at the same r, by (3/4)ω₀²(2/5 + 4/15) = 0.5 ω₀² relative.

**The second order.** Two readings, as in section 24. Queued (the thing
reads in every lattice interval, waiting or not): it owes w|u| per interval
and ticks (1 − w|u|)T times in T intervals, exactly 1 − x, x = w|u|, frozen
at x = 1. Strict (a waiting thing reads nothing): it owes w|u| per tick, so
T = T_tick(1 + x) and the rate is 1/(1 + x) = 1 − x + x², never frozen. GR
needs, at second order, a coefficient that depends on the radial coordinate:
√(1 − 2x) = 1 − x − x²/2 in the Schwarzschild r, (1 − x/2)/(1 + x/2) =
1 − x + x²/2 in the isotropic r, the flat coordinate grid the lattice has
(up to the conformal factor). The two readings straddle the isotropic value
(0 and +1 against +½) and neither is either: **different law at second
order**, of size x² = (GM/r)² at the GR w, 1 to 3 % of the period for a ring
at r = 8 from S = 40 (x = 0.17). What a thing reads while it waits, open
since round 3, is now this: it decides between 0 and +x².

**(ii) The redshift.** A clock at r₁ runs at ρ(1 − w|u|₁), one at r₂ at
ρ(1 − w|u|₂); the light things between carry no clock (R7′), every one of
them is late by the same Shapiro delay of section 41 in a static field, so
the received rate against the receiver's clock is

```text
ν₂/ν₁ = (1 − w|u|₁)/(1 − w|u|₂),    z = ν₁/ν₂ − 1 ≈ w c₁ G M (1/r₁ − 1/r₂)  →  G M (1/r₁ − 1/r₂) at w = 1.861 √(G m),
```

GR's GM(1/r₁ − 1/r₂)/c² in form and, for a body of equal owners, in
coefficient at the w of (i); 0.5373 w √(GM)(1/r₁ − 1/r₂) for one owner.

**Dictionary.** w c₁ ↔ the ratio of the wait's coupling to the push's, 1 at
GR; x = w|u| ↔ GM/(rc²); the queued and strict readings ↔ the second-order
coefficient 0 or +1 against GR's ∓½.

**Check.** Section 39's |u|(r) (0.96 to 1.02 of the coefficient on the
diagonals at r = 8 to 24); the rest is algebra on it, and the second order
is the two series.

**Verdict.** Gravitational time dilation: **reached** in form, 1 − wc₁GM/r,
with GR's coefficient at w = 1.861 √(Gm) for a body of owners of one content
m; **different law** for a single owner (√M) and across compositions
(Σ√m_j); the second order **different law** (0 or +x² against −x²/2 or
+x²/2). The redshift: **reached** in the potential's form, with the same w.

## 41. Round 6: the bending of light, the Shapiro delay, and one w

**Rules used.** R11, section 39's |u|; points 10, 21, 25 (a thing's one
path, its step by the momentum, a thing that owes a tick does not cross its
Link); section 35 (iii) and (iv) (the push over a pass, GM/b); the integrals
∫ dx/√(b² + x²) = asinh(x_A/b) + asinh(x_B/b) ≈ ln(4x_Ax_B/b²) and
∂_b of it → −2/b; ∫ b dx/(b² + x²)² = π/(2b²).

**(iii) The bending.** Three things are bent.

*The image of light*, a real light thing's one path. The exact local
mechanism: a thing at a Node with heading h and momentum p that owes k
intervals stays at the Node k intervals (point 25) and then leaves through
the Port its momentum decides (point 21: the first axis whose component has
reached its content, else its heading). The wait is a scalar count on the
thing, without an axis: it enters no component of the momentum and chooses
no Port. The gradient of the wait across the beam is a relation between
neighbouring paths, and a thing has one (point 10): nothing at its Node
tells it that the Node one Link nearer M would have held it longer. **The
wait turns no path**: α_image = GM/b at every w, the push alone (section 35
(iii)). Its only trace on the path is second order and only under the
queued reading: a thing that reads the push in every interval it stays takes
Δp_⊥ = p ∫ J_⊥ (1 + w|u|) dx, and the correction is

```text
Δα/α_image = w ∫ J_⊥|u| dx / ∫ J_⊥ dx = (π/4) w |u|(b) = 0.785 w c₁ G M / b     (0 under the strict reading),
```

α_image(1 + 0.79 GM/b) at the GR w. A quarter of Einstein's 4GM/(c²b) in
every reading. If a lawful reading were to bring the time half to the path,
it would have to enter the momentum, the only thing that turns a path: per
interval, M_thing times the lattice gradient of the wait's potential across
the thing's Node, w(|u|(x + e_i) − |u|(x − e_i))/2 on each axis toward the
larger amplitude, a second push of size w M_thing · 0.5373 √(GM)/r² toward
M, an inverse square of strength w c₁ G M M_thing/r², Newton's own at the GR
w; over a pass it would add 2GM/b to the image (3GM/b, front 5GM/b), not
Einstein's 4 either, the return half of the push still never reaching a
thing at speed 1 (section 34). The Node does not hold that gradient: its six
amplitudes carry the wave's direction in their sizes (0.62, 0.045, 0.083)
and the wavefront's curvature in their phases (section 44), and the
envelope's change over one Link, |u|/r, is below the engine's 1/32 wherever
r > 32 |u|. Stated, not written.

*The front of light*, the surfaces of equal phase of successive light things
from one emitter, read by an interferometer or a two-slit behind the mass.
Each thing is late by Δt(b) = w ∫|u| dx = w · 0.2143 √S [asinh(x_A/b) +
asinh(x_B/b)]. The front's local normal at the ray b after the pass:
two neighbouring rays at b and b + δb differ in direction by θ′(b)δb and in
delay by Δt′(b)δb, so the front through the two things is tilted from the
rays' perpendicular by −Δt′(b), and its normal is turned by θ(b) − Δt′(b):

```text
α_front(light) = α_image + w · 0.2143 √S · 2X/(b√(b² + X²))  →  G M/b + 2 w c₁ G M/b  =  G M/b + 1.075 w √(G M)/b   (one owner),
                                                                 →  3 G M/b   at w = 1.861 √(G m)   (a body of equal owners),
```

toward the mass, the wait's term 1/b (against round 5's 1/b²): **Einstein's
space half, 2GM/b, exactly in the front at the w of the clock**, and the
front and the image disagree by it. Against 4GM/b: the front three quarters,
the image a quarter. An astronomical plate reads the image; a phase
interferometer (VLBI) reads the front; physics has both at 4GM/b.

*The front of the field*: unchanged from round 5, a shadow reads nothing and
waits nothing under R11, so 0.

**(iv) The Shapiro delay.** For light, the wait along the pass:

```text
Δt(light) = w ∫ |u| dx = w · 0.2143 √S · [asinh(x_A/b) + asinh(x_B/b)] ≈ w c₁ G M · ln(4 x_A x_B / b²)
          →  G M · ln(4 x_A x_B / b²)   at w = 1.861 √(G m)     (one owner: 0.5373 w √(G M) · ln(4 x_A x_B / b²)),
```

against GR's 2GM ln(4x_Ax_B/b²): **the logarithm reached, the coefficient
half**, the ratio 1 against 2 of section 24 (the same wait serves a clock,
one part of the metric, and light's index, two parts). The delay grows with
the path as the logarithm while the deflection saturates: no fixed ticks per
radian (round 5's 2.72 w). The field's delay: 0 (a shadow waits nothing);
the recoil of a push is not delayed. Point 16 admits one rule per pair of
families, so a w of light's family different from matter's is lawful:
w_γ = 2 w_m gives Shapiro exact and the front 4GM/b + GM/b = 5GM/b;
w_γ = (3/2) w_m gives the front 4GM/b exactly and Shapiro at three quarters;
no pair gives both, the push's GM/b lying outside the index. Stated, not
adopted.

**(viii) One w.** For a body of owners of one content m, w = 1.861 √(Gm)
gives GR's clock 1 − GM/r, GR's redshift, Einstein's space half in the front
(front 3GM/b), and Shapiro's logarithm at half; the image stays GM/b. This
is section 24's table with 11/9 replaced by 1.861 √(Gm) and the lingering
diffusive amount replaced by the amplitude of a wave field that passes; the
single thing of content M, and A6's star, obey it with the law in √M. **Not
reached** in full: reached for the clock, the redshift and the front's space
half; Shapiro at half; the image at a quarter.

**Dictionary.** Δt′(b) ↔ the tilt of the front by the delay gradient; the
index of the vacuum for light ↔ 1 + w|u| = 1 + GM/r at GR's w, half of GR's
1 + 2GM/r; w_γ/w_m ↔ γ of the parametrized post-Newtonian metric.

**Check.** *The path sums* (section 39's runs, lines parallel to x at impact
parameter b, x ∈ [−28, 28]): Σ_x|u| = 0.970, 0.977, 0.982 of
0.2143√S · 2asinh(28/b) at b = 8, 12, 16 at period 16 and 0.974, 0.982, 0.991
at period 32; the growth with the half-length X at b = 8: 0.315, 0.516,
0.651, 0.751 at X = 7, 14, 21, 28 against 0.311, 0.522, 0.666, 0.774 (the
asinh's growth, ratios 1.01 to 0.97) while Σ_x n saturates, 0.0204, 0.0293,
0.0332, 0.0354 (the atan of section 35); d(Σ_x|u|)/db = 0.94, 0.99, 0.97 of
−0.2143√S · 2X/(b√(b² + X²)) at period 16 and 0.96, 0.90, 1.12 at period 32;
Σ|u|/ΣJ_⊥ = 47.6, 62.1, 74.3 against 48.0, 60.7, 71.7 (the wait's integral
against the push's, in intervals per radian, no longer a constant).
*The mechanism*: points 10, 21 and 25 as quoted; the second-order integral
π/(2b²) is elementary.

**Verdict.** The image: **different law**, GM/b at every w (the wait turns no
path; a quarter of Einstein). The front of light: **reached** in its space
half, 2GM/b at the w of the clock, the front 3GM/b (**different law**, three
quarters). Shapiro: **reached** in the logarithm, **different law** in the
coefficient (half of GR's), a per-family w reaching either Shapiro or the
front but not both. One w: **not reached** in full; the clock, the redshift
and the front's space half at w = 1.861 √(Gm), as in round 3.

## 42. Round 6: Coulomb near a mass, the far field of a thing near a mass, and the books

**Rules used.** R11 and section 39; section 31 (Coulomb and Newton under
R10, ζ = 1); section 36 (the same questions under the count); point 7 (the
books per bit), point 3 as amended (the return is a field), point 11 (the
computation is the things' content); `node_mixing` and the dense layer's
`_mix` as they stand (node-mixing-v1), `pushed_ray` (clock-readings-v1).

**(v) Coulomb's law between two things at rest near a mass.** A and B at
separation s, both at r from a mass M. In lattice time nothing changes: the
push B takes from A reads A's amount, whose flux S_A is declared and
conserved through every shell (section 26 (ii)), and R11 touches no shadow;
the force is k_C q_A q_B/s² at every r from M, **reached** as in section 36.
In local time each thing's clock runs at 1 − w|u_M|(r), so the same
momentum per lattice interval is, per tick of the local clock,

```text
F_local = F / (1 − w|u_M|) = F [1 + w c₁ G M / r] = F [1 + G M / r]   at w = 1.861 √(G m),
```

the potential's form, where section 36 had the acceleration's. Physics has
the locally measured force unchanged (the freely falling frame is flat) and
the coordinate force carrying √g₀₀ ≈ 1 − GM/r; here the lattice force is
the flat one and the local force is larger by 1/√g₀₀ at first order:
**different law** in the local measure, by GR's factor in the inverse
place. A second-order companion: A's wave has the frequency of A's slowed
clock, so its wavelength is longer by 1 + w|u_M| and its fixed anisotropy
(15/8)ω_A²K₄ smaller by (1 − w|u_M|)². No path term: A's shadows crossing
M's field wait nothing (a shadow reads nothing), so the retardation stays
section 28's √3 s and there is no screening.

**(vi) The far field of a thing near a mass.** B's flux is conserved, so
J = S_B/(4πr²) holds: **1/r² kept**; the wavelength longer by 1/(1 − w|u_M|),
the anisotropy smaller; no lens and no pile-up (nothing holds a shadow); the
amplitude of B's field at a third thing's Node is |u_B| of section 39 with
B's slowed clock, so B's own potential is unchanged in size and longer in
wavelength. Under R11 the far field of a thing near a mass is the far field
of that thing with a slower clock, nothing else, as under option I of round
5.

**(vii) The books.** The wait is a counter on the thing and on nothing
else. In the engine's terms: `pushed_ray` adds to the thing's `owed` the
push's components in quanta times the wait's numerator and the thing spends
one interval per denominator; under R11 it adds instead n_w × |3u|, |3u| the
integer root of Σx² + Σy² of the owner's coherent sum at the scale
32 × 256 = 8192 (section 39 (iv)), summed over the owner groups present at
its Node (owner, flow and sign; the thing's own groups excluded, point 3),
and spends one interval per 24 576 d accumulated: exact integers, the
register rule on the thing's side, the mean rate 1 − w Σ|u_j| to within one
interval per 1/(wΣ|u_j|) intervals. Nothing is sourced, parked or held: the
shadows are returned as before with their amounts, phases and momenta, the
push is what R4′ gives, so the ledgers of amount, momentum and charge (point
7) are untouched, and the third law is unaffected: the return carries the
same −Δp on the same field at the same speed, the wait delaying the thing's
next step and never its reply. Standing content at the thing's Node reads
zero (section 39 (ii)), so the self-reading exclusion of section 34 is
needed only for the thing's own outgoing wave, which point 3 already
computes as zero. **Exact**, one counter on the thing, as option I of
section 36.

**The cost of |u|.** The Node forms u already: `node_mixing` computes
(sum_x, sum_y) = Σ_j A_j at the phase tables' scale before the six leaving
amplitudes (cx = sum_x − 3x_entry, cy likewise), and the dense layer's
`_mix` forms the same sums (ax.sum, ay.sum) before subtracting 3 ax[OPPOSITE];
the six roots per group per Node per interval are taken for the A_j. The
size |3u| = √(sum_x² + sum_y²) is one integer root more, on products already
inside the 64-bit work (|cx|, |cy| < 2³¹ is checked), and it is needed only
at a Node that holds a thing, once per owner group present: one root per
thing per group per interval against the six the mixing takes at every Node
of every group. The computation of the world stays the things' (point 11),
and the shadows' cost is unchanged. The engine's wait-reads-v1 (PR #308) is
this: `arrival_amplitude` forms the group's sum over the shadows at the
thing's Node (per Port the amount at the phase of its sum, the root of
amount × 32², the six summed on the tables), takes the root of x² + y² once
per group per interval inside the push's loop over the shadows, and floors
it to whole units of 32; it reads 3|u| where this document reads |u|, and
multiplies by the content (section 39). Its `owed` is in units of 1/d of an
interval and the whole units of amplitude are floored per interval, not
accumulated: below one unit of 3|u|, that is |u| < 1/3 (r > 3w · 0.2143 √S,
every r of A6's board), the engine's amplitude wait is zero, where the
register rule stated above accumulates the fraction and waits per whole
unit in the mean; the far-field law of this round is read in the engine
only with that accumulation (a remainder on the counter, as the push has
`push_remainder`).

**Check.** Section 31's algebra; the engine's `node_mixing` and `_mix` as
read on 2026-09-18 (the coherent sum formed before the outputs; the root of
amount × 32²; the `owed` counter in units of 1/d); the exactness is by
construction (the counter changes no ray).

**Verdict.** Coulomb near a mass: **reached** in lattice time in every
reading; **different law** in local time, by 1 + GM/r at the GR w (the
potential's form now). The far field of a thing near a mass: **1/r² kept**,
a slower clock and a longer wavelength, no lens. The books: **exact**, one
counter on the thing; the third law unaffected. The cost: one integer root
per thing per owner group per interval, on a sum the Node already forms
(wait-reads-v1 takes it so); the engine's floor per interval reads nothing
below |u| = 1/3, an accumulating remainder on the counter being what the
far field needs.

## 43. Round 6: the sizes for A6, the separating observable and the verdicts

**Rules used.** Sections 39 to 42; section 30 (the integer wave, 64 to 256
quanta per Node); section 19 (the capture radius b_c = GM); section 37 (the
sizes under the count); the A6 entry of
[EXPERIMENTS.md](EXPERIMENTS.md#a6-light-bending-by-a-bound-group-and-g_eff-n²-over-n--28-to-216).

**(ix) The sizes.** The star of A6 a clocked thing of flux S, one owner,
GM = S/(2π), b_c = GM. A thing at rest waiting always, w|u| ≥ 1, is frozen
inside

```text
r_h = w · 0.2143 √S = w · 0.5373 √(G M)         (mean field);
r_h = G M   exactly at the star's own GR w = 0.7425 √S  (GR: 2GM in the Schwarzschild r, GM/2 in the isotropic r),
```

against section 37's 0.93 √(wGM) under the count: linear in w, not in √w,
and r_h < b_c whenever S > 1.81 w²: at w = 1 every star of flux above 2
hides its horizon inside its capture radius, and at the GR w the two
coincide. In whole quanta (section 39 (iv)): r_wave = 0.023 √S (256 quanta
per Node) or 0.046 √S (64), so the window r_h < r < r_wave in which a thing
moves inside a whole-quanta wave exists only for w < 0.11 (or 0.22); on
A6's board (S = 10 to 100, r_wave = 0.07 to 0.23 Links) there is no wave in
whole quanta at any Node, and the amplitude the integer Node forms is at
most a third of the count everywhere. A whole-quanta wave at r = 8 needs
n(8) ≥ 256, S ≥ 1.2·10⁵. The sizes at S = 10, 25, 40, 100 (GM = 1.6, 4.0,
6.4, 15.9), w = 1, the mean field:

```text
                          S = 10          S = 25          S = 40          S = 100
r_h (amplitude / count)   0.68 / 1.17     1.07 / 1.86     1.36 / 2.35     2.14 / 3.71
ring at r = 8  slowed by  8.5 % / 2.2 %   13.4 % / 5.4 %  17.0 % / 8.6 %  26.8 % / 21.5 %
ring at r = 16            4.2 % / 0.5 %   6.7 % / 1.3 %   8.5 % / 2.2 %   13.4 % / 5.4 %
ring at r = 32            2.1 % / 0.13 %  3.4 % / 0.34 %  4.2 % / 0.5 %   6.7 % / 1.3 %
light at b = 8, X = 28: late by   2.7 / 0.45 ticks   4.2 / 1.1     5.3 / 1.8     8.4 / 4.5
light at b = 8, X = 96            4.3 / 0.51          6.8 / 1.3     8.6 / 2.1    13.6 / 5.1
image G M / b at b = 8            0.20 rad            0.50          0.80          1.99
front's wait tilt at b = 8        0.17 w rad          0.27          0.34          0.54
```

(the count's figures from section 37, with the free-field n; at the thing's
Node they are half to two thirds of that, section 39 (iii)).

**(x) The single observable that separates the two readings in one run.**
The clock's slope against r: three rings at r = 8, 16, 32 from the mass, in
the formula layer, in one run. Under the amplitude the period's excess
halves per doubling of r; under the count it quarters: at S = 40, w = 1,
17.0, 8.5, 4.2 % against 8.6, 2.2, 0.5 %, the ratio of the excess at r = 8
to that at r = 32 being 4 against 16; over 100 periods of 16 the excess is
270, 136, 68 ticks against 138, 34, 9. The same run reads a second
discriminant: a light thing along the line at b = 8 is late by 5.3 w ticks
under the amplitude (growing with the path as the asinh, 8.6 w at X = 96)
against 1.8 w (saturating), whole ticks in one pass; and two runs at S and
4S read √S against S in the ring's slowing (doubling against quadrupling).
A6's own geometry (the register after a pass) separates nothing: the image
is GM/b under both.

**The verdicts**, extending section 38 (option I, the law as it stands, is
the count; R11 the amplitude):

| Law | Round 5, I (the wait reads the count, section 38) | Round 6, R11 (the wait reads the amplitude) | Run |
| --- | --- | --- | --- |
| What a thing at rest reads | n = (√3/2)GM/r² (free field; at the thing's Node half to two thirds of it) | **\|u\| = √(S/(4√3π))/r = 0.537 √(GM)/r**, the potential's 1/r, the root of the flux (measured 0.96 to 1.02 of it) | a thing's wait count beside a body |
| The mass a clock reads | Σ_j m_j | **different law**: Σ_j √m_j (√M for one owner; linear in M for owners of one content) | a ring beside one owner of 64 and beside two of 32 |
| Gravitational time dilation | 1 − (√3w/2)GM/r² | **reached** in form: 1 − wc₁GM/r, GR at w = 1.861 √(Gm) = √(ξm/(πR)); second order 0 (queued) or +x² (strict) against GR's −x²/2 or +x²/2 | three rings at r = 8, 16, 32, formula layer |
| Gravitational redshift | (√3w/2)GM(1/r₁² − 1/r₂²) | **reached**: wc₁GM(1/r₁ − 1/r₂) | two rings |
| Light bending, the image | GM/b | **GM/b**, every w (the wait turns no path; second order (π/4)w\|u\|(b) under the queued reading) | A6 with the wait |
| Light bending, the front | GM/b + 2.72w GM/b² | **reached** in the space half: GM/b + 2wc₁GM/b = 3GM/b at the GR w (three quarters of Einstein) | a two-slit behind the mass |
| The field's front through a mass's field | 0 | 0 | — |
| Shapiro delay of light | 2.72w GM/b, no logarithm | **reached** in the logarithm: wc₁GM ln(4x_Ax_B/b²), **half** of GR's coefficient at the GR w; the delay grows with the path | A6 arrival tick, X = 28 and 96 |
| Shapiro delay of the field | 0 | 0 | — |
| Coulomb near a mass | reached; ×1/(1 − wn) in local time | **reached** in lattice time; ×(1 + GM/r) in local time at the GR w | A5s beside a body |
| Far field of a thing near a mass | 1/r² kept; λ_w longer by 1 + wn | **1/r² kept**; λ_w longer by 1 + w\|u\|; no lens | E11 beside a body |
| The books (point 7) | exact; the counter on the thing | **exact**; the counter on the thing reads \|3u\| at scale 8192, one root per thing per group per interval on a sum the Node forms (wait-reads-v1 does; it floors per interval and carries the content, section 42) | E11 (a) |
| Newton's third law | exact, through the field | **exact**, unaffected (the wait delays the step, never the reply) | E11 (a) |
| The standing set under the reading | read in full (n) | **new**: u = 0 on the flat bands, invisible; 3Σ\|u\|² = the wave bands' amount | a lone shadow re-released at a thing |
| One w for the four tests | not reached (no GM/r term) | clock, redshift and the front's space half at w = 1.861 √(Gm); Shapiro at half; the image at a quarter: **not reached** in full (round 3's table with 11/9 → 1.861 √(Gm)); a per-family w reaches Shapiro or the front, not both | — |
| The horizon | 0.93 √(wGM), inside b_c for GM > 0.87w | **r_h = w · 0.537 √(GM)**, = GM at the star's GR w; inside b_c for S > 1.81w² | — |
| The integer wave and the wait | incompatible at w ≥ 1/256 | the amplitude formed only inside a whole-quanta wave, ≤ n/3 outside: **not reached** in whole quanta at w ≥ 0.22; a window r_h < r < r_wave at w < 0.11; the formula layer otherwise | A6 in the formula layer; a dense wave at w = 1/32 |

Open after this round, one line each: the composition law Σ_j √m_j (whether
the family's quantum, of which every thing is a whole multiple, makes the
owners of nature one content, which would restore the linear law); the
second order of the clock (0 or +x²), and the near-field correction at the
thing's Node (the neighbours' u raised by 2 to 16 % by the mirror); the
front's tilt read directly by a two-slit behind a mass in the formula layer
(the derivation's −Δt′(b) against the pattern); round 5's coefficients
restated with the count at a thing's Node (half to two thirds of the free
n); the whole-quanta window at w ≤ 1/10 (a dense wave of 256 to 3000 quanta
per Node with a thing inside it); the ratio 1 against 2 of the clock's and
light's wait (a per-family w, which point 16 admits); whether the
reading is per owner (Σ_j|u_j|, this round) or of the total sum
(|Σ_j u_j|, which beats between owners of differing clocks and adds as √N
between owners of random phase); and the unit of the wait, the content (this
document, every clock alike) or the quantum of push (the engine's counter
since clock-readings-v1, a clock slowed in proportion to its own content),
which two rings of different content at one r decide.

## 44. Round 6: a local 1/r reading without the root, and the amplitude as the basic integer

The model owner's question of the same day, on the direction of round 6: is
there a local reading at a thing's Node that falls as 1/r without the
integer square root, from the phase's rotation or from anything the Node
already holds (amounts per Port, phases per Port, their differences, the
number of Ports carrying the owner's shares, the pattern of whole-quantum
arrivals over intervals); and what the alternative of carrying the amplitude
as the shadow's basic integer, with the intensity as its square read where
counting happens, does to exact conservation, the push and the books.

**Rules used.** R10, R2, section 26 (the exact relations between u and the
Port amplitudes), section 27 (v) (the far field), section 30 (the integer
rule), points 5, 7, 22, 25 (the amount never cancels, the books exact, the
parked shadows, the amounts add on a lane).

**(i) What the Node holds, and its degree in r.** For a monochromatic field
the Port amplitudes are exactly (from B_p = u − A_p, R2 and e^{−iωt}):

```text
A_p(x) = [e^{iω} u(x) − u(x + e_p)] / (2i sin ω),
```

so everything the Node holds per owner is a function of u at the Node and
its six neighbours. In the far field of a clocked thing, u = U e^{ik r}/r
(section 27 (v)), and for a Node at distance r on an axis, with c_p = e_p·r̂:

- *The amounts.* a_p = |A_p|² = (|U|²/r²) f_p(r̂, ω, k) [1 + O(1/(kr)²)],
  degree −2 in r, with fixed ratios f_p (0.62, 0.045, 0.083 at ω → 0 for
  the forward, backward and transverse arrivals). The near-field term of
  A_p is in quadrature with its main part, A_p ∝ (1 − (k/ω)c_p) −
  i c_p/(ωr) + O(1/r²) at small ω, so the modulus squared has no 1/r term:
  every amount, every sum, difference, product or ratio of amounts, the
  parked ninths and their mean (4/9), the count of Ports carrying shares (6
  in the mean field) are of even degree in 1/r, and the ratios of degree 0.
- *The phases.* φ_p = arg u + const_p + γ_p/r + O(1/r²). The common part,
  arg u = kr − ωt, is r modulo the wavelength: periodic, and no monotone
  function of r can be built from it or from its rotation, which is ω per
  interval at every r. The constants are the plane wave's Port offsets,
  ω/2 for the transverse arrivals, (ω − k)/2 for the forward one,
  (ω + k)/2 + π for the backward one. The 1/r terms are exact from the
  formula above: γ = cot((ω + k)/2)/2 for the forward arrival, cot((k −
  ω)/2)/2 for the backward one, k/4 for the transverse ones (0.83, 3.35,
  0.17 at period 16; at ω → 0, 1/((1 + √3)ω) and 1/((√3 − 1)ω)). **The
  Node's phases hold a 1/r quantity**: the curvature of the wavefront,
  the wavelength over r. It carries no S and no G; it is ∝ K/(M r), the
  Compton length of the source over r, falling with the source's content
  where the potential rises with it; it needs the wave in whole quanta
  (the same condition as the amplitude, section 39 (iv)) and a phase
  resolution finer than it, 2π/N < γ/r, r < 8.5 Links at N = 64 and period
  16, and for a mass of nature at 10⁶ m it is 10⁻²¹ rad. Not the
  potential.
- *The counts over intervals.* The rate of whole-quantum arrivals is n,
  degree −2; the interval between arrivals 1/n, degree +2 (a counter on the
  thing can hold it).

Every quantity formed from these by sums, differences, products, ratios,
comparisons and counts is therefore of even degree in 1/r when it carries
the coupling S, with two exceptions, both nonlinear: the root of an amount
(degree −1 with √S: the amplitude), and an amount divided by a curvature
phase, (S f_p/r²)/(γ/r) = S f_p ω r/(γ r²)·(ω/ω) ∝ S ω/r ∝ GM²/(K r) (degree
−1 with S, but the content squared, the potential times the source's
clock; a division by an angle resolved only within a few wavelengths of
the source, and needing the wave). There is no third: the phase alone
carries no r, the amounts fall as 1/r², and their ratios and counts do not
fall at all. **The amplitude via the root is the minimum**: the field is
linear in the amplitude and the count is its square (section 26: n = 3|u|²),
so the potential's 1/r is the square root of the count's 1/r² and nothing
the Node holds recovers an odd power of r from even ones without a root.

**(ii) The amplitude as the basic integer.** The alternative: a shadow's
basic integer is its amplitude (a Gaussian integer x + iy at a scale s per
quantum^{1/2}, or a size and a phase step), the amount being (x² + y²)/s²,
read as a square where counting happens (the push, a mark). Assessed
against the law:

- *Exact conservation of the amount.* The mixing on amplitudes is the
  division by 3: S₃ = J − 3I has S₃² = 9I, so exactness at a Node needs
  Σ_q A_q ≡ 0 (mod 3) in both components, which no field satisfies at
  every Node and interval; the outputs must be rounded, and the amount
  Σ|B_p + δ_p|² − Σ|B_p|² = 2Re Σ B_p* δ_p + Σ|δ_p|² is first order in the
  rounding δ and of either sign: not a bounded remainder but a drift and a
  random walk, which no register on the amplitude can hold (the residual
  is quadratic). Measured (a plane wave on a periodic 16³ box, 256 ticks,
  rounding to the nearest Gaussian integer at every Node): the total amount
  ×2.8, ×1.5, ×1.1 at s = 1 for 64, 256, 1024 quanta per Node; +11, +16,
  −8 % at s = 4; +3.0, −1.7, +0.1 % at s = 32, with a one-tick rounding
  error of the amount per Node of rms 0.16 to 13 quanta and a bias of −1.5
  to +4 quanta at s = 1. The amount-basic rule of node-mixing-v1 (the whole
  quanta and the ninths apportioned by |B_p|², section 30) is exact by
  construction. Point 7 (the books close at every Node and interval) holds
  in the mean only under the alternative.
- *The push.* It reads the amount per Port, (x² + y²)/s², a rational, with
  the whole quantum of point 23's count a threshold on it: unchanged in
  form and no cheaper (a square per Port in place of a root per Port). But
  two shadows of one owner on one lane (point 25: the amounts add) or at a
  Node sum coherently in amplitude, |A₁ + A₂|² ≠ |A₁|² + |A₂|²: an amount
  would be created or destroyed at every merge, against point 5 (a phase
  decides the heading, never an amount) unless the size is reset to
  √(a₁ + a₂), which is the root again.
- *The books.* Point 7, point 25 and the remainders of section 3.17 are
  written on amounts; under the alternative they hold in the mean; the
  momentum the shadows carry is apportioned by shares of the amount, which
  needs the amount at every Node anyway. And the wait's reading of the
  size, |Σ_p A_p|/3 = √(Σx² + Σy²)/3, is a root in either representation
  (or the count again if it read the square): the root moves from the
  mixing to the reading and to every lane merge; it does not disappear.

**Dictionary.** The parity of degrees ↔ intensity is quadratic in the
field; γ/r ↔ the wavefront's curvature, λ_w/(2πr)-sized; Gaussian integers
↔ the amplitude as two integers.

**Check.** *The phases* (section 39's runs on the axis at r = 8 to 24, the
time-harmonic component of each Port amplitude over the last period): the
measured Port phases against the exact formula from u at the neighbours
agree to 0.01 rad (forward −0.039, −0.075, −0.091, −0.111, −0.109 against
−0.038, −0.076, −0.090, −0.112, −0.113 at period 16; backward −2.228 to
−2.455 against −2.228 to −2.438); against the plane-wave offsets plus the
1/r terms, (ω − k)/2 + 0.832/r = −0.044, −0.079, −0.096, −0.106, −0.113 for
the forward arrival at r = 8 to 24 and ω/2 + k/(4r) = 0.218 to 0.203 for
the transverse (measured 0.206 to 0.215; the plane-wave offset alone is
0.196), and at period 32 (ω − k)/2 + 3.63/(2r) = +0.154, +0.079, +0.041
against +0.159, +0.083, +0.026 at r = 8, 12, 16. *The amounts*: the Port
ratios 0.68, 0.05, 0.067 at r = 8 and 0.63, 0.06, 0.078 at r = 24
(period 16), |A_fwd|² r² = 0.071 to 0.061, the residual variation the
anisotropy and the O(1/(kr)²) term. *The integers*: the drift table above
(16³, 256 ticks, seconds).

**Verdict.** A local 1/r reading without the root: **none for the
potential**. The amounts and everything linear in them fall as 1/r²
(**exact** in the mean field), the phase's rotation carries no r, and the
one 1/r quantity the Node holds, the wavefront's curvature in the Port
phases (γ/r, **new**, measured to 0.01 rad), carries no coupling and falls
with the source's content; the amplitude via the root is the minimum. The
amplitude as the basic integer: **not lawful** under points 5, 7 and 25
(the amount conserved in the mean only, a drift of 0.1 to 180 % in 256
ticks measured; an amount created or destroyed at every coherent merge)
and not cheaper (the root returns at the wait's reading and at every
merge); the amount-basic rule with the root toward the mixing is the
minimum that keeps the books exact.

## 45. Round 7: a thing emits; what a finite amount given once cannot do, on any board

Round 7 (2026-09-18, the evening, after PR #313) derives the model owner's
decision of the same evening (Highlights 5.4, "A thing emits; nothing is
given with the board", branch docs/a-thing-emits, PR #319, its two
commits): a thing releases shadows every interval in proportion to its
content, a shadow is never made to disappear, and the stream leaves the
world at the edge of an open board, which stands for infinity. What the
round establishes on paper: why the field of a thing at rest could not be
a stock of shadows given with the board (this section), what the fixed
point of the emitting thing on the open board is and when it is reached
(section 46), what the whole quanta do to it (section 47), what the tests
of rounds 4 to 6 become under it (section 48), what the emission does to
the rest of the law (section 49), and the run plan (section 50). As
before: bottom-up from the stated operator, no physics assumed, no engine
run, no edit to the engine; every number is checked by an iteration of the
stated rules on a box of 25³ to 41³ Nodes (seconds each, 45 s for the
longest integer run), cited after each derivation and never used as its
source. Unlike rounds 4 to 6 the scratch script is committed this time, as
`tools/derivations_round7.py` (its subcommands `meanfield`, `integer`,
`edge`, `home`, `walk`, `transit`), because the run plan of section 50
quotes its fixed point as the prediction; it is not an engine run and
establishes nothing about the engine.

**The rules as they stand after the decision.** R10 (the Node mixes the
six, section 26), R2 (one Link per interval), R4′ (the two readings, point
16), R11 (the amplitude reading, section 39), point 3 as amended (the
return is a field), and three rules stated here as what a Node does in one
interval, since nothing else is a rule of this model:

- **R12, the emission** (Highlights 5.4, "A thing emits"). In every
  interval a thing of content M releases q = ρ M quanta as its shadows, ρ
  one rate for the world (point 18's ratio, now a rate), q/6 through each
  of its six Ports in whole quanta with the fraction parked at the thing as
  a remainder per Port (six parked shadows of the thing's own number,
  point 22); every share carries the thing's phase of that interval and
  its owner number. The release costs the thing nothing: shadows are free
  in the books and in time (points 7, 9, 11).
- **R13, home under emission** (point 3, "absorbed and released again with
  the thing", read with R12). Shadows of the thing's own number that reach
  its Node are absorbed and released again with the thing: their amount
  joins that interval's release, shared six-fold with the fresh q at the
  thing's phase (on a lane the amounts add and the phase is the coherent
  sum's, point 25). This is one of four readings of "home" that section
  46 (viii) assesses; it is the one under which the flux of the field
  equals the emission, and the round adopts it below.
- **R14, the edge.** A share sent through a Port that has no Node beyond
  it leaves the board and is booked on the shadows' line as escaped;
  nothing ever arrives through such a Port. The edge Node mixes as every
  other Node, with that Port's arrival zero.

**Assumptions and limit.** Mean field first (the linear map on
amplitudes; the integer form is section 47). One owner. A thing at rest,
its Node absorbing and re-releasing by R13; a probe, where one is read,
returns every share of another owner through the Port it came in (point
3). The board a cube of half-width H (33³: H = 16; 41³: H = 20), the thing
at its centre.

**(i) Theorem 1: a finite amount given once holds no static flux, on any
board.** Let the shadows' total amount be X at t = 0 with no emission
(R12 off), let every Node conserve amount (the unitarity of S, section 26
(ii); the integer rule's registers, section 30; a thing's Node returning
or re-releasing what reaches it; a mark returning), and let the board be
closed. For any set Ω of Nodes write n_Ω(t) for the amount resident in Ω
and Φ_∂Ω(t) for the net Link current leaving Ω through its boundary Links
in interval t. Continuity (section 26 (ii)) is n_Ω(t + 1) − n_Ω(t) =
−Φ_∂Ω(t), exactly, so that summed over T intervals

```text
(1/T) Σ_{t<T} Φ_∂Ω(t) = (n_Ω(0) − n_Ω(T)) / T,        |(1/T) Σ_{t<T} Φ_∂Ω(t)| ≤ X / T.
```

Two statements follow. (a) If the state is a fixed point, or a cycle of
period P, the mean current over one period through every closed surface
is exactly zero: a static field carries no net flux through any shell,
only circulations. (b) On any orbit the time-mean flux through any closed
surface tends to zero at least as X/T. Under the count reading a thing at
x takes per interval J(x) = Σ_p a_p(x)(−e_p), and for a wave J = Φ on
every Link (section 26 (iii), ζ = 1); in general the sum of J·r̂ over the
Nodes of a shell is the Link flux through the shell plus the difference of
the outward amounts on its two faces (section 26 (ii)), a bounded term of
zero time-mean in any bounded state. A static 1/r² push at every angle is
a steady flux S = 4πr²J through every shell; by (a) and (b) S = 0 for a
static state and S ≤ X/T for any state. **A force that is a count needs a
stream; a stream needs a source and a sink; a stock of shadows conserved
on a closed board is neither. Exact.** On an open board the same X passes
and escapes (the A6 lane): the flux is transient and its time-mean is
again at most X/T. Nothing in the size of X, the profile it is written in,
the phase it carries or the length of the run changes this.

What Theorem 1 does not forbid, and what E11 measured, is the shape of the
long-time state on the closed board: the amount spreads over the V Nodes
toward X/V per Node with circulating trains on top, and the push at any
Node is the trains', of zero mean and large swing. E11 (`standing_closed`,
33³, X = 37 748 736, V = 35 937, X/V = 1050 per Node): no fixed point and
no cycle within 120 ticks; the free count per Node flat in r, 2603, 3038,
3059 at r = 4, 8, 12 over ticks 101 to 120 (slope +0.16 ± 0.05 over the L1
shells), the flat state of the theorem, not 1/r²; the content of the
shell k = 4 swinging from 40 312 (t = 1) to 294 (t = 40) to 4390 (t = 88)
per Node as the train leaves, thins and reconverges; the probe's push
changing sign every two or three intervals (36 to 66 sign changes in 119)
with window means 637 ± 588, 1155 ± 685, 1846 ± 621 on the axis at r = 4,
8, 12 (one to three standard errors from zero; the "slope +0.96" is the
ratio of two such means); the free amplitude flat in r (slope +0.07 ±
0.24); and the amplitude at the probe's Node falling as 1/r (−0.83 ±
0.17) with a count 5.5, 4.1, 0.85 times the free field's: the probe's own
mirror piling the passing train at itself, as E11's reading says, and no
potential. Every one of these numbers is what (a) and (b) say a conserved
stock does, and none is the field of a thing at rest.

**(ii) Theorem 2: a closed board with emission and no sink has no fixed
point, and buries the law it carries.** With R12 on and no edge the total
is X(t) = X(0) + q t exactly (the iteration: 400.00 q at t = 400). For Ω
enclosing the thing the mean flux through ∂Ω over T intervals is q −
(n_Ω(T) − n_Ω(0))/T; if the added amount spreads uniformly (the ergodic
limit of Theorem 1's state) n_Ω grows as q t |Ω|/V, and the mean flux
tends to q (1 − |Ω|/V): **the 1/r² net flux of the emission survives on a
closed board, in the long time mean, for r ≪ L.** But three things bury
it. The count per Node grows as q t/V (22 quanta per Node per interval at
q = 786 432 on 33³) and overtakes the direct field's count at r = 12
(803, section 46) at t ≈ 37; the push a thing reads is the signed sum of
six Port amounts that grow without bound, and its fluctuation is the
circulating trains' (E11: ±10⁴ per interval at a count of 3000). Measured
(the mean field, 33³ periodic, R12 with R13 at period 16, 400 ticks, the
last sixteen ticks): the flux through the cube of half-width 8 is 0.38 q
against the ergodic 0.86 q and through half-width 12 it is −0.26 q
against 0.57 q, the trains swinging every window by ±0.5 q; the push at r
= 8 on the axis is 49 against the open board's 1105, at r = 12 it is 2928
against 267, at (7, 7, 7) it is −1560 against +517; the count at r = 12 is
32 447 against 451. The integer rule adds its own noise on a count that
never stops growing, and a bounded integer per lane (point 25) overflows
in finite time: 2^31 quanta on the board after 2730 intervals at this q.
**No fixed point, no cycle, no bounded orbit, and no reading of 1/r²
within the noise: closed boards are out under emission by this theorem,
not by preference.**

**(iii) What "the standing set a formula can give" (points 11, 13) can and
cannot mean.** It can mean the fixed point of R12 with R14 on an open
board: a stream in balance, in which the amount on the board is the
emission times the transit and the flux through every shell is the
emission; a formula gives it (the resolvent of the one-step map with the
escaping edge at the source's frequency, or the iteration of section 46
run once), and the prefill may write it at tick 0 (section 49). It can
also mean the flat-band content the switch-on leaves beside the thing
(2.2 q at period 16, section 46 (iv)), which stands, has u = 0 (section
39 (ii)) and carries no flux. It cannot mean a stock of X shadows
circulating on a closed board (Theorem 1), a stock passing an open board
(the A6 lane), or a standing 1/r profile (section 37). The phrase "the
size of the shadow set" of the superseded paragraph has no referent left:
what a thing has is a rate, ρ, and what is on the board is what the rate
and the board's transit make of it.

**Check.** Theorem 1 is two lines of algebra on the continuity identity
of section 26 (ii), which the iteration satisfies to 10⁻¹⁴ (section 26's
check); the E11 numbers are quoted from its tables; Theorem 2's numbers
are the `meanfield --periodic` run of the committed script (33³, period
16, `recycle`, 400 ticks, 1.9 s).

**Verdict.** A static 1/r² push from a finite conserved amount: **not
reached on any board, exactly** (the time-mean flux through every shell
is at most X/T, and zero for a fixed point or a cycle). A closed board
with emission: **no fixed point** (the total grows as q t; the 1/r² net
flux survives in the ergodic mean and is buried under a count growing as
q t/V and the trains' ±0.5 q swings; the integers overflow). The standing
set a formula can give: **the open-board fixed point of the stream**, and
nothing given once.

## 46. Round 7: the fixed point of an emitting thing on the open board

**Rules used.** R12, R13, R14, R10, R2, R11, sections 26, 27, 29, 39.

**(i) The edge is a sink for 93 % and a mirror for 7 %.** At an edge Node
one Port has no neighbour: A_p = 0 for that Port, and B_p = u escapes
through it. For a plane wave at normal incidence and long wavelength this
is the transmission-line picture of section 26: the Link line terminated
in its own impedance while the mesh's wave impedance is that impedance
over √3 (six equal Ports in three dimensions), so the wave is reflected
with

```text
R = (√3 − 1)/(√3 + 1) = 0.268 in amplitude,     R² = 0.072 in amount    (normal incidence, k → 0),
```

and more at shorter wavelength and grazing incidence. Measured (a slab of
64 × 4 × 4 Nodes, periodic across, a plane source at x = 2, the open edge
at x = 63, the +x and −x waves fitted on u(x) over x = 8 to 60): R = 0.268
at period 64 (fit residual 0.1 %), 0.273 at period 32, 0.299 at period 16.
The edge is therefore not infinity for the amplitude; it is infinity for
the amount, since what it reflects crosses the board and meets an edge
again (0.07 per encounter): at the fixed point the escape per interval is
the emission exactly (measured 1.000 q). What the 7 % does to the field
inside is (iii).

**(ii) Existence.** On the wave bands (section 27 (iv)) the one-step map
with R14 is a contraction: every packet reaches an edge within 2√3 H
intervals and 93 % of it leaves, so after k crossings 0.07^k remains. On
the flat bands it is not: standing content never reaches the edge, and
whatever the switch-on puts there stays (2.2 q at period 16, (iv)). The
source under R13 is a feedback loop: with ε the fraction of what the
thing's Node sends out that does not come back to it (the radiated
fraction, (iv)) the home amount h obeys h = (1 − ε)(q + h), so h = q (1 −
ε)/ε and the loop converges as (1 − ε)^k over the near field's round trips
of two to four intervals. **The fixed point exists and is unique for the
wave part; the flat part is what the transient left.** It is a fixed
point in the period-mean (the field is a monochromatic wave at the
source's frequency, every amplitude turning with it and every amount and
every J constant in time, section 26 (iii)).

**(iii) The far field: amplitude 1/r, count and push 1/r², and what
modulates them per Node.** For a thing of flux S = q (the emission, by
R13 and continuity: the flux through every shell at the fixed point is
the emission, measured 1.000 ± 0.001 q through the cubes of half-width 2
to 15 on 33³ and 2 to 19 on 41³), the outgoing spherical wave of section
27 (v) with S = q, plus the edge's reflected part:

```text
|u|(r) = 0.2143 √q / r (1 + δ_u),      n(r) = √3 q /(4π r²) (1 + δ_n) = 0.1378 q / r² (1 + δ_n),      J_r(r) = q /(4π r²) (1 + δ_J).
```

Measured at the fixed point in the shell means (all Nodes at r ± 0.5, r =
6 to 16, 33³, period 16, the recycle rule): |u| r/√q = 0.206 to 0.223,
n r²/q = 0.1405 to 0.1520, J_r 4πr²/q = 1.008 to 1.068; on 41³ (r = 6 to
20): 0.207 to 0.222, 0.139 to 0.151, 1.00 to 1.06; at period 32 on 33³:
0.20 to 0.23, 0.142 to 0.155, 1.00 to 1.08. The count's excess of 2 to 10
% over 0.1378 is the reflected wave (R² = 7 %, whose amount adds while
its push subtracts), the push's mean excess of 3 to 5 % the boundary term
of section 26 (ii) (J against Φ, ∝ 2/r). The log-log slope of the shell
means over r = 6 to 16 is −2.00 ± 0.03 for J and for n, and −1.00 ± 0.03
for |u|: **1/r in amplitude and 1/r² in count and push, reached at the
fixed point of the open board, with the flux equal to the emission.**

Per Node the field is modulated, and the modulation is derived, not
noise. Two terms. The fixed anisotropy (15/8) ω₀² K₄(r̂) of section 27 (v):
at period 16 (ω₀ = 0.393) −12 % on an axis and +8 % on (111), at period 32
−3 % and +2 %. And the edge's standing wave: the wave reflected by the
nearest face returns from the distance 2H − r with the relative amplitude

```text
ρ_R = R · r /(2H − r)      (0.04, 0.09, 0.16 at r = 4, 8, 12 for H = 16;   0.03, 0.07, 0.12, 0.18 at r = 4, 8, 12, 16 for H = 20),
```

and two counter-running waves make section 29's mirror pattern: the Port
amounts and J modulated by ±2ρ_R with the period λ_w/2 along the line to
the face (4.6 Links at period 16, 9.2 at period 32), the count nearly flat
(its depth k₀²/6), the amplitude |u| modulated by ±ρ_R. Measured at E11's
Nodes (33³, period 16; J_r 4πr²/q, n r²/q, |u| r/√q):

```text
                 r = 4 (axis)  8      12   |  (3,3,0) (6,6,0) (9,9,0)  |  (2,2,2) (5,5,5) (7,7,7)
J_r 4πr²/q        1.41       1.13   0.61  |   1.05    1.11    0.66    |   0.97    1.12    1.21
n r²/q            0.160      0.158  0.083 |   0.150   0.149   0.099   |   0.147   0.156   0.181
|u| r/√q          0.215      0.251  0.172 |   0.223   0.242   0.134   |   0.228   0.235   0.243
```

(period 32: J_r 4πr²/q = 1.92, 1.06, 1.23 on the axis, 1.14, 1.05, 0.89
on (110), 0.94, 1.06, 0.92 on (111), the axis at r = 4 inside the near
field r < λ_w/2 = 9; 41³ at period 16: 1.43, 0.88, 0.58, 1.18 on the axis
at r = 4, 8, 12, 16). The per-Node push at r = 12 on 33³ is therefore
0.6 to 1.2 of the law by direction, ±40 % as ±2ρ_R = ±32 % says with the
anisotropy on top, and the three-radius log-log fit that E11 makes per
direction reads at the mean-field fixed point −2.76 (axis), −2.43 (110)
and −1.82 (111) at period 16, −2.41, −2.23, −2.02 at period 32: **the
per-direction three-probe fit reads the edge's ripple, not the law; the
law is read in the shell mean** (or along one line at every radius, or on
a board whose edge is matched, section 49). The wave fraction 3|u|²/n is
0.87 to 1.19 at r ≤ 9 and 0.54 to 1.08 at r = 12 to 13: the count is the
square of the amplitude on average over a shell and not at every Node,
the ripple falling on |u| and on n differently (section 29). In the far
field of an unbounded board it would be exact.

**(iv) What the thing radiates, what comes home, and the standing set.**
A single Node emitting into the mesh radiates poorly at long wavelength.
Under absorb-only (the thing's Node absorbs its own arrivals and sends
q/6 per Port, no re-release) the fraction of the emission that becomes
the far flux is

```text
ε(ω₀) = 0.312, 0.094, 0.027 at periods 16, 32, 64        (∝ ω₀^1.8; a point source in the mesh radiates as ω²),   0.004 for a clockless thing,
```

the rest coming back to the Node within a few intervals and being
absorbed there (0.688, 0.906, 0.973 of what it sent). Under absorb-only,
therefore, the force constant would carry the source's clock, G =
ε(ω₀) ρ/(4π), a thing with a faster clock attracting more per quantum,
and a clockless thing not at all: that reading is out. Under R13 (recycle)
what comes home is released again, the thing's Node sends q/ε per
interval and the far flux is exactly q whatever the clock: the home line
carries h = q (1 − ε)/ε = 2.20, 9.60, 36.0 q per interval at periods 16,
32, 64 (measured 2.202, 9.598, 36.02), the flat-band content beside the
thing is 2.16, 9.8, 38 q, and the amount on the board at the fixed point
is

```text
N* = 42.8 q (33³, period 16),   62.8 q (33³, 32),   146 q (33³, 64);     51.5 q (41³, 16),   65.7 q (41³, 32),
```

of which the wave in transit is about 2.11 H q (the mean distance from
the centre to a face of the cube over directions is 1.221 H, at the speed
1/√3: 34 q for H = 16, 42 q for H = 20), the rest the near field within a
wavelength of the thing and the reflected part. **The amount on the board
is bounded by the emission times the transit, plus a standing set beside
the thing that grows with the period of its clock.**

**(v) A clockless thing has a flux and no potential.** E11's body (content
2²⁸ at K = 1 with N = 64: 2²⁸ ≡ 0 mod 64) releases one phase. Under R13 its
fixed point is reached only after about 2700 intervals, with 802 q on the
board (255 q standing, the rest a near field with the axis 12 times the
diagonal at r = 4: J_r 4πr²/q = 12.4 on the axis and 0.89 on (111) at r ≈
4, 2.1 and 0.97 at r ≈ 8.5, the shell means 1.0 to 1.1 from r = 10 on);
the flux is q through every shell (0.975 at t = 3000, still rising), the
count 0.14 to 0.17 q/r² beyond r = 10, and |u| = 0.0122 √q at every Node,
a constant: u is the k = 0 mode, and there is no 1/r potential and
nothing for the wait to read. Under absorb-only a clockless thing radiates
0.4 % of its emission. **The confrontation source must have a clock**, m/K
≢ 0 mod N: for the body of 2²⁸, K = 2²⁶ (four phase steps per interval,
period 16) or K = 2²⁷ (period 32).

**(vi) The transient.** The first tick after which every later
period-mean within radius R stays within the tolerance of the final
state (33³, period 16, recycle, from an empty board):

```text
                              R = 4     R = 8     R = 12    R = 16 (41³)
count within 5 % / 1 %        48 / 96   96 / 192  128 / 208   176 / 256
per-Node push within 5 %      144       208       272         272
flux through every cube within 1 %:  128 (33³), 128 (41³);  within 2 % at h ≤ 8:  48 to 64
```

(41³, period 16: count 1 % at 112, 160, 224, 256; period 32 on 33³:
count 1 % at 224 for every R, push 5 % at 288 to 384). Against √3 H = 28
(33³) and 35 (41³): the flux through the inner shells is the emission
within 2 % by about 2√3 H, the owner's "about L√3", and the amount on the
board is within 1 % of N* at t ≈ 128 (period 16) and 192 (period 32); the
per-Node count and push settle only after the edge's reflection has
crossed the board twice (4√3 H = 110) with the dispersive tails of
section 27 (iii) and the source's feedback on top, at 7 to 10 √3 H. **A
run that reads the fixed point per Node needs about 300 intervals on 33³
and on 41³ from an empty board; one that reads the flux, about 60.**

**(vii) The books at the fixed point.** Per interval: released q + h,
absorbed at home h, escaped q (measured 3.20, 2.20, 1.000 q at period
16): the emission line and the escape line are equal and the home line
closes on itself; the things' line is untouched (R12 costs nothing).

**(viii) The four readings of home, and the one that stands.** Absorb-only:
a fixed point, clean and spherical (n r²/q = 0.046 ± 0.003 at every Node
of 33³ at period 16), but the flux is ε(ω₀) q, (iv): out. Re-release
through the Port the shadow came in, merged coherently with the emission
(the orchestrator's earlier "back out along the line it came home on"):
the flux is q by construction but there is no fixed point in 2000
intervals, the flux through the cubes swinging 0.5 to 1.5 q, the per-Node
push 0.24 to 4.1 of the law, the total drifting from 62 to 67 q, and for a
clockless thing a flux channelled along the body diagonals (J_r 4πr²/q =
7.6 to 9.1 on (111) at r = 8.7 to 12.1 against 0.62 to 0.92 on the axis
after 2000 intervals): out. The linear soft source (an amplitude added to
the mixed outputs, section 27 (v)): the net emitted amount is 0.126 q at
period 16, amount not conserved by construction, no rule of the engine:
out. R13, absorbed and released again with the thing, six-fold, at the
thing's phase: the flux q, a fixed point, spherical in the shell means:
**adopted.**

**(ix) The volume decay, rejected.** The orchestrator's first elaboration,
a sink in the volume with one lifetime λ, was struck by the model owner
the same evening (a shadow is never made to disappear; physics has no
decay of a field in time). For the record, what it would have given, on
paper and not checked by iteration: a uniform decay commutes with the
linear map, so the damped field is the undamped one times (1 − 1/λ)^{t/2}
in amplitude along the flight, the far field of a clocked thing is |u| ∝
e^{−√3 r/(2λ)}/r and n ∝ e^{−√3 r/λ}/r², the reach λ/√3 in the count and
2λ/√3 in the amplitude, the amount on any board q λ exactly, and a
clockless thing acquires a far field of a different law (the k = 0 mode
driven against the damping, n ∝ 1/r⁴, J ∝ 1/r³ inside the reach). None of
it is pursued.

**Check.** All numbers above are the committed script's `meanfield` runs
(33³ and 41³, periods 16, 32, 64 and 0, the variants `recycle`, `absorb`,
`rerelease`, `soft`, 480 to 3000 ticks, 2 to 16 s each), its `edge` run
(the slab) and its `transit` estimate; the flux identity (the escape
equals the emission) holds to 10⁻³ at the fixed point in every recycle
run; the coefficients 0.2143, 0.1378 and 1 are section 27 (v)'s with S =
q.

**Verdict.** The fixed point on the open board: **reached** (unique for
the wave part; the flux through every shell equals the emission; 1/r in
amplitude and 1/r² in count and push in the shell means to ±3 %). The
edge as infinity: **different law** (a mirror for 7 % of the amount, R =
0.268 in amplitude, exact at long wavelength; the fixed point rippled
per Node by ±2 R r/(2H − r), ±32 % at r = 12 on 33³, so that a
three-probe fit per direction reads −1.8 to −2.8). Home: **R13, absorbed
and released again with the thing**, the only reading with a fixed point
and the flux equal to the emission. A clockless thing: **no potential**
(u constant) and a 2700-interval transient. The transient: **about 2√3 H
for the flux, 7 to 10 √3 H per Node.** The amount on the board: **bounded**,
42.8 q on 33³ and 51.5 q on 41³ at period 16.

## 47. Round 7: the fixed point in whole quanta

**Rules used.** R12 to R14 in their integer form; R10's integer rule
(section 30: at each Node the whole quanta arriving are shared over the
Ports as ⌊n_in |B_p|²/Σ|B|² + ρ_p⌋, ρ_p the Node's remainder register for
that Port, the leaving share carrying the phase of B_p rounded to the
circle of N steps); the emission ⌊q/6 + ρ_p⌋ per Port with six registers
on the thing; R13 pooling the home amount with the fresh q before the
six-fold share.

**(i) The emission in whole quanta, and the chain by hand.** A thing of
content M at rate ρ releases ⌊ρM/6 + ρ_p⌋ per Port, the fraction parked
in the thing's register for that Port: for q = ρM = 786 432 = 6 · 2¹⁷ the
release is 2¹⁷ per Port every interval and the registers stay empty; for
q = 5 the six registers each fill by 5/6 per interval and fire five times
in six, so the emission per Port is a cycle of period 6 and the thing
carries up to 5 · 5/6 parked quanta. On a chain (one dimension, two Ports,
S = J − I the swap: every share passes straight, nothing comes home, R13
idle) with the thing at 0 and the ends open at ±L, the shares of the
tick t emission are at ±t after t intervals, so the state at Node x is
the emission of tick t − |x|: the whole chain repeats with the emission's
period (2 for q = 5: 2, 3, 2, 3, … each way; 1 for q even), the amount on
the chain is q L at the cycle (40 for q = 5, L = 8) and the escape q per
interval. **In one dimension the integer fixed point exists exactly, as a
cycle whose period is the emission's, never as a fixed point unless q is
a multiple of the Ports.** The three-dimensional map is deterministic on
bounded integers, so it too is eventually periodic in principle; but the
mean-field fixed point is not an integer state (the six shares of every
Node have fractions at every Port), the registers of 36 000 Nodes and
the phase circle make the period astronomical, and what can be asked is
whether the orbit is bounded and stationary in the reading's windows.

**(ii) The lattice near the source: stationary in the wave, drifting in
the standing content, and the drift is the phase circle's.** The integer
form of the section 46 fixed point (33³, open, period 16, q = 786 432,
R13, N = 64, 1600 intervals): the flux through the cubes of half-width 2
to 15 is 0.999, 0.997, 0.993, 0.990, 0.989 q in the last window; the
push at r = 4, 8, 12 on the axis in 96-interval windows has the standard
deviation over windows 4.6, 3.6, 4.6 % of its mean; the shell means at t
= 400 are n r²/q = 0.17, J_r 4πr²/q = 1.00 to 1.14, |u| r/√q = 0.19 to
0.22 at r = 4 to 14. But the amount on the board does not stop: 42.3 q at
t = 64, 49.9 at 400, 67.9 at 1600, while the registers hold a constant
0.14 q; the excess is standing content (the flat-band amount, total −
3Σ|u|², which the engine can form from the sums it already has):

```text
standing content, q:   2.2 (t = 32)   4.2 (128)   9.4 (400)   16.1 (800)   27.1 (1600)      N = 64:    +1.7 % of q per interval
                       2.2            2.5         3.0         3.4          (3.7 at 800)     N = 256:   +0.17 %
                       2.2            2.3         2.6         2.9                           N = 1024:  +0.08 %
```

(period 32 at N = 64: +2.1 %; four times the quanta, q = 3 145 728 at N =
64: +1.7 %, the same fraction). **The drift is the rounding of the phase
to N steps, not the rounding of the amount**: every leaving share's phase
error of order 2π/(N√12) scatters a part ∝ 1/N² of its amplitude out of
the wave into the flat bands, which never reach an edge and never leave
(section 27 (iv); the escape is a sink for waves only). At N = 64 the
residue is 1.7 to 2.3 % of the emission per interval, forever: over a run
of 400 intervals it is 7 q, 15 to 20 % of the count at the reading radii,
and the per-Node push wanders as it accumulates (the axis at r = 4: 1.23,
1.44, 1.83, 2.14, 1.27 of the law in the windows ending at 100, 400,
1000, 1200, 1600; at r = 12: 0.60, 0.61, 0.43, 0.54, 0.63; (5, 5, 5): 0.85,
1.11, 1.31, 1.36, 1.27), the count at r = 12 rising from 0.08 to 0.21
q/r². At N = 256 the same windows are stationary to three digits (1.41,
1.13, 0.61 on the axis at r = 4, 8, 12 and 1.11, 1.22 at (5, 5, 5), (7,
7, 7), the mean field's 1.41, 1.13, 0.61, 1.12, 1.21) and the push's
window deviation is 0.4 to 0.8 %; at N = 1024 the residue's growth is at
the floor the amount rounding sets. Round 4's table (section 30) read the
push of a plane wave over 500 intervals and found N = 64 lossless; that
is still true of the push of the wave, and what it did not measure is the
standing content the wave sheds, which is not a loss of push but an
addition to the count that no rule removes. **In whole quanta the field
of an emitting thing has a fixed point in the window means at N ≥ 256 and
a drift of 1.7 to 2.3 % of the emission per interval at N = 64.** The
width of the phase circle is the model owner's (Highlights 5.4,
definitions: N = 64, "a wider circle adds no measured precision"); this
is the measured precision it adds, flagged in section 49.

**(iii) Sparse sources: a lone quantum does not travel, and the field of
a small thing is a parked haze.** Under the largest-remainder rule a lone
quantum arriving at a Node is sent back (4/9 against five 1/9), and the
registers it leaves make the next arrival go elsewhere: a rotor walk,
measured over 100 walks of 1024 steps: the mean square displacement is 2
Links² at t = 16 to 64 and 8 at t = 1024, the quantum shuttling within
two or three Links of its start for ever. Under the engine's floor rule a
lone quantum parks at the first Node it reaches (⌊4/9⌋ = 0) until others
arrive. So below one quantum per Port per interval the field neither
propagates as a wave (section 30) nor as a diffusion: it parks, and flows
only as the parked residue primes each Node's registers, the amount
parked within radius r being of order 4πr³ × (2 to 5) quanta. Measured on
the open 33³ board at period 16, R13, 1600 intervals:

```text
q per interval        256                                        64
escape at t = 1600    0.78 q                                     0.12 q
flux through cubes    1.00, 0.99, 0.97, 0.84, 0.79 q (h = 2..15)  1.03, 1.00, 0.91, 0.64, 0.21 q
amount on the board   686 q and rising                           565 q and rising
count n r²/q          1.3, 2.9, 5.8 on the axis at r = 4, 8, 12   3.6, 3.3, 2.4          (the wave: 0.147)
push J_r 4πr²/q       −0.36, −2.4, +4.6 (axis); 2.6, 5.4, −1.0 (110); 3.5, 10.2, 2.6 (111)      4.2, 0.5, 3.8; −3.3, 5.2, 2.6; 3.5, 2.1, 2.6
```

(25³, 1200 intervals: at q = 4096 the flux is 0.99 q through h ≤ 8 and
the shell mean of J_r is 1.06 to 1.16 of the law while the count rises
from 0.25 to 0.74 q/r² between r = 2 and 10 and the per-Node push runs
from −0.5 to +1.6 of the law; at q = 32 768 the shell mean is 1.00 to
1.16, the count 0.23 to 0.30, the per-Node push 0.8 to 1.9.) **For a
source of 256 or of 64 quanta the 1/r² law is not read at r = 4, 8, 12 or
16 in whole quanta for any ρ ≤ 1**: the sign of the push is wrong at one
Node in three, its size off by factors of ten, the count ten to forty
times the wave's and falling as 1/r^0.7, Gauss's flux through a closed
shell equal to the emission only after the residue within it is primed
(about r³ intervals at q = 256, the outer shells not yet at 1600), and
the amount on the board growing without bound at 0.3 to 0.4 q per
interval. The law needs the wave, n ≥ 256 quanta per Node at the reading
radius (section 30): q ≥ 1740 r², that is 2.8·10⁴, 1.1·10⁵, 2.5·10⁵,
4.5·10⁵, 7.0·10⁵ for r = 4, 8, 12, 16, 20; the flux law in the shell mean
holds within 10 to 15 % down to q ≈ 4·10³.

**(iv) ρ for the confrontation runs.** Four constraints. The wave at the
farthest reading radius, q ≥ 1740 r². The amount on the board, N* = 42.8
q (33³, period 16), 62.8 q (33³, 32), 51.5 q (41³, 16), 65.7 q (41³, 32)
plus the residue, within the engine's 4·10⁷: q ≤ 9.3, 6.4, 7.8, 6.1 ·10⁵.
The source's clock, m/K ≢ 0 mod N. And the emission a power of two per
Port, so that the thing's registers stay empty. The choice:

```text
ρ = 3/2048 per interval per quantum of content   (`release` [1, 2048] per Port heading: 2¹⁷ per Port from a body of 2²⁸),   q = 786 432,
period 16 (K = 2²⁶ for the body of 2²⁸ at N = 64; K = 2²⁴ at N = 256),
33³: N* = 3.4·10⁷,  n = 7226, 1806, 803, 452 at r = 4, 8, 12, 16,  J_r = 3912, 978, 435, 245,  |u| = 48.8, 24.4, 16.3, 12.2 quanta^{1/2};
41³: N* = 4.05·10⁷ (at the limit; n(20) = 289, J_r(20) = 156), or `release` [1, 4096] with N* = 2.0·10⁷ and n(20) = 145, the shell means still readable.
```

Period 32 (K = 2²⁷) is the second choice: anisotropy 3 % instead of 12 %
and the ripple's period 9.2 Links instead of 4.6, at the price of a
slower settling (224 to 384 intervals) and a larger standing set (N* =
62.8 q, so `release` [1, 4096] on 33³: 2.5·10⁷, n(12) = 401, n(16) = 226).

**Check.** The chain is arithmetic (the stream 2, 3, 2, 3 and its mean
2.5 checked by the script's emission loop); the lattice numbers are the
committed script's `integer` runs (33³ at N = 64, 256, 1024 and at q =
3 145 728; 25³ at q = 64 to 32 768; 33³ at q = 64 and 256; 11 to 45 s
each) and its `walk` run; the thresholds are section 30's 256 quanta per
Node with the coefficient 0.147 of section 46.

**Verdict.** The integer fixed point: **a cycle in one dimension, exact**;
in three, **reached in the window means at N ≥ 256** (the push stationary
to 0.4 to 0.8 % per 96-interval window, the per-Node values the mean
field's to three digits) and **not reached at N = 64** (a standing residue
growing at 1.7 to 2.3 % of the emission per interval, the count at the
reading radii 15 to 20 % high after 400 intervals and rising, the
per-Node push wandering ±30 %). The 1/r² law for a source of 256 or 64
quanta: **not reached** at any r ≥ 4 and any ρ ≤ 1 (a parked haze;
Gauss's flux only after priming). The rate for the runs: **ρ = 3/2048,
period 16, open 33³ and 41³**.

## 48. Round 7: the tests under the fixed point

**Rules used.** Sections 46 and 47; R4′ (the two readings, point 16); R11
and sections 39 to 41 (the wait reads the amplitude); point 3 as amended
(the return is a field); section 28 (the retardation √3 r); section 19's
algebra for the product laws.

**The dictionary that changes.** A thing of content M has the flux S = ρM
(section 46: the flux through every shell equals the emission). Under the
count reading with the mass reading a thing of content M_B at r takes per
interval M_B J_A = M_B ρ M_A/(4πr²) (1 + δ), δ the per-Node modulation of
section 46 (iii), so

```text
G = ρ /(4π)   in lattice units,      S = 4π G M,      b_c = G M = S/(4π),      r_h = w · 0.2143 √S = w · 0.760 √(G M)   (the amplitude's horizon, section 43),
```

against S = 2πGM in rounds 5 and 6, which counted the recoil half of
rounds 2 to 4 (the return walking home whole). Under point 3 as amended
and R14 the return is a field and the fraction of it that ever reaches its
owner on the open board is f_home = 0.68, 0.16, 0.08 % at r = 4, 8, 12 for
a six-fold return and 0.15, 0.025, 0.013 % for a lone share turned back
(measured by the `home` subcommand on 41³, 300 intervals; about 1.3/(4πr²)
of the return; the rest escapes); so G = (ρ/4π)(1 + f_home) with f_home
below 1 % at r ≥ 4: **the recoil half is gone, and G is the emission rate
over 4π.** Every coefficient of round 6 that carried √S keeps its form
with S = 4πGM: |u| = 0.2143 √S/r = 0.760 √(GM)/r (was 0.537), and GR's
clock coefficient sits at w = 1.316 √(Gm) = 0.371 √(S_m) for a body of
owners of content m (was 1.861 √(Gm) = 0.743 √(S_m)).

**(i) Newton.** F_B = G M_A M_B/r² (1 + δ) r̂, the product law and the
equivalence (the acceleration J_A reads nothing of M_B, point 16):
**unchanged in form**, G = ρ/(4π); **changed** by the loss of the recoil
half (G halves against rounds 5 and 6 at the same ρ), by the per-Node
modulation δ (the anisotropy (15/8)ω₀²K₄, −12 % on an axis at period 16,
and the edge's ripple ±2R r/(2H − r), ±8, 18, 32 % at r = 4, 8, 12 on
33³), and by the requirement of a clock on the source (a clockless thing
has a flux but a 2700-interval transient and a 12-fold anisotropic near
field). **Needs a run**: A5s repeated on the open board, the push on B in
windows against M_B ρ M_A/(4πd²) (1 + δ) with δ from section 46's table,
and the shell mean where the runner can read it.

**(ii) Coulomb.** The charge reading (q_A/M_A) q_B × J_A gives k_C q_A
q_B/r² with k_C = ρ/(4π) = G, the sign as declared, ζ = 1 (J = Φ) in the
shell mean and per Node within the ripple: **unchanged** (section 31's
algebra with S = q). **Needs a run**: A5s with the charge reading, the
product law pp : pq : qq = 1 : 1/2 : 1/4 at one d.

**(iii) The third law.** A's field pushes B by M_B ρ M_A/(4πr²)(1 + δ_B),
B's field pushes A by M_A ρ M_B/(4πr²)(1 + δ_A): with one ρ for the world
the two are equal and opposite in the mean field up to δ_B − δ_A, the
difference of the two Nodes' modulations, which is zero for a pair placed
symmetrically about the board's centre and up to ±2R r/(2H − r) each
otherwise (±30 % at r ≈ 12 on 33³); the recoils add f_home < 1 % and then
leave the board with their momentum (a line in the books: the momentum
that escaped). In whole quanta the two fields are two orbits whose window
means differ by the rounding (4 % per 96-interval window at N = 64, below
1 % at N = 256). **Changed**: from "exact through the return" (section
32) to **the symmetry of the two direct pushes**, exact in the mean field
for one ρ and a symmetric placement, with the edge's ripple as the
remainder for an asymmetric one and the escaped recoil below 1 %. The
books: things + in flight + escaped = 0 at every interval, the escaped
momentum a new line. **Needs a run**: A5s repeated, the push on A against
the push on B per window, and the escaped momentum line.

**(iv) The clock and the redshift (R11).** ρ_eff/ρ = 1 − w|u| with |u| =
0.760 √(GM)/r (1 + δ_u), GR's coefficient at w = 1.316 √(Gm): **unchanged
in form**, **changed** in the coefficient by √2 (S = 4πGM) and by the
ripple δ_u = ±R r/(2H − r) (±4, 9, 16 % at r = 4, 8, 12 on 33³), which a
ring of a few Links' radius averages over its Nodes; the second order
(0 or +x²) unchanged; the standing set beside the source (2.2 q at period
16) has u = 0 and is not read (section 39 (ii)). The redshift z = w c₁ GM
(1/r₁ − 1/r₂) with the same w. **Needs a run**: the three rings of
section 43 in the formula layer, with section 46's fixed point as the
field.

**(v) The bending.** The image GM/b is the path integral of J_⊥ (section
35 (iii)); at the fixed point the integral along lines at impact
parameter b over x ∈ [−H, H], against (S/4π)(2/b) H/√(b² + H²):

```text
b                  3      4      5      6      8      10     12
33³, period 16     1.30   1.17   1.17   1.17   0.96   0.97   0.90
41³, period 16     1.30   1.18   1.15   1.10   0.95   1.01   0.94
33³, period 32     1.70   1.36   1.23   1.15   1.03   1.00   1.11
```

**Changed** at b ≤ 6 by the near field of the source (r ≲ λ_w = 9.2 at
period 16, 18.5 at 32): the image is 17 to 30 % more than GM/b at period
16 and 15 to 70 % at period 32; **unchanged** within ±10 % at b ≥ 8. The
front of light and the field's front: the path sum of |u| against
0.2143√S · 2 asinh(H/b) is 0.998, 0.998, 1.009, 1.031, 0.974, 0.945, 1.074
at b = 3 to 12 on 33³ (0.99 to 1.03 on 41³): **unchanged** within 7 %, the
space half 2GM/b at the GR w as in section 41. **Needs a run**: A6 on 33³
at b = 3 to 8 in the formula layer (the star's S = 4πGM is 20 to 200
quanta per interval for GM = 1.6 to 16, the sparse regime of section 47
(iii), so the star's field is the fixed point of section 46 as a
formula, never whole quanta), the register after the pass against GM/b
times the row above.

**(vi) The Shapiro delay.** The same path sum of |u|, the logarithm cut
at X = H as in section 41: **unchanged** within 7 % on 33³ and 3 % on 41³;
the coefficient half of GR's at the GR w, as before; no screening (the
edge reflects, it does not absorb the amplitude's reach). **Needs a run**:
A6's arrival tick, with the ring for w.

**(vii) The wait of point 23 at a probe.** A probe of content 1 at r = 12
reads 435 quanta per interval at the chosen ρ and never steps: E11's
frozen probe, **unchanged**.

| Test | Under the fixed point of section 46 | Changed by | Run |
| --- | --- | --- | --- |
| Newton, the product law and the equivalence | **unchanged in form**, G = ρ/(4π) | the recoil half lost (G halves at fixed ρ); δ per Node (anisotropy −12 % axis at period 16; ripple ±2R r/(2H − r)); a clock required on the source | A5s repeated, open board |
| Coulomb, k_C = G, the sign, ζ = 1 | **unchanged** | — (ζ = 1 in the shell mean, the ripple per Node) | A5s with the charge reading |
| The third law | **changed**: the symmetry of the two direct pushes; exact in the mean field for one ρ and a symmetric pair | δ_B − δ_A up to ±30 % at r ≈ 12 on 33³ for an asymmetric pair; the recoil f_home < 1 % escapes; 4 % per window at N = 64 (< 1 % at 256) | A5s: the push on A against the push on B; the escaped momentum line |
| The clock and the redshift (R11) | **unchanged in form**; w_GR = 1.316 √(Gm) | S = 4πGM (√2 in the coefficient); the ripple ±R r/(2H − r) in \|u\| | three rings, formula layer |
| The bending, the image | **changed at b ≤ 6** (+17 to +30 % at period 16); unchanged at b ≥ 8 | the source's near field r ≲ λ_w | A6 on 33³, b = 3 to 8, formula layer |
| The bending, the front; Shapiro | **unchanged** within 7 % | the path sum of \|u\| is the 1/r law's | A6 (a two-slit behind the star; the arrival tick) |
| The wait at a probe | **unchanged** | — | E11's probe worlds |

**Check.** The path sums are the `paths` output of the `meanfield` runs
(33³ and 41³ at periods 16 and 32); f_home is the `home` run; the
algebra is sections 19, 31, 39 to 41 with S = q.

**Verdict.** Newton and Coulomb: **reached** in form with G = k_C =
ρ/(4π), the recoil half gone, δ per Node derived. The third law:
**different law** (the symmetry of two fields, with the edge's ripple and
the escaped recoil as remainders). The clock, the redshift, the front and
Shapiro: **unchanged** from round 6 with S = 4πGM. The image at b ≤ 6:
**changed** by the near field, derived per b.

## 49. Round 7: what the emission does to the rest of the law

**Rules used.** R12 to R14, point 7 (the books per bit), point 22 (a
Node is its Ports; parked shadows), point 25 (the lanes), point 3 as
amended, Highlights 5.4's paragraphs on the mark's counter and the
prefill, section 28 (the retardation and the Mach cone), sections 46 and
47.

**(i) The books.** The shadows' ledger carries per interval and per
thing: released, q + h (the fresh emission and the home amount released
again, R12 with R13); home, h; escaped, q at the fixed point; and the
parked remainders, the thing's six emission registers and the Nodes' Port
registers, bounded (0.14 to 0.27 q on 33³ and 41³, section 47 (ii)). At
the fixed point released − home = escaped: **the emission line and the
escape line are equal, the home line closes on itself, and the things'
line is exact and untouched** (R12 costs a thing nothing; a shadow is
never destroyed; what leaves the board is the only loss, as point 22
says). Two lines the books need that they do not have: the standing
content, total − 3Σ_x|u|², which the engine can form from the sums the
mixing already makes and which section 47 (ii) shows growing at N = 64;
and the momentum that escaped, since a return carries the push inverted
and leaves the board with it (section 48 (iii)): things + in flight +
escaped = 0 at every interval is the closed form of the third law under
R14, and the replay check of E11 and A5s must add the escaped line.

**(ii) The prefill as the fixed point at tick 0.** What to write: per
Node and Port the amount and the phase of the mean-field fixed point of
section 46 for the world's q, period and board (the iteration of the
linear map with R12 to R14 for 4√3 H intervals, things held, which the
dense layer can run once before tick 0 as the fill; or the resolvent of
the one-step map at the source's frequency), rounded to whole quanta per
Node and Port with the fractions parked (the second rule of the
superseded paragraph, kept), the thing's six registers empty, the books
opened with the counted content on a prefill line of the shadows'
ledger (released before tick 0). The integer orbit then starts within
its rounding of the fixed point and its standing residue grows from
there as from a cold start (section 47 (ii)). What the prefill saves is
the transient, about 300 intervals on 33³; what it cannot give is a
stationary integer field at N = 64. E11's `initial_field` `{"fill": 12}`
was twelve intervals of emission stopped; under R12 the fill is the
emission itself, and the only sense left to the key is the number of
intervals run before tick 0. A control is forced: the cold start must
reach the prefilled run's window means within the rounding, which is
the test that the prefill is the fixed point and not a profile.

**(iii) A thing born mid-run (E13).** Its emission begins at its birth
from nothing given: the flux at r is within 2 % of the law after √3 r +
about 30 intervals (the source's feedback loop and the dispersive tail),
the per-Node count and push after 7 to 10 √3 H (section 46 (vi)), the
amount on the board rises to N* within about 130 intervals at period 16,
and nothing is orphaned. Its field reaches an observer at r after √3 r,
its light after r to √3 r (section 28), unchanged.

**(iv) A thing absorbed at a mark.** Its emission ends with it. The
amount it left drains through the edge: the wave part is gone to 99 %
after about two transits with the 7 % bounces (110 to 140 intervals on
33³); the flat-band content beside where it stood (2.2 q at period 16)
stays where it is, with u = 0, no flux and no potential, a lawful relic of
the transient. Its shadows that come home find the mark, which is their
home from then on (Highlights 5.4: "the mark becomes the home of that
thing's shadows"): the mark's resident thing, the counter, absorbs them
into its shadow line and, being a thing of content C, releases them
again with its own emission ρC, carrying the absorbed thing's owner
number in its set (point 25: a merged thing carries the numbers of all it
merged). So the counter should hold, per family, the content absorbed on
its real line and what came home on its shadow line, and nothing else;
and the absorbed content's field is not lost but re-sourced from the mark
at once, since the counter's emission grows by ρ times what it absorbed.
The field of a thing that ended fades only in the sense that its source
moved. **Forced by the definitions**; the one alternative, a counter that
does not emit, would take content out of the world's emission at every
click, a screen with no field, which R12 does not allow for matter.

**(v) A moving thing.** A free ray moves at 1 and its field at 1/√3
(section 28): ahead of it nothing arrives, behind it the emission of each
interval spreads from where it was, the Mach cone of half-angle 35.3°.
Its self-field: the forward share of each interval's release, q/6, rides
the lane the thing takes next and is home at the next Node, a round trip
of length zero absorbed and released again (R13), so a moving thing
carries q/6 with it and leaves 5q/6 per interval behind, and nothing of
its field pushes it (the home meeting sums to zero, point 3). A slow
thing (a loop moving by its corners, v ≪ 1/√3) meets its own field at
its Node every interval, h per interval; in uniform motion the field of a
source under the wave equation with speed c_w is the boosted field,
contracted by √(1 − 3v²) along the motion and pointing at the present
position to first order in v, so the home line is symmetric and the
self-push zero; under acceleration the home line is asymmetric by the
lag, a self-force of the field's own, **needs a run** (a loop pushed by
a body: whether its home line pushes back). The field a moving thing
leaves behind is the field of where it was, retarded by √3 r; the field
ahead of a slow thing is the boosted static one.

**(vi) The lanes.** A thing's outgoing lane on each Port carries one
shadow of its number per interval: the release (q + h)/6 in whole quanta
with that Port's register, at the thing's phase (R13 pools the home
amount before the six-fold share, so the lane's sum is one amount and one
phase and no coherent merge is needed on the lane). A share of another
owner arriving at the thing's Node is returned through the Port it came
in on that owner's slot of the same lane (point 3), beside the thing's
own release: two shadows of two owners on one lane, as point 25 allows.
**Forced.**

**(vii) What needs a decision by the model owner, and what is forced.**
Decisions: (1) the width of the phase circle, N = 64 as declared (the
emitted field sheds 1.7 to 2.3 % of the emission per interval into
standing content that never leaves, section 47 (ii)) or N = 256 (the
field stationary to three digits); (2) the edge, plain escape (a mirror
for 7 % of the amount, the fixed point rippled ±2R r/(2H − r) per Node,
section 46 (i)) or a matched edge (an edge Node's table that reflects the
escaping share with the coefficient −R, an engine feature and a declared
thing at the edge); (3) the prefill's form, the fill by iteration or the
resolvent, or none for the first run; (4) whether the escaped momentum
line closes the third law's books or whether the owner wants the recoil
kept on the board. Forced by the derivation: R13 (the only reading of
home with a fixed point and the flux equal to the emission), a clock on
the source (m/K ≢ 0 mod N), the shell mean as the reading of the law,
the emission at no cost to the thing, the mark's counter as the new
source of what it absorbed, G = ρ/(4π), and the confrontation runs on
open boards of 300 intervals or more before the reading.

**Check.** The drain time is the transient of section 46 (vi) read
backward; the boosted field is the wave equation's, section 26 (ii); the
rest is the rules as quoted.

**Verdict.** The books: **exact** on the things' line, **balanced** on
the shadows' line at the fixed point, with two lines to add (the standing
content, the escaped momentum). The prefill: **the fixed point at tick 0,
by iteration**, with a cold-start control. A thing born or absorbed:
**nothing orphaned**, the field re-sourced at the mark. A moving thing:
**the Mach cone and a forward share that rides with it**; the self-force
of a slow accelerated thing **needs a run**.

## 50. Round 7: the verdicts and the run plan

| Claim | Round 7 | Established or needs a run |
| --- | --- | --- |
| A finite amount given once holds a static 1/r² push | **not reached on any board, exactly** (Theorem 1: the time-mean flux through every shell ≤ X/T, zero for a fixed point or a cycle); E11's flat count, ±10⁴ push and 36 to 66 sign changes are the theorem's state | established |
| A closed board with emission and no sink | **no fixed point** (the total grows as q t; the 1/r² net flux survives in the ergodic mean and is buried; the integers overflow) | established; closed boards are out |
| The open-board fixed point of a clocked thing | **reached**: the flux through every shell = the emission (1.000 q); \|u\| = 0.2143 √q/r, n = 0.1378 q/r² (+2 to 10 % from the edge), J_r = q/(4πr²), in the shell means to ±3 %, slope −2.00 ± 0.03 | established (mean field); E11 repeated confirms |
| The edge as infinity | **a mirror for 7 %** (R = 0.268 in amplitude, exact at long wavelength); the field rippled per Node by ±2R r/(2H − r); a three-probe fit per direction reads −1.8 to −2.8 | established; the matched edge is a decision |
| Home | **R13**: absorbed and released again with the thing, six-fold, at its phase; absorb-only gives G ∝ ε(ω₀) = 0.31, 0.09, 0.03 at periods 16, 32, 64; the mirror re-release has no fixed point; the soft source conserves no amount | established |
| A clockless thing | a flux and **no potential** (u constant), a 2700-interval transient, 800 q on the board | established; the source must have a clock |
| The transient | the flux within 2 % by 2√3 H (the owner's L√3); the per-Node count within 1 % by 7√3 H and the push within 5 % by 8 to 10 √3 H: about 300 intervals on 33³ and 41³ | established |
| The amount on the board | **bounded**: 42.8 q (33³), 51.5 q (41³) at period 16; 62.8, 65.7 q at period 32; the wave in transit 2.11 H q | established |
| The integer fixed point | **a cycle in one dimension**; in three, **stationary in the window means at N ≥ 256** (0.4 to 0.8 % per window, the mean field's per-Node values to three digits) and **drifting at N = 64** (standing content +1.7 to 2.3 % of q per interval, the count +15 to 20 % after 400 intervals, the per-Node push ±30 %) | established; N is a decision |
| Sources of 256 and 64 quanta | **no 1/r² at any r ≥ 4 for any ρ ≤ 1** (a parked haze, the sign wrong at one Node in three, the count 10 to 40 times the wave's); the wave needs q ≥ 1740 r² | established |
| ρ for the runs | **3/2048** per interval per quantum (`release` [1, 2048]), period 16, open 33³ and 41³; no λ | chosen |
| Newton, Coulomb | **reached** in form, G = k_C = ρ/(4π), the recoil half gone (f_home < 1 %), δ per Node derived | A5s repeated |
| The third law | **the symmetry of the two direct pushes**; exact for one ρ and a symmetric pair; the ripple difference and the escaped recoil as remainders | A5s repeated, the escaped momentum line |
| The clock, the redshift, the front, Shapiro | **unchanged** from round 6 with S = 4πGM (w_GR = 1.316 √(Gm)); the ripple in \|u\| averaged by a ring | the three rings; A6 |
| The image at b = 3 to 8 | **+17 to +30 % at b ≤ 6** at period 16 (the near field), within 10 % at b = 8 | A6 on 33³, formula layer |
| The books | the shadows' line balanced (released − home = escaped), the things' exact; two lines to add | E11, A5s replays |

**The three runs to make first.** Every world open, the body of the
catalog's `proton` family of content 2²⁸ with a clock (K = 2²⁶ at N = 64:
four phase steps per interval, period 16; K = 2²⁴ if N = 256), `release`
[1, 2048] per Port heading (q = 786 432 per interval), `wait_per_quantum`
1, the dense layer, 400 intervals with the reading over 300 to 400, no
prefill for the first run and the prefill as a second run against it.

1. **E11 repeated with emission** (33³ and 41³, the body alone, then the
   nine probe worlds). Read per interval: the released, home and escaped
   lines; the amount on the board; the standing content total − 3Σ|u|²;
   the flux through the cubes of half-width 4, 8, 12; the shell means of
   n, J_r and |u| at r = 4 to 16 (to 20 on 41³); E11's nine Nodes; the
   wave fraction. **The fixed point is reached** when the flux through
   every cube is within 1 % of q, the escape within 1 % of q, and the
   shell means over ticks 300 to 400 are within 3 % of 0.147 q/r²,
   q/(4πr²) and 0.2143 √q/r with no trend beyond the residue's (at N =
   64: the count rising by 0.017 q per interval in the standing content,
   the push's shell mean not); the per-Node values are then section 46
   (iii)'s table within ±5 % (N = 64) or ±1 % (N = 256), and the probes'
   push per 96-interval window the same table. What decides against the
   derivation: a flux short of q by more than 3 %, a shell-mean slope
   outside −2.00 ± 0.1 at r = 6 to 16, or a standing content growing
   faster than 3 % of q per interval.
2. **A5s repeated** (33³, two bodies of 2²⁸ on the axis at d = 4, 6, 8,
   12 placed symmetrically about the centre, then one pair off-centre,
   then the pairs 2²⁸ : 2²⁷ and 2²⁷ : 2²⁷ at d = 8). Read: the push on
   each body per window against M_B ρ M_A/(4πd²)(1 + δ) with section 46's
   δ, the ratio of the two pushes (1 within 5 % for the symmetric pair;
   the ripple difference for the off-centre one), the product law 1 : 1/2
   : 1/4, and the books with the escaped momentum: bodies + in flight +
   escaped = 0 every interval. What decides against: the two pushes
   unequal by more than the derived ripple, or a product law off by more
   than 10 %.
3. **A6 on 33³** (b = 3 to 8, the star's field the fixed point of section
   46 as a formula with S = 4πGM for GM = 1.6 to 6.4, light things of
   2¹⁸ at speed 1, a ring at r = 8 for w). Read: the register after the
   pass against GM/b times 1.30, 1.17, 1.17, 1.17, 1.05, 0.96 at b = 3 to
   8; the arrival tick against w · 0.2143 √S · 2 asinh(16/b); the ring's
   period against 1 + w · 0.2143 √S/8. What decides against: the image
   outside the derived row by more than 10 % at b ≥ 4.

**λ and ρ.** No λ: a shadow is never made to disappear. ρ = 3/2048 per
interval per quantum of content for the confrontation runs, one rate for
the world, G = ρ/(4π) = 2.33·10⁻⁴ in lattice units; a smaller ρ by a
power of two at the same period trades the wave's margin at r = 16 for
headroom on the board, a longer period trades anisotropy for a larger
standing set and a slower settling.

Open after this round, one line each: the growth of the standing content
in the engine's own integer rule against this document's (the same
apportionment, the same phase rounding, so the same 1.7 % of q per
interval is expected at N = 64, to be read as total − 3Σ|u|²); the
matched edge (an edge table with the coefficient −R) and what it does to
the ripple; the reflection of the edge at oblique incidence and the
corners; the self-force of an accelerated slow thing through its home
line; the near-field correction to the image at b ≤ 6 derived in closed
form (the reactive field of a point source in the mesh); and the
radiated fraction ε(ω₀) of a point source in closed form (measured
∝ ω₀^1.8).

## 51. Round 8: the law of the shadow in points, a draft for the model owner

Round 8 (2026-09-18, the evening, after PR #323) takes the model owner's
decision of the same evening (Highlights 5.4, "The law of the shadow: only
shadows and events"): "No real and shadow. There is only shadow. There are
events, which are a whole quantum. That is all. The shadow spreads like a
ray from the event." This section writes the law as points, the
mathematician's draft for the owner to keep or strike point by point,
each with what today's engine already has and what is new; sections 52 to
55 derive its consequences on the fixed point of round 7 (sections 46 to
49, cited and not repeated); section 56 gives the verdicts, the smallest
engine that implements the law, and the first three worlds to run on it.
As in every round: bottom-up from the stated rules, no physics assumed,
no engine run, no edit to the engine; the numbers of sections 52 to 54
come from `tools/derivations_round8.py` (committed, an iteration of the
stated rules on a box of 41³ to 129 × 41² Nodes, seconds to a minute
each), cited after each derivation and never used as its source. Nothing
below is a decision: every point is the orchestrator's and the
mathematician's reading of the owner's words, flagged as such, and the
owner's sentence outranks it wherever they differ.

**Two words fixed first, since the owner's "quantum" carries both.** A
*unit* is one quantum of amount, the integer the books count and the
mixing shares (section 30). The *quantum of a family*, q_F, is the whole
number of units every held content of that family is a multiple of
(Highlights 5.4, definitions, "its quantum, of which every thing of it is
a whole multiple"); for light it is the amount a quantum was born with,
carried as its message. The owner's "an event is a whole quantum" is read
below as: a whole unit arriving at held content is an event, and a whole
q_F assembled at held content is the event a table acts on (a click, a
capture, a step). Where the two differ the text says which.

**S1. The objects.** (a) A Node is its six Ports and nothing else (point
22). On every Port, per family, per number and per sign, the shadows that
arrived in the interval: an amount in units, a phase on the circle of N
steps, the heading (the Port), and the message (the emitter's content and
its whole charge; for light, the birth amount). A shadow carries no bit,
no momentum, no step count and no owner beyond its number. Below one unit
it is parked at the Node in ninths (point 22). (b) Held content: at a
Node, per family, a content M in units (a whole multiple of q_F), a
momentum p ∈ ℤ³ with three accumulators, a phase φ, the set of numbers it
carries (one at birth, all of them after a merge, point 25), a wait
counter, and the family's declared tables (what it does with each family
that arrives, what it emits, when it breaks). Matter is held content and
nothing else; light is never held longer than a table says (S5). *The
engine has*: (a) is the dense layer's arrays per family, owner and sign
with the parked ninths (`reg`), less the flow axis and the momentum arrays
of return-field-v1 and less the bit of bit-law-v1; (b) is the external
body (content, momentum with its accumulators, phase, `momentum_table`),
the mark's resident thing (content per family, momentum, owners, the
`on_click` table) and the stock of a source, which are three objects
today. *New*: one object, held content, in place of the three; no ray of
bit 1 anywhere; no momentum on a ray.

**S2. The interval.** In this order, at every Node, every interval:

1. *Move.* What left through a Port in interval t is at the neighbour at
   the end of t and is that Node's arrival in t + 1 (R2); through a Port
   with no Node beyond it, it escapes and is booked (R14).
2. *Mix.* At a Node holding no content of the arriving family, the six
   arrivals of one number are one coherent sum and leave by S = J/3 − I,
   the amounts shared in whole units by |B_p|², the ninths parked, each
   share at the phase of its sum (R10, section 26; the integer rule of
   section 30); shadows of different numbers are mixed apart and counted
   together. Nothing is declared here and no event happens.
3. *Absorb.* At a Node holding content of family F, every whole unit of
   family G arriving in the interval, and every parked share of G that
   reaches a unit there, is an event: it is absorbed by F's table for G.
   The table has two entries, the push (S3) and the fate of the amount:
   *re-released* (the default for the free families, the matter shadows
   read as gravity and electricity: the unit joins this interval's release
   of the holder, S2.4, and its number and phase are gone), *kept* (light
   absorbed: the unit joins M, paid, a click when the holder is a mark
   that counts, S6) or *passed* (the table says pass: the unit is mixed as
   at an empty Node and the holder is not pushed). What arrives with the
   holder's own number is absorbed like the rest for its amount (re-
   released, section 52 shows it must be) and, by the reading of section
   54, for nothing else.
4. *Release.* The holder releases, in this interval, ρM units of its own
   family plus every unit re-released in S2.3, one sixth through each Port
   with a remainder per Port (six parked shadows of its own number, R12
   with R13, section 46 (viii)), every share at the holder's phase of this
   interval, with the holder's numbers and its message. ρ is one rate for
   the world (section 52 (iv): not per family). The release costs the
   holder nothing. What its emission table says of light is released
   beside it, paid from M (S5).
5. *The clock.* φ advances by M/K steps of N, K one for the world (point
   19), in every interval the holder does not wait.
6. *The wait.* The holder reads Σ_j |u_j| over the numbers at its Node
   that are not its own, |u_j| the size of the coherent sum of number j's
   six arrivals (R11, section 39), and owes w intervals per whole unit of
   it, the fraction kept on the counter; in an interval it owes, it does
   not release, does not advance its phase and does not step. A quantum
   of light in flight pays the same at every Node it crosses (S5).
7. *The step.* Each accumulator adds its component of p; when one reaches
   M the whole content is released through that Port as a ray of amount M
   carrying its record (p less M on that axis, φ, the numbers, the wait
   counter) and is held at the neighbour on arrival: a release and an
   absorption, one Link, no walk (section 53 for the timing and the bound).

*The engine has*: 1, 2 and the parked shares exactly (node-mixing-v1,
node-is-ports-v1, lanes-v1, dense-field-v1); the accumulator step of the
external body (external-body-v1, "motion by fields only"); the wait
counter of clock-readings-v1 and the amplitude of wait-reads-v1 (per group
at the thing's Node, floored per interval; section 42 says what its
remainder must do); the absorption into a counter of detector-absorb-v1
and the resident thing. *New*: the release from held content every
interval (R12, feature 19, not on `main`), the re-release of every
absorbed unit at the holder's phase (R13 for every family, not only home),
the absence of any return (return-field-v1 retired: no share ever turns
back at a holder; it is absorbed and re-emitted), the step as a release
and an absorption, and the wait of a quantum in flight (a hold per Node
per family, section 55 (v)).

**S3. The readings (point 16 as amended, unchanged in content).** A
whole unit of amount a with heading h (h = −e_p for an arrival through
Port p) absorbed by held content of family F, content M, whole charge q,
from a message of content M_A and whole charge q_A:

```text
gravity:      Δp = − M · a h                        (toward the emitter; the equivalence: a = F/M reads nothing of M),
electricity:  Δp = + (q_A / M_A) · q · a h          (like charges apart; nothing of M),
light:        Δp = + a h,  M ← M + a                (absorbed whole; a click where the holder counts),
```

the two free readings applied to the same unit of a matter shadow; the
cross-section is the content for gravity and the whole charge for
electricity, as point 16 says, and the message carries q_A/M_A. The wait
reads the size, not the amount (S2.6). *The engine has*: both readings
(clock-readings-v1's `push_of`, charge-per-thing-v1); the amplitude
(wait-reads-v1). *New*: nothing in the readings; only that the unit is
absorbed after being read, never turned back.

**S4. The number.** Every held content gets one number at its birth and
stamps it on what it releases; a merge carries the numbers of both; a
unit absorbed and re-released leaves with the holder's numbers and phase,
its own gone: coherence is the last emitter, nothing inherits, nothing is
orphaned (a field whose source ended is re-sourced from wherever its
units are next absorbed, section 49 (iv)). The Node reads the number in
one place only: which arrivals are one coherent sum (S2.2, S2.6). There is
no home: the holder's own number is one number among those it absorbs
(S2.3), and what "home" named is section 52's balance. *The engine has*:
the owner axis of the dense layer, the owners set of the resident thing.
*New*: no home rule, no route, no owner on a returning share.

**S5. Light.** A paid family: a held content releases it only by its
emission table, spending its content (a lamp burns, a transition emits
a = ΔM at the change of the emitter's rate, section 18); it is absorbed
only by a table, into content (a click, a capture, the photoelectric
table of section 55 (vii)), or passed. In flight it is a shadow like every
other: it spreads by the mixing at the field's speed 1/√3, its phase
stamped at release and rotating by its message over K per interval, which
is a uniform rotation of the whole field of that message and changes no
amount and no fringe (section 52 (v)); its message is its birth amount
a = q_γ, and a whole q_γ assembled at a holder by the remainder rule, per
number, is the event a light table acts on: one absorption per quantum.
It pays the wait at every Node it crosses (S2.6), so light in a
potential has an index (section 55 (v)). *The engine has*: the light
family as a wave-ray family, the funded emission of a source, the click
as an absorption into the counter. *New*: light as a spreading shadow
with a message, never a ray on one path; the quantum q_γ assembled by the
remainder rule per number; the wait in flight.

**S6. The mark.** Held content whose table for a family says *kept* and
counts: a screen is matter, its count is content, a click is the
absorption of a whole quantum (q_γ of light; the whole content of a
matter content that steps into it), and a mark that misses is a table
(*passed* one arrival in d). It is pushed by what it absorbs and slowed by
what it reads like every holder, and it re-releases the free shadows it
absorbs like every holder. There is no draw and nothing returns from a
mark. *The engine has*: the mark with its resident thing and its
`on_click` table (detector-absorb-v1, node-is-ports-v1, feature 16h's
retirement of the mark's exception). *New*: nothing but the absence of the
return.

**S7. The open edge.** The board's edge is infinity: a share sent through
a Port with no Node beyond escapes and is booked (R14); it reflects 7 % of
the amount as a mirror does (section 46 (i)), which the reading of the
law in shell means tolerates and a matched edge would remove (section 49
(vii)). No world of a confrontation is closed (Theorem 2, section 45).
*The engine has*: the open boundary of the dense layer. *New*: the closed
board and the prefill as a stock are retired; the prefill survives only
as the fixed point written at tick 0 (section 49 (ii)).

**S8. The books.** Per family and per interval: held (the contents),
in flight, parked, released (free, R12 and the re-releases), escaped, and
the paid lines of light (emitted from content, absorbed into content);
held + in flight + parked = Σ released − Σ escaped + the paid lines, exact
in units at every interval. Charge lives on held content alone and every
table conserves it. Momentum lives on held content alone and changes only
by the pushes; no ledger of the field's momentum exists (S1: a shadow
carries none; section 26: the mixing conserves no signed flux), so the
third law is not a ledger identity but the symmetry of the two fixed
points, section 55 (ii), and the sum of the held momenta is constant only
in the steady state and only for one ρ. Point 7's "the books are kept per
bit" is retired with the bit. *The engine has*: the ledger per family and
per bit, the escaped line, the audit. *New*: one bit, hence one ledger
per family; the momentum lines of the shadows retired; the released line
of R12.

**S9. What is random.** Nothing. What a mark does not know is which
number's units and how many arrive in the interval; the remainder rule
decides which Node of a screen reaches a whole quantum first; the only
uncertainty in the model is the observer's (point 8), and Bell's bound is
section 55 (ix).

**S10. Retired with the bit.** The bit and its inheritance; the return
(a shadow turned back at a meeting, its −Δp and its momentum arrays); the
trace and the step count; home as a rule (it is R13's re-release of one
number among all); the walk back of a missed thing; the draw and the
ticket seed; the per-family phase width; the closed board and the prefill
as a stock; "a thing has one path" (nothing has a path: a held content is
at one Node and steps, a quantum in flight is everywhere its amplitude
is). Kept from the law of the bit: the mixing (24), the lanes (25), the
remainder rule (22), the readings (16, 18), charge per thing (16 as
amended), the clock as content over K (19), the wait reading the size
(23 as amended), the step by the accumulator (21, read as section 53), the
label as coherence, the emission (R12), the open board (R14), the mark's
counter as content.

| What the engine has today | Under the law of the shadow |
| --- | --- |
| Rays of bit 1 (things) and bit 0 (shadows), one path per thing | shadows only; held content at Nodes; no path |
| The external body, the mark's resident thing, a source's stock | one object: held content (S1 (b)) |
| The dense layer's arrays per family, owner, sign, flow, with momentum | the same arrays without the flow axis and without momentum |
| The parked ninths, the largest-remainder mixing (node-mixing-v1) | unchanged (S2.2) |
| The prefill as a stock (`initial_field` fill) | the fixed point at tick 0 at most (S7) |
| The return with −Δp (return-field-v1) | none: absorbed and re-released (S2.3, S2.4) |
| Home: absorbed and re-released with the thing | one number among all in S2.3 and S2.4; no rule |
| The wait counter on the thing (clock-readings-v1), the amplitude (wait-reads-v1, floored) | the counter with a remainder, reading Σ_j\|u_j\| over other numbers (S2.6); a hold per Node for light in flight |
| The accumulator step of the external body | the step of every held content, as a release and an absorption (S2.7, section 53) |
| The click as an absorption into the counter | the same, of a whole q_γ assembled by the remainder rule per number (S5, S6) |
| The emission (feature 19, not on `main`) | R12 for every held content, R13 for every absorbed unit (S2.4) |
| The ledger per family and per bit | per family; the released and escaped lines; no field momentum (S8) |

**Verdict.** The law as points: **stated** (S1 to S10), with two words
fixed (unit, q_F), one order of operations (S2), and the flags: the
absorption of the holder's own number for amount only (section 52 and
54), the step's timing (section 53), one ρ (section 52 (iv)), the wait of
light in flight as a hold per Node (section 55 (v)), and q_γ as the
message of light (S5, section 55 (vi) and (vii)).

## 52. Round 8: a held content is stable; the balance in integers, one ρ, the rotation in flight, and the sparse source

**Rules used.** R12, R13, R14 (section 45), R10 (section 26), S2 to S5 of
section 51; the fixed point of section 46 ((iv), (v), (vii)), the integer
form of section 47 ((i), (iii)); point 16 as amended, point 25 (the lanes).

**(i) The balance, and why home must be a no-op for the amount.** At the
fixed point of the open board a held content of content M releases q + h
units per interval, absorbs h at its own Node and the edge takes q, with
q = ρM the emission and h = q (1 − ε)/ε the home amount, ε(ω′) the
fraction of what the Node sends that never comes back (section 46 (iv):
ε = 0.312, 0.094, 0.027 at the periods 16, 32, 64 of the holder's clock,
0.004 for a clockless holder; h = 2.20, 9.60, 36.0, 250 q). The first
reflection alone returns four ninths of every share after two intervals
(section 26 (i)); the rest of h is the later returns of the near field.
Three things a Node could do with a unit that arrives with its own number,
and what each does to M:

```text
re-released (R13, S2.3 and S2.4):   M(t + 1) = M(t) exactly;  the flux through every shell q;  nothing lost.       kept.
kept (added to M):                  M(t + 1) = M(t) + h(t) = M(t)(1 + 2.20 ρ)  at period 16:  +0.32 % per interval at ρ = 3/2048
                                    (doubling in 215 intervals); +5.3 % at period 64; +37 % for a clockless holder.        out.
destroyed:                          M constant, but the flux is ε q (section 46 (iv), absorb-only: G ∝ ε(ω′)) and a shadow
                                    disappears, which the owner forbids.                                                   out.
```

So a held content at rest on the open board neither evaporates (no unit
of a free family ever leaves M: R12 costs nothing) nor grows (no unit of
a free family ever enters M: every one is re-released), **exactly, in
integers, at every interval**, and the only reading of home that gives
this together with a flux equal to the emission is the re-release. What
arrives with another number is re-released the same way (S2.3), so the
holder's flux out is q + c, c the cross amount it absorbs: the field of A
is partly re-sourced as B's, by c/q_B = 0.138 q_A/(d² q_B), below 1 % at
d ≥ 4 for equal contents. In whole units the release is ⌊(q + h + c)/6 +
ρ_p⌋ per Port with six registers on the holder (section 47 (i)), the
arrivals are whole units with the ninths parked at the holder's Node and
absorbed when they reach a unit, and M is untouched by any of it. In an
interval the holder owes (S2.6) it releases nothing, so its flux in the
mean is q (1 − w|u|), and the balance closes in the mean as before
(released − home = escaped). Only the paid lines of light change M, by a
table: a lamp burns and a screen fills by design, and a matter content
with no light table is constant for ever. **Reached exactly.**

**(ii) The near field must stay below the family's quantum: a bound on ρ.**
Under S2.7 a share of amount at least q_F arriving on one lane is held as
content (that is how a stepping content is held at its neighbour with no
bit to say so). The largest share on any lane of the board is the
holder's own release through one Port, (q + h)/6 = ρM/(6ε); for it to
stay below q_F = M (the holder's own quantum, the smallest it can be),

```text
ρ < 6 ε(ω′) = 1.87, 0.56, 0.16 at periods 16, 32, 64,  and 0.024 for a clockless holder;     ρ = 3/2048 is below all four.
```

Above the bound the holder's own field would condense into a second held
content at its neighbour every interval, carrying the family's charge
from nothing; a world above it is refused. **New**: the rate has an upper
bound set by the family's quantum and the holder's clock, and a clockless
holder's is forty times the smallest.

**(iii) Neither per family nor per thing: one ρ.** A's field pushes B by
ε_g M_B ρ_A M_A/(4πd²) and B's pushes A by ε_g M_A ρ_B M_B/(4πd²) (section
48 (iii), with the gravity reading's multiplier ε_g of section 55 (x)
carried along); they are equal and opposite only if ρ_A = ρ_B, and the
charge reading gives the same condition. A rate per family would break
the third law between families by ρ_A/ρ_B and make Newton's constant a
property of the pair. **ρ is one rate for the world, as K and N are**;
what a lamp releases is not ρ but its emission table, paid (S5).

**(iv) The rotation in flight is a gauge, and the wave's number is a
difference of two rates.** Let every share advance its phase by δ per
Link (S5: a quantum rotates by its message over K). Then A_p(x, t + 1) =
e^{iδ} B_{opp}(x + e_p, t), and Ã = e^{−iδt} A obeys the plain map of
section 26: the whole field of one rate class turns uniformly, no amount,
no push and no fringe within the class changes. A holder stamping its
phase at ω = 2πM/(KN) per interval drives, in the tilde frame, the source
of section 27 (v) at

```text
ω′ = ω − δ:      the flux q at every ω′ (R13);   the potential |u| = 0.2143 √q / r only for ω′ ≢ 0;   λ_w = 2π / k(ω′);   h = q (1 − ε(ω′)) / ε(ω′).
```

If a matter shadow rotated at its holder's own rate (the message's
content over K), ω′ = 0 for every held content: a flux with no
potential, u constant, a 2700-interval transient and 800 q on the board
(section 46 (v)), and nothing for the wait to read near any mass: out.
If it rotates by one unit's amount over K (light's rule read for a unit)
or not at all (round 7, the engine's shadows), ω′ = (M − 1)/K or M/K and
the field is section 27 (v)'s. For light, the lamp's stamping rate M_L/K
and the quantum's rotation q_γ/K give ω′ = (M_L − q_γ)/K on the board, while
the frequency read at any Node in the lattice frame is the lamp's M_L/K
(the field is linear and time-invariant); Planck's relation is section
18's beat, unchanged. **Flagged for the owner**: a matter shadow's
rotation in flight must not be its holder's clock; the derivation below
takes the engine's reading (no rotation, ω′ = M/K).

**(v) A held content at rest: the field of a big one and of a small one.**
Section 47 (iii) is the fact that matters most under the law of the
shadow, since matter is now held content and nothing else: the field of
a holder is a wave, with the 1/r² push and the 1/r potential, only where
the count is at least about 256 units per Node per interval, q ≥ 1740 r²;
below that it is a parked haze that primes outward at about r³/q
intervals, with the sign of the per-Node push wrong at one Node in three
and no 1/r² at any r ≥ 4 for a source of 256 or 64 units per interval at
any ρ ≤ 1. What this means:

- *An electron of tens of units has no field beyond its own Node.* At
  ρ = 3/2048 a content of 32 emits 0.047 units per interval, one unit
  every 21 intervals, which parks at the first Node it reaches; at ρ = 1
  it emits 32 per interval, a wave to r = 0.14 Links. Its push on a
  partner at r ≥ 4 is not 1/r² in any window; in the long-time mean the
  flux through a closed shell around it equals q by continuity once the
  haze inside is primed (about r³/q intervals: 10⁴ intervals at r = 4 and
  q = 1), so the shell-and-time mean of the push is q/(4πr²), and per Node
  it is noise. The E8 and A8 worlds of an electron of 32 and a proton of
  64 cannot confront Coulomb under this law.
- *Nature's electron is not a sparse source in these units.* The
  electric-to-gravitational ratio in lattice units is Q_AQ_B/(ε_g M_AM_B)
  (section 55 (x)); at ε_g = 1 nature's 4.2·10⁴² for two electrons puts the
  electron's charge at 2·10²¹ times its content in units, and at any ε_g
  the unit of amount is set by G through ρ. The content of a thing in
  units is a number of the world the owner has not fixed (section 10);
  what this round fixes is the condition for its field to be a wave at
  the radii of interest: M ≥ 1740 r²/ρ.
- *For a run the content must be raised, not ρ*: a wave at r = 8 needs
  q ≥ 1.1·10⁵, that is M ≥ 7.6·10⁷ at ρ = 3/2048 or M ≥ 1.1·10⁵ at ρ = 1
  (the bound of (ii) allows ρ = 1 at period 16), and the board holds 42.8 q
  = 4.7·10⁶ units at the fixed point in either case. The proton of 2²⁸ of
  E11 and A5s is a wave source to r = 21 at ρ = 3/2048; the electron of
  a run must be of the same order to have a field at all.
- *The two-slit lamp and the Bell source* must release light quanta whose
  amount is a wave at the screen: q_γ ≥ 1740 r² with r the lamp-to-screen
  distance (r ≈ 34 for A1's L = 24 and half-width 24: q_γ ≥ 2·10⁶ units
  per quantum, a lamp of 2²² holding two of them, one of 2³¹ a thousand);
  a quantum of 4 units, A1's photon, is a haze at the wall and never a
  fringe. What a screen then counts is section 55 (vi).

**Check.** (i) and (ii) are arithmetic on section 46 (iv)'s ε and h; (iii)
is section 48 (iii)'s algebra; (iv) is the substitution Ã = e^{−iδt}A in
the map of section 26 (ii), an identity; (v) quotes section 47 (iii).

**Verdict.** The stability of a held content: **reached exactly** (M
constant at every interval under the re-release; the kept reading grows
by 2.2 ρ per interval, the destroying one is forbidden). Home as a no-op
for the amount: **forced**. The bound ρ < 6 ε(ω′): **new**. One ρ for the
world: **forced** by the third law. The rotation in flight: **a gauge**;
the holder's shadows must not rotate at the holder's clock (**flagged**).
The field of a small content: **a haze, no 1/r² in any window** (section
47 (iii)); the electron of a run must carry M ≥ 1740 r²/ρ, and the lamps
of A1 and A2 must release quanta of q_γ ≥ 1740 r².

## 53. Round 8: the step and the speed of a held content

**Rules used.** S2.7 of section 51 (the step as a release and an
absorption), point 21 and the five settled rules' (i), section 3 (the
accumulator of the external body), point 25 (one ray per lane), section
26 (iii) (the field's group speed ≤ 1/√3 in every direction), section 27
(iii) (the front by direction), S2.6 (a waiting interval has no step).

**(i) Two readings of point 21 for a held content, and the trap.** Point
21 was written for a ray that moves one Link every interval and turns
when a component of its momentum reaches its content; for held content
the same words admit two readings. *The accumulator* (external-body-v1,
section 3): every interval each axis accumulator adds p_i; when one
reaches M the content steps through that Port and the accumulator gives
back M; p is untouched. Then x_i(t) = p_i t/M to within one Link, v =
p/M exactly, uniform hopping at constant p: **Newton's first law by
bookkeeping**, and dp/dt = F with the pushes of S3, Newton's second. *The
literal drop* ("the momentum drops by that content"): a content with
|p_i| < M never moves, one with p_i ≥ M steps once and keeps p_i − M;
motion needs a force in every interval and stops with it, v = F/M per
interval, Aristotle's law. The first reading is the one below, the
owner's "drops by that content" being the accumulator's giving back M as
the engine does today; the second is stated so that it is not written by
accident.

**(ii) The step, and the ray that carries it.** When an accumulator
reaches M the whole content leaves through that Port as one share of
amount M on the lane, at the holder's phase, with its numbers, its
message, its momentum, its remaining wait and its two other accumulators
riding with it; it arrives at the neighbour at the end of the interval
and is held there: by S2.7 a share of amount at least q_F arriving on one
lane is content and is never mixed (section 52 (ii) keeps every field
share below q_F for ρ < 6ε). It is the one ray with a momentum on it, and
it needs no bit: its amount says what it is. A neighbour that already
holds content of the family merges it (point 25: the amounts add, the
phase is the coherent sum's, the momenta and charges add, the numbers are
kept as a set); one of another family meets it by the pair's table
(section 5.2). **Forced by S1 and S2**, up to the record riding on the
share, which is the orchestrator's elaboration.

**(iii) The timing, and the bound on the speed.** Under S2's order the
neighbour absorbs the arriving content in step 3 of the next interval and
may step it again in step 7 of the same interval, so a content whose
accumulator is full moves one Link every interval: the timing T1,
|v|₁ ≤ 1. Under the reading that an event occupies its interval (the
absorption in step 3 ends the content's interval as a wait does, S2.6,
and the mixing at an empty Node occupies nothing, point 15: computation
is the events), the content released in interval t is held at the
neighbour from the end of t, absorbed as the event of t + 1, and steps
first in t + 2: the timing T2, |v|₁ ≤ 1/2. The two against the field's
front, which moves at 1/√3 = 0.577 Links per interval in every
direction (section 26 (iii)), in Euclidean Links per interval:

```text
direction          matter, T1        matter, T2        the field's front     T1 / field     T2 / field
axis (100)         1.000             0.500             0.577                 1.73           0.87
diagonal (110)     0.707             0.354             0.577                 1.22           0.61
body (111)         0.577             0.289             0.577                 1.00           0.50
```

Under T1 a full content outruns its field on an axis and on (110) and
keeps pace with it on (111) (the Mach cone of section 28 for held
content, 35° behind it); under T2 it is slower than its field in every
direction, by 0.87 on an axis and 0.50 on (111), and the field's front,
sharp on (111) and smeared on the axes (section 27 (iii)), always
precedes it. The lattice gives no timing under which the two speeds
coincide: matter's bound is an L1 bound (one lane, one Link, one
interval) and the field's is Euclidean and isotropic at long wavelength;
"light and matter share one c" is not available on this lattice exactly,
and T2 is the reading under which nothing outruns the field. **T2 is the
reading taken below and flagged for the owner**: an event takes the
interval; the mixing takes none.

**(iv) Beyond the cap.** Under T2 the accumulator can be served at most
once in two intervals, so a content with p_i > M/2 (T1: p_i > M) moves at
the cap and its accumulator is held at M until the next step is allowed;
p itself keeps every push it takes. So

```text
v_i = min(p_i / M, 1/2)   (T2;  1 under T1),      p unbounded, v bounded:
```

a kinematics in which the momentum grows without bound while the speed
saturates at the lattice's c_m = 1/2, against nature's v = p/√(p² + M²)
with c: **different law** in the form of the saturation, the same in its
existence. A content falling from rest at infinity has v² = 2GM_A/r
(dp/dt = F and v = p/M, section 11 (b)), so it reaches the cap at
r = 8 G M_A and inside that radius its momentum keeps growing at the
capped speed: section 11 (b)'s dark body, its radius now 8GM.

**(v) The speed in a potential.** In an interval the holder owes (S2.6)
nothing of it advances: no phase step, no accumulator, no release. So a
held content of momentum p at a Node where it reads |u| moves at

```text
v = (p / M) (1 − w |u|)   Links per interval,      0 at r_h = w · 0.760 √(G M) (section 48),
```

round 3 (iv)'s slowing of a free thing, now for held content and in the
potential's form; its momentum still integrates the push at the full
rate, so it gains p while it moves slower, as there. **Reached** in form
(the frozen-star coordinate speed 1 − 2GM/r of the Schwarzschild metric
has the same shape with a coefficient 2 against 1 at the GR w, as the
clock's second order has, section 40).

**(vi) Light.** A quantum of light in flight is a wave of the mixing: its
front moves at 1/√3, never at 1 (section 26 (iii): no signal of the
mixed field outruns 1/√3 at any wavelength, exact), sharp on the body
diagonals and smeared on the axes (section 27 (iii)), and in a potential
at 1/(√3 (1 + w|u|)) (section 55 (v)). What the runs of the law of the
bit measured as light at speed 1 (the light thing on its one path) has no
counterpart here.

**Check.** The table is arithmetic on the L1 step and section 26 (iii)'s
bound; (i) is section 3's derivation; (iv) and (v) follow from S2.6 and
S2.7 as stated.

**Verdict.** The step: **forced** as a release and an absorption, the
record riding on one share of amount M (flagged). The speed: v = p/M by
the accumulator, **Newton's first law by bookkeeping** (the literal drop
would be Aristotle's, stated and not adopted); the bound **1/2 on an
axis and 0.29 on (111) under T2**, below the field's 1/√3 in every
direction; **1 under T1**, above it on the axes (T2 taken, flagged).
Beyond the cap: **different law** (p unbounded, v saturated). In a
potential: v = (p/M)(1 − w|u|), **reached** in form.
