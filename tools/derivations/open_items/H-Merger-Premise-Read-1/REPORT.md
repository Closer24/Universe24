# H-Merger-Premise-Read-1: report (the engine head 0aa0b8ff4, 2026-10-26, a 75-minute box)

**Verdict: the law's letter requires reading (a), the premise read at the pair's own state as the birth
laid it, and that is what the engine already reads (close.meet reads `plane_starts`, the record's
levels at the interval's START, before the step of that interval); the two readings are one act on the
board.** The stepped current of a pair laid whole is exactly den A (g_minus + g_plus) and is 0 at 1 of
14 births on the hole 60 and 1 of 14 on the chiral 60, so reading (b) would move 13 of 14; yet the
records are the same under either reading: the hole 60 and the chiral 60 keep every Node line, their 17
births each, their 2,288 and 2,903 credits, their 539 and 612 turns, their taken and booked to the
digit and the run back 20 of 20; the 48 on the chiral 3-cube at 60 reads 3 equal and 45 apart under
reading (b), the head's own count. What parts is the refusals' NAMES (hole: sense 9,274 to 9,323, stop
9,146 to 9,314, twist 229 to 164, orientation 248 to 96; chiral: sense 10,393 to 10,254, stop 9,371 to
9,586, twist 42 to 7, orientation 110 to 69) and, on the chiral, one merger birth of 17, whose two ends
are exchanged with the per-end dP_take moved and its sum kept. Laws checked and held: the run back
exact (20 of 20 on four records), the current's antisymmetry 60 of 60, the Node lines' current against
the board's 60 of 60, the Wronskian at the marks 14 of 14, the births' children of opposite sign 17 of
17, EX-S1's exact identity 2,305 of 2,305 clicks, the energy's beat 2,288 of 2,288, integers only
(floats 0), the one-Link reach, the 48, the fixed count of integers, the 128 bits (112 at the marks).
The one unmet: gate 15's pre-EX-S1 inequality taken >= booked per birth, 14 of 17 on the hole 60, which
reads the births alone and so stands the same on the head's record.

The derivation, the algebra, the tables, the two sentences and the ledger row: DERIVATION.md beside
this file. The flag's replacements: repl_pr1.json. The measures: out/.

## The generic problem above the item (Addition 10, step 0)

The close reads one meaning at TWO moments: the premise, the standing share and EQ-S1's net current at
the interval's start (close.py:88-90 and :331, bodies.py:31), and the merger's take and the credit's
sense at the interval's end (merger.py:168-176 and :120-133, take.py:60-98, bodies.py:147). The
candidate sentence CL-S1 (the close's one moment) is written in DERIVATION.md section 0; the item's own
question has one answer once that sentence stands, and no flag is needed for it.

## What was cut short

The quartet on a carrying leg (the third lift over den; the chiral 3-cube and 5-cube at 60, the hole
5-cube at 60, the worlds under H-Quartet-Carriage-2/worlds/ and -1/worlds/) was not run: the box ended
with the 48 just finished. The bodies record (tests/worlds/world_bodies.json, 300 intervals) was not
run. No chain is still running; every run of this hand has exited. The records that stand:
/dev/shm/tmp/pr1/note_hole.json, close_hole.json, note_chiral.json, close_chiral.json,
c48_close_chiral3.json, head_world_hole.json, head_world_nature.json, and the flagged copy
/dev/shm/tmp/pr1/src_pr1.

## Bugs and readings, by file and line

1. **merger.py:168-176 (`read_ends`, through `levels_at`) and merger.py:120-133 (`share_fall`)**: the
   merger's take reads the record's levels and the share's fall off the LIVE lines, that is the state
   the step of the same interval left, while the meeting that let the take happen was read at the
   interval's start (close.py:88-90). One meaning, two moments; the sentence CL-S1.
2. **take.py:60-98 (`fall_of`)**: the same split on the gap-0 row - the taken line and the fall are
   read at the live lines while `node.start_x` in the same function is the interval's start.
3. **bodies.py:147 (`credit`)**: the credit's logged sense is `gram.charge(row.shape, row.lines)`, the
   live lines, while the same function's standing count and EQ-S1's net current come from
   `plane_starts`. A third moment, in a logged field alone.
4. **merger.py:224-258 (`write_ends`)**: the two ends of a merger are written in the order the meeting
   named them, and the two ends are neighbours on one Link, so the SECOND write books its momentum
   against a board the first write has changed: the per-end dP_take depends on the naming of the ends
   (measured on the chiral 60, the two ends' dP_take -9,292,034,116,582,087,500 and
   +3,687,315,125,627,812,500 under one naming against -5,604,718,990,954,275,000 and 0 under the
   other, the sum the same integer). The sum conserves; the attribution per Node does not. A momentum
   booked per Node that depends on the write order is a reading to settle (AJ-S2's key).
5. **close.py:104-112 (`meet`, the rest branch)**: `list_of(node, rec, 0)` is called with the number 0
   and `room` 0 for a merger, so the merger's birth log carries a room that was never drawn; the field
   is read by the readers as a drawn room.
6. **merger.py:308-325 (`light_children`)**: the merger's two children are laid by `rise_of` at each
   end with no sense, so the orientation close.meet derives (which end is the + child) reaches the
   board nowhere - it reaches the log alone. The orientation of a merger is a name, not an act: this
   is why the two readings of the premise cannot part the board, and it is the fact to put to the owner
   beside MG-S2 (MG-S1 says "the + child at the end whose charge is positive", and the engine lays the
   same two children either way).
