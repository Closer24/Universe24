"""Initial-state patterns; their names never select a runtime update rule."""
from .spec import Patch, Socket, TensorSpec
from universe24.core.group_2o import DIRECTIONS

PAIR = (0, 14)
PAIRS = {'O': (4, 0), 'N': (2, 2), 'R': (0, 4)}


def _pair_at(x=0):
    return tuple((x, 0, 0, g) for g in PAIR)


def _tensor(tensor):
    return TensorSpec() if tensor is None else tensor


def SignalSource(*, a=0, b=1, present=True, tensor=None):
    if type(a) is not int or type(b) is not int or type(present) is not bool:
        raise ValueError('Initial source counters are integers and presence is Boolean')
    aa, bb = (a, b) if present else (0, 0)
    return Patch('signal-source', {addr: (sign*aa, sign*bb, 2)
                  for addr, sign in zip(_pair_at(), (1, -1))}, tensor=_tensor(tensor),
                 ports={'signal': _pair_at()}, sources={'signal': _pair_at()},
                 evidence_domains=('Prepared paired disturbances; not established physical light.',))


def GuideSegment(*, start, stop, sockets=(), remainder_pair=(4, 0), tensor=None):
    if type(start) is not int or type(stop) is not int or start > stop:
        raise ValueError('Guide needs inclusive integer start <= stop')
    slots = tuple(sockets)
    if any(type(s) is not int or not start <= s <= stop for s in slots) or len(set(slots)) != len(slots):
        raise ValueError('Socket coordinates must be distinct and inside the guide')
    pair = tuple(remainder_pair)
    if len(pair) != 2:
        raise ValueError('Two channel remainders required')
    cells = {(x, 0, 0, g): (0, 0, r) for x in range(start, stop+1)
             if x not in slots for g, r in zip(PAIR, pair)}
    return Patch('guide', cells, tensor=_tensor(tensor),
                 ports={'start': _pair_at(start), 'end': _pair_at(stop)},
                 sockets=tuple(Socket('at-' + str(x), _pair_at(x)) for x in slots),
                 evidence_domains=('Only the registered source/receiver geometries have demonstrated behavior.',))


def Receiver(*, remainders=(4, 0), counters=((0, 0), (0, 0)), tensor=None):
    remainders, counters = tuple(remainders), tuple(tuple(v) for v in counters)
    if len(remainders) != 2 or len(counters) != 2 or any(len(v) != 2 for v in counters):
        raise ValueError('Receiver needs two counter pairs and two remainders')
    cells = {address: (*ab, r) for address, ab, r in zip(_pair_at(), counters, remainders)}
    readouts = tuple({'id': f'memory-{r0}-{r1}', 'label': f'Remainder pair ({r0}, {r1})',
                     'kind': 'all_equal', 'clauses': [
                         {'address': address, 'component': 'r', 'equals': str(r)}
                         for address, r in zip(_pair_at(), (r0, r1))]}
                    for r0, r1 in ((4, 0), (0, 4), (2, 4), (4, 2), (2, 2), (0, 0)))
    return Patch('receiver', cells, tensor=_tensor(tensor),
                 ports={'memory': _pair_at(), 'node': tuple((0,0,0,g) for g in range(48))},
                 readouts=readouts,
                 evidence_domains=('Clock/memory roles are passive interpretations of these same counters. '
                                   'Known finite two-arrival studies do not establish indefinite reuse.',))


def PairedArm(*, variant='O', direction=1, gate_pairs=None, length=6, tensor=None):
    if type(direction) is not int or direction not in (-1, 1) or variant not in PAIRS:
        raise ValueError('Paired arm needs direction +/-1 and variant O/N/R')
    if type(length) is not int or length < 3:
        raise ValueError('Paired arm length must be an integer >=3')
    pairs = (PAIRS[variant], PAIRS[variant]) if gate_pairs is None else tuple(tuple(p) for p in gate_pairs)
    if len(pairs) != 2 or any(len(p) != 2 for p in pairs):
        raise ValueError('Two exact remainder pairs required for sites 2 and 3')
    cells = {}
    for j in range(1, length+1):
        pair = pairs[j-2] if j in (2, 3) else PAIRS['O']
        for g, r in zip(PAIR, pair):
            cells[(direction*j, 0, 0, g)] = (0, 0, r)
    return Patch('paired-arm', cells, tensor=_tensor(tensor),
                 ports={'inlet': _pair_at(direction), 'outlet': tuple((direction*length, 0, 0, g) for g in range(48)),
                        'memory-2': _pair_at(direction*2), 'memory-3': _pair_at(direction*3)},
                 evidence_domains=('O/N/R paired study: +++ tensor, centered source, steps 6..40. '
                                   'Length six only in that evidence; other lengths/patterns need separate tests.',))


def GuidedPacketSource(*, present=True, tensor=None):
    """Four-site packet and retained transverse halo, supplied entirely at t=0.

    Requires a separately assembled periodic guide with remainder pair (0,4)
    and sockets at local x=0,1,2,3. Tested translation uses the +++ tensor.
    """
    if type(present) is not bool:
        raise ValueError('Initial packet presence must be Boolean')
    tensor = _tensor(tensor)
    cells = {}
    for x in range(4):
        a = (1 if x == 0 else -1 if x == 2 else 0) if present else 0
        b = (1 if x == 1 else -1 if x == 3 else 0) if present else 0
        cells[(x,0,0,0)] = (a,b,4)
        cells[(x,0,0,14)] = (-a,-b,0)
    for x in (1,2):
        for direction in range(2,6):
            dx,dy,dz = DIRECTIONS[direction]
            for g,sign in ((0,1),(14,-1)):
                address = (x+dx,dy,dz,tensor.ports[direction][g])
                value = (0,0,2-2*sign*tensor.weights[direction][g])
                if address in cells and cells[address] != value:
                    raise ValueError('Packet halo assignments conflict')
                cells[address] = value
    addresses = tuple((x,0,0,g) for x in range(4) for g in PAIR)
    return Patch('signal-source', cells, tensor=tensor,
                 ports={'packet': addresses, 'front': _pair_at(1)}, sources={'packet': addresses},
                 evidence_domains=('Guided packet: +++ tensor, full periodic (0,4) guide, L=5/17/31; '
                                   'exact whole-state +x translation through one period. '
                                   'Not established free-vacuum light or a waiting/confirmation device.',))
