"""Contracts protect real initial states and never supply runtime decisions."""
from copy import deepcopy
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import tempfile
import unittest

from research.components import BoardSpec, Patch, Receiver, TensorSpec, place
from research.experiments.run import assemble
from research.staged_blocks.composition import (RunContext, ComponentPreparation, compose_initial,
    example_specs, source_off_state, validate_source_off, run)
from research.staged_blocks.contracts import (load_catalog, stage_report, require_stage,
    click_observer, observe_states, orbit_observer, state_observer)
from universe24 import Cube, State
from universe24.core.group_2o import group, rotate

ROOT = Path(__file__).resolve().parents[1]


class StagedCompositionTests(unittest.TestCase):
    def prepare(self, patch, *, name='p', side=33, seed=0, time0=0, at=(16,16,16), orientation=0, reserved=()):
        return ComponentPreparation(place(patch, name=name, at=at, orientation=orientation),
                                    side, seed, time0, reserved)

    def test_context_tensor_background_and_timezero_conflicts(self):
        context = RunContext(BoardSpec(33), seed=7)
        for field in ('side', 'seed', 'time0'):
            values = {'side':33, 'seed':7, 'time0':0}
            values[field] += 1
            with self.assertRaisesRegex(ValueError, field):
                compose_initial(context, [self.prepare(Receiver(), **values)])
        with self.assertRaisesRegex(ValueError, 'time0'):
            RunContext(BoardSpec(33), time0=1)
        other = TensorSpec.from_signs((-1,1,1))
        with self.assertRaisesRegex(ValueError, 'Tensor conflict.*fingerprint'):
            compose_initial(context, [self.prepare(Receiver(tensor=other), seed=7)])
        with self.assertRaisesRegex(ValueError, 'Background conflict'):
            compose_initial(context, [self.prepare(Patch('different', {}, background=(0,0,4)), seed=7)])
        with self.assertRaises(FrozenInstanceError):
            other.body_signs = (1,1,1)
        with self.assertRaisesRegex(ValueError, 'body-013'):
            TensorSpec(model_id='different-body-actions')

    def test_rotated_conflict_has_world_address_both_values_and_stable_order(self):
        algebra = group()
        lift = 1
        xyz = rotate(algebra.rotations[lift], (1,0,0))
        world = (*tuple(v+16 for v in xyz), algebra.multiplication[lift][0])
        first = self.prepare(Patch('one', {(1,0,0,0):(1,0,2)}), name='a', orientation=lift)
        second = self.prepare(Patch('two', {world:(0,1,4)}), name='b', at=(0,0,0))
        messages = []
        for components in ([first,second], [second,first]):
            with self.assertRaises(ValueError) as caught:
                compose_initial(RunContext(BoardSpec(33)), components)
            messages.append(str(caught.exception))
        self.assertEqual(messages[0], messages[1])
        for text in (str(world), '(1, 0, 2)', '(0, 1, 4)'):
            self.assertIn(text, messages[0])

    def test_channels_are_resources_not_whole_node_locks(self):
        one = self.prepare(Patch('one', {(0,0,0,0):(1,0,2)}), name='a')
        two = self.prepare(Patch('two', {(0,0,0,1):(0,1,4)}), name='b')
        prepared = compose_initial(RunContext(BoardSpec(33)), [one,two])
        self.assertEqual(tuple(prepared.initial.at((16,16,16,0))), (1,0,2))
        self.assertEqual(tuple(prepared.initial.at((16,16,16,1))), (0,1,4))
        self.assertEqual(prepared.engine.coupling.fingerprint, TensorSpec().fingerprint)

    def test_identical_share_and_exclusive_channel_reservation(self):
        patch = Patch('cell', {(0,0,0,0):(0,0,2)})
        a, b = self.prepare(patch, name='a'), self.prepare(patch, name='b')
        compose_initial(RunContext(BoardSpec(33)), [a,b])
        reserved = self.prepare(patch, name='a', reserved=((0,0,0,0),))
        with self.assertRaisesRegex(ValueError, 'resource conflict.*16, 16, 16, 0'):
            compose_initial(RunContext(BoardSpec(33)), [reserved,b])
        with self.assertRaisesRegex(ValueError, 'explicit initial triple'):
            self.prepare(patch, reserved=((0,0,0,1),))

    def source_pair(self, *, source_value=(0,1,2), clock_value=(1,0,2), seed=0):
        source = Patch('signal-source', {(0,0,0,0):source_value}, sources={'signal':((0,0,0,0),)})
        clock = Patch('prepared-clock', {(0,0,0,1):clock_value})
        return compose_initial(RunContext(BoardSpec(33), seed=seed),
                               [self.prepare(source, name='source', seed=seed),
                                self.prepare(clock, name='clock', seed=seed)])

    def test_source_off_preserves_remainders_clock_and_context(self):
        on, off = self.source_pair(), self.source_pair(source_value=(0,0,2))
        result = validate_source_off(on, off, ['source.signal'])
        self.assertTrue(result['matched_source_off'])
        self.assertEqual(source_off_state(on, ['source.signal']), off.initial)
        self.assertEqual(off.initial.at((16,16,16,1)).a, 1)
        for bad in (self.source_pair(source_value=(0,0,4)),
                    self.source_pair(source_value=(0,0,2), clock_value=(0,0,2))):
            with self.assertRaisesRegex(ValueError, 'Source-off conflict at'):
                validate_source_off(on, bad, ['source.signal'])
        with self.assertRaisesRegex(ValueError, 'context conflict'):
            validate_source_off(on, self.source_pair(source_value=(0,0,2), seed=1), ['source.signal'])
        with self.assertRaisesRegex(ValueError, 'declared source'):
            source_off_state(on, ['undeclared'])

    def test_stage_graph_allows_research_but_blocks_unproved_claims(self):
        self.assertTrue(stage_report('finite_ack')['allowed'])
        self.assertFalse(stage_report('finite_ack', purpose='deploy')['allowed'])
        with self.assertRaisesRegex(ValueError, 'unmet contracts'):
            require_stage('router')
        catalog = load_catalog()
        rows = {row['id']:row for row in catalog['stages']}
        self.assertNotIn('prepared_orbit', rows['quiet_capture']['requires'])
        # A valid quiet-memory alternative must work even before any orbit claim.
        rows['prepared_orbit']['status'] = 'prepared'
        for identifier in ('quiet_capture','waiting_capture'):
            rows[identifier]['status'] = 'observed'
            rows[identifier]['evidence'] = ['synthetic-stage-gating-test-only']
        report = stage_report('waiting_capture', purpose='claim', catalog=catalog)
        self.assertTrue(report['allowed'])
        self.assertEqual(rows['prepared_orbit']['status'], 'prepared')
        broken = deepcopy(catalog)
        broken['stages'][0]['requires'] = ['carrier']
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'catalog.json'
            path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(ValueError, 'cycle'):
                load_catalog(path)

    def test_catalog_evidence_paths_exist(self):
        catalog = load_catalog()
        for row in catalog['blocks'] + catalog['stages']:
            for evidence in row['evidence']:
                self.assertTrue((ROOT/evidence.split('#')[0]).is_file(), evidence)

    def test_pure_observer_keeps_every_C_class_and_checks_phase_order(self):
        cube = Cube(7)
        addresses = [(3,3,3,g) for g in range(3)]
        before = State(cube, cells={a:(0,0,0) for a in addresses})
        after = State(cube, cells={a:(0,1,2*g) for g,a in enumerate(addresses)})
        # Synthetic readout fixture: this checks classification, not a dynamical claim.
        observer = click_observer(addresses)
        observed = observe_states(observer, [before,after])
        self.assertEqual([row['kind'] for row in observed['events']], [0,1,2])
        self.assertEqual(observed['classes_retained'], [0,1,2])
        state_spec = state_observer({addresses[0]:(0,0,0)})
        self.assertEqual(observe_states(state_spec,[before,after])['matches'], [True,False])
        phases = [{addresses[0]:(0,0,0)}, {addresses[0]:(0,1,0)}]
        orbit = orbit_observer(phases)
        self.assertTrue(observe_states(orbit,[before,after,before])['matches_entire_interval'])
        self.assertFalse(observe_states(orbit,[before,before])['matches_entire_interval'])
        with self.assertRaises(TypeError):
            observer['classes'] = (1,)
        self.assertEqual(before.at(addresses[0]), (0,0,0))

    def test_four_available_blocks_compile_and_controls_keep_the_clock(self):
        specs = example_specs()
        self.assertEqual(len(specs), 4)
        self.assertTrue(all(len(spec['components']) == 4 for spec in specs))
        for on, off in ((specs[0],specs[1]),(specs[2],specs[3])):
            prepared_on, prepared_off = assemble(on), assemble(off)
            validate_source_off(prepared_on, prepared_off, ['carrier.packet'])
            self.assertNotEqual(prepared_off.initial.at(prepared_off.ports['clock.center'][0]).a, 0)
        self.assertEqual(specs[0]['controls']['arrangement'], 'isolated')
        self.assertEqual(specs[2]['controls']['arrangement'], 'connected')

    def test_real_four_block_demo_reports_coexistence_and_interaction_separately(self):
        with tempfile.TemporaryDirectory() as folder:
            report = run(Path(folder)/'demo', presenter=False)
            self.assertTrue(report['isolated_coexistence_passed'])
            self.assertTrue(report['connected_interaction_observed'])
            self.assertFalse(report['new_capture_or_approval_claim'])
            self.assertEqual(len(report['records']), 4)
            self.assertTrue(report['checks']['connected']['matched_source_off'])
            self.assertTrue(report['checks']['isolated']['prepared_clock_unchanged_by_source_control'])
            self.assertTrue((Path(folder)/'demo'/'protocol.json').is_file())
            self.assertTrue((Path(folder)/'demo'/'result.json').is_file())


if __name__ == '__main__':
    unittest.main()
