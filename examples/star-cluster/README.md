# Star-cluster encounter experiment

This configuration-only candidate asks whether the existing local scalar transport
and vector exchange support orbital motion. It is **not a validated gravity law**.
The engine is unchanged. Runtime input is ordinary JSON, assembled once from the
environment, definitions, initial conditions and run parts. No compilation is needed.

## Candidate and units

A held 27-site cube has central mass 2048 and 26 neighboring masses of 64,
total 3712. The probe has mass 64 (or 128 in the mass control). All quantities
use declared abstract lattice units; they are not kilograms, SI gravity or actual
stellar scales. A source emits its mass in scalar signal each resident interval.
The signal branches causally along cardinal links under the existing outward law.

A responding record exchanges `mass * delivered_signal_flux / denominator`
with local spatial momentum. The carrier loses the outward-directed vector and
the field receives its opposite, using the engine's integer remainder registers.
The denominator is 2048, or 512 in the stronger-response control. Motion uses
balanced routing with L1 momentum divided by mass. An L1 speed above one cell per
tick exceeds the causal link limit and is explicitly counted.

These operations are local. There is no host-computed distance force, global
orbit correction, hard-coded central potential or quarter-turn orbital rule.
The scalar source is external injection; local momentum stock is a reaction
owner, not a gravitational potential-energy definition. A held cluster is
externally supported. A live cluster has neither a pressure law nor a mechanism
that makes it a stable star. Moving sources emit only while resident.
The probe itself does not emit. Momentum deposited in the local field has no
forwarding or readback law: this is one-way attraction with exact accounting,
not demonstrated mutual gravitational recoil.

## Five families and eight variants

`matrix.json` declares radial infall, tangential orbit search, offset fast flyby,
inclined encounter and live-cluster response. Each has a base, half and double
initial momentum, doubled probe mass at the same initial p/m, a proper cyclic
axis rotation, reversed seed order, zero emission and stronger response.
Thus the audit runs 40 cases. Base cases allow 192 ticks; screening cases allow
48. An actual probe escape terminates the case. Reversed seeds test ordering;
they are not a reversed-time experiment. Rotation keeps the law fixed.

The boundary is open to exclude periodic return as a false orbit. The field
starts empty: startup is a declared transient, not a pre-existing static star.
The small 11-cube is a bounded screening experiment. A trajectory that escapes it
cannot establish behavior in an infinite domain.

## Acceptance and limits

Every completed tick checks all conserved inventories, including link ownership,
external source, reaction, dissipation and escape. Mass and combined momentum
must have zero error. Kinetic energy is only a read-only proxy; no total energy
conservation, capture energy or Kepler binding is inferred from it.

Positions are discrete actual resident or link-origin coordinates. For open
boundaries these need no periodic unwrapping. Co-residence is reported as contact;
no elastic collision or accretion law has been added. The signed angular advance
is projected onto the initial orbital plane. Two full revolutions without contact
or escape are the minimum for a *finite-time circling candidate*, not permanent
binding. Radial launch has no initial orbital plane. Live-cluster radii use the
declared initial center, so even a circling candidate would need a moving-barycenter
audit before any binary-orbit claim. An exception is retained as a runtime fault.
The classifier suppresses the orbit-candidate label for the live-cluster family.

A real Newtonian orbit requires suitable tangential velocity and energy.
An unbound two-body visitor does not automatically become captured; energy
exchange with another body or dissipation is needed
([NASA trajectories](https://science.nasa.gov/learn/basics-of-space-flight/chapter4-1/)).
These reference expectations do not feed the simulator.

Outward branching is not necessarily isotropic or inverse-square. In particular,
a shell average can look like inverse-square merely because the shell area grows.
Inspect directional delivered flux, deflection and rotated cases; do not substitute
a smooth radial glow for the measured field in the visualization.

## Run and evidence

From the repository root, with development dependencies installed:

```console
python examples/star-cluster/audit.py --output /path/outside/source/star-audit --workers 4
python examples/star-cluster/audit.py --output /path/outside/source/one-case --case tangential-base
```

Each case saves exact runtime initialization, trajectory, field slice, result,
event digest, inventory errors, delays and causal-speed warnings. The top-level
metadata records the active engine fingerprint and Python version.
The read-only renderer uses those saved states; it never reruns or changes physics.
Generated artifacts use the normal retention lease and stay outside the repository.

## Measured outcome (2026-09-12)

Engine fingerprint: `32b43d07936e674658eabe364e9b2b107b7ce39946dbd5f13d063e40fc6e2710`,
Python 3.14.7, source base `263c7be483516ef836f4bfd1056dac7222e55079`.
All 40 planned cases ran: 25 escaped, four ended the 48-tick screen after
cluster contact, and 11 explicitly stopped. No accepted orbit was found.

| Base family | Actual end tick | Observation |
| --- | ---: | --- |
| Radial | 35 | Reaches the center, passes through, then escapes |
| Tangential | 20 | Deflects, then escapes; 0.164 projected turns |
| Offset flyby | 18 | Deflects without cluster contact, then escapes |
| Inclined | 115 | Contacts the cluster; 1.956 projected turns, then escapes |
| Live cluster | 9 | Receiving capacity is exhausted as sources concentrate |

The longest winding in any screened case was 2.054 projected turns, but with
cluster contact: it is not an accepted orbit. These are projected angles, not
proof of a Kepler ellipse. Four short screens do not establish their later fate.

Five stops were excessive requested movement rates; six were receiving-capacity
exhaustion. The engine rejected them rather than clipping velocities or discarding
matter. All 11 were replayed with the same physical event digest and an explicit
check of the partially committed final state. Across all checked states, mass,
signal-source accounting and combined momentum error were exactly zero.
Maximum recorded local cost was 397293, below the configured budget; no additional
computational waiting cycles occurred.

The separate 32-tick field scan compares equal Euclidean radius 3, averaging
ticks 17 through 32. Axial radial flux is 54.75--55; permutations of (1,2,2)
give 35.1875--35.2292. This is about a 56% directional difference. As a
**host-only Newtonian reference**, summing the same 27 point masses with unit G
gives radial acceleration 401.5427 on (3,0,0) and 419.9250 on (1,2,2), only
about a 4.6% difference and in the opposite direction. The reference calculation
does not supply forces to any run. Cluster shape alone therefore does not explain
the measured candidate's angular pattern; this is not an inverse-square validation.

The unchanged seed-order control reproduces the base traces over matching
windows. Rotation and doubled mass are comparisons to inspect, not presumed
symmetries: the flyby exits at tick 18 in the base, tick 20 after cyclic rotation,
and tick 17 with doubled mass and momentum. Integer routing and field allocation
still affect the finite trajectories.

What is missing for the requested physical interpretation: a validated central
field law, mutual source/probe reaction rather than an inert reaction reservoir,
a closed energy law and a supported range below the causal-speed bound. A stable
star also needs internal support/contact physics. Simply grouping masses does
not provide these properties.

```console
python examples/star-cluster/field_scan.py --output /path/outside/source/star-field-scan
python examples/star-cluster/review.py --input /path/outside/source/star-audit --output /path/outside/source/star-reviewed
python examples/star-cluster/render.py --input /path/outside/source/star-reviewed --output /path/outside/source/star-movie
```

The review replays faulted cases and recomputes winding from saved trajectories;
it verifies the engine fingerprint and fault event digest. `display.json`
chooses the GIF cases, frame limit, timing, dimensions and camera turn.
Blue arrows show a measured Z=5 signal slice at four-tick sample intervals,
not all three-dimensional field stock. Lattice markers use a two-cell display
stride. Escaped cases freeze at their actual last frame. Rendering changes no run.

Boss, field-development, physics-rule-validation, simulation-configuration and
simulation-runner Skills were reviewed. Their existing law/hypothesis/evidence,
locality and recorded-output requirements cover this experiment, so no additional
Skill or procedural exception was needed.
