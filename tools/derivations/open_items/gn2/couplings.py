"""gn2 pick 1: the coupling K = omega_0 Gamma of every lift of the two universe files, and of (779, 1021), read on the orbit in integers (the copy's coupling_of)."""
import os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.set_int_max_str_digits(0)
spec = importlib.util.spec_from_file_location('lean_gn2', os.path.join(HERE, 'flagged', 'lean_full.py')); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
universe, world = mod.load_world(os.path.join(HERE, 'toy_former', 'world_node.json'))
b = mod.Lean(universe, world)
found = {'gamma': b.gamma, 'X': b.X, 'orbit cos at counts 0,1,703,1000,1571,3141 over X': [b.pair_angle(n)[0] for n in (0, 1, 703, 1000, 1571, 3141)]}
found['K per pair (num/den in millionths, K)'] = [[(r.pair[0] * 1000000) // r.pair[1], b.coupling_of(r.pair)] for r in b.records()]
found['K at (779, 1021)'] = b.coupling_of((779, 1021))
found['K at (1654253232, 1655909141) and (506298091, 1655909141) and (1655880909, 1655909141)'] = [b.coupling_of(p) for p in ((1654253232, 1655909141), (506298091, 1655909141), (1655880909, 1655909141))]
print(json.dumps(found))
