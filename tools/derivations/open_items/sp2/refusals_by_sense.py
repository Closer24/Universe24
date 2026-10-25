"""sp2: is the toy's lay refusal (`refuse`: a child not laid where its family stands at the Node) Pauli's exclusion in the
clicks? Pauli's refuses a LIKE sense and admits the OPPOSITE sense at one Node. This reading runs David's emergence seed
(toy/world_toy.json: the 5-cube at den 15,162,856,759,112,389, the sea with its hole and one quantum more) for N intervals
through the copy, with `refuse` wrapped to read, at every refused landing Node, the sign of the standing record's own
Wronskian W against the child's sense (-1 at the minus end, +1 at the plus end), and counts the refusals by agreement:
like (the standing W has the child's sign), opposite (the other sign), none (W = 0 there: the standing record neutral).
A refusal that reads the share alone refuses all three alike. Integers only.

usage: refusals_by_sense.py [intervals]
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lean_sp2 as L


class Reading(L.Lean):
    def refuse(self, born, owns):
        counts = self.__dict__.setdefault('by_sense', {'like': 0, 'opposite': 0, 'none': 0, 'kept': 0, 'crowded': 0})
        for at, s_, minus, plus, room in born:
            re, im = self.records()[s_].lines
            for where, sense in ((minus, -1), (plus, 1)):
                if int(owns[s_][where]) > 0:  # this landing refuses the whole birth (the toy's rule); read the standing W's sign there
                    W = int(re.now[where] * im.before[where] - im.now[where] * re.before[where])
                    counts['like' if W * sense > 0 else 'opposite' if W * sense < 0 else 'none'] += 1
        kept = L.Lean.refuse(self, born, owns)
        counts['kept'] += len(kept)
        return kept


def main():
    sys.set_int_max_str_digits(0)
    intervals = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    universe, world = L.load_world(os.path.join(HERE, 'toy', 'world_toy.json'))
    b = Reading(universe, world)
    for _ in range(intervals): b.step()
    found = {'world': 'toy/world_toy.json', 'intervals': intervals, 'refused landings by the standing W against the child sense': b.__dict__.get('by_sense', {}), 'births': b.counts['births'], 'refused_lay (toy count)': b.counts['refused_lay'], 'body_clicks': b.counts['body_clicks']}
    print(json.dumps(found))
    json.dump(found, open(os.path.join(HERE, 'outputs', 'refusals_by_sense.json'), 'w'))


if __name__ == '__main__':
    main()
