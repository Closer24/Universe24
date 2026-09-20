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

`click_model/` holds the work toward version 2 of paper 1 (the owner's
decision of 2026-09-20: one manuscript, the click model as the fifth
candidate, submitted as a new arXiv version of paper 1; the record in
[Highlights 5.4](../docs/HIGHLIGHTS.md#54-the-detector), "DECIDED: the
paper is coordinated by a separate agent"): `PLAN.md` the two-page plan,
`RECORD.md` its long form with every argument and number, `checks/` the
plan's own computations from the
[amplitude-v1 design](../docs/designs/amplitude-v1/DESIGN.md) with the
repository's tables (`s_of_n.py`, the design's Bell value at every N;
`which_path_window.py`, a partial which-path window; computations and not
runs, their outputs beside them), and `main.tex` the draft of the new
sections (the model, the four theorems, the measurement table with design
placeholders, the literature), to be merged into `main.tex` above as
version 2 once `amplitude-v1` and its runs are on `main` and in the
[experiments register](../docs/EXPERIMENTS.md); no number is cited before
it is registered.
