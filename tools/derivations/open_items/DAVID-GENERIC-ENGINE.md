# The generic engine: the twelve integers, the fifteen branches, the refusals

David, 2026-10-27, 15:5x UTC, for the Boss (his seventh consultation, the task of 12:2x UTC), on the owner's words of 11:3x UTC to the Scribe, with the Scribe's full read (6446048473). On the head 608d97134 (DAVID-GENERIC-ENGINE_CHECKS.txt).

## (A) The twelve integers: each derived, bit for bit (a fold)

An AST scan of the engine proper (the readers apart) finds exactly twelve literals beyond 0 and 1. Each is derived from the world file's shape (d = its length) or from 0 and 1, and each derived value equals the typed one:

| typed | derived |
|---|---|
| spokes.AXES = 3 | d, the world's dimension |
| spokes.SIDES = 2; trains.HAND = 2; POWER_AXIS = 2; acts.mid's, rule3.half's and odd's 2 | 1 + 1 |
| trains.POWER_TIME = 4 | d + 1 |
| meshes.mesh_teeth's 4 Gamma | twice the standard's rate 2 Gamma |
| cycle.QUARTERS = 4 | the least k with i^k = 1, by the Gaussian product |
| setting.HALF_SPANS = (1, 2, 3) | the h whose doubled cosines close at the half turn: the crystallographic restriction, searched until it fails |

With them the shapes follow:

- REGULATOR = (d + 1)(d + 2) / 2, the symmetric tensor's parts (DAVID-TENSORS.md);
- OFFSET = d + 1.

**The cost:** AXES becomes the world's, read at the load, and its 58 reads go through the Clock.

## (C) The refusals: the four fixed trains derived, so nothing is left to refuse

**Measured on every committed universe file** (6 of 6): the four fixed trains are exactly the ones built from d and den alone:

| train | built as |
|---|---|
| the light | shape 2 at (den, den) |
| the regulator | shape (d + 1)(d + 2) / 2 at (den - den div Gamma, den) |
| the offset | shape d + 1 at (den, den) |
| the phase clock | shape 1, wall 1 + 1 |

Built in the files' own order (the light first, then the file's gapped rows, then the regulator, the offset and the phase clock), every world's row index stands.

**So the universe file holds the matter alone:** den, Gamma, T, the trace, and the gapped pairs.

- trains_of's refusals of the roles fall away.
- What remains is one refusal: a shape the law does not read. A gapped shape-2 train is a hand, and a gapped shape-4 train is twin hands.

**A fold of every state integer.** The records' embedded universe loses four rows.

## (B) The fifteen branches: two numbers read, most of them folds

Every branch on a train's identity reads one of two numbers:

1. **The spring 0** (pinion = rim: the light, the hand with no gap). This is the taker every take draws on and the hand that chimes into no one:
   - bobs.py:33;
   - striking.py:46, 67, 131, 188;
   - unspring.py:125, 127, 209, 215, 233;
   - setting.py:53, 59, 68, 80;
   - tick.py:283;
   - clock.py:69.
2. **The shape d + 1 at the spring 0** (the offset): its time gear is the one the charge kicks (tick.py:219).

**Where the act is a product, the branch is the coupling** min(spring, 1), which is 0 for the light and 1 for matter, with the same integers:

- the meeting's charges (striking.py:67) are the coupling times the sweep, so the light's product w[0] w[1] is 0 and no rest meeting is read;
- the counters of a chime (bobs.py:33) take the coupling times each trigger (the standing, the crossing), so the light's counters stay 0 and it never chimes into itself;
- the emission's gear is the taker's.

**Where the act itself differs, the branch is physics, not spelling.** The light's take (the least count toward its before) and the merger's take (the record's levels taken whole) are two acts, as are the light's drift seas and the matter's rest seas. One act for both moves the charts, so it is the owner's word. The close's own book comes first (DAVID-CLOSE-LAW.md items 1 and 2).

## In order, ranked by what the owner gains

1. **(C) The universe file as the matter alone.** It removes the five role refusals and four rows a file, a fold.
2. **(A) The twelve integers derived.** A fold, with the counter at 0 in the engine proper.
3. **(B) The product branches as couplings.** A fold.
4. **(B) The two takes and the two seas as one act each.** The owner's word.
