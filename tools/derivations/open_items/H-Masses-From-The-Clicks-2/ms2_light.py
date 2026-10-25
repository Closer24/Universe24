"""ms2: light's clicks in an engine record as a far reader has them: every take of the gap-0 line (the light) at a birth or a body's
credit, the levels absorbed and the walls booked, and the gap-0 plane's own credits (predicted 0: the sea never clicks of itself).
Usage: python ms2_light.py <record.json>"""
import json, sys
sys.set_int_max_str_digits(0)
run = json.load(open(sys.argv[1]))
den = int(run["den"]); planes = [int(x) for x in run["planes"]]; gap0 = planes.index(den)
births = [e for e in run["log"] if e["event"] == "birth"]; credits = [e for e in run["log"] if e["event"] == "credit"]
takes_b = {(e["i"], tuple(e["node"])) for e in births}
print(sys.argv[1], "intervals", run["intervals"])
print("births", len(births), "takes at births (one per taking Node and interval)", len(takes_b),
      "levels of light absorbed at births", sum(e["levels"] for e in births if e["children_at_node"] >= 1) if births else 0,
      "booked", sum(e["booked"] for e in births), "taken", sum(e["taken"] for e in births))
print("body credits", len(credits), "levels of light absorbed at credits", sum(e["levels"] for e in credits),
      "gap-0 plane's own credits", sum(1 for e in credits if e["line"] == gap0))
print("refused: stop", run["counts"]["refused_stop"], "lay", run["counts"]["refused_lay"], "orientation", run["counts"]["refused_orientation"])
