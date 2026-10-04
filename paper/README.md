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
and the formulas it shares with nature", the method, the
Universe24 it computes and the comparison, by the owner's word (2026-10-03, the
title chosen in the writer's session; "cellular automaton" the literature's name
for a lattice of integers stepped by one local rule); the meeting of the past with the future stands in the introduction as the
statement of what a click is. The source carries a submission switch
(`\submissiontrue` in the preamble of each document): the project's documents
are then cited as [1], [2], [3] alone, without their line names, and the
journal's name leaves the supplement's title. The paper is kept to about 34 pages and to what is safe: the rule, its exact
properties, the measurement with the sign of the charge (Section 5.5), the
families, the bodies and their clusters, the weak-field forms with both
potentials and the magnetic force (Section 8, Tables 1 and 2), the two
hypotheses by name where they stand (Sections 7.5 and 10.2), and the three
files derived and read by the gates, whose runs Section 3.7 reports; the
compact pixel's numbers stand only in the long version. The runs the
paper reports are the gates' (Section 3.7): the back-in-time gate's MATCH on
every file, taken by the owner's word of 2026-10-01 ("if there is a run of
the reversal that looks good and agrees with nature, take it"), and the two
slits', Bell's and GHZ's gates, the blind written first and the runs of Bell's and
the GHZ's identical to theirs, the two slits' 278 against its Huygens blind 273, the engine's check of the algebra and no experiment against nature;
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
  definitions or from the documents' rows, one (`two_slits_frames.pdf`) from the
  engine's own look of the shipped two-slits file, labelled a GameBoard reading, and none by a
  generative tool, with 8 pt lettering at the drawn size (Figs. 1 and 2 are
  included at that size, the other four at 0.66 to 0.75 of the text width), within the
  journal's and arXiv's rules for artwork (at most 174 mm wide, 8 pt lettering
  in one sans-serif typeface for the words and the symbols, fonts embedded,
  every line at least 0.3 pt, black and grey, no transparency), with an EPS
  beside each PDF for the journal. The paper uses eight: `lattice.pdf` and `octahedron.pdf` (the two panels
  of Fig. 2, the GameBoard and the octahedron of the Nodes one interval away
  with the cube's group and the inscribed sphere of radius 1 / sqrt 3) by
  `python paper/general_formula/octahedron.py` and `click_body.pdf` (Fig. 4,
  the click at a NodeReader: space and time with the NodeReader's region of
  two Nodes, the past meeting the future, the region before the close and
  after the write at the drawn Node, the hole by the faces' identity, and
  the ledger, schematically, in black and grey) by `python paper/general_formula/click_body.py`;
  `bands.pdf` (light's and matter's bands along one axis, from the law's line)
  by `python paper/general_formula/bands.py`; `two_slits_rows.pdf` (the two
  slits' declared file and its screen's row, the Huygens blind of the
  expectation file beside the law's real line of `two_slits_real_line.txt`,
  the numbers typed from those two files) by
  `python paper/general_formula/two_slits_rows.py`; and `method.pdf` (the
  method's three layers, from nature's measurements to the paper's reading) by
  `python paper/general_formula/method.py`; and `moving_clock.pdf` (the moving
  clock's factor from the band against Lorentz's) by
  `python paper/general_formula/moving_clock.py`; and `two_slits_frames.pdf` (Fig. 7,
  the two slits mid-run: the light record's level at the intervals 18, 40 and 62
  of the 130, a GameBoard reading and no measurement, from the three frames
  recorded in `figures/two_slits_frames.json` by `python paper/general_formula/two_slits_frames.py --look <world>.look.json`
  after `PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json --ticks 130`)
  by `python paper/general_formula/two_slits_frames.py`. The folder holds
  these eight figures, that recording and nothing else.
- `general_formula/invariant_check.py`: S.14's check of the adiabatic invariant, the one-Node
  line stepped over 20,000 intervals with the rotation lowered from 0.841 to 0.600, D / sin(omega)
  within 4e-5 of its start (Section 7.4). Run with `python paper/general_formula/invariant_check.py`.
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
  of the engine. It reads the two slits' file as the engine's loader reads it
  (`examples/events/two_slits/two_slits.json` with its mode file, the universe
  file it names and the blind `expectation.json` beside it) and steps Rule3's
  line for light at the vacuum's paces in floating point, with no integer
  division and no remainder, on the same declared board, wall, gaps, laid message and
  screen regions, reading what the engine's click lines report, the net current
  through each region's front boundary Ports over the expectation's window over
  the count wall, so that the integer run is checked against it to the rounding.
  The message lay carries the law's division act (the uniform component taken
  out of each level in proportion to the envelope, in real arithmetic), so the
  lay is the one the pinned commit's mode file holds, within the integer
  rounding of a level; the script prints no draw, the clicks' row being the
  folder's. Run with `PYTHONPATH=src python paper/general_formula/two_slits_real_line.py`
  at the pinned commit; it runs from the repository on the folder's files. Its
  printed output stands beside it as `two_slits_real_line.txt`, every
  number with its definition: the total over the whole passage, the twelve
  regions' quanta and shares, the visibility, the wings and the arrival (in the
  engine's interval labels and in the physical ones), the meeting round's file
  with its source face open, the Huygens blind of the expectation file, the
  central maximum against the first minima in the draw's scatter, the arrival's
  spread sigma_t from the band and the lay's widths, and the same file scaled
  toward the continuum.

The paper carries one experiment, the two slits, and no experiment against nature: until a run has worked and the advisor and
the reviewer have confirmed it, no click count of a run stands in it beside
nature's, the gates' runs above being the engine's check of the algebra; the
implementation's three gates, the two slits, Bell and GHZ, stand as the engine's
files and the law's derivations of what each must give. The derivations of
the bodies' clicks, the two potentials (the clock's share and Kepler's) and
the magnetic force enter with their statuses as the mathematician derived
them and the advisor checked them, never as results. The paper's outline, its
chapters and its questions are on the issue "The paper: the outline, the
chapters and the questions".

## The paper's gates and the derivation scripts' count

`general_formula/paper_gates.py` runs on every pull request through `tests/test_paper_gates.py`:
the marks (every `\claimmark` one of the key's eight words, every `\fence` one of the two, a fence
beside every derived or theorem mark of the main text), the struck phrases (the words earlier prints
removed, with the history forms "pending", "not yet", "earlier version" and their kin, none allowed
back), and the twins (a number or a word printed in two places asserted equal). The derivation
scripts' count is a ratchet the same test holds: of the 127 derived and computed marks of the main
text, 4 name a Python script beside them (`invariant_check.py`, `surplus_check.py`, `test_the_draw.py`, `test_the_meeting.py`) and
123 name none; the count may only fall, and the paper claims nothing beyond it (the supplement
carries the algebraic steps of every derived mark; the scripts' map is the law's fill, part 4).

## Submission rules and status

The paper goes first to arXiv and then to Foundations of Physics
(Springer). The rules below were read from the venues' published pages; the
author checks the live pages before submitting. The order that avoids
rework: the GitHub release and its Zenodo version DOI, then arXiv, then
the journal.

### Foundations of Physics

- The abstract has 150 to 250 words, with no undefined abbreviation and no
  unspecified reference; there are 4 to 6 keywords. Met: the paper's abstract
  and `abstract_journal.txt` beside it are one text of 250 words of prose
  (277 tokens with the TeX signs), every formula in it the paper's.
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
  the final size, lines of at least 0.3 pt, the widths 39, 84, 129 or 174 mm
  and the height at most 234 mm (Springer's general artwork guidelines, as the
  writer holds them; the author checks the journal's page before submitting,
  the venues' pages being unreachable from the writer's session). Met: the
  four figures drawn 174 mm wide are
  included at that size, their lettering 8 pt at the final size, and the four
  drawn narrower at theirs.
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
  "34 pages, 7 figures, 4 tables; supplementary material of 31 pages as an
  ancillary file; code and documents at doi:10.5281/zenodo.22738746". The abstract has 1,630
  characters counted with its TeX signs, below the cap, and is the paper's own abstract.
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
- The discipline: foundations of physics, the journal's own scope; the paper is
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
