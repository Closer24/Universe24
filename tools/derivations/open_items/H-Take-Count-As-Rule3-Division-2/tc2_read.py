"""tc2's reader of a record written by tc2_record.py: the laws in the clicks from the log alone. Per record: the births and credits; the
exact take (EX-S1): taken >= owed and taken - owed == the new remainder at every birth and credit; the children's Wronskian odd under
the slot exchange (CA-S1: the lay on the exchanged slots gives -W) and nonzero; the lattice momentum at every birth: the P balance
dP_take + the two lays' dP (0 where exact) and its size in permille of the take's recoil (an integer quotient), the moment 2J about the
taker from the two ends' lays (cross(2 r, dP) in Link-halves, coordinates unwrapped about the taker); the run back. With a second record
the course against it: the births' intervals and Nodes, the first apart interval. Usage: tc2_read.py <record.json> [against.json]"""
import json, sys
sys.set_int_max_str_digits(0)


def cross3(r, p):
    return [r[1] * p[2] - r[2] * p[1], r[2] * p[0] - r[0] * p[2], r[0] * p[1] - r[1] * p[0]]


def read(path):
    r = json.load(open(path))
    cube, log = int(r["cube"]), r["log"]
    births = [e for e in log if e["event"] == "birth"]
    credits = [e for e in log if e["event"] == "credit"]
    c = dict(record=path, flag=r["flag"], hash=r["hash"], births=len(births), credits=len(credits), run_back=r["run_back"], of=r["of"],
             takes=r["takes"], refused_stop=r["counts"]["refused_stop"], turns=r["counts"]["turns"])
    takes = [e for e in births + credits if "owed" in e]
    c["taken_ge_owed"] = sum(int(e["taken"]) >= int(e["owed"]) for e in takes)
    c["taken_minus_owed_is_remainder"] = sum(int(e["taken"]) - int(e["owed"]) == int(e["remainder"]) for e in takes)
    c["of_takes_logged"] = len(takes)
    c["levels_moved"] = sum(int(e["levels"]) for e in takes)
    odd = nonzero = 0
    for e in births:
        a, b = e["amplitude"]
        for stood, sense, w_end in zip(e["stood"], (-1, 1), e["W_children"]):
            rn, rb, inn, ib = stood
            w_now = (rn + sense * a) * (ib + b) - inn * rb
            w_x = rn * ib - (inn + b) * (rb + sense * a)
            odd += w_now == int(w_end) and w_x == -w_now
            nonzero += w_now != 0
    c["W_odd_under_exchange"], c["W_nonzero"], c["of_children"] = odd, nonzero, 2 * len(births)
    p_exact = j_exact = 0
    max_permille = 0
    for e in births:
        dpt = [int(x) for x in e["dP_take"]]
        ends = [[int(x) for x in v] for v in e["dP_lay_ends"]]
        p = [dpt[k] + ends[0][k] + ends[1][k] for k in range(3)]
        p_exact += p == [0, 0, 0]
        scale = max(1, max(abs(x) for x in dpt))
        max_permille = max(max_permille, max(abs(x) for x in p) * 1000 // scale)
        at = e["node"]
        j2 = [0, 0, 0]
        for n, dp in zip((e["minus"], e["plus"]), ends):
            rel = [((n[k] - at[k] + cube // 2) % cube) - cube // 2 for k in range(3)]
            j2 = [x + y for x, y in zip(j2, cross3([2 * x for x in rel], dp))]
        j_exact += j2 == [0, 0, 0]
    c["P_balance_exact"], c["J_about_taker_exact"], c["max_P_balance_permille_of_recoil"] = p_exact, j_exact, max_permille
    c["birth_intervals"] = [e["i"] for e in births]
    return c, births


a, ba = read(sys.argv[1])
if len(sys.argv) > 2:
    b, bb = read(sys.argv[2])
    ka = [(e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"])) for e in ba]
    kb = [(e["i"], tuple(e["node"]), e["line_pair"], tuple(e["minus"]), tuple(e["plus"])) for e in bb]
    same = sum(1 for k in ka if k in kb)
    apart = sorted(set(ka) ^ set(kb))
    a["against"] = dict(record=sys.argv[2], births_there=len(kb), births_shared=same, first_apart_interval=None if not apart else apart[0][0],
                        hash_equal=a["hash"] == b["hash"], credits_there=b["credits"])
print(json.dumps(a, default=str))
