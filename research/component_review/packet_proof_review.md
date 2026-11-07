# Independent proof review: the prepared guided packet

This proof concerns the fixed body-013 coupling with signs `(+,+,+)`, the
declared preparation, and every periodic cube side `L >= 5`. It establishes a
translated mathematical pattern on a prepared guide. It does not establish
free-vacuum light, a silent waiting receiver, or a physical time variable.

## Row calculation

On the chosen X row, channel 0 has the following initial triples:

| X position | `(a,b,r)` |
| --- | --- |
| 0 | `(1,0,4)` |
| 1 | `(0,1,4)` |
| 2 | `(-1,0,4)` |
| 3 | `(0,-1,4)` |
| All other positions | `(0,0,0)` |

Channel 14 has opposite counters and the complementary remainder `4-r`.
Both channel labels have the identity spatial rotation. Their X connections
use the identity body action, so their row input is `u(x)=b(x-1)+b(x+1)`.
All off-row counters are initially zero.

For channel 0, the only nonzero row inputs occur at X=0 and X=4, where they
are `+1` and `-1`. At X=0, Rule3 maps `(1,0,4)` to `(0,0,0)`. At X=4, it
maps `(0,0,0)` to `(0,-1,4)`. At X=1,2,3 the zero-input update respectively
gives `(1,0,4)`, `(0,1,4)`, and `(-1,0,4)`. The remaining row positions do
not change. Channel 14 obeys the corresponding complementary calculation.
Thus the complete row moves one position in +X. The calculation also holds
when X=4 is the last position of an L=5 row.

## Transverse retained remainders

Each source channel has one receiver in each of the four transverse spatial
directions. The two source channels reach distinct receiver channels, since
each directional map is a permutation. Distinct transverse neighbors do not
coincide for the stated cube sizes.

For one such receiver, let `q` be its signed input from the positive packet
counter. Here `q` is `+1` or `-1`. Its initial remainder is `2-2q` at X=1,2,
and 2 elsewhere. Its old inputs are `q` at X=1, `-q` at X=3, and zero at
the other X positions. Consequently:

- X=1 changes from `r=2-2q` to `r=2`.
- X=2 keeps `r=2-2q`.
- X=3 changes from `r=2` to `r=2-2q`.

Every numerator `2u+r` lies in `{0,2,4}`. Every transverse quotient is
therefore zero, and both transverse counters remain zero. The remainder
halo moves one position in +X. Since it generates no nonzero counters,
there is no additional outward influence. All other channels retain their
declared background. No retained remainder has been dropped from this proof.

## Iteration, recurrence and events

The fixed coupling is spatially homogeneous. Translation commutes with the
whole synchronous update. The one-step identity just proved therefore gives
`W^t(S)=T_x^t(S)` for every nonnegative integer `t`.

Translation by L returns the full periodic state. Channel 0 has exactly one
site with `a=+1`, so no smaller positive translation returns the state. Its
minimal positive period is exactly L. There are four guarded arithmetic
events per update: the front and rear changes in each of channels 0 and 14.
The transverse halo has no such event.

The source-off control retains all the same initial remainders but sets every
counter to zero. It is stationary by Rule3, for arbitrary valid remainders.
This control is not required to be spatially translation invariant.

## Computational evidence and limits

`review_packet.py` reconstructs the preparation using the independent exact
matrix receiver relation, then checks every full transition, inverse,
translation, recurrence, and guarded event for all six registered runs at
L=5,17,31. These are 106 transitions and 112 retained states. The direct
algebra above, rather than those finite sizes alone, supports the all-L claim.

The entire periodic guide is part of the preparation. The moving disturbance
is compact relative to that guide, not relative to the uniform `(0,0,2)`
background. Interaction with an arbitrary receiver, perturbation robustness,
other coupling signs, and successful write-then-route composition require
separate work.
