# Conservative transverse directional-wave candidate

`conservative-transverse-directional-wave-v1` defines directional propagation and
a conditional polarization interaction through ordinary initialization rules.
Energy and momentum have explicit normalized definitions and exact local guards.
This is a candidate field law, not established Maxwell dynamics. The catalog's
earlier E/B copy profile remains unchanged.

## Local contract

The [law](../examples/directional-wave/law.json) owns six signed three-vectors
`a_px, a_mx, a_py, a_my, a_pz, a_mz`. Each belongs to one cardinal travel direction
`n_p` and satisfies `dot(n_p,a_p)=0`. Names are configured references; the engine
has no directional-wave or electromagnetic name dispatch.

| Part | Contract |
| --- | --- |
| Input | Six resident mode amplitudes, including completed neighbor arrivals |
| State | Six vector fields with zero baselines; no source identities or history |
| Validation | Clamp components to the declared bound, project transverse, and require the original a_p unchanged |
| Encounter | If both opposite modes are nonzero, simultaneously assign `a_p := n_p cross a_p` to both |
| Streaming | Clear each retained mode and send it through its configured cardinal port |
| Transit | Exactly `link_ticks` per nearest-neighbor transfer |
| Scope | Periodic, source-free fields without carriers or dissipation |
| Capacity | Six fields, five rules, at most twelve assignments/invariants per rule |

Validation is an identity on transverse input. Longitudinal input fails the
unchanged-value guard atomically, including solitary seeds; no component is
silently removed. The three opposite-pair encounter rules are disjoint and commute.

The candidate restricts each amplitude component to absolute value at most
536870911, half the engine's positive payload maximum rounded down. A quarter-turn
changes a component by at most twice this limit, so the transformation ledger fits
the existing bound. Per-mode squares and local guard subtotals fit checked 64-bit
work. Validation requires the clamped projection to equal the original value;
oversized input is rejected atomically rather than silently clamped. Tests include
all six modes at the limit and rejection just above it.
A solitary mode propagates without changing polarization. The interaction rotates
polarization, not trajectories. Unequal opposite streams cannot simply be turned
sideways while preserving their nonzero momentum without additional owners.

## Energy, momentum and derived readouts

For actual resident and in-flight mode owners, define:

```text
U = sum_p dot(a_p,a_p)
P = sum_p n_p * dot(a_p,a_p)
E = sum_p a_p
B = sum_p cross(n_p,a_p)
```

U and P are the candidate's normalized wave energy and momentum. A momentum unit
corresponds to an energy unit divided by that run's link speed; no SI calibration
is supplied. E and B are local derived readouts, not additional owned stock.
[definition.json](../examples/directional-wave/definition.json) records the
channel identities, readout definitions and assumptions.

Each changing rule checks per-mode U and P including retained stock and **all six
outgoing owners**, with each outgoing term weighted by its actual port. These
guards detect amplification and misrouting before node commit. Their sums preserve
the declared U and P. Source-free fixed-port streaming gives each mode one unique
predecessor, avoiding uncontrolled merging from different directions. Received
samples are views of already-owned stock, never extra energy. Polarization can
change linear component sums; the ordinary transformation ledger records that.

For `a_+X=3Y, a_-X=2Y`, U=13, P=5X and the initial overlap has E=5Y, B=Z.
The encounter produces `a_+X=3Z, a_-X=-2Z`, hence E=Z, B=-5Y with unchanged U/P.
For a single transverse opposite-axis pair, the algebraic identities
`U=(dot(E,E)+dot(B,B))/2` and `P=cross(E,B)` hold in this normalization.
They do not hold generally for summed readouts across several propagation axes.
For example, `a_+X=a_-X=Y, a_+Z=a_-Z=-Y` has E=B=0 but U=4. Displays must retain
mode/energy visibility at such nodes. No unique physical packet decomposition is
asserted.

Coincident initial modes preserve their directions even when E or B cancels.
There is no sign-of-cross launcher. This resolves that earlier packet launcher's
ambiguity; it does not prove that all aggregate E/B formulations are insufficient.

## Configure once and reuse

[experiments.json](../examples/directional-wave/experiments.json) places the named
modes and selects duration, shape, link time and whether to enable encounters.
The law is defined once. Preparing a run only assembles ordinary JSON; changing
configuration does not compile or rebuild the simulator.

```sh
python examples/directional-wave/prepare.py --case approach_unequal --output artifacts/wave-input.json
python -m event_universe --init artifacts/wave-input.json --output artifacts/wave-run
```

Cases: `approach_unequal`, `free_unequal`, `coincident_electric`,
`coincident_magnetic`, `six_way`, `periodic_seam`. Use new output paths and add
`--visualize` only when recording is wanted. The ordinary HTML exposes actual
mode fields. [observe.py](../examples/directional-wave/observe.py) reads copied
state for U/P and E/B without advancing or repairing the world.
[display.json](../examples/directional-wave/display.json) controls the example GIF's
nodes, axes, readout/mode/travel arrows, camera, dimensions and playback timing.

To reproduce the comparison, install the project's optional `render` dependencies,
then run from the repository with `src` on `PYTHONPATH` (or an editable install):

```sh
python examples/directional-wave/prepare.py --case free_unequal --output artifacts/free-input.json
python -m event_universe --init artifacts/free-input.json --output artifacts/free-run --visualize
python -m event_universe --init artifacts/wave-input.json --output artifacts/encounter-run --visualize
python examples/directional-wave/verify.py --recording artifacts/free-run/run.html
python examples/directional-wave/verify.py --recording artifacts/encounter-run/run.html
python examples/directional-wave/render.py --reference artifacts/free-run/run.html --recording artifacts/encounter-run/run.html --output artifacts/wave-gif
```

The headless verifier replays every tick, checks U/P and compares every recorded
physical snapshot. It stamps the exact input, source, definition and recording.
The separate renderer accepts matching verified recordings whose configurations
differ only by enabling the saved encounter rules. It reads state without running
the simulator. Hollow glyphs mark actual in-flight owners when link time exceeds
one tick; they are display interpolation within that link, not resident nodes.
All output directories must be new; the renderer leases its output while writing.

## Acceptance and limits

[Tests](../tests/test_directional_wave.py) cover independent unequal-input values,
coincident pure-E/pure-B readouts, six simultaneous modes, a dark aggregate,
solitary motion, atomic longitudinal/amplification/misrouting rejection, periodic
seams and returns, double transit time and even lattices. All 24 proper cubic
rotations use the **same law** with rotated initial positions, mode identities and
vectors; no field rule is rotated to make the comparison pass.

The conditional encounter is nonlinear; arbitrary superposition is not promised.
The quarter-turn is invertible on the admissible subspace; four encounters restore
polarization. Tests compare complete state at the same field phase after the
periodic circuit. This does not establish arbitrary-angle isotropy, spatial
mixing, Gauss constraints, charge/current continuity, Maxwell propagation,
Lorentz response, matter exchange or quantum photons. Those require separately
specified laws and independent acceptance evidence.
The newer native event program is absent here: its current contract explicitly
rejects composition with spatial fields until timing and ownership are specified.
