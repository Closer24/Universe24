"""lc1: the summary of a course file (lc1_course.py's out.json), integers only: the mean volume's tops and returns to the
seed's sum, the first turn (interval, Nodes, e before / at / after, the carrier's Links' sums around it), the Links' sums'
extremes, the residues in per mille, the spread's course, births and credits. Usage: lc1_read.py <course.json> [seed X sum]."""
import json
import sys


def permille(num, abs_sum):
    return 0 if abs_sum == 0 else (1000 * num) // abs_sum


def main(argv):
    sys.set_int_max_str_digits(0)
    rows = json.load(open(argv[1]))
    seed_sum = int(argv[2]) if len(argv) > 2 else rows[0]["X sum"]
    sums = [r["X sum"] for r in rows]
    tops = [(rows[k]["i"], sums[k]) for k in range(1, len(rows) - 1) if sums[k - 1] <= sums[k] and sums[k] > sums[k + 1]]
    falls = [rows[k]["i"] for k in range(1, len(rows)) if sums[k] < sums[k - 1]]
    returns = [(rows[k]["i"], sums[k]) for k in range(1, len(rows)) if sums[k] <= seed_sum and sums[k - 1] > seed_sum]
    first_turn = next((k for k, r in enumerate(rows) if r["turns at i"] > 0), None)
    out = {
        "intervals": len(rows),
        "seed X sum": seed_sum,
        "X sum at the end": sums[-1],
        "X sum min / max": [min(sums), max(sums)],
        "tops (interval, X sum)": tops[:12],
        "falling intervals count": len(falls),
        "first falling interval": falls[0] if falls else None,
        "returns to the seed's sum (interval, X sum)": returns[:12],
        "X min / max at the end": [rows[-1]["X min"], rows[-1]["X max"]],
        "e course (i, e, e max)": [(r["i"], r["e"], r["e max"]) for r in rows if r["i"] in (1, 5, 10, 20, 30, 50, 100, 150, 200, 220, 250, 300, 400)],
        "carrier links num: max |.| / abs max": [max(abs(r["carrier links num"]) for r in rows), max(r["carrier links abs"] for r in rows)],
        "carrier links quot sum over the run": sum(r["carrier links quot"] for r in rows),
        "carrier links quot min / max": [min(r["carrier links quot"] for r in rows), max(r["carrier links quot"] for r in rows)],
        "carrier links quot negative intervals": sum(1 for r in rows if r["carrier links quot"] < 0),
        "carrier weighted residue per mille: max |.|": max(abs(permille(r["carrier links wnum"], r["carrier links wabs"])) for r in rows),
        "identity X p^2 - Gamma^3: max |.| over the run": max(r["ident max"] for r in rows),
        "sea kick residue per mille: max |.|": max(abs(permille(r["sea kick num"], r["sea kick abs"])) for r in rows),
        "sea kick num sum over the run": sum(r["sea kick num"] for r in rows),
        "sea kick abs max": max(r["sea kick abs"] for r in rows),
        "mass pull sum max": max(r["mass pull sum"] for r in rows),
        "write sum min / max": [min(r["write sum"] for r in rows), max(r["write sum"] for r in rows)],
        "forms gap0 at the end": rows[-1]["forms gap0"],
        "turns total": sum(r["turns at i"] for r in rows),
        "births / credits at the end": [rows[-1]["births"], rows[-1]["body_clicks"]],
        "frozen at the end": rows[-1]["frozen"],
    }
    if first_turn is not None:
        k = first_turn
        around = [rows[j] for j in range(max(0, k - 1), min(len(rows), k + 3))]
        out["first turn"] = {
            "interval": rows[k]["i"],
            "nodes": rows[k]["turned"],
            "count": rows[k]["turns at i"],
            "e before / at / after / after2": [r["e"] for r in around],
            "e max before / at / after / after2": [r["e max"] for r in around],
            "carrier links quot before / at / after / after2": [r["carrier links quot"] for r in around],
            "carrier links num before / at / after / after2": [r["carrier links num"] for r in around],
            "sea kick num before / at / after / after2": [r["sea kick num"] for r in around],
            "X sum before / at / after / after2": [r["X sum"] for r in around],
        }
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv)
