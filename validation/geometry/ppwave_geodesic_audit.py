"""Optional independent symbolic check; requires the validation extra (SymPy).

Derives the connection from the metric, checks the continuous geodesics,
then compares actual engine outputs to algebraic powers, not another copy
of the integer recurrence. This is an audit, never a runtime dependency.
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from validation.geometry import ppwave_geodesic_clock as experiment


def audit():
    import sympy as s
    U, V, X, Y = s.symbols("U V X Y", real=True)
    c, epsilon = s.symbols("c epsilon", real=True)
    length = s.symbols("length", positive=True)
    coords = [U, V, X, Y]
    metric = s.Matrix([[c*(X**2-Y**2),-1,0,0],[-1,0,0,0],
                       [0,0,1,0],[0,0,0,1]])
    inverse = metric.inv()
    connection = [[[s.simplify(sum(inverse[a,d]*(
        s.diff(metric[d,b], coords[k])+s.diff(metric[d,k], coords[b])
        -s.diff(metric[b,k], coords[d])) for d in range(4))/2)
        for k in range(4)] for b in range(4)] for a in range(4)]
    for value in (0, 1):
        curve = s.Matrix([U, (value*s.cosh(U)*s.sinh(U)/length**2+epsilon*U)/2,
                          (1-value+value*s.cosh(U))/length, 0])
        velocity = curve.diff(U)
        acceleration = velocity.diff(U)
        substitution = {c:value, V:curve[1], X:curve[2], Y:0}
        for a in range(4):
            residual = s.simplify(acceleration[a]+sum(
                connection[a][b][k].subs(substitution)*velocity[b]*velocity[k]
                for b in range(4) for k in range(4)))
            assert residual == 0
        assert s.simplify((velocity.T*metric.subs(substitution)*velocity)[0]) == -epsilon
    report = experiment.run()
    for case in report["cases"]:
        for row in case["decoded"]:
            n = row["n"]
            if case["curvature"]:
                plus, minus = (s.expand((2+sign*s.sqrt(3))**n) for sign in (1,-1))
                q, p = s.simplify((plus+minus)/2), s.simplify((plus-minus)/(2*s.sqrt(3)))
            else:
                q, p = 1, 0
            assert row["q"] == q and row["p"] == p and row["product"] == q*p
    return dict(symbolic_geodesic_equations=8, all_residuals_zero=True,
                norm_is_minus_epsilon=True, engine_cases=len(report["cases"]),
                samples_compared=sum(len(case["decoded"]) for case in report["cases"]))


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
