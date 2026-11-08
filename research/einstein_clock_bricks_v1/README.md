# Universe24: exact clock-and-gravity prerequisites (all 48 channels)

**Status (2026-11-08): rigorous restricted results, NOT an Einstein-gravity derivation.** These are genuine algebraic/reproducible ingredients for testing a clock-based emergence of spacetime. They do **not** establish physical mass, energy, universal gravitational redshift, a Lorentzian metric, curvature, or the Einstein field equations.

The reference model is unchanged: 48 `2O` channels at every site, two unbounded integers `(a,b)` and one remainder `r∈{0,...,5}` per channel; six reciprocal spatial ports; fixed sign triple; one synchronous, exactly invertible Rule3 step. No gravity state, time gate, detector intervention, or additional force is introduced. All runs were done with the six core files exactly matching Git blob hashes of commit [`c5a23743`](https://github.com/Closer24/Universe24/commit/c5a23743d96936190210dd510105ed470d4a0b23).

## New exact restricted clock-rate coincidence

For fixed `+++` coupling and `L=7`, the same all-48-channel source `(-1,-1,0)` at one neighboring spatial site changes two distinct all-48-channel probe preparations:

| Probe `(a,b,r)` in each of 48 channels | Isolated local period | Sourced local period | Far reference period | Ratio of local cycle rates |
|---|---:|---:|---:|---:|
| `(-1,-1,0)` | 4 | 5 | 4 | `4/5` |
| `(0,-1,4)` | 4 | 5 | 4 | `4/5` |

The seeds are not mere phase translations of one isolated scalar oscillator: their integer-counter squared norms `a²+b²` are different (`2` vs `1`) and their retained remainders differ. The result survives **all six face-neighbor directions**, with and without the source (24 full-board runs, 40 updates per run, 960 exact advance/rewind comparisons). With the source and distant control together, the whole board returns at steps 20 and 40; without the source at multiples of 4. No click classifier was used to count time.

**Scope:** This is a *two-preparation clock coincidence*, not the equivalence principle. Other preparations, including `(1,1,4)` and `(0,1,2)`, respond differently to the same source. The clocks strongly interact with their source; the probe limit, a long-range field, clock transport, time dilation for moving clocks, and a source-independent metric are unproved. The rate is a ratio of exact recurrence periods measured in reference updates, not independently validated physical proper time.

## Exact signed-Laplacian constraint on persistent scalar backgrounds

Index every channel address by `ν=(x,g)` and let `A_σ` be the unchanged reciprocal six-port operator. Define `θ=floor(r/2)`, `ε=r mod 2`, `p=3(b-a)+θ-1` and `L_σ=6I-A_σ`. Rule3 is **exactly**

```
p' = p - L_σ b
b' = b + floor((p'+1)/3)
ε' = ε
```

For any **complete-state period T**, summing the first equation yields `L_σ b̄=0`, where `b̄=T^{-1} Σ_n b_n`. On the reciprocal signed graph,

`v^T L_σ v = Σ_{undirected edges {ν,η}} (v_ν - w_νη v_η)^2 ≥ 0`.

Thus every edge demands `b̄_ν=w_νη b̄_η`. With connected `+++` graph, `b̄` is **spatially/channel uniform**; a spatially varying static field cannot be defined simply as the time-mean `b` of a periodic solution. If a connected signed graph has a frustrated cycle, that period mean is exactly zero. The result also applies to accumulation points of time averages of **uniformly bounded** trajectories, since `(p_T-p_0)/T→0`. This leaves room for nonlinear *correlations, phase responses and signal travel times*, not a static `b`-density shortcut.

We checked connectivity and signed gauge consistency for all eight sign triples with `L=3,4,5,6` (all 48 channels at all sites). In these *tested finite cases*, the one-dimensional null sectors are:

- odd `L`: `+++`, `+--`;
- even `L`: `+++`, `+--`, `-++`, `---`;
- other triples: no zero mode.

In the 24 balanced `(L,sign,magnitude)` cases with `m=1,-2`, the resulting nonzero `a=b=mη`, `r=2` states were verified as exact Rule3 fixed points. This finite classification is not asserted for every `L` without further proof. Nontrivial all-channel isolated/pair examples of periods 4, 5, 4 had exactly zero time-mean `b` everywhere.

## Exact local continuity, not physical stress-energy

The existing signed arithmetic account is `Q_ν=6(b_ν-a_ν)+r_ν-2=2p_ν+ε_ν`. For `+++`, define oriented edge current `J_{ν→η}=2(b_ν-b_η)=-J_{η→ν}`. Then the full board satisfies

`Q'_ν-Q_ν+Σ_{η~ν}J_{ν→η}=0`.

Grouping the **48 channels per spatial site** gives an exact lattice event-space continuity equation:

`q'(x)-q(x)+Σ_i [J_i(x+e_i/2)-J_i(x-e_i/2)]=0`,

with `q(x)=Σ_g Q_(x,g)` and `J_i(x+e_i/2)=2Σ_g[b_(x,g)-b_(x+e_i,f_i(g))]`.

This was checked on 364 spatial sites with random dense all-48 states, as well as separately in all-channel balanced-vacuum runs. **`Q` is not identified as physical energy, and `J` is not `T_{μν}`.** Einstein requires conservation of a independently identified energy–momentum tensor. Signed variants outside `+++` generally do not conserve this `Q`.

## Exact sign-symmetric, first-step isotropic transmission substrate

Let `z=14` be the center of `2O`. For each central pair `{g,zg}` at every spatial site, set the retained remainders to `(0,4)` and counters to `(0,0)`. The resulting 24/24 phase-balanced state is fixed under all eight sign choices. With `J(a,b,r)=(-a,-b,4-r+2(r mod 2))` and `C:g↦zg`, the combined `K=C∘J` commutes with Rule3 and leaves that background fixed; positive and negative all-48 impulses are exact full-state `K` partners at every step (2,304 signed-port covariance checks and 96 six-step partner checks).

For the passive direction vectors `n_g=R(g)(1,1,2)^T`, the two directional threshold-response tensors are **exactly**

`Xi⁺ = (1/96)Σ_{θ_g=2}n_g n_g^T = I/2`,
`Xi⁻ = (1/96)Σ_{θ_g=0}n_g n_g^T = I/2`.

A unit impulse `b↦b+1` in **all 48 channels** at one site then produces exactly 24 changed `b` counters in *each of six neighbors after one step*. The usual uniform remainder-2 vacuum gives zero neighbor `b` changes at that step. This is a limited *signal response* ingredient.

**Failure to overclaim:** By step 3 the six neighbor amplitudes on the balanced substrate differ (`7,10,8,4,10,7`), hence the substrate is **not globally isotropic**. A separate prepared-clock trial on that substrate had no local exact period over 16 steps; the source spread across the `L=7` torus. No universal slowdown or Einstein causal metric emerged from it.

## Evidence and reproducibility

Run (Python standard library only):

```bash
python research/einstein_clock_bricks_v1/audit.py
```

The command checks the pinned six core Git blobs; prepares initial states only; executes unmodified `Engine.advance/rewind`; and prints a deterministic JSON summary. A captured verified output is [`results.json`](./results.json). If the core is deliberately changed, run this historical audit on the pinned commit rather than silently comparing different rules.

The Einstein-facing benchmark remains: show that several independent **physically calibrated** clock and signaling systems exhibit a common quadratic proper-time law `Q_x(v/c)=A(x)+2B_i(x)v^i/c-C_ij(x)v^iv^j/c²`, giving one nondegenerate Lorentzian metric, and **independently** derive a stress-energy source and Einstein dynamics or a well-defined limit. Merely naming a tensor in the `48` counters does not meet this benchmark.

Physics benchmarks (not validations of this automaton): [Puetzfeld–Obukhov–Lämmerzahl, gravitational clock compass](https://doi.org/10.1103/PhysRevD.98.024032); [Carlip, challenges for emergent gravity](https://doi.org/10.1016/j.shpsb.2012.11.002); [Jacobson, thermodynamics of spacetime](https://doi.org/10.1103/PhysRevLett.75.1260).
