# Six-part physics audit

These read-only experiments investigate current main
`7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2`. They assemble existing laws and
declare counterfactual preparations; no production tensor, click decoder or
runtime is modified. Several successful checks demonstrate a failed physical
gate, so a zero process exit code is not a claim of Born/Bell/GR completion.

From the repository root, with validation dependencies installed:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python -m experiments.research.six_lens_clocks
python -m experiments.research.six_lens_clicks --out runs/six-lens/02-clicks
python -m experiments.research.six_lens_born --out runs/six-lens/03-born-algebra
python -m experiments.quantum.bell_cone_audit --out runs/six-lens/04-bell-experiments/engine-reference
python -m experiments.research.six_lens_bell --input runs/six-lens/04-bell-experiments/engine-reference --out runs/six-lens/04-bell-experiments/independent.json
python -m experiments.research.six_lens_complexity --out runs/six-lens/05-complexity-cycles/reproduced
python -m experiments.research.six_lens_integration --out runs/six-lens/06-integration/wiring
python experiments/geometry/frame48_audit.py --out runs/six-lens/06-integration/frame48
```

The clock audit has a fixed output path under `runs/six-lens/01-clocks/`.
The complexity audit intentionally stops selected feedback cases only after
a complete exact step exceeds the declared bit budget. Remainders and
complete initial/final data remain retained. The Bell checker independently
reads saved trial records and replays the external reference's random tickets.
It does not import the original scorer or supply Engine outcomes.

The [synthesis](../../docs/PHYSICS_GAP_SYNTHESIS.md) links six detailed reports,
limitations and prioritized acceptance gates. The compact checked evidence
is in `docs/evidence/six_lens_physics.json`; raw fresh runs stay under `runs/`.
The remote baseline is the study reference, not a promise that rerunning on
future code uses that same source. Compare the generated source hashes.
