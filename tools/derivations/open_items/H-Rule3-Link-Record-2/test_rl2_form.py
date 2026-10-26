"""rl2's one test (under 1 s): Rule3's conserved form Q_D = a^T D a + a-^T D a- - a^T D A a- is exact under the leapfrog a+ + a- = A a when D A is symmetric; the head's one-sided reach 2 num p_i^2 Q_ij is exact under D = diag(1 / p_i^2) (the carrier's unit) and every symmetric reach (arith, geom, harm, link) only under D = I: no symmetric reach keeps the law's weighting."""
import subprocess
import sys
from pathlib import Path


def test_rl2_conserved_form_weighting():
    out = subprocess.run([sys.executable, str(Path(__file__).with_name("form_check.py"))], capture_output=True, text=True, check=True).stdout.splitlines()
    exact = {(l.split("  ")[0].strip(), "diag" in l): l.rstrip().endswith(": 0") for l in out}
    assert exact[("head one-sided 2 num p_i^2 Q", True)] and not exact[("head one-sided 2 num p_i^2 Q", False)]
    for name in ("arith num (p_i^2+p_j^2) Q", "geom 2 num p_i p_j Q", "harm 4 num p_i^2 p_j^2 Q / (p_i^2+p_j^2)", "link 2 num p_ij^2 Q (p_ij the mean pace)"):
        assert exact[(name, False)] and not exact[(name, True)], name
