"""Ray delay: rays wait at a loaded Node; phase per interval makes the wait visible to phase.

A lamp fires one Kerengonen ray per tick along +x through a Node loaded by a
mass's outward computation field, to a screen that absorbs it. Without
`ray_delay` the field clock is fixed and the ray ignores the load; with it the
ray waits at the loaded Node the intervals the load alone prices; with
`ray_phase_per_tick` the waited intervals also advance its phase.
"""

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import OPERATIONS, unpack
from event_universe.initialization import parse_initial_state

LAMP, MASS, SCREEN = 2, 6, 10
ROW = (2, 2)
STEPS = 8


def document(*, ray_delay=False, phase_per_tick=False, emission=200000, budget=2000, ticks=40):
    doc = {
        "schema_version": 1,
        "model_id": "ray-delay-contract-v1",
        "boundary": "open",
        "shape": [15, 5, 5],
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "computation_field": "computation",
        # Departure-only delay keeps the held lamp and screen on their fixed cycle:
        # funded emission and absorption reject a delayed carrier plan.
        "delay_direction": "along",
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {"name": "mass", "components": 1, "units": "unit", "signed": False, "conserved": True},
            {
                "name": "computation",
                "components": 1,
                "units": "load unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 16, "momentum": [0, 0, 0]},  # one ray, so its phase is its own
                "transport": {"mode": "hold"},
            },
            {
                "name": "screen",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "mass body",
                "fields": ["mass"],
                "defaults": {"mass": 1},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[24, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 64,
                "kerengonen": {"phase_steps": STEPS, "phase_advance": 1},
            },
            {"field": "computation", "baseline": 0, "transport": "outward"},
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "quanta",
                "amount": 16,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            },
            {
                "type": "mass body",
                "field": "computation",
                "amount": emission,
                "denominator": 1,
                "source": True,
            },
        ],
        "spatial_couplings": [
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        "seeds": [
            {"position": [LAMP, *ROW], "type": "lamp"},
            {"position": [SCREEN, *ROW], "type": "screen"},
            {"position": [MASS, 4, 2], "type": "mass body"},
        ],
        "ray_delay": ray_delay,
        "ray_phase_per_tick": phase_per_tick,
    }
    return doc


def first_click(doc):
    """Tick of the first absorbed quantum at the screen and the phase it recorded."""
    world = Simulation(parse_initial_state(doc))
    for tick in range(1, doc["ticks"] + 1):
        world.step()
        for record in world.nodes[(SCREEN, *ROW)].records:
            if record is not None and record.type_index == 1:
                quanta = world.record_values(record)["quanta"][0]
                if quanta:
                    return tick, unpack(record.absorbed_phases[0])[0]
    return None, None


def test_rays_ignore_the_load_on_the_fixed_field_clock():
    free, _ = first_click(document())
    loaded, _ = first_click(document(emission=0))
    assert free == loaded


def test_ray_delay_holds_rays_at_the_loaded_node():
    plain, _ = first_click(document())
    delayed, _ = first_click(document(ray_delay=True))
    control, _ = first_click(document(ray_delay=True, emission=0))
    assert control == plain
    assert delayed is not None and delayed > plain


def test_phase_per_interval_shifts_the_absorbed_phase_by_the_wait():
    free_tick, free_phase = first_click(document())
    plain_tick, plain_phase = first_click(document(ray_delay=True))
    shifted_tick, shifted_phase = first_click(document(ray_delay=True, phase_per_tick=True))
    waits = plain_tick - free_tick
    assert waits > 0 and shifted_tick == plain_tick
    # Per link only: the delayed ray arrives with the undelayed phase.
    assert plain_phase == free_phase
    # Per interval as well: every waiting interval adds one advance.
    assert shifted_phase == (free_phase + waits) % STEPS


@pytest.mark.parametrize(
    ("extra", "message"),
    [
        ({"ray_phase_per_tick": True, "ray_delay": False}, "requires ray_delay"),
        ({"ray_delay": True, "computation_field": None}, "requires computation_field"),
        ({"ray_delay": "yes"}, "must be a boolean"),
    ],
)
def test_rejected_ray_delay_settings(extra, message):
    doc = document()
    for key, value in extra.items():
        if value is None:
            doc.pop(key)
        else:
            doc[key] = value
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)
