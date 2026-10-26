"""The spin part at the births and the clicks' booked momentum, read from the record cache's logs (no run): per birth the two children's senses and Wronskians summed; per click dP_take + dP_lay. Usage: python am2_senses.py <record.json>..."""
import json, sys
sys.set_int_max_str_digits(0)
for path in sys.argv[1:]:
    r = json.load(open(path))
    log = r["log"]
    births = [e for e in log if e.get("event") == "birth"]
    sense_sums = [sum(e["senses"]) for e in births]
    w_sums = [sum(e["W_children"]) for e in births]
    opp = sum(1 for e in births if e["W_children"][0] * e["W_children"][1] < 0)
    events = {}
    for e in log:
        events[e.get("event")] = events.get(e.get("event"), 0) + 1
    print(json.dumps({"record": path.split("/")[-1], "events": events, "births": len(births),
                      "births with senses summing to 0": sum(1 for s in sense_sums if s == 0),
                      "births with W_children summing to 0": sum(1 for s in w_sums if s == 0),
                      "births with opposite Wronskians": opp,
                      "W_children values": sorted(set(abs(e["W_children"][0]) for e in births)),
                      "senses seen": sorted(set(tuple(e["senses"]) for e in births))}))
