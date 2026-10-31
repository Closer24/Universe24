# The sixth hostile code reader (A) on writer A's audit series, 8069c3630..0f7ecfa05, 2026-10-31

(Written by the Boss from the reader's hand-back, the reader's harness having refused the write; the text is the
reader's, shortened in layout. Logs in hcr6a/: gate.log, mutants.log, gmut.log, probe_run.log, shards_old.txt,
shards_new.txt, docgates.log, mut/*.log, mut/*.gate. Worktrees removed; nothing edited, committed or pushed.)

VERDICT on 8069c3630..0f7ecfa05: NOT PASSED

One BLOCKING item, a one-line fix. Everything else holds: the gate no refusal and no note, the shards identical,
probe.txt byte for byte, every named blob matching.

## BLOCKING

B-1. B3 is only moved: the 2 of "both ends" is now spelt as a slice and a 1.
- src/tensor24/decoder/records.py:306, `if ends and len(ends[1:]) != 1:` (d871dd658). For a non-empty ends,
  len(ends[1:]) != 1 is exactly len(ends) != 1 + 1: ENDS is gone, but the constant two still stands, typed as "the
  first and one other", read from no structure (no Mesh, no schema form).
- The gate refuses the check when the 2 is spelt as a sum (mutant G11, len(ends) != 1 + 1, REFUSED as TWICE); the slice
  form escapes the TWICE rule's syntax.
- SECOND.md's B3 fix gives two lawful ways: take the two ends from the schema's own form, or drop the check. The commit
  takes neither. (Unlike B2, where `not lines[1:]` is the audit's own fix and asks only whether a line exists after the
  first; here the code asks whether the count after the first is exactly 1.)
- Fix: drop the arity check (schema.Whole.ends is "both or none", and no run writes whole clicks) and cut its two
  cases, "a click with one end" and "a click with three ends" (tests/test_the_tensor24_decoder.py:146 and :147, the
  ENDS message at :71), on the owner's word about unnecessary tests; or type the schema's field as a pair and read the
  two from that form.

## MINOR

- m-1. C8 half closed: derive/G/g0_lane.py still builds its paths by string (lines 10, 13, 16, 19, 21, 24, 26:
  S + '/derive/G', f'{G}/...', os.path.exists(S + '/check.lock')); SECOND.md's C8 fix names both halves (no float, and
  joinpath). Fix: Path(...).joinpath, or name it open.
- m-2. B1 lawful in kind, but the star now exists twice: records.py:170-171, board() builds its own star only to take
  its length (the audit's lawful class, as SENSES = len(star(1))), a second star beside files.star and load.star (N6's
  class). Fix (the audit's preferred F7): the runner writes the Spokes into the header and the decoder reads them; or
  name the copy open beside N6.
- m-3. derive/boss/hand_per_quantum/universe.json:3 types den 15162856759112389, full_rate 1000 and width 128, second
  copies of examples/tensor24/universe.json's integers (C6's class); before the commit the probe read them from the
  example file. The file is a lawful place for a world (the loader reads it; the gate's DECLARE guards its pinions,
  mutant G7 REFUSED). Fix: name it under C6, or read the integers and the chosen block from the example file and only
  the trains from its own.
- m-4. Nothing guards the removed floats and fakes against coming back: surviving mutants M6 (check.py's whole_ms reads
  2 digits for 3; no test reads check.py), G9 (UNRECORDED_MS = 5000.0 in tools/check.py: the gate's float rule does not
  reach check.py), G10 (board() back to len(sides) * len(("+", "-")): no note, the gate ratchets the old LENGTH hit
  against main, and no test fails). The range weakens nothing; the guard is not there. Fix: a small yes/no test of
  whole_ms and seconds(), and the keeper's float rule over tools/.
- m-5. tb_tables.py (David's blob, F3) keeps a typed basis: line 43, plane = [[1, -1, 0], [0, 1, -1]] (the typed G and
  3 G^-1 and the linear-search root are gone; G = plane plane^T, its adjugate and det computed and checked kept by the
  24). A record probe under the ruling. Fix: read E's basis from engine/kinds if it gives one, or name it open.

Notes, not faults of the range: documents_gates.py gate (3) runs over nothing (tools/numbers.json holds no
"derivation" entry, so derived() cannot fail as things stand; Sofer's file). tests_shape.py:69 gives kinds 80 + SLACK
while the file has 83 lines after 26826b7c5 (the 120 budget holds). B5's axial() reads the count from board.py's
sx, sy, sz = shape by catching ValueError (files.py:84-85), lawful. check.py's bound is a hair stricter (30.04 s
fails, where rounding to a tenth passed it), not a weakening. g0_lane.py and check.py cut seconds by digits, lawful in a
log or message line.

## Each commit against its audit item

- d871dd658: B1 WAYS CLOSED (see m-2); B2 framed CLOSED (not lines[1:]); B3 ENDS NOT CLOSED (B-1); B4 NAMES CLOSED (one
  optional argument per name, any/all, zip(strict=True)).
- da51bca23 (F8, check.py floats): CLOSED; the CI shards identical old against new (shards_old.txt = shards_new.txt).
- 8f17b6884 (F6, hand_per_quantum): CLOSED; probe.txt byte for byte the committed one and 8069c3630's (12.6 s).
- 822caaa4d (F8, documents_gates floats): CLOSED; hash-object 3f8cb47b8be3, equal to origin/scribe-5; the six gates
  hold.
- 17eaaa351 (ROOM slack, the owner's word): CLOSED; only ROOM, SLACK = 40, its comment and five reasons change.
- 26826b7c5 (B5 AXES): CLOSED; the count read from board.py's structure; mutant M5 caught.
- 7fe9af995 (David's five probes): CLOSED; six blobs equal origin/toys-5 733528210; g5_draw.py b27970eb37f2 (the
  patch text not checked; the diff only reads GRIP and W through the loader); see m-5.
- 0f7ecfa05 (C8 g0_lane): the float CLOSED; the joinpath half open and not named (m-1).

## Agreed audit items left open on node-live (at 0f7ecfa05)

B3 (B-1); B6 (schema.py MINOR = len(ADDED), the owner's, on purpose). Gone from the tree: F1, F2, F6 part two; the well
and mesh lays hold no NUM/DEN, SLOTS, PERIOD or the values.append recurrence. Not checked here: the live world's
setting.json pulse (F5, outside the range). Still named open outside the range: C6 (the mesh lay's SCAN), C7, C10,
C13, N1 to N7. No other agreed FAKE or FORBIDDEN item is left unnamed, apart from B-1 and m-1.

## What was run

The worktree at 0f7ecfa05 with .venv linked (removed); mutants in scratch copies. The gate (gate5 scribe_scan.py,
--base origin/main --summary): no refusal, no note, exit 0. Test mutants 6 of 7 killed (M6 survives). Gate mutants:
REFUSED G7 (a pinion off den), G8 (a / and round in g0_lane), G11 (1 + 1 in booked); surviving with no note G9, G10,
G12 (time.time() back in g0_lane, as at base). The probe rerun in a copy. The shards compared; documents_gates.py (six
gates hold); the files tool with none, one and three files. Diffs read: no assert removed or added in the range; no
scribe_scan* file touched; no non-ASCII added. The full check was not run (the other reader runs it).

## The Boss's rulings (02:2x UTC)

- B-1: fix by dropping the arity check and its two test cases (the owner's word on unnecessary tests). Writer A.
- m-1 and m-3: fixed with B-1 (joinpath in g0_lane; the probe reads the example's integers). m-2 and m-5: named open
  beside N6 and as a record probe. m-4: the guard of tools/ is the keeper's float rule, sent to Sofer; no new test.
