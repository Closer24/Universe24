"""H-Rule3-Link-Record-2: the flagged copy of src at /dev/shm/tmp/rl2/src_rl2. RL2_FORM from the environment names the reach's form: unset, the head bit for bit; "arith" num (p_i^2 + p_j^2) Q_ij; "geom" 2 num p_i p_j Q_ij; "harm" 4 num p_i^2 p_j^2 Q_ij over (p_i^2 + p_j^2) rounded half up; "link" 2 num p_ij^2 Q_ij at the Link's own pace, p_ij the Link pace of the two ends' mean content rounded half up (the tension's own mean). The two ends' paces are read once per rule call at the array level (six takes of one array), no per-Port vectorize. FR-S1's two lines carried under FR2_RELEASE as fr2 wrote them. Usage: make_copy_rl2.py <src> <copy>"""
import os
import shutil
import sys

src, copy = sys.argv[1], sys.argv[2]
if os.path.exists(copy):
    shutil.rmtree(copy)
shutil.copytree(src, copy, ignore=shutil.ignore_patterns("__pycache__"))


def replace(path, old, new, count=1):
    text = open(path, encoding="utf-8").read()
    assert text.count(old) == count, (path, old[:60], text.count(old))
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


rule3 = os.path.join(copy, "event_universe/core/rule3.py")
replace(
    rule3,
    "from event_universe.core.ports import PORTS\n",
    "from event_universe.core.ports import PORTS\n"
    "import os as _os\n\n"
    "RL2_FORM = _os.environ.get('RL2_FORM', '')  # rl2 (H-Rule3-Link-Record-2), flagged: the reach's form; unset the head bit for bit\n",
)
replace(
    rule3,
    "    reaches = tuple((node_squared + node_squared) * factor * num for factor in links)\n",
    "    reaches = tuple((node_squared + node_squared) * factor * num for factor in links)\n"
    "    if RL2_FORM and partners is not None:\n"
    "        reaches = tuple(rl2_reach(RL2_FORM, pace, other, factor, num) for other, factor in zip(partners, links))\n",
)
replace(
    rule3,
    "    unit: Any = 1,\n) -> Rule:\n",
    "    unit: Any = 1,\n    partners: tuple[Any, ...] | None = None,\n) -> Rule:\n",
)
replace(
    rule3,
    "def link_factor(gamma: Any, unit: Any, tension: Any) -> Any:\n",
    "def rl2_reach(form: str, pace: Any, other: Any, factor: Any, num: Any) -> Any:\n"
    "    \"\"\"rl2, flagged: the reach of one Link read alike from both ends, from the Node's pace p_i, the far end's pace p_j (or, for the form 'link', the Link's own pace handed in as `other` at both slots) and the Link's factor: arith num (p_i^2 + p_j^2) Q; geom 2 num p_i p_j Q; harm 4 num p_i^2 p_j^2 Q over (p_i^2 + p_j^2) rounded half up by the division act, 0 where both paces are 0; link 2 num p_ij^2 Q.\"\"\"\n"
    "    import numpy as np\n"
    "    if form == 'arith':\n"
    "        return (pace * pace + other * other) * factor * num\n"
    "    if form == 'geom':\n"
    "        return (pace * other + pace * other) * factor * num\n"
    "    if form == 'link':\n"
    "        return (other * other + other * other) * factor * num\n"
    "    if form == 'harm':\n"
    "        both = pace * pace + other * other\n"
    "        wall = np.where(np.asarray(both) == 0, 1, both) if np.ndim(both) else (both or 1)\n"
    "        top = (4 * num) * pace * pace * other * other\n"
    "        return division_forward(top + top, wall + wall, wall)[0] * factor\n"
    "    raise ValueError(f'rl2: no form named {form}')\n\n\n"
    "def link_factor(gamma: Any, unit: Any, tension: Any) -> Any:\n",
)
node = os.path.join(copy, "event_universe/node.py")
replace(
    node,
    "        clock, pace = readings.paces_of(self, c)\n        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G)\n",
    "        clock, pace = readings.paces_of(self, c)\n"
    "        partners = None\n"
    "        if rule3.RL2_FORM and np.ndim(pace):\n"
    "            # rl2, flagged: the far end's pace at each Port, one take per Port of one array; for the form 'link' the Link's own pace from the two ends' mean content rounded half up (the tension's own mean)\n"
    "            if rule3.RL2_FORM == 'link':\n"
    "                partners = tuple(paces.link_pace_of(self.gamma, paces.rounded(c + across(c, port), 2)) for port in range(PORTS))\n"
    "            else:\n"
    "                partners = tuple(across(pace, port) for port in range(PORTS))\n"
    "        return rule3.rule_integers(pair[0], pair[1], self.gamma, clock, pace, factors, self.G, partners)\n",
)
# FR-S1's two lines (H-Frozen-Node-Release-2/out/src_fr2.diff), flagged FR2_RELEASE
replace(
    node,
    "        if frozen is not None:\n            top = top & ~frozen\n",
    "        if frozen is not None and not FR2_RELEASE:\n            top = top & ~frozen\n",
)
replace(
    node,
    "from event_universe.links import Link, turned\n",
    "from event_universe.links import Link, turned\nimport os\n\nFR2_RELEASE = bool(os.environ.get('FR2_RELEASE'))  # fr2's flag, FR-S1's two lines; unset the head bit for bit\n",
)
interval = os.path.join(copy, "event_universe/interval.py")
replace(
    interval,
    "from typing import TYPE_CHECKING, Any\n",
    "import os\n\nfrom typing import TYPE_CHECKING, Any\n\nFR2_RELEASE = bool(os.environ.get('FR2_RELEASE'))\n",
)
replace(
    interval,
    "        node.restore(node.all_lines(), [line for row in self.held for line in row], self.frozen)\n",
    "        if self.direction == -1 and self.kept is not None and FR2_RELEASE:\n"
    "            node.restore(node.all_lines(), [line for row in self.held for line in row], self.frozen & ~self.top)\n"
    "            node.restore(node.all_lines(), [line for row in self.kept for line in row], self.frozen & self.top)\n"
    "        else:\n"
    "            node.restore(node.all_lines(), [line for row in self.held for line in row], self.frozen)\n",
)
print("copy at", copy)
