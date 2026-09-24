# The submission checklist: arXiv, GitHub and Foundations of Physics

The state at the head of `paper-48` (2026-09-24). What is ready is in the
repository; what only the author can do is marked **the author's hand**.
The order that avoids rework: the GitHub release and its Zenodo version
first, arXiv second (its identifier goes into the cover letter), the
journal third.

## Ready in the repository

- `main.tex`, one document, compiled by `pdflatex` three times with
  standard packages only (geometry, amsmath, amssymb, amsthm, booktabs,
  graphicx, hyperref, caption, float, longtable, array); it compiles from
  a clean directory holding `main.tex` and `figures/` alone, 46 pages, no
  undefined reference.
- `main.pdf`, the compiled output at the same commit.
- `figures/`: the three figures the paper includes (`groups_to_click.pdf`,
  `lattice.pdf`, `octahedron.pdf`), each drawn by its script
  (`groups_figure.py`, `figures.py`, `octahedron.py`) from the
  definitions, none by a generative tool; the five figures of the
  records file beside them.
- `records.tex`, the paper's records (the register, the proofs, the
  hand-worked update, the tables and the sections moved to history),
  cited as one reference; a source file of the archive, not a document
  to compile.
- The title page: the title, the author's name, affiliation, email and
  ORCID.
- The abstract: 245 words (the journal's template asks 150 to 250),
  1453 characters (arXiv allows 1920).
- Keywords after the abstract (six).
- The declarations in the journal's list: funding, competing interests,
  ethics approval, consent to participate and for publication, data
  availability, code availability, author contributions, the use of a
  large language model.
- The reference list, numbered, in the document itself (no `.bib` file
  is needed).
- `COVER_LETTER.md`, the cover letter for the journal, current with the
  title and the paper's state.
- The archive: the Zenodo concept DOI 10.5281/zenodo.22738746 in the
  data availability statement; the MIT licence in the repository.

## GitHub (the author's hand, with the Boss)

1. Merge PR #1006 (`paper-48`) into `main`.
2. Tag the merge commit as a release (for example `paper-v1`) so that the
   reproduction appendix's commit is a fixed, citable point.
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
   with `gr-qc` as a cross-list for the relativistic chain is the honest
   choice; the moderators may reclassify a foundational lattice model to
   `physics.gen-ph`, which is theirs to decide.
3. The upload: the source, not the PDF alone: `main.tex` and `figures/`
   (the three included figures suffice; the others do no harm), and
   `records.tex` with the records' five figures as ancillary files under
   `anc/`. The bundle `Universe24_arxiv_<commit>.tar.gz` in the author's
   files is that layout, compiled clean at 46 pages.
4. The metadata: the title as in the paper; the abstract as plain text
   (below); the author as on the title page; the licence: CC BY 4.0 is
   the usual choice for a paper whose code is MIT; the comment line:
   "46 pages, 3 figures; code and data at doi:10.5281/zenodo.22738746".
5. After the posting, the arXiv identifier goes into the cover letter.

The abstract as plain text for the arXiv form (the same words as the
paper's, the macros written out):

> The paper has one algebraic object: the integer group ring of a cyclic group, the phase in N_phi steps, on a cubic lattice whose symmetries are the 48 signed permutations, their rotations the group of order 24; six bounded integer operations act at every Node. Outside are detectors and clicks only; a record ends at one comparison, the click, the one non-local step. An amplitude is an integer sum of N_phi-th roots of unity, Born's form its square at the click under one axiom of the apparatus, Born's rule its limit; interference counts, marginals and CHSH are exact rationals. Exact on the lattice: the books, Gauss's law, every direction's pace, the CHSH sum 181/64 from 512 to 8192, 1.05 standard errors from the measurement. Recovered in limits: c = 1/sqrt(3); Tsirelson's value in the joint limit of the grain and the tables' scale; under a shell average Newton's inverse square. Under two named hypotheses, Lorentz's factors and Einstein's step are reached, the equivalence principle under the first alone; the law as built meets the first only. Only a detector's counts and their ratios are compared with nature; every number is computed before its run; the pinned readings fill the table as runs merge, none yet, a miss written as a miss. The bending's 2(1 + gamma) and the atom's 1/j^2 ladder are conjectures. The law as built has no relativistic dynamics; its sequential wheel signals in a pair's order, not its counts.

## Foundations of Physics, Springer (the author's hand)

1. An account on the journal's submission system (Springer Nature's
   Editorial Manager, reached from the journal's "Submit manuscript"
   page); the manuscript type: Article (the journal sets no page limit).
2. The files: `main.tex` with `figures/` as the source (the journal
   recommends its LaTeX template `sn-jnl` and accepts a manuscript in
   another class), `main.pdf` as the compiled output, `records.tex` as
   supplementary material if the system asks for one (the paper cites it
   as its records file).
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
- His word on the open items the paper still carries: the glossary's
  OPEN rows, the venue's name, the referee's proposals the Boss holds.
