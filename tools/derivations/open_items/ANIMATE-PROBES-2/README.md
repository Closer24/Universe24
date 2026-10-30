# Animate's probes of the many bangs, kept with their outputs (the derivation protocol's step 3)

**Record:** these probes run the old engine (src/event_universe) or read its records, which the owner's word of
2026-10-30, 09:2x UTC, takes out ("only the new engine matters"). They stand for their findings, cited by the
pages that name them, and are not run on the new engine.

The draft is ANIMATE-MANY-BANGS.md. Nothing here is engine code, and nothing was pushed to an engine branch.

## 1. many_bangs.py: the course on the engine

- **The tree:** engine-5.0-test at 33d9ecaa (its src at that commit), with draft C's drives.py and course.py beside this harness. Copy many_bangs.py into tools/derivations/open_items/derive/C of that tree, then run `python -I many_bangs.py <the tree> <variant> <quanta> <ticks> [<rewind n> <rewind from> ...]` with an interpreter that has numpy and pytest (tests.laws imports pytest).
- **The world:** tests/worlds/world_bang.json on universe_bang.json, 64 Node-clocks, the seed's quanta set by the argument. The drive is draft C's vol0, the derived push with no clamp.
- **The variants, one change each:**
  - **base:** law 4's two triggers and BH-S1 (its hold and restore, its masks on the Meshes and the dial, the click's skip), as draft C ran it.
  - **nofloor:** law 4's floor clause struck.
  - **notick:** nofloor, and BH-S1's restore struck. Law 4 reads the time gear of a clock with no tick as held: a mask, refused by "no bound and no floor", kept as the first form.
  - **carry:** law 11 at the time gear. The time gear's notch is a dial of X_c teeth, X_c the stretch of the stopped load, and its whole turn (X div X_c at the tick's start) is the turnover. There is no weak maximum and no floor, and BH-S1 is struck everywhere. This is the draft's form.
  - **carry_nof2:** carry, with the Mesh factor read from the tension unclipped (F2 struck).
  - **weakmin:** notick, with law 4's bottom as the top's mirror, the weak minimum (X0 >= X1 <= X2, one strict), in place of the floor.
  - **fallmin:** weakmin, with the bottom entered from above only (X0 > X1 <= X2).
- **Its readings:**
  - X per tick, least and largest;
  - the tops, the local turnovers and the floor's firings;
  - the births per tick and per bang, and the books per click phase;
  - the bottoms' state hashes;
  - the retrace after each top: X at top + k against X at top - 2 - k;
  - the state hash with and without the dial;
  - the rewind;
  - a refusal by name with its tick.
- **The audit, on every variant:** how many values each bound the engine still holds changed in the run:
  - a load below 0;
  - a tension below 0 or above Gamma;
  - a Mesh factor zeroed by a stopped end;
  - the dial held at a stopped clock;
  - the end teeth's fallback;
  - the draw's room capped;
  - the coupling's cap.
- **The outputs, many_bangs_<variant>_<quanta>_<ticks>.txt:**
  - **At 5,000,000 quanta and 250 ticks,** every variant. Base, nofloor and notick end at 77e8684641d42469; carry at 640f11b7135fcbfc, the same without the dial (131263b34da818ef). carry_nof2 is refused at tick 15. weakmin turns over at every tick, and fallmin replays the first bang.
  - **Over 1,000 ticks,** base and carry at 5,000,000 and 500,000 quanta. At 5,000,000 they are the same without the dial (1bc59fa2b92b6617). At 500,000 they part in the dial and the clicks counter alone (draft, P5).

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

## 3. kinds_ladder.py: the 24's ladder, bang by bang

- **Pure integers, no engine:** `python kinds_ladder.py`. The eight kinds of 2O are given by their characters in Z[sqrt 2]; every multiplicity is the class sum over 48, an integer. It reads:
  - the table's orthonormality;
  - the ladder from the one big bang's calibre (all A1);
  - the ladder with the twin hands beside them, each bang fusing every pair of kinds present, and the slower one, each bang adding one twin hand;
  - the tensor powers of E1/2 to n = 8;
  - every kind's exchange sign;
  - two mutants.
- **The output:** kinds_ladder.txt.
  - The orthonormality fails at 0 pairs.
  - The ladder from A1 stays at A1.
  - With E1/2 the eight kinds stand at bang 4, or at bang 6 one twin hand at a time.
  - The exchange sign is +1 on the 24's own kinds and -1 on the spinor kinds.
  - The mutants fail.

---
Animate, reader-5.
