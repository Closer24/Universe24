"""rl1 (H-Rule3-Link-Record-1): the flagged copy of the engine at /dev/shm/tmp/rl1/src, the Link coupling's form from the environment RL1_FORM. Unset or empty: the head bit for bit (R_ij = 2 num p_i^2 Q_ij, the Node's own pace squared). "sum": num (p_i^2 + p_j^2) Q_ij (the arithmetic form, hp2's). "geo": 2 num p_i p_j Q_ij (the geometric form, tq2's). "link": 2 num p_ij^2 Q_ij, p_ij the Link's pace at the two ends' mean content rounded half up (the former two-end pace, kept by name). Every form reads the far end through core.ports.across alone (one Node and its six Links) and is written once per interval on the whole board: no per-Node call. Usage: make_copy_rl1.py <src_root> <copy_root> [fr2.diff]"""
import os
import shutil
import subprocess
import sys

src = os.path.join(sys.argv[1], "event_universe")
root = sys.argv[2]
dst = os.path.join(root, "event_universe")
if os.path.exists(root):
    shutil.rmtree(root)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
if len(sys.argv) > 3:  # FR-S1's two lines first (H-Frozen-Node-Release-2/out/src_fr2.diff), the form's lines after
    subprocess.run(["patch", "-p1", "-d", root, "-i", os.path.abspath(sys.argv[3])], check=True)


def replace(path, old, new):
    text = open(path).read()
    assert text.count(old) == 1, ("the replacement site is not unique", path, old[:60])
    open(path, "w").write(text.replace(old, new))


rule3 = os.path.join(dst, "core", "rule3.py")
replace(
    rule3,
    "    factors: tuple[Any, ...] | None = None,\n    unit: Any = 1,\n) -> Rule:",
    "    factors: tuple[Any, ...] | None = None,\n    unit: Any = 1,\n    others: tuple[Any, ...] | None = None,\n    form: str = \"\",\n) -> Rule:",
)
replace(
    rule3,
    "    reaches = tuple((node_squared + node_squared) * factor * num for factor in links)\n",
    """    if others is None or not form:
        reaches = tuple((node_squared + node_squared) * factor * num for factor in links)
    elif form == "sum":  # rl1: the arithmetic form num (p_i^2 + p_j^2) Q_ij, p_j the far end's own pace
        reaches = tuple((node_squared + other * other) * factor * num for factor, other in zip(links, others))
    elif form == "geo":  # rl1: the geometric form 2 num p_i p_j Q_ij
        reaches = tuple((pace * other + pace * other) * factor * num for factor, other in zip(links, others))
    elif form == "link":  # rl1: the Link's own pace p_ij at the two ends' mean content, 2 num p_ij^2 Q_ij
        reaches = tuple((other * other + other * other) * factor * num for factor, other in zip(links, others))
    else:
        raise ValueError(f"RL1_FORM {form!r} is not a form of the Link coupling")
""",
)
node = os.path.join(dst, "node.py")
replace(
    node,
    "from event_universe.features import phase\n",
    "from event_universe.features import phase\nimport os\n\n# rl1 (H-Rule3-Link-Record-1): the Link coupling's form from the environment; unset, the head bit for bit\nRL1_FORM = os.environ.get(\"RL1_FORM\", \"\")\n",
)
replace(
    node,
    """        clock, pace = readings.paces_of(self, c)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)""",
    """        clock, pace = readings.paces_of(self, c)
        if RL1_FORM and np.ndim(pace):
            # rl1: the far end's reading per Port through across alone, once for the whole board
            if RL1_FORM == "link":
                from event_universe.core import paces as paces_
                means = [paces_.rounded(c + across(c, port), 2) for port in range(PORTS)]
                others = tuple(paces_.link_pace_of(self.gamma, np.asarray(m, dtype=object)) for m in means)
            else:
                others = tuple(across(pace, port) for port in range(PORTS))
            return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G, others, RL1_FORM)
        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)""",
)
print("copy at", root)
