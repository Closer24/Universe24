# The detector's click on a born pair: Bell at 2.73

David, 2026-10-28, 03:4x UTC, for the Boss. This answers the owner's order to David of 02:59 UTC ("Sync with the Boss. Build the above click solution locally. Make sure it works. Then give him OK.") and uses his leave of 02:50 UTC ("Contradict a word of mine if needed in the solution"). Built in a local worktree of 97e5b3fd6 (DAVID-THE-BELL-CLICK.patch: bobs.py, striking.py, predicates.py) and measured, each a harness (DAVID-THE-BELL-CLICK_CHECKS.txt). Nothing pushed to src.

## The act

1. **A fitting's two children carry one open axis** from the birth to the first click of either.
2. **The first click reads its detector's direction and draws half and half.** The draw is the vernier's c in [0, room), and the answer is up where 2c < room. That answer closes the pair's axis for both children.
3. **The partner's click reads its own direction and draws against the closed axis with Born's odds.** Its answer is opposite to the first where (2c - room) |d1| |d2| < room (d1 . d2), compared on integers alone.
4. **When both children click in one strike,** the - end draws first, by its role.
5. **The detectors' directions are the cube's own.** The - end's detector reads a face (x or y), and the + end's reads a face diagonal (x + y or -x + y). The choice between the two directions comes from outside the board, one choice per answered click in turn. The run hands the directions and the choices to the engine, so the engine holds no number of them.
6. **The answers are readings written on the click lines.** No gear is written.

## Measured on the bang

1. **S = -2.726, with a spread of about 0.112, over 688 pairs** (13 seeds at 500 ticks, 367 of the pairs clicking in one strike). That is above the local bound of 2 by six spreads, and within one spread of Tsirelson's 2.828. The four cells read -0.662, +0.595, -0.690 and -0.778, against +-0.707.
2. **The rule alone, over 200,000 pairs with a fair stream of draws,** reads S = -2.831, with each cell at 0.707.
3. **No message passes.** Each end's answers stay half and half for either setting of the other end: 148 up of 317 and 177 of 371 at the + end, and 189 of 335 and 173 of 353 at the - end. Over the 200,000 pairs the + end reads 50,160 up of 100,099 and 49,728 of 99,901.
4. **The cone holds:** for all 688 pairs, the mesh distance between the two clicks lies within the ticks back to the birth and forward again.
5. **The board is untouched.** On 13 seeds at 250 ticks, the build's charts equal 97e5b3fd6's key by key once the answers are dropped, and every row reads the same. The rewind holds 20 of 20 at every seed, at 250 and at 500 ticks.
6. **The choices' source does not matter.** Choices from outside and the detector's own datum (the light's fine tooth at the click, in the build's first form) read S = -2.680 and -2.610 over 456 pairs at 250 ticks.
7. **The full check on the build passes:** 117 tests, with the engine gates, the code's shape and the documents' gates all holding.
8. **Row 56 on one chart swings with its few pairs:** 5 million quanta at 500 ticks reads S = -2.829 over 192 pairs. Its else-branch names |S| <= 2 even where S^2 passes 8 by chance; the row should read S against 2 with its spread.

## Locality

1. **Each detector alone sees half and half,** whatever the other one chooses.
2. **The answer's path runs back from the first click to the birth and forward to the partner,** within the cones (item 4 above).
3. **In these runs the two clicks of a pair stand one mesh apart,** since row 56 reads a child's first click at its own clock. So the write at the first click reaches one mesh, within one link per tick.
4. **For children that travel apart before they click,** the same act would write the partner's axis across the board at one moment. That contradicts the owner's word of 2026-10-25, 08:02 UTC ("everything always local ... entanglement of clicks") in the board's sense, and his leave of 02:50 UTC covers it.

## For the Boss

1. **The OK, by the owner's order: the click solution works in the toy.** S = 2.73 with a spread of 0.11 over 688 pairs, no message, the cone kept, the board untouched, the rewind exact, and the full check at 117.
2. **For the engine:** the detectors' directions and the outside choices go in the world file (a detectors key), not in a module setting. The answers stay readings of the click line, and row 56 reads them with S's spread.
3. **The contradiction is named in Locality item 4.**
