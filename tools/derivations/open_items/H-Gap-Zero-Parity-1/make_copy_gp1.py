"""gp1's flagged copy of the engine: src/event_universe copied whole to src_gp1/event_universe with one act behind one environment flag, empty for the head bit for bit.
GP1_FORM "ii": the children's lay carries the charge's sign on the re line (merger.child_at and the run back in close.py): a child of the sense s is laid at the quarter turn as re_now = s A, im_before = B (the head: re_now = A, im_before = s B), A B = T div 2 as MS-S1 has it, its Wronskian s A B = s T div 2 unchanged, the two children's W summing to 0 as before; the child of the sense -1 is the head's child turned by a half turn of its plane (z -> -z), the same record, the same share, the same charge. Under the conjugation composed with the half turn (re odd, im even, C P on the plane as the emission's lay already needs it) the lay at one end maps to the lay of the opposite sense at the image end, so the two lays onto the gap-0 row (the emission re F_im - im F_re, odd under C, and the children) carry ONE parity."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "src_gp1"  # the copy's folder: src_gp1 for the record runs, src_gp1_pick the same copy for the mirror runs (one text, two folders so that the two sets of runs never share a cache)
dst = os.path.join(here, name, "event_universe")
if os.path.exists(os.path.join(here, name)):
    shutil.rmtree(os.path.join(here, name))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


merger = os.path.join(dst, "merger.py")
replace(merger, "from event_universe import gram\n", "import os\n\nfrom event_universe import gram\n\nGP1_FORM = os.environ.get(\"GP1_FORM\", \"\")  # gp1's flag: empty is the head bit for bit\n")
replace(
    merger,
    """    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
""",
    """    if GP1_FORM == "ii":  # gp1: the charge's sign on the re line, re_now = s A, im_before = B
        dp = momentum_of(node, re.now, re.before, where, d_now=sign * sense * node.A, num=num)
        dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * node.B, num=num)
        lay(node, s, where, (sense * node.A, 0, 0, node.B), sign)
        return [a + b for a, b in zip(dp, dp_im, strict=True)]
    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
""",
)
closepy = os.path.join(dst, "close.py")
replace(
    closepy,
    """                if laid is None:
                    lay(node, s, tuple(where), (a, 0, 0, sense * b), -1)
""",
    """                if laid is None:
                    if os.environ.get("GP1_FORM", "") == "ii":  # gp1: the same form undone
                        lay(node, s, tuple(where), (sense * a, 0, 0, b), -1)
                    else:
                        lay(node, s, tuple(where), (a, 0, 0, sense * b), -1)
""",
)
text = open(closepy).read()
if "\nimport os\n" not in text:
    replace(closepy, "from __future__ import annotations\n", "from __future__ import annotations\n\nimport os\n")

# gp1: lr2's centred pick behind GP1_PICK (lr2's make_copy_lr2.py, the same text), so that the mirror STATE is measured with the digit read r and W - 1 - r alike and the step's parity is isolated from the read's; off for every record run
take = os.path.join(dst, "take.py")
replace(take, "import numpy as np\n", "import numpy as np\nimport os\n\nGP1_PICK = os.environ.get(\"GP1_PICK\", \"\")  # lr2's centred pick behind gp1's flag: empty is the head bit for bit\n")
replace(
    take,
    """            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
""",
    """            wl = at_node(line.wall, n)
            if GP1_PICK == "1":  # lr2's centred digit, r and W - 1 - r alike
                rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f), int(wl))
                origin = origin and rem == 0
            else:
                rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f))
                origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
""",
)
nodepy = os.path.join(dst, "node.py")
replace(
    nodepy,
    '''    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds."""
        return rem, values
''',
    '''    def digit_of(self, rem: int, values: int, wall: int | None = None) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds; with the wall named (lr2's centred digit) the distance from the centre |2 r + 1 - wall| div 2, the same for r and wall - 1 - r, over half the count."""
        if wall is None:
            return rem, values
        distance = rem + rem + 1 - wall
        return half(distance if distance >= 0 else -distance), half(values)
''',
)
print("built", dst)
