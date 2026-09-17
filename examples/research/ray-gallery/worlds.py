"""Five small legal worlds, one per ray kind the engine can propagate.

The five documents are committed under configs/ (written by this module's builders);
record_ticks.py and render_rays.py in this directory read them back. The bonded-pair,
claim-and-gather and lottery-detector panels of the 2026-09-16 recording were deleted
on 2026-09-17 with the bond registry, claim-gather and the lottery capture (issue #164,
bucket B.5); their numbering is kept so that the recorded evidence stays readable.

Every world is schema 1, open boundary, shape 15 x 9 x 3 with all activity in
the plane z = 1, so that one XY panel shows the whole recorded state. Nothing
here is a new engine rule: each document is a configuration on a contract that
docs/SPATIAL_FIELDS.md already names, and the runner's run.json records the
identity it selected. Records (lamps, charges, mirrors, detectors, screens,
masses) are labelled as records in the panel; rays are the propagating stock.
"""

from __future__ import annotations

from event_universe.core.disturbance_state import OPERATIONS

SHAPE = [15, 9, 3]
ROW = 4  # the y of the main line
Z = 1
COSTS = {name: 1 for name in OPERATIONS}

QUANTA = {
    "name": "quanta",
    "components": 1,
    "units": "quantum",
    "signed": False,
    "conserved": True,
    "extensive": True,
}
MOMENTUM = {
    "name": "momentum",
    "components": 3,
    "units": "quantum times heading",
    "signed": True,
    "conserved": True,
    "extensive": True,
}


def _base(model_id: str, ticks: int, *, slots: int = 2, budget: int = 100000) -> dict:
    return {
        "schema_version": 1,
        "model_id": model_id,
        "boundary": "open",
        "shape": list(SHAPE),
        "slots_per_node": slots,
        "link_ticks": 1,
        "normal_budget": budget,
        "ticks": ticks,
        "operation_costs": dict(COSTS),
    }


def _hold(name: str, fields: list[str], defaults: dict) -> dict:
    return {"name": name, "fields": fields, "defaults": defaults, "transport": {"mode": "hold"}}


# 1. Outward octant field from a held charge (conservative-outward-v1, split_outward,
#    carried straight allocation phase). Axis weights [1, 1, 0] keep the halo in
#    the plane z = 1 so the panel shows every unit.
def outward_halo(ticks: int = 14) -> dict:
    raw = _base("rays-panel-outward-halo-v1", ticks)
    raw.update(
        fields=[
            {
                "name": "strength",
                "components": 1,
                "units": "charge unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "radiation",
                "components": 1,
                "units": "field unit",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
        ],
        disturbance_types=[_hold("charge", ["strength"], {"strength": 216})],
        spatial_fields=[
            {
                "field": "radiation",
                "baseline": 0,
                "transport": "outward",
                "axis_weights": [1, 1, 0],
                "octant_weights": [1, 1, 1, 1, 1, 1, 1, 1],
            }
        ],
        emissions=[
            {
                "type": "charge",
                "field": "radiation",
                "amount": {"field": "strength"},
                "denominator": 1,
                "source": True,
            }
        ],
        seeds=[{"position": [7, ROW, Z], "type": "charge"}],
        allocation_phase="straight",
    )
    return raw


# 2. Straight directional rays (isotropic-ray-field-v1): three funded lamps with a
#    fixed heading each, one link per tick along an integer line; rays cross
#    without responding.
def straight_rays(ticks: int = 22) -> dict:
    raw = _base("rays-panel-straight-rays-v1", ticks)
    per_ray, rays = 8, 6
    raw.update(
        fields=[QUANTA, MOMENTUM],
        disturbance_types=[
            _hold(name, ["quanta", "momentum"], {"quanta": per_ray * rays, "momentum": [0, 0, 0]})
            for name in ("lamp_x", "lamp_y", "lamp_diag")
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0], [0, 1, 0], [2, 1, 0]],
                "rays_per_tick": 1,
                "ray_slots": 16,
            }
        ],
        emissions=[
            {
                "type": "lamp_x",
                "field": "quanta",
                "amount": per_ray,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": [1, 0, 0],
            },
            {
                "type": "lamp_y",
                "field": "quanta",
                "amount": per_ray,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": [0, 1, 0],
            },
            {
                "type": "lamp_diag",
                "field": "quanta",
                "amount": per_ray,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": [2, 1, 0],
            },
        ],
        seeds=[
            {"position": [0, ROW, Z], "type": "lamp_x"},
            {"position": [7, 0, Z], "type": "lamp_y"},
            {"position": [0, 0, Z], "type": "lamp_diag"},
        ],
    )
    return raw


# 3. Kerengonen phased rays (kerengonen-ray-field-v1): two lamps in phase, 8 phase
#    steps advancing 2 per link, a screen of 9 absorbers ten links downstream.
#    Manhattan path difference |y - 2| - |y - 6| gives 0 at the center (bright),
#    2 links = half a turn at y = 3 and 5 (dark), 4 links = a full turn beyond.
def double_slit(ticks: int = 30) -> dict:
    raw = _base("rays-panel-double-slit-v1", ticks)
    headings = [[8, j, 0] for j in range(-6, 7)]
    per_ray = 4
    emit_ticks = 18
    stock = per_ray * len(headings) * emit_ticks
    raw.update(
        fields=[QUANTA, MOMENTUM],
        disturbance_types=[
            _hold("lamp_a", ["quanta", "momentum"], {"quanta": stock, "momentum": [0, 0, 0]}),
            _hold("lamp_b", ["quanta", "momentum"], {"quanta": stock, "momentum": [0, 0, 0]}),
            _hold("screen", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": len(headings),
                "ray_slots": 512,
                "kerengonen": {"phase_steps": 8, "phase_advance": 2},
            }
        ],
        emissions=[
            {
                "type": name,
                "field": "quanta",
                "amount": per_ray * len(headings),
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            }
            for name in ("lamp_a", "lamp_b")
        ],
        spatial_couplings=[
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        seeds=[
            {"position": [2, ROW - 2, Z], "type": "lamp_a"},
            {"position": [2, ROW + 2, Z], "type": "lamp_b"},
        ]
        + [{"position": [12, y, Z], "type": "screen"} for y in range(SHAPE[1])],
    )
    return raw


# 4 and 5. The bonded-pair and claim-and-gather panels were deleted on 2026-09-17
#    with the bond registry and claim-gather (Highlights 3.18 deleted, 5.1 and 5.4).


# 6. Mirror reflection (kerengonen-ray-field-v1, kerengonen_mirror): a lamp between
#    two mirror records fires 8 quanta each way once; each mirror absorbs the ray
#    that reaches it and next cycle re-emits it back along the mirrored heading at
#    the carried phase. This is the cavity of exploration-ray/bound_pair_proxy.py
#    widened to the panel.
def mirror_cavity(ticks: int = 40) -> dict:
    raw = _base("rays-panel-mirror-cavity-v1", ticks, slots=4)
    parcel = 8
    raw.update(
        fields=[QUANTA, MOMENTUM],
        disturbance_types=[
            _hold("lamp", ["quanta", "momentum"], {"quanta": 2 * parcel, "momentum": [0, 0, 0]}),
            _hold("mirror", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0], [-1, 0, 0]],
                "rays_per_tick": 2,
                "ray_slots": 16,
                "kerengonen": {"phase_steps": 64, "phase_advance": 4},
            }
        ],
        emissions=[
            {
                "type": "lamp",
                "field": "quanta",
                "amount": 2 * parcel,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            },
            {
                "type": "mirror",
                "field": "quanta",
                "amount": {"field": "quanta"},
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": "carried",
                "kerengonen_mirror": "x",
            },
        ],
        spatial_couplings=[
            {
                "name": "mirror_absorbs",
                "type": "mirror",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        seeds=[
            {"position": [7, ROW, Z], "type": "lamp"},
            {"position": [3, ROW, Z], "type": "mirror"},
            {"position": [11, ROW, Z], "type": "mirror"},
        ],
    )
    return raw


# 7. Ray delay under a computation field: a lamp fires one Kerengonen ray per tick
#    along +x through a Node loaded by a mass body's outward computation field;
#    with ray_delay the Node holds its resident rays for k = ceil(load / budget) - 1
#    cycles. Directional (along) departure delay keeps the held lamp and screen on
#    their fixed cycle, as tests/test_ray_delay.py does.
def ray_delay(ticks: int = 44, *, emission: int = 28000, budget: int = 1000) -> dict:
    raw = _base("rays-panel-ray-delay-v1", ticks, budget=budget)
    per_ray, rays = 16, 8
    raw.update(
        computation_field="computation",
        delay_direction="along",
        ray_delay=True,
        ray_phase_per_tick=False,
        fields=[
            QUANTA,
            MOMENTUM,
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
        disturbance_types=[
            _hold("lamp", ["quanta", "momentum"], {"quanta": per_ray * rays, "momentum": [0, 0, 0]}),
            _hold("screen", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
            _hold("mass body", ["mass"], {"mass": 1}),
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 64,
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            },
            {"field": "computation", "baseline": 0, "transport": "outward", "axis_weights": [1, 1, 0]},
        ],
        emissions=[
            {
                "type": "lamp",
                "field": "quanta",
                "amount": per_ray,
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
        spatial_couplings=[
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            }
        ],
        seeds=[
            {"position": [2, ROW, Z], "type": "lamp"},
            {"position": [12, ROW, Z], "type": "screen"},
            {"position": [7, ROW + 2, Z], "type": "mass body"},
        ],
    )
    return raw


# 8. The lottery-detector panel was deleted on 2026-09-17 with the lottery capture
#    (Highlights 3.19: the only draw is at a Node whose Detector bit is set).


PANELS: list[dict] = [
    {
        "key": "1-outward-halo",
        "title": "1. Outward octant field",
        "build": outward_halo,
        "contract": "conservative-outward-v1 / split_outward / carried-straight-phase-v1",
        "field": "radiation",
        "kind": "octants",
    },
    {
        "key": "2-straight-rays",
        "title": "2. Straight directional rays",
        "build": straight_rays,
        "contract": "isotropic-ray-field-v1 (funded, directed heading)",
        "field": "quanta",
        "kind": "rays",
    },
    {
        "key": "3-double-slit",
        "title": "3. Kerengonen phased rays",
        "build": double_slit,
        "contract": "kerengonen-ray-field-v1 (share capture)",
        "field": "quanta",
        "kind": "rays",
    },
    {
        "key": "6-mirror-cavity",
        "title": "6. Mirror reflection",
        "build": mirror_cavity,
        "contract": "kerengonen-ray-field-v1 (kerengonen_mirror x, carried phase)",
        "field": "quanta",
        "kind": "rays",
    },
    {
        "key": "7-ray-delay",
        "title": "7. Ray delay under computation field",
        "build": ray_delay,
        "contract": "kerengonen-ray-field-v1 + ray_delay + computation-field-load (along)",
        "field": "quanta",
        "kind": "rays",
    },
]
