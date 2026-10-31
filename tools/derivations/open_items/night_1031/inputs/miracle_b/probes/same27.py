"""Check that the click world's 27 Node-clocks each run the one-Node-clock world's trajectory: at every reading, the
widest count alike and E32 (and its held and other parts) 27 times the one Node-clock's. Whole numbers only.
Usage: python3 -I same27.py <the click world's output> <the one Node-clock's output>"""
import re, sys
from pathlib import Path
pat = re.compile(r"^round (\d+): widest (\d+) bits; E32 (-?\d+) \(\d+ ppm from the lay; held (-?\d+), other (-?\d+)\)")
def readings(path):
    out = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = pat.match(line)
        if m:
            out[int(m.group(1))] = tuple(int(x) for x in m.groups()[1:])
    return out
big, one = readings(sys.argv[1]), readings(sys.argv[2])
common = sorted(set(big) & set(one))
alike = sum(1 for n in common if big[n][0] == one[n][0] and all(big[n][i] == 27 * one[n][i] for i in (1, 2, 3)))
print(f"readings compared {len(common)}; widest alike and E32, held and other each 27 times the one Node-clock's at {alike}")
