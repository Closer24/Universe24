"""U1 (brief u, items (a) and (d)): the three shapes against the lines the engine holds. The tests' small universe (den 1,021, Gamma 1,000, T 36,000, G 16) on the bare 3-cube torus is loaded as the engine loads it; every line of every family is named by the loader's attributes (held, wronskian, rotation, axes, plane, flux) and its position in its row and classified into the 10 (the metric), the 4 (the potential), the 2 (a plane) or a fourth shape; the integers per Node before the first birth and after it are read through tools/node_integers.py; the walls' bit lengths; Rule3's integers of the sign's time line against light's at the vacuum content and at the board's content; the arithmetic of the fixed count under the three shapes. Integer readings only; the output beside the script as shapes_count.json.

Run: PYTHONPATH=<worktree>/src TMPDIR=/dev/shm/tmp python tools/derivations/open_items/H-Three-Shapes-1/shapes_count.py"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from event_universe import node, registry, world_files  # noqa: E402
from event_universe.core.ports import AXES, LINK_UNIT  # noqa: E402
from event_universe.core.rule3 import wall_of  # noqa: E402
from event_universe.lattice import Lattice  # noqa: E402
from event_universe.loader import universe  # noqa: E402
from event_universe.world_files import load_world  # noqa: E402
from tests.laws_universe import GAMMA, SMALL, bare_torus  # noqa: E402


def load_tool(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


TOOL = load_tool("node_integers", ROOT / "tools" / "node_integers.py")
LEVELS = 3  # a line's integers at a Node: now, before, remainder


def bits_of(value) -> int:  # type: ignore[no-untyped-def]
    flat = np.asarray(value, dtype=object).reshape(-1).tolist()
    return max(abs(int(x)).bit_length() for x in flat)


def classify(board: Lattice) -> list[dict]:  # type: ignore[type-arg]
    """Every line of every family named and classified into the three shapes by the loader's attributes."""
    found = []
    for index, family in enumerate(board.families):
        state = board.states[index]
        rows = registry.records_of(family, state.lines)
        entry = {
            "family": family.name,
            "pair": list(family.pair),
            "held": family.held,
            "wronskian": family.wronskian,
            "rotation": family.rotation,
            "axes": family.axes,
            "plane": family.plane,
            "flux": family.flux,
            "width": family.width,
            "rows_or_records": rows,
            "lines": len(state.lines),
            "write_remainders": len(state.write_remainders),
            "phase_lines": sum(len(r) for r in state.phases),
        }
        if family.held and not family.wronskian:
            entry["shape"] = "10 (the metric g)"
            entry["lines_named"] = ["g_00: the time line (the volume X, the clock; the stress's trace written into it)"] + [
                f"g_{a}{a}: tension line {a} (3 T_aa - SUM T_bb, the traceless diagonal; even under the axis's inversion)"
                for a in "xyz"
            ]
            entry["held_of_the_10"] = 1 + AXES
            entry["missing_of_the_10"] = [
                "g_xy, g_yz, g_zx: the three shear lines (T_2g), named in the docstrings (records.axis_positions, derived.held_write_of) and held by no row of the loader",
                "g_0x, g_0y, g_0z: the three odd lines of the flux (T_1u, Row.flux False in universe.rows_of), the momentum density's seat",
            ]
            entry["extra"] = [f"{len(state.write_remainders)} write remainders (one per held line, the write's carried division)"]
        elif family.held and family.wronskian:
            entry["shape"] = "4 (the potential A_mu) per row"
            entry["lines_named_per_row"] = ["A_0: the time line (sourced by the Wronskian, the charge density)"] + [
                f"A_{a}: odd line {a} (sourced by the sense current J_{a}; negated under the axis's inversion)" for a in "xyz"
            ]
            entry["held_of_the_4"] = family.width
            entry["rows"] = rows
            entry["extra"] = [
                f"{len(state.write_remainders)} write remainders (one per held line)",
                f"{sum(len(r) for r in state.phases)} phase lines ({len([r for r in state.phases if r])} rows beyond the free row x 10: 6 pair lines cos/sin per owned Link, 3 count lines, 1 phase row Phi)",
                f"{rows - 1} rows beyond the one row (one per charged record, No record reads its own write; the law's sentence of 19:0x UTC has one row)",
            ]
        elif family.plane:
            entry["shape"] = "2 (a plane: re, im) per record"
            entry["lines_named_per_record"] = ["re", "im (the sense its Wronskian's sign)"]
        else:
            entry["shape"] = "1 (a scalar line): a fourth shape, light's own row, outside the owner's three"
            entry["lines_named"] = ["the massless line (den, den), the seed laid on every Node but the origin"]
        found.append(entry)
    return found


def main() -> None:
    folder = Path("/dev/shm/tmp/u1_count")
    folder.mkdir(parents=True, exist_ok=True)
    world_files.REPOSITORY_ROOT = folder
    lines: list[dict] = []  # type: ignore[type-arg]
    board = Lattice(load_world(bare_torus(folder, 3, 60)), output=lines.append)
    den, unit = SMALL["integers"]["den"], board.unit
    out: dict = {"universe": SMALL, "shape": list(board.shape), "width_bits": board.world.width.bit_length()}  # type: ignore[type-arg]
    out["universe_file_keys"] = list(universe.INTEGER_KEYS)
    out["rows_derived_from_den"] = [[row.name, list(row.pair), row.lines] for row in universe.rows_of(SMALL["integers"])]
    out["families_at_the_start"] = classify(board)
    start = TOOL.line_of(board)
    out["integers_before_the_first_birth"] = {k: start[k] for k in ("integers", "per_family", "same_at_every_node", "largest_bit_length", "largest_at")}
    while not board.born_at and board.interval < 60:
        board.step()
    after = TOOL.line_of(board)
    out["first_birth_interval"] = board.interval
    out["born_families"] = [board.families[i].name for at in sorted(board.born_at) for i in board.born_at[at]]
    out["integers_after_the_first_birth"] = {k: after[k] for k in ("integers", "per_family", "same_at_every_node", "largest_bit_length", "largest_at")}
    out["growth_per_record"] = {
        "records_born": sum(registry.records_of(board.families[i], board.states[i].lines) for i in board.turning),
        "integers_grown": after["integers"] - start["integers"],
    }
    out["families_after_the_first_birth"] = classify(board)
    # the walls' bit lengths: Rule3's wall, the write walls, their product (whether the write remainder could ride the line's third integer)
    rule_wall = wall_of(den, GAMMA, unit)
    walls = {"rule3_wall": rule_wall, "rule3_wall_bits": rule_wall.bit_length()}
    for index in board.held:
        family = board.families[index]
        line_walls = [int(np.asarray(w, dtype=object).reshape(-1).max()) for w in board.write_walls[index]]
        walls[family.name] = {
            "write_walls": line_walls[: family.width],
            "write_wall_bits": [w.bit_length() for w in line_walls[: family.width]],
            "product_with_rule3_wall_bits": [(w * rule_wall).bit_length() for w in line_walls[: family.width]],
        }
    walls["product_bits_at_the_54_bit_den"] = {
        "den": 15162856759112389,
        "rule3_wall_bits": wall_of(15162856759112389, GAMMA, unit).bit_length(),
        "volume_time_wall_bits_scaled": (int(walls[board.families[board.held[0]].name]["write_walls"][0]) * 15162856759112389 // den).bit_length(),
        "product_bits": (wall_of(15162856759112389, GAMMA, unit) * int(walls[board.families[board.held[0]].name]["write_walls"][0]) * 15162856759112389 // den).bit_length(),
    }
    out["walls"] = walls
    # Rule3's integers: the sign's time line against light's, at the vacuum and at the board's content
    light, sign = board.world.seed, board.held[1]
    vac_light = node.rule_of(board.families[light], GAMMA, 0, None, unit)
    vac_sign = node.rule_of(board.families[sign], GAMMA, 0, None, unit)
    centre = (1, 1, 1)
    content, factors = board.read(light, 1, 0)
    at_board = node.rule_of(board.families[light], GAMMA, content, factors, unit)
    out["rule3_sign_against_light"] = {
        "vacuum_light": {"reach": int(vac_light.reaches[0]), "mass": int(vac_light.mass), "wall": int(vac_light.wall)},
        "vacuum_sign": {"reach": int(vac_sign.reaches[0]), "mass": int(vac_sign.mass), "wall": int(vac_sign.wall)},
        "same_at_the_vacuum": vac_light == vac_sign,
        "light_at_the_boards_content_centre": {
            "content": int(np.asarray(content)[centre]),
            "reach_port_0": int(np.asarray(at_board.reaches[0], dtype=object)[centre]),
            "mass": int(np.asarray(at_board.mass, dtype=object)[centre]),
        },
        "sign_reads_content": bool(any(not board.families[r.family].rotation for r in board.families[sign].reads)),
        "note": "the sign's row reads no content (derived.with_reads): its Rule3 steps at the vacuum's paces at every Node while light steps at the Node's; the potential does not gravitate on this engine",
    }
    # the fixed count under the three shapes, arithmetic on the engine's own per-record numbers
    planes = 3
    sign_row = board.families[sign].width
    phase_per_row = 2 * AXES + AXES + 1
    out["count_arithmetic_three_planes"] = {
        "engine_as_it_stands_one_record_per_plane": start["integers"] + planes * (LEVELS * 2 + LEVELS * sign_row + sign_row + LEVELS * phase_per_row),
        "three_shapes_sign_one_row_no_phase_lines": 10 * LEVELS + 10 + 4 * LEVELS + 4 + planes * 2 * LEVELS,
        "plus_phase_lines_as_the_engine_holds_them_one_row": 10 * LEVELS + 10 + 4 * LEVELS + 4 + planes * 2 * LEVELS + LEVELS * phase_per_row,
        "plus_phase_without_the_count_cache": 10 * LEVELS + 10 + 4 * LEVELS + 4 + planes * 2 * LEVELS + LEVELS * (2 * AXES + 1),
        "plus_phi_alone": 10 * LEVELS + 10 + 4 * LEVELS + 4 + planes * 2 * LEVELS + LEVELS,
        "lights_own_row_if_kept": LEVELS,
        "engine_holds_of_the_10": 1 + AXES,
        "engine_holds_of_the_4": sign_row,
        "engine_holds_of_the_2": 2,
    }
    out["births_lines"] = [
        {k: v for k, v in line.items() if k in ("event", "interval", "family", "children", "senses", "nodes", "taken", "walls", "excess", "records")}
        for line in lines
        if line.get("event") in ("birth", "refused")
    ][:6]
    (HERE / "shapes_count.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("integers_before_the_first_birth", "first_birth_interval", "growth_per_record", "count_arithmetic_three_planes")}, default=str))
    print(json.dumps(out["integers_after_the_first_birth"], default=str))
    print(json.dumps(out["walls"], default=str))
    print(json.dumps(out["rule3_sign_against_light"], default=str))


if __name__ == "__main__":
    main()
