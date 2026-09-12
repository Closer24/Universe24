"""Keep the orbit audit's no-force controls and known wave limitation explicit."""

import importlib.util
import sys
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    path = ROOT / "examples/directional-star-audit" / (name + ".py")
    spec = importlib.util.spec_from_file_location("star_audit_" + name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def test_star_profiles_share_rate_but_differ_in_mass_and_charge():
    cases = module("configuration").configurations()
    raw = cases["active"]
    assert raw["shape"] == [128] * 3 and raw["ticks"] == 256
    assert sum(s["values"]["mass"] for s in raw["seeds"][:27]) == 1260000
    assert [p["defaults"]["mass"] for p in raw["disturbance_types"][1:]] == [4, 4000, 4]
    for candidate in cases.values():
        assert not any(
            candidate.get(k)
            for k in ("couplings", "interactions", "spatial_couplings", "spatial_interactions")
        )
        assert all(not p.get("updates") for p in candidate["disturbance_types"])
        assert candidate["boundary"] == "open"
        parse_initial_state(candidate)


def test_asynchronous_wave_does_not_inherit_synchronous_norm_claim():
    wave = module("wave_audit")
    norms = {}
    for name, raw, names in wave.configurations():
        world = Simulation(parse_initial_state(raw))
        initial = wave.norm(world.snapshot(), names)
        for _ in range(7):
            world.step()
        norms[name] = (initial, wave.norm(world.snapshot(), names))
    assert norms["control"] == (549755813888, 549755813888)
    assert norms["zero_wait"] == norms["control"]
    # Known candidate-composition limitation, not an accepted energy law.
    assert norms["directional_wait"] == (549755813888, 541165879296)
