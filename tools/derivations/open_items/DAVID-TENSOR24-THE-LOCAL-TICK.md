# The asynchronous board: each node-clock on its own tick, reads that need no order, and the exact rewind

David, 2026-10-28, 13:5x UTC, for the Boss (Sofer and Animate copied). It answers the Boss's ask (6468114771) for "the formula of the local tick, with its order-free reads; the step stays one local event, and the rewind stays exact". That ask stands on the owner's word through Animate, at 11:2x to 11:3x UTC (Hebrew, translated): "Possible when it is very large. Every clock has its own tick, which can slow and speed up. Note that not the whole board ticks together: the board is to run asynchronously."

A helper drafted the derivation and I reran its nine probes; the outputs are identical. They are in DAVID-TENSOR24-THE-LOCAL-TICK_CHECKS.txt, with the draft's proofs in full. The draft reads toys-5 b56643b0e (src and cut 0's letter), the plan at engine-5.0-test 08ec59132, and the law at scribe-5 f32b67cc3: lines 37, 98 and 557, quoted for Sofer. This page covers protocol steps 1 to 4. A second hand follows, then Sofer's check and my sign-off. No src is pushed.

## The local tick

1. **The state gains one integer per node-clock:** its dial tau, the great clock's notch where its now stands.
   - Its tick lasts L = lambda(X) + lambda(X+), symmetric in the time gear's two slots.
   - Its before-notch is tau - L(X-, X). It is read from the state and not stored.
2. **The event.** The node-clock steps at its own notch, by cut 0's one formula. Every read across a Mesh is the neighbour's notch at the reading node-clock's moment:

       m = b + R((n - b) u, L_y),  u = tau - sigma_y,  R(k, L) = (k + mid L) div L

   R is the carry's own rounding. In clock words, each Spoke reads the neighbour's hand where it stands at this node-clock's notch, between its before and its now. PROVED: the read is exact at both ends of the neighbour's tick.
3. **The order inside the event is forced:** the readings, then the impulse at W, then the regulator, then the carry at W+, then the dial.
4. **With one tick for all, it is the head bit for bit, in any order.**
   - On its own integers: 324 asynchronous runs (186,624 events), 0 differ from the head's form.
   - On the head's own tick.py (hole, nature and bang, three random event orders per tick): 1,225,152 reads, 60,912 pulls, 60,912 carries and 71,064 regulator gears, 0 differ.
   - Mutants:
     - reading "the value last sent", the law's line 557 taken literally, differs in 32 of 36 runs;
     - the weight read from the wrong end differs in 36 of 36.
5. **The notch's unit costs nothing.** Only differences and ratios of dials enter, so "very large" is free: two tick laws give identical runs on 12 of 12 boards.

## Reads that need no order

1. **The rule:** a node-clock is due when its dial is at most each neighbour's.
   - Every read then falls inside the neighbour's current tick.
   - Neighbouring dials differ by at most one tick, so the dials can be held modulo a turn, with no great-clock number.
   - Two events at one notch commute, so every runner gives the same board. PROVED.
   - CHECKED: 432 runs on 54 boards (two rates, three rates, or a rate per node-clock), with 3,963 events tied with a neighbour; 0 disagree. The dial bound is reached exactly.
2. **Only value reads are free of order.** A neighbour's fine tooth, stride or before is not, and the head makes such reads across a Mesh:
   - the centred count reads the ratchet's stride (meshes.py:95); 237 of 27,000 such reads on nature change with the order;
   - the pawls read the ratchet's fine tooth;
   - mesh_lead reads the neighbour's before (meshes.py:142);
   - hands.wind reads the neighbours' befores.

   Each is to be rewritten as a value read.
3. **The red-black partition is derived and not needed.**
   - The 24 about every node-clock generate exactly two orbits, the parity classes of x + y + z, with no Mesh inside a class. On an odd side there is one orbit and no two-colouring at all (CHECKED on sides 3 to 6).
   - Margolus's blocks are kept by only 3 of the 24 about a node-clock.
   - The partition would cost a typed even side and a chosen order between the classes, and it breaks odd translations (3 of 3). Value reads make it unnecessary.

## The exact rewind

1. **Undo the latest before-notch first** (any local maximum will do), each act inverted in the reverse order: acts.carry at going -1. No log and no stack. PROVED.
   - CHECKED: 432 runs (sides 3 to 5, four tick laws, three reads, both roundings, T 600 and 602), 477,088 events, with the tick slowed 74,493 times and sped 80,323 times: 0 fail.
   - Each mutant fails 6 of 6: the wrong undo order, the drive undone at going +1, a read one notch early, and the undo carried at W+.
2. **The time reversal on the asynchronous board,** T S T = S^-1: 81 runs, 117,030 events.
   - It holds with the reads lin and near (0 of 27 fail each), and fails with past (27 of 27).
   - The odd-rounded read fails 9 of 9, and so does a one-slot tick.
   - At even teeth it needs the frame of DAVID-TENSOR24-ANY-TEETH.md.

## What is kept, and what stays open

1. **The books are kept.** PROVED: 3,907 of 3,907 events, with the read's rounding recomputed on the rewind.
2. **The sweep is kept exactly per event** (30 of 30). The Mesh's two parts cancel where every node-clock has one tick (12 of 12), but not at different rates (0 of 18): the residue is 2e-3 to 9e-3 of the gross flux with lin. OPEN: exactness at different rates needs one flux booked for both ends, the local time stepping's refluxing.
3. **The 24 hold for the reads they never negate** (288 images, 0 off). At a read tie on T1 and T2 gears, half up keeps the time reversal and breaks the negation, and the odd rounding does the reverse. No rounding keeps both (PROVED). This joins the carry's open tie rule.
4. **The light cone:** each event reads only its seven sites, so one Mesh per local tick (24 of 24; a two-Mesh read fails 16 of 24). Measured in notches:
   - **past:** 0 of 372 node-clocks reached faster than one Mesh per shortest tick; least delay 1.039;
   - **near:** 154 of 372; least delay 0.65;
   - **lin:** 318 of 372; least delay 0.32.

   A read that keeps the time reversal must see the new slot by half its tick (PROVED). So a strict cone in notches and the time reversal conflict. I recommend lin; the choice is the owner's (OPEN).

## The lapse, counted once (my general relativity item)

1. **The head already holds the rate in the step's coefficients:** the beat through the spring D, and light's speed through the grips.
2. **A tick that also slows with the rate counts the lapse twice.** lambda = X makes the tick go as the rate to the power -(d + 1) in the head's gauge.
3. **To count it once:** the tick set from the rate, the spring at the vacuum's clock, and one power of the rate in the grips, the ruler alone. Then per notch the beat goes as the rate and light as its square, as the law's same clock and same ruler have them. The redshift then comes from the tick itself, not from the typed exponential (E8).
4. **Which integer of the regulator gives the tick is OPEN and mine,** with the rows of gravity it moves. Under the law's "no bound and no floor", lambda = X needs X >= 1, a range. lambda = 1 + X X has none (CHECKED in 108 runs). The rate's own tick must be range-free too.
5. **Nothing in the proofs depends on lambda's form:** every proof holds for any lambda >= 1, and the probes run four forms.

## What it replaces

1. **The global tick loop** (tick.run, the runner's loop over ticks) becomes the local event and the runner's event loop: "while some node-clock is due, step one, or all that are due at once".
2. **These stay fakes and go:**
   - the great clock's index (clock.ticks);
   - the rewind stack (clock.stack);
   - the start-board copies (Tick.held, phase.snapshot, Tick.at);
   - the reads across a Mesh that are not value reads (above);
   - the whole-board reductions inside the step (count_max, max_transient);
   - the click's whole-board phase;
   - the dial kept as the rate summed per tick;
   - the lapse typed into the coefficients (E8).
3. **The law's line 557** reads "the value its neighbour last sent". It should read "the neighbour's notch where it stands at the reading node-clock's moment", or the order matters.

## OPEN, by name

1. Which integer of the regulator gives lambda, with the coefficients counting the rate once, and the stopped clock as a tick that never comes due.
2. The read's tie rule on T1, T2 and A2 gears, the same decision as the carry's.
3. The head's non-value reads, rewritten as value reads: the sprung hands' Mesh turn, the click's orientation, twist and wind, and the pawl's change at a turnover.
4. **The clicks inside the event.** A click that writes the far end of a Mesh (the fitting's lay, the unspringing) writes outside its node-clock, and the commuting proof forbids that. Two candidates:
   - the far end takes the write at its own next event, as a value it reads;
   - a click only where the two ends share a notch.
5. The sweep and the wind at different rates.
6. The cone in notches: the owner's choice.
7. Stability at different rates over long runs, probed only to about 20 ticks.
