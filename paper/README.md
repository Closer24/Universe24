# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript.

- `general_formula/main.tex`: the paper, algebra alone. Every formula is
  taken from `docs/ALGEBRA.md` and cited by the name of its section, and
  every claim carries its mark: theorem, derived, computed, assumption or
  hypothesis. The paper holds no run, no code and no experiment: the forms
  of nature are derived from the line as predictions, each beside the form
  it is compared with. Build it with `pdflatex main.tex` twice. It needs
  only its two figures.
- `general_formula/main.pdf`: the compiled paper.
- `general_formula/figures/lattice.pdf` and `octahedron.pdf`: the two
  figures, drawn from the definitions with no run by
  `python paper/general_formula/octahedron.py --output paper/general_formula/figures`.
- `general_formula/algebraic_runs.py`: the experiments run algebraically,
  every number of the paper's table computed from the law's formulas on
  declared worlds, by no run of the engine:
  `python paper/general_formula/algebraic_runs.py`.
- `general_formula/shape_check.py`: the check of the proposition on the
  bound record's shape (the symmetry under the 48 and the decay rates),
  a computation of the algebra on a lattice, by no run of the engine.
- `general_formula/dimension_check.py`: the check of the scaling of one
  hollow on a chain, a plane and a box, the bodies it allows by mass, a
  computation of the algebra on a lattice, by no run of the engine.
- `general_formula/SUBMISSION.md`: the submission checklist for arXiv and
  the journal.
- `general_formula/COVER_LETTER.md`: the cover letter for the journal.

The experiments enter after their runs on the engine with blind pins, as a
second part; this paper is the first, complete in itself.
