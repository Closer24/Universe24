"""DECODE3g: where the joint past's gate opens at L = 8 (one source, fair marginals, the share 5 / 46 per cent). It
executes decode3g.py's own exp_neg_up and ladder_gate, lifted by name. Whole numbers. argv: the output name."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

TEXT = HERE.joinpath("decode3g.py").read_text(encoding="utf-8")


def lift(name):
    head = TEXT.index("\ndef " + name + "(") + 1
    body = TEXT[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


g = {"carry": carry, "SC": 10 ** 30}
exec(compile(lift("exp_neg_up") + lift("ladder_gate"), "decode3g.py", "exec"), g)
out = []
for n in (2000, 2200, 2300, 2400, 2500, 3000):
    h, _ = carry(n, 2, 0)
    sym = [h * h, h * (n - h), (n - h) * h, (n - h) * (n - h)]
    ok, bound = g["ladder_gate"]((sym, [h, n - h]), (h, n - h), n, 8, 920, 18)
    out.append(f"n {n} a half: the joint past's gate at L = 8 opens {ok} (its bound {carry(1000000 * bound, g['SC'], 0)[0]}"
               f" per million, against {carry(1000000, 920, 0)[0]})")
HERE.joinpath(sys.argv[1]).write_text("\n".join(out) + "\n", encoding="utf-8")
