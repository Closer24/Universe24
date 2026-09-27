# The law of the GameBoard

The one document of the law: what the engine computes, in whole numbers,
and why. Every symbol is named in English where it first appears. A
scalar is written plain, a vector in bold lowercase (**n**), a matrix or
an operator in bold uppercase (**C**). A line that no longer holds is
not in this document.

## The GameBoard and the families

### The objects

A **Node** is a physical location. The **GameBoard** is all the Nodes
together, a box of `shape` = (N_x, N_y, N_z) Nodes; each axis is periodic
(the box a torus on that axis) or open (a face beyond which no Node
lies), as the world declares. Two Nodes that differ by one step along
one axis are joined by a **Link**; each Node has six Links, one through
each of its six **Ports**, named by their outward direction +x, -x, +y,
-y, +z, -z. An axis of one layer folds: its two Ports return the Node
itself. The local information of a Node is its **NodeState**: the
levels and remainders of the families at that Node, and nothing else.
A change of a NodeState is an **Event**; the rule that makes it is a
**LocalRule**, and there is one LocalRule, Rule3 ([Rule3](#rule3)).

A **family** is one kind of physical value with its own declarations
([a family's declaration](#a-familys-declaration)). A family's **record** is a set of levels over the
GameBoard, one integer per Node per level, with a remainder per Node; a
family with two levels per Node holds a **pair** (re, im) at each Node.
A **body** is a set of Nodes on which a family's **count** stands, with
the values the body's writer declares (its content, its momentum, its
spin, its moment); a body is one connected region.

### A family's declaration

Every physical number comes from the world's files: the universe file
(the families and the universe's integers) and the world file (the
bodies, the detectors, the readings). The engine holds no number of its
own; a scale that is no physics (the amplitude unit A of [the generator](#the-generator) (f), a
product bound) is derived from the integer width, never written.

The universe's integers: the Node clock Gamma (the pace of an empty
Node, every family's clock unit); the amplitude bound A_bound, the
largest level a record may reach before the run is refused; Lambda, the
charge's weight; the momentum unit Q_unit; the twist table ([the transport](#the-transport)).

A family's row: its parts (1 for a scalar; [1, 3] a time part and a vector;
[1, 3, 6] a time part, a vector and a symmetric tensor); its phase (1, one
level per Node; 2, a pair); its kinds (the key `kinds`, an integer from 1,
required; every shipped family declares 1): a family of k kinds holds k
counts and k levels at every Node, each stepping by the family's one line,
and a read's weight is one integer for every kind or a k x k integer matrix
mixing them, the read the bilinear form over the kinds; its pair [num, den],
the cosine of its rest rotation, cos omega_0 = num / den, or the word "body"
where every body and record declares its own; its reads, each a read family
with a signed weight, a twist (an integer, or "own") and by (plain, or q,
the reading record's charge sign); its held writer (the count word, the held
factors, the dipole); its self-source unit P_2 (0 off); its clicks (whether
it takes and gives, and its quantum's norm T, one integer per family, the
action of one quantum). T is a declaration: Rule3 is linear and its form's
scale is free, so no line of Rule3 fixes T; nature pins it and no body
declares it.

### The interval

The engine steps every family from the state at the interval's start to
the state at its end. Every read is of the start's values: the six
neighbours' levels, the Node's own pace, the arrivals, never a value
written in the same interval; one Link per interval and nothing in zero
time. The interval has five places, in order:

(i) the clicking families' step, every component, with the transport through
the Ports and the self-source; (ii) the bookings at the Ports (the current),
the ladder, the takings and the givings, the count's line; (iii) the held
families' step; (iv) the holds written (a body's values into its family's
levels), the clicks' changes of a body's content, charge and momentum
included; (v) the bodies on one Node: the feed, the induction, the spin's
step, the recoil's accumulator.

The order within a place, where two primitives write one value, is the
step file's (`law/step.json`), one data file shared by every world,
read at the start, its digest in every run's output. A click's writes
enter at the next interval. Backward, the places run in reverse order
and each primitive runs its own inverse.

### Readings and measurements

A **measurement** is a detector's click: the one act of the law on the
state that ends a record at the detector and changes the detector's own
record ([the count's line](#the-counts-line)). Only a measurement is compared with nature. A
**GameBoard reading** (a level, a support, a total, a body's centre) is
a diagnostic and is labelled so wherever it appears; a number whose kind
is not named is not a result. Displays read state and write nothing.
Every run is headless; the readings are declared in the world file and
written in one format, each labelled DETECTOR, GAMEBOARD or HOST.

## Rule3

### The line

Every family, at every Node, with the wall w, the read coefficient R_a on
each axis a, the self coefficient S, the level a_now at the interval's
start, a_before one interval earlier, and the remainder r kept at the Node:

  w a_next + r' = SUM_a R_a (arr_(+a) + arr_(-a)) + S a_now - w a_before + r,
  0 <= r' < w,

arr_(±a) the **arrival** through the Port ±a: the neighbour's level, or
its rotation by the Link's angle ([the transport](#the-transport)); 0 beyond an open face;
the Node's own level on a folded axis. The remainder r is the Node's own
and never travels.

The coefficients at a Node, from its paces ([the paces](#the-paces)) and its
family's pair [num, den]:

  w   = 6 den Gamma^2,
  R_a = 2 num p_a^2,
  S   = 12 den Gamma^2 - 6 (p_0^2 + Gamma^2)(den - num) - 4 num (p_x^2 + p_y^2 + p_z^2).

At the vacuum's pace p_0 = p_a = Gamma the line is the plain second-order
wave rule of the pair: a_next + a_before = 2 cos omega a_now with the
six-neighbour coupling, the rotation omega_0 with cos omega_0 = num /
den at wave number zero. A held family's field steps at its row's pair,
[1, 1] or any other, with the pace 1 and the wall 3 den, at first order.

### The direction

Let sigma be the direction, +1 forward and -1 backward, and let div and
mod be the floor division and its remainder in [0, w), and rho the
remainder carried in. With

  u = sigma (SUM_a R_a arr_a + S x - w y) + rho,
  z = sigma (u div w),  rho' = u mod w,

forward (x, y, rho) = (a_now, a_before, r) gives (z, rho') = (a_next, r');
backward (x, y, rho) = (a_now, a_next, r') gives (z, rho') = (a_before, r).

PROOF. Forward, sigma = 1, the line is the definition of div and mod.
Backward, sigma = -1: write Y for the right side's first two terms, SUM_a
R_a arr_a + S a_now. Then u = w a_next - Y + r', and z = -floor(u / w) =
ceil((Y - w a_next - r') / w). From the forward line, Y - w a_next - r' = w
a_before - r with 0 <= r < w, whose ceiling divided by w is a_before
exactly; and rho' = u - w floor(u / w) = w a_before - (Y - w a_next - r') =
r. So the backward call returns (a_before, r) bit for bit; the reversibility
of every run needs no second function. Checked bit for bit on 20,000 random
cases against a forward and a backward function written separately.

### The four acts

Rule3's line is one act; declared coefficients make it four:

(a) THE READ, the line above over the GameBoard (the six arrivals); (b) THE
ONE-NODE STEP, the line with the neighbours' reads declared 0: a_next +
a_before = (a / b) a_now, the rotation by the angle whose doubled cosine is
a / b (Chebyshev's recurrence); with a / b = 1 and the coefficient on
a_before declared 0 it KEEPS a level; with a / b = 2 from (0, 1) it COUNTS,
a_t = t; (c) THE DIVISION, the line with R = S = 0: w a_next + r' = the
numerator + r, Euclid's division with the remainder kept; (d) THE LOAD, a
declared integer in the numerator, how a count enters a level.

A COMPOSITION of Rule3's acts with declared coefficients is a finite
sequence of these acts, each with its coefficients (a pair, a weight, a
wall, a load) declared in the files, applied to declared levels.

THEOREM (what the acts can form). Every composition of the four acts is
a piecewise-linear function of the levels with integer slopes: a sum of
linear forms and of floors of linear forms, composed. No such function
is quadratic in the levels.

PROOF. Each act is a linear form of the levels or the floor of one; a
floor of a linear form is piecewise linear with integer slopes; sums and
compositions of piecewise-linear functions with integer slopes are of
the same kind. The second difference of such a function in any one
level is 0 almost everywhere, while the second difference of a product
now_i before_j in the pair (now_i, before_j) is 1. So nothing bilinear
comes from the acts alone.

What the theorem separates: every product of two levels in the engine
is a **booking**, a reading of a bilinear form with declared
coefficients and no write ([the booking](#the-booking)); the one thing written from a
product is the count, by the count's line ([the count's line](#the-counts-line)), and that
product is Rule3's own conserved current.

THE THREE TESTS OF EVERY RULE. A line enters the law only if it is
generic (one primitive with declared integers, no family's name and no
kind), vector (one of the acts on the state, no root and no float) and
local (its own record and the six neighbours, nothing kept at a Node
beyond the law's numbers). A hypothesis that needs more is stated under
its own name, outside the law.

### The paces

The **pace** of a Node for a family is what its reads make of the Node
clock:

  p_0 = Gamma - SUM over the reads of (weight x by x the read family's time level at the Node),
  p_a = p_0  - SUM over the reads of (weight x by x the read family's aa component div 2),  a = x, y, z,

one division per read per axis with the remainder kept on the reading
family's record. A positive weight is a hollow (the read family's level
slows the clock, an attraction); a negative weight is a hill. By "q" the
weight is multiplied by the reading record's charge sign. A family with
no reads steps at p_0 = p_a = Gamma, the plain rule. The clock's slowing
is this pace: a record at a Node of pace p rotates and moves as a record
at Gamma does, with its intervals p / Gamma as long.

THE GUARD, two-sided: 0 < p <= P at every Node, with the edge

  P = isqrt(Gamma^2 (18 den + 6 num) div (18 num + 6 den)),

above Gamma where num < den. Below 0 the pace is no clock; beyond P the step
is unstable: the mode at wave number pi has the factor (S - 6 R) / w, which
is -2 num / den at p = Gamma and falls below -2 once p^2 / Gamma^2 exceeds
(18 den + 6 num) / (18 num + 6 den), so the record grows without bound; P is
the largest pace at which p^2 (18 num + 6 den) <= Gamma^2 (18 den + 6 num)
holds exactly. A hill lessens a hollow and never exceeds it; a pace outside
the guard refuses the run naming the Node.

THE BAND AT A PACE, a reading of the line and no new rule: at a Node of pace p on every axis a record's rotation at wave number k along an axis is cos omega = 1 - (p / Gamma)^2 (1 - (num / (3 den)) (2 + cos k)), with cos k_x + cos k_y + cos k_z in place of 2 + cos k off an axis, so the band of rotations a body's Nodes carry narrows with p^2: a record whose rotation lies outside the band there is evanescent inside (for [1, 1], cosh kappa = (Gamma / p)^2 (1 - cos k) - 1 per Node) and is reflected whole, and one whose rotation lies inside is slowed to the band's group velocity (num / (3 den)) (p / Gamma)^2 sin k_in / sin omega with 1 - cos k_in = (Gamma / p)^2 (1 - cos k) for [1, 1]; light ([1, 1]) meets a total mirror exactly where p < Gamma sin(k / 2), that is where the count c exceeds Gamma (1 - sin(k / 2)) (2,929 at lambda = 4 Links, 3,891 at 4.78), and a window otherwise, with the step's partial share at each face.

A body is a balance of a hollow and a hill of different ranges: a
hollow alone in three dimensions binds no record (it collapses into its
own well or disperses); gravity is the one-signed exception. This is a
theorem of the rule read from its runs, not a line added to it.

### The bound

The rule's total at a Node whose levels and arrivals stand at the
amplitude A is at most 6 A |R| + A |S| + w (A + 1). Every world declares
integers under which this total sits below 2^63 - 1, the width of the
engine's integers, or the loader refuses it naming the total; the
generator's amplitude unit is the largest A that keeps it inside
([the generator](#the-generator) (f)). With Gamma = 10^4 and A = 2^20 the total is near 3 x
10^18, one third of the room.

### The transport

A family with a pair (re, im) at each Node and a read with a twist turns
its arrivals by the Link's angle. On the Port along axis a in the sense
sigma, for each such read with the factor f (the weight times the
record's own rotation for the twist "own", else the declared twist; by q
the charge sign):

  k = sigma x f x (V_a at this Node + V_a arrived through the Port),

V_a the read family's vector component along the axis; both ends form the
same number with opposite signs, so the transport back is the inverse
rotation. The **twist table** of the universe gives, for the angle k in
units of theta_unit = 1 / (4 Gamma 2^16) radians, a Pythagorean triple (c,
s, d) with c^2 + s^2 = d^2 exactly: |k| = k_1 2^10 + k_0, the fine triple of
k_0 and the coarse triple of k_1 composed, (c_1 c_0 - s_1 s_0, s_1 c_0 + c_1
s_0, d_1 d_0), with (c, -s, d) for k < 0 and (1, 0, 1) at k = 0; a k beyond
the coarse table, or any k on a world without a table, refuses the run
naming the Port. The arriving pair is rotated to the nearest unit:

  R_re = (2 c re - 2 s im + d) div 2 d,   R_im = (2 s re + 2 c im + d) div 2 d,

two read acts of Rule3 with the coefficients (2c, -2s) and (2s, 2c) on the
two arrivals, the load d, the wall 2 d, the remainder not kept: a remainder
carried across intervals is one to one only while d stands, and d changes
with the angle every interval; the rounding is unbiased in the mean and the
inverse recomputes the same triple from the start's levels, exact. The
record's own rotation "own" is round(2^16 omega_0), written once by the
loader from the record's pair (matter) or from its wavelength on light's
dispersion (light), so no per-world number is declared. The charge's twist
on a charged record is Lambda times "own", by q: no separate number exists.

### The second level

A phase-2 family runs [the line](#the-line) on each of its two levels with the
transported arrivals; with no twist the second level stays exactly zero
when it starts zero. The **self-source** of a family with the unit P_2
above 0, at every Node from the start's levels,

  Sigma_self = (SUM over the six Links, the family's records and their levels of (a_j - a_i)^2) div P_2,

is subtracted from the step's right side as w Sigma_self: each
difference is a read act, its square a booking of the family's own
levels, the division Rule3's with the remainder not kept; P_2 = 0 turns
the line off, and a nonzero P_2 stands at or above 24 A_bound.

### The conserved form

The read matrix 2 num p_i^2 is not symmetric where the paces differ, so
the form carries the weight 1 / p_i^2 on the Node terms and the plain
current on the Links:

  E = SUM_i [w (now_i^2 + before_i^2) - S_i now_i before_i] / p_i^2 - 2 num SUM_i now_i S_6(before)_i,

S_6 the sum over the six neighbours. E is exact where the paces stand and
changes by the work term where they move; it is a GameBoard reading.
Its Link term, the plain current num (now_i before_j - before_i now_j)
through the Link ij, is the current of Rule3's own conservation law and
the one product the click reads ([the count's line](#the-counts-line)).

PROOF at constant paces. Without the rounding the line is a_next +
a_before = **M** a_now with **M** the matrix whose diagonal is S_i / w
and whose entries on the six Links are R / w. Let **D** be the diagonal
matrix of the weights 1 / p_i^2; then **D M** is symmetric, since R_a =
2 num p_a^2 at the reading Node and the weight 1 / p_i^2 cancels it on
both sides of every Link. For a symmetric **K** = **D M** the quantity
Q(x, y) = x . **D** x + y . **D** y - x . **K** y satisfies Q(a_next,
a_now) = Q(a_now, a_before): with a_next = **M** a_now - a_before,
a_next . **D** a_next - a_next . **K** a_now = (**M** a_now - a_before)
. **D** (**M** a_now - a_before) - (**M** a_now - a_before) . **D M**
a_now = a_before . **D** a_before - a_before . **D M** a_now, which
is the other side. Multiplied by w this is E up to the Link term's
sign convention. With the rounding, each Node's remainder adds at most
one unit of the level per interval to the walk of E.
## The click

### The booking

The **current** of a record into Node i from its neighbour j through
their Link over an interval is the bilinear form of its two levels at
the two ends,

  F_ij = weight x (now_i before_j - before_i now_j),

the pair's second level added (im_now_i im_before_j - im_before_i
im_now_j), the weight the family's common wall in the form's units (its
num where one pair stands); positive inward, as the ladder reads it: a
record of wave number k travelling from i to j has F_ij = -2 weight x
|psi|^2 sin omega sin k, below 0. It is antisymmetric, F_ji = -F_ij, and
it is the Link term of the conserved form of [the conserved form](#the-conserved-form): the current of
Rule3's own conservation law. The booking reads it at a Port and writes
nothing.

### The count's line

The **family of clicks** is one family like every other: its level at a
Node is the **count** c, the number of quanta there; its wall is T, the
quantum's norm; its read is the current. At every Node,

  T c_next + r' = T c_now + SUM_j F_ij + r,   0 <= r' < T,

the sum over the six Ports of the current into the Node from its
neighbour over the interval, r the remainder kept at the Node: Rule3
with the coefficient 1 on each axis's inflow through its two Ports, T on
the count and the wall T. The **click** is the division: a quantum moves
whole from one Node to the next exactly when the remainder crosses T,
and never a fraction of one. The record ends where its last quantum
leaves it; the count that arrives at a detector's Node is the
detector's click, and a detector's count is the family of clicks' level
at its Nodes; an emitter's giving is the count leaving through its
outer Ports into the born record. The same line carries a body: the
count follows its record's current at every Node, one quantum at a
time, so a body moves without any accumulator of its position.

THE REMAINDER'S ORIGIN. The remainder at a Node starts at the ladder's
origin, (2 u + 1) T div 2 with u the record's residue ([the ladder](#the-ladder)):
started at 0, a Node with no quantum reads the count -1 at its first
outward swing (T c + r below 0), a hole the line conserves and nature
does not show. A body's count is laid with its record: at every Node
T c + r is the Node's share of the record's form plus the origin, so
the count follows the norm with the margin T / 2 against the rounding's
walk.

THE INVERSE is the same line with the current reversed: T c_now + r =
T c_next + r' - SUM_j F_ij, exact, the currents read from the
interval's levels as the forward step read them.

THEOREM (the count is conserved). Over any region of Nodes, SUM (T c_i +
r_i) changes in one interval only by the currents through the region's
boundary Links.

PROOF. Summing the line over the region, each interior Link's current
enters one Node's right side as +F and its neighbour's as -F and
cancels; what remains is the sum over the boundary Links, a telescoping
sum, exact in integers. On a periodic GameBoard with no face the sum is
constant to the bit.

THE VELOCITY. The record's wave number is conserved by the record's line,
and the count's line is the continuity equation of the current in integers,
so the count's centroid moves at the current's velocity, with no leak beyond
the ladder's remainder; a body at rest has zero net current at every Node in
the mean and its count stays in place (the open point, [what is
open](#what-is-open)). On the shipped worlds: the resting Lorentz world's
body keeps its count in place under its own standing record stepped by the
loop, two hundred intervals, the swing 2 x 10^-9 of T / 2; a record of two
levels with the phase k per Link, stepped by the loop on the moving Lorentz
world's GameBoard, carries its count at Rule3's group velocity R 2 sin k /
(2 w sin omega), the count's centroid within one Node of the record's over
six hundred intervals, and the integrated inflow of a slab is the change of
the form's share there within the rounding's re-allocation of the Link
terms. Under the count's line a moving body is the moving mode of
[the generator](#the-generator) (e), its count moved by its record's current.

THE BOUND. The total at a Node is at most 6 x weight x 4 A^2 + T (c + 1)
+ T: one current per Port, each the weight times the two products of two
levels at A on each of the two level pairs, the count's wall T (c + 1)
and the remainder below T. The shipped universe (A = 2^20, the weight
800) is within int64; a world declaring A beyond 2^24 at the weight
10^3 is refused by name; the generator's A ([the generator](#the-generator) (f)) is
admitted.

### The ladder

Until the count's line is bound in the loop, the click is read by the
**ladder**, the same division act on a record's inward flux. The data:
the record's residue u (its remainder at its giving Node), its norm T,
its wheel V, hence its threshold theta = (2 u + 1) T / (2 V), fixed at
the giving; the named detectors in their declared order with the face
last. At every interval each Node i of a detector receives the one-way
inward flux f_i(t) >= 0 of the record through its Ports (a Link between
two Nodes of one detector is not a Port and carries no offer); the
record's running total is C(t) = C(t - 1) + SUM_i f_i(t). The click is
at the first interval t* with C(t*) >= theta, at the Node whose segment
of that interval's increment, laid in the ladder's order, contains theta
- C(t* - 1); there the record ends, whole. The rungs are the division
act: b_k = (2 V C_k + Total) div (2 Total).

THEOREM (one quantum, one click). theta is crossed exactly once.

PROOF. C is non-decreasing, theta < T, and the total offered with the
face last is at least T (what leaves offers everything at the face), so
C crosses theta once; the deletion of the record at once leaves nothing
to cross it again.

THEOREM (Born's rule). Let u be spread evenly over {0, ..., V - 1}; then
the probability that the click lands at Node i is C_i(infinity) / T, the
detector's share of the record's total inward flux, whatever the time
profile.

PROOF. theta is then spread evenly over V points in [0, T).
The segments [C(t - 1) + SUM_{j < i} f_j(t), C(t - 1) + SUM_{j <= i}
f_j(t)), one per (interval, Node), partition [0, C(infinity)) and have
the lengths f_i(t); so P(the click at interval t at Node i) = f_i(t) / T
to the grain 1 / V, and summing over t gives the share. The counts over
many records are binomial about the shares, since the residues are
equidistributed and not a permutation.

A detector is one connected region of Nodes with one name; separate places
are separate names. A detector set is one Node of the count's line with its
Ports the set's outer Ports, the sum of its Nodes' lines with one remainder;
Born's rule is the shares of the current among the set's Nodes.

## The primitives

Every primitive of the engine is one folder under
`src/event_universe/features/` with its declaration (its name, its
place, what it reads, what it writes, its line here) and its function
`apply(term, start, own)`, which calls Rule3 and nothing else; the loop binds
the folders through the register and the step file. No folder holds a
number, a family's name or a default. Every write of a primitive is a
whole integer into a declared level; every division's remainder lives
on the record of the primitive that divided.

| Primitive | Place | Reads | Writes | The line |
| --- | --- | --- | --- | --- |
| the pair | (i) | the pair [num, den] | the record's levels | Rule3's coefficients from the declared pair ([the line](#the-line)) |
| the degree | (i) | the parts | the record's levels | the same line on 1, 3 or 6 components |
| the phase | (i) | the phase | the record's levels | phase 2 is Rule3 on the pair; phase 1 is Rule3 with the coefficient on a_before declared 0 |
| the signed read | (i), first on the right side | the read families' levels at the start, the signed weights, by, the tensor's parts | the paces | [the paces](#the-paces); the guard two-sided |
| the send | (i) | the record's level | the Link's value | the value on the Link is the level times the read's weight, R's factor |
| the receive | (i) | the Link's value, the twist reads, the twist table | the arrivals | [the transport](#the-transport): the angle per Port a read act over the wall 1, the triple the tables' composed reading, the rotation two read acts over the wall 2 d with the load d, the six arrivals summed per axis |
| the internal representation | (i) | the generators' tables | the record's pairs | n pairs, each rotated at the Port by the generators' exact tables in sequence, the one-Node step at the tables' pairs |
| the self-source | (i) | the family's own levels, P_2 | the family's level | [the second level](#the-second-level) |
| the operation | (i) | the coefficients | the record's levels | Rule3's line itself |
| the wait | (i) | the record's age | the record's age | the count (b) at a / b = 2: one interval |
| the clicks | (ii) | the current at the detectors' Ports, u, V, T | the record's tally; a body's content M_k at t + 1 | the ladder of [the ladder](#the-ladder) until the count's line is bound in the loop |
| the count's line | (ii) | the body's own record's levels at the Node and across its six Ports as the step produced them (a given record is another record; a loaded level carries no current), T, the weight | the count at a Node, its remainder | [the count's line](#the-counts-line) |
| the lifetime | (ii) | the record's age, L (the key `lifetime` of the record's family's row, an integer from 1; absent, for ever) | the record's end, a click at the face | the age is the count (b) on the record; at age L, wherever the record stands, it clicks at the face, the ladder's last detector, its whole content to the border the key names, after the ladder's click of that interval (the clicks first), so that every record clicks once |
| the clicks list | (ii) | the record's remainders, the wheels | the taken momentum's shares | the products' shares are the click's draw; the sum is the taken momentum exactly |
| the hand | (ii) | **S** and **n** of the taking body at their levels now, the declared hand (the key `hand` of the clicking record's family's row, -1 or +1; absent, no check) | admits or refuses the click | **S** . **n** is a booking of the spin's and the momentum's levels, the three products summed; its sign in {-1, 0, 1} against the declared hand refuses the click where their product is -1 and admits it otherwise, a set with no body and the face admitting with no check; a refused record stays whole with its running total and clicks at the next admitting set in the ladder's order, the face last |
| the polariser | (ii) | the record's pair at a polariser body's Nodes, the body's moment D (its axis and its angle a, [the transport](#the-transport)) | the record's pair; the two sets' shares | a hypothesis under its own name, not yet in the engine: at the body's Nodes the record's pair is turned back by the angle a through the transport and its second level is taken by the body's second set, the first level passing to its first set, so the shares of the click are cos^2 and sin^2 of the angle between the record's pair and the axis, the ladder then as written; a body with no moment polarises nothing |
| the giving | (ii) | the body's own levels, the weight g, the outward current through its outer Ports, T, M, **n** | the given family's level at the body's outer Ports; at the open M_k -= 1 and **n** at t + 1 | the three acts of one window in this order: the open (M_k -= 1 of the given family and the bulk share n_a -= sgn(n_a) (|n_a| div M), the division act with the wall M, both written at t + 1), the write (the given level at the body's outer shell += g x a_body each interval, a load, before the bookings; the outer shell is the body's Nodes with a Port to a Node outside the body, and no inner Node is written), the close (at outward x den >= norm the record named, its direction the tally's sign per axis); the open is the click's count move with the opposite sign, and a close is never an open: the count moves once per window |
| the pair-giver | (ii) | the giving's window; the emitter's keys `records` (1 today; 2 for a pair), `sense` (an exact pair [m, j], [1, 0] the same sense, [1, 1] a quarter turn) and `axis` (x, y or z) | two records at the close, each with its own ladder and norm, both with the window's residue u; at the open M_k -= 2 | a hypothesis under its own name, not yet in the engine: the close at outward x den >= 2 norm names two records, the shell's Nodes with an outer Port along +axis the first and along -axis the second, each with the norm T and the one residue u of the window (one draw, two clicks), the second's pair turned at the close by the triple of `sense` (the rotation act of [the transport](#the-transport), the remainder not kept); generic (declared integers, no name), vector (the count act and the rotation act), local (the shell's own Nodes) |
| the hold | (iv) | a body's content M_k, the quantum's weight w_k of each family's row (its key `quantum`, an integer from 1, required), W, **n**, the held factors, the dipole | the held family's levels at the body's Nodes; the body's remainders | the count s = SUM_k w_k M_k, a load into the time part; the vector part (factor x s x n_a) div W, the tensor part (factor x s x n_a n_b) div W^2, each with its remainder carried; the dipole sigma (D x e_j)_i div its divisor at the six neighbours |
| the source | (iv) | the record's D_i = now^2 - next x before at its Nodes, E_s (the source's scale) | the sourced family's level at the record's Nodes; the record's remainder | D_i is the booking of the record's own two levels (the form); the level gains weight x ((D_i + r_i) div E_s) each interval, the division act as a load; with a table weight x (s_cap D_i div (s_cap E_s + D_i)), s_cap the table's cap, no remainder, the denominator refused at or below 0; the field's shape is the static limit of Rule3, (Delta - kappa^2) a = -sigma / q with kappa^2 = 6 den / num - 6 (kappa the inverse reach, sigma the source, q the charge's weight) |
| the recoil | (iv) | the click's tally sigma_a, Q_unit, P_body (the rotation of the body's own mode, its period by the one-Node rule from its clock pair, never declared), lambda_q (the quantum's wavelength, 2 N q / p from its family's clock [p, q] on the world's N steps), L | a body's momentum **n**; the body's remainders | n_a += sigma_a x 3 Q_unit P_body (L div lambda_q) div L at the close, the giver and the taker with opposite signs: the quantum's momentum over the body's energy on the momentum's wall, W P_body / (M lambda_q) with W = 3 Q_unit M (the body's quanta cancel), so the velocity moves by P_body / (lambda_q M) and a heavy body's recoil is small by its quanta; a taker with no mode of its own has no period and takes no recoil; a kick that would carry 3 (**n** . **n**) to W^2 or beyond is refused naming the body (no speed at the wall, [the paces](#the-paces)); the store one remainder per axis on the one declared wall of the universe, L = the least common multiple of the wavelengths 2 N q / p over the families with a clock that a body of the world gives (a world with no giver has L = 1), each whole or the clock refused at load by name, which every lambda_q divides, so that clicks of every wavelength add exactly (the sum's exact floor); L divides the wavelengths' product and is refused by name at or beyond 2^63; a world whose families carry no clock has L = 1, nothing declared |
| the feed | (v) | the reads' levels at the two faces of each axis of the body (the Nodes read across its Ports), the body's two levels of momentum **n** (now and before, as the spin's), W, Gamma | a body's two levels of momentum **n**; the body's remainders | the contraction at a face, C = SUM over the reads of f x [the time level - (n_b V_b) div W + (n_b n_c h_bc) div W^2] over the face's Nodes with **n** now, f the read's factor (the weight, or minus the body's charge times the weight by q), V and h the read family's vector and tensor parts; the leapfrog n_next = n_before + 2 W x (C_+ - C_-) div (2 Gamma D_a F_a), the two levels then (n_next, n now), D_a the faces' distance in Links and F_a a face's Nodes; the potential per unit of mass is -C / (2 Gamma), so a body falls toward content the same for every family |
| the induction | (v) | the reads' vector parts summed over the body's N Nodes as the interval leaves it and at its start, the body's two levels of momentum **n**, W, Gamma | a body's two levels of momentum **n**; the body's remainders | the momentum part of the contraction, P_a = -SUM over the reads of f x V_a (the coefficient of n_a div W); both levels of **n**: n_a += W x SUM f x (V_a now - V_a before) div (2 Gamma N), minus the change of P_a; with the feed, d/dt (n_a - W P_a div (2 Gamma)) = W x (the gradient of C)_a div (2 Gamma): the Lorentz force and its gravitational twin in one line (the tensor part's change is second order and not carried) |
| the spin's step | (v) | **S** at its two levels (S_now, S_before), the read families' vector parts and time parts at the body's six neighbours, mu, **n**, W, Gamma, and the row `spins_step` of the family whose dipole is the spin: the curl's weight c_num / den and the tidal term's weight t_num / den (two pairs over one denominator) | a body's spin **S** | the leapfrog on the two levels, S_next = S_before + 2 [(Omega x S_now) + mu x B_q] div (W Gamma), the remainder on the body (the 2 the span of a step on two levels, the form's, as the feed's); Omega from the read whose dipole is the spin, Omega_x = [c_num x factor x (V_z(+y) - V_z(-y) - V_y(+z) + V_y(-z)) + (t_num ((t(+y) - t(-y)) n_z - (t(+z) - t(-z)) n_y)) div W] div (2 den) and cyclic, V the read's vector part and t its time part, the factor the read's weight (by q, minus Q times it); B_q from the read whose dipole is the moment, the same curl on its vector part times the read's weight div 2; the curls and the gradient reads with the coefficients +1 and -1 at the six neighbours (a neighbour beyond an open face reads 0), the crosses bookings, every division the division act with its remainder on the body; backward the same terms from S_before, subtracted, every division stepped back |
| the recoil's accumulator | (v) | sigma_a, k_q (the quantum's wave number), M | a Port's angle accumulator | sigma_a x (k_q div M) into the Port's angle, the taker and the giver with opposite signs |
| the trace | any | every act's integers | nothing | a reading of every act, it writes nothing |

The hop is retired: the count's line moves the count with its record's
current, and no accumulator of a body's position remains. The rows whose own
code the count's line retires when bound: the ladder's rungs, the giving's
open and close, the clicks list's count move, the lifetime's tally.

A body's writes into its family's levels (the hold): a body of quanta
M_k of the family k, each family's quantum weighing w_k (the key
`quantum` of its row, an integer from 1, required; every shipped family
declares 1), has the count s = SUM_k w_k M_k, the charge Q, the
momentum's whole part **n** on the wall W = 3 Q_unit M (its velocity
**v** = **n** / W in Links per interval), the spin **S** and the moment
**mu**; at every Node of its support it writes gravity's time part s, its
vector (4 s n_a) div W, its tensor (2 s n_a n_b) div W^2, the charge's time
part Q and vector (Q n_a) div W, the held factors (1, 4, 2) and (1, 1) the
universe file's numbers; and the dipoles at its Node's six neighbours, gravity's vector i at the Node + sigma e_j gaining sigma (S x e_j)_i, the charge's (sigma (mu x e_j)_i) div 2.
## The stable body

### What a body is

A body is its count and its record. The count c_i is the family of clicks'
level at the body's Nodes, in quanta; it enters Rule3 through the pace
alone, p_i = Gamma - c_i, and it never splits: a quantum moves whole, by the
count's line. The record (now, before) of the body's family splits by the
send and is bound by the count. The world file names the body's family, its
Nodes, its count per Node, its momentum **n** at its two levels (now and
before, both declared, a resting body's equal) and its spin's two levels
where it has one, and on a body that gives its stocks and its emitter (the
given family, the weight g, the norm T with its denominator, the ladder by
name), and nothing else: no lowered pair on its Nodes, no seed, no stop, no
profile, no closed Port, no period (P_body is its mode's rotation).

### The well

At a Node with count c Rule3's one-Node rotation rises from cos omega_0 =
num / den by (1 - p^2 / Gamma^2)(den - num) / den, and its bonds fall from
num / (3 den) to num p_i p_j / (3 den Gamma^2): the symmetric form of the
line with the weights 1 / p_i. The depth is bounded by the family's own 1 -
cos omega_0, so a family whose pair lies close to 1 binds nothing: on [800,
809] (1 - cos omega_0 = 0.011) no cube of any side at any count is bound; on
[800, 1200] (1 / 3) at Gamma = 10^4 a cube of side 12 is bound from 500
quanta per Node (the mode's share inside 0.79, 0.92 at 1000, 0.997 at 5000),
of side 6 from 1000, of side 3 at 3000, one Node at 5000; omega_b / omega_0
for side 12 is 0.832 at 500 and 0.771 at 2000. A body's clock is set by its
count and its side, from the rule: a body's mass is its count.

### The generator

The generator builds every world from zero; it declares nothing and
holds no float.

(a) THE INPUT AND THE REGION. The input is a world file in the law's
form: the GameBoard, the Node clock, the universe file it names and one
body by its Nodes with their counts; nothing on the command line. The
iteration runs on the body's Nodes and their surroundings, out to where
the mode's tail falls below one unit; the count stays on the body's Nodes.

(b) THE ITERATION. Rule3's read act with the before-coefficient 0, a <-
(SUM_a R_a arr_a + S a) div w on the region, then the division act to
the amplitude unit A (the level times A over its largest size): the
power iteration of the symmetric form's top mode (the bound mode, above
the band, the eigenvalue largest in size), at cos omega_0 / cos omega_b per step.

(c) THE STOP FROM THE INTEGERS. The profile is an integer vector bounded by
A, so the iteration is a map on a finite set and enters a cycle; the stop is
the first repeat, exact, no tolerance and no declared count, the profile
there the mode within one unit of A.

(d) THE TWO LEVELS AND THE AMPLITUDE FROM THE COUNT. The mode's second
level is the read act once more, halved (**M** phi = 2 cos omega_b
phi); the two levels are scaled together
so that the record's conserved form equals c T, c the body's count and
T the family's quantum norm: the body's record carries exactly its
quanta's norm, and nothing of the body is declared. THE UNITS: the ladder reads a record's norm with the weights 1 / R_i and
the family's common wall L, the form of [the conserved form](#the-conserved-form)
times L / (2 num), so the ladder's T is the form's T times L / (2 num).

(e) THE MOVING BODY. The momentum **n** names the velocity **v** =
**n** / W. The moving body is the resting envelope with the phase k per
Link along the axis of motion, the rotation act on its two levels by the
triple of the pair (m, j), cos k = (m^2 - j^2) / (m^2 + j^2), exact; k is
the pair at which the packet's own current along the axis, SUM over its
Links of F_ij = now_i before_j - before_i now_j at the norm T (M quanta),
equals T n / (3 Q_unit), the count's line's velocity of the packet, M
cancelling: by bisection on j at the declared m (the body's `momentum` n and its `phase_denominator` m are its numbers in the world file, k is derived).
The read with the arrivals along the axis turned by +k and -k on a fixed
well is a gauge of the plain read: its fixed point is the rest mode, its
current 0 and its rotation the rest's at every k; the packet is stationary
in the body's frame only where the count's line moves the well at **v**; the
loader's proper pair of a moving body is the packet's rotation at its centre.
Generic: one primitive, the family's pair and the body's two numbers; vector: the rotation act, a booking, the division act, no root; local: each Node's six Links.

(f) THE AMPLITUDE UNIT A IS DERIVED, NEVER WRITTEN: the largest amplitude at
which Rule3's total stays inside the integer width at every content of the
region, the bound of [the bound](#the-bound) solved for the amplitude, A =
(2^63 - 1 - w) div (6 R + |S| + w) at the content whose coefficients are
largest (between 2^22 and 2^23 in the cases of (c)). The fixed point does
not depend on A beyond its resolution: at A / 2 the profile agrees with the
one at A, rescaled, within 12 units of the coarser, and the rotation to
10^-6; the final scale comes from c T.

(g) THE FIELD AT REST, THE START OF A WORLD. The generator iterates the held
family's own line to rest first, at the pair of the family's row, as the
rewriting hold makes it: the body's Nodes clamped to the count, the
homogeneous line outside (a source row's static limit, (Delta - kappa^2) a =
-sigma, is the other case, not this one). From nothing the level at every
Node is num S_6(a) div (6 den) by the division act on a fine unit derived
from the width, the body's Nodes rewritten each time; the map is monotone,
so the levels rise to a fixed point, the stop its first repeat; the levels
are the rest within one unit, and the mode is solved on that content:
generic (one primitive, the row's pair, no family name), vector (the
division act alone, no root, no float) and local (the six reads and the
hold's rewrite). A world starts from the field at rest, never from zeros,
whose transient rings. Under [1, 1] the clamp's rest between periodic faces
is the uniform level, the count itself, no well and no mode there (the
source row's periodic problem at kappa = 0 has no rest at all); between open
faces the harmonic well.

THE START. The loop writes every held family at the load at its rest, the
fixed point of the family's line under the hold's rewrite, by one folder
found by its name, once before the first interval and never in it: on a
chain (one layer on two axes) the rise between the bodies' Nodes in one pass
in integers, the tridiagonal line of the same map; elsewhere the clamp
iterated. Generic (the row's pair), vector (the division act, no root),
local (the six reads and the rewrite); the cost is the load's.

### The velocity

Rule3 is translation-invariant, so the record's wave number k is conserved
where no pace gradient stands: the record's centre moves at its group
velocity v_g(k) exactly, bound or spreading. The count follows the record by
the count's line: with the record's norm c T the current across the body's
face is c T v_g per interval, so c v_g quanta cross per interval and the
count's centroid moves at v_g, exact up to the remainder. The well moves
with the count one quantum at a time, 1 / c_i of a Link, so the record is
never kicked by a whole Link; the leak of a hop of the whole well by one
Link, delta = 1 - <phi | X phi>^2 with X the shift by one Link, is 0.031 at
side 12 and 1000 per Node (0.021 at 500, 0.040 at 2000; 0.099 at side 6 and
2000; 0.38 at side 3 and 5000; 0.999 at one Node and 9000), and per Link of
travel delta / c = 3 x 10^-5 at side 12 and 1000: the bound norm, and with
it the velocity, falls by 3 x 10^-5 per Link there. A one-Node body of one
quantum binds nothing and is a free record: its velocity is v_g(k) with no
count to follow it.

The run beside these numbers (the cube of side 12 on [800, 1200] at 1000 per
Node at v = 1 / 3 on a periodic box, 10^4 intervals): the count's centroid
against v t, the slope v within the remainder; the share inside the cube
0.92 at the start, falling by at most 3 x 10^-5 per Link; the clock's period
2 pi / omega_b(k), 7.74 intervals at k = 0. A larger fall, or a slope that
drifts, names a missing law; the body's own numbers are never patched.

## What the law says of nature

### The postulates

1. The world is Nodes and Events. Space is the GameBoard; an Event is a wall
crossed by a remainder at a Node: a level stepped, a count moved, a click;
nothing else happens. 2. A Node holds bounded local information: its
NodeState, fixed in size, read from itself and its six neighbours; no read
beyond them, no list that grows with the world, nothing of the past kept.
Every physical update uses its own record and the six causally available
neighbours with fixed work and storage for a fixed set of families
(LOCALITY-1); a self-field estimated or subtracted from anything global is
forbidden, whatever the size of its final answer. 3. Consistency is local
and causal: an Event first changes its own Node and travels Link by Link,
one Link per interval, each Node updating on receipt under the same rule.
The one exception is the click: a record ends at once, whole, at the
detector. 4. The causal speed is one Link per interval, built in; every
other speed is a rational, a count of Links over a count of intervals. 5.
Every physical calculation is on bounded integers; there is no float, no
root and no draw in the law; a Node keeps only the law's own numbers: each
record's two levels and its remainder, the family's pair and the Node clock
from the content there. 6. A measurement is a detector's click, an action of
the law on the state: the record ends at the detector and the detector's own
record changes. Only a click is compared with nature or pinned as an
expectation; displays and the host's readings read state and write nothing.
7. The Inside is the GameBoard, where no one measures; the Outside is the
detectors and their clicks, the only thing claimed to represent nature.

### The constants

The speed of light is one Link per interval. The quantum of action is
one click, its energy the quantum's norm T of its family. Newton's
constant is not declared: a body of energy count s makes the level c(r)
= s times the reference flux over the distance r in Links, and the
level slows the clock by the potential Phi = -c / (2 Gamma), so

  G = (the reference flux) / (2 Gamma) per unit of energy count,

with the reference flux a number of the GameBoard's geometry (about 1.4 for
a cube of side 3) and the energy unit setting the mass of one unit of level.
A world at a smaller Gamma has stronger gravity per unit of content; the
ratios between rows carry G once and cancel it. The quantum of distance is
the Link, of time the interval; nothing between two Nodes or two intervals
is observed. The potential at a body's Nodes changes by G per unit of energy
count and never by less: the quantum of gravity is the click.

### The rows against nature

Each row is a detector's click on a declared world, read blind, with
U_b = c_b / (2 Gamma) the potential at the point named; the bands are
the rounding's, one Node of centroid or one interval, and the draw's
where counts are read.

(a) THE REDSHIFT: two clocks of one family at the levels c_1 and c_2; the ratio of their tick intervals is the root of (1 - 2 U_1 + 2 U_1^2) / (1 - 2 U_2 + 2 U_2^2), 1 - (U_1 - U_2) to first order.
(b) THE BENDING: a beam past a body at closest distance b, the centroid at a receiver L Links beyond shifted by 4 U_b L toward the body.
(c) THE DELAY: a round trip past the body, delayed by 4 U_b times the path's length within the well's reach.
(d) THE PERIHELION: an orbiting emitter at semi-axis a and eccentricity e advances 6 pi U_p per orbit with U_p the potential at a (1 - e^2).
(e) THE MOVING CLOCK: a body at velocity v has its tick lengthened by the dispersion's factor, 0.8146 against 1 / gamma = 0.8165 (gamma the Lorentz factor) at k = 0.18556 per Link, the GameBoard's own term inside the rows' bands.
(f) THE CHARGE: like signs a hill, unlike a hollow; a reader of charge q reads + q Lambda d in its pace and - q Lambda (**n** . **A**) div W on its vector part, so like charges moving together repel less.
(g) THE TWO SLITS: a giving body, a wall body with two openings d Links apart (its count above the mirror's of [the paces](#the-paces)) and a screen body L Links beyond carrying the sets in strips: the strips' shares of the clicks are the openings' interference at lambda_q, cos^2 (pi d y / (lambda_q L)) at the height y under one opening's envelope, the bright strips lambda_q L / d apart, to the first order in the GameBoard's anisotropy; the exact shares are the two arms' phases **k** . **r** with the wavevector set by cos k_x + cos k_y + cos k_z = 3 cos omega den / num at the record's rotation, a term that at lambda_q = 4 Links on d = 16 and L = 97 moves the second bright pair from 6 to 8.5 strips of 4 Nodes and falls below one strip at lambda_q = 16; the record's rows show it splitting at the openings and its parts meeting on the screen (GAMEBOARD).
(h) BELL: one giving of two records by [the pair-giver](#the-primitives), their pair angles phi_L and phi_R (0 and the declared sense), one residue u, a polariser body at each end set to a and b, two sets at each end, the polariser's own set offered before the far one: the outcome at an end is its own set exactly when u / V < sin^2 (a - phi) and the far set otherwise, a step function of the one u, so E(a, b) = 1 - 2 |sin^2 (a - phi_L) - sin^2 (b - phi_R)|, the marginals cos^2 (a - phi_L) and cos^2 (b - phi_R), and |S| <= 2 at every setting, four correlations of two step functions of one shared u, the local bound; at the settings 0, pi / 4 and pi / 8, 3 pi / 8 with the same sense E(0, pi / 8) = cos (pi / 4) and S = 2 exactly, against nature's cos 2(a - b) and 2 sqrt 2; a run above 2 is a finding, and no cell is tuned.
(j) DE BROGLIE'S FRINGES: (g) with a matter record given by a body of a lighter family: a giver of rotation omega_b radiates only a family whose free band holds it, num / (3 den) <= cos omega_b <= num / den (a bound mode's rotation lies above its own family's band, so no body radiates its own family); the record's wave number is the band's, cos omega_b = (num / (3 den)) (2 + cos k), its group velocity v = (num / (3 den)) sin k / sin omega_b, and to the second order k = omega_b v / c_m^2 with c_m^2 = omega_0 / (3 tan omega_0) the family's own light speed (0.2508 on [800, 1200]): de Broglie's law with the rest rotation as the mass; the strips' shares are (g)'s at lambda = 2 pi / k.
(k) THE TWO-QUBIT COMPUTER: one qubit is a record's two arms after the splitter of (l), its gates the splitter, a window body as a phase gate (the phase (k_in - k) l over a depth l, [the paces](#the-paces)) and the polariser; two qubits are the pair-giver's two records with one u, whose coincidences are (h)'s E; a controlled gate needs one record to turn another's phase, which the acts alone cannot (the theorem of the four acts) and a read can only through the pace: a target family reading the control family with the weight g_c has its pace wobble with the control's level, the first order averaging out over the control's rotation and the second order a hill of g_c^2 A^2 / (4 Gamma) over the overlap (A the control's amplitude), so the blind expectation is (h)'s E with that small phase, and a controlled phase of order one is a hypothesis under its own name, not in the law.
(l) MACH-ZEHNDER: a giving body, a splitter (a body of a count inside the record's band, one Node deep along the beam, its reflected share s the slab's from [the paces](#the-paces), one half at the count found by bisection), a mirror on each arm (a count above the mirror's), a second splitter and two sets: the shares of the clicks are 4 s (1 - s) cos^2 (Delta / 2) at the cross exit and one minus that at the straight exit, Delta = k (L_1 - L_2) the arms' phase difference, so at equal arms and s = 1 / 2 every click is at the cross exit; the record's rows show the two arms (GAMEBOARD).
(m) THE ROUND TRIP: a giver receding at v from a mirror at rest, its set on itself, giving every P intervals: the forward record's wave number solves Omega(k) + k v = omega_b (the giver's rotation seen from the GameBoard), the returned record has the same rotation and wave number, and the returned clicks come every P (u + v) / (u - v) intervals with u the group velocity at that k: the two-way Doppler ratio with the light's group velocity in place of c.
(n) SAGNAC: a giver with its set on itself moving at v along a ring of N Links (a periodic chain): one record's two arms return after N / (u + v) and N / (u - v) intervals, u the light's group velocity, so the set's clicks fall in two groups whose means differ by 2 N v / (u^2 - v^2), which is 4 A omega / u^2 for the ring's area A and angular speed omega to the first order in v / u (each arm's Doppler shift of k the second), and coincide at rest; a giver at rest on the ring reads one group at N / u.
(o) THE MOVING MASS: a body giving a lighter matter family (a row whose band holds the giver's rotation, (j)) toward a set L Links away: the record's quanta move at the count's line's velocity v = (num / (3 den)) sin k / sin omega_b, the set's clicks come L / v intervals after each giving, and the giver's momentum moves by 3 Q_unit P_body (L div lambda_q) div L per quantum given (the recoil); the record's rows show one packet at v (GAMEBOARD).
(p) THE MEDIUM'S DELAY: a light record through a window body of depth l (a count below the mirror's of [the paces](#the-paces)) is slowed inside to v_in = (p / Gamma)^2 sin k_in / (3 sin omega) with 1 - cos k_in = (Gamma / p)^2 (1 - cos k), the index v_g / v_in, and a set beyond reads the passage longer by l (1 / v_in - 1 / v_g), a round trip by twice that; through a window moving at w along the beam the record's wave number inside is matched at the moving face, omega - k w = omega_in - k_in w, and its speed inside is the band's group velocity at that k_in, not v_in + w; Fresnel's drag w (1 - v_in^2 / v_g^2) is nature's number beside it.
(q) DARK MATTER: a heavy body in a box and a light test body at the distance r on a circular orbit (v^2 = r a): the held field's rest outside the body is Laplace's ([1, 1]), c(r) = s x the reference flux / r falling to the faces' 0 (the open faces' images steepen it near a face), so a = (c_+ - c_-) / (Gamma D) falls as 1 / r^2 and v^2 as 1 / r, Kepler's fall-off, under the hold's write as a load and as a sum alike (the source inside, Laplace outside); the DETECTOR reads the orbit's period in the waits' phase as in (d); a flat v(r) is the finding that names a missing law.
(r) DARK ENERGY: a giver and two far sets on a long periodic chain over 10^5 intervals: Rule3 is translation-invariant, so a free record keeps its wave number and rotation exactly and the sets' mean click interval stays the giving's period P at every distance, the record's rows widening by the dispersion as the root of t while its count does not move (GAMEBOARD), the rounding's walk at most one unit of level per Node per interval; a mean interval growing with the distance is the finding.

A row outside its band is a finding: it names the missing law or the
defect, and no body's numbers are patched to meet it.

## What is open

1. Whether a body at rest jitters when its current's swing reaches T / 2: on sixteen Nodes the swing over 400 intervals is one percent of T / 2.
2. The loop does not carry the recoil yet: no click moves a body's
momentum in any shipped world (the folder stands, its store on L).
3. The self-source's cubic term: not in the engine, the line is the squares' sum alone.
4. The twist table's small angles: a triple with d at most 10^9 reaches no angle below 6.3 x 10^-5 radians.
