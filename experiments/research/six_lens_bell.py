"""Independent read-only verification of saved Bell/cone audit records.

No imports from the Engine, its Bell scorer, or its quantum sampler. The
probability and counterfactual checks below use only exported records.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
from itertools import accumulate, combinations, product
import json
from pathlib import Path


CONTEXTS = tuple(product((0, 1), repeat=2))
SIGNS = (1, 1, 1, -1)


def signed_chsh(values):
    return sum(s*v for s, v in zip(SIGNS, values))


def evaluate_records(rows, reader):
    cells, accepted_sources = {}, {}
    for x, y in CONTEXTS:
        emitted = [r for r in rows if r['settings'] == [x, y]]
        kept = [r for r in emitted if reader != 'C2_coincidences_only'
                or all(d['C2'] for d in r['detectors'])]
        outcomes = []
        for row in kept:
            pair = []
            for d in row['detectors']:
                detected = d['click'] if reader == 'all_arrival_clicks' else d['C2']
                pair.append((1 if d['quotient'] >= 0 else -1) if detected else 1)
            outcomes.append(pair)
        n = len(outcomes)
        key = f'{x}{y}'
        cells[key] = {'emitted': len(emitted), 'included': n,
            'E': str(F(sum(a*b for a, b in outcomes), n)) if n else None,
            'mean_A': str(F(sum(a for a, b in outcomes), n)) if n else None,
            'mean_B': str(F(sum(b for a, b in outcomes), n)) if n else None}
        accepted_sources[key] = {k: str(F(v, n)) for k, v in
            Counter(r['source_label'] for r in kept).items()} if n else {}
    complete = all(c['E'] is not None for c in cells.values())
    score = abs(signed_chsh([F(cells[f'{x}{y}']['E']) for x, y in CONTEXTS])) if complete else None
    return {'cells': cells, 'S': str(score) if score is not None else None,
            'accepted_source_distributions': accepted_sources}


def independent_checks(directory):
    report = json.loads((directory/'report.json').read_text())
    records = json.loads((directory/'trials.json').read_text())
    results = {}
    for case, rows in records.items():
        readers = {name: evaluate_records(rows, name) for name in
            ('all_arrival_clicks', 'C2_all_emissions', 'C2_coincidences_only')}
        for name, values in readers.items():
            original = report['cases'][case]['readers'][name]
            assert values['S'] == original['S']
            for key, cell in values['cells'].items():
                assert all(original['cells'][key][k] == v for k, v in cell.items())
        vertices = {}
        for label in sorted({r['source_label'] for r in rows}):
            source_rows = [r for r in rows if r['source_label'] == label]
            assert len(source_rows) == 4
            assert len({r['source_triples_sha256'] for r in source_rows}) == 1
            for side, setting in CONTEXTS:
                local = [r['detectors'][side] for r in source_rows if r['settings'][side] == setting]
                assert local[0] == local[1]
            vertices[label] = {name: evaluate_records(source_rows, name)['S']
                              for name in ('all_arrival_clicks', 'C2_all_emissions')}
            assert all(F(s) <= 2 for s in vertices[label].values())
        results[case] = {'readers': readers, 'per_source_absolute_CHSH': vertices,
            'any_setting_independent_nonnegative_source_weighting_bounded_by_2': True}

    accepted = results['selection_stress']['readers']['C2_coincidences_only']['accepted_source_distributions']
    distances = {}
    for left, right in combinations(accepted, 2):
        support = set(accepted[left]) | set(accepted[right])
        distances[left+'-'+right] = str(sum(abs(F(accepted[left].get(k, '0'))
            -F(accepted[right].get(k, '0'))) for k in support)/2)
    assert set(distances.values()) == {'1'}

    # Different computation than the production mean-factor formula: explicitly
    # form every local Bernoulli product distribution and sum signed outcomes.
    grid = [F(i, 8) for i in range(9)]
    stochastic_max = F(0)
    for a0, a1, b0, b1 in product(grid, repeat=4):
        expectations = []
        for x, y in CONTEXTS:
            pa, pb = (a0, a1)[x], (b0, b1)[y]
            expectations.append(sum(a*b*(pa if a == 1 else 1-pa)
                *(pb if b == 1 else 1-pb) for a, b in product((-1, 1), repeat=2)))
        stochastic_max = max(stochastic_max, abs(signed_chsh(expectations)))
    assert stochastic_max == 2
    deterministic_scores = [signed_chsh([a[x]*b[y] for x, y in CONTEXTS])
        for a in product((-1, 1), repeat=2) for b in product((-1, 1), repeat=2)]
    assert set(deterministic_scores) == {-2, 2}

    # Independent singlet/Bloch-vector prediction, rather than multiplying
    # the integer matrices used by the benchmark.
    alice, bob = ((0, 1), (1, 0)), ((F(3, 5), F(4, 5)), (-F(3, 5), F(4, 5)))
    q = report['quantum_reference']
    for x, y in CONTEXTS:
        expected_E = -sum(a*b for a, b in zip(alice[x], bob[y]))
        expected_P = [(1+a*b*expected_E)/4 for a, b in product((1, -1), repeat=2)]
        cell = q['cells'][f'{x}{y}']
        assert expected_E == F(cell['E'])
        assert expected_P == list(map(F, cell['probabilities']))
        assert cell['mean_A'] == cell['mean_B'] == '0'
    replay = {key: Counter() for key in q['cells']}
    wins, total = 0, 0
    with gzip.open(directory/q['sample_log'], 'rt') as stream:
        for line in stream:
            row = json.loads(line)
            x, y = row['settings']
            key = f'{x}{y}'
            cell = q['cells'][key]
            assert 0 <= row['ticket'] < sum(cell['weights'])
            expected = next(i for i, upper in enumerate(accumulate(cell['weights'])) if row['ticket'] < upper)
            assert expected == row['outcome']
            assert row['measurement_microtick'] == report['measurement_deadline']
            replay[key][expected] += 1
            a, b = ((1, 1), (1, -1), (-1, 1), (-1, -1))[expected]
            wins += int(a*b == -(-1)**(x*y))
            total += 1
    for key, counts in replay.items():
        assert [counts[i] for i in range(4)] == q['cells'][key]['sample_counts']
    return {'baseline': '7d238e84a2167a4d3fe7bc7942da0cbf97bd29b2',
        'cases': results, 'selected_source_total_variation_between_settings': distances,
        'independent_local_stochastic_models': len(grid)**4,
        'independent_local_stochastic_CHSH_max': str(stochastic_max),
        'deterministic_response_tables': len(deterministic_scores),
        'deterministic_signed_CHSH_counts': dict(Counter(deterministic_scores)),
        'quantum_reference': {'independent_singlet_probabilities_match': True,
            'exact_CHSH': q['exact_CHSH'], 'sample_CHSH': q['sample_CHSH'],
            'all_tickets_replayed': total, 'sample_CHSH_game_wins': wins,
            'sample_win_fraction': str(F(wins, total)), 'local_game_expected_win_bound': '3/4',
            'physical_experiment_significance_claimed': False},
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = independent_checks(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'cases'}, indent=2))


if __name__ == '__main__':
    main()
