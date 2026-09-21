"""A12 under the click, Malus's law from the table entries in force (the
mathematician's note docs/designs/malus/NOTE.md; the model owner's go,
record 330 of docs/LOG_2026-09-20.md; the run of 2026-09-21), on the three
worlds `malus_a`, `malus_b` and `malus_c` of series L's generator
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`malus`, the pin written before the run and the run's readings beside it).
The expected integers of docs/TEST_EXPECTATIONS.md ("The amplitude law:
Malus"), every number read from the register and none a literal here:

(a) the pin derived again from the worlds and the engine's own half-angle
    tables of 2N = 512 (`phase_cosines`, `phase_sines`): the cells'
    weights (with a rotation s1 before the read the read's label 0 carries
    C'[s1] and its label 1 S'[s1]; the end's channels + and - weigh
    C'[s2]^2 and S'[s2]^2 on the label 0 and S'[s2]^2 and C'[s2]^2 on the
    label 1) and the click's rungs b_k = (2 W C_k + T) // (2 T) over the
    wheel's W births equal the register's weights, rungs and counts, the
    pass the cell 0+ (BEAM_LAW note 46; the note's section 3);
(b) the replay of each world: the records of the ordinals 1 .. W are
    gathered with u over every residue of the wheel once, every gather's
    cells carry the register's rungs in the click's order, and the chosen
    cells (the read's label, the end's channel) count as the register's
    pin and as the run's reading, bit-exact (`malus_a` 0+ 128 and 0- 128,
    `malus_b` 0+ 0 and 0- 256, `malus_c` 0+, 0-, 1+ and 1- 64 each; the
    counts over every record gathered by the end as the run's); the books
    balanced at the end;
(c) the rotate keeps the record's u (the u question of the note's section
    2): on `malus_c` every `split` line at the rotation carries `rebirth`
    False, the record's own identity and its birth u, two per arriving row;
    the `rotate` line's setting, bit, turn and rows with the record's units
    before and after; the `read` line's two rows of the record (the labels
    0 and 1 at the rotation's amount and multiplicity, the set bit a half
    turn on), as registered.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
BASE = 1 << 32


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATOR = load("amplitude_make_worlds", ROOT / "examples" / "events" / "amplitude" / "make_worlds.py")
EXPECTATIONS = json.loads(
    (ROOT / "examples" / "events" / "amplitude" / "expectations.json").read_text("utf-8")
)
MALUS = EXPECTATIONS["malus"]
WORLDS = GENERATOR.malus_worlds()
NAMES = [name for name in MALUS if name.startswith("malus_")]


def settings_of(world: dict[str, object]) -> tuple[int | None, int]:
    """The first polariser's rotation (None where none is declared) and the
    last polariser's window, read from the world's tables."""
    rotate: int | None = None
    window: int | None = None
    for entry in world["measured"]:  # type: ignore[attr-defined]
        table = entry.get("table", {}).get("light", {})
        if "rotate" in table:
            rotate = int(table["rotate"]["setting"])
        if "phase_window" in table:
            window = int(table["phase_window"])
    assert window is not None
    return rotate, window


def derived(
    rotate: int | None, window: int, n: int, births: int
) -> tuple[dict[str, int], list[int], dict[str, int]]:
    """The note's section 3 on the engine's tables: the cells' weights in
    the click's order (the read's labels ascending, the channels + before
    -), the rungs and the counts over the births."""
    cosines, sines = phase_cosines(2 * n), phase_sines(2 * n)
    c2, s2 = cosines[window], sines[window]
    if rotate is None:
        weights = {"0+": c2 * c2, "0-": s2 * s2}
    else:
        c1, s1 = cosines[rotate], sines[rotate]
        weights = {
            "0+": (c1 * c2) ** 2,
            "0-": (c1 * s2) ** 2,
            "1+": (s1 * s2) ** 2,
            "1-": (s1 * c2) ** 2,
        }
    total = sum(weights.values())
    rungs, cumulative = [0], 0
    for weight in weights.values():
        cumulative += weight
        rungs.append((2 * births * cumulative + total) // (2 * total))
    counts = {name: rungs[k + 1] - rungs[k] for k, name in enumerate(weights)}
    return weights, rungs, counts


def run(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def gathers_of(simulation: NatureBeamSimulation, births: int) -> list[dict[str, object]]:
    """The gathers of the lamp's records of the ordinals 1 .. births."""
    assert simulation.layer is not None
    found = sorted(
        (
            g
            for g in simulation.layer.gathers
            if BASE + 1 <= int(g["record"]) < BASE + 1 + births  # type: ignore[call-overload]
        ),
        key=lambda g: int(g["record"]),  # type: ignore[call-overload]
    )
    assert len(found) == births
    return found


def cell(gather: dict[str, object]) -> str:
    """The chosen cell: the read's label then the end's channel."""
    return "".join(str(item[2]) for item in gather["chosen"])  # type: ignore[union-attr]


def counts_of(gathers: list[dict[str, object]], cells: list[str]) -> dict[str, int]:
    counted = Counter(cell(g) for g in gathers)
    assert set(counted) <= set(cells), counted
    return {name: counted.get(name, 0) for name in cells}


def test_the_pin_is_derived_from_the_worlds_and_the_tables():
    """(a)."""
    births = int(MALUS["wheel"][1])
    assert births == MALUS["births"]
    for setting, table in MALUS["tables"].items():
        n = int(WORLDS[NAMES[0]]["N"])
        assert [phase_cosines(2 * n)[int(setting)], phase_sines(2 * n)[int(setting)]] == table
    for name in NAMES:
        world = WORLDS[name]
        registered = MALUS[name]
        rotate, window = settings_of(world)
        assert (rotate, window) == (registered["rotate"], registered["window"]), name
        weights, rungs, counts = derived(rotate, window, int(world["N"]), births)
        assert weights == registered["weights"], name
        assert rungs == registered["rungs"], name
        assert counts == registered["counts"], name
        assert counts["0+"] == registered["pass"], name
        assert sum(counts.values()) == births


def test_the_replay_counts_as_registered():
    """(b)."""
    births = int(MALUS["births"])
    for name in NAMES:
        world = WORLDS[name]
        registered = MALUS[name]
        cells = list(registered["counts"])
        simulation, _ = run(world)
        assert simulation.layer is not None
        gathers = gathers_of(simulation, births)
        assert sorted(int(g["u"]) for g in gathers) == list(range(births)), name  # type: ignore[call-overload]
        for gather in gathers:
            assert [rung for _, rung in gather["cells"]] == registered["rungs"][1:], name  # type: ignore[union-attr]
            assert ["".join(str(f[2]) for f in factors) for factors, _ in gather["cells"]] == cells  # type: ignore[union-attr]
        counts = counts_of(gathers, cells)
        assert counts == registered["counts"] == registered["measured"]["counts"], name
        all_gathered = counts_of(list(simulation.layer.gathers), cells)
        assert all_gathered == registered["measured"]["all_gathered"], name
        report = simulation.layer.report()
        assert (report["gathered"], report["open"]) == (MALUS["run"]["gathered"], MALUS["run"]["open"])
        assert min(int(g["tick"]) for g in gathers) == MALUS["run"]["first_gather_tick"]  # type: ignore[call-overload]
        assert simulation.books(recount=True)["balanced"], name


def test_the_rotate_keeps_the_record_u():
    """(c)."""
    name = next(n for n in NAMES if MALUS[n]["rotate"] is not None)
    registered = MALUS[name]["measured"]
    _, lines = run(WORLDS[name])
    births = {int(line["record"]): int(line["u"]) for line in lines if line.get("event") == "birth"}
    splits = [line for line in lines if line.get("event") == "split"]
    assert len(splits) == registered["split"]["lines"]
    assert all(line["rebirth"] is registered["split"]["rebirth"] for line in splits)
    assert all(int(line["record"]) in births for line in splits)
    assert (
        all(int(line["u"]) == births[int(line["record"])] for line in splits)
        is registered["split"]["u_kept"]
    )
    assert set(Counter(int(line["record"]) for line in splits).values()) == {
        registered["split"]["per_record"]
    }
    first = splits[0]
    assert {k: first[k] for k in registered["split"]["first"]} == registered["split"]["first"]
    rotate = next(line for line in lines if line.get("event") == "rotate")
    expected = registered["rotate_line"]
    assert {k: rotate[k] for k in ("setting", "bit", "turn", "rows")} == {
        k: expected[k] for k in ("setting", "bit", "turn", "rows")
    }
    assert rotate["records"] == [[BASE + 1, *expected["units"]]]
    read = next(
        line for line in lines if line.get("event") == "read" and line.get("detector") == "first"
    )
    assert [[row[1], row[2], row[3], row[4]] for row in read["rows"]] == registered["read_rows"]  # type: ignore[index]
    assert all(row[0] == BASE + 1 for row in read["rows"])  # type: ignore[index]
