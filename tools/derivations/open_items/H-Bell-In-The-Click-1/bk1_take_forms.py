"""The two forms of the close's take on a record (bk1, the generic unification): births by the taken row's kind, the emitter's one take per Node of the children's walls summed (`take_at`, the birth's case) against the gapped row's one take per end (`merger_take`, logged under `takes`); the credits' take from the gap-0 row at the body's Node, laid back (EQ-S1) or standing; so how many times the letter's take holds in two forms on one record. Usage: python bk1_take_forms.py <world.json>"""
import json
import sys
from collections import Counter

from event_universe.loader.world import load_world
from event_universe.node import Node


def main(path):
    universe, world = load_world(path)
    node = Node(universe, world)
    for _ in range(int(world["intervals"])):
        node.step()
    rec0 = node.records().index(node.emitter())
    births = [e for e in node.log if e["event"] == "birth"]
    credits = [e for e in node.log if e["event"] == "credit"]
    out = {
        "world": path,
        "emitter_record": rec0,
        "births": len(births),
        "births_one_take_per_node (taken row the emitter)": sum(1 for b in births if "takes" not in b),
        "births_one_take_per_end (merger_take)": sum(1 for b in births if "takes" in b),
        "births_by_taken_row": dict(Counter(b["taken_row"] for b in births)),
        "children_record (line_pair)": dict(Counter(b["line_pair"] for b in births)),
        "births_children_at_one_node": dict(Counter(b["children_at_node"] for b in births)),
        "credits": len(credits),
        "credits_taken_from_the_emitter": sum(1 for c in credits if c.get("taken_row", rec0) == rec0),
        "credits_laid_back": sum(1 for c in credits if "laid_back" in c),
        "births_laid_back": sum(1 for b in births if "laid_back" in b),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    main(sys.argv[1])
