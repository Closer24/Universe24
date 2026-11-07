# Separating the stopping and restarting inputs

This is a mathematical construction study under the existing Rule3 law. It
does not modify the completed orbit protocol or establish a new autonomous
capture, waiting, approval or release component.

## Target from a recorded input word

The recorded clock interaction motivating this study has center state
`(-1,0,0)` before an actual input -1. Rule3 produces `(0,0,4)` with quotient
-1 and a guarded C. The next actual +1 produces `(0,1,0)`, quotient +1 and
another C. Thus two events, not one, occur in that recorded example.

A new target is to separate those actual inputs by at least eight complete
zero-input updates. The stopped triple `(0,0,4)` then remains unchanged until
the later input. This is an arithmetic interface specification. It cannot be
implemented by supplying u from an experiment runner; ordinary neighboring
counters must produce the entire input history.

## Exact translating-row family

Take a confined row whose X coupling is positive, whose only active counters
are on that row, and whose full profile translates by one site in +X per
update. Let all counters have finite support and let the distant row remainder
be zero. Index the profile by integer i and let `A_i=sum_(j<=i) a_j`, with A
zero outside a finite interval. The translation conditions give

```text
b_i = a_(i-1)
ell_i = a_i + a_(i-2) = u_i
r_i-r_(i-1) = 4*(a_i+a_(i-2))
r_i = 4*(A_i+A_(i-2)).
```

Therefore valid row remainders require `A_i+A_(i-2)` to lie in `{0,1}`.
For a transverse passive recipient of weight w, a retained moving halo is

```text
halo_r_i = 2-2*w*A_(i-1).
```

The halo receives `w*b_i`; its quotient is zero and its next remainder equals
the previous profile at i-1. Valid halo remainders require `A_i` in `{-1,0,1}`.
These two conditions are sufficient: direct substitution verifies the complete
row and halo translation. A complementary channel with opposite counters and
remainder `4-r_i` supplies the corresponding paired pattern. Directional maps
are permutations, so the paired transverse recipient channels are distinct.

This family includes the existing packet `A=(1,1)`. It also includes the
shorter word `A=(1)` and longer valid trains. These are mathematical profiles;
only previously registered members have existing complete-board experiments.
Periodic embeddings need enough room for the complete support, its halo and
the declared observation horizon, or a separate wrap-around proof.

The row argument applies to identity-body-action corridors with positive X
sign. Transverse signs change the required halo remainders but not the row
equations. It is not a theorem about every multichannel pattern, internal
periodic carrier, active transverse structure or scattering preparation.

## Why a single stretched bipolar pair fails

Suppose `a_0=+1`, `a_d=-1` and all other a values are zero. Then A is one at
indices 0 through d-1. For d=1 or d=2, all row and halo remainders are valid.
For every d>=3, however,

```text
r_2 = 4*(A_2+A_0) = 8,
```

which is outside the permitted remainder range. The familiar d=2 packet is
not the only possible short packet, but increasing its lobe separation while
keeping everything else zero is impossible within this ansatz. Adding an
arbitrary constant background remainder cannot fit an eight-unit excursion
inside `0..5`.

More general valid words can have widely separated completed packets. They
cannot obtain the proposed long wait merely by retaining the first unit
counter lobe and postponing its first compensating lobe beyond two sites.
Additional intermediate counter structure, different channels, transverse
activity or a nontranslating converter must then be present. The actual
clock's effective input already includes scattering and feedback; this
obstruction does not classify that entire apparatus.

## Two-lane cancellation of intermediate inputs: a construction target

There is a precise alternative at the input-word level. Let one free packet
contribute `f(t)=-delta(t)+delta(t-2)` at a receiver. A train with starts
0,4,8 is a valid translating profile by the conditions above; so is a second
train with starts 2,6. Their formally summed receiver contributions are

```text
f(t) + f(t-2) + f(t-4) + f(t-6) + f(t-8)
    = -delta(t) + delta(t-10).
```

There are nine zero-input updates between the two nonzero inputs. Starting
from `(-1,0,0)`, the conditional receiver word gives C at updates 1 and 11,
holds `(0,0,4)` at states 1 through 10, and restarts at `(0,1,0)` at state 11.

This is **not linear superposition of Rule3 solutions**. Within each lane,
the full counter/remainder profile is checked against the translation
equations. Only the neighbor-input sum is linear. A genuine two-lane device
still needs distinct legal incoming addresses, compatible initial shared
halo states, both singleton controls, retained outgoing information and proof
or measurement that receiver feedback does not change the required words.
Putting the same five starts onto a single lane does not work: the cumulative
profile violates the remainder bound.

During the nominal wait, two nonzero incoming contributions may cancel in the
receiver's sum. A protocol requiring every external term individually zero
would reject that situation even though the receiver is stationary. Therefore
this would need its own prospective waiting contract; it cannot be counted as
a pass of a stricter isolated-region study. Nor is a prepared delayed train
already a message computed by an internal route-selection mechanism.

## Bounded check and next decision

The finite arithmetic check is fixed in
[`pulse_words.py`](pulse_words.py): all 6,561 length-eight cumulative words
over `{-1,0,1}`, isolated-pair distances 1..16, and the two explicitly listed
packet trains. Every accepted profile is substituted into the scalar Rule3
row and passive-halo equations. This is a mathematical finite check, not a
massive search or a full-board run. Reproduce it with:

```bash
python -m research.staged_blocks.pulse_words
python -m unittest discover -s tests -p test_staged_pulse_words.py -v
```

The completed check accepts 100 of the 6,561 width-eight words. All accepted
words satisfy the explicit row and halo translation equations; isolated-pair
distances 1 and 2 pass and distances 3 through 16 fail the remainder bound.
Both stated individual trains and the conditional two-event word pass. The
three regression tests complete in under one second in this environment.

The next autonomous experiment should freeze one two-input geometry, the
complete two train preparations, receiver state, arrival times, all source
controls, an eight-update wait predicate and a finite budget before execution.
It should record each of the six actual incoming terms, all receiver channels,
all other outputs and the complete inverse. A failed waveform match would
identify the conversion or feedback problem directly. No such autonomous
two-lane experiment is claimed by this note.

## Explicit joint geometry for the bounded bridge study

For the +++ tensor, use lower-row channels 0/14 at `(x,c,c)` and upper-row
channels 6/36 at `(x,c+2,c)`. The receiver is channel 2 at `(c,c+1,c)`.
Independent matrix routing gives

| Sender and direction | Shared recipient channel | Weight |
| --- | --- | --- |
| Lower 0, +Y | 2 | +1 |
| Lower 14, +Y | 24 | +1 |
| Upper 6, -Y | 2 | +1 |
| Upper 36, -Y | 24 | +1 |

All four row channels have identity ports in both world-X directions. Both
rows can therefore carry the same world-+X translating profiles; no K transform
is required for this +++ construction. The upper pair is 6/36, not 0/14.
The rows and outer transverse halo planes must remain distinct: use L>=5
transversely and enough X space for the declared support without aliasing.
This is not an additional claim about the small-L wrapped construction.

Choose lower cumulative support at offsets `{0,1,4,5,8,9}` and upper support
at `{2,3,6,7}` relative to a common X origin. Their cumulative values are one
on those sets and zero elsewhere. Construct each row using the equations
above. At every shared middle-row halo address, assign the remainder **once**:

```text
r_(channel 2)  = 2-2*(A_lower(i-1)+A_upper(i-1))
r_(channel 24) = 2+2*(A_lower(i-1)+A_upper(i-1)).
```

The summed cumulative value is either zero or one, so these shared remainders
are valid. Every nonshared halo retains its single-row formula. Substitution
shows that the shared halo has zero quotient and translates with both rows.
Together with the separately verified row equations, this gives an exact free
two-lane translating carrier, including its shared retained state. This solves
the initial shared-halo constraint without adding complete states.

An initially running clock is a further interaction, not part of that free
carrier proof. A candidate compatible baseline uses center `(0,1,0)`, base
remainders zero on its two Y recipients in the guides, and base remainder two
on its other four recipients. Advance the **entire** clock preparation to
phase two before the run. With common source origin `x0=c-24`, the leading
free input reaches the clock at old time 13, when this clock would have
state `(-1,0,0)`.

The prospectively suggested clock-coupled prediction is a first C at update
14, a fixed complete 48-channel center node at states 14 through 23, and a
second C at update 24. Its predicted effective inputs are -1, nine zeros,
then +1. The initial row remainder shift also compensates the clock's input
at the approaching front: `u=-2,r=2` and the free front's `u=-1,r=0` have
the same quotient -1 and next remainder 4. These calculations motivate the
bridge validation; the complete interaction still needs its registered
forward runs and independent audit.

The stronger full-336-region autonomous hold is a different criterion. During
the proposed center pause, the two adjacent guide nodes carry active counters
and intermediate nonzero inputs cancel at the center. That does not satisfy
an isolated protected-region hold, even if the entire center node is fixed.
Both verdicts must remain explicit.

All four lane-presence controls must keep the same joint remainders. Removing
one train can then generate additional activity near the initial shared halo:
its remaining train no longer receives the other train's cancellations. Such
a singleton is not the independently prepared free train with its own halo.
The control must be measured as specified, not repaired by changing remainders.
The construction target remains finite, prepared and fully reversible; it is
not yet an internally computed route-approval mechanism.
