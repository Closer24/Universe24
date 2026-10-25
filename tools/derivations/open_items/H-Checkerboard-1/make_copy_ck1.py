"""ck1's flagged copy of the engine: src/event_universe copied whole to src_ck1/event_universe with three named text replacements, every flag unset is David's path bit for bit.
(1) take.py, read_number's digit: a48b's A48B_FOLD (the approved A48-S1 is the value "frame2": every remainder returned to its laid frame by the exchange's own count of reversals, folded by the two's complement, the digit on the lattice, the base halved); the text is a48b's make_copy_a48b.py verbatim.
(2) interval.py, the emission's quotient over the mean wall: ma1's MA1_ODD (1 the law's odd rounding, 2 the odd floor sign(E) (|E| div W)); the text is ma1's make_copy.py verbatim.
(3) close.py, the bodies' closing: CK1_CROSS=1 reads the record's re line's zero crossing in either direction (before < 0 <= now or now < 0 <= before), even under the negation of the line, in place of the upward crossing alone; the beat is then the half period.
Usage: python make_copy_ck1.py (writes src_ck1/ beside this file)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "src", "event_universe")
root = os.path.join(here, "src_ck1")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))

# (1) a48b's replacement in take.py
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
assert text.count(old) == 1, "the replacement site is not unique (take.py)"
text = text.replace(old, new)
old2 = """    for line, r in rules:
        f0 = lattice("""
new2 = """    is_im = node.is_im()  # a48b: the exchange's own count of reversals per line
    for li, (line, r) in enumerate(rules):
        f0 = lattice("""
assert text.count(old2) == 1, "the loop head is not unique (take.py)"
text = text.replace(old2, new2)
text = text.replace("import numpy as np\n", "import numpy as np\nimport os\n\nA48B_FOLD = os.environ.get(\"A48B_FOLD\", \"\")  # a48b's flag: empty is David's path bit for bit\n", 1)
open(path, "w").write(text)

# (2) ma1's replacement in interval.py
p = os.path.join(dst, "interval.py")
s = open(p).read()
old_fwd = "        node.write(laid_line, quotient(self.emission, self.w_div), 1)\n"
old_bwd = "        node.write(self.lines(self.gap0)[0], quotient(self.emission, self.mean_wall()), -1)\n"
assert s.count(old_fwd) == 1 and s.count(old_bwd) == 1, "the write sites are not unique (interval.py)"
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
assert s.count(old_def) == 1, "laid_on is not unique (interval.py)"
s = s.replace(old_def, new_def)
open(p, "w").write(s)

# (3) ck1's replacement in close.py: the closing's crossing
p = os.path.join(dst, "close.py")
s = open(p).read()
old_up = """        upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
            re.before, re.now
        )
"""
new_up = """        if os.environ.get("CK1_CROSS", "") == "1":  # ck1's flag: the zero crossing in either direction, even under the line's negation
            upward = np.vectorize(
                lambda b, n: 1 if (int(b) < 0 <= int(n) or int(n) < 0 <= int(b)) else 0, otypes=[object]
            )(re.before, re.now)
        else:
            upward = np.vectorize(lambda b, n: 1 if (int(b) < 0 <= int(n)) else 0, otypes=[object])(
                re.before, re.now
            )
"""
assert s.count(old_up) == 1, "the crossing site is not unique (close.py)"
s = s.replace(old_up, new_up)
s = s.replace("import numpy as np\n", "import numpy as np\nimport os\n", 1)
open(p, "w").write(s)
print("copy written:", dst, "flags: A48B_FOLD (take.py), MA1_ODD (interval.py), CK1_CROSS (close.py); all unset = David's path")
