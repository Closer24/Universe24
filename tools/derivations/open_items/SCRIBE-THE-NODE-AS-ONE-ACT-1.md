# The Node-clock as one act: the frame, the sentence proposed and the cuts

The owner's questions of 2026-10-28, 05:4x to 05:5x UTC, to the Scribe (ledger rows 303 to 305): the whole system as a tensor machine and the Node-clock a simple one, every family a kind of tensor; whether a singularity can be caught; how everything converges to the clock and whether the 24 arranges it. His order after them: "Sync the Boss." The Reader reports his word to the Reader: "Sync only with the Writer on the right way." This file holds the frame, the sentence entered in the law on the owner's word of 06:0x UTC (decided, not built), the step's acts by kind and the order of the cuts, as agreed in the thread with the Reader and put to the Boss and David.

## The frame

- **The dial.** Every component of every tensor of every family is a gear: an integer with a carried remainder, the position on a dial and the count of its turns. The only dynamics is the dial's turn (acts.carry): the quotient leaves, the remainder stays.
- **The 24 and the dials.** The cube's 24 turns act on dials in two ways only: they exchange which dial (the axes, g e_a = s_a e_a') and they reflect a dial about its mid tooth (r to 2 mid - r, acts.mirror). A train's kind is a way of doing that: the scalar, the pseudoscalar, E, the vector and the shear, five in all (dimensions 1, 1, 2, 3 and 3). They follow from the one vector kind (the six Spokes' signed permutations, core/spokes.py, the engine's one typed number) by its symmetric, antisymmetric and triple products, so no table of a kind need be typed.
- **The couplings.** A product of two kinds splits by the group's product table: the stress, a product of two gradients, is the trace, E and the shears (the regulator's gears, the shears struck at d09f1a8a5); the metric's ten gears are two scalars, E, a vector and a shear; the potential's four a scalar and a vector.
- **The clock.** It is the kind the 24 leaves in place, the scalar: the time gear, the rate, the load, the trace. At a point the cube's turns fix, only that kind can be read.
- **The singular points** (row 304): the light, the null element, known by identity at 18 reads in 7 files and 8 branches in 4 (the Boss's counter at 526a5666d); the points the cube's turns fix, where a frame has no direction (David's unfair draw, row 302); the frozen Node-clock, where the metric degenerates.

## The sentence in the law (status: decided, unbuilt)

**The Node-clock is one act.** The Node-clock's step is one act: one division with a carried remainder over one integer contraction of the Node-clock's own gears and its six Meshes' gears, the same for every train. A gear is a dial, an integer with a carried remainder; a train is a tensor whose kind is a way the cube's 24 turns exchange and reflect its dials (five kinds, derived from the lattice's axes), and the contraction of two kinds is fixed by the group's product table; what differs between families is the kind and the integers of the universe file (the pair, the couplings), never a branch of the code. Every gear is read before any is written. At a point the cube's turns fix only the scalar kind is read: the clock is what the 24 leaves in place.

## The step's acts by kind

The independent read of 97e5b3fd6 (SCRIBE-AUDIT-97E5B3F-1.md) lists 26 acts in tick.py's step beyond Rule3's one carry. Read by kind (the Scribe's reading, for the Reader and David to check):

| # | the act (tick.py, 97e5b3fd6) | kind |
| --- | --- | --- |
| 1 | stretch.load_of: the load a of a stretch, the inverse of the rate table by search | pointwise map |
| 2 | readings.rates_of and stopped_of: the rate table and the clamp | pointwise map |
| 3 | the dial: dial + going * where(stopped, 0, rate) | bookkeeping |
| 4 | factors(...): the Mesh factor of the tension, a halving carry, a clamp, a carry | pointwise map |
| 5 | pawls(ratchet.fine): the parity by a carry on 2 | bookkeeping |
| 6 | rates.rounded(offset * rate, full rate) | pointwise map |
| 7 | the ratchet's turn and the drive carry (clock.act) | bookkeeping |
| 8 | centred_count and clock.count_max | global reduction |
| 9 | offsets(clock, pawls, count): the Mesh's turn by the (cos, sin) pair | contraction |
| 10 | the coupling's power and offsets(count * c) | contraction |
| 11 | hands.lead | contraction |
| 12 | rest_rate_of: the cosine search | pointwise map |
| 13 | skewed: the tangent triples | contraction |
| 14 | clock.pulls and through_mesh: four rounded reads a Spoke a hand | contraction |
| 15 | Pauli's numerator: grip * (cx * sx + cy * sy + cz * sz), then a carry | contraction |
| 16 | the release: the sum of stretch times cross | contraction |
| 17 | u_in and u_out: rounded(p + p + 1, d) | pointwise map |
| 18 | carry(n, ...), carries(mass), carries(-pull) | bookkeeping |
| 19 | stress_of: the stress, a product of two gradients | contraction |
| 20 | the clamp of the regulator's drive at plus and minus the hold | pointwise map |
| 21 | the regulator's act: the time gear's carry and the axis gears' drive carries | bookkeeping |
| 22 | where(w > 0, w, mean_teeth) | pointwise map |
| 23 | clock.drive, push_of and recoil: the release's drive carry per axis | contraction |
| 24 | clock.turnover: the comparisons, the exchange, the flip | gate |
| 25 | clock.click: the engage, the jam, the unwinds, the winds, the Born pick, the bobs | gate |
| 26 | bits_of per gear into clock.max_transient | global reduction |

**Nine contractions, eight pointwise maps of one gear, five of bookkeeping, two gate acts, two global reductions.** The pointwise maps need a place in the one act (a chain of Rule3 carries, or data; they carry the audit's E8 and E9, the rate's exponential table and the Mesh factor). The two global reductions are no act: clock.count_max and clock.max_transient are written in the step and read by run.py's census alone (checked), so they are readings of the whole lattice and leave the step.

## The order of the cuts and the checks

1. The fair draw (the Boss's, in progress after David's finding of 05:02): the draw reads invariants only at the points the cube's turns fix, the precondition of every draw.
2. The pure contractions with no gate (regulation.stress_of, the hands' products, the Meshes' cross and gradient).
3. The pointwise maps.
4. The gate (click, chime, merger ends, turnover) as one act for every family.
5. The two global reductions out of the step into the readers.

After each cut, by David on toys-5 and merged by the Boss as usual: the Reader's per-row diff of the 77 rows between the two engines on the same seeds, the 16 records and the 3 committed charts as before, the rewind exact 20 of 20, the suite, `scribe_scan.py --patch FILE --base <head>` (counts only fall, a new file is clean; code moved between files shows as new hits, and the owner's word allows it), and one generic test: at a fixed point of a symmetric setting every gear of a non-scalar kind is 0.

## Not decided

The Boss's order within the owner's go (the program Tenzor24, TENZOR24.md); whether the reflections are parted or held (ledger row 299).
