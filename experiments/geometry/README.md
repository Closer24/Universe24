# Geometry experiments

Default Einstein evolution is installed in `universe24.layers.adm` and runs with `python -m universe24`. The `adm_*` files are compatibility entry points. `full_gr_audit.py` is an independent symbolic observer. Existing fixed-six pp-wave, geodesic and Palatini experiments remain unchanged. Earlier variable-divisor PR27 wave benchmarks are archived under `docs/archive/pre-fixed-six/pr27`, not reactivated.

See [the main README](../../README.md), [equations](../../docs/INTEGER_ADM.md), and [event board](../../docs/UNIVERSE24_EVENTS.md).

## Compact null-covector experiment

`python experiments/geometry/compact_null_wave.py` runs a separate two-channel
profile model and compares its exact coframe histories and metric against the
existing pp-wave experiment. The output includes the complete `(a,b,r)` trace
and channel manifest. See [the algebra, comparison scope and negative controls](../../docs/COMPACT_NULL_WAVE.md).

## Integrated research components

The transported probe and its negative common-metric controls from PR #31 are now included. Run `python experiments/geometry/transported_probe_clock.py`; replay the original evidence with `--replay runs/transported-probe/checked.json`. `python -m universe24 --probe-experiment --L 5` allocates this test chart alongside Einstein in one Engine, with isolated channels. It does not supply the physical board metric. See [UNIFIED_SYSTEM.md](../../docs/UNIFIED_SYSTEM.md).
