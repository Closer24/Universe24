"""Hand k1: the engine runs of engine_measure.py as one set, each a subprocess (no shell loop), their JSON lines gathered.

    PYTHONPATH=src python tools/derivations/k1/run_engine_set.py <set name> <den,Gamma,T,G,N[,cube]> ...
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PYTHON = "/home/user/Universe24/venv314/bin/python"


def main() -> None:
    name, configs = sys.argv[1], sys.argv[2:]
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), TMPDIR="/dev/shm/tmp")
    out = HERE / f"engine_{name}.jsonl"
    with out.open("w") as handle:
        procs = [
            subprocess.Popen([PYTHON, str(HERE / "engine_measure.py"), *config.split(",")], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True)
            for config in configs
        ]
        for config, proc in zip(configs, procs, strict=True):
            text, _ = proc.communicate()
            handle.write(text if text.strip().startswith("{") else f'{{"config": "{config}", "error": {text.strip()[-600:]!r}}}\n')
            handle.flush()
    print(out.read_text())


if __name__ == "__main__":
    main()
