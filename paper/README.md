# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript.

- `general_formula/main.tex`: the paper, written from the law alone. Every
  formula is taken from `docs/ALGEBRA.md` and cited by the name of its
  section; the engine is described from `docs/ENGINE.md`. No experiment is
  run in the paper: its eighteen rows are the law's blind expectations,
  each beside the form of nature it is compared with. Build it with
  `pdflatex main.tex` twice. It needs only its two figures.
- `general_formula/main.pdf`: the compiled paper.
- `general_formula/figures/lattice.pdf` and `octahedron.pdf`: the two
  figures, drawn from the definitions with no run by
  `python paper/general_formula/octahedron.py --output paper/general_formula/figures`.
- `general_formula/SUBMISSION.md`: the submission checklist for arXiv and
  the journal.
- `general_formula/COVER_LETTER.md`: the cover letter for the journal.

The experiments' rows enter the paper after their runs on the engine with
blind pins, one row per run, in the same file.
