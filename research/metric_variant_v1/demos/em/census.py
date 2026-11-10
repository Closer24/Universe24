"""Census of the MATTER + EM tensor (manager's binding condition 4/5): a-read monomials per block, physical supports
wider than one link, OD3 placement, designated reads vs force terms (no coincidence), constants, rank."""
from collections import Counter

from emlib import Q0, HOP0, MASS0, save
from research.metric_variant_v1.core import compose
from research.metric_variant_v1.layers.em import build_current_driver, build_em
from research.metric_variant_v1.layers.matter import build_matter, build_static_lapse_mechanism

out = {}
for wil in (0, HOP0 // 8):
    m = build_matter(Q=Q0, hop=HOP0, mass=MASS0, wilson=wil)
    e = build_em(Q=Q0, matter=m, g_phi=4, g_A=1, sigma=2 ** 11 if wil == 0 else 2 ** 8)
    lap = build_static_lapse_mechanism(Q=Q0, matter=m)
    drv = build_current_driver(Q=Q0, em=e, axis=2, kappa=6 * Q0, coupling=1)
    T = compose(m, e, lap, drv)
    names = T.names

    def kind(g):
        n = names[g]
        return "matter" if n.startswith("matter.") else n

    a_reads = Counter()
    for mm in T.monomials:
        if any(f.field == "a" for f in mm.factors):
            a_reads[(kind(mm.target), tuple((kind(f.gear), f.offset, f.field) for f in mm.factors))] += 1
    sup = Counter((names[mm.target], tuple((names[f.gear], f.offset) for f in mm.factors)) for mm in T.support_violations())
    # designated vs undesignated raw terms (per block, before merging): no coincidence allowed
    clash = 0
    for blk in (m, e, lap, drv):
        des, plain = set(), set()
        for t in blk.terms:
            key = (blk.qualify(t[0]), tuple(sorted((blk.qualify(f[0]), tuple(f[1]), f[2]) for f in t[2])))
            (des if len(t) == 4 else plain).add(key)
        clash += len(des & plain)
    od3 = 0
    for g in range(T.G):
        if not names[g].startswith("matter."):
            continue
        per = {}
        for mm in T.monomials:
            if mm.target == g and mm.degree == 1 and mm.factors[0].offset != (0, 0, 0):
                per.setdefault(mm.factors[0].offset, set()).add(mm.factors[0].gear)
        od3 = max([od3] + [len(v) for v in per.values()])
    out[f"wilson={wil}"] = dict(
        G=T.G, monomials=len(T), rank=T.rank, census=T.census(), constants=int(T.has_constant),
        a_read_patterns={f"{k[0]} <- {k[1]}": v for k, v in sorted(a_reads.items())},
        a_read_total=sum(a_reads.values()), support_wider_than_link=len(T.support_violations()),
        support_patterns=sorted({f"{k[0]} <- {[x[0] for x in k[1]]}" for k in sup}),
        designated=len(T.designations), designated_vs_force_term_coincidences=clash,
        od3_max_distinct_gears_per_face_neighbour=od3, stages=[[names[i] for i in s] for s in T.stages])
save("EM-census", out)
for k, v in out.items():
    print(k, {kk: vv for kk, vv in v.items() if kk not in ("a_read_patterns",)})
    for p, c in v["a_read_patterns"].items():
        print("   ", c, p)
