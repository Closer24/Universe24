"""KEY4's migration of the five shipped worlds on node-all 9d75a4904, a stand-in for each world's lay tool's write
step (the lay tools' own patches beside it, lay_*.diff): every world's universe.json loses its chosen key and its
setting.json lays the key once, as the key's middle, beside its ticks, each file's other bytes unmoved.

The middle is today's key moved: (key - 1) div senses with its remainder 0, senses the Spokes along one axis read from
the star (node-all's load.py line 190). It is the middle of the click's unit K, the file's key, not of the edge dial D
= (kappa div senses) K, which the node computes from it. Nothing is derived; the value is each world's own.
Whole numbers; Rule3's carry the one division; paths by joinpath.

Run: python -I migrate.py <tree_all> <tree_key4>, Python 3.14; it prints each world's key today and the middle laid.
"""

import json
import sys
from pathlib import Path

TODAY, KEY4 = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(TODAY.joinpath("src")))

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.runner.files import NAMES, star  # noqa: E402

for world in sorted(f.name for f in TODAY.joinpath("examples").glob("*/")):
    held = {name: TODAY.joinpath("examples", world, f"{name}.json").read_text(encoding="utf-8") for name in NAMES}
    universe, piece, setting = (json.loads(held[name]) for name in NAMES)
    axes = len(piece["shape"])
    senses, _ = carry(len(star(axes)), axes, 0)
    key = universe["chosen"]["key"]
    middle, rest = carry(key - 1, senses, 0)
    assert rest == 0, (world, key)
    cut = f'"key": {key}, '
    assert held["universe"].count(cut) == 1, world
    ticks = f'"ticks": {setting["ticks"]}, "gears"'
    assert held["setting"].count(ticks) == 1, world
    moved = {
        "universe": held["universe"].replace(cut, ""),
        "piece": held["piece"],
        "setting": held["setting"].replace(ticks, f'"ticks": {setting["ticks"]}, "middle": {middle}, "gears"'),
    }
    u_new, s_new = json.loads(moved["universe"]), json.loads(moved["setting"])
    assert "key" not in u_new["chosen"] and {**u_new["chosen"], "key": key} == universe["chosen"], world
    assert {k: v for k, v in s_new.items() if k != "middle"} == setting and s_new["middle"] == middle, world
    folder = KEY4.joinpath("examples", world)
    folder.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        folder.joinpath(f"{name}.json").write_text(moved[name], encoding="utf-8")
    print(f"{world}: key today {key} (universe.json chosen.key); laid as setting.json middle {middle}"
          f" (key = {senses} x {middle} + 1, the remainder {rest}); its gears {len(setting.get('gears', []))}, ticks"
          f" {setting['ticks']}, each byte of the gears unmoved")
