# Complete-ray finite residence

`finite-residence.json` supplies the `node-ray-coupling-v1` fixture defined in
[the published contract](../../docs/SHARED_RAY_COUPLING.md). It uses the common
indexed scalar/vector evaluator for complete native rays. Energy and vector
momentum are declared invariant expressions in the input.

Two funded emitters one Link from the center each supply five energy units and
their corresponding directed momentum. Supported emission recoil transfers that
momentum from each source to its ray, leaving both source momentum registers zero.
Their phase seven advances to zero on arrival. The common guarded heading
exchange assigns two local residence intervals, then phase evolution closes the
guard and both rays leave through opposite Ports.

| Completed world tick | Actual ray owners | Phase | Remaining local delay |
| --- | --- | --- | --- |
| 1 | Two center residents | 0 | 0 |
| 2 | Two center residents | 1 | 1 |
| 3 | Two center residents | 2 | 0 |
| 4 | Opposite adjacent Nodes | 3 | 0 |

All ten energy units and all momentum remain owned by emitters, resident rays,
Link packets or escaped inventory. No Detector or lottery is involved. This is
finite residence and release, not an emergent nucleus, an electron orbit or a
physical frequency. The configured phase recurrence is eight intervals. The
operator has outgoing channels and uses no contact binding flag.

Run the ordinary simulator with this explicit initialization. The experiment
runner adds independent controls and reads actual ray owners for requested
canonical HTML and GIF.

Structural projection properties are `amount`, `heading`, `phase`, `advance` and
`delay`. Indexed roles select configured spatial field names or required
properties. Only heading, phase and delay are writable. Native
`interaction_delay` remains separate from the pacing remainder. The first
implementation admits at most six roles and 32 selected ray slots, positive
unit-axial unpaced rays, the default fixed `H=1` clock, and Detector-only sampling.
JSON and typed `InitialState` callers use the same capability validation. Other
clocks, response/absorption of participating rays and other unsupported owner
combinations fail before the run; the claim and bond samplers this rule once
excluded were deleted on 2026-09-17.

With the project environment active:

```bash
PYTHONPATH=src python examples/generic-ray-coupling/compare_controls.py artifacts/ray-controls
PYTHONPATH=src python examples/generic-ray-coupling/render_gif.py artifacts/ray-controls/residence/ray-recording.json artifacts/ray-controls/residence.gif
```
