# KEY4: the key's middle, one scalar of the world's initialization, on node-all

Status: DRAFTED 2026-10-31 ~09:4x UTC, for the THIRD pair. KEY3's mathematician PASSED it on node-live 1794d474b, with
port conditions (P1 to P4). Its physicist did NOT PASS it, on one BLOCKING item: on node-all the laid middle is neither
the click dial's middle nor any tooth's birth (B1). KEY4 ports KEY3 onto node-all 9d75a4904 (origin/node-all). It folds
B1, the physicist's m1 to m7, the mathematician's P1 to P4 and MINORs 1 to 10, the Boss's rulings of 07:5x UTC
(BRIEF_PAIRS.md, last section), the ninth code reader's MINOR 6 (hcr9/REPORT9.md) and the Boss's ruling on MIN1's case
(c). The owner's word (05:5x UTC): "if it is an initialization number for the node, allowed, and all the rest generic,
it has to enter the initialization tensor, no? Or the node computes it by itself at initialization."

Files, all in key4/. Whole numbers; Rule3's carry the one division; paths by joinpath; Python 3.14 with -I (node-all
requires 3.14), nice 19, one process at a time, every probe run twice and byte-identical.
- tree_all/: node-all 9d75a4904 by git archive, read-only: its src, tests, tools and five worlds.
- tree_key4/: the copy. Its src differs in runner/load.py and runner/files.py; runner/plans.py (edging's return, its
  parameter's name and its docstring); one line of runner/run.py; the Click record's docstring in engine/state.py; and
  decoder/records.py's carded (key4_src.diff, 341 lines, written by patch_src.py). Its five worlds are migrate.py's.
- p_key4_all.py runs node-all's own side on tree_all. p_key4.py runs the read, its no's and W on tree_key4 against
  it. worlds4.py is node-all's prefixes/write.py procedure, with byte-level digests of every record and ledger.
- lay_*.diff (patch_lays4.py): the four lay tools ported to node-all. lay_key4/ ran the four on the copy's src and
  lay_all/ ran node-all's own click, mesh and well lays, once each.
- The runs' outputs, sha256 (each probe alike with its twin): migrate.py d43ff57823f64bac; p_key4_all.py
  da1f0481f03a9c42 (and every file it writes); p_key4.py e4f41cb8fc1fcba4 (and every file it writes). The lay.txt
  files: the copy's click lay 26a07de91d7de2f4 and node-all's 4077c2d9b5cc6eec; the mesh lay 2f314e6c51dd2243 on
  both; the live lay ba494a75a461ba65 and the well lay f4734d88505f329b, node-all's committed ones. pytest: node-all
  ee2d3ca982a0b34c, the copy 98ea27ba6d2ffac1; mypy 843649a0230c7553 on both; ruff ruff_key4.txt.

VERDICT FIRST:
- The one scalar is the key's middle: setting.json's "middle", a whole number of at least 0, laid once beside "ticks"
  and "gears". universe.json's chosen.key is retired by name. The field's words say "the key's middle".
- The node computes the rest at its initialization:
  - the click's unit, K = 2 middle + 1 (load.dial);
  - every edge side's dial, D = (kappa div senses) K (plans.edging), kappa read from the plan's structure: the Boss's
    ruling on MIN1's case (c), which writer H's line in edging builds; on the five shipped worlds node-all's kappa is
    already the structure's (S);
  - every side's tooth at its birth, D's middle, (D - 1) div senses (load.dialled).
  On the click and mesh worlds D = 3K, born at 3 middle + 1; on our bang and the live and well worlds D = K, born at
  the middle.
- D is odd by structure on every plan laid today (kappa 2 or 6). The load refuses an even D by name: the case of a
  monomial on an edge holding four legs, which makes kappa div senses 4 or 12 and D even for every middle (R7).
- edging returns its scale with its carry's remainder, which the load names (R8, the ninth code reader's K1). laid_out
  takes the scale from the load and no longer reads the retired key.
- A load promise, load.keyed, refuses by name a world that lays a second key anywhere, or none. The decoder names a
  card's key off the header's dial (m5, drafted in the diff).
- MEASURED, a check that can fail, against node-all's own runs: the copy reads the click world's migrated files, which
  hold no chosen key. It computes K = 50,811,429, D = 152,434,287 on 175 sides and 4,725 teeth born at 76,217,143, and
  gives node-all's 12,636 lines (0 differing) and end digest cb66502ed09837fe. Each no fails or is refused by name:
  an even dial at one tooth changes 102 lines; an even unit everywhere and the middle handed as the unit are refused,
  and change every line past the promise; another form and the read ignoring the key change every line; a second key,
  no key, a scale with a remainder and a four-leg monomial are refused, nothing loaded.
- The migration comes first and lands as one change. The five worlds' 13 records are node-all's line by line, but the
  header's two file texts and digests; the ledgers are node-all's byte for byte; the pins equal node-all's
  tests/tensor24_prefixes.jsonl byte for byte.
- The key's value goes to the owner with C7's provenance and THIRD7's period (528,480 or 1,585,440 rounds at 9K), and
  no key is picked for L's order (section 8).

## 1. Where the one scalar sits (DERIVED on node-all)

1.1 The file and the field: setting.json, the world's initialization. The field is "middle", at the setting's top:
    {"version": 1, "ticks": 5000, "middle": 25405714, "gears": [...]}.
    - The gears lay the initialization's entries indexed by (train, component, site). The middle is its one entry with
      no index, so every Node-clock reads the same one.
    - It is the key's middle: the middle of the click's unit K = 2 middle + 1, the file's key today. It is not the
      middle of the edge dial D, and not a tooth's birth (1.2).
    - It is not in universe.json's chosen block, the strengths. chosen.key is retired: the format names it with its
      reason (files.RETIRED), and the load names it as a second key.
    - It is named middle, not key, because its value is not today's key. Today's integer under the old name is refused
      (R6); under the new name it loads silently (N, the physicist's m6).
1.2 Kept apart from the teeth's initial values.
    - On node-all a click tooth stands on every edge side (t, u), at its own Node-clock and across each Spoke, not on a
      train. Every side's tooth is born at D's middle, (D - 1) div senses, D = (kappa div senses) K (MEASURED, L, on
      node-all's files and on the copy's alike):

| world | middle | K | kappa div senses | D, on every side | sides | every tooth born at | teeth |
|---|---|---|---|---|---|---|---|
| tensor24, our bang | 0 | 1 | 1 | 1 | 28 | 0 | 1,792 |
| tensor24-click | 25,405,714 | 50,811,429 | 3 | 152,434,287 | 175 | 76,217,143 | 4,725 |
| tensor24-live | 0 | 1 | 1 | 1 | 28 | 0 | 10,080 |
| tensor24-mesh | 0 | 1 | 3 | 3 | 63 | 1 | 11,340 |
| tensor24-well | 0 | 1 | 1 | 1 | 63 | 0 | 40,824 |

    - So the key's middle is a tooth's birth only where kappa div senses is 1. On the click and mesh worlds the teeth
      are born at 3 middle + 1, D's own middle: (3K - 1) div 2 = 3 middle + 1. This is the physicist's B1, and the
      field's words now say what it is: the key's middle, never the click dial's.
    - No field lays a tooth's own initial value. The gears lay a, b and the gear's tooth r, and the fine tooth is born
      at 0. A later field (VARY's generic initialization, THIRD6's hidden teeth) would be its own, and would move that
      tooth, not the dial (the physicist's KEY2 B1 (d)).
1.3 How the loader reads it, generically (the copy's runner/load.py and plans.py):
    - load.keyed reads the middle off the files as held, with the load's promise (2.1; load.py 180, called at 253);
    - load.dial computes the click's unit, K = senses middle + 1 (load.py 212, called at 256);
    - plans.edging lays every side's dial D = (kappa div senses) K, kappa read from the plan, and returns the scale
      kappa div senses with the remainder its carry leaves (plans.py 49 and 85 to 94; load.py 274);
    - load.dialled lays every side's tooth at its birth, (D - 1) div senses, and names a remainder or an even D (2.2;
      load.py 217, called at 277);
    - laid_out takes the Mesh edges' factor from the load, Loaded.scale (load.py 407). It no longer reads a key.
    No world is named, no number is typed but 1, and the read is the same for every world.
1.4 The 2, named: the pair's two ends, now an edge's two sides.
    - An edge (t, u) is passed on two sides, (t, u) carrying P and (u, t) carrying -P. Each side's tooth is born at D's
      middle, and the two sum to D - 1, so the carry's law gives q(t, u) + q(u, t) = 0 at every place.
    - The key's middle is K's own complement under k -> K - 1 - k, so K = 2 middle + 1. Of the two units whose middle
      the rule (K - 1) div senses gives as that middle (2 middle + 1 and 2 middle + 2), it is the odd one.
    - D's middle is D's own complement while D is odd: D - 1 - (3 middle + 1) = 3 middle + 1 at D = 3K.
    - The loader reads this 2 by its existing rule, senses, the Spokes along one axis (load.py 252; files.SENSES).
      That is another count, equal on this star (the mathematician's KEY2 MINOR 3).
    - K stays the click's unit (the physicist's reading): a two-leg monomial weighs kappa / 2 on both legs, so the
      edge weights scale the passing and the dial alike, by kappa div senses.

## 2. The load's promises (DERIVED; MEASURED in 4)

2.1 One key: load.keyed walks the universe and the setting as held. It names, each where it stands:
    - every field that lays a key anywhere else, at any depth (a train's card, the retired chosen.key, a setting.key):
      "a second key";
    - a middle that is not one whole number of at least 0 (a list per site, rows per tooth);
    - no key laid, so that no world falls silently to the click's unit 1.
    For a refused world, load builds nothing: it returns None with the departures, the form the load test already
    gives a refusal, and the run tool returns them with nothing written (run.py 270).
2.2 The dials: load.dialled reads what edging laid. It names:
    - a scale with a remainder: kappa over senses leaving anything, as kappa + 1 does (the ninth code reader's K1, whose
      scale and shares are kappa's own, so that only the remainder shows it);
    - an even D: (kappa div senses) K with kappa div senses even, the case of a monomial on an edge holding four legs
      (3.1). Its two teeth born at (D - 1) div senses would sum to D - 2, and the edge's books would open (NOT_CLOSED
      11).
    Each is named and nothing is loaded. Both are whethers over the load's own counts at the load, of the format's
    existing kind; the act holds no new test.
2.3 The format names the same lays by its table: setting.middle is required (files.MIDDLE, not OPTIONAL), and "key"
    is retired with its reason. The lay tools call load directly, without the format, so the promises sit in load.
    - The width (the mathematician's MINOR 3): no promise holds a dial's width, today or after. The format bounds the
      middle, as every file integer, by the width. K takes one bit more and D up to two more again (B1: a middle of
      128 bits gives K of 129 and D of 131). On node-all today D = 3 key already passes the width by up to two bits.
      The run's promise "wide" reads the counts a and b alone; the teeth are whole numbers of any size, and the record
      writes them whole.
2.4 Why one, and no field (the Boss's ruling; the physicist's KEY2 B1 (c)). A key varying across sites would lay a
    click-rate field: a clock with a larger dial clicks less for the same passing, the click world's mark of a deeper
    clock. The initialization would then set a dilation the clocks should show. It is not lawful. The physicist
    measured it on node-live (p_dilate.py): one Node-clock's trains on 3K wrote 129 click lines against its like
    neighbour's 161. On node-all one D stands on every side of the board (MEASURED, L).

## 3. What one scalar keeps (DERIVED on node-all)

3.1 Odd, K by construction and D by structure.
    - K = 2 middle + 1 for every whole middle.
    - D = (kappa div senses) K. kappa is the product of senses and of every legs count above two that a monomial on an
      edge holds, each once: 2, times 3 where a tie lies on an edge, times 4 where four legs do (edging, plans.py 80).
    - kappa is read from the structure (the Boss's ruling on MIN1's case (c): an existence test reads the factor with
      every chosen strength at 1). Writer H's one line in plans.edging on node-fold makes the code read it so. On the
      five shipped worlds the structural kappa is node-all's own (S, MEASURED); KEY4's diff carries no second form of
      that line.
    - Today's plans lay, per monomial: the notch on the square's slots (one train); the held rows' own spring (one
      train, the held rows twice, one leg); the tie (the held train's two positions one leg, the tied pair two: three
      legs on an edge); the hands' tie (two legs on an edge). So kappa is 2 or 6, kappa div senses 1 or 3, and D is odd
      for every middle.
    - A monomial on an edge holding four legs weighs quarters of kappa (3/4, 2/4, 1/4 by its trains' legs), so kappa
      takes 4 and kappa div senses is 4 or 12: D is even for every middle. No plan lays one today. The load refuses it
      by name (R7, MEASURED: kappa 24, D = 12 K = 609,737,148).
    - So the ODD rule on chosen.key retires with it. It never guarded D on node-all: today's rule reads the file's key,
      not the dial the act runs on (the mathematician's P1).
3.2 The books at a place. Each side's carry gives D q(t, u) = P(t, u) + k - k+, and the two sides of an edge carry
    P and -P at one D from teeth summing to D - 1, so q(t, u) + q(u, t) = 0 by the carry's law. With one D on every
    side, every side's q books its passing in one unit. With D's apart, the same q would weigh differently, and a
    place's sides could read balanced over a breach. One scalar gives one K, and the plan one kappa, so one D. Per the
    Boss's 07:5x ruling, the per-edge books close by construction (the record's faithfulness, a code check), and a
    place's sum is its across net, no reading of conservation.
3.3 The third click (the physicist's KEY2 B1 (b); THIRD7). THIRD7's coupled turn shears a triangle's edge teeth on one
    dial, 3D: 9K on the click world, 457,302,861 = 3^3 x 641 x 26,423 at its key, odd for every middle, 9 (2 middle +
    1), its middle 9 middle + 4 its own complement. One D on every side gives one triangle dial. EDGE1's edge teeth,
    when built, read the same D, and no edge birth is laid: KEY2's OPEN item on the edge births stays closed.
3.4 The run back, per side and for any odd D: Rule3's complement and the carry's sign law (EDGE1 1.4). MEASURED here:
    every record's run back is exact (section 5).
3.5 The 24 at the load (KEY2 MINOR 4): turn the files, then initialize. A turn permutes the sites and turns each gear's
    components, and moves no entry that has no index; kappa counts legs in the plan, which a turn does not change. So
    the turned files load the same K and the same D on every side, and act(g s) = g act(s) holds with the layout's
    dials unturned. The engine's 24 test applies: a scalar is invariant, and no per-site field can be laid (2.1).

## 4. The check that can fail (MEASURED on node-all's own runs; each side run twice, alike)

Node-all's side is p_key4_all.py: node-all's loader on its own files. The read's side is p_key4.py: the copy's load on
the migrated files, whose universe holds no chosen key, so no integer is handed to the read. 200 rounds, SCALE1's
window. The lines are compared one by one against node-all's 12,636.

| variant | what changes | K | D, every side's | lines | differing | end digest alike |
|---|---|---|---|---|---|---|
| U, uniform, by the read | nothing | 50,811,429 | 152,434,287 | 12,636 | 0 | yes |
| E1, an even dial at one tooth | D + 1 on the giver's side to the taker, site 0 alone | 50,811,429 | 152,434,288 there | 12,636 | 102 | no |
| E2, an even unit everywhere | K = senses middle + senses | 50,811,430 | 152,434,290 | refused by name; with that promise mutated away, 12,636 | 12,636 | no |
| O, another form, odd at this middle | K = axes middle + 1 | 76,217,143 | 228,651,429 | 12,312 | 12,636 | no |
| I, the read ignoring the key | keyed gives the unlaid 0 | 1 | 3 | 14,094 | 14,094 | no |
| M, the middle handed as the unit | K = middle | 25,405,714 | 76,217,142 | refused by name; with that promise mutated away, 12,474 | 12,636 | no |

- U is not an identity. The value moved is the world's own (migrate.py halves today's key), but the unit and the dials
  are the read's: E2, O, I and M change only the read, and each changes every line. D = 3K and the births 76,217,143
  (4,725 teeth) are computed by the node, read from no file.
- In every variant the end's counts (a, b, r, rd) equal node-all's: the click pushes nothing into the gears.
- E1 is the mathematician's even key at one tooth, now at one side of one edge: 102 lines.
- E2 and M lay an even D, and the load refuses each by name (2.2). Mutated past that promise, they run and change
  every line.
- The giver is train 3 and the taker train 4 by the loader's flags, as the click lay reads them.

The second keys, a broken scale and an even D by the plan. Each is refused, and nothing is loaded. The run tool returns
the format's departures for R1 to R6 and writes no record and no ledger.

| the lay | the load's promise | the format |
|---|---|---|
| R1, the giver's card lays its own odd key, K + 2 | universe.trains[3].key: a second key | universe.trains[3]: the key 'key' is not in the format, with the retired reason |
| R2, the middle laid per site, site 0's one more | setting.middle: one whole number ..., not a list of 27 | setting.middle: a whole number of at least 0 ..., not [...] |
| R3, KEY2's form, rows per tooth, the giver's at site 0 one more | the same, not a list of 135 | the same, not [[0, 0, 25405714], ...] |
| R4, universe.chosen.key kept beside the middle | universe.chosen.key: a second key | universe.chosen: the key 'key' is not in the format, with the retired reason |
| R5, no key laid | setting.middle: no key laid | setting.middle: ..., not None |
| R6, today's integer under its old name, setting.key | setting.key: a second key; setting.middle: no key laid | setting: the key 'key' is not in the format; setting.middle: not None |
| R7, a monomial of four legs on an edge (the giver's rows 14 and 15 and the taker's 20 and 21, factor 1, added at the load's join) | the edge dial 609,737,148 (12 K): even ... | (no file lays a monomial) |
| R8, the scale's carry leaving 1, as kappa + 1 = 7 does (7 = 3 x 2 + 1, the scale as it was) | the edge dials' scale: kappa over senses leaves 1 ... | (no file lays kappa) |

- R7, its promise mutated away: kappa 24, D = 12 K, every tooth born at 304,868,573, and an edge's two teeth sum to
  609,737,146 = D - 2 at birth. The carry keeps that sum modulo D, and an edge's books then open only where a side's
  tooth and its passing land on D - 1, one residue in D: 200 rounds wrote 12,636 lines and hit none (0 places). So the
  breach is the complement law's, exact at birth, and it shows in a click only where a tooth meets that one residue.
  The promise refuses it by structure, not by a count seen.
- N, today's integer under the new name, "middle": 50811429: the format and the load name nothing, since every whole
  number is a lawful middle. It loads at K = 101,622,859, D = 304,868,577, born 152,434,288. Its first-click record
  shows D on the header's dial and every card, and its click lines and end digest differ from node-all's pin: the
  pins catch it on the shipped click world (m6).
- B, the width: a middle of 2^128 - 1 (128 bits, the format's largest) passes both and loads at K of 129 bits and D of
  131. A middle of 2^128 is named by the format (the width) and not by the load, which the lay tools call directly
  (2.3).
- S, the structure (3.1): edging's scale as laid and with every chosen strength at 1 is 1, 3, 1, 3 and 1 on our bang
  and the click, live, mesh and well worlds. The click world with its hold at 0 gives 1 as node-all's edging lays it
  (D = K) and 3 by the structure (D = 3K): the ninth code reader's reading, which writer H's line settles.

## 5. The migration, first (MEASURED)

5.1 The shipped worlds, examples/tensor24* at 9d75a4904. Their files are 1794d474b's byte for byte (git diff
    1794d474b 9d75a4904 -- examples/ moves README.md alone), so migrate.py's files equal KEY3's, 15 of 15 (cmp).

| world | key today (chosen.key) | middle laid | K | D | births | laid by | records read |
|---|---|---|---|---|---|---|---|
| tensor24, our bang | 1 | 0 | 1 | 1 | 0 | by hand: no lay tool (stage 0b, 86ee3f5ed) | whole, 10 rounds |
| tensor24-click | 50,811,429 | 25,405,714 | 50,811,429 | 152,434,287 | 76,217,143 | click_lay/lay.py | 200; its first click, 1; 4 |
| tensor24-live | 1 | 0 | 1 | 1 | 0 | live_lay/lay.py | 200; 4; 4 |
| tensor24-mesh | 1 | 0 | 1 | 3 | 1 | mesh_lay/lay.py | 200; its first click, 20; 4 |
| tensor24-well | 1 | 0 | 1 | 1 | 0 | well_lay/lay.py | 200; 4; 4 |

5.2 Unmoved means, for each of the 13 records (node-all's write.py procedure, worlds4.py, the mathematician's MINOR 6:
    every world but our bang run 200 rounds, then to its first click, then 4 rounds; our bang whole):
    - every line after the header is node-all's byte for byte: the click lines (12,636 on the click world's 200
      rounds, 56,866 on the mesh world's) and the end line with its digest, its rounds undone, the run back exact and
      the end's teeth on every side;
    - the header is node-all's byte for byte but for its files: the board, the kinds, every train card's key, the dial
      and the birth (152,434,287 and 76,217,143 on the click world; 3 and 1 on the mesh world; 1 and 0 elsewhere);
    - the ledger beside it is node-all's byte for byte;
    - the header's file digests move with universe.json's and the setting's texts alone, the piece's never;
    - the copy's decoder reads every record with no cause, and node-all's decoder reads node-all's alike.
    The lines write.py writes equal node-all's tests/tensor24_prefixes.jsonl byte for byte, on node-all and on the
    copy.
    The three silent worlds (the mathematician's MINOR 8): our bang and the live and well worlds write no click line
    and lay no monomial on an edge (D = 1). There "unmoved" rests on what can still fail: the end digest (it holds
    every tooth at its birth, 0), the end's teeth, the ledger and the cards. A middle of 1 would move each of them
    (DERIVED: K = 3 = D there, every tooth born at 1).
5.3 The lay tools (lay_*.diff, patch_lays4.py, run once each in lay_key4/ on the copy's src; node-all's own click,
    mesh and well lays run once each in lay_all/):
    - click_lay lays MIDDLE = 25405714 in the setting it writes and in its own loads; its key-1 runs pass the middle 0
      and read the click's unit off the loader (D over edging's scale); item 3 drops the parity half (MINOR 4) and names
      C7 in place of "a chosen unit" (m3). MEASURED: it writes migrate.py's setting byte for byte, and its lay.txt is
      node-all's own run's but for the two lines naming where the key is laid (item 3 and the last line). node-all's
      own tool writes node-all's shipped setting byte for byte.
    - On node-all both read the key-1 swing as 0 and the window as not held. That is node-all's own reading, not the
      key's: its run_one sums each train's sides through a reshape that takes the reach axis in, so on the lay's one
      Node-clock it reads Mesh sides, which carry nothing there. It waits for the re-lay (README line 134).
    - live_lay, mesh_lay and well_lay lay MIDDLE = 0 in the setting each writes and in its own loads: 5 lines each.
      MEASURED: each writes migrate.py's setting byte for byte (135, 187 and 2,937 gears unmoved). The live and well
      lay.txt are node-all's committed ones byte for byte. The mesh lay.txt is node-all's own run's byte for byte;
      node-all's committed one predates its edges (mesh_lay.py changed at f71c19390, lay.txt at c0375a1db) and differs
      from both in its click counts alone (on the 125 rounds 7,592 click lines against 36,192, the held train's 4,302
      against 6,827 and the tied hand's 3,290 against 0).
    - Our bang has no lay tool: its middle 0 is laid by hand, as its one gear is.
5.4 The order (the mathematician's MINOR 7): one change, not two states. Today's format refuses a migrated file (no
    chosen.key; "middle" not in its table), and the patched lay tools need the copy's load. So the five worlds' files,
    the format, the load and edging, the lay tools, the decoder's guard and the tests land together. In the copy no
    world can run at the unit by default: an unmigrated world is refused by name (R4, R5).
5.5 What else moves with it, on node-all (the mathematician's P4 and MINOR 2; the physicist's m7):
    - Tests (MEASURED, pytest on node-all's 46 tests: 46 pass on node-all; on the copy 35 pass and 11 fail, each one
      laying the retired key or a setting with no middle; the decoder's, the worlds' (the pins), the engine's and the
      rest pass):
      - test_the_tensor24_files.py's departure table, one test: the key's rule, lines 41, 86 and 87 (fails at 299);
      - test_the_tensor24_load.py, two tests: CHOSEN with its key (line 30), held.click[-1] == CHOSEN["key"] (63)
        and key == scale x the chosen key (153); nothing loads (55, 128);
      - test_the_tensor24_run.py, three tests: the cards' keys against chosen.key (212), the pair world's key
        614,401 (168), whose middle is 307,200, the even-key case (242 and 249), and the width test's setting with
        no middle (334);
      - test_the_tensor24_edges.py, two tests: the test's key 1,000,003 laid as chosen.key (30), whose middle is
        500,001, and its scale read as the key over that key (81), which edging's scale replaces;
      - test_the_tensor24_half.py, three tests: load on {"gears": []}, a setting with no middle (151).
    - tools/tests_shape.py line 54: TENSOR24_LOAD's ROOM reason, "the chosen key and notch read into the click" (m7).
    - examples/README.md: line 11 (the setting's fields: the middle beside the ticks and the gears, with m6's line);
      lines 114 to 118 (the key CHOSEN in the universe file, and "a chosen unit of wind below the quantum", m3); line
      134 ("the edge key 3 times the key"); line 183 ("the edge key 3, the key 1 times kappa / two").
    - Probes that call load with a setting of no middle, each now returning None with "no key laid": drive_mirror (2
      calls), frozen_edge, g3_frame (and its chosen key 1), hand_per_quantum/probe.py (2) and its universe.json's
      chosen key, term5_books (2), term5_edge (2), term9_edge (2), and david_open's c1_quantum_per_mode,
      c2_held_by_the_clock and g5_draw; david_open's m3_beat and ANIMATE-SPRING's spring.py call an older load already.
      The four lay tools move by their patches (5.3).
    - Unmoved: the decoder's tests, the record's schema, tests/tensor24_prefixes.jsonl and tools/tensor24_files.py
      (which reads load's departures).

## 6. The physicist's MINORs m1 to m7

m1 (the value's provenance). 25,405,714 is the file's key moved as (key - 1) div 2. The key, 50,811,429, was set from a
   run: the audit's C7, "the nearest odd whole to the seventh (a typed 7) of the giver's largest swing at key 1",
   named-open for the owner beside C5. So the slot is an initialization number in the owner's sense, but the number in
   it was set from an outcome on an earlier lay. Today's lay no longer reproduces it: on node-live it read a swing of
   687,744,000 at the key 1, 13 keys a beat (KEY3 5.3), not 7; on node-all its key-1 reading waits for the re-lay
   (5.3). The value stands only as the file's own (the Boss's 05:3x ruling, "the key stays the file's own, as laid")
   until the owner rules (section 8).
m2 (THIRD7). D = 3K is the click world's edge dial (MEASURED, L) and 3D = 9K the triangle's dial: both clock facts,
   both odd for every middle (3.3). At a steady passing THIRD7's path is periodic, a clock fact of the click world at
   its key (section 8). THIRD6's D^3 is no longer cited. THIRD7's road ("the key ... with a number to meet") is
   answered in section 8: no key is picked for L's order.
m3 (the click lay's words). The patched click lay (lay_click_lay.diff) strikes "a chosen unit of wind below the
   quantum" from its item 3 and names the key's provenance there: "the swing over the key, a clock fact; the key's
   value the file's own, set from a run at the key 1, the audit's C7, OPEN for the owner". Its docstring names C7 too.
   examples/README.md line 117 moves with it (5.5). The window's oddness now comes by construction; what remains of
   the window (K at most the swing) is a condition read, not a pick.
m4 (the node alone). Three candidates are now named, and each needs a picked form:
   - KEY1's edge entry c: key 1 at the unit, and the CHOSEN F as filed;
   - the gear's dial W(a) + W(b): it picks a form (which end, which slots) and is silent on the click world at the
     unit;
   - the ledger's (gate_s5 SCRIBE-STATUS-LEDGER and SCRIBE-OWNER-WORDS): the giver's norm read from the files with no
     run, 40^2 = 1600. It is even, so the edge dial 3 x 1600 = 4,800 is even and its birth 2,399 is one short of its
     complement; a read per Node-clock varies with the lay, a varied key; 1601, the whole lay's norm, is a sum of two
     hands' norms picked to be odd; and the ledger itself refuses an odd giver picked for the window.
   Node-all's node already computes the structural part of its dial: D = (kappa div senses) K, kappa from the plan.
   The scalar K's middle stays the initialization's. "The node alone" is in section 9's OPEN with the three tried.
m5 (the decoder). Drafted in key4_src.diff: decoder/records.py's carded names a train card whose key is off the world's
   one key, the 1.4 header's dial (or, in a header with no dial, the first card's). MEASURED (C, on the click world's
   first-click record, 81 lines, each card's key moved by senses):
   - the metric's card, a train no click line names, at 152,434,289: node-all's decoder reads it with no cause; the
     copy's names it: "line 1's train card 2 holds the key 152434289, off the world's one key 152434287";
   - the giver's card: node-all's paired names a side ("line 3's side to train 2 and its partner hold teeth not
     summing to the key less 1, 152434288"); the copy's carded names the card first ("train card 4 holds the key
     152434289, ...");
   - the record itself, and every W record, reads with no cause by the copy's decoder.
   No decoder test's fixture lays two keys (the cards' key 7 throughout), and the decoder's tests pass on the copy
   (5.5).
m6 (the new name). Today's integer under the new name, "middle": 50811429, loads silently at K = 101,622,859 and D =
   304,868,577 (N, MEASURED): every whole number is a lawful middle, so nothing can refuse it by its value. It shows
   on the record's cards and dial, and the pins catch it on the shipped click world (N: its first-click record's click
   lines and end digest both differ from the pin's). The fix is one line in examples/README.md beside the setting's
   fields: "middle: the key's middle, (key - 1) div 2; the record's dial shows the edge dial (kappa div senses)
   (2 middle + 1)" (5.5).
m7 (tests_shape). tools/tests_shape.py line 54 (node-all) holds TENSOR24_LOAD, the load test's ROOM reason: "the
   chosen key and notch read into the click". It moves with the load test (5.5). By the same file's size rule (tests/
   only shrink), R1 to R8 written as tests need room or deletions to offset them: the load test's CHOSEN-key lines
   (5.5) are the first to offset.

## 7. The mathematician's port conditions and MINORs

P1 (D's oddness): met by 3.1 and 2.2. D's oddness is shown by structure on every plan laid today, and the load
   refuses an even D by name (R7). The case is a monomial on an edge holding four legs.
P2 (laid_out's second read of the key): met. laid_out reads the Mesh edges' factor from Loaded.scale, edging's own
   (load.py 407), and no file key (the ninth code reader's MINOR 6: the scale comes from edging with its remainder,
   which the load names, R8).
P3 (the hunks): key4_src.diff is written against node-all 9d75a4904 itself; nothing of KEY3's diff is applied.
P4 (what else moves on node-all): 5.5, from a full test run on both trees (MEASURED).
MINOR 1 (THIRD7 superseded 6.3): met (m2; section 8).
MINOR 2 (probes calling load with no middle): named in 5.5, node-all's list.
MINOR 3 (the width): 2.3 names which promise holds what, and B measures it.
MINOR 4 (the click lay's parity half): the patched click lay drops it: "odd by construction, no parity read".
MINOR 5 (O): "another form, odd at this middle": axes middle + 1 is odd for even middles alone.
MINOR 6 (worlds.py): worlds4.py re-writes node-all's write.py procedure (the same worlds and order, REACH 200 for
   every world, the first click round, PREFIX 4, the same fields), and adds digests of every record line and ledger.
MINOR 7 (the order): the migration lands as one change, not two states (5.4).
MINOR 8 (the silent worlds): 5.2 says what "unmoved" reads there.
MINOR 9 (today's integer under the new name): N, beside R6 (m6).
MINOR 10 (ruff's output): ruff_key4.txt holds it, on the copy's whole src under node-all's pyproject.toml (ruff
   0.16.9): "All checks passed!" and "27 files already formatted". mypy strict under the same file: "Success: no issues
   found in 27 source files", on node-all and on the copy alike (mypy_tree_all.txt, mypy_tree_key4.txt).

## 8. The key's value, to the owner

The value goes to the owner in the batch, with three things beside it.
8.1 C7's provenance. 50,811,429 was set from a run: the nearest odd whole to a seventh (a typed 7) of the giver's
    largest swing at the key 1, on an earlier lay (the audit's C7, named-open for the owner beside C5). It is an
    initialization number set from an outcome. Until the owner rules it stands as the file's own, laid as its middle,
    25,405,714, and no key moves.
8.2 THIRD7's period, a clock fact of the click world at its key. The triangle's dial is 3D = 9K = 457,302,861 = 3^3 x
    641 x 26,423. THIRD7's turn L has orders 9, 160 and 2,936 modulo 27, 641 and 26,423, so L^N = I with N = 528,480.
    At a steady passing the path is periodic: N rounds where 3 divides the passing y, and 3N = 1,585,440 where it does
    not (the round's N-th power moves tau by D y; THIRD7's mathematician, B2, MEASURED at 3N). So the prime factors of
    the world's key fix the third click's memory at a steady passing.
8.3 No key is picked for L's order. THIRD7 names the road "the key ... with a number to meet": L's order on the
    triangle's dial must exceed any record at a steady passing. A key picked so that it does would be a strength
    chosen for an outcome, which the owner forbids (03:5x UTC). The order is a condition a world meets or fails: the
    click world at its key meets it for a record of fewer than N (or 3N) rounds at a steady passing, and fails it past
    them. The owner rules on the value; KEY4 moves none.

## 9. Status

DERIVED: the field and its generic read (1); K = 2 middle + 1, the 2 as an edge's two sides (1.4); the load's promises
(2); K odd by construction, D odd by structure on every plan laid today, the four-leg case even for every middle, the
books in one unit, the triangle's one dial 3D, the run back and the 24 at the load (3).
MEASURED: on node-all's own runs, the read reproduces the click world and its no's fail or are refused by name (4); the
five worlds' 13 records are unmoved line by line and their ledgers byte for byte, and the pins stand byte for byte (5);
the structural kappa is node-all's on all five worlds (S); the decoder's one-key guard (m5); the patched lay tools
write migrate.py's settings byte for byte (5.3); node-all's tests on both trees (5.5); ruff and mypy clean (MINOR 10).
OPEN: the key's value, the owner's (section 8); the node alone, three candidates tried, each needing a picked form
(m4); writer H's structural line in plans.edging (node-fold), until which a chosen 0 can still move kappa (S, the
click world at hold 0); the click lay's readings on node-all, which wait for the re-lay (README line 134); whether a
world meets the third click's condition (THIRD7).
No light and no matter on the board: every number here is a clock fact.
Not built: nothing in the repository changes; the copy is the candidate, key4_src.diff against node-all 9d75a4904.
