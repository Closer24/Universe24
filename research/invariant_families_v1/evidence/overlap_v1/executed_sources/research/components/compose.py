"""Strict one-time assembly; all runtime evolution stays in the reference engine."""
from dataclasses import dataclass

from universe24 import Coupling, Cube, Engine, State
from universe24.core.group_2o import group, rotate
from .spec import BoardSpec, Placement, freeze, plain


@dataclass(frozen=True, slots=True)
class PreparedBoard:
    engine: Engine
    initial: State
    ports: object
    sources: object
    readouts: tuple
    manifest: object


def finalize(board, placements):
    if not isinstance(board, BoardSpec):
        raise TypeError('Expected BoardSpec')
    placements = tuple(placements)
    if any(not isinstance(p, Placement) for p in placements):
        raise TypeError('Only immutable placements are accepted')
    if len({p.name for p in placements}) != len(placements):
        raise ValueError('Placement names must be unique')
    cube = Cube(board.side)
    algebra = group()
    cells, writers, ports, sources, source_owner = {}, {}, {}, {}, {}
    sockets, readouts, records = [], [], []
    for p in sorted(placements, key=lambda item: item.name):
        patch = p.patch
        if patch.tensor != board.tensor:
            raise ValueError('Tensor conflict: every patch must use the same complete tensor')
        if patch.background != board.background:
            raise ValueError('Background conflict between patch and board')
        def transform(address):
            xyz = rotate(algebra.rotations[p.orientation], address[:3])
            xyz = tuple(v + offset for v, offset in zip(xyz, p.at))
            if p.wrap:
                xyz = tuple(v % board.side for v in xyz)
            return cube.validate_address((*xyz, algebra.multiplication[p.orientation][address[3]]))
        address_universe = {a for a, _ in patch.cells}
        address_universe.update(a for addresses in patch.ports.values() for a in addresses)
        address_universe.update(a for addresses in patch.sources.values() for a in addresses)
        address_universe.update(a for socket in patch.sockets for a in socket.addresses)
        address_universe.update(c['address'] for r in patch.readouts for c in r['clauses'])
        transformed = {a: transform(a) for a in address_universe}
        if len(set(transformed.values())) != len(transformed):
            raise ValueError('Placement wraps distinct local addresses onto the same channel')
        assignments = []
        for local, triple in patch.cells:
            address = transformed[local]
            if address in cells and cells[address] != triple:
                raise ValueError(f'Initial-state conflict at {address}; no overwrite or addition is allowed')
            cells[address] = triple
            writers.setdefault(address, []).append((p.name, patch.kind))
            assignments.append([*address, *triple])
        for key, addresses in patch.ports.items():
            ports[p.name + '.' + key] = tuple(transformed[a] for a in addresses)
        for key, addresses in patch.sources.items():
            identifier = p.name + '.' + key
            moved = tuple(transformed[a] for a in addresses)
            for address in moved:
                if address in source_owner:
                    raise ValueError('Independent sources alias the same initial address')
                source_owner[address] = identifier
            sources[identifier] = moved
        for socket in patch.sockets:
            sockets.append((p.name, socket.name, tuple(transformed[a] for a in socket.addresses), socket.allowed_kinds))
        for readout in patch.readouts:
            item = plain(readout)
            item['id'] = p.name + '.' + item['id']
            item['label'] = p.name + ': ' + item['label']
            for clause in item['clauses']:
                clause['address'] = list(transformed[tuple(clause['address'])])
            readouts.append(item)
        records.append({'name': p.name, 'kind': patch.kind, 'at': p.at,
                        'orientation_2o': p.orientation, 'explicit_wrap': p.wrap,
                        'raw_assignments': assignments, 'evidence_domains': patch.evidence_domains})
    for owner, label, addresses, allowed in sockets:
        for address in addresses:
            candidates = writers.get(address, [])
            if not any(writer != owner and kind in allowed for writer, kind in candidates):
                raise ValueError(f'Unfilled or incompatible socket {owner}.{label} at {address}')
    coupling = Coupling(board.tensor.body_signs)
    if (coupling.ports, coupling.weights, coupling.fingerprint) != (board.tensor.ports, board.tensor.weights, board.tensor.fingerprint):
        raise ValueError('Final tensor differs from its validated contract')
    manifest = {'format': 'universe24-assembly-v1', 'side': board.side,
                'background': board.background, 'tensor': board.tensor.data(),
                'components': records, 'ports': ports, 'sources': sources,
                'raw_assignments': [[*address, *value] for address, value in sorted(cells.items())],
                'assignment_owners': [{'address': address, 'owners': owner} for address, owner in sorted(writers.items())],
                'sockets': [{'owner': owner, 'name': label, 'addresses': addresses, 'allowed_kinds': allowed}
                            for owner, label, addresses, allowed in sockets],
                'assembly_valid': True, 'behavior_verified_by_assembly': False,
                'runtime_callbacks': False}
    return PreparedBoard(Engine(coupling), State(cube, board.background, cells),
                         freeze(ports), freeze(sources), freeze(readouts), freeze(manifest))
