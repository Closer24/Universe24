"""Hand dn1: the record's den (examples/events/universe24, 154 bits) beside the toy's den (54 bits, the control): the circle (the primes 1 mod 4, the lifts, the legs, the gaps), the ratios against nature, every wall's bit length (the integers that carry den), the conversion lists of the law (conversion.birth_of, conversion.lists_of, and the plane parent's exact lists for n -> p + e), and the toy's universe and world files written in the toy's format. Integers only: every ratio a quotient at a named scale with its remainder; no float.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/dn1/den_record.py
"""

from __future__ import annotations

import json
import sys
import time
from itertools import combinations_with_replacement, product
from pathlib import Path

sys.set_int_max_str_digits(0)

from event_universe import conversion
from event_universe.core.rule3 import largest_below, wall_of
from event_universe.loader.circle import circle_points, factors, lift_points, two_squares
from event_universe.loader.universe import universe_of

HERE = Path(__file__).resolve().parent
GAMMA, T, G = 1000, 36000, 16
RECORD = 21397363965165989151899244775347635252768274397  # examples/events/universe24/universe_universe24.json
CONTROL = 15162856759112389  # the toy's universe_toy.json
NATURE_P_OVER_E_PER_1E9 = 1836152673  # m_p / m_e = 1836.15267343
NATURE_N_OVER_P_PER_1E9 = 1001378419  # m_n / m_p = 1.00137841931
WIDTH = 128


def quotient(a: int, b: int, scale: int) -> list[int]:
    """a / b at the scale as [quotient, remainder] of (a x scale) div b: the integer reading."""
    q, r = divmod(a * scale, b)
    return [int(q), int(r)]


def bits(x: int) -> int:
    return int(abs(x)).bit_length()


def circle_of(den: int) -> dict:
    primes = factors(den)
    lifts = list(lift_points(den))  # the file's order: the engine's lift order
    rows = []
    for vector, num, s in lifts:
        gap = den - num
        rows.append(
            {
                "vector": list(vector),
                "prime": [p for p, e in sorted(primes.items()) if p % 4 == 1][list(vector).index(2)],
                "num": num,
                "s": s,
                "gap": gap,
                "g_milli": quotient(gap, den, 1000),
                "g_per_1e15": quotient(gap, den, 10**15),
                "g_per_1e24": quotient(gap, den, 10**24),
                "intervals_per_radian_den_div_s": quotient(den, s, 1),
                "compton_milli_links_isqrt_den2_over_3s2": largest_below((den * den * 10**6) // (3 * s * s)),
                "quantum_wall_3Ts": 3 * T * s,
                "quantum_wall_bits": bits(3 * T * s),
                "mass_D_at_vacuum_12_gap_Gamma2_G2": 12 * gap * GAMMA * GAMMA * G * G,
                "mass_D_bits": bits(12 * gap * GAMMA * GAMMA * G * G),
            }
        )
    by_leg = sorted(rows, key=lambda r: r["s"])
    ratios = {}
    if len(by_leg) == 3:
        e, p, n = by_leg
        ratios = {
            "lightest_over_middle_over_heaviest_vectors": [e["vector"], p["vector"], n["vector"]],
            "p_over_e_per_1e9": quotient(p["s"], e["s"], 10**9),
            "nature_p_over_e_per_1e9": NATURE_P_OVER_E_PER_1E9,
            "p_over_e_miss_per_1e9": quotient(p["s"], e["s"], 10**9)[0] - NATURE_P_OVER_E_PER_1E9,
            "n_over_p_per_1e9": quotient(n["s"], p["s"], 10**9),
            "nature_n_over_p_per_1e9": NATURE_N_OVER_P_PER_1E9,
            "n_over_p_miss_per_1e9": quotient(n["s"], p["s"], 10**9)[0] - NATURE_N_OVER_P_PER_1E9,
            "n_over_e_per_1e9": quotient(n["s"], e["s"], 10**9),
            "beats_ratio_is_leg_ratio": "the beat per period of a rest rotation is 2 pi den / s intervals; the ratio of two lifts' beats is the inverse ratio of their legs (the mass ratio) to the rounding of a period",
            "p_over_e_from_intervals_per_radian_per_1e6": quotient(e["intervals_per_radian_den_div_s"][0], p["intervals_per_radian_den_div_s"][0], 10**6),
        }
    w = wall_of(den, GAMMA, G)
    W_c = 3 * den * T
    walls = {
        "den": {"value": den, "bits": bits(den)},
        "w_6_den_Gamma2_G2": {"value": w, "bits": bits(w)},
        "W_c_3_den_T": {"value": W_c, "bits": bits(W_c)},
        "one_link_read_modulus_3_W_c": {"bits": bits(3 * W_c)},
        "volume_time_write_wall_54_den_Gamma4_T": {"bits": bits(54 * den * GAMMA**4 * T)},
        "volume_axis_write_wall_54_den_T_Gamma2": {"bits": bits(54 * den * T * GAMMA**2)},
        "sign_write_wall_T": {"bits": bits(T)},
        "phase_wall_2": {"bits": bits(2)},
        "volume_pair_den_minus_den_div_Gamma": {"num": den - den // GAMMA, "gap": den // GAMMA, "bits": bits(den)},
        "reach_R_at_vacuum_2_num_Gamma2_G2_light": {"bits": bits(2 * den * GAMMA * GAMMA * G * G)},
        "own_S_light_2w_minus_6R_at_vacuum": {"value": 2 * w - 12 * den * GAMMA * GAMMA * G * G, "bits": bits(2 * w - 12 * den * GAMMA * GAMMA * G * G)},
        "level_room_within_128_bits_under_w": {"bits_left_for_a_level_times_w": WIDTH - bits(w)},
        "den_bits_at_which_w_passes_128": 128 - bits(6 * GAMMA * GAMMA * G * G) + 1,
    }
    for r in rows:
        r["num_bits"] = bits(r["num"])
        r["s_bits"] = bits(r["s"])
    return {
        "den": den,
        "den_bits": bits(den),
        "primes_1_mod_4_with_two_squares": {str(p): {"exponent": e, "a_b": list(two_squares(p)), "bits": bits(p)} for p, e in sorted(primes.items()) if p % 4 == 1},
        "points_in_the_open_quadrant": len(circle_points(den)),
        "lifts_in_the_file_order": rows,
        "ratios": ratios,
        "walls": walls,
    }


def gaussian(num: int, den: int) -> tuple[int, int]:
    found = conversion.gaussian((num, den))
    assert found is not None
    return found


def plane_parent_lists(den: int, bound: int) -> dict:
    """The exact lists a plane parent (a lift at the sense +1) could convert into among the circle's points at their senses (the law's rotation exactness: the children's Gaussian product equals the parent's point scaled by den^(children - 1), exact; the charge: the senses summed equal the parent's; no three-line record in this toy, so the baryon count is 0 = 0), up to `bound` children. Derived from conversion.py's clause with the engine's own `gaussian` and `times`."""
    points = circle_points(den)
    lifts = {tuple(v): (num, s) for v, num, s in lift_points(den)}
    names = {}
    for v, num, s in points:
        names[(num, s)] = "lift " + str(list(v)) if tuple(v) in lifts else "point " + str(list(v))
    out = {}
    for v, num, s in lift_points(den):
        parent = (num, s)
        found = []
        for size in range(1, bound + 1):
            for outs in combinations_with_replacement(range(len(points)), size):
                for senses in product((-1, 1), repeat=size):
                    if sum(senses) != 1:
                        continue
                    table = tuple(sorted(zip(outs, senses)))
                    if table in found:
                        continue
                    point = (1, 0)
                    for k, sense in table:
                        _v, n_k, s_k = points[k]
                        point = conversion.times(point, (n_k, sense * s_k))
                    if point == (parent[0] * den ** (size - 1), parent[1] * den ** (size - 1)):
                        found.append(table)
        out[names[parent]] = {
            "lists": [[(names[(points[k][1], points[k][2])], sense) for k, sense in table] for table in found],
            "count": len(found),
        }
    return out


def conversion_lists(den: int, bound: int) -> dict:
    """The engine's own lists at this den: birth_of for the massless parent (the lifts' conjugate pairs, the lightest first) and lists_of for two massless quanta up to `bound` children, with the time each took in integer milliseconds."""
    t0 = time.monotonic_ns()
    integers, families = universe_of({"integers": {"den": den, "node_clock": GAMMA, "quantum_action": T}})
    loaded_ms = (time.monotonic_ns() - t0) // 10**6
    massless = next(k for k, f in enumerate(families) if f.pair[0] == f.pair[1] and not f.held)
    lifts = {num for _v, num, _s in lift_points(den)}
    label = lambda k: families[k].name + (" (lift)" if families[k].pair[0] in lifts else "")
    t1 = time.monotonic_ns()
    births = conversion.birth_of(families, massless)
    births_ms = (time.monotonic_ns() - t1) // 10**6
    t2 = time.monotonic_ns()
    lists = conversion.lists_of(families, 2, bound)
    lists_ms = (time.monotonic_ns() - t2) // 10**6
    return {
        "families": len(families),
        "load_ms": loaded_ms,
        "birth_of(massless)": [[(label(k), sense) for k, sense in table] for table in births],
        "birth_of_ms": births_ms,
        "lists_of(2 quanta, bound %d)" % bound: {"count": len(lists), "sizes": sorted({len(t) for t in lists}), "first_six": [[(label(k), sense) for k, sense in table] for table in lists[:6]], "ms": lists_ms},
        "lifts_born_as_conjugate_pairs": sorted({label(k) for table in births for k, _s in table}),
        "every_lift_born": {families[k].pair[0] for table in births for k, _s in table} == lifts,
    }


def write_files(record: dict, control: dict) -> None:
    def universe(c: dict) -> dict:
        den = c["den"]
        rows = [{"shape": 2, "pair": [den, den]}]
        rows += [{"shape": 2, "pair": [r["num"], den]} for r in c["lifts_in_the_file_order"]]
        rows += [{"shape": 10, "pair": [den - den // GAMMA, den]}, {"shape": 4, "pair": [den, den]}, {"shape": 1, "wall": 2}]
        return {"integers": {"den": den, "node_clock": GAMMA, "quantum_action": T, "link_unit": G}, "rows": rows}

    def hole(universe_file: str, cube: int, intervals: int, den: int) -> dict:
        return {"universe": universe_file, "shape": [cube, cube, cube], "intervals": intervals, "seed": [{"lay": "sea", "row": [den, den]}, {"lay": "hole", "at": [0, 0, 0]}, {"lay": "at", "row": [den, den], "centre": [1, 0, 0], "quanta": 1}]}

    def bodies(universe_file: str, cube: int, intervals: int, den: int, heavy_num: int) -> dict:
        return {"universe": universe_file, "shape": [cube, cube, cube], "intervals": intervals, "seed": [{"lay": "sea", "row": [den, den]}, {"lay": "at", "row": [heavy_num, den], "centre": [3, 3, 2], "width": 2, "quanta": 125}, {"lay": "at", "row": [heavy_num, den], "centre": [3, 3, 5], "width": 2, "quanta": 125}]}

    for tag, c in (("record", record), ("control", control)):
        (HERE / f"universe_{tag}.json").write_text(json.dumps(universe(c), indent=1) + "\n")
        den = c["den"]
        for cube, intervals in ((3, 120), (5, 120)):
            (HERE / f"world_{tag}_hole{cube}.json").write_text(json.dumps(hole(f"universe_{tag}.json", cube, intervals, den)) + "\n")
        heavy = max(c["lifts_in_the_file_order"], key=lambda r: r["gap"])  # the heaviest lift by its gap: the proton's at the record's den, (2, 0, 0) at the control
        (HERE / f"world_{tag}_bodies7.json").write_text(json.dumps(bodies(f"universe_{tag}.json", 7, 60, den, heavy["num"])) + "\n")


def main() -> None:
    out = {}
    for tag, den in (("record", RECORD), ("control", CONTROL)):
        t0 = time.monotonic_ns()
        c = circle_of(den)
        c["circle_ms"] = (time.monotonic_ns() - t0) // 10**6
        t1 = time.monotonic_ns()
        c["plane_parent_exact_lists_up_to_3_children"] = plane_parent_lists(den, 3)
        c["plane_parent_lists_ms"] = (time.monotonic_ns() - t1) // 10**6
        c["engine_conversion"] = conversion_lists(den, 2)
        out[tag] = c
    write_files(out["record"], out["control"])
    (HERE / "den_record.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
    # the text summary
    lines = []
    for tag in ("record", "control"):
        c = out[tag]
        lines.append(f"== {tag}: den {c['den']} ({c['den_bits']} bits), primes {list(c['primes_1_mod_4_with_two_squares'].keys())}, points {c['points_in_the_open_quadrant']}")
        for r in c["lifts_in_the_file_order"]:
            lines.append(f"  lift {r['vector']} prime {r['prime']}: num bits {r['num_bits']}, s bits {r['s_bits']}, g {r['g_milli'][0]}/1000, g per 1e15 {r['g_per_1e15'][0]}, den div s {r['intervals_per_radian_den_div_s'][0]} (intervals per radian), Compton {r['compton_milli_links_isqrt_den2_over_3s2']} milli-Links, quantum wall 3Ts {r['quantum_wall_bits']} bits, D at vacuum {r['mass_D_bits']} bits")
        for k, v in c["ratios"].items():
            lines.append(f"  {k}: {v}")
        for k, v in c["walls"].items():
            lines.append(f"  wall {k}: {v}")
        for parent, found in c["plane_parent_exact_lists_up_to_3_children"].items():
            lines.append(f"  exact lists of the plane parent {parent} (sense +1), up to 3 children: {found['count']}: {found['lists']}")
        lines.append(f"  engine conversion: {c['engine_conversion']}")
        lines.append(f"  times ms: circle {c['circle_ms']}, plane parent lists {c['plane_parent_lists_ms']}")
    text = "\n".join(lines) + "\n"
    (HERE / "den_record.txt").write_text(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
