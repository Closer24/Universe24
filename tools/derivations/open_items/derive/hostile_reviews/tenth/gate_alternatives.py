"""Probe 2: Sofer's gate (scribe_scan.scan) on engine/contract.py as committed and with the source made of dtype=object
whatever the caller's gears (np.zeros_like(gears, dtype=object), np.zeros(gears.shape, dtype=object)); and on runner/load.py
with the lay's arrays of int64 (a mutant the closed list does not reach in runner/).
usage: python -I gate_alternatives.py <worktree>"""

import sys
from pathlib import Path

WT = Path(sys.argv[1])
sys.path[:0] = [str(WT / "tools/derivations/open_items"), str(WT / "tools")]
import scribe_scan  # noqa: E402

contract = (WT / "src/tensor24/engine/contract.py").read_text()
load = (WT / "src/tensor24/runner/load.py").read_text()
old = "    source = 0 * gears\n"
variants = {
    "contract.py as committed": ("tensor24/engine/contract.py", contract),
    "source = np.zeros_like(gears, dtype=object)": ("tensor24/engine/contract.py", contract.replace(old, "    source = np.zeros_like(gears, dtype=object)\n")),
    "source = np.zeros(gears.shape, dtype=object)": ("tensor24/engine/contract.py", contract.replace(old, "    source = np.zeros(gears.shape, dtype=object)\n")),
    "source = np.zeros_like(gears)  (no dtype)": ("tensor24/engine/contract.py", contract.replace(old, "    source = np.zeros_like(gears)\n")),
    "load.py as committed": ("tensor24/runner/load.py", load),
    "load.py, the lay's arrays dtype=np.int64": ("tensor24/runner/load.py", load.replace("np.zeros((rows, sites), dtype=object)", "np.zeros((rows, sites), dtype=np.int64)").replace("np.zeros((1, sites), dtype=object)", "np.zeros((1, sites), dtype=np.int64)")),
    "load.py, the plan's factor dtype=np.int64": ("tensor24/runner/load.py", load.replace("np.array(factor, dtype=object)", "np.array(factor, dtype=np.int64)")),
}
base = {name: None for name in variants}
for name, (rel, source) in variants.items():
    assert source != contract or name == "contract.py as committed" or rel != "tensor24/engine/contract.py"
    hits = scribe_scan.scan(rel, source)
    blocks = [h for h in hits if scribe_scan.RULES[h.rule][0] == "BLOCK"] if hasattr(scribe_scan, "RULES") else hits
    print(f"{name:<48} hits {len(hits)}: {sorted({(h.rule, getattr(h, 'detail', '')) for h in hits})}")
