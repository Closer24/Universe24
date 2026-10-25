"""Hand z1, brief z: the seed as a list of lays, read from the world file's `seed` key by this tool and laid through the
engine's one lay act (`lay.laid`), the engine's own seed (`seed.uniform_seed`) stood aside for the run (the loader of
this branch refuses the `seed` key by name, `loader/keys.keyed`: the deviation named in the report). Three forms:
`sea` (one quantum of the massless row at every Node: the level now the drift v = isqrt(T), the before 0, laid as built
with no weights, ALGEBRA.md, The uniform seed is a lay), `hole` (the sea's quantum removed at one Node: the one-Node lay
of -v now, laid as built), `at` (a packet with a centre, a half-width and a count: on the massless row the drift at the
centre, sigma 0, the sea plus one; on a gapped plane row the conjugate pair's records at the law's raised-cosine
envelope of half-width `width` (ALGEBRA.md, The packet lay (h): (1 + cos(pi j / h)) / 2, exact in the integers at
h = 2 (2, 1) and h = 3 (4, 3, 1)), each record at rest, re_before = re_now cos omega_0, im_before = sense re_now sin
omega_0 at the vacuum's content, the amplitude the largest integer whose share reads at most `quanta` of the record's
unit, the division act alone). Integers only; no float anywhere in this module."""

from __future__ import annotations

import json
import sys
from math import isqrt
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from event_universe import lay, records, seed, share, world_files  # noqa: E402
from event_universe.core.paces import sine_den  # noqa: E402
from event_universe.core.rule3 import division_forward, largest_below  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.loader.circle import lift_points  # noqa: E402
from event_universe.loader.derived import count_wall  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402

ENGINE_KEYS = ("universe", "shape", "intervals")
FORMS = ("sea", "hole", "at")
ENVELOPES = {2: (2, 1), 3: (4, 3, 1)}  # the raised cosine's integer weights per axis at the half-widths 2 and 3


def read_seed_world(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """The world file with its `seed` list: the engine's three keys and the list apart."""
    document = json.loads(path.read_text(encoding="utf-8"))
    seeds = document.get("seed", [])
    engine = {key: document[key] for key in ENGINE_KEYS}
    return engine, seeds


def refused(seeds: list[dict[str, Any]], families: Any, shape: tuple[int, int, int]) -> list[str]:
    """What the loader refuses by name: a form not among the three; a lay naming a family by a name and not a pair;
    a pair no row of the universe carries; a gapped `at` of width 0 (a one-Node body: a body is laid over its packet);
    a `sea` or `hole` on a gapped row (the drift is the massless row's double root alone); a Node off the board."""
    found = []
    pairs = {tuple(f.pair): i for i, f in enumerate(families)}
    for number, entry in enumerate(seeds):
        form = entry.get("lay")
        if form not in FORMS:
            found.append(f"lay {number}: the form {form!r} is none of {list(FORMS)}")
            continue
        if "family" in entry or "name" in entry:
            found.append(f"lay {number}: a lay named by a family is refused; a row is its pair [num, den]")
        if form in ("sea", "at"):
            row = entry.get("row")
            if not (isinstance(row, list) and len(row) == 2 and tuple(row) in pairs):
                found.append(f"lay {number}: the row {row} is no pair of the universe's rows")
                continue
            massless = row[0] == row[1]
            if form == "sea" and not massless:
                found.append(f"lay {number}: a sea of a gapped row has no drift (the double root is the massless row's)")
            if form == "at" and not massless and int(entry.get("width", 0)) not in ENVELOPES:
                found.append(f"lay {number}: a gapped packet of width {entry.get('width')} is refused: a body is laid over its packet, the half-width 2 or 3 (the exact raised cosines)")
        for key in ("at", "centre"):
            if key in entry:
                node = entry[key]
                if not (isinstance(node, list) and len(node) == 3 and all(0 <= int(x) < s for x, s in zip(node, shape, strict=True))):
                    found.append(f"lay {number}: the Node {node} is off the board {list(shape)}")
    return found


def drift_of(action: int) -> int:
    """The law's form of the drift: the largest v with v^2 <= T (seed.drift_of, largest_below), the share 3 den v^2 against the unit 3 den T."""
    return largest_below(action)


def mask_of(shape: tuple[int, int, int], node: list[int]) -> np.ndarray:
    found = np.zeros(shape, dtype=bool)
    found[tuple(int(x) for x in node)] = True
    return found


def envelope(shape: tuple[int, int, int], centre: list[int], width: int) -> np.ndarray:
    """The law's raised-cosine envelope as integer weights over the torus about `centre`: the product over the three axes of the weights at the torus distance per axis, 0 beyond the half-width."""
    weights = ENVELOPES[width]
    found = np.zeros(shape, dtype=object)
    for where in np.ndindex(*shape):
        product = 1
        for a in range(3):
            d = (where[a] - centre[a]) % shape[a]
            d = min(d, shape[a] - d)
            product *= weights[d] if d < len(weights) else 0
        found[where] = product
    return found


def rest_pair(num: int, den: int) -> tuple[int, int, int]:
    """cos omega_0 and sin omega_0 of a pair as integers over den at the vacuum's content: (num, s, den), s = isqrt(den^2 - num^2) exact for a Pythagorean pair."""
    return num, sine_den(num, den), den


def lay_sea(board: Lattice, index: int) -> dict[str, Any]:
    """The sea: every line of the massless row's first record at the drift v now and 0 before at every Node, one call of the act with no weights, laid as built."""
    from event_universe.emission import emitted_lines

    family, drift = board.families[index], drift_of(board.world.quantum_action)
    now, before = records.full(board.shape, drift, board.kind), records.zeros(board.shape, board.kind)
    first = records.record_slice(family, 0).start
    for line in emitted_lines(family):
        lay.laid(board, index, first + line, (now, before), None, None)
    return {"form": "sea", "row": list(family.pair), "drift": drift, "nodes": int(np.prod(board.shape))}


def lay_hole(board: Lattice, index: int, at: list[int]) -> dict[str, Any]:
    """The hole: the sea's quantum removed at one Node, the one-Node lay of -v on the level now, laid as built."""
    from event_universe.emission import emitted_lines

    family, drift = board.families[index], drift_of(board.world.quantum_action)
    here = mask_of(board.shape, at)
    first = records.record_slice(family, 0).start
    zeros = records.zeros(board.shape, board.kind)
    for line in emitted_lines(family):
        lay.laid(board, index, first + line, (np.where(here, -drift, 0).astype(board.kind), zeros), None, None, here)
    return {"form": "hole", "at": list(at), "drift": drift}


def lay_at_massless(board: Lattice, index: int, at: list[int], quanta: int) -> dict[str, Any]:
    """The sea plus one: `quanta` quanta more of the massless row at one Node, the drift each, laid as built (the seed hand's S1, tests/laws_universe.sea_plus_one)."""
    from event_universe.emission import emitted_lines

    family, drift = board.families[index], drift_of(board.world.quantum_action)
    here = mask_of(board.shape, at)
    first = records.record_slice(family, 0).start
    zeros = records.zeros(board.shape, board.kind)
    for line in emitted_lines(family):
        lay.laid(board, index, first + line, (np.where(here, quanta * drift, 0).astype(board.kind), zeros), None, None, here)
    return {"form": "at", "row": list(family.pair), "centre": list(at), "quanta": quanta, "drift": drift}


def record_share(board: Lattice, k: int, r: int) -> np.ndarray:
    content, factors = board.read(k, 1, r)
    own = share.family_share(board.families[k], board.lines_of(k, r), board.world.node_clock, content, factors, board.unit)
    return np.asarray(own, dtype=object)


def lay_at_gapped(board: Lattice, index: int, centre: list[int], width: int, quanta: int) -> dict[str, Any]:
    """A body: the conjugate pair of the plane row `index` (its two records, the senses -1 and 1, as the birth lays them) each at `quanta` quanta over the law's raised-cosine envelope of half-width `width` about `centre`, each record at rest at the vacuum's content: re_now = (A w_i) div w_0, re_before = (re_now num) div den, im_now = 0, im_before = sense (re_now s) div den, s = isqrt(den^2 - num^2); A the largest integer at which the record's share, read by the engine's own form, is at most `quanta` of its unit W_rec (a search by comparisons, no root but isqrt's bisection); laid through the one act with the envelope as the weights (a gapped family takes no correction), the remainder at the lay's origin."""
    family = board.families[index]
    num, s, den = rest_pair(*family.pair)
    board.born_point(index)
    weights = envelope(board.shape, centre, width)
    top = int(weights.max())
    unit = count_wall(family, board.world.quantum_action)
    kind = board.kind
    found = []
    for record, sense in ((0, -1), (1, 1)):
        first = records.record_slice(family, record).start
        remainder = board.states[index].lines[first].remainder

        def levels(amplitude: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
            re_now = np.vectorize(lambda w: (amplitude * int(w)) // top, otypes=[object])(weights)
            re_before = np.vectorize(lambda v: (int(v) * num) // den, otypes=[object])(re_now)
            im_before = np.vectorize(lambda v: sense * ((int(v) * s) // den), otypes=[object])(re_now)
            return re_now, re_before, np.zeros(board.shape, dtype=object), im_before

        content, factors = board.read(index, 1, record)

        def share_at(amplitude: int) -> int:
            re_now, re_before, im_now, im_before = levels(amplitude)
            lines = [records.Record(re_now, re_before, remainder), records.Record(im_now, im_before, remainder)]
            return int(np.asarray(share.family_share(family, lines, board.world.node_clock, content, factors, board.unit), dtype=object).sum())

        low, high = 0, 1
        while share_at(high) <= quanta * unit:
            high += high
        while high - low > 1:  # the largest amplitude whose share is at most the count: comparisons alone
            middle = (low + high) // 2
            if share_at(middle) <= quanta * unit:
                low = middle
            else:
                high = middle
        amplitude = low
        re_now, re_before, im_now, im_before = levels(amplitude)
        lay.laid(board, index, first, (re_now.astype(kind), re_before.astype(kind)), weights, None, weights != 0)
        lay.laid(board, index, first + 1, (im_now.astype(kind), im_before.astype(kind)), weights, None, weights != 0)
        total = int(record_share(board, index, record).sum())
        found.append({"record": record, "sense": sense, "amplitude": amplitude, "share": total, "unit": unit, "quanta_milli": (1000 * total) // unit, "peak_level": int(re_now.max())})
    return {"form": "at", "row": list(family.pair), "centre": list(centre), "width": width, "quanta": quanta, "cos_num": num, "sin_num": s, "den": den, "g_milli": (1000 * (den - num)) // den, "records": found, "nodes_laid": int((weights != 0).sum())}


def lay_list(board: Lattice, seeds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The seed list laid in its order through the one act, each entry its integers back."""
    pairs = {tuple(f.pair): i for i, f in enumerate(board.families)}
    found = []
    for entry in seeds:
        form = entry["lay"]
        if form == "sea":
            found.append(lay_sea(board, pairs[tuple(entry["row"])]))
        elif form == "hole":
            found.append(lay_hole(board, board.world.seed, entry["at"]))
        elif form == "at":
            index = pairs[tuple(entry["row"])]
            if entry["row"][0] == entry["row"][1]:
                found.append(lay_at_massless(board, index, entry["centre"], int(entry.get("quanta", 1))))
            else:
                found.append(lay_at_gapped(board, index, entry["centre"], int(entry["width"]), int(entry["quanta"])))
    return found


def board_of(path: Path, folder: Path, output: Any = None) -> tuple[Lattice, list[dict[str, Any]], list[dict[str, Any]]]:
    """The seed world loaded: the engine's three keys written beside the universe into `folder` for the loader, the massless lays (`sea`, `hole`, the massless `at`) laid in the engine's own seed's place before the start, the gapped packets after the start (their records born at the lay, `born_point`, which needs the start's walls); the Lattice, the lays' integers and the refusals."""
    engine, seeds = read_seed_world(path)
    universe = (path.parent / engine["universe"]).read_text(encoding="utf-8") if not Path(engine["universe"]).is_absolute() else Path(engine["universe"]).read_text(encoding="utf-8")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(universe, encoding="utf-8")
    (folder / "w.json").write_text(json.dumps({**engine, "universe": "u.json"}), encoding="utf-8")
    world_files.REPOSITORY_ROOT = folder
    world = load_world(folder / "w.json")
    bad = refused(seeds, world.families, world.shape)
    if bad:
        raise ValueError("; ".join(bad))
    before_start = [e for e in seeds if e["lay"] in ("sea", "hole") or (e["lay"] == "at" and e["row"][0] == e["row"][1])]
    after_start = [e for e in seeds if e not in before_start]
    laid: list[dict[str, Any]] = []
    real = seed.uniform_seed

    def seeded(board: Lattice, index: int) -> None:
        laid.extend(lay_list(board, before_start))

    seed.uniform_seed = seeded
    try:
        board = Lattice(world, output=output)
    finally:
        seed.uniform_seed = real
    laid.extend(lay_list(board, after_start))
    return board, laid, bad


def light_quanta(board: Lattice) -> tuple[int, int, int]:
    """The massless row's share summed over the board in the current's units, the quanta at the vacuum's weight by the division act (share div W_c, and the per-Node rounding's sum)."""
    shares, _frozen = board.share_of(board.world.seed)
    total = int(np.asarray(shares, dtype=object).sum())
    unit = board.credit.units[board.world.seed]
    per_node = int(np.asarray(share.quanta_of(shares, unit, object), dtype=object).sum())
    return total, int(division_forward(total, unit, 0)[0]), per_node


def lifts_of(den: int, action: int) -> list[dict[str, int]]:
    """den's lifts with their gaps and sines as integer readings."""
    found = []
    for vector, num, s in lift_points(den):
        found.append({"vector": list(vector), "num": num, "sin": s, "g_milli": (1000 * (den - num)) // den, "sin_milli": (1000 * s) // den, "walls_pair": 2 * 3 * action * s, "W_c": 3 * den * action, "walls_over_Wc_milli": (1000 * 2 * 3 * action * s) // (3 * den * action)})
    return found
