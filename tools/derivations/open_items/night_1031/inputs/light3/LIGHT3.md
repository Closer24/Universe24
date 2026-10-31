# LIGHT3: light's click lines, the echo with a turn at B, and the cone, read per clock

Status: DRAFTED 2026-10-31, 08:4x UTC, read by no hostile reader. It replaces LIGHT2 whole and builds on:
- the Boss's rulings of 07:5x UTC, both parts (BRIEF_PAIRS.md);
- the six rulings sent with both readers' reports: light2_math/REPORT.md (3 BLOCKING) and light2_phys/REPORT.md (4
  BLOCKING).

The code is node-all 9d75a4904 (= origin/node-all), taken by git archive into light3/all and read only.
- Against 4ce1aa9d7, only the decoder (shadow, clicks, records, the new guard sides.py) and two schema constants
  changed. The engine, the runner and the worlds did not.
- So the shipped mesh record is the same byte for byte: sha256 8768fdf6e51f1ce2..., as in LIGHT2 and NATURE1.

The freeze:
- Every probe takes its paths from its own folder (light3) and imports the engine from light3/all/src.
- Every record a probe reads lies in light3/runs or light3/tests. No probe reads or writes outside light3.
- The readers' built records and the physicist's dumps were copied into light3/tests/readers by cp, before any probe
  ran.

The probes, all in light3/:
- p_light3.py: the reading.
- p_tests3.py: the logic's tests, on 13 records built by hand (tests/case01 to case13).
- p_turns3.py: how many clocks turn, and the cone's never-reached set.
- p_diff3.py and p_diff3b.py: the reflector's board check, two records compared.
- lay_light3.py: the lay tool. It writes test worlds from the shipped files, never by the loader.
- drive.sh: the eight runs, by the runner's own tool.
- probe.sh and probe2.sh: every probe twice. All 16 outputs came out the same both times (out/twice.txt,
  out/twice2.txt).

Laws kept:
- one process at a time, under nice, after the load wait;
- whole numbers only, and no division in any probe.

Every record first passes the decoder's own guard (sides.paired). That guard reads the header's train-card keys, and
only for itself. No reading reads a header kind, a card name, a file, the setting or the board's sides.

## 0. The answer first

1. Rule L, per clock, with the medium a set of trains (section 1). Shipped mesh world:
   - The medium is {train 0}, 125 clocks. Trains 1 and 2 are matter, 122 clocks each.
   - The record cut after round 20 reads {0, 2}; from round 21 on it reads {0}.
   - The no is the click world: no Mesh meeting, so light's lines are NOT SHOWN.
2. The clock is the causal unit (section 2). Shipped mesh world:
   - 18,096 meetings join 369 clocks in 3 components, of 187, 91 and 91.
   - Of the 122 sites with two clocks or more, none has all its clocks in one component.
   - The cone per clock from round 20: 120 clocks reached at their first meeting's round, 62 only later, 187 never.
     The 187 are exactly one whole component.
3. The echo, with the turn at B (section 3).
   - B's give at b2 goes to the site that B's last light takes, at b1, came from.
   - Fronts round a closed board fail it: H1, H1b, R4 and R6 read NOT SHOWN, though each reads SHOWN without the turn.
   - H2 reads B = place 4 alone, with the hold (4, 5).
   - The uniform relay of matter passes it. With no reflector laid, it reads SHOWN on the physicist's ring180k excerpt
     and at the test key: 4 echoes on ring60k, 8 on ring180k.
   - 110 of the shipped world's 122 matter clocks that meet light turn somewhere.
   - So the yes is OPEN, by the ruling's own words.
4. The worlds, at the file's key (section 4): NOT SHOWN under the turn on all four (mesh, mesh180h, ring60, ring60h).
   The test key's SHOWN readings are the uniform relay's.
5. The reflector: the held hand's count laid at one site, a test's lay (section 5).
   - On the shipped 180 ring it changes 110 lines within the 125 rounds. All are B's own meetings at site 40 and none
     is a light line. On a ring of 60, the change spreads from round 100, after the second front crosses B.
   - Read in one record, it shows NOT SHOWN at the file's key. At the test key it shows the plain ring's 8 echoes and
     none off the laid B.
   - 3.4 (ii) leaves the owner's batch.
6. The face is out (section 6). A's count and B's hold are read in their own meetings.
   - 4 of 2,956 windows on the shipped record hold an own meeting of A.
   - A's count is 0 in every echo found anywhere, and B's hold is 0 in every one printed.
   - The steady clicking clock at A and at B is owed, with C-a's check.
7. A's quiet and the key (section 7): the key's road is KEY4's, and nothing here picks a key.
8. Then the conversions C-a, C-b, C-e, C-c, C-d, in that order (section 8).

## 1. Light's click lines: rule L per clock, the medium as a set of trains (DERIVED; MEASURED)

1.1 The reads. A click line (r, s, t) carries:
    - sides: one per edge of its clock at its own Node-clock, [u, q, k, k+];
    - across: its Mesh sides that carried, [u, p, q, k, k+].
    A meeting is a side of q not 0, read once from both its listings (the Boss's 07:5x ruling: a side at q 0 is no
    meeting). Its giver is the end whose q is below 0. It is "own" when both clocks stand at one site, and "Mesh" when
    they stand one Mesh apart.
    - A Mesh side is read here as a meeting of its two clocks: one give and one take of a quantum at one round.
    - Whether the decoder's own meeting reading (A4) counts a quantum across a Mesh as a meeting is DECODE3f's (the
      Boss's 07:5x ruling). The chains here need only that its two clocks pass one quantum at one round.
1.2 The rule.
    - A medium clock has Mesh meetings and no own meeting. A matter clock has an own meeting.
    - The medium is the set of trains with Mesh meetings and no own meeting by any of their clocks, each train named.
    - The matter trains are the other trains that meet. A and B of section 3 are taken among their clocks.
    - Light's lines are the Mesh meetings with a clock of the medium at one end.
1.3 MEASURED on the shipped mesh record (21,589 click lines, well formed by the guard):
    - 18,096 meetings: 4,442 own and 13,654 across a Mesh.
    - Per train, [medium, matter] clocks: train 0 [125, 0], train 1 [0, 122], train 2 [0, 122].
    - The medium is {0}, and no train is mixed. The physicist's per-clock count agrees.
1.4 When the set changes with the record's length (DERIVED from 1.2).
    - A train joins the medium set with its first Mesh meeting, while none of its clocks has met at its own site. It
      leaves for good at its first own meeting.
    - So a prefix's medium set is provisional and can grow and shrink. A train once read as matter stays matter. The
      reading is the whole record's, and the decoder names it so: "the medium on this record, to round R".
    - MEASURED: cut after round 20 the set is {0, 2}, since train 2's first own meeting comes at round 21; from round
      21 on it is {0}. So a reading taken before a train's first own meeting would take matter for light.
    - The mathematician's H4 (train 0 out, train 3 back) reads the set {0, 3}, both named.
    - At the test key, the set stays {0}, but train 2 is mixed per clock. On ring60k, 32 of its 56 clocks that meet
      meet only across a Mesh; on ring180k, 84 of 112. Read per train, they stay matter, because their train meets at
      its own site elsewhere. A reading per clock would call them medium. Named, and not decided here.
1.5 Its no. The click world (the shipped files, the run cut at 200 rounds, a test's cut) reads NOT SHOWN: 12,636 lines,
    6,723 meetings, all own.
    - DERIVED: the click world's mesh strength is 0. plans.crossing's coupling is the Mesh plan's factor, the mesh
      times the table's entry, so every Mesh edge passes 0 and no across side is written at any length of run.
    - There each site's three clocks are one component: 27 components of 3 clocks each.
1.6 Light's lines are first clicks: a Mesh edge lies on no triangle, and step.act carries every side by the plain carry
    (LIGHT2 1.6, SOUND for both readers).
1.7 NATURE1's board numbers stay board numbers, and no reading here reads them. Those numbers: the first lines step one
    site per two rounds, and sites 83 to 137 write nothing. No site index is read as a coordinate, and no round as a
    duration.

## 2. The clock is the causal unit: the meeting components and the cone (DERIVED; MEASURED)

2.1 A chain (the ruling) is meetings that share a clock, each at a strictly later round than the round its clock was
    reached at. The next link is given by the clock that took the last one, or by a clock that met it in a recorded
    meeting at a later round. Rounds are read by order alone. The directed chain (light links given by reached clocks
    alone) is measured beside it.
2.2 The components (MEASURED):
    - shipped mesh: 3, of 187, 91 and 91 clocks;
    - ring60: 3, of 90, 43 and 43.
    No site with two clocks or more has all its clocks in one component (0 of 122; 0 of 58). At every site the medium
    clock never meets the site's matter clocks, and no chain links them. This agrees with both readers.
2.3 Why (DERIVED, as the physicist gives it).
    - The medium's own grip books no edge: plans.edging books a monomial only when its value legs stand in two trains.
    - So every light line is the medium's meeting with the tied train one Mesh away.
    - The hop from the tied clock at a site to the medium clock at the same site is the Node-clock's act, not a
      meeting.
2.4 The cone per clock, from round 20's meetings (MEASURED, shipped mesh): of 369 clocks, 120 are reached at the round
    of their first meeting, 62 only later, and 187 never.
    - p_turns3: the 187 are exactly one whole component, the one round 20's meetings do not touch.
    - Its clocks begin from the lay through the board's act: the Boss's named gap, "the board's wave carries the
      influence ... with no click".
2.5 The per-Node-clock order, beside it and named a board check: a site is reached when any of its clocks is, and so a
    site's trains are pooled through the board's act, with no meeting.
    - At the file's key, every site with a meeting is reached at the round of its first one: 125 of 125 sites on the
      shipped record, 60 of 60 on ring60.
    - At the test key: ring60k 53 at their first round, 4 later, 3 never; ring180k 100, 12, 3.
2.6 measure.past is the board's cone: rounds between at least Meshes between, read on the board's sides and site
    indices. It is a clock fact (the act reads one Mesh a round) and the decoder's D8 check, never physics.
    - AUDIT2's B7: a Mesh click reads its partner's next count, so it can stand one Mesh past that cone.
    - The click world's cone is 2.4's, read by order alone, and it does not lean on measure.past.

## 3. The echo, with the turn at B (DERIVED; MEASURED)

3.1 THE RULE. A, a clock of a matter train, gives a light link at round g.
    - A's quiet: A's own next light meeting after g, at t, is a take. A's own meetings at its site may stand between;
      they are A's own count.
    - The turn at B: B is a clock of a matter train at another site. It gives a light link at b2, with g < b2 < t, to
      a clock at site P, and every light take B made in its last such round before b2, at b1, came from site P.
    - The chains: a chain of meetings from A's give reaches, before b1, a clock B took from at b1. A chain of meetings
      from B's give at b2 reaches, before t, the clock A takes from at t.
    - Read beside it: A's count, A's own meetings strictly between g and t; and B's hold, B's own meetings strictly
      between b1 and b2.
    - It picks no number, no distance and no duration, and it is decidable in whole numbers on a finite record.
3.2 The least quiet: t >= g + 3 on every record (DERIVED for all records; the mathematician's MINOR 5).
    - b1 > g, since B's giver is reached no earlier than g;
    - b2 > b1, by the turn;
    - t > b2, since A's giver is reached no earlier than b2.
    So A is quiet on light for at least two rounds.
3.3 Against a front going round a closed board (DERIVED). A front that goes round without turning has every matter
    clock take from one side and give to the other. No clock's give then goes to the site of its last take, so no B
    turns. MEASURED on the built records (p_tests3, every record well formed by the guard):
    - H1, one front round a ring of 6: NOT SHOWN; without the turn SHOWN, B at places 2 and 4.
    - H1b, a ring of 10: NOT SHOWN; without the turn SHOWN, B at places 2, 4, 6 and 8.
    - R4, one front once round a ring of four: NOT SHOWN; without the turn SHOWN.
    - R6, two halves through the antipode of a ring of six: NOT SHOWN; without the turn SHOWN, 6 readings.
3.4 The other built cases:
    - H2, a line 0 to 4 turned at place 4 only: SHOWN with B = (4, 2) and the hold (4, 5) for A = (0, 2), and the same
      B for A = (2, 2), an echo the record holds. B = place 2 is read for neither A.
    - H3, an out-and-back through a hop between two clocks of place 1 that never meet: no echo for A = (0, 2), since
      the hop is no meeting and no chain crosses it. The record does hold an echo for A = (1, 2), off B = (3, 2) with
      the hold (3, 4): A gives at 2, B takes from site 2 at 3 and gives back to site 2 at 4, A takes at 5. The rule
      reads that one.
    - H4: SHOWN, with the medium {0, 3}.
    - My own:
      - L1, an echo whose A and B meet their own sites every round: SHOWN, A's count 2, B's hold 0;
      - L2, A gives light between: NOT SHOWN;
      - L3, no give at B: NOT SHOWN;
      - L4, the back link in B's give's round: NOT SHOWN;
      - L5, a front out along a line: NOT SHOWN.
3.5 The uniform relay of matter passes the turn (MEASURED).
    - U, the physicist's ring180k excerpt (rounds 112 to 124), rebuilt balanced: A = (16, 2) gives at 112. B = (18, 2)
      takes from site 17 at 116 and gives back to site 17 at 118, and A takes at 124. SHOWN, under both chains.
    - At the test key, with no reflector laid, ring60k reads 4 echoes under the turn and ring180k 8. Their B's are
      (6, 2), (11, 2), (18, 2), (22, 2), (29, 2) and (34, 2), every one a tied clock like the others.
    - p_turns3, on the shipped record: 110 of the 122 matter clocks that meet light turn somewhere, from 0 to 31 turns
      each. A turn at B is the common case here, not the mark of a laid reflector, because in these worlds every
      light meeting joins a matter clock to a medium clock one Mesh away (2.3), and the quanta on such an edge go both
      ways.
    - None of the conditions tried singles out a laid B: the turn, both chains and A's own quiet are all met by the
      uniform relay. What a laid B changes is how much turns back and when, and reading that would mean comparing B
      with the other matter clocks in one record. That road is not derived here.
    - THE YES IS OPEN, by the ruling's own words: no condition has been found that both a front round a closed board
      and the uniform relay fail.
    - Named cases that order alone cannot tell from a turn: the antipode of an even lay (LIGHT2 3.3), a clock that
      takes from one front and gives into another, and the uniform relay.
3.6 Variants measured beside the rule: the directed chain; no turn; and the site quiet (a board check: no light line of
    any clock at A's site between g and t).

## 4. The worlds, read by the rule (MEASURED, every probe twice)

Echoes are counted under the rule: chains of meetings, the turn, A's own quiet.

| record | lines | components | cone own / later / never | echoes | directed | no turn | windows | A ticking |
|---|---|---|---|---|---|---|---|---|
| mesh, shipped | 21,589 | 3: 187, 91, 91 | 120 / 62 / 187 | 0 | 0 | 0 | 2,956 | 4 |
| mesh180h (held 2 at 40) | 21,589 | 3: 187, 91, 91 | 120 / 62 / 187 | 0 | 0 | 0 | 2,956 | 4 |
| ring60 | 15,352 | 3: 90, 43, 43 | 56 / 30 / 90 | 0 | 0 | 2 | 2,156 | 4 |
| ring60h (held 2 at 40) | 15,352 | 3: 90, 43, 43 | 56 / 30 / 90 | 0 | 0 | 2 | 2,140 | 4 |
| ring60k, test key | 5,055 | 4: 65, 34, 34, 3 | 38 / 26 / 72 | 4 | 2 | 6 | 272 | 0 |
| ring180k, test key | 5,439 | 7: 61, 61, 60, 60, 3, 3, 3 | 76 / 44 / 131 | 8 | 6 | 10 | 232 | 0 |
| mesh180hk, test key (held 2 at 40) | 5,439 | 7, as ring180k | 76 / 44 / 131 | 8 | 6 | 10 | 232 | 0 |
| click200 (a test's cut) | 12,636 | 27 of 3 | 81 / 0 / 0 | - | - | - | - | - |

- "A ticking" counts the windows holding an own meeting of A strictly inside.
- On every record the medium is {0}, except the click world's, which has no medium.
- Every record passed the guard, and every run's end line reads exact 1 (the runner's rewind).
- The site quiet (the board check) reads 0 echoes on every record.
- On ring60 the two no-turn readings, B = (1, 2) and (39, 2), are pass-throughs: B takes from one side and gives to
  the other. The turn removes them.
- The test key 10^8 + 1 is a test's, never the world's (section 7).

## 5. The reflector: the held hand's count laid at one site (a test's lay; MEASURED)

5.1 The lay (the Boss's ruling): the shipped mesh world with the held hand's first count, now and before, set to 2 in
    place of 1 at site 40, and nothing else moved.
    - It is a seed, not a strength: the world-maker's initialization, named a test's lay and never a shipped world.
    - mesh180h is it on the shipped ring of 180. ring60h is the physicist's, on a ring of 60. mesh180hk is mesh180h at
      the test key, a check of the rule only.
    - It sets the tied clock's spring at B (plans.holding, 2 hold f |k|^2), a site-local coefficient. So it lays B
      apart from its neighbours, a clock other than the medium.
5.2 The board check, two records compared (p_diff3, a check and never the reading):
    - mesh against mesh180h (the shipped ring, 125 rounds): 110 lines differ, all at site 40, all of trains 1 and 2,
      from round 44 to the end.
      - None of them has a different across field, and none stands in one record alone (p_diff3b, twice). It also
        follows from p_diff3's "at 1 site": a Mesh side is written at both of its sites.
      - So within the shipped run the lay changes only B's own meetings, its tie with the held hand, and no light
        line anywhere.
    - ring60 against ring60h: 1,095 lines differ, at 24 sites. The first is at round 44, site 40, train 1. At the
      rounds printed (44, then every tenth round), only site 40 differs through round 90. From round 100 the
      difference spreads both ways:
      - round 100: 8 sites, 35 to 42;
      - round 110: 13 sites, 32 to 44;
      - round 120: 21 sites, 28 to 48;
      - round 125: 24 sites, 27 to 50.
      This reproduces the physicist's B4. His own caveat stands: on a ring the second front also crosses B, so what
      moves back toward the lay's side mixes the turned part with the passed part.
    - So on the ring of 60 the lay acts from B on light's lines, both ways. On the shipped ring and run, only B's own
      meetings show it.
5.3 The one-record reading by the rule:
    - mesh180h: NOT SHOWN under every variant, the same as the shipped record. Its light lines are the same lines.
    - ring60h: NOT SHOWN under the turn; without the turn, the plain ring's two pass-throughs.
    - mesh180hk, the test key: every reading past the record's name is the same as ring180k's. That is 8 echoes, all
      of the uniform relay, and none with B at site 40.
5.4 So the lay is lawful (the ruling) and acts from B on the board (5.2, on the ring of 60). In one record its echo is
    NOT SHOWN, for three reasons:
    - within the shipped run its turn does not reach the light lines;
    - at the file's key, A's quiet on light holds only in short windows (2,956 windows, of which 4 have A ticking);
    - where a window does hold a turn, nothing in the order tells the laid B from the uniform relay (3.5).
    LIGHT2's 3.4 (ii), a new coupling, leaves the owner's batch: the lay is the reflector. The square's road leaves too
    (the physicist's m3): it is a loader rule written for an outcome, and the square writes no click line.

## 6. A's count and B's hold: the face is out, the steady clicking clock is owed

6.1 The FACE2 ruling: a clock's own count is its own meetings between two of its meetings, and the face is a board
    field that no conversion reads. So:
    - t2 - t1 is A's own meetings strictly between its give and its take, while A is quiet on light;
    - B's hold is B's own meetings strictly between b1 and b2.
    LIGHT2's face field and its strict variant are withdrawn. The strict variant matched LIGHT2's verdicts only
    because A writes no line at all in those windows (the physicist's m7).
6.2 MEASURED:
    - shipped mesh: 4 of 2,956 windows hold an own meeting of A;
    - ring60k and ring180k: 0 of 272 and 0 of 232, so A's count is 0 in every echo found there;
    - B's hold is 0 in every echo printed (the first three of each variant) and on U.
    So wherever the order reads a turn here, A has counted nothing between, and 2r would be 0.
6.3 Owed, by name: the steady clicking clock at A and at B, a matter clock with own meetings while it is quiet on
    light.
    - Its count must not be the round in disguise (the physicist's B3 (iii)). A clock that meets at every round
      counts rounds, and then no moving clock could count less.
    - C-a's check: two clocks at rest read each other at one 2r, A to B and B to A. The echoes are repeated and read
      alike before B's hold is subtracted (B3 (iv)), and the earliest chain each way is light's path (B3 (v)).
    - No world here lays such a clock. Whether a lay of the held hand gives one, by its own spring, is OPEN.

## 7. A's quiet and the key (ruling 6)

- A key set so that light falls quiet would be a strength chosen for an outcome. The key's road is KEY4's (one scalar,
  the key's middle, laid once), and whatever quiet follows is the world's. Nothing here proposes a key.
- At the file's key the record is a readout. Key 3 divides every passing (the Boss's 07:5x ruling: their gcd is
  30,000), so the click teeth never move. The physicist measured 41,376 of 41,376 sides at their birth.
- The test key 10^8 + 1 is the file's spring plus 1. It is no candidate, and it stands here only as a test's, never
  the world's.

## 8. The conversions after this text (Big Pic's order, the face replaced)

1. C-a, time and distance by echo: 2t and 2r from A's own count at its give and its take, less B's hold.
   - Needs: the steady clicking clock at A and B (6.3), and a world whose echo reads SHOWN by a condition 3.5 lacks.
   - Its check: two clocks at rest read each other at one 2r.
2. C-b, the interval t1 t2.
   - Needs: C-a for two observers echoing one event.
   - Its check: one product.
3. C-e, lengths and isotropy.
   - Needs: C-a along three long axes (the mesh world is a line).
   - Its check: the 24 keep the echo distances.
4. C-c, Bondi's k and the twins.
   - Needs: the moving-clock world, beside C-a's pieces.
   - Its checks: k alike both ways; k_AC = k_AB k_BC by cross-multiplication; the free path's own count the greater.
5. C-d, the redshift.
   - Needs: two steady clicking clocks at two depths, and a well whose clocks click.

Rule L can be built in the decoder now; shadow.echo reads "no rule yet". The echo rule can be built with its yes named
OPEN: at the file's key it reads NOT SHOWN on every shipped world.

## 9. The readers' items

The mathematician:
- B1, a turn at B: built (3.1). H1 reads NOT SHOWN, and H2 reads B = 4 alone with the hold (4, 5). The cases order
  alone cannot tell are named (3.5).
- B2, chains through meetings: built (2.1). The components are named (2.2), and the cone is per clock (2.4).
- B3, the reflector: laid at one site and run, at the file's key and at a test key (section 5). It is no longer
  asserted.
- M1, the medium a set, with prefixes: 1.2 and 1.4.
- M2, built records balanced: every record passes the guard, and no event repeats.
- M3, file names: case01 to case13, one per case.
- M4, probes inside their folder: the freeze.
- M5, the least quiet: 3.2.
- M6, A's own quiet: 3.1, with the site quiet as a board check.
- M7, the earliest b1: replaced by the last take (3.1).
- M8, click200 frozen: runs/click200.

The physicist:
- B1, through clocks: 2.1 to 2.5.
- B2, a front and the uniform relay: 3.3 and 3.5, with the yes OPEN.
- B3, the face out: section 6.
- B4, the held hand: section 5. Reproduced on ring60h; on the shipped ring it shows only in B's own meetings within the
  run.
- m1, per clock and the whole record: 1.3 and 1.4.
- m2, the key: section 7.
- m3, the square: 5.4.
- m4, the lay's interior as geometry: dropped, and the site readings are named board checks (2.5).
- m5, file names: case01 to case13.
- m6, the freeze.
- m7: 6.1.

## 10. Standing

- DERIVED:
  - rule L, its set reading and its prefixes (1.2, 1.4);
  - the click world's no (1.5);
  - the least quiet (3.2);
  - the turn against a closed board's front (3.3);
  - why the medium and its site's matter never meet (2.3);
  - measure.past as a board check (2.6).
- MEASURED, each twice (out/twice.txt, out/twice2.txt): 1.3, 1.4, 1.5, 2.2, 2.4, 2.5, 3.3 to 3.5, section 4, 5.2,
  5.3 and 6.2.
- OPEN:
  - the echo's yes: a condition that both a closed board's front and the uniform relay fail;
  - the steady clicking clock;
  - per-clock or per-train matter at the test key (1.4);
  - C-a to C-e.
- Not claimed: no speed, distance or cone of light is read from a site index or a round.

Questions for the Boss:
1. May the echo rule be built with its yes named OPEN?
2. Is a one-record comparison of clocks' counts (B's turn against the other matter clocks') a lawful road to the
   condition 3.5 lacks, or a board label in disguise?
3. Is a lay of the held hand that makes A and B steady clicking clocks the world-maker's to lay?
4. Matter per train (as ruled) or per clock, where a train's clocks split (1.4)?
