# Paper draft

`main.tex` is the manuscript draft for Reality Theory (Universe24). It cites
only measurements recorded in [validation](../docs/VALIDATION.md) and the
experiment reports under [examples](../examples). Build with `pdflatex main.tex`
twice. The draft is not part of the simulator package and no test reads it.

`figures.py` draws the seven figures from recorded summary files only (the
interference, phased-ray Bell, crossing-null, bonded-probe and bonded-sweep
summaries);
`figures/` holds the PDFs it wrote from the runs recorded in the validation
log. Regenerate with:

```sh
PYTHONPATH=src python paper/figures.py --interference artifacts/causal-interference/summary.json \
  --bell artifacts/kerengonen-bell/summary.json --crossing artifacts/crossing-nulls/summary.json \
  --bond-sequence artifacts/bell-chsh/summary-bond.json \
  --bond-uniform artifacts/bell-chsh/summary-bond-uniform.json \
  --bond-biased artifacts/bell-chsh/summary-bond-biased.json \
  --bond-sweep artifacts/bell-chsh/summary-bond-sweep.json --output paper/figures
```

`redshift/main.tex` is the second manuscript, on the redshift from delay
growth; its two figures come from `redshift/figures.py` with the sweep
summary and the Hubble fit written by `examples/relativity-probes/redshift_sweep.py`
and `redshift_hubble.py` (the latter needs the public Pantheon+ table,
`Pantheon+SH0ES.dat`, which is not in the repository).

`arxiv_metadata.md` holds the titles, abstracts (within arXiv's 1920
characters) and category choices for both manuscripts, and
`release_notes_0.3.1.md` the notes for the matching GitHub release; both
are kept here so that a submission can be rebuilt from the repository
alone. The packages to upload are `main.tex` with `figures/` and
`redshift/main.tex` with `redshift/figures/`.

`general_formula/` is the third manuscript, the paper on the general
formula (the owner's decision of 2026-09-21: one paper only, on the map
**F** of the integer torus, every result as its consequence, the click
model as its measurement chapter; it was begun on 2026-09-20 as the
click-model paper, `paper/click_model/`, and the directory was renamed
with the decision): `main.tex` the draft, to be built with
`pdflatex main.tex` twice and uploaded with its `figures/`; `PLAN.md` the
decisions and the referee rounds; `RECORD.md` the long form of the first
plan; `NUMBERS.md` every number and its source; `checks/` the paper's own
computations from the designs' formulas with the repository's tables
(computations and not runs, their outputs beside them); `figures.py` and
`octahedron.py` the figure scripts. Every run the paper cites is in the
[experiments register](../docs/EXPERIMENTS.md); every formula is the
derivation's ([DERIVATIONS_BEAM.md](../docs/DERIVATIONS_BEAM.md)) with its
section number; papers 1 and 2 are not changed by it.

The figures of the third manuscript are drawn from the runs of series L
only: run the worlds, summarise them, draw.

```sh
PYTHONPATH=src python tools/run_series.py --jobs 4 --out runs/L examples/events/amplitude/*.json
PYTHONPATH=src python paper/general_formula/summarize_runs.py runs/L --output paper/general_formula/figures/summary.json
PYTHONPATH=src python paper/general_formula/figures.py --summary paper/general_formula/figures/summary.json --output paper/general_formula/figures
```

(`expectations.json` is not a world and is skipped by the runner's
parser; `slits_one` carries no key and is the reading's reference.)
`paper/general_formula/NUMBERS.md` maps every number of the manuscript to its
source; `figures/summary.json` carries the runs' fingerprint.
