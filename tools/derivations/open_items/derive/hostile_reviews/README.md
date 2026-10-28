# The hostile reviews of Tensor24's code

Each review is a fresh reader who did not write the code, run on the review branch tensor24-review: it approves only
what it could not break, with evidence it ran. Every change it asks is made before the branch moves to the three
integration branches. The fourth to seventh reports are here, the fourth, fifth and seventh with the probes their
authors are to run; the first three stand in the Boss's posts on #2187 (6474866014, 6476982394, 6478559511).

| review | commits read | verdict | the changes, where |
| --- | --- | --- | --- |
| first | dce3c56bd (stage 0a) | approve with changes, R1 to R5 | 36e4cef82 |
| second | 86ee3f5ed to 68de1bef0 (stage 0) | approve with changes, R1 to R11 | 227cde2fe |
| third | 1faf2f65c to 227cde2fe (stages 1 to 3) | approve with changes, C1 to C5 | 81521e0f4; C5 by David's word (6478324607) |
| fourth | 3b606a606 and 4b39f234b (the gate, stage 5) | approve with changes, R1 and four gate follow-ups | 81521e0f4; Sofer's c267a2229, adopted in 2eec73c1d |
| fifth | 81521e0f4, 49c65abfa, 0970b0deb | approve with changes, four | the commit that adds this folder (the checker); the decoder's three are Animate's |
| sixth | 2eec73c1d, 6fa366dbe, 3f9e974ad, 37d2d06e2, 13672be1e (the gate, the fifth's changes, stage 4, tb out) | approve; nine follow-ups, none blocking | the commit that adds sixth/; the gate's one is Sofer's |
| seventh | 814fe5c45, 8469170ad, 823690afc (the gate's text lines, the sixth's follow-ups, the decoder's fixes) | approve with changes, four, all the decoder's | Animate's; the Boss's two follow-ups in the commit that adds seventh/ |

Each probe runs as `python3 -I <probe> <a worktree of tensor24-review> [...]`, its docstring naming its arguments;
its output stands beside it. The copies here are the readers' files but for the text rules: the fourth report's
verdict is in lower case and its two quoted phrases are described; one probe's raw U+2028 is written as its escape,
and the fifth's sketch of tests is renamed decoder_tests_strengthened.py, so pytest does not collect it.

- fourth/: REPORT.md; gate_weakened.sh (the self-test against weakened scans), gate_floor_sideways.py (floored()
  on a side line), gate_closed_list.py and gate_dynamic_assign.py (dynamic imports beside the closed list).
- fifth/: REPORT.md; decoder_raises.py (the reader's and the tool's raises); decoder_mutants.py (sixteen source
  mutants of the decoder, run against the decoder's tests or against decoder_tests_strengthened.py, the reader's
  sketch of five tests more).
- sixth/: REPORT.md, its follow-ups each with where it went.
- seventh/: REPORT.md; decoder_readings.py (row 15 and the ticks on lawful and broken records), decoder_mutants_s8.py
  (eighteen mutants of the decoder's new text), decoder_tests_s8.py (the reader's sketch of 21 tests, run by
  decoder_tests_s8_run.py) and decoder_precedence.py (row 15's order of decision).
