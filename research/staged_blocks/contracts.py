"""Declarative research contracts and pure observers; never an evolution rule."""
from __future__ import annotations

import json
from pathlib import Path

from research.components.spec import freeze, local_address, plain
from universe24.core.state import channel
from universe24.observation import classify

HERE = Path(__file__).resolve().parent
STATUSES = frozenset({'proven', 'prepared', 'observed', 'search', 'not_demonstrated'})
CLAIMABLE = frozenset({'proven', 'observed'})


def load_catalog(path=None):
    """Return a fresh, checked catalog; changing metadata never changes a board."""
    data = json.loads(Path(path or HERE / 'stages.json').read_text())
    if data.get('format') != 'universe24-staged-contracts-v1':
        raise ValueError('Unsupported stage catalog format')
    for collection in ('blocks', 'stages'):
        rows = data.get(collection)
        if not isinstance(rows, list) or not rows:
            raise ValueError(f'{collection} must be a nonempty list')
        identifiers = [row.get('id') for row in rows]
        if any(not isinstance(item, str) or not item for item in identifiers) or len(set(identifiers)) != len(identifiers):
            raise ValueError(f'{collection} IDs must be unique nonempty text')
        for row in rows:
            if row.get('status') not in STATUSES:
                raise ValueError(f"Unknown status for {row['id']}")
            if not row.get('scope') or not isinstance(row.get('evidence'), list):
                raise ValueError(f"Scope and evidence are required for {row['id']}")
            if row['status'] in CLAIMABLE and not row['evidence']:
                raise ValueError(f"A claimable status needs evidence: {row['id']}")
    stages = {row['id']: row for row in data['stages']}
    visited, active = set(), set()

    def visit(identifier):
        if identifier not in stages:
            raise ValueError(f'Unknown prerequisite: {identifier}')
        if identifier in active:
            raise ValueError(f'Stage dependency cycle at {identifier}')
        if identifier in visited:
            return
        active.add(identifier)
        dependencies = stages[identifier].get('requires')
        if not isinstance(dependencies, list) or len(set(dependencies)) != len(dependencies):
            raise ValueError(f'Prerequisites must be a distinct list: {identifier}')
        alternatives = stages[identifier].get('requires_any', [])
        if not isinstance(alternatives, list) or len(set(alternatives)) != len(alternatives):
            raise ValueError(f'Alternative prerequisites must be a distinct list: {identifier}')
        for predecessor in dependencies + alternatives:
            visit(predecessor)
        active.remove(identifier)
        visited.add(identifier)

    for identifier in stages:
        visit(identifier)
    return data


def stage_report(stage_id, *, purpose='investigate', catalog=None):
    """Report scientific claim eligibility; investigations remain runnable."""
    if purpose not in {'investigate', 'claim', 'deploy'}:
        raise ValueError('Purpose must be investigate, claim or deploy')
    catalog = load_catalog() if catalog is None else catalog
    stages = {row['id']: row for row in catalog['stages']}
    if stage_id not in stages:
        raise ValueError(f'Unknown stage: {stage_id}')
    def inspect(identifier, ancestors=()):
        if identifier not in stages or identifier in ancestors:
            raise ValueError('Unknown or cyclic stage prerequisite: ' + identifier)
        row = stages[identifier]
        blockers = []
        for predecessor in row['requires']:
            blockers.extend(inspect(predecessor, (*ancestors, identifier)))
        alternatives = row.get('requires_any', [])
        alternatives_checked = [(predecessor, inspect(predecessor, (*ancestors, identifier)))
                                for predecessor in alternatives]
        if alternatives_checked and all(issues for _, issues in alternatives_checked):
            blockers.append({'stage': identifier, 'status': row['status'],
                             'reason': 'At least one alternative contract must be accepted',
                             'alternatives': [{'stage': name, 'blockers': issues} for name, issues in alternatives_checked]})
        if row['status'] not in CLAIMABLE or not row['evidence']:
            blockers.append({'stage': identifier, 'status': row['status'],
                             'reason': 'The stated capability has no accepted evidence in this catalog'})
        return blockers

    blockers = inspect(stage_id)
    return {'stage': stage_id, 'status': stages[stage_id]['status'], 'purpose': purpose,
            'allowed': purpose == 'investigate' or not blockers,
            'claim_ready': not blockers, 'blockers': blockers,
            'scope': stages[stage_id]['scope'], 'runtime_controller': False,
            'investigation_does_not_promote_status': True}


def require_stage(stage_id, *, purpose='claim'):
    report = stage_report(stage_id, purpose=purpose)
    if not report['allowed']:
        names = ', '.join(item['stage'] for item in report['blockers'])
        raise ValueError(f'{purpose} blocked for {stage_id}; unmet contracts: {names}')
    return report


def _rows(cells):
    items = cells.items() if hasattr(cells, 'items') else cells
    rows, seen = [], set()
    for address, values in items:
        address = local_address(address)
        if address in seen:
            raise ValueError(f'Duplicate observer address: {address}')
        seen.add(address)
        rows.append([*address, *channel(values)])
    if not rows:
        raise ValueError('An observer must inspect at least one channel')
    return sorted(rows)


def state_observer(cells):
    """Freeze exact full triples, including explicitly requested background cells."""
    return freeze({'kind': 'exact_state', 'cells': _rows(cells), 'passive': True})


def orbit_observer(phases):
    """Freeze an ordered local orbit; phase matching alone is not capture evidence."""
    phases = [_rows(phase) for phase in phases]
    if not phases:
        raise ValueError('An orbit requires at least one explicit phase')
    addresses = [row[:4] for row in phases[0]]
    if any([row[:4] for row in phase] != addresses for phase in phases):
        raise ValueError('Every orbit phase must cover the identical full address set')
    if len({json.dumps(phase) for phase in phases}) != len(phases):
        raise ValueError('Orbit phases must be distinct; use the minimal period')
    return freeze({'kind': 'orbit', 'phases': phases, 'passive': True})


def click_observer(addresses):
    addresses = tuple(local_address(address) for address in addresses)
    if not addresses or len(set(addresses)) != len(addresses):
        raise ValueError('Click addresses must be nonempty and distinct')
    return freeze({'kind': 'all_arithmetic_C', 'addresses': sorted(addresses),
                   'classes': (0, 1, 2), 'passive': True})


def observe_states(observer, states):
    """Read retained states only. No engine, callbacks, filters or state mutation."""
    spec, states = plain(observer), tuple(states)
    if not states:
        raise ValueError('At least one complete retained state is required')
    if any(state.cube != states[0].cube or state.background != states[0].background for state in states):
        raise ValueError('All observed states must use the same board and background')
    if spec.get('passive') is not True:
        raise ValueError('Only passive registered observations are supported')

    def matches(state, rows):
        return all(tuple(state.at(tuple(row[:4]))) == tuple(row[4:]) for row in rows)

    if spec['kind'] == 'exact_state':
        return {'matches': [matches(state, spec['cells']) for state in states]}
    if spec['kind'] == 'orbit':
        indices = [next((i for i, phase in enumerate(spec['phases']) if matches(state, phase)), None)
                   for state in states]
        advance = [a is not None and b == (a + 1) % len(spec['phases'])
                   for a, b in zip(indices, indices[1:])]
        return {'phase_indices': indices, 'correct_phase_transitions': advance,
                'matches_entire_interval': all(i is not None for i in indices) and all(advance)}
    if spec['kind'] == 'all_arithmetic_C' and spec.get('classes') == [0, 1, 2]:
        events = []
        for t, (before, after) in enumerate(zip(states, states[1:]), start=1):
            for address in spec['addresses']:
                event = classify(before.at(tuple(address)), after.at(tuple(address)))
                if event is not None:
                    kind, quotient = event
                    events.append({'step': t, 'address': address, 'kind': kind,
                                   'quotient': str(quotient)})
        return {'events': events, 'classes_retained': [0, 1, 2]}
    raise ValueError('Unsupported registered observer')
