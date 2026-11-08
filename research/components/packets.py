"""Complete initial packet preparations and explicit passive remainder hardware."""
from universe24.core.group_2o import DIRECTIONS
from .spec import Patch, Socket
from .clocks import _positive_tensor, _boolean, _integer

REGISTER_ADDRESSES = tuple((x, -1, 0, g) for x in (1, 2) for g in (13, 45))


def EvenPacketSource(*, present=True, tensor=None):
    """Corrected even +X packet on a complete (0,0) remainder guide.

    ``present=False`` is true absence: guide remainder zero and transverse
    background remainder two. It differs from legacy GuidedPacketSource's
    counter-only mask. All preparations happen before the first native step.
    """
    _boolean(present, 'present')
    tensor = _positive_tensor(tensor)
    cells = {}
    for x, (a, b) in enumerate(((1, 0), (0, 1), (-1, 0), (0, -1))):
        for g in (0, 14):
            cells[x, 0, 0, g] = (a if present else 0, b if present else 0, 4 if present else 0)
    for x in (1, 2):
        for d in range(2, 6):
            dx, dy, dz = DIRECTIONS[d]
            for g in (0, 14):
                cells[x + dx, dy, dz, tensor.ports[d][g]] = (0, 0, 0 if present else 2)
    core = tuple((x, 0, 0, g) for x in range(4) for g in (0, 14))
    return Patch('signal-source', cells, tensor=tensor, ports={'packet': core},
                 sources={'packet': core}, evidence_domains=(
                     'Exact prepared even packet on the +++ periodic (0,0) guide. '
                     'Whole packet/halo absence when present=False; no photon identification.',))


def RemainderTarget(*, remainder=0, tensor=None):
    """Twelve complete resting sites; a two-site, four-channel target at the center."""
    tensor = _positive_tensor(tensor)
    _integer(remainder, range(6), 'remainder')
    centers = {(0, 0, 0), (1, 0, 0)}
    nodes = centers | {tuple(x[i] + d[i] for i in range(3))
                       for x in centers for d in DIRECTIONS}
    cells = {(*x, g): (0, 0, 0 if x[1:] == (1, 0) and g in (0, 14) else 2)
             for x in nodes for g in range(48)}
    core = tuple((*x, g) for x in sorted(centers) for g in (13, 45))
    cells.update({a: (0, 0, remainder) for a in core})
    return Patch('passive-remainder-target', cells, tensor=tensor,
                 ports={'core': core, 'region': tuple(sorted(cells))},
                 evidence_domains=('Initial resting hardware only; no generic detector or memory guarantee.',))


def RegisterWriter(*, present=True, tensor=None):
    """Even packet with four explicit sockets owned by SourceOverlapRegister.

    These sockets coincide physically with the packet's original transverse
    remainder halo. Different ownership does not imply disjoint preparations.
    """
    packet = EvenPacketSource(present=present, tensor=tensor)
    cells = {a: v for a, v in packet.cells if a not in REGISTER_ADDRESSES}
    return Patch('signal-source', cells, tensor=packet.tensor, ports=packet.ports,
                 sources=packet.sources,
                 sockets=(Socket('register', REGISTER_ADDRESSES, ('receiver',)),),
                 evidence_domains=('Source-overlap register clearing, not remote writing. '
                                   'Absent writer retains the separately owned register hardware.',))


def SourceOverlapRegister(*, tensor=None):
    """Four resting r0 addresses shared with a corrected writer's initial halo."""
    tensor = _positive_tensor(tensor)
    return Patch('receiver', {a: (0, 0, 0) for a in REGISTER_ADDRESSES}, tensor=tensor,
                 ports={'core': REGISTER_ADDRESSES}, evidence_domains=(
                     'Departure of the initially overlapping writer can clear r0 to r2. '
                     'A delayed orthogonal read distinguishes them in registered geometries only.',))
