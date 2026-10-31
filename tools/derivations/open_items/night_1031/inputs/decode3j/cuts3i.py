"""DECODE3i's readings file, computed once (never at read time): readings3i.json. It keeps readings3h's (3b) cuts and
constants (now the run tool's board checks), and adds, for R4's family at N_T 58 and 74 (5 / N_T per cent a test):
- CUT_FW, one degree, as cuts3h computes it;
- the lag sums' cuts: the chi-square on 16 and on 8 degrees, upper tail, by the Poisson sum (even degrees),
  P(X > x) = e^(-x/2) SUM_(j < k/2) (x/2)^j / j!; the least whole thousandth whose tail is at most the level.
Whole numbers; Rule3's carry the one division. argv: the readings3h.json path, the output name."""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

TEXT = HERE.joinpath("cuts3h.py").read_text(encoding="utf-8")


def lift(name):
    head = TEXT.index("\ndef " + name + "(") + 1
    body = TEXT[head:].split("\n")
    keep = [body[0]]
    for ln in body[1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        keep.append(ln)
    return "\n".join(keep) + "\n"


SC = 10 ** 90
TERMS = 320
exec(compile("".join(lift(n) for n in ("atan_inv", "exp_half", "poisson_part", "least", "one_ok")), "cuts3h.py",
             "exec"), globals())
PI = 16 * atan_inv(5) - 4 * atan_inv(239)


def upper_ok(c, k, nt):
    """True where P(X_k > c / 1,000) <= 5 / (100 nt), k even: SUM_(j < k/2) (c/2000)^j / j! <= e^(c/2000) / (20 nt)."""
    m, _ = carry(k, 2, 0)
    return 20 * nt * poisson_part(c, m) <= exp_half(c)


rd = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
rd["CUT_FW"].update({str(nt): least(lambda c: one_ok(c, nt), 3000, 30000) for nt in (58, 74)})
rd["LAGSUM"] = {str(nt): {str(k): least(lambda c: upper_ok(c, k, nt), 1000 * k, 1000 * (k + 80)) for k in (8, 16)}
                for nt in (58, 74)}
HERE.joinpath(sys.argv[2]).write_text(json.dumps(rd, indent=1, sort_keys=True) + "\n", encoding="utf-8")
