# The beat read free of the phase: the act

David, 2026-10-27, 16:3x UTC, for the Boss (part C of his task of 16:01 UTC), on the owner's word of 15:5x UTC, "Yes to all, by your recommendation" (item 7: the beat read free of the phase). Measured on the head 0d59ff812, and pair_3 measured again on 5f8680de2 with the same hashes (DAVID-OWN-BEAT_CHECKS.txt). No src touched.

## The finding

The head's beat (bobs.py) counts the zero crossings of the three gear, the hand's real part. A global turn of one hand (z -> i z on its notches, now and before) changes nothing physical, yet it moves the crossings and so the chimes. A hand swinging on a line (a sea laid at sense 0), turned onto the twelve gear, never crosses at all, so it never chimes.

## The act (one change in the chiming)

1. **The reference.** At the first tick of a winding (wound goes from 0 to 1), the hand's notch now (three, twelve) is kept at the clock as its reference. Where that notch is 0, the next tick's is kept. The crossing timer restarts there (crossed = 0).
2. **The beat.** The head's crossing rule (CK-S1: the product of the two readings below 0, or exactly one of them 0) is read on the dot of the reference with the notch, r3 three + r12 twelve, before and now, in place of the three gear's notches. The beat is the ticks between two such crossings, as at the head.
3. **The chime stands:** wound >= beat > 0, as at the head.
4. **The rewind.** The reference is state: it goes into the rewind note's counters and into the state the rewind compares, two arrays per hand.

A turn of the hand by any Gaussian g multiplies the dot by |g|^2, which keeps its sign. So the beat reads the hand's own angle and no global phase. The act adds one product sum per clock in whole numbers, and no formula.

## Measured (120 ticks; every run's rewind 20 of 20)

"Turned" is the hand's train turned a quarter at the seed. "The same" means the chimes' list of (tick, clock, hand) hashes the same.

| world | the head's beat: unturned / turned | the own beat: unturned / turned |
|---|---|---|
| plasma_3 | 135 / 135 chimes, moved (the first at tick 4 / 3) | 135 / 135, the same |
| pair_3 (a hand on a line, sense 0) | 81 / **0** | 108 / 108, the same |
| universe_3 (two hands, senses +1 and -1) | 189 / 216 | 189 / 189, the same |

**The tests for the Boss:**

1. The chimes' list is the same under a quarter turn of the chiming train, on all three worlds.
2. The rewind is exact with the reference in the state.
3. pair_3 chimes after the turn.

## The charts it moves (their own ticks, the rewind 20 of 20)

| chart | chimes | fittings |
|---|---|---|
| the hole | 2,262 to 2,341 | 18 to 13 |
| the chiral | 3,003 to 4,526 | 16 to 16 |
| the bodies | 17,944 to 18,300 | 23 to 26 |

The Boss regenerates them once with the wave.

## Not the beat's (for the list)

A quarter turn of the light at the seed moves the hole and the chiral under either beat:

| chart | the head's beat | the own beat |
|---|---|---|
| the hole | fittings 18 to 20 | fittings 13 to 18 |
| the chiral | fittings 16 to 18 | fittings 16 to 15 |

The fittings read the light's gears one by one: the child is laid at the fixed notches (A, B), and the draw reads the fine teeth. Whether these are read free of the light's phase too is a separate question for the owner's word.
