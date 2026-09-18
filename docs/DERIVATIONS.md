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
known physics. The summary table is [section 15](#15-the-verdicts-in-one-table-round-1-see-section-21-for-round-2); round 2 (sections 17 to 21, the model owner's points 16 to 21 of 2026-09-18) is summarized in [section 21](#21-round-2-the-verdicts-that-change-and-those-that-stand); round 3 (sections 22 to 25: Boss's vectorial steering rule and phase-reading push of 2026-09-18, verified, and the wait of point 23, PR #278) is summarized in [section 25](#25-round-3-the-verdicts); round 4 (sections 26 to 33: the model owner's point 24 of 2026-09-18, the Node mixes the six, derived as an operator and verified) is summarized in [section 33](#33-round-4-the-verdicts).

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
