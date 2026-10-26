"""a483's flagged copy of the engine: src/event_universe copied whole to src_a483/event_universe with the one-Link read behind the environment flag A483_READ (take.read_number and close.list_of). Unset or empty: the head (A48-S1) bit for bit. "1": the remainder returned to its laid frame as A48-S1 returns it, folded by the one rule of the remainder (the ones' complement, min(rho, wl - 1 - rho)), the digit the folded remainder's distance below the half (half(wl) - 1 - folded) div F, the base (wl div F) div 2 + 1; the origin the exact half alone (every rho == half(wl)), where the draw is one unit on from the taken record in the records' order (the tie broken by the law's own order). "2": A48-S1's two's-complement fold with the same origin and tie break (the two effects measured apart)."""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "..", "..", "..", "..", "src", "event_universe")
dst = os.path.join(here, "src_a483", "event_universe")
if os.path.exists(os.path.join(here, "src_a483")):
    shutil.rmtree(os.path.join(here, "src_a483"))
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


take = os.path.join(dst, "take.py")
replace(take, "import numpy as np\n", "import numpy as np\nimport os\n\nA483_READ = os.environ.get(\"A483_READ\", \"\")  # a483's flag: empty is the head bit for bit\n")
replace(
    take,
    """            rho = mirrored(rem, wl, (1 - bit) * (1 + is_im[li]))
            folded = min(rho, remainder(wl - rho, wl))
            origin = origin and folded in (half(wl), mirrored(half(wl), wl, 1))
""",
    """            rho = mirrored(rem, wl, (1 - bit) * (1 + is_im[li]))
            if A483_READ == "1":  # a483: the fold by the one rule, the digit the distance below the half
                folded = half(wl) - 1 - min(rho, mirrored(rho, wl, 1))
                origin = origin and rho == half(wl)
            elif A483_READ == "2":  # a483: A48-S1's fold, the origin the exact half alone
                folded = min(rho, remainder(wl - rho, wl))
                origin = origin and rho == half(wl)
            else:
                folded = min(rho, remainder(wl - rho, wl))
                origin = origin and folded in (half(wl), mirrored(half(wl), wl, 1))
""",
)
replace(
    take,
    """    if origin or coarse:
        node.counts["refused_origin"] += origin
        return None
""",
    """    if A483_READ in ("1", "2") and coarse:
        return None
    if A483_READ in ("1", "2") and origin:  # a483: the origin names the record one on from the taken in the records' order
        node.counts["origin_order"] = node.counts.get("origin_order", 0) + 1
        return unit, 1
    if origin or coarse:
        node.counts["refused_origin"] += origin
        return None
""",
)
close = os.path.join(dst, "close.py")
replace(close, "import numpy as np\n", "import numpy as np\nimport os\n\nA483_READ = os.environ.get(\"A483_READ\", \"\")  # a483's flag\n")
replace(
    close,
    """    planes = [k for k, r in enumerate(records) if r.shape == PLANE]
    return planes[int(remainder(quotient(number, node.units[rec]), len(planes)))]
""",
    """    planes = [k for k, r in enumerate(records) if r.shape == PLANE]
    if A483_READ in ("1", "2"):  # a483: the children's record counted from the taken record in the records' order
        return planes[int(remainder(planes.index(rec) + quotient(number, node.units[rec]), len(planes)))]
    return planes[int(remainder(quotient(number, node.units[rec]), len(planes)))]
""",
)
print("copy written:", dst)
