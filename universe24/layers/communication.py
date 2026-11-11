"""Local message transport compiled into the fixed-six tensor.

A prepared lane translates an integer payload one face edge per update. There
is no clock hand, age counter, scheduler callback or global state read. The
optional receiver reads the upstream message and reacts in the same update.
"""
from __future__ import annotations

from ..core.lattice import DIRECTIONS
from ..core.tensor import Block, GearType

LANES = ('px', 'nx', 'py', 'ny', 'pz', 'nz')
NAMESPACE = 'comm'
RECEIVER = 'ref.R00'
RECEPTION = ('Local incoming message drives the reference receiver; the receiver '
             'does not feed back into the transport lanes. No reciprocal force is claimed.')


def build_communication(*, name: str = NAMESPACE, receiver: str | None = RECEIVER,
                        label: str = 'official') -> Block:
    """Build six independent lanes and optional one-way local reception.

    u_d(x) = 3 [b_d(x-d) + b_d(x+d)]. On the prepared sector
    a_d(x)=b_d(x+d), Rule3 gives b'_d(x)=b_d(x-d), a'_d=b_d,
    r'_d=r_d. All integer payloads and legal remainders are allowed.
    The receiver gets u_receiver(x) += 3 sum_d b_d(x-d).
    """
    if type(name) is not str or not name.isidentifier():
        raise ValueError('communication namespace must be an identifier')
    if receiver is not None and (type(receiver) is not str or '.' not in receiver
                                 or receiver.startswith(name + '.')):
        raise ValueError('receiver must name a gear outside the communication namespace')
    terms = []
    for lane, direction in zip(LANES, DIRECTIONS):
        upstream = tuple(-v for v in direction)
        for offset in (upstream, direction):
            terms.append((lane, 3, ((lane, offset, 'b'),)))
        if receiver is not None:
            terms.append((receiver, 3, ((lane, upstream, 'b'),),
                          {'designated_one_way': RECEPTION}))
    return Block(tuple(GearType(lane, label) for lane in LANES), tuple(terms),
                 name=name, vacuum={lane: 0 for lane in LANES},
                 params={'kind': 'local-message-transport', 'receiver': receiver,
                         'directions': DIRECTIONS, 'prepared_speed': 'one edge per update'},
                 doc='Prepared integer messages between neighboring nodes; no per-node clock.')
