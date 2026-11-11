# Single-edge experiment: exact algebra, incomplete physics

This is an explicit alternative tensor for the same Rule3 engine, **not an accepted replacement for the default**. It satisfies the stronger support condition, retains actual link registers, and is exactly reversible. It changes dynamics. An explicit passive coordinate map repairs an initially mismatched electromagnetic diagnostic, but neither this experiment nor the default has established Einstein spacetime.

## Board events and observed clicks

P3 of the research proposal assigns the underlying event network a possible (3+1)-dimensional spacetime interpretation. P7 defines clicks as local observations of that network. These are two descriptions of one proposed physical system, not two independent physical spacetimes.

In the executable algebra, a history is `(S_n)`, with computational labels `(n,x,i)`. Tensor dependencies give a directed graph of possible influences between updates. A click is a selected transition under the fixed map `Theta(S_n,S_(n+1))`. The update counter and lattice coordinates are simulation coordinates. An effective spacetime geometry would have to be inferred from the board's signal and clock dynamics and agree with measurements in the click stream.

The intended claim can therefore be: **the board realizes spacetime, and clicks reveal its observable events**. The code does not yet prove that the resulting geometry is Lorentzian, observer independent, or governed by Einstein's equations. Assigning names such as `metric.h00` or recording `(step,x,y,z)` does not supply that proof. A smooth relativistic limit also needs a declared scale and convergence regime for this discrete finite simulation.

## What the tensor contains

The serialized tensor stores gear types, each physical link's positive axis, every input offset and time register, integer coefficients, observation labels and the common Q. Actual a,b,r values belong to the state. L and periodic boundary conditions specify the ambient network separately.

A link gear `U_i(x)` with axis e occupies `{x,x+e}` while being stored at x. A node gear occupies `{x}`. The strong condition requires the union of the output's and all inputs' declared supports to lie in one node or one adjacent pair. It is checked on the translation-invariant template, before periodic wrapping; a tiny board cannot hide a violation by identifying endpoints.

## The new construction

For each of the 90 original link-gear types U_i introduce an independent node mediator H_i at its base site. Keep U_i, its endpoints and metadata. The original 382 types plus 90 new types give 472 triples per spatial site. Every added type is audit-labelled.

Let R replace each original link variable U_i by H_i, including its old-a and old-b references; original node variables stay unchanged. Write F_i(Ra,Rb) for the original polynomial input after that substitution. For an original node output j, set

\[
\widetilde u_j(x)=F_j(Ra,Rb)(x).
\]

For a link type with positive axis e, choose one explicit fixed integer `1 <= k <= Q` and set

\[
\begin{aligned}
\widetilde u_{H_i}(x)&=F_i(Ra,Rb)(x)
  +k\,[b_{U_i}(x)+b_{U_i}(x-e)-2b_{H_i}(x)],\\
\widetilde u_{U_i}(x)&=(D-2k)b_{U_i}(x)
  +k\,[b_{H_i}(x)+b_{H_i}(x+e)],\qquad D=6Q.
\end{aligned}
\]

All these inputs go through exactly the existing scalar update:

\[
(\ell,r')=\operatorname{divmod}(2\widetilde u+r,D),\qquad
a'=b,\quad b'=\ell-a.
\]

The added coupling is a reciprocal node/link spring. With the shared field sign s_i, its polynomial potential is

\[
\Phi_{\rm edge}=-\frac{k}{2s_i}\sum_x
  \left[(b_{U_i}(x)-b_{H_i}(x))^2+
        (b_{U_i}(x)-b_{H_i}(x+e))^2\right].
\]

Its signed derivatives give exactly the added spring terms. The U inertia comes from `D b_U^2/(2s_i)`. This describes the coupling algebra; it does not identify a conserved positive physical energy of the complete integer dynamics.

The seed copies the original link's a,b,r into the corresponding H once. Thereafter U and H evolve independently. No copying, synchronization, projection, runtime parameter change or observation feedback enforces equality.

Any mirror statement in the inherited seed-preparation report concerns the source preparation. A physical mirror, full cube action on the new mediators or gauge symmetry of the extended dynamics is not supplied by the inverse proof and must be checked separately.

## Why the structural claims hold

**Support.** Every original polynomial term now involves node variables only. Original storage locality confines such a term to x and at most one face neighbor. Each added U term uses its own link and its two endpoint H values. Each H spring term uses an incident link. Therefore every monomial has strict one-edge physical support.

**Rank and arithmetic.** R changes indices, not degree. The added terms are linear. Maximum input degree remains three, so tensor rank remains four. Q and D do not change; all tensor coefficients, states and recurrence operations remain exact integers.

**Inverse.** The original acyclic old-a dependency graph is relabelled injectively under R. The new U equations and spring couplings add b reads only, so no old-a cycle is introduced. Recover b=a' and then use the same staged inverse from A6a. The inverse holds on the entire extended state space, not only on the prepared subspace H=U. The tested stage sizes are 455,1,16.

**Actual mediation.** U affects endpoint H registers, and H affects U. The original U metadata is retained. These are new degrees of freedom, not a cosmetic deletion of link endpoints. However, the old gauge equations now act on node H variables; their former gauge transformation law cannot simply be attributed to physical links U. Full gauge covariance and the desired physical interpretation need a new derivation.

## Why an unchanged one-step rewrite is impossible on the same state

The baseline `em.A_x(x)` input has coefficient Q-1 multiplying `em.A_x(x-e_y)`. That input link is outside the output edge `{x,x+e_x}`. Take two zero-amplitude states, with identical remainders, that differ only by D in that outside input's b register. All data on the output edge agree, but the old next output differs by exactly `2(Q-1)`.

Any rule using only the same output edge must give the same next output for those two states. Therefore it cannot equal the old update on all states. One must change dynamics, add retained mediator state and possibly delays, or retain the less restrictive locality condition. This is a counterexample to this unchanged-state, unchanged-tick rewrite, not a proof that every possible enlarged local realization is impossible.

The regression test verifies this counterexample. In the new realization that outside perturbation reaches the physical output link after two updates, instead of one.

## Executed checks and failures

The recorded example uses Q=8,589,934,593, k=33,554,432, L=4 and 120 updates. k is an explicit construction choice. It was examined alongside weaker and stronger alternatives; it is not derived from Rule3 or selected by the running board.

| Check | Result |
|---|---|
| Gear types / physical link types | 472 / 90 |
| Tensor rank / live monomials | 4 / 19,042 |
| Strict support violations | 0, compared with 3,300 in the baseline |
| Largest declared support diameter | One lattice edge |
| Independent scalar comparisons | 2,832 sampled transitions, including large integers; zero mismatches |
| Full random extended-state inverse | Passed, including independent H/U values and integers beyond int64 |
| 120-update seed replay and rewind | Exact; maximum state bit length 36 in this run |
| Official events | 152,617; event-file decoder agrees exactly |
| Physical-link perturbation cone | No differences outside one edge per update over the tested three updates |
| Same-tick equivalence with baseline | False; old and new visible matter records also differ |
| Old electromagnetic Lorenz identity | Fails from update 2; 2,496 nonzero site-updates in 40 updates, maximum defect 1,946,575 |
| Lorenz identity with explicit source-coordinate view | Passes: zero nonzero site-updates over 40 updates |
| Strong-coupling control k=Q | Exceeds a 128-bit growth limit at update 38 (282 bits); exact rewind still holds |
| Gravitational response of cosmic clock records | No response: exact structural decoupling, confirmed in 40 updates |

The unchanged cosmic clock signal is expected: its subsystem is isolated from the modified package. It is not evidence that the new links preserve gravitational physics. Bounded values over 120 updates do not establish long-time stability.

The electromagnetic diagnostic is the **Lorenz gauge identity**, not a test of Lorentz boosts. Reading the old A names from the new physical U registers is the wrong coordinate map for the inherited Phi equation: that equation now reads H. `observe.strict_edge.source_coordinate_view` selects H for each former source-link coordinate and leaves original node coordinates unchanged. It copies data for observation only. With this declared map, the Lorenz identity is restored exactly in the tested run, as predicted by the unchanged form of the Phi equation in those coordinates.

This map is many-to-one and is not an inverse or an assertion that the old physical theory was recovered. The source-coordinate H equations contain the additional force `k(U(x)+U(x-e)-2H(x))`; it is not removed by relabelling. Full Maxwell/gauge dynamics, physical calibration and relativistic equivalence require separate tests. The source and new clocks remain independent of the proposed metric sector; calling them universal proper-time clocks is consequently unsupported.

Machine-readable records: [locality and replay](evidence/single_edge_audit.json), [strong-coupling failure](evidence/single_edge_strong.json), [physical acceptance checks](evidence/single_edge_physics_gate.json).

## Einstein-spacetime acceptance requirements

1. Define local clocks, signal exchange and radar measurements from actual board dynamics. Reconstruct the same effective metric from multiple preparations and observer constructions; do not insert it into the decoder.
2. Derive a shared Lorentzian causal cone and local Lorentz symmetry in the claimed regime, with quantified direction, boost, lattice and finite-volume errors.
3. Establish universal clock and matter response, including gravitational redshift and free fall, rather than a response confined to selected gears.
4. Identify stress-energy and show the appropriate balances and metric field equations. A Newtonian source profile or selected weak-field factor does not establish full Einstein dynamics.
5. Show that the declared click observables reproduce these measurements. Moving the proposed spacetime interpretation from clicks to the board does not remove the observable requirements.

One precise continuum target is a family of operational reconstructions from board histories to metrics `g_epsilon` and identified stress tensors `T_epsilon`, with a stated scale epsilon. In the claimed regime, clock records should converge to

\[
d\tau^2=-g_{\mu\nu}dx^\mu dx^\nu/c^2
\]

for timelike trajectories (signature -+++), freely propagating light should follow the same metric's null cone, and a specified norm of the field-equation residual should tend to zero:

\[
G_{\mu\nu}[g_\epsilon]+\Lambda g_{\epsilon,\mu\nu}
-\frac{8\pi G}{c^4}T_{\epsilon,\mu\nu}\longrightarrow0.
\]

These are targets to derive and test, not extra update equations implemented in the decoder. The computational geometry, the reconstructed physical geometry, and agreement with measured clicks must be distinguished throughout the proof.

These are research acceptance conditions, not outputs the tool fabricates. `physics_gate` records `accepted_as_physics_preserving_replacement=false` for the present experiment. For context, see [Will's review of relativity tests](https://arxiv.org/abs/1403.7377). Multi-link interactions can themselves be local: [Mathur and Rathor](https://arxiv.org/abs/2109.00992) explicitly distinguish link/plaquette descriptions and the extra structure needed when introducing auxiliary variables. Their duality is not a proof for this automaton.

## Reproduction

```bash
python -m unittest universe24.tests.test_strict_edge -v
python -m universe24.tools.audit_contract --single-edge --stiffness 33554432 --L 4 --steps 120 --out runs/single-edge
python -m universe24.tools.audit_contract --replay runs/single-edge
python -m universe24.tools.physics_gate --out runs/physics-gate/report.json
python -m universe24.tools.audit_contract --single-edge --stiffness 8589934593 --L 4 --steps 120 --max-bits 128 --out runs/single-edge-strong
```

The final command deliberately returns exit code 2 at the recorded growth limit; it saves the completed prefix and its exact inverse/replay check. It is a negative control. The model is fixed throughout every run. Construction is in `layers/strict_edge.py`, seed extension in `prepare/strict_edge.py`, passive coordinate selection in `observe/strict_edge.py`, and evolution still uses the unmodified `core/engine.py`.
