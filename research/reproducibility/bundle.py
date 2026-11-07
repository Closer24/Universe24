"""Versioned JSON bundles and exact, deterministic comparisons (stdlib only)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def loads_strict(text):
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError(f'duplicate JSON member: {key}')
            obj[key] = value
        return obj
    return json.loads(text, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def read_json(path):
    return loads_strict(Path(path).read_text(encoding='utf-8'))

def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write('\n')


def validate(value, schema, at='$'):
    """Validate the documented closed subset used by our JSON schemas.

    This is not a general JSON Schema engine. Reject unsupported schema keywords
    rather than silently skipping constraints. No automatic schema migration.
    """
    known = {'$schema', '$id', 'title', 'description', 'type', 'properties',
             'required', 'additionalProperties', 'items', 'minItems', 'maxItems',
             'enum', 'const', 'minimum', 'maximum', 'minLength', 'pattern'}
    if set(schema) - known:
        raise ValueError(f'{at}: unsupported schema keywords {set(schema)-known}')
    types = {'object': lambda x: type(x) is dict, 'array': lambda x: type(x) is list,
             'integer': lambda x: type(x) is int, 'number': lambda x: type(x) in (int, float),
             'string': lambda x: type(x) is str, 'boolean': lambda x: type(x) is bool,
             'null': lambda x: x is None}
    if 'type' in schema and not types[schema['type']](value):
        raise ValueError(f'{at}: expected {schema["type"]}')
    if 'enum' in schema and not any(type(value) is type(x) and value == x for x in schema['enum']):
        raise ValueError(f'{at}: value outside enum')
    if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
        raise ValueError(f'{at}: wrong constant/version')
    if type(value) is dict:
        missing = set(schema.get('required', [])) - value.keys()
        if missing:
            raise ValueError(f'{at}: missing {sorted(missing)}')
        properties = schema.get('properties', {})
        for key, item in value.items():
            child = properties.get(key, schema.get('additionalProperties', True))
            if child is False:
                raise ValueError(f'{at}: unknown field {key}')
            if type(child) is dict:
                validate(item, child, f'{at}.{key}')
    if type(value) is list:
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', float('inf')):
            raise ValueError(f'{at}: array length')
        for i, item in enumerate(value):
            if 'items' in schema:
                validate(item, schema['items'], f'{at}[{i}]')
    if type(value) in (int, float):
        if value < schema.get('minimum', -float('inf')) or value > schema.get('maximum', float('inf')):
            raise ValueError(f'{at}: numeric range')
    if type(value) is str:
        if len(value) < schema.get('minLength', 0):
            raise ValueError(f'{at}: short string')
        if 'pattern' in schema and re.fullmatch(schema['pattern'], value) is None:
            raise ValueError(f'{at}: pattern mismatch')
    return value


def validate_named(value, name):
    validate(value, read_json(ROOT / 'research' / 'schemas' / f'{name}.schema.json'))
    if name == 'protocol':
        ids = [case['id'] for case in value['cases']]
        if len(ids) != len(set(ids)):
            raise ValueError('Duplicate protocol case IDs')
        for case in value['cases']:
            path = Path(case['config'])
            if path.is_absolute() or '..' in path.parts:
                raise ValueError('Config must be a repository-relative path')
            if case['expected_steps'] < case['expected_first_return']:
                raise ValueError('Observation window cannot test the claimed period')
    if name == 'result':
        for case in value['cases']:
            if case['pass'] and not (type(case['first_full_state_return']) is int
                    and case['first_full_state_return'] == case['expected_first_return']
                    and case['final_equals_initial'] and case['full_state_inverse_pass']):
                raise ValueError('Contradictory passed example')
        if value['execution_status'] == 'error' and not value['errors']:
            raise ValueError('Error result requires an error explanation')
        if value['implementation_status'] == 'passed':
            conditions = [value['execution_status'] == 'completed', not value['errors'],
                          bool(value['cases']), all(c.get('pass') is True for c in value['cases']),
                          value['reflection_certificate_equal'] is True,
                          value['negative_claim_result'].get('implementation_check_pass') is True]
            if value['scope'] == 'full':
                suite = value['suite']
                conditions += [suite.get('executed') is True, suite.get('pass') is True,
                               type(suite.get('returncode')) is int and suite['returncode'] == 0,
                               type(suite.get('test_count')) is int and suite['test_count'] > 0]
            if not all(conditions):
                raise ValueError('Contradictory or incomplete passed result')
    return value


def first_difference(expected, actual, at='$'):
    """Return first deterministic structural difference, not just a hash mismatch."""
    if type(expected) is not type(actual):
        return {'path': at, 'expected': expected, 'actual': actual}
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            return {'path': at, 'expected_keys': sorted(expected), 'actual_keys': sorted(actual)}
        for key in sorted(expected):
            difference = first_difference(expected[key], actual[key], f'{at}.{key}')
            if difference is not None:
                return difference
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            return {'path': at, 'expected_length': len(expected), 'actual_length': len(actual)}
        for i, (x, y) in enumerate(zip(expected, actual)):
            difference = first_difference(x, y, f'{at}[{i}]')
            if difference is not None:
                return difference
    elif expected != actual:
        return {'path': at, 'expected': expected, 'actual': actual}
    return None


def compare_bundles(left, right, experiments_only=False):
    """Compare evidence outputs, excluding only explicitly nondeterministic provenance."""
    left, right = Path(left), Path(right)
    # Code/input identity must match; environment/checkout metadata and runtime may differ.
    lm = validate_named(read_json(left / 'manifest.json'), 'manifest')
    rm = validate_named(read_json(right / 'manifest.json'), 'manifest')
    for key in ('engine_commit', 'protocol_sha256', 'source_sha256', 'coupling_fingerprints'):
        difference = first_difference(lm[key], rm[key])
        if difference:
            return {'file': 'manifest.json', 'field': key, **difference}
    names = ('protocol.json', 'result.json')
    for name in names:
        kind = name.split('.')[0]
        a = validate_named(read_json(left / name), kind)
        b = validate_named(read_json(right / name), kind)
        if experiments_only and name == 'result.json':
            a = {k: v for k, v in a.items() if k not in ('scope', 'suite')}
            b = {k: v for k, v in b.items() if k not in ('scope', 'suite')}
        difference = first_difference(a, b)
        if difference:
            return {'file': name, **difference}
    cases = [item['id'] for item in read_json(left / 'protocol.json')['cases']]
    for case in cases:
        for name in ('input.json', 'initial.json', 'final.json', 'result.json'):
            relative = f'cases/{case}/{name}'
            difference = first_difference(read_json(left / relative), read_json(right / relative))
            if difference:
                return {'file': relative, **difference}
        relative = f'cases/{case}/trace.jsonl'
        x = [loads_strict(row) for row in (left / relative).read_text().splitlines()]
        y = [loads_strict(row) for row in (right / relative).read_text().splitlines()]
        difference = first_difference(x, y)
        if difference:
            return {'file': relative, **difference}
    return None
