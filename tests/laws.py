"""The helpers of the law's tests: the tests' universe in the derived form (`UNIVERSE`, `universe_copy`, `universe_beside`, the charged row `CHARGED` and the seed row `LIGHT_ROW`), rows built by hand (`real_rows`), a module loaded by its path (`load_file`; the step's oracle `ORACLE` and its first form `arrivals_rule3`, tools/step_oracle.py), the refusal by name (`refused`), the flux form's linear sums (`linear_sum`, `weighted_linear_sum`) and a board's state for the run back (`board_state`, `same_state`). The builders of laid worlds (the packet, the flux world, the Coulomb chain, the turning universe) left 2026-10-24 with the tests of the cancelled worlds: the suite is the law's sentences at one Node on the bare torus with the one universe file."""

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from event_universe.lattice import Lattice
from event_universe.loader.derived import Row
from event_universe.records import Record

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "examples" / "events"
UNIVERSE = {  # the tests' universe at the rule's integers (Gamma 6,000, T 32,768, the width 63, G 16), its rows derived and nothing declared (2026-10-24): gravity, the holder of the volume, gapped at the declared seed's gap 999 over 1000 at the rule's den; the charge, the sign holder; the binding holder [2400, 2401], a second holder of the volume; matter, one real line; the rule's own universe examples/events/rule.json (gravity massless at the level weight 1,000 and the rest 60, the binding holder sourced by the form alone, every read declared) the tests' universe to 2026-10-24, kept by name as the record of the law to that day
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {"name": "gravity", "pair": [5994, 6000]},
        {"name": "charge", "pair": [6000, 6000]},
        {"name": "binding", "pair": [2400, 2401]},
        {"name": "matter", "pair": [4000, 6000], "dimension": 1},
    ],
}
# smallest body the generator lays on it in seconds (a test runs under 30 seconds, the owner's word)
CHARGED = {
    "name": "charged",
    "pair": [3600, 6000],
    "dimension": 2,
}  # a Pythagorean plane under the sign (2026-10-24: the sign's reader is Pythagorean; matter's [4000, 6000] until then); its reads derived, every holder, the sign's among them
LIGHT_ROW = {
    "name": "light",
    "pair": [6000, 6000],
    "dimension": 1,
}  # the one massless family of quanta, the seed every world is laid with (ALGEBRA.md, The uniform seed is a lay)


def universe_copy() -> dict[str, Any]:
    """The tests' universe, a copy of its own (`UNIVERSE`)."""
    return json.loads(json.dumps(UNIVERSE))


def real_rows(*rows: tuple[str, tuple[int, int], int, int | None]) -> list[Row]:
    """Rows of real lines built by hand (loader.derived.Row), each (name, pair, lines, level weight): one part, no plane, sourced by the form where it is held at the write weight 1, acting on the pace, and every row reading every held row among them at the weight 1 (the loader derives its rows from the pair and the dimension alone since 2026-10-24; these rows, a massless holder of the content among them, are the tests' own, no file's)."""
    held = tuple((name, 1) for name, _pair, _lines, weight in rows if weight is not None)
    return [Row(n, p, k, 1, False, False, False, w, w and 1, 0, held) for n, p, k, w in rows]


def load_file(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    sys.modules[name] = module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def refused(match: str, call, *args, **keys):
    with pytest.raises(ValueError, match=match) as refusal:
        call(*args, **keys)
    return refusal.value


def universe_beside(tmp_path, drop=(), charged=False, **pairs):  # type: ignore[no-untyped-def]
    """The tests' universe written beside a world as u.json (the families `drop` names left out, the reads derived from the rows that stand, a family's pair replaced where `pairs` names it, the charged row, a Pythagorean plane, added where `charged`)."""
    universe = universe_copy()
    universe["families"] = [family for family in universe["families"] if family["name"] not in drop]
    universe["families"] += [json.loads(json.dumps(CHARGED))] if charged else []
    for family in universe["families"]:
        family["pair"] = pairs.get(family["name"], family["pair"])
    if not any(  # the seed family where the universe holds no massless family of quanta, 2026-10-24
        "dimension" in f and f["pair"][0] == f["pair"][1] for f in universe["families"]
    ):
        universe["families"] += [json.loads(json.dumps(LIGHT_ROW))]
    (tmp_path / "u.json").write_text(json.dumps(universe), encoding="utf-8")


ORACLE = load_file(
    "step_oracle", ROOT / "tools" / "step_oracle.py"
)  # the step's oracle: the law's first form with the one Node's interval around it
arrivals_rule3 = (
    ORACLE.arrivals_rule3
)  # the first form of Rule3, written in the tool and in no file of src/


def linear_sum(wall: int, line: Record) -> int:
    """The linear sum of one line over the board, L = SUM over the Nodes of [w (now - before) + r], w the family's wall 6 den Gamma^2 G^2 (the flux form of Rule3: w (next - 2 now + before) + r' - r = SUM over the Ports of R_ij (arrival - now) - D now, so the Link terms pair off on a closed board read at one rate and L moves by the mass term alone, zero for light); a lattice reading, no level written."""
    now, before = line.now.astype(object), line.before.astype(object)
    return int((wall * (now - before) + line.remainder.astype(object)).sum())


def weighted_linear_sum(wall: int, line: Record, weights: Any) -> int:
    """The linear sum weighted by the Node's rate, L'' = SUM over the Nodes of weight_i x [w (now - before) + r] with weight_i = scale div p_i^2, scale the least common multiple of the distinct p_i^2 on the board, so that every weight is a whole number (the caller's, no division here): R_ij / p_i^2 = 2 num Q_ij G^2 is the same at a Link's two ends whatever their rates, so the weighted Link terms of the flux form pair off on a closed board at any fixed content profile and L'' of light is kept exactly where L moves by the pairing term; a lattice reading."""
    now, before = line.now.astype(object), line.before.astype(object)
    scaled = np.broadcast_to(np.asarray(weights, dtype=object), now.shape)
    return int(((wall * (now - before) + line.remainder.astype(object)) * scaled).sum())


def board_state(board: Lattice) -> list[tuple[list[tuple[Any, Any, Any]], list[Any]]]:
    """Every family's lines (now, before, remainder) and write remainders copied as Python's integers, the state a run back is compared against bit for bit (the light mean's test)."""
    copied = lambda a: np.asarray(a, dtype=object).copy()  # noqa: E731
    return [
        (
            [(copied(line.now), copied(line.before), copied(line.remainder)) for line in st.lines],
            [copied(r) for r in st.write_remainders],
        )
        for st in board.states
    ]


def same_state(
    a: list[tuple[list[tuple[Any, Any, Any]], list[Any]]],
    b: list[tuple[list[tuple[Any, Any, Any]], list[Any]]],
) -> bool:
    """Two states of `board_state` equal in every line and every write remainder."""
    return all(
        all(np.array_equal(u, v) for x, y in zip(la, lb, strict=True) for u, v in zip(x, y, strict=True))
        and all(np.array_equal(u, v) for u, v in zip(ra, rb, strict=True))
        for (la, ra), (lb, rb) in zip(a, b, strict=True)
    )
