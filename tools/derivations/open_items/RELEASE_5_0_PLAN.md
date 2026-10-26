# The plan for the commit of engine 5.0 onto main (the owner's word of 2026-10-26, 17:1x UTC; his word is needed at step 7 and at nothing else)

Main is the released state of the project and nothing reaches it but a release. This plan is the order of that one commit, with every gate it must pass, what it carries, what it leaves behind, and the one decision that is the owner's.

## 1. Where the two branches stand (measured 17:1x UTC)

| what | main | engine-5.0-test |
|---|---|---|
| head | 4326fecce, the version 4.0.0 released 2026-10-25 | 536 commits ahead, 2 behind |
| the engine's source | the 4.0 engine | the 5.0 engine (the click one act, the Node's core, the booking, the take's count, the lay one act) |
| tests, in lines | 5,138 | 2,226 (the suite re-cut; the ratchet's whole point) |
| the reader's folder | none | 432 files, about 190 MB of pages, readings and frames |
| the hands' folders | none of this cycle | 10,138 files under tools/derivations |
| the documents | the 4.0 law | the 5.0 law with every sentence of the cycle |

The two commits main holds and the branch does not are main's own return of 2026-10-24 and the 4.0.0 version bump: they merge into the branch BEFORE anything else, so the release does not revert main.

## 2. What must be true before the commit (the gates, in order, every one exiting 0)

1. The branch's own full check at a quiet load: `$S/bin/full_check.sh $S/e5 6703dd95c` exits 0 and the push is green (the standing rule: push only on exit 0, main never touched before the release).
2. The six folds of the engine are in and confirmed (ENGINE_5_PLAN.md section 2): a release of a half-folded engine would carry two spellings of acts the law spells once.
3. Main's two commits merged into engine-5.0-test and the conflicts resolved by name (expected: the version files alone).
4. A confirming hand on the release itself (H-Confirm-Release-5-1): the merge of main into the branch read whole, then the seven gates on the merged tree with CHECK_BASE set to main's head, every one named with its exit and its reason, the suite's own times against the ten-minute ceiling per shard and the thirty-second bound per test, and the record tests' pins read against the committed readings. Its report lands before the commit.
5. The ratchets' baseline, which is the one real obstacle and needs David first: tools/tests_shape.py, tools/record_code_shape.py, tools/engine_gates.py and tools/documents_gates.py all compare a head against a base. At a release the base is main at 4.0, so the comparison is between two different engines and means nothing (tests fell from 5,138 lines to 2,226, which the gate reads as a pass for the wrong reason, while the code shape and the module counts read as breaches for the wrong reason). **The mend, David's, one clause in tools/check.py and the four gates: at a release commit, named by the version bump in pyproject.toml, the ratchets take their base from the released branch's own previous head, not from main, and print that they did.** Without it the first run of the checks on main after the push is noise, and noise on main is what a release must never leave.
6. The release's own files, in one commit with the merge: the version 5.0.0 in pyproject.toml and CITATION.cff with the date, the CHANGELOG's Unreleased section closed as 5.0.0 with the cycle's laws by name, .zenodo.json, and every document that names the version (README.md, index.html, llms.txt, the papers' front matter).
7. **The owner's word on what the release carries**, the one decision that is his and not mine:
   - the engine, the tests, the documents, the examples and the tools that gate: carried, no question;
   - **the reader's folder (about 190 MB of pages, readings and frames)**: my recommendation is to carry the table of the gates, the readings of the committed records and ONE folder of pages (the newest), and to leave the older folders on the branch, naming them in the changelog. A released repository of a quarter of a gigabyte of generated pages serves nobody who clones it, and the pages are regenerated from the records by one command.
   - **the hands' folders (10,138 files under tools/derivations)**: my recommendation is to carry them whole. They are the project's derivation record, every law's proof and every refusal's measure, they are text, and a law without its derivation is an assertion.

## 3. The order of the commit itself

1. The branch green and the folds in (section 2, items 1 and 2).
2. David's release clause for the ratchets (item 5), confirmed like any build.
3. `git merge origin/main` into engine-5.0-test; the version files resolved to the release's own numbers; the push green.
4. The release's files written (item 6) and pushed on the branch.
5. H-Confirm-Release-5-1 reports; every refusal mended and the report re-run until it names none.
6. The owner's word on the carry (item 7) and on the release itself.
7. The commit onto main: a merge of engine-5.0-test into main with no fast forward, its message naming the release, the laws of the cycle and the branch's head sha; no force, no rewrite, no pull request (the owner's standing rule), main's history kept.
8. The tag 5.0.0 on that commit, the Zenodo deposit as the former releases, and the branch left standing for the next cycle.
9. The checks run on main by their own workflow at the push: their result is read and named here within the hour. A red check on main after a release is the release's own failure and is mended at once on the branch and re-committed, never left.

## 4. What the release does NOT do

It does not change a law (the laws it carries are the ones the owner approved, each by name and date); it does not touch the records' own courses; it does not rewrite main's history; it does not open a pull request; and it does not wait for the open derivations (the child's axis, the matter, the bang's one record): those are the next cycle's, and the changelog names them as open by name, since a release that hides its open questions is a worse release than one that names them.

## 5. The rollback, in one line

Main's previous head is kept by its sha in the release's message and by the tag of 4.0.0; a release found broken is returned by one revert commit on main, as main was returned on 2026-10-24, and the branch carries the mend.
