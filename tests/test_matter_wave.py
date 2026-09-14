"""Matter-wave probe: a moving particle dissolves on its tick and the world closes."""

import importlib.util
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "matter_wave_probe", ROOT / "examples/matter-wave/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_the_particle_flies_then_dissolves_and_its_husk_stops():
    headings = PROBE.cone_headings(32, PROBE.HEADING_SCALE)
    raw = PROBE.document(32, headings, ticks=12, dissolve_tick=4)
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["matter"][0]
    seen = []
    for _ in range(12):
        world.step()
        for position, node in world.nodes.items():
            for record in node.records:
                if record is not None and record.type_index == 0:
                    values = world.record_values(record)
                    seen.append((position[0] - PROBE.CENTER, values["matter"][0]))
    # Half a link per tick while its matter is whole; from the first quantum of the
    # train it stands still and pays the rest out where it is.
    positions = [x for x, _ in seen]
    assert positions[0] == PROBE.START_X - PROBE.CENTER
    assert max(positions) > positions[0]
    matter = [m for _, m in seen]
    assert matter[:4] == [matter[0]] * 4 and matter[4] < matter[0]
    assert len({x for x, m in seen if m < matter[0]}) == 1
    assert world.totals()["matter"][0] + world.escaped_totals()["matter"][0] == initial
    assert parse_initial_state(PROBE.document(64, headings, ticks=4, phased=False))
