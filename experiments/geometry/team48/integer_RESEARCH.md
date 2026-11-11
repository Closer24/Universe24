# Exact integer encodings investigated by the seven-agent review

These are isolated experiments. They do not replace the default Einstein ADM
law, and none of the arithmetic identities below proves discrete Einstein
constraint preservation or stability.

## One field bank and one computational sign

For a polynomial right-hand side of degree at most two, write
`f(y)=f2(y)+f1(y)+f0`. Set `s_(n+1)=-s_(n-1)`, starting with two signs.
Store one gear per physical field with `a=s_(n-1)y_(n-1)` and `b=s_n y_n`.
One extra phase gear stores `a_c=s_n,b_c=s_(n+1)` and has input zero.
The fixed input for a field is

`u = 6h b_c [f2(b) + a_c f1(b) + f0]`.

Whenever every coefficient of `2h f` is integral, all field inputs are
multiples of three. Every remainder is then frozen, including arbitrary
initial remainders from zero through five. Rule3 gives exactly
`y_(n+1)=y_(n-1)+2h f(y_n)`. Quadratic terms have input degree three;
linear terms use both clock counters and also have degree three. Old-a
dependencies run only from the sign channel to physical fields and are
acyclic. Multiplying a legal local term by a local clock preserves strict
single-edge support. The phase must be spatially uniform.

All retained memory is counted: F physical fields use F+1 channels and
3(F+1) integer entries per lattice node. The 24-field vacuum uses25;
the Fermi-frame complex Klein-Gordon plus comoving dust model uses36;
adding independent source-free Maxwell uses42. The triangular20-field
geometry makes these32 and38 respectively. There are no extra scratch
registers in this encoding. The phase is computational, not proper time.

This saves a redundant explicit time bank; it leaves the physical leapfrog
map unchanged. The nonlinear integer coefficient obstruction, spatial CFL
barrier, constraint drift and possible metric degeneration remain. Generic
fine coefficients are explicitly rejected, never rounded secretly.

## A one-channel exact repeated division primitive

Take one channel with fixed linear input `u=10b`. Use even remainder
`r=2e`, with `e` in `{0,1,2}`. Define exact integer coordinates

`z=(3a-b-e)/2`, `w=(3b-a+e)/2`.

The domain is `3a-b-e` even. Its coordinate form is
`w-z+e = 0 (mod4)`, with inverse

`a=(3z+w+e)/4`, `b=(z+3w-e)/4`, `r=2e`.

Rule3 implies, without modifying its divisor,

`e_next=(b+e) mod3 = z mod3`,
`z_next=(z-e_next)/3 = floor(z/3)`,
`w_next=3w-e`.

To verify the congruence used above, reduce `2z=3a-b-e` modulo3:
`z=b+e (mod3)`. These formulas preserve the coordinate domain. The map
has the explicit inverse

`e_old=(-w_next) mod3`,
`z_old=3z_next+e_next`,
`w_old=(w_next+e_old)/3`.

Prepare `a=b=N,r=0`. Then `z_0=w_0=N` and after k Engine ticks
`z_k=floor(N/3^k)` for every signed integer N. A constant denominator
for the arithmetic readout is justified by the proved invariant above; it
is not an arbitrary physical metric ratio. This law is linear, local,
horizon independent, has one channel/three retained integers per node,
and needs zero clock or scratch channels. Discarded digits remain encoded
in the growing history coordinate, so bit memory is not bounded.

The primitive is a real use of the fixed-six carry for exact refinement
arithmetic. It is not yet an autonomous reusable field-update compiler:
its exact quotient readout contains the private core remainder, which
polynomial tensor factors cannot read. A quotient handoff, stopping/reuse
schedule, and error/stability analysis for a complete sourced Einstein step
are still missing. The experiment does not conceal them in a callback.

## A limited obstruction to exact nonternary division

For polynomial integer initial counters with a fixed initial remainder,
after t fixed Engine steps, congruent inputs modulo `3^(t+1)` produce
counter outputs congruent modulo3. Each core division loses at most one
factor of three; the remainder update preserves the rest. This follows
inductively from polynomial congruence preservation. Consequently no fixed
number of such steps followed only by an integer polynomial counter readout
can realize `floor(N/2)` for all unbounded integers N: choose N=0 and
N=`3^(t+1)`. Their required outputs differ by1 modulo3. This statement
does not cover prepared encodings that already supply nonpolynomial
information, remainder-informed rational readouts, or adaptive schedules.
It does not obstruct the constructive ternary divider above.

Run `python -m experiments.geometry.team48.integer_audit` for exact
arithmetic and encoding evidence, written under `runs/team48/integer/`.

## Exact comparison with PR39

`integer_pr39_audit.py` uses the materialized PR39 modules at reviewed head
`35344a1ba5c12c857404115e893911411ece7d35`. Its original70-channel Engine
and the square-dust36-channel Engine agree on all35 physical fields in both
time slices, after explicitly renaming its Pi/Q/W fields. The symbolic RHS
and H/M constraints agree too. All four clock phases, nonzero retained
remainders, signed large integers, independent scalar Engine oracles and
complete rewind are tested. This is physical-trajectory equivalence between
different retained encodings, not equality of their complete states.

Run `python -m experiments.geometry.team48.integer_pr39_audit`.

## Staggered offsets permit selected cubic equations

`integer_staggered.py` is a separate compiler with an explicit offset
`delta_i` in `{0,1}` for every field. Put `sigma_i(n)=s_(n+delta_i)`.
Encode `b_i=sigma_i(n)y_i(n)` and `a_i=sigma_i(n-1)y_i(n-1)`.
The shared phase gear remains `a_c=s_n,b_c=s_(n+1)` with input zero.
Offset zero therefore uses current sign `a_c` and next sign `b_c`;
offset one uses current sign `b_c` and next sign `-a_c`.

For each monomial of `2h f_i`, multiply its integer coefficient by three,
the target's next sign and every input field's current sign. Cancel pairs
of the same clock sign using `a_c^2=b_c^2=1`. This identity holds on the
proved prepared sector and is preserved exactly by the zero-input clock.
All resulting inputs are multiples of three, so every core carry remains
unchanged. Rule3 then gives precisely the desired physical leapfrog.

For a degree-d monomial, the clock powers before cancellation are

`power_a = delta_i + d - sum(delta_inputs)`,
`power_b = 1 - delta_i + sum(delta_inputs)`.

Degree-two terms always leave exactly one clock factor. Degree-one terms
leave either zero or two clock factors. A cubic term leaves no clock
factors exactly when

`delta_i + sum(delta_inputs) = 1 (mod2)`.

Otherwise it would have degree five and is rejected. This is not a
compiler for arbitrary cubic equations: a self-cubic `dot(x)=x^3` fails
for both possible offsets. Old-a reads still involve only the single phase
channel, and all physical field factors read old-b values. Exact inversion
and single-edge support therefore follow the same structural requirements.

The positive-pair geometry assigns opposite offsets to K/Gamma, Pi/Xi,
and E/M, with off-diagonal B opposite K. Its diagonal representation
`B_aa=p_a^2+q_a^2` produces precisely the supported cubic terms. With
charged scalar, Maxwell, signed square-density dust and the three amplitude
pairs, the actual compiled tensor has43 physical fields plus one phase:
**44 channels,132 retained integer entries per lattice node**, with no
hidden scratch registers. Its input degree is three.

For each amplitude pair, the physical leapfrog reads
`p_next=p_previous+h*K_aa*p` and likewise for q. Thus
`W_n=p_n*q_previous-q_n*p_previous` obeys `W_next=-W_n` exactly.
If each initial W is nonzero at every node, p and q cannot vanish together
at any tick. All three diagonal B entries and hence det(B) stay positive.
This proof does not require bounded coefficients or frozen matter.

This positive-pair model changes the physical discrete dynamics. It is
continuum-equivalent to the triangular frame coordinate change, not
trajectory-equivalent to the old B leapfrog. Nonzero W supplies a second
discrete mode: continuum p and q solve the same first-order equation and
have constant ratio, so exact continuum sample pairs have W=0. A physical
refinement family must make its normalized W vanish while independently
showing convergence and controlling constraints. Neither is proved here.

The returned continuum-jet constraints cannot substitute a product rule
for differences of the composite B. Discrete diagnostics must reconstruct
B first and difference that actual array; the geometry reviewer supplied
`geometry_positive_pairs.sampled_constraints` for this distinction.

Run `python -m experiments.geometry.team48.integer_staggered_audit` for
the actual44-channel tensor, all four phases, independent scalar and cubic
RHS oracles, nonzero carries, Wronskians, positivity and complete rewind.
Hamiltonian/momentum preservation and general Einstein convergence remain
separate unfulfilled gates.
