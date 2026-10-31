import json, sys, time
from pathlib import Path
T = Path(sys.argv[1]); W = Path(sys.argv[2]); n = int(sys.argv[3])
sys.path.insert(0, str(T.joinpath("src"))); sys.path.insert(0, str(T))
import numpy as np
from tensor24 import main as tmain
from tensor24.engine import step
from tensor24.engine.state import State
from tensor24.runner import load as loadmod
from tensor24.runner.files import sites_of, star
u, p, s = (json.loads(W.joinpath(x + ".json").read_text()) for x in ("universe", "piece", "setting"))
kinds, c, square = tmain.made(star(len(p["shape"])))
loaded, found = loadmod.load(u, s, sites_of(p["shape"]), kinds, c, square)
lay = tmain.layout(u, p["shape"], loaded)
st = State(*loaded.state)
t0 = time.process_time()
for i in range(n):
    st = step.tick(lay, st)
t1 = time.process_time()
uni = all(all(np.array_equal(x[:, :1].repeat(x.shape[1], axis=1), x) for x in (st.a, st.b, st.r)) for _ in [0])
print(f"{n} rounds in {t1 - t0:.2f} s cpu; sites alike: {uni}; widest {max(int(abs(int(v))).bit_length() for v in st.a.ravel())} bits")
