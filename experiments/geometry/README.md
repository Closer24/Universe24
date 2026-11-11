# Geometry experiments

Default Einstein evolution is installed in `universe24.layers.adm` and runs with `python -m universe24`. The `adm_*` files are compatibility entry points. `full_gr_audit.py` is an independent symbolic observer. Existing fixed-six pp-wave, geodesic and Palatini experiments remain unchanged. Earlier variable-divisor PR27 wave benchmarks are archived under `docs/archive/pre-fixed-six/pr27`, not reactivated.

See [the main README](../../README.md), [equations](../../docs/INTEGER_ADM.md), and [event board](../../docs/UNIVERSE24_EVENTS.md).

## Frame48 research candidate

`python experiments/geometry/frame48_audit.py` runs the new horizon-independent
48-channel nonlinear frame-map experiment. Its exact inverse passes; general
Einstein validation, resolution, nondegeneracy and physical-clock gates remain
false. [Research, equations, literature and handoff](../../docs/FRAME48_RESEARCH.md)
include both successful and negative controls. It does not replace the ADM CLI.

## Compact null-covector experiment

`python experiments/geometry/compact_null_wave.py` runs a separate two-channel
profile model and compares its exact coframe histories and metric against the
existing pp-wave experiment. The output includes the complete `(a,b,r)` trace
and channel manifest. See [the algebra, comparison scope and negative controls](../../docs/COMPACT_NULL_WAVE.md).

## Integrated research components

The eight-channel `compact_flrw.py` experiment adds a distinct homogeneous
dust/radiation sector with sourced geometry, proper time and a null affine
counter. Its fixed tensor has no construction-time horizon. It does not
replace the general ADM model. See [the exact recurrence and clock conventions](../../docs/COMPACT_FLRW_CLOCKS.md).

The transported probe and its negative common-metric controls from PR #31 are now included. Run `python experiments/geometry/transported_probe_clock.py`; replay the original evidence with `--replay runs/transported-probe/checked.json`. `python -m universe24 --probe-experiment --L 5` allocates this test chart alongside Einstein in one Engine, with isolated channels. It does not supply the physical board metric. See [UNIFIED_SYSTEM.md](../../docs/UNIFIED_SYSTEM.md).
## Coupled frame, complex scalar and dust

`python experiments/geometry/frame_matter_audit.py --out runs/frame-matter`
exports the experimental 70-channel coupled tensor, complete replay traces
and source-hashed evidence. See [the algebra and physical gates](../../docs/FRAME_MATTER.md).
It proves exact reversible execution and nonnegative encoded dust density;
general Einstein constraint propagation, refinement and operational clocks
remain unvalidated. The default ADM event-board geometry is unchanged.
