# Electric charge and electromagnetic interaction: operational research target

Status: sourced physical requirements and proposed board tests; no electromagnetic
mechanism has been demonstrated. Sources checked on 2026-11-08. This note does
not change Rule3, couplings, preparations, observers or frozen studies.

## Established physical target

Electric charge is a property governing electromagnetic interaction, not an
additional fundamental force. CERN distinguishes the electromagnetic interaction
and its photon mediator from the strong, weak and gravitational interactions
[S1]. This distinction does not identify a Universe24 carrier with a photon.

In classical electrostatics, isolated point charges obey the Coulomb form
`F = k*q1*q2*r/|r|^3`, with like-sign repulsion and opposite-sign attraction;
the potential energy is `V = k*q1*q2/|r|` up to a constant. These statements
have declared point-source/static limits. Distributed charges, conductors and
polarizable neutral objects require a fuller field description [S2].

Charge conservation is local: `partial_t rho + div j = 0`. For a region,
charge change equals minus outward current flux. The classical moving-charge
response is `F=q(E+v cross B)`, so electrostatic sign tests alone cannot derive
magnetism [S3]. Maxwell theory supplies retarded fields: changes depend on
source motion at an earlier light-cone time. Simply delaying an inverse-square
static force omits terms needed for the actual electromagnetic field [S4].

Conservation remains an experimental target, not a result inferred merely from
naming a variable. An original 2025 analysis of XENONnT electron-recoil data
searched for invisible charge-nonconserving electron decay and reported no
significant signal, obtaining a channel-specific lifetime bound [S5]. That
experiment does not test Universe24 and supplies no evidence for this model.

## Define charge from records, before assigning it to counters

The proposed operational object is a stable, identifiable structure whose
charge label predicts detector records in more than one apparatus. Freeze
source, trajectory, detector, no-click, timing and sign conventions first.
A reference probe establishes the positive-sign convention. Candidate charge
sign then predicts the direction of deflection relative to matched source-off
motion. Magnitude requires consistent relative response across independently
calibrated probes, distances and incoming velocities. A signed counter, a
single C2 event or disappearance of an outgoing packet is insufficient.

At the click level retain arrival-time differences, outgoing detector locations,
missing-record frequencies, angular distributions and all trial outcomes.
Calibration must not be refitted separately for each tested sign or distance.
If momentum or inertial mass is not yet independently defined, report calibrated
kinematic response; do not silently call it force or scattering cross section.

## An exact board ingredient, and why it is not already electric charge

For +++ coupling define the existing local algebraic account
`q_i = 6*(b_i-a_i)+r_i-r_background`. Rule3 gives
`Delta q_i = 2*sum_(j adjacent i) b_j - 12*b_i`.
On the reciprocal six-edge channel graph this can be written as a discrete
continuity identity with antisymmetric current `J_ij=2*(b_i-b_j)`:
`Delta q_i = -sum_j J_ij`. Thus the total account is conserved on the periodic
board. This is exact algebra, not a new physical result or runtime rule.
The general signed-coupling balance is different; do not assume that the same
account is conserved for all eight sign triples. See ../forces_algebra.md.

There is a sharper operational obstruction to identifying this raw account
with measured electric charge. Write `r=2*s+p`, where `p` is remainder parity.
The complete `(a,b,s)` dynamics and existing guarded C records are independent
of p. Changing only p at one address changes raw Q while leaving those internal
responses identical. Therefore a charge defined solely by these responses
cannot simply equal raw Q. The parity-subtracted account remains a possible
mathematical candidate, but has no demonstrated Coulomb response or physical
charge calibration either. See ../algebra.md and the existing staged-blocks
parity proof. Neither conservation nor a sign supplies the missing interaction.

A board hypothesis may seek persistent structures carrying an active conserved
label, with ordinary Rule3 disturbances transporting its influence. Any apparent
long-range interaction must arise through successive local updates. No field,
force, charge-dependent coupling, selector or detector action may be inserted.

## Prospective gates and falsifiable predictions

These are proposals, not executed protocols. Exact preparation families,
finite domains, budgets and tolerances must be frozen before any run.

| Gate | Required records and controls | Failure of the proposed domain |
| --- | --- | --- |
| Sign response | Same-sign, opposite-sign, neutral and absent-source controls with independently functional identified structures | Sign reversal fails to reverse the calibrated interaction response, or an apparent response is lost structure identity |
| Conserved transported label | Sum labels of every incoming/outgoing structure and all retained radiation; test region change against boundary transport | Missing balance cannot be attributed to declared error or unresolved emitted state |
| Range and direction | Several distances, axes and off-axis directions; compare matched singleton trajectories | Response exists only at an engineered contact/guide or depends on orientation beyond registered tolerance |
| Retardation | Change only initial source preparation; compare detector-time onset to the local causal cone and independent propagation calibration | Apparent early response comes from a changed detector/guide preparation, or no consistent delayed response exists |
| Effective static law | Fit one Coulomb-like coefficient on a training subset, freeze it, test held-out distances and charge magnitudes | A single coefficient fails the registered held-out error bound |
| Magnetic extension | Moving source/probe families and reversed velocities, with the same charge calibration | Electric-only fit fails to predict the declared velocity-dependent transverse response |

Use an explicit dimensionless residual such as
`epsilon = max_cases |response_measured-response_predicted|/response_scale`,
where the positive scale and tolerance are fixed before validation. Keep absolute
error separately near predicted zero. Exact integer conservation residuals
should be zero when claiming an exact identity. Deterministic repeats do not
supply independent statistical samples; uncertainty over a preparation ensemble
needs a declared sampling procedure and retained no-click outcomes.

A candidate potential requires a family of trajectories or calibrated work
measurements. Fit `1/r`, screened and finite-range alternatives on equal data;
a visually attractive pair is not a Coulomb law. Distinguish boundary-mediated
returns from long-range response by size and nonwrapping controls. The lattice
causal bound alone is not isotropic physical light speed.

## Present gaps and next concrete decision

Current clock phase records, transmission control and driven pause preparations
do not provide calibrated charged particles, three-dimensional freely moving
probes, a long-range field, an effective Coulomb potential, magnetic response
or charge-conserving physical scattering predictions. The new stationary pair
study can test interacting organization, but fixed-site phase changes do not
measure attraction. Its results must not be relabeled electromagnetic evidence.

The first useful gate is a source-controlled response of independently tracked
moving structures, with opposite/same-label and source-off controls, unchanged
coupling and complete inverse audit. Only after that passes should a charge
interpretation advance to distance laws and retardation. A negative result
bounds the chosen preparation and observer family; it does not exclude every
Rule3 electromagnetic candidate.

## Primary and institutional sources

- [S1] CERN, *The Standard Model*, institutional description of particles and
  interactions. https://home.web.cern.ch/science/physics/standard-model
- [S2] R. P. Feynman, R. B. Leighton and M. Sands, *The Feynman Lectures on
  Physics*, Volume II, Chapter 4, authored treatment of Coulomb electrostatics
  and Maxwell equations. https://www.feynmanlectures.caltech.edu/II_04.html
- [S3] Same authors, Volume II, Chapter 13, authored treatment of charge
  continuity and Lorentz response. https://www.feynmanlectures.caltech.edu/II_13.html
- [S4] Same authors, Volume II, Chapter 21, authored derivation/discussion of
  retarded electromagnetic fields. https://www.feynmanlectures.caltech.edu/II_21.html
- [S5] Z. H. Zhang, X. P. Geng, J. W. Hu and Z. H. Zhang, *Test of electric
  charge conservation in dark matter direct detection experiments*, Physical
  Review D 112, 035032, published 2025-08-20; original research analysis.
  https://doi.org/10.1103/trv7-c28m

The physical requirements in the first section are sourced. Operational board
labels, proposed gates, error metrics and feasibility judgments above are this
project's research proposals, not conclusions of those sources.
