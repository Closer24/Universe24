"""Behavioral boundaries for new initial-only family components."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from research.components import (BoardSpec, TensorSpec, Patch, GuideSegment, place, finalize,
                                 LocalizedSixClock, CompactFiveClock, CooperativeClockPair,
                                 EvenPacketSource, RegisterWriter, SourceOverlapRegister,
                                 assemble_scatterer, assemble_remainder_register)
from research.experiments.run import assemble
from research.component_families.verify import inventory, load_case, verify_case, EVIDENCE
from research.component_families.observations import translated, expected_register_checks, validate_register_checks


class FamilyComponentsTests(unittest.TestCase):
    def test_six_clock_all_phases_remainders_and_halo_parities(self):
        # Independent scalar orbit + halo accumulated input; compare every full state.
        phases = ((0, 1), (1, 1), (1, 0), (0, -1), (-1, -1), (-1, 0))
        for phase, (a0, b0) in enumerate(phases):
            for remainder in range(6):
                for parity in range(2):
                    p = finalize(BoardSpec(7), [place(LocalizedSixClock(
                        phase=phase, core_remainder=remainder, halo_parity=parity), at=(2, 2, 2), name='clock')])
                    state, a, b = p.initial, a0, b0
                    halo = {addr: p.initial.at(addr).r for addr in p.ports['clock.halo']}
                    for _ in range(6):
                        self.assertTrue(all(state.at(addr) == (a, b, remainder) for addr in p.ports['clock.core']))
                        self.assertTrue(all(state.at(addr) == (0, 0, r) for addr, r in halo.items()))
                        halo = {addr: r + 2 * b for addr, r in halo.items()}
                        a, b = b, b - a
                        state = p.engine.advance(state)
                    self.assertEqual(state, p.initial)

    def test_five_clock_full_orbits_and_conjugation(self):
        expected = {'dimer': ((0, 1, 4), (1, 1, 0), (1, -1, 2), (-1, -1, 0), (-1, 0, 4)),
                    'plaquette': ((0, 1, 2), (1, 1, 0), (1, -1, 4), (-1, -1, 0), (-1, 0, 2))}
        halo = (0, 2, 4, 2, 0)
        for shape, orbit in expected.items():
            for phase in range(5):
                for conjugated in (False, True):
                    p = finalize(BoardSpec(7), [place(CompactFiveClock(shape=shape, phase=phase,
                        conjugated=conjugated), at=(2, 2, 2), name='clock')])
                    state = p.initial
                    transform = lambda v: (-v[0], -v[1], 4 - v[2] + 2 * (v[2] % 2)) if conjugated else v
                    for t in range(5):
                        k = (phase + t) % 5
                        self.assertTrue(all(state.at(a) == transform(orbit[k]) for a in p.ports['clock.core']))
                        self.assertTrue(all(state.at(a) == transform((0, 0, halo[k])) for a in p.ports['clock.halo']))
                        state = p.engine.advance(state)
                    self.assertEqual(state, p.initial)

    def test_shared_halo_requires_explicit_joint_preparation(self):
        with self.assertRaises(ValueError):
            finalize(BoardSpec(15), [place(LocalizedSixClock(), at=(4, 4, 4), name='first'),
                                    place(LocalizedSixClock(phase=3), at=(7, 4, 4), name='second')])
        for first in (False, True):
            for second in (False, True):
                p = finalize(BoardSpec(15), [place(CooperativeClockPair(first_active=first,
                    second_active=second), at=(4, 4, 4), name='pair')])
                states = list(p.engine.evolve(p.initial, 6))
                if first == second:
                    self.assertEqual(states[6], states[0])
                else:
                    self.assertTrue(any(states[2].at(a).b for a in p.ports['pair.shared']))

    def test_even_packet_true_absence_and_whole_state_translation(self):
        for present in (False, True):
            p = finalize(BoardSpec(17), [place(GuideSegment(start=0, stop=16,
                sockets=(5, 6, 7, 8), remainder_pair=(0, 0)), at=(0, 8, 8), name='guide'),
                place(EvenPacketSource(present=present), at=(5, 8, 8), name='source')])
            if not present:
                self.assertEqual(len(p.initial.cells), 34)
            for t, state in enumerate(p.engine.evolve(p.initial, 18)):
                self.assertEqual(state, translated(p.initial, (t, 0, 0)))

    def test_strict_public_parameters_and_tensor(self):
        for factory, kwargs in [(LocalizedSixClock, {'phase': True}),
                                (LocalizedSixClock, {'halo_parity': False}),
                                (LocalizedSixClock, {'active': 1}),
                                (CompactFiveClock, {'conjugated': 1}),
                                (CompactFiveClock, {'phase': 1.0}),
                                (CooperativeClockPair, {'first_active': 1}),
                                (EvenPacketSource, {'present': 1})]:
            with self.assertRaises((TypeError, ValueError)):
                factory(**kwargs)
        for factory in (LocalizedSixClock, CompactFiveClock, CooperativeClockPair, EvenPacketSource):
            with self.assertRaises(ValueError):
                factory(tensor=TensorSpec((-1, 1, 1)))
        with self.assertRaises(ValueError):
            assemble_remainder_register(translation=(1, 0, 0))
        with self.assertRaises(ValueError):
            assemble_remainder_register(probe_delays=(28, 29), probes_present=(True, True))
        with self.assertRaises((ValueError, TypeError)):
            assemble_scatterer(gap=True)

    def test_register_socket_is_physical_source_overlap(self):
        source = dict(EvenPacketSource().cells)
        register = SourceOverlapRegister()
        self.assertEqual(len(register.cells), 4)
        self.assertTrue(all(source[a] == v == (0, 0, 0) for a, v in register.cells))
        with self.assertRaises(ValueError):
            finalize(BoardSpec(17), [place(RegisterWriter(), at=(5, 8, 8), name='writer')])
        with self.assertRaises(ValueError):
            finalize(BoardSpec(17, background=(0, 0, 0)), [place(register, at=(5, 8, 8), name='register')])

    def test_scatterer_true_absence_controls_are_stationary(self):
        for target in (False, True):
            p = assemble_scatterer(source_present=False, target_present=target)
            self.assertTrue(all(v.a == v.b == 0 for v in p.initial.cells.values()))
            self.assertEqual(p.engine.advance(p.initial), p.initial)

    def test_three_clock_json_returns_after_thirty_steps(self):
        path = Path(__file__).resolve().parents[1] / 'research/component_families/examples/three_clocks.json'
        p = assemble(json.loads(path.read_text()))
        self.assertEqual(list(p.engine.evolve(p.initial, 30))[-1], p.initial)
        self.assertEqual(set(p.ports), {'dimer.core', 'dimer.halo', 'dimer.center',
            'plaquette.core', 'plaquette.halo', 'plaquette.center', 'cube.core', 'cube.halo', 'cube.center'})

    def test_compact_evidence_inventory_and_initial_digest_validation(self):
        index = inventory()
        self.assertEqual((index['cases'], index['states'], index['transitions']), (31, 1671, 1640))
        case = load_case(index['records'][0])
        corrupted = copy.deepcopy(case)
        corrupted['initial']['cells'].append(corrupted['initial']['cells'][0])
        with self.assertRaises(ValueError):
            verify_case(corrupted)

    def test_expected_negative_does_not_hide_new_failures(self):
        row = next(r for r in inventory()['records'] if r['id'] == 'repeated-L337-w0-p11')
        case = load_case(row)
        checks = expected_register_checks(case)
        self.assertFalse(all(checks.values()))
        validate_register_checks(case, checks)
        for positive in ('read1_native_C_contract', 'written_remainder_hold',
                         'restoration_windows', 'exact_full_reference_clock'):
            altered = dict(checks, **{positive: False})
            with self.assertRaises(AssertionError):
                validate_register_checks(case, altered)

    def test_evidence_rejects_symlinks_and_extra_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / 'evidence'
            shutil.copytree(EVIDENCE, evidence)
            alias = root / 'alias'
            alias.symlink_to(evidence, target_is_directory=True)
            with self.assertRaises(ValueError):
                inventory(alias)
            extra = evidence / 'extra.txt'
            extra.write_text('unexpected')
            with self.assertRaises(ValueError):
                inventory(evidence)
            extra.unlink()
            moved = root / 'provenance.json'
            (evidence / 'provenance.json').rename(moved)
            (evidence / 'provenance.json').symlink_to(moved)
            with self.assertRaises(ValueError):
                inventory(evidence)

    def test_case_changed_after_inventory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / 'evidence'
            shutil.copytree(EVIDENCE, evidence)
            row = inventory(evidence)['records'][0]
            path = evidence / row['path']
            path.write_bytes(path.read_bytes() + b'changed-after-inventory')
            with self.assertRaises(ValueError):
                load_case(row, evidence)


if __name__ == '__main__':
    unittest.main()
