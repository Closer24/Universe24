# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript. It is written from the current documents on `main` alone: every
formula is taken from `docs/ALGEBRA.md`, `docs/ENGINE.md` or
`docs/HIGHLIGHTS.md` and cited by the name of its section or line, and every
claim carries its mark (theorem, derived, computed, assumption, hypothesis or
experiment, the last for a number the model does not fix with the experiment
named, and fitted where an input was chosen with the result known) and its
fence (GameBoard for a reading of the lattice, clicks for a formula of what a
detector reports). Its title is "Universe24: a simple integer rule and the group of order 24
give the two slits, Bell's correlation and the weak-field forms of gravity as
clicks"; the earlier title, the meeting of the past with the future, stands in
the introduction as the statement of what a click is. The paper is kept to 30 pages and to what is safe: the rule, its exact
properties, the measurement, the families, the bodies and their clusters, the
weak-field forms with both potentials, and the two worlds derived and not run;
the magnetic force, the sign of the charge, the hypotheses and the compact
pixel's numbers stand only in the long version. The paper holds no
run of its own; only a detector's click is a measurement, and a number read off
the GameBoard is a diagnostic. Table 1 of the paper lists every result with its
kind, its fence and what it rests on, and Table 2 the formulas of clicks with
their statuses.

- `general_formula/main.tex`: the paper. Build it with `pdflatex main.tex`
  twice; it needs only its figures.
- `general_formula/main.pdf`: the compiled paper at the same commit.
- `general_formula/supplement.tex` and `supplement.pdf`: the supplementary
  material, the algebraic steps of every derivation the paper states without
  its proof, Derivations S.1 to S.25 in the order of the paper's sections,
  cited in the paper as (S.n); submitted as supplementary material to the
  journal and as an ancillary file to arXiv.
- `general_formula/figures/`: the figures, each drawn by a script from the
  definitions or from the documents' rows, none from a run and none by a
  generative tool, at its final size and included at it, 1:1 (at most 119 mm
  wide, 8 pt sans-serif lettering, fonts embedded, no transparency), with an
  EPS beside each PDF for the journal. The paper uses two: `lattice.pdf` by
  `python paper/general_formula/octahedron.py` and `meeting.pdf` (the click as
  the meeting of the future with the past, schematically) by
  `python paper/general_formula/meeting.py`. The others, `octahedron.pdf`,
  `band.pdf`, `channels.pdf` (by `band_and_channels.py`) and `branches.pdf`
  (by `branches.py`), belong to the long version of the paper, which stays in
  the branch's history (commit 5adef30), and are kept for it.
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

The paper carries no experiment: until a run has worked and the advisor and
the reviewer have confirmed it, no run's number stands in it; the
implementation's two gates, the two slits and Bell, stand as the engine's
worlds and the law's derivations of what each must give. The derivations of
the bodies' clicks, the two potentials (the clock's share and Kepler's) and
the magnetic force enter with their statuses as the mathematician derived
them and the advisor checked them, never as results. The paper's outline, its
chapters and its questions are on the issue "The paper: the outline, the
chapters and the questions".

## Submission rules and status

The paper goes first to arXiv and then to Foundations of Physics
(Springer). The rules below were read from the venues' published pages; the
author checks the live pages before submitting. The order that avoids
rework: the GitHub release and its Zenodo version DOI, then arXiv, then
the journal.

### Foundations of Physics

- The abstract has 150 to 250 words, with no undefined abbreviation and no
  unspecified reference; there are 4 to 6 keywords. Met.
- A section "Statements and Declarations" stands before the references,
  or the submission is returned as incomplete: funding, competing
  interests, ethics and consent, data availability, author contributions.
  Met; the system asks for the same at submission.
- Data availability is stated (the Springer Nature policy). Met by the
  Zenodo concept DOI; the version DOI is added at the release.
- A large language model is never an author; its use is documented in the
  method (the paragraph on how to read the paper) and in the statements; no figure is
  made by a generative tool. Met.
- A preprint is allowed; its DOI and licence are declared at submission,
  and the preprint is updated with the journal's DOI after publication.
- Review is single-blind, so the title page stays.
- At most three levels of displayed headings; tables and figures are
  cited in numerical order, every table has a caption, and a figure's
  label reads "Fig." in bold. Met.
- Artwork: vector figures with embedded fonts, lettering of 8 to 12 pt at
  the final size, lines of at least 0.3 pt, at most 119 mm wide. Met.
- The template `sn-jnl` is recommended and another class is accepted at
  submission; the switch at acceptance changes the preamble alone.
- The scope is the conceptual bases of modern physics; a desk rejection
  follows overclaiming, missing references or a text that reads as
  internal notes. Met: the text is in the author's voice with every term
  defined, every result names what it rests on and whether an input was
  fitted to it, and every named result has a published source checked
  against its publisher's record.

### arXiv

- The metadata: the title, the author, the abstract as plain ASCII of at
  most 1920 characters with the math written out (`$6\pi$` as `6 pi`,
  `$2\sqrt 2$` as `2 sqrt(2)`), and the comments line, for example
  "30 pages, 2 figures, 4 tables; code and documents at
  doi:10.5281/zenodo.22738746". The abstract has 248 words and 1434
  characters.
- The source, not the PDF: `main.tex` and `figures/*.pdf` alone, without
  the EPS files and the scripts; it compiles under pdflatex in a clean
  directory, and no `.bbl` is needed since the references are in the
  document. Met.
- The licence: CC BY 4.0, the author's choice, irrevocable for a version;
  an announced paper is never removed.
- The category: `quant-ph` with `gr-qc` as a cross-list; the moderators
  may move a foundational lattice model to `physics.gen-ph`.
- Endorsement: since 21 January 2026 an institutional email alone does
  not endorse; an author without accepted papers in the category needs a
  personal endorser.
- The paper is complete in English, refereeable and written to scholarly
  standards, with references; the author answers for every word, and
  unchecked text from a language model (an invented reference, a
  chatbot's remark, a placeholder) brings a one-year ban.

### Open before submission

These need the author's decision or hand:

1. arXiv: the account, an endorser, the licence, and whether an earlier
   paper of the project was posted.
2. The archive: a GitHub release of the paper's commit and its Zenodo
   version DOI.
3. The cover letter, written for this paper.
4. The journal: an Editorial Manager account; the preprint declared at
   submission.
