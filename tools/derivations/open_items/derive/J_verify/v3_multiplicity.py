"""J_verify v3: a train whose hand is a kind with an internal two-fold label (two flavours, two levels or two
senses at one Node-clock) has more than one directionless pair dial, and one of each symmetry, so the pair
dial no longer selects eps. Integers only. python3 -I v3_multiplicity.py (must end with 0 failures)."""
import sys
import importlib.util
spec = importlib.util.spec_from_file_location("v1", __file__.replace("v3_multiplicity.py", "v1_kinds.py"))
v1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v1)
FAIL = []
def check(name, ok, info):
    if not ok:
        FAIL.append(name)
    print(f"  [{'ok' if ok else 'FAILED'}] {name}: {info}")
K = v1.kinds()
for name in ("E1/2", "T1", "A1", "G3/2"):
    gens, spinor = K[name]
    s2 = 2 if spinor else 1
    g2 = [v1.kron(g, v1.ident(2)) for g in gens]
    tot = v1.nullity_bilinear(g2, s2)
    sym = v1.nullity_bilinear(g2, s2, "sym")
    alt = v1.nullity_bilinear(g2, s2, "alt")
    check(f"{name} with a two-fold internal label: invariant bilinears of both symmetries (the dial exists for eps = +1 and -1)", tot == 4 and sym > 0 and alt > 0, f"{tot} total, {sym} symmetric, {alt} antisymmetric")
print("result:", f"{len(FAIL)} failures")
raise SystemExit(1 if FAIL else 0)
