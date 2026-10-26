"""Question (g): the light's own angular momentum under the lay as the take reversed, read from a v2 record's birth lines: per child the plane's Wronskian W (the intrinsic datum, GP-S1: A B = T div 2) against T div 2; per close the light's own Link records after the far lay, F_re(i, j) = sense A q_j on each of the take's Node's six Links (the im line's record 0: im now is 0), their lattice momentum 2 num_s F along the Link, the moment about the take's Node (0 term by term) and about the board's centre in doubled coordinates, and whether that moment is a multiple of T, of T div 2, or of num_s T (a unit) or of none. Integers only. Usage: lt2_photon.py <record.json> [out.json]"""
import json
import sys

sys.set_int_max_str_digits(0)
AXES = 3


def unwrap(where, at, cube):
    out = []
    for w, a in zip(where, at, strict=True):
        d = (w - a) % cube
        d = d - cube if d > cube // 2 else d
        out.append(a + d)
    return out


def cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


def main(argv):
    d = json.load(open(argv[1]))
    cube = int(d["cube"]) if "cube" in d else int(d["world"]["shape"][0])
    t_ = int(d["T"])
    nums = [int(r["pair"][0]) for r in d["universe"]["rows"] if "pair" in r]
    births = [e for e in d["log"] if e["event"] == "birth"]
    a_ = int(births[0]["amplitude"][0]) if births else 0
    half_t = t_ // 2
    children = children_half_t = 0
    for e in births:
        for w in e["W_children"]:
            children += 1
            children_half_t += abs(int(w)) == half_t
    by_close = {}
    for e in births:
        by_close.setdefault(int(e["i"]), []).append(e)
    centre2 = [cube - 1] * AXES
    links = 0
    j_node_zero = 0
    closes = 0
    mult_t = mult_half = mult_num_t = 0
    max_abs_j = 0
    for i in sorted(by_close):
        entries = by_close[i]
        far = {}
        for e in entries:
            for s, where, _total, q, _rw, _rest in e.get("lay_far", []):
                far[(int(s), tuple(where))] = int(q)
        if not far:
            continue
        closes += 1
        j_c = [0] * AXES
        for e in entries:
            if "far_records" not in e:
                continue
            at = e["node"]
            s = int(e["line_pair"])
            sense = -1 if e["minus"] == at else 1
            for where, _r, _t in e["far_records"]:
                q = far.get((s, tuple(where)), 0)
                links += 1
                f_re = sense * a_ * q
                j_un = unwrap(where, at, cube)
                axis = [k for k in range(AXES) if j_un[k] != at[k]][0]
                side = 1 if j_un[axis] > at[axis] else -1
                p = [0] * AXES
                p[axis] = -side * 2 * nums[s] * f_re
                mid2 = [at[k] + j_un[k] for k in range(AXES)]
                arm_n = [m - 2 * x for m, x in zip(mid2, at, strict=True)]
                j_node_zero += cross(arm_n, p) == [0] * AXES
                arm_c = [m - c for m, c in zip(mid2, centre2, strict=True)]
                j_c = [x + y for x, y in zip(j_c, cross(arm_c, p), strict=True)]
        max_abs_j = max(max_abs_j, max(abs(x) for x in j_c))
        mult_t += all(x % t_ == 0 for x in j_c)
        mult_half += all(x % half_t == 0 for x in j_c)
        mult_num_t += all(x % (nums[int(entries[0]["line_pair"])] * t_) == 0 for x in j_c)
    found = {
        "record": argv[1],
        "T": t_,
        "A, B": births[0]["amplitude"] if births else None,
        "children": children,
        "children with |W| = T div 2 (one child of light, the intrinsic datum)": children_half_t,
        "light's Link records read (F_re = sense A q_j along the Link)": links,
        "links whose moment about the take's Node is 0": j_node_zero,
        "closes with the far lay": closes,
        "closes whose light 2J about the centre is a multiple of T": mult_t,
        "closes whose light 2J about the centre is a multiple of T div 2": mult_half,
        "closes whose light 2J about the centre is a multiple of num_s T": mult_num_t,
        "max |light 2J about the centre|": max_abs_j,
    }
    print(json.dumps(found))
    if len(argv) > 2:
        json.dump(found, open(argv[2], "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
