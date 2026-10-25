"""pc1: every carried form against the letter (clock_alone, and the Link's pace rounded once from it) over EVERY content the records visit (the hole seed 60, the chiral seed 300, the bodies' seed 120, the hole seed 900): the count equal, the count off by one unit and where.
Usage: python pc1_visited.py <out.json>"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'toy_pc1'))
import pc1_paces
from event_universe.core import paces as engine_paces
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for name, path in (('hole seed 60', 'out/records/world_toy_60_memo.json'), ('chiral seed 300', 'out/records/world_chiral_300_memo.json'), ('bodies seed 120', 'out/records/world_bodies_120_memo.json'), ('hole seed 900', 'out/hole_900_scaled.json')):
    R = json.load(open(os.path.join(HERE, path)))
    gamma = R['gamma']; visited = R['contents_visited (pc1)']
    letter = {c: engine_paces.clock_alone(gamma, c) for c in visited}
    letter_link = {c: int(engine_paces.rounded(letter[c] * letter[c], gamma)) for c in visited}
    row = {'gamma': gamma, 'contents visited': len(visited), 'min/max': [min(visited), max(visited)]}
    for flag in ('plain', 'half', 'gamma', 'gamma2', 'scaled'):
        car = pc1_paces.Carried(flag)
        off = [c for c in visited if car.clock(gamma, c) != letter[c]]
        off_link = [c for c in visited if car.link(gamma, c) != letter_link[c]]
        row[flag] = {'clock equal': len(visited) - len(off), 'clock off by one': sum(1 for c in off if abs(car.clock(gamma, c) - letter[c]) == 1), 'clock off by more': sum(1 for c in off if abs(car.clock(gamma, c) - letter[c]) > 1), 'where (first 12)': off[:12], 'link pace equal': len(visited) - len(off_link), 'link pace off': len(off_link), 'memo bits': car.memo_bits(gamma)}
    out[name] = row
    print(json.dumps({name: row}))
json.dump(out, open(sys.argv[1], 'w'), indent=1)
