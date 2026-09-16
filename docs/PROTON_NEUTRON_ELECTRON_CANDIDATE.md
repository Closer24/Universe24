# Contact-bound nucleus and circulating electron: numerical pilot v1

Status: **prospective, untested candidate**. This design precedes behavior
implementation. Base: local `c10af8ff92d4f9db2d8562bbffb2b2974188999b`, published
as `8d74f809a168c3f46653373e79ed14062789ad9f`. Model identity:
`contact-bound-ray-electron-pilot-v1`. The user authorized this new hypothesis;
it is not a claim that the following operators were already implied by the
central specification. That specification's reviewed 2026-09-16 paragraphs
P00125-P00129, P00168, P00313-P00317 remain relevant structural requirements.

The first target is a real recorded run with two retained nucleon identities
at one Node because of an explicit contact binding gap, and a charged carrier
that responds to a causally delivered field. Whether the carrier circulates,
escapes or falls inward is an experimental result. No desired path, radius,
return time or inward-pointing global coordinate enters an update.

This is a **classical, open-field, coarse-grained numerical pilot**. It is not
QCD, an isolated energy-closed atom, an electronic eigenstate, or a quantitative
deuterium prediction. Nuclear contact-energy closure is required separately
from the unclosed electronic/radiation dynamics. The three software owners are
physics/mathematics for this law, architecture for its bounded composition, and
configuration developers for the pair and electron builders. The related
[acceptance map](NUCLEAR_ELECTRON_ACCEPTANCE.md) remains open beyond this scope.

## Physical references and the interpretation of motion

[CODATA 2022](https://physics.nist.gov/cuu/Constants/Table/allascii.txt) gives
`a0 = 5.29177210544e-11 m`, `alpha = 0.0072973525643`, and
`m_d/m_e = 3670.482967655`. Its tabulated central rest energies imply
`(m_p + m_n - m_d)c^2 = 2.22456637 MeV`; this subtraction does not supply an
independent uncertainty because the input estimates are correlated. Nuclear
capture gamma measurements are an independent source for the binding gap:
[Van Der Leun and Alderliesten, 1982, ENSDF reference](https://www.nndc.bnl.gov/ensdf/DSfromRefServlet?kn=1982VA13&searchType=references).
The gap is a supplied calibration here, not a prediction of this contact law.

For the leading nonrelativistic two-body Coulomb reference, let
`mu = m_e*m_d/(m_e+m_d)`, `a_D = a0*m_e/mu`, and
`I_D = (mu/m_e)*13.605693122990 eV`. Independent evaluation gives
`a_D = 5.29321381547e-11 m` and `I_D = 13.6019873471 eV`. These are leading
Schrodinger values, not precision spectroscopy including relativity, QED,
hyperfine or nuclear-size corrections.

The eigenstate law is `psi_nlm(r,t)=phi_nlm(r)*exp(-i E_n t/hbar)` with
`E_n=-I_D/n^2`. A stationary state's spatial probability density does not rotate
like a marked classical point. The 1s radial probability peaks at `a_D`, its
mean radius is `3*a_D/2`, and it is spread over radii. Its overall energy phase
is not a directly observable orbital revolution; relative phases yield
transition frequencies `abs(E_n-E_m)/h`. A wave packet can have moving density,
and a state with angular momentum can carry current, without assigning a
unique classical path. See the independent
[MIT hydrogen eigenstate derivation](https://ocw.mit.edu/courses/6-974-fundamentals-of-photonics-quantum-electronics-spring-2006/8a3eb732190cc7fc2520fa122bed8dcd_hydrogen_atom.pdf).

Consequently a phase register is not required to test this pilot's classical
recurrence. It would be required, with a specified coherent operator and a
measurement, to claim quantum phase or transition-frequency agreement. Do not
add a cosmetic phase counter and call its frequency an electronic prediction.

## Units, fixed parameters and timing

| Parameter | Fixed pilot selection |
| --- | --- |
| Link time and length | `H=1` model tick and one neighboring Node; no SI tick is claimed |
| Additional output waits | All six `W_d=0`; prove the ordinary budget exceeds actual bounded work |
| Electron mass and transport scale | `m_e=512`, `S=16`, `D_e=S*m_e=8192` |
| Nucleon masses | `m_p=m_n=M=940032`; equal masses are a stated approximation |
| Contact gap | `B=669889164`, split as `gap=B/2=334944582` per constituent |
| Main electron preparation | Center-relative Node `(8,0,0)`, momentum `(0,2048,0)` |
| Leading comparison acceleration | `r_double_dot=-(1/2)*r/abs(r)^3`, a read-only continuum benchmark |
| Preparation | First 64 local carrier cycles hold the electron with response disabled; source field must arrive causally; then release the preparation constraint |
| Main domain and horizon | Open `41^3`, nucleus at center, 768 active electron cycles after preparation |
| Randomness | No Detector, no sampling, exactly zero random tickets |

The radius and momentum select an initial condition, not an attractor. The
continuum benchmark predicts `v=1/4` and `T=64*pi = 201.06192983` model ticks.
Its kinetic code `p dot p/(2*m_e)` is 4096. A comparison energy unit
`epsilon=I_D/4096 eV` maps this one kinetic value to the Bohr reference, and
`L=a_D/8` maps the preparation radius. The chosen gap is the nearest multiple
of 12 to `2.22456637e6/epsilon`, with approximately `0.0198 eV` encoding offset.
This is static input encoding, not runtime rounding.

Those optional length/energy comparisons **do not give the pilot a physical
atomic clock**: `v=0.25` relative to one-Link-per-tick causality is not
`v/c=alpha`. Simultaneously matching the chosen length, energy and inertial
mass would give Link speed approximately `4*alpha*c`, not `c`. Do not publish
the pilot period in physical hertz or silently rescale away this mismatch.

If circulation passes, the prespecified slower control changes `S` from 16 to
548 and multiplies every force impulse coefficient by `16/548`, with retained
exact division remainder. Keep momenta, preparation radii, masses and source
law fixed; lengthen preparation and horizon by `548/16` where appropriate.
Then initial `v/c_link=4/548`, close to alpha with a separately reported
representation error, and the continuum period is `64*pi*548/16`. This is a
regime control, not proof of electromagnetism or quantum mechanics.

## Bounded shared payload and ownership

Use ordinary immutable type definitions and same-type pair assignments. Do
not use `output_types` conversion or add a species branch to the engine.
Recommended shared field names (14 of the existing limit of 16) are:
`mass`, `charge`, `momentum`, `baryon`, `sector`, `bound`, `gap`, `radiation`,
`excitation`, `internal_direction`, `motion_remainder`, `hop_direction`, `age`,
and `charge_field`. A field may be absent from a type that does not need it.

Mass, charge and baryon count retain their existing meanings. `sector` selects
the admitted interaction lifecycle by properties: fresh unbound, bound, or
outgoing dissociation. Proton and neutron retain their two record IDs, unit
baryon counts and charges 1 and 0. `bound` is 0 or 1. The distinct owned
energies `radiation` and `excitation` are nonnegative. `gap` is immutable.
`internal_direction` is a retained signed unit axis of the admitted breakup
channel, not a physical momentum counted twice. Drift remainders and hop
direction are nonextensive transport state. Actual ray packets own emitted
radiation; pending proposals do not create another owner.

All payloads fit magnitude `2^30-1`; all products and sums are checked in the
existing working-register domain. Nuclear momenta in the admitted controls
are at most `2*M` per component. Reject unsupported masses, nonexact division,
overflow, unmatched ownership, occupied output capacity, unsynchronized pair
transport histories and unsupported profile composition before mutation.
No clipped value or discarded remainder is an accepted fallback.

## Effective strong contact operator

The admissible first capture is two fresh nucleon-sector records at the same
Node, with opposite `internal_direction`, total charge 1, two baryons, equal
mass M, zero synchronized transport history, and the declared attractive
coupling enabled. This is an unresolved point-composite model at atomic
resolution; it does not resolve a femtometer wavefunction or predict a nuclear
potential. Eligibility and energy thresholds, not names or a timer, select it.

Define `P=p_1+p_2`, `K=(p_1 dot p_1+p_2 dot p_2)/(2*M)`, and
`K_cm=(P dot P)/(4*M)`. The admitted baseline uses `p_1=M*ex`, `p_2=-M*ex`,
so `P=0`, `K=M`, and `K_cm=0`. Capture assigns atomically:

```text
p_1' = p_2' = P/2
bound_1' = bound_2' = 1
sector_1' = sector_2' = bound_sector
radiation_i' = radiation_i + (K - K_cm + B)/2
all other constituent properties and IDs retained
```

Every quotient must be exactly represented. The baseline result is zero
constituent momentum and `radiation_i=335414598`. The joint readout

```text
E_nuclear = sum_i [p_i dot p_i/(2*M) + radiation_i + excitation_i
                  - gap_i*bound_i] + emitted_radiation_energy
P_nuclear = sum_i p_i + actual_emitted_radiation_momentum
```

is unchanged. The initial value of `E_nuclear` is exactly 940032. This
identity is necessary at commit and over later emission, not just at planning.
It does not establish electronic energy closure.

The carrier transport mode remains move. With nonzero common momentum both
bound constituents move together using the same exact velocity/history; they
are not pinned to a coordinate. A mandatory boost control starts with
`p_1=2*M*ex`, `p_2=0` and captures to `p_1'=p_2'=M*ex`, moving at `1/16`
Node per tick. Keep its radiation/source tests separate if moving emission is
unsupported. An unsupported moving-emitter composition is a visible failure,
not a reason to discard one record or erase its history.

Captured radiation is finite and funded by that owned stock. At the first
admitted postcapture emission, each constituent emits six equal axial packets
of 55902433 units, one through each Port, debiting its entire radiation stock.
The six directions sum to zero, so opposite packet momentum/recoil cancels
locally under the selected normalized radiation convention. Packets arrive no
earlier than departure+H. These are configured computation/radiation packets,
not calibrated physical gamma quanta or a predicted radiative-capture rate.
Omit `recoil_field` only in this exact equal-six-axis case: its vector sum is
identically zero at each emission, while enabling it conflicts with the
electron's separate spatial momentum owner. An asymmetric emission needs a
new explicit recoil transfer and cannot use this exception.
If the existing funded ray interface requires separate phases, preserve these
amounts, ownership and once-only debit; do not replace this with an external
source. This radiation field is distinct from the open electric signal below.

### Dissociation and perturbation

A declared local excitation can pay to remove the gap and give an opposite
relative kick `+q*ex,-q*ex`. Required total energy is
`E_required=B+q*q/M`; the complete incoming/owned excitation is an actual
owner. Use exact representable q, first `q=0` and `q=M`. If funded, set
`bound=0`, enter outgoing dissociation sector, add opposite kicks to the common
momentum, and debit exactly `E_required/2` from each equal excitation owner.
Retain unused excitation. The q=0 threshold is B; q=M costs `B+M` and gives
outgoing momenta `+M*ex,-M*ex` from rest. Below threshold there is no change.
The first finite profile admits one capture and one dissociation; outgoing
sector cannot recapture before leaving. Repeated capture cycles are outside
this first contract and may not be silently claimed.

Controls may prepare these explicit local excitation owners in initial state;
that is a funded perturbation preparation, not a simulated photon cross
section. Any later arriving-energy extension must debit a real donor and
respect its Link transit. Mere elapsed time never releases or binds the pair.
The `B-1` negative control explicitly admits unequal excitation owners
`(B/2-1, B/2)`. Their insufficiency leaves both records unchanged; it is not
an invalid-input substitute for the negative physical control. The funded
q=0 and q=M controls use equal integer shares as specified above.

## Electron drift and local field response

The existing last-hop flux is the three-vector
`F=(a_+X-a_-X,a_+Y-a_-Y,a_+Z-a_-Z)` of causally arrived signed scalar rays.
No remote center or live source position is read. Select existing exchange
response with `delta_p=C*charge*F`; use the API's sign convention so a negative
carrier in outward positive flux receives an inward impulse. Deposit the
opposite change into the existing local momentum owner. It is part of the
configured combined momentum accounting, not identified electromagnetic
field momentum or an automatically delivered nuclear recoil.

The electric signal is produced only by the bound positive constituent. The
electron emits no field in this first test. Its source stock is openly
external under the existing source ledger. Thus stationary center motion in
the combined run follows initial P=0 plus omitted backreaction, not infinite
mass or a hidden anchoring operation. The separate boost and dissociation
controls establish that the nucleus itself is a movable binding candidate.

Use a fixed symmetric ray heading table and immutable emission cadence.
The developer may choose a bounded cubically symmetric table based on capacity
before any orbit run; publish its exact integer directions, ordering, packet
budget and independent source-isolation check as a preparation annex. Do not
change it after observing an orbit under this identity. A static calibration
probe and angular field checks below must precede orbital experiments.

Balanced routing that resets its quota whenever momentum direction changes
does not preserve changing-direction displacement. Instead select this new
generic owned remainder operation, expressed in existing sequential updates:

```text
R_trial = R + p
if max(abs(R_trial)) < D: d = (0,0,0)
otherwise: d = signed unit axis at largest abs(R_trial), ties X then Y then Z
R' = R_trial - D*d
hop_direction' = d
transport: one neighboring hop in d, or no hop when d=0
```

Here `D=S*mass` is fixed per admitted carrier. Preserve R through every change
of p and every ordinary movement; no normalization, division rounding,
direction-change reset or target-orbit condition is allowed. Expressions may
use the preexisting generic abs, comparison, max, component, vector, integer
multiply/add/subtract operations. The implementation must fit AST bounds; it
must not add a second formula owner in the engine.

Require `sum(abs(p))<=D` before this operation. At most one Link starts in one
update. From R=0, `sum(abs(R))<3*D` holds inductively: a no-hop step has all
three components below D; a hop subtracts D from the absolute sum after an
increment of at most D. This bounds stored remainders even when two axes need
service. The telescoping identity `D*sum(d)=sum(p)+R_initial-R_final` holds
exactly for the executed drift updates. It gives a bounded position-code
error, not a claim that in-flight carriers receive unarrived forces. Frame
analysis must use actual completed transitions and state which drift cycles
were executed. No multiple-Link same-tick catch-up is permitted.

### Calibration fixed before orbital outcomes

Prepare source-only rays and a held, nonreacting diagnostic at radius8. Use
the exact completed-cycle mean outward X flux `F8` after causal startup over
one complete immutable source cycle; preserve the rational numerator and
denominator of that mean. Set `C=64/F8`. This is the one calibrated coefficient:
the comparison law requires an initial radial impulse of 64 momentum codes
per cycle at radius8. If F8 is zero or changes without a finite repeatable
source period, this source choice fails preparation; do not invent a result.

Then freeze C, source table, emission, S, bounds and horizon. Before releasing
the electron, independently sample all six axis points at radius8, oblique
points `(6,6,0)` and `(4,4,4)` with their actual radii, and radii4 and16.
Report magnitude,
direction and inverse-square discrepancies. A radial-force approximation
passes only if axis magnitudes agree within 5%, oblique radial magnitude is
within 25% of the continuum reference, tangential fraction is at most 25%,
and radius4/16 radial magnitudes are within 25% of the expected factors4 and
1/4. A failing field can still be run once for a diagnostic GIF, but cannot
be reported as validated Coulomb motion. Corrections need a new design version
and preserve the failed evidence; never fit the coefficient to a trajectory.

## Prospective acceptance and negative controls

| Test | Independent expectation / failure |
| --- | --- |
| N0 disabled strong coupling | Same initial opposite nonzero nucleon momenta leave the common Node; no capture radiation, no binding flag |
| N1 capture and funding | Same two IDs co-resident; p=0 each, radiation335414598 each before funded emission; total E940032 and P0 throughout; one emission batch only |
| N2 moving pair | `(2*M,0)` momentum pair captures to `(M,M)` and translates together with unchanged P; no pin/hold law |
| N3 gap | Excitationtotal `B-1` cannot dissociate; B with q0 can change to free sector without new kinetic energy; `B+M` with qM yields opposite momenta and separation, exactly paid |
| N4 symmetry/errors | Relabel particles/properties consistently and rotate axes; mapped traces agree. Overflow, nonexact division and replay cannot duplicate/debit inventory |
| E0 no coupling | Electron momentum constant, exact drift telescoping identity; no artificial closed path; six axis rotations and a changing-momentum pure-update control |
| E1 no prearrival | No field response before the first physically admissible arrival; every ray crosses one Link in H; no same-tick cascade |
| E2 candidate circulation | During768 active cycles, radius stays in `[4,12]`, no boundary escape, and at least3 positive-orientation section crossings occur after a full winding; first three full revolution intervals are each within25% of201.06193, and differ pairwise by at most20% of their mean |
| E3 perturbation | Repeat with initial tangential momentum `7/8` and `9/8` of2048; retain the same laws and report finite binding, peri/apoapsis and precession; a failure is retained, not repaired by coefficient fitting |
| E4 domain and orientation | Translated61-cubed run shares the41-cubed causal prefix before boundary influence; axial rotations and reflection preserve mapped predictions within stated lattice error |
| E5 nonunique classical radii | If E2 passes, use R18 with pY4096/3 (explicit exact representation or preregistered input-error bound), then R32 with pY1024; predictions are T216*pi and512*pi. Longer horizons and domains follow those values, not observed periods |
| E6 slow regime | If E2 passes, use S548 and force factor16/548 as specified above; report source/retardation and lattice differences, with no physical-frequency claim from the fast pilot |
| D0 draws | Every candidate and control has exactly zero random tickets; no Detector is synthesized from a ordinary response |

For E2, release at the initial positive-X section with positive tangential
momentum is endpoint `t0=0` of the active observation. Let t1,t2,t3 be the
successive same-oriented section returns after one, two and three completed
windings. The three intervals are `t1-t0`, `t2-t1`, and `t3-t2`. Do not count
the initial section twice or demand a fourth return to obtain three periods.

The radius-band test is a finite engineering target, not a proof of infinite
stability. Winding/section extraction is a read-only world/event audit; it is
not a simulated Detector. A recurrence of position alone is weaker than full
state recurrence. Record full carrier momentum/remainder at section crossings
and report their mismatch separately. Do not call a missing return zero
frequency; its measured frequency is unavailable.

The classical continuum benchmark has a family of circular orbits with
`v=sqrt(kappa/r)` and `T=2*pi*sqrt(r^3/kappa)`. Roots and pi belong only to
this independent analytic readout, never ordinary physical updates. A single
stable numerical trajectory cannot establish a uniquely necessary radius or
frequency. A comparison with quantum deuterium would require independently
measured localization, energy levels and coherent relative phases beyond this
pilot.

## Evidence, output and publication

Publish this design and the architecture annex before behavior changes. The
pair builder returns a valid pair-only initialization; the electron builder
deep-copies it and appends fields/rules without changing the pair contract.
One writer owns each builder. Recheck actual merged field count, bounded
operation cost, source preparation, parser support and fingerprint.

Use the canonical runner. Save actual initialization, events, states, scalar
acceptance data and the normal HTML visualization for every requested world.
Produce the requested GIF from those recorded frames, with visible model
identity, tick, nucleus constituent count, radius and candidate pass/failure.
No interpolation, artificial circular marker, hidden failed segment or
precomputed orbital path may replace measured motion. A stationary center
can display two identities inside one Node without drawing fake intranuclear
orbits. Rendering may project 3D onto a labeled plane; it cannot modify state.

Required closure remains: independent physics/architecture review, affected
checks, original failing controls, exact submitted source and owned inventories.
Successful capture and circulating motion close only this named finite pilot,
not strong-interaction derivation, weak physics, full atom energy closure or
quantum orbital spectroscopy.
