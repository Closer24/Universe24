"""Optional rank-four transported probe and clock candidate; no Einstein claim."""
from universe24.core import Tensor

ZERO, PLUS_Z, MINUS_Z = (0, 0, 0), (0, 0, 1), (0, 0, -1)
COFRAME = tuple(f"E{a}{mu}" for a in range(4) for mu in range(4))
CLOCKS = ("control", "candidate")


def build():
    """One fixed tensor, including metric-dependent cubic clock terms.

    R(X,Y)=(Q Y,S X), Q=[[0,-1],[1,k]], det Q=1.
    u=3(R+R^-1)b embeds this map on a=R^-1 b for static geometry.
    k=0 for the control; k=-g_tt for the candidate. This choice of clock
    coupling is a hypothesis tested (and rejected off axis) by the runner.
    """
    names = list(COFRAME) + ["probe.X", "probe.Y"]
    names += [f"{clock}.{bank}{j}" for clock in CLOCKS for bank in ("X", "Y") for j in (0, 1)]
    terms = []
    def f(name, offset=ZERO):
        return (name, offset, "b")
    for name in COFRAME:
        terms.append((name, 6, (f(name),)))
    terms += [("probe.X", 3, (f("probe.Y"),)),
              ("probe.X", 3, (f("probe.Y", PLUS_Z),)),
              ("probe.Y", 3, (f("probe.X"),)),
              ("probe.Y", 3, (f("probe.X", MINUS_Z),))]
    designation = {"designated_one_way":
                   "Prepared clock transport and test-clock geometry coupling; no backreaction or force potential."}
    for clock in CLOCKS:
        x0, x1, y0, y1 = [f"{clock}.{bank}{j}" for bank in ("X", "Y") for j in (0, 1)]
        linear = [(x0, -3, y1, ZERO), (x0, 3, y0, PLUS_Z),
                  (x1, 3, y0, ZERO), (x1, 3, y1, PLUS_Z),
                  (y0, 3, x0, MINUS_Z), (y0, 3, x1, ZERO),
                  (y1, 3, x1, MINUS_Z), (y1, -3, x0, ZERO)]
        terms += [(target, c, (f(source, offset),), designation)
                  for target, c, source, offset in linear]
        if clock == "candidate":
            # -g_tt = E00^2-E10^2-E20^2-E30^2, evaluated from old state.
            for a, sign in enumerate((1, -1, -1, -1)):
                for target, source in ((x1, y1), (y0, x0)):
                    terms.append((target, 3*sign,
                                  (f(f"E{a}0"), f(f"E{a}0"), f(source)), designation))
    return Tensor(names, terms, strict_support=True)
