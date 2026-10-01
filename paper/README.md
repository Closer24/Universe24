# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript. It is written from the current documents on `main` alone: every
formula is taken from `docs/ALGEBRA.md`, `docs/ENGINE.md` or
`docs/HIGHLIGHTS.md` and cited by the name of its section or line, and every
claim carries its mark (theorem, derived, computed, assumption or hypothesis).
The paper holds no run of its own; a run enters only through the documents'
rows, labelled DETECTOR (a click) or GAMEBOARD (a diagnostic).

- `general_formula/main.tex`: the paper. Build it with `pdflatex main.tex`
  twice; it needs only its figures.
- `general_formula/main.pdf`: the compiled paper at the same commit.
- `general_formula/figures/`: the figures, each drawn by a script from the
  definitions or from the documents' rows, none from a run and none by a
  generative tool: `lattice.pdf` and `octahedron.pdf` by
  `python paper/general_formula/octahedron.py`, `band.pdf` and `channels.pdf`
  by `python paper/general_formula/band_and_channels.py`, `branches.pdf` (the three
  masses along the two branches, from the rows of the law) by
  `python paper/general_formula/branches.py`, `two_slits.pdf` (the clicks credited
  to the screen's twelve declared detectors beside the blind row, for the three
  worlds, from row (g) of the law) by `python paper/general_formula/two_slits.py`,
  and `bell.pdf` (the correlation at the four settings against the settings'
  calibrated phases, from row (h) of the law) by
  `python paper/general_formula/bell.py`, and `meeting.pdf` (the click as the
  meeting of the future with the past, schematically, from the definitions) by
  `python paper/general_formula/meeting.py`.
- `general_formula/einstein_check.py`: the Einstein rows computed from Rule3's
  coefficients by the geometric optics of the band (the bending, the perihelion),
  by no run of the engine; the law cites it under `the paces`.
- `general_formula/stable_body_check.py`: the stable body theorem in closed
  form and the lattice check of the two kernels' constants; the law cites it
  under `the functional and the dilation`.
- `general_formula/surplus_check.py`: the form's exact fall under a deepening
  well at a kept count, the free part and a cloud breathing in a static well;
  the law cites it under `the surplus leaves`.
- `general_formula/dimension_check.py`: the bodies one hollow allows on a
  chain, a plane and a box, the check of `the hollow's dimension`.

The experiments' rows enter after their runs on the engine with blind
expectations; the paper carries two experiments and no more, the two slits and
Bell, both run, each written as it stands beside its blind row. The paper's
outline, its chapters and its questions are on the issue "The paper: the
outline, the chapters and the questions".
