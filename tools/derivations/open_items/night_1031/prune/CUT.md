# The test pruner's cut list, on origin/node-live e3adade10 (2026-10-31, written by the Boss from the pruner's hand-back)

28 test functions: 20 KEEP, 8 CUT, about 713 of the 2,696 lines in tests/ (26%).

Why: the run writes only a header, Click lines, an end and a ledger of Count lines (runner/run.py:86-119, 208-213);
schema.py:9-11 says no run writes a Whole, Split, Rate or Books line. Four readers still read those lines (and the
ledger's wind/windings, the header's time_gear, the cards' parts): row 15 (books.py), row 46 (bangs.py),
measure.cone_check and measure.twins. On every real record they print NOT READ. Cut each reader together with its
tests and its line in tools/tensor24_decode.py (lines 79-83); cutting the tests alone leaves four untested readings in
the tool, any of which could drift to SHOWN unseen.

CUT (file names drop the tests/test_the_tensor24_ prefix):
- decoder.py:296 wind read over every train (row 15's second reading, on the ledger's wind, which no run writes)
- decoder.py:355 books close where they hold the click (row 15 on whole clicks; the live books are read by
  shadow.books, decoder.py:575, and on a real run in run.py:291-295)
- decoder.py:464 each law fails on its mutant (five of six laws are row 15's; the sixth duplicates decoder.py:189-197;
  keep law_nothing alone if row 15 stays in the tool)
- decoder_cases.py:236 books read each holding once (row 15's holdings, windings and chains)
- decoder_bangs.py:92 and :154 (row 46; the whole file)
- decoder_measure.py:161 duration and twins (retired whole and rate lines); :179 ledger and tool hold the measurement's
  rules (D8/D6 on retired lines; the Count once check duplicates run.py:229 and decoder.py:252)
- decoder_measure.py:98 in part: keep 107-118 (measure.meshes and measure.past, the live cone shadow.cone reads), cut
  100-106 and their builders (cone_check on retired lines)

After the cuts: lower the ROOM budgets to the new counts (plus the owner's 40 of slack), drop the decoder_bangs entry;
three kept tests assert the tool's output starts with "row 15" (decoder.py:567, decoder.py:510, decoder_cases.py:301)
and need their expected first line changed.

Check before cutting src: whether shadow.py (C5, C6) imports anything from books.py, bangs.py or measure.py's parts
being cut; keep what it uses.

Gaps (not cuts): only examples/tensor24 is run by a test; tensor24-click, -live, -mesh and -well are checked as files
only, so their run, run back and digest are unguarded. read_ledger checks Count lines against schema.Ledger, not
schema.Count (decoder/records.py:350).
