"""The cycle pattern's symmetry on the 4-cube, in integers: every map Node -> Node of the form x -> g x + t (g one of the cube's 48 signed permutations, t a translation of Z_4^3) under which the phase digit transforms as p -> s p + c (s = 1 a global quarter turn c of the plane, which the step is covariant under by CS4-S2; s = -1 the conjugation, the C P mirror) is listed, the group's size and its orbits on the 64 Nodes counted; the same for the pattern with the hole's digit at the class 0 (the holed Nodes marked) and for the hole at the origin."""
import itertools

P1 = [0, 0, 1, 1, 2, 2, 3, 3, 1, 1, 0, 0, 3, 3, 2, 2]
N = 4


def phase(x, y, z):
    return (P1[4 * (x % 4) + (y % 4)] + z) % 4


NODES = [(x, y, z) for x in range(N) for y in range(N) for z in range(N)]
G48 = []
for perm in itertools.permutations(range(3)):
    for signs in itertools.product((1, -1), repeat=3):
        G48.append((perm, signs))


def act(g, t, at):
    perm, signs = g
    return tuple((signs[a] * at[perm[a]] + t[a]) % N for a in range(3))


def symmetries(marked):
    """The maps preserving the phase up to (s, c) and mapping the marked set onto itself."""
    found = []
    for g in G48:
        for t in itertools.product(range(N), repeat=3):
            for s in (1, -1):
                cs = {(phase(*act(g, t, at)) - s * phase(*at)) % 4 for at in NODES}
                if len(cs) == 1 and {act(g, t, at) for at in marked} == set(marked):
                    found.append((g, t, s, cs.pop()))
    return found


def orbits(group):
    seen, found = set(), []
    for at in NODES:
        if at in seen:
            continue
        orbit = {act(g, t, at) for g, t, _s, _c in group}
        seen |= orbit
        found.append(len(orbit))
    return found


for name, marked in (("ga2, no hole", []), ("hole at the class 0", [at for at in NODES if phase(*at) == 0]), ("hole at the origin", [(0, 0, 0)]), ("hole at every Node", NODES), ("hole at the even lattice", [at for at in NODES if all(v % 2 == 0 for v in at)])):
    full = symmetries(marked)
    turns = [m for m in full if m[2] == 1]
    print(f"{name}: maps preserving the pattern up to a quarter turn {len(turns)} (orbits on the 64 Nodes: {orbits(turns)}); with the conjugation too {len(full)} (orbits: {orbits(full)})")
