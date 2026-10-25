"""The pump's two faces measured apart (hand V2, 2026-10-25; the brief's item (a)): the count of the uniform massless sea's quanta on the bare 3-cube torus of the tests' small universe (den 1,021, Gamma 1,000, T 36,000), (A) at a content set by hand at every interval with the volume's write off, so that only the read's unit can move, and (B) on the plain course with the write on, the acts of the interval without the close (no birth), so that the unit and the dynamics move together. Read at each content, integers: the drift now - before of the sea at every Node (the dynamics), the share per Node in the current's units and in quanta of W_c = 3 den T (the engine's own `share_of` and `quanta`), the paces, and the prediction (3 den (now - before)^2 Gamma^2) div p_a^2 from the conserved form's Node term with its weight 1 / p_a^2 (ALGEBRA.md, The count is the record's share; The clock is the Node's, the tension is the Link's). (B) reads beside them the volume's second difference per interval against its two derived terms, the write (4 v^2 x SCALE) div (E_s T) (the form v^2 at the factor e^(-4 U) times the volume Gamma e^(4 U)) and the pair's mass D X div w, D = 12 (den - num) p_0^2 G^2. Command: PYTHONPATH=src TMPDIR=/dev/shm/tmp /home/user/Universe24/venv314/bin/python tools/derivations/open_items/H-Pump-And-Redshift-2/pump_unit.py"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np

from common import ACTION, DEN, GAMMA, SCALE, dump, impose_volume, lattice_of, paces_at, quotient, volume_at, write_off

from event_universe import seed
from event_universe.core import rule3
from event_universe.core.ports import LINK_UNIT
from event_universe.core.rule3 import division_forward
from event_universe.features import volume
from tests.laws_universe import uniform_sea

LEVELS = (0, 100, 200, 400, 600, 800, 1000, 1200, 1500, 1800, 2000)
STEPS = 12  # intervals stepped at each imposed content before the reading
COURSE = 320  # intervals of the plain course


def sea_board(folder: Path):  # type: ignore[no-untyped-def]
    """The bare 3-cube with the uniform sea laid (the law's seed to 2026-10-24, laid by name as the tests lay it: the origin holds a quantum too, so the board has no hole and no digit)."""
    seed.uniform_seed = uniform_sea
    return lattice_of(folder, (3, 3, 3))


def reading(board, light: int) -> dict:  # type: ignore[no-untyped-def]
    """The sea read at the Nodes, integers: the drift, the share, the count in quanta of W_c, the content read."""
    line = board.states[light].lines[0]
    now = np.asarray(line.now, dtype=object)
    before = np.asarray(line.before, dtype=object)
    drift = now - before
    content = np.asarray(board.read(light)[0], dtype=object).reshape(-1)
    shares, cold = board.share_of(light)
    quanta, _ = board.quanta(light)
    shares = np.asarray(shares, dtype=object).reshape(-1)
    unit = int(board.credit.units[light])
    total = int(sum(int(s) for s in shares))
    return {
        "drift_min": int(drift.min()),
        "drift_max": int(drift.max()),
        "content_min": int(content.min()),
        "content_max": int(content.max()),
        "share_min": int(shares.min()),
        "share_max": int(shares.max()),
        "share_total_over_W_c": quotient(total, unit * len(shares)),
        "quanta_min": int(np.asarray(quanta).min()),
        "quanta_max": int(np.asarray(quanta).max()),
        "quanta_total": int(np.asarray(quanta, dtype=object).sum()),
        "frozen": int(np.asarray(cold).sum()),
        "W_c": unit,
    }


def predicted(level: int, drift: int) -> dict:
    """The conserved form's Node term of the uniform sea at a content, (3 den (now - before)^2 Gamma^2) div p_a^2 in the current's units, and its count in quanta of W_c, each a quotient with its remainder."""
    found = paces_at(level)
    numerator = 3 * DEN * drift * drift * GAMMA * GAMMA
    share = quotient(numerator, found["p_a"] * found["p_a"])
    count = quotient(numerator, found["p_a"] * found["p_a"] * 3 * DEN * ACTION)
    return {"share": share, "quanta": count, **found}


def part_a(folder: Path) -> list[dict]:
    """(A) The unit alone: the content imposed, the write off, twelve intervals at each content, the sea read."""
    board = sea_board(folder / "a")
    light = board.world.seed
    write_off(board)
    v = seed.drift_of(ACTION)
    rows = []
    for level in LEVELS:
        x = volume_at(level)
        for _ in range(STEPS):
            impose_volume(board, x, x - x // 2)  # a rising line, so the fifth act never fires
            board.advanced_to_the_close()
            assert not board.turned.any(), "a top fired under the imposed volume"
        impose_volume(board, x, x - x // 2)
        read = reading(board, light)
        model = predicted(level, v)
        row = {"level": level, "X": x, "v": v, **model, **read}
        row["share_less_predicted"] = read["share_min"] - model["share"]["quotient"]
        rows.append(row)
        print(
            f"A level {level:5d} X {x:12d} p_0 {model['p_0']:4d} p_a {model['p_a']:4d} e^U x1e6 {model['e_U_scaled']:9d} "
            f"weight x1e6 {model['weight_scaled']:13d} drift {read['drift_min']}..{read['drift_max']} "
            f"share {read['share_min']}..{read['share_max']} predicted {model['share']['quotient']} "
            f"(diff {row['share_less_predicted']}) quanta {read['quanta_min']}..{read['quanta_max']} "
            f"predicted quanta {model['quanta']['quotient']} rem {model['quanta']['remainder']}"
        )
    return rows


def part_b(folder: Path) -> list[dict]:
    """(B) The plain course with the write on, the interval's acts without the close: X, the level, the drift, the count, the volume's second difference against its two derived terms."""
    board = sea_board(folder / "b")
    light, held = board.world.seed, board.held[0]
    v = seed.drift_of(ACTION)
    num, den = board.families[held].pair
    wall = rule3.wall_of(den, GAMMA, LINK_UNIT)
    rows = []
    history = []
    first_two = None
    write_term = quotient(4 * v * v * SCALE, ACTION)  # 4 v^2 / (E_s T) at the scale, E_s = 1
    for interval in range(COURSE):
        line = board.states[held].lines[0]
        x_now = int(np.asarray(line.now, dtype=object).reshape(-1)[0])
        x_before = int(np.asarray(line.before, dtype=object).reshape(-1)[0])
        level = int(np.asarray(volume.level_of(GAMMA, np.array([x_now], dtype=object)))[0])
        found = paces_at(level)
        read = reading(board, light)
        history.append(x_now)
        mass = rule3.mass(num, den, found["p_0"], LINK_UNIT)
        row = {
            "interval": board.interval,
            "X": x_now,
            "X_before": x_before,
            **found,
            **read,
            "predicted_quanta": predicted(level, v)["quanta"],
            "write_term_scaled": write_term["quotient"],
            "mass_term_scaled": int(division_forward(mass * x_now * SCALE, wall, 0)[0]),
            "turned": int(board.turned.sum()),
        }
        if len(history) >= 3:
            row["X_second_difference"] = history[-1] - 2 * history[-2] + history[-3]
        if first_two is None and read["quanta_min"] >= 2:
            first_two = (board.interval, level, x_now)
        rows.append(row)
        if interval % 20 == 0 or row["turned"]:
            print(
                f"B interval {board.interval:4d} X {x_now:9d} level {level:5d} e^U x1e6 {found['e_U_scaled']:8d} drift "
                f"{read['drift_min']}..{read['drift_max']} quanta {read['quanta_min']}..{read['quanta_max']} "
                f"predicted {row['predicted_quanta']['quotient']} X'' {row.get('X_second_difference', '-')} "
                f"write x1e6 {row['write_term_scaled']} mass x1e6 {row['mass_term_scaled']} turned {row['turned']}"
            )
        board.advanced_to_the_close()
    tops = [r["interval"] for r in rows if r["turned"]]
    print(f"B first interval at two whole quanta per Node by the count alone (interval, level, X): {first_two}")
    print(f"B turns at: {tops[:5]} ... ({len(tops)} intervals with a turn); X max {max(history)} at {history.index(max(history))}")
    return rows


def main() -> None:
    folder = Path(tempfile.mkdtemp(prefix="v2_pump_"))
    a = part_a(folder)
    b = part_b(folder)
    print(dump("pump_unit.json", {"part_a": a, "part_b": b, "den": DEN, "gamma": GAMMA, "T": ACTION}))


if __name__ == "__main__":
    main()
