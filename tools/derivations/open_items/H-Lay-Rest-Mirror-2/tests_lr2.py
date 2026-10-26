"""lr2's test (under 15 s) on the flagged copy with both flags on: (1) the centred digit reads r and W - 1 - r alike at every r of a wall of 20 and 2 classes; (2) the lay's rest at the seed: a negated level's line stands at W - 1 - half, a positive one's at the half, the write remainder likewise; (3) the laid state's integers under the inversion of the file (a rotation on the diagonal, det 1) carried back equal the base's at the laid lines. Run: LR2_LAY=1 LR2_PICK=1 python -m pytest tests_lr2.py."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src_lr2"))
sys.set_int_max_str_digits(0)
os.environ["LR2_LAY"], os.environ["LR2_PICK"] = "1", "1"
from event_universe.core.rule3 import half, mirrored  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

WORLD = os.path.join(HERE, "worlds", "world_chiral_3_30.json")


def test_centred_digit_reads_the_mirror_alike():
    u, w = load_world(WORLD)
    node = Node(u, w)
    for wall in (20, 2, 18000):
        for r in range(wall):
            assert node.digit_of(r, wall, wall) == node.digit_of(wall - 1 - r, wall, wall)
        assert node.digit_of(half(wall), wall, wall)[0] == 0 and node.digit_of(0, wall, wall)[0] == half(wall) - 1


def test_lay_rest_follows_the_level_sign():
    u, w = load_world(WORLD)
    node = Node(u, w)
    rec = node.records().index(node.emitter())
    row = node.records()[rec]
    at = (1, 1, 1)
    node.lay(rec, at, (0, 0, -5, -7))  # the im line negated at one Node
    re, im = row.lines[0], row.lines[1]
    assert int(im.rem[at]) == int(mirrored(half(im.wall), im.wall, 1)[at]) if hasattr(im.wall, "shape") else int(mirrored(half(im.wall), im.wall, 1))
    others = [x for x in np.ndindex(*node.shape) if x != at]
    assert all(int(im.rem[x]) == int(half(im.wall if not hasattr(im.wall, "shape") else im.wall[x])) for x in others)
    assert all(int(re.rem[x]) == int(half(re.wall if not hasattr(re.wall, "shape") else re.wall[x])) for x in np.ndindex(*node.shape))
    if re.wr is not None:
        assert all(int(re.wr[x]) == int(half(re.wwall if not hasattr(re.wwall, "shape") else re.wwall[x])) for x in np.ndindex(*node.shape))


def test_inverted_file_lays_the_carried_levels():
    u, w = load_world(WORLD)
    cube = int(w["shape"][0])
    inv = dict(w, seed=[dict(lay, **{k: [(-v) % cube for v in lay[k]] for k in ("at", "centre") if k in lay}) for lay in w["seed"]])
    a, b = Node(u, w), Node(u, inv)
    for la, lb in zip(a.all_lines(), b.all_lines(), strict=True):
        for name in ("now", "before", "rem"):
            x, y = getattr(la, name), getattr(lb, name)
            for at in np.ndindex(*a.shape):
                assert int(x[at]) == int(y[tuple((-v) % cube for v in at)])
