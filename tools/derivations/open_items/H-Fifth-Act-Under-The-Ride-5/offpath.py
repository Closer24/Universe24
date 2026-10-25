"""Hand r5: the flag off on the patched src against the pristine branch's src (git archive of 7dc781bc2's src under
/dev/shm/tmp/pristine_r5): the digest of every forward array and the run back, per board. Output offpath.json."""

import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
found = {}
for board in ("open", "hole", "sea"):
    for name, src in (("patched", str(ROOT / "src")), ("pristine", "/dev/shm/tmp/pristine_r5/src")):
        env = dict(os.environ, PYTHONPATH=src, U24_SRC=src, TMPDIR="/dev/shm/tmp")
        env.pop("U24_RIDES", None)
        subprocess.run(["/home/user/Universe24/venv314/bin/python", str(HERE / "top_local.py"), "0", board], cwd=ROOT, env=env, check=True, capture_output=True)
        d = json.loads((HERE / f"top_local_0_{board}.json").read_text(encoding="utf-8"))
        found[f"{board}_{name}"] = {k: d[k] for k in ("digest_of_every_forward_array", "per_step_matched", "chained_matched", "turn_intervals", "births")}
    found[f"{board}_equal"] = found[f"{board}_patched"] == found[f"{board}_pristine"]
(HERE / "offpath.json").write_text(json.dumps(found, indent=1), encoding="utf-8")
print(json.dumps(found, indent=1))
