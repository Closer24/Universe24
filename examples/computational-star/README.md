# Computational star: measured vector processing delay

This is a **delay-only experiment**. It deliberately has no interaction,
coupling, spatial coupling, momentum update or field-dependent routing.
The engine is unchanged. It tests processing delay, not a supplied force law.

## Configuration

The reusable package separates environment, definitions, initial placement and
run controls. The open world is 64 x 64 x 64. A held 27-site cluster consists of
one mass 1,000,000 and 26 masses 10,000. Each of three independent probes has
mass 4, so the cluster/probe ratio is 315,000:1. These are abstract mass units,
not a calibrated star, self-bound object, coherent extended particle or solar model.
The held cluster supplies no pressure or internal stellar dynamics.

The source owns a scalar `cost_field` called `work`, plus an immutable vector
`load_axis=[1,1,1]`. Its last committed measured cost C emits

```text
computational_load = max(C - H, 0) * load_axis
H = ordinary_work = 64
```

This is an explicit source law using generic integer operations. The source
starts with work=0. Metering the emission machinery itself can bring its first
cycle above H; this is not a derived relation between rest mass and work.
The source reads its last committed measurement while a later proposal waits.

The three-component field propagates causally through the existing outward
channels, halves each component on a completed link using schema-2 integer
decay, and has finite external source allowances of 1,000,000 per component
per source. The allowance is not energy or mass funding. Vector orientation
is component data, not automatically an outward force vector or separate
delay per direction.

Processing the arriving field adds actual metered spatial work to a resident
carrier cycle. The existing uniform-cell timing law computes
`extra_wait = (max(1,ceil(C/B))-1)*link_ticks`, with B=64 and link_ticks=1.
The field itself retains fixed link timing; it is the carrier's commit that waits.
No host timing, interpolated trajectory or global force calculation drives this.

Probe momentum is fixed at (1,0,0). Routing reads only momentum; the constant
rate denominator is 4, matching these mass-4 probes. This is not a new generic
mass-to-speed law for arbitrary masses.

## Five controls and measured result

All five cases completed 128 ticks without fault.

| Case | Inner hops | Middle hops | Outer hops |
| --- | ---: | ---: | ---: |
| Active measured load | 7 | 29 | 32 |
| No emission | 32 | 32 | 32 |
| Smaller source masses only | 7 | 29 | 32 |
| Reversed load vector | 7 | 29 | 32 |
| Scheduling budget 100,000 | 32 | 32 | 32 |

The inner probe's largest measured cycle cost was 602, versus 8 without the
field. It experienced 97 elapsed ticks of extra waiting by tick 128; the sum
of scheduled waits is 99 because the final proposal remains pending.
The middle probe experienced 12 extra ticks, and the outer probe zero.
All observed departure ports are +X in exactly the same prefix order as the
no-emission reference. **Motion slows but no trajectory bends or orbits.**

Mass and momentum are checked over resident and link ownership at every
observation. Every probe retains mass 4 and momentum (1,0,0).
All declared inventory errors are zero, including external field injection,
completed-link dissipation and open-boundary escape. This does not define a
conserved physical energy for the computational field. Constant probe mass
and momentum imply a constant Newtonian kinetic proxy, not a closed system
energy law.

The small-mass control changes every source mass to 4; probe positions,
departure times, local costs and recorded field states remain exactly equal
to the active case. The vector-reversal control negates the field while
preserving all probe timing and positions. These comparisons confirm a
critical limit: **neither mass magnitude nor vector sign is itself processing
work in this model**. The large mass ratio is configuration data, not an
explanation of the observed delay.

The high-budget control changes B only; H stays 64. It tests scheduling
capacity with a fixed emission threshold. Its source measurement cadence can
also differ, so it is not claimed to expose an identical field history.

## Reproduction and evidence

```console
python examples/computational-star/audit.py --output /path/outside/source/delay-study --workers 3
python examples/computational-star/verify.py --input /path/outside/source/delay-study --output /path/outside/source/delay-verification
python examples/computational-star/render.py --input /path/outside/source/delay-study --output /path/outside/source/delay-movie
```

The exact runtime JSON, every-tick recorded state, departure and cycle evidence,
inventory errors and physical event digest are saved per case. `verify.py`
checks complete cases and exact mass/sign controls, and separates elapsed from
scheduled waiting. An earlier audit output calls the latter `extra_wait_sum`;
the verification report gives both explicit quantities. `display.json`
controls sampling, playback, image size, view window and camera rotation.

The GIF is a recorded global audit view of a zoomed region, not an image
constructed from signals received by a physical local observer. Purple marks
show the magnitude of the measured vector field on Z=32. Momentum arrows are
unchanged even while a record waits. Hollow probes show the no-field control.
Marker sizes are illustrative. The three probes are separate trajectories;
their different progression must not be called rotation of one bound object.

The source base is `7074e2c4490486f8524d687557af70579521da0a`; active-engine
fingerprint is recorded in output metadata. The candidate uses the unmerged
experiment-package stack, not a claim that a newer main was run.
The independent pulse regression additionally shows costs 5 versus 106 at
B=80, shifting departures from ticks 3/7 to 4/8 with identical +X ports.

## Interpretation and retained rule

For computational-gravity tests requested as delay-only, do not add a direct
momentum-changing field, feed load into the routing direction or prescribe
an orbit. Any claimed path curvature must be demonstrated from the specified
local mechanism. Uniform waiting of an isolated whole record does not supply
that mechanism. A directional timing law or coherent extended disturbance
would be a separately defined model extension, not something established here.

Boss, simulation-runner and physics-rule-validation were reviewed; their
existing evidence requirements apply unchanged. Field-development retains
the scoped no-force rule and links here. The older star-cluster example remains
historical evidence for a different, explicitly momentum-changing candidate.
