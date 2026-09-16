"""Eight small legal worlds, one per ray kind the engine can propagate.

The eight documents are committed under configs/ (written by this module's builders);
record_ticks.py and render_rays.py in this directory read them back.

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


# 4. Bonded rays (bonded-ray-field-v1): one Node emits a pair per tick, Alice's
#    quantum along -x and Bob's along +x, bonded to their birth (Node and tick).
#    Plus detectors three links out hold settings; the bond registry answers both
#    ends. A ray not taken walks one link on to a minus detector.
def bonded_pair(
    ticks: int = 12,
    *,
    hidden_phase: int = 0,
    alice: int = 0,
    bob: int = 8,
    seed: int = 3,
    pairs: int = 4,
) -> dict:
    raw = _base("rays-panel-bonded-pair-v1", ticks)
    steps = 64
    detector = ["quanta", "momentum", "setting"]
    raw.update(
        fields=[
            QUANTA,
            MOMENTUM,
            {
                "name": "setting",
                "components": 1,
                "units": "phase step",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        disturbance_types=[
            _hold("source_alice", ["quanta", "momentum"], {"quanta": pairs, "momentum": [0, 0, 0]}),
            _hold("source_bob", ["quanta", "momentum"], {"quanta": pairs, "momentum": [0, 0, 0]}),
            _hold(
                "plus_alice", detector, {"quanta": 0, "momentum": [0, 0, 0], "setting": alice % steps}
            ),
            _hold("minus_alice", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
            _hold("plus_bob", detector, {"quanta": 0, "momentum": [0, 0, 0], "setting": bob % steps}),
            _hold("minus_bob", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[-1, 0, 0], [1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "kerengonen": {"phase_steps": steps, "phase_advance": 0, "capture": "share"},
                "bond": {"seed": seed},
            }
        ],
        emissions=[
            {
                "type": "source_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": hidden_phase % steps,
                "heading": [-1, 0, 0],
                "bond_field": "origin",
            },
            {
                "type": "source_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": (hidden_phase + steps // 2) % steps,
                "heading": [1, 0, 0],
                "bond_field": "origin",
            },
        ],
        spatial_couplings=[
            {
                "name": "plus_alice_absorbs",
                "type": "plus_alice",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "bond_setting": "setting",
            },
            {
                "name": "minus_alice_absorbs",
                "type": "minus_alice",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            },
            {
                "name": "plus_bob_absorbs",
                "type": "plus_bob",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "bond_setting": "setting",
            },
            {
                "name": "minus_bob_absorbs",
                "type": "minus_bob",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
            },
        ],
        seeds=[
            {"position": [7, ROW, Z], "type": "source_alice"},
            {"position": [7, ROW, Z], "type": "source_bob"},
            {"position": [4, ROW, Z], "type": "plus_alice"},
            {"position": [3, ROW, Z], "type": "minus_alice"},
            {"position": [10, ROW, Z], "type": "plus_bob"},
            {"position": [11, ROW, Z], "type": "minus_bob"},
        ],
    )
    return raw


# 5. Claim and gather (claim-gather-ray-field-v1 on isotropic-ray-field-v1): a
#    particle dissolves into eight planar rays at a quarter link per tick; a
#    screen two links along +x takes the first ray and opens a claim that floods
#    the world at link speed; every free ray of the train turns homeward.
def claim_gather(ticks: int = 40) -> dict:
    raw = _base("rays-panel-claim-gather-v1", ticks, slots=1)
    headings = [
        [1, 0, 0],
        [-1, 0, 0],
        [0, 1, 0],
        [0, -1, 0],
        [1, 1, 0],
        [-1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
    ]
    raw.update(
        fields=[
            {
                "name": "matter",
                "components": 1,
                "units": "matter quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "matter quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        disturbance_types=[
            _hold(
                "particle",
                ["matter", "momentum", "train"],
                {"matter": 64, "momentum": [0, 0, 0], "train": 7},
            ),
            _hold("screen", ["matter", "momentum"], {"matter": 0, "momentum": [0, 0, 0]}),
        ],
        spatial_fields=[
            {
                "field": "matter",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": len(headings),
                "ray_slots": 256,
                "pace": [1, 4],
                "claim": {"ticks": 1000, "slots": 4},
            }
        ],
        emissions=[
            {
                "type": "particle",
                "field": "matter",
                "source": False,
                "recoil_field": "momentum",
                "dissolve": {"after_ticks": 2, "over_ticks": 8},
                "train_field": "train",
            }
        ],
        spatial_couplings=[
            {
                "name": "screen_absorbs",
                "type": "screen",
                "field": "matter",
                "mode": "absorb",
                "momentum_field": "momentum",
                "claim": True,
            }
        ],
        seeds=[
            {"position": [7, ROW, Z], "type": "particle"},
            {"position": [9, ROW, Z], "type": "screen"},
        ],
    )
    return raw


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


# 8. Lottery capture (kerengonen-ray-field-v1, capture lottery, capture_salt): the
#    bell-chsh lottery mode. Two sources at one Node emit one quantum per tick,
#    Alice's along -x at the hidden phase, Bob's along +x half a turn on. A
#    reference lamp one link above each plus detector lands a quantum per tick at
#    the detector's setting phase; the lottery takes the arriving ray with the
#    coherence of the pair, and a ray not taken walks on to the minus detector.
#    Settings a quarter turn from the ray phases give coherence one half.
def lottery_detector(
    ticks: int = 16,
    *,
    hidden_phase: int = 0,
    alice: int = 16,
    bob: int = 48,
    seed: int = 1,
    quanta: int = 8,
) -> dict:
    raw = _base("rays-panel-lottery-detector-v1", ticks)
    steps = 64
    raw.update(
        fields=[QUANTA, MOMENTUM],
        disturbance_types=[
            _hold("source_alice", ["quanta", "momentum"], {"quanta": quanta, "momentum": [0, 0, 0]}),
            _hold("source_bob", ["quanta", "momentum"], {"quanta": quanta, "momentum": [0, 0, 0]}),
            _hold("reference_alice", ["quanta", "momentum"], {"quanta": ticks, "momentum": [0, 0, 0]}),
            _hold("reference_bob", ["quanta", "momentum"], {"quanta": ticks, "momentum": [0, 0, 0]}),
            _hold("plus_alice", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
            _hold("minus_alice", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
            _hold("plus_bob", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
            _hold("minus_bob", ["quanta", "momentum"], {"quanta": 0, "momentum": [0, 0, 0]}),
        ],
        spatial_fields=[
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[-1, 0, 0], [1, 0, 0], [0, -1, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "kerengonen": {
                    "phase_steps": steps,
                    "phase_advance": 0,
                    "capture": "lottery",
                    "capture_seed": seed,
                },
            }
        ],
        emissions=[
            {
                "type": "source_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": hidden_phase % steps,
                "heading": [-1, 0, 0],
            },
            {
                "type": "source_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": (hidden_phase + steps // 2) % steps,
                "heading": [1, 0, 0],
            },
            {
                "type": "reference_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": alice % steps,
                "heading": [0, -1, 0],
            },
            {
                "type": "reference_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": bob % steps,
                "heading": [0, -1, 0],
            },
        ],
        spatial_couplings=[
            {
                "name": f"{name}_absorbs",
                "type": name,
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "capture_salt": salt,
            }
            for name, salt in (("plus_alice", 0), ("minus_alice", 1), ("plus_bob", 2), ("minus_bob", 3))
        ],
        seeds=[
            {"position": [7, ROW, Z], "type": "source_alice"},
            {"position": [7, ROW, Z], "type": "source_bob"},
            {"position": [4, ROW, Z], "type": "plus_alice"},
            {"position": [3, ROW, Z], "type": "minus_alice"},
            {"position": [4, ROW + 1, Z], "type": "reference_alice"},
            {"position": [10, ROW, Z], "type": "plus_bob"},
            {"position": [11, ROW, Z], "type": "minus_bob"},
            {"position": [10, ROW + 1, Z], "type": "reference_bob"},
        ],
    )
    return raw


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
        "key": "4-bonded-pair",
        "title": "4. Bonded rays",
        "build": bonded_pair,
        "contract": "bonded-ray-field-v1 (bond_field origin, bond_setting)",
        "field": "quanta",
        "kind": "rays",
    },
    {
        "key": "5-claim-gather",
        "title": "5. Claim and gather",
        "build": claim_gather,
        "contract": "claim-gather-ray-field-v1 (pace 1/4, dissolve)",
        "field": "matter",
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
    {
        "key": "8-lottery-detector",
        "title": "8. Lottery capture at a detector",
        "build": lottery_detector,
        "contract": "kerengonen-ray-field-v1 (capture lottery, capture_salt)",
        "field": "quanta",
        "kind": "rays",
    },
]
