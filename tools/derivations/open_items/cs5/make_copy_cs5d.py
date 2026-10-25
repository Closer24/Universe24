"""cs5's fourth copy (src_cs5d from src_cs5c, the flags kept): CS5_CROWD_OFF=1, the lay's crowd refusal lifted (CS_COMPARISON 5(b): the owner's word on the crowd rule, per Node as written or lifted), so two children of one record may land at one Node in one close and sum on its lines (the conjugate pair's sum, as seed.lay_packet lays ma2's pair on one record); unset, the copy is src_cs5c. A test of the Boss's reading (1) on the one-plane file under that word, no proposal.
Usage: python make_copy_cs5d.py"""
import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src_cs5c", "event_universe")
root = os.path.join(here, "src_cs5d")
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "close.py")
s = open(p).read()
old = """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
"""
new = """    crowded = [k for k in kept if landing[(k[1], k[2])] > 1 or landing[(k[1], k[3])] > 1]
    if os.environ.get("CS5_CROWD_OFF", "") == "1":  # cs5's control: the crowd refusal lifted
        crowded = []
"""
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
print("copy written:", dst, "flag: CS5_CROWD_OFF (close.py)")
