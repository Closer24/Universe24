"""LIGHT3's lay tool: writes a test world's three files from a shipped world's files, never by the loader. Each test
world is the shipped files with the changes named on the command line, and nothing else moved:
- ring=<n>: the piece's shape [n, 1, 1], the setting's gears kept where their site is under n;
- key=<k>: the universe's chosen key k, a test's key, never the world's;
- held=<site>:<count>: the held hand's first count (now and before alike, at rest) at that one site, the shipped lay
  otherwise: a test's lay, the world-maker's initialization, a seed and not a strength (the Boss's ruling);
- ticks=<t>: the setting's ticks, a test's cut of the run.
A file nothing changes is copied byte for byte.
Usage: python -I lay_light3.py <shipped folder> <out folder> [ring=<n>] [key=<k>] [held=<site>:<count>] [ticks=<t>]"""

import json
import sys
from pathlib import Path


def main():
    shipped, out = Path(sys.argv[1]), Path(sys.argv[2])
    asked = dict(arg.split("=", 1) for arg in sys.argv[3:])
    out.mkdir(parents=True, exist_ok=True)
    universe = json.loads(shipped.joinpath("universe.json").read_text(encoding="utf-8"))
    piece = json.loads(shipped.joinpath("piece.json").read_text(encoding="utf-8"))
    setting = json.loads(shipped.joinpath("setting.json").read_text(encoding="utf-8"))
    named = []
    if "key" in asked:
        universe["chosen"]["key"] = int(asked["key"])
        out.joinpath("universe.json").write_text(json.dumps(universe, indent=2) + "\n", encoding="utf-8")
        named.append(f"key {asked['key']} (a test's)")
    else:
        out.joinpath("universe.json").write_bytes(shipped.joinpath("universe.json").read_bytes())
    if "ring" in asked:
        n = int(asked["ring"])
        piece["shape"] = [n, *piece["shape"][1:]]
        setting["gears"] = [gear for gear in setting["gears"] if gear[2] < n]
        out.joinpath("piece.json").write_text(json.dumps(piece) + "\n", encoding="utf-8")
        named.append(f"ring {n}")
    else:
        out.joinpath("piece.json").write_bytes(shipped.joinpath("piece.json").read_bytes())
    held_train = None
    if "held" in asked:
        site, count = (int(x) for x in asked["held"].split(":"))
        # the held hand's train: the one card whose kinds are the one-dimensional kinds together at part 1, as the
        # shipped files write it; the tool reads the file's card for the lay, which is the world-maker's act
        cards = universe["trains"]
        held_train = [i for i, c in enumerate(cards) if c["kinds"] == ["A1", "A2"] and c["part"] == 1][0]
        moved = 0
        for gear in setting["gears"]:
            if gear[0] == held_train and gear[1] == 0 and gear[2] == site:
                gear[3], gear[4] = count, count
                moved += 1
        named.append(f"held hand (train {held_train}) count {count} at site {site} ({moved} gear line moved)")
    if "ticks" in asked:
        setting["ticks"] = int(asked["ticks"])
        named.append(f"ticks {asked['ticks']} (a test's cut)")
    if "ring" in asked or "held" in asked or "ticks" in asked:
        text = json.dumps(setting) + "\n"
        out.joinpath("setting.json").write_text(text, encoding="utf-8")
    else:
        out.joinpath("setting.json").write_bytes(shipped.joinpath("setting.json").read_bytes())
    print(f"{out.name}: from {shipped.name}; " + ("; ".join(named) if named else "the shipped files byte for byte")
          + f"; {len(setting['gears'])} gears, ticks {setting['ticks']}")


if __name__ == "__main__":
    main()
