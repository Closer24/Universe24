# Researcher 8: compiler feasibility and independent synthesis

Date: 2026-11-11. Inspected local base `613ea1b`, PR #47 baseline
`621fc1f55800e50e1db5f6a30ce24bb83716a49a`, reports 01–06, actual core tensor
rules and the new principal-symbol proposal from researcher 7. Read current
issue #40, including the parallel integration team's held-out failure. This
report and its audit change no production law, reader or physical status.

## Recommendation

There is now a concrete way to combine two of this round's ingredients:
differentiate one local quartic edge potential to get reciprocal cubic
forces, then run those forces through native Rule3. A two-field executable
below verifies this connection and its exact shift-charge balance. It also
demonstrates why this is still only a primitive: a proposed positive stiffness
coordinate reaches zero immediately, and nonlinear growth remains.

For gravity, first repair the actual continuum formulation's off-constraint
principal symbol. Researcher 7's added-constraint construction is the most
specific new candidate in this review; I independently reproduced its
flat-symbol effect in two directions. Then derive a compatible discrete
gravity–matter identity, a refinable integer encoding and an exhaustive
allocation. Replacing only the integrator cannot remove a continuum
principal-symbol defect.

## Primary papers inspected

| Source and exact part read | Useful result | Boundary here |
| --- | --- | --- |
| Bennett, [Logical Reversibility of Computation](https://worrydream.com/refs/Bennett_1973_-_Logical_Reversibility_of_Computation.pdf), IBM JRD 17 (1973), introduction, construction and discussion pp.525–530 | Compute, copy the result, and reverse the computation can restore workspace while retaining input/output. Segmenting changes the time/storage tradeoff. | The theorem assumes sufficient temporary storage. It supplies neither a four-slot arithmetic circuit nor a static Rule3 schedule. Packing a history into one unbounded integer does not eliminate its bit cost. |
| Calderbank, Daubechies, Sweldens and Yeo, [Wavelet Transforms That Map Integers to Integers](https://cm-bell-labs.github.io/who/wim/papers/integer.pdf), §§3.1, 3.3–3.4, equations (3.3)–(3.8) | Sequential triangular additions remain invertible when the same rounded predictor is recomputed on reversal. The S transform preserves information through sum/difference parity. | Arbitrary filter rounding, sequential access and scaling steps are operations to compile; they are not already permitted polynomial inputs. This is a lifting design principle, not an Einstein solver. |
| Rein and Tamayo, [JANUS](https://arxiv.org/pdf/1704.07715), §§2.1–2.4, equations (3),(5) | Recomputed rounded forces allow bitwise-reversible integer updates for separable mechanical dynamics. Formal symplecticity is distinguished from a smooth map on real space. | Force evaluation still uses floating arithmetic and external rounding. These cannot enter this Engine as callbacks. Its separable force assumption does not cover generic GR kinetic terms. |
| Marsden and West, [Discrete mechanics and variational integrators](https://lagrangeweb.web.engr.illinois.edu/pubs/MaWe2001/MaWe2001.pdf), §1.3.3 theorem 1.3.3, §4.3.6 and following discussion | A symmetry of a discrete Lagrangian yields its discrete momentum map. Energy conservation in extended time requires the corresponding additional discrete equation. | A force derived from a potential is not by itself proof that an integer floor map is a discrete variational integrator. Fixed-step reversibility is not a proof of exact physical energy conservation. |

These are original texts inspected at the cited equations, not conclusions
inferred only from abstracts. The following Rule3 results are independent
project-specific calculations.

## What the native coordinates allow—and what they do not

The verified bijection is `q=b`, `p=6(b-a)+r`. For `u=6q+F(q)`,

```
p_next = p + 2 F(q)
q_next = q + floor(p_next/6).
```

This combines a kick and a fixed drift. It is not a general in-place
assignment language. In particular:

* The tensor accepts `a,b` factors, not `r`. Equal `a=3,b=5` with remainders
  0 and 1 has native momenta 12 and 13, but identical polynomial `u(a,b)`.
  A desired force `F=p` therefore cannot be read directly as that polynomial
  on the unrestricted legal state space. This is not a prohibition on all
  restricted representations or multi-channel encodings.
* An input depending on its target's old `a` is rejected by the acyclic
  inverse contract. Reinterpreting the triple as a physical canonical pair
  does not remove that validation rule.
* A pure momentum shear at fixed q is not one native microtick: for
  `q=0,p=5,F=1`, the forced drift also changes q to 1. A sequence of
  alternating abstract kick/drift operations needs an explicit embedding.
* The direct scaled nonlinear force coefficient is
  `3*h^2*c_d/S^(d-1)`, which is generally noninteger under refinement.
  Native algebra does not solve this obstruction from report 01.
* A clock multiplying a cubic force produces degree four. Temporary products
  and a different invariant schedule may help, but they count as retained
  workspace and must be restored without discarding history.

The audit verifies both validator rejections and the two exact scalar
counterexamples. No general native lifting compiler has been constructed.

## Executed reciprocal edge primitive

Use one field `phi` and one dynamical stiffness coordinate `g` at every node.
On each positive x edge `(i,j)`, take

```
V_ij = (g_i^2+g_j^2)*(phi_j-phi_i)^2/2.
```

This is a proposed mechanical potential, **not** an Einstein action or
metric. Differentiating the same expression gives

```
F_phi_i,ij = +(g_i^2+g_j^2)*(phi_j-phi_i)
F_phi_j,ij = -(g_i^2+g_j^2)*(phi_j-phi_i)
F_g_i,ij  = -g_i*(phi_j-phi_i)^2
F_g_j,ij  = -g_j*(phi_j-phi_i)^2.
```

For each node, sum the two incident x-edge contributions and use
`u_phi=6phi+F_phi`, `u_g=6g+F_g`. The expanded tensor has **2 total channels,
6 retained integers per node, 14 monomials, degree three, no old-a input and
strict single-face support**. No phase, denominator, extra link bank or
workspace is hidden. The spatial experiment is one-dimensional on a periodic
cubic lattice.

Since each edge supplies opposite phi forces,

`sum_i p_phi_i(next)-sum_i p_phi_i = 2 sum_i F_phi_i = 0`.

This holds exactly for all carry values because it is a native momentum
identity. It is the charge of uniform shifts of phi, **not demonstrated
spacetime momentum**. Reciprocal mixed derivatives are checked symbolically.

Actual Engine execution uses 27 nodes, six updates and spatially mixed
remainders containing all six values. Each transition agrees with an
independently written edge-force/native-coordinate oracle, each step inverts
and full rewind is exact. Total native phi momentum remains **63**. Retained
field bit lengths are `1,1,2,3,3,10,29`; six-valued remainders require up to
three bits separately. The audit records complete-state maximum bits as
`3,3,3,3,3,10,29`, including every a, b and r entry.

Two failures are intentionally retained:

1. Initially `g=1` everywhere, but **11 nodes have g=0 after one update**.
   Positivity of the expression `g^2` alone does not establish nondegeneracy.
   This invalidates any attempt to rename this primitive's g as a protected
   metric coordinate without a new invariant.
2. Deleting the g reaction leaves phi's opposite forces and native total
   momentum conservation intact, but violates reciprocity: at
   `phi_i=0,phi_j=1,g_i=g_j=1`, the mixed-derivative mismatch is **2**.
   That one-way model also rewinds. A conserved quantity and inverse do not
   establish reciprocal matter–geometry coupling.

No exact energy, boundedness, stable refinement, proper clock or Einstein
constraint is asserted. The primitive is not appended to the current44 law.

## Independent review of the actual geometry symbol

I re-extracted the code's flat principal matrices independently of audit07:
set `B=I,K=G=0`, replace each spatial derivative by `n_i*z_field`, and
differentiate the RHS with respect to the derivative jets. This tests the
continuum extension of the actual source equations, not an Engine orbit.

For both z and `(1,2,3)` directions, the original full24 symbol has
`nullity(A),nullity(A^2),nullity(A^3)=(14,16,18)`; triangular20 gives
`(10,12,14)`. These exact increases establish zero-eigenvalue Jordan chains.
The chain identified by researcher7 is off the torsion constraint surface;
it must not be described as a physical graviton instability without further
analysis. It nevertheless matters for numerical errors away from constraints.

Independently adding the proposed full-frame terms

```
Delta K_ab   = (R_ba-R_ab)/2
Delta G_abc  = -(delta_ac*M_b-delta_bc*M_a)/4
```

gives the expected characteristic polynomial

`lambda^14 (lambda^2-|n|^2)^2 (lambda^2-|n|^2/2) (lambda^2-|n|^2/8)^2`

and the square-free annihilator

`A (A^2-|n|^2 I)(A^2-|n|^2 I/2)(A^2-|n|^2 I/8)=0`

in both independently checked directions. This confirms the reported
diagonalizability there. Audit07 owns the all-direction derivation and
the associated candidate. The test here does not establish nonlinear
constraint propagation, a coupled strong-hyperbolicity theorem, an accepted
45-channel physical model or a positive-metric invariant.

## Staged next experiment

1. **Formulation:** test researcher7's full-frame constraint additions with
   matter and independent constraints, including oblique/high-frequency
   perturbations. Count the full-frame change; do not apply a successful
   full-frame result to the triangular reduction automatically.
2. **Local identities:** extend the demonstrated reciprocal edge construction
   to the selected gravitational variables and derive the actual discrete
   constraint/current propagation relation. A flux diagnostic alone does not
   change the old failing equations.
3. **Arithmetic:** target one explicit rounded shear such as
   `(Q,P)->(Q,P+2*floor(G(Q)/3^k))`, followed by its declared drift, with an
   inverse computed from retained coordinates. Start with a finite k and
   signed inputs. Derive a static sequence of fixed-six microticks with
   restored workspace, not a Python loop that computes the quotient for the
   Engine. First require a full channel ledger and per-stage inverse proof;
   if this cannot be compiled within the chosen budget, report blocked.
4. **Clocks:** reuse the massive scalar I/S port only after actual resolved
   periods and transport exist. Its zero added-state diagnostic is useful,
   but click-only measurement still requires an implemented retained record.
5. **Acceptance:** use predeclared fixed-domain, fixed-final-time refinement,
   held-out initial data, bit/time budgets, all remainders and negative
   controls. Preserve the parallel integration team's reported held-out
   gradient/momentum failure; do not tune it away.

The four protected44 spare channels or the three remaining channels in the
source-only full-frame45 candidate are **not** a proved arithmetic/apparatus allocation. No
closed solution for that composition is supplied here.

## Reproduction and review record

```
python -m validation.research_eight.08_reciprocal_native
```

Fresh evidence: `runs/research_eight/08_reciprocal_native.json`, including
source/tensor hashes, all rows, compiler negative controls and independent
symbol checks. I also independently reran audit01, audit02 and audit04;
all exited zero with their physical failure controls retained. Their complete
reports—not the zero process exit code—define each claim's scope.

General Einstein constraints, efficient refinable nonlinear arithmetic,
nondegenerate geometry and operational clocks remain open. The achieved
bridge is an actual cubic reciprocal edge primitive plus an independent
review of a promising formulation repair.
