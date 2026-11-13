# Event-space energy and momentum audit

Status: local research candidate, not the installed law. The intended comparison
is between event spaces reconstructed from transfers and clicks. This interpretation
does not establish equivalence with Einstein spacetime.

## Mechanism and domain

The candidate uses the unchanged integer Engine with 960 cubic tensor terms.
Fingerprint: `8983c714df78c435aff2d2247af66509bb3a7c46d9390dcb870b2fa3423ca759`.
Its map is an onsite collision, one-edge streaming, and orientation turn.
The collision exchanges opposite occupied pairs (1010 and 0101).
There are still 48 retained channels, but central duplicate channels must agree:
only 24 occupation bits per node are independent. This is a restricted invariant
sector, not a replacement valid on the installed law's arbitrary Boolean domain.
No extra link memory is introduced. Every occupied bit still hops one edge per
update; this candidate does not implement variable link flight times.

## What passed

The actual Engine passed scalar evaluation, all 48 covariance checks, positive
integer states, exact rewind, total occupation Q and vector P conservation.
Local continuity of Q and all three P components passed 64 updates. A four-run
interaction control changed aggregate node occupation after two updates; the
matched free control had zero interaction contrast.

Let M = sum R_g z_g, v=(1,1,1), and P=Mv. Collision preserves M locally;
streaming preserves its global sum; the orientation turn gives M_next=M T.
The unwrapped hop flux satisfies J_t+J_(t+1)+J_(t+2)=P, independently checked
over 108 actual Engine updates. With A=(1,0,-1), channel-event coordinates
X=x+R_g A/3 also satisfy 3J + M_next A - M_old A = P each update.
These are global transport identities with a fixed channel-dependent coordinate
calibration, not a common curved node metric.

Postulating E=epsilon Q and p=epsilon P in units c_eff^2=1/3 supplies a
kinematic energy-current account. Epsilon is not derived from CPU work.
Three 12-update preparations gave Q^2-|P|^2/3 equal to 0, 16, and 32/3,
with conservation and exact rewind. A nonzero invariant for a collection does
not identify bound matter; opposed beams already have this property.

## Distribution result: overall acceptance failed

Fresh central-duplicate cohorts used seeds 61000–61015 at L=5, T=30 and
71000–71007 at L=7, T=42. Lower integrated squared occupation is better.
All 144 candidate/current/previous-candidate trajectories passed positivity,
occupation conservation and rewind. Relative to the installed law:

| Cohort | Better / equal / worse | Mean relative change |
| --- | --- | --- |
| L5, density 1/8 | 8 / 0 / 8 | +0.0842% |
| L5, density 1/2 | 8 / 1 / 7 | -0.0494% |
| L7, density 1/8 | 3 / 0 / 5 | -0.3211% |
| L7, density 1/2 | 8 / 0 / 0 | -1.3485% |

The dense L7 result is favorable, but improvement is not robust across cohorts.
The installed edge gate reduces to free transport on this duplicated sector;
results from the previous arbitrary-48-bit experiment cannot be transferred here.

## Bounded extension obstruction

An exhaustive orbit formulation examined full eight-bit same-face C8 gates
preserving Q and R_g(1,1,1) momentum, with bijective cubic forward and inverse
maps: 36 necklaces, 223 assignments, 398 equality constraints. Independent exact
rational reduction expresses physical redistribution score as
480(x209+x210+x212+x214). Rational dual certificates bound each listed variable
by 1/2; binary assignment forces each to zero. Thus this specific family cannot
redistribute physical orientation occupation. This does not exclude other
natural-number sectors, momentum definitions, or broader tensor families.

## Reproduction and remaining criteria

Local research sources and outputs are in `runs/momentum-law`,
`runs/momentum-tests`, `runs/momentum-algebra`, and `runs/momentum-root`.
They are ignored research work, not installed runtime modes. For example,
from this checkout run `PYTHONPATH=. python runs/momentum-root/event_account.py`.
The exact obstruction is audited by `certificate8.py` and
`certificate8_integral.py` in the algebra directory (SymPy and SciPy required).

A shared causal metric, local Lorentz behavior, proper clocks, stable species,
dark matter, gravitational waves and Einstein field equations remain unproved.
The finite set of free velocities has isotropic second moments but anisotropic
fourth moments. Conservation and calibrated global flux alone do not meet these
criteria. The installed tensor remains unchanged because the combined target
of physical transport accounting and reliable load spreading has not passed.
