"""Ownership, exact composition, mixed remainders and retained-state replay."""
from fractions import Fraction
import gzip
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from universe24.core import Engine, State, Tensor
from universe24.core.channels import ChannelAssembly, Component
from universe24.algebra.integer_circuit import Circuit
from universe24.layers.adm import compile_adm, flat_data
from universe24.layers.universe import UniverseProgram
from validation.adm_reference import run, replay_trace


class ChannelTests(unittest.TestCase):
    def test_same_local_names_have_distinct_owners_and_exact_dynamics(self):
        a = Tensor(['x','y'], [('x',1,(('y',(1,0,0),'b'),)),
                               ('y',-2,(('x',(0,0,0),'a'),))], strict_support=True)
        b = Tensor(['x','y'], [('x',3,(('y',(0,1,0),'b'),)),
                               ('y',5,(('x',(0,0,0),'b'),))], strict_support=True)
        joined = ChannelAssembly([Component('geometry',a,'test'),Component('matter',b,'test')])
        rng = np.random.default_rng(42)
        seeds = {name:State(3,rng.integers(-5,6,(2,27)),rng.integers(-5,6,(2,27)),
                           rng.integers(0,6,(2,27))) for name in ('geometry','matter')}
        large=seeds['matter'].b.astype(object);large[0,0]=2**100+1
        seeds['matter']=State(3,seeds['matter'].a,large,seeds['matter'].r)
        full = seed = joined.pack(seeds)
        states = {name:s.copy() for name,s in seeds.items()}
        engines = {'geometry':Engine(a),'matter':Engine(b)}
        engine = Engine(joined.tensor)
        for _ in range(9):
            full = engine.step(full)
            for name in states:
                states[name] = engines[name].step(states[name])
                self.assertTrue(joined.extract(full,name).same_as(states[name]))
        self.assertTrue(engine.rewind(full,9).same_as(seed))
        self.assertEqual(joined.tensor.rank,max(a.rank,b.rank))
        self.assertNotEqual(joined.channel('geometry','x'),joined.channel('matter','x'))
        port = joined.read_port('matter','x')
        self.assertEqual(port['access'],'read-only')
        with self.assertRaises(TypeError):port['channel']=0
        with self.assertRaises(TypeError):joined.channel('matter',0)
        with self.assertRaises(ValueError):joined.channel('matter','geometry.x')
        seed_before=seed.copy();seeds['matter'].b[:]=0
        self.assertTrue(seed.same_as(seed_before))

    def test_duplicate_owner_incomplete_seed_and_budget_fail_closed(self):
        t=Tensor(['x'],[]);part=Component('same',t,'test')
        with self.assertRaisesRegex(ValueError,'duplicate'):ChannelAssembly([part,part])
        with self.assertRaises(ValueError):ChannelAssembly([Component('bad.name',t,'test')])
        with self.assertRaisesRegex(ValueError,'budget'):
            ChannelAssembly([part,Component('other',t,'test')],max_channels=1)
        joined=ChannelAssembly([part])
        for seeds in ({},{'extra':State(3,*(np.zeros((1,27),dtype=object) for _ in range(3)))}):
            with self.assertRaises(ValueError):joined.pack(seeds)
        with self.assertRaises(ValueError):joined.pack({'same':State(3,*(np.zeros((2,27),dtype=object) for _ in range(3)))})

    def test_probe_chart_is_isolated_and_has_no_claim_to_physical_metric(self):
        circuit=Circuit();phi=circuit.input('phi')
        base=circuit.compile({'0.phi':phi,'1.phi':phi+1})
        program=UniverseProgram(base,{'fields':['phi'],'steps':1},probe_experiment=True)
        data={'phi':np.ones((5,5,5),dtype=object)}
        seed=program.prepare(5,data)
        engine=Engine(program.tensor);final=engine.run(seed,base.ticks)
        for component in program.assembly.components:
            expected=Engine(component.tensor).run(program.assembly.extract(seed,component.name),base.ticks)
            self.assertTrue(expected.same_as(program.assembly.extract(final,component.name)))
        self.assertEqual(program.tensor.G,base.tensor.G+54+26)
        manifest=program.channel_manifest()
        self.assertFalse(manifest['probe_common_metric_validated'])
        self.assertEqual(program.read(final,'1.phi'),Fraction(2))
        self.assertTrue(engine.rewind(final,base.ticks).same_as(seed))

    def test_real_einstein_outputs_unchanged_and_c2_trace_replays(self):
        base,parameters=compile_adm(scale=4096,mass_squared=0)
        program=UniverseProgram(base,parameters)
        data=flat_data(3,4096)
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory);report=run(program,data,parameters,out)
            self.assertGreater(report['component_observations']['communication']['C2'],0)
            self.assertEqual(report['channel_allocation']['total_channels'],base.tensor.G+54)
            replay=iter(replay_trace(out/'full_trace.jsonl.gz'))
            engine=Engine(program.tensor)
            initial=before=next(replay)
            for after in replay:
                self.assertTrue(engine.step(before).same_as(after))
                before=after
            final=before
            self.assertTrue(engine.rewind(final,program.ticks).same_as(initial))
            plain=Engine(base.tensor).run(base.prepare(3,data),base.ticks)
            self.assertTrue(program.assembly.extract(final,'einstein').same_as(plain))
            for key in base.outputs:
                self.assertEqual(program.read(final,key),base.read(plain,key))
            manifest=json.loads((out/'channels.json').read_text())
            self.assertEqual(len({c['name'] for c in manifest['channels']}),program.tensor.G)
            for value in manifest['field_readouts'].values():
                for part in value.values():
                    if part['channel'] is not None:
                        self.assertEqual(program.assembly.owners[part['channel']],'einstein')
            with gzip.open(out/'full_trace.jsonl.gz','rt') as file:
                self.assertEqual(json.loads(next(file))['format'],'Rule3-full-triples-delta-v2')
                self.assertTrue(any(json.loads(line)['r'] for line in file))

    def test_legacy_trace_remains_readable(self):
        seed=State(3,*(np.zeros((1,27),dtype=object) for _ in range(3)))
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'v1.json.gz'
            with gzip.open(path,'wt') as file:
                file.write(json.dumps({'format':'Rule3-full-triples-delta-v1','seed':seed.to_dict()})+'\n')
                file.write(json.dumps({'tick':1,'b':[[0,0,'a']]})+'\n')
            states=list(replay_trace(path))
            self.assertEqual(int(states[1].b[0,0]),10)
            np.testing.assert_array_equal(states[1].r,seed.r)


if __name__=='__main__':unittest.main()
