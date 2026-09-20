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

`click_model/` is the third manuscript's directory, coordinated by a separate
session by the model owner's decision of 2026-09-20
([Highlights 5.4](../docs/HIGHLIGHTS.md#54-the-detector), "DECIDED: the paper
is coordinated by a separate agent"): `click_model/PLAN.md` holds the plan
(the one claim as recommended and as the evidence supports it, paper 3 against
a revision of paper 1, the formal definition, the four theorems, the
literature, the figures, reproducibility, the disclosure of AI assistance and
the venue), and `click_model/checks/` the plan's own computations from the
[amplitude-v1 design](../docs/designs/amplitude-v1/DESIGN.md) with the
repository's tables (`s_of_n.py`, its output `s_of_n.txt`: the design's Bell
value at every N), computations and not runs. The draft `click_model/main.tex`
is written only after `amplitude-v1` and its Bell runs are on `main` and in
the [experiments register](../docs/EXPERIMENTS.md); it cites nothing else.
