# The record's schema 1.2, proposed (Animate)

The asks:
- Sofer's owed line (5) of 6494833685 ("the scheduler on a full board and schema 1.2"), and the Boss's gaps G1 to G7 (ANIMATE-DECODER-CLOSURE, part 2);
- decisions 36 and 37 (the Boss's 6496331673): no exception to a generic rule, the time gear one train among the others, and masses measured only in clicks, with the Boss's ask of Animate there: "the mass reading on the record, as the definition";
- Sofer's 6496692228, item 6: the toy told weights by kind (now one formula, ANIMATE-SCHEDULER, item 7);
- decision 40 (b), the slot rule: a full slot refuses after the split click's draw, and the refused quantum goes back to its giver by 5.1's books line.

It takes in decisions 33 to 39 and decision 40 (b), the one rule of ANIMATE-SCHEDULER, and B's record (ANIMATE-B-RECORD).

It is a proposal for the Boss, whose schema it is. Nothing is built: the decoder's code waits with the build (decision 32). `python -I lines.py` writes example lines from the draws the one rule makes and reads them back (lines.txt).

## The answer

1. **1.2 is a minor version.** Every 1.1 record stays readable as it is. 1.2 adds fields and retires one line kind (Turnover). Under decision 40 (b) it drops one field it had proposed, back (G6).
2. **No field holds a train apart.** The header names no switch (decision 33), no time gear and no seed (decisions 36 and 37). The time gear's count is one train's line in the ledger, like every train's. Every field has one form for every train, every part and every take.
   - **Under decision 39** the great clock is the metric's ten gears: the rate (the lapse) and the length (the ruler), A1 each; the lean (the shift), T1; and the stretch by direction (the shears), E + T2. Each is an ordinary family, so each has a card and one ledger line per Node-clock, like any train. No field names them apart.
3. **The fields** are those of part 1, each with the readings that need it and what the decoder names where it is absent.
4. **The one rule writes one split click per draw.**
   - A band's split click names its members (each member's lay and its party there), its joint histories (per member, the site that takes it and the line of its frame it is taken on), sigma_f, c over room and drawn, and its layer.
   - A slot's split click (decision 40 (b)) has the same form. Its members are its arrivals, and each of its histories is one set it may take: per member, the slot where it is taken, or its giver's site where the slot refuses it. Its sizes are all alike.
   - A setting is a split click of the same form: its sizes over its frames, c over room and drawn, and the takes it heard.
   - Each take names its lay, the frame its setting set and the line it took.
   - Each refusal is a Books line at the slot, one quantum laid back to its giver (5.1's books line), naming its lay.
5. **A mass is a reading, never a field** (decision 37; part 4): the rest beat of a train the clicks build, read at its clicks twice, the two agreeing through the one key.
6. **Shown on the one rule's own draws** (lines.py):
   - a pair drawn in two layers at its birth;
   - two quanta, each drawn at its own birth to z, where one slot is free; the slot's own draw takes one and refuses the other.

   Both pass the decoder's own reader (1.1's guards, the 1.2 fields unnamed) and three 1.2 checks: every take and every refusal names a lay, every draw is law 9's over its sizes, and every member goes where its draw's history says.

## 1. The fields

| field | line | what it holds | the readings that need it | where it is absent |
| --- | --- | --- | --- | --- |
| count (G1) | Ledger, per Node-clock | every train's count at "step", one line per Node-clock, the time gear's train one of them; a reading names the train it reads by its card | the bangs: rows 1, 1b, 14, 34, 46, 58 to 61; E7's q; the bang's spread across Node-clocks; the bottom's uniformity (row 63, E1); each swing's top per Node-clock | NOT READ: the ledger holds the board's sum alone |
| parts (G2) | Train | the trains a composite binds; none for a train the file lays | row 46's depth; rows 8, 27, 76 and 77; a particle's reading and its mass (part 4) | the depth NOT READ, the card named |
| work (G3) | Whole | the click's work, s T_k q (a+ - b) | row 66, the energy in the clicks; a moving mass (part 4) | read from the ledger alone, the flux cancelling over the board |
| unit (G4) | Train | the books' unit, the same on every card under decision 36 | row 15; Planck's key (rows 40 and 66); a mass's windings | NOT READ where two units could stand; a card whose unit differs is named |
| birth (G5) | Whole (a take), Books (a refusal) | the round and site of the lay it takes from, or that a refusal is laid back to | the handshake; S, M and the joint clicks; g2; one quantum written once; one lay followed through its clicks; the cone check on refusals | NOT READ: no take names its lay |
| members (G5 for a band) | Split | each member's lay (round, site) and its party there | the same, from the band's side | as birth |
| load (G7) | Whole, Split | the counts the click's Node-clock reads its clock and ruler at, the one clock and ruler of every act (line 693): as built the time gear's count; under decision 39 the rate's and the length's counts, with the lean and the shears for a reading by direction. Where G1 is written every round, G7 is G1's line at the click's round and site, and the click line need not repeat it | proper time: rows 10, 12, 13, 30 and 45; E7's q from the clicks' clocks; the frame reading; a mass's beat in its own proper time | NOT READ for those rows |
| parts (the histories) | Split | per joint history, per member, the site that takes it and the line of its frame it is taken on: a twin's 0 is +, 1 is -; a spread quantum's k is its k-th absorber; at a slot's split click, the slot where it is taken, or its giver's site where the slot refuses it | every reading of a band and of a slot | the 1.1 Split (one part per line) |
| frames (the tag) | Split | per member, the frame brought back, in 1.1's axis form (rho, spin), with its detector's site | the handshake; the sizes at the source | NOT READ for the handshake (one run) |
| layer | Split | the draw's order at its Node-clock, where a birth's parts are drawn as their settings come back | the layered law (each layer's line conditional on the earlier ones) | 1 |
| axes, heard | Split (a setting) | the frames the setting draws among, and the takes it heard by light (round, site), none for a free one; its sizes, c, room and drawn as any draw's | late settings; every machine's cone | NOT READ for late settings |
| detector, written | Whole (a take) | the frame its setting set, as its first line, and the line taken, in 1.1's axis form (moved from the Split); one form for every take | S, M, the joint clicks, no signal | the 1.1 Split's own |
| clock, tooth | Whole (a clock's click) | clock: the round and site of the lay that made the clicking clock (G5 for a clock); tooth: its face's teeth from that lay, before and after the click | proper time read twice; the twin reading | NOT READ for both |
| agree | End | 1 where the backward run, from the record's clicks, gives back every frame written | the passes' verification | NOT READ |

## 2. Retired, and never added

- **Turnover (K7):** retired, as the architect ruled. The converter drops it, the decoder's kind goes, and the reader refuses the line by name in every record. It was a line for the time gear alone (Sofer's audit, item 14).
- **The switch (decision 33):** never added. Every Node-clock runs both ways, and the header names no switch.
- **The time gear and the seed in the header (decisions 36 and 37):** never added.
  - The time gear is one train, its count one line in the ledger.
  - Every train a file lays is the seed, at pinion = den. A card with no parts at a pinion below den is a declared mass: the reader names it, and reads no mass for it.
- **back (G6), proposed and dropped** (decision 40 (b)): sigma_b is alike in every history, so no draw weighs it, and the tag carries the frames alone (the Boss's 6499341713, item 1). The slot's fullness acts after the draw, in its own split click.
- **The backward run writes nothing** (decision 34). The tag's one field, the frames, stands on the split click, where the forward reading of the one hand meets the tag that came back.

## 3. The lines, as the one rule writes them (lines.txt)

A pair at site 50, its first twin taken at 45 and its second at 70, the second's frame set by the first's outcome. The birth draws twice, layer by layer:

```
{"kind": "split", "round": 1, "site": 50, "count": 1, "train": 0, "members": [[1, 50, 0]], "parts": [[[45, 0]], [[45, 1]]], "sizes": [2, 2], "c": 3, "room": 4, "drawn": 1, "layer": 1}
{"kind": "split", "round": 1, "site": 50, "count": 1, "train": 0, "members": [[1, 50, 1]], "parts": [[[70, 0]], [[70, 1]]], "sizes": [9, 49], "c": 3, "room": 58, "drawn": 0, "layer": 2}
{"kind": "whole", "round": 6, "site": 45, "count": 6, "train": 0, "q": 1, "birth": [1, 50], "detector": {"train": 0, "rho": 2, "spin": [2, 0, 0]}, "written": {"train": 0, "rho": 2, "spin": [-2, 0, 0]}}
{"kind": "whole", "round": 36, "site": 70, "count": 36, "train": 0, "q": 1, "birth": [1, 50], "detector": {"train": 0, "rho": 29, "spin": [-20, 0, 21]}, "written": {"train": 0, "rho": 29, "spin": [-20, 0, 21]}}
```

Two quanta laid at sites 10 and 30, over x (4) and z (20) and over y (36) and z, each drawn at its own birth to z, where one slot is free (decision 40 (b)). The slot's own split click at z, its two arrivals both drawn, takes B and refuses A, and A's refusal is a Books line at z, one quantum laid back to its giver. Each take writes its frame and its line in the same form as a twin's: a frame of an absorber pair's own lines reads as the axis z, its first absorber + and its second -.

```
{"kind": "split", "round": 1, "site": 10, "count": 1, "train": 0, "members": [[1, 10, 0]], "parts": [[[4, 0]], [[20, 1]]], "sizes": [2, 3], "c": 3, "room": 5, "drawn": 1, "layer": 1}
{"kind": "split", "round": 1, "site": 30, "count": 1, "train": 1, "members": [[1, 30, 0]], "parts": [[[36, 0]], [[20, 1]]], "sizes": [3, 2], "c": 4, "room": 5, "drawn": 1, "layer": 1}
{"kind": "whole", "round": 11, "site": 20, "count": 11, "train": 1, "q": 1, "birth": [1, 30], "detector": {"train": 1, "rho": 1, "spin": [0, 0, 1]}, "written": {"train": 1, "rho": 1, "spin": [0, 0, -1]}}
{"kind": "split", "round": 11, "site": 20, "count": 11, "train": 0, "members": [[1, 10, 0], [1, 30, 0]], "parts": [[[20, 1], [30, 1]], [[10, 1], [20, 1]]], "sizes": [1, 1], "c": 1, "room": 2, "drawn": 1, "layer": 1}
{"kind": "books", "round": 11, "site": 20, "train": 0, "kept": 1, "birth": [1, 10]}
```

**What (b) changes in the record's order, for the Boss and David:** every draw stands at or before the takes it decides.
- Each quantum's end is drawn at its birth, at round 1, before any of its takes.
- The slot's split click stands at z at round 11, the round and site of the arrivals it decides, and decides only what happens there: which arrival is taken and which is refused. Within the round the schema's order writes the whole click before the split; the two share their round and site.
- Under the withdrawn weighing the two quanta were one band, drawn at z at round 11, after B's take at y at round 7, which that draw decided. That line is withdrawn with the weighing.

## 4. The mass, as the record reads it (decision 37)

**The definition.** A mass is the rest beat of a train the clicks build: the windings it books per tick of its own clock where it stands still, read at its clicks twice, the two readings agreeing through the one key. Nothing else on the record is a mass.

1. **What can carry one:** a train whose card names its parts (G2), a composite the clicks bound from the seed.
   - A train the file lays has no parts. It is the seed, at pinion = den, and carries no mass.
   - The time gear's spring is the board's own (decision 37), and no mass is read from it.
2. **The first reading, the beat:** at each of its whole clicks, its face (K4: the sweep Q and the tooth), per tick of its own clock (G7, so the beat is in its own proper time). Where its clicks book no momentum (rows 23 and 71), it is the rest beat.
3. **The second reading, the windings:** the windings its click books (K3, at its card's unit, G4), with the kept.
4. **They agree through the one key:** q = 2 Q div key at every click (rows 40 and 66). The mass is the number the two readings share.
5. **Moving:** the beat is read in the clock's own count (G7, part 6), and no motion changes it: a moving clock reads its rest beat at its clicks, with no formula turning its energy and momentum into a mass (the owner's word to Animate, 2026-10-30: no formulas). A beat that turns with the direction of motion is the board's frame showing in the shadow (root II, the causal-set test).
6. **A species:** the trains the clicks build with the same parts and the same charge booked. One species has one mass: every lay of it reads one rest beat.
7. **Stable:** its windings are held in the ledger from its lay to the end, with no click taking them (row 46). Where a click takes them, the rounds between are its lifetime.
8. **A mass ratio:** two species' rest beats read at one load, a ratio of whole numbers, set against nature's with the tries counted.

**Each failure is named:**
- the beat and the windings disagree at a click;
- two lays of one species read two rest beats;
- the composite comes apart before its beat is read twice;
- a rest beat, read in its own proper time (G7), moves with the load: the swing showing in a mass, against **The same clock and the same ruler for every act** (line 693). The Boss's side finding predicts it for a binding made by a value x value coupling row, whose strength reads no ruler (6495615190, item 4);
- a moving clock's beat, read in its own count, differs from its rest beat.

**Guards:** G2 (parts), G4 (unit), G7 (load), G3 (work, for a moving mass's energy) and G5 (one lay followed through its clicks).

## 5. The record without the turnover line, as one change (turnover_out.patch)

Decision 38 asks it of Animate, and G1 of the Boss's plan takes it (6497161018). Under decision 32 no decoder code enters src, so it stands here as one patch, ready the moment the build resumes. `git apply` takes all nine files on reader-5's head; on tensor24-review it takes the src and tests hunks (`--include='src/*' --include='tests/*'`), the converter and the decoder's page being reader-5's.

- **src/tensor24/decoder/records.py:** the turnover kind leaves the reader's kinds. A turnover line is then refused as any line of a kind the schema does not hold: "the line kinds ['turnover'] are unknown". No guard of its own is added.
- **src/tensor24/record/schema.py:** the Turnover record goes, and the lines' order names Whole, Split, Rate and Books.
- **The two decoder tests:**
  - the order's case stands on a whole click and a rate line;
  - a turnover line is refused by its kind (a new test);
  - the mutant that reads the whole click's q rule on every kind is killed by a rate line with an unnamed q 0, where a turnover at q 0 killed it before.
- **tools/tensor24_convert.py:** the converter writes no turnover line. ANIMATE-DECODER-1's first slice and page follow: the three records lose their 1,934, 861 and 1,073 turnover lines, and every other count is unchanged.
- **Checked in a scratch worktree:** the decoder's 130 tests pass; ruff check and format hold; the decoder's 204 mutants are all killed (mutants.txt in the patch), the kinds' order mutant now swapping the whole click and the rate line.
- **Left to the writer** (the Boss's): engine/__init__.py's docstring names the turnover among the engine's parts, and algebra/carry.py's names the fine tooth reflected at it. Both are the engine's words, not the record's.

## 6. The measurement's rules: proper time and invariants (D6 to D8)

The owner's text to the Boss (space and time are a four-dimensional spacetime's shadows, the interval's minus sign is light's limit) and his word, "This is also important for the decoder, no?", entered by the Boss as D6 to D8 (6499708355, 6499774896). The reader's code is owed at G5 (decision 32).

1. **Proper time, never the board's tick.** As built, decoder/clocks.py counts beats from the rate lines, which are the great clock's ticks: a gap.
   - A clock's proper time between two of its clicks is read twice, and the two agree:
     - (i) its own count, the face's tooth at each click (K4), followed through one lay's clicks (G5);
     - (ii) the sum of the rate gear's count, N, along its path, from G1's lines (or G7 on each click).
   - A disagreement is named, never averaged.
   - The round is order alone: which click is before which, and the cone from the round, the site and light's speed. It is never a duration.
2. **Invariants only, and no formula** (the owner's word to Animate, 2026-10-30): a clock's own count between two of its clicks, the clock itself being the sum along its path; its rest beat, read in that count (part 4); a quantum's lay and its take, two events on one light line; a distance by echo, a clock's own count between laying a quantum and taking its echo.
   - A reading that compares rounds as times is refused by name: "compares board ticks, no reading".
   - Every row that reads a duration (the bang's length, q per era, the gravity rows 10, 12, 13, 30 and 45) reads it from proper counts.
3. **The twin reading:** two clocks whose clicks share a first and a last event (a meeting at one Node-clock at one round), their own counts between the two compared.
   - It fails where the counts are equal while the paths differ, or where they differ by other than the lapse and the motion.
   - Guards: G5, and G7 or G1.
4. **The cone check on every record:** the no-signal reading of B's record, run on every record.
   - For every click, a take or a refusal, its law against every setting outside that click's past cone, binned by that setting. It reads each click, never a party's whole outcome.
   - Equal laws within the Poisson spread, or the record is named as signalling, with the pair named.
   - Under decision 40 (b) it holds on hand_slot's two boards exactly: the far twin's click is 1/2 at every near frame, and A's click at x is 2/5 with B and without (ANIMATE-SCHEDULER part 5).
   - A's fate at z moves with B's birth (taken 3/5; taken 12/25 and refused 3/25), lawfully, since z lies on B's birth's light cone. A check that binned A's whole outcome would name that a signal; the check by click names none.
   - Under the withdrawn weighing, "a full slot weighs 0", it fails there: 11/29 against 107/174, and 2/5 against 10/19.

**As built in the decoder** (src/tensor24/decoder/measure.py; tested on records built in memory, N5):
- **The cone:** one Mesh a round. The Meshes between two sites are the shorter way round each side, summed; an event on the cone stands inside it.
- **The cone check** reads each take (a whole click naming its lay), each refusal (a Books line naming its lay) and each setting (a split click naming its lay among its members, with its axes and the one drawn).
  - The lays laid at one site are trials alike. Each click and each setting is placed by its round after its lay's round, and its site.
  - At each click's place, against each setting's place outside its past cone, each trial's outcome there (the line written, refused, or none) is binned by the frame drawn.
  - Shares are compared exactly, by cross products. A spread for the act's records is the Boss's to rule.
- **Proper time read twice:** between two of a clock's clicks at one Node-clock, (i) its tooth after's difference and (ii) the Node-clock's ticks from the rate lines; the two agree through one beat at every pair. A clock that moves between two clicks has no path on the record (G1 per train would give it).
- **The twin reading:** two clocks meeting twice by two paths, each path the sites of its clicks between; equal counts are named. Whether a difference is the lapse's and the motion's reads the metric along each path, which waits on the owner's ruling of the metric's representation.
- **No board tick (D7):** a duration is a clock's own count between two of its clicks. Asked between other events, it is refused: "compares board ticks, no reading".

## 7. What does not follow

- **The writer:** the runner, which writes every line; and stage 9, which makes the clicks.
- **A mass, on any record so far:** no record holds a train the clicks built. Whether the act builds one from the seed is decision 37's decisive question (David's ladder).
- **G1's size:** one ledger line per Node-clock per round for every train. Whether the runner writes it every round, or at each Node-clock's turning points alone, is the Boss's to choose.
- **A frame of more than two lines** (a quantum over three absorbers): the take's frame and line in 1.1's axis form hold for two lines; for more, the lines themselves (not shown).
- **A refused quantum's way back to its giver:** the record holds the refusal at the slot (a Books line naming the lay); the giver's books at its own Node-clock, and the way back's path and tick, are the runner's.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - every field is written by the forward run: a lay, a take, a split click at the Node-clock where its draw is made, each Node-clock's line of every train's count;
  - the tag's field, the frames, is what the backward run brought to the split click;
  - a slot's split click is its own law-9 draw over equal weights, and a refusal is one quantum laid back to its giver by a Books line;
  - a mass is read from a built train's own clicks: its face and its booked windings, through the one key.

  No term is declared, and no field holds a train apart.
- **(b) What the clicks show, the books first:** every take and every refusal names its lay, every draw is law 9's over its sizes, and every member goes where its draw's history says, on the one rule's own draws.
- **(c) What does not follow, asked of the clicks:** the runner's own lines; G1's size; a mass, until the clicks build a train.

---
Animate, reader-5.
