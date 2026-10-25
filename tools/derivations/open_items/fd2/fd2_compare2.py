"""David's toy against one copy on one world: the state hash at every interval (the first interval apart), the counts, the log equality, the births and credits; the copy named by its folder.
Usage: python fd2_compare2.py <copy folder> <world.json> [control_digits]"""
import sys, os, json, importlib.util, copy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.set_int_max_str_digits(0)
def load(name, folder):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, folder, 'lean_full.py')); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
folder, world_path = sys.argv[1], sys.argv[2]
david = load('lean_david', 'toy_david'); other = load('lean_' + folder, folder)
universe, world = david.load_world(world_path)
if len(sys.argv) > 3: world = cp.deepcopy(world); world.setdefault('control', {})['digits'] = sys.argv[3]
n = int(world['intervals']); a = david.Lean(universe, world); b = other.Lean(universe, world)
equal = 0; first = None
for t in range(n):
    a.step(); b.step()
    if a.state_hash() == b.state_hash(): equal += 1
    elif first is None: first = t + 1
rem_apart = sum(int((la.rem != lb.rem).sum()) for la, lb in zip(a.all_lines(), b.all_lines()))
lev_apart = sum(int((la.now != lb.now).sum()) + int((la.before != lb.before).sum()) for la, lb in zip(a.all_lines(), b.all_lines()))
print(json.dumps({'copy': folder, 'world': os.path.basename(world_path), 'control digits': sys.argv[3] if len(sys.argv) > 3 else None, 'intervals': n, 'state hash equal': [equal, n], 'first interval apart': first, 'log equal': json.dumps(a.log, sort_keys=True) == json.dumps(b.log, sort_keys=True), 'counts David': {k: str(v) for k, v in a.counts.items()}, 'counts copy': {k: str(v) for k, v in b.counts.items()}, 'remainder entries apart at the end': rem_apart, 'level entries apart at the end': lev_apart}))
