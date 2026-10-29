# The hostile reviews of Tensor24's code

Each review is a fresh reader who did not write the code, run on the review branch tensor24-review: it approves only
what it could not break, with evidence it ran. Every change it asks is made before the branch moves to the three
integration branches. The fourth to fourteenth reports are here, the fourth, fifth and the seventh to eleventh with
the probes their authors are to run; the first three stand in the Boss's posts on #2187 (6474866014, 6476982394, 6478559511).

| review | commits read | verdict | the changes, where |
| --- | --- | --- | --- |
| first | dce3c56bd (stage 0a) | approve with changes, R1 to R5 | 36e4cef82 |
| second | 86ee3f5ed to 68de1bef0 (stage 0) | approve with changes, R1 to R11 | 227cde2fe |
| third | 1faf2f65c to 227cde2fe (stages 1 to 3) | approve with changes, C1 to C5 | 81521e0f4; C5 by David's word (6478324607) |
| fourth | 3b606a606 and 4b39f234b (the gate, stage 5) | approve with changes, R1 and four gate follow-ups | 81521e0f4; Sofer's c267a2229, adopted in 2eec73c1d |
| fifth | 81521e0f4, 49c65abfa, 0970b0deb | approve with changes, four | the commit that adds this folder (the checker); the decoder's three are Animate's |
| sixth | 2eec73c1d, 6fa366dbe, 3f9e974ad, 37d2d06e2, 13672be1e (the gate, the fifth's changes, stage 4, tb out) | approve; nine follow-ups, none blocking | the commit that adds sixth/; the gate's one is Sofer's |
| seventh | 814fe5c45, 8469170ad, 823690afc (the gate's text lines, the sixth's follow-ups, the decoder's fixes) | approve with changes, four, all the decoder's | Animate's; the Boss's two follow-ups in the commit that adds seventh/ |
| eighth | 83a0b214a, 3fbbd1cd0, 91226e796 (stage 6) | approve with changes, five, all of the tests | the commit that adds eighth/ |
| ninth | af564daac, 54b9e6a63, 83a0b214a to 927071a14 (stage 6 after the eighth's changes) | approve with changes, two: the load's raises and four gaps of the tests | the commit that adds ninth/; two follow-ups Sofer's |
| tenth | 0ff2ae0dc (the ninth's changes) | approve with changes, two: J of the caller's dtype, and six gaps of the load's tests | the commit that adds tenth/ |
| eleventh | 9e5233d7f (stage 7a) | approve with changes, one: the run back with every divisor row away from 1 | the commit that adds eleventh/ |
| twelfth | ac2f5689f, 69eb983f9, 06c823ca2 (the decoder after the seventh review, the gate's amendment 4) | approve with changes, six, all the decoder's | Animate's, asked on #2187 |
| thirteenth | fc8c810ff, 610fef782, d61cdb7bd, e0c52c053 (the engine since the tenth) | approve with changes, two of text: the charge identity's condition, and item (u) put to the owner | the commit that adds thirteenth/ |
| fourteenth | cb7a54943, c98cf9154, a49138552, 1de239790, 1a4d1fdfe (the merged engine tests, the files' one checker, the room by file) | approve with changes, four: the room counted twice, the checker's tests, the keys hidden from the note KEYS, two of text | the commit that adds fourteenth/ |

From the twelfth on, a review leaves its report alone here (the owner's word of 2026-10-29, 02:5x UTC, the plan's
decision 26): its probes stay in the reader's scratch, each named in the report, and the Boss gives an author the
probes a change needs. Each probe runs as `python3 -I <probe> <a worktree of tensor24-review> [...]`, its docstring
naming its arguments; its output stands beside it. The copies here are the readers' files but for the text rules: the
fourth report's verdict is in lower case and its two quoted phrases are described; one probe's raw U+2028 is written
as its escape, and the fifth's sketch of tests is renamed decoder_tests_strengthened.py, so pytest does not collect
it.

- fourth/: REPORT.md; gate_weakened.sh (the self-test against weakened scans), gate_floor_sideways.py (floored()
  on a side line), gate_closed_list.py and gate_dynamic_assign.py (dynamic imports beside the closed list).
- fifth/: REPORT.md; decoder_raises.py (the reader's and the tool's raises); decoder_mutants.py (sixteen source
  mutants of the decoder, run against the decoder's tests or against decoder_tests_strengthened.py, the reader's
  sketch of five tests more).
- sixth/: REPORT.md, its follow-ups each with where it went.
- seventh/: REPORT.md; decoder_readings.py (row 15 and the ticks on lawful and broken records), decoder_mutants_s8.py
  (eighteen mutants of the decoder's new text), decoder_tests_s8.py (the reader's sketch of 21 tests, run by
  decoder_tests_s8_run.py) and decoder_precedence.py (row 15's order of decision).
- eighth/: REPORT.md, each change with where it went; source_mutants.py (48 source mutants of stage 6, its L17 and C1
  re-aimed at the ninth's new lines, so it runs at 0ff2ae0dc and after), its output at 91226e796 and after the changes,
  each made with the strings as they stood.
- ninth/: REPORT.md, each change with where it went; new_mutants.py (29 source mutants of stage 6 and a control), its
  output at 927071a14 and after the changes; load_raise.py (the load's raises on files the checker holds, and the
  contraction's time), gradient_kinds.py (the gradient at a train's second kind, and the fine tooth),
  fuzz_files_deepcopy.py (Sofer's fuzz with its harness mended) and gate_board_dodges.py (six wraps the gate
  misses), each with its output; eighth_source_mutants_rerun.out (the eighth's 48 after the ninth's changes).
- tenth/: REPORT.md, each change with where it went; contract_equiv.py (contract against the dense form and a naive
  loop, and its dtypes), mutants_s11.py (34 source mutants of the changed code, its output at 0ff2ae0dc and after),
  proposed_checks.py (the six checks the reader asked, at 0ff2ae0dc and after), load_edges.py, zeros_raises.py and
  gate_alternatives.py, each with its output.
- eleventh/: REPORT.md, the change and each follow-up with where it went; run_back.py (the act's run back, and the
  promises broken), images_full_act.py and images_full_act_all.py (the 24 on the whole act), order_full_act.py,
  stage4_alike.py, local_pure.py with its control, and mutants_s12.py (51 source mutants of stage 7a, its output at
  9e5233d7f and its four survivors after), each with its output.
