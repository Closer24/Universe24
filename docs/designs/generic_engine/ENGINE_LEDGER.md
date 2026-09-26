# The engine's ledger: what is implemented, what is to do

The model owner's word of 2026-09-26 (11:35Z, in Nature24's session): one place that says
what the engine implements and what is still to do; the engine is closed when everything has
moved to "implemented" and the "to do" column is empty. One row per generic support and per
family attribute; each row names where the support lives and the test that proves it. A row
without a green test stays "to do". The Boss owns the ledger; Nature24 is the second party who
checks each row; The 3 moves a row by landing its build and its test. Read from emitter-click
01109b05 and stroke-side 2ec28033; the attributes' detail is in FAMILY_ATTRIBUTES.md.

## 1. Implemented

| Support | Where | The test that proves it |
| --- | --- | --- |
| the rule, one step at every Node (9.57 (1), 9.91 (2)) | `events/rule.py` | the one step equal to the rule's transcription bit for bit on random arrays (`docs/designs/rule_alone/rule_alone.py`); the resting worlds bit for bit at every commit |
| the representation as parts, 1, 1 + 3, 1 + 3 + 6 (9.86) | the loader's `parts`, the stepping of every component | the leak test per part (commit 2) |
| the four paces from the reads (9.91 (2)) | commit 3 | bit for bit with the tensor zero |
| the held source of a body: the count, its factors, its dipole (9.91 (3)) | the loader's `held` | the holds' tests of commit 2 |
| the reads with a positive weight and a twist | the loader's `reads` | the digests of the shipped worlds |
| the wall W = 3 Q M | commit 4 | its test |
| the charge's four components with light as its wave, the transport (9.86, 9.81 (2)) | commit 4 | its tests; the twist table provisional |
| the point emitter as the law's one giving (9.69 (2), 9.85 (5)) | commit 7 | the point emitter's tests |
| the four-vector click without the recoil | commit 5 in part (01109b05) | its tests |
| the spin's step and the self-source slot | commit 6 in part, provisional | its tests |
| the click journal and the backward run | record 2070's build | the property test |
| the families file and the leak test (record 2075) | `universe.json`, the runner | a family with no source exactly zero at every interval |
| the cancel of the ray law, nothing deleted | stroke-side, merged | `tests/test_cancelled_paths.py` |
| the check-mode worlds' generator | stroke-side, merged | `tests/test_check_mode_worlds.py` |
| the engine start file, every default out of the code (record 2089) | `examples/events/engine_start.json` | its test |

## 2. To do

| Support | What is missing | The test that will prove it |
| --- | --- | --- |
| a signed read weight, a hill (9.108 (8)) | the loader bounds the weight from 1 | a family with a hill on gravity behaves as a hill against the algebra's number, no code touched |
| the source verb of a record (9.98 (11) (b), 9.108 (10) (a)) | no record adds its count into a family's level; only the body's hold and the field's self source | a sourced family's level equals the static response to a held record, in integers |
| the guard on both sides of the pace, at run time | the load's guard alone, from below | a world whose content reaches Gamma or 0 at run time stops with the guard's line |
| the click that keeps the momentum (9.109 (2)) | the recoil's store in the Ports' accumulators | one body keeps its speed across clicks; the ninth question's rerun in the engine |
| a free body moving by the rule (record 2168 (3)) | the pair well and the hop still there | the falling body of item 1 as a world file, no `fixed` |
| the internal representation as a family attribute (9.88 (7) (i)) | the primitives are a draft with no attribute and no hook | a family of n pairs transported around a loop returns to itself |
| the twist table's precision (9.96 (2) (c)) | the fine table all identities | the mathematician's line and its test |
| the attribute set as generic terms (9.88 (7) (ii)) | the loader admits a fixed set of keys | an attribute declared only in the file gives its effect with no code change |
| universe.json and the words of record 2128 | the words in part | the loader reads `universe`, `q`, `stocks` and refuses the old words |
| the residue lines and the eight failing tests | listed in docs/CANCELLED_WORLDS.md section 9 | the gate green |
| commit 10, the convergence test | not run | the check-mode table blind with everything on, the rule of three per row |
| no flag, family name or number in the code (records 2172 to 2174) | the review after the merge | a grep of `src/event_universe`, empty |

## 3. The closing condition

The engine is closed when section 2 is empty and every row of section 1 has its green test on
main. From then on a force, a coupling or a well is a line in the files, and a run in check
mode is how it is tried.

Every row of this ledger is tried from run files alone: the world file, the universe file and
the start file, run by the one command (`tools/run_inputs.py`), with the engine never rebuilt
for it (the model owner's word of 2026-09-26, 11:45Z). The test of the closing: if trying a
thing needs a line of code, the engine is not closed.
