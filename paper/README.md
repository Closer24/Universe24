# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript (the model owner's decision of 2026-09-26: what came before is
gone; only the new paper stands).

- `general_formula/main.tex`: the paper. Build it with `pdflatex main.tex`
  twice. It needs only its two figures.
- `general_formula/main.pdf`: the compiled paper.
- `general_formula/figures/lattice.pdf` and `octahedron.pdf`: the two
  figures, drawn from the definitions with no run by
  `python paper/general_formula/octahedron.py --output paper/general_formula/figures`.
- `general_formula/SUBMISSION.md`: the submission checklist for arXiv and
  the journal.
- `general_formula/COVER_LETTER.md`: the cover letter for the journal.

Every formula of the paper is taken from the algebra, `docs/ALGEBRA.md`,
chapters 8 and 9, and every pin from the algebra's section 9.22 (8) or the
lab tools' part B, each cited in the paper.
