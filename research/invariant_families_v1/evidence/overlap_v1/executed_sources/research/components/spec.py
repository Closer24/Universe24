"""Immutable initial-data contracts. No evolution or runtime component objects."""
from dataclasses import dataclass, field
from types import MappingProxyType
from collections.abc import Mapping

from universe24 import Channel, Coupling, Cube
from universe24.core.state import channel

MODEL = 'universe24-2O-body-013-v1'


def freeze(value):
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, (tuple, list)):
        return tuple(freeze(item) for item in value)
    if value is None or type(value) in (str, int, bool, float):
        return value
    raise TypeError('Metadata must contain only data')


def plain(value):
    if isinstance(value, Mapping):
        return {key: plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    return value


def local_address(value):
    value = tuple(value)
    if len(value) != 4 or any(type(v) is not int for v in value) or not 0 <= value[3] < 48:
        raise ValueError('A local address needs three integer coordinates and channel 0..47')
    return value


def name(value):
    if not isinstance(value, str) or not value or len(value) > 200 or '.' in value:
        raise ValueError('Names must be nonempty text without dots, at most 200 characters')
    return value


def address_map(value):
    result = {}
    for key, addresses in dict(value).items():
        name(key)
        rows = tuple(local_address(a) for a in addresses)
        if not rows or len(set(rows)) != len(rows):
            raise ValueError('A named location must contain unique, nonempty addresses')
        result[key] = rows
    return MappingProxyType(result)


@dataclass(frozen=True, slots=True)
class TensorSpec:
    body_signs: tuple = (1, 1, 1)
    model_id: str = MODEL
    ports: tuple | None = None
    weights: tuple | None = None
    fingerprint: str | None = None

    def __post_init__(self):
        if self.model_id != MODEL:
            raise ValueError('Only the current body-013 model is supported')
        coupling = Coupling(tuple(self.body_signs))
        for field_name in ('ports', 'weights'):
            supplied = getattr(self, field_name)
            actual = getattr(coupling, field_name)
            if supplied is not None and tuple(tuple(row) for row in supplied) != actual:
                raise ValueError('Tensor ' + field_name + ' differ from the fixed reference tensor')
            object.__setattr__(self, field_name, actual)
        if self.fingerprint is not None and self.fingerprint != coupling.fingerprint:
            raise ValueError('Tensor fingerprint differs from the exact ports and weights')
        object.__setattr__(self, 'body_signs', coupling.body_signs)
        object.__setattr__(self, 'fingerprint', coupling.fingerprint)

    @classmethod
    def from_signs(cls, signs=(1, 1, 1)):
        return cls(tuple(signs))

    def data(self):
        return {key: plain(getattr(self, key)) for key in
                ('model_id', 'body_signs', 'ports', 'weights', 'fingerprint')}


@dataclass(frozen=True, slots=True)
class BoardSpec:
    side: int
    background: Channel = Channel(0, 0, 2)
    tensor: TensorSpec = field(default_factory=TensorSpec)

    def __post_init__(self):
        Cube(self.side)
        bg = channel(self.background)
        if bg.a or bg.b:
            raise ValueError('The declared background must be stationary: a=b=0')
        if not isinstance(self.tensor, TensorSpec):
            raise TypeError('Board tensor must be an exact TensorSpec')
        object.__setattr__(self, 'background', bg)


@dataclass(frozen=True, slots=True)
class Socket:
    name: str
    addresses: tuple
    allowed_kinds: tuple = ('signal-source', 'receiver')

    def __post_init__(self):
        name(self.name)
        addresses = tuple(local_address(a) for a in self.addresses)
        if not addresses or len(set(addresses)) != len(addresses):
            raise ValueError('Socket addresses must be unique and nonempty')
        kinds = tuple(self.allowed_kinds)
        if not kinds or any(not isinstance(k, str) or not k for k in kinds):
            raise ValueError('Socket filler kinds must be explicit')
        object.__setattr__(self, 'addresses', addresses)
        object.__setattr__(self, 'allowed_kinds', kinds)


@dataclass(frozen=True, slots=True)
class Patch:
    kind: str
    cells: object
    tensor: TensorSpec = field(default_factory=TensorSpec)
    background: Channel = Channel(0, 0, 2)
    ports: object = field(default_factory=dict)
    sources: object = field(default_factory=dict)
    sockets: tuple = ()
    readouts: tuple = ()
    evidence_domains: tuple = ()

    def __post_init__(self):
        name(self.kind)
        if not isinstance(self.tensor, TensorSpec):
            raise TypeError('Patch tensor must be an exact TensorSpec')
        bg = channel(self.background)
        if bg.a or bg.b:
            raise ValueError('Patch background must be stationary')
        rows = self.cells.items() if isinstance(self.cells, Mapping) else self.cells
        cells = []
        seen = set()
        for address, value in rows:
            address = local_address(address)
            if address in seen:
                raise ValueError('Duplicate address inside a raw patch')
            seen.add(address)
            cells.append((address, channel(value)))
        object.__setattr__(self, 'cells', tuple(sorted(cells)))
        object.__setattr__(self, 'background', bg)
        object.__setattr__(self, 'ports', address_map(self.ports))
        object.__setattr__(self, 'sources', address_map(self.sources))
        sockets = tuple(self.sockets)
        if any(not isinstance(s, Socket) for s in sockets) or len({s.name for s in sockets}) != len(sockets):
            raise ValueError('Sockets require distinct names and explicit contracts')
        if any(address in seen for socket in sockets for address in socket.addresses):
            raise ValueError('A socket must exclude its addresses from the patch assignments')
        if any(address not in seen for rows in self.sources.values() for address in rows):
            raise ValueError('A source must explicitly assign its own initial channels')
        object.__setattr__(self, 'sockets', sockets)
        readouts = []
        for item in self.readouts:
            if set(item) != {'id', 'label', 'kind', 'clauses'} or item['kind'] != 'all_equal':
                raise ValueError('Patch readouts use only passive all_equal predicates')
            name(item['id'])
            clauses = []
            for clause in item['clauses']:
                if set(clause) != {'address', 'component', 'equals'} or clause['component'] not in ('a', 'b', 'r'):
                    raise ValueError('Invalid passive readout clause')
                clauses.append({**clause, 'address': local_address(clause['address'])})
            if not clauses:
                raise ValueError('A readout needs at least one clause')
            readouts.append({**item, 'clauses': clauses})
        if len({r['id'] for r in readouts}) != len(readouts):
            raise ValueError('Duplicate patch readout ID')
        object.__setattr__(self, 'readouts', freeze(readouts))
        object.__setattr__(self, 'evidence_domains', freeze(self.evidence_domains))


@dataclass(frozen=True, slots=True)
class Placement:
    patch: Patch
    at: tuple
    name: str
    orientation: int = 0
    wrap: bool = False

    def __post_init__(self):
        if not isinstance(self.patch, Patch):
            raise TypeError('Only a data-only Patch can be placed')
        name(self.name)
        at = tuple(self.at)
        if len(at) != 3 or any(type(v) is not int for v in at):
            raise ValueError('Placement requires three exact integer coordinates')
        if type(self.orientation) is not int or not 0 <= self.orientation < 48:
            raise ValueError('Orientation must be an explicit 2O lift label in 0..47')
        if type(self.wrap) is not bool:
            raise ValueError('Wrapping must be explicitly Boolean')
        object.__setattr__(self, 'at', at)


def place(patch, *, at, name, orientation=0, wrap=False):
    return Placement(patch, tuple(at), name, orientation, wrap)
