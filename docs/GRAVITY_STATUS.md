# Clocks, activity and gravity: current evidence

Universe24 investigates whether counter interactions can change calibrated
clock and signal behavior in a way described by one effective spacetime
geometry. The metric would be inferred from those measurements, not inserted
as another state variable or force in Rule3.

**There is a restricted, reproducible clock-rate result. There is no derived
gravitational time-dilation law, physical metric or Einstein field equation.**
All results below use the existing model: one board, 48 channels per site,
six spatial inputs, fixed pre-run coupling and the same integer Rule3.

## What is established

| Result | Evidence class and scope |
| --- | --- |
| Complete balance coordinates | Exact rewriting with `p=3(b-a)+floor(r/2)-1` and `epsilon=r mod 2`; the complete coordinates are `(b,p,epsilon)`, not `p` alone. |
| Restricted rate coincidence | Two specified all-48-channel probe preparations change from local period 4 to 5 under the same adjacent source, while a far reference keeps period 4. The measured recurrence-rate ratio is `4/5`. |
| Signed-Laplacian restriction | A complete periodic orbit has `L_sigma mean(b)=0`. This excludes a spatially varying static field defined only as the periodic mean `b` in the connected positive graph. |
| Local arithmetic continuity | The positive coupling has an exact local storage/current identity for the existing arithmetic account `Q`; it is not established energy or stress-energy. |
| Collective activity identity | The sum of the activity tensor's traces is a quadratic coupling functional whose gradient gives the exact `p` increment. Its value alone does not determine the next state or a clock rate. |
| Autonomous finite-guide link | A prepared local source launches a phase front, the endpoint records and returns it, and the source retains return parity. Records are cyclic; this is not an accumulated elapsed-time counter. |
| Exact variational Rule3 | The full-48 chart `(b,p,epsilon)` has a nearest-neighbor discrete generating action for every signed tensor. Its auxiliary symplectic embedding is not physical spacetime or conserved energy. |
| Newtonian spatial operator | The 48-channel-uniform `+++` sector yields the 3D scalar Laplacian with a `1/(4*pi*r)` Green tail, but no self-sustained mass source or force has been derived. |
| Einstein clock-signal gate | A nonconstant static conformal lapse with unchanged *physical* coordinate null cones cannot be a vacuum Einstein solution at Lambda=0. Present pulse fronts are not calibrated photons, so no PPN gamma is extracted. |

The first four results are documented in the existing
[all-48-channel prerequisites](../research/einstein_clock_bricks_v1/README.md).
The [collective activity audit](../research/collective_clock_geometry/README.md)
provides the activity derivation and an independent replay of the rate result.
The [finite-guide clock link](../research/clock_link_v1/README.md) supplies a
separate data-only preparation and fresh reproducibility evidence.

## The measured 4/5 result and its boundary

At side `L=7` with fixed `+++` coupling, every channel at the source has initial
triple `(-1,-1,0)`. The source is one face neighbor from the probe. The two
probe preparations are `(-1,-1,0)` and `(0,-1,4)`, each assigned to all 48
channels at its site. Each isolated local period is four; each sourced local
period is five. A distant reference remains period four.
The local recurrence includes all 48 complete triples at the probe site. With
the source and reference present, the complete board returns at updates 20 and
40; its period is not asserted to be five.

The original package checks all six neighbor directions, both probe seeds and
source-present/source-absent controls: 24 full-board runs of 40 updates.
These are exact recurrence comparisons, not missing-click counts. The two
probe seeds are not phase translations of one isolated counter orbit.

This result must not be replaced by the blanket statement that no two clock
preparations exhibit a common changed rate. It also must not be generalized to
universal gravitational slowing: other specified seeds respond differently.
The source and probe strongly interact, and an autonomous signal-based proper
time calibration, a probe limit and a long-range field have not been shown.

## What the activity tensor actually implies

Write `A` for the reciprocal signed coupling operator, `L_sigma=6I-A`, and

\[
S_{ij}(x)=\frac14\sum_{g,d}
\bigl(b_{x,g}-w_d(g)b_{x+d,h}\bigr)^2d_i d_j.
\]

Here `h` and `w_d(g)` are the existing channel map and sign for direction `d`.
In the lattice-axis coordinates this squared-mismatch diagnostic is diagonal
and positive semidefinite. The exact global identity is

\[
V(b)=\sum_x\operatorname{tr}S(x)=\frac12 b^T L_\sigma b.
\]

With `p=3(b-a)+floor(r/2)-1`, the unchanged update is equivalently

\[
p'=p-\nabla_bV=p+Ab-6b,\qquad
b'=b+\left\lfloor\frac{p'+1}{3}\right\rfloor,\qquad
\epsilon'=\epsilon.
\]

The gradient is taken from the quadratic expression as a function of all `b`
coordinates and evaluated at the integer state. It cannot be recovered merely
by knowing a numerical value of `V` or the local entries of `S`. No continuous
integration or extra force is performed by the engine.

Also,

\[
\sum_g\bigl(p'_{x,g}-p_{x,g}\bigr)^2
\le 24\operatorname{tr}S(x).
\]

This bounds the balance change; it does not identify its sign or a ticking
frequency. `p` is not automatically a monotone clock phase, and `V` is not a
proved conserved energy. Equal activity does not imply equal next states.
**No formula `N=F(S)` for gravitational clock slowing has been derived.**

## What still separates clock response from Einstein gravity

1. Specify working internal clocks and fixed readouts, then compare their
   readings through autonomous signals and retained records. Simulator update
   labels remain a verification index until an operational time is constructed.
2. Test whether independent clock constructions have the same normalized rate
   response across source strengths, phases, separations and moving probes.
   Preserve mismatches and disrupted clocks as failures of that stated test.
3. Derive spatial relations and signal propagation as well as clock rates.
   In a suitable static, zero-shift description a measured lapse `N` would give
   `g_tt=-c^2 N^2`; this conditional translation alone does not determine the
   spatial metric or curvature.
4. Require one nondegenerate Lorentzian metric to predict unused clock,
   signal and motion measurements. Then compute its Einstein tensor
   `G_mn=R_mn-(R/2)g_mn`.
5. Identify energy, momentum, stress and flux independently from the state and
   test `G_mn+Lambda g_mn=kappa T_mn` in a stated limit and error range. Defining
   `T` from the left side would not test Einstein dynamics.

The [physical target sheet](../research/clock_selection/physics_targets/gravity.md)
states the observation-level benchmarks. A varying recurrence period is useful
evidence about a prepared device, but changing its geometry or seed is not by
itself a gravitational effect on the same calibrated clock.

## Reproduction and provenance

The all-48-channel package was already present at commit
[`37fe77be`](https://github.com/Closer24/Universe24/commit/37fe77be8f489ba722ac687ff544b3956352e62f).
Its original files and results remain unchanged. The added activity and
clock-link packages are newly executed reconstructions after transient local
workspace files became unavailable. Their receipts describe only their own
fresh checks; historical local run counts are not presented as recovered data.

Use each linked package's command and read its declared preparation domain,
source hashes, controls, complete-state inverse checks and limitations. None
of these packages modifies the core, coupling or arithmetic C classifier.

## Variational action, Newtonian kernel and Einstein consistency

The [new all-channel variational/Einstein gate](../research/variational_gravity_gate_v1/README.md) is a **mathematical bridge and falsification framework, not an Einstein gravity solution**. It extends the existing exact `p`/strain identity (above; no change to Rule3) by a phase-space action and a separately checked Einstein-vacuum metric constraint.

For each complete channel, the invertible chart is `(b,p,epsilon)`, `p=3(b-a)+floor(r/2)-1`, `epsilon=r mod 2`; `p'=p-L_sigma b`, `b'=b+floor((p'+1)/3)`, `epsilon'=epsilon`. Let `V(b)=b^T L_sigma b/2`. Choose a differentiable real interpolation `K` with `K'(m)=floor((m+1)/3)` at integer `m` (the linked audit supplies an explicit monotone interpolation). Then the *auxiliary* nearest-neighbor discrete action

```text
S = sum_n [ p_(n+1) · (b_(n+1)-b_n)
            - sum_channels K(p_(n+1))
            - V(b_n) ]
```

has stationary equations exactly equal to native Rule3 on all integer states, with the original remainder reconstructed from `(p,epsilon)`. It gives a canonical/symplectic real-valued embedding, **not a claim that the physical cellular automaton is continuous**. The naive `H=V+sum K` is *not* conserved by the finite update; neither it nor the earlier arithmetic account `Q` is proved to be physical stress-energy.

For `+++`, the channel-uniform scalar sector is preserved exactly and `(L_+ b)_(x,g)=6 B_x-sum_(d=±x,±y,±z)B_(x+d)` for **every one of the 48 channels**. Its 3D Green kernel has leading static far-field `G(r)=1/(4*pi*r)+O(r^-3)`. On a finite periodic board `L_scalar G_L=delta_0-1/L^3`; the kernel is an **inverse of a spatial operator**, not a demonstrated self-generated source, acceleration, or gravity. The exact orbit identity `L_sigma mean_T(b)=-(p_T-p_0)/T` shows why a complete periodic trajectory cannot create a nonuniform static mean-`b` potential in the connected positive case. A self-consistent source with independently measured physical mass remains missing.

In a stationary, zero-shift *physical* ansatz `ds²=-N²c²dt²+H² dx_i dx_i`, physical null signals would obey `v_null/c=N/H`. If they had position-independent isotropic coordinate speed `c`, then `H=N`, `g_mu_nu=N² eta_mu_nu`. With `omega=ln N`, exact four-dimensional curvature gives `G_00=-2 Delta omega-|grad omega|²` and `sum_i G_ii=4 Delta omega+5|grad omega|²`, hence `sum_i G_ii+2G_00=3|grad omega|²`. An exterior **vacuum** Einstein solution with `Lambda=0` therefore requires `grad N=0` under this restricted ansatz. This does **not** imply that equal first-arrival update indices from current Universe24 pulses establish that ansatz; amplitude controls show they are not calibrated photon speeds.

In weak-field isotropic PPN coordinates, `N≈1-U/c²` and `v_null/c≈1-(1+gamma)U/c²`. GR requires `gamma=1` and thus the log-slope `d ln(v_null/c)/d ln(N)≈2` for a calibrated signal family; an unchanged physical coordinate null speed would instead imply `gamma=-1`. These are **prospective model-discrimination tests**, not fitted model results. The specified source perturbs two prepared clock types by the same ratio `4/5`, but its influence is confined and seeded midpoint pulse arrival depends on amplitude/sign; no long-range mass profile, universal clock or physical null cone is established.

**Reproduce:** `python -m research.variational_gravity_gate_v1.audit`, `python -m research.variational_gravity_gate_v1.signal_gate`; optional NumPy `python -m research.variational_gravity_gate_v1.newtonian_kernel`, optional SymPy `python -m research.variational_gravity_gate_v1.check_einstein_symbolic`, and `python -m unittest discover -s tests -p test_variational_gravity_gate.py -v`. The pinned five unmodified core blobs originate from `c5a23743`; local clean-tree checks passed seven regressions. Detailed observations, serialized receipts and limitations are in the linked research package. Neither the core nor the Presenter nor the observation classifier is altered.
