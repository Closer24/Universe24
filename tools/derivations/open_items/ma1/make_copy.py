"""ma1's flagged copy of the engine: src copied under engine_ma1/ with ONE named replacement in interval.py, the emission's quotient over the mean wall read through `emission_levels`: with MA1_ODD absent the floor `quotient(E, W)` bit for bit David's path; MA1_ODD=1 the law's odd rounding of a signed coefficient (paces.odd_rounded: sign(E) rounded(|E|, W) half up); MA1_ODD=2 the odd floor, sign(E) quotient(|E|, W) (the floor's odd extension, positive emissions bit for bit). Both in `writes` (forward) and `unwrite` (backward), the same function."""
import shutil, sys
from pathlib import Path

here = Path(__file__).resolve().parent
src = here.parents[2] / "src" / "event_universe"
dst = here / "engine_ma1" / "event_universe"
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)
p = dst / "interval.py"
s = p.read_text()
old_fwd = "        node.write(laid_line, quotient(self.emission, self.w_div), 1)\n"
old_bwd = "        node.write(self.lines(self.gap0)[0], quotient(self.emission, self.mean_wall()), -1)\n"
assert s.count(old_fwd) == 1 and s.count(old_bwd) == 1
s = s.replace(old_fwd, "        node.write(laid_line, emission_levels(self.emission, self.w_div), 1)\n")
s = s.replace(old_bwd, "        node.write(self.lines(self.gap0)[0], emission_levels(self.emission, self.mean_wall()), -1)\n")
old_def = "def laid_on(node: Node, line: Line, levels: Any) -> None:\n"
new_def = '''def emission_levels(emission: Any, wall: Any) -> Any:
    """ma1's flag: the emission's levels over the mean wall. Absent: the floor (David's path bit for bit). MA1_ODD=1: the law's odd rounding of a signed coefficient. MA1_ODD=2: the odd floor sign(E) (|E| div W)."""
    import os

    flag = os.environ.get("MA1_ODD", "")
    if flag == "1":
        return paces.odd_rounded(emission, wall)
    if flag == "2":
        signed = np.asarray(emission)
        negative = (signed < 0).astype(signed.dtype)
        sign = 1 - 2 * negative
        return sign * quotient(sign * emission, wall)
    return quotient(emission, wall)


def laid_on(node: Node, line: Line, levels: Any) -> None:
'''
assert s.count(old_def) == 1
s = s.replace(old_def, new_def)
p.write_text(s)
print("copy written:", dst, "replacements: 3 (two call sites, one function)")
