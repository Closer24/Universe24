# Proposal: node channels, a shared metric, and transported probes

Status: research proposal only. No executable coefficients, new result, or
change to the default construction is supplied by this document.

## One law, several channel roles

Keep one fixed integer polynomial coupling tensor and the unchanged Rule3
update with divisor six. As in [MODEL.md](MODEL.md), use
v=(1,b,a) and u_i=sum_(jkl) T_ijkl v_j v_k v_l.
Constant slots represent lower-degree terms. This is one order-at-most-four
coupling tensor; actual order four requires nonzero cubic input terms.
Every monomial must obey single-face-neighbor support, and old-a dependencies
must remain acyclic. All forward reads use the same complete old snapshot.

A channel at a node retains (a,b,r). Assigning a geometric, probe, or clock
role does not introduce a different update rule.

| Proposed channel role | Intended meaning |
| --- | --- |
| Coframe E | Local geometric components |
| Connection, where required | Geometric transport information |
| Probe | A localized pattern transported between actual board nodes |
| Clock | An independently constructed ticking mechanism carried with or compared to the probe |

Sixteen components describe a 4 by 4 coframe, but that is not a promise of
sixteen total channels: retained banks, connection, probe and clock channels
must be counted explicitly in the eventual construction. The existing
48-channel group-reference block must not silently be reinterpreted or replaced.

## Read the metric from the state

Use the passive decoder

    g_mu_nu = sum_ab eta_ab E^a_mu E^b_nu,
    eta = diag(-1,1,1,1).

Specify a fixed unit calibration and coordinate chart. An invertible E gives
a Lorentzian metric; preservation of invertibility is a separate obligation.
The metric may vary as channel values evolve while T remains fixed.
This decoded rank-two tensor is not another coupling law and is not the
rank-four Riemann tensor. Observers never feed corrections into evolution.

## What "following Einstein's lines" means

The target is free-fall geodesics of the decoded metric, not the drawn edges
of the storage graph. For an affine parameter lambda, the continuum target is

    d²x^mu/dlambda² + Gamma^mu_alpha_beta[g]
        (dx^alpha/dlambda)(dx^beta/dlambda) = 0.

For timelike motion, compare an independent clock's ticks with proper time
computed from the same metric (in c=1 units),

    d tau² = -g_mu_nu dx^mu dx^nu.

A null signal instead has ds²=0 and no ticking proper time. Accelerated bodies
need not follow geodesics. Discrete node hops need a declared event-to-coordinate
decoder and approximation regime before comparison with these equations.

Do not steer the probe with an external geodesic solver during a run. Its
motion and clock ticks must result from the predeclared tensor and complete
seed. Compute geometric predictions passively for comparison.

## First experiment and acceptance criteria

Start with a separate optional construction, testing flat and curved
preparations under the same tensor and calibration. The current
[pp-wave sector](PPWAVE_PALATINI_LOCAL.md) is a possible restricted starting
point, not a generic gravity solution.

1. Demonstrate a localized probe moving through board links. The existing
   [geodesic extension](PPWAVE_OPERATIONAL_ROUTE.md) stores a worldline at one
   carrier node and does not yet meet this criterion.
2. Decode geometry, probe events and an independent clock under one fixed
   protocol. Predict held-out trajectories and clock readouts without
   per-run or per-species scale fitting.
3. Declare a finite chart, boundary treatment, observation interval and
   quantitative error criterion before comparing against geodesics and
   proper time. Report seam failures and off-preparation controls.
4. Export the exact tensor, complete seed, decoder, channel inventory and
   source provenance. Verify locality, full-state forward/inverse recovery,
   nondegeneracy over the stated domain, and the relevant fixed-six tests.

A test-probe milestone may omit backreaction, but must say so. Recovering
Einstein dynamics additionally requires a defined matter source, consistent
backreaction, local balances, constraint preservation and an appropriate
continuum limit. Geodesic agreement alone does not establish any of these.

The next implementation task is to construct and test explicit channel
couplings satisfying this specification. Their existence with the desired
behavior has not been demonstrated here. A new tensor is a model change;
keep its evidence separate from the default and historical runs.
