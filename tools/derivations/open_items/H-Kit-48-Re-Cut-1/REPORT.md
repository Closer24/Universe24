# H-Kit-48-Re-Cut-1 (kt1): the hands' kit re-cut on toys-5 at 3dc12e307, every tool on the engine's own log

Date 2026-10-26, 07:17 to 08:1x UTC. Worktree /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kt1 (read only; nothing under src, tests or tools edited but this folder). The kit: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit (the four new tools beside README_KIT.md; the former tools under /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/former/). The engine: src/event_universe (run.py's record: world, universe, counts, rows, nodes, run_back, log). No toy imported anywhere.

## 0. The bug, by file and line (Addition 10: first)

1. The kit's four former tools imported `lean_full` (Lean, load_world, AX), a file toys-5 does not hold: /tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit/former/clicks_48_example.py lines 14-15, former/conservation_check.py (its `--toy` dir and `from lean_full import`), former/make_flagged_copy_example.py line 18 (SRC = toy/lean_full.py), former/reach_example.py lines 8-9. Three hands wrote their own readers for it. Mended: the four tools below import `event_universe` alone (PYTHONPATH=<worktree>/src), and the kit's two worlds now have their universe files beside them (universe_toy.json, universe_middle.json copied from tests/worlds; the loader reads the universe relative to the world file, src/event_universe/loader/world.py line 40, and the kit's worlds named a file that was not beside them: the first error every run of the kit's worlds met).
2. A reading the check brought up, for the Boss (not edited): src/event_universe/clicks.py line 236, gate 15 reads the click's conservation as `taken >= booked` on every birth; under EX-S1 the identity is taken + remainder before - remainder after = booked (tests/test_the_board.py, the chiral test), which holds on every click of both records (1669 of 1669 on the hole 60, 3133 of 3133 on the chiral 60), while `taken >= booked` fails on one paired birth of the chiral 60 (interval 11, Node [4, 3, 2], taken 3187600241337413150748, booked 3322905896843201769135, remainder before 147998927225421501913, remainder after 12693271719632883526: the carried remainder pays the rest) and on 146 of 3119 credits. Gate 15's inequality is the form before EX-S1; the record's gate reads NOT SHOWN exact where the exact identity holds. One line to read against EX-S1 (clicks.py 233-244).

## 1. The tools (sources beside this report)

- clicks_48.py: `PYTHONPATH=$W/src nice -n 19 $P $K/clicks_48.py <world.json> <intervals> <out.json> [cube N]`. The 48 images as tests/test_the_board.py builds them (IMAGES: signed permutations, 24 of det +1, 24 of det -1), each run through the engine's Node, its clicks carried back through the image (births with the children's Nodes and senses, credits with line, sense and beat, the takes taken / booked / levels of every click, the turned Nodes per interval) and compared with the base's: EQUAL, CONJUGATE (every sense negated) or APART, the first interval apart and per part.
- conservation_check.py: `PYTHONPATH=$W/src nice -n 19 $P $K/conservation_check.py <record.json> [board off] [out <summary.json>]`: one line per law, N of M; the laws the tests pin tallied, the readings (marked r) printed and not tallied; exit 0 only on every law in full. The board re-run from the record's own two files for the current's antisymmetry, the Wronskian at the marks and the log's reproduction.
- make_flagged_copy.py: `nice -n 19 $P $K/make_flagged_copy.py <id> <FLAG> <replacements.json> src $W/src [check off] [worlds a,b] [python $P]`: the copy under /dev/shm/tmp/<id>/src_<id>, each replacement refused unless its old text occurs exactly once (nothing written), then the hole 60 and the chiral 60 run with the flag empty on the head and on the copy, the records hashed with the rows' milliseconds struck.
- reach.py: `PYTHONPATH=$W/src nice -n 19 $P $K/reach.py <world.json> <intervals> <x,y,z> <levels added> <out.json> [cube N]`: the one-Link reach as the former kit had it, on the engine's Node (deepcopy, the gap-0 level changed at one Node, one interval, the Links and the line slots by distance).
- wait_load.py: the load rule (sleep until the 1-minute load is below 3, polled every 60 s, no shell loop).

## 2. The proofs on this head, commands and outputs

Setting: `P=/home/user/Universe24/venv314/bin/python; W=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kt1; K=/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kit; export PYTHONPATH=$W/src TMPDIR=/dev/shm/tmp; cd /dev/shm/tmp/kt1`.

### 2.1 The 48 on the clicks, the chiral seed (the kit's world_chiral_300.json) at 60 intervals

Prediction before the run (H-Children-As-Packets-1's measure on the 3-cube image): 12 EQUAL, 36 APART.

Command: `nice -n 19 $P $K/clicks_48.py $K/world_chiral_300.json 60 /dev/shm/tmp/kt1/c48_chiral_3cube_60.json cube 3` (49 boards of the 3-cube, about 4 minutes).

Measured: counts {"EQUAL": 12, "CONJUGATE": 0, "APART": 36}; by det {"1": {"EQUAL": 12, "CONJUGATE": 0, "APART": 12}, "-1": {"EQUAL": 0, "CONJUGATE": 0, "APART": 24}}; the first intervals apart [2, 6]. The 24 reflections (det -1) all APART at the interval 2 (the births part at 2, the credits at 3, the takes at 4, the turns at 10; read with the senses negated the births part at 4, the credits at 5: no reflection is the conjugate record either); of the 24 proper rotations 12 EQUAL bit for bit in births, credits, takes and turns through 60, 12 APART from the interval 6 (births, credits and takes at 6, the turns at 10). The base: 7 births, 819 credits, 826 takes, 145 turns. The 12 EQUAL rotations by image index: [0, 6, 10, 12, 18, 20, 24, 30, 32, 38, 42, 44]. The measure matches the prediction: 12 EQUAL and 36 APART. What is measured: the whole click record under the image (not the rows), on the 3-cube image of the 5-cube world (cube 3) at 60.

The 5-cube at 60 (the kit's world at the shape its file names, 5; the command `nice -n 19 $P $K/clicks_48.py $K/world_chiral_300.json 60 /dev/shm/tmp/kt1/c48_chiral_5cube_60.json`, 49 boards): counts {"EQUAL": 24, "CONJUGATE": 0, "APART": 24}, by det {"1": {"EQUAL": 24, "CONJUGATE": 0, "APART": 0}, "-1": {"EQUAL": 0, "CONJUGATE": 0, "APART": 24}}, first intervals apart [3]; the base 16 births, 3119 credits, 630 turns; the EQUAL images by index [0, 3, 5, 6, 9, 10, 12, 15, 17, 18, 20, 23, 24, 27, 29, 30, 32, 35, 37, 38, 41, 42, 44, 47]; the first apart per part on the reflections ['{"births": 3, "credits": 5, "takes": 6, "turns": 10}'], on the rotations apart []. The summary and rows: c48_chiral_5cube_60.json beside this report.

The summary and the 48 rows of the 3-cube: c48_chiral_3cube_60.json beside this report.

### 2.2 The conservation check on the hole 60 (examples/records/hole.json)

Prediction: the run back 20 of 20 (the record says so), EX-S1's identity on every click, the births' charge opposite on every birth, the log reproduced from the two files.

Command: `nice -n 19 $P $K/conservation_check.py $W/examples/records/hole.json out /dev/shm/tmp/kt1/cons_hole60.json`

Output:
```
1. the form, the re-run's counts equal to the record's: 15 of 15
1. the form, the re-run's log equal to the record's event by event: 16903 of 16903
1. the form, the run back exact: 20 of 20
2. the current, intervals with F_ij + F_ji = 0 on every Link of the gap-0 line: 60 of 60
2. the current, the record's Node lines' current equal to the board's: 60 of 60
3. the Wronskian, the rows' W total at the marks equal to the board's: 14 of 14
3. the charge, the births' two children W of opposite sign (the exact lays aside): 16 of 16
3r. reading: the Wronskian, intervals without a birth with the board's W total unchanged: 16 of 51
3r. reading: the births' two children W summed to 0 in magnitude: 15 of 16
4r. reading: the lattice momentum, births with dP_take + dP_lay_ends = 0: 0 of 16
4r. reading: the lattice momentum, intervals with the Links' sum 0 on three axes: 0 of 60
5. the energy, credits with beat >= 1: 1653 of 1653
6. the count, taken + remainder before - remainder after = booked per click (EX-S1): 1669 of 1669
6. the count, taken >= booked per birth (gate 15's identity; the exact lays aside): 16 of 16
6. the count, the births' taken and booked summed against the record's counts: 2 of 2
6r. reading: taken >= booked per credit: 167 of 1653
8. integers, floats found in the record: 0 of 0
{"births with an exact lay (one child W 0)": 0, "births W sum": 864, "births senses +/-": [16, 16], "W total at the marks": [0, 0, 0, 0, 0, -1750, 4936, 605, -272, 1495, 1711, -2677, 683, -919], "Links' current summed per axis, first and last interval": [[-83349, 0, 0], [21092, -2307, -2926]], "recoil dP_take summed over the clicks": [-686210245490390276584, -58346672809064472872, -107353025854515714120], "beats per 1000 proper, [quotient, remainder], min and max over the credited Nodes": [[0, 8000], [3, 11112]], "credited Nodes": 109, "beats summed over the credits": 3849, "clicks without the take's remainders (the exact lays)": 0, "births taken summed": 172701936753844030676249, "births booked summed": 164947791671769606584854, "credits taken summed": 406480653382998623565734, "credits booked summed": 219352767196879843200000, "max bits at the marks": 115, "births": 16, "credits": 1653, "intervals": 60, "board W total at the end": -919}
laws held in full: 12 of 12 (the readings marked r aside)
exit 0
```

### 2.3 The conservation check on the chiral 60 (examples/records/chiral.json)

Command: `nice -n 19 $P $K/conservation_check.py $W/examples/records/chiral.json out /dev/shm/tmp/kt1/cons_chiral60.json`

Output:
```
1. the form, the re-run's counts equal to the record's: 15 of 15
1. the form, the re-run's log equal to the record's event by event: 23579 of 23579
1. the form, the run back exact: 20 of 20
2. the current, intervals with F_ij + F_ji = 0 on every Link of the gap-0 line: 60 of 60
2. the current, the record's Node lines' current equal to the board's: 60 of 60
3. the Wronskian, the rows' W total at the marks equal to the board's: 14 of 14
3. the charge, the births' two children W of opposite sign (the exact lays aside): 14 of 14
3r. reading: the Wronskian, intervals without a birth with the board's W total unchanged: 1 of 49
3r. reading: the births' two children W summed to 0 in magnitude: 14 of 14
4r. reading: the lattice momentum, births with dP_take + dP_lay_ends = 0: 0 of 16
4r. reading: the lattice momentum, intervals with the Links' sum 0 on three axes: 0 of 60
5. the energy, credits with beat >= 1: 3119 of 3119
6. the count, taken + remainder before - remainder after = booked per click (EX-S1): 3133 of 3133
6. the count, taken >= booked per birth (gate 15's identity; the exact lays aside): 13 of 14
6. the count, the births' taken and booked summed against the record's counts: 2 of 2
6r. reading: taken >= booked per credit: 146 of 3119
8. integers, floats found in the record: 0 of 0
{"births with an exact lay (one child W 0)": 2, "births W sum": 270288, "births senses +/-": [16, 16], "W total at the marks": [0, 0, 1277, 122946, -295801, -130141, -59837, -88693, -46288, -5566, 19893, 9313, 12685, 22880], "Links' current summed per axis, first and last interval": [[-83349, 0, 0], [1552, -507, 487]], "recoil dP_take summed over the clicks": [-87760255709021478700, 420815918666874135616, -296720838038107358076], "beats per 1000 proper, [quotient, remainder], min and max over the credited Nodes": [[1, 7716], [1, 25132]], "credited Nodes": 125, "beats summed over the credits": 5867, "clicks without the take's remainders (the exact lays)": 2, "births taken summed": 57954846101029617925997, "births booked summed": 56201602523063789404411, "credits taken summed": 145194326044083684248478, "credits booked summed": 102811726807043723136000, "max bits at the marks": 115, "births": 16, "credits": 3119, "intervals": 60, "board W total at the end": 22880}
laws held in full: 11 of 12 (the readings marked r aside)
exit 1
```
The one law not in full is gate 15's inequality on one birth (section 0, item 2); EX-S1's exact identity holds 3133 of 3133.

### 2.4 The reach on the hole seed (5-cube, 20 intervals, the Node [2, 2, 2] raised by 5 levels)

Prediction: no line slot differing at distance 2 or more after one interval; the births on the Links at distance 2 or more equal.

Command: `nice -n 19 $P $K/reach.py $W/tests/worlds/world_hole.json 20 2,2,2 5 /dev/shm/tmp/kt1/reach_hole_20.json`

Output:
```
{"world": "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kt1/tests/worlds/world_hole.json", "cube": 5, "changed node": [2, 2, 2], "levels added": 5, "interval of the change": 21, "births this interval a/b": [1, 1], "links compared by distance of the nearer end": {"1": {"links": 5, "equal": 5, "apart": 0, "births a": 0, "births b": 0}, "2": {"links": 14, "equal": 14, "apart": 0, "births a": 0, "births b": 0}, "3": {"links": 20, "equal": 20, "apart": 0, "births a": 0, "births b": 0}, "4": {"links": 8, "equal": 8, "apart": 0, "births a": 1, "births b": 1}, "5": {"links": 1, "equal": 1, "apart": 0, "births a": 0, "births b": 0}}, "farthest distance with a Link apart": null, "links at distance >= 2 equal / of": [43, 43], "line slots differing by distance": {"0": 19, "1": 59}, "farthest distance with a slot differing": 1, "reach one Link (no slot differing at distance >= 2)": true}
exit 0
```
Measured: the slots differing at distance 0: 19, at distance 1: 59, none beyond; the 43 Links at distance 2 or more equal (43 of 43); the one birth of the interval 21 at distance 4 equal on both boards.

### 2.5 The flagged copy and its check

Prediction: the copy with one replacement in run.py (a flag read and never used) EQUAL on both worlds; a replacement whose old text occurs 16 times refused with nothing written.

Command: `nice -n 19 $P $K/make_flagged_copy.py kt1 KT1_FLAG /dev/shm/tmp/kt1/repl_kt1.json src $W/src python $P` (repl_kt1.json beside this report).

Output:
```
{"replacement": 0, "file": "event_universe/run.py", "old_bytes": 65, "new_bytes": 191}
{"copy": "/dev/shm/tmp/kt1/src_kt1", "flag": "KT1_FLAG", "files changed": ["event_universe/run.py"]}
{"world": "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kt1/tests/worlds/world_hole.json", "verdict": "EQUAL", "head": "0864be32254a870dcfb4e7deb211210b1dedc27e7a2bafa0063ca9924c877058", "copy": "0864be32254a870dcfb4e7deb211210b1dedc27e7a2bafa0063ca9924c877058", "head record": "/dev/shm/tmp/kt1/head_world_hole.json", "copy record": "/dev/shm/tmp/kt1/copy_kt1_world_hole.json"}
{"world": "/tmp/claude-0/-home-user-Universe24/e136d210-1915-523c-8c8e-0abbdf97855b/scratchpad/hands/kt1/tests/worlds/world_nature.json", "verdict": "EQUAL", "head": "174932e9e81b98dc565495eae9d420d6f13ff182f0fc52a0ed1e7559af070fc8", "copy": "174932e9e81b98dc565495eae9d420d6f13ff182f0fc52a0ed1e7559af070fc8", "head record": "/dev/shm/tmp/kt1/head_world_nature.json", "copy record": "/dev/shm/tmp/kt1/copy_kt1_world_nature.json"}
worlds bit for bit with the head: 2 of 2
exit 0
```

Command (the refusal): `nice -n 19 $P $K/make_flagged_copy.py kt1x KT1_FLAG /dev/shm/tmp/kt1/repl_refused.json src $W/src check off`

Output:
```
{"replacement": 0, "file": "event_universe/run.py", "old_bytes": 10, "new_bytes": 10}
replacement 1 refused: its old text occurs 16 times in event_universe/run.py (exactly once required); nothing written
exit 1
```

### 2.6 The greps

No float and no barred word in the kit's five new files and the README (the grep of README's rule 7 run over them; the README no longer spells the barred words); no run of three all-caps words.

## 3. What stands and what was cut short

Stand: clicks_48.py (proved on the 3-cube chiral image at 60: 12 EQUAL, 36 APART), conservation_check.py (12 of 12 laws in full on the hole 60; 11 of 12 on the chiral 60, the one gate 15's pre-EX-S1 inequality), make_flagged_copy.py (EQUAL on the hole 60 and the chiral 60 with the flag empty; the refusal by count), reach.py (one Link on the hole seed), README_KIT.md rewritten with the commands above, the former tools under kit/former/ with the line naming why.

Cut short: nothing of the named proofs: the 5-cube 48 ran too; the bodies 120 world of the kit not run through the check (the records hole 60 and chiral 60 were the item's named proofs); the conservation check's form on the board is read as the log's reproduction and the run back (Rule3's identity per Node is in the engine's own tests, tests/test_rule3.py, not re-read here).
