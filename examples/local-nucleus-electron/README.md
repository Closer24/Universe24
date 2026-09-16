# Contact-bound nucleus and electron candidate

Status after the user's mechanism clarification: **comparison model only**.
The requested nucleus consists of trapped rays under the existing generic
coupling. This contact-gap implementation does not establish that mechanism
and must not be presented as the requested atom, even when its arithmetic and
finite controls pass. Preserve its runs under their original model identity.

This supplied classical pilot follows the published
[numerical hypothesis](../../docs/PROTON_NEUTRON_ELECTRON_CANDIDATE.md) and
[component/trace contract](../../docs/LOCAL_NUCLEUS_ELECTRON_ARCHITECTURE.md).
It is not a QCD derivation, closed atom energy model or quantum orbital law.
The strong and electron builders provide initialization dictionaries to the
existing simulator; observers and the GIF exporter do not evolve a second world.

Run the six nuclear controls with the project Python runtime:

```bash
PYTHONPATH=src python examples/local-nucleus-electron/run_experiments.py \
  --suite nuclear --output /absolute/fresh/nuclear-controls
```

Each control preserves its input, event trace, full per-tick `states.jsonl`,
final state, metadata and canonical HTML. Capture and radiation funding,
disabled coupling, synchronized motion and three excitation thresholds are
separate experiments. The zero-kick breakup changes the binding sector without
creating kinetic energy; spatial separation is required only in the funded
nonzero-kick and disabled-coupling controls.

The electron source must first pass through the separate
[frozen calibration procedure](ELECTRON.md). Supply its exact rational force
coefficient to the combined runner; there is no fitted default:

```bash
PYTHONPATH=src python examples/local-nucleus-electron/run_experiments.py \
  --suite electron --force-numerator NUMERATOR --force-denominator DENOMINATOR \
  --ticks 832 --output /absolute/fresh/electron-candidate
```

The combined world records every carrier state and the complete ownership
accounting each tick. Its HTML omits spatial packet maps to bound display size;
that omission is labeled in `run.json`. Full final state and causal field events
remain available. Field-calibration failure permits a labeled diagnostic run,
not a passing Coulomb or circulation claim. A shortened diagnostic cannot pass
the preregistered 768-active-cycle recurrence criterion.

`measurements.load_run()` reads these files without filling missing ticks.
Independent acceptance belongs in `acceptance.py`; it must not tune parameters
or repair a failed trace. Relevant implementation tests are
`tests/test_local_nucleus_strong.py`, `tests/test_local_electron_configuration.py`
and `tests/test_state_trace.py`.

To render an actual recorded candidate using a read-only Python installation
with Pillow:

```bash
python examples/local-nucleus-electron/render_gif.py \
  --html /absolute/run/run.html --electron electron --nucleons proton neutron \
  --output /absolute/result.gif
```

The GIF uses recorded integer ticks and actual Node/Link owners. Two nuclear
glyphs inside one Node are display offsets, not intranuclear orbits. Playback
loops, glyph offsets and viewing speed provide no physical period measurement.
