# Notes 01: what the probes measured, in the order they were run (the second text's deriver, 2026-10-30)

## The library and its checks

fb_lib.py is the first text's, copied and extended (the first text's functions kept as they were, for the comparisons).
Before any probe: the ring model (one row on a given clock) against an independent per-site loop at e = 1/2, 300 rounds:
0 misses; against the board's light row (tick_board_m on 1 x 1 x 16, the board's own 00 history as the given clock),
200 rounds: 0 misses. So every ring number is the board's act on one row.

## The order of findings

1. The derivation (00_notes_derivation.md) gave the counting tooth, the pivot dial and the mirror's M. The first sanity
   run: the c = 0 control equals the act as built 40 of 40; the 6-grip standing lay equals the first text's 40 of 40;
   moving and non-uniform lays run back 40 of 40 with the books at 0; the first text's mirror on the Mesh tooth 25 of
   40; the first text's dial with the Mesh tooth breaks its promise at round 8 on the standing non-uniform lay and at
   round 3 on the moving one; Big Pic's own-dial tooth at round 8.
2. The first stability check on the physicist's ring lays (6000 rounds) was meant as a confirmation and was not one:
   bounded on the staggered uniform clock and at e = 1, growing at e = 1/10 faster than the first text's act.
3. The controls isolated it: the uniform clock at 1.1 L_0 in phase is bounded; the same e = 1/10 lay with its two
   junction Meshes cut is bounded; Big Pic's own-dial tooth grows faster still.
4. Scans (exploration, fb2work/, not probes): the contrast (e = 1/2 the worst, x2^51 in 8000 rounds), the coupling
   (bounded at a quarter of the grip on the step lay, the smooth well growing at every coupling but slowly at a 64th),
   seven rules (none bounded on the well), the lever m = 1, 2, 4, 8 (no cure), and a linearized period map in floats
   (exploration only; never quoted as a measurement): the first text's kick grows on every lay at a rate in
   proportion to the coupling, every two-ended rule only in resonance bands that narrow with the coupling. These
   decided what the probes had to show; the numbers quoted in FWDBACK2.md are the probes' own.
5. probe_mt6 (the steps): Big Pic's numbers reproduced in the engine's floor act; both teeth at the density reading's
   level. On the mathematician's ring the difference with the flat run read his flat run's left-moving remnant (the
   density reading showed -129); his own measure (the extreme of a on the near side) gives -14 for it and for this
   text's tooth.
6. probe_mt7 (the readers' lays, 6.5 minutes): the table of section 4.
7. probe_mt2 (the board): the twelve lays pass; the books' identity holds at every round (the spring lays' 00 row
   moves by exactly its spring's paid pushes, which a plain "drift" line had first misreported as a move of the
   books); the mutants fail as derived; the moving 00 lays keep their clocks.
8. probe_mt5 (hostile): case H leaves the domain at round 4 under this text's act (the 00 row's swing between two
   sites a full L_0 apart carries one below rest); the first text's doubling lay had L(before) = 0, which this text's
   run back reads as a dial of 0 (a division by zero): laid from 2 L_0 instead. Outside the domain on a standing clock
   a turn of 2 runs back (the gear's carry always taken), noted as OPEN.
9. probe_mt4 at 10 rounds did not finish in five minutes (the plan's quartic products); 6 rounds, as the first text.
10. probe_mt8 (seven rules) made the exploration's rule comparison a probe.

## The rules audit

A token scan of fb_lib.py and every probe for "/", "//", "%", "**", float, math, random, fractions, decimal, sqrt,
round, divmod, pow: two index slips found and replaced by the carry (fb_lib's Mesh numbering, nb.shape[0] // 2;
probe_mt7's mode index, x % 8), neither changing a value; then clean. The reruns were taken after the fix.
