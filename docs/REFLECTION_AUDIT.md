# Spatial reflections of the existing signed Rule3 model

## Result

The existing coupling supports every orientation-reversing cubic spatial map
when accompanied by a suitable **uniform signed permutation of the 48
channels**, with an exact transformation of retained remainders. The scalar
law, coupling matrices, number of channels and runtime engine need no change.

For the current body signs (1,-1,1), channel permutations without sign changes
are insufficient. For each of the 24 improper spatial maps there are eight
support permutations. Each admits a consistent sign assignment, normalized
to +1 on source channel 0. Negating the entire assignment gives another valid
map. The tests also verify signed lifts for all eight body-sign choices.

There is an important distinction: the particular x-plane mirror lift chosen
below has order four on the full retained state. Applying it twice restores
the spatial position but leaves a nontrivial internal operation. It is not
an ordinary order-two action on the full state, nor a proof of a physical
parity representation for the project's proposed observables.

## Exact action

Let M be a signed permutation matrix on physical space with determinant -1,
such as M_x=diag(-1,1,1). Seek a permutation f of the 48 channels and signs
sigma_g in {-1,+1}, the same at every spatial site.

An address (x,g) maps to (M*x,f(g)), modulo the periodic board size. For a
positive sign retain (a,b,r). For a negative sign apply

    J(a,b,r)=(-a,-b,4-r+2*(r mod 2)).

The remainder transformation is

    0 <-> 4,  2 <-> 2,  1 <-> 5,  3 <-> 3.

It stays within 0,...,5, preserves parity and is involutive. In particular the
usual background (0,0,2) stays fixed, so the operation is compatible with the
sparse representation. The helper rejects uniform backgrounds not fixed by J;
the algebraic operation itself is defined on arbitrary full states.

In the previously derived mechanical coordinates

    q=b,   p=3*(b-a)+floor(r/2)-1,   epsilon=r mod 2,

J is simply (q,p,epsilon)->(-q,-p,epsilon).

## Coupling identities and proof of full-state covariance

Write pi_d(g) for the channel connected through direction d and w_d(g) for
its sign. The required identities are

    f(pi_d(g)) = pi_(M*d)(f(g))
    sigma_g*w_d(g) = w_(M*d)(f(g))*sigma_(pi_d(g)).

They imply that the input sum at the transformed channel is sigma_g times
the original input sum. If C_d is the original 48x48 coupling matrix and P is
the signed permutation matrix P[f(g),g]=sigma_g, the same identities read

    C_(M*d) P = P C_d.

The scalar rule is compatible with the negative input transformation exactly:

    Rule3(J(s),-u) = J(Rule3(s,u)).

To see this directly, write 2u+r=6*ell+r_next and epsilon=r mod 2. Since 2u
is even, r_next has the same epsilon. Then

    -2u + (4-r+2*epsilon)
      = 6*(-ell) + (4-r_next+2*epsilon).

The second term is already the unique allowed remainder in 0,...,5. Hence
the new quotient is -ell and both updated counters also change sign. No
approximation is involved. Applying this independently to all channels proves

    W T_M = T_M W

for every state, every board size with the declared periodic geometry, and
the verified coupling identities. Random finite-state tests supplement this
proof; they do not replace it.

## How the channel map was found

The six port permutations act transitively on the 48 channel labels. Choose
an image f(0). For each edge, the first identity forces the next channel's
image. A breadth-first traversal either determines the entire permutation
or finds a contradiction. Enumerating all 48 possible images of channel 0
therefore exhausts ALL uniform channel permutations, without trying 48!
independent possibilities.

For each surviving permutation, choose sigma_0=+1 and propagate the second
identity. A conflicting sign would reject the candidate. All eight surviving
support permutations admit consistent signs for every tested coupling choice.

`reflection_audit_results.json` saves an explicit x-mirror permutation and all
48 signs, together with the summary for all improper maps and coupling signs.
The implementation uses exact integers throughout.

## Applying the mirror twice

For the chosen x-mirror lift, f(0)=10 in the current fixed group enumeration.
Let z=-1 be the central group element (label 14) and Z its channel permutation.
The verified identities for body signs (1,-1,1) are

    f(f(g))=z*g
    sigma_g*sigma_(f(g))=-1.

Therefore

    T_Mx^2 = J_all Z,
    T_Mx^4 = identity.

J_all applies the sign/remainder reversal to every channel. Both J_all and Z
are already symmetries of the unchanged evolution. Their combination is
nontrivial on a general state. Merely calling this a physical spinor parity
operation would not establish its action on scalar, vector, tensor or spinor
observables. That identification and a coherent interpretation of the larger
generated symmetry group remain separate tasks.

Indeed none of the eight support permutations for the x-plane reflection is
an involution: four have order four and four order eight. Thus an ordinary
order-two full-state mirror is unavailable within this class of uniform
signed channel permutations. This statement does not exclude more general
nonlinear or position-dependent transformations.

## Why a naive mirror fails

On a side-7 board, prepare only channel 2 at position (0,0,0) with (a,b,r)=(0,3,2).
Use the current coupling signs (1,-1,1). Reflect x without changing the
internal channels, then advance once. At address (1,0,0,15) the result is
(0,1,2). Advancing first and then reflecting gives background (0,0,2) there;
the excitation appears in channel 34 instead. This disproves the naive mirror,
while the combined signed transform passes the exact identity above.

## Tests and reproduction

    python -m research.reflection_audit
    python -m unittest discover -s tests -p test_reflection_audit.py -v

Checks cover every improper spatial matrix and all possible images of channel
0, signed coupling identities for all 8 sign choices, all 48 existing lifted
rotations, all 6 remainders with large positive and negative counters, full
state evolution under the combined mirror, and its square and fourth power.

The distinction between 2O and the full spatial reflection group remains:
2O has 48 quaternionic elements over 24 proper rotations. A background source
for that algebraic distinction is John Baez's account:
https://math.ucr.edu/home/baez/week230.html . The new covariance result here is
derived from this repository's actual coupling; it is not a theorem imported
from that source.

Only research helpers, tests and documentation were added. A reflection is
used to transform a whole preparation or compare runs, never as an additional
step inside forward evolution.
