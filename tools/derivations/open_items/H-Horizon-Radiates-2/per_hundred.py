"""hr2: a streamed record by hundreds of intervals: the credits, their levels, the births, the frozen lines, the max content, the hood and rest content sums, the turned lines among the Nodes that ever froze; and the credits of the last 300 intervals before the first freeze by distance from the Nodes that will freeze. Usage: per_hundred.py <stream.jsonl> [step]"""
import json, sys
sys.set_int_max_str_digits(0)
ls = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
step = int(sys.argv[2]) if len(sys.argv) > 2 else 100
print("i_from i_to credits levels births frozen_lines max_content hood_sum rest_sum board_sum turned_ever")
for a in range(0, len(ls), step):
    b = ls[a:a + step]
    cr = [c for l in b for c in l["clicks"] if c["event"] == "credit"]
    print(b[0]["i"], b[-1]["i"], len(cr), sum(c["levels"] for c in cr), sum(l["births"] for l in b), sum(len(l["frozen"]) for l in b), max(l["max_content"] for l in b), b[-1]["hood_content_sum"], b[-1]["rest_content_sum"], b[-1]["board_content_sum"], sum(len(l["turned_ever"]) for l in b))
last = [l for l in ls if l["clicks"] and any(c["event"] == "credit" for c in l["clicks"])]
print("last interval with a credit:", last[-1]["i"] if last else None, "first:", last[0]["i"] if last else None)
