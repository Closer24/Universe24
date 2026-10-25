"""cs4: a reader of cs3's record cyc_c14_q1_400.json at the two bangs: for every Link that reached the lay at an interval, the into-Node, its orbit (x mod 2, y mod 2), its phase class at the seed and at the interval (p + i mod 4), the plane drawn, and the outcome (a birth with taken / booked, or the stop with fall / walls, or the lay's refusal).
Usage: python probe_cs3.py <record.json> i1 i2 ..."""
import json
import sys


def main(argv):
    sys.set_int_max_str_digits(0)
    with open(argv[1], encoding="utf-8") as f:
        rec = json.load(f)
    log = rec["log"]
    lay = next(e for e in log if e["event"] == "lay_pattern")
    phases = lay["phases"]
    cube = int(rec["cube"])
    def p_of(node):
        x, y, z = node
        return phases[(x * cube + y) * cube + z]
    for i in [int(v) for v in argv[2:]]:
        print("interval", i)
        births = [e for e in log if e["event"] == "birth" and e["i"] == i]
        stops = [e for e in log if e["event"] == "refused" and e["cause"] == "stop" and e["i"] == i]
        lays = [e for e in log if e["event"] == "refused" and e["cause"] == "lay" and e["i"] == i]
        landing = [e for e in log if e["event"] == "landing" and e["i"] == i]
        print("  landing:", landing)
        for name, group in (("births", births), ("stops", stops), ("lay refusals", lays)):
            print("  ", name, len(group))
            table = {}
            for e in group:
                n = tuple(e["node"])
                key = (n[0] % 2, n[1] % 2, p_of(n), (p_of(n) + i) % 4, e.get("line_pair", e.get("row")), e.get("taken", e.get("fall")), e.get("booked", e.get("walls")), e.get("children_at_one_node"), e.get("standing"))
                table[key] = table.get(key, 0) + 1
            for k, v in sorted(table.items(), key=lambda kv: str(kv[0])):
                print("     orbit (x%2,y%2)", k[0], k[1], "p_seed", k[2], "p_now", k[3], "plane/row", k[4], "taken|fall", k[5], "booked|walls", k[6], "crowd", k[7], "standing", k[8], "count", v)


if __name__ == "__main__":
    main(sys.argv)
