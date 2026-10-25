"""sl1's one-Node test (Addition 6, step 2; under 15 s): the chiral seed on the 5-cube under the generic close (the flagged copy, SL1_CLOSE=generic) run to the close after the first birth; at the born pair's Link the generic close reads, from the letter alone: the taken row's current F_re = 0 and F_im = 0 exactly (the orientation refuses the undoing), the twist 0, both ends whole in the child's unit, the gap-0 row standing above 0 at both ends (the lay would refuse two light children), and the fall at either end below the walls of two light quanta (the stop would refuse); the state after N intervals equal to the repository's src bit for bit (the generic close takes no gapped meeting). Run: python one_node_test.py  (or pytest one_node_test.py)."""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORLD = os.path.join(HERE, "worlds", "world_chiral_30.json")


def node_with(package: str, flag: bool):
    """A fresh interpreter's worth of modules is not available inside one process: the package is imported once per process, so this helper is used by the two subprocess runs below."""
    raise NotImplementedError


def run_hash(package: str, intervals: int, flag: bool) -> tuple[str, list]:
    """A child process runs the world on the named package to `intervals` and prints the state's hash and the log; the two packages cannot share one interpreter."""
    import subprocess

    code = (
        "import os, sys, json\n"
        + ("os.environ['SL1_CLOSE'] = 'generic'\n" if flag else "")
        + "sys.path.insert(0, %r)\n" % (os.path.join(HERE, "src_sl1") if package == "copy" else os.path.normpath(os.path.join(HERE, "..", "..", "..", "src")))
        + "sys.set_int_max_str_digits(0)\n"
        + "from event_universe.loader.world import load_world\n"
        + "from event_universe.node import Node\n"
        + "u, w = load_world(%r)\n" % WORLD
        + "n = Node(u, w)\n"
        + "for _ in range(%d): n.step()\n" % intervals
        + "print(json.dumps({'hash': n.state_hash(), 'log': n.log, 'counts': {k: str(v) for k, v in n.counts.items()}}))\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True, env={**os.environ, "TMPDIR": "/dev/shm/tmp"})
    found = json.loads(out.stdout.strip().splitlines()[-1])
    return found["hash"], found["log"], found["counts"]


def test_the_born_pair_is_refused_by_the_letter_at_the_next_close() -> None:
    intervals = 5
    h_src, log_src, _c = run_hash("src", intervals, False)
    h_copy, log_copy, counts = run_hash("copy", intervals, True)
    assert h_src == h_copy, "the generic close changed the state: a gapped meeting was taken"
    births = [e for e in log_copy if e["event"] == "birth"]
    assert births and births[0]["i"] == 3, births[:1]
    probes = [e for e in log_copy if e["event"] == "sl1_probe" and e["i"] == e["birth_i"] + 1]
    assert len(probes) == len([b for b in births if b["i"] + 1 <= intervals])
    for p in probes:
        assert p["F_re"] == 0 and p["F_im"] == 0, p  # (a) the orientation refuses the undoing: the lay's symmetry
        assert p["twist"] == 0, p  # (b) the twist is 0 at an isolated born pair
        assert p["whole_both_ends"] == 1, p  # the pair stands whole at both ends in the child's unit at the vacuum's weight
        assert all(f[0] is None and f[1] < p["walls_two_light"] for f in p["falls"]), p  # (c) the stop: neither end can pay two light quanta
        assert p["gap0_standing"][0] > 0 or p["gap0_standing"][1] > 0, p  # (d) the lay refuses two light children where the sea stands at either end (close.refuse: owns > 0 at the - or the + end; the share reads below 0 at a Node beside the hole)
    refused_own = [e for e in log_copy if e["event"] == "refused" and e.get("taken_row") in (0, 1, 2) and e["cause"] == "orientation"]
    own_links = {(tuple(p["node"]), tuple(p["link"]), p["i"]) for p in probes}
    hit = {(tuple(e["node"]), tuple(e["link"]), e["i"]) for e in refused_own}
    assert own_links <= hit, own_links - hit  # every born pair's Link is refused by the orientation at the next close (a pair met again later, F = 0 still, counts beyond)
    print("PASS: births %d, probes at the next close %d, F_re = F_im = twist = 0 at every one, whole at both ends, the stop and the lay would refuse; hash equal %s" % (len(births), len(probes), h_src[:16]))
    print("counts:", {k: v for k, v in counts.items() if k.startswith("sl1_")})


if __name__ == "__main__":
    import time

    t0 = time.monotonic_ns()
    test_the_born_pair_is_refused_by_the_letter_at_the_next_close()
    print("seconds:", (time.monotonic_ns() - t0) // 10**9)
