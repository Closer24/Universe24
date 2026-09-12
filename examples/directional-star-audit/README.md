# Does directional waiting produce a star orbit?

**Result: no orbit in the tested carrier model.** Thirteen 128-cubed worlds,
256 ticks each, contain three reusable abstract profiles: light neutral,
heavy neutral and light charged. All 39 trajectories keep their momentum and
ordered routing direction. The radial encounter slows from 64 to 58 departures,
passes through the center and leaves. Near-offset and oblique passes do not bind.
No gravitational force, momentum response, collision or prescribed turn is used.

## Source and reproduction

The recorded audit integrates main `521b63567d186bab2fac982a1e1f9d0a592a73a5`
with the PR65 stack at `a646cbd1d1439a05369cd596789c40ff09268f67`.
Main contains the new separation of physical catalog metadata from explicit
representation profiles. Timing is the PR65 positive-projection candidate, not
the incompatible six-coefficient candidate in open PR57 or elementary engine PR62.
Observer configuration/runner merge conflicts were reconciled without changing
the timing, routing or field laws. Actual simulator source fingerprint:
`1e545b3f8a269e90a947bfacba82a14eede4ec5c6ef750d1e09d33127f8eff4c`.

The submitted branch also integrates the subsequent read-only validation update,
main `b0988512fa7f42a057c08dee7d6baa83cbf3eef7`. All thirteen parsed physical inputs
are byte-equivalent after normalized serialization, and the physical core, field
laws and simulation API are unchanged from the recorded integration. The recorded
source fingerprint above belongs to the actual runs, not the later host adapters.
Shared preflight now retains configured-topology checks for inline and external
observers. This integration does not replace the saved experiment evidence.

The [configuration builder](configuration.py) reuses the computational-star
experiment and the [three entity definitions](entities.json). Final inputs are
saved per case. The massive held cluster has 27 constituents and mass 1,260,000;
probe masses are 4, 4,000 and 4, giving ratios 315,000 and 315. These are
configured lattice units, not calibrated Sun/electron/proton dynamics. All probes
have the same declared quarter-hop rate. Charge is retained but no electric force
is enabled. The star has no solid surface or collision law in this experiment.

Use the project Python 3.14 environment, with `PYTHONPATH` pointing to its `src`:

```powershell
python examples/directional-star-audit/audit.py --output C:/temporary/star-audit
python examples/directional-star-audit/audit.py --near --output C:/temporary/star-near
python examples/directional-star-audit/wave_audit.py --output C:/temporary/wave-audit
python examples/directional-star-audit/render.py --input C:/temporary/star-audit --output C:/temporary/star-movie
```

Choose fresh writable output directories outside protected checkout ancestors.
Generated outputs use the standard 24-hour retention lease. [Display options](display.json)
affect recording presentation only. The GIF overlays three independent runs;
all three entity profiles coincide within each run. It shows the active run's
recorded field slice, including waiting packets. It does not invent an orbit.

## Carrier measurements

All cases completed 256 ticks, without engine faults, momentum changes, incorrect
link transit, or linear inventory-balance errors. Inventory includes resident,
waiting, transit, supplied, escaped and dissipated quantities. Departures are
dispatch counts; they are not a continuum velocity or a physical energy test.

| Experiment | Closest scheduled route radius | Departures per entity | Outcome |
| --- | ---: | ---: | --- |
| Offset pass, active field | 4 | 64 | Leaves on the original line |
| Same pass, no directional waiting | 4 | 64 | Control |
| Same pass, no emission | 4 | 64 | Control |
| Star mass reduced to 108 | 4 | 64 | Same timing and field event counts |
| Reversed emitted vector | 4 | 64 | Different field waits, no carrier turn |
| Approach from opposite side | 4 | 64 | Leaves on the original line |
| Oblique approach | sqrt(5) | 64 | Original staircase direction |
| Radial approach | 0 | 58 | Slows, crosses center, leaves |
| Symmetric initial source orientations | 4 | 64 | No binding |
| Near pass: active, small mass, reversed vector, opposite approach | 2 | 64 each | No binding in four controls |

The radial world records six delayed carrier departures across the three profiles
and 14,223 delayed field departures. Offset runs record 13,981 field waits but
no delayed carrier departure: the field is short ranged and its arrival phase
matters. Seeing a field in a display does not prove a particular carrier sampled
nonzero resident load when its moving proposal began. Waiting field packets are
owned inventory but are not part of the timing law's resident-vector sample.

No closed covering-space path occurred. Open boundaries prevent a torus return
from being mistaken for an orbit. Polar angle is undefined at the center; the
radial crossing's angular diagnostic must not be interpreted as winding.

## Why waiting alone cannot turn these carriers

The generic movement law chooses the port from the carrier's owned routing inputs
before the engine attaches directional waits. For fixed nonzero momentum p,
each permitted cardinal step has p dot d > 0. Therefore p dot x strictly increases
per hop, independent of waiting duration. A bounded closed orbit is impossible
under these assumptions. This is a consequence of this representation and law,
not proof that all possible local wave/time models cannot exhibit refraction.

## Confirmed wave composition failure

The separate wave audit uses the existing six-mode local reflection candidate,
an open 33-cubed world and one seed with E=(0,1,0), B=(0,0,1), using its standard
integer amplitude scale. Optional load=(2,0,0), divisor=1 delays +X departures.
Q sums the squared mode amplitude over every resident and waiting/transit owner.

| Case | Initial Q | Q at tick 7 | Q at tick 12 |
| --- | ---: | ---: | ---: |
| Original timing | 549755813888 | 549755813888 | 549755813888 |
| Enabled law, zero load | 549755813888 | 549755813888 | 549755813888 |
| Directional waiting | 549755813888 | 541165879296 | 489177481216 |

The final difference is -11.019134521484375%. No engine error is raised.
Independent review reproduced the first -1.5625% change at tick 7 and isolated it
to four actual delivery merges. At each, retained and incoming same-mode
amplitudes +32768 and -32768 cancel, changing Q by -2 * 32768 squared.
Their exact cross-terms explain the complete global loss. The generic engine
preserves linear component addition; the synchronous reflection model's global
quadratic invariant is not inherited by asynchronous arrival merging. Its local
reflection guards run after this loss and cannot detect it. Q is not established
physical electromagnetic energy.

## Bugs, limitations and required code/model decisions

1. **Asynchronous wave composition needs a contract.** Preserve separately owned
   arrivals in bounded temporal/mode state and define a norm-preserving local
   operation, or explicitly reject this candidate combination. Add the tick-7
   counterexample as acceptance coverage. Do not normalize the state afterward.
2. **Whole-carrier orbit dynamics are absent.** A configuration-only wait cannot
   bend the current fixed-direction record. Testing emergence without an inserted
   force needs a localized, stable distributed excitation whose propagation and
   measured position can change under the existing local dynamics. Such binding
   has not been defined or demonstrated; no steering law was added here.
3. **Mass is not computational work.** The emitted load reads measured cycle work
   above a threshold; it does not read mass. Scaling a stored mass value does not
   change the number of elementary operations. A mass-dependent workload must be
   separately defined and measured before calling this a stellar gravity model.
4. **Vector orientation is not automatically radial.** Outward transport preserves
   payload components. Emitting (1,1,1) supplies a preferred orientation, not a
   vector that points radially at each receiving node. The symmetric source-axis
   control does not establish a radial metric or an orbit.
5. **Composition/integration gaps remain explicit.** PR65 rejects moving emitters,
   spatial responses, native events and SI calibration. Its schema conflicts with
   open PR57's different timing law. The two cannot be silently combined as one
   model. Origin-wide backpressure also stalls later fast-port batches and can
   change source cadence; this is the current policy, not a discovered force.
6. **Exported schema omits the inline observer.** Adding
   `"observer": {"position": [0, 0, 0]}` to `examples/basic.json` passes shared
   preflight but is rejected by the packaged runtime JSON Schema as an additional
   property. The PR58 observer and PR56 schema need a shared schema definition
   and cross-validator acceptance coverage. The observer-free audit inputs are
   unaffected. This report records the gap rather than expanding the schema here.

The simulator's physical laws were not changed to force a successful result.
The run Skill already requires negative controls and source-specific evidence;
the field-development Skill already prohibits inserted steering in this task.
No new Skill is needed. The recorded counterexample and this report provide the
next implementation acceptance case.
