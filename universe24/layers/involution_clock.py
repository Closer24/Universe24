"""Optional exact reversible routing circuit embedded in scalar Rule3.

This is a chosen fixed tensor, not a derivation of a circuit or physical law
from Rule3. No existing/default model is changed. Three active node channels
carry a retained Boolean control c and left/right data l,r. The local Fredkin
involution P and nearest-neighbour wire involution J are

    P(c,l,r) = (c, l+c*(r-l), r+c*(l-r)),
    J(c)_x=c_x, J(l)_x=r_(x-e), J(r)_x=l_(x+e).

P is an involution for c in {0,1}; J is an involution without a restriction on
data. Both preserve Boolean arrays and the number of data bits. Set

    u = (D/2)*(P(b)+J(b)), D=6Q, a_0=P(b_0), 0<=r_0<D.

The ONLY runtime operation remains Rule3. Since 2u is divisible by D, the
quotient is P(b)+J(b) and the remainder is unchanged. On a=P(b) the next b is
J(b), and the next a=J(next_b). On a=J(b) the next b is P(b), and next a=P(next_b).
Thus J,P alternate automatically in the retained two-time state; no phase
counter, scheduler, callback or extra update is needed. The reverse identities
give the same invariant union in reverse. The intersection of the two phase
graphs is harmless: P(b)=J(b) makes both descriptions agree on the next value.

Every Boolean initial b, with a=P(b) and an allowed remainder array, has an
exact bounded trajectory with Boolean a,b and constant remainders. On a finite
periodic board its trajectory is periodic, because the restricted evolution is
a bijection of a finite set. This is a theorem for this prepared sector, not a
stability assertion for arbitrary states of the full integer automaton.

For c=1 everywhere a right-channel pulse advances one site along +e every two
updates. At a site with c=0 the local swap is disabled, so an incoming pulse is
reflected by the next wire swap. The control is retained in the state; there is
no erasure of alternatives or quantum collapse. Mixed static controls make
fixed transmission/reflection circuits, not an optimizing choice mechanism.

All remainders remain fixed, hence every official click has class C0. Clicks
also record the two-time memory change, not just occupation of a moving bit.
This construction therefore does not require or derive C2 selection/collapse.
The control-dependent Fredkin terms are nonreciprocal and explicitly designated;
no Hamiltonian, energy, synchronization, gravity or quantum claim is made.
"""
from __future__ import annotations

from ..core.lattice import DIRECTIONS, ZERO
from ..core.tensor import GearType, Tensor


CONTROL_WHY = (
    "Optional Boolean Fredkin circuit: a retained control selects a local swap. "
    "Its own value is unchanged, so the control-dependent terms are deliberately "
    "nonreciprocal, not derivatives of a shared physical potential. "
    "The exact involution proof applies to the prepared binary-control sector."
)


def build_involution_clock(*, Q: int = 1, axis: int = 0,
                           namespace: str = "involution", spectators: int = 0) -> Tensor:
    """Build fixed polynomial data for the three-channel Fredkin/wire circuit.

    The channel order is control,left,right followed by explicit static
    spectators. ``axis`` chooses one spatial wire direction before the run;
    this circuit does not have full cube-rotation symmetry. All gears are
    node-stored, and every monomial has physical support on at most one edge.

    ``spectators=45`` produces 48 channels only by padding with P=J=identity.
    They are not a 2O group representation, and add no routing capability.
    Prepare those spectator channels with a=b, as required by a=P(b).

    Initial data must satisfy c in {0,1} and a=P(b) for the stated theorem.
    A convenient seed construction is a copy of b with left/right entries
    exchanged exactly at nodes whose control is one. No seed preparation or
    forward evolution is performed by this layer builder.
    """
    if type(Q) is not int or Q < 1:
        raise ValueError("Q must be a positive Python int")
    if type(axis) is not int or not 0 <= axis < 3:
        raise ValueError("axis must be 0, 1 or 2")
    if type(namespace) is not str or not namespace.isidentifier():
        raise ValueError("namespace must be a nonempty identifier")
    if type(spectators) is not int or spectators < 0:
        raise ValueError("spectators must be a non-negative Python int")
    c, left, right = (f"{namespace}.{name}" for name in ("control", "left", "right"))
    gears = [GearType(c, label="audit"), GearType(left), GearType(right)]
    half_D = 3 * Q
    e = DIRECTIONS[2 * axis]
    minus_e = tuple(-component for component in e)
    f = lambda gear, offset=ZERO: (gear, offset, "b")
    terms = [
        (c, 2 * half_D, (f(c),)),
        (left, half_D, (f(left),)),
        (left, half_D, (f(right, minus_e),)),
        (right, half_D, (f(right),)),
        (right, half_D, (f(left, e),)),
    ]
    for target, other in ((left, right), (right, left)):
        terms.extend([
            (target, half_D, (f(c), f(other)), {"designated_one_way": CONTROL_WHY}),
            (target, -half_D, (f(c), f(target)), {"designated_one_way": CONTROL_WHY}),
        ])
    for j in range(spectators):
        name = f"{namespace}.spectator{j:03d}"
        gears.append(GearType(name, label="audit"))
        terms.append((name, 2 * half_D, (f(name),)))
    return Tensor(gears, terms, Q=Q, strict_support=True)


__all__ = ["build_involution_clock"]
