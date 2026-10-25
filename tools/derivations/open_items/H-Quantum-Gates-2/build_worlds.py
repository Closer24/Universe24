"""The worlds of the quantum gates (hand qg2), written from integers alone: the two beams at the wave numbers (k_x, +k_y) and (k_x, -k_y), the far field of two slits (two coherent sources at the angles +theta and -theta), and the one beam as the control (one slit open); the wave number h = den sin(k / 2) in den's unit, k_x = k_y = pi / 2 so h = largest_below(den^2 / 2), the fringe period along y = pi / k_y = 2 Links.

Usage: python build_worlds.py [quanta] [intervals] [cube]"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[3] / "src"))
from event_universe.core.rule3 import largest_below, quotient  # noqa: E402


def main(argv):
    quanta = int(argv[1]) if len(argv) > 1 else 200
    intervals = int(argv[2]) if len(argv) > 2 else 24
    cube = int(argv[3]) if len(argv) > 3 else 9
    universe = json.loads((HERE / "worlds" / "universe_middle.json").read_text())
    den = int(universe["integers"]["den"])
    h = int(largest_below(quotient(den * den, 2)))  # den sin(pi / 4): k = pi / 2 per Link
    centre = [quotient(cube, 2)] * 3
    shape = [cube] * 3
    beam = lambda hy, at: {"lay": "at", "row": 0, "centre": at, "quanta": quanta, "width": 3, "sense": 1, "wave": [h, hy, 0], "top": 3}
    worlds = {
        "slits_one": [beam(h, centre)],
        "slits_two": [beam(h, centre), beam(-h, centre)],
        "slits_two_z": [beam(h, centre), beam(-h, [centre[0], centre[1], centre[2] + 1])],
    }
    for name, seed in worlds.items():
        world = {"universe": "universe_middle.json", "shape": shape, "intervals": intervals, "seed": seed}
        (HERE / "worlds" / f"{name}.json").write_text(json.dumps(world))
    print(json.dumps({"den": den, "h": h, "cube": cube, "quanta": quanta, "intervals": intervals, "k per Link": "pi/2 on x and y", "fringe period (Links)": 2}))


if __name__ == "__main__":
    main(sys.argv)
