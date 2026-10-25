"""a48b's flagged copy of the engine: src/event_universe copied whole to src_a48b/event_universe, with one text replacement in take.py (read_number's digit), behind the environment flag A48B_FOLD: unset or empty, David's path bit for bit; "ones" the ones' complement fold of the digit min(d, B - 2 - d) (fd1's min(r, w - 1 - r)); "frame" the remainder mirrored once where the Node's frame bit is complemented (an odd count of turns) then folded by the two's complement min(rho, W - rho), the digit folded div F, base (W div F) div 2 + 1; "lattice" the lattice digit delta = (r + F - 1) div F folded by the two's complement, min(delta, W div F - delta), base (W div F) div 2 + 1."""
import os
import shutil
import sys

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "src_a48b", "event_universe")
if os.path.exists(os.path.join(here, "src_a48b")):
    shutil.rmtree(os.path.join(here, "src_a48b"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
path = os.path.join(dst, "take.py")
text = open(path).read()
old = """            rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
            coarse = coarse and values <= AXES
            digits.append((quotient(rem, f), values + 1))
"""
new = """            rem, values = node.digit_of(int(line.rem[n]), quotient(wl, f))
            origin = origin and rem in (w_half, mirrored(w_half, node.w, 1))
            coarse = coarse and values <= AXES
            if A48B_FOLD == "ones":  # a48b: fd1's fold, the digit of min(r, w - 1 - r)
                digits.append((quotient(min(rem, wl - 1 - rem), f), values + 1))
            elif A48B_FOLD == "lattice":  # a48b: the lattice digit ceil(r / F) folded by the two's complement
                delta = quotient(rem + f - 1, f)
                digits.append((min(delta, values - delta), quotient(values, 2) + 1))
            elif A48B_FOLD == "frame":  # a48b: the remainder returned to its lay's frame (mirrored once per turn, the frame bit the walled row's remainder at the slot's Node), folded by the two's complement, the digit on the lattice
                bit = int(rules[0][0].rem[n])
                rho = mirrored(rem, wl, 1 - bit)
                folded = min(rho, remainder(wl - rho, wl))
                digits.append((quotient(folded, f), quotient(values, 2) + 1))
            elif A48B_FOLD == "frame2":  # a48b: the same, the reversals counted as the exchange counts them (twice per turn for an im line, once for every other line), then the two's-complement fold
                bit = int(rules[0][0].rem[n])
                rho = mirrored(rem, wl, (1 - bit) * (1 + is_im[li]))
                folded = min(rho, remainder(wl - rho, wl))
                digits.append((quotient(folded, f), quotient(values, 2) + 1))
            else:
                digits.append((quotient(rem, f), values + 1))
"""
assert text.count(old) == 1, "the replacement site is not unique"
text = text.replace(old, new)
old2 = """    for line, r in rules:
        f0 = lattice("""
new2 = """    is_im = node.is_im()  # a48b: the exchange's own count of reversals per line
    for li, (line, r) in enumerate(rules):
        f0 = lattice("""
assert text.count(old2) == 1, "the loop head is not unique"
text = text.replace(old2, new2)
text = text.replace("import numpy as np\n", "import numpy as np\nimport os\n\nA48B_FOLD = os.environ.get(\"A48B_FOLD\", \"\")  # a48b's flag: empty is David's path bit for bit\n", 1)
open(path, "w").write(text)
print("copy written:", dst, "flag A48B_FOLD in", path)
