"""em2: the four emitter runs in parallel (default and flag, content 0 and 400)."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PY = "/home/user/Universe24/venv314/bin/python"
n, q = sys.argv[1], sys.argv[2]
jobs = []
for tag, src, flag, c in [("em_default_c0", "src", False, "0"), ("em_flag_c0", "src_em2", True, "0"), ("em_default_c400", "src", False, "400"), ("em_flag_c400", "src_em2", True, "400")]:
    env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, src) if src == "src" else os.path.join(HERE, src), TMPDIR="/dev/shm/tmp")
    env.pop("EM2_EMISSION", None)
    if flag: env["EM2_EMISSION"] = "quantum"
    log = open(os.path.join(HERE, "out", tag + ".txt"), "w")
    jobs.append((tag, subprocess.Popen([PY, os.path.join(HERE, "one_node_emitter.py"), c, n, q, os.path.join(HERE, "out", tag + ".json")], stdout=log, stderr=subprocess.STDOUT, env=env)))
for tag, p in jobs:
    p.wait(); print(tag, "exit", p.returncode)
