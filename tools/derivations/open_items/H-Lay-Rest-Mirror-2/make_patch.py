"""lr2's spec for David as one patch against the head 2ab32b518 (lr2.patch): the flagged copy's two acts with no flag, the head's lines replaced. (1) The centred digit, node.digit_of(rem, values, wall) = (|2 r + 1 - W| div 2, values div 2), the base (W div F) div 2 + 1, the origin where every line's distance is 0 (take.read_number). (2) The lay's rest at the seed (take.lay, node.interval 0): every line of the laid record born at the half of its wall, mirrored once where its own level is negative (now, or before where now is 0), the write remainder likewise. Built by this script from src/, nothing under src/ edited."""
import os
import shutil
import subprocess

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, "..", "..", "..", ".."))
src = os.path.join(root, "src", "event_universe")
dst = os.path.join(here, "src_patch", "event_universe")
if os.path.exists(os.path.join(here, "src_patch")):
    shutil.rmtree(os.path.join(here, "src_patch"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


take = os.path.join(dst, "take.py")
replace(
    take,
    """        line_.now[where] = line_.now[where] + sign * now
        line_.before[where] = line_.before[where] + sign * before
""",
    """        line_.now[where] = line_.now[where] + sign * now
        line_.before[where] = line_.before[where] + sign * before
    if node.interval == 0:  # LR-S1: the seed's rest born at the half and mirrored once where the line's own level is negative (rule (iv) of the one rule, the odd rounding's birth), so the lay of a negated line is the lay mirrored
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
            rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f), int(wl))  # LR-S1: the centred digit, r and W - 1 - r alike
            origin = origin and rem == 0
""",
)
replace(take, "    origin, coarse, w_half = True, True, half(node.w)\n", "    origin, coarse = True, True\n")
nodepy = os.path.join(dst, "node.py")
replace(
    nodepy,
    '''    def digit_of(self, rem: int, values: int) -> tuple[int, int]:
        """One line's digit at a Node: its remainder on the lattice and the count of values the lattice holds."""
        return rem, values
''',
    '''    def digit_of(self, rem: int, values: int, wall: int) -> tuple[int, int]:
        """One line's digit at a Node (LR-S1, the centred digit; David's mend, #2187 6406297069): the remainder's distance from the centre of its wall, |2 r + 1 - wall| div 2, the same integer for r and wall - 1 - r (the one rule's mirror), over half the count of values the lattice holds; the base (wall div F) div 2 + 1 in the read."""
        distance = rem + rem + 1 - wall
        return half(distance if distance >= 0 else -distance), half(values)
''',
)
out = subprocess.run(["diff", "-ruN", "src/event_universe", os.path.relpath(dst, root).replace("src_patch/", "", 1) if False else os.path.relpath(os.path.join(here, "src_patch", "event_universe"), root)], cwd=root, capture_output=True, text=True).stdout
out = out.replace(os.path.relpath(os.path.join(here, "src_patch"), root) + "/event_universe", "src/event_universe")
open(os.path.join(here, "lr2.patch"), "w").write(out)
print("lr2.patch written", len(out.splitlines()), "lines")
