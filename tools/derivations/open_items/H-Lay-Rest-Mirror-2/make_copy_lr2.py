"""lr2's flagged copy of the engine: src/event_universe copied whole to src_lr2/event_universe with two acts behind two environment flags, each empty for the head bit for bit.
LR2_LAY "1": the lay's rest (take.lay, the one lay act, at the seed alone, node.interval 0): after the levels are laid, every line of the laid record has its rotation remainder (and its write remainder where the line writes) born at the half of its wall and mirrored once by the one rule (W - 1 - half) where the line's own laid level is negative (now, or before where now is 0), the odd rounding's birth, rule (iv) of the one rule: the rest's sign carried by the level's sign, so the lay of a negated line is the lay mirrored and the recipe commutes with every element of the 48 and with the conjugation.
LR2_PICK "1": the centred digit (node.digit_of): a line's remainder r at the wall W read as its distance from the centre |2 r + 1 - W| div 2 (r and W - 1 - r alike), the base (W div F) div 2 + 1; the origin where every line's distance is 0."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "src_lr2", "event_universe")
if os.path.exists(os.path.join(here, "src_lr2")):
    shutil.rmtree(os.path.join(here, "src_lr2"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


take = os.path.join(dst, "take.py")
replace(take, "import numpy as np\n", "import numpy as np\nimport os\n\nLR2_LAY = os.environ.get(\"LR2_LAY\", \"\")  # lr2's flag: empty is the head bit for bit\nLR2_PICK = os.environ.get(\"LR2_PICK\", \"\")\n")
replace(
    take,
    """        line_.now[where] = line_.now[where] + sign * now
        line_.before[where] = line_.before[where] + sign * before
""",
    """        line_.now[where] = line_.now[where] + sign * now
        line_.before[where] = line_.before[where] + sign * before
    if LR2_LAY == "1" and node.interval == 0:  # lr2: the rest's sign carried by the level's sign at the seed
        for line_ in lines:
            negative = np.where(line_.now != 0, line_.now < 0, line_.before < 0)
            line_.rem = np.where(negative, mirrored(half(line_.wall), line_.wall, 1), half(line_.wall)) + 0 * line_.rem
            if line_.wr is not None:
                line_.wr = np.where(negative, mirrored(half(line_.wwall), line_.wwall, 1), half(line_.wwall)) + 0 * line_.wr
""",
)
replace(
    take,
    """            rem, values = node.digit_of(int(line.rem[n]), quotient(at_node(line.wall, n), f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
""",
    """            wl = at_node(line.wall, n)
            if LR2_PICK == "1":  # lr2: the centred digit, r and W - 1 - r alike
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
print("src_lr2 built")
