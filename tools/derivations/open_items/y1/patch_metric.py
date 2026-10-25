"""Hand y1 (2026-10-25): the metric's six missing lines behind the flag U24_METRIC, applied to src/ by exact replacement; every replacement named on stdout; the branch's path bit for bit with the flag off (every edit either a new function called only under the flag, or a branch on the flag whose off side is the former text, or a default parameter whose default is the former behaviour). Run once from the worktree root."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "src" / "event_universe"
EDITS: list[tuple[str, str, str]] = []


def edit(path: str, old: str, new: str) -> None:
    EDITS.append((path, old, new))


# 1. the flag, read once (core/ports.py)
edit("core/ports.py", "from typing import Any\n", "import os\nfrom typing import Any\n")
edit(
    "core/ports.py",
    "\n\ndef shifted(",
    "\nMETRIC = (\n    os.environ.get(\"U24_METRIC\") == \"1\"\n)  # hand y1, 2026-10-25: the metric's ten lines written, ridden and read (ALGEBRA.md, The three shapes, U-S1); off, every path of the branch bit for bit\n\n\ndef shifted(",
)
# 2. the volume's row at ten lines (loader/universe.py)
edit("loader/universe.py", "from event_universe.core.ports import AXES\n", "from event_universe.core.ports import AXES, METRIC\n")
edit(
    "loader/universe.py",
    "    return Row(name, pair, 1 + AXES, 1, False, False, False, 1, 1, 0, ())\n\n\ndef volume_pair",
    "    lines = 1 + AXES * (AXES if METRIC else 1)  # U24_METRIC: g_00, the three g_aa, the three g_0a, the three g_ab\n    return Row(name, pair, lines, 1, False, False, False, 1, 1, 0, (), flux=METRIC)\n\n\ndef volume_pair",
)
# 3. every axis line by its position among the nine readings (records.py)
edit("records.py", "from event_universe.core.ports import AXES, SIDES\n", "from event_universe.core.ports import AXES, METRIC" + ", SIDES\n")
edit(
    "records.py",
    "    if family.flux:\n        positions += [AXES + axis for axis in range(AXES)]\n    assert len(positions)",
    "    if family.flux:\n        positions += [AXES + axis for axis in range(AXES)]\n    if METRIC and family.flux and not family.wronskian:  # U24_METRIC: the tensions, the fluxes, the shears, by position\n        positions = list(range(family.width - 1))\n    assert len(positions)",
)
# 4. the shear's reading (features/currents, readings.py)
edit(
    "features/currents/__init__.py",
    "    x, y, z = (tension(weight, n) for n in neighbours)\n    return x, y, z\n",
    "    x, y, z = (tension(weight, n) for n in neighbours)\n    return x, y, z\n\n\ndef shear(weight: int, neighbours: tuple[Neighbours, Neighbours, Neighbours]) -> Vector:\n    \"\"\"U24_METRIC (hand y1, 2026-10-25): the shear's part on each axis pair xy, yz, zx at every Node from one level pair's neighbours, weight x D_a now x D_b now with D_a now = now_(i+a) - now_(i-a) the Node's own centred difference, the off-diagonal of the tensor whose diagonal is `tension`, T_2g under the cube's 48, one Link's reach, no division (ALGEBRA.md, The off-diagonal parts where declared, the former declared layer).\"\"\"\n    x, y, z = (n.ahead - n.behind for n in neighbours)\n    return weight * x * y, weight * y * z, weight * z * x\n",
)
edit("readings.py", "from event_universe.core.ports import AXES, arrival\n", "from event_universe.core.ports import AXES, METRIC, arrival\n")
edit(
    "readings.py",
    "    return (*stresses_of(weight, lines, currents.stress, frames), *fluxes)\n",
    "    found = (*stresses_of(weight, lines, currents.stress, frames), *fluxes)\n    if METRIC:  # U24_METRIC: the shear's parts D_a D_b on the three axis pairs after the fluxes (`currents.shear`)\n        found = (*found, *stresses_of(weight, lines, currents.shear, frames))\n    return found\n",
)
# 5. the ride: the flux and shear lines at the wall w (X_now + X_ahead), no trace (flux.py)
edit("flux.py", "from event_universe.core.ports import AXES\n", "from event_universe.core.ports import AXES, METRIC\n")
edit(
    "flux.py",
    "def step_momentum(\n    own: Sequence[Record], rule: Rule, direction: int, volumes: tuple[Any, Any, Any]\n) -> list[Record]:",
    "def step_momentum(\n    own: Sequence[Record],\n    rule: Rule,\n    direction: int,\n    volumes: tuple[Any, Any, Any],\n    traceless: bool = True,\n) -> list[Record]:",
)
edit(
    "flux.py",
    "    wall3, mass3 = AXES * rule.wall, AXES * rule.mass\n",
    "    scale = (\n        AXES if traceless else 1\n    )  # U24_METRIC: the flux and shear lines ride at the wall w (X_now + X_ahead) with their own Link terms whole, no trace\n    wall3, mass3 = scale * rule.wall, scale * rule.mass\n",
)
edit(
    "flux.py",
    "        traceless = AXES * np.asarray(flux, dtype=object) - total\n",
    "        projected = AXES * np.asarray(flux, dtype=object) - total if traceless else np.asarray(flux, dtype=object)\n",
)
edit(
    "flux.py",
    "            entered * level + born * (level - other) + (now + now) * (traceless - mass3 * level) + rest\n",
    "            entered * level + born * (level - other) + (now + now) * (projected - mass3 * level) + rest\n",
)
edit(
    "flux.py",
    "            if not (traced and 1 <= number - span.start <= AXES)\n",
    "            if not (traced and 1 <= number - span.start <= (family.width - 1 if METRIC else AXES))\n",
)
# 6. shear.py: the lines that ride, their birth and their wall's factor
edit("shear.py", "from event_universe.core.ports import AXES\n", "from event_universe.core.ports import AXES, METRIC\n")
edit(
    "shear.py",
    "        for record in range(family.records)\n        for a in range(AXES)\n    ]\n",
    "        for record in range(family.records)\n        for a in range(family.width - 1 if METRIC else AXES)\n    ]\n\n\ndef ride_scale(family: Any, position: int) -> int:\n    \"\"\"The factor of the wall w an axis line at `position` (1 + a within its row) rides the volume with: AXES on the three tension lines (the traceless triple at 3 w (X_now + X_ahead)); under U24_METRIC 1 on the flux and shear lines (w (X_now + X_ahead), no trace; hand y1, 2026-10-25).\"\"\"\n    return AXES if position <= AXES else 1\n",
)
edit(
    "shear.py",
    "        lines[first + 1 : first + 1 + AXES] = flux.step_momentum(\n            lines[first + 1 : first + 1 + AXES], rule, direction, volumes\n        )\n",
    "        lines[first + 1 : first + 1 + AXES] = flux.step_momentum(\n            lines[first + 1 : first + 1 + AXES], rule, direction, volumes\n        )\n        if METRIC:  # U24_METRIC: the flux and shear lines ride the volume at the wall w (X_now + X_ahead)\n            rest = slice(first + 1 + AXES, first + family.width)\n            lines[rest] = flux.step_momentum(lines[rest], rule, direction, volumes, False)\n",
)
edit(
    "shear.py",
    "        for number in range(1, 1 + AXES):\n            lines[number] = replace(lines[number], remainder=np.asarray(half, dtype=object))\n",
    "        for number in range(1, 1 + AXES):\n            lines[number] = replace(lines[number], remainder=np.asarray(half, dtype=object))\n        if METRIC:  # U24_METRIC: the six lines' remainders born at half their wall w (X_0 + X_0), w X_0\n            plain = wall_of(family.pair[1], board.world.node_clock, board.unit) * records.exact(lines[0].now)\n            for number in range(1 + AXES, family.width):\n                lines[number] = replace(lines[number], remainder=np.asarray(plain, dtype=object))\n",
)
# 7. swap.py: the complement at the riding line's own wall
edit(
    "swap.py",
    "                    if first < number <= first + family.width - 1:\n                        times[number] = lines[first]\n",
    "                    if first < number <= first + family.width - 1:\n                        times[number] = (lines[first], shear.ride_scale(family, number - first))\n",
)
edit(
    "swap.py",
    "            if number in times:  # 3 w (X_now + X_before) of the row's own time line\n                time = times[number]\n                own = (\n                    3\n                    * wall\n",
    "            if number in times:  # 3 w (X_now + X_before) of the row's own time line (w (X_now + X_before) on a flux or shear line, U24_METRIC)\n                time, scale = times[number]\n                own = (\n                    scale\n                    * wall\n",
)
edit(
    "swap.py",
    "        times: dict[\n            int, records.Record\n        ] = {}",
    "        times: dict[\n            int, tuple[records.Record, int]\n        ] = {}",
)
# 8. the read: gravity's fold of the planes' Link pair from the flux lines (flux.pairs_of, plane.py)
edit("plane.py", "from event_universe.core.ports import AXES, SIDES, arrival\n", "from event_universe.core.ports import AXES, SIDES, arrival\nfrom event_universe.core.paces import rounded\n")
edit("plane.py", "from event_universe.records import Record\n", "from event_universe.records import Record, level_at\n")
edit(
    "plane.py",
    "def link_pairs(\n    pair: tuple[int, int],\n    gamma: int,\n    content: Any,\n    factors: tuple[Any, ...],\n    sign: tuple[Any, ...] | None,\n    phases: Phases | None = None,\n    amplitude: int = 0,\n) -> tuple[tuple[Any, ...], tuple[Any, ...]] | None:",
    "def odd_links(families: Any, states: Any, direction: int) -> tuple[Any, ...]:\n    \"\"\"U24_METRIC (hand y1, 2026-10-25): the flux lines g_0a of every held row of the content that carries them, summed at the weight 1 (every plane reads every holder of the volume at 1, derived.with_reads), each along the Node's six Links as V_ij = V_a(i) + V_a(j) through the +a Port and -(V_a(i - a) + V_a(i)) through the -a Port (`link_levels` at (1, 1), gravity's turn + along the current; ALGEBRA.md, The clock family on the Ports), at the level the step in `direction` starts from (the same number read back).\"\"\"\n    levels: list[Any] = [0, 0, 0]\n    for family, state in zip(families, states, strict=True):\n        if family.held and not family.wronskian and family.flux:\n            for a in range(AXES):\n                levels[a] = levels[a] + level_at(state.lines[1 + AXES + a], direction)\n    return link_levels((levels[0], levels[1], levels[2]), (1, 1))\n\n\n@cache\ndef rotation_unit(pair: tuple[int, int], gamma: int) -> int:\n    \"\"\"U24_METRIC (hand y1, 2026-10-25): K = omega_0 Gamma, the family's rest rotation to the unit, cos omega_0 = num / den, found on the phase line's own orbit by a search by comparisons and no root (ALGEBRA.md, The clock family on the Ports: 'computed from the pair [num, den] with one rounding, as the clock's pace is computed from the content'): the pair at the amplitude X = Gamma 2^20 iterated act by act at the line's unit 2 Gamma (one act the half angle 1 / (2 Gamma), features/phase.iterate), the count n the first at which den x (X cos(n / (2 Gamma))) falls below num x X, so omega_0 = n / (2 Gamma) to the half angle and K = rounded(n, 2); 0 for a massless pair.\"\"\"\n    num, den = pair\n    if abs(num) >= den:\n        return 0\n    unit = 2 * gamma\n    amplitude = gamma * (1 << 20)\n    cosine, sine = seed(amplitude, unit)\n    count = 0\n    while den * int(cosine[0]) >= num * amplitude:\n        cosine, sine = iterate((cosine, sine), 1, unit)\n        count += 1\n    return int(rounded(count, 2))\n\n\ndef fold_pairs(\n    pair: tuple[int, int],\n    gamma: int,\n    factors: tuple[Any, ...],\n    links: tuple[Any, ...],\n    evens: tuple[Any, ...],\n    odds: tuple[Any, ...],\n) -> tuple[tuple[Any, ...], tuple[Any, ...]]:\n    \"\"\"U24_METRIC (hand y1, 2026-10-25): gravity's pair on each Link in Port order composed with the sign's (ALGEBRA.md, The clock family on the Ports, the engine V2's fold form): X^c_g = X_ij and X^s_g = sgn(V_ij) rounded(6 X_ij K |V_ij| / Gamma^2), K = omega_0 Gamma (`rotation_unit`), the angle 12 V omega_0 = 4 V omega_0 / c^2 along the current (c^2 = 1 / 3), odd in V exactly (`signed_rounded`) so that X^s_ji = -X^s_ij; the product with the sign's pair (`evens`, `odds`) rounded once into the Link unit X_ij: ((X^c_s X_ij - X^s_s X^s_g) div X_ij, (X^s_s X_ij + X^c_s X^s_g) div X_ij), the composed odd part odd under the 48's axis reversal (both odd parts negated) and the even part even; a massless pair (K = 0) turns nothing.\"\"\"\n    k = rotation_unit(pair, gamma)\n    found_even: list[Any] = []\n    found_odd: list[Any] = []\n    for factor, link, c, s in zip(factors, links, evens, odds, strict=True):\n        x = 2 * pair[0] * factor\n        odd = signed_rounded(6 * x * k * link, gamma * gamma)\n        found_even.append(signed_rounded(c * x - s * odd, x))\n        found_odd.append(signed_rounded(s * x + c * odd, x))\n    return tuple(found_even), tuple(found_odd)\n\n\ndef link_pairs(\n    pair: tuple[int, int],\n    gamma: int,\n    content: Any,\n    factors: tuple[Any, ...],\n    sign: tuple[Any, ...] | None,\n    phases: Phases | None = None,\n    amplitude: int = 0,\n    gravity: tuple[Any, ...] | None = None,\n) -> tuple[tuple[Any, ...], tuple[Any, ...]] | None:",
)
edit(
    "plane.py",
    "        evens, odds = tuple(f[0] for f in phased), tuple(f[1] for f in phased)\n    pace = paces.link_pace_of(gamma, content)\n",
    "        evens, odds = tuple(f[0] for f in phased), tuple(f[1] for f in phased)\n    if gravity is not None:  # U24_METRIC: gravity's fold from the flux lines along the Links (`fold_pairs`)\n        evens, odds = fold_pairs(pair, gamma, factors, gravity, evens, odds)\n    pace = paces.link_pace_of(gamma, content)\n",
)
edit("plane.py", "from event_universe.features.phase import fold, signed_read, signed_rounded\n", "from event_universe.features.phase import fold, iterate, seed, signed_read, signed_rounded\n")
edit("flux.py", "from event_universe.plane import link_levels, link_pairs, phase_links\n", "from event_universe.plane import link_levels, link_pairs, odd_links, phase_links\n")
edit(
    "flux.py",
    "    found = link_pairs(families[index].pair, gamma, content, factors, sign, phases, amplitude)\n",
    "    gravity = (\n        odd_links(families, states, direction) if METRIC and sign is not None else None\n    )  # U24_METRIC: the flux lines along the Links, read by every turned plane (a real line reads none: the theorem of The clock family on the Ports)\n    found = link_pairs(families[index].pair, gamma, content, factors, sign, phases, amplitude, gravity)\n",
)

if __name__ == "__main__":
    changed: dict[str, int] = {}
    for path, old, new in EDITS:
        file = ROOT / path
        text = file.read_text(encoding="utf-8")
        if text.count(old) != 1:
            print(f"REFUSED {path}: the text occurs {text.count(old)} times:\n{old}")
            sys.exit(1)
        file.write_text(text.replace(old, new), encoding="utf-8")
        changed[path] = changed.get(path, 0) + 1
        print(f"edited {path}: {old.strip().splitlines()[0][:90]!r} -> {new.strip().splitlines()[0][:90]!r}")
    print("files", changed)
