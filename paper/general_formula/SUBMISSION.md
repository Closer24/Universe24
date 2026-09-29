# The submission checklist: arXiv, GitHub and Foundations of Physics

The state at the head of `paper-new-engine`. What is ready is in the
repository; what only the author can do is marked **the author's hand**.
The order that avoids rework: the GitHub release and its Zenodo version
first, arXiv second (its identifier goes into the cover letter), the
journal third.

## Ready in the repository

- `main.tex`, one document, compiled by `pdflatex` twice with standard
  packages only (geometry, amsmath, amssymb, amsthm, booktabs, graphicx,
  hyperref, caption, microtype, float, enumitem, longtable, array); it
  compiles from a clean directory holding `main.tex` and `figures/` alone,
  32 pages, no undefined reference.
- `main.pdf`, the compiled output at the same commit.
- `figures/`: the two figures the paper includes (`lattice.pdf`,
  `octahedron.pdf`), both drawn by `octahedron.py` from the definitions,
  none by a generative tool; `algebraic_runs.py`, the script that computes
  every number of the paper's table from the law's formulas.
- The title page: the title, the author's name, affiliation, email and
  ORCID.
- The abstract: 248 words (the journal's template asks 150 to 250),
  1452 characters (arXiv allows 1920).
- Keywords after the abstract (six).
- The declarations in the journal's list: funding, competing interests,
  ethics approval, consent to participate and for publication, data and
  code availability, author contributions, the use of a large language
  model.
- The reference list, numbered, in the document itself (no `.bib` file
  is needed); the project's own documents cited by the name of their
  sections at the archive's DOI.
- `COVER_LETTER.md`, the cover letter for the journal, current with the
  title and the paper's state.
- The archive: the Zenodo concept DOI 10.5281/zenodo.22738746 in the
  data availability statement; the MIT licence in the repository.

## What the paper claims and does not

The paper is algebra alone: every formula is `docs/ALGEBRA.md`'s, the
theorems are proved on the lattice, every claim carries its mark (theorem,
derived, computed, assumption, hypothesis), and the forms of nature are
derived from the line as predictions with the form of nature beside each,
and every experiment is run algebraically on a declared world, its numbers
computed by `algebraic_runs.py` from the law's formulas. It holds no run
of the engine, and no agreement with nature is claimed; the runs on the
engine are a second part.

## GitHub (the author's hand, with the Boss)

1. Merge the paper's pull request into `main`.
2. Tag the merge commit as a release (for example `paper-v2`) so that the
   archive's commit is a fixed, citable point.
3. Let Zenodo mint the version DOI of that release (the GitHub-Zenodo
   integration does it on a release), and put the version DOI beside the
   concept DOI in the data availability statement of the next build.
   (A referee's objection: a concept DOI resolves to the latest version;
   a version DOI fixes what the paper cites.)

## arXiv (the author's hand)

1. An arXiv account under the author's name and email; a first
   submission in a category may need an endorsement (arXiv asks for it
   at submission and names how to obtain it).
2. The category: `quant-ph` as the primary (Bell, Born, interference)
   with `gr-qc` as a cross-list for the relativistic rows is the honest
   choice; the moderators may reclassify a foundational lattice model to
   `physics.gen-ph`, which is theirs to decide.
3. The upload: the source, not the PDF alone: `main.tex` and `figures/`.
4. The metadata: the title as in the paper; the abstract as plain text
   (the paper's words, the macros written out); the author as on the
   title page; the licence CC BY 4.0, the author's choice (the usual
   choice for a paper whose code is MIT; irrevocable for each version);
   the comment line: "32 pages, 2 figures; code and documents at
   doi:10.5281/zenodo.22738746".
5. After the posting, the arXiv identifier goes into the cover letter.

## Foundations of Physics, Springer (the author's hand)

1. An account on the journal's submission system (Springer Nature's
   Editorial Manager, reached from the journal's "Submit manuscript"
   page); the manuscript type: Article (the journal sets no page limit);
   the article type Research; the classification, in this order:
   Foundations of Quantum Mechanics first, since the paper's substance is
   Born's rule, the click as the measurement, Bell and no-signalling on a
   discrete foundational model; Mathematical Physics second; Relativity
   and Gravitation third where a further category is allowed; never a
   broad "General Physics". The venue is decided: Foundations of Physics,
   Springer (link.springer.com/journal/10701); the title page's
   affiliation, email and ORCID are confirmed by the author.
2. The files: `main.tex` with `figures/` as the source (the journal
   recommends its LaTeX template `sn-jnl` and accepts a manuscript in
   another class), `main.pdf` as the compiled output.
3. The cover letter from `COVER_LETTER.md`, with the arXiv identifier
   added; the journal allows a preprint.
4. The declarations are in the manuscript; the system asks for the same
   (funding, competing interests, data availability, the use of a large
   language model, no generative figures) and for the author's ORCID.
5. Suggested and excluded reviewers: optional; the review is single-blind,
   so the title page stays as it is.
6. What the editor may still ask: the Springer Nature template's title
   block (a mechanical change of the preamble, the text untouched) and
   the version DOI of the archive; both are hours, not days.

## What the author must supply that the repository cannot

- The arXiv account (and an endorser if asked), the category choice and
  the licence choice.
- The journal's account and the submission itself.
- The release tag on GitHub and the Zenodo version DOI (with the Boss).
- His word on the second part: the experiments after their runs on the
  engine, a paper of their own.

## Common causes of a desk rejection, checked against the paper

- Out of the journal's scope: the paper is a foundational model of
  quantum and relativistic phenomena with its method stated; the cover
  letter names the journal's own precedents ('t Hooft; Harrigan and
  Spekkens).
- Overclaiming in the title or abstract: the abstract says what is exact,
  what is a hypothesis under its own name, and that nothing is run; the
  paper's last section lists what is open and what is not claimed.
- Missing or incomplete declarations: funding, competing interests,
  ethics, consent, data, code, author contributions and the use of a
  large language model are all present, in the journal's list.
- Undisclosed use of generative tools: the declaration states the model's
  maker, the tool, the year, the extent, the author's direction and
  responsibility, and that the model is not an author; the cover letter
  repeats it; no figure is generative.
- Duplicate or simultaneous submission: the arXiv preprint is allowed by
  the journal and is named in the cover letter; the paper is submitted to
  one journal.
- Unavailable data or code: the archive's concept DOI is in the
  declaration; the version DOI is added at the release.
- References incomplete or mostly self-citations: every external claim
  has a published source; the project's own documents are cited by the
  name of their sections, at the archive.
- Poor English or structure: the paper follows the structure of the
  field's papers (the object, the theorems, the derivations, the
  hypotheses, the comparison, the limits); reviewers still check the
  language.
- Excessive length or a missing methods statement: no page limit at the
  journal; the method is stated in the introduction's reading rule and
  its tree of marks.
- Authorship and identity: one author, a real affiliation, email and
  ORCID on the title page (the author confirms the three).
