# The Node-clock as one act: the frame, the sentence proposed and the cuts

The owner's questions of 2026-10-28, 05:4x to 05:5x UTC, to the Scribe (ledger rows 303 to 305): the whole system as a tensor machine and the Node-clock a simple one, every family a kind of tensor; whether a singularity can be caught; how everything converges to the clock and whether the 24 arranges it. His order after them: "Sync the Boss." The Reader reports his word to the Reader: "Sync only with the Writer on the right way." This file holds the frame, the sentence entered in the law on the owner's word of 06:0x UTC (decided, not built), the step's acts by kind and what David derived; the plan, with the order of the cuts and the checks, is the Boss's file tools/derivations/open_items/TENSOR24.md, which took this file whole.

## The frame

- **The dial.** Every component of every tensor of every family is a gear: an integer with a carried remainder, the position on a dial and the count of its turns. The only dynamics is the dial's turn (acts.carry): the quotient leaves, the remainder stays.
- **The 24 and the dials.** The cube's 24 turns act on dials in two ways only: they exchange which dial (the axes, g e_a = s_a e_a') and they reflect a dial about its mid tooth (r to 2 mid - r, acts.mirror). A train's kind is a way of doing that: A1 the scalar, A2 the sign of x y z (a quarter turn reverses it), E, T1 the vector and T2 the shear, five in all (dimensions 1, 1, 2, 3 and 3). The twist the engagement reads is kept by every turn and reversed by every mirror (David's check on meshes.train_twists over the 48 images of a random hand): a scalar of the 24 and the pseudoscalar of the 48, so a fixed-point test names its group. They follow from the one vector kind (the six Spokes' signed permutations, core/spokes.py, the engine's one typed number) by its symmetric, antisymmetric and triple products, so no table of a kind need be typed.
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

## What David derived (06:06 UTC, the thread's item 1226, posted to the Boss; the code of the third checked)

- **The fixed-point test names its group.** At a point the 48 fix, the twist's kind reads 0 with the rest; at a point only the 24 fix, it may stand.
- **The contractions are products of trains and not one linear sum.** The stress, the masses, the forms and Pauli's numerator are of degree 2 in the gears; the release is of degree 3 (the stretch times the cross of a hand and its pull). In the hand's plane there are two products (hands.dot, meshes.cross); on the cube three, from the six Spokes (the trace, the cross spokes.transverse, the diagonal's split regulation.tensor_parts). A train's kind is its cube kind times its own (one gear, the Gaussian pair, the twins' four). A cut keeps its bits within what clock.max_transient reads now.
- **Three of the eight pointwise maps are no map of the step.** The rate table p_0(c) = Gamma (1 - 1 / Gamma)^c is one carry per unit of load at the teeth Gamma and one rounding (rates.Side.fill_to, core/rates.py:41 and :91): act 2 is no formula and no data, act 1 is that chain read backward, and act 12 (rest_rate_of) is found once per ratio and kept on the clock (clock.rest_rates, regulation.py:28-32, clock.py:90), a constant of the setting. The Mesh factor, the clamps and the selections he derives one by one before they are built.

## The order of the cuts and the checks

The order of the cuts and the checks after each cut are the Boss's plan (tools/derivations/open_items/TENSOR24.md, sections 6 and 9). The Scribe's part in them is the scan: `scribe_scan.py --patch FILE --base <head>` (counts only fall, a new file is clean; code moved between files shows as new hits, and the owner's word allows it).

## Not decided

The Boss's order of the cuts (the program Tensor24, his file TENSOR24.md); the reflections as the 24 exactly with one one-hand coupling (the Boss's recommendation, ledger row 312; the clause's last line stands as written) or the 48 (the last line then names the 48); in both, the clause's word pseudoscalar for the A2 kind is the twist's kind in the 48 and waits for the owner's word.
