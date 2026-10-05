# Paper

The project has one paper: `general_formula/main.tex`. There is no other
manuscript. It is written from the current documents on `main` alone: every
formula is taken from `docs/ALGEBRA.md`, `docs/ENGINE.md` or
`docs/HIGHLIGHTS.md` and cited by the name of its section or line, and every
claim carries its mark (theorem, derived, computed, assumption, hypothesis or
experiment, the last for a number the model does not fix with the experiment
named, and fitted where an input was chosen with the result known) and its
fence (lattice for a reading of the lattice, clicks for a formula of what
a NodeDetector reports). Its title is "Universe24: an integer cellular automaton read through clicks,
the formulas it shares with nature and the ones it adds", the method, the
Universe24 it computes and the comparison, by the owner's word (2026-10-03, the
title chosen in the writer's session; "cellular automaton" the literature's name
for a lattice of integers stepped by one local rule); the meeting of the past with the future stands in the introduction as the
statement of what a click is. The source carries a submission switch
(`\submissiontrue` in the preamble of each document): the project's documents
are then cited as [1], [2], [3] alone, without their line names. The paper is kept to about 40 pages and to what is safe: the rule, its exact
properties, the measurement with the sign of the charge (Section 5.5), the
families, the bodies and their clusters, the weak-field forms with both
potentials and the magnetic force (Section 8, Tables 1 and 2), the two
hypotheses by name where they stand (Sections 7.5 and 10.2), and the one
run the paper reports, the two slits' at the frozen commit (Section 3.7), and Bell's and the GHZ's
values as evaluations of the declared credit, exact in the shares; the
compact pixel's numbers stand in the repository and not in the paper. The one run the
paper reports is the two slits' (Section 3.7): the back-in-time gate's MATCH on its
file, taken by the owner's word of 2026-10-01 ("if there is a run of
the reversal that looks good and agrees with nature, take it"), and its screen's
row against the blind written first, the engine's check of the algebra and no experiment
against nature; Bell's and the GHZ's values are evaluations of the declared credit, exact in
the shares, and the folder's runs of them are the repository's and no claim of the paper;
only a NodeDetector's click is a measurement, and a number read off the lattice
is a diagnostic. Table 1 of the paper lists every result with its
kind, its fence and what it rests on, and Table 2 the formulas of clicks with
their statuses.

- `general_formula/main.tex`: the paper. Build it with `pdflatex main.tex`
  twice; it needs only its figures.
- `general_formula/main.pdf`: the compiled paper at the same commit. The paper's pins:
  the implementation at the frozen commit 1fe3790a and the three documents (the law,
  the engine's document, the decisions) at the tagged release 1.1.0; the commit is of 2026-10-05.
- `claims.md`: the paper's claims table, one row per marked sentence of the paper (its place,
  marks, fence, kind, the source the sentence gives, the breaker that could break it and its state),
  built by `general_formula/claims_table.py` at every print; `claims_breakers.json` holds the
  breakers written by hand, keyed by the sentence's opening words (the method of 2026-10-04, #1538).
- `general_formula/supplement.tex` and `supplement.pdf`: the supplementary
  material, the algebraic steps of every derivation the paper states without
  its proof, Derivations S.1 to S.56 in their own order, each naming its section,
  cited in the paper as (S.n); its front carries the glossary of the long version's
  words, the paper's claims list, the two tables of the formulas and the Nomenclature;
  the derivations of the hypotheses under their own names and of the implementation
  stand in the long version at the tag `paper-long-v1.1` in its own numbering, cited
  as (S.n of the long version); built in Springer Nature's class like the article (the owner's
  word of 2026-10-05: the readable format only, up to 50 pages); submitted as supplementary material to the
  journal (Online Resource 1, its title page carrying the article's title,
  the journal, the author, the affiliation and the email, as Springer
  asks) and as an ancillary file to arXiv, `anc/supplement.pdf` in the
  source.
- `general_formula/figures/`: the figures, each drawn by a script from the
  definitions or from the documents' rows, one (`two_slits_frames.pdf`) from the
  engine's own look of the shipped two-slits file, labelled a lattice reading, and none by a
  generative tool, with 8 pt lettering or above at the drawn size (the panel letters 9 pt; Figs. 3 and 5 are
  included at 0.66 of the text width, the other five at the drawn size), within the
  journal's and arXiv's rules for artwork (at most 174 mm wide, 8 pt lettering
  in one sans-serif typeface for the words and the symbols, fonts embedded,
  every line at least 0.3 pt, black and grey, no transparency), with an EPS
  beside each PDF for the journal. The paper uses eight: `lattice.pdf` and `octahedron.pdf` (the two panels
  of Fig. 1, the lattice and the octahedron of the Nodes one interval away
  with the cube's group and the inscribed sphere of radius 1 / sqrt 3) by
  `python paper/general_formula/octahedron.py` and `click_body.pdf` (Fig. 4,
  the click at a NodeDetector: space and time with the NodeDetector's region of
  two Nodes, the past meeting the future, the region before the close and
  after the write at the drawn Node, the hole by the faces' identity, and
  the books, schematically, in black and grey) by `python paper/general_formula/click_body.py`;
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
  of the 130, a lattice reading and no measurement, from the three frames
  recorded in `figures/two_slits_frames.json` by `python paper/general_formula/two_slits_frames.py --look <world>.look.json`
  after `PYTHONPATH=src python tools/look/record.py examples/events/two_slits/two_slits.json --ticks 130`)
  by `python paper/general_formula/two_slits_frames.py`. The folder holds
  these seven figures (eight files), that recording and nothing else.
- `general_formula/invariant_check.py`: S.14's check of the adiabatic invariant, the one-Node
  line stepped over 20,000 intervals with the rotation lowered from 0.841 to 0.600, D / sin(omega)
  within 4e-5 of its start (Section 7.4). Run with `python paper/general_formula/invariant_check.py`.
- `general_formula/schroedinger_check.py`: S.63's check of Schroedinger's equation as the
  slow limit of the line, a Gaussian packet stepped by the line without the remainder on a
  chain against Schroedinger's centre and spread with the band's inertia 3 tan omega_0
  (Section 3.3). Run with `python paper/general_formula/schroedinger_check.py`.
- `general_formula/dark_matter_check.py`: Section 7.5's dark matter in kind checked on the
  band: a one-line record's Wronskian 0, the fall of a free quantum of the scalar row the same at
  every amplitude and count and equal to S.18's closed form, the free quantum cold (its group
  velocity to 0 with k). Run with `python paper/general_formula/dark_matter_check.py`.
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
  division and no remainder, on the same declared lattice, wall, gaps, laid packet and
  screen regions, reading what the engine's click lines report, the net current
  through each region's front boundary Ports over the expectation's window over
  the count wall, so that the integer run is checked against it to the rounding.
  The packet lay carries the law's division act (the uniform component taken
  out of each level in proportion to the envelope, in real arithmetic), so the
  lay is the one the pinned commit's mode file holds, within the integer
  rounding of a level; the script prints no draw, the clicks' row being the
  folder's. Run with `PYTHONPATH=src python paper/general_formula/two_slits_real_line.py`,
  from the paper's commit on the folder's files as they stand at the pinned commit
  1fe3790a (a worktree of it); the script lays the before level as the generator does at
  that commit (`tools/pixel_mode.advanced_real_part`), so its lay is the mode file's to the
  rounding of the quadrature before the transform (0.4 percent of the amplitude in the
  before level) and its printed output is the line at the engine's own lay. Its
  printed output stands beside it as `two_slits_real_line.txt`, every
  number with its definition: the total over the whole passage, the twelve
  regions' quanta and shares, the visibility, the wings and the arrival (in the
  engine's interval labels and in the physical ones), the meeting round's file
  with its source face open, the Huygens blind of the expectation file, the
  central maximum against the first minima in the draw's scatter, the arrival's
  spread sigma_t from the band and the lay's widths, the same file scaled
  toward the continuum, and the integer step's walk per band mode and per Node.

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
scripts' count is a ratchet the same test holds: of the 131 derived and computed marks of the main
text, 120 name a script beside them (the derivation modules of `tools/derivations/`, each from Rule3's
line alone with no engine import and no run's file, the paper's own check scripts, or, for a computed
mark, the run's reader) and 11 name none: the atoms' ground levels computed by hand (S.60) and the qualitative statements (a body's four statements, the stable body's
proposition, the three kinds of binding, the k^4 term's ten percent, the seat of the electromagnetic binding
energy, confinement, the polarisations, the Lorentz form, antimatter's opposite charge (the Wronskian's sign, Section 5.5)) and the integer Wronskian's
witness of S.9; the count may only fall, and the paper claims nothing beyond it (the supplement
carries the algebraic steps of every derived mark; the scripts' map is the law's fill, part 4).

## The automation for the short version and the supplement

The long version's tools, handed to the editor for the short main text and the rebuilt supplement
(the owner's word of 2026-10-05); each line says what the tool checks, how it runs and what the
short version changes in it. Run them in the order of the last paragraph after every push.

**The gates on every pull request** (`tools/every_pull_request.txt`: the paper gates, the documents
gate and the language gate; `python tools/check.py` selects the changed files and their consumers,
`--full` runs everything, every test under 30 s). `general_formula/paper_gates.py` runs ten gates on
`main.tex` and `supplement.tex` together and exits non-zero on any miss:

- The marks: every `\claimmark` one of the key's words and every `\fence` one of the two. The short
  main carries no macro; its mark is the sentence's last parenthesis opening with a key word (the
  key's eight words and the tables' four: calibration, declaration, definition, untested), the fence
  after the first semicolon, then the pointers, and `claims_table.py` reads that form (below).
- The struck phrases: the words earlier prints removed never return; a hand adds a phrase to the list
  when a cut strikes it for good.
- The twins: a number or a word printed in two places asserted equal across the two documents. A cut
  that removes one side of a pair fails the gate; the pair is re-keyed to where the number still
  stands, or removed, in the same push.
- The derivations' Inputs graph: no cycle beyond `claims_table.KNOWN_CYCLES`, a set that may only
  shrink; its numbers take the supplement's renumbering map.
- The bare board: the lattice by its one noun.
- The nomenclature: every letter in math mode in either document has its `\nom` row in the
  supplement's Nomenclature; a row leaves only with the last use of its letter.
- The units and the abbreviations: a bare number after a named quantity carries its unit, every
  abbreviation is expanded at its first use in the same document; a cut that deletes a first use
  moves the expansion to the next.
- The team's idioms: the hands' names, the ledger's rows and the comment ids stand nowhere in the paper.
- The pointers: every `\ref` has its `\label`, an equation is cited by `\eqref` alone, every literal
  pointer of the supplement, the captions and this README names a number the paper has, counted from
  `main.tex`'s source order; every `\cite` has its `\bibitem` in the same document, every `\bibitem`
  is cited, none doubled, the list in the order of first citation. Every section, equation, figure or
  table that leaves or moves renumbers the literal pointers, and the gate lists each by line; after an
  edit that moves a citation, `cut_tools/reorder_bib.py` restores the order.
- The captions and the names: no caption ends with punctuation; no author-year parenthesis outside `\cite`.

**The claims reader**, `python paper/general_formula/claims_table.py`, writes `paper/claims.md` at
every print: the marked sentences (the plain parenthesis or the macro; the itemised lists' items read
as sentences; a sentence inside an assumption or theorem environment marked by the environment), each
with its place, marks, fence, kind, the sources it names, its breaker and state; the candidates (a strong
word in an unmarked sentence, a report and no gate); the tables' rows by the short version's labels,
read from the main or, once a table has moved, from the supplement; the supplement's derivations with
their Status lines. Its two gates of the move, held as ratchets in `tests/test_paper_gates.py`: no row
of the claims list without a marked sentence at the row's place (a sentence in the row's section, at any
level, carrying the row's first status word, and a sentence there naming one of the row's derivations),
and no plain mark opening with a word outside the key; both counts may only fall. Beside them the
breakers' gate, `tests/test_counterexamples.py`, runs every row of `tools/derivations/counterexamples.py`
(a claim tried inside its condition and outside it in the algebra of Rule3's line) and asserts its key
is a row of `paper/claims_breakers.json`; the keys are the long version's sentences, table labels and
derivation numbers, and they take the short version's rows and the renumbering map in one commit.

**The numbers' provenance.** Every computed number of the main is one a script prints from Rule3's
lines or the one run the paper reports: the derivation modules of `tools/derivations/` (each from the
line alone, no engine import; `tools/derivations/README.md` the map) and the paper's own checks in
`general_formula/` (`einstein_check.py`, `schroedinger_check.py`, `invariant_check.py`,
`stable_body_check.py`, `surplus_check.py`, `dark_matter_check.py`, `dimension_check.py`,
`two_slits_real_line.py` with its printed row). The scripts' names left the short text at the owner's
word; the provenance stays theirs, and the supplement's derivations keep the modules' names.
`short_checker.py` audits every number of the short files against the long version at the tag and
prints the accepted misses and the weak places; `claims_triage.py` wrote `paper/claims_triage.md`, the
map of what is core, support and out that the cut follows.

**The cut tools** (`general_formula/cut_tools/README.md`): the bibliography's order, the build in
Springer's class with the page each section starts on, the abstract's counts, the doubled passages,
the DOI check against Crossref, a sentence-level grep.

**The figures.** Each figure's script writes its PDF, EPS and PNG into `figures/`, committed; the
lattice and the octahedron, the two slits' rows, the method, the run's frames; the click, the bands and
the moving clock stay for the long version. Drawn at 131 mm with 8 pt lettering in the glossary's words.

**The supplement at the rebuild.** Every derivation in its environment with its Inputs, Steps and Status
lines (the reader and the Inputs gate read that form); the Status line in the key's words; the
Nomenclature at the front; its own bibliography in the order of first citation; the claims list whole
under its label, where the reader finds it once the main no longer holds it; the main's citations of
the long version's numbers kept apart from the new numbering, as the front note states.

**The run at every push:** the claims reader (the two counts at their ratchets, the NO SOURCE marks
read); the paper gates; the bibliography's order after an edit that moves a citation; the five paper
tests (`test_paper_gates`, `test_documents`, `test_repository_language`, `test_counterexamples`,
`test_the_paper_claims_engine`); `python tools/check.py`; the build of both documents in Springer's
class three times with no error and no undefined reference, the page counts posted; `short_checker.py`;
the build's by-products deleted before the commit.

## Submission rules and status

The paper goes first to arXiv and then to Foundations of Physics
(Springer). The rules below were read from the venues' published pages; the
author checks the live pages before submitting. The order that avoids
rework: the GitHub release 1.1.0 and its Zenodo version DOI, then arXiv, then
the journal.

### Foundations of Physics

- The abstract has 150 to 250 words, with no undefined abbreviation and no
  unspecified reference; there are 4 to 6 keywords. Met: the paper's abstract
  and `abstract_journal.txt` beside it are one text of 247 to 250 words
  (whitespace tokens, each formula counted by its tokens), every formula in it the paper's.
- A section "Statements and Declarations" stands before the references,
  or the submission is returned as incomplete: funding, competing
  interests, ethics and consent, data availability, author contributions.
  Met; the system asks for the same at submission.
- Data availability is stated (the Springer Nature policy). Met by the
  Zenodo concept DOI; the version DOI is added at the release. The code's licence is MIT, the preprint's CC BY 4.0.
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
  the venues' pages being unreachable from the writer's session). Met for the five
  figures the short version keeps (the lattice and the octahedron, the bands, the click,
  the two slits' rows, the moving clock): drawn 131 mm (the text width of `sn-jnl`'s
  `sn-mathphys-num`, 372 pt, one column) or 129 mm wide with every lettering 8 pt or
  above at the drawn size (the panel letters 9 pt), redrawn on 2026-10-05, the click
  figure as two panels, (a) and (b), at 131 mm, its (c) and (d) the text of the short version;
  the method figure (6.2 to 8 pt) and the frames leave for the report and the supplement.
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
  "43 pages, 7 figures, 6 tables; supplementary material of 39 pages as an
  ancillary file; code and documents at doi:10.5281/zenodo.22738746". The plain-text abstract has 1,492
  characters, below the cap, and is the paper's own abstract.
- The source, not the PDF: `main.tex` and `figures/*.pdf`, with the
  supplement's PDF as `anc/supplement.pdf`, without the EPS files and the
  scripts; it compiles under pdflatex in a clean directory, and no `.bbl`
  is needed since the references are in the document. Met.
- The licence: CC BY 4.0, the author's choice, irrevocable for a version;
  an announced paper is never removed.
- The category: `quant-ph` as primary, since the paper's claim is about
  measurement and Bell, with `nlin.CG`
  (a reversible cellular automaton) as the cross-list; `gr-qc` is not asked, the paper's
  gravity standing against the tests at the rule's own pair; the moderators may move
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

1. arXiv: the account and the licence. This is the project's first paper and a
   new submission; no earlier paper of the project was posted, and the endorsement
   is the author's own step at arXiv.
2. The archive: the GitHub release 1.1.0 of the paper's commit and its Zenodo
   version DOI (the archive's version 1.1.0).
3. The cover letter, `cover_letter.md` beside this file, with its two placeholders
   (the arXiv identifier, the date) filled by the author.
4. The journal: an Editorial Manager account; the preprint declared at
   submission.
