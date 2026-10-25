"""t48: the 48 on the clicks by the test's own comparison at several interval counts on the engine in PYTHONPATH; the counts and the time of each, to pick the shortest run."""
import sys, time
sys.set_int_max_str_digits(0)
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
import event_universe.take as take
from tests import test_the_48_on_the_clicks as t
print("engine", take.__file__, "flag", os.environ.get("A48B_FOLD", ""))
images = t.signed_permutations()
for n in [int(x) for x in sys.argv[1:]]:
    t0 = time.perf_counter()
    got = t.the_48_on_the_clicks(n, images)
    ms = int((time.perf_counter() - t0) * 1000)
    print("intervals", n, "ms", ms, "base births", got["base_births"], "first turn", got["first_turn"], "births after turn", got["births_after_turn"], "counts", got["counts"])
    print("  unlawful:", [(k, d, v) for k, (g, d, v, _) in enumerate(got["verdicts"]) if v != ("equal" if d == 1 else "senses exchanged")])
