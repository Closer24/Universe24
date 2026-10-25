"""cs4: the universe files, every gapped pair a point of den's circle (circle.txt of cs3; the loader refuses a pair off it): the toy's integers and its carrier, shape-4 and walled rows kept; the gapped rows chosen by the stop's condition (the walls 6 T s against the one take at the into-end).
  universe_lift.json: the light and the light lift alone (2 records): the draw mod 2.
  universe_l4.json: the light and the four points with num above s whose walls one take can pay at one quantum (s 8137489624680, 115762739551980, 123899975345340, 132037175453340).
  universe_l3.json: the light and the three points in one level bracket at two quanta (s 115762739551980, 123899975345340, 132037175453340).
  universe_l3h.json: universe_l3 with the toy's two heavy rows (the owner's matter) beside them.
Usage: python files.py <universe_toy.json> <out_dir>"""
import json
import sys

sys.set_int_max_str_digits(0)
toy = json.load(open(sys.argv[1], encoding="utf-8"))
den = int(toy["integers"]["den"])
light = [r for r in toy["rows"] if r["shape"] == 2 and r["pair"][0] == r["pair"][1]]
tail = [r for r in toy["rows"] if r["shape"] != 2]
heavy = [r for r in toy["rows"] if r["shape"] == 2 and r["pair"][0] in (2458210083751875, 2580388913625285)]
lift = [{"shape": 2, "pair": [15162854575528411, den]}]
three = [{"shape": 2, "pair": [n, den]} for n in (15162414850065661, 15162350539855939, 15162281862624061)]
files = {
    "universe_lift.json": light + lift,
    "universe_l4.json": light + lift + three,
    "universe_l3.json": light + three,
    "universe_l3h.json": light + three + heavy,
}
for name, rows in files.items():
    u = {"integers": dict(toy["integers"]), "rows": rows + tail}
    json.dump(u, open(f"{sys.argv[2]}/{name}", "w", encoding="utf-8"))
    print(name, "gapped rows", sum(1 for r in rows if r["pair"][0] != den), "records", len(rows))
