# Electron and frozen-source implementation

`electron_configuration.add_electron(document, parameters=...)` deep-copies the
strong initialization. Required integer parameters are `force_numerator` and
`force_denominator`, obtained from the independent static calibration. An
explicit zero coefficient is a free control. Defaults are mass512, speed_scale16,
launch_age64, radius8, momentum(0,2048,0), source_enabled1. The four vector motion
properties and age are nonextensive whole-carrier state. With the ten nuclear
properties and the electric stock, the combined schema has exactly16 fields.

The numerical, motion and source contracts were published before implementation
in PR156, designa0b037de and source742eb3d. The source checksum and all source
geometry are frozen in `docs/ELECTRON_RAY_PREPARATION.md`. This version samples
the last delivered travel Port; it does not sample the carried heading vector.
The prior geometric review predicts anisotropy; that prediction is not a run.

Run `electron_calibration.py OUTPUT` with the project Python3.14 runtime and
`src` on PYTHONPATH. It executes the existing canonical runner for84 ticks,
preserves canonical HTML, and reads exact full-sweep flux windows from events.
`calibration.json` records the frozen coefficient, all probe sequences, static
field gate, source/initialization hashes, measured timing and zero-draw probe.
The field gate is an independent prerequisite. Failure does not authorize
retuning or a claim of orbital acceptance. A shortened diagnostic after failure
must say early stop and cannot support a radius/frequency conclusion.

The combined profile removes the closed nuclear-only global audit because the
electric source is explicitly open. The original strong pair invariants remain
unchanged. Opposite electron momentum is deposited in the existing local
spatial owner; this is not a closed electromagnetic energy or nuclear recoil law.

`tests/test_local_electron_configuration.py` supplies independent drift values,
changed-momentum and tie controls, rejection above the one-hop speed bound,
preparation age ordering, immutable extension checks and a canonical free world.
Actual frequency/localization acceptance belongs to the independent scorer and
uses recorded material owners, not display frames.
