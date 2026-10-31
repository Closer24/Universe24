import json, sys
from pathlib import Path
T = Path(sys.argv[1]); W = Path(sys.argv[2])
sys.path.insert(0, str(T.joinpath("src"))); sys.path.insert(0, str(T))
import numpy as np
from tensor24 import main as tmain
from tensor24.runner import load as loadmod, plans
from tensor24.runner.files import sites_of, star
u, p, s = (json.loads(W.joinpath(n + ".json").read_text()) for n in ("universe", "piece", "setting"))
kinds, c, square = tmain.made(star(len(p["shape"])))
loaded, found = loadmod.load(u, s, sites_of(p["shape"]), kinds, c, square)
print("found", found)
row, of, kind, comp, off = plans.rows_of(loaded.trains)
print("rows", len(row), "trains", [t["name"] for t in u["trains"]])
print("of", list(of)); print("held", list(loaded.trains.held), "tied", list(loaded.trains.tied), "square", list(loaded.trains.square))
f, legs = loaded.potential
legs = np.stack(legs, axis=1)
live = [(int(a), [int(x) for x in l]) for a, l in zip(f, legs) if int(a) != 0]
print("live monomials", len(live))
for a, l in live: print(a, l)
lay = tmain.layout(u, p["shape"], loaded)
print("rest", set(int(x) for x in np.asarray(lay.gearing.rest).ravel()), "stretch", set(int(x) for x in np.asarray(lay.gearing.stretch).ravel()), "kick", set(int(x) for x in np.asarray(lay.gearing.kick).ravel()), "drive", sorted(set(int(x) for x in np.asarray(lay.gearing.drive).ravel())), "parity", sorted(set(int(x) for x in np.asarray(lay.gearing.parity).ravel())))
print("push plan factors nonzero", int(sum(int(x) != 0 for x in lay.push.factor)), "mesh plan nonzero", int(sum(int(x) != 0 for x in lay.mesh.factor)), "clock read nonzero", int(sum(int(x) != 0 for x in lay.clock.factor)))
a = np.asarray(loaded.state[0]); print("laid a nonzero rows", sorted(set(np.nonzero(a)[0].tolist())), "sites", a.shape[1])
