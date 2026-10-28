# Animate's probes of the many bangs, kept with their outputs (the derivation protocol's step 3)

The draft is ANIMATE-MANY-BANGS.md. Nothing here is engine code, and nothing was pushed to an engine branch.

## 1. many_bangs.py: the course on the engine

- **The tree:** engine-5.0-test at 33d9ecaa (its src at that commit), with draft C's drives.py and course.py beside this harness. Copy many_bangs.py into tools/derivations/open_items/derive/C of that tree, then run `python -I many_bangs.py <the tree> <variant> <quanta> <ticks> [<rewind n> <rewind from> ...]` with an interpreter that has numpy and pytest (tests.laws imports pytest).
- **The world:** tests/worlds/world_bang.json on universe_bang.json, 64 Node-clocks, the seed's quanta set by the argument. The drive is draft C's vol0, the derived push with no clamp.
- **The variants, one change each:**
  - **base:** law 4's two triggers and BH-S1's restore, as draft C ran it.
  - **nofloor:** law 4's floor clause struck.
  - **notick:** nofloor, and BH-S1's restore struck. Law 4 reads the time gear of a clock with no tick (Mesh rate 0 at the tick's start) as held, and nothing else changes.
  - **weakmin:** notick, with law 4's bottom as the top's mirror, the time gear's weak minimum (X0 >= X1 <= X2, one strict), in place of the floor (the Boss's candidate).
  - **fallmin:** weakmin with the bottom entered from above only (X0 > X1 <= X2).
- **Its readings:**
  - X per tick, least and largest;
  - the tops, the local turnovers and the floor's firings;
  - the births per tick and per bang, and the books per click phase;
  - the bottoms' state hashes;
  - the retrace after each top: X at top + k against X at top - 2 - k;
  - the rewind.
- **The outputs:**
  - many_bangs_base_5M_250.txt, many_bangs_nofloor_5M_250.txt and many_bangs_notick_5M_250.txt: all three end at the state hash 77e8684641d42469;
  - many_bangs_notick_5M_1000.txt;
  - many_bangs_notick_500k_1000.txt;
  - many_bangs_weakmin_5M_250.txt: the board turned over at every tick, X = 1,000 throughout, no birth;
  - many_bangs_fallmin_5M_250.txt: a turnover at every top and every bottom, the same top 4,638,548,302 at every bang, no birth.

## 2. tst_time_gear.py: T S T = S^-1 for the time gear's step

- **Pure integers, no engine:** `python tst_time_gear.py`. The step is X+ = 2 X - X- + q with the drive's floor carry; T exchanges the slots and turns the drive's fine tooth.
- **Three rules for the tooth:**
  - the flip, r to T_d - 1 - r;
  - the mirror, r to (2 mid - r) mod T_d;
  - a mutant that keeps the tooth.

  Each runs at every teeth count from 8 to 15, every tooth, every push in [-3 T_d, 3 T_d], and X-, X in [-2, 2].
- **The output:** tst_time_gear.txt.
  - The flip: 0 failures at every count.
  - The mirror: failures at the even counts only, exactly where r = 0 or r' = 0.
  - The mutant: failures everywhere.

---
Animate, reader-5.
