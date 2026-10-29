# The record's schema 1.2, proposed (Animate)

The asks: Sofer's owed line (5) of 6494833685 ("the scheduler on a full board and schema 1.2"), and the Boss's gaps G1 to G7 (ANIMATE-DECODER-CLOSURE, part 2). It takes in decisions 33 to 35, the one rule of ANIMATE-SCHEDULER, and B's record (ANIMATE-B-RECORD).

It is a proposal for the Boss, whose schema it is. Nothing is built: the decoder's code waits with the build (decision 32). `python -I lines.py` writes example lines from bands the one rule draws and reads them back (lines.txt).

## The answer

1. **1.2 is a minor version.** Every 1.1 record stays readable as it is. 1.2 adds fields, retires one line kind (Turnover), and takes in no switch.
2. **The fields** are those of part 1, each with the readings that need it and what the decoder names where it is absent.
3. **The one rule writes one split click per band draw.** The click names its members (each member's lay and its party there), its joint histories (per member, the site that takes it and its sign there), sigma_f and sigma_b, c over room and drawn, and its layer. Each take names its lay and holds 1.1's detector and written.
4. **Shown on the one rule's own bands** (lines.py):
   - a pair drawn in two layers at its birth;
   - two quanta joined by one free slot, drawn at the absorber where they are one.

   Both pass the decoder's own reader (1.1's guards, the 1.2 fields unnamed) and three 1.2 checks: every take names a lay, every draw is law 9's over sizes times back, and every member is taken where its band's drawn history says.

## 1. The fields

| field | line | what it holds | the readings that need it | where it is absent |
| --- | --- | --- | --- | --- |
| time_gear (G1) | Header | the time gear's train | the bangs: rows 1, 1b, 14, 34, 46, 58 to 61; E7's q | NOT READ: the header names no time gear |
| site (G1 per site) | Ledger | one Node-clock's line: the time gear's count at "step" | the bang's spread across Node-clocks; the bottom's uniformity (row 63, E1); each swing's top per Node-clock | NOT READ: the ledger holds the board's sum alone |
| parts (G2) | Train | the trains a composite binds; none for the seed | row 46's depth; rows 8, 27, 76 and 77; a particle's reading (decision 35) | the depth NOT READ, the card named |
| work (G3) | Whole | the click's work, s T_k q (a+ - b) | row 66, the energy in the clicks | read from the ledger alone, the flux cancelling over the board |
| unit (G4) | Train | the books' unit: the drive's notches, or the sweep | row 15; Planck's key (rows 40 and 66) | NOT READ where two units could stand |
| birth (G5) | Whole (a take) | the round and site of the lay it takes from | the handshake; S, M and the joint clicks; g2; one quantum written once | NOT READ: no take names its lay |
| members (G5 for a band) | Split | each member's lay (round, site) and its party there | the same, from the band's side | as birth |
| back (G6) | Split | sigma_b per joint history: a slot's free count, 0 where a history overfills it | the draw (rows 18 and 25); the sizes at the source | read as 1 at every part: law 9 over sigma_f, as 1.1 |
| load (G7) | Whole, Split | the time gear's count at the click's Node-clock | proper time: rows 10, 12, 13, 30 and 45; E7's q from the clicks' clocks; the frame reading | NOT READ for those rows |
| parts (the histories) | Split | per joint history, per member, the site that takes it and its sign along the frame there (0 where no frame) | every reading of a band | the 1.1 Split (one part per line) |
| frames (the tag) | Split | per member, the frame brought back, in 1.1's axis form (rho, spin), with its detector's site | the handshake; the sizes at the source | NOT READ for the handshake (one run) |
| layer | Split | the draw's order at its Node-clock, where a birth's parts are drawn as their settings come back | the layered law (each layer's line conditional on the earlier ones) | 1 |
| axes | Split (a setting) | the frames a detector's light chooses among | late settings | NOT READ for late settings |
| detector, written | Whole (a take) | the frame the detector took in, and the part it wrote (1.1's Reading form, moved from the Split) | S, M, the joint clicks, no signal | the 1.1 Split's own |
| seed | Header | the seed train (decision 35: the one train a file may hold, at pinion = den) | a card neither the seed nor bound of parts is named as a declaration | every card read as the file gave it |
| agree | End | 1 where the backward run, from the record's clicks, gives back every sigma_b written | the passes' verification | NOT READ |

## 2. Retired, and never added

- **Turnover (K7):** retired, as the architect ruled. The converter drops it, the decoder's kind goes, and the reader refuses the line by name in every record.
- **The switch (decision 33):** never added. Every Node-clock runs both ways, and the header names no switch.
- **The backward run writes nothing** (decision 34). The tag's two fields (frames, back) stand on the split click, where the forward reading of the one hand meets the tag that came back.

## 3. The lines, as the one rule writes them (lines.txt)

A pair at site 50, its first twin taken at 45 and its second at 70, the second's frame set by the first's outcome. The birth draws twice, layer by layer:

```
{"kind": "split", "round": 1, "site": 50, "count": 1, "train": 0, "members": [[1, 50, 0]], "parts": [[[45, 1]], [[45, -1]]], "sizes": [2, 2], "back": [1, 1], "c": 3, "room": 4, "drawn": 1, "layer": 1}
{"kind": "split", "round": 1, "site": 50, "count": 1, "train": 0, "members": [[1, 50, 1]], "parts": [[[70, 1]], [[70, -1]]], "sizes": [9, 49], "back": [1, 1], "c": 3, "room": 58, "drawn": 0, "layer": 2}
{"kind": "whole", "round": 6, "site": 45, "count": 6, "train": 0, "q": 1, "birth": [1, 50], "detector": {"train": 0, "rho": 2, "spin": [2, 0, 0]}, "written": {"train": 0, "rho": 2, "spin": [-2, 0, 0]}}
{"kind": "whole", "round": 36, "site": 70, "count": 36, "train": 0, "q": 1, "birth": [1, 50], "detector": {"train": 0, "rho": 29, "spin": [-20, 0, 21]}, "written": {"train": 0, "rho": 29, "spin": [-20, 0, 21]}}
```

Two quanta laid at sites 10 and 30, over x (4) and z (20) and over y (36) and z, joined by z's one free slot. The band is drawn once, at z:

```
{"kind": "whole", "round": 7, "site": 36, "count": 7, "train": 1, "q": 1, "birth": [1, 30]}
{"kind": "whole", "round": 11, "site": 20, "count": 11, "train": 0, "q": 1, "birth": [1, 10]}
{"kind": "split", "round": 11, "site": 20, "count": 11, "train": 0, "members": [[1, 10, 0], [1, 30, 0]], "parts": [[[4, 0], [36, 0]], [[4, 0], [20, 0]], [[20, 0], [36, 0]], [[20, 0], [20, 0]]], "sizes": [6, 4, 9, 6], "back": [1, 1, 1, 0], "c": 13, "room": 19, "drawn": 2, "layer": 1}
```

**One thing the tie shows, for the Boss and David:** the band's split line stands at z at round 11, after B's take at y at round 7, which it decides.
- The draw is made where the band's parts are one, and the two quanta are one only at z.
- Its word rides back along B's path to B's source and out to y. That is the backward run of decision 28, the influence from the future to the past that the owner calls necessary.
- The record keeps forward order, and the decoder links the take to its band through members and birth.

## 4. What does not follow

- **The writer:** the runner, which writes every line; and stage 9, which makes the clicks.
- **G1 per site's size:** one ledger line per Node-clock per round for the time gear's train. Whether the runner writes it every round, or at each Node-clock's turning points alone, is the Boss's to choose.
- **A band joined by a hand and by a slot at once:** the same fields (its members from two lays), not shown here.

## Method: addressed

- **(a) Which clock or gear makes each term:**
  - every field is written by the forward run: a lay, a take, a split click at the Node-clock where its band is one, the ledger's time gear;
  - the tag's two fields are what the backward run brought to the split click.

  No term is declared, and the seed is named so that a declaration can be.
- **(b) What the clicks show, the books first:** every take names its lay, every draw is law 9's over sizes times back, and every member is taken where its band's drawn history says, on the one rule's own bands.
- **(c) What does not follow, asked of the clicks:** the runner's own lines, and the size of G1 per site.

---
Animate, reader-5.
