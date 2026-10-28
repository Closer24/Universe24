"""Probe: T S T = S^-1 for the time gear's step, every state counted, pure integers (Animate, the many bangs).

The time gear's step (the regulator: its own teeth, no meshes, the hold 2 teeth; draft C, section 1):
    X+ = 2 X - X- + q,   q, r_d' = carry(N + r_d, T_d)       (the drive's floor carry, its fine tooth kept)
with N the push read at the tick's start, the same forward and on the turned state (the forms are their own image
under the exchange: the engine's symmetric form). The turnover T exchanges the two slots and turns the drive's fine
tooth by a rule m. The retrace after a top needs S(T(s+)) = T(s) for s+ = S(s). Checked here for two rules m:
  flip    r -> T_d - 1 - r            (the rule the engine applies to the regulator's own fine tooth)
  mirror  r -> (2 mid - r) mod T_d    (the rule the engine applies to the drive's fine tooth, mid = T_d div 2)
at every teeth count T_d from 8 to 15, every fine tooth r_d in [0, T_d), every push N in [-3 T_d, 3 T_d] and
X-, X in a small range. A mutant (the turnover that keeps the fine tooth) must fail.
"""


def carry(total, teeth, fine):
    u = total + fine
    return u // teeth, u % teeth


def step(state, n, teeth):
    before, now, r = state
    q, r2 = carry(n, teeth, r)
    return now, 2 * now - before + q, r2


def turn(state, teeth, rule):
    before, now, r = state
    return now, before, rule(r, teeth)


RULES = {
    "flip": lambda r, w: w - 1 - r,
    "mirror": lambda r, w: (2 * (w // 2) - r) % w,
    "kept (mutant)": lambda r, w: r,
}


def main():
    print("teeth  rule            states  retrace fails  where the fails sit")
    for teeth in range(8, 16):
        for name, rule in RULES.items():
            count = fails = 0
            sites = set()
            for r in range(teeth):
                for n in range(-3 * teeth, 3 * teeth + 1):
                    for before in range(-2, 3):
                        for now in range(-2, 3):
                            s = (before, now, r)
                            s1 = step(s, n, teeth)
                            back = step(turn(s1, teeth, rule), n, teeth)
                            count += 1
                            if back != turn(s, teeth, rule):
                                fails += 1
                                sites.add("r = 0" if r == 0 else ("r' = 0" if s1[2] == 0 else "other"))
            print(f"{teeth:5d}  {name:14s}  {count:6d}  {fails:13d}  {sorted(sites) if sites else '-'}")


if __name__ == "__main__":
    main()
