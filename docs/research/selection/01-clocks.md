# Native clocks and a bounded reversible selection mechanism

This lane contributes two exact constructions under the existing fixed-six
Engine: a bounded material-state clock control, and a compiler embedding a
local reversible three-bit gate with transport. The latter is shared with the
structural-complexity lane. It supplies dynamic memory that changes future
packet routing, not another one-way intensity register.

The source base is PR #49 `a3013a9`; the one-runtime Engine ancestry is
main `4c494c1`, with the prior #49 audit retained.
The corrected full45 proposal in #50 (`62202fdc`) leaves only three slots.
This mechanism uses three, but **is not appended to that geometry as if an
allocation automatically supplied stress or metric coupling**. The separate
reciprocal apparatus lane owns its 45+2+1 allocation. These are typed research
checks using one existing Engine, not selectable installed physical worlds.

## Primary literature and what is newly derived

- Fredkin and Toffoli, *Conservative Logic* (1982), particularly the unit-wire
  and controlled-routing definitions in §§3.2.3–3.2.5 of the
  [author-paper reprint](https://fab.cba.mit.edu/classes/862.16/notes/computation/Fredkin-2002.pdf),
  motivates reversible routing with retained information. Its gate does not
  establish this project's field encoding or quantum probability law.
- Elze, *Action principle for cellular automata and the linearity of quantum
  mechanics*, [arXiv:1312.1615, §II](https://arxiv.org/html/1312.1615v1),
  derives a particular integer Hamiltonian automaton under an action
  principle. Its linearity and sampling-theory assumptions are additional
  structure. The nonlinear Boolean construction below is not claimed to
  inherit that paper's Schrödinger correspondence.

The native coordinate identity, fixed-six period-six invariant, face-matching
invariant, and `F+F^-1` prepared-sector construction below are derived here
and checked against the actual Engine. Lane4 supplies the specific reversible
ready-memory sorting gate. Classical retained bits are not quantum amplitudes.

## One channel already contains a native clock phase

For each complete retained triple define

\[
 q=b,\qquad p=6(b-a)+r,\quad 0\le r<6.
\]

This is an exact bijection: `b=q`, `r=p mod 6`, and
`a=q-floor(p/6)`. It changes coordinates, not the ownership convention:
one channel still counts all three retained integers. Write `u=6q+f`; the
unchanged Rule3 becomes the two integer shears

\[
 p'=p+2f,\qquad q'=q+\lfloor p'/6\rfloor.
\]

No runtime solver or time variable has been added. For `u=3b`, the original
coordinates have the especially simple update

\[
 (a,b,r)\longmapsto(b,b-a,r).
\]

Its sixth power is the identity for every signed integer pair and every valid
remainder, and it preserves the positive quadratic form

\[
 E=a^2+b^2-ab=\frac{(a-b)^2+a^2+b^2}{2}.
\]

In native coordinates the kick is `p'=p-6q`. This is an actual bounded phase
orbit in retained state. It needs neither an additional clock register nor
per-step external scheduling. It is a computational oscillator control;
calibration against proper time of an evolving metric remains a separate
physical experiment.

## Local connections between native clock states

Take two channels and one fixed face direction e, with
`(Cv)_0(n)=v_1(n+e)` and `(Cv)_1(n)=v_0(n-e)`. This pairing operator is symmetric
and satisfies `C²=1`. Compile `u=3Cb`. The complete map is

\[
 a'=b,\qquad b'=Cb-a,\qquad r'=r.
\]

It preserves

\[
 E_C=\|a\|^2+\|b\|^2-a\mathbin{\cdot}Cb
       \ge\tfrac12(\|a\|^2+\|b\|^2).
\]

After three updates both retained slices equal their signed partner values:
`(a,b)->(-Ca,-Cb)`; after six they return. This demonstrates bounded causal
exchange of phase-bearing state on every face direction and across periodic
seams. It does not by itself create new structure or a thermodynamic arrow.
There is no global board-age input: the whole board has one autonomous map,
with local states serving as relational phase information.

## From clock-like reversibility to actual memory-based selection

Let G be any permutation of the eight triples `(m,x,y)` of Boolean values.
Its three output functions and those of `G^-1` have unique multilinear
integer representations of degree at most three on that domain. The code
constructs these coefficients by exact Boolean-cube interpolation.

Use lane4's gate: first form `s=y(1-x)` and `m'=m XOR s`; then conditionally
swap x and y according to m'. Its table is a three-cycle of states 1,6,5
(indexed as `4m+2x+y`), with the other five fixed. It is **not involutive**.
When m=0, its output lanes are `(max(x,y),min(x,y))`, while the changed memory
retains which input was selected. Used memory changes later decisions; there
is no irreversible reset to a perpetually ready state.

Let S shift **only x** one face forward, leaving memory and y at their nodes,
and put `F=S G`. Its inverse is `F^-1=G^-1 S^-1`. Thus:

- Forward output x reads all gate inputs at the incoming face; other outputs
  read the target node.
- Every inverse output reads memory and y at target plus x at the outgoing
  face.

Each term therefore lies on one physical face edge. Streaming x and y in
opposite directions would generally make the inverse cubic memory term span
both neighbors and violate the contract; that construction is deliberately
not used.

Compile the one fixed tensor

\[
 u(b)=3\big(F(b)+F^{-1}(b)\big).
\]

Preparation constructs the complete old slice `a=F^-1(b)` from a Boolean b;
all remainder values 0 through 5 are allowed. Since the input is a multiple
of three, Rule3 gives

\[
 a'=b,\qquad b'=F(b)+F^{-1}(b)-a=F(b),\qquad r'=r.
\]

The next state again obeys `a'=F^-1(b')`, so induction proves the Boolean
domain and exact first-order behavior for arbitrarily many updates. No
inverse-gate oracle runs during evolution: both F and its Boolean inverse
have already been compiled into fixed polynomial monomials. The Engine sees
only the original integer tensor. Runtime has no branch selector, optimizer,
global score or callback.

Outside the prepared sector, the polynomial Rule3 map remains exactly
invertible, but the Boolean gate interpretation and boundedness are not
asserted. The validator rejects such a seed for that claim. This distinction
is essential: proof on a restricted initial-data sector is not a global
bound on every integer trajectory.

## Budget, conserved quantity and observation boundary

The selector has three retained channels `(memory,moving,local)`: nine
integers per node, 22 canonical monomials, maximum degree three, and no old-a
input dependency. On its proved sector a and b stay Boolean and carries stay
in 0..5. The sum of x+y over the periodic board is conserved by the local
permutation and transport. Memory bits are allowed to change; their values
retain history and modify later routing.

This particle-count invariant is not a proof of stress-energy or momentum
conservation. The moving lane has a distinguished face direction, and no
evolving metric has been coupled to its speed. Its finite invariant state
space also means each full orbit eventually recurs: indefinite strictly
increasing state complexity is not a claim of this construction. Lane4 tests
finite structural growth, memory dependence and return/burst protocols on
this same mechanism.

All remainders are unchanged, so its canonical arithmetic events are C0.
The click decoder remains passive. A recorded click can identify a retained
interaction, but never supplies an unrecorded new state update. Structural
selection is already in G and its memory. Neither a Born distribution nor
quantum collapse is assumed or inferred from these events.

## Checked implementation and public handoff

`validation/selection/clocks.py` exports:

| Function | Purpose |
| --- | --- |
| `clock_tensor`, `clock_invariant` | Native one-channel phase and exact positive invariant |
| `matched_clock_tensor`, `matched_invariant` | Two-channel face exchange and positive invariant |
| `build_native_gate(table,direction)` | Compile F+F^-1 into an immutable three-channel tensor |
| `first_order(values,table,L,direction,inverse=False)` | Independent truth-table/shift reference, outside runtime |
| `prepare_gate(table,current,L,direction,remainders)` | Complete invariant-sector initial data |
| `validate_prepared_state` | Check the claimed sector before interpreting the run |

Reproduce:

```bash
python -m validation.selection.clocks --out runs/selection/clocks
```

The checked run reports:

| Check | Result |
| --- | --- |
| Signed native-clock initial pairs with all six carries | 726 passed |
| Face-clock transitions, all six directions | 36 passed |
| Selector complete states against independent first-order oracle | 1,152 passed |
| Complete 24-step selector rewinds | 48 passed |
| Arbitrary off-sector three-step rewinds | 6 passed |
| Strict face-support violations | 0 |
| Selector canonical events | 46,944, all C0 |
| Invariant-sector maximum bit lengths | a/b: 1; retained r: 3 |

The clock test also uses signed 90- and 100-bit preparations. Selector traces
include periodic seams and all carry classes. Each tensor fingerprint and
the audit source hash are saved in `runs/selection/clocks/clocks.json`.
The selection oracle uses table lookups and shifts, never the polynomial
tensor evaluator or production Engine to construct the expected result.

What is now constructive is the exact bounded state/memory/transport
mechanism in three channels. The next physical gate is a compatible stress
and metric-response encoding for those same state variables, with complete
source accounting and preserved domain. Appending it to 45 fields without
that coupling would only satisfy an arithmetic budget, and is not done here.
