# The amplitudes on the great clock: a hand's norm, its sweep and the standard's length

David, 2026-10-27, 14:5x UTC, for the Boss, on the owner's word of 12:4x UTC and the Boss's readings (a) to (e) with his addendum of 12:4x UTC.

## The words

The owner, through the Boss, in translation: "And then there is a beautiful solution for the amplitudes on the board... check whether there is a coherent picture with David; if yes, put it into the code and push."

The Boss's correction of his own reading (b): the owner's rule of 11:3x UTC says no formula in the engine, so a typed a^2 = n rim T / (2 s) would be a formula; a coherent solution is an act of the clock.

**The marks:**

- **measured:** on the clock head 41ad9bc81 (the identities also on boss-spin-1 5850be5b7), by the scripts in DAVID-AMPLITUDES_CHECKS.txt;
- **checked:** whole-number algebra;
- **read:** read in the code.

**The names.** A hand is one complex number z = three + i twelve, a Gaussian integer, per notch (z_now, z_before). Its ratio is rho = pinion + i s, with |rho|^2 = rim^2 exactly (the loader refuses a pair off the rim's circle, MS-S2). The sweep is W = Im(conj(z_now) z_before), the engine's three_now twelve_before - twelve_now three_before (hands.sweep). e = T div 2 = A B.

## The verdict

**Yes: a coherent picture, exact in whole numbers.**

1. **The wind is a norm.** At the vacuum a uniform hand's wind is the mean of two Gaussian norms: the before-hand's distances from its two rest predictions, one per sense.
2. **The sweep is the count.** At rest the wind is SPOKES times the sine times the sweep, up to the lay's two remainders. So a rest hand's quanta are its sweep in e, and the setting's count, the charge and Pauli's count are one count.
3. **At one clock the wind is the same for every family.** One e costs at least one light quantum, and the quarter turn at equal norms costs the least. That is the child's lay (A, B), derived and not declared.
4. **The standard's length follows from the rim.** With X = Gamma rim, every state integer and every reading line of the three charts stands bit for bit, and one declaration goes.

**Into the code, in order:**

1. X derived (a fold).
2. The identities as the engine's own tests (a fold).
3. The rest lay carried (moves records: the owner's word on them).

**Not into the code:** a typed amplitude. No one division reproduces the searches, and the searches are the clock's own act: they read the wind by comparisons and contain no formula.

## 1. (a) A rest hand's wind is its norm times its chord

### The vacuum's gearing

At the content 0 (p_0 = Gamma, every mesh's factor G^2) [read: core/rule3.gearing]:

| | value |
|---|---|
| teeth | w = SPOKES rim Gamma^2 G^2 |
| spring | D = 2 SPOKES (rim - pinion) Gamma^2 G^2 |
| each grip | R = 2 pinion Gamma^2 G^2 |
| hold | S = 2 w - D - SPOKES R = 0 |

In a uniform lay every neighbour's gears equal the clock's, so the meshes' shared term is 0. The wind's division is exact: (2 own) Gamma / (4 Gamma^3 G^2) = 3 [rim (n^2 + b^2) - 2 pinion n b] per gear.

### The wind as two norms

```
wind = 3 [rim (|z_now|^2 + |z_before|^2) - 2 pinion Re(conj(z_now) z_before)]
     = (3 / (2 rim)) (|rim z_before - rho z_now|^2 + |rim z_before - conj(rho) z_now|^2)
```

So **the wind is the mean of two norms**: how far the before-hand stands from the rest prediction of each sense. [checked]

**Measured:** hands.wind equals the first line on every sprung hand of the toy, the middle and ga2:

- at every amplitude from 1 to 3,000 and at nine large ones;
- for the three senses;
- 0 off in 9,027 per hand.

### The bound, and equality at rest

```
wind >= SPOKES s |W|
```

Equality holds exactly at rest, where z_before = z_now rho / rim or z_now conj(rho) / rim.

**The proof.** Write P = Re(conj(z_now) z_before). Then rim (|z_now|^2 + |z_before|^2) >= 2 rim sqrt(P^2 + W^2), and the least of 2 rim sqrt(P^2 + W^2) - 2 pinion P is 2 s |W|, at P = pinion |W| / s. So the rest hand is the hand of least wind for its sweep. [checked]

### The code's rest lay

The code lays a rest hand as:

- three_now = a;
- three_before = (a pinion) div rim, with the remainder r1;
- twelve_before = sense (a s) div rim, with the remainder r2.

Its wind is then:

```
wind = SPOKES s |W| + 3 (r1^2 + r2^2) / rim      (rim divides 3 (r1^2 + r2^2))
```

[checked; measured: 0 off in 6,018 per hand]

The winding is 3 T s = SPOKES s e on every sprung hand [read: rule3.winding_of; measured]. So:

```
wind / winding = |W| / e + (r1^2 + r2^2) / (rim T s)
```

**A rest hand's quanta are its sweep in e.** The remainder adds less than 2 rim / (T s) of a quantum:

- 5.6 x 10^-5 for a heavy hand;
- 0.104 for the toy's light lift, where rim / s = 1,863.

### The Boss's two forms

- **E = 12 G^2 (rim - pinion) a^2 (Gamma^2 + p_0^2 pinion / rim)** is the own form of the unrounded rest lay at any clock rate. At the vacuum it carries the weight to 6 a^2 s^2 / rim, the Boss's limit.
  - Measured: wind / (6 a^2 s^2 / rim) runs from 0.99874 to 1 at a >= 10^6, and to 12 digits at 10^12.
  - Since rim - pinion = |rho - rim|^2 / (2 rim), the squared chord, the Boss's "norm times chord" holds.
- **In the sweep:** the unrounded rest hand sweeps W = a^2 s / rim, so 6 a^2 s^2 / rim = SPOKES s W. In clock words: **a rest hand's wind is SPOKES times its sine times its sweep.** The Boss's "SPOKES times the rim times its twelve shadow squared", 6 rim (a s / rim)^2, is the same number before rounding.
- **The oscillator's law.** n quanta at rest read a^2 = n rim e / s, proportional to n / omega.

## 2. (b) The amplitude for n quanta: the searches stay

There are three searches:

- setting.set_even: the least a whose wind passes n windings;
- setting.fitted: the largest a whose summed packet wind stays at most n windings;
- cycle.least_share: the light's least A whose least wind over the board reaches n windings.

### Uniform, set_even

Measured on every sprung hand of the three universes: the three senses at n = 1 to 200, so 600 cases a hand and 4,200 in all.

| hand | rim / s | the typed form a^2 = n rim T / (2 s) agrees | the sweep's count agrees |
|---|---|---|---|
| toy's light lift | 1,863.3 | 0 of 600 | 198 of 600 |
| toy, heavy | 1.013 | 506 | 548 |
| toy, heavy | 1.015 | 516 | 552 |
| middle's light lift | 171.25 | 53 | 256 |
| middle, heavy | 1.050 | 498 | 549 |
| ga2, two hands | 1.000 | 391 each | 508 each |

A miss is one notch for a heavy hand. For a light lift it is hundreds of notches: on the toy at n = 1, the search lays 5,690, the typed form 5,792 and the sweep's count 6,000.

### The packets, fitted (the middle's heavy hand)

| width, quanta | the search | the typed form at the packet's own weight | the sweep's count | wind / (SPOKES s W) |
|---|---|---|---|---|
| 2, 125 (the bodies' lay) | 823 | 822 | 839 | 1.0343 |
| 3, 218 | 598 | 596 | 603 | 1.0172 |
| 3, 600 | 990 | 989 | 999 | 1.0172 |
| 1, 125 | 1,464 | 1,463 | 1,537 | 1.1031 (= rim^2 / s^2) |

At the search's amplitude the bodies' packet holds 124.54 windings of wind and 120.41 e of sweep. A packet's wind passes its sweep's count by its meshes' energy, the price of holding a hand at a few clocks.

### Verdict on (b)

- **No one division reproduces the searches.** A typed a^2 = n rim T / (2 s) is the formula the owner's rule of 11:3x UTC bars. It also moves the charts of every world laid by the fourth form, the packets and the cycle.
- **The searches are already the clock's own act:** each reads the clock's wind and compares.
- **The norm carried** (the Boss's correction) does not help either:
  - N = (n rim e) div s with its remainder on a fine wheel is one carry, but the hand's amplitude is then N's root, which is a search (largest_below);
  - a Gaussian hand of norm exactly N exists only where N is a sum of two squares.

  So it removes no search and still moves the charts.
- **What the picture gives the searches** is their reason. They land at a^2 ~ n rim e / s, and the two counts they could read, the wind (the energy) and the sweep (the charge), agree at uniform rest and part in a packet by its meshes' energy.

## 3. (c) The rest form as a Gaussian carry

### The head's lay is off the rest velocity

A hand's gear rides at the mean wall W = (w div 2)(X_before + X_now). Its momentum is P = W (now - before) + fine - mid(W), the half wall being the momentum's zero [read: tick.impulse].

The head lays three_before toward zero and leaves the fine wheel at the half wall. So the lay's momentum passes the rest momentum by W r1 / rim on the three gear and by W r2 / rim on the twelve gear: up to one notch per tick [checked].

- **A heavy hand** at a = 135: under 1% of its velocity.
- **The toy's light lift** at a = 5,690, whose three gear rests at 0.0008 notch per tick: the error is 0.9992 notch per tick, 1,200 times its rest velocity. The head's rest light lift runs off at one notch per tick.

### The carried lay

One carry per gear. N_exact is the rest lay's own numerator: a pinion on the three gear, and sense a s on the twelve gear, summed over the senses laid. W div rim = 3 Gamma^2 G^2 (X_before + X_now) is a whole number at every clock.

```
V      = W now - (W div rim) N_exact + mid(W)
before = now - V div W
fine   = V mod W
```

**The lay's momentum is then the rest momentum exactly,** counted in the fine wheel's teeth, and its before is the head's to one notch (asserted at every clock laid).

On the twelve gear the two senses give V(-1) + V(+1) = 2 mid(W), the wall itself at an even wall: the two's complement. So the carried lay spells the negated line's mirror (F48-S1's) by its own numerator, with no act beyond the carry. [checked]

### Measured, one clock at the vacuum

This is the riding gear's own kick and carry (tick.impulse and tick.carry, a uniform hand). It reproduces the engine's light lift at ticks 1, 10 and 30 to the notch.

**The toy's light lift (rest velocity 0.0008 notch per tick), its three gear:**

| tick | the rest orbit | the head's lay | the carried lay |
|---|---|---|---|
| 1 | 5,690.0 | 5,691 | 5,690 |
| 10 | 5,689.9 | 5,700 | 5,690 |
| 30 | 5,689.3 | 5,720 | 5,690 |
| 300 | 5,616.4 | 5,987 | 5,690 |
| 1,000 | 4,890.1 | 5,864 | 4,947 |

**A heavy hand at a = 135:**

| tick | the rest orbit | the head's lay | the carried lay |
|---|---|---|---|
| 1 | 21.9 | 23 | 22 |
| 30 | -23.2 | -24 | -25 |
| 1,000 | 116.9 | 108 | 134 |

### Measured, in the engine (a sea of one quantum on a 3-cube with the light's sea)

The light lift's three gear:

- **the head's lay:** 5,691, 5,700 and 5,720 at ticks 1, 10 and 30;
- **the carried lay:** 5,690 at all three;
- **the rest orbit:** 5,690.0, 5,689.9 and 5,689.3.

**Not at rest to the tooth**, for two reasons:

- The leapfrog carries the velocity's fraction and not the position's, so a slow gear moves only once its velocity reaches half a notch: 57 notches behind the orbit at tick 1,000.
- The hand's wind loads the regulator, so its rest orbit is the loaded clock's: both lays' twelve gears lag the vacuum's orbit alike, 74 and 75 against 91.6 at tick 30.

For the heavy hand the two lays part by a few notches, inside the integer orbit's own drift: at tick 1,000 they stand 9 and 17 notches off the orbit.

### What moves

**Every world laid at rest:**

- the bodies' chart;
- the tests' fourth-form worlds (pair_3, plasma, plasma_3, universe, universe_3);
- the tests' packet worlds (collapse 500, 800 and 1,200, emission, emission_one, packet).

**The hole and the chiral lay no rest hand and stand as they are.**

**Measured on the bodies' world (120 ticks):**

| | the head's lay | the carried lay |
|---|---|---|
| the lays' amplitudes | 823 and 823 | 823 and 823 |
| befores moved one notch | | 19 clocks of each packet, the three gear |
| fittings | 23 | 21 |
| chimes | 17,944 | 17,870 |
| turns | 2,270 | 2,426 |
| the rewind | 20 of 20 | 20 of 20 |

On plasma_3 (100 ticks), the light lift's three gear moves one notch at its 27 clocks. The counts stand (0 fittings, 135 chimes, 27 turns), and the state moves.

This is a new clause of the setting: the lay carries its own remainder, where every gear is born at the half wall. **It is the owner's word.**

## 4. (d) The standard's length derived from the rim

**What X is.** The standard is the meshes' turning hand: its pair at a count is X e^(i n theta_0), with theta_0 about 1 / Gamma, and the mesh turns an arrival by it to the notch, (X^c c - X^s s) div X [read: meshes.through_mesh]. So X is the turn's resolution. Above a world's floor the turn rounds to the same integers.

**Derived: X = Gamma rim.**

- The standard's first step, X div Gamma, is then the rim exactly, so one count of the standard sweeps one rim of arc. The meshes' turning hand and the rates' circle (rho on the rim's circle) are measured by one length.
- It is a multiple of Gamma, which first_pair needs.
- It is far above the floor of 23 Gamma.
- X = Gamma (rim div Gamma), the rim to whole Gammas, is the other spelling, and it is measured the same.

**Measured.** The three committed charts were regenerated from their worlds with each derivation in place of the declared 288,230,376,000. Against the committed chart, all of these are the same:

- the Node lines, the rows, the counts and the turns;
- the run back, 20 of 20;
- the log, but for two fields;
- the reading, line for line.

| chart | X = Gamma rim | X = Gamma (rim div Gamma) |
|---|---|---|
| hole | 15,162,856,759,112,389,000: same | 15,162,856,759,112,000: same |
| chiral | the same X: same | the same X: same |
| bodies | 1,655,909,141,000: same | 1,655,909,000: same |

**What moves:**

- two fields of every chime's frame: X, and the phase pairs read at X (bobs.py:93 and :99). The frame records the scale the reckoner reads it at (reckoner.py:248), so every reading stands;
- the universe files lose the key `amplitude`: tests/worlds universe_toy, universe_middle and universe_ga2, and The-One-Record-Of-Nature's copy;
- the committed charts are regenerated for their embedded universe and those two fields alone.

## 5. (e) The child's lay read from the norm

**The child's lay.** (A, B) = balanced_notches(e), with z_now = sense A on the three gear and z_before = i B on the twelve gear: a sweep of sense e [read: unspring.fitted_notches, MS-S1].

**At one clock the wind is the same for every family:**

```
wind = 3 rim (|z_now|^2 + |z_before|^2)      to within 6 (the meshes' halves' floors)
```

[checked; measured: every hand of the three universes, five lays, at most 6 off]

Since |z_now|^2 + |z_before|^2 >= 2 |W|:

- one e at one clock costs at least 3 rim T, one light quantum (the unsprung's winding 3 T rim = SPOKES rim e);
- the least is at the quarter turn with equal norms.

(125, 144) is the clock's nearest: A B = e exactly and A nearest B, at 1.010028 light quanta. **So the child's lay is the norm's least for one e at one clock: derived, not declared, and the same for every family.**

**G0 stays withdrawn.** A child at its own family's rest form at one of its own quanta is a one-clock hand of norm a^2 = rim e / s. Its wind is 6 rim a^2 = rim / s light quanta: 1,863 for the toy's light lift and 171 for the middle's, so it is never born.

**The two bounds:**

| where | the wind is at least |
|---|---|
| uniform | SPOKES s \|W\| |
| one clock | SPOKES rim \|W\| |

Their ratio rim / s is what it costs to hold a slow family's quantum at one clock.

## 6. The smallest build, in order (the Boss's)

1. **X derived from the rim.** A fold of every state integer and every reading:
   - features/standard: the length from the rim, X = Gamma rim, carried above the floor as now;
   - clock.py reads it there;
   - assembly/piece.py refuses the key `amplitude` by name as a declaration;
   - the four universe files lose the key;
   - the three charts are regenerated for the frames' two scale fields;
   - tests/test_the_phase_line.py's amplitude test re-cut to the derived length.
2. **The identities as the engine's tests.** A fold; no engine file changes:
   - the uniform rest wind is SPOKES s |W| + 3 (r1^2 + r2^2) / rim;
   - the uniform wind is the mean of the two norms;
   - the one-clock wind is 3 rim (|z_now|^2 + |z_before|^2) to within 6;
   - the winding is SPOKES s e.
3. **The rest lay carried,** on the owner's word on the moved charts: one carry per gear in setting.rest_hand's lays (the formula in section 3), refused nowhere, every gear's before within one notch of the head's.

**Not built:**

- the typed amplitude;
- the norm-laid hand.

## 7. For the owner's word

1. **The rest lay carried** (section 3) moves the bodies' chart and eleven test worlds; the hole and the chiral stand as they are.
2. **Which count a lay's "n quanta" names:**
   - the wind (the energy), as now: a packet of 125 holds 120.4 e;
   - or the sweep (the charge, Pauli's count): the packet is laid at 839, holds 124.9 e, and its wind is 129.2 windings.

   The two agree for a uniform hand at rest. Moving the count to the sweep moves every chart laid at rest, and the bobs' count with it.
3. **X derived** needs no word beyond the owner's rule against declarations: the state and the readings stand.

A document and its checks; no file of the engine head changed.
