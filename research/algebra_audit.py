"""Finite exact checks supplementing docs/ALGEBRA_AUDIT_2026-11-07.md.

Run from the repository root: python -m research.algebra_audit
No mutations, runtime interventions, alternate evolution laws or dependencies.
"""
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from random import Random
import sys

from universe24.core import Channel, Coupling, Cube, Engine, State
from universe24.core.rule3 import forward, inverse
from universe24.observation.diagnostics import signed_account

SOURCE_COMMIT = "ed1556e202eb0f3cc60342c75d44012c2eeb71c3"
SEED = 241107


def state_digest(state):
    data = [state.cube.side, list(state.background),
            [[list(addr), list(value)] for addr, value in sorted(state.cells.items())]]
    return sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()


def audit():
    rng = Random(SEED)
    counts = {"scalar_cases": 0, "dense_channel_comparisons": 0,
              "full_state_roundtrips": 0, "signed_Q_identities": 0}
    for a, b, r, u in product(range(-2, 3), range(-2, 3), range(6), range(-7, 8)):
        s = Channel(a, b, r)
        n = forward(s, u)
        assert inverse(n, u) == s
        assert forward(inverse(s, u), u) == s
        assert n.r % 2 == r % 2
        shifted = forward(s, u + 1)
        assert 6 * (shifted.b - n.b) + shifted.r - n.r == 2
        p = 3 * (s.b - s.a) + s.r // 2 - 1
        pn = 3 * (n.b - n.a) + n.r // 2 - 1
        assert pn == p + u - 6 * b
        assert n.b == b + (pn + 1) // 3
        counts["scalar_cases"] += 1

    cases = []
    for signs in product((-1, 1), repeat=3):
        engine = Engine(Coupling(signs))
        cube = Cube(3)
        old = State(cube, cells={
            (*pos, g): Channel(rng.randint(-4, 4), rng.randint(-4, 4), rng.randrange(6))
            for pos in product(range(3), repeat=3) for g in range(48)
        })
        new = engine.advance(old)
        for pos in product(range(3), repeat=3):
            neighbors = tuple(old.node(cube.adjacent((*pos, 0), d, 0)[:3])
                              for d in range(6))
            assert engine.update_node(old.node(pos), neighbors) == new.node(pos)
            counts["dense_channel_comparisons"] += 48
        assert engine.rewind(new) == old
        assert engine.advance(engine.rewind(old)) == old
        counts["full_state_roundtrips"] += 2
        change = signed_account(new) - signed_account(old)
        assert change == 2 * (2 * sum(signs) - 6) * sum(s.b for s in old.cells.values())
        counts["signed_Q_identities"] += 1
        cases.append({"signs": list(signs), "coupling_fingerprint": engine.coupling.fingerprint,
                      "initial_state_sha256": state_digest(old),
                      "final_state_sha256": state_digest(new), "account_change": change})

    cube = Cube(3)
    engine = Engine(Coupling((1, -1, 1)))
    old = State(cube, cells={(0, 0, 0, 0): Channel(0, 1, 2)})
    signed_counterexample = signed_account(engine.advance(old)) - signed_account(old)
    assert signed_counterexample == -8

    engine = Engine(Coupling((1, 1, 1)))
    state = State(cube, Channel(0, 0, 0), {
        (*pos, g): Channel(0, 1, 0)
        for pos in product(range(3), repeat=3) for g in range(48)
    })
    for t in range(10):
        assert len(state.cells) == 48 * 3**3
        assert all(s == Channel(t, t + 1, 0) for s in state.cells.values())
        state = engine.advance(state)
    assert all(s == Channel(10, 11, 0) for s in state.cells.values())

    root = Path(__file__).resolve().parent.parent
    files = list(sorted((root / "universe24/core").glob("*.py")))
    files += [root / "universe24/observation/diagnostics.py", Path(__file__).resolve()]
    return {
        "source_commit": SOURCE_COMMIT,
        "source_identity_note": "Pinned reviewed commit; hashes below identify actual executed files.",
        "source_sha256": {str(path.relative_to(root)): sha256(path.read_bytes()).hexdigest()
                          for path in files},
        "python_version": sys.version,
        "status": "passed",
        "counts": counts,
        "scalar_domain": {"a": [-2, 2], "b": [-2, 2], "r": [0, 5], "u": [-7, 7]},
        "ensemble": {"generator": "Python random.Random", "seed": SEED,
                     "sign_order": "itertools.product((-1,1),repeat=3)",
                     "address_order": "itertools.product(range(3),repeat=3), then g=0..47",
                     "draw_order": "a=randint(-4,4), b=randint(-4,4), r=randrange(6)",
                     "rng_reseed_between_cases": False, "side": 3,
                     "steps": 1, "boundary": "periodic", "background": [0, 0, 2]},
        "cases": cases,
        "signed_Q_counterexample": {"side": 3, "signs": [1, -1, 1],
                                    "background": [0, 0, 2], "steps": 1,
                                    "initial_deviations": [[[0, 0, 0, 0], [0, 1, 2]]],
                                    "account_change": signed_counterexample},
        "uniform_drift": {"side": 3, "signs": [1, 1, 1], "initial_all_channels": [0, 1, 0],
                          "steps": 10, "formula": "(a,b,r)=(t,t+1,0)", "passed": True},
        "scope": "Finite implementation checks, not proof over all states or physical validation."
    }


if __name__ == "__main__":
    result = audit()
    output = Path(__file__).with_name("algebra_audit_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "counts": result["counts"],
                      "output": str(output)}))
