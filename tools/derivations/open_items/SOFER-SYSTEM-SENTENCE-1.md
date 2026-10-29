# The owner's sentence against the system (Sofer's check of 2026-10-29)

The owner's direct word to Sofer, 2026-10-29, 02:0x UTC (in Hebrew, verbatim in translation): "Rates multiply along a gear train, so the time gear's law is linear in the logarithm of the rate. Let it enter as a law that is enforced and as a postulate, in simple words. Update yourself from the Boss. Check whether this describes the system: The most precise formulation of the system: a board of clocks, each of them a train of gears, and the gears of neighbouring clocks mesh with each other. Time belongs to the clock, and the arithmetic belongs to the gear."

The first part is Postulate 6 (docs/ALGEBRA.md line 35, entered at 27620200f in the words of the Boss's post 6485503701, which carry the owner's). The second part is the sentence checked here, and it is the same sentence that stands in **The principle of the clock and the gear** (line 35, entered at 48c7e26fe).

## The verdict

**The sentence describes the system.** Each clause meets a place in the law and in the code (tensor24-review 9e5233d7f, stage 7a), and no clause is false. Three precisions follow, none a correction of the picture.

## Clause by clause

| clause | what the system has | where | holds |
| --- | --- | --- | --- |
| a board of clocks | the lattice of Node-clocks, six neighbours each (+x, -x, +y, -y, +z, -z), the board built from the piece's shape by Rule3's carry | docs/ALGEBRA.md, **The picture over the postulates**; CLOCK_WORDS: Node-clock, great clock; engine/state.py Layout.nb; runner/board.py | yes |
| each of them a train of gears | a Node-clock holds one gear per component of each family (the load lays a, b, r, go and r_d at every Node-clock, 2 rows at 64 sites in the example); its gears mesh among themselves, through the 24's tables (engine/contract.py: two gears' readings into a third) and through the time gear's teeth (7b) | CLOCK_WORDS: gear, hand, composite clock; engine/step.py sources(), drive() | yes, with precision (a) |
| the gears of neighbouring clocks mesh with each other | a gear is pulled by the same row's gear at each of the six neighbours, as seen at the reader's count, through the grip of the Mesh between them; the gradient is read from the neighbours' gears | CLOCK_WORDS: Mesh, "the meshing of two neighbouring clocks"; engine/mesh.py pull(), seen() | yes |
| time belongs to the clock | the beat's dial, the count and the time of the now slot are one array per Node-clock, shape (1, sites); so are the due beat and the order of the reads (a neighbour is read at the reader's count) | engine/state.py State ("per Node-clock its dial, count and time"); engine/mesh.py due(), seen(); engine/step.py beat() | yes |
| the arithmetic belongs to the gear | the now and before slots, the fine tooth, the going and the drive's fine tooth are arrays per gear, shape (rows, sites); every act on them is a sum, a product or Rule3's carry | engine/state.py State ("per gear its now and before slots, fine tooth, going and drive's fine tooth"); engine/step.py gear(), drive() | yes |

A run of the load on the example files prints the shapes: a, b, r, go and r_d are (2, 64), the dial, the count and the time are (1, 64). The separation the sentence states is the separation the arrays have: no gear's array holds a count or a time, and no clock's array holds a notch.

One exception that is none: the Node-clock's own dial is itself a gear (CLOCK_WORDS: dial, "a gear read as a count with a whole turn"), and the beat is its carry, so the clock's time is a gear's carry; it stands in the clock's arrays because it is the clock's.

## Three precisions

(a) **The word train.** In the documents a train is all the gears of one kind at every Node-clock, stepped by one gearing: the law's word for a family (CLOCK_WORDS: train; the universe file's `trains`). In the owner's sentence, and in Postulate 6 ("a gear train"), the word is the mechanical one: gears that turn each other in a chain, so that the rates multiply along it. The picture is one: the gears at a Node-clock are a gear train in that sense, and a family's row across the board is a train in the documents' sense. The clock words take one more row, **gear train**, so that each word keeps one meaning (entered with this record). The owner decides whether the documents' train is renamed; the code's Train and the files' `trains` key are the documents' sense.

(b) **The word board.** The documents named the whole lattice the great clock and renamed its former word board in 1,507 places (CLOCK_WORDS, the renamed words, by the owner's words of 2026-10-27 and 2026-10-28); the code keeps board (runner/board.py). The owner's sentence says a board of clocks. The two words name the same lattice, the great clock with its tick, the board seen as the place of the clocks. The owner decides whether the dictionary takes board back for that second sense.

(c) **What the sentence leaves out, which the system has.** The shapes of the gears, from the 24 (five kinds, the tables C through which the gears of one clock mesh), Rule3's carry as the one act with the sum and the product, and the click, an event, the carry's quotient leaving. None of them contradicts the sentence: they are the arithmetic that belongs to the gear. The principle's phrasing in the law carries them ("every number is a gear's notch, and the one act on the gears is the sum, the product and Rule3's carry, alike on every train, its shapes from the 24").

## What the sentence does not cover, outside the machine

The runner (files, load, the rewind check) and the decoder (the reader of the record) stand outside the board: they build it, run it and read what it wrote, and they hold no clock and no gear of their own. The sentence describes the machine, not these.

## Recommendation

Enter the sentence as the opening of **The picture over the postulates** in the owner's words (it states the picture in one line where the paragraph takes five), keep the principle where it stands, and add the two dictionary rows of (a) and (b) on his word.
