# Coherent cube waves: verified comparisons, failed CPU ceiling

All16 full-engine records satisfy the registered coherent-sector and finite-time
linear-comparison predicates. Independent replay confirms208 complete states,
192 transitions and all complete rewinds, raw arithmetic events, parity and Q
checks. **The resource protocol fails its CPU ceiling:** capture/analysis used
328.943 seconds against300, an overrun of28.943 seconds. The mathematical
comparison result and resource failure are separate outcomes; the original
result and receipt have not been rewritten.

The [frozen protocol](coherent_wave_protocol.json) has SHA-256
`c027015b1ecfa2f157ef2f54fb9564c21a507f055d287189f6d215d3447e44f0`.
The executed producer has SHA-256
`a18c8acd9edb29b55f9c6bf7b7cad7cd0b1aac06f11af981f861436fcdecc136`.
See [complete evidence](evidence/coherent_wave_v1/result.json),
[independent audit](evidence/independent_audit/coherent_wave_v1.json), and the
[explicit resource qualification](evidence/coherent_wave_resource_qualification.json).

## What the full engine evolved

Each periodic cube has side7 or9. Every site initially assigns the same triple
to all48 channels, with remainder2. Four separately prepared wave vectors
`n=(1,0,0),(1,1,0),(1,1,1),(2,0,0)` and two amplitudes N=1000 or100000 give
the16 cases. Every run contains states0 through12. No reduced field solver
evolves a native state: the unchanged full48-channel Rule3 engine performs all
updates and inverses under the same fixed +++ tensor.

For `k=2*pi*n/L`, the predeclared comparison frequency satisfies
`cos(omega)=(cos(kx)+cos(ky)+cos(kz))/3`. The target is
`cos(k dot x-omega*t)`. Initial b and a are nearest-integer scaled target values
at0 and−1 respectively. An80-digit interval calculation certifies each unique
rounded integer before capture. Exact initial counters, interval witnesses and
the pinned mpmath1.3.0 Python sources are retained. The independent auditor
reconstructs those values using a separate120-digit direct-cosine calculation.

The cubes are occupied by dense global periodic fields. This is neither a
compact freely propagating packet nor a superposition test: four modes are
prepared in separate runs. The exact coherence theorem concerns this invariant
sector; robustness to channel-asymmetric perturbations is a different test.

## One comparison law across the family

The [mathematical derivation](coherent_wave_algebra.md) gives a linear comparison
with exactly matched rounded initial counters and normalized error bound
`RMS <= t*(t+1)/(3*N)`. The experiment checks its squared form using integers
only, with no tolerance or fitted frequency. For the ideal unrounded cosine
mode, interval arithmetic checks the separate rounding-inclusive envelope
`(2*t+1)/(2*N)+t*(t+1)/(3*N)`, plus a fixed numerical slack of1e−50.
All13 frame checks pass in every case.

| Cube side | Wave vector | Maximum rounded-initial RMS, N=1000 | Maximum rounded-initial RMS, N=100000 |
| ---: | --- | ---: | ---: |
|7|(1,0,0)|0.000984036|0.00000830426|
|7|(1,1,0)|0.001116779|0.00000874701|
|7|(1,1,1)|0|0|
|7|(2,0,0)|0.000692735|0.0000113270|
|9|(1,0,0)|0.000810392|0.00000732950|
|9|(1,1,0)|0.001009061|0.00000748272|
|9|(1,1,1)|0|0|
|9|(2,0,0)|0.001128212|0.00000852865|

These maxima summarize the registered0..12 interval. The theorem bounds the
envelope by1/N; it does not demand monotonic empirical error for every pair of
amplitudes or an unqualified infinite-time limit. Zero error against the
rounded-initial linear comparison does not mean zero initial rounding error
against the ideal cosine. All actual guarded C events remain in the records;
the field RMS theorem does not by itself bound threshold click-time errors.

The conserved +++ account Q is checked as algebra, not identified with physical
energy or electric charge. Neither the derived gapless comparison branch nor
these finite native records establish photons, masslessness, Lorentz symmetry,
Born probabilities or the preferred-complexity hypothesis.

## Resource failure and reproducibility

Wall time329.164 seconds stayed below900, and83,484,377 retained bytes stayed
below128 MiB. All35 archived project sources match the executed live sources.
The CPU check ran between complete records; the final record's capture,
observation and serialization exceeded the remaining allowance. No case or
frame was dropped afterward, and no retrospective budget increase was made.
A future recorder must reserve a complete case's declared bound before
admission or safely retain an interrupted record. Such a computational stop
would be an incomplete experiment, never a physical selection operation.

From the repository root, prepare an isolated optional research environment
and use a fresh output directory:

```sh
python -m venv .venv-wave
.venv-wave/bin/python -m pip install mpmath==1.3.0
.venv-wave/bin/python -m research.clock_selection.coherent_wave --output runs/coherent-wave-new
.venv-wave/bin/python -m unittest tests.test_clock_selection_coherent_wave
```

Machine-dependent budget exhaustion remains an explicit possible outcome.
The original frozen run's CPU failure stays part of its evidence.

The [unchanged Presenter collection](evidence/presenter_coherent_waves/index.html)
contains all four L9/N100000 recordings, each with13 complete states and454,896
stored rows. Every experiment stays intact on its own bounded page. Reset view
shows the full cube; rotation changes the camera only. These full-volume fields
provide a different visible geometry from the narrow prepared guide used by
the writer/probe experiments.
