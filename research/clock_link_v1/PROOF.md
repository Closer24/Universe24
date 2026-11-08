# Exact finite-guide trajectory

This is a proof about a deliberately prepared family under the existing
`+++` Rule3, not a derivation of physical light or gravity. The complete
state includes every remainder, including the zero-counter halo.

## Preparation and geometry

Let D be even and at least 2, M=D+1, P=4M. Along an X-directed row, channel
0 at position 0 starts at `(0,1,2)`. Positions 1 through D in that channel
start at `(0,0,4)`. Every other site-channel starts at `(0,0,2)`.
The periodic side is at least D+3, so the two exterior axial recipients are
distinct; the transverse recipients are distinct as well. Translation and
proper whole-component rotation carry the statement to equivalent placements.
The existing `+++` routing has identity X ports on channel 0. Its other four
ports lead to the transverse remainder recipients used below. No links change.

Define the truncated sequence s(q)=cos(pi*q/2) for integer q>=0 and zero
otherwise. It is exactly the integer sequence `1,0,-1,0,...`. Define
H(q)=sum_{0<=j<q}s(j), with H(q)=0 for q<=0. For positive q, its values by
q modulo 4 are `0,1,1,0`. Let Theta(q)=1 for q>=0 and zero otherwise.

## Closed row state for one complete period

For 0<=t<P the source has

```
b_0(t) = s(t),    a_0(t) = s(t-1),
r_0(t) = 2 + 2 F_1(t).
```

For i=1,...,D define

```
b_i(t) = s(t-i) - s(t+i-2M) + s(t-i-2M) - s(t+i-4M),
a_i(t) = b_i(t-1),
F_i(t) = H(t-i) - H(t+i-2M) + H(t-i-2M) - H(t+i-4M),
r_i(t) = 4 - 4[Theta(t-i) - Theta(t-2M+i)
                + Theta(t-2M-i) - Theta(t-4M+i)].
```

Use F_0(t)=H(t). Every exterior recipient of row address i has zero
counters and remainder `2+2F_i(t)`. All other addresses stay at `(0,0,2)`.
Each such recipient has only that one counter-active row donor. Thus this
formula specifies the complete 48-channel three-dimensional board, not a
replacement one-dimensional evolution law.

## Verification of every Rule3 update

The definition of H gives `F_i(t+1)-F_i(t)=b_i(t)`. Since M is odd, splitting
the four ordered activation intervals gives `F_i(t)` in {-1,0,1}; for i=1
it lies in {0,1}. These are finite identities of the four residue classes
of t modulo 4 in each interval, independent of the magnitude of D.

Consequently each halo numerator is
`2*b_i(t)+(2+2F_i(t))=2+2F_i(t+1)`, an integer in {0,2,4}. Its quotient is
zero and its next remainder is exactly the stated value. The source similarly
has only row donor b_1, numerator `2+2F_1(t+1)` in {2,4}, and quotient zero.
It therefore obeys `a'_0=b_0`, `b'_0=-a_0` throughout, while retaining its
longer-period remainder record.

For an interior row address, substitution of the four s terms gives

```
u_i(t) = b_(i-1)(t)+b_(i+1)(t) = b_i(t+1)+b_i(t-1).
```

At the right boundary use b_(D+1)=0: the two image terms cancel there.
At the left boundary the image expression reduces to the source s(t) over
the updates of this period. The sum u_i is nonzero only on four front
transitions: +1 into states i and 2M+i, and -1 into states 2M-i and 4M-i.
At a +1 front the previous remainder is 4, so `divmod(2+4,6)=(1,0)`.
At a -1 front it is 0, so `divmod(-2,6)=(-1,4)`. Elsewhere u_i=0 and the
remainder stays 0 or 4 with zero quotient. These are exactly the four
Theta changes above, and `b'=ell-a` is the displayed row recurrence.

At state P, every row counter and remainder and every halo remainder equals
its state-0 value. Determinism extends the construction by repetition for all
future times; the native inverse also repeats it backward. The period is
exactly P, rather than merely a divisor: the complete source triple carries
an echo bit with a block of Q=2M zeros followed by Q ones. Its counter pair
alone has period four. No asymptotic or continuum approximation is used.

## Events and records

The source core has quotient zero and no native C events. The adjacent port
i=1 has C1/+1 at transitions `1+nQ` and C2/-1 at `2D+1+nQ`. The endpoint
i=D has C1/+1 at `D+nQ` and C2/-1 at `D+2+nQ`. Thus the endpoint responds
after two updates and the two port-to-endpoint legs each take D-1 updates.
One whole-board period contains two round trips.

The fixed passive source observer

`B=int((r_0==4)==(a_0+b_0>0))`

equals `floor(t/Q) mod 2`. It is undefined on a zero-counter source. The
fixed target observer `I=a_D*a_D+b_D*b_D` equals 4 on states D+2 through
3D+1 inclusive: **2D consecutive states, 2D-1 unchanged transitions**.
It equals 1 on the two-state arrival transients D..D+1 and 3D+2..3D+3,
and zero elsewhere in the period. Source B is unchanged for Q consecutive
states, spanning Q-1 unchanged transitions. Both are cyclic parity records.
The target is driven by guide inputs; it is not an isolated persistent memory.

Changing only the initial source to `(-1,0,2)` yields the canonical complete
initial state after one update. All events are therefore delayed by one.
The raw delayed source bit at state zero is 1: that is startup preparation,
not evidence of an earlier returned signal. With source counters absent,
all counters are zero and every remainder is fixed forever under Rule3.

## Domain and evidence

Odd D is not included in this theorem. The reusable factory additionally
requires D>=14 so both first record windows exceed 24 unchanged transitions.
The theorem concerns this exact preparation and its translated/properly rotated
copies, not arbitrary noise, arbitrary coupling tensors, overlapping assemblies
or spontaneous emergence. Two separated copies can coexist if their complete
supports and halos remain disjoint; their interaction needs a separate test.

`exact.py` evaluates the formula directly. `audit.py` compares complete native
states with this formula and an independent matrix-routing gather implementation,
including inverses, native events, controls and disjoint composition. Its new
receipt is a fresh reconstruction after workspace cleanup. The unavailable
earlier local recordings and their historical counts are not reused as evidence.
