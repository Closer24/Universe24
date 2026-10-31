"""Write a world's files with every CHOSEN strength at 1 (the key the world's own), for reading the coupling's
support from the structure alone. Args: <world dir> <out dir>."""
import json
import sys
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for name in ("universe", "piece", "setting"):
    data = json.loads(src.joinpath(name + ".json").read_text(encoding="utf-8"))
    if name == "universe":
        for k in data["chosen"]:
            if k != "key":
                data["chosen"][k] = 1
    out.joinpath(name + ".json").write_text(json.dumps(data), encoding="utf-8")
print("written", out)
