# Validation evidence

Since 2026-09-17, by the model owner's decision in
[Highlights 5.5](HIGHLIGHTS.md#55-acceptance-tests-and-open-decisions), this is
the record of research runs and physical milestones: a phenomenon that several
rules produce together, an example world's numbers, a comparison of two worlds
or a known experiment is one run of the engine, made once, recorded with a
source fingerprint and a date, and never repeated as a test. Tests and their
expected integers are listed in [test expectations](TEST_EXPECTATIONS.md). A
change is checked against the tests selected by the import graph; the whole
suite runs together only when the shared core changes, and then once, in
parallel. Entries below keep the scope they had when recorded.

## Series G under the law's line drive: four runs on drive-default de55417 - 2026-09-22

The branch `drive-default` at `de55417` (the generator's momenta by the
line rule committed before the run, DEFAULT.md section (c), with a new
`expectations.json`): the four worlds of `examples/events/hubble/` run
through `tools/run_series.py --jobs 4` (Python 3.14.0rc2, numpy 2.5.3,
headless; source fingerprint `760e373a542f918f`, the merged tree), every run completed
at 400 intervals with the books balanced at every tick, `run.json`
carrying `"drive": "line"`; the digests (state, audit, events)
`37da0b5205c1`, `43e88eac951e`, `70c0b242d3fa` (`coasting_scalar`),
`c7247f008801`, `9c470be9ac7b`, `6e70f694d6ec` (`coasting_age`),
`672dead38b8b`, `80eb8d08988b`, `48138918d9ff` (`pushing_scalar`),
`abe82f4dd214`, `ede6cf6b118d`, `4e38b22ccf75` (`pushing_age`); run times
59.5 to 64.6 s at 293 to 296 MB peak (host measurements). The gate world
`hubble/pushing_age` replayed at its cap 1: its state and books moved
with the momenta and are re-pinned in `gate_set.json` (`d4d6a113...`,
`a128731b...`; the events none at the cap; the flip day's `ec7ec1d8...`
in git at de55417, the per-axis under `former`). The readings by kind
(230 inside, 22 outside in the detector's own clock; `coasting_age` H
t_0 = 1.0102) are in [the series' README](../examples/events/hubble/README.md#re-read-under-the-laws-line-drive-2026-09-22-measured-against-the-pins-of-expectationsjson-committed-at-de55417-before-the-run)
and [the register](EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20).
The re-read in the detector's own clock under the per-axis drive stays
registered as the reading the paper's rows rest on.

## Series G2 under the law's line drive: eighteen runs on drive-default f187059 - 2026-09-22

The branch `drive-default` at `f187059` (the generator's momenta by the
line rule committed before the run, DEFAULT.md section (c); both
registers with the drive named): the nine worlds of
`examples/events/hubble_stars/` and the nine of `record/` run through
`tools/run_series.py --jobs 4` (Python 3.14.0rc2, numpy 2.5.3, headless;
source fingerprint `e67f6b9a5469d75d`, the flip's engine before the merge with main's
generic entry), every run completed at 400 intervals with the books
balanced at every tick, `run.json` carrying `"drive": "line"`; the
digests in [the series' README](../examples/events/hubble_stars/README.md#re-read-under-the-laws-line-drive-2026-09-22-measured-against-the-pins-of-expectationsjson-and-recordexpectationsjson-committed-at-f187059-before-the-run);
run times 62 to 76 s at 308 to 319 MB peak (host measurements).
`tools/hubble_stars_readings.py`: the reading's formula 648 of 648, the
luminosity 648 of 648, 1340 readings inside, 19 outside (the scalar
clock's worlds, as in every registration; `double_none`'s q 0.06 above
its bracket; `coasting_age`'s nearest form), none moved; the coasting
form the Milne form exactly (`record/coasting_none` q = -0.104, H (t_0 +
T_0) = 1.0232, the re-run at head's numbers to the digit). The runs of
2026-09-20 to 2026-09-22 stay registered as the readings the paper's rows
3 and 4b rest on, under the drive they name.

## Series D under the law's line drive: eight runs on drive-default 01178c9 - 2026-09-22

The branch `drive-default` at `01178c9` (the generator's pins under the
line drive committed before the run, DEFAULT.md section (c): n = 4, 6, 10
at S = 1, 8, 32, `expectations.json`): the eight worlds of
`examples/events/orbit/` (the six and the two lamp worlds, unchanged) run
through `tools/run_series.py --jobs 4` (Python 3.14.0rc2, numpy 2.5.3,
headless; source fingerprint `e67f6b9a5469d75d`), every run completed at 4000
intervals with the books balanced at every tick, `run.json` carrying
`"drive": "line"`; the digests (state, audit, events) `59be4ca61a3d`,
`1aaa91745a3f`, `71a07e974623` (`s1_r12`), `9290bd45da8a`,
`093ee9a4f342`, `0864d3f9b739` (`s1_r24`), `427229f38496`,
`0dbe076f857d`, `2b62770b018a` (`s8_r12`), `5290784349c1`,
`1b1309bb81ea`, `5aa469e76af2` (`s8_r24`), `c80fafec6823`,
`ffa81ca1cd85`, `7fa866a5c1ca` (`s32_r12`), `df0e4a62fdda`,
`4042645cc047`, `51ac141d66d5` (`s32_r24`), `b16ee1dc218a`,
`b47bb336a684`, `e2d5f8cde2fe` (`s32_r12_lamp`), `a0a4562bc3fc`,
`83189e4e0aec`, `6e49bb6b6cae` (`s32_r24_lamp`); run times 10 to 15 s
(host measurements). The readings by kind (no orbit closed by the
criterion; the first Link exactly as pinned in all eight; the lamp
worlds' loops the S = 32 worlds' to the Link) are in
[the series' README](../examples/events/orbit/README.md#re-read-under-the-laws-line-drive-2026-09-22-measured-against-the-pins-of-expectationsjson-committed-at-01178c9-before-the-run)
and [the register](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19).
The runs of 2026-09-19 to 2026-09-21 stay registered as the readings the
paper's rows of series D rest on, under the drive they name.

## Series H under the law's line drive: seven runs on drive-default 543d202 - 2026-09-22

The branch `drive-default` at `543d202` (the generator's pins under the
line drive committed before the run, DEFAULT.md section (c): p(8) =
346015159, h = 5536242544, `expectations.json`): the seven worlds of
`examples/events/bohr/` run through `tools/run_series.py --jobs 4` (Python
3.14.0rc2, numpy 2.5.3, headless; source fingerprint `e67f6b9a5469d75d`),
every run completed at its declared intervals (3000 to 10400) with the
books balanced at every tick, `run.json` carrying `"drive": "line"`; the
digests (state, audit, events) `44017b44f66b`, `c2d460c3f1a5`,
`7b4cc6dedd12` (`r2`), `18eb629c707b`, `7cb5dbcf37d7`, `9fd752af138b`
(`r4`), `88b7b85a9666`, `3912506e4c30`, `1b1eccd2798d` (`r6`),
`f4f00d3b7ad2`, `775bd147c597`, `da83bca6186a` (`r8`), `f679e97bc54b`,
`92077bd37aa5`, `f130c0bdbaa3` (`r12`), `19d1004433c1`, `81c0dc66c280`,
`789a21214a5c` (`r15`), `cc0d52b69e70`, `fe47bb711572`, `ec97eb215469`
(`r16`); run times 47 to 190 s at 82 to 354 MB peak (host measurements).
The gate world `bohr/r2` replayed at its cap 689 with the world's new
momentum and action: its digests moved again and are re-pinned in
`gate_set.json` (`02b91cd0...`, `51fe825f...`, `fe666ff9...`; the flip
day's `66a8f776...` at the registered integers in git at 5b3c7686, the
per-axis digests kept under `former`). The readings by kind (no
coherence reading at any radius; the first Link exactly as pinned at
every radius) are in [the series' README](../examples/events/bohr/README.md#re-read-under-the-laws-line-drive-2026-09-22-measured-against-the-pins-of-expectationsjson-committed-at-543d202-before-the-run)
and [the register](EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20).
The runs of 2026-09-20 stay registered as the readings the paper's rows
of series H rest on, under the drive they name. The atoms series' three
worlds (`examples/events/atoms/`, unchanged by the flip: their momenta
were derived for this drive) ran once each on the same checkout
(`tools/run_series.py --jobs 3`; the digests `80425f1adcab`,
`92077bd37aa5`, `e0ee793f1653` for `hydrogen_r12` in 126 s,
`ac10ba004826`, `acedae509e82`, `6bd33ee057e2` for `hydrogen_r12_centred`
in 135 s, `cb93a6bbed5c`, `5714d91bea4e`, `1a169e20d306` for `helium_r12`
in 236 s), every run completed with the books balanced; the readings
against the pins of PINS.md and CENTRED_STEP.md section 4 are in
[the atoms' README](../examples/events/atoms/README.md) (the centred loop
stays for the run with the periods 1421, 1410, 1310; helium's pair
scattered by a close pass).

## Series D3 under the law's line drive: five runs at n = 10 on drive-default ec267fe - 2026-09-22

The branch `drive-default` at `ec267fe` (the generator's pins under the
line drive committed before the run, DEFAULT.md section (c)): the five
worlds of `examples/events/orbit_lamp/` run through `tools/run_series.py
--jobs 4` (Python 3.14.0rc2, numpy 2.5.3, headless; source fingerprint
`e67f6b9a5469d75d`), every run completed at 4000 intervals with the books
balanced at every tick, `run.json` carrying `"drive": "line"`; the digests
(state, audit, events) `f9246d61f777`, `a9b7a6558894`, `a389fa9f2fdc`
(`r12`), `abad1975b63d`, `b455040b33b4`, `51017b7f689f` (`r24`),
`976cc8449f69`, `e4d5fe6d4762`, `0235dd02ef23` (`r24_4m`),
`f7c89f2266e3`, `467d6e37fcaa`, `58d4c1b72ec0` (`r12_control`),
`71ed70737f6c`, `467d6e37fcaa`, `f56c7ee96593` (`r24_control`); run times
25.8, 26.7, 26.5, 11.5 and 10.8 s (host measurements). The readings by
kind and their verdicts (4 inside, 12 outside, none moved) are in
[the series' README](../examples/events/orbit_lamp/README.md#the-re-run-under-the-laws-line-drive-at-n--10-2026-09-22-measured-against-the-pins-of-expectationsjson-committed-at-ec267fe-before-the-run)
and [the register](EXPERIMENTS.md#d3-newton-after-a-detector-2026-09-22).
The per-axis re-run at n = 9 stays registered as the reading the paper's
D3 row rests on, under the drive it names.

## The line drive the law's drive: the gate set replayed under the flip on main 6cfea3c6 - 2026-09-22

The branch `drive-default` from main `6cfea3c6` (the model owner's word,
record 972; [the design](designs/drive_b/DEFAULT.md); the key `drive_b`
deleted, the per-axis drive of history under `per_axis_drive`). The
seventeen worlds of `examples/events/gate_set.json` replayed at their caps
(`tools/run_series.py --list examples/events/gate_set.json --fast --jobs
4`; Python 3.14.0rc2, headless), every run completed with the books
balanced at every tick. Of the ten worlds with digests, five replayed byte
for byte: `detector/grouped_12_nodes`, `weak/j2_ladder`,
`weak/j3_deuteron_crowd` (its cap 1 precedes the first push),
`hand/wu` (no moving body) and `drive_b/plane_b` (the state `f2de6815...`,
the events `92ef9f38...`: the line drive under the key and under the law
are the same integers); five moved, as DEFAULT.md section (f) predicted,
each keeping its former digests under `former` in the gate set:
`weak/j3_deuteron` (the state `5ccfca07...` for `b6ebcb93...`, the events
`5f0b9b52...` for `5344feb6...`, the books unchanged: the nucleons' attempted
steps and accumulators), `bohr/r2` (the state `66a8f776...`, the books
`d26bec6a...`, the events `414a3849...`: the electron's orbit at the line
drive's pace), `nucleus/alpha_square` (`d538cd89...`, `21187688...`,
`a537ce54...`: the pushed nucleons), `hubble/pushing_age` (the state
`ec7ec1d8...` alone: the accumulators at the first self-creation, `p_a Q`
for `p_a`; the books and the events unchanged at the cap 1) and
`coupling/1b_m16` (`af07c81b...`, `7dd43ac7...`, `def8455b...`: the pushed
probe). The seven lamp worlds without digests completed as before. Run
times: `heisenberg/w27_beam` 920 s at 10.7 GB peak, `weak/j3_deuteron` 42 s,
`bohr/r2` 22 s, `nucleus/alpha_square` 15 s, the rest under 10 s (host
seconds, the runner's). What the flip predicts (DEFAULT.md (f)): only a world
with a moving body moves, which the replay shows.

## Series X, the directional drive: six runs and the gate set's byte identity against main 166403d8 - 2026-09-22

The branch `drive-b-v1` from main `166403d8` (`drive-b-v1`, the world key
`drive_b`, off by default; [the design](designs/drive_b/DESIGN.md),
[the register entry](EXPERIMENTS.md#x-the-directional-drive-2026-09-22)).
The six worlds of `examples/events/drive_b/` run once through
`tools/run_series.py --jobs 3` on the head (the source fingerprint
`fcaf6f194e62...` of `run.json`; Python 3.14.0rc2, numpy 2.5.3, headless):
`axis_b`, `plane_b`, `cube_b` (200 intervals, 0.10 to 0.11 s; the state
`97d5da64...`, `f2de6815...`, `a7824708...`; the events `65d837f2...`,
`92ef9f38...`, `aa3c5a29...`) and the controls `axis_main`, `plane_main`,
`cube_main` (0.10 s each; the same states, the events `3dcd225e...`,
`f5a5e395...`, `65c097c0...`), every run completed with the books balanced
at every tick; the digests, the source sha and the readings are the run
blocks of `examples/events/drive_b/expectations.json` (`runs`). The
readings (`tools/drive_b_readings.py`): 0 record checks failed, 19 inside,
0 outside, nothing moved: the clicks at 51, 101 and 152 on face:+x from
(40, 20, 20), (40, 40, 20) and (40, 40, 40) under the key, at 36, 50 and 65
from (40, 20, 20) without it (DETECTOR); every step within one Link of the
line, every drive below 3 W (GAMEBOARD). The OFF identity: the gate set's
sixteen worlds keep the digests of `gate_set.json` (`tests/test_drive_b.py`
(a) replays `detector/grouped_12_nodes`; `tests/test_amplitude_click.py`
(d) and `tests/test_massive_rows.py` (a) replay every lamp-free gate
world), and `plane_b` joins the gate set as the first world that declares
the key (the state `f2de6815...`, the events `92ef9f38...`). What the key
predicts (DESIGN.md section 4): a world without it reads as it did to the
byte, which the replay shows; under it the plane body reaches the face at
(40, 40, 20) where the control reaches it at (40, 20, 20), which the
readings show.

## Series S, the covariant readings: four runs and the OFF replay against main f5417ab3 - 2026-09-21

The branch `covariant-readings` from main `f5417ab3` (`covariant-readings-v1`,
the world key `covariant_readings`; [MIGRATION](MIGRATION.md#the-covariant-readings-on-2026-09-21-a-world-key-absent-by-default),
[the register entry](EXPERIMENTS.md#s-the-covariant-readings-2026-09-21)).
The four worlds of `examples/events/covariant/` run once through
`tools/run_series.py` on the head (the source fingerprint
`24e0c1bacec8...` of `run.json`; Python 3.14.0rc2, numpy 2.5.3, headless,
two jobs): `j4_muon_rest`, `j4_muon_3640`, `j4_muon_12856` (420 intervals,
0.3 s each; the state `24516f20...`, `211f7fc7...`, `1db7fbd7...`; the events
`b5edd2d2...`, `0675fdfb...`, `985f4fdc...`) and `coasting_none_covariant` (400
intervals, 42.9 s; the state `e1b1fc8b...`, the events `296bce62...`), every
run completed with the books balanced at every tick; the digests, the
source sha and the readings are the run blocks of
`examples/events/covariant/expectations.json` (`runs`), and the cap of 60
intervals of the coasting world (`runs_at_the_cap`, the state `79f8479c...`, re-pinned under clock-age-v1 on 2026-09-21 (775ce3ba... until the word))
is what `tests/test_covariant_readings.py` (f) replays with the three J4
worlds. The OFF replay: `hubble_stars/coasting_none` without the key run
on the base tree (main `f5417ab3`, the fingerprint `5d254c85...`) and on the
head: the state `1a385429...`, the books `33cf0ac7...` and the events
`f75ca182...` equal on both (`off_replay` of the same file); the gate set's
digests of `gate_set.json` unchanged (`tests/test_amplitude_click.py`
(d)). What the key predicts (17.6): a world without it reads as it did to
the byte, which the replay shows; under it the muon's clock at E'_0 / E'
and the moving star's z at gamma (1 + beta) - 1, which the readings show
(24 inside, 1 outside by the tool's count: the 64th self-creation at 124
against the continuum's 125.2 +- 1, the discrete cadence's offset, and
inside the design's own integer pin 124 (DERIVATIONS_BEAM 17.6 M2: the 64th self-creation "at the integers 70 and 124 by the primitive's own count"; the continuum's 64 gamma = 125.2 is the limit, one gamma - 1 above the cadence from an empty accumulator; the physics-rule review REVIEW_3, must-fix 3: a relabel, nothing moved)). After the merge of main
`8dd743db` into the branch (the host's batches and memos, bit-exact) the
source fingerprint is `7a5072eb...`; the three J4 worlds and the coasting
cap replay to the registered digests on it (`tests/test_covariant_readings.py`
(f), 9 passed), so the run blocks stand as made.

## The crossing rule: the gate set and the movers replayed against no-tables 2bbc5a64 - 2026-09-21

The branch `crossing` (the step before the law, the two marks, the reading
at the crossing, the key `doppler` and the grain deleted;
[MIGRATION](MIGRATION.md#the-crossing-rule-on-2026-09-21-the-step-before-the-law-a-row-and-a-body-met-once-the-key-doppler-and-the-grain-deleted),
[BEAM_LAW note 48](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation))
against the tree it grew from, `no-tables` at `2bbc5a64`: the gate set
(`examples/events/gate_set.json`, sixteen worlds at their caps) and the
movers (the nine `hubble_stars/` worlds and their nine `record/` worlds,
the four `hubble/` worlds, the four of the catalog, the eight of the
nucleus, the three of the binding, `weak/j3_deuteron`, `j3_deuteron_crowd`,
`j3_neutron_free`, `coupling/1b_m1`, `1b_m4`, `1b_m16`, `orbit/s1_r12`,
`s8_r12`, `s32_r12` and `bohr/r2`, `r4`, `r6`, `r8`, at their registered
length), every world run on both trees through the runner (`python -m
event_universe --init ... --ticks`), one process at a time, and compared
per world by a digest driver (the disk held no two full replays of the
movers, so each run's `events.jsonl` was digested and deleted): the
sha256 of `events.jsonl`, of the books (`json.dumps` of `run.json`'s
`audit`, as `tools/run_series.py` and `tests/test_amplitude_click.py` (d)
take it) and of `state.json` with the two marks `step_port` and
`last_step_port` stripped from every measured event (the marks alone are
new in every state), the count of `step` and `contact` lines on both
trees and the head's `fast_steps`. The state of a free measured event
carried the accumulator's `flow` rows on the base and carries none on
the head (the rows deleted with the grain), so `state.json` moves for
every world with a free body even where its events and books are the
same (`weak/j3_neutron_free`); the verdict `identical` needs all three
digests equal. The source fingerprints (`source_sha256` of `run.json`):
the base `d78de1fd8594bf9218d74fd89af1c7ab7ebf1cc7930d76ff33ba192ac565a1b7`
(no-tables 2bbc5a64); the head
`3550193441db5690af4f5ceb050830c7a711445fe213dde4b1be62c97c8695d1`
(crossing 227b0271, no-tables 8e1d1ad6 merged) on the gate set, the
stars, the record worlds and the first twelve of the rest, and
`2395f67171797598e6053f923440092634699149bae44a6ff44e73cfa6b14566`
(crossing 96ec8b6b, main 3be07117 merged: the architect's cleanup of the
host, claimed bit-exact on main, is the only source change between the
two heads) on the rest's twenty others. `heisenberg/w27_beam` at its cap
200 was killed on the base tree (exit -9, the run near 4 GB while other
checks ran on the machine) and is not compared; it completed on the head
(660968 lines, 0 steps). What the rule predicts (note 48): a world whose
measured events are all fixed, or whose free bodies never cross a Link
and never fire under a push, reads the same records; a world with a
completed step or a fire under a push moves (the step before the law,
the drive by the momentum after the previous interval's push, the swap
and the entered Node's rows read, the leapfrog re-reads gone). What the
table shows: every world without a stepping or pushed body is identical
(the marks apart); an adjacent pair that only contacts keeps its books
and moves its events alone, the contact ticks one interval later
(`weak/j3_deuteron`, `nucleus/alpha_line`, `deuteron_1`, `pp_1`;
`catalog/neutron_star` with seven contact lines fewer, 186 -> 179, and
`weak/j3_deuteron_crowd` with one, 69 -> 68, their books the same);
series G2's gravity and double worlds
lose about a tenth of their read lines (the leapfrog re-reads) and their
stars make more Links (1319 -> 1427 in `gravity_none`, 1082 -> 1299 in
`double_none`: the push from behind falls, the deceleration is smaller,
the design's prediction (i)), the coasting worlds keep their steps to
the unit; the orbit worlds `s8_r12` and `s32_r12` make 147 Links for 488
and 305 for 607 (the body's re-reads of its own rows gone, fewer pushes;
an observation, not a diagnosis), `s1_r12` keeps its 60; Bohr's electron
in `r2` makes 52 Links for 59 at the cap 689, five of them right after
another (`fast_steps` 5, the report of note 48), and 109 for 93 over
3000 intervals. Every run balanced at every completed tick on both
trees.

| world | verdict | events.jsonl | the ledger | state.json | step lines | contact lines | fast steps | balanced | ticks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bell/a0_b0.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 160 |
| `weak/j3_deuteron.json` | moved | changed (721329 -> 721329 lines) | same | changed | 0 | 64 | 0 | yes | 700 |
| `bohr/r2.json` | moved | changed (170354 -> 170333 lines) | changed | changed | 59 -> 52 | 0 | 5 | yes | 689 |
| `catalog/lamp_mirror_screen.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 14 |
| `lensing/heavy_meeting.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 111 |
| `detector/grouped_12_nodes.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 2 |
| `bell/fixed.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 13 |
| `weak/j2_ladder.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 1 |
| `weak/j3_deuteron_crowd.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 1 |
| `heisenberg/w27_beam.json` | MISSING OR FAILED |  |  |  |  |  |  |  |
| `nucleus/alpha_square.json` | moved | changed (390833 -> 391080 lines) | changed | changed | 24 -> 22 | 30 -> 31 | 0 | yes | 180 |
| `hubble/pushing_age.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 1 |
| `coupling/1b_m16.json` | moved | changed (38 -> 37 lines) | changed | changed | 4 -> 3 | 0 | 2 | yes | 25 |
| `heisenberg/w1_beam.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 1 |
| `catalog/sun_planet.json` | moved | changed (25 -> 24 lines) | changed | changed | 2 | 0 | 0 | yes | 12 |
| `hand/wu.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 23 |
| `hubble_stars/coasting_none.json` | moved | changed (49588 -> 49580 lines) | changed | changed | 1536 | 0 | 0 | yes | 400 |
| `hubble_stars/coasting_scalar.json` | moved | changed (49255 -> 49232 lines) | changed | changed | 1523 | 0 | 0 | yes | 400 |
| `hubble_stars/coasting_age.json` | moved | changed (49396 -> 49381 lines) | changed | changed | 1525 | 0 | 0 | yes | 400 |
| `hubble_stars/gravity_none.json` | moved | changed (98723 -> 88217 lines) | changed | changed | 1319 -> 1427 | 0 | 0 | yes | 400 |
| `hubble_stars/gravity_scalar.json` | moved | changed (98210 -> 87744 lines) | changed | changed | 1312 -> 1416 | 0 | 0 | yes | 400 |
| `hubble_stars/gravity_age.json` | moved | changed (98498 -> 88018 lines) | changed | changed | 1314 -> 1417 | 0 | 0 | yes | 400 |
| `hubble_stars/double_none.json` | moved | changed (99447 -> 89627 lines) | changed | changed | 1082 -> 1299 | 0 | 0 | yes | 400 |
| `hubble_stars/double_scalar.json` | moved | changed (98050 -> 88518 lines) | changed | changed | 1070 -> 1277 | 0 | 0 | yes | 400 |
| `hubble_stars/double_age.json` | moved | changed (98726 -> 89081 lines) | changed | changed | 1069 -> 1282 | 0 | 0 | yes | 400 |
| `hubble_stars/record/coasting_none.json` | moved | changed (49588 -> 49580 lines) | changed | changed | 1536 | 0 | 0 | yes | 400 |
| `hubble_stars/record/coasting_scalar.json` | moved | changed (49255 -> 49232 lines) | changed | changed | 1523 | 0 | 0 | yes | 400 |
| `hubble_stars/record/coasting_age.json` | moved | changed (49396 -> 49381 lines) | changed | changed | 1525 | 0 | 0 | yes | 400 |
| `hubble_stars/record/gravity_none.json` | moved | changed (98723 -> 88217 lines) | changed | changed | 1319 -> 1427 | 0 | 0 | yes | 400 |
| `hubble_stars/record/gravity_scalar.json` | moved | changed (98210 -> 87744 lines) | changed | changed | 1312 -> 1416 | 0 | 0 | yes | 400 |
| `hubble_stars/record/gravity_age.json` | moved | changed (98498 -> 88018 lines) | changed | changed | 1314 -> 1417 | 0 | 0 | yes | 400 |
| `hubble_stars/record/double_none.json` | moved | changed (99447 -> 89627 lines) | changed | changed | 1082 -> 1299 | 0 | 0 | yes | 400 |
| `hubble_stars/record/double_scalar.json` | moved | changed (98050 -> 88518 lines) | changed | changed | 1070 -> 1277 | 0 | 0 | yes | 400 |
| `hubble_stars/record/double_age.json` | moved | changed (98726 -> 89081 lines) | changed | changed | 1069 -> 1282 | 0 | 0 | yes | 400 |
| `hubble/coasting_age.json` | moved | changed (27013 -> 27352 lines) | changed | changed | 1504 -> 1505 | 0 | 0 | yes | 400 |
| `hubble/coasting_scalar.json` | moved | changed (27013 -> 27352 lines) | changed | changed | 1504 -> 1505 | 0 | 0 | yes | 400 |
| `hubble/pushing_age.json` | moved | changed (36903 -> 34818 lines) | changed | changed | 1426 -> 1449 | 0 | 0 | yes | 400 |
| `hubble/pushing_scalar.json` | moved | changed (36354 -> 34360 lines) | changed | changed | 1411 -> 1431 | 0 | 0 | yes | 400 |
| `catalog/clock_near_mass.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 50 |
| `catalog/lamp_mirror_screen.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 50 |
| `catalog/neutron_star.json` | moved | changed (1638 -> 1631 lines) | same | changed | 0 | 186 -> 179 | 0 | yes | 40 |
| `catalog/sun_planet.json` | moved | changed (570 -> 558 lines) | changed | changed | 11 | 0 | 0 | yes | 50 |
| `nucleus/alpha_line.json` | moved | changed (6997904 -> 6997904 lines) | same | changed | 0 | 777 | 0 | yes | 3000 |
| `nucleus/alpha_square.json` | moved | changed (712965 -> 796402 lines) | changed | changed | 76 -> 63 | 31 | 0 | yes | 3000 |
| `nucleus/deuteron_1.json` | moved | changed (3477876 -> 3477876 lines) | same | changed | 0 | 327 | 0 | yes | 3000 |
| `nucleus/deuteron_1_kick.json` | moved | changed (3477871 -> 3477872 lines) | same | changed | 0 | 322 -> 323 | 0 | yes | 3000 |
| `nucleus/deuteron_3.json` | moved | changed (379797 -> 377443 lines) | changed | changed | 17 | 0 | 0 | yes | 3000 |
| `nucleus/pp_1.json` | moved | changed (3477783 -> 3477783 lines) | same | changed | 0 | 234 | 0 | yes | 3000 |
| `nucleus/pp_1_weak.json` | moved | changed (410028 -> 414066 lines) | changed | changed | 19 | 0 | 0 | yes | 3000 |
| `nucleus/pp_3.json` | moved | changed (319953 -> 323412 lines) | changed | changed | 17 | 0 | 0 | yes | 3000 |
| `binding/alpha_square_bond.json` | moved | changed (753038 -> 741524 lines) | changed | changed | 79 -> 62 | 31 -> 32 | 1 | yes | 3000 |
| `binding/deuteron_bond.json` | moved | changed (3477899 -> 3477899 lines) | changed | changed | 0 | 348 | 0 | yes | 3000 |
| `binding/proton_bond_lamp.json` | identical | same | same | same (the marks apart) | 0 | 0 | 0 | yes | 3000 |
| `weak/j3_deuteron.json` | moved | changed (721329 -> 721329 lines) | same | changed | 0 | 64 | 0 | yes | 700 |
| `weak/j3_deuteron_crowd.json` | moved | changed (721330 -> 721329 lines) | same | changed | 0 | 69 -> 68 | 0 | yes | 700 |
| `weak/j3_neutron_free.json` | moved | same | same | changed | 0 | 0 | 0 | yes | 600 |
| `coupling/1b_m1.json` | moved | changed (4814 -> 4813 lines) | changed | changed | 11 | 168 -> 167 | 10 | yes | 200 |
| `coupling/1b_m4.json` | moved | changed (4846 -> 4845 lines) | changed | changed | 11 | 168 -> 167 | 10 | yes | 200 |
| `coupling/1b_m16.json` | moved | changed (4942 -> 4941 lines) | changed | changed | 11 | 168 -> 167 | 10 | yes | 200 |
| `orbit/s1_r12.json` | moved | changed (46589 -> 46589 lines) | same | same (the marks apart) | 60 | 0 | 40 | yes | 4000 |
| `orbit/s8_r12.json` | moved | changed (47140 -> 46695 lines) | changed | changed | 488 -> 147 | 0 | 74 | yes | 4000 |
| `orbit/s32_r12.json` | moved | changed (47338 -> 46938 lines) | changed | changed | 607 -> 305 | 0 -> 2 | 76 | yes | 4000 |
| `bohr/r2.json` | moved | changed (776928 -> 777077 lines) | changed | changed | 93 -> 109 | 0 | 6 | yes | 3000 |
| `bohr/r4.json` | moved | changed (776327 -> 776362 lines) | changed | changed | 150 -> 141 | 0 | 4 | yes | 3000 |
| `bohr/r6.json` | moved | changed (775284 -> 775742 lines) | changed | changed | 142 -> 185 | 0 | 4 | yes | 3000 |
| `bohr/r8.json` | moved | changed (1089668 -> 1088973 lines) | changed | changed | 228 -> 167 | 0 | 3 | yes | 4200 |

13 identical, 52 moved and 1 not compared of the 66 rows (the eight
worlds in both the gate set and the movers' lists appear twice, at their
cap and at their registered length).

Runtime source SHA-256 as above (three fingerprints), Python 3.14.0rc2,
headless.

## No tables: the batch under the share's accumulator and the Nodes' claims - 2026-09-20

The branch `no-tables` after its third item (no remainder discarded at
run time: `share_of` with the row's accumulator, `place_over_nodes` with
the Nodes' claims; [MIGRATION](MIGRATION.md#no-registers-at-nodes-no-tables-on-2026-09-20-the-last-counts-join-the-table-the-flight-as-the-positions-accumulator-no-remainder-discarded)):
the 95 candidate worlds (series L, K, H, the catalog, G2's 27) run at
their registered length under the guards and compared with the same
worlds on the tree before the item (series H against the action-row
tree, the rest against the head of `fraction-free`): 87 identical in
events and books (every world of L including record 144's cone and the
which-path worlds, every world of K, every world of G2, the catalog's
`lamp_mirror_screen` and `neutron_star`; `clock_near_mass` in its events
and books, its `state.json` carrying the `place` claims of a body that
releases nothing), 8 moved: the seven worlds of series H (the electron a
body on three Nodes, its releases placed by the Nodes' claims) and the
catalog's `sun_planet` (the sun two bodies on sets of three Nodes). What
moved and by how much (the columns as in the fraction-free table below):

| world | what moved | births | waits | steps | clicks | ages |
| --- | --- | --- | --- | --- | --- | --- |
| `bohr/r12.json` | events, books | 0 | 0 | 0 | 1925039 | same |
| `bohr/r15.json` | events, books | 0 | 0 | 0 | 2657829 | same |
| `bohr/r16.json` | events, books | 0 | 0 | 0 | 2683089 | same |
| `bohr/r2.json` | events, books | 0 | 0 | 0 | 776599 | same |
| `bohr/r4.json` | events, books | 0 | 0 | 0 | 775789 | same |
| `bohr/r6.json` | events, books | 0 | 0 | 0 | 774793 | same |
| `bohr/r8.json` | events, books | 0 | 0 | 0 | 1088889 | same |
| `catalog/sun_planet.json` | events, books | 50 | 0 | 10 -> 11 | 209 -> 244 | same |

Series H's orbits under the claims: the register's H entry and the Bohr
README. `sun_planet`: the planet at (22, 25, 0) after 50 intervals with 11
steps ((23, 25, 0), 10), the screen's 152 light clicks (147), the faces'
`mass` 19, 19, 7, 7 (19, 19, 0, 21) and `light` 6, 0, 28, 5 (6, 0, 22, 6),
the escaped `light` 39 units of content 304 (34 of 263).

## No tables: the gate set under the flight rule - 2026-09-20

The branch `no-tables` after its second item (the flight table retired:
`Flight.walk_step`, the position's accumulator per direction off the age;
[MIGRATION](MIGRATION.md#no-registers-at-nodes-no-tables-on-2026-09-20-the-last-counts-join-the-table-the-flight-as-the-positions-accumulator-no-remainder-discarded)):
the seventeen worlds of the gate set (`examples/events/gate_set.json`) run
at their registered length under the guards, `events.jsonl`, `state.json`
and the books digested and compared with the same worlds on the tree
before the item (`bohr/r2` against the action-row tree of the first item,
the sixteen others against the head of `fraction-free`, the digests of
the register replay below): 17 of 17 identical in events, state and
books. The step table per direction over its period was built from the
same rule at load, so nothing could move; the replay is the proof.

## No tables: series H under the action row - 2026-09-20

The branch `no-tables` ([MIGRATION](MIGRATION.md#no-registers-at-nodes-no-tables-on-2026-09-20-the-last-counts-join-the-table-the-flight-as-the-positions-accumulator-no-remainder-discarded);
the model owner's record 155) against its base `ddec5166` (the head of
`fraction-free`): the seven worlds of series H run on both trees at their
registered length under the guards (`--wall-seconds 1200 --memory-mb
4096`), `events.jsonl` and `state.json` digested, the books (`audit`)
digested. The turn by momentum as the `action` row moves the electron's
phase and nothing of its steps: the events of every world moved (the
rays' phases), the books of every world are identical, every orbit's
closings, periods, returns, radii and escapes are the signed drive's
(`tools/bohr_readings.py` on both, the numbers in the register's H entry).
The digests (the first 16 hexadecimal digits of the sha256):

| world | events.jsonl (was) | events.jsonl (now) | state.json (now) | books |
| --- | --- | --- | --- | --- |
| `r2` | `ea52bf20dda2d125` | `af97b4fd9a61444d` | `0fb4d0945f04b5ba` | identical |
| `r4` | `4532306a56eb3276` | `d37ae7d22246744b` | `bc2d82f5250901d4` | identical |
| `r6` | `9cd943bafcc6def4` | `541ad66e08b551ab` | `1e117afc41fd7990` | identical |
| `r8` | `30f5083c1186d478` | `830a6f3caa7062a9` | `3fa56b6963e2b810` | identical |
| `r12` | `da8cc1cd922ef2e1` | `a08542a5cd0bf548` | `ab7be58212465791` | identical |
| `r15` | `b82a90b67b4d0fb4` | `4f4b6d9cd339e07b` | `f499a30e4fb8c5e6` | identical |
| `r16` | `929dbfe2afda38ec` | `9dfa570683034b9b` | `af507d6861a76026` | identical |

## The click branch: the gate set of sixteen worlds replayed against main fd59f01e - 2026-09-21

The branch `click` at its fourth commit, the birth wheel, on b1e2ab4c (the
exact phase), the tree of the commit that carries this section (the click's
weight as the inner product,
the click without amplitudes, the exact phase at the click and the birth
wheel: [BEAM_LAW notes 37 (xi) and (xii), 45 and 46](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[MIGRATION](MIGRATION.md)) against main `fd59f01e`'s tree: the sixteen worlds
of `examples/events/gate_set.json` replayed on both trees at their caps
(`tools/run_series.py --list --fast --jobs 2 --wall-seconds 1800 --memory-mb
6144`), `events.jsonl`, `state.json` and the books (`audit` of `run.json`)
digested (the first 12 hexadecimal digits of the sha256; `w27_beam` beyond
the wall of 1800 s on both trees at its cap of 200 intervals, not compared,
as in the fraction-free entry). No gate world
declares the pair form of `phase_per_link`, so no click line gains `exact`;
every lamp world's `state.json` gains the birth wheel's accumulator under
`acc` as `wheel` and nothing else moves. The last column is the comparison
with the new report keys dropped (`wheel` under `acc`; `exact` and
`remainder` on click lines): the physics of every world identical.

| world | what moved | events.jsonl | state.json | books | with the new keys dropped |
| --- | --- | --- | --- | --- | --- |
| `1b_m16` | byte-identical | `20aa2b23913e` | `87c7a42691be` | `8830f84aef5d` | identical |
| `a0_b0` | `state.json` alone | `f62fe63bd87d` | `f8daa51b0ddd` (was `c16b8829f65f`) | `e52b8d0aa384` | identical |
| `alpha_square` | byte-identical | `ea432ba27eac` | `be034bcdfc61` | `15fceb127a2f` | identical |
| `fixed` | `state.json` alone | `13b9afa28162` | `54596bee45a3` (was `0f6c7ff36b30`) | `7364e3cf3872` | identical |
| `grouped_12_nodes` | byte-identical | `4b4994530f29` | `ab7bc500cbdb` | `975863cdb72c` | identical |
| `heavy_meeting` | `state.json` alone | `5b33f4d85380` | `3577f590a4ed` (was `1e44459125e7`) | `86e3ef8e18a0` | identical |
| `j2_ladder` | byte-identical | `e3b0c44298fc` | `5684eec9f321` | `9f16ab276ee0` | identical |
| `j3_deuteron` | byte-identical | `4638b98e16b8` | `ea32b17fefcd` | `9f286fe9bb10` | identical |
| `j3_deuteron_crowd` | byte-identical | `e3b0c44298fc` | `701ebdb24897` | `9a55af2c0750` | identical |
| `lamp_mirror_screen` | `state.json` alone | `588ce119eeb1` | `8b28facb12d6` (was `99c2238d962b`) | `8ac486c8c9ad` | identical |
| `pushing_age` | byte-identical | `e3b0c44298fc` | `60ddede6051f` | `7e219a1d03c8` | identical |
| `r2` | byte-identical | `35f5c6c3503e` | `a48ba880411b` | `d830bd8e0e27` | identical |
| `sun_planet` | `state.json` alone | `364c375f4232` | `b9c58c783d2f` (was `d14d83a91dc1`) | `2dfec0c224d0` | identical |
| `w1_beam` | `state.json` alone | `56f9cb190070` | `9008662fb1b6` (was `8b7abe69fbfe`) | `465f5b4e0bd2` | identical |
| `w27_beam` | not compared: not completed: wall 1800 s on main, not completed: wall 1800 s on the branch | | | | |
| `wu` | byte-identical | `d4d927fb55cd` | `8a84a189f93c` | `4d746dbe6084` | identical |

## The fraction-free law: the register replayed once on the branch against the base a2120413 - 2026-09-20

The branch `fraction-free` ([BEAM_LAW note 41](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[MIGRATION](MIGRATION.md#the-fraction-free-law-on-2026-09-20-every-count-an-accumulator-on-the-bodys-record))
at its head after stage 2 with main `e62291a8` merged, against the base
`a2120413`'s tree: every world of the register run on both trees at its
registered length under the guards (`--wall-seconds 1200 --memory-mb
4096`; the scratchpad driver runs one world per worker at a time, keeps
each run's digests and counts and deletes the run; the series whose
readers were re-read kept their runs through `tools/run_series.py` with
the same guards), `events.jsonl` and `state.json` digested, the books
(`audit` of `run.json`) digested. Every `state.json` moves for the new
field `acc`; a world "moved" below moved in its events or its books.
Not compared: `heisenberg/w27_beam` (skipped as ordered); `heisenberg/w27_wave`, `buildup/w27_rate1`, `buildup/w27_rate47` and `buildup/w27_rate8` (beyond the wall of 1200 s on the base tree under the guards, not run on the head); `heisenberg/w9_beam` and `heisenberg/w9_wave` (beyond the address-space guard of 4096 MB on both trees, about 750 s in); every other world of the register completed on both trees with the books balanced at every tick. 82 worlds identical in events and books; 103 moved.

**The gate set on the head** (the seventeen worlds of
`examples/events/gate_set.json`; the first 16 hexadecimal digits of the
sha256): the lamp worlds and the crowd worlds moved in their events, the
others in `state.json` alone.

| world | events.jsonl | state.json | moved |
| --- | --- | --- | --- |
| `two_slits` | `66dc28e5d78c2b52` | `9ee8ab4bc36d5916` | `state.json` alone |
| `read` | `78ecef7035ed4f3f` | `d235b7058770dedd` | events and books |
| `a0_b8` | `f62fe63bd87d2eb6` | `20fd7737901c78e0` | events and books |
| `j2_filter` | `1c92c9c3817755e7` | `83d753e01dde2f07` | `state.json` alone |
| `w_exchange` | `80ebe74909824bad` | `3ef35eb1990eba21` | `state.json` alone |
| `j3_neutron_free` | `ca857e2846aa5b86` | `63bb34fa06e762da` | `state.json` alone |
| `deuteron_1` | `6234c00fd3e478ac` | `4d9800a8f3fadc04` | `state.json` alone |
| `mass_meeting` | `3b2084d4f019e9e2` | `66167ad24afcb871` | `state.json` alone |
| `r2` | `ea52bf20dda2d125` | `b7174c3573d53eaa` | `state.json` alone |
| `coasting_age` | `b61079d07448b763` | `34e8635179f3d166` | `state.json` alone |
| `7_pp` | `da177386799d3861` | `b0578cb7ecac70f3` | `state.json` alone |
| `lamp_mirror_screen` | `0369ed2673eed0f1` | `dc6d12ef9f8ad2d4` | events and books |
| `sun_planet` | `8b76ebc4e170ec5f` | `e509ed3b4092515a` | events and books |
| `w3_beam` | `3154f2153b355fb7` | `9a5ce7f26e476104` | `state.json` alone |
| `one_content` | `a8b1f8191dd478a4` | `39b9a32b10d31c5f` | `state.json` alone |
| `age` | `39a304861b12c02b` | `c812d006e0083eb7` | `state.json` alone |
| `periodic_z_node` | `ec81debeb25e6df5` | `2e9421257caaed60` | `state.json` alone |

**What moved and by how much** (births the `birth` lines, waits the sum of
`waited` over the measured events, steps the sum of `steps`, clicks the
`click` lines, ages the measured events whose age at the end moved; the
dated lines of the register entries carry the readers' numbers):

| world | what moved | births | waits | steps | clicks | ages |
| --- | --- | --- | --- | --- | --- | --- |
| `amplitude/bell_0_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_0_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_16_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_16_24_far.json` | events, books | 300 -> 299 | 0 | 0 | 768 -> 764 | same |
| `amplitude/bell_16_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/bell_choosers.json` | events, books | 1000 -> 999 | 0 | 0 | 5894 -> 5890 | same |
| `amplitude/bell_n1024_0_128.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_0_384.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_256_128.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n1024_256_384.json` | events, books | 1044 -> 1043 | 0 | 0 | 4142 -> 4138 | same |
| `amplitude/bell_n4096_0_1536.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_0_512.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_1024_1536.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/bell_n4096_1024_512.json` | events, books | 4113 | 0 | 0 | 16418 | same |
| `amplitude/cnot_ghz_xxx.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_xyy.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_yxy.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_ghz_yyx.json` | events, books | 270 -> 267 | 0 | 0 | 484 -> 478 | same |
| `amplitude/cnot_pair_0_24.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_0_8.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_16_24.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_pair_16_8.json` | events, books | 180 -> 178 | 0 | 0 | 300 -> 296 | same |
| `amplitude/cnot_twice.json` | events, books | 180 -> 178 | 0 | 0 | 284 -> 280 | same |
| `amplitude/cone_intervals.json` | events, books | 192 -> 190 | 0 | 0 | 134 -> 132 | same |
| `amplitude/cone_links.json` | events, books | 192 -> 190 | 0 | 0 | 134 -> 132 | same |
| `amplitude/ev_169.json` | events, books | 80 -> 79 | 0 | 0 | 213 -> 210 | same |
| `amplitude/ev_29.json` | events, books | 80 -> 79 | 0 | 0 | 213 -> 210 | same |
| `amplitude/ghz_xxx.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_xyy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yxy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yyx.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/ghz_yyy.json` | events, books | 80 -> 79 | 0 | 0 | 450 -> 444 | same |
| `amplitude/mz_345.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_balanced.json` | events, books | 80 -> 79 | 0 | 0 | 69 -> 68 | same |
| `amplitude/mz_equal.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_half.json` | events, books | 80 -> 79 | 0 | 0 | 138 -> 136 | same |
| `amplitude/mz_quarter.json` | events, books | 80 -> 79 | 0 | 0 | 276 -> 272 | same |
| `amplitude/mz_unequal_f0.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/mz_unequal_f16.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/mz_unequal_f8.json` | events, books | 80 -> 79 | 0 | 0 | 280 -> 276 | same |
| `amplitude/path_0_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_0_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_16_24.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/path_16_24_far.json` | events, books | 300 -> 299 | 0 | 0 | 768 -> 764 | same |
| `amplitude/path_16_8.json` | events, books | 80 -> 79 | 0 | 0 | 286 -> 282 | same |
| `amplitude/rotations_3.json` | events, books | 110 -> 109 | 0 | 0 | 196 -> 194 | same |
| `amplitude/slits_low.json` | events, books | 230 -> 229 | 0 | 0 | 22302 -> 22117 | same |
| `bell/a0_b0.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b12.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b16.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a0_b24.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a0_b32.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a0_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a16_b24.json` | events, books | 160 -> 159 | 0 | 0 | 292 -> 290 | same |
| `bell/a16_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a4_b12.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/a4_b8.json` | events, books | 160 -> 159 | 0 | 0 | 294 -> 292 | same |
| `bell/fixed.json` | events, books | 148 -> 147 | 0 | 0 | 503 -> 501 | same |
| `bell/one_clock.json` | events, books | 1940 -> 1939 | 0 | 0 | 7671 -> 7669 | same |
| `bell/read.json` | events, books | 1940 -> 1939 | 0 | 0 | 7669 -> 7667 | same |
| `bell/written_a0_b29.json` | events, books | 141 -> 140 | 0 | 0 | 474 -> 472 | same |
| `bell/written_a0_b8.json` | events, books | 141 -> 140 | 0 | 0 | 475 -> 473 | same |
| `bell/written_a25_b29.json` | events, books | 141 -> 140 | 0 | 0 | 469 -> 467 | same |
| `bell/written_a25_b8.json` | events, books | 141 -> 140 | 0 | 0 | 470 -> 468 | same |
| `binding/proton_bond_lamp.json` | events, books | 3000 | 0 | 0 | 1735769 | same |
| `catalog/lamp_mirror_screen.json` | events, books | 104 | 0 | 0 | 636 -> 668 | same |
| `catalog/neutron_star.json` | events, books | 0 | 109 -> 97 | 176 -> 186 | 684 -> 708 | 14 of 14 bodies, by -1 to 1 |
| `catalog/sun_planet.json` | events, books | 50 | 0 | 10 | 209 | same |
| `hubble/pushing_age.json` | events, books | 0 | 145 -> 146 | 1429 -> 1426 | 8351 -> 8358 | 25 of 31 bodies, by -3 to 3 |
| `hubble/pushing_scalar.json` | events, books | 0 | 639 -> 617 | 1408 -> 1411 | 8200 -> 8204 | 24 of 31 bodies, by -4 to 8 |
| `hubble_stars/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/doppler/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/doppler/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/doppler/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/doppler/double_age.json` | events, books | 9485 -> 9464 | 115 -> 112 | 1281 -> 1277 | 15248 | 17 of 25 bodies, by -3 to 5 |
| `hubble_stars/doppler/double_none.json` | events, books | 9600 -> 9576 | 0 | 1296 | 15388 -> 15364 | same |
| `hubble_stars/doppler/double_scalar.json` | events, books | 9435 -> 9410 | 200 -> 195 | 1281 | 15141 -> 15138 | 19 of 25 bodies, by -4 to 7 |
| `hubble_stars/doppler/gravity_age.json` | events, books | 9558 -> 9523 | 42 -> 53 | 1420 -> 1418 | 15377 -> 15347 | 19 of 25 bodies, by -2 to 3 |
| `hubble_stars/doppler/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1426 | 15419 -> 15395 | same |
| `hubble_stars/doppler/gravity_scalar.json` | events, books | 9526 -> 9504 | 94 -> 90 | 1415 | 15316 -> 15303 | 20 of 25 bodies, by -3 to 2 |
| `hubble_stars/double_age.json` | events, books | 9474 -> 9469 | 126 -> 107 | 1070 -> 1069 | 15276 -> 15256 | 18 of 25 bodies, by -3 to 6 |
| `hubble_stars/double_none.json` | events, books | 9600 -> 9576 | 0 | 1082 | 15387 -> 15362 | same |
| `hubble_stars/double_scalar.json` | events, books | 9449 -> 9408 | 179 -> 197 | 1072 -> 1070 | 15156 -> 15144 | 18 of 25 bodies, by -3 to 3 |
| `hubble_stars/gravity_age.json` | events, books | 9534 -> 9525 | 66 -> 51 | 1310 -> 1314 | 15345 -> 15339 | 15 of 25 bodies, by -2 to 5 |
| `hubble_stars/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1319 | 15403 -> 15379 | same |
| `hubble_stars/gravity_scalar.json` | events, books | 9512 -> 9504 | 107 -> 90 | 1311 -> 1312 | 15295 -> 15284 | 22 of 25 bodies, by -1 to 4 |
| `hubble_stars/record/coasting_age.json` | events, books | 9538 -> 9521 | 62 -> 55 | 1521 -> 1525 | 15389 -> 15405 | 18 of 25 bodies, by -2 to 4 |
| `hubble_stars/record/coasting_none.json` | events, books | 9600 -> 9576 | 0 | 1536 | 15483 -> 15459 | same |
| `hubble_stars/record/coasting_scalar.json` | events, books | 9517 -> 9504 | 97 -> 90 | 1524 -> 1523 | 15355 | 22 of 25 bodies, by -4 to 6 |
| `hubble_stars/record/double_age.json` | events, books | 9474 -> 9469 | 126 -> 107 | 1070 -> 1069 | 15276 -> 15256 | 18 of 25 bodies, by -3 to 6 |
| `hubble_stars/record/double_none.json` | events, books | 9600 -> 9576 | 0 | 1082 | 15387 -> 15362 | same |
| `hubble_stars/record/double_scalar.json` | events, books | 9449 -> 9408 | 179 -> 197 | 1072 -> 1070 | 15156 -> 15144 | 18 of 25 bodies, by -3 to 3 |
| `hubble_stars/record/gravity_age.json` | events, books | 9534 -> 9525 | 66 -> 51 | 1310 -> 1314 | 15345 -> 15339 | 15 of 25 bodies, by -2 to 5 |
| `hubble_stars/record/gravity_none.json` | events, books | 9600 -> 9576 | 0 | 1319 | 15403 -> 15379 | same |
| `hubble_stars/record/gravity_scalar.json` | events, books | 9512 -> 9504 | 107 -> 90 | 1311 -> 1312 | 15295 -> 15284 | 22 of 25 bodies, by -1 to 4 |
| `masses/cavity_equal.json` | events, books | 1200 | 0 | 0 | 1176 | same |
| `masses/cavity_unequal.json` | events, books | 12000 | 0 | 0 | 11976 | same |
| `weak/j1_lattice.json` | events, books | 0 | 1592 -> 1536 | 0 | 231224 -> 231008 | 56 of 4234 bodies, by 1 to 1 |
| `weak/j1_source.json` | events, books | 0 | 2848 -> 2708 | 0 | 405620 -> 406292 | 220 of 4235 bodies, by -2 to 4 |
| `weak/j3_deuteron.json` | events, books | 0 | 1110 -> 1149 | 62 -> 64 | 707078 -> 718743 | 115 of 764 bodies, by -2 to 11 |
| `weak/j3_deuteron_crowd.json` | events, books | 0 | 1111 -> 1149 | 66 -> 69 | 705380 -> 718741 | 115 of 764 bodies, by -2 to 12 |

**Identical in events and books** (the lamp-free, crowd-free worlds: the
push's accumulators stay 0 at Lambda 1, the drive is as built): `amplitude/slits_one.json`, `binding/alpha_square_bond.json`, `binding/deuteron_bond.json`, `bohr/r12.json`, `bohr/r15.json`, `bohr/r16.json`, `bohr/r2.json`, `bohr/r4.json`, `bohr/r6.json`, `bohr/r8.json`, `catalog/clock_near_mass.json`, `coupling/1a_m1.json`, `coupling/1a_m16.json`, `coupling/1a_m4.json`, `coupling/1b_m1.json`, `coupling/1b_m16.json`, `coupling/1b_m4.json`, `coupling/2.json`, `coupling/3.json`, `coupling/3a.json`, `coupling/3b.json`, `coupling/4.json`, `coupling/5.json`, `coupling/5_long.json`, `coupling/5p.json`, `coupling/6.json`, `coupling/7_00.json`, `coupling/7_mm.json`, `coupling/7_mp.json`, `coupling/7_pm.json`, `coupling/7_pp.json`, `coupling/7_pp_m4.json`, `detector/grouped_12_nodes.json`, `detector/periodic_z_node.json`, `detector/shared_100_nodes.json`, `detector/shared_3_nodes.json`, `hand/nu_hand.json`, `hand/w_hand.json`, `hand/w_two_sides.json`, `hand/wu.json`, `heisenberg/w1_beam.json`, `heisenberg/w1_wave.json`, `heisenberg/w3_beam.json`, `heisenberg/w3_wave.json`, `hubble/coasting_age.json`, `hubble/coasting_scalar.json`, `lensing/control.json`, `lensing/control_meeting.json`, `lensing/heavy.json`, `lensing/heavy_meeting.json`, `lensing/lens_meeting.json`, `lensing/mass.json`, `lensing/mass_meeting.json`, `lensing/near.json`, `lensing/near_meeting.json`, `nucleus/alpha_line.json`, `nucleus/alpha_square.json`, `nucleus/deuteron_1.json`, `nucleus/deuteron_1_kick.json`, `nucleus/deuteron_3.json`, `nucleus/pp_1.json`, `nucleus/pp_1_weak.json`, `nucleus/pp_3.json`, `one_content.json`, `one_slit.json`, `orbit/s1_r12.json`, `orbit/s1_r24.json`, `orbit/s32_r12.json`, `orbit/s32_r24.json`, `orbit/s8_r12.json`, `orbit/s8_r24.json`, `redshift/age.json`, `redshift/scalar.json`, `two_contents.json`, `two_slits.json`, `weak/j2_default.json`, `weak/j2_filter.json`, `weak/j2_ladder.json`, `weak/j2_stride2.json`, `weak/j2_stride2_odd.json`, `weak/j3_neutron_free.json`, `weak/w_exchange.json`.

## The one click: the gate set of sixteen worlds replayed against main 45c0eb48 - 2026-09-20

The branch `amplitude-impl` (the one click of `amplitude-v1`, stage (vii)
step 4: the record form the law, the world key `amplitude` deleted, the
layer releasing a gathered record's offers; MIGRATION (vii-4)) with main
`45c0eb48` (binding-v1, hand-v1, doppler-v1, the signed drive, the family
definitions, series G2 and N) merged, against main's own tree at the same
commit: `examples/events/gate_set.json` (sixteen worlds at their listed
ticks; `hand/wu` added by main; the binding worlds are not in it),
`tools/run_series.py --list --jobs 2 --wall-seconds 1200 --memory-mb 4096`
on both trees, Python 3.14.0rc2, numpy 2.5.3, headless, four cores.

| World | Lamp | Verdict | Branch `state` / ledger / `events` | Run |
| --- | --- | --- | --- | --- |
| `1b_m16` | no | identical | `391d4cbdc763` / `baee1e32e96a` / `dc1054aa43c4` | completed, 200 ticks, 1 s, 203 MB |
| `a0_b0` | yes | changed (state, audit, events) | `9b451889cd06` / `91a5a13fd355` / `3d1d052d21b8` | completed, 160 ticks, 1 s, 44 MB |
| `alpha_square` | no | identical | `26799da3d3b2` / `9102a8f9fd11` / `600166fb5bdd` | completed, 3000 ticks, 15 s, 188 MB |
| `fixed` | yes | changed (state, audit, events) | `3ea73ba982e3` / `1b0055d6e563` / `212d4902f832` | completed, 148 ticks, 1 s, 182 MB |
| `grouped_12_nodes` | no | identical | `f0b869e4d566` / `cc8eb7346911` / `a4b2d2b35cfc` | completed, 4 ticks, 0 s, 182 MB |
| `heavy_meeting` | yes | changed (state, audit, events) | `3a96b17ac66e` / `e47e934e892c` / `362156ce8cde` | completed, 400 ticks, 26 s, 182 MB |
| `j2_ladder` | no | identical | `380fbbf27895` / `48335f1672dc` / `911390d0f64b` | completed, 1037 ticks, 3 s, 182 MB |
| `j3_deuteron` | no | identical | `d4485137fd01` / `431cc87afa9f` / `23196889fbed` | completed, 700 ticks, 24 s, 77 MB |
| `j3_deuteron_crowd` | no | identical | `9bdcf69e2620` / `677af7000b26` / `094a32eb6c0f` | completed, 700 ticks, 37 s, 182 MB |
| `lamp_mirror_screen` | yes | changed (state, audit, events) | `7617e6dc7d0b` / `2c4c5c44bbc2` / `4423c47250ed` | completed, 50 ticks, 0 s, 182 MB |
| `pushing_age` | no | identical | `5e40e4bea36a` / `ae00571de265` / `4d89f6b6182b` | completed, 400 ticks, 48 s, 292 MB |
| `r2` | no | identical | `e8e3e137bd61` / `fe50819ae70d` / `ea52bf20dda2` | completed, 3000 ticks, 20 s, 105 MB |
| `sun_planet` | yes | changed (state, audit, events) | `1757e809a645` / `04edc2d85c46` / `846544571a4b` | completed, 50 ticks, 1 s, 629 MB |
| `w1_beam` | yes | changed (state, audit, events) | `16ea674e1446` / `c645e89fb22d` / `5a74c8894578` | completed, 350 ticks, 116 s, 898 MB |
| `w27_beam` | yes | not completed on the branch | - | not completed: wall 1200 s, None ticks, 1200 s, 3502 MB |
| `wu` | no | identical | `023c13135cc7` / `d9cd4631d45f` / `d4d927fb55cd` | completed, 40 ticks, 0 s, 629 MB |

The verdict: every world without a lamp is byte-identical to main in
`state.json`, the ledger and `events.jsonl` (nine of nine, `hand/wu` among
them), every world with a lamp changed (six of seven completed), and
`w27_beam` (a lamp at the rate [47, 1] over 27 opening Nodes) did not
complete on the branch within the wall guard (1200 s, 3.5 GB; main
completed its 350 intervals in 83 s, `73d4980059d3` / `b5c15a82715e` /
`439252c03ee8`): the host cost of the record form on a crowd world, the
GameBoard's rows of distinct records not merging (the register's A10 line;
MIGRATION (vii-4)). The changed set is exactly the lamp worlds: the record
form itself (every lamp births records born at u with the path phase, one
click per record by the ladder, the push by share), no defect and no
refusal; each re-registers by its dated line in the register (the owner's
decision, record 137). The fast pass at the caps (`--fast`) pins the nine
lamp-free worlds to main's digests in `tests/test_amplitude_click.py` (d).

## Series N, the binding that costs content: three runs and the gate set replayed - 2026-09-20

The worktree `binding-v1` on `b8620d8f` (current main) with the give at the
contact (`binding-v1`, [BEAM_LAW note 40](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
the sources' fingerprint
`22935341b7400e13b850aefe86b65528ff595cc0647f78a5a7b3fe543ac09941`
(the runner's `source_sha256`
`4a1db891b7d392b3f4be77effc77e4102c37c9637459a903e9456c6082f05cc6`),
Python 3.14.0rc2, numpy 2.5.3, headless, four cores.

| Check | Result |
| --- | --- |
| Series N, `examples/events/binding/` (three worlds, `tools/run_series.py --jobs 2 --wall-seconds 1200`, 3000 intervals each) | every run completed in 13 to 53 s with the books balanced at every tick; the digests (state, audit, events): `deuteron_bond` `b66833650869` / `ae9319ed637a` / `c05fb3c3a433`, `proton_bond_lamp` `67b598ee4d37` / `65de22cd56dd` / `45fd5c0c63a2` (under the one click of `amplitude-v1`, the key deleted and the world regenerated without it: `cf524330f3e6` / `5f20f826d21f` / `660ac30e7957`, the same 2993 gathers of 2961 x 8 and 32 x 7, 7 open, no contact, `held.bond` 2; B1 and B3 not re-run: no lamp, no key), `alpha_square_bond` `35e1ce3c9cf2` / `247cd70da903` / `51c4fba7ca0d`; every reading inside its pin (B3's dispersal inside in kind, at other ticks than series I's), the table in [the worlds' README](../examples/events/binding/README.md#what-was-measured-2026-09-20) and the entry in [EXPERIMENTS, N](EXPERIMENTS.md#n-the-binding-that-costs-content-2026-09-20) |
| The gate set, `examples/events/gate_set.json` (15 worlds at their listed ticks), main `b8620d8f` against the branch, `tools/run_series.py --list ... --compare` | every world identical in `state.json`, the ledger and `events.jsonl`: a0_b0 `dc4cba74e3a5` / `90cab346067c` / `dfa00b9ef9b6`, j3_deuteron `d4485137fd01` / `431cc87afa9f` / `23196889fbed`, r2 `e8e3e137bd61` / `fe50819ae70d` / `ea52bf20dda2`, lamp_mirror_screen `9de7f52ec260` / `9041dac91aae` / `e6ca788d38ca`, heavy_meeting `395040805a4d` / `18c5eb4625ac` / `188ced16170a`, grouped_12_nodes `f0b869e4d566` / `cc8eb7346911` / `a4b2d2b35cfc`, fixed `d078ace3e8d8` / `6466e974280d` / `77ca1b3b3bc9`, j2_ladder `380fbbf27895` / `48335f1672dc` / `911390d0f64b`, j3_deuteron_crowd `9bdcf69e2620` / `677af7000b26` / `094a32eb6c0f`, w27_beam `73d4980059d3` / `b5c15a82715e` / `439252c03ee8`, alpha_square `26799da3d3b2` / `9102a8f9fd11` / `600166fb5bdd`, pushing_age `5e40e4bea36a` / `ae00571de265` / `4d89f6b6182b`, 1b_m16 `391d4cbdc763` / `baee1e32e96a` / `dc1054aa43c4`, w1_beam `d843680c8246` / `61bc435a99ff` / `1e08efda9aab`, sun_planet `f7043252f62a` / `583a5e8e5163` / `4b793a913b22` (r2, 1b_m16 and alpha_square write `contact` records: without a body that holds a paid family the record carries no `given` and the contact is the hand-over alone) |
| `tests/test_binding.py` (a) to (d) | the give at the first hand-over, the remainder, the take on the line, a body that carries nothing: the integers of [TEST_EXPECTATIONS](TEST_EXPECTATIONS.md#the-binding-that-costs-content) |
| `python tools/check.py` | ruff lint and format, mypy and the selected tests green; `--full` before the push |

The first build gave on the heading opposite to the momentum's sign; the
reading of B1 showed the neutron's row given toward the proton (its
momentum +270 720 after the proton's hand-over, its step -x) and taken
back at tick 31; the rule is the step's sign, as the design states, and
the runs above are of the corrected engine. The runs establish what the
rule does on the engine (the give once, the border's clicks with the
content, the pair stable, the books exact, the alpha at 2.0 x); they
establish no physical law, for or against.

## The hand: the gate set of fifteen worlds replayed without a declaration - 2026-09-20

`hand-v1` ([BEAM_LAW note 39](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[MIGRATION](MIGRATION.md), "The hand") adds the row's column `hand`, the
measured event's `axis`, the keys `hand` on a family, a lamp, a transit row
and a table entry, the right-hand rule in `become` and the parity filter;
every world without a declaration must read as it did, byte for byte (the
column is 0 everywhere, its width in the packed merge key 0, no line of the
record gains a key). The gate set (`examples/events/gate_set.json` as on
`origin/main` at `56a258f8`, fifteen worlds, `doppler-v1` merged) replayed
with `tools/run_series.py --list ... --compare` against the base tree's
summary (the base `56a258f8`, the head this change rebased onto it): 15 of
15 identical in `events.jsonl`, `state.json` and the ledger (`audit`), exit
0 (the same verdict, 15 of 15, was read first against the base `d768f831`
before `doppler-v1` landed). The digests (the first 16 hexadecimal digits of
the sha256):

| world | events.jsonl | state.json |
| --- | --- | --- |
| `a0_b0` | `dfa00b9ef9b652ac` | `dc4cba74e3a5966f` |
| `j3_deuteron` | `23196889fbed5e62` | `d4485137fd018bba` |
| `r2` | `ea52bf20dda2d125` | `e8e3e137bd611658` |
| `lamp_mirror_screen` | `e6ca788d38ca28b9` | `9de7f52ec26093ac` |
| `heavy_meeting` | `188ced16170ac007` | `395040805a4d05ee` |
| `grouped_12_nodes` | `a4b2d2b35cfc84ea` | `f0b869e4d5663db6` |
| `fixed` | `77ca1b3b3bc9558d` | `d078ace3e8d8f865` |
| `j2_ladder` | `911390d0f64b2f3e` | `380fbbf27895583b` |
| `j3_deuteron_crowd` | `094a32eb6c0f9a3f` | `9bdcf69e26201653` |
| `w27_beam` | `439252c03ee8eef1` | `73d4980059d3e116` |
| `alpha_square` | `600166fb5bdd434b` | `26799da3d3b2f850` |
| `pushing_age` | `4d89f6b6182b92a2` | `5e40e4bea36aa902` |
| `1b_m16` | `dc1054aa43c44a9c` | `391d4cbdc763ec76` |
| `w1_beam` | `1e08efda9aabbd33` | `d843680c8246c097` |
| `sun_planet` | `4b793a913b22fe50` | `f7043252f62a9b78` |
| `wu` (the sixteenth, this change's) | `d4d927fb55cdfa9a` | `023c13135cc76634` |

`hand/wu.json` is added to the gate set as the first world declaring the
keys (`ticks` 40, `cap` 23: the antineutrino's face click); its row above
is from its one run on this source, the base row of the next replay. The worlds of
series P were run once and read against their pins
([the hand series](../examples/events/hand/README.md); [EXPERIMENTS](EXPERIMENTS.md),
"P, the hand").

## Series G2, the Hubble diagram with stars behind the detector: three runs - 2026-09-20

The branch `claude/series-g2-stars`, headless, three jobs, Python 3.14.0rc2,
numpy 2.5.3; the worlds of `examples/events/hubble_stars/` through
`tools/run_series.py --jobs 3` and the readings through
`tools/hubble_stars_readings.py`, every run of 400 intervals completed with
the books balanced at every interval; the readings registered in
[G2](EXPERIMENTS.md#g2-the-hubble-diagram-with-stars-behind-the-detector-2026-09-20)
and the worlds' [README](../examples/events/hubble_stars/README.md).

| Run | Engine and fingerprint | Worlds | Result |
| --- | --- | --- | --- |
| The first registration | the branch's law before the key `amplitude`, source fingerprint `b4d074f2b762e58d15037a46b614e89609a48bcee2211eaf471af16e3d4923d1` | the nine worlds `<crowd>_<clock>`, 36 to 39 s each | the reading's formula 648 of 648 inside 2 %, the luminosity 631 of 648 inside 5 %, 34 pinned readings inside and 29 outside, none moved; re-run under the record click on `claude/amplitude-impl` at `62369cb8`: the same clicks and readings to the last digit |
| The second run | main `f3a41f28` merged (the step drive, PR #373; the record click), source fingerprint `8ede1e0ff40e69ed05a71d7fd09cca21bad5e37f0c715018f3e77a504f518afb` | `record/coasting_none`, `gravity_none`, `gravity_scalar`, `gravity_age`, `double_none`, 37 to 41 s each | the expectations pinned first by the emitter-only rule; the reading's formula 360 of 360, the luminosity 360 of 360, the longest burst 1 Link, 759 readings inside and 1 outside (the scalar clock's k) |
| The third run | main `56a258f` merged (doppler-v1, PR #379; the signed drive, PR #377), source fingerprint `39672332ebd7d87ee17f29c927df6ed0fc9b66e2c926c202e021646454b38b9e`, the identities `amplitude-v1` and `doppler-v1` | `doppler/coasting_none`, `gravity_none`, `gravity_scalar`, `gravity_age`, `double_none`, 37 to 41 s each | the expectations pinned first by the flux rule at the grain (`docs/designs/hubble_stars/EXPECTATION_2.md`); the reading's formula 120 of 120, the luminosity 120 of 120, the longest burst 1 Link, 35 readings inside and 5 outside (the scalar clock's q and its forms; the double crowd's q); the coasting world's gather and click lines identical to the second run's |

## The amplitude law: the gate set of seventeen worlds replayed without the key after commit (i) and at stage (v) - 2026-09-20

`amplitude-v1` (the branch `amplitude-impl`, commits (i) `ca2e5fad`, (ii)
`9ca0600c`, (iii) `578742e3`, (iv) `f3d4ad54` and (v)) adds the world key
`amplitude`; every world without it must read as it did, byte for byte
([MIGRATION](MIGRATION.md), the design's section 6). The owner's change of
2026-09-20 to the design's test 7 replaces the replay of every registered
world by a gate set of one world per table rule, key and family kind, so
that every engine path runs once (the full register replay and the
coverage-measured gate set belong to a later trimming pull request). The
gate set (the scratchpad tools `replay.py` and `compare.py`: every world
run with the base tree `7f986124` and with the branch, `events.jsonl` and
`state.json` digested, `run.json` compared with its volatile fields
removed), what each world covers:

| world | covers |
| --- | --- |
| `two_slits` | `rerelease` on 91 directions, a lamp, the `wave` reading, z periodic |
| `bell/read` | the read form of `phase_window`, `pass`, a free and a paid family |
| `bell/a0_b8` | `measure` under `phase_window` (the chooser), a lamp |
| `weak/j2_filter` | `phase_width` on `measure` |
| `weak/w_exchange` | `become`, `lifetime`, a charged paid family |
| `weak/j3_neutron_free` | `columns`, `lifetime`, `become`, the `beam` reading |
| `nucleus/deuteron_1` | `columns` and `lifetime` on free families |
| `lensing/mass_meeting` | `meeting`, `read`, `measure` |
| `bohr/r2` | `action` (the turn by momentum) |
| `hubble/coasting_age` | `read`, `measure`, `pass` with `reads` |
| `coupling/7_pp` | free families alone, z periodic |
| `catalog/lamp_mirror_screen` | `rerelease` with `phase_window`, a lamp |
| `catalog/sun_planet` | `rerelease` with a free crowd |
| `heisenberg/w3_beam` | the `beam` reading on a `rerelease` world |
| `one_content` | one free family, open faces |
| `redshift/age` | `pass` with `reads` on a free family |
| `detector/periodic_z_node` | `in_transit`, a paid family, z periodic |

After commit (i) and at stage (v) (the working tree that (v) commits, the
engine with the layer, the split, the gate and the review's fixes), the
seventeen replays give `events.jsonl` and `state.json` identical to the
base tree's, and `run.json` differs by the key `amplitude` false added and
nothing else (`run_json_diff.py`: `/amplitude (added)` on every world).
The digests at stage (v) (the first 16 hexadecimal digits of the sha256):

| world | events.jsonl | state.json |
| --- | --- | --- |
| `two_slits` | `7b1135dc8480a022` | `bb1b1ffde3a9f8a3` |
| `read` | `1ec4bbab4473d4f5` | `2ab033bb2a9a23a3` |
| `a0_b8` | `601a3937eb4e59f6` | `9608515fa4d8705f` |
| `j2_filter` | `1c92c9c3817755e7` | `709d6c476ac6dab9` |
| `w_exchange` | `80ebe74909824bad` | `c1514fd62be5fe9c` |
| `j3_neutron_free` | `ca857e2846aa5b86` | `5777301aacbd71e1` |
| `deuteron_1` | `5a8be8d83e20abe1` | `bfbaec73edb1bf1f` |
| `mass_meeting` | `c307b0721938e66a` | `fee84f9d69b12795` |
| `r2` | `6b39d6192485557b` | `958fcc9dc314e073` |
| `coasting_age` | `6d33d3ac82b6bea9` | `71b6cb3cba97e561` |
| `7_pp` | `da177386799d3861` | `ceb7df3e3d69b9cf` |
| `lamp_mirror_screen` | `e6ca788d38ca28b9` | `4ad0e0bde47ebf16` |
| `sun_planet` | `9eb5b1953114c8a8` | `3cecc7c2a1361553` |
| `w3_beam` | `800eaa869e738837` | `29a06f0c188ea4bd` |
| `one_content` | `a8b1f8191dd478a4` | `861f21006fe5f65e` |
| `age` | `39a304861b12c02b` | `4542d6a424ca4419` |
| `periodic_z_node` | `ec81debeb25e6df5` | `e7b814baedb8d3fe` |

The physics reviewer of commits (i) and (ii) replayed `two_slits`,
`bell/read` and `two_contents` independently with the same digests
(`7b1135dc...`, `1ec4bbab...`, `951a50a7...`). The keyed worlds of series L
are the register's ([EXPERIMENTS](EXPERIMENTS.md), "L, the amplitude
law"); `tests/test_amplitude_layer.py` (e) checks that every gate-set
world parses without the key.

Stage (vi) (the design's section 6 as the model owner's half-hour
version: the key forced true and the crowd's pointer gate off, the
working tree not committed, the scratchpad `replay_vi`) replayed the same
seventeen worlds against the stage-(v) digests: `two_slits`,
`lamp_mirror_screen` and `w3_beam` are refused at load (the lamp's rate
other than [1, 1]), `sun_planet` fails in the run (two multiplicities of
one record at one set), and of the thirteen that ran twelve change
`events.jsonl` (`read`, `a0_b8` and `mass_meeting` in their clicks;
`7_pp`, `age`, `coasting_age`, `j2_filter`, `one_content` and
`w_exchange` by the columns `record`, `branch` and `multiplicity` written
on every line with no value differing; `deuteron_1`, `j3_neutron_free`
and `r2` by their digests) and thirteen change `state.json`
(`periodic_z_node` by its rows' columns alone). Worlds outside the
crowd-threshold series change, so stage (vi) stopped and the key stays
([MIGRATION](MIGRATION.md), (vi)); the branch's engine is stage (v)'s.

## The weak force in the world's terms: the 85 example worlds replayed after each commit, series J - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` from its tip `6a596b34`
(the strong force, series I, the wave threshold and the four unifications
landed; source fingerprint
`da947becf3343b3e812d59ea88ba51650ba791cf19c7782f8d665763f2df0f49`, the
fingerprint of the entry below), Python 3.14.0rc2, numpy 2.5.3, headless,
four cores. Every world of `examples/events/` (85 before series J's worlds
were added) was run with the runner at its declared `ticks` before the
first change and after each commit of the model owner's decision of
2026-09-20, "go on everything" ([BEAM_LAW note 36](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
and `events.jsonl`, `state.json` and `run.json` (its volatile fields
`elapsed_seconds`, `source_sha256` and `package_version` removed) compared
by SHA-256, file by file, raw and normalized (the document parsed, the
record keys the commit added removed wherever they occur, re-serialized
with sorted keys and hashed: the added keys are reports of the record,
named per row, and a raw difference by them alone is not a changed
integer).

| After | Source fingerprint | `events.jsonl` | `state.json` raw / normalized | `run.json` (stable) raw / normalized | Keys added to the record |
| --- | --- | --- | --- | --- | --- |
| (i) the window's width `phase_width` (N / 2 by default) | `55f30af0309c2812646384a0caf4d16a956e5ae525df878a008c6bf075e90941` | 85 identical, 0 changed | 4 / 85 identical | 4 / 85 identical | `widths` per measured event (None where no width is declared) |
| (ii) D-1, a paid family's whole charge per unit of amount on the charge line | `b28c5865ec143004b36203e8aad70a4bed65f80896cc6b5f526f6d71748732b6` | 85 identical, 0 changed | 4 / 85 identical (the `widths` of (i) alone) | 4 / 85 identical (the same) | none (no registered world declares a charge on a paid family) |
| (iii) the transformation `become`, the identity `weak-v1` | `071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c` | 85 identical, 0 changed | 4 / 85 identical (the `widths` of (i) and the added `became` of the states) | 0 / 85 identical (the added `become` in `numbers` of every declared measured event, None everywhere) | `became` per measured event (the transformations fired) and its books' measured line; `become` per measured event in `numbers` (None where none is declared) |
| (iv) the W world (no key added; the source byte-identical to (iii)'s) | `071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c` | as (iii): 85 identical, 0 changed | as (iii) | as (iii) | none |

No registered series moves (C, 7, D, E, G, H, I, K, Bell, A10, the
catalog): every reading of the register is the same integer under the
window's width, and the 81 worlds whose `state.json` and `run.json`
differ raw differ by the added `widths` key alone (the four raw-identical
ones, `deuteron_3`, `pp_1_weak`, `pp_3` and `alpha_square`, are the
nucleus worlds whose bodies all left the GameBoard, so their final states
hold no measured event for the key to enter). The commands: `python -m
event_universe --init <world> --output <dir>` per world, four at a time,
the outputs digested and pruned; `python tools/check.py --base 6a596b34`
green after the commit (487 tests selected), `--base 2605f75f` green after
(ii) (464 tests), `--base af7ce995` green after (iii) (507 tests), `--base
HEAD` green after (iv) (196 tests) and after the clock's correction (28
tests); `python tools/check.py --full` green on the merge with the branch
tip `4c9be1f6` (the window read from a reading, issue #363, and the choosers
on the GameBoard: both sides kept, the weak force's note renumbered 35):
ruff, mypy strict and 603 tests; then on the merge with `origin/main`
`a9c12384` (the G1 tie, the rays fixes, #363 and the meeting: both sides
kept, the weak force's note renumbered 36 and its hypothesis 21) ruff,
mypy strict and 619 tests, and six worlds replayed under the merged
engine against their own side's engine (`two_slits`, `bell/read`,
`lensing/mass_meeting` and `nucleus/deuteron_1` against main's,
`weak/j2_default` and `weak/w_exchange` against this branch's):
`events.jsonl` byte-identical in all six, `state.json` and `run.json`
equal but for the other side's added keys (`widths`, `became` and
`become` on main's worlds; `meeting` and `turned` on the weak worlds).

**Series J1 and J3, the neutron's decay against its clock** (the register
entry [J, the weak force (2026-09-20)](EXPERIMENTS.md#j-the-weak-force-2026-09-20)):
the five worlds `j1_lattice`, `j1_source`, `j3_deuteron`,
`j3_deuteron_crowd` and `j3_neutron_free` of `examples/events/weak/` run
through `tools/run_series.py --jobs 3` at the fingerprint
`071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c`, 650, 650, 700, 700 and 600
intervals, completed in 231, 238, 82, 70 and 53 s with the books balanced
at every tick (the charge line the same pair through every
transformation); `tools/weak_readings.py`: 0 record checks failed, 15
readings inside, 3 outside, none moved. The expectations were written
before the runs by `examples/events/weak/make_worlds.py` into
`expectations.json` (each neutron's trigger tick from the count its
clock read at tick 100 of a warm run without the `become` keys, at +
floor(at x c / 2^20)). Inside: the shell's 64 beta clicks a step in both
J1 worlds (the width over the median 0.036 and 0.038 against nature's
3.17), every click the content 3, the count the neutrons'; the deuteron's
pair holding after the transformation (0 steps of 39 and 21 attempted),
the gated neutron never firing in 700 intervals, the free neutron firing
at 512 exactly, every beta reaching its shell. Outside, the one GAMEBOARD
criterion in three worlds: the corners of `j1_lattice` at 524 against the
pinned 522 (the warm run's count at one tick, 12 rows of 1839, had caught
a gap of their line-mates' rows; their count at the trigger 15 rows,
27585), 48 neutrons of `j1_source` and the deuteron's neutron 1 to 3
intervals after their pinned ticks (the count over a clock's history
under a fan's dwells is not the one tick's count the estimator took); the
numbers in the register, nothing moved.

**The W world, the exchange at one Link** (the register entry
[J, the weak force (2026-09-20)](EXPERIMENTS.md#j-the-weak-force-2026-09-20)):
`examples/events/weak/w_exchange.json` run through `tools/run_series.py`
at the fingerprint `071197bc5d0f08cbe52aa44dca0e0d7ad9adf99ef6bf6023231310b9bb8f211c` (the
transformation's: the W world changes no source), 16 intervals, 0.1 s,
the books balanced at every tick; `tools/weak_readings.py`: 0 record
checks failed, 5 readings inside, 0 outside: the neutron's `become` at
tick 8 with the W on +x, the proton's click at tick 9, its charge [0, 1]
and content 1839 after, the border `lifetime` 0, the momenta -192 and
+192.

**Series J2, the neutrino's passage through a filled bar** (the register
entry [J, the weak force (2026-09-20)](EXPERIMENTS.md#j-the-weak-force-2026-09-20)):
the five worlds of `examples/events/weak/j2_*.json` run through
`tools/run_series.py --jobs 4` at the fingerprint
`55f30af0309c2812646384a0caf4d16a956e5ae525df878a008c6bf075e90941`, 1037
intervals each, every run completed in about 3 s with the books balanced
at every tick; `tools/weak_readings.py`: 0 record checks failed, 13
readings inside, 0 outside, none moved. The expectations were computed
before the runs from the engine's flight table by
`examples/events/weak/make_worlds.py` (the first-arrival ages 13 at 8
Links and 326 at 190; 1024 arrivals at the first reader, 711 rays reaching
the far detector) and every count came out exactly: 16 of 1024 at the
first reader of `j2_filter` (1 / 64), 0 at the 127 behind it, 699 at the
far detector; 64 readers of 16 in `j2_ladder` and 0 beyond; 512 and 352
in `j2_default`; 32 and 688 in `j2_stride2`; 0 and 711 in
`j2_stride2_odd`.
## The meeting: the 85 example worlds replayed with the key absent, the ten registered worlds replayed with it, and series K old against new - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` from its tip `329c5660`
(the record of the decision on the meeting) with the meeting's commits
(the engine and its tests, `41971d27`; the worlds, the tool and the
register after it), source fingerprint
`dc1cce964db367167732b1727d9dc8d2fcf73a27bf13e33a1822cc5a84fff1a3`,
Python 3.14.0rc2, numpy 2.5.3, headless, four cores
([BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
the model owner's decision, "DECIDED: the meeting, M-R").

**The key absent: every world byte-identical.** Every world of
`examples/events/` as it stood at the tip (85: the coupling twenty-one,
the Bell ten, the orbit six, the Bohr seven, the nucleus eight, the
lensing four, the Hubble four, the redshift two, the buildup three, the
Heisenberg eight, the detector four, the catalog four, `one_content`,
`two_contents`, `one_slit`, `two_slits`) was run with the runner at its
declared `ticks` on the tip's tree (the base, `git archive 329c5660`) and
on the meeting's tree, and `events.jsonl`, `state.json` and `run.json`
(its volatile fields `elapsed_seconds`, `source_sha256` and
`package_version` removed) compared by SHA-256, file by file:

| Tree | `events.jsonl` | `state.json` | `run.json` (stable) |
| --- | --- | --- | --- |
| the meeting's, the key absent | 85 identical, 0 changed | 85 identical | 0 identical, 85 changed: the record's new key `meeting` (false) and the `turned` lines (zero) in every audit line's `families[<name>]` and `momentum` and in the per-tick `momentum` list, and nothing else (`7_00` and `control` re-run on both trees and their records compared key by key with the added keys removed: no other difference) |

**The key declared: the ten registered worlds byte-identical.** The six
worlds of series 7 (`7_00`, `7_mm`, `7_mp`, `7_pm`, `7_pp`, `7_pp_m4`),
`2` (series C), `s8_r12` (series D), `r4` (series H) and `coasting_age`
(series G) were copied with `"meeting": true` added and run on the
meeting's tree at their declared `ticks` (200, 200, 4000, 3000 and 400):
every one completed, and its `events.jsonl` and `state.json` are
identical to the same world's replay without the key on both trees (no
paid row in transit meets a free row in any of them, as the design
counted). `control_meeting`, the control of series K under the key, is
byte-identical in `events.jsonl` to `control` (the sha256
`22ec156b13a2aa21...`).

**Series K old against new.** The four worlds of K under the key
(`<name>_meeting.json`) and the lens world, `tools/run_series.py --jobs 2`
under the load of the replay, `tools/lensing_readings.py` (0 record
checks failed, 14 readings inside, 9 outside, none moved; the entry
[K under the meeting](EXPERIMENTS.md#k-under-the-meeting-2026-09-20)):

| World | K without the key (registered): centroid shift y, mean age, count, faces, the mass's clicks of light | K under the key: the same | expected under the key |
| --- | --- | --- | --- |
| `control` | 0, 89.40, 1455, 0, 0 | 0, 89.40, 1455, 0, 0 | unchanged |
| `mass` | 0.000, 89.40, 1455, 0, 0 | -1.790, 89.90, 1350, 0, 122 | -3.0 +- 0.5, 90.43, 0.996 of the control, 0 |
| `heavy` | 0.000, 89.40, 1455, 0, 0 | -4.359, 90.64, 1242, 210, 1 | -4.3 +- 0.5, 90.64, 0.858, 209 |
| `near` | 0.000, 89.40, 1455, 0, 0 | -2.301, 89.71, 1237, 77, 169 | -2.6 +- 0.5, 89.72, 0.901, 136 |
| `lens` | - | the crossing 71.0 Links past the mass, 394 taken by the mass | about 70 |

The meeting's cost, host time on an idle machine: `mass` stepped
in-process for 400 intervals 19.9 ms per interval without the key and
24.5 ms with it, the meeting 4.6 ms per interval, 67 permutations built
in the run at 0.58 ms each.

The commands: `python replay.py --src <tree>/src --out <dir> --jobs 3`
(the base) and `--jobs 2` (the meeting's tree; the scratchpad's replay
script of the four unifications: `python -m event_universe --init <world>
--output <dir>` per world, the outputs digested and pruned to keep the
disk), `compare.py <before> <after>`; the keyed copies run the same way
from a tree holding them beside a copy of the meeting's `src`. `python
tools/check.py --base HEAD^` green on the engine's commit alone (450
tests selected, ruff, mypy strict) and `--base HEAD` green on the working
tree with the register (487 tests); `python tools/check.py --full` green
on the merge with the branch tip (the entry of the merge below the
commits).
## The choosers on the GameBoard: the key replayed, and the run - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` from its tip `9379b01c`
with the one additive key of issue #363 (a table entry's `phase_window`
read from a reading, [BEAM_LAW note 34](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
source fingerprint after the key
`38792132301970e7c276cfee4184534dcd2223fe3a4d906c78be3714afd5c142`,
Python 3.14.0rc2, numpy 2.5.3, headless. Twenty-one example worlds (the
Bell ten, `one_content`, `two_contents`, `two_slits`, `one_slit`,
`lamp_mirror_screen`, `clock_near_mass`, `sun_planet`, `neutron_star`,
`w1_wave`, `shared_3_nodes`, `periodic_z_node`) run with the runner at
their declared `ticks` on a copy of the source tree before the key and on
the tree after it, and `events.jsonl`, `state.json` and `run.json` (its
volatile fields `elapsed_seconds`, `source_sha256` and `package_version`
removed) compared by SHA-256: 21 identical, 0 changed, in each of the
three files. The Bell ten read again through `tools/bell_chsh.py` on the
tree after the key: S = 2 and S' = 3/2 exactly, 326 criteria, 0 failed.

The run ([A2 with the choosers on the GameBoard](EXPERIMENTS.md#a2-with-the-choosers-on-the-gameboard-2026-09-20);
`examples/events/bell/read.json` and its six controls, `tools/bell_choosers.py`):
`read` 1940 intervals in about 5 s, the books balanced at every tick, 1920
pairs in 15 bins, every E the triangle exactly, S = 2 exactly on
(0, 25) x (8, 29), the largest S over every quadruple 2, every marginal
1/2, 46 criteria, 0 failed; the four `written` worlds S = 2 exactly, 91
criteria, 0 failed; `fixed` E(0, 8) = 1/2, 24 criteria, 0 failed;
`one_clock` E = 1 in 64 bins of one phase, no quadruple, 68 of 214
criteria failed (the control that must fail). `python tools/check.py`
green on the change, `python tools/check.py --full` green on the merge
with the branch tip.

## The four unifications of the formulas: the 85 example worlds replayed after each commit - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` from its tip `e98453f7`
(the strong force landed; source fingerprint
`0b39130239c775492fe336818039801e572af6bb0128b9f8be41bcd031163228`, the
fingerprint of the entry below), Python 3.14.0rc2, numpy 2.5.3, headless,
four cores. Every world of `examples/events/` (85: the coupling
twenty-one, the Bell ten, the orbit six, the Bohr seven, the nucleus
eight, the lensing four, the Hubble four, the redshift two, the buildup
three, the Heisenberg eight, the detector four, the catalog four,
`one_content`, `two_contents`, `one_slit`, `two_slits`) was run with the
runner at its declared `ticks` before the first change and after each of
the four commits of the model owner's decision ([BEAM_LAW note 33](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)),
and `events.jsonl`, `state.json` and `run.json` (its volatile fields
`elapsed_seconds`, `source_sha256` and `package_version` removed) compared
by SHA-256, file by file.

| After | Source fingerprint | `events.jsonl` | `state.json` | `run.json` (stable) |
| --- | --- | --- | --- | --- |
| (1) the pointer as the first moment of the one reading over the circle | `1e84ce8ef9df6e86ff84c64b04ffa5c8241e9a16d6ba1cb8566406b47679241d` | 85 identical, 0 changed | 85 identical | 85 identical |
| (2) every age against a key as the one `by_clock`; `K` as the rate [n, d] | `59543c35c50110f5c40714f7f24895e1178d0ea4a68b18dcdff3c6cd1aeeca10` | 85 identical, 0 changed | 85 identical | 85 identical |
| (3) one moment table over one set object shared by a body and a detector | `b2708413e219ca9136981c3d68936f96ad4a7317ae4ce61e0c9b0bd6f9631711` | 85 identical, 0 changed | 85 identical | 85 identical |
| (4) the columns floored at the clock age | `da947becf3343b3e812d59ea88ba51650ba791cf19c7782f8d665763f2df0f49` | 85 identical, 0 changed | 85 identical | 85 identical |

No registered series moves (C, 7, D, E, G, H, I, K, Bell, A10, the
catalog): every reading of the register is the same integer under the
four unifications. The elapsed seconds of the runs were taken under
concurrent load (the checks ran beside the replays) and are not a
measurement; the pointer's table (thirteen columns per row where two
products were formed) and the one table over the set are host cost, not
the model's local cost. The commands: `python -m event_universe --init
<world> --output <dir>` per world, four at a time, the outputs digested
and pruned (the disk of the session holds no five copies of the 4.4 GB
of records); a differing world would have been re-run from the kept copy
of the base tree. `python tools/check.py --base HEAD` green after each
commit (246, 469, 221 and 222 tests selected), `python tools/check.py
--full` green on the merge with the branch tip.

## The `wave` threshold on the pointer's square: the 66 example worlds compared, A10 and Bell re-read - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on the commit of the `wave`
threshold on the pointer's square and the escaped momentum per family
([BEAM_LAW note 32](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
issues #359 step A, #360, #361 item 1), source fingerprint
`0b39130239c775492fe336818039801e572af6bb0128b9f8be41bcd031163228`,
against the commit before it (`23a7e0fd2135e714bf072d09c5a0d4925ad0d3edb8b32adab0f84f1e9a010599`),
Python 3.14.0rc2, numpy 2.5.3, headless, four cores. Every example world
of `examples/events/` under the Beam Law but series I (66) was run under
both with `tools/run_series.py` and the runs compared file by file.

| Check | Result |
| --- | --- |
| The 66 worlds, `events.jsonl` before against after | 65 byte-identical: the coupling twenty-one, the Bell ten, the orbit six, the Bohr seven, the redshift, Hubble and detector worlds, `one_content`, `two_contents`, `two_slits`, `one_slit`, and `w1_wave`, `w3_wave`, `w9_wave` and the four `w*_beam` (no set of theirs ever read a pointer below its threshold with an amount at it); `w27_wave` differs |
| `w27_wave` (A10, `tools/heisenberg_readings.py` on both) | 2312 `pass` records naming `threshold` (antiphase pairs at a pixel, the pointer 0) where the pairs clicked with the record 0; the pairs go on: face:+x 0 -> 408 clicks, face:+y and face:-y 12 833 -> 13 613 each, the escaped 25 666 -> 27 634, 38 of the 161 pixels' records differ, the sum of the screen's records 0.16 % higher; the count FWHM 0.761 -> 0.758, the count rms 0.325 -> 0.321, the record FWHM 0.185 and the product 4.99 unchanged, the record rms 0.224 -> 0.225, the clicks 150 187 -> 148 131; 0 record checks failed; the books balanced at every tick |
| The Bell ten (`tools/bell_chsh.py` on both) | S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24) = 2 exactly before and after, every run check passed |
| `two_slits`, `one_slit` | byte-identical: their 27 220 and 13 610 screen clicks unchanged (no antiphase pair met a pixel in one interval) |
| The escaped momentum per family (`run.json`'s `escaped` lines) | each family's own where the world's total was written into every line: `w27_wave` light (10 830 512, 0, 0) and wall (0, 0, 0) where both read the total; the faces' `families` carry `momentum` beside the face's total; the books' escaped line unchanged |
| `tests/test_nature_beam_detector.py` (i), the re-pinned (a) to (d), `tests/test_nature_beam_readings.py` (d), `tests/test_nature_beam_body.py` (b), `tests/test_nature_beam_books.py`; `python tools/check.py` | ruff lint and format, mypy and 499 selected tests green |

The runs establish what the threshold on the pointer's square does on the
engine (rays that cancel pass and go on; the coherent record of a set they
passed is unchanged; the record of what they reach later is not); they
establish no physical law.

## Series I, the nucleus: eight runs - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on the commits of the one
mechanism (the columns `de6c4968`, the lifetime and the held content
`7a77fa0c`, the contact through the table `b2c164c2`) and the series I
commit, source fingerprint
`a86447318c757023605e4ba33ab1ef1a15726fef839b893d5d50b899750188f5`,
Python 3.14.0rc2, numpy 2.5.3, headless, four cores.

| Check | Result |
| --- | --- |
| Series I, `examples/events/nucleus/` (eight worlds, `tools/run_series.py --jobs 3`, 3000 intervals each) | every run completed in 4 to 87 s with the books balanced at every tick; `tools/nucleus_readings.py`: 0 record checks failed, 29 readings inside, 1 outside (the first step of two protons at three Links at tick 66 against the steady toy's 30 .. 60), none moved; the table in [EXPERIMENTS, I](EXPERIMENTS.md#i-the-nucleus-2026-09-20) |
| `tests/test_nucleus_readings.py` | the tool's reading of a run written by the runner pinned to the record: the design's pair on the six headings (the pushes (128, 0, 0) from -7936 and +8064, the hand-overs 256, 128, 640, the border's 12 clicks per interval from tick 4) |
| `python tools/check.py` | ruff lint and format, mypy and the selected tests green |

The runs establish what the one mechanism does on the engine (the
designed pushes integer by integer, the deuteron bound at one Link and
free at three, the binding threshold of two protons, the square sheared
and the line held); they establish no physical law, for or against.

## The columns, the lifetime, the held content and the contact through the table: the 66 example worlds compared - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on the commits of the one
mechanism ([BEAM_LAW note 31](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)):
the columns (`de6c4968`, `columns-v1`), the lifetime and the held content
(`7a77fa0c`) and the contact through the table (this commit), Python
3.14.0rc2, numpy 2.5.3, headless, four cores. Every example world of
`examples/events/` under the Beam Law (66; the entity worlds excluded) was
run with `tools/run_series.py` under the engine before the columns
(`ad20aa65`, source fingerprint
`d29df4af8cfd79512d827d32df7b885948b2a90a4865cf1993b01bb74b76095c`), under
the columns (`da74b0fff14e65e23f80154ba6528a3af0a328ea4a7565f071ee3de2f33ce84b`)
and under the contact
(`23a7e0fd2135e714bf072d09c5a0d4925ad0d3edb8b32adab0f84f1e9a010599`), and
the runs compared file by file.

| Check | Result |
| --- | --- |
| The columns: 66 worlds, before against after | `events.jsonl` byte-identical in every world; `state.json` equal but for the added `charges` per measured event; `run.json` equal but for the added `columns` keys and `hypotheses` (the two built-in columns are the landed form integer by integer) |
| The lifetime and the held content: 66 worlds | unchanged: no example world declares a `lifetime` or `held` (the border and the held content are exercised by `tests/test_lifetime.py`) |
| The contact through the table: 66 worlds, the columns against the contact | 60 worlds byte-identical in `events.jsonl` (no body of theirs ever stepped onto another); 6 worlds differ from the first refused step of a body on: the coupling `1b_m1`, `1b_m4`, `1b_m16` (tick 32), Bohr `r2` (tick 72) and `r4` (tick 454), the orbit `s8_r12` (tick 174); every run completed with the books balanced at every tick |
| `python tools/check.py` after each commit (`tests/test_columns.py`, `tests/test_lifetime.py`, `tests/test_contact.py` among the selected) | ruff lint and format, mypy and the selected tests green |

The six worlds under the contact, old (the refused step leaving the labels
as they were) against new (the occupant's table reading the body,
`measure` by the keys), `tools/bohr_readings.py` and
`tools/orbit_readings.py` on the new runs:

| World | Old | New |
| --- | --- | --- |
| coupling `1b_m1` | the free probe at x = 61 from tick 31, every further step refused, its momentum growing under every read to (-2 260 249 792, 0, 0) at tick 200, the source's (1 073 741 824, 0, 0) | the same 11 steps to x = 61; from tick 32 every refused step hands the probe's x component to the fixed source, 169 hand-overs (-146 316 992 at tick 32, then about -12.58 million per interval, one per interval), the probe's momentum (0, 0, 0) and the source's (-1 186 507 968, 0, 0) at tick 200; the sum of the two the same; the escaped line the same |
| coupling `1b_m4`, `1b_m16` | the probe's momenta m times `1b_m1`'s: (-9 040 999 168, 0, 0) and (-36 163 996 672, 0, 0) | 169 hand-overs m times `1b_m1`'s (-585 267 968 and -2 341 071 872 at tick 32); the probe (0, 0, 0), the source (-2 598 548 224, 0, 0) and (-12 541 676 544, 0, 0) |
| Bohr `r2` | 1.47 turns of the angle, one closing (T 79, return 1.0 Links, mean radius 1.74), r 1.0 .. 16.3, the electron out through face:-x at tick 254 after 33 steps, no coherence reading | 7 hand-overs to the fixed proton (ticks 72, 312, 389, 393, 404, 421, 425; 0.46 to 1.34 x 10^9 label units each, on x and on y), 2.07 turns, two closings (T 84 and 166, returns 0.0 and 1.4 Links, mean radii 1.74 and 2.66), r 1.0 .. 17.9, the phase's turn per orbit 0.688 (the design 0.946), C(2) = 0.60 and the slope 1.27 (outside C >= 1.0), out through face:+x at tick 688 after 76 steps; the proton's momentum (2 316 591 360, 3 929 525 040, 0) |
| Bohr `r4` | 1.28 turns, one closing (T 138, return 2.0, mean radius 2.66), r 1.0 .. 18.4, out through face:+y at tick 540 after 68 steps | one hand-over at tick 454 (1 186 767 242 on y), 1.25 turns, the same one closing, r 1.0 .. 18.0, out through face:+y at tick 600 after 68 steps; no coherence reading either way |
| orbit `s8_r12` | the angle reaching 2 pi at tick 198 with the return (+5, 0), mean radius 15.20, C 1.54 on the turn, out through face:+x at tick 271 after 144 steps | one hand-over at tick 174 (251 on y, the probe at the Node beside the source), the angle reaching 1.00 turn and no closing, r 1.0 .. 60.0, 17 reads of 3335 units, C 0.30 over the run, out through face:+x at tick 260 after 133 steps; the source's momentum (0, 251, 0) |

The registered entries of series C, D and H keep the numbers of their date
(a run is recorded once) and each carries a note pointing here; `r15`,
`r16` and every other world with a body are unchanged, no step of theirs
having been refused. The runs establish what the contact does on the
engine (the hand-over as pinned, the books closed); they establish no
physical law.

## A10 at a low rate, the single-click build-up: three runs - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` at the tip `9fc895a2` (the
Beam Law, `beam-v1`; the engine unchanged by the run), source fingerprint
`a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b`,
Python 3.14.0rc2, numpy 2.5.3, headless, four cores; the model owner's go
of 2026-09-20 on the physicist's entry 5 of the law's own predictions and
the owner's decision on issue #359 ([Highlights 5.4](HIGHLIGHTS.md#54-the-detector));
the readings registered in
[A10 at a low rate](EXPERIMENTS.md#a10-at-a-low-rate-the-single-click-build-up-2026-09-20)
and the worlds' [README](../examples/events/buildup/README.md).

| Check | Result |
| --- | --- |
| A10 at a low rate, `examples/events/buildup/` (three worlds, `tools/run_series.py --jobs 3`, 420, 1200 and 7780 intervals) | every run completed (55.4, 38.8, 91.8 s) with the books balanced at every tick; `tools/buildup_readings.py`: 0 record checks failed, 2 readings inside, 1 outside, none moved: the narrowing of the coherent record against the count 0.307 at the rate 47 (expected >= 0.2), 0.052 at 8 (reported), -0.017 at 1 (expected 0 +- 0.02); R / I at the record's peak at the rate 1 1.200 at y = 58 (expected 1 +- 0.02: outside; the centre pixel 0.843), the coincidences of the synchronized comb 6.6 % of the cells and 12.3 % of the clicks |
| `tests/test_buildup_readings.py` | passed: on a 14 x 5 plane at the rates 2 and 1 the tool's pixels equal the engine's detector sets, R / I = 2 exactly with every cell a coincidence and 1 exactly with none, the wavelength (64 / 8) / sqrt 3 |
| `python tools/check.py` (the scoped selection) | ruff lint and format, mypy and the selected tests green; the language, hygiene and navigation gates green |

Re-run under the `wave` threshold on the pointer's square after the
merge of the strong force's commits (source fingerprint
`0b39130239c775492fe336818039801e572af6bb0128b9f8be41bcd031163228`,
[the entry above](#the-wave-threshold-on-the-pointers-square-the-66-example-worlds-compared-a10-and-bell-re-read---2026-09-20)):
the three worlds change (an antiphase pair at a pixel passes where it
clicked with the record 0 and goes on), the clicks in the window 172 753
-> 169 855, 171 871 -> 158 878 and 171 742 -> 158 622, the cells with 2+
rays 25 921 -> 25 277, 46 174 -> 39 263 and 10 560 -> 4000, the record's
FWHM, the product and R / I at the peak unchanged, the narrowing 0.292,
0.050 and -0.005 (were 0.307, 0.052, -0.017), every verdict the same (2
inside, 1 outside), 0 record checks failed; the rows old against new are
in [EXPERIMENTS, A10 at a low rate](EXPERIMENTS.md#a10-at-a-low-rate-the-single-click-build-up-2026-09-20).
Series K's four worlds (`examples/events/lensing/`) are unchanged under
it, reading by reading (16 inside, 0 outside).

The runs establish what this engine's screen reads at a low rate (the
lobe of the coherent record vanishes as the coincidences within one
interval do); they establish no physical law. The physicist's entry 5 is
registered as measured, a plain disagreement with nature (Merli,
Tonomura) and, by the owner's decision on #359, the law's limit.

## Series K, light beside a mass: four runs - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` at the tip `9fc895a2` (the
Beam Law, `beam-v1`; the engine unchanged by the series), source
fingerprint
`a1b2a949ccda2194537ecae4c6ff7380642f8f7d7877c01ab0e1649ba51c5d4b`,
Python 3.14.0rc2, numpy 2.5.3, headless, four cores; the model owner's go
of 2026-09-20 on the physicist's entry 2 of the law's own predictions
([Highlights 5.4](HIGHLIGHTS.md#54-the-detector)); the readings registered
in [K](EXPERIMENTS.md#k-light-beside-a-mass-2026-09-20) and the worlds'
[README](../examples/events/lensing/README.md).

| Check | Result |
| --- | --- |
| Series K, `examples/events/lensing/` (four worlds, `tools/run_series.py --jobs 4`, 400 intervals) | every run completed (6.5, 9.1, 9.9, 9.1 s) with the books balanced at every tick; `tools/lensing_readings.py` (with the replay): 0 record checks failed, 16 readings inside, 0 outside, none moved: the deflection of the beam's centroid 0.000 pixel in y and z beside the mass at b = 6, twice the mass, and b = 3 (expected 0 +- 0.5; nature 46 to 91 radians or the capture), the delay 0.00 interval (0 +- 1), the count 1455 the control's (1 +- 1 %), the phase rate 8.000 the lamp's turn (8 +- 0.05); the replay: 447 rows in flight at most, none turned, 162 Nodes per interval shared with the crowd |
| `tests/test_lensing_readings.py` | passed: the speed 32 / 55 and the dwell 55 / 32 off `flight_table`; on a 13 x 5 x 3 box the tool's pixels equal the engine's detector sets, the arrival at the age 17 (m(17) = 10), the centroid (3, 1), the phase rate 8.000, the crowd by series E's form, the replay's 17 rows and one meeting Node, 6 verdicts inside |
| `python tools/check.py` (the scoped selection) | ruff lint and format, mypy and the selected tests green; the language, hygiene and navigation gates green |

The runs establish what this engine's detectors read of a beam beside a
mass (nothing of the mass: the flight is blind to the crowd); they
establish no physical law. The physicist's entry 2 is registered as
measured and as a plain disagreement with nature (Eddington, Shapiro).

## Series G, the Hubble diagram behind the detector: four runs - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` at the merge of the charge
per unit of content (`b9a0e6c6`) with the worlds and the tool of the series
(the engine unchanged by the later tip), source fingerprint
`5a93868357b564b3c0448e04db424eaf3acb1617e1ab1a448a42989e88481776`, Python
3.14.0rc2, numpy 2.5.3, headless, four cores: the four worlds of
`examples/events/hubble/` through `tools/run_series.py --jobs 4` (36.6,
37.3, 35.8, 36.6 s for `coasting_scalar`, `coasting_age`, `pushing_scalar`,
`pushing_age`, 400 intervals each), every run completed with the books
balanced at every tick; `tools/hubble_readings.py` (with the replay, 3
minutes): 0 record checks failed, the reading's formula 288 of 288 inside
2 %, 22 pinned readings inside and 26 outside, none moved; the readings
registered in
[G](EXPERIMENTS.md#g-the-hubble-diagram-behind-the-detector-2026-09-20)
and the worlds' [README](../examples/events/hubble/README.md).

| Check | Result |
| --- | --- |
| The reading's formula, 1 + z against (1 + k)(1 + v / c) from the record (detector readings) | 288 of 288 inside 2 % over the three windows; the coasting worlds z = v / c declared to 0.003 rms and tau to 1.3 intervals of the throw's own coasting form |
| The linear law, H t_0 (the coasting worlds) | 0.875, 0.949, 1.029 at t_0 = 150, 250, 350: outside, inside, inside |
| The coasting form q = 0 the nearest at the near H, rms below 0.02 | inside at t_0 = 150 (rms 0.026, outside), outside at 250 and 350 (q = -0.55 the nearest by the initial distances r_0 / c); the best-H rms of the three forms within 0.005 |
| The decelerating form (the pushing worlds): H t_0 < 1, q_eff > 0, q = -0.55 the farthest | H t_0 > 1 in 5 of 6 windows, q_eff > 0 in 5 of 6, q = -0.55 the nearest in 6 of 6; on the GameBoard p(400) / p(0) = 0.68 to 0.96, every source decelerated; the Doppler part alone H t_0 = 0.80 to 0.99 |
| What is observed today, q = -0.55 the nearest | in 10 of 12 windows (expected outside in every run) |
| The bend of the age clock | reported: zero in the coasting crowd, -0.089 to +0.081 per source in the pushing crowd, no monotone bend |
| `tests/test_hubble_readings.py` | passed: c = 32 / 55 and m(17) = 10, m(34) = 20 off the flight table; on a bar of 61 the tool's `record` lines, click ages and steps equal the engine's, k = 0, z within 0.05 of 1 + v / c at v = 1 / 2 |
| `python tools/check.py` (the scoped selection) | ruff lint and format, mypy and the selected tests green |
| `tools/hubble_readings.py --no-replay --from-one-point` on the same four runs (the physicist's review, 2026-09-20; not pinned) | the near fit reads an exact coasting throw from one point at the windows' taus as H t_0 = 1.10 to 1.15, so q = -0.55 is "the nearest at the near H" for a coasting form itself; with every tau reduced by (r_0 / c) / (1 + z) the coasting readings lie on the Milne form at H t_0 = 1.01 to 1.04 with a best-H rms of 0.0045 to 0.0056 (q = -0.55 within 0.001 of it, q = +0.5 at 0.012 to 0.013); the pushing Doppler part from one point 3 to 11 % below the coasting run's H t_0, q = 0 the best form in 4 of 6 windows (q = -0.55 by 0.001 or less in the other two); `tests/test_hubble_readings.py` 3 passed (the collapse onto the Milne form exact, the near fit's bias upward) |

The runs establish what this detector reads of a throw on this engine (the
Doppler of the throw times the emitters' clocks, and the shape of the curve
against three forms); they establish no physical law, and the resemblance
to the accelerating form is registered with its two causes on the GameBoard
(the throw's initial distances and the emitters' clocks), not as an
acceleration. The review's follow-up (the register entry's last bullet)
finds the resemblance to be the near fit's own bias on any coasting form
plus the initial distances: a limit of the reading, not a finding.

## A body on a set, the turn by momentum and series H, Bohr's lines behind the detector - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on three commits after the
tip `38c9b621` (the body on a set of Nodes with one record, `span`; the
turn by momentum, `action` and `phase_by_momentum`, `bohr-v1`; series H),
[BEAM_LAW note 30](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
source fingerprint `d29df4af8cfd79512d827d32df7b885948b2a90a4865cf1993b01bb74b76095c`.
Python 3.14.0rc2, numpy 2.5.3, headless, four cores.

| Check | Result |
| --- | --- |
| `tests/test_nature_beam_body.py` (a) to (f) | passed: a set of one Node equal to the measured event of the engine before the change record by record and row by row over 30 intervals with rays, collisions and clicks (the reference integers taken on that engine first: 152 clicks, 20 record lines, 5 steps, 5 homes, the record 37348285440); the set of three Nodes reading, clicking, owing and pushing as one, stepping as one, refused at an occupied Node, clicking on the face, wrapping; the books balanced with a set that releases (the shares 8, 4, 4 then 4, 8, 4); the turn's phases 11, 37 and 50, 32, 14, 59, 41 as derived by hand, composed over axes 14 and 18, today's phase without `action`; the rays' rows identical with and without the two keys on a colliding crowd of 324 rays over 40 intervals; every refusal by name and the record |
| `tests/test_push_width.py` (a), `tests/test_nature_beam_clock.py` (e) | `engine.step_axis` and `engine.count_owed` pinned to the step rule and the owed count, no integer changed |
| `python tools/check.py --base 38c9b621` after each feature | ruff lint and format, mypy and 335 then 337 tests green |
| Series H, `examples/events/bohr/` (seven worlds, `tools/run_series.py --jobs 4`, 3000 to 10300 intervals) | every run completed in 19 to 87 s with the books balanced at every tick; `tools/bohr_readings.py`: 0 record checks failed, 1 coherence reading inside and 1 outside, five worlds without a reading (fewer than two closed turns): no orbit closed within r / 4 at any radius; at r = 8 two turns of mean radius 8.11 and 7.95 with T 722 and 736 (838 derived), the returns 5 and 4 Links, the escape at the close pass of the third turn; the phase's turn per orbit 0.234 of a circle against 0 designed; C(2) = 0.84 against the expected 1.0 ([the register](EXPERIMENTS.md#h-bohrs-lines-behind-the-detector-2026-09-20), [the README](../examples/events/bohr/README.md)) |
| `tests/test_bohr_readings.py` (a) to (c) | the tool's flight time, pointer per turn, coherence and run reading pinned to the engine's `manhattan_steps`, `coherent_pointer` and the runner's record |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite green on the final commit |

The runs establish that the body on a set and the turn by momentum do what
the notes say on the engine (the turn as pinned, the GameBoard unchanged), and
that on this fan and this width no orbit of the electron closes well enough
for Bohr's lines to be read behind the detector; they establish no physical
law, for or against.

## Charge per unit of content: series 7 equal integer by integer, B1 and B3 corrected - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on the tip `b0c4a193`, three
commits: the label's product checked per row before it is formed (the
architect's B1), the push reading the content the frame read (B3, the
orchestrator's D1), and the charge per unit of content with the push as one
product and the record's two columns gone (the model owner's decision;
[BEAM_LAW notes 26 to 28](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation);
[changelog](../CHANGELOG.md); [migration](MIGRATION.md#charge-per-unit-of-content-on-2026-09-20-the-familys-charge-a-pair-no-charge-on-a-measured-event-the-records-two-columns-gone)).
Python 3.14, numpy, headless.

| Check | Result |
| --- | --- |
| B1 (`tests/test_nature_beam_label.py` (c), (d)) | a merged row of weight 2^56 on (1, 1, 0) accepted with the label 2^56 x (45, 45, 0), on (1, 0, 0) refused naming the Node [2, 2, 2], the amount and 2^56 x 64 = 2^62; the mirror's merged re-emission refused at the recount naming [5, 5, 0] |
| B3 (`tests/test_nature_beam_push.py` (j)) | the architect's probe world in both family orders: the same reads (-960, -1536, ... at ticks 11 to 16), `held` {5, 114}, `pushed` (-356544, 0, 0); before: [B, A] read -1536 at tick 11 and (-378432, 0, 0) |
| Series 7, the six worlds through `NatureBeamSimulation` on the tip before and after the charge per unit of content | every `read` record equal (181 per world, 185 in `7_pp_m4`), `pushed` and momenta equal, 4635 and 4663 events, the books balanced with the recount; the worlds regenerated with the families `q` and `p` and their pairs |
| The push's fixtures (`test_nature_beam_push` (a) to (e), (i)) | re-fixtured on two free families with the pairs [3, 4], [1, 5], [-3, 4], [1, 2], [2, 1]: every integer unchanged (-1088, -1472, -1280, 0, -544 per read) |
| `tools/migrate_nature_beam_worlds.py --check` on every example world | unchanged (the series 7 worlds regenerated by the generator); the old `7_pp` refused naming both events and the family; the old `7_pp` with the probe's charge removed rewritten to the family charge [1, 2] |
| The ray suites, `python -m pytest tests/test_ray_*.py ...` | green (the label, push, parsing, bijection, detector, worlds and entity suites) |

The runs establish that the charge per unit of content changes no integer
of the registered series 7 readings and that the two blocking defects are
closed by pinned tests; they establish no physical law.

## The age whole and the clock's redshift in space: series E - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` on the age commit (the
ray's age kept whole and read by the measured event, [BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 25; [changelog](../CHANGELOG.md)), source fingerprint
`cd90313373651164e7f1a1e5f2d0f5019356cd5fb4bc9d3f909511b4f783be52`.
Python 3.14.0rc2, numpy 2.5.3, headless, four cores.

| Check | Result |
| --- | --- |
| `tests/test_nature_beam_age.py` (a) to (e) | passed: the age 200 whole after 200 intervals (35 until the change); a head-on pair parked with the ages 60 kept and the class cycle ha hb -> +z-z -> +y-y observed (the first derivation had the pair leave on z without meeting again; the pin was corrected to the observed cycle before registration); the re-emission and the birth at 0; the age moment 41, 61 with here, fixed under the 48 symmetries; the clock's ages 1, 2, 3, 4, 5, 6, 6, 7, 7, 7, 7, 8, ... under `reads: "age"` equal to the hand derivation at every interval, the scalar reader unchanged; the bound's default 108 and 222, the refusals, the stub refused at its 13th interval; the GameBoard identical with the ages whole and reduced over 40 intervals of a colliding crowd |
| A sample of the registered worlds under the whole age (`one_content`, `two_contents`, `two_slits`, coupling `1b_m16` and `5_long`, orbit `s32_r12`, Bell `a0_b8`) | every run completed with the books balanced at every tick, no age past its default bound (the coupling plane 830, the orbit plane 830, the two slits 620, the cube 252); the `audit` of `run.json` unchanged (the clocks read the presence by default, integer by integer); `state.json` differs where a ray's age had passed its period |
| `python tools/check.py` (the scoped selection of the age commit) | ruff lint and format, mypy and 300 tests green |
| Series E, `examples/events/redshift/` (`scalar`, `age`; `tools/run_series.py --jobs 2`, 300 intervals each) | both completed, the books balanced at every tick, 16.0 s and 15.5 s; `tools/redshift_readings.py`: 0 record checks failed, 11 readings inside, 3 outside: k_s x r^2 = 39.0 to 44.8 (mean 41.5) and k_a x r = 33.1 to 39.2 (mean 36.1) over r = 6 to 14, their ratio 0.870 against sqrt 3 / 2; the redshift ratios of the age clocks 0.50, 0.57, 0.72, 0.82 at r = 6, 8, 10, 12 against the fitted 1 / r law 0.52, 0.65, 0.78, 0.90, outside the 15 %-of-shift criterion at r = 8, 10, 12 ([the register](EXPERIMENTS.md#e-the-clocks-redshift-in-space-under-the-age-reading-2026-09-20), [the README](../examples/events/redshift/README.md)) |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite green on the final commit |

The runs establish that the age reading of a measured event reads M / r
where the presence reads M / r^2 on this engine, and that the whole age
changed no integer of the GameBoard's step; they establish no physical law.
## The label along the unit vector of the direction: series C x 64 exactly, Bell unchanged, series D re-run - 2026-09-19

The worktree of `claude/universe24-new-3ytqde` on the tip `5b3873f0` (the
exact record merged), two commits: the momentum label along the unit
vector u_d of the direction at the flight table's scale Q = 64, with the
physics-rule reviewer's four corrections, and the re-registration
([BEAM_LAW section 2](BEAM_LAW.md#2-the-record-of-a-ray-and-the-world-file)
and note 23; [changelog](../CHANGELOG.md); [migration](MIGRATION.md#the-label-along-the-unit-vector-of-the-direction-on-2026-09-19-the-momentum-units-change-by-q--64)).
Python 3.14.0rc2, numpy 2.5.3, headless, four cores; source fingerprint
`0eaa589ab51cdc0a12a863cd23e535e1e8ac052e8b4f3f8facf30ef05a323c5a` on every run below.

| Check | Result |
| --- | --- |
| The table u_d (`tests/test_nature_beam_label.py` (a)) | the eight pinned vectors of the verdict; 63^2 < \|u_d\|^2 < 65^2, u_{-D} = -u_D, equivariance under the 48 on the table; over all 1780418 primitive directions with components in -64 .. 64 the integer rule equals the float rounding (0 mismatches), no component beyond 64, no exact tie, \|u_d\| within 1.35 % of 64 |
| The books under the label (`test_nature_beam_label` (b)) | a lamp of content 3 on the six headings and eight fan directions: every label 3 x u_d, the recoil -(the labels born) = (-1134, -723, -363) exactly, measured + transit + escaped = (0, 0, 0) at every one of 60 intervals through clicks at a screen (each click the ray's own label), a mirror on (7, 5, 0) (exactly 2 x 3 x (52, 37, 0) per ray reflected) and the open faces; the running transit line equal to the recount |
| The bound (`test_nature_beam_label` (c), `test_nature_beam_world_parsing` (d)) | content x amount = 2^56 refused by the parser and by `label_weights` naming 64 x 2^56 = 2^62; 2^56 - 1 accepted; the bound-edge worlds at 1/64 of their amounts read the same integers (-(2^62 - 64), the bound reached exactly) |
| The suite, `python -m pytest -n auto` | 391 passed in 10.6 s; every momentum pin x 64 (the fan fixtures on u_d), every position of `test_push_width` and `test_nature_beam_clock` (d) unchanged with the declared momenta x 64 (`by_clock(age, 64 n, 64 k) = by_clock(age, n, k)`), `test_nature_beam_push` (e) 96 per tick where 2, 1 alternated, `test_nature_beam_detector` (e)'s beyond-register row 2^52 -> 2^49 |
| Series C, `tools/run_series.py --jobs 4` on the 21 coupling worlds, `tools/coupling_readings.py` | 392 criteria passed, 0 failed; 19 readings inside, 9 outside, every reading equal to the registered one (the tool divides the labels by Q where it compares with q or an amount); every push, momentum and momentum book line x 64 exactly against the registered run, the series 7 electric part included (item 7 unlike signs (-4517272576, 0, 0) = 64 x (-70582384, 0, 0)); the counts, presences, clocks and Gauss's flux unchanged; 0.3 to 2.5 s per run |
| Bell, the ten A2 worlds, `tools/bell_chsh.py` | 326 criteria passed, 0 failed; S = 2 exactly, the lamp's momentum [0, 0, 0]; every printed line as registered |
| Series D, the six orbit worlds regenerated by `make_worlds.py` (p = 192, 320, 576 label units), `tools/orbit_readings.py` | 12 record checks passed, 0 failed, 3.9 to 6.1 s per run; no orbit closed by the criterion; S = 32, r = 12 bound for 2891 intervals and 6.74 turns (the first closing of the angle at 289 against 343 expected, the mean radius 11.25, C 1.32; seven closings, every return 2 to 10 Links off), S = 32, r = 24 one turn in 829 (687 expected), S = 8, r = 12 one turn in 198 (196), S = 1 no read ([EXPERIMENTS](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19)) |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite green |

The runs establish that the label's scale changed every momentum of the
six-heading worlds by the one factor 64 and nothing else, that the
readings tools compare in the units they claim, and how the orbit worlds
read under the decided label; they establish no physical law.
## A10, the width of an opening and the spread behind it: eight runs - 2026-09-20

The worktree of `claude/universe24-new-3ytqde` after the detector-set
commit (`dacbe0f3`), source fingerprint `f3fb33607190c86c...`, Python
3.14.0rc2, numpy 2.5.3, headless, four cores: the eight worlds of
`examples/events/heisenberg/` through `tools/run_series.py --jobs 4`
(2.1, 4.5, 12.5, 52.7 s for w = 1, 3, 9, 27 under `beam`; 2.2, 5.0, 12.7,
52.4 s under `wave`), every run completed with the books balanced at every
tick; `tools/heisenberg_readings.py` 16 record checks passed, 0 failed;
the readings registered in
[A10](EXPERIMENTS.md#a10-the-width-of-an-opening-and-the-spread-behind-it-under-the-beam-law-2026-09-20)
and the worlds' [README](../examples/events/heisenberg/README.md). The
runs establish what this screen reads of the spread behind an opening
under the two readings; they establish no physical law, and the reading
of the lobe fails at w <= 9 on the sparse fan (a limit of the reading,
registered).

## The detector as a set with one record, the two readings and the phase returned: the runs compared - 2026-09-19

The worktree of `claude/universe24-new-3ytqde` on the tip `382a17df` (the
Highlights record of the owner's principle), one commit: the detector set
(`DetectorSet`), the `reading` key (`beam` the default, `wave`) and the
phase returned to the set's measured events ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors),
note 23; [changelog](../CHANGELOG.md)). Python 3.14.0rc2, numpy 2.5.3,
headless, four cores. The 45 example worlds run through
`tools/run_series.py --jobs 2` on the tip's source (extracted with `git
archive`) and on the changed source; `events.jsonl` compared line by line
with the `record` lines set aside, `run.json` by its `audit`, its
detectors and its status.

| Check | Result |
| --- | --- |
| The 45 worlds, tip against the change: every `click`, `pass`, `home`, `read`, `rerelease` and `step` line | identical in 43 of 45 worlds (the Bell ten, the coupling twenty-one, the detector four, the orbit six, `one_content`, `two_contents`); `two_slits` and `one_slit` identical after the screen's pixel detectors are renamed (`screen` -> `screen_<y>`: the only difference in their 59320 and 30881 lines) |
| The books (`audit` per tick), the status, the faces' records | equal in 45 of 45 |
| The `record` lines | the same number of lines in every world (one per detector set per family per interval, the sets being one Node each in every shipped world); their values differ where the default `beam` now counts (the Bell counters 1 per click instead of 32^2 x 256^2; the detector examples likewise) and are equal on the `wave` screens |
| `two_slits`, `one_slit`: the screen's record per pixel | equal on all 121 pixels (the tip's one detector's per-Node `measured[].record` against the change's 121 one-Node `wave` detectors), 27220 and 13610 clicks alike |
| `tools/bell_chsh.py` on the ten Bell runs, tip and change | 326 criteria passed, 0 failed on both; every printed line equal but the order Python prints a set in; S = 2, S' = 3/2, the offsets 14 and 16; the change's `run.json` carries the counters' `phase` as the last click's (15, 16, 18, 55 in `a0_b8`; 0 on the tip) and their detectors' record as the count (80, 65, 83, 64) with `reading` `beam` |
| `tests/test_nature_beam_detector.py` (f), (g), (h); `tests/test_nature_beam_worlds.py` (a) | passed: the set of three Nodes records 32^2 x 256^2 whichever Node the ray reached, the threshold 2 over the set, the window on the set's phase 8; the phase returned 40 and the lamp's rays at the received phase; the beam pairing (2 in phase click, opposite cancel, the arc with a window, the greedy order, the split row); the two-slit correlation with the two-source cosine unchanged above 0.85 with the screen as 121 one-Node `wave` detectors |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite (390 tests) green |

The runs establish what the set changed in the record of the shipped
worlds (the reading, not the GameBoard: no click, pass, push, step or book
moved) and that the Bell readings are unchanged under the default; they
establish no physical law.

## The detector's record exact, never refused: the runs unchanged and `two_contents` completed - 2026-09-19 (after the batching)

The worktree of `claude/universe24-new-3ytqde` on the tip `3fb70572` (the
batching merged), one commit: the record's bound and refusal replaced by
the exact record ([BEAM_LAW section 5](BEAM_LAW.md#5-the-detectors-record-the-re-emission-the-face-detectors),
note 19; [changelog](../CHANGELOG.md)). Python 3.14.0rc2, numpy 2.5.3,
headless, four cores. The same byte-identity check as the batching's: the
45 example worlds run through `tools/run_series.py --jobs 4` on the tip's
source (extracted with `git archive`) and on the changed source;
`events.jsonl` and `state.json` compared byte for byte, `run.json` as a
document without `elapsed_seconds` and `source_sha256`.

| Check | Result |
| --- | --- |
| The 45 worlds, tip against the change | 44 of 45 identical (`events.jsonl`, `state.json`, `run.json` with the per-tick `audit`); `two_contents` differs only by completing: on the tip it fails at tick 19 (`the amount 262144 clicked at face:+y in one interval exceeds the affordable amount ... 261123`), after the change it completes 200 intervals, and the tip's 19-interval `events.jsonl` (5158 bytes) is the byte prefix of the new one (498555 bytes) |
| `two_contents`, 200 intervals | completed, the books balanced at every tick (`conserved_at_every_completed_tick` true), 0.2 s; the two pushes equal and opposite along x, toward each other, +/-411217348788224 = 2^24 x 187 x 2^17 (each content times the flow of the other's beam over the 187 intervals it arrived); `face:+y` clicks 47448064 units and holds the record 181 x 2^62 = 834715169335357210624 (70 bits; two beams of 2^17 in phase per interval since the 20th, 2^62 each interval, one past the law's bound 2^62 - 1), `face:+x` 713 x 2^60 = 822033032784681893888; the escaped momentum (0, 0, 0); `run.json` and `state.json` carry the records as exact integers beyond 2^63 |
| `tests/test_nature_beam_detector.py` (e), `tests/test_nature_beam_worlds.py` (e) | passed: the pointer's register bound 560759486676481; 261123, 261124, 2^18, two rows a quarter turn apart and 2^52 recorded exactly against the Python-int computation through the tables (2^52 records 2^130 with the pointer (2^65, 0)); two intervals of 2^18 accumulate 2^63 and round-trip through JSON; the face click of 2^18 records 2^62; `two_contents` for 20 intervals not refused, every face's record equal to the Python-int square at every tick |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite green |

The runs establish that the exact record changed no integer of a world
that ran before and that the refusal alone kept `two_contents` from
completing; they establish no physical law.

## The host's batching: the runs unchanged byte for byte - 2026-09-19

The worktree of `claude/universe24-new-3ytqde` on the base `b2830bf9` (the
Beam Law with the one push form), five commits of optimizations
([BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
note 22; [changelog](../CHANGELOG.md)). Python 3.14.0rc2, numpy 2.5.3,
headless, four cores. The byte-identity check: the 45 example worlds (the
ten Bell worlds, the twenty-one coupling worlds, the four detector worlds,
the six orbit worlds, `one_content`, `two_contents`, `two_slits`,
`one_slit`) run through `tools/run_series.py --jobs 4` on the base source
(extracted with `git archive`) and on every commit's source; `events.jsonl`
and `state.json` compared byte for byte, `run.json` compared as a document
without `elapsed_seconds` and `source_sha256`.

| Check | Result |
| --- | --- |
| The 45 worlds after each of the five commits | 45 of 45 identical (`events.jsonl`, `state.json`, `run.json` with the per-tick `audit`) on every commit; `two_contents` fails at tick 19 on the base and after alike (the affordable amount at `face:+y`, 2^18 > 261123, a pre-existing refusal of the night's bound), its partial artifacts identical |
| `tools/bell_chsh.py` on the ten Bell runs, `tools/coupling_readings.py` on the twenty-one coupling runs | 326 and 392 criteria passed, 0 failed, on the base and after every commit; every printed line equal but the order Python prints a set in and the seconds line |
| The suite, `python -m pytest -n auto` | 381 passed in 16.8 s on the base; 386 passed in 5.5 s after (the flight test 7.3 -> 0.75 s with the cached collision table, the two slits' world test 12.7 -> 3.8 s) |
| `python tools/check.py --full` | ruff lint and format, mypy and the whole suite green on the final commit |
| Timings, the best of three headless runs with the record and the books every tick (ms per interval / us per Node / us per row, base -> final) | plane source `coupling/5` 2.97 / 0.203 / 0.745 -> 1.61 / 0.110 / 0.403; `two_slits` 12.38 / 1.71 / 2.43 -> 3.51 / 0.48 / 0.69; Bell `a0_b8` 0.53 / 25.2 / 19.9 -> 0.47 / 22.4 / 17.6; `one_content` 0.77 / 0.049 / 6.2 -> 0.58 / 0.037 / 4.7; orbit `s32_r12` 1.47 / 0.101 / 1.11 -> 0.77 / 0.053 / 0.58 |

The runs establish that the host's batching changed no integer of the law;
they establish no physical law.

## The push as one form, the one label, the affordable amount and series D re-registered - 2026-09-19 (the night)

The worktree of `claude/universe24-new-3ytqde` on the tip `c5eb5868` (the
moments change, the NatureBeam rename, the width of the push and series
D). The physics-rule review's F1 and F2 corrected, F3 and F7 dissolved,
proposal 2 implemented ([BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation),
notes 18 to 21; [migration](MIGRATION.md#the-push-as-one-form-the-one-label-and-the-affordable-amount-on-2026-09-19-the-night)).
Runtime source SHA-256 `cc7815756f50640ad10582af461cf58267c424eb8182177e580d0b5eedbd4769`; the tip's `70763568dc216a8b7a0ecdfac36654cdf1e1da80bb6b20d34eccfac2d8c62c8e`. Python 3.14.0rc2,
headless, four cores.

| Check | Result |
| --- | --- |
| `tests/test_nature_beam_push.py` (new) | 5 passed: the reviewer's world (every push -5 V + by_clock(age, 3 V, 4), `pushed` (-340, 0, 0)), the sign, the uncharged probe, the cancellation q_A q_B = M_B (push 0 exactly), the fractional floor (-170, 0, 0), a paid emitter (the label sum, the lamp's momentum + transit + escaped = 0 at every tick), a fan emitter ((-40, -20, 0) per read), the one label at the click, the re-emission and the home |
| `tests/test_nature_beam_collision.py` (d), `tests/test_nature_beam_detector.py` (e) | 4 and 5 passed: no collision at a measured event's Node (the head-on pair passes, the windowed click takes its label, nothing at rest); the affordable amount 261123 (a row at the bound records 2139119616^2, 261124, a sum of two rows, 2^52 and a face refused naming the sum) |
| The ray suite and the consumers, `python tools/check.py --base HEAD` | ruff lint and format clean, mypy on the changed sources, every selected test passed |
| Twenty-one coupling runs, `python tools/run_series.py --jobs 4`, on both sources | every `events.jsonl` identical byte for byte between the tip's source and the new one (the series 7 `read` records row by row: the one form equals the three-branch push integer by integer); `tools/coupling_readings.py`: 392 criteria passed, 0 failed, 19 inside, 9 outside on both, the printed readings equal line by line but the fingerprint; `state.json` differs on the coupling worlds by the two columns `charge`, `mass` of the free family's rows, on nothing else |
| Ten Bell runs on both sources | `events.jsonl` and `state.json` identical on all ten; `tools/bell_chsh.py`: 326 criteria passed, 0 failed on both, every printed line equal but the fingerprint and the order Python prints a set in |
| The affordable amount on the registered worlds | the coupling faces click 174762 units per interval (the 2^17 beam and the two z rays re-emitted in six shares), inside the bound; the first draft of the bound (2^17) refused them and was corrected to the derived value before the register was read |
| Six orbit runs (series D re-registered), `python tools/run_series.py --jobs 4` | all completed in 5.7 to 6.5 s, the books balanced at every tick; `tools/orbit_readings.py`: 12 record checks passed, 0 failed, exit 0; no orbit closes at any width (S = 1 and 8 zero reads, S = 32 at r = 12 one eccentric turn in 229 intervals returning two Links off, S = 32 at r = 24 falls in); registered in [D, the orbit](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19) |
| `python tools/check.py --full` | ruff lint and format on 115 files clean, mypy on 21 source files clean, 437 passed in 17 s on four workers |

The runs establish that the one form is the earlier computation on every
registered world and that the label is read consistently; they establish
no physical law. The orbit readings are research results, registered and
not moved.

## The table from the keys and the moments: the runs unchanged - 2026-09-19 (the night)

Base `636f391c` on `claude/universe24-new-3ytqde` (the Beam Law with
the owner's approval of the mathematician's proposals 1 and 3 recorded).
The two generic replacements ([migration](MIGRATION.md#the-table-from-the-keys-and-the-moments-on-2026-09-19-the-night),
[BEAM_LAW section 10](BEAM_LAW.md#10-implementation-notes-2026-09-19-the-implementation)
notes 15 and 16) checked against the registered runs: the thirty-five example
worlds (the ten Bell worlds, the twenty-one coupling worlds, `one_content`,
`two_contents`, `two_slits`, `one_slit`) run through `tools/run_series.py`
on the base source (runtime SHA-256 `703f9427...`, the fingerprint of the
registered runs) and on the changed source (`5ba9a47b98e16c80ebf4e46ed57987a2274431f1abe35c2d74a09e6f9f24b794`),
Python 3.14, headless.

| Check | Result |
| --- | --- |
| Every example world parsed on both sources | 39 worlds (the `detector/` worlds through the entity loader): the parsed `NatureBeamWorld`s equal structure by structure (tables, windows, `reads`, the families' free flags, every other field) |
| The Bell and coupling runs, `events.jsonl`, `state.json` and the `audit` per tick | identical SHA-256 digests on both sources for all 31 runs, and for `one_content` and `two_contents` (33 of 35) |
| `tools/bell_chsh.py` on the ten new runs | 326 criteria passed, 0 failed; every printed line equal to the base run's but the source fingerprint (and the order Python prints a set in) |
| `tools/coupling_readings.py` on the twenty-one new runs | 392 criteria passed, 0 failed; 19 readings inside, 9 outside, the printed readings equal to the base run's line by line |
| `two_slits`, `one_slit` (fans) | the digests differ, as the decision says: a fan ray now pushes by its label `content x amount x D` and not by the unit Link of its last step; the world test's correlation still passes (`test_nature_beam_worlds` (a)) |
| Host cost | `one_content` 0.24 s per 200 intervals (0.44 before), `1a_m1` 0.62 s (0.65), `5_long` 3.1 s (3.9), `two_slits` 5.8 s (4.6): the moments per Node cost about what the slots did |

The runs are the register's evidence that the replacements are generic; they
establish no physical law.
## The width of the push and the orbit series D - 2026-09-19

The worktree of `claude/universe24-new-3ytqde` on the base `0a33a202` (the
Beam Law merged), the D1 commit (the world key `width`,
[BEAM_LAW section 3](BEAM_LAW.md#3-the-nodes-interval-nature_beam) step 5 and
note 15) and the orbit series on it. Runtime source SHA-256
`587cbf4852a7fafddc07b2ab35a6a530ed27607ea1aaaec8b17d89933e66d788`,
Python 3.14, headless, four cores.

| Check | Result |
| --- | --- |
| `tests/test_push_width.py` | 4 passed: S = 1 as the rule was, S = 8 once per 9 self-creations at p = M, the step off the clock with no remainder under a count owed (the step on the paying interval), the key's default, record and refusals |
| `python tools/check.py` on the D1 commit | ruff lint and format clean, mypy on 11 source files, 228 passed in 25 s on four workers |
| Six orbit runs, `python tools/run_series.py --jobs 4` | all completed in 5.5 to 6.4 s each (1 ms per interval on 121 x 121 with a fan of 120 directions and about 1200 rows in flight), the books balanced at every tick; `python tools/orbit_readings.py`: 12 record checks passed, 0 failed, exit 0; one orbit closed by the criterion (S = 32, r = 12: 346 intervals against 343 derived, the return one Link off), an eccentric loop; no other closing; the mean push C 1.1 on the first turns; registered in [D, the orbit under the Beam Law, on the plane](EXPERIMENTS.md#d-the-orbit-under-the-beam-law-on-the-plane-2026-09-19) |
| `tests/test_orbit_world.py` | 1 passed in 0.5 s: the probe of `s32_r12` at (71, 60, 0) after 346 intervals with its momentum's y component positive, the books balanced |

## The Beam Law: the engine, the suite and the re-registered runs - 2026-09-19

Base `ce0b22af` on `claude/universe24-new-3ytqde` (the merge of the three
reversible corrections). The engine of the Beam Law
([BEAM_LAW.md](BEAM_LAW.md)) implemented in stages on that base (the engine,
then the tests, the examples and the tools, then the coupling tool, then the
documents), `events-v1` deleted ([migration](MIGRATION.md#the-law-of-the-ray-on-2026-09-19-rays-v1)).
Runtime source SHA-256 `703f9427d9f70e6c619218e457edca0b7647381a8cc7a20d140e4a3d9dd3f671`, Python 3.14, headless.

| Check | Result |
| --- | --- |
| `pytest -n auto` over the suite | 372 passed in 20 s on four workers (the ten `test_ray_*` modules, the consumers, retention and the gates); `tests/test_nature_beam_worlds.py` runs the two slits three times on 60 x 121 x 1 for 500 intervals and the ten Bell worlds through `tools/bell_chsh.py` |
| The collision table at load | 6561 states, 5440 classes, INV[FWD[s]] = s on every state, the amount and the heading sum conserved by every move (`test_nature_beam_collision` (a)) |
| The bijection | 50 intervals forward and 50 inverse on a periodic 8 x 8 x 4 GameBoard with 324 records return the store bit-exact (`test_nature_beam_bijection`) |
| The one reading | the seven basis vectors orthogonal, the slots recovered, the 48 GameBoard symmetries rotate the flow and fix the scalars (`test_nature_beam_readings` (a)) |
| The two slits (world test) | the record's interference term correlates with the two-source cosine at lambda = 8 / sqrt 3 at 0.893 (the design pinned 0.9 for a fan of 203 directions; this world's fan is 91), below 0.5 at the periods 4 and 16; the plain count additive to the unit |
| Ten Bell runs of 160 ticks, `python -m event_universe --init examples/events/bell/<name>.json` | all completed, the books balanced, nothing escaped; E as pinned in every run; S = 2 exactly; S' = 3/2 exactly; the offsets plus 14, minus 16; no-signalling exact; `python tools/bell_chsh.py`: 326 criteria, 0 failed, exit 0 ([A2 under the Beam Law](EXPERIMENTS.md#a2-under-the-beam-law-2026-09-19)) |
| Twenty-one coupling runs, `python tools/run_series.py --jobs 4` | all completed in 0.5 to 3.3 s each; the books balanced at every tick; the measured content constant; age + waited = the intervals completed; `PYTHONPATH=src python tools/coupling_readings.py`: 392 criteria passed, 0 failed, exit 0; 19 readings inside the expectation of BEAM_LAW section 8 and 9 outside, registered in [C under the Beam Law](EXPERIMENTS.md#c-the-couplings-under-the-beam-law-on-the-plane-2026-09-19) (the ring means of six beams follow the GameBoard ring's Node count; the presence slope -0.76; the clock on the axis owed the beam's presence) |
| Performance | 0.23 us per Node per interval on the coupling plane (121 x 121, one source), about 1.0 us on the two slits (about 5100 rows in flight, about 2.7 us per row), against the design's budget of 3.6 us; measured with `time.perf_counter` around `NatureBeamSimulation.step`, a host cost |
| Gates | `ruff check`, `ruff format --check` and `mypy --strict` on `src`, `tests` and `tools` clean; `tests/test_repository_language.py`, `test_repository_hygiene.py`, `test_repository_navigation.py` passed; `python tools/check.py --full`: ruff lint and format on 108 files, mypy on 21 source files, 372 passed |

The register entries mark measured against expected line by line; a reading
outside its expectation is reported, not moved. The runs of the law of events
below keep their scope.

## External detector definition with a periodic return - 2026-09-19

[Experiment E14](EXPERIMENTS.md#e14-an-external-detector-definition-with-a-periodic-return)
was recorded at 11:15 UTC on source
`32235267e55ac8c9df5b1d4bafa3f02a209b7faf`, Python 3.14.7. Each of two
three-interval cases ran once through `runner.run_initialization`, using
`examples/events/detector/periodic_z_node.json` and its external
`entities/detectors.json`. The checked-in phase-16 input was preserved exactly;
the control changes only the incoming phase to 0. The 9-by-9-by-1 world has
only Z periodic. One ordinary material Event at (4,4,0), loaded from
`single_node_detector`, routes one +Z carrier through its same-Node return Link.
N=32, K=1024, reference 0, threshold 1 and capacity 31 were fixed before the run.

Both cases exactly meet the independent expectations: pointer values at ticks
0 through 3 are **0,1,2,3**; the same one carrier retains its owner, phase and
momentum (0,0,1); one material unit plus one transit unit remains 2; nothing
escapes. Complete live states differ at all four times. The three contacts are
three encounters with one circulating carrier, not three distinct quanta.
The material phase and local age are 0,1,2,3; the readout reads that physical
state. Read-only profiling captures only successful constructor/step returns,
and its hook is restored in `finally`. Final captured state equals `state.json`.
An initial host-output lease conflict stopped before simulation construction;
correcting the helper's output layout did not repeat a physical case.

The package fingerprint was unchanged before and after the gate and run:
`7e6367eeed29b3d44e48aee05b3ecd2a68d7c3f9fc122fbfa6efd17da679c0c2`.
The exact definitions SHA-256 is
`3ad1e2351a905044ccd6e61717959276029c3e4b70cdcfaa1e48830e51137cb5`.
Runner metadata matches each preserved input, bundle and expanded document:

| Phase | Document | SHA-256 |
| --- | --- | --- |
| 0 | Original | `05de03b2e231694460a94f8c234c66523e4957436e0d059cd07e5396bde35bc8` |
| 0 | Portable bundle | `197fbf7a0f008c4108f7735a988cf47271adf478b7492a93ece545c09de2ceeb` |
| 0 | Expanded | `a2fc96e389a279e17f9467b1e6e147438c0ffaccbbece445fe90701f9e259e6b` |
| 16 | Original | `143e3f1d0c8f8470f97c8d34c63e5164f168ba130c5e0ee31eb5e9b1aad6e494` |
| 16 | Portable bundle | `931f4ee392c5bde399ec684ba0576664f64afdb056b617bdc778cfb632f57e52` |
| 16 | Expanded | `daf5c37916ff07d6508fa0e156cfe9e5fa65f86ceb0587eaf26988aef140085e` |

On that exact source, `PYTHONPATH=src python tools/check.py --base origin/main`
against main `95768835097c0afcd422bb48e1a065479de1fc01` passed **458 tests in
60.80 seconds** with nine workers, Ruff lint/format, strict mypy on 22 source
files, and source/wheel builds containing the external definitions.
Independent topology and detector checks previously passed 52 cases; the final
selection includes their coverage and entity loading/consumer checks.

The separate saved report `universe24_periodic_detector_entities_9x9.html`
embeds both complete input closures, full states, event/run records and GIF
frames. Its SHA-256 is
`a2aee7d2d3855380164ac9ccd062726fa53ba8b022c9a4b2f427dfc40baf7f92`.
The display is the x-y plane at z=0, uniformly one Link per grid spacing and
one interval per frame; GIF playback is 850 ms/frame. First/last images were
visually inspected. Actual viewer JavaScript passed phase selection and
timeline checks, rendering 81 Nodes, total 2 and final contact count 3.
Full-browser rendering was not verified. The earlier open-GameBoard report is
unchanged. This compact periodic graph establishes no arbitrary 3D equivalence,
speedup, energy law, absorption/reset, Heisenberg relation or entanglement.

## Reversible detector: a shared output retains incoming phase - 2026-09-19

Recorded at 10:01 UTC on source commit
`17dd34c0f8d54b045ab0e4ff9c28e0399dfe6911`, Python 3.14.7. This is the
explicitly selected `reversible-detector-v1` candidate of
[the detector contract](DETECTOR_REQUIREMENTS.md), not the default absorption
rule. [Experiment E13](EXPERIMENTS.md#e13-a-shared-physical-detector-retains-incoming-phase)
uses `examples/events/detector/shared_3_nodes.json`, with only the incoming
phase varied between 0 and 16. Each four-interval case was executed once through
`EventSimulation`; its initial state and every completed state were recorded.
The world is 9 by 9 by 1, open, with the x-y plane at z=0. Material Nodes
(3,4,0), (4,4,0), (5,4,0) form a chain; the last Node is the shared output.
One carrier starts at (2,4,0), heading +X. N=32, K=1024, reference phase 0,
threshold 1, capacity 31. Expectations below were fixed before execution.

| Observable | Expected and observed exactly, in both cases |
| --- | --- |
| Physical output at ticks 0 through 4 | 0, 0, 0, 0, 1; it changes only when the carrier reaches the output |
| Complete live states, phase 0 versus phase 16 | Different at all five recorded times; the carrier retains its input phase |
| Shared visible output, phase 0 versus phase 16 | Equal at all five recorded times |
| Amount on the GameBoard | One transit unit plus three material units, total 4, at every recorded time |
| Material-plus-transit momentum | (1,0,0) at every recorded time |
| Escaped amount | 0 |

The package source fingerprint from `event_universe.runner.source_fingerprint`
was `5d4d2dcf360f8a0f8375977e151b451b64d42fa76ff163ad5561887d6c57b84b`
before and after the run and submission checks. The saved input JSON SHA-256
values are `95f8ee4d986645edb47c4640cf1f68fedecef5cbfe2169997c3e5f481393c562`
(phase 0) and `b9d5ae382cd6fb320b3ad4694dba33f488373d8f8498887bce938a4d570dbe00`
(phase 16). The self-contained report `universe24_physical_detector_9x9.html`
was saved with both input documents, full state records, event records,
fingerprints, an embedded GIF and the existing interactive HTML viewer.
Every displayed region uses one Link per grid spacing and one interval per
frame; GIF playback uses 850 ms per frame. First and last frames were visually
inspected. Viewer JavaScript passed a minimal-DOM execution check for both
scenario selection and final-tick display; full browser rendering was not
verified because the browser download was unavailable.

Independent rule tests passed 26 cases, including the published 3,240-input
injectivity/inverse domain, recoil, retained prior apparatus state, causal
timing, threshold independence, distinct owner channels, detached diagnostics,
deterministic replay and atomic capacity/edge refusals. A near-bound pointer
decoding overflow was reproduced before correction and its regression now
passes. On the exact source commit above,
`PYTHONPATH=src python tools/check.py --base origin/main` selected the related
engine consumers and, because packaging configuration changed, the repository
checks: **344 passed in 77.92 seconds**, Ruff lint/format passed, strict mypy
passed on 21 source files, and both source and wheel distributions built.

Scope: a finite nondestructive transduction demonstration. It supplies no
apparatus energy law, physical reset or absorption mechanism, does not make
default lossy transitions reversible, and derives no Heisenberg, Born or Bell
result. A shared count does not establish entanglement.

## The coupling series C under the law of events, on the plane - 2026-09-19

Base: `ddb4470a` on `claude/universe24-new-3ytqde` (main after PR #345). No
engine change: twenty-one worlds (`examples/events/coupling/`, written by
`make_worlds.py`, a GameBoard of 121 x 121 x 1 with `"boundary": {"z":
"periodic"}`), the analysis `tools/coupling_readings.py` and the register
entry [C, the couplings under the law of events, on the plane](EXPERIMENTS.md#c-the-couplings-under-the-law-of-events-on-the-plane-2026-09-19).
The physics-rule reviewer's design of 2026-09-19, pinned for 61^3 and moved
to the plane by the model owner's decision the same day ("cancel the runs;
let it run on two-dimensional GameBoards"). A research run, made once; not a
test; a reading outside its bound reported, never moved.

| Check | Result |
| --- | --- |
| `python -m event_universe.configuration_validation examples/events/coupling/<name>.json` on the twenty-one worlds | all VALID (kind `events`) |
| Twenty-one runs, `python -m event_universe --init examples/events/coupling/<name>.json --output artifacts/coupling/<name>`, four at a time | all completed; the books balanced at every completed tick; the measured content constant; age + waited = the intervals completed in every world; 168 s of wall time for the twenty worlds (19 to 102 s each) and 63 s for `5_long` (1000 intervals) |
| Item 1, equivalence | identity held: push_m = m x push_1 at all 185 records and three axes for m = 4, 16; the free probes' 11 steps identical for the three m and equal to the rule off the clock on the reads' cumulative push; one merge each at tick 27; registered: the first read at tick 15 with amount 1, the first step at 16 |
| Item 2, the third law with unequal contents | within the bound: \|P_A\| / \|P_B\| 1.256 and 1.213 over the last two windows (3.6 % apart), 1.071 cumulative, toward each other, transverse / axial 0.009 |
| Item 3, superposition | identity held exactly (187 records per number; the total push the sum) |
| Item 4, retardation | the front as derived by hand at every derived Node: -x 4 (5, 180), +y 6 (7, 2), -y 8 (9, 2), +x 4 (5, 180), +x 6 (7, 3); registered on +x past the front: r = 8 (11, 8), r = 12 to 40 (r + 3, 1), the same in every world |
| Item 5, the far field (world 5, ticks 251-300) | the slopes count -0.993, flow -1.048, carried -1.014, size -0.481 (within the bounds); count x r / q 0.33 flat within 1.9 %; flow x 2 pi r / q 0.95 to 1.08; the flux through the square / q 0.995, 0.993, 0.988 at h = 4, 8, 12; outside the bound: carried x 2 pi r / q 1.43 to 1.50 (in-plane Ports 1.18 to 1.26), the flux at h = 20 (0.979) and 40 (0.931), the escape 0.892 q (the fixed point not reached); `5_long`: the escape 0.948 q over ticks 951-1000, rising 0.889 to 0.947 over the 100-interval windows from 300 to 1000 |
| Item 5P, the axis pattern (ticks 151-200) | push x 2 pi r / (m q) 1.71, 1.57, 1.49, 1.54, 1.44, 1.35, 1.40, 1.30, 1.25 at r = 4 to 40; the amount read equal to the replay's count at every tick at every probe |
| Item 6, the clock (`suspension` 1) | identity held: (age, waited, owed) equal to the replay at all nine radii, age + waited = 200; age(200) 6, 9, 13, 19, 25, 31, 38, 47, 63 at r = 4 to 40; outside the bound: age(200) = age(60) at r = 4, 6, 20 (k + 1 above 100 at every radius against the 200-interval window; the counts written finite, 403 to 118) |
| Item 7, the electric reading | identity held: `pushed` (0, 0, 0) for like signs, twice (-2634004, 5855, 0) for unlike, the content-4 probe 3 times; electric / gravity -1 and -1/4 exactly |
| Convergence | (a) carried x 2 pi r / q 1.454 flat within 3.8 % over r >= 5, not equal to the flow's 0.988 within 5 %; (b) the lost fraction 0.970 to 0.685 falling with r against k / (k + 1) 0.998 to 0.990; (c) 0.055, 0.031, 0.034; (d) exact |
| `PYTHONPATH=src python tools/coupling_readings.py artifacts/coupling` | 405 criteria, 390 passed, 15 failed (every failure a reading outside its bound, listed above), exit 1; the negative control (a copy of the runs with one push of 1a_m4 changed by one unit, not kept) fails the equivalence identity as well, 16 failed, exit 1 |
| Gates | `ruff check` and `ruff format --check` on the two new Python files clean; `MYPYPATH=src mypy --strict tools/coupling_readings.py` clean; `pytest -q tests/test_repository_language.py tests/test_repository_hygiene.py tests/test_repository_navigation.py tests/test_configuration_validation.py -p no:cacheprovider` 34 passed; `PYTHONPATH=src python tools/check.py --base origin/main`: ruff lint and format on the two new Python files and 80 passed in 68 seconds over `test_architecture`, `test_check_scope`, `test_configuration_validation`, `test_event_worlds` and the three repository gates (the worlds sit under `examples/events/coupling/`, one level below the glob of the shipped-world preflight test, so they are preflighted by the CLI and by every run, not by that test) |

Runtime source SHA-256 `06a050c9d27a5ab11febe10be40865866e7f0dcbc129400e08c2d7f6b71c8560`, Python 3.14.0rc2, headless.

## The Bell run A2 under the law of events: S = 2 exactly - 2026-09-19

Base: `1f9f280` on `main` (after PR #335), branch
`claude/universe24-new-3ytqde`. No engine change: ten worlds
(`examples/events/bell/`, written by `make_worlds.py`), the analysis
`tools/bell_chsh.py` and the register entry
[A2, under the law of events](EXPERIMENTS.md#a2-under-the-law-of-events-2026-09-19).
The verdict the physicist and the mathematician pinned before the run
(Highlights 5.4): with a deterministic local phase window CHSH is at most 2
as an identity on the record, the correlation is the triangle 1 - 4 k / N,
and the CHSH settings give S = 2 exactly, the model's limit, outcome 1 of A2
against the 2015 data. A research run, made once; not a test.

| Check | Result |
| --- | --- |
| Ten runs of 138 ticks, `python -m event_universe --init examples/events/bell/<name>.json --output artifacts/bell/<name>` | all completed; the books balanced at every completed tick; `escaped` 0 for both families; only `click` and `pass` records; the lamp's momentum [0, 0, 0] at the end; about 0.12 s per run |
| E over 128 pairs (same / different) | (0, 8) +1/2 (96 / 32), (0, 24) -1/2 (32 / 96), (16, 8) +1/2 (96 / 32), (16, 24) +1/2 (96 / 32); the controls (0, 0) +1 (128 / 0), (0, 32) -1 (0 / 128), (0, 16) 0 (64 / 64); (0, 12) +1/4 (80 / 48), (4, 8) +3/4 (112 / 16), (4, 12) +1/2 (96 / 32): every one as pinned |
| S = E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24); S' = E(0, 8) - E(0, 12) + E(4, 8) + E(4, 12) | 2 exactly; 3/2 exactly |
| The tick offsets read off the record | plus tick = age + 9, minus tick = age + 10, the same in every run |
| No-signalling | exact: the ages at which `alice_plus` clicks identical across every b for each a, and Bob's across every a for each b |
| `python tools/bell_chsh.py artifacts/bell` | 326 criteria, 0 failed, exit 0; the negative control (a copy of one run with one click's phase changed by one, not kept) fails the phase criterion and exits 1 |
| Gates | `ruff check tools tests src`, `ruff format --check tools`, `mypy tools/bell_chsh.py` clean; `pytest -q tests/test_repository_language.py tests/test_repository_hygiene.py tests/test_repository_navigation.py tests/test_configuration_validation.py` 34 passed; `python tools/check.py --base origin/main`: ruff lint and format on the two changed Python files and 80 passed in 63 seconds over `test_architecture`, `test_check_scope`, `test_configuration_validation`, `test_event_worlds` and the three repository gates (the ten worlds sit under `examples/events/bell/`, one level below the glob of the shipped-world preflight test, so they are preflighted by the CLI and by every run, not by that test) |

Runtime source SHA-256 `53a70962c5f2c8c860a0895dbc9d6cb7cf125d53aa3d5f0ce6aa5464c79a87f9`, Python 3.14.0rc2, headless.

## Test suite reduced to one test per rule - 2026-09-17

Base: main `5df25f3` (after PR #184), branch `cleanup/prune-tests`, merged
with main `bbb4de7` (PR #186) before publication. Decision
of the model owner, 2026-09-17: one module per generic rule and one per feature
of the ray-event model; see the
[migration note](MIGRATION.md#test-suite-reduced-on-2026-09-17-one-test-per-rule)
for the deleted modules and studies. Python 3.14.0rc2 on Linux, headless,
single-process, `-p no:cacheprovider`, on a host shared with two other test
runs.

| Check | Result |
| --- | --- |
| Whole suite before the reduction | 108 modules; 2,191 passed, 3 visual-only skipped in 622 seconds (the same suite runs about 15 minutes in CI) |
| Whole suite after the reduction, merged with main `bbb4de7` (PR #186, `test_detector_mark.py`) | 40 modules; 1,009 passed in 35 seconds; the slowest modules are `test_ray_delay.py` (13 s), `test_kerengonen.py` (7 s) and `test_repository_language.py` (5 s) |
| Documentation gates (`test_repository_navigation.py`, `test_repository_language.py`, `test_repository_hygiene.py`, `test_json_documents.py`) | 80 passed before and after |
| `python tools/check.py` against `origin/main` | ruff lint and format, mypy on the changed tool, and the affected kept modules passed |

The dated records below keep their original scope: a module they name that is
absent from the suite inventory
was deleted on 2026-09-17, and its numbers remain evidence about that revision.

## Integrated ray ownership and local Focus - 2026-09-14

Reviewed integration input: PR #116 at `b517590b4011f1e2ff9a53be7b61fe76b50f7b08`,
including PR #93, against main `e705435aef311e9000ac6f19136835fa860a6958`.
The first ten targeted counterexamples failed on that input. Their corrections
cover retained-ray validation, funded inventory during a load wait, absorption,
bounded pace state, exact shares, negative threshold funding and claim admission.
Later controls cover directed self-exclusion, explicit unsupported compositions,
observer failure, immutable pace preparation and release of an empty wait.

`tests/test_local_focus.py` and `tests/test_ray_merge_contracts.py`: **50 passed**
on Python 3.14.7. The independent physics review passed the first 49 cases and
the final empty-wait regression separately. The full affected gate and required
CI remain the merge requirements; their actual outcome is recorded in the PR.
That integration set the bond registry aside; the bounded registry entry
below restores it as the declared split of postulate 4. The existing quantum
owner and Q-ORACLE option are unchanged.

Follow-up integration includes main `a686925`, the single-draw reference branch
at `df9c350`, and the relativity probe branch at `280a43b`. Replay now compares the
actual exposed snapshots (hashes are display only), with assertion failures for
mismatches and a changed-seed control. The eight-tick quantum replay and the
12-tick equal-mass collision restart passed; this is no claim about inverting
private queues or arbitrary evolution. The original full local and CI gates
each found one obsolete unreduced-pace assertion (2,780 passed, 7 skipped).
The corrected exact-ratio assertion retains physical trajectory and inventory
checks; its 79-test affected gate passed. Final combined CI is recorded in
[PR #117](https://github.com/Closer24/Universe24/pull/117).

Runtime fingerprint for the measured candidate:
`c297b049e409c84a56906ecf6267fcd4af10b2c9a556ba25c74818e669bfb1f7`.
It hashes sorted `src/event_universe/**/*.py` paths and bytes, separated by NULs.
A headless 256-tick periodic world, shape 513 x 5 x 5, one moving scalar carrier,
one slot and no fields, produced the same complete inventory and model-cost
fingerprint in both modes. Three alternating timing samples had medians
0.2008405 seconds ordinary and 0.0866774 seconds Focus (**2.32x**). Carrier phase
visits fell from 98,944 to 768. Separate tracemalloc runs peaked at 295,185 and
292,785 bytes; that small difference is not a general memory-saving claim.
Both modes retain the same historical Nodes; Focus retains one awake address.
This result does not promise faster dense-world or pure-ray execution.

The input and measured report use the normal 24-hour artifact retention under
`artifacts/local-focus-integration-20260914`. The scheduler argument, memory scope
and reproducible A/B controls remain in Local Focus and its
tests. Existing architecture/physics-review Skills already require local owner
validation, bounded state and independent expectations; no new Skill rule is
needed for these fixes.

## Funded envelope emission - 2026-09-14

Base: `0299cb98bf07f00dc10bad858b674ded449be03e` (main after PR #108). Runtime
source fingerprint of the executed harness:
`f12f349495c0bfd156390a79a7f49fc5df9c368117b25604e212fe68798e676a`. The opt-in
funded envelope emission (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17)
lets `"source": false` pay the wave's classical field from its own conserved
stock. Funded octant emission by ordinary records is now admitted under both
schemas; the plan's conservation check counts it and books the transfer.

Recorded on the interference harness at `phi = pi`, stock 3000, budget 1000
per mode: with no capture the wave paid 211 units, sources stayed zero, totals
stayed at 3000 and the quantum inventory ended at 2789; with a capture at tick
7 the wave paid 199, the localized record received 2801 and then paid 25 per
tick, and the one retarded emission after the capture (2 units) was the entire
recorded source. The runner's strict conservation flag held in both runs.

```sh
python tools/check.py --base 0299cb98bf07f00dc10bad858b674ded449be03e
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The affected gate passed: **2,655 passed and five visual-only skipped**. Ruff,
formatting and strict mypy passed on 120 source files. Python 3.14.0rc2 on
Linux. The stock is bookkept by the quantum owner and the field returns nothing
to it; this is emission-side closure, not a complete field-matter loop.
## Two-wing Bell test - 2026-09-14

Base: `53e44a5` (main after PR #101). Runtime source fingerprint of the
executed harness: `fcd527461961e59fd1295547db9318716245303b7384aa15612a4d7ca23f387a`.
No source module under `src/` changed; the addition is the
two-wing Bell test (`examples/quantum/bell_chsh.md`, deleted on 2026-09-17) harness and template,
its acceptance test, a check-scope entry and index updates.

The harness ran sixteen exact and 400 seeded headless nine-tick worlds under
the unchanged `local-quantum-events-v2` program. Recorded correlations were
`3/5, 3/5, 4/5, -4/5` and CHSH `14/5`, equal to the exact rational prediction
computed before the runs; Alice's weights were `[4, 4]` for every Bob setting
and Bob's marginal `1/2` for every Alice setting; the seeded coincidence
estimate was `74/25`; the dephased control gave `6/5`. Every run reported
conserved totals, two decisions at tick 8 nine Links apart, and classical
outcome codes equal to the recorded quantum outcomes.

```sh
python tools/check.py --base origin/main
PYTHONPATH=src python examples/quantum/bell_chsh.py --output artifacts/bell-chsh --trials 100
```

The affected gate passed: **219 passed, two visual-only skipped**, including
check-scope, configuration validation, repository navigation, language and
hygiene checks. Ruff and formatting passed. Python 3.14.0rc2 on Linux. This is
an exact model calculation with simulated tickets, not a laboratory Bell test.

## Null notices and field-dependent phase - 2026-09-14

Base: `1c782390456ea9629eb0f73c030095574d80e454` (main after PR #99), on top of
the interference harness below. Runtime source fingerprint of the executed
harness: `fcd527461961e59fd1295547db9318716245303b7384aa15612a4d7ca23f387a`.
Two opt-in extensions of `causal-contact-fields-v1` were added, both inactive
without their configuration keys: null notices (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17)
and the field-dependent phase (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17).
The envelope output bank grew from twelve to eighteen fixed slots; the
NodeState contract fixture was widened accordingly and no other test changed.

Recorded on the interference harness: after an arm null at tick 1 with notices
enabled, the source emits 25 of 25 units from tick 2, the next gate emits 9 and
16, and every scale ends at 625/81; an output null at tick 7 reaches the source
at tick 9 with scale 625/337. With a field phase on the M arm, coil fields 0,
200, 400 and 800 select exponents 0, 0, 1 and 2 and record output weights
`[12745, 2880]` and `[160225, 230400]`, equal to the independent Gaussian-integer
prediction; a coil beside the far side of the source selects exponent 0.

```sh
python tools/check.py --base 1c782390456ea9629eb0f73c030095574d80e454
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The affected gate passed: **2,348 passed and five visual-only skipped**, with
seven setup errors in `test_maxwell_configuration.py` and `test_run_live.py`
that came from a missing render extra; after installing `.[render]` those two
files passed (14 passed, two skipped). Ruff, formatting and strict mypy passed
with no issues on 118 source files. Python 3.14.0rc2 on Linux. These are
measured behaviors of configured candidates; no classical limit, energy closure
or multi-excitation Born consistency is established.

## Two-arm interference and coupling summary - 2026-09-14

Base: `1c782390456ea9629eb0f73c030095574d80e454` (main after PR #99). Runtime
source fingerprint of the executed harness:
`4916707db38c4f364552a24a727678698912f509a27969c4217ca02005ca6cf6`. No source
module under `src/` changed; the addition is an experiment harness, its
acceptance test, a reader-facing coupling summary and index updates.

The interference harness (`examples/quantum/causal_interference.md`, deleted on 2026-09-17) ran
thirteen headless 14-tick worlds on the unchanged `causal-contact-fields-v1`
profile. Recorded output decision weights were `[337, 288]`, `[49, 576]` and
`[337, 288]` for `phi = pi/2, pi, 3pi/2`, with no uncertain decision at
`phi = 0`; all equal the exact rational prediction computed before the runs.
Mean source emission after recombination was 25, 13.5, 2 and 13.5 units per
tick against 25, 13.48, 1.96 and 13.48 predicted. The arm-detector variant gave
`[9, 16]` at tick 1 for every phase and no uncertain output decision. After an
arm null the source Node emitted 9 of 25 units per tick: the retarded-source
rule measured. Every run reported balanced accounting and conserved totals.

```sh
python tools/check.py --base 1c782390456ea9629eb0f73c030095574d80e454
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The affected gate passed: **101 passed, two visual-only skipped**, including
repository navigation, language and hygiene checks. Ruff and formatting passed.
Python 3.14.0rc2 on Linux. This records a measured behavior of a configured
candidate; it does not establish a classical limit, field back-action or
energy closure, as stated in the coupling summary (`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17).

## Negative field phase with complex reference - 2026-09-14

Base: integration commit `3a5e7d1`. Independent physics review found that a
negative field exponent conjugated `unit` alone. With `vacuum = unit = i`,
the configured relative phase is one but H U(-1) H returned probability zero
instead of one. Native equivalent coefficient pairs also disagreed: a -400 coil
gave capture probability `576/3125` for `(5, 3+4i)` and `2304/3125` for
`(5i, -4+3i)`.

After correcting a test-only query API typo, the new regressions produced
**12 failures and 5 passes before the runtime fix**. Conjugating both
coefficients repaired the negative relative phase; all **33 field-phase tests
passed in 4.96 seconds**, including the headless runner. The native twelve-tick
controls now agree on capture probability `576/3125`, source envelope weight
`2549/3125` and balanced ordinary field accounting. Inverse powers in both orders
and common complex representations are checked using actual interference
queries, not only matrix entries.

Independent read-only review passed the fix and separately ran 32 tests with
the artifact-writing headless case deselected. Both quantum and ordinary
consumers use the same corrected table; local field scheduling, costs, fixed
NodeState and causal callback inputs are unchanged. The physics Skill records
the missed complex-reference case. Real-vacuum examples retain their behavior.

Final active-source SHA-256:
`8fa258a94a71641e0c71b69038ad57b632e344b998b78d728b99af923a738d3f`.
The earlier full-suite result below predates this focused correction.

On that final source, `python tools/check.py --base 3a5e7d1` passed **2,093
tests with five opt-in visual skips in 216.85 seconds**. Ruff/format passed on
both changed Python files and strict mypy passed on 22 affected source files.
The selection covered causal/recurrent contacts, generic fields and carriers,
conservation, Node/Link timing, parallelism, boundaries, retention and repository
contracts. The saved position-output aggregate passed in **12.48 seconds** with
unchanged native traces and costs when diagnostics were enabled or disabled.
Its source hash matches the final fingerprint above; joint quantum/apparatus
energy closure remains explicitly false. No local build or visualization ran.

## Current-main contact integration - 2026-09-14

Integrated main `53e44a51dd238dff34d5e7ced0f337e8f1c7341f` (PR #101) with
experiment commit `47b7ea01fa7f568dfdd2eca6db99d0da9dca9658`. Retained both
causal and recurrent definitions, using keyword construction for their options.
Recurrent generations explicitly reject unimplemented null-notice/field-phase
combinations. Fixed an automatic-merge error that lost the local field callback
between `start_sources` and `_start_bank`.

On source fingerprint
`5f50a477f657361842f6ed45def673bed50bf30262e0d36cde2088dbe9a349ed`, the user's
requested full gate `python tools/check.py --base 47b7ea0 --full` passed:
**2,865 tests, 30 opt-in visual skips, 313.81 seconds**. Ruff and formatting
passed on 390 files; strict mypy passed on 120 source files. All original quantum,
moment, locality, field, retention, parallelism and new experiments were included.
Focused phase/null/recurrent integration additionally passed 44 tests.

The new composition regressions subsequently use canonical JSON resources rather
than importing other test modules. Their eight cases passed after correcting an
event-label typo; 91 related selector/repository checks passed. Runtime source
remained identical. The updated selector includes both JSON dependencies.
The optional rendering tests were skipped deliberately, and no build ran.

## Spatial wave moments and local position output - 2026-09-14

Continuation base: `86eeb9c5b1c0297067a0ce828ba2faa147c3c151` on draft PR #104,
including open PR #100; fetched main was `d66b43eb193954a9a14a5a33deefd290d61ed547`.
The new candidate report (`examples/quantum/position_moment_response.md`, deleted on 2026-09-17)
specifies the finite observable, local re-encoding and unclosed energy terms.
There are no production changes relative to this base. Production fingerprint
remains `1cf98faec97a7a58fd4ba1b7703d4521e6ea9f02646c6e3338d49753de42e419`.

Initial focused integration: **4 passed in 14.07 seconds**, including the full
headless aggregate, two deliberately invalid moment proposals and renamed,
bounded owners. The observable helper separately passed 30 cases before the
additional entangled-environment regression. Independent physics review passed
the scoped implementation, 33 focused checks and the explicit measurement
controls; the entangled case has mean1, second3 and variance2 without records.
The affected gate `python tools/check.py --base 86eeb9c` passed **151 tests**
with **two opt-in visualization skips** in **39.59 seconds**. Ruff and format
passed on eight changed Python files; no production module needed type checking.
The selected scope includes the new integration/observable tests, resource
selection, repository gates, workspace and headless movie consumers.

Native middle capture derives variance2 and later transfers it to the reservoir;
endpoint capture derives1. Actual propagated wave energy readouts change
10 -> 11 -> 10, or remain11 after middle capture. These are reported as a missing
joint closure, not repaired. Opposite-phase loop states have means +2/-2 despite
equal position probabilities. Position re-encoding does not recover that
incident direction; target mean3 still comes from the configured reservoir.

The physics Skill now requires the distinction between incident state,
re-encoding, vacuum, ensemble drift and selected change. Boss, configuration,
runner and PR Skills were reviewed; their existing scope, ownership and evidence
rules need no further change. Live Highlights was read and reconciled in the
versioned coverage map; it was not edited. No build or visualization ran.

## Local moment response and reserved receipts - 2026-09-14

Task base: `3a2fdfdc796212961a2f305544f0d98998506864`; current main was
`1c782390456ea9629eb0f73c030095574d80e454`. This work includes the still-open
PR #100 dependency and the earlier bounded quantum-to-classical investigation.
The local response report (`examples/quantum/local_moment_exchange.md`, deleted on 2026-09-17) defines
the supplied candidate, input authoring, exact outcomes and remaining limits.

The complete headless experiment passed in **10.8934 seconds** on the final
source. It includes the primary 800-tick native recording, six signed-axis
audits through escape, no-reservoir control, three-tick Links, computation budget
20, and independent exact quantum state-exchange controls. The ordinary audits
preserve mean momentum and expected quadratic kinetic energy, including quantum
inventory and escaped stock. They do not retain full phase or branch correlations.
Independent physics review passed this restricted scope, including rejection of
non-unit masses, false certainty and missing audit fields. Independent ownership
review also accepted the generic unlocked-spare receipt correction.

Active-source SHA-256, checked before and after the experiment:
`1cf98faec97a7a58fd4ba1b7703d4521e6ea9f02646c6e3338d49753de42e419`.
This identifies the tested Windows checkout bytes, including its line endings.
All physical source changes are confined to the reserved-slot receipt fix.

`python tools/check.py --base 3a2fdfd` passed **1,723 tests with five opt-in
visual skips** in 183.53 seconds. Ruff/format passed for nine changed Python
files; strict mypy passed for ten affected source files. The selector covered
native/quantum contacts, field/carrier ownership, local conversions, integer
arithmetic, Node/Link timing, boundaries, generic names, UI/runner consumers and
retention. Eight receipt regressions first failed on the original implementation;
the two focused files then passed 71 tests after repair. No full-suite flag,
simulator build or visualization was used. Versions: Python 3.14.7, pytest 9.1.1,
Ruff 0.16.7 and mypy 2.3.1; Windows pytest used a fresh explicit base directory.

Main advanced during publication to `d66b43eb193954a9a14a5a33deefd290d61ed547`
with PR #102's shared-test builders and active local-contract coverage. Merge
`2baa7c7` retains both the new upstream expectations and this branch's quantum
and moment-response cases. Production source is byte-identical to the fingerprint
above, so the actual experiment remains applicable. The integration gate,
`python tools/check.py --base 304445d`, passed **646 tests** in 29.57 seconds;
Ruff/format passed for 27 affected files. The final documentation and prior
quantum-to-classical experiment regression had also passed 23 tests before this
test-only integration. No failed check was bypassed, and no upstream production
law changed.

## Quantum-to-classical claim investigation - 2026-09-14

The reproducible investigation (`examples/quantum/quantum_classical_check.md`, deleted on 2026-09-17)
ran on `be518fe1089457032b201324372201086e1edbcf` with experiment-only additions;
production source was unchanged. Its source fingerprint, exact numerical
results and limitations are recorded in that report. The aggregate completed
in 3.88 seconds: ten native interference worlds, sixteen coherent-environment
controls, the existing five-cycle Markov comparison and three 96-tick spatial
contact controls. Numerical expectations pass; emergence of a Newtonian
trajectory is **not established**. Independent review checked the saved native
weights, fixed timing and the distinction between configured hold and emergence.

`python tools/check.py --base be518fe1089457032b201324372201086e1edbcf` passed
**106 tests with two opt-in visual skips** in 27.72 seconds. Ruff and formatting
passed for six changed Python files. The affected scope includes the new
headless CLI experiment, resource-consumer selection and repository language,
hygiene, navigation, workspace and recorded-output contracts. Production source
and its prior physics evidence are unchanged; no full-suite run, package build
or visualization was requested. Python 3.14.7, pytest 9.1.1 and Ruff 0.16.7 were
used with a fresh explicit Windows pytest base directory.

## Recurrent local contact outcomes - 2026-09-14

Recorded task base: `3e5eaea5ad88688b2509ec34f5d43246dc62d15e`. The branch then
fast-forwarded to `31915ae805a18a125483fb92ef36ad81062d691f`; that main update only
changes citation/README text. The tested active source SHA-256 remains
`cddaff84568049b2c7fdf88355476a9e57657440052bf944b93874a1bb39cd95`.

The mandatory affected gate passed **2,297 tests with five opt-in visual skips**
in 174.86 seconds. Ruff and formatting passed for 14 changed Python files;
strict mypy passed for 71 affected source files. Sixteen new recurrent tests are
included. Shared NodeState and resolver changes select carrier/field/quantum,
locality, boundaries, headless output and retention consumers. No full-suite flag,
package build or visualization was used. Interpreter/tool versions remain
Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1. Windows tests used a fresh
explicit `PYTEST_ADDOPTS=--basetemp=...` path because the default temp root has an
existing enumeration-permission failure.

After the citation-only main update and final documentation edits, all 28
repository language, hygiene and navigation checks passed. The Windows checkout
has mixed checkout line endings; Git's source archive differs only by CRLF/LF
encoding. Every archived source file was compared with the tested source after
newline normalization. An additional actual run from the exact staged Git source
archive completed 48 ticks in 0.1714972 seconds, with source SHA-256
`141d41edc8854adad5f5c1d64ed4db7be6cfd3f11ed99041b84646204b90e5f6`.
Its event files, state, input, model costs and accounting exactly match the first
run; only source byte identity and elapsed host time differ. The second run's
outputs retain the ordinary 24-hour registration. Automatic approval review
blocked removal of the disposable source snapshot; it remains outside Git at
`artifacts/recurrent-index-source-0914` and is not enrolled for automatic cleanup
because the retention guard protects source directories.

Main subsequently advanced to `1c782390456ea9629eb0f73c030095574d80e454` with the
catalog-contact authoring example. Integration preserves both resource-consumer
registrations and selector tests; production source fingerprints are unchanged.
The additional affected gate, `python tools/check.py --base 1c04760194b8dd60c24305620450608dfae30893`,
passed **382 tests with two opt-in visual skips** in 67.32 seconds, including all
39 catalog-contact cases. Ruff and formatting on its four affected Python files
passed. The earlier production/physics evidence remains applicable.

```sh
python tools/check.py --base 3e5eaea5ad88688b2509ec34f5d43246dc62d15e
python -m event_universe --init examples/quantum/repeated_contacts.json --output artifacts/repeated-contacts-0914-verified
```

The actual primary-runner example completed **48/48 ticks in 0.1671985 seconds**
with `display=none`, eight random draws and reported model cost 7,632. Its input
SHA-256 is `f73311793174e383d3dcd513e875d10fba40820cf2744706df79f15afa627c3e`.
The event sequence (`examples/quantum/repeated_contacts.md`, deleted on 2026-09-17) has new-wave results
at ticks 3, 9 and 21, continuation at 6/12/15/18 and localization at 24. Charge -1
and mass 1 retain one owner at every tick. Ordinary injection -36 and dissipation
-36 leave zero final field stock, with every-tick accounting balanced. Saved
metadata, causal events and final state were inspected; generated files stay
outside Git under the runner's 24-hour retention registration.

Independent physics review supplied three passing counterexamples: remote
generation changes cannot choose a local null's ordinary emitter before a causal
notice arrives; a resolved new-wave result cannot be replayed into another
origin; source preparation requires complete-domain vacuum, not just local
vacuum. Exhaustive instruments independently yield source counts 9/16 out of 25
and capture counts 9/16/144 out of 169. A renamed configuration with an additional
signed conserved vector and alternate localized output retains the same events,
inventory and finite emission. Existing one-shot, conditional-state, origin and
field regressions pass on this source.

The implementation contract, postulates, definitions, architecture, restart guide,
Highlights map and numerical expectations accompany the code. The physics-review
Skill gains the demonstrated remote-generation/replay checks; the configuration
Skill routes complete instruments and finite capacities. Boss, field-development
and architecture-review were reviewed: their existing ownership and evidence
rules cover this extension, so no duplicate workflow was added. The scope remains
finite supplied one-excitation domains and retarded ordinary sources, not a
derived Hamiltonian, reciprocal field action or physical energy/momentum closure.

## Null notices and field-dependent phase - 2026-09-14

Base: `1c782390456ea9629eb0f73c030095574d80e454` (main after PR #99), on top of
the interference harness below. Runtime source fingerprint of the executed
harness: `fcd527461961e59fd1295547db9318716245303b7384aa15612a4d7ca23f387a`.
Two opt-in extensions of `causal-contact-fields-v1` were added, both inactive
without their configuration keys: null notices (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17)
and the field-dependent phase (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17).
The envelope output bank grew from twelve to eighteen fixed slots; the
NodeState contract fixture was widened accordingly and no other test changed.

Recorded on the interference harness: after an arm null at tick 1 with notices
enabled, the source emits 25 of 25 units from tick 2, the next gate emits 9 and
16, and every scale ends at 625/81; an output null at tick 7 reaches the source
at tick 9 with scale 625/337. With a field phase on the M arm, coil fields 0,
200, 400 and 800 select exponents 0, 0, 1 and 2 and record output weights
`[12745, 2880]` and `[160225, 230400]`, equal to the independent Gaussian-integer
prediction; a coil beside the far side of the source selects exponent 0.

```sh
python tools/check.py --base 1c782390456ea9629eb0f73c030095574d80e454
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The affected gate passed: **2,348 passed and five visual-only skipped**, with
seven setup errors in `test_maxwell_configuration.py` and `test_run_live.py`
that came from a missing render extra; after installing `.[render]` those two
files passed (14 passed, two skipped). Ruff, formatting and strict mypy passed
with no issues on 118 source files. Python 3.14.0rc2 on Linux. These are
measured behaviors of configured candidates; no classical limit, energy closure
or multi-excitation Born consistency is established.

## Two-arm interference and coupling summary - 2026-09-14

Base: `1c782390456ea9629eb0f73c030095574d80e454` (main after PR #99). Runtime
source fingerprint of the executed harness:
`4916707db38c4f364552a24a727678698912f509a27969c4217ca02005ca6cf6`. No source
module under `src/` changed; the addition is an experiment harness, its
acceptance test, a reader-facing coupling summary and index updates.

The interference harness (`examples/quantum/causal_interference.md`, deleted on 2026-09-17) ran
thirteen headless 14-tick worlds on the unchanged `causal-contact-fields-v1`
profile. Recorded output decision weights were `[337, 288]`, `[49, 576]` and
`[337, 288]` for `phi = pi/2, pi, 3pi/2`, with no uncertain decision at
`phi = 0`; all equal the exact rational prediction computed before the runs.
Mean source emission after recombination was 25, 13.5, 2 and 13.5 units per
tick against 25, 13.48, 1.96 and 13.48 predicted. The arm-detector variant gave
`[9, 16]` at tick 1 for every phase and no uncertain output decision. After an
arm null the source Node emitted 9 of 25 units per tick: the retarded-source
rule measured. Every run reported balanced accounting and conserved totals.

```sh
python tools/check.py --base 1c782390456ea9629eb0f73c030095574d80e454
PYTHONPATH=src python examples/quantum/causal_interference.py --output artifacts/causal-interference
```

The affected gate passed: **101 passed, two visual-only skipped**, including
repository navigation, language and hygiene checks. Ruff and formatting passed.
Python 3.14.0rc2 on Linux. This records a measured behavior of a configured
candidate; it does not establish a classical limit, field back-action or
energy closure, as stated in the coupling summary (`docs/QUANTUM_CLASSICAL_COUPLING.md`, deleted on 2026-09-17).

## Causal quantum source envelopes - 2026-09-13

Recorded change base: `d8261d4d239e524d18011166f6372ec2949cbe42`; integrated
main remains `523b39804e8be78ec2069b7af8b6498ccb19810a` after a fresh fetch.
Final active source SHA-256:
`1ac603cc9fb6bc34967dcd1b9c4dc6c6e08680229e6e6ed7527f8d4dbf432aaa`.
The affected gate passed **2,273 tests with five opt-in visual skips** in
154.64 seconds. Ruff and formatting on 24 changed Python files and strict mypy
on 69 affected production modules passed. Shared NodeState and resolver interfaces
select the carrier, field, quantum, locality, boundaries, headless-output and
retention consumers. No full-suite flag or package build was used.

```sh
python tools/check.py --base d8261d4d239e524d18011166f6372ec2949cbe42
python -m event_universe --init examples/quantum/causal_charge.json --output artifacts/causal-charge-final-verified
python -m event_universe --init examples/quantum/localized_charge.json --output artifacts/causal-localized-final-verified
python -m event_universe --init examples/quantum/wave_origins.json --output artifacts/causal-origins-final-verified
```

Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1 were used. Windows'
existing default pytest temporary root denied directory enumeration; the successful
gate sets `PYTEST_ADDOPTS` to a fresh explicit workspace `--basetemp`.
Two initial type annotation failures were corrected before the successful gate.

The new arithmetic, integration and atomic-publication modules contribute 59
focused cases, all included above. A 3:4 split emits -9 and -16 from configured
full strength -25; inverse propagation recombines the complex amplitudes. Tests
cover finite fractional allowances, low-budget source deposits, every periodic
seam and both Port choices on length-two axes, immutable frozen gate inputs,
local null versus capture, delayed terminal handling, generic label substitution,
formula-free NodeState and rejection before sampling or changing inventory.
Observers see the deposited field stock and consumed emission allowance together.
Two terminal regressions added after that gate passed separately: duplicate
notices charge receive/read work without restarting termination, and a terminal
commit before a later valid amplitude prevents reactivation. Thus all 61 new
focused cases have passing evidence; these last two are not included in 2,273.

Independent physics review passed those 59 cases and confirmed the final source
after preserving the two existing engine files' line endings. Its separate
five-Link comparison captured remotely at tick 9: the distant ordinary envelope
remained 3/5, with the same finite allowance as the detector-free control, through
tick 13. The terminal notice retired it at tick 14. A null outcome did not
renormalize that distant source. The ordinary source never queried quantum
probabilities or used shared origin retirement to change its remote state.

The checked-in causal example completed **10/10 ticks in 0.0884438 seconds**,
with `display=none`, one random draw and total reported model cost 1,555.
Source preparation commits at tick 0 and successful absorption at tick 3.
All three local envelopes retire by tick 5. Charge -1 and mass 1 retain one
owner at every completed tick. Cumulative ordinary field injection is
`[-25, -50, -75, -100, -134, -159, -159, -159, -159, -159]`.
Its configured localization residue retains the final -159 field quantity;
there is no global erasure of previously emitted stock. Source, residue,
dissipation and escape accounting balances at every tick.

On the same source, the unchanged localized-only example completed **8/8 ticks
in 0.0267102 seconds**, retaining field injection -18 and model cost 268.
The existing origin example completed **5/5 ticks in 0.0078832 seconds**, retaining
one random draw and model cost 17. All three actual runner outputs are headless,
excluded from Git and enrolled in 24-hour retention.

The causal source contract (`docs/CAUSAL_QUANTUM_SOURCES.md`, deleted on 2026-09-17), postulates, definitions,
architecture, Highlights coverage, examples, test expectations and physics-review
Skill are updated together. The example now has an explicit affected-test mapping.
Existing Boss and test-runner instructions already cover the required coordination
and validation; no extra scheduled task was added. Live Highlights was reconciled
read-only. After measurement, the ordinary envelope is an explicitly retarded,
potentially unnormalized approximation, not a globally conditioned Born query.
Already started gates retain both frozen operands across null results and can
subsequently repopulate a local source. This candidate does not establish QED,
field/matter energy closure, shared aggregate CPU contention or a universal
classical limit.

## Localized contact, quantum propagation and classical fields - 2026-09-13

Integrated base: `523b39804e8be78ec2069b7af8b6498ccb19810a`. Implementation
commit `8cd2156` and integration commit `b459a45` have active source SHA-256
`fc69868e9e282e7c157258f8a454653e095fa366f077dab403652c58009effca`.
The affected gate passed **2,195 tests with seven opt-in visual skips** in
147.94 seconds. Ruff, formatting on 23 changed Python files and strict mypy on
63 affected production modules passed. The scope includes contact conversion,
quantum origins, ordinary fields, movement, boundaries, locality, genericity,
interfaces, headless output and retention. Python 3.14.7, pytest 9.1.1,
Ruff 0.16.7 and mypy 2.3.1 were used; no full-suite flag or package build was used.

```sh
python tools/check.py --base origin/main
python -m event_universe --init examples/quantum/localized_charge.json --output artifacts/localized-contact-final
python -m event_universe --init examples/quantum/wave_origins.json --output artifacts/wave-origins-contact-regression
```

The 51 focused contact cases are included in the gate. They check committed
ownership transfer, valid zero versus undefined momentum, null/click instruments,
finite classical sources, delayed cycles, Link timing, all six periodic seams,
split/recombination, exhaustive capture tickets, label substitution and rejection
before drawing. A third coupled resident retains its quantity and the common
field reaction in every capture alternative. Public concurrent readouts cannot
observe a half-completed ordinary/quantum transfer. A moving disturbance creates
no origin before arrival; its actual source and capture events occur at ticks 1
and 4. A legacy capacity-boundary regression was corrected by restricting early
preflight to the contact profile; the original legacy test remains unchanged.

Independent physics review passed 50 focused cases and a separate moving-arrival
probe, then reviewed the final delta at `b459a45` and passed both targeted checks.
The later source changes add the public read lock, scope the early preflight and
retain the moving-arrival regression. Merged main's quantum changes clarify
terminology without changing physical behavior. The final affected gate above
covers the complete integrated source.

The localized example completed **8/8 ticks in 0.0245987 seconds**, with
`display=none`. Source conversion occurs at tick 0 and capture two Links away at
tick 2. Charge -1 and mass 1 are conserved at every completed tick, including the
quantum inventory exactly once. Classical source injection is -6 before conversion
and -12 after capture; it is zero during the delocalized interval. The final -18
field quantity is localized residue under the selected schema-2 field law, with
zero escaped or dissipated quantity. Source accounting balances at every tick;
it is not an equality between charge and field energy. The deterministic example
uses no random draws and records total model cost 268, including carrier cost 246.

The existing origin example completed **5/5 ticks in 0.0074054 seconds** on the
same source, preserving one random draw and three oracle calls. Origin 3 resolves
to record 13 at tick 2; origin 4 remains active. Both runs are headless and their
generated outputs remain outside Git under the 24-hour retention policy.

The contact contract (`docs/LOCALIZED_QUANTUM_CONTACT.md`, deleted on 2026-09-17), postulates, definitions,
architecture, test expectations and Highlights coverage describe the same finite
hybrid model. The physics-review Skill now requires commit-time ownership,
complete alternative validation and explicit field-source accounting. Boss,
architecture and test-runner Skills already cover the necessary workflow and
need no additional role or procedure. Live Highlights was reconciled read-only.
This candidate does not derive QED, a physical momentum observable, field/matter
energy conservation or a universal classical limit. Optional playback references
are conservative support, not localized charge or probability; no visualization
was generated or visually inspected.

## Quantum origin cells and certified cancellation - 2026-09-13

The final submission integrates main `cc042ce6c51a34775c292371538c5cd6acd4e423`
(straight-ray fields). Final active source SHA-256:
`9d561027fce33c2c63a73cd003c84f3cd4bc988933177755f8e1598869c400e8`.
The resulting affected gate passed **2,141 tests with five opt-in visual skips**
in 158.74 seconds; Ruff/format and strict mypy on 60 affected source modules
passed. This includes the native cancellation tests and new ray-field consumers.
The ordinary runner again completed 5/5 ticks, in 0.0123118 seconds, with the
same one draw, 23 events and model cost 17. Its output is
`artifacts/wave-origins-integrated`, with headless display and 24-hour retention.

Independent integration review confirmed that the quantum/origin/event/runtime
files are unchanged, the Node audit supports both origin references and rays,
and native v3 still rejects independent spatial fields. No unsupported quantum
and ray-field composition was introduced by the merge.

### Initial implementation checks

Base: `2c20d00094639263fbe387c0a62420dcef108285`. Validated active source SHA-256:
`25be12915099c34f027563bb6844bf0dcf99299787fad1ba1b7e5dd9460b4ed2`.
The affected gate passed **2,114 tests with five opt-in visual skips** in
159.43 seconds. Five additional native cancellation regressions added after
selection passed separately in 0.32 seconds. Ruff, formatting and strict mypy
on 59 affected production modules passed. The final documentation, navigation,
language and hygiene checks passed all 28 cases in 16.46 seconds. Python 3.14.7,
pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1 were used.
The shared NodeState/event interfaces select broad carrier, field, boundary,
locality, genericity, retention and quantum consumers; no `--full`, package build
or visualization was requested.

```sh
python tools/check.py --base origin/main
python -m pytest tests/test_native_wave_cancellation.py
python -m event_universe --init examples/quantum/wave_origins.json --output artifacts/wave-origins-verified
```

The new origin tests exercise six-entry Node banks, a rejected seventh arrival,
simultaneous one-Link propagation, concurrent first claims, both detector orders,
conditional Born weights, phase reversal, exact checkpoints, continuing outcomes
and next-tick retirement. Direct status lookup needs no historical traversal.
The separate chronological predecessor list and its traversal API are removed;
immutable events, causal dependencies and current register heads remain.

Independent physics review passed 45 focused tests in 0.59 seconds on the exact
source above. It also independently reproduced target-head invalidation of a
cached null certificate. The initial proposal could suppress a remote X gate or
an observable instrument through shared retirement status. The final code rejects
that composition: a skipped gate must preserve the complete joint density; a
skipped instrument must have only its declared null outcome, also preserving that
density. Tests include phase changes invisible in local marginals and random
records from an unchanged unobserved channel. Quantum certification is extra
bounded host work; only the origin relevance lookup is O(1).

The ordinary runner completed 5/5 ticks in 0.0072459 seconds, with `display=none`.
The saved initialization matches the checked-in example. Origin 3 resolves to
record 13 at tick 2; other Nodes remove its reference at tick 3. Origin 4 remains
active. The final report has one random draw, three oracle calls including two
cancellation certifications, 23 causal events, total model cost 17 and carrier
cost zero. The configured terminal instrument resets occupation to vacuum;
the continuing test variant explicitly uses a position instrument. This finite
candidate does not derive a physical momentum observable, generic absorption
exchange, a universal classical limit or unrestricted no-signalling.

The origin contract (`docs/WAVE_ORIGINS.md`, deleted on 2026-09-17), postulates, definitions, Highlights coverage
and physics-review Skill describe the same supported scope and rejection paths.
Boss and test-runner instructions already cover bounded ownership and proportional
verification. Generated outputs and validation logs remain outside source commits
and are enrolled in 24-hour retention.

## Linked quantum histories on native Nodes - 2026-09-13

Base: `5a2e21d892eba82c5aaff0582152e79f94c0fdc5`. Active source SHA-256:
`4eff11aa7181a6c0105ded591467d9205f92a797cc8346d1ce76c2c92fbbdeb9`.
The affected gate passed **2,019 tests with five explicitly visual skips** in
138 seconds, with Ruff and strict mypy on 58 affected production modules.
The selection includes ordinary carrier/field, native quantum, NodeState,
locality, genericity, boundary, retention and interface consumers; no full-suite
flag, package build or rendering was used.

```sh
python tools/check.py --base origin/main --tests tests/test_quantum_linked_nodes.py tests/test_native_event_runtime.py tests/test_native_quantum_channels.py
python -m event_universe --init examples/quantum/linked_paths.json --output artifacts/linked-paths-verified
```

Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1 were used. On Windows,
the gate used a short external temporary path with forward slashes in
`PYTEST_ADDOPTS`. An earlier backslash-only value was parsed as a relative path,
putting generated fixtures inside the repository and exceeding Windows path
limits. That run had 14 environment/hygiene failures; moving those fixtures out
and correcting the invocation produced the complete pass without a source fix.
The existing tracked CRLF in `disturbance_engine.py` is preserved; Git whitespace
validation uses `core.whitespace=cr-at-eol` rather than rewriting the whole file.

The new 28 focused cases cover local predecessor histories, immutable snapshots,
split/join interference, both recorded outcomes, complex phases, exact correlated
checkpoints, distinct colocated registers, fixed cursor size and atomic failures.
An independent reviewer passed 110 relevant tests, then confirmed that the only
later source adjustment was a local type annotation and formatting. The reviewed
contract and final fingerprint are unchanged in behavior. The original timing
defect was independently reproduced: a tick-1 checkpoint incorrectly rejected
a valid tick-2 operation across a two-tick Link. The corrected cursor keeps its
last modeled time, including distinct times within one checkpointed component.

The ordinary headless run completed 4/4 ticks in 0.005711 seconds on the exact
source above. Saved initialization equals the checked-in JSON byte for byte;
display is `none`. Its eight causal records finish with heads `(5, 6, 7, 7)`.
The output retains each stream's predecessor separately. No carrier sources,
ordinary cycles or model costs are invented for empty quantum-only Nodes.
Independent test readouts give final C/D probabilities 0/1, 1/0 after a phase
reversal, and 1/2 each after either intermediate position outcome. Every case
is repeated with and without compaction. These are configured finite-register
laws, not a derivation of quantum field dynamics or the classical limit.

The physics-review Skill now links to the checkpoint/readiness contract;
`quick_validate.py` passed using the existing isolated PyYAML 6.0.3 dependency.
Boss, architecture and test-runner instructions already cover ownership,
independent expectations and proportional checks; no extra role or Skill is
needed. Live Highlights reconciliation is recorded in
the coverage map.
Generated artifacts stay outside source commits and retain their 24-hour leases.

## Joint reactions and delayed rule validity - 2026-09-13

Incremental base: `a7a0000e3005ae41b37639f5dcf76e56532be69f`, continuing PR 86
on main `bb177121ec2efdc6c998a8290b9e7b09c7706c62`. Final active source SHA-256:
`1c85d9200fc57378c971fc7409532555713be04916139027eb9c08439cc918c8`.
The rule contract separates indexed
participant/field proposals, consumed triggers and persistent conditions.
The final affected gate passed: **1,879 tests passed and five visual-only tests
were skipped**. Ruff, formatting and strict mypy (55 affected modules) passed.
The final documentation checks also passed (28 cases).

The focused regressions include 23 parser cases, 16 joint-reaction cases and
21 field-guard cases. The independent reviewer ran 85 related cases before the
final read-only audit registration, then all 10 NodeState checks afterward.
The declaration audit initially rejected the new `FieldRuleGuard` owner. It now
recursively audits that record; a negative test rejects a hidden expression in
its outgoing metadata. The check was extended, not bypassed.

```sh
python tools/check.py --base a7a0000e3005ae41b37639f5dcf76e56532be69f
python -m event_universe --init examples/node-vector/joint-reaction.json --output artifacts/joint-reaction-final-run
python tools/profile_node_vectors.py . artifacts/joint-reaction-memory/report.json reactions
```

Python: 3.14.7. The first gate hit access-denied errors in the existing Windows
pytest temporary root. The final gate uses a fresh external temporary directory
and cache through `PYTEST_ADDOPTS`; no test or engine behavior is changed to
work around filesystem permissions. Both modified Skills passed `quick_validate.py`
using a separate PyYAML 6.0.3 validation dependency directory.

The final headless run completed 8/8 ticks on the final source, with commits at
ticks 3 and 7. Saved initialization matches the checked-in configuration. Both
spatial ledgers balance; externally defined squared-length and vector-sum
readouts remain 34 and (4, 6, 2). Final carriers are (0, 2, 0) and (1, 0, 0);
the local fields are (0, 0, 2) and (3, 4, 0). This is a supplied register
permutation, not a derivation of physical energy or particle interactions.

All five host-memory cases used source
`44640835b60c5623fdc0104b3a95f927b1a1fd7856e3d52dce0c3af5d7ac2342`.
The only subsequent production change registers `FieldRuleGuard` with the
read-only NodeState auditor; reconstructing that file's earlier bytes reproduces
the measured source hash exactly. No evolving-state or stepping code changed.
The joint owner graph remains constant at ticks 16/32/64/128/256:

| Nodes | Reachable owner graph bytes |
| --- | ---: |
| 1 | 5,908 |
| 8 | 40,068 |
| 27 | 132,712 |

The field-rule probes measured 6,892 bytes for one Node and 48,248 to 48,444
bytes for eight Nodes; the latter change reflects Python integer object sharing
at later clock values. The largest traced interval peak was 485,116 bytes.
These are reachable Python allocations and tracemalloc observations, excluding
native allocator/RSS coverage. Pending rule metadata is bounded by configured
rules, slots, components and six outputs. Host indexes still scale with visited
Nodes; no whole-world O(1) or speedup claim follows.

The established joint reaction delta limit is unchanged: an extreme endpoint
swap can fail if the transfer itself exceeds `MAX_VALUE`, even when each
endpoint fits. Failure is explicit. Physics-validation and regression Skills
now cover delayed substep checks; Boss and architecture Skills already route
this work correctly, so no new Skill or scheduler was introduced.

## Guarded integer Node execution - 2026-09-13

Base: `bb177121ec2efdc6c998a8290b9e7b09c7706c62`. Tested active source SHA-256:
`68cec05fc6463e4ef2ced0f1d0d2ff1b63de4d1cb30b6b011424e26245bebf9f`.
The Node contract defines the supported scope and
separates imposed constraints from unestablished physical emergence.

The dependency-selected gate completed with **1,814 passed and five visual-only
skips**. Ruff, formatting and strict mypy passed. The default package import
regression initially caught an eagerly loaded diagnostic module; the report now
loads it only when requested, and the final gate passes that original assertion.

```sh
python tools/check.py --base bb177121ec2efdc6c998a8290b9e7b09c7706c62
```

Python was 3.14.7. Coverage includes existing carrier/spatial/causal/quantum
regressions, locality and formula-free state, bounded indexed rules, generic
renaming, k timing, zero/canceling arrivals, pending field deltas and paired
reactions. The new pre-commit guard tests reject nonlinear merging and changes
to momentum or charge without changing actual owners or accounting. Constructor
and direct-service tests prevent silently omitting the mandatory guard.
Known initial readout overflow is rejected in preflight without constructing a
world or creating output. Failed diagnostic projection reports an explicit error
and no partial values. Named host totals include actual owners once and do not
apply the local capacity limit to an entire multi-Node world.

Two ordinary headless CLI runs each completed eight requested ticks on that
source. `six-records.json` (input SHA-256
`12d3464890ff80df034aa5ea4bcead6fbef31a2ff916c06789b5f18fedc9ae2e`)
committed at ticks 3 and 7 and retained declared E=21, P=(3,0,0), Q=0,
J=(0,15,0). `two-fields.json` (input SHA-256
`faf174035d96cc66d2382dc600cc2c06131087cb50dfddad9d4d42d8e6b38605`)
performed the paired exchange at tick 2 and retained E=7 and zero P/Q/J.
Run metadata and event logs were inspected; display was `none`.
These are externally defined register readouts and permutation/exchange laws,
not derived electromagnetic or quantum dynamics.

### Memory and architecture

The reproducible host probe is profile_node_vectors.py:

```sh
python tools/profile_node_vectors.py . artifacts/node-vector-memory/report.json
```

Use `PYTHONPATH=src` and a new output file. It records source/configuration identity,
plain stepping time, traced peaks and unique reachable owner allocations for
nine fixed-degree cases through 256 ticks. On the tested source, carrier owner
graphs at equivalent cycle checkpoints remained unchanged from tick 16 to 256:

| Nodes | Components | Slots per Node | Retained owner bytes |
| ---: | ---: | ---: | ---: |
| 1 | 8 | 8 | 3,680 |
| 8 | 8 | 8 | 24,008 |
| 27 | 8 | 8 | 79,184 |
| 8 | 16 | 8 | 27,144 |
| 8 | 32 | 8 | 33,416 |
| 8 | 8 | 16 | 27,592 |
| 8 | 8 | 32 | 34,760 |

Eight colocated carrier/field Nodes retained 48,444 bytes at tick 256. Their
196-byte rise from tick 128 reflects seven additional 28-byte Python integer
objects after clock values leave the shared small-integer cache. A separate
1,024-tick follow-up on source `785c9ec2b01b7caf8756906eb24075f067fa73f2f88e9b6f248b9150a4c9081e`
held exactly 48,444 bytes at ticks 256, 512 and 1,024; that earlier source precedes
the final initial-readout and receipt-bound checks and is identified separately.

The largest final-source measured interval peak was 363,444 traced bytes.
Measurements exclude native allocator/RSS, configuration allocation before tracing,
observers and recorded history. Shared Python objects are counted once; these
numbers are not physical register counts. Timing is a single host sample and
tracing adds substantial overhead; no simulation speedup is claimed.

State and output capacity are fixed per Node, and shared definitions/services are
outside evolving Node payloads. However, the host retains maps and port banks for
all visited positions. Whole-host memory therefore scales with visited Nodes,
not just currently active Nodes. Repeated sorting and immutable temporary tuples
also remain runtime costs. The fixed-Node probes do not establish bounded memory
for unbounded exploration or generic graph/coarse-graining support.

### Review and workflow

Independent reviews checked schema/aggregation, local clock/field ownership,
nonlinear balances, API bypasses, and current-value reporting. Review findings
were fixed with retained regressions: nonadditive spatial ownership rejection,
unrelated-field merge eligibility, received-mask consumption, missing guards and
initial-readout overflow. The regression Skill now links the Node contract and
the focused checks; its frontmatter validator passed using existing local
validation dependencies. Other reviewed Skills already express the needed
architecture and physical-evidence boundaries. No schedule or live Highlights
document was changed. The [Highlights map](HIGHLIGHTS_IMPLEMENTATION.md) records
the explicit user clarification of h and k.

## Property-selected couplings and passive local conservation - 2026-09-13

Base: `ed65f829a6ddc797cafec1bf34156ca59bdcb7dd`. The
property contract covers all supported single-carrier
and pair selectors, shared property ownership, overlapping matches and sequential
drivers. The audit contract measures configured energy
and all three momentum components from committed owners and actual link flux.
Independent physics review passed this declared additive-owner scope; it does
not establish physical quantity identification or universal field laws.

The ordinary entities CLI compiled electron, positron and electron-neutrino
bindings from `examples/known-entities/property-coupling-probes.json`. Canonical
preflight returned valid, then the ordinary headless runner completed four ticks.
Run metadata recorded source SHA-256
`9b268934fcd4f11e5852778ce628626d0d40b3bc29f239ae4e8945ac31054dc2`
and initialization SHA-256
`faf0f6c3883396095d16c8d0fe52750d3638936bd1e2f552013587b32cb4fd4d`.
Six node audits passed: combined energy remained 14, momentum remained (0, 0, 0),
and escaped energy/momentum were zero. Two finite local reservoirs transferred
to both charged carriers; the neutral control remained unchanged. These are
explicit supplied inventory probes, not derived electromagnetic dynamics.

The final affected gate completed with 1,656 passed and five visual-only skips:

```sh
python tools/check.py --base ed65f829a6ddc797cafec1bf34156ca59bdcb7dd
```

Ruff and strict mypy passed. Tools: Python 3.14.7, pytest 9.1.1, Ruff 0.16.7
and mypy 2.3.1. This was dependency-selected validation, not `--full` or visual
validation. Regression coverage includes missing properties versus zero values,
shared drivers, delayed commits, open-boundary flux, nonlinear packet merging,
late ordinary updates, each momentum component, passive audit timing, and UI
renames. Deliberate conservation failures preserve the offending state and saved
failure report. Independent review also checked the earlier coupled-excitation
candidate and its rejected packet-overlap case.

Native reflection cost changes from 135 to 121 because two seven-operation
invariant evaluations no longer add physical work; transmission remains 116.
The physical operation difference is still five, and the established outcome,
probability and causal safety assertions remain in the regression suites.

Architecture, field-development, physics-rule-validation and configuration Skills
now link the property/audit contracts and require passive measurement with
explicit quantity assumptions. Boss and PR-review Skills were reviewed; their
existing routing and merge requirements remain sufficient. Skill frontmatter
is unchanged; repository language and link checks passed. The live Highlights
revision is reconciled in its [coverage map](HIGHLIGHTS_IMPLEMENTATION.md), without
editing the live document. The PR records the submitted head/tree and final CI.

## Coupled unit-excitation candidate - 2026-09-13

Base: `6a2816526083c23069bf3b0f3fcb6a9dc5b17944`.
The candidate contract uses saved initialization rules,
with no changes under `src/` or to the physical reference catalog. Independent
physics review checked local ownership, elementary state generation, fixed
bounds, live delayed-commit guards and the explicit single-packet envelope.
The review found and closed an emission/input-overlap hole in the authoring check.

Four ordinary headless CLI runs completed: `incoming_positive`, `incoming_zero`
and `emission` for 8 ticks each; `delayed` for 30 ticks. Each ran canonical
configuration preflight first. Saved input bytes matched the prepared cases,
and every run recorded source SHA-256
`7dac1815abbdcbbd78f1ab175901bc04d9280d76a570eb2d9458032417ed1378`.
Final internal/recoil values were Y/+X for both absorption runs, zero/zero for
zero coupling, and zero/-X with spatial -Y for emission. Ordinary spatial
accounting was balanced. The independent tests additionally check the candidate's
nonlinear U/P at each tick; the ordinary runner's empty conserved-field totals
are not evidence of those nonlinear balances.

The incoming packet reached the receiver at audit tick 2. Immediate absorption
committed at that same audit tick, after receipt; its changed state is visible
in the post-step snapshot labeled tick 3. Delayed absorption committed at tick 7.
Emission committed at audit tick 0, sent at tick 1 and arrived at tick 2. These are
world/event audit times, distinct from local observer counters and playback.
Generated outputs use the existing 24-hour retention contract; the saved law,
cases, tests and commands reproduce the evidence after output expiry.

All 38 focused candidate cases passed, including CLI preparation and overwrite
protection. The affected gate uses the recorded base plus the existing local-field
and spatial transaction suites for regression:

```sh
python tools/check.py --base 6a2816526083c23069bf3b0f3fcb6a9dc5b17944 --tests tests/test_local_field_rules.py tests/test_spatial_interactions.py
```
 The PR records the exact final count,
head/tree and CI result. Tools: Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and
mypy 2.3.1. No full-suite or visual audit is claimed. Boss, configuration, runner,
field-development, architecture, physics, test, regression and merge Skills were
reviewed: their existing scope, hypothesis and event-time rules remain sufficient;
new technical knowledge is linked through this candidate's contract and maps.

## Read-only configuration preflight - 2026-09-13

Base: `521b63567d186bab2fac982a1e1f9d0a592a73a5`. The
validation architecture gives strict JSON decoding
one owner and delegates each format to its existing semantic validator. The UI
and runner share initialization/observer preparation. It introduces no physical
formula, inferred law, catalog measurement conversion or simulation during a check.

The 102 facade tests cover all 38 shipped initializations, explicit dependencies,
unsupported authoring formats, observer composition, no world/filesystem effects,
reports, CLI batches and shared UI/runner rejection. The shipped profiles return
46 classical and 46 quantum successes. Profile tests retain independent validation
of unselected rows, subset/single-representation support and input immutability.
Strict JSON tests cover nonfinite constants, exponent overflow, duplicate decoded
keys, scalar editor fragments, finite numbers and consistent byte decoding.
Native tests cover initial event requirements at and below the exact capacity;
the insufficient two-cell case failed before the parser correction.

Independent review found decoder and semantic recursion errors that escaped the
report boundary. Regression tests now check contextual invalid reports, UI
rejection and continuation to the next CLI file. Existing runtime, native-event,
workspace, field, accounting and output regressions remain in the affected scope.
The broad regression also caught a sidecar being read before an inline/external
conflict was rejected. The shared selection check now runs before sidecar I/O;
the existing missing-file regression and a read-forbidding test retain that order.
The first CI run exposed two tests that assumed Windows decoder stack depth.
Linux decoded the same nested array and correctly rejected its format. The real
input tests now assert rejection, attribution and batch continuation regardless
of which valid rejection happens first. Separate bounded-decoder replacement
tests require syntax reports for input, catalog and initialization dependencies.
Static success does not guarantee future capacities or physical acceptance.

Validation command:
`python tools/check.py --base 521b63567d186bab2fac982a1e1f9d0a592a73a5`.
The PR records the final selected count and CI result for the submitted head.
Tools: Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1. Validation is
headless and affected; no unrelated full-suite or visual audit is claimed.

The simulation-configuration, simulation-runner, architecture-review and
test-runner Skills now link one maintained preflight contract and distinguish
configuration validity, completed execution and physical acceptance. All four
pass Skill Creator's quick validator (PyYAML 6.0.3 in temporary tooling only).
Boss and PR-review Skills were reviewed; their existing routing and merge rules
remain sufficient, so no additional Skill or orchestration layer was created.
The live Highlights revision is reconciled in its
[coverage map](HIGHLIGHTS_IMPLEMENTATION.md); the live document was not changed.

## Descriptive physical catalog and explicit profiles — 2026-09-12

Base: `98b774ac3b02aa5cd350d5513b1e1fddbe3a2c81`. The version 2
physical reference adds sourced properties and possible
channels without introducing runtime laws. All 46 original classical/quantum
profile pairs were extracted unchanged into `representation-probes.json`.

An independent baseline worktree produced all 92 compiled configurations and
three 12-tick worlds: a charged conjugate pair with the electromagnetic field,
the four-component Higgs field probe, and the finite quantum pair/field
preparation. The new compiler produces identical configurations, all 39 complete
snapshots, every event, computation report and spatial accounting record.
This checks behavior preservation, not the physical validity of those probes.

Reference tests compare the declared PDG 2025 values, conventions and statuses;
structural checks cover citations, units, aliases, reciprocal links, reaction
charge balance and rejected executable content. The affected gate is
`python tools/check.py --base 98b774ac3b02aa5cd350d5513b1e1fddbe3a2c81`.
The PR records its final count and CI result for the submitted head. Validation
uses Python 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1. Runs are headless;
no unrelated full-suite audit or visual verification is claimed.

The simulation-configuration guide now requires explicit experiment profiles and
keeps reference measurements outside runtime laws. Boss, architecture, physics
review and PR-review Skills already cover these boundaries; no additional Skill
or workflow is needed. The Highlights revision and reconciliation are recorded
in its [versioned companion](HIGHLIGHTS_IMPLEMENTATION.md); the live document
was read, not changed.

Each record applies to its identified source and configuration, not all future
checkouts. Original paths and hashes in historical results are retained. Use
[the migration map](MIGRATION.md#explicit-historical-component-names) after a rename
and [project status](PROJECT_STATUS.md) for the current source map.

## Conservative directional-wave configuration and authoring Skill — 2026-09-12

Based first on main `2e753fed1f6922d9d2082d6d43c9e150f237bdd6`, then integrated
with main `fb083c159fe1f51612203962d9a7921683eb31c8`, then `0f94cbd`, and finally
`99b9f5f0034ea288f7de0a2a8d7645220c45d8aa` (tree
`b7609f1d22f04a1421d30f0d4a6acc7ad1774b03`). The candidate changes no runtime
source file. The final source fingerprint is
`8de38e5f4ba9db0b188168bf9d33c647b3abe3df2a3450a7cbaa9016a29f2e8d`.

The candidate contract and six saved cases use ordinary
local field rules. The unequal encounter changes 3Y/2Y into 3Z/-2Z and preserves
normalized U=13 and P=5X. All physical guards, encounters and streaming are JSON;
preparation assembles input and observation/rendering do not advance the world.

- Python 3.14.7, pytest 9.1.1 and Ruff 0.16.7: affected gate **230 passed,
  2 opt-in visual skips**. No runtime typing scope changed. The gate included
  49 candidate cases plus check selection, local fields, entity compilation,
  native events, integer arithmetic, cell-state ownership, local Lorentz response,
  recorded-movie, workspace, language and navigation regressions.
- Candidate checks include all 24 proper cubic rotations with the same unchanged
  law, periodic translation/return, slow links, six simultaneous modes, aggregate
  cancellation, per-mode bounds and atomic rollback after invalid proposals.
- An independent physics reviewer accepted locality, all 24 changing-rule U/P
  expressions, numeric bounds and readout ownership. Independent pre/post-main
  comparison against fb083c1 covered seven cases and 244 ticks per runtime: every
  complete state matched, with exact U/P and spatial accounting throughout.
  Subsequent review of 0f94cbd confirmed the shared integer dot/cross operations
  preserve checked ordering, signs and rejection behavior for this candidate.
  The added 99b9f5f cell-state guard accepted three 72-tick slow-link cases:
  2,903 cell inspections and 360 packet inspections, with exact U/P throughout.
- Two canonical 36-tick recordings on the integrated source were independently
  replayed headlessly: all 37 recorded states matched exactly, with zero U/P
  error at every tick. Inputs are identified by SHA-256
  `813deba62d78bd398eda3b7ded525fe72ff3b3510f715c4e01481d8c07f9c1c1`
  (free) and `9759f56cd53b5553f28950c2037d578f8526fe550090f41be3681bed29b92ce1`
  (encounter). Definition SHA-256 is
  `10c896ba55ce774c0bad3e9d5b5c781425206b32e417ea4574e540246d0d5d65`.
- Pillow 12.3.0 decoded the requested comparison GIF: 37 frames, 720 x 980,
  7,940 ms, 1,361,123 bytes. Encounter and post-encounter images were inspected.
  Swapped reference roles, duplicate comparison inputs and a changed recording
  with a stale proof were all rejected. The [saved GIF](https://drive.google.com/file/d/1_q_8CEM4pY_jRn_jI3kw5m_KrfsSTez-/view)
  shows the free/reference and interacting runs with nodes, axes, modes, E/B and U/P.
- The new configuration Skill
  explains the distinct input, catalog/law, execution and display formats. Its
  complete two-stream template completed 18 ticks with inventory 2 conserved;
  its electron/proton/neutron catalog command compiled and completed 36 ticks
  with open-boundary accounting. Both were headless. Skill frontmatter validation
  used the bundled validator with PyYAML 6.0.3 in a separate validation dependency
  directory; no project dependency was added.

The exact affected gate invocation was `python tools/check.py --base HEAD --tests
tests/test_local_field_rules.py tests/test_entity_compiler.py
tests/test_native_event_runtime.py tests/test_integer_arithmetic.py
tests/test_cell_state_contract.py tests/test_local_lorentz_field.py`, where local
validation HEAD had the exact
remote main tree above. Generated recordings, replay proofs, GIFs and local gate
artifacts remain outside source commits; reproduction commands are in the contract.
The full suite and unrelated historical render tests were not selected.

The [Highlights coverage map](HIGHLIGHTS_IMPLEMENTATION.md) records the live
document revision and the candidate's relation to existing rules and hypotheses.
Skill review added the requested authoring responsibility and linked Boss/runner
to it. Existing field-development, physics review and visualization workflows
already cover the candidate; no broader procedure change was needed. This result
is a discrete polarization-interaction candidate, not Maxwell dynamics, trajectory
scattering, charge coupling or arbitrary-angle isotropy. Native event programs
remain absent; their spatial-field composition is explicitly unsupported.

## Physical inventory and elementary probes — 2026-09-12

Base: main `09464b41b2c44a191aa2fcbdf4b036680bd646a5`. The sourced
entity catalog contains 11 field
categories and 35 particle/multiplet entries. These are inventory entries,
not a count of implemented physical fields. Its definitions and support
assessment are explained in PHYSICAL_ENTITIES.md.
Highlights was retrieved on 2026-09-12, including its implemented-entities
section; the user's elementary-vector-operation restriction is binding.

No engine code changes. The two new configurations produce updates only by
copying, swapping or clearing vector values; guards and dot-product invariants
validate those proposals. The old unequal-mass formula remains a clearly labeled
comparison benchmark. No new configuration derives its state from that formula.

The new focused suite passed eight checks: catalog/source/conjugate consistency,
elementary update assignments, equal-mass contact on 9-cubed/X and 15-cubed/Y
domains, outgoing/rest/unequal-mass exclusions, and causal two-vector transport.
The same-local-mechanism checks are not a continuum-limit proof. The final PR
records the mandatory affected gate and exact submitted tree.

Both new inputs were run with the existing CLI and `--visualize`. The pair
completed 16 ticks and 17 recorded frames: contact at tick 4, reversed momentum
in the next sample, final X positions 1 and 7, positive mass 2 in total and zero
net charge/momentum throughout. Its summed raw squared momentum remains 2.
The field probe completed six ticks and seven frames, with exactly three
nearest-neighbor transfers taking two ticks each. Its isolated E/B pulse retains
raw squared amplitude 18 and has no source or dissipation. Both runs report
balanced accounting and use unchanged runtime fingerprint
`b8b0db5aba5c8ee14cfb87be318471f3e1352d0e83b5afb5640e3d49903c37a2`.
Recorded data and metadata were inspected; no graphical-browser validation is
claimed. Generated HTML stays outside the source commit.

This verifies restricted classical proxies and a vector transport mechanism,
not Maxwell dynamics, a photon, gravity or annihilation. Boss and specialist
Skills already route to the updated postulates and owner contracts; no duplicate
Skill rule or new agent role is needed.

## Generic local field rules — 2026-09-12

The extension starts from main `12c85316f011d0601adcd0f4a31f0f52e59eaa27`.
Its authoritative scope is LOCAL_FIELD_RULES.md: retained
field stock, six delivered/outgoing ports, multiple scalar/vector components,
explicit invariants and joint carrier/field transactions. It introduces no
electromagnetic law or quantum-photon result. Highlights was read on 2026-09-12;
the user's node-with-six-ports clarification governs the interface.

The necessary checks exercise simultaneous vector updates, exact six-port
inventory and link delay, independent counterflow samples, integer bounds,
immutable baselines, delayed arrival preservation and stale-invariant rejection.
Active rules retain their results after renaming and declaration permutation.
A zero-net joint chain retains both commit guards and prices their work. Existing
exchange into a local field retains its reaction instead of forwarding it outward.
Unsupported carrier-only joint rules without spatial owners fail initialization.

Independent architecture and physics-rule reviews checked local ownership,
frozen proposals, fixed field timing, bounded arithmetic and commit-cost
reservation. The implementation keeps generic calculations under `fields/`;
engine code schedules them and commits validated ownership changes.

The affected gate uses CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1.
Only changed files and their affected consumers are selected. No full audit,
older-Python compatibility suite or unrelated parameter sweep is part of this
acceptance. Exact final check counts and submitted source identity are attached
to the PR; the gate saves its commands in `artifacts/check-scope.json`.

The explicit visual run uses `examples/local_field_rules.json` with the existing
CLI and `--visualize`: a 9 by 9 by 9 GameBoard, eight transitions, and nine recorded
frames. Starting at `a=(3,4,0), b=(0,0,0)`, the configured rule applies
`a'=b, b'=-a`; the combined squared amplitude is 25 in every recorded frame.
All eight cycles contain component transformations, with no external sources
and balanced spatial ledgers. This quantity is a declared mathematical
invariant, not an established physical energy. The standalone HTML uses recorded
node values and port packets; directional samples are not counted as extra stock.

Boss, field, architecture, test, physics-review, run and PR Skills were reviewed.
Their existing links already route to the updated owner contracts, so no
duplicated procedural rules were added to Skills. Generated run files remain
outside source commits and follow the existing output-retention policy.

## Merge follow-up: affected checks — 2026-09-12

While combined feature head `4dfc1df7543aa7e7568f5112e2e2eb879e464714` passed
GitHub Actions run `34678735217`, main advanced to
`64d26a89842637ab71517ec45aebfa7c3deae331` through PR #29. That change affects
validation selection and contributor guidance, not simulation code. The merge
preserves its default affected-code checks, full-history checkout and explicit
base selection, together with one-day CI artifact retention. Unconditional
example runs and package builds are removed from CI as required by current main.

The new check-scope report uses the existing exact-file retention lease; it does
not claim the whole artifacts directory. Explicit selector edges retain the
generic identity suite's dynamically selected examples and the historical
runpy tool's application consumer. Dry-run selection creates no output.
Current contributor and specialist guidance already defer to the check command
and affected dependencies; no additional Skill change is required.

`python tools/check.py --base 4dfc1df7543aa7e7568f5112e2e2eb879e464714` selected
the selector, language and navigation suites: 29 tests passed in 4.57 seconds,
with Ruff lint/format passing for both affected Python files. Seven selector and
report regressions failed before the integration corrections; all 15 selector
tests now pass, including active writer protection and failed-command expiry.
No `src/event_universe` file changed: runtime fingerprint `cf684492a86605a68c29aba0a169a6e992478b2f7f7b3d70804e8fce7f2d4f4a`
and the preceding simulation, full-gate and packaging evidence remain applicable.
The exact selected commands are recorded in the leased `artifacts/check-scope.json`.

## Merge with atomic interactions — 2026-09-12

The authorized PR #27 merge found that main had advanced through PR #28 to
`15029ba8d02bd7f1bb1dd1148fe55405ec1536b1`. The integration combines that exact
main tree with tested feature head `137830fd621b9522598e0719e7bd2055ead595a9`.
Signed commit, tree and blob hashes were verified through the GitHub connection
before the local merge. The previous head's CI pass alone was not reused as
evidence for the combined source.

Conflict resolutions preserve recursive spatial flux when adding integer
dot/matrix/comparison operators, all optional initial-state fields, both spatial
schemas and boundaries, spatial work scheduling and atomic pair rules. API
assembly retains spatial planner/coupler/decayer injection. Replacements preserve
carried residuals and finite allowances. Atomic interactions follow proposed
spatial response and ordinary exchange, before routing; invalid carrier proposals
do not roll back earlier independent field transport or emission.

The initial independent conflict-resolution review passed 301 focused cases.
Four new combined numerical tests and the original atomic/language cases passed
26 focused checks. A spatial Z turn followed by an atomic swap yields carrier
vectors `(0,-1,0)` and `(0,5,0)` with opposite recoil `(4,-4,0)`; first-link half
retention accounts for survivors `(2,-2,0)` and equal signed loss. Raising the
coupling price by six increases local cost by 18 across the three responses.
Delayed commits retain the frozen response while emission exhausts its allowance;
nested transform/dot/comparison expressions retain delivered flux context. A
rejected atomic proposal leaves earlier independent emission accounted.

Independent physics-rule review found no additional ownership, locality, timing
or conservation blocker. The first full-gate attempt stopped at mixed line
endings in two resolved files; Ruff normalized those endings without a semantic
change. The final runtime fingerprint is
`cf684492a86605a68c29aba0a169a6e992478b2f7f7b3d70804e8fce7f2d4f4a`.
Wheel and sdist build and asset/source equality checks passed in the leased
`../runs/merge27-packaging/` directory. The packaged source precedes this
evidence-only documentation addition. No visualization was requested or generated.

The unchanged full gate passed: 1,093 tests, 30 explicitly visual skips, Ruff
lint/format (169 files) and strict mypy (66 source modules), in 120.05 seconds.
Independent headless comparisons against archived feature `137830f` retained
byte-identical initialization, ordered events and final state for `open_world`
(12 ticks), `three_mass_finite` (120) and `spatial_turning` (12), with equal
per-tick snapshots and ledgers. Metadata excludes only source identity and host
elapsed time. The new collision separately passed 360 ticks with mass 5,
momentum `(5,0,0)` and kinetic diagnostic `35/2` throughout; contact is at tick
120, reversal at 121, final X positions 3 and 13 and every link takes one tick.
No old-source equivalence is claimed for that new example.

The comparison archives identify Python fingerprints `df6553380020d5c6ccebc2f4b2f64687141c66938ac9e08528a5792dc795f812`
(baseline) and `f6d202ba997eaf4bf35ad3c63f0aa37680926aae50be676dd68a8edb32c49d25`
(combined snapshot). Only verified CRLF/LF normalization in two files separates
that snapshot from final `cf684492`; the final source passes the full gate.
Temporary run, comparison and source-normalization records live under
`../runs/merge27-regression/`, with the same 24-hour artifact policy.

The workspace includes all 11 packaged templates. Shared workflow, Boss and
PR-review Skills were reviewed; their existing rules already require refreshed
main, coordinated provider/consumer reconciliation and current-tree validation,
so no additional procedural rule was needed for this merge.

## Genericity audit — 2026-09-12

The audit continues published feature head `188e3d3` on main base `c252254`.
It covers the active initialization-to-law-to-engine path, spatial responses,
costs, timing, ledgers and workspace adapters. No physical engine, parser or
arithmetic implementation changed. Historical named research APIs remain
explicit model selections, not the primary generic Simulation.

| Check | Result |
| --- | --- |
| Active engine/field review | No physical-name or model-ID dispatch; 233 focused existing tests passed |
| Durable identity regressions | 18 cases compare six scenarios across six transitions after renaming labels/units, reordering declarations, or both; snapshots, complete ordered events, costs, timing and ledgers agree |
| Executed behaviors | Source updates, splitting, delayed commits, cost reporting, paired exchange, finite emission/decay, norm-preserving rotation, delivered flux and open exits are required to occur |
| Independent composite audit | 744 snapshot/event/accounting comparisons passed across eight boundary/transit/budget combinations; low budgets actually reduced committed cycles |
| Editor fixes | Draft storage retains arbitrary template keys, including `__proto__`; generated field/type names skip existing declarations without changing defaults |
| Failure-before evidence | Eight new editor cases failed before the fix; the historical diagonal tool separately failed to import its obsolete Simulation name |
| Focused verification | 60 workspace tests and 9 historical application tests passed; one explicitly visual application case skipped |
| Independent diff review | No blocking finding; all 30 selected new regressions passed |
| Unchanged full gate | Ruff lint/format and strict mypy passed; 1,075 tests passed, 30 explicitly visual cases skipped in 118.03 seconds |
| Static scope | 167 formatted Python files; 66 typed package modules |
| Packaging | Wheel and sdist built in a leased temporary source copy; packaged editor bytes match source and sdist includes the new identity suite and explicit historical tool |

The Python runtime fingerprint remains
`f2cfc31cb5d85bd3dc414d871c36bde17453b0773e9bc51505b2424474a7893d`.
Temporary build/equality evidence is under `../runs/genericity-packaging/`;
the full gate report is `artifacts/junit.xml`. Both follow the 24-hour output
retention policy. Package source checks preceded this evidence-only addition.

The historical diagonal tool now imports `ScalarSimulation` explicitly; its
regression checks importability without rendering. The editor fixes affect
configuration handling only. Identity comparisons normalize semantic labels,
preserve ordered rules/axes/seeds and require nonzero activity. They establish
the tested scenarios and duration, not equivalence of every private register or
arbitrary user-defined algorithms.

The movie currently omits spatial populations and spatial transfers, although
those remain in saved state/recording data. Spatial extension settings remain
editable through complete JSON. This capability limit is documented in
[WORKSPACE.md](WORKSPACE.md); no visualization was requested or generated.
The architecture-review Skill now requires role-aware renaming, declaration
permutations and observed activity. Shared workflow and Boss guidance were
reviewed and already cover integration ownership and the required full gate.

## Generated-output retention — 2026-09-12

This host-only update continues published feature head `45da520` on main base
`c252254`. The policy and ownership rules are in [RETENTION.md](RETENTION.md).
Physical laws, costs and simulated time are unchanged.

| Check | Result |
| --- | --- |
| Unchanged full gate | Ruff lint/format and strict mypy passed; 1,045 tests passed, 30 explicitly visual cases skipped |
| Static scope | 166 formatted Python files; 66 typed package modules |
| Expiry and safety | Exact 24-hour boundaries, latest-write extension, active writers, orphan-child dependencies, source/link rejection, generation replacement, interrupted quarantine/reuse, verified adoption and singleton watcher covered |
| Runner/UI integration | Successful, failed and cancelled jobs, real HTTP/CLI equality, expired links and fresh/empty/sibling-relative output paths covered |
| Independent review | Filesystem replacement, interrupted cleanup and orphan-parent probes passed; existing artifact inventory excludes source and original example/configuration directories |
| Headless regression | Final 12-tick open run has byte-identical initialization, events and state to the prior published run |
| Packaging | Wheel and sdist built; four changed package modules match final source bytes, and sdist includes the retention contract |
| Local operation | 192 reviewed generated files enrolled with expected filesystem identities; no historical file was over 24 hours old, so initial cleanup removed none |
| Scheduling | Hidden singleton watcher started for five reviewed local output roots; a second start confirmed it already running; hourly thread automation `universe24` maintains it and catches up after interruption |
| Automatic deletion | The running watcher removed a newly registered, deliberately expired generated probe without a manual cleanup invocation |

The five operational roots are this workspace's `runs/` and the `artifacts/`
directories in `Universe24`, `Universe24-fields`, `Universe24-init` and
`Universe24-output`. A separate older UI reports outputs under a sibling
`con/outputs/movie-workspace/` directory. That directory is outside this session's
writable roots, so this deployment does not claim retention coverage there.

The final runtime fingerprint is
`f2cfc31cb5d85bd3dc414d871c36bde17453b0773e9bc51505b2424474a7893d`.
The open-run event hash remains
`42376d9d97516e7d5667d35489e06f7e4db1426666e3e4a0fa359920554273bd`;
the final state hash remains
`7a8f082a80c77a1218bfba678bd8fcf249e531926e08814b1306476b66388320`.
Temporary evidence is in `../runs/retention-open-final/`,
`../runs/retention-validation.json`, `../runs/retention-packaging/` and
`artifacts/junit.xml`; those paths follow the same expiry policy.

The first real sibling-relative CLI invocation exposed an unnormalized `..` in
its lease target. Both runners now validate the original lexical path before
passing its resolved path to retention; dedicated regressions cover that case.
The unchanged full gate was repeated after this correction. No visualization
was requested or generated. Workflow and simulation-runner guidance now require
temporary-evidence handling and explicit ownership for custom diagnostics.

## Publication integration with the configuration workspace — 2026-09-12

The publication candidate combines local field head `d3bb0ce` with exact remote
main `c252254eecb5e3b090f9ae40667c383db11a14fc`. Remote Git objects were obtained
through the authorized GitHub connection and their content hashes verified before
integration; the local Git HTTPS client could not authenticate. Main's workspace,
movie assets, presets and parser interface are preserved.

The integration fixes three consumers: terminal movie transfers accept a missing
destination and retain outward coordinates in open worlds; results distinguish
balanced loss/escape from failed accounting; renaming fields also updates nested
flux expressions. These changes do not modify physical engine calculations.

| Check | Result |
| --- | --- |
| Unchanged full gate | Ruff lint/format, strict mypy, 970 passed; 30 explicitly visual cases skipped |
| Static scope | 161 formatted Python files; 65 typed package modules |
| UI regressions | 13 headless JavaScript cases passed, after 10 failed before the fixes; existing periodic/accounting controls retained |
| Workspace regressions | 19 passed, including real HTTP submission of the finite open example and exact signed escape/loss totals |
| CLI/workspace equality | All input, state and event bytes remain exact; metadata equality excludes only the validated host elapsed timer |
| Integrated periodic run | 5,000 ticks in 10.481 host seconds; event and state files byte-identical to the verified pre-integration run |
| Integrated open run | 12 ticks; event and state files byte-identical, carried escape 72 and spatial escape 20 plus loss 52 |
| Packaging | Wheel and sdist built; packaged topology and changed UI assets match current source bytes |
| Visual inspection | Not requested; no visualization generated |

Both integrated runs balanced every completed tick. Their runtime fingerprint is
`26d7ad18f8eef8581168a6e926d7266605bc286d199437207763a54eb6a67e42`.
Canonical evidence is in `../runs/publish-periodic-5000/` and
`../runs/publish-open-12/`. The earlier benchmark still identifies its own source
and does not imply a new timing comparison. The full gate writes
`artifacts/junit.xml`; package evidence is outside the checkout in
`../runs/publish-final-packaging/` and `../runs/publish-final-build.log`.

The first merged gate exposed two obsolete test expectations: the template list
omitted five new examples and metadata byte equality included elapsed host time.
The final tests enumerate all intended examples, validate the timer and preserve
all physical equality checks. No failed physical requirement was removed.
The publication PR records remote commit and CI status; integration into this
feature branch is not a claim that the feature is merged into main. Existing
workflow and specialist guidance already require consumer validation and exact
source identity, so this integration needed no further Skill change.

## Configured boundaries and spatial scheduling — 2026-09-12

This change continues local `4a976f827ae62e16e5d23e319b1d2ce963227d9e`.
The user selected opposite-face reentry for a closed world and removal with
escaped-quantity accounting for an open world. Both schemas default to periodic
boundaries; the chosen configuration applies to carriers and spatial fields.
See the boundary contract.

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 935 passed and 28 explicitly visual cases skipped |
| Static scope | 156 formatted Python files; 64 typed package modules |
| New tests | 121 cases across configuration/topology, open ownership/escape, dormant scheduling and headless boundary output |
| Independent physics review | 264 affected/regression cases passed; 12 additional open/periodic, transit 1/2/3 and ordinary/delayed-budget runs matched full-sweep snapshots, events and accounting over 90 ticks each |
| Independent inventory audit | Full cell/link inventory equals indexed totals after every reviewed tick; skipped cells have no populations, pending receive cost or reported local cost |
| Periodic faces | All six positive/negative faces of a 3x4x5 domain wrap without changing the carried vector; arrivals at ticks 3 and 6 retain the full transit time |
| Terminal field exit | Original signed payload escapes after full transit; no outside cell, attenuation, merge, receive event or receiver cost |
| Open CLI example | 12 ticks, carried escape 72; spatial injection 72 = escape 20 + dissipation 52; no remaining carrier, dynamic stock or packet, and no outside address |
| Three-carrier CLI | 5,000 ticks completed in 10.356 host seconds; three records and mass 10 retained; every completed tick balances |
| Canonical periodic regression | Full ordered event file is byte-identical to the prior verified finite run; final state matches after removing only new boundary and escaped-ledger metadata |
| Package build | `python -m build --no-isolation` built wheel and sdist |
| Visualization | Not requested or generated |

The performance comparison used exactly the same initialization bytes, 5,000
ticks and per-tick accounting plus three-record checks. The baseline was a
verified archive of commit `4a976f8`; the candidate was an identified source
snapshot. Each source was run once for this comparison. Host times were:

| Measured work | Baseline seconds | Candidate seconds |
| --- | ---: | ---: |
| Simulation stepping | 34.105 | 9.159 |
| Separate accounting and record checks | 40.177 | 1.653 |
| Complete measured loop | 74.393 | 10.920 |

This is approximately 6.8 times faster for that scenario and machine. All nine
saved checkpoints have equal physical values, event counts and modeled costs;
the full final state is equal after removing new boundary metadata. The benchmark
observer did not save an ordered event digest; the separate canonical CLI
comparison above did compare the complete event files. The optimization skips
dormant spatial cell planning and resident-population summation. Empty link
buffers can still be scanned; it does not remove every historical host traversal
or alter the model's local computation charges.

Runtime fingerprint, unchanged across the final runs and independent review:
`dd4ac82debd3fb0e28b33ea4a26297930e42c53d627ca2a69d60c8c934dc56b4`.
The benchmark input fingerprint is
`a89397e6b87f9605c2e7dcc128925f22da23e26e450ccc6f17136c1e102cc74f`.
The canonical periodic example now explicitly includes the default boundary key,
so its input fingerprint is
`2d0742951aa49cbe88e6ae87ffff74859031ffbde301c4e9ade4bed7b4b540cf`.
The open example fingerprint is
`b4e3038d3b0539a7dabc11afd1dd346a272ee51af73c2c81dafd4a65b870d76f`.
Runtime/tools remain CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1.

Saved evidence is outside the checkout: `../runs/boundary-periodic-5000/`,
`../runs/boundary-open-12/`, `../runs/boundary-verification.json`,
`../runs/boundary-performance/baseline-4a976f8-verified/` and
`../runs/boundary-performance/optimized-working-4a976f8/`. Run directories
contain exact inputs, metadata, events and final state. Benchmark directories
contain timing, source identity, checkpoints and comparison reports.

Closed topology does not disable configured decay: combined momentum plus signed
loss balances, while physical momentum alone is not conserved by that law. Open
accounting additionally includes escaped quantities. General self-field
attribution, energy conservation and carrier stopping remain unestablished.
The existing isolated field branch has not been published or integrated into
remote main `c252254eecb5e3b090f9ae40667c383db11a14fc`, which was read with no
open PRs; local fetching remains unavailable. No external Highlights edit is
implied. Boss and affected Skills were reviewed; the shared workflow now requires
import-path and source-fingerprint verification when reusing an editable
environment across worktrees, following a detected wrong-checkout import.

## Finite integer fields and allowances — 2026-09-12

This change continues local `e8e5c4cd59ec3ddd8c191e0faac4468acd0a5d71`.
Schema 2 selects `finite-dissipative-v1`; schema 1 keeps its separately named
conservative law. See SPATIAL_FIELDS.md for the law and
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md) for independent acceptance inputs.

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, 814 passed and 28 explicitly visual cases skipped |
| Static scope | 152 formatted Python files; 63 typed package modules |
| New tests | 108 cases across schema validation, integer decay, finite source integration and finite coupling allowances |
| Independent physics review | 219 affected/new and retained regression cases passed; separate periodic signed-rotation and single-charge decay-cost checks passed |
| Finite moving source | 40 headless ticks; lifetime injection 720 and dissipation 720; final dynamic field zero and carried strength 72 |
| Three carriers with computation field | 5,000 headless ticks in the original 65x65x65 domain; initial rate c/10 and all three first arrivals at tick 10 |
| Three-carrier balances | Mass 10 throughout; final combined vector `(-1,7,0)` plus signed dissipation `(-1,3,0)` equals initial `(-2,10,0)`; every completed tick balances |
| Spatial extinction | All 2,160 computation units injected by the three sources dissipated; dynamic computation and reaction populations vanish by tick 12; computation baseline remains 1 |
| Rotation | Affordable turns retain carrier norm and commit exact opposite reaction; insufficient allowance rejects both sides without changing fractional state |
| Legacy regression | Existing conservative spatial, movement, coupling, integer, locality, architecture and headless application contracts remain in the full gate |
| Visualization | Not requested or generated |

Final runtime source fingerprint:
`faa5de68bdfb0ceb77ddaa8a75d1bdce18333ef5c019d3c8b7572e4e78d268f3`.
The independent review first recorded fingerprint
`65782ddf166c906c53f0df2dc6e76fb1491a5163c54e3ff2c3aabd1b3f768659`;
the subsequent runtime change was Ruff normalization of mixed line endings in
`initialization.py`, with no arithmetic or scheduling change. The final full
gate passed after normalization. Saved final-source runs reside outside the
checkout in `../runs/finite-fields-v2-verified/` and
`../runs/three-mass-finite-v2-verified/`, with input, metadata, events and state.
The three-carrier initialization fingerprint is
`a89397e6b87f9605c2e7dcc128925f22da23e26e450ccc6f17136c1e102cc74f`.

Decay loss is explicitly nonconservative. The runner reports physical conservation
as false for these dissipative examples while its separate loss-accounting check
passes. No energy law, general self-field attribution or automatic carrier rest is
claimed. The old no-decay 5,000-tick experiment remains paused at tick 140 and is
not resumed under the changed law.

Remote main was read at `c252254eecb5e3b090f9ae40667c383db11a14fc`, with no open
pull requests. Local fetching was unavailable; this evidence does not claim the
candidate has been integrated with that main or published to GitHub. The code
remains on the existing isolated field branch. Boss, field development and physics
review Skills were reviewed; their existing candidate, locality, ownership and
independent-validation instructions already cover this change, so no Skill edit
is needed. The latest user request is the authority for the new law; no external
Highlights document was modified in this implementation task.

## Generic spatial exchange and rotation — 2026-09-12

The response extension continues local commit `5ff53888413afd421d129ffacb0d749ca0be8f08`
on base main `a53e1a2f83d4dca898ed827b2f6e4d101932be95`.
SPATIAL_COUPLINGS.md defines the selected integer law,
local sampling, atomic recoil, timing and fixed preparation tariff. This section
supersedes the earlier outward-only candidate's missing-turning limitation;
general source attribution is still a separate unimplemented capability.

| Check | Result |
| --- | --- |
| Unchanged `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 706 passed and 28 visualization cases skipped |
| Static scope | 147 formatted Python files; 62 typed package modules |
| New response suite | 53 passed: signed axes, axis order, zero/invariant axes, carried fractions, scalar flux, routing, frozen samples, exact reaction arrival and atomic overflow |
| Independent physics review | Scoped pass on final runtime fingerprint; 157 relevant cases and nine additional signed-rotation/transit examples passed |
| Three-turn CLI example | Completed ticks 1, 2 and 3 at `(15,16,15)`, `(14,16,15)` and `(14,15,15)`; vectors `(0,5,0)`, `(-5,0,0)` and `(0,-5,0)` |
| Rotation accounting | Carrier squared norm stays 25; total carrier plus field vector stays `(5,0,0)` at every completed tick; source vector remains zero |
| Moving-source regression | Five ticks; source strength 72, spatial stock and injected amount both 360; all completed ticks conserve |
| Basic/exchange regression | Saved state and event files remain byte-identical to unmodified-base runs |
| Visualization | No visualization requested or generated |

Runtime source fingerprint:
`d06be12cd1a88df93b2cd9f8523344ddce2bc18827ce2839beb147f607056505`.
The turning initialization fingerprint is
`6cf38af8b1078cbfb53c9085ead7062c0c338cce97f028f10465645b2a32561f`.
Saved runs are outside the checkout in `../runs/spatial-coupling-validation/`:
`spatial_turning/`, `moving_source/`, `basic/` and `exchange/`, each with input,
metadata, events and final state. The full gate writes `artifacts/junit.xml`.
Runtime/tool versions remain CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7 and
mypy 2.3.1. Source fingerprints depend on exact file bytes, including line endings.

The three field reactions are `(5,-5,0)`, `(5,5,0)` and `(-5,5,0)` at their
respective local commits. Immediate and delayed cases verify first field arrival
at `commit_tick + link_ticks`, including transit times one and two. The independent
review also checked transit time three with a non-cardinal `(2,3,4)` vector.

Straight cardinal scalar-flux rotation passes an isolated-source control without
changing its vector or fractional state, while an external transverse pulse acts.
This is a geometric property, not a general self-filter. A separate diagnostic
in `../runs/spatial-coupling-review/` confirms a bounded own-front estimate for ten
straight steps and a straight/wait sequence. An unpaused turn has actual own stock
48 but a one-path estimate 42 at tick two; periodic return has actual 24 versus
estimate zero. These diagnostic references never feed the simulator's physics.
Continuous-angle rotation, general self attribution and general energy or angular
momentum conservation are not claimed by the discrete response law.

The field-development Skill now distinguishes combined vector conservation from
carrier norm and requires an external transverse control, causal reaction packets
and accurate cost-tariff wording. Shared, Boss, architecture, test and physics
Skills were reviewed; their existing instructions needed no additional change.
Highlights was read on 2026-09-12 at the same revision as the preceding integration;
the new executable contract is persisted here, without modifying that document.

## Configured outward spatial fields — 2026-09-11

This optional candidate is based on main
`a53e1a2f83d4dca898ed827b2f6e4d101932be95`. Its transport, timing and remaining
model gaps are defined in SPATIAL_FIELDS.md. The implementation
separates a continuously emitting carrier from its spatial stock and selects the
new law explicitly through initialization. This section records local evidence;
the submitted PR records its exact commit and remote CI result.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 653 passed and 28 visualization cases skipped |
| Static scope | 144 formatted Python files, 61 typed source modules |
| Independent physics review | Scoped pass on the final source fingerprint; 104 relevant cases passed, including fixed transit, signed conservation, delayed proposals and carried fractions |
| Moving source example | Five completed ticks; carrier advances one cell on each tick, from `(15,15,15)` to `(20,15,15)` |
| Source accounting | Carried strength stays 72; initial spatial stock 0, committed emission 360 and final spatial stock 360; balance checked after every completed tick |
| Existing basic/exchange examples | Final state and event files are byte-identical to runs from the unmodified base tree |
| Paired vector rotation | 16 additional numerical cases passed across eight rotations/sign cases and two computation budgets; component-wise recoil balance preserved |
| Package build | Wheel and sdist built successfully with `python -m build --no-isolation` |
| Visualization | No visualization requested or generated; rendering-only tests were skipped |

The moving-source run and independent review identify the runtime source as
`b1a958835fc92efe8f6a584dfa4c3fae4abd5427d47b77e8664a131185e09c81`.
The saved initialization fingerprint is
`3f9fcee4b315698e31794d9eedbcf1ce954010a85b41484f3719f3f70c41a862`.
Local evidence is preserved outside the source checkout in
`../runs/spatial-validation/`, including `current-moving_source/`, the two
baseline/current comparisons, package outputs and the build log. Each run has
its initialization bytes, events, final state and `run.json`. Additional rotation
evidence is in `../runs/rotation-conservation/`. The full gate writes
`artifacts/junit.xml`. Source fingerprints depend on runtime file bytes and may
differ across platform line endings.

Runtime and tools: CPython 3.14.7, pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1,
build 1.6.1 and setuptools 84.0.0. The shared, Boss, architecture, test and physics
Skills were reviewed; their existing rules were sufficient. The field-development
Skill now requires coarrival, turning and periodic-return checks before claiming
self attribution, and distinguishes illustrative shells from executable rules.

Automatic self-field subtraction and spatial-field-driven turning are **not
implemented**. Equal-speed coarrival and alternate field paths invalidate the
proposed first-arrival proof; merged integer rounding also prevents inferring an
exact self contribution from a single tracked path. The existing paired-record
rotation checks do not establish that missing law. The new field clock is fixed
at one link per `link_ticks`; priced spatial work can delay a new carrier cycle
but does not throttle spatial forwarding. This timing choice is explicit in the
candidate contract, not evidence that the earlier uniform-delay law is unchanged.

## Initialization-defined disturbances — 2026-09-11

The generic implementation was integrated with main
`ec0826b20286a166498beacd6cb68002624826eb`, including its historical renderer
performance and concurrent-preview changes. The active CLI requires `--init`;
historical scenarios use `event_universe.legacy_runner`. Both paths are headless
unless visualization is explicitly selected. This section records local
verification; the submitted PR records the remote commit and CI result.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy, 569 passed and 28 visualization cases skipped |
| Static scope | 133 formatted files, 57 typed source modules |
| Initialization | 42 checks cover schema bounds, expressions, arbitrary names and invalid input |
| Generic ownership and arithmetic | 23 checks cover signed scalar/vector conservation, whole-record movement, coupling, exact delay, frozen proposals, capacity and failure atomicity |
| Generic application | 12 checks cover required input, headless imports/output, input-byte identity, failed-tick reporting and renamed simulation equivalence |
| Independent physics review | Six reproduced defects corrected and covered; scoped review passed, including pair-remainder lifetime and counterflow channels |
| Basic example | 8 completed ticks; initial/final totals mass 2, charge -1, signal 12; conservation checked after every completed tick |
| Exchange example | 8 completed ticks; initial/final balance 8; conservation checked after every completed tick |
| Visualization | No world visualization generated; rendering-only cases require `--visualize-runs` |

Both final example runs have local source fingerprint
`3f26ce8cb69c01368f4b04166c82bdaafe2a2db4b6d6381ea5215f1e6f2ebe6b`.
Their preserved outputs are `artifacts/basic-final/` and
`artifacts/exchange-final/`, each containing the exact initialization bytes,
events, final state and `run.json` metadata. The full gate writes
`artifacts/junit.xml`. Source fingerprints identify runtime file bytes and may
differ across platform line-ending conventions.

Runtime: CPython 3.14.7. Tools: pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1,
build 1.6.1 and setuptools 84.0.0. Historical fixed-physics regression contracts
remain active under their named APIs. The new framework supports same-field
paired exchange, fixed capacity and bounded integer laws; it does not establish
gravity, wave equations, relativity or arbitrary energy conservation.

The agreed high-level specification was reconciled with Universe 24 Highlights
on 2026-09-11. Detailed executable requirements are in
DISTURBANCES.md, with inputs and acceptance cases in
[TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md). Earlier evidence below describes
historical candidates and earlier output defaults.

## Python 3.14 and necessary tests — 2026-09-11

Validated locally with CPython 3.14.7 in the project virtual environment, based on
main `7e517afb7a274821de05bf247ece91827c1b030b`. The runtime selection, CI and
agent workflow now use Python 3.14. Older-Python, archived-v10 equality and
historical facade API tests are no longer gates, as requested by the user.
Current physical contracts and known failure evidence remain covered.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint/format, strict mypy and 461 pytest cases |
| Static scope | 114 Python files formatted; 48 package modules type checked |
| Test reduction | Four fewer collected cases, six fewer worlds and 447 fewer simulation ticks |
| Test visualization | All 94 current-engine worlds rendered through the existing HTML/GIF pipeline |
| Contact CLI | Completed 48 ticks; momentum equal at every completed tick; all state audits passed |
| Visual inspection | Contact frame at tick 24 shows both particles, field, axes and total momentum (0,0,0) |
| Package build | Wheel and sdist built; minimum Python is 3.14 and sdist includes `.python-version` |
| Agent Skills | Boss, architecture, regression and necessary-tests Skills validated; shared workflow updated |

Installed project tools: pytest 9.1.1, Ruff 0.16.7, mypy 2.3.1, Matplotlib 3.11.1,
Pillow 12.3.0, NumPy 2.5.3 and build 1.6.1. Isolated package build used
setuptools 84.0.0. Contact source fingerprint:
`c7696ccccad62080363a35673f9e6be053c3f5461909160de8792abc8b621256`.

The remaining suite is defined in [TEST_EXPECTATIONS.md](TEST_EXPECTATIONS.md).
Local outputs are `artifacts/junit.xml`, `artifacts/test-runs.html` and
`artifacts/contact/run.html` with run metadata. The integration PR and its Actions
run record the remote result for the submitted commit. No old-Python or archived
engine compatibility run was performed. Earlier evidence below is historical.

## Historical validation — 2026-09-10

The required checks were executed locally on Python 3.12. GitHub Actions is
configured but was not executed on a remote repository in this task.

| Check | Result |
| --- | --- |
| Ruff lint | Passed |
| Ruff format | 52 Python files already formatted |
| mypy strict | Passed, 26 package modules |
| pytest | 206 passed, 0 failures, 0 errors, 0 skipped |
| Frozen-reference comparison | Exact after all 278 compared ticks |
| Contact application run | Completed 48 ticks; total momentum equal at every tick |
| Turning application run | Completed 110 ticks; total momentum equal at every tick |
| Generic field/turning | Signed and weighted fields, exact residues, direction policies and bounds passed |
| Current model | Exact field sample, source mapping, clipping and transverse response passed |
| Public component replacement | Field/turning/activity injection, remainder-only evolution and invalid-result rejection passed |
| Calculation boundaries | Absolute/relative imports and formula-free assembly checked, including forbidden-example tests |
| Dedicated expectations | GameBoard, movement, source/range/activity policies and all diagnostic projections passed |
| Test visualization | 41 engine/reference runs rendered through the shared GIF/HTML pipeline |
| Full XYZ display | 48-tick contact run completed with total momentum preserved; shared GIF/HTML pipeline |
| Display equivalence | Plane and volume runs produced identical physical events and final reports |
| Visual inspection | Final frames of contact and turning checked; plane labels visible |

The full-state comparison checks every materialized cell, particle register,
occupancy slot, active-frontier member, force record, blocked move and path entry
after each step. It covers 120 stationary-source steps, 48 contact steps and 110
turning steps. This is evidence for those scenarios, not a proof over all inputs.

The contact event first has transverse impulse `(0,1,0)` at event tick 15, visible
in the completed frame labelled tick 16. Event records use the tick being
processed; completed frames use the count of finished ticks. This is the
preserved v10 convention.

Source fingerprint used by the preserved plane application runs:
`66855a6339d5ef4448c94ed8e47db7366a7387ea2d816aab7bedb1821d5494df`.

The full XYZ contact visualization uses source fingerprint
`47b24f3f6c8446a39c93e8badcb3baa305b4454e66ddc29fd76accd671914349`.
Its midpoint was visually inspected. After the suite, only display color,
marker size and opacity were adjusted; the XYZ demonstration was regenerated.

The source-only scalar field and full-vector turning variant are test fixtures.
They demonstrate component replacement through `Simulation`; the production
default model and its identifier remain unchanged.
An additional local-retention fixture verifies the expected sample sequence
`(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0)`, ensuring a replacement
field is not stopped while only its remainder changes. Calculation inputs,
expected outputs and ownership are documented in `TEST_EXPECTATIONS.md`.

| Tool | Version |
| --- | --- |
| pytest | 9.1.1 |
| Ruff | 0.16.6 |
| mypy | 2.3.1 |
| Matplotlib | 3.10.8 |
| Pillow | 12.3.0 |
| build | 1.6.0 |
| setuptools | 84.0.0 |

Detailed outputs are in `artifacts/checks.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, and each scenario's `run.json` and `run.html`.
Known model assumptions and limits remain in `SIMULATOR_DEFINITIONS.md`.

## v11 local-link candidate validation — this change

- Required `python tools/check.py` completed: Ruff lint/format passed (60 Python
  files), strict mypy passed (31 source modules), **222 pytest tests passed**.
- All original frozen-v10 comparisons passed without changing expected traces.
- Eighteen new tests cover geometry, transport and the linked engine. The
  stationary-source regression initially exposed an owner-only directional
  artifact; the symmetric two-endpoint proposal protocol now passes it.
- 46 engine/reference test runs were captured using the existing renderer.
- The linked application completed 360 elementary ticks on a 32×24×12 GameBoard,
  with two particles and base link length 10. Total momentum matched the initial
  value at every completed tick. All runtime state audits passed.
- The final rendered frame was inspected: XY slice z=6 and tick=360 are visible.
  Arrows are scaled direction indicators; the drawing remains an address-grid
  view, not a geometrically stretched embedding.
- These tests establish the enumerated locality and numerical properties in
  tested cases; they do not establish Einstein geodesics or gravity. The example
  particles crossed the region on straight tracks; no attraction is claimed.

Current outputs: `artifacts/local-links-check.log`, `artifacts/junit.xml`,
`artifacts/test-runs.html`, `artifacts/local-links/run.json`, `.html`, `.gif`,
`.mp4` and `events.jsonl`. The video is a conversion of the existing GIF replay,
not a separately simulated trajectory.

Source fingerprint for the linked application: `53786817fe9f2c9a089a875894523229b6eb02d52bc077095fea2cc482693875`.

## Concurrent update reconciliation

The archive advanced from version 3 to version 4 while this change was being
implemented. The guarded write rejected replacement of that newer archive.
The full-XYZ renderer, `--view-3d`, its independent frame capture and both new
diagnostic tests were preserved. Link changes were reapplied to version 4.
The required gates were repeated on this merged tree: **224 tests passed**,
Ruff lint/format passed and strict mypy passed. The test renderer captured
48 engine/reference runs. The linked application was rerun from the merged
source; its current fingerprint is recorded in `artifacts/local-links/run.json`.
Earlier evidence is preserved under `artifacts/local-links-before-merge` and
`artifacts/local-links-check-before-merge.log`.
## Executable catalog and bounded conversions, 2026-09-12

Base: `d1d7251ba739fb7231eff0d41037744456297ddd`. Python 3.14.7.
The affected gate selected 764 passing cases and five explicitly optional visual
skips; Ruff and mypy passed. Selection includes consumers of the shared
initialization, record schema and local interaction law, not a full-suite switch.
All 46 catalog entries compile through the canonical validator. Representative
active worlds cover shared carrier, scalar and vector behavior without repeating
the same dynamics for every particle name.

Independent architecture/physics review found and resolved strict catalog input
validation and a conversion restriction on nonzero arrival channel tags. A real
incoming-pair regression now verifies conversion after neighbor arrival; channel
provenance is preserved while actual carried fractional progress remains rejected.
Boss, architecture, fields, physics, tests and simulation Skills were reviewed;
their existing workflow covers this change, so no Skill edit was necessary.
Highlights was read on 2026-09-12.
No change to that Google document is implied.

Three CLI runs generated recorded HTML with source fingerprint
`1695a4c8757b6493e5bf58613a6b6cd97e533df81d1f17f58723c9a9354d4fce`:

| Probe | Evidence |
| --- | --- |
| Catalog electron/positron/EM registers | Four ticks; inventory 2, charge 0, momentum (2,0,0), E/B component stock (0,1,0); causal carrier and field transfers |
| `conversion.json` | Six ticks; two held records become outgoing types, stock 5 and momentum zero remain |
| Incoming variant from `test_incoming_carriers_convert_after_real_neighbor_arrival_and_reverse` | Six ticks; seeds at x=3/5 meet at x=4, convert and reverse to x=2/6; stock 5 and momentum zero remain; link time 2 |

Metadata, final states, event traces and HTML data were inspected. Browser visual
inspection was not performed; the existing renderer is unchanged. These are
representation/conversion tests, not physical annihilation, Maxwell, mass,
spinor, gauge, metric or general energy derivations. Git PR/CI evidence identifies
the final integrated tree; generated output follows finite retention.

## Repository consistency baseline — 2026-09-12

The whole-repository audit starts from main
`2e753fed1f6922d9d2082d6d43c9e150f237bdd6` (228 tracked project files).
[Baseline run 34693224761](https://github.com/Closer24/Universe24/actions/runs/34693224761)
executed `python tools/check.py --full` using Python 3.14.7, Ruff 0.16.7,
mypy 2.3.1 and pytest 9.1.1: Ruff check/format passed, strict mypy passed
73 source files, and pytest passed 1,249 cases with 30 explicit visualization skips.
The temporary read-only audit workflow was the only addition in that run;
its source tree was otherwise the recorded main revision.

The inventory found one byte-identical collision configuration pair and no exact
production function-body copies at the inspected threshold of 12 source lines.
This is a duplication heuristic, not proof of absence of semantic overlap.
The cleanup consolidates that input, explicitly names historical scalar owners,
extends source-language/navigation/hygiene coverage and preserves reference files.
Final submitted-tree validation is recorded in its PR/CI, not inferred from this
baseline result. No visual inspection or newly derived physical law is claimed.

## Parallel Node tick planning — 2026-09-13

Base: `db5fd9f2518d8551fdeaacd64a583e9fa6d5dd62`. The affected gate ran on
CPython 3.14.7 with pytest 9.1.1, Ruff 0.16.7 and mypy 2.3.1. Ruff lint and
format passed, strict mypy passed 12 source modules, and pytest passed 1,183
cases with five explicit visualization skips. The selected suite included the
generic disturbance engine, spatial fields, conservation and accounting,
open boundaries, quantum consumers, runners, repository architecture and
language rules.

Six initialization modes across five independent profiles were compared after
every tick with one worker and two isolated interpreter workers, including the
shared delayed field/carrier Node clock. Snapshots, event order, local and global
totals, sources, dissipation, escaped quantities and modeled computation cost
were identical. Bounds, native event-program rejection and concurrent host caller
rejection were also exercised.

A headless acceptance run used `finite_fields.json` for eight ticks with four
workers. It completed with balanced accounting, eight disturbance Node tasks,
117 spatial Node tasks, 16 planning batches and a largest active batch of 19.
The run reported `display: none` and created no visualization. These checks
establish deterministic barrier behavior for the tested inputs; they do not
claim that parallel host scheduling speeds up small or inexpensive worlds.

## Localizing decay residue as the schema 2 default — 2026-09-13

Base: `5a2e21d` (main after PR #89). Schema 2 decay gained an optional
`residue` key. The default `"localize"` keeps the completed-link attenuation of
moving stock but deposits every removed fraction as stationary stock owned by
the receiving Node, so total spatial inventory is preserved and a thinning wave
comes to rest as whole units at known Nodes. The explicit `"dissipate"` value
selects the earlier loss law unchanged; the historical dissipative tests and the
records above were produced under that law and now name it explicitly.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, full affected pytest scope |
| Finite moving source | `finite_fields.json`, 40 headless ticks: injection 720, dissipation 0, localized deposits 720, final field total 720, conserved and balanced at every completed tick |
| Open example | `open_world.json`, 12 ticks: carried escape 72, spatial escape 20, localized deposits 52, dissipation 0 |
| New tests | 20-unit pulse keeps total 20 with deposits 10, 5, 3, 1, 1 under both field clocks; separate deposits before merging; deposits survive later arrivals; residue validation; runner identity `finite-localizing-v1`; parallel/serial equivalence on `finite_fields.json` and `three_mass_finite.json` |
| Visualization | Not requested or generated |

Deposits are never transported, decayed, sampled or read by rules, and the
schema 1 conservation audits still do not cover schema 2. This is a configured
integer law, not a derived particle, absorption or energy model.

Integration review of the Claude candidate added signed-vector, mixed-residue
and deposit-overflow atomicity checks: all 23 finite spatial-engine tests passed
on Python 3.14.7. The independent local-law review found no implementation
blocker and required distinguishing conserved signed inventory from moving flux.
The 40-tick headless `finite_fields.json` run at runtime source SHA-256
`061b1fcc2d6b210b6450b11ecb33ee8e1b8c479c33e222d21451c2927803d3a7`
completed with source 720, localized inventory 720 and zero dissipation.
At ticks 40, 80 and 120 the same probe retained 155 spatial Nodes and a
140-byte deposit tuple/payload allocation per Node. This is a Python-owned
deposit-storage measurement, not total process RSS or universal memory proof.
The existing merge and physics review Skills already require these boundaries;
no additional Skill rule was needed.
The integration affected check passed Ruff, formatting and strict mypy, with
2000 pytest passes and 5 visualization skips. One retention test encountered a
Windows file-replacement permission error; rerunning its entire 17-test module
in a fresh temporary directory passed. All 28 repository language, navigation
and hygiene checks also passed. Required CI is checked on the published head.

## Straight-ray field candidate and the inverse-square probe — 2026-09-13

Base: `ca51869` on this branch. `"transport": "ray"` (`isotropic-ray-field-v1`)
adds straight-moving rays that carry an integer heading and three accumulators,
a per-Node ray slot capacity, emission over a configured heading sequence, and
attenuation, deposits, escape and flux samples through the existing accounting.
The probe (`examples/inverse-square/`, deleted on 2026-09-17) measured it as a read-only
world/event audit at host Euclidean distance, not as an operational observer.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, 2,022 tests with five explicit visualization skips |
| New tests | `tests/test_ray_field.py`: DDA period, emission shares and cursor, per-tick totals and shell stock, receiver flux, localize/dissipate attenuation, explicit slot failure, open-boundary escape, configuration limits, runner identity; parallel/serial equivalence on `isotropic_rays.json` |
| Ray probe | 41-cubed open world, 4,096 headings at scale 24, 64 rays per tick, one 64-tick sweep measured: log-log slopes -2.25 (axis), -2.05 (face diagonal), -1.92 (body diagonal); flux per solid angle uniform to a 6 to 8 percent coefficient of variation over 72 detector patches at R = 4, 8, 12, 16; no empty nodes through R = 12 |
| Octant law on the same probe | Slopes -4.96, -3.40, -0.90; shell means exact `emission / (4R^2 + 2)` |
| Accounting | 544,195,584 emitted units resident, in flight or escaped; zero dissipation; balanced at every tick; finite fitted slopes, not asymptotic proofs |
| Visualization | Not requested or generated |

The result is geometric dilution of straight rays, not a gravitational law: no
constant, mass coupling or attraction is claimed, and node-level graininess at
large radius is finite direction sampling.

## Gravity probe on the straight-ray field — 2026-09-13

Base: `cc042ce` (main after PR #92). Configuration only, plus one engine fix:
a coupling reaction that amends a departing packet now keeps the rays on that
port, so rays pass through Nodes whose carriers respond to them (previously they
were dropped there). The probe (`examples/gravity-probe/`, deleted on 2026-09-17) couples
held and moving bodies to the ray flux with `mass x flux / D`, `D = 16`, and
reads the result as a read-only world/event audit at host Euclidean distance.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, full affected pytest scope |
| New tests | `tests/test_gravity_probe.py`: momentum toward the source proportional to mass within the integer remainder, combined momentum conserved, a body that falls through the source and oscillates; `tests/test_ray_field.py`: rays pass a reacting receiver unchanged |
| Held bodies | 41-cubed open world, 4,096 headings, 64 rays per tick, one 64-tick sweep measured: mass-1 acceleration slopes -2.03 (axis), -1.94 (face diagonal), -1.92 (body diagonal) against host `r`; `a x r^2 x D / emission` between 0.06 and 0.11 in every direction; identical acceleration for masses 1, 2 and 4 at every Node; combined momentum exactly zero |
| Falling bodies | Rate scale 64, start eight links out: masses 1 and 2 share every Node on every tick with momenta in exact ratio 2; the sparse field gives a few inbound kicks (momentum -20 and -40), one outbound kick, and escape through the open boundary at tick 139; the dense-field small-world test shows a bound oscillation instead |
| Visualization | Not requested or generated |

The coupling constant is the configured `1 / D`; the emission per tick plays
the role of the source mass. The reaction stays in the local momentum field at
the body's Node and never reaches the source, so this is attraction toward a
fixed source, not a two-body law. No physical constant is identified.

## Particle interaction probes — 2026-09-13

Base: `8b9f79f` on this branch. Configuration only. Each charged body emits its
own signed straight-ray field and responds to the others' with `-(charge x flux)`;
a bound pair converts into a free proton and a recoiling core through the
existing two-record conversion. Read as a read-only world/event audit.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, full affected pytest scope |
| New tests | `tests/test_particle_interactions.py`: head-on repulsion without sharing a Node with reversed equal-and-opposite momenta, attraction at rest, neutral crossing, matched kicks with unequal recoil, timed emission with mass 4 and zero momentum conserved |
| Dense field | 21-cubed open world, 512 headings all firing every tick: like charges turn at distance 2 (tick 13) and reverse; opposite charges meet at tick 14 and pass through; neutral bodies cross at tick 14 unchanged; a light body is pulled in or pushed out by the sign of the charge product; emission at tick 10 with the proton at one hop per tick and the core at one third |
| Self-field | With one shared field a moving body met its own rays at the next Node and pushed itself regardless of the other charge; separate fields per body remove this in configuration |
| Visualization | Not requested or generated |

No energy is represented, so encounters within one link produce unbounded
kicks; no species, constant or unit is identified.

## Local self-exclusion for ray emitters — 2026-09-13

Base: `1d28d5f` on this branch. A ray field may set `self_exclusion`: a
departing emitter carries the `(amount, cursor)` of its departure cycle and, on
arrival, subtracts the rays of that cycle whose first DDA step took the port it
left through from the flux and value it samples. Work is bounded by
`rays_per_tick`; only the record's own registers are read.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy, 2,035 tests with five visualization skips |
| Lone mover | Six axis rays, momentum 16, speed one quarter hop per tick: momentum stays 16 through every move with exclusion; without it the body reaches 7,696 in eight ticks from its own wake |
| Shared field | Like charges repel through one field (closest approach 2 at tick 13, both reverse); opposite charges meet at tick 14; neutral bodies cross; light body pulled in or pushed out by the charge product; emission unchanged |
| Positional laws | `emissions` is a keyword-only field on the coupling laws, so existing positional joint-law construction is unchanged |
| Visualization | Not requested or generated |

Self-field returning from any distance other than one link is not excluded; a
general self-field law remains the open hypothesis in `POSTULATES.md`.

## Funded emission, absorption and rays in the audit — 2026-09-13

Base: `09190d0` on this branch. The conservation audit measures a ray as a
quantum: its amount joins the declared spatial energy expression and
`amount x heading` is intrinsic momentum. An emission with `source: false`
pays each quantum from the record field of the same name, clipped to stock, and
`recoil_field` takes `-(amount x heading)`. A coupling in `absorb` mode banks
every ray that arrives at the record's Node into the same-named field and adds
`amount x heading` to `momentum_field`, from arrivals only, so an emitter never
absorbs its own fresh emission.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 58 files, 2,041 tests with five visualization skips |
| New tests | `tests/test_energy_audit.py`: funded emission debits and recoils with the audit closed; a stock of 5 emits 2, 2, 1, 0; escaped quanta are measured escape; an absorber banks five quanta with momentum (5, 0, 0); a moving absorber-emitter never eats its own wake; absorb validation |
| Radiation pressure | 21-cubed open world, lamp of 200,000 quanta firing 252 mirrored headings at 8 quanta per ray, sail of mass 64 four links away: 11,249,738 Node events checked with zero residual; at tick 12 the world holds 199,976 quanta and 24 escaped; the sail carries (512, 0, 64) from 32 absorbed quanta and the lamp's momentum is zero at every tick |
| Earlier probes | Head-on, light-beside-heavy and proton emission tables repeated unchanged at the new source |
| Audit cost | Every checked event re-measures every active Node and packet: 4 ticks of the probe take 1 s, 8 ticks 51 s, and the 512-heading, 40-tick version did not finish in hours, so the probe runs 12 ticks |
| Visualization | Not requested or generated |

Only the repulsive push closes this way. An attraction that pays for the
kinetic energy it creates has no local rule yet, and the charge probes still
carry no energy.

## Quantum-to-classical probes — 2026-09-14

Base: `3c52a08` on this branch, after merging main. Three host-side
measurements on existing rules only, in
examples/quantum-classical (`examples/quantum-classical/README.md`, deleted on 2026-09-17).

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,349 tests with five visualization skips |
| New tests | `tests/test_quantum_classical.py`: the dephased walk equals the classical chain with variance `t - 3/4` while the coherent walk is wider; quanta click as 0 or 1 and every emitted quantum is accounted for; capture attempts land on the pass ticks with charge and mass exact |
| Walk | 25 registers, 14 steps: coherent width exponent 1.005; record discarded every step or every second step reproduces the classical Markov chain exactly at every step (exponent 0.558 with the `-3/4` offset); every fourth step gives 0.778 |
| Counting | One quantum per tick over 4,096 golden-stride headings, six detectors per radius: values only 0 or 1; `rate x r^2` between 0.066 and 0.100 for r = 2 to 8, log-log slope -2.17; relative spread of window counts falls about twofold per fourfold window; 4,077 escaped and 20 in flight after the sweep |
| Capture | 10,000 seeded worlds of the causal charge example: capture fractions 0.6335, 0.2383, 0.0837, 0.0280 and 0.0165 uncaptured against 16/25, 144/625, 1296/15625, 11664/390625 and 6561/390625; chi-square 4.65 on four degrees of freedom; charge -1 and mass 1 at every tick |
| Visualization | Not requested or generated |

The mixers and instruments are explicit configured laws. Nothing here derives
a Hamiltonian, a collapse criterion or a species; the seam between the finite
quantum rules and the classical ones is measured, not explained.

## Signed-quanta gravity: attraction paid by the pulled body — 2026-09-14

Base: `3c52a08` on this branch, after merging main. A funded emission may emit
a negative amount, an `absorb` coupling takes the share
`amount x fraction / fraction_denominator` of each crossing ray and pays a
negative share from the record's own stock, never beyond it, forwarding the
rest; a ray field is absorbed or exchanged, never both.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,349 tests with five visualization skips |
| New tests | `tests/test_energy_audit.py`: a fraction 1/4 absorbs one quantum of each 4-quantum ray and forwards 3; negative quanta pull an absorber with stock 3 by 2 then 1 and credit the emitter; absorb and exchange on one ray field rejected. `tests/test_gravity_probe.py`: bodies pay exactly the momentum they gain, the far body takes its share of what the near one left, a body with stock 50 stops at -50 with the event audit passed |
| Held bodies | 41-cubed world, one mass per world, source of -1,048,576 quanta per tick over 4,096 mirrored headings: the three masses agree within 3 percent at every Node; mass-1 log-log slopes axis -1.96, face diagonal -2.37, body diagonal -2.29; `a x r^2 x D / emission` between 1.4 and 3.1; every body paid exactly the quanta of its absorbed shares; records plus rays in flight plus escaped equal the initial stock in all three worlds |
| Audited world | 16 ticks, 16 rays per tick, mass 4 one link above the source: 595,153 Node events with zero residual; body paid 30,720 quanta for momentum (1024, 1792, -694272); source credited 4,194,304 |
| Fall | Dense field of 512 rays per tick: masses 1 and 2 follow the same path tick for tick with momentum in ratio 2, pay from stock, pass the source and leave at nine tenths of a hop per tick without turning back |
| Visualization | Not requested or generated |

The source's stock rises by what it emits, and a radial fall through the
GameBoard `r = 1` singularity escapes at the speed cap: both are properties of
this candidate, recorded rather than corrected.

## Kerengonen phased rays — 2026-09-14

Base: `3c52a08` on this branch, after merging main. The optional `kerengonen`
key on a ray field gives every ray a phase step that advances per link; rays
merge only with equal phase, and the coherence of the rays resident at a Node,
from a fixed-point integer cosine table, gates the sampled value and the
absorbed share. Amounts are never changed by phase. Funded emission and
absorption are now booked as field reactions, so the runner's per-tick
accounting balances for them.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,355 tests with five visualization skips; the integer audit of physical modules passes with the fixed-point cosine table |
| New tests | `tests/test_kerengonen.py`: phase advance and wrap, merge by phase, exact coherence at equal, opposite and quarter phases, the two-lamp line reading 4, 0, 4, 0, 4 against a plain 4 everywhere with the audit closed, coherence-gated absorption (4 then nothing at the dark Node, 20 at the bright one, 20 at the dark one with a half-turn offset), runner identity `kerengonen-ray-field-v1`, six validation rejections, and the double-slit probe's composition and closure |
| Double slit | 31 x 31 x 3 open world, lamps at y = -3 and +3, 59 planar headings, 16 quanta per ray, 8 phase steps, 48 ticks: screen absorption 928 at the center, 704 at a quarter turn, 64 at a half turn, about one half in the wings, against a plain 928, 1376, 928; a half-turn offset on the second lamp inverts the even Nodes (0 at the center, 928 at y = +-2); quanta closed in all three worlds |
| Audited world | 8 headings, 24 ticks, five-Node screen: 1,280,412 Node events with zero residual, 160 quanta absorbed in phase at the center, energy 5,632 plus 512 escaped against 6,144 initial, momentum (-2112, 0, 0) against (2112, 0, 0) escaped |
| Unchanged | The plain ray field, the gravity, particle, radiation-pressure and quantum-to-classical probes keep their results without the key |
| Visualization | Not requested or generated |

Quanta that cancel are not redistributed; they continue and escape. That is the
candidate's open question, recorded in `POSTULATES.md`.

## Kerengonen lottery capture — 2026-09-14

Base: `3c52a08` on this branch, after merging main. `kerengonen.capture`
selects how an absorber takes a ray: `share` (the coherent share of the
amount, truncated toward zero) or `lottery` (the whole ray or nothing, drawn by
a local ticket seeded by `capture_seed` and salted by the ray met). The ticket
state is a record row, `absorb_tickets`; the same seed and rays repeat the same
clicks.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,357 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: the ticket rule and its bound; in-phase and dark Nodes take 18 and 2 quanta exactly like the share rule; at a quarter turn two seeds take between 2 and 16 whole single quanta where the share rule takes 2, with the audit closed on 800 quanta; unknown capture, a seed without the lottery and a seed at the modulus rejected |
| Single-quantum double slit | 96 ticks, one quantum per ray, two seeds: 154 at the center, 4 at the half turn and 152 at a one-lamp Node for both seeds and for the share rule; 127 to 135 at the quarter turn and 60 to 121 in the wings for the lottery against 2 to 6 for the share rule; absorbed totals 2,354 for either seed against 578; quanta closed in all three worlds |
| Unchanged | With `capture` absent the share rule and every earlier result stand |
| Visualization | Not requested or generated |

At full or zero coherence the lottery and the share rule are the same law; at
partial coherence the lottery turns the coherent share into a click rate on
whole quanta. The ticket is a configured local sequence, not a claim about
physical randomness.

## Kerengonen integration and ownership guards - 2026-09-14

Integrated main `53e44a51dd238dff34d5e7ced0f337e8f1c7341f` with the ray candidate
through `289499798058230323b005ecb09c4421fbb459bc`. This entry records the reviewed
`a5c17b3` snapshot; the later de Broglie commits were not part of that snapshot. Existing main's
quantum field-phase and causal-null features are preserved.

Independent physics review found and reproduced missing ray momentum in ordinary
runner accounting, physical-step trigonometric construction beyond integer
bounds, phase-blind self-exclusion, stale stock under delayed carrier plans,
cross-field capture seeds, partial unfunded negative lottery capture and an
emission I/O guard that admitted unrelated carrier changes. The integration fixes
these paths and rejects the unsupported delayed/response compositions explicitly.
An exhausted emission now performs one normally priced metadata-clearing cycle
before a later departure. The candidate contract records these limits.

Validation uses Python 3.14.7 with the intended checkout on PYTHONPATH:

- Final affected gate against `53e44a5`: **2,441 passed, five opt-in visual skips**
  in 238.08 seconds; Ruff lint/format and strict mypy passed. The selection follows
  changed providers and their consumers; no `--full` selection was used.
- Independent integration regressions: 18 passed in 1.04 seconds, including
  constructor-only immutable phase tables after cache eviction and the maximum
  phase count. The earlier pre-correction gate passed 2,423 tests but did not
  expose the now-preserved counterexamples; it is not reused as final evidence.
- Three actual 24-tick headless runner cases use
  `examples/kerengonen-double-slit/run_experiments.py`'s `document` with eight
  planar headings, `audit=True` and `screen_half=2`: ordinary phases, a four-step
  offset at the second lamp, and the plain ray control. The center absorber
  receives respectively **160, 0, 160** quanta; other four screen Nodes receive 0.
  Every completed tick passes component/escape accounting and the independent
  local energy/momentum audit. All cases start with 6,144 quanta and zero total
  momentum, end with 5,632 quanta and momentum (-2112, 0, 0) in the domain, and
  record escaped (512 quanta, momentum (2112, 0, 0)).
- Those three audit reports record 1,280,412 / 1,293,638 / 1,280,412 Node balance
  checks and take 63.42 / 70.88 / 73.01 seconds on this host while checks also run.
  These are read-only global audit costs, not model event costs or a speed benchmark.
- A separate reference probe compares 19,236 prepared sine/cosine entries across
  14 phase counts, including 4,095 and 4,096, with host mathematical reference
  values. All agree. Preparing 97 distinct near-maximum definitions retains only
  16 entries in each host table cache; traced additional allocations are
  3,116,560 bytes retained and 3,246,976 bytes peak. This measures host law/cache
  allocations, not total process RSS or world storage. Each live field retains
  at most two 4,096-entry immutable tables outside NodeState.

Verified runner source SHA-256 before and after all three cases:
`b44d9898a10b64b7609a4a57351d70a9b9898634856f51984bb4fd499c8d2fb7`.
Inputs, state, events and run metadata were retained outside the source tree under
`kerengonen-verified-runs-20260914` and follow the ordinary retention policy.
No visualization, simulator/package build or new physical species law was added.
Independent physics review gives a scoped pass; live PR/CI state supplies the
separate publication and merge evidence. Existing Skills already require these
ownership, arithmetic and provenance checks; no duplicate Skill rule was needed.

## Kerengonen carried phase: one lamp, two re-emitting slits — 2026-09-14

Base: `3c52a08` on this branch, after merging main. A record that absorbs on a
Kerengonen field keeps, per absorb rule, the phase step nearest the direction
of the coherent sum of what it took (`absorbed_phases`, a record row, from
integer cosine and sine tables), and an emission with
`"kerengonen_phase": "carried"` starts its rays at that phase plus one advance.
A carried phase requires an absorb rule on the same field for the emitter.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,358 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: a slit that re-emits the phase it absorbed makes a lamp's wave arrive at a Node three links on opposite to a second lamp's (reading 0), equal with that lamp offset four steps (4), partial at a fixed re-emission phase (3); a carried phase without an absorb rule is rejected |
| Single-source double slit | 31 x 31 x 3 open world, one lamp of 64 quanta per ray over a 117-heading forward cone for 64 ticks, an absorbing wall eight links on with re-emitting slits at y = -3 and +3, a 25-Node screen twelve links beyond: with phase, 2,430 at the center, 978 at a quarter turn, 140 at a half turn, about one half at three quarters, and exactly the single-slit value where only one slit's rays reach; without phase, two slits give exactly the sum of the two single slits at every Node; the wall keeps 332,800 quanta in both; every world closes on its initial stock |
| Unchanged | Constant emission phases, the lottery and the plain field keep their results |
| Visualization | Not requested or generated |

The wave's phase survives absorption and re-emission at a Node: two slits lit
by one lamp are two sources in the lamp's phase, and the fringe needs no
second lamp. The re-emission is over the field's whole heading set, a point
Huygens source; no diffraction law is derived from the slit's shape.

## De Broglie on matter rays — 2026-09-14

Base: `3c52a08` on this branch, after merging main. A ray may carry its own
phase advance per link, stamped at emission by `kerengonen_advance` from an
expression over the emitter's fields divided by a denominator and taken modulo
the phase steps; rays merge only with equal advance, and a Huygens slit
carries the advance of the largest share it absorbed with the phase.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,361 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: a ray's own advance overrides the field's, rays of different advance do not merge, beams of momentum 16 and 32 at `|p| / 4` carry advances 4 and 8 with phases in ratio two, a negative advance and one without the key are rejected, and a slit re-emits the absorbed advance (readings 2, 4, 0 for lamp offsets 0, 16, 48 on 64 steps); `tests/test_de_broglie.py`: the probe composes for every momentum and closes |
| De Broglie probe | Beams of momentum 16, 32 and 64 (advance 4, 8, 16) through Huygens slits at y = +-6, 117-heading cone, 64 ticks: first dark fringe at y = 4, 2, 1 as predicted, period 8, 4, 2; bright Nodes at 0; 0 and +-4; 0, +-2, +-4, +-6; ratios exactly one where only one slit reaches; the plain field gives exactly the sum of the single slits for every momentum; all twelve worlds close on their initial matter |
| Unchanged | Rays without their own advance use the field's; every earlier Kerengonen result stands |
| Visualization | Not requested or generated |

The rule `|p| / D` is configured, not derived; what the measurement shows is
that the GameBoard, the Huygens slits and the coherence gate carry it from the
source to the screen: wavelength inverse to momentum, three doublings in a
row. The beam is a held source; a record in flight is not yet a matter ray.

## Kerengonen guards reconciled with current main - 2026-09-14

Main `c3c39d035a1020f2acde0cbf2e80ee442e29fa03` includes PR #98 and its
per-ray advance extension. This reconciliation preserves that extension and the
reviewed ownership/accounting corrections from `a5c17b3`. Departure rows now keep
four integers: amount, cursor, phase and advance. Self-exclusion compares the
complete key, independently of later emitter changes. Clearing uses four zeros;
the fallback sentinel alone cannot keep an exhausted source active indefinitely.
These are fixed per-rule owner registers, not a new world index or ray history.

- The affected gate included architecture,
  locality, energy accounting, Kerengonen, de Broglie and the new guard cases:
  **2,448 passed, five opt-in visual skips in 208.61 seconds**. Ruff lint/format
  and strict mypy passed. The base was `origin/main` at `c3c39d0`; with the merge
  not yet committed, its merge-base was `53e44a5`, so this selection also covered
  the incoming main changes. No full-suite flag or simulator build was used.
- Independent re-review: scoped pass; all 22 guard cases passed. Added cases
  distinguish foreign advances, preserve departure state after emitter changes,
  select the largest actually absorbed share's advance, and distinguish explicit
  zero from field fallback. Existing Kerengonen/de Broglie tests also passed.
- Four actual headless runner cases use the reconciled source. Three eight-tick
  two-lamp controls absorb **20 / 0 / 20** quanta at the center (equal phases,
  opposite phases, plain rays). Each ends with 784 quanta in the domain and 16
  escaped, with zero combined momentum. A twelve-tick funded emitter with its own
  advance 2 on a field whose fallback is 1 exercises absorption and escape: the
  domain holds 595 quanta and momentum (0, -10, 0), while escaped rays hold 5
  quanta and momentum (0, 10, 0). Every completed tick passes ordinary accounting
  and the independent local conservation audit.

Verified runtime source SHA-256 before and after all four runs:
`ee714a5470fa98b4ceccf254c8182060e1af512184d018828a69f4f5e37a563c`.
Inputs, states, events and metadata are retained outside the checkout under
`kerengonen-reconciled-runs-20260914` with the ordinary artifact retention policy.
The bounded prepared-table/cache design is unchanged; the new metadata remains
fixed by configuration. The explicit delayed-owner and response-sampling limits
remain documented in the candidate contract. The configured momentum-to-advance
relation is not a derived de Broglie law.

## Bell test on the phased-ray field - 2026-09-14

Base: `2e50880` on `main`. Configuration only: no source module changed. The
new probe `examples/kerengonen-bell/run_experiments.py` runs the CHSH form of
Bell's test on `kerengonen-ray-field-v1` with the four settings and the
combination of the quantum owner's two-wing experiment, read as phases on a
360-step circle (0, 90, 53 and 307 degrees).

| Check | Result |
| --- | --- |
| Share rule, 288 worlds, hidden phase on a five-step grid | `S = 826177/589824 = 1.4007`, equal in every correlation to the local model `mean cos(phase - a) cos(phase - b)` computed from the cosine table independently of the update code |
| Lottery rule, single quanta, 96 worlds, 2232 pairs per setting | `S = 397/279 = 1.423` under the original draw; `386/279 = 1.384` re-measured after the lottery draw became the square of the ticket state (source `ae732df611ba461d40f355e13f4d335fcc82203bbfb760f43c77614bc777bc2f`); both consistent with 1.40 within the counting spread of about 0.05 |
| Plain ray field, same worlds without the key | every outcome +1, `S = 2` exactly |
| Quantum owner, same settings (two-wing Bell experiment) | `S = 14/5` |
| Closure | every world's quanta in records, in flight and escaped equal the initial stock; the audited world passes the local conservation audit with 21504 source and 21504 lamp quanta absorbed at each analyzer |
| New tests | `tests/test_kerengonen_bell.py`: five cases, 7.3 seconds |
| Affected gate against `origin/main`, including the merged two-wing Bell test, gallery and isotropy probe | 339 passed, four visual-only skipped, in 62 seconds; ruff lint and format passed |

Runtime source SHA-256
`f12f349495c0bfd156390a79a7f49fc5df9c368117b25604e212fe68798e676a`, Python
3.14.0rc2, headless; the harness took 4 minutes 14 seconds. The classical
value is the model's prediction, one half of the quantum owner's correlation
at every setting pair, and not a loss of visibility. No physical constant or
species is identified.

## Crossing null notices corrected locally - 2026-09-14

Base: `6d37bcd` on `main`. The opt-in null notice now carries the null's
ordering key (tick, position), every Node that records a null with a notice
keeps a null record (its unscaled weight and the scale it assumed), and a
notice ordered before the Node's own null that arrives afterwards is answered
with the exact correction `(1 - w s) / (1 - w s g)`, sent through a separate
six-slot correction bank. `OUTPUT_SLOTS` is twenty-four. The default profile
and the option's existing acceptance are unchanged.

| Check | Result |
| --- | --- |
| Crossing nulls at tick 4 on registers M and D of a three-register split | stale product `390625/177489` at the source, corrected to the conditional `25/9` at every Node by tick 7 with one correction, at D |
| Sequential nulls one and two ticks apart | `25/9` with no correction |
| Analytic targets computed independently in the probe | `625/481 x 625/369 x 19721/15625 = 25/9` |
| Spatial accounting | balanced at every tick in all three worlds |
| Existing envelope, notice, contract, interference, funded and field-phase suites | 243 passed before the new cases; `tests/test_null_notices.py` 18 passed with them |
| Affected gate against `origin/main`, shared with the emission-scale sweep below | 3013 passed, 32 visual-only skipped, in 1187 seconds; ruff lint, format and strict mypy passed on 120 source files |

Runtime source SHA-256
`6c5eb5f5151944a865ec91d2b7ffb786d7c56a898a02446733dc6bd78a2c4fdf`, Python
3.14.0rc2, headless. Several excitations in one domain remain outside the
candidate by construction, as the contract now states.

## Emission-scale sweep of the two-arm interferometer - 2026-09-14

Base: the crossing-null commit on this branch. Configuration only: the
two-arm harness gains `scale_configuration`, which raises the full source
emission to 25, 250, 2500 and 25000 units per tick at `phi = pi/2` and `pi`.

| Check | Result |
| --- | --- |
| Per-tick departure of the S emission from `amount x |a_S|^2` | below one unit at every amount and phase; 0.52, 0.8, 0, 0 at `pi/2` and 0.04, 0.6, 0, 0 at `pi` |
| Relative departure of the six-tick mean | 1.5e-3, 2.5e-4, 0, 0 at `pi/2`; 2.0e-2, 3.4e-3, 0, 0 at `pi`; exact on every tick at multiples of 625 |
| Accounting | balanced at every completed tick in all eight worlds |
| Affected gate against `origin/main` | the same run as the crossing-null entry above: 3013 passed, 32 visual-only skipped |

This is the emission-side classical limit only: the integer field becomes the
continuous law as the amount grows. The wave's dynamics are configured.
## A particle in flight as a matter wave, and the small-stock sweep — 2026-09-14

Base: `c3c39d0` on main after PR #98. Engine: an emitted amount below
`rays_per_tick` fills only as many headings as it has quanta and moves the
cursor on by that many, so a small stock sweeps the whole sequence in turn
instead of the same few headings every tick. Probes: the de Broglie beam and
the new matter-wave particle read the advance from a `wavenumber` field set
from the momentum of the flight, never from the recoiling momentum.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed on the affected scope: Ruff lint and formatting, strict mypy, 1,780 tests with five visualization skips |
| New tests | `tests/test_ray_field.py`: 2 quanta over a four-heading sweep take headings 0 and 1, then 2 and 3, then 0 and 1, while a covering stock still advances by the count; `tests/test_matter_wave.py`: the particle flies, stops on its tick, pays its matter out and the world closes |
| Matter wave | One particle of 479,232 quanta, momentum 32 or 64, a sixteen-tick train through Huygens slits at y = +-6: first dark fringe at y = 2 and y = 1, bright Nodes at 0, +-4 and at 0, +-2, +-4, +-6; ratios exactly one where only one slit reaches; the plain field exactly the sum of the single slits; the husk stops with the recoil its rays carried; matter closed in all eight worlds |
| De Broglie beam | Re-run on the `wavenumber` field: first dark at 4, 2, 1 for momenta 16, 32, 64, unchanged |
| Earlier versions | A one-tick pulse gave no fringe (the two paths meet only where they are equal); a 7,488-quantum train gave a momentum-independent pattern because the slits' small stock re-emitted over the same few headings, the engine fix above |
| Visualization | Not requested or generated |

The particle's matter lands spread as its wave, not at one Node; landing whole
at one place needs a causal retirement of the rest of the wave, which the
quantum layer has and the ray field does not yet.

## Kerengonen mirror: a standing wave between a lamp and a mirror — 2026-09-14

Base: `c3c39d0` on main after PR #98. The absorbed row keeps the heading of
the largest share; an emission with `kerengonen_mirror` (x, y or z) sends its
whole amount back as one ray along the mirror image of that heading, at the
carried phase and advance. The heading sequence must contain every image, the
emission must name a recoil field, and the emitter must absorb on the field.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,431 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: reflected rays travel -x with the field's advance, the mirror holds 4 quanta and the reversed momentum, the line reads 0, 2, 5, 7, 7, 5, 2, 0, 0, 2, 5 at advance 4 and 6, 1, 1, 6 repeating at advance 8, closure on 400 quanta, four validation rejections; `tests/test_kerengonen_mirror.py`: periods 8 and 4 at advances 4 and 8 on a shorter run |
| Mirror probe | Lamp at x = -16, mirror at x = +16, 8 quanta each way per tick, 96 ticks: periods 16, 8 and 4 for advances 2, 4 and 8, all as predicted by `64 / (2 x advance)`, readings from 0 at the nodes to 15 at the antinodes; a flat 8 without the mirror; the mirror ends with momentum +1016 along x; quanta closed in every world |
| Visualization | Not requested or generated |

A mirror across a GameBoard axis only; an oblique or partial mirror needs a
heading map beyond one sign flip.

## A thick screen behind the double slit — 2026-09-14

Base: `c3c39d0` on main after PR #98. Configuration only: the two-lamp
double-slit world with screens one, two, four and eight Nodes deep.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,432 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: a three-layer screen's first layer absorbs exactly what a one-layer screen does and the layers behind add to it, both worlds closed |
| Thick screen | Phased totals 13,280, 17,062, 18,752 and 19,682 for one, two, four and eight layers against a plain 21,408 absorbed entirely in the first layer; the first-layer fringe (928 at the center, 64 at the half turn) unchanged by the layers behind; every world closed |
| Visualization | Not requested or generated |

The thin-screen deficit is energy that lands deeper, not energy lost.

## Dissolution as an engine parameter — 2026-09-14

Base: `c3c39d0` on main after PR #98. A funded ray emission may carry
`"dissolve": {"after_ticks": N, "over_ticks": K}` instead of an amount: a
record row counts the record's cycles and keeps the stock it held when the
rule first saw it; nothing is emitted for `N` cycles, then that stock over `K`
cycles, never more than is left.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,434 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: a record of 10 quanta with after 3 and over 4 holds 10, 10, 10, 7, 4, 1, 0; a moving one flies while it holds quanta and stops when empty; dissolution on a sourced emission, an emission without amount or dissolve, and over_ticks 0 are rejected. `tests/test_matter_wave.py` on the engine schedule |
| Matter wave | The probe on the engine schedule with the particle stopping at its first quantum: first dark at y = 2 and y = 1 for momenta 32 and 64, bright at 0, +-4 and at 0, +-2, +-4, +-6, ratios exactly one beyond the slits' reach, the plain field exactly the sum of the single slits, matter closed; a particle that kept moving during its train gave first darks in place but a blurred fringe (0.40 and 0.36 at the dark Nodes) and the plain field no longer the sum of the single slits |
| Visualization | Not requested or generated |

A moving source during its train is a different experiment, recorded as such;
the schedule is local to the record and follows it wherever it goes.

## Can the ray be what it is not: whole landing, oblique mirrors, Euclidean fringes — 2026-09-14

Base: `c3c39d0` on main after PR #98. Three limits recorded for the ray were
put to the engine. Whole landing of a dissolved particle at one Node was
argued, not implemented: rays carry conserved stock at link speed, and no
local rule can retire the rest of the wave when one Node captures without a
signal faster than the rays, so the escape routes (domain-owned inventory or
sub-luminal matter rays with causal retirement) are recorded in the
postulates. Diagonal mirrors (`xy`, `xz`, `yz`) and partial mirrors (an
absorb `fraction`) were added; a ray field may set `"metric": "euclidean"`
(`euclidean-ray-pace-v1`): the slowest heading hops every tick and every other
ray waits at its Node by its pace, so every heading covers equal Euclidean
distance per tick.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,439 tests with five visualization skips |
| New tests | `tests/test_kerengonen.py`: integer square root, paces 2364/4096, 2364/2896 and 1 for the axis, face and body diagonal, reaches 6, 9 and 12 links after twelve ticks, closure on 400 quanta, an unknown metric rejected; a diagonal `xy` mirror returns +x along +y with nothing back along -x; a quarter-fraction mirror passes 3 of 4 and returns 1, closed. `tests/test_euclidean_pace.py` on the probe |
| Round front | One lamp on the 26 neighbor headings, twelve ticks: links metric reaches 12 links in every heading, Euclidean radii 12, 8.49 and 6.93 (spread 1.732, an octahedron); Euclidean metric reaches 6, 9 and 12 links, radii 6, 6.4 and 6.93 (spread 1.155, round to within a link); both closed |
| Euclidean fringe | Two lamps four links apart, 29 headings to a screen twelve links away, 64 steps at advance 16, readings summed over the last eight of forty ticks: links metric darkest 0 at x = -1 and 1 and a flat 64 from x = 3 to 9 (Manhattan path difference saturates at four links, a full turn); Euclidean metric darkest 0 at x = -5 and 5 with 64 at the center and 96 at the edges, where the predicted half turn falls at x = -5, -4, 4, 5; the plain field on the Euclidean metric reads 64 to 128 as one or two rays of each lamp are resident per tick; all closed |
| Visualization | Not requested or generated |

The metric is a configured choice: the GameBoard's Manhattan fringe and the
Euclidean fringe are both exact consequences of where rays meet, and the
Euclidean pace buys the round front with rays that are slower, never faster,
than one link per tick.

## Claim and gather: a captured wave lands whole at one Node — 2026-09-14

Base: `c3c39d0` on main after PR #98. The second escape route was built: a
ray field with `claim` (`claim-gather-ray-field-v1`) and a `pace` below link
speed. Rays carry a train (`train_field`, stamped or carried through a
Huygens slit); an absorb rule with `claim` opens a claim at the capturing
Node, which floods Node to Node at link speed with a parent port per Node;
free rays of the train that meet the claim turn homeward along those ports
and the claiming record takes them whole; where two claims meet the earlier
opening wins, then the lower origin, and the later root yields.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,446 tests with five visualization skips |
| New tests | `tests/test_claim_gather.py`: the isotropic gather tick by tick (first claim at tick 26, 1,875 Nodes claimed, 64 quanta at the screen with momentum zero, closed), the same world without a claim, a rival that clicks first and gathers 62 while the later root keeps 2, one double-slit landing at one root, claim and homing validation, rejected configurations, the identity, a quarter pace, and the event audit closing through capture, flood and gather (819,183 Node events on a 13 x 13 x 3 world, 13 gathered and 3 escaped before the flood) |
| Isotropic gather | 64 quanta at a quarter link per tick, screen six links away: first claim at tick 26, every quantum at the screen by tick 57, screen momentum (0, 0, 0), nothing escaped, closed at every tick; without the claim the screen keeps its line's 8; a rival four links away clicks first at tick 18, gathers 62 by tick 39 and the farther screen keeps 2 |
| Double-slit landing | 48 capture seeds on the Euclidean metric at half pace with 1/256 lottery clicks: 48 of 48 landed at one root with nothing in flight, closed; winner holds 0.585 to 1.0 of what reached the screen (median 0.891); landings by band against the fringe's share: `\|y\| <= 1` 6 of 8.2 expected, `2..3` 11 of 16.9, `4..5` 10 of 9.5, `>= 6` 21 of 13.5; on the links metric the same run put no landing within `\|y\| <= 1` because the Manhattan front reaches the outer Nodes first. Re-measured the same day with the lottery drawing the square of its ticket state: 48 of 48 landed, winner 0.614 to 0.992 (median 0.87), bands 5, 7, 13 and 23 |
| Visualization | Not requested or generated |

The landing is whole and takes time; the first-click bias toward the Nodes
the wave reaches first, and the pieces kept by captures that raced the
flood, are measured limits of the rule, not hidden by it.

## Bell's test on the ray: CHSH below the local bound — 2026-09-14

Base: `c3c39d0` on main after PR #98. A funded ray emission may name a fixed
`heading` (a directed emitter); an absorb rule may add `capture_salt` so two
detectors on one field draw their own ticket sequences; and the lottery now
draws the square of its ticket state, because the state is affine in its
salts and two records that met the same rays drew numbers a fixed distance
apart. The Bell probe (`examples/bell-chsh/`, deleted on 2026-09-17) puts two phased rays
from one source through plus/minus detectors whose capture probability is the
Kerengonen coherence with a reference ray at the setting phase.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,450 tests with five visualization skips |
| New tests | `tests/test_ray_bell_chsh.py`: aligned and opposite hidden phases land deterministically for three seeds, closed; one seed over the 64 hidden phases gives S = 1.5001 and E(0, 0) = -0.5312, below 2 and against the quantum 2.828; capture_salt at the modulus or without the lottery rejected. `tests/test_kerengonen.py`: a directed emitter fires every ray along -x and closes, a heading outside the list or with a mirror is rejected |
| CHSH | 16 seeds x 64 hidden phases x 4 setting pairs: E = -0.422, 0.326, -0.387, -0.346 against the two-lottery prediction -0.354, 0.354, -0.354, -0.354 and the quantum -0.707, 0.707, -0.707, -0.707; S = 1.481 (predicted 1.414, local bound 2, quantum 2.828); E(0, 0) = -0.525 (predicted -0.5); plus rates 0.47 to 0.51; no missing pair of 4,096; every run closed |
| Malus's law | Plus rate over 32 seeds at hidden phase 0, 8, 16, 24, 32: 1.0, 0.84, 0.53, 0.12, 0.0 against cos^2 1.0, 0.85, 0.5, 0.15, 0.0 |
| Re-measured under the squared draw | Single-quantum double slit, two seeds: 154 at the center, 4 at the half turn and 152 at the one-lamp Node as before; 122/128 and 121/118 at y = +-1, 79/82 and 85/81 at +-3, 93/96 and 96/110 at +-5, 112/110 and 109/101 at +-10; totals 2,340 and 2,347 against 578 for the share rule (first measurement 2,354 each); the claim-and-gather landing ensemble is re-measured in its own entry below |
| Visualization | Not requested or generated |

A local model's answer, as the theorem requires: the ray reproduces Malus's
law, the shared origin and no-signaling, and not the correlation beyond 2.

## Gathered gravity: claim-and-gather does not make dark matter — 2026-09-14

Base: `c3c39d0` on main after PR #98. Configuration only: the signed-quanta
gravity field with `claim`, a source whose train label advances every tick,
and one body per world with or without a claiming absorb rule. The question
was whether gathering a train to its catcher focuses the pull enough to fall
slower than the inverse square, the dark-matter signature.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,451 tests with five visualization skips |
| New tests | `tests/test_gathered_gravity.py`: on a 13-cubed world with 128 headings the claiming body pays more and is pulled more than four times harder than the plain one, both closed |
| Gathered gravity | 21-cubed world, 512 mirrored headings, one negative quantum per ray per tick, 60 ticks: plain axis pull 148, 24, 26, 26 at r = 3, 5, 7, 9 (the floor is the one axis quantum); claiming axis pull 2,962, 2,705, 2,395, 2,046 (slope -0.32), paid 9,548 down to 3,636; off axis at (r, 2, 1) plain 47.8, 49.9, 24.2, 0 and claiming 924, 745, 572, 0 (slope -0.71 over the crossed Nodes; no line crosses r = 9.27); at half pace and r = 5 the claiming pull falls to 243 while the body pays 11,045, a whole train's momentum cancelling; every world closed |
| Visualization | Not requested or generated |

The claim delivers a train's quanta to its catcher and the momentum of only
the part the flood can reach; the pull it makes is neither inverse square nor
flat, and it disappears when the gather is complete. No dark-matter
appearance from focusing.

## Bell's test with deterministic hidden variables: S = 2 exactly — 2026-09-14

Base: `c3c39d0` on main after PR #98. A third Kerengonen capture,
`threshold`: the whole ray is taken when its coherent share reaches one half,
so a detector's outcome is fixed by the hidden phase and its setting, with no
ticket. The Bell probe runs it with `--capture threshold`.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 69 files, 2,452 tests with five visualization skips |
| New tests | `tests/test_ray_bell_chsh.py`: the threshold run over the 64 hidden phases gives E = -0.5, 0.5, -0.5, -0.5, S = 2.0 and E(0, 0) = -0.9375, closed, below the quantum 2.828; `tests/test_kerengonen.py`: the capture wording |
| CHSH, threshold | 64 hidden phases, one run each: E(a, b) = -0.5, E(a, b') = 0.5, E(a', b) = -0.5, E(a', b') = -0.5, exactly the triangle-wave prediction; S = 2.0, the local bound; E(0, 0) = -0.9375; plus rates 0.5156; no missing pair; every run closed |
| Visualization | Not requested or generated |

Hidden variables instead of dice reach the bound and stop there, as Bell's
theorem requires of any local model; the quantum excess stays out of reach.

## Bonded rays: the split of postulate 4 and the quantum CHSH value — 2026-09-14

Historical branch evidence only. The integrated ordinary engine rejects bonded
activation; the current ownership boundary is recorded at the top of this file.

Base: `c3c39d0` on main after PR #98. Postulate 4 is split: energy, momentum,
matter and every controllable message move at most one Node per step; the
joint outcome of a bonded pair is answered for both ends at once by the bond
registry, one object for the world. A Kerengonen field may add `bond`
(`bonded-ray-field-v1`), an emission `bond_field`, an absorb rule
`bond_setting`; the registry answers the first question on a bond by an
even coin and the second so that the ends agree with probability
`(1 - cos(difference)) / 2`. The Bell probe runs it with `--capture bond`.

| Check | Result |
| --- | --- |
| `python tools/check.py` | Passed: Ruff lint and formatting, strict mypy on 70 files, 2,457 tests with five visualization skips |
| New tests | `tests/test_bonds.py`: 400 first answers split 150 to 250 each way, equal settings always disagree, a half turn always agree, a quarter turn agree 150 to 250 times of 400; seed at the modulus and a bond of zero rejected. `tests/test_bell_chsh.py`: equal settings never agree and a half turn always do for three seeds; one seed per slot gives E = -0.7188, 0.8125, -0.7188, -0.7188, S = 2.9689 and E(0, 0) = -1.0, above 2; bond seed at the modulus, bond_field and bond_setting without a bonded field, and a bond without kerengonen rejected |
| CHSH, bonded | 16 registry seeds x 64 slots x 4 setting pairs, the pair bonded by a configured label: E = -0.7188, 0.707, -0.7188, -0.7188 against the quantum -0.7071, 0.7071, -0.7071, -0.7071; S = 2.8634 (quantum 2.8284, local bound 2); E(0, 0) = -1.0; plus rates 0.47 to 0.52 on either side whatever the other side's setting; no missing pair of 4,096; every run closed |
| CHSH, bonded to the origin | The same run with `"bond_field": "origin"`, each ray stamped at birth with its Node and tick and carrying it to the detector: E = -0.6699, 0.6895, -0.6699, -0.6699; S = 2.6992; E(0, 0) = -1.0; plus rates 0.50 to 0.52; no missing pair; every run closed; both rays of a pair verified to carry one origin code |
| Visualization | Not requested or generated |

The three captures on one probe: lottery 1.48, deterministic hidden
variables 2.00, bond 2.86 against the quantum 2.83; the last needs the split
of postulate 4 and nothing else.

## Postulate 22: one integer per interaction - 2026-09-14

The registry below was then made bounded and idempotent (the entry that
follows); its numbers were re-measured there.

Base: `a686925` on `main` (after PR #116). The bond registry now draws one
number per bonded pair: the first question draws it and answers by its upper
half; the second question draws nothing and answers by the lower half of the
same number against the settings' difference. Postulate 22 states the rule for
every uncertain interaction. The lottery and the quantum owner's tickets are
unchanged.

| Check | Result |
| --- | --- |
| `tests/test_bonds.py` | 400 bonds: 800 questions, 400 numbers, first answers split evenly, equal settings never agree, a half turn always, a quarter turn about half |
| `tests/test_ray_bell_chsh.py`, one seed | E = -0.6875, 0.7188, -0.6875, -0.6875, S = 2.7813, E(0, 0) = -1.0, closed |
| Bonded Bell probe, 16 seeds, 1,024 pairs per correlation | E = -0.721, 0.699, -0.721, -0.721; S = 2.861 against the quantum 2.828 and the bound 2; E(0, 0) = -1.0; plus rates 0.49 to 0.51 whatever the other setting; 0 missing pairs; every run closed |

Runtime source SHA-256
`48ea5e8b167319719a7f25edbd3cea66b69fe5f3d57e1575b55099084061b880`, Python
3.14.0rc2, headless. The number is a hidden variable in Bell's sense, shared
between the two ends of a pair; no end can read it, so nothing is signalled.

## The bond as physics: a bounded, idempotent registry - 2026-09-14

Base: `cd5e2df` on `main` (after PR #118), with `integrate/focus-and-ray-updates`
merged. The bond registry drives ordinary Simulation again as the declared
split of postulate 4, and answers the objections raised against it: it holds
at most 4096 open pairs and releases a pair at its second answer; a question
repeated by the same end with the same setting returns the same answer with
no new number; the pair's one number is a fixed function of the seed and the
birth code (two salted ticket steps with a square between them, so that
consecutive birth codes draw independent numbers). Postulates 4 and 22 carry
the bounded wording.

| Check | Result |
| --- | --- |
| `tests/test_bonds.py` | 400 bonds: first answers 199, 187 and 185 of 400 positive on three seeds, quarter-turn agreements 208, 199 and 170; equal settings never agree, a half turn always; the same end asking again gets the same answer without a new number; the other end releases the pair; the 4097th open pair is refused |
| `tests/test_ray_bell_chsh.py`, one seed | E = -0.6562, 0.8125, -0.6562, -0.6562, S = 2.7811, E(0, 0) = -1.0, closed |
| Bonded Bell probe, 16 seeds, 1,024 pairs per correlation | E = -0.709, 0.762, -0.709, -0.709; S = 2.889 against the quantum 2.828 and the bound 2; E(0, 0) = -1.0; plus rates 0.48 to 0.51 whatever the other setting; 0 missing pairs; every run closed |
| Ray, bond, Focus, merge-contract, guard, Kerengonen, claim, pace, delay, contract, architecture, locality and configuration suites | 373 passed; document suites 97 passed |

Runtime source SHA-256
`9c3eedc70b2ba4d55142615bb1afe9b49dff846b204ef45830f4a83a122a81c9`, Python
3.14.0rc2, headless. A run above 2 sqrt 2 is counting spread: the registry's
law gives E = -cos exactly in expectation.

## An outside number source for bonded pairs - 2026-09-14

Base: `064f7be` on `main` (after PR #120). `bond.stream` hands the registry
each pair's number from configuration instead of its own sequence; the
second end answers from the pair's stored number. The Bell probe's
`--source uniform` and `--source biased` measure the door of postulate 22.

| Check | Result |
| --- | --- |
| Uniform outside source, 16 seeds, 1,024 pairs per correlation | E = -0.697, 0.699, -0.697, -0.697; S = 2.7911; E(0, 0) = -1.0; rate shifts 0.0 and 0.0049; every run closed |
| Biased outside source, same runs | E = -0.703, 0.670, -0.703, -0.703; S = 2.7792; E(0, 0) = -1.0; Alice +1 always; Bob's plus rate 0.8350 at Alice's `a` and 0.1484 at her `a'` for `b'`, a shift of 0.6866; every run closed |
| `tests/test_bonds.py`, `tests/test_ray_bell_chsh.py` | stream order, idempotent repeats, exhaustion, validation; one-seed uniform and biased sources pinned (S = 2.625 both, Bob's shift 0.6875 biased) |
| Affected gate against `origin/main` | 2716 passed, 7 visual-only skipped, in 1487 seconds; ruff lint, format and strict mypy passed |

Runtime source SHA-256 `0beb4d822bd98980e5947c8e8c20f76825e52dabe64aac8abf8346ecb67b467b`, Python 3.14.0rc2, headless.
The bias leaves the Bell value untouched, since the agreement law reads the
lower half of the number, and shows only in the marginal: a signal, as the
postulate's derivation states.

## Statistics of the bonded Bell value and the causal anatomy of the candidates - 2026-09-14

Base: `780a9c1` on `main` (after PR #123). No engine change. The Bell probe
gains `--sweep` (fresh pairs for every setting pair, binomial standard
errors, four replicas per level, the GameBoard compared with the registry alone
outcome by outcome) and `--causal` (at fixed hidden variable, how often an
outcome moves with the other end's setting). The postulates and the coupling
document name the assumption of Bell's theorem each candidate breaks.

| Check | Result |
| --- | --- |
| `--sweep`, 64 pairs per correlation, GameBoard, 4 replicas | S = 3.0938, 2.7188, 3.2188, 2.6875; mean 2.9297, predicted error of the mean 0.0791, spread 0.2668; expectation 2.828125; 1,024 of 1,024 GameBoard outcomes identical to the registry's; every run closed, no pair missing |
| `--sweep`, 256 pairs per correlation, GameBoard, 4 replicas | S = 2.8828, 2.8984, 2.8047, 2.8203; mean 2.8516, predicted error of the mean 0.0432, spread 0.0460; expectation 2.828125; 4,096 of 4,096 GameBoard outcomes identical to the registry's; every run closed, no pair missing |
| `--sweep`, 1,024 pairs per correlation, GameBoard, 4 replicas | S = 2.7383, 2.8672, 2.8887, 2.8887; mean 2.8457, predicted error of the mean 0.0228, spread 0.0723; expectation 2.828125; 16,384 of 16,384 GameBoard outcomes identical to the registry's; every run closed, no pair missing |
| `--sweep`, 4,096 pairs per correlation, GameBoard, 4 replicas | S = 2.8774, 2.8052, 2.8325, 2.8325; mean 2.8369, predicted error of the mean 0.0109, spread 0.0299; expectation 2.828125; 65,536 of 65,536 GameBoard outcomes identical to the registry's; every run closed, no pair missing |
| `--sweep`, 1,000 pairs per correlation, registry alone, 4 replicas | S = 2.8540, 2.8500, 2.8500, 2.8560; mean 2.8525, predicted error of the mean 0.0221, spread 0.0030; expectation 2.828125 |
| `--sweep`, 10,000 pairs per correlation, registry alone, 4 replicas | S = 2.8522, 2.8412, 2.8544, 2.8216; mean 2.8424, predicted error of the mean 0.0070, spread 0.0150; expectation 2.828125 |
| `--sweep`, 100,000 pairs per correlation, registry alone, 4 replicas | S = 2.8284, 2.8319, 2.8325, 2.8232; mean 2.8290, predicted error of the mean 0.0022, spread 0.0043; expectation 2.828125 |
| `--sweep`, 1,000,000 pairs per correlation, registry alone, 4 replicas | S = 2.8263, 2.8257, 2.8300, 2.8256; mean 2.8269, predicted error of the mean 0.0007, spread 0.0021; expectation 2.828125 |
| `--source agreement`, 16 seeds per slot, 1,024 pairs per correlation | E = -1, 1, -1, -1; S = 4.0, the Popescu-Rohrlich box; Alice's plus rate 0.49 at every pair, Bob's 0.51, 0.49, 0.51, 0.51; rate shifts 0.0 and 0.0156; every run closed: a bias in the agreement half moves no marginal and is not held to the quantum value |
| `--causal`, 256 hidden variables per candidate | lottery and threshold: no outcome moves with the other end's setting at either end (0 of 256); bonded: Alice's coin never moves with Bob's setting, Bob's answer moves with Alice's setting for 184 of 256 hidden variables at b' (0.7188, the law's 362/512 = 0.7070) and 0 at b; every run closed |
| `tests/test_ray_bell_chsh.py` | one seed of the agreement-biased source gives E = -1, 1, -1, -1, S = 4.0, even plus rates and rate shifts 0.0 and 0.0312; the registry's expectation is 181/64; 16 GameBoard pairs per setting pair equal the registry's 64 outcomes one by one; a hundred thousand registry pairs land within three standard errors of 2.828125; the lottery never moves an outcome with the other end's setting, the bonded pair moves Bob's answer with Alice's setting for 47 of 64 hidden variables at b' and never at b |
| Affected gate against `origin/main` | 2078 passed, 5 visual-only skipped, in 1216 seconds; ruff lint, format and strict mypy passed |

Runtime source SHA-256 `0beb4d822bd98980e5947c8e8c20f76825e52dabe64aac8abf8346ecb67b467b`, Python 3.14.0rc2, headless.
The GameBoard equals the registry pair by pair at every level: the Bell value
lives in the registry's law and the GameBoard adds transport. The 2.889 of the
first run was sampling spread on correlated samples. In Bell's terms the
bonded pair is deterministic, measurement-independent and
parameter-dependent; its unmoved plus rates are no-signalling, not locality.

## Redshift from delay growth on a closed row, read by a local clock - 2026-09-15

Base: `25ca82f` on `main` (after PR #124). No engine change.
`examples/relativity-probes/redshift_sweep.py` runs a train of twelve rays
under `ray_delay` and `delay_direction: "along"` across closed rows to an
absorbing eye with its own clock; `redshift_hubble.py` fits the law's shapes
to the public Pantheon+ Hubble-flow sample.

| Check | Result |
| --- | --- |
| Rows 16 to 96 at emission 16, budget 1000, baseline 7000 | row 16: z = 0.0682; row 24: z = 0.2159; row 32: z = 0.3864; row 48: z = 0.7727; row 64: z = 1.2955; row 96: z = 2.8068; duration ratio = 1 + z in every run; eye clock = tick count; twelve quanta conserved; field linear in age; hop-schedule slope 0.0116 to 0.0159 per link against `E / B = 0.016` |
| Emission 8, 16, 32 at row 48 | z = 0.284, 0.773, 2.329; slopes 0.0073, 0.0158, 0.0318 |
| Launch hop 1, 4, 8, 16 at row 48 | z = 1.818, 0.659, 0.773, 0.830 (the launch offsets of the ceiling) |
| Wave, phase per link / per interval / no emission | frequency ratio 0.583 (law 0.564) / -0.13 against -0.09 steps per tick / 1.000 |
| Moving bodies as light (not used) | emitters of a 24-row completed 320 to 436 cycles in 700 ticks with the train present and 700 without |
| `redshift_hubble.py`, 1,580 Hubble-flow supernovae, diagonal errors | linear load reading A / B: delta chi-square +1817 / +93 against flat LambdaCDM (Omega_m 0.334); quadratic load B: +62; fitted power law n = 1.4 (B): +4.5; best reading A (n = 5): +234 |
| `tests/test_redshift_sweep.py` | six tests: the quick row's gaps, z, duration ratio and slope; the control; the row length guard; the deceleration parameters of the shapes; the fit recovering its own shape; the wave's frequency ratios |
| Affected gate against `origin/main` | 167 passed, 2 visual-only skipped, in 66 seconds; ruff lint and format passed (no source file changed) |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.

## Redshift: one source, the full covariance and the shape's q0 - 2026-09-15

Base: `6ac2eff` on `claude/hopeful-bardeen-qgwlo6` (after PR #125). No engine change.
Three additions to the redshift probes after a review of the second
manuscript: a single-source mode of `redshift_sweep.py` (twelve lamps on one
Node, each emitting once at a fixed interval of that Node's clock, all rays
crossing the same distance), the full statistical-plus-systematic covariance
of the Pantheon+ release in `redshift_hubble.py` (`--covariance`), and the
deceleration parameter reported for the luminosity-distance shape rather
than for the scale factor.

| Check | Result |
| --- | --- |
| Single source, row 48, emission 16, budget 1000, baseline 7000, 1600 ticks | one Node emits every 24 ticks of its own clock (three launch hops at k_e = 8); D = 47; gaps at the eye 48, 50, 49, 47, 52, 49, 51, 50, 48, 50, 52 against 24 at the source; z = 1.0682, duration ratio 2.0682, ray-by-ray k_o / k_e = 2.0321; alpha measured 0.0155, from the hop schedule 0.0160; eye clock = tick count; twelve quanta conserved; field linear in age |
| Single source, wave, phase per link | frequency -0.5614 steps per tick at the source, -0.3227 at the eye, ratio 0.5747 against 1 / (1 + z) = 0.4835 |
| Single source, no emission, 700 ticks | gaps of 24 and z = 0.000, the interval at the source read against the configured launch hop (a first fix read it against the measured first hop, 7, and gave z = 0.143) |
| `redshift_hubble.py --covariance`, 1,580 objects | delta chi-square against flat LambdaCDM: linear load A / B +1891 / +106; quadratic load A / B +697 / +64; fitted power law n = 1.4 (B) +9.0; best reading A (n = 5) +252; LambdaCDM chi-square 1387.1 on 1,580 objects |
| Deceleration parameter of the shape | 1 - d''(0) / d'(0) by finite differences: reading A n = 5 gives +0.203 where the scale factor's -(n - 1) / n is -0.8; the manuscript's table carried the scale-factor value and is corrected |
| `tests/test_redshift_sweep.py` | seven tests, the single-source row added: on a 16-row at emission 32 the gaps are 36, 38, 36, 39, 37, 38, 37, 39, 34, 39, 37 against 24 at the source, z = 0.553, duration ratio 1.553, ray-by-ray k_o / k_e 1.5051, the two within 1.2 ticks per gap |
| Full gate against `origin/main` | 3,211 passed, 32 skipped, 0 failed in 28 minutes (the changelog entry widened the selection to the whole suite); ruff lint and format passed; the package built |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.

## Redshift: the wave read over its own span, the exponent under the covariance, and the sources - 2026-09-15

Base: `3874c06` on `main` (after PR #127). No engine change. A fourth
review of the second manuscript: the 19 percent gap between the single
source's frequency ratio and its prediction was a measurement-point
mismatch (the frequency was read twelve links along the path, the
prediction taken over the whole distance); the exponent scan now runs under
the full covariance as well; two citations were misquoted.

| Check | Result |
| --- | --- |
| Wave, train, phase per link, read from link 12 to the eye (span gap ratio 1.7143) | frequency -1.8182 steps per tick at the source, -1.0604 at the eye, ratio 0.5832 against 1 / 1.7143 = 0.5833: by construction, the phase difference between rays being conserved along the path |
| Wave, train, phase per interval | ratio 0.1396 against (1 + (nu_e - 1) / 1.7143) / nu_e = 0.1398 |
| Wave, train, no emission | ratio 1.000 |
| Single source, wave, phase per link, read from link 1 (span gap ratio 2.0682) | -0.6667 and -0.3227, ratio 0.484 against 0.4835 (the earlier 0.5747 read the source at link 12) |
| Single source, wave, 256 phase steps | -2.6667 and -1.2906, ratio 0.484 against 0.4835: independent of the phase resolution |
| Single source, wave, launch hop 16 (48-tick interval at the source), 3400 ticks | z = 1.072 (1.068 at launch hop 8), ratio 0.483 against 0.4826: converging with the tick resolution |
| `redshift_hubble.py --covariance`, exponent scan 1 to 20 in steps of 0.05 under each error model | reading B: best n = 1.40 under both, interval within one unit of chi-square 1.40 to 1.45 under the covariance, delta chi-square +9.0 against LambdaCDM; reading A: chi-square falls monotonically to the grid's edge (n = 20: +114) and its n -> infinity limit (D ~ z) gives +81 |
| Citations | Blondin et al. 2008: (1 + z)^-b with b = 0.97 +- 0.10 for the whole sample (the manuscript had 1.07 +- 0.06); Lubin and Sandage 2001: n = 2.59 +- 0.17 (R) and 3.37 +- 0.13 (I) before the luminosity-evolution correction (the manuscript had called them corrected values) |
| `tests/test_redshift_sweep.py` | seven tests; the wave test now checks the reading span, the span gap ratio and the single source's ratio |
| Affected gate against `origin/main` | 168 passed, 2 visual-only skipped in 103 seconds; ruff lint and format passed |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.

## Redshift: the exponent's interval refined, and the comparison of non-nested families - 2026-09-15

Base: `42cbd76` on `main` (after PR #129). No engine change. A fifth review
of the second manuscript: the interval within one unit of chi-square had
the width of one grid step, and the "three standard deviations" drawn from
delta chi-square = 9 does not follow for two families that are not nested.

| Check | Result |
| --- | --- |
| `redshift_hubble.py --covariance`, exponent refined in steps of 0.001 around the coarse minimum, interval ends interpolated | reading B: best n = 1.405 under the covariance (1.386 with the diagonal errors), interval within one unit of chi-square 1.35 to 1.465 (diagonal 1.335 to 1.448), delta chi-square +9.0 against LambdaCDM unchanged; reading A: monotonic to the grid's edge at n = 20, no interval |
| Wording | delta chi-square = 9 with one fitted parameter each is reported as a preference for LambdaCDM with no significance level attached (non-nested families); with equal parameter counts it is the Akaike difference, a relative likelihood of about 0.01 |
| Table 2 caption | the reading-A family's n -> infinity limit (chi-square 1468.5 under the covariance) is better than Einstein-de Sitter (2083.7); the caption no longer says "Einstein-de Sitter or worse" for all of reading A |
| Traceability | the single source's earlier source frequency, -0.56 read at link 12, is stated beside the corrected -0.667 read at link 1 |
| Affected gate against `origin/main` | 161 passed, 2 visual-only skipped in 26 seconds; ruff lint and format passed |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.

## Redshift: preference against exclusion, the clock's stakes, and the nearest literature - 2026-09-15

Base: `724241f` on `main` (after PR #130). No engine change. A sixth
review of the second manuscript, read as a standalone paper.

| Check | Result |
| --- | --- |
| Goodness of fit against model preference | covariance chi-square per degree of freedom (1,579): flat LambdaCDM 0.88, fitted power law (reading B, n = 1.4) 0.88, reading-A limit (n -> infinity) 0.93, quadratic load A 1.32, linear load A 2.08; "excluded" and "fails" replaced by "behind" wherever the shape passes on its own |
| `redshift_hubble.py` | the fitted power law (n = 1.4, reading B) is a named shape, so its binned residuals are reported and drawn: chi-square 699.31 diagonal (0.4429 per dof), 1396.1 covariance, +9.0 against LambdaCDM, as before |
| Single source against the continuum | the measured gap of 49.6 ticks is 1.2 ticks below the continuum's 50.8 and 2.0 above the launch-offset value of 47.6; the manuscript had said "within a tick" |
| Pantheon+ sample | 1,701 light curves of 1,550 supernovae; 1,580 Hubble-flow light curves kept |
| Tolman | Lubin and Sandage's exponents are reduced under an assumed q0 = 1/2 geometry, so they are not model-independent; the manuscript now calls the comparison an indication, not a test of the model |
| Clock | the stakes stated: a clock at r(t) cycles per tick reads (r_o / r_e)(k_o / k_e), and one that slowed as 1 / k would cancel the stretch |
| Literature | the cosmic-refraction models (Chen and Kantowski 2008) named as the nearest continuum relatives, with what the GameBoard adds and does not add |
| Figures | the law figure's legend moved outside the axes; the residual figure gains the fitted power law |
| Affected gate against `origin/main` | 161 passed, 2 visual-only skipped in 25 seconds; ruff lint and format passed (a first run reported four failures in `test_ray_integration_guards.py` whose assertion text was an older version of the file: stale pytest bytecode; the file passes directly and the gate passed after the caches were cleared) |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.

## Redshift: degrees of freedom, the emission interval, and two leftover sentences - 2026-09-15

Base: `e5ec321` on `main` (after PR #131). Manuscript only. A seventh
review, which judged the paper ready as a computational study after
consistency fixes.

| Check | Result |
| --- | --- |
| Degrees of freedom | the LambdaCDM row (Omega_m = 0.334, the release's own fit to this sample, not refitted) and the fitted power law each carry one shape parameter fitted to the sample and one offset: 1578 degrees of freedom for both, 1579 for the shapes with no fitted parameter; chi-square per degree of freedom unchanged at two decimals (0.88, 0.88, 0.93) |
| Table 2 caption | states both grid stages (0.05, refined to 0.001 within 0.1 of the coarse minimum) and the provenance of Omega_m |
| Emission interval | written Delta t_e: k_e for the train, 24 ticks for the single source in every run, so the control's k_e = 7 no longer reads as a 21-tick interval |
| Wording | "do not fit" in the introduction became "well behind LambdaCDM"; the closing paragraph names what the paper establishes before what would ground its cosmological reading |
| Affected gate against `origin/main` | 161 passed, 2 visual-only skipped in 26 seconds; ruff lint and format passed |

Runtime source SHA-256 `c70c279be058f8730358a9110a9a51a1c201e91f5f0d884641cbfc3ef263fb14`, Python 3.14.0rc2, headless.
