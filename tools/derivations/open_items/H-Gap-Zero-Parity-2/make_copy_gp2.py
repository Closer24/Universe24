"""gp2's flagged copy of the engine: src/event_universe copied whole to src_gp2/event_universe with two acts behind two environment flags, each empty for the head bit for bit.
GP2_FORM "children_sign": the children's lay carries the sense on the re line (merger.child_at, the one lay of a child for every children's record alike, the merger's light children among them, and close.unclick): the child at the sense s laid as (s A, 0, 0, B) in place of (A, 0, 0, s B); the two lays have the same charge W = s A B = s (T div 2), the same share (the levels' negatives), and differ by the quarter turn's square (the pi rotation of the - child), so the - child is the + child's image under the sign's rule (re -> -re) and not under the conjugation (im -> -im).
GP2_PICK "1": lr2's centred digit (node.digit_of): a line's remainder r at the wall W read as |2 r + 1 - W| div 2 (r and W - 1 - r alike), the base (W div F) div 2 + 1; the origin where every line's distance is 0; so the mirror state's draw is the base's, and the lays' parity is measured alone."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "src_gp2", "event_universe")
if os.path.exists(os.path.join(here, "src_gp2")):
    shutil.rmtree(os.path.join(here, "src_gp2"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


merger = os.path.join(dst, "merger.py")
replace(merger, "from __future__ import annotations\n", "from __future__ import annotations\n\nimport os\n\nGP2_FORM = os.environ.get(\"GP2_FORM\", \"\")  # gp2's flag: empty is the head bit for bit\n")
replace(
    merger,
    """    dp = momentum_of(node, re.now, re.before, where, d_now=sign * node.A, num=num)
    dp_im = momentum_of(node, im.now, im.before, where, d_before=sign * sense * node.B, num=num)
    lay(node, s, where, (node.A, 0, 0, sense * node.B), sign)
""",
    """    if GP2_FORM == "children_sign":  # gp2: the sense on the re line, (s A, 0, 0, B)
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
replace(closepy, "import numpy as np\n", "import numpy as np\nimport os\n\nGP2_FORM = os.environ.get(\"GP2_FORM\", \"\")  # gp2's flag: empty is the head bit for bit\n")
replace(
    closepy,
    """                if laid is None:
                    lay(node, s, tuple(where), (a, 0, 0, sense * b), -1)
""",
    """                if laid is None and GP2_FORM == "children_sign":  # gp2: the child's lay taken back in its form
                    lay(node, s, tuple(where), (sense * a, 0, 0, b), -1)
                elif laid is None:
                    lay(node, s, tuple(where), (a, 0, 0, sense * b), -1)
""",
)
take = os.path.join(dst, "take.py")
replace(take, "import numpy as np\n", "import numpy as np\nimport os\n\nGP2_PICK = os.environ.get(\"GP2_PICK\", \"\")  # lr2's centred pick under gp2's name: empty is the head bit for bit\n")
replace(
    take,
    """            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
""",
    """            wl = at_node(line.wall, n)
            if GP2_PICK == "1":  # lr2's centred digit, r and W - 1 - r alike
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
print("src_gp2 built")
