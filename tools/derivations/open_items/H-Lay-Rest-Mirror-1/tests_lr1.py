"""lr1's one test (under 15 s): (1) at the interval 0 on the chiral 3-cube the reflected FILE lays every level of the C P mirror state and not its odd lines' remainders (the half of an even wall is not its own mirror under W - 1 - r; 135 to 216 entries apart per reflection, every one on a line laid at the level 0), with the lay rule flagged or not; (2) the centred digit |2 r + 1 - W| reads r and W - 1 - r alike on every wall of the Node. Run: PYTHONPATH=<src> python -m pytest tests_lr1.py -q (LR1_PICK=1 LR1_LAY=1 for the flagged copy)."""
import json
import os
import sys

import numpy as np

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], os.environ.get("LR1_SRC", os.path.join(HERE, "src_lr1")), os.path.join(HERE, "..", "..", "..", ".."), "0", "/dev/null"]
exec(open(os.path.join(HERE, "run_48_lr1.py")).read().split("if __name__")[0])


def test_reflected_file_lays_the_mirror_levels_not_the_odd_rests():
    m = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
    base = Node(json.loads(json.dumps(universe)), world)
    by_file = Node(json.loads(json.dumps(universe)), world_image(world, m))
    lev = rem = zero = 0
    for li, (lj, s) in enumerate(line_signs(base, m)):
        src, dst = base.all_lines()[li], by_file.all_lines()[lj]
        for x in np.ndindex(*base.shape):
            gx = image(m, x)
            lev += s * int(src.now[x]) != int(dst.now[gx]) or s * int(src.before[x]) != int(dst.before[gx])
            w = int(src.wall[x]) if isinstance(src.wall, np.ndarray) else int(src.wall)
            want = w - 1 - int(src.rem[x]) if s == -1 else int(src.rem[x])
            if want != int(dst.rem[gx]):
                rem += 1
                zero += int(src.now[x]) == 0 and int(src.before[x]) == 0
    assert lev == 0, f"levels apart {lev}"
    assert rem == zero, f"{rem} remainders apart, {zero} of them on lines laid at 0"
    assert rem > 0, "the z reflection's odd lines' remainders at the half are not the mirror's: the law unmet by the lay"


def test_centred_digit_reads_r_and_its_mirror_alike():
    node = Node(json.loads(json.dumps(universe)), world)
    os.environ["LR1_PICK"] = "1"
    try:
        for line in node.all_lines():
            w = int(line.wall[0, 0, 0]) if isinstance(line.wall, np.ndarray) else int(line.wall)
            for r in (0, 1, w // 2 - 1, w // 2, w - 1):
                a, b = node.digit_of(r, 1, w), node.digit_of(w - 1 - r, 1, w)
                assert a == b, (r, w, a, b)
            assert node.digit_of(w // 2, 1, w)[0] == 1
    finally:
        os.environ.pop("LR1_PICK", None)
