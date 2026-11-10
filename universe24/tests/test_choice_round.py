"""TC.19b (NOTES_choice.md amendment 10:57:13 UTC): the round-cone F7 (time-difference source, rho0 = 0.75), A = 30.

    OMP_NUM_THREADS=2 nice -n 10 python -m unittest universe24.tests.test_choice_round -v
"""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from universe24.demos.choice.round_cone import exp_f7_round  # noqa: E402

RES = Path("runs/tests") / "choice"


def stamp():
    return subprocess.run(["date", "-u"], capture_output=True, text=True).stdout.strip()


class TestChoiceRound(unittest.TestCase):
    def test_TC19b_round_cone_f7(self):
        t0 = stamp()
        r = exp_f7_round(30, rho0=0.75)
        r["_started"], r["_finished"] = t0, stamp()
        RES.mkdir(parents=True, exist_ok=True)
        (RES / "TC.19b.json").write_text(json.dumps(r, indent=1))
        self.assertTrue(r["odd"] and r["rewind_all_runs"] and r["recip_ok"])
        for t in range(9):
            self.assertEqual(r["per_tB"][str(t)]["max|E|"], 0.0, t)
        for t in (9, 10):
            self.assertLessEqual(r["per_tB"][str(t)]["maxS"], 2.0)
        self.assertLessEqual(max(r["per_tB"][str(t)]["maxS"] for t in range(51)), 2 * 2 ** 0.5)
        rho = [r["per_tB"][str(t)]["rho"] for t in range(30, 51)]
        self.assertTrue(0.7 <= min(rho) and max(rho) <= 1.0, rho)


if __name__ == "__main__":
    unittest.main()
