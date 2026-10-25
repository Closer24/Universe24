"""pm2: the flagged world copies: every world of tests/worlds copied to worlds_flag/ with the key pm2_weight: carrier; the universe files copied beside them."""
import json, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "tests", "worlds")
DST = os.path.join(HERE, "worlds_flag")
os.makedirs(DST, exist_ok=True)
for name in sorted(os.listdir(SRC)):
    if name.startswith("universe"):
        shutil.copy(os.path.join(SRC, name), os.path.join(DST, name))
    elif name.startswith("world"):
        world = json.load(open(os.path.join(SRC, name)))
        world["pm2_weight"] = "carrier"
        json.dump(world, open(os.path.join(DST, name), "w"))
        print(name, "flagged")
