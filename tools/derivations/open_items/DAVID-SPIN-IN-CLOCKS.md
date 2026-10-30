# Spin one half in the clock's words: the twin hands

David, 2026-10-27, 13:4x UTC, for the Boss, on the owner's words of 12:02 and 13:10 UTC.

## The words

The owner, to David, in translation:

- **12:02 UTC:**
  - "There is no former spin, right? Everything moves to the new spin, derived from the clocks, the great clock and the chimes."
  - "Only when spin and spin one half are solved completely, pass it to the Boss, and explain what it is in clocks, on the great clock and at the chimes."
  - "Matter is symmetric and force carriers are not, and that brings Pauli; on the great clock it is something else, with the phase, and at the chimes something else."
- **13:10 UTC:**
  - "Give the solution in the clock's language and not in the former language; make sure everything is solved for spin."
  - "Is a hand in this actually a complex number?"

**The language.** Every name below is the clock dictionary's (DAVID-CLOCK-NAMES.md), and the code is the engine's own since the Boss's 67a7633d5. The phenomena keep nature's names: spin, Pauli, Kramers, Zeeman, Stern-Gerlach.

**The marks:**

- **measured:** on the build DAVID-SPIN-IN-CLOCKS_DIFF.txt (67a7633d5 plus 7 files, +161 -37), by the scripts in DAVID-SPIN-IN-CLOCKS_CHECKS.txt;
- **checked:** whole-number algebra;
- **read:** read in the code;
- **derived:** derived here.

## 1. A hand is a complex number

**Yes.** A hand is two gears, its shadow on the three-o'clock line and on the twelve-o'clock line. So a hand is one complex number, three + i twelve, and both parts are whole numbers: a Gaussian integer.

- The hand's quarter turn (three, twelve) -> (-twelve, three) is the multiplication by i.
- A hand's rest rate turns it by the ratio's angle, cos omega_0 = pinion / rim. Rule3 does this on each gear by its carry, with no cosine taken.
- The sweep, the area one tick of the hand spans, is the hand's charge.

**A sprung train of twin hands is two complex numbers**, (up, down): exactly the spinor of spin one half. The Pauli gearing on it is whole swaps and signs on the four gears:

- sigma_x swaps the twins;
- sigma_z reverses the down twin;
- sigma_y = i sigma_x sigma_z.

The half turns' lifts -i sigma_a are whole too, so two half turns give -1. [checked: DAVID-SPIN-DOUBLET_CHECKS.txt, item 1]

## 2. The build: the twin hands

| what | the engine's act | where |
|---|---|---|
| a twin train | a sprung train of four gears at a ratio not the regulator's is a pair of twin hands, read from its count of gears and its ratio (no key, no new size) | trains.trains_of, Train.twin |
| the fitting | a fitting's two fitted hands go on the twins, the - fitted on the drawn hand and the + fitted on its twin, so the spin is kept and the unsprung carries none | trains.twin_of, striking.jam, unspring.fitted_advanced |
| the unspringing | two quanta of one twin train engage across the twins (the hand at the mesh's +a end, its twin at the other, opposite in sweep); each end unwound from its own hand | striking.engage, striking.twin_at, unspring.read_ends |
| the gearing to the offset | the offset's one-mesh curl Phi turns the twins through the Pauli gearing, per gear SUM grip SUM_a Phi_a (sigma_a x); one carry at the drive teeth SPOKES (full rate + full rate), the fine tooth kept on the gear's drive wheel, so nothing is thrown away and the rewind is exact (g = 2: grip / (2 full rate) per spoke) | tick.Tick.twin_pulls, tick.offset_curl |
| the setting | a lay names the hand of a twin train ("hand": 0 or 1) | assembly.setting |
| the chart | a twin fitting names its + hand; a twin unspringing names each end's hand | run.fitting, unspring.unspring_end |

**No switch stands in the engine.** The tests' controls each replace one function:

- the twins' pulls off: Tick.twin_pulls;
- a held curl: tick.offset_curl;
- the neutral control, the offset's turn of the twins off: meshes.coupling_of.

**The engine's own checks on the build:** the suite 106 of 106, ruff, ruff format and mypy. The numbers gate holds: no integer beyond 0 and 1 is added and no string is added outside the setting's key table. The diff applies whole on 0660dd42e as well, and the owner's rules as gates (tools/engine_gates.py there: no literal beyond 0 and 1, no read of a train by its identity) hold with it. [measured]

## 3. What it is, in clocks, on the great clock and at the chimes

### In clocks

**The twins.** A matter train is twin hands at every clock, and a force carrier is one hand. The offset's curl is a gear between the twins, and its ratio is one half:

- the twins' axis (the spin) turns once around when each twin has turned half a turn against a free twin, so the hands read -1;
- two turns of the axis bring them home.

**Nothing in the build sets the half.** The gearing is the Pauli gearing, and the measured hand follows cos(theta / 2) (below).

**Kramers' reversal** carries the up twin onto the down twin and back with a sign, and twice gives -1. A one-hand train has no such reversal: on one hand every reversal squares to +1. [checked; measured]

### On the great clock, with the phase

**The setting.** One mode: the heavy lift's up twin set even at every clock of a 5-cube, with a held curl along x and the neutral control.

**The reading.** The spin's part S_z / N of the twins' wind, and the overlap of the twins' gears with the same run with the twins' pulls off:

| the spin's turn theta | tick | S_z / N | the overlap with the free run |
|---|---|---|---|
| pi | 7 | -0.952 | -0.153 |
| 2 pi | 15 | +0.943 | **-1.007** |
| 3 pi | 25 | -0.989 | +0.039 |
| 4 pi | 36 | +0.977 | **+1.006** |

**So S_z = cos(theta) and the overlap = cos(theta / 2).** The spin is home after one turn, and the hands only after two. This is the owner's "on the great clock it is something else, with the phase": the -1 lives in the hands' phase, which no reading of one hand shows. [measured]

### At the chimes

**What a chime is (read: bobs.py).** A sprung hand wound at a whole winding through one beat chimes, and the unsprung hand pays one winding. The chime names its hand, so every chime names its spin.

1. **Pauli.** Counted by the sweep, every chime of every twin hand, on the hole and the chiral as twins, has at most one sweep of e (the key's half) at its clock, and so does every clock at every tick: two bobs per clock per train, on opposite twins. **The sweep is the count:** each fitted hand carries one e. The wind is no count, because a hand held at one clock by a slow rest rate moves fast, about 1,863 of its own windings for the light lift. [measured]
2. **Kramers.** With no curl, the twins beat alike: 625 and 625 chimes, every beat 2 ticks. [measured]
3. **The two beats (the Zeeman doublet).** In a held curl along z:
   - the up twin beats slower and the down twin faster: 375 chimes with beats 2 and 3 (mean 2.333), against 750 chimes at beat 2;
   - the one-tick shift on the gears is +15 on the up twin and -15 on the down twin, the derived pinion B0 x div (3 rim full rate) to the notch.

   [measured]
4. **The full turn's sign.** Both twins are set just below one winding, so no bulk clock stands, with the curl held in the half x < 3. The boundary clocks stand when the two halves' hands are opposite:
   - **1,224** chimes at the boundary while theta is below 495 degrees (around 2 pi);
   - **0** from 495 degrees on (through 4 pi, to 786 degrees);
   - the bulk chimes 1,584 times all along.

   The spin points the same way at 2 pi and at 4 pi, and the chimes tell the two apart. [measured]
5. **The two spots (Stern-Gerlach).** A slab of the twins (z = c - 1 .. c + 1, even across x and y), with a held curl along z with a gradient, Phi_z = 400 + 4000 (z - c), and the neutral control:

   | | up chimes | down chimes | weighted by the beat | the great clock's wind |
   |---|---|---|---|---|
   | twins' pulls on | 2,268 | 1,944 | up **+446**, down **-328** milli | up +565, down -574 |
   | twins' pulls off | 1,377 | 1,377 | 0 and 0 | 0 and 0 |

   Each chime is weighted by its beat, because a chime comes once a beat and a slowed twin chimes less; so the weighted count is the time wound. **A charged twin train does not split.** With the offset's turn of the twins on and the field laid as the offset's odd gear, the orbital pull drags both twins alike: the great clock +68 and +56 milli against the control's +37 and +37, and the bobs scatter (171 chimes). That is Bohr's reading of free electrons, so Stern-Gerlach needs a neutral spin one half, as Stern and Gerlach's silver was. [measured]
6. **Force carriers symmetric.** The unsprung hand stands at many windings where bobs chime: up to 12,865, 20,666 and 1,849 of the bob's windings on the head's hole, chiral and bodies charts. It pays one winding per chime, and N windings set in its one hand at one clock hold N (DAVID-STEP-3.md section 2). [measured]
7. **The spin kept at the striking.** On the hole 60 and the chiral 60 as twins:
   - **fittings:** 38 and 34; fitted up 32 and down 32 on each, every fitting on opposite twins;
   - **unspringings:** 6 and 2, every one across the twins;
   - **the spin made by the striking:** 0;
   - **the rewind:** 20 of 20, and 20 of 20 again with the twins' pulls on (a field left to the engine, and a held curl).

   [measured]

## 4. The owner's law, read in his two places

**On the great clock, with the phase:**

- matter is a symmetric pair of twin hands: one rest rate (one beat with no curl), each twin carried onto the other by Kramers' reversal, which squares to -1. Its phase needs 4 pi.
- A force carrier is one hand with no twin. Its phase is back at 2 pi.

**At the chimes:**

- matter is antisymmetric: one sweep per hand per clock. A second fitted hand is jammed where its hand stands, because n fitted hands on one hand at one clock would sweep n^2 e. So a train holds two quanta per clock, one per twin.
- The carrier is symmetric: N windings in its one hand at one clock.

**One number decides both**, the count of hands in the train: the twins bring Pauli, and the one hand shares. **Asked of the owner** in Hebrew: whether this reading is his. [derived; measured]

## 5. What stays open, by name (each the owner's word or a step of the build)

1. **The 48 on the twins' gears.** The half turns' lifts are whole, and the Pauli gearing is covariant under them (checked). On the gears the reversal of a gear needs the reversed gear's own flip, (teeth - fine) mod teeth (F48-S1, derived and not built): that is the engine's own open item, for every hand alike.
2. **Two readings of a hand's phase.** The beat reads the three gear's crossings, and the vernier reads the fine teeth. So the twins' quarter turn (the half turn's lift) moves the chimes by a quarter beat. A beat read free of the phase (half a turn from the hand's own angle when it began to stand) moves every chart, which is the owner's word.
3. **A split hand never chimes.** A quantum split between the twins or between places never stands at a whole winding in one hand. So the spin's Bell test reads only along the twins' axis, with every pair opposite (E = -1). The split hand's chime is the measurement's law, the owner's word.
4. **A neutral twin train.** Every sprung train is geared to the offset at one charge (coupling_of = 1; the general K / full rate is UN-S2, the owner's word). Stern-Gerlach at the chimes needs a neutral one, as nature's needs silver.
5. **The setting jams nothing.** The bodies' setting lays 125 windings on one hand (both senses at a clock). Pauli at the setting is the owner's word.
6. **The precession dephases** in a packet of many rates: the second-order clock's precession rate is kappa Phi / omega per mode. One mode, or a slow packet, precesses clean.

## 6. For the Boss

1. **The build.** DAVID-SPIN-IN-CLOCKS_DIFF.txt applies whole on 67a7633d5 (7 files, +161 -37), with every test passing.
   - With no twin train in a calibre, every chart stands bit for bit: the control's hashes are the head's, and the record tests pass.
   - Behind your one flag, it is the toy's step.
2. **The gates** are the checks file's scripts. The Reader's gates 41 and 42 then read a twin train in place of a size-8 train, and gate 43 reads per hand by the sweep. Add a new gate for the boundary's chimes at 2 pi against 4 pi.
3. **The owner's words, by name:**
   1. the count of hands as the exchange;
   2. the unspringing across the twins;
   3. the offset's curl on the twins (SR-S3 restored on twin hands);
   4. the setting's jam per hand;
   5. a beat free of the phase;
   6. the split hand's chime;
   7. a neutral twin train (UN-S2).

**Earlier, corrected.** DAVID-SPIN-SOLVED.md stands as the former language's record: the same build at 900fc2f4a, its measurements the same to the digit here. G0 stays withdrawn.

A document, its diff and its checks; no code of the engine head changed.
