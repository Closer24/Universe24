# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript. It is written from the current documents on `main` alone: every
formula is taken from `docs/ALGEBRA.md`, `docs/ENGINE.md` or
`docs/HIGHLIGHTS.md` and cited by the name of its section or line, and every
claim carries its mark (theorem, derived, computed, assumption, hypothesis or
experiment, the last for a number the model does not fix with the experiment
named, and fitted where an input was chosen with the result known) and its
fence (GameBoard for a reading of the lattice, clicks for a formula of what a
a NodeReader reports). Its title is "Universe24: an integer cellular automaton read through clicks,
the setups it computes, and the clicks of nature it approaches", the method, the
setup it computes and the comparison, by the owner's word (2026-10-03, the
title chosen in the writer's session; "cellular automaton" the literature's name
for a lattice of integers stepped by one local rule); the meeting of the past with the future stands in the introduction as the
statement of what a click is. The source carries a submission switch
(`\submissiontrue` in the preamble of each document): the project's documents
are then cited as [1], [2], [3] alone, without their line names, and the
journal's name leaves the supplement's title. The paper is kept to about 33 pages and to what is safe: the rule, its exact
properties, the measurement with the sign of the charge (Section 5.5), the
families, the bodies and their clusters, the weak-field forms with both
potentials and the magnetic force (Section 8, Tables 1 and 2), the two
hypotheses by name where they stand (Sections 7.5 and 10.2), and the three
setups derived and read by the gates, whose runs Section 3.7 reports; the
compact pixel's numbers stand only in the long version. The runs the
paper reports are the gates' (Section 3.7): the back-in-time gate's MATCH on
every setup, taken by the owner's word of 2026-10-01 ("if there is a run of
the reversal that looks good and agrees with nature, take it"), and the two
slits', Bell's and GHZ's gates, the blind written first and the run identical
to it, the engine's check of the algebra and no experiment against nature;
only a NodeReader's click is a measurement, and a number read off the GameBoard
is a diagnostic. Table 1 of the paper lists every result with its
kind, its fence and what it rests on, and Table 2 the formulas of clicks with
their statuses.

- `general_formula/main.tex`: the paper. Build it with `pdflatex main.tex`
  twice; it needs only its figures.
- `general_formula/main.pdf`: the compiled paper at the same commit.
- `general_formula/supplement.tex` and `supplement.pdf`: the supplementary
  material, the algebraic steps of every derivation the paper states without
  its proof, Derivations S.1 to S.62, numbered as added, each naming its section,
  cited in the paper as (S.n), S.61 the engine's derivation ledger and S.62 the
  implementation's versions of the click's write and their readings, which stand
  there and not in the main text (the owner's word of 2026-10-03: a derivation
  is shown as a derivation, and the main text reports no run but the two slits
  with Bell's and the GHZ's gates); submitted as supplementary material to the
  journal (Online Resource 1, its title page carrying the article's title,
  the journal, the author, the affiliation and the email, as Springer
  asks) and as an ancillary file to arXiv, `anc/supplement.pdf` in the
  source.
- `general_formula/figures/`: the figures, each drawn by a script from the
  definitions or from the documents' rows, none from a run and none by a
  generative tool, at its final size and included at it, 1:1, within the
  journal's and arXiv's rules for artwork (at most 174 mm wide, 8 pt lettering
  in one sans-serif typeface for the words and the symbols, fonts embedded,
  every line at least 0.3 pt, black and grey, no transparency), with an EPS
  beside each PDF for the journal. The paper uses seven: `lattice.pdf` and `octahedron.pdf` (the two panels
  of Fig. 1, the GameBoard and the octahedron of the Nodes one interval away
  with the cube's group and the inscribed sphere of radius 1 / sqrt 3) by
  `python paper/general_formula/octahedron.py` and `click_body.pdf` (Fig. 2,
  the click at a bound body: space and time at the body's Node, the past
  meeting the future, and the Node before and after the write, schematically,
  in black and grey) by `python paper/general_formula/click_body.py`;
  `bands.pdf` (light's and matter's bands along one axis, from the law's line)
  by `python paper/general_formula/bands.py`; `two_slits_rows.pdf` (the two
  slits' declared setup and its screen's row, the Huygens blind of the
  expectation file beside the law's real line of `two_slits_real_line.txt`,
  the numbers typed from those two files) by
  `python paper/general_formula/two_slits_rows.py`; and `method.pdf` (the
  method's three layers, from nature's clicks to the paper's reading) by
  `python paper/general_formula/method.py`; and `moving_clock.pdf` (the moving
  clock's factor from the band against Lorentz's) by
  `python paper/general_formula/moving_clock.py`. The others,
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
- `general_formula/two_slits_real_line.py`: the two slits' row by the law's
  real line, the reference computation Sections 3.7, 9.1 and 9.2 and Table 2
  cite (`docs/ALGEBRA.md` row (g) and item 1 of the click formulas), by no run
  of the engine. It reads the two slits' setup as the engine's loader reads it
  (`examples/events/two_slits/two_slits.json` with its mode file, the universe
  file it names and the blind `expectation.json` beside it) and steps Rule3's
  line for light at the vacuum's paces in floating point, with no integer
  division and no remainder, on the same declared board, wall, gaps, emitter and
  screen regions, reading what the engine's click lines report, the net current
  through each region's front boundary Ports over the expectation's window over
  the count wall, so that the integer run is checked against it to the rounding.
  Run with `PYTHONPATH=src python paper/general_formula/two_slits_real_line.py`;
  its printed output stands beside it as `two_slits_real_line.txt`, every
  number with its definition: the total over the whole passage, the twelve
  regions' quanta and shares, the visibility, the wings and the arrival (in the
  engine's interval labels and in the physical ones), the meeting round's setup
  with its source face open, the Huygens blind of the expectation file, the
  central maximum against the first minima in the draw's scatter, the arrival's
  spread sigma_t from the band and the lay's widths, and the same setup scaled
  toward the continuum.

The paper carries no experiment: until a run has worked and the advisor and
the reviewer have confirmed it, no click count of a run stands in it beside
nature's, the gates' runs above being the engine's check of the algebra; the
implementation's three gates, the two slits, Bell and GHZ, stand as the engine's
setups and the law's derivations of what each must give. The derivations of
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
  unspecified reference; there are 4 to 6 keywords. Met by the journal's
  version of the abstract, `abstract_journal.txt` beside the paper: the
  arXiv abstract without its opening question, light's speed sentence, the
  cube's 48, the alpha clause and the shadow, 248 words,
  every formula in it the arXiv abstract's.
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
  "33 pages, 2 figures, 4 tables; supplementary material of 27 pages as an
  ancillary file; code and documents at doi:10.5281/zenodo.22738746". The abstract has 327 words and 1917
  characters counted with its TeX signs, below the cap.
- The source, not the PDF: `main.tex` and `figures/*.pdf`, with the
  supplement's PDF as `anc/supplement.pdf`, without the EPS files and the
  scripts; it compiles under pdflatex in a clean directory, and no `.bbl`
  is needed since the references are in the document. Met.
- The licence: CC BY 4.0, the author's choice, irrevocable for a version;
  an announced paper is never removed.
- The category: `quant-ph` as primary, since the paper's claim is about
  measurement and Bell, with `gr-qc` (the weak-field forms) and `nlin.CG`
  (a reversible cellular automaton) as cross-lists; the moderators may move
  a foundational lattice model to `physics.gen-ph`, which is their call.
- The field: foundations of physics, the journal's own scope; the paper is
  not a general-relativity paper (its gravity stands against the tests at
  the rule's own matter pair) and not a particle-physics paper, and should
  not be sent to a journal of either.
- Endorsement: since 21 January 2026 an institutional email alone does
  not endorse; an author without accepted papers in the category needs a
  personal endorser; the author has one (2026-10-02).
- The paper is complete in English, refereeable and written to scholarly
  standards, with references; the author answers for every word, and
  unchecked text from a language model (an invented reference, a
  chatbot's remark, a placeholder) brings a one-year ban.

### Open before submission

These need the author's decision or hand. The Statements and Declarations,
the author contributions and the statement on the use of a language model
are the author's own words and are submitted in the author's name: the
author confirms each of them in the submission system, and the paper and
the supplement are uploaded under the author's own accounts at arXiv and at
the journal.

1. arXiv: the account, the licence, and whether an earlier paper of the
   project was posted; the endorser is in hand (the author, 2026-10-02).
2. The archive: a GitHub release of the paper's commit and its Zenodo
   version DOI.
3. The cover letter, written for this paper.
4. The journal: an Editorial Manager account; the preprint declared at
   submission.
