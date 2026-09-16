"""Shared machinery for the exploration experiments E1-E4 (research evidence only).

Run every script from the repository root with PYTHONPATH=src; each takes --output DIR
(default artifacts/research/bell-postulate-22) and writes or reads DIR/<experiment>/.

Builds bonded Bell worlds like examples/bell-chsh/run_experiments.py:document(...,
capture="bond") with extra knobs (asymmetric detector distances, an absent end, a
replay detector, a second pair, a wider lattice) and wraps the world's bond registry
with a logging proxy so every registry question is recorded with the world tick.
Nothing here modifies src/; the wrapper replaces the bound method on one registry
instance owned by one Simulation object created by the script.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from event_universe import Simulation  # noqa: E402
from event_universe.core.spatial_state import (  # noqa: E402
    PHASE_COSINE_SCALE,
    TICKET_MODULUS,
    next_ticket,
    origin_bond,
    phase_cosines,
    ray_salt,
    ticket_draw,
)
from event_universe.fields.bonds import BondRegistry  # noqa: E402
from event_universe.initialization import parse_initial_state  # noqa: E402
from event_universe.runner import source_fingerprint  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "bell_probe", ROOT / "examples" / "bell-chsh" / "run_experiments.py"
)
PROBE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(PROBE)

DEFAULT_OUTPUT = ROOT / "artifacts" / "research" / "bell-postulate-22"
PHASE_STEPS = PROBE.PHASE_STEPS
HALF_TURN = PROBE.HALF_TURN
SETTINGS = PROBE.SETTINGS
PAIRS = PROBE.PAIRS
EXPECTED_S = float(PROBE.EXPECTED_BOND_S)  # 724/256 = 2.828125
COSINES = phase_cosines(PHASE_STEPS)


def expected_e(alice: int, bob: int) -> float:
    """The registry's exact expectation: -c/256 for the table cosine of the difference."""
    return -COSINES[(alice - bob) % PHASE_STEPS] / PHASE_COSINE_SCALE


def output_argument(parser: argparse.ArgumentParser) -> None:
    """The directory that holds every experiment's result files (one subfolder each)."""
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="result directory")


def stamp() -> dict:
    return {
        "sampling_profile": "historical-autonomous-v1",
        "source_sha256": source_fingerprint(),
        "python": sys.version,
        "repository_root": str(ROOT),
    }


# --- world builder -----------------------------------------------------------------


def bonded_world(
    hidden: int,
    alice: int,
    bob: int,
    seed: int,
    *,
    dist_alice: int = PROBE.DISTANCE,
    dist_bob: int = PROBE.DISTANCE,
    width: int = PROBE.WIDTH,
    depth: int = 3,
    ticks: int | None = None,
    stream: list[int] | None = None,
    alice_present: bool = True,
    bob_present: bool = True,
    replay_setting: int | None = None,
    second_pair: dict | None = None,
) -> dict:
    """A bonded Bell world (capture "bond") with extra knobs.

    replay_setting: a second bonded detector ("again_alice") one link past Alice's
    plus detector at that setting; the minus detector moves one link further.
    second_pair: {"source": (x, y, z), "hidden": h, "alice": s, "bob": s} adds a
    second bonded pair emitted along -y / +y from that Node with its own four
    detectors at the same distances (needs depth >= 2*dist+3).
    """
    center = width // 2
    mid = depth // 2
    if ticks is None:
        ticks = max(dist_alice, dist_bob) + 6 + (2 if replay_setting is not None else 0)
    body = {
        "fields": ["quanta", "momentum"],
        "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    detector = {"fields": ["quanta", "momentum", "setting"], "transport": {"mode": "hold"}}

    def det(name: str, setting: int) -> dict:
        return {
            "name": name,
            **detector,
            "defaults": {"quanta": 0, "momentum": [0, 0, 0], "setting": setting % PHASE_STEPS},
        }

    def source(name: str, train: int) -> dict:
        return {
            "name": name,
            "fields": ["quanta", "momentum", "train"],
            "defaults": {"quanta": 1, "momentum": [0, 0, 0], "train": train},
            "transport": {"mode": "hold"},
        }

    def emission(name: str, phase: int, heading: list[int]) -> dict:
        return {
            "type": name,
            "field": "quanta",
            "amount": 1,
            "denominator": 1,
            "source": False,
            "recoil_field": "momentum",
            "kerengonen_phase": phase % PHASE_STEPS,
            "train_field": "train",
            "heading": heading,
            "bond_field": "origin",
        }

    def absorb(name: str, bonded_detector: bool) -> dict:
        return {
            "name": f"{name}_absorbs",
            "field": "quanta",
            "mode": "absorb",
            "momentum_field": "momentum",
            "claim": True,
            **({"bond_setting": "setting"} if bonded_detector else {}),
            "type": name,
        }

    plus_alice, plus_bob = center - dist_alice, center + dist_bob
    types = [
        source("source_alice", 1),
        source("source_bob", 2),
        det("plus_alice", alice),
        {"name": "minus_alice", **body},
        det("plus_bob", bob),
        {"name": "minus_bob", **body},
    ]
    emissions = [
        emission("source_alice", hidden, [-1, 0, 0]),
        emission("source_bob", hidden + HALF_TURN, [1, 0, 0]),
    ]
    couplings = [
        absorb("plus_alice", True),
        absorb("minus_alice", False),
        absorb("plus_bob", True),
        absorb("minus_bob", False),
    ]
    seeds = [
        {"position": [center, mid, 1], "type": "source_alice"},
        {"position": [center, mid, 1], "type": "source_bob"},
    ]
    minus_alice_x = plus_alice - 1
    if replay_setting is not None:
        types.append(det("again_alice", replay_setting))
        couplings.append(absorb("again_alice", True))
        seeds.append({"position": [plus_alice - 1, mid, 1], "type": "again_alice"})
        minus_alice_x = plus_alice - 2
    if alice_present:
        seeds.append({"position": [plus_alice, mid, 1], "type": "plus_alice"})
        seeds.append({"position": [minus_alice_x, mid, 1], "type": "minus_alice"})
    if bob_present:
        seeds.append({"position": [plus_bob, mid, 1], "type": "plus_bob"})
        seeds.append({"position": [plus_bob + 1, mid, 1], "type": "minus_bob"})
    headings = [[-1, 0, 0], [1, 0, 0], [0, -1, 0]]
    if second_pair is not None:
        sx, sy, sz = second_pair["source"]
        headings = [[-1, 0, 0], [1, 0, 0], [0, -1, 0], [0, 1, 0]]
        types += [
            source("source_alice2", 3),
            source("source_bob2", 4),
            det("plus_alice2", second_pair["alice"]),
            {"name": "minus_alice2", **body},
            det("plus_bob2", second_pair["bob"]),
            {"name": "minus_bob2", **body},
        ]
        emissions += [
            emission("source_alice2", second_pair["hidden"], [0, -1, 0]),
            emission("source_bob2", second_pair["hidden"] + HALF_TURN, [0, 1, 0]),
        ]
        couplings += [
            absorb("plus_alice2", True),
            absorb("minus_alice2", False),
            absorb("plus_bob2", True),
            absorb("minus_bob2", False),
        ]
        d = PROBE.DISTANCE
        seeds += [
            {"position": [sx, sy, sz], "type": "source_alice2"},
            {"position": [sx, sy, sz], "type": "source_bob2"},
            {"position": [sx, sy - d, sz], "type": "plus_alice2"},
            {"position": [sx, sy - d - 1, sz], "type": "minus_alice2"},
            {"position": [sx, sy + d, sz], "type": "plus_bob2"},
            {"position": [sx, sy + d + 1, sz], "type": "minus_bob2"},
        ]
    return {
        "schema_version": 1,
        "model_id": "bell-chsh-ray-probe-v1-exploration",
        "sampling_profile": "historical-autonomous-v1",
        "shape": [width, depth, 3],
        "boundary": "open",
        "slots_per_node": 4 if second_pair is not None else 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": PROBE.COSTS,
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
            {
                "name": "train",
                "components": 1,
                "units": "label",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
            {
                "name": "setting",
                "components": 1,
                "units": "phase step",
                "signed": False,
                "conserved": False,
                "extensive": False,
            },
        ],
        "disturbance_types": types,
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": headings,
                "rays_per_tick": 1,
                "ray_slots": 8,
                "kerengonen": {"phase_steps": PHASE_STEPS, "phase_advance": 0, "capture": "share"},
                "claim": {"ticks": 4 * ticks, "slots": 8},
                "bond": {"seed": seed, **({"stream": list(stream)} if stream is not None else {})},
            }
        ],
        "emissions": emissions,
        "spatial_couplings": couplings,
        "seeds": seeds,
    }


# --- running ------------------------------------------------------------------------


class Logged:
    """A world whose registry questions are logged with the world tick."""

    def __init__(self, raw: dict) -> None:
        self.raw = raw
        self.world = Simulation(parse_initial_state(raw))
        self.registry: BondRegistry = self.world._execution._spatial_planner.bonds
        self.log: list[dict] = []
        original = self.registry.draw

        def draw(bond: int, setting: int, salt: int) -> int:
            before = self.registry.numbers
            outcome = original(bond, setting, salt)
            self.log.append(
                {
                    "tick": self.world.tick,
                    "bond": bond,
                    "setting": setting,
                    "salt": salt,
                    "outcome": outcome,
                    "drew_number": self.registry.numbers - before,
                    "open_after": len(self.registry.open),
                }
            )
            return outcome

        self.registry.draw = draw
        self.initial = self.world.totals()["quanta"][0]

    def run(self, ticks: int | None = None) -> None:
        for _ in range(self.raw["ticks"] if ticks is None else ticks):
            self.world.step()

    def outcomes(self) -> dict:
        """Where each train landed: +1 at a plus-type detector, -1 at a minus-type one."""
        world = self.world
        names = [kind["name"] for kind in self.raw["disturbance_types"]]
        detectors = {
            node.position: names[record.type_index]
            for node in world.inventory_view().nodes
            for record in node.records
            if record is not None
            and names[record.type_index].split("_")[0] in ("plus", "minus", "again")
        }
        landed: dict[int, int] = {}
        for node in world.inventory_view().nodes:
            for claim in node.claims[0] if node.claims else ():
                if claim.parent < 0:
                    kind = str(detectors.get(claim.origin))
                    landed[claim.train] = 1 if kind.startswith("plus") else -1
        escaped = world.escaped_totals()["quanta"][0]
        return {
            "alice": landed.get(1),
            "bob": landed.get(2),
            "alice2": landed.get(3),
            "bob2": landed.get(4),
            "escaped": escaped,
            "closed": world.totals()["quanta"][0] + escaped == self.initial,
            "numbers": self.registry.numbers,
            "questions": self.registry.questions,
            "released": self.registry.released,
            "open": len(self.registry.open),
            "log": self.log,
        }


def run_world(raw: dict) -> dict:
    logged = Logged(raw)
    logged.run()
    return logged.outcomes()


def salt_positions(logged: Logged) -> dict[int, tuple[int, int, int]]:
    """Map each resident ray's salt to the Node holding it (call between steps)."""
    table = {}
    for node in logged.world.inventory_view().nodes:
        for ray in node.rays[0] if node.rays else ():
            table[ray_salt(ray)] = node.position
    return table


# --- statistics --------------------------------------------------------------------


def se_rate(p: float, n: int) -> float:
    return math.sqrt(max(p * (1 - p), 0) / n) if n else 0.0


def se_corr(e: float, n: int) -> float:
    return math.sqrt(max(1 - e * e, 0) / n) if n else 0.0


def correlation_stats(pairs: list[tuple[int, int]]) -> dict:
    n = len(pairs)
    if n == 0:
        return {"pairs": 0, "E": None, "sigma_E": None}
    e = sum(a * b for a, b in pairs) / n
    pa = sum(a > 0 for a, _ in pairs) / n
    pb = sum(b > 0 for _, b in pairs) / n
    return {
        "pairs": n,
        "E": round(e, 5),
        "sigma_E": round(se_corr(e, n), 5),
        "alice_plus_rate": round(pa, 5),
        "sigma_alice_rate": round(se_rate(pa, n), 5),
        "bob_plus_rate": round(pb, 5),
        "sigma_bob_rate": round(se_rate(pb, n), 5),
    }


def chsh_from(correlations: dict[str, dict]) -> dict:
    e = {key: value["E"] for key, value in correlations.items()}
    if any(value is None for value in e.values()):
        return {
            "S": None,
            "sigma_S": None,
            "expected_S": EXPECTED_S,
            "z": None,
            "within_3_sigma": False,
            "note": "a setting pair never occurred: degenerate setting chooser",
        }
    s = abs(e["a,b"] - e["a,b2"] + e["a2,b"] + e["a2,b2"])
    sigma = math.sqrt(sum(value["sigma_E"] ** 2 for value in correlations.values()))
    return {
        "S": round(s, 5),
        "sigma_S": round(sigma, 5),
        "expected_S": EXPECTED_S,
        "z": round((s - EXPECTED_S) / sigma, 3) if sigma else None,
        "within_3_sigma": abs(s - EXPECTED_S) <= 3 * sigma,
    }


def chi2_sf(x: float, df: int) -> float:
    """Survival function of chi-square with df degrees of freedom (regularized gamma)."""
    if x <= 0:
        return 1.0
    a, z = df / 2.0, x / 2.0
    # Series for the lower regularized gamma P(a, z); Q = 1 - P.
    if z < a + 1:
        term = 1.0 / a
        total = term
        for n in range(1, 500):
            term *= z / (a + n)
            total += term
            if term < total * 1e-15:
                break
        p = total * math.exp(-z + a * math.log(z) - math.lgamma(a))
        return max(0.0, min(1.0, 1.0 - p))
    # Continued fraction for Q(a, z) (Lentz).
    tiny = 1e-300
    b = z + 1 - a
    c = 1 / tiny
    d = 1 / b
    h = d
    for i in range(1, 500):
        an = -i * (i - a)
        b += 2
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < 1e-15:
            break
    return max(0.0, min(1.0, math.exp(-z + a * math.log(z) - math.lgamma(a)) * h))


def chi2_independence(rows: list[tuple]) -> dict:
    """Chi-square test of independence between two categorical columns of pairs."""
    xs = sorted({r[0] for r in rows})
    ys = sorted({r[1] for r in rows})
    n = len(rows)
    counts = {(x, y): 0 for x in xs for y in ys}
    for x, y in rows:
        counts[(x, y)] += 1
    rx = {x: sum(counts[(x, y)] for y in ys) for x in xs}
    ry = {y: sum(counts[(x, y)] for x in xs) for y in ys}
    stat = 0.0
    for x in xs:
        for y in ys:
            expected = rx[x] * ry[y] / n
            if expected > 0:
                stat += (counts[(x, y)] - expected) ** 2 / expected
    df = (len(xs) - 1) * (len(ys) - 1)
    p = chi2_sf(stat, df) if df > 0 else 1.0
    return {
        "n": n,
        "chi2": round(stat, 4),
        "df": df,
        "p": p,
        "table": {f"{x}|{y}": counts[(x, y)] for x in xs for y in ys},
    }


def mutual_information_bits(rows: list[tuple]) -> float:
    n = len(rows)
    from collections import Counter

    joint = Counter(rows)
    px = Counter(r[0] for r in rows)
    py = Counter(r[1] for r in rows)
    return sum(c / n * math.log2((c / n) / ((px[x] / n) * (py[y] / n))) for (x, y), c in joint.items())


def number_halves(number: int) -> tuple[int, int]:
    """The coin (upper half: +1 if 2n < M) and the agreement fraction bucket of the lower half."""
    coin = 1 if 2 * number < TICKET_MODULUS else -1
    rest = (2 * number) % TICKET_MODULUS
    return coin, rest


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")


__all__ = [
    "PROBE",
    "DEFAULT_OUTPUT",
    "ROOT",
    "output_argument",
    "PHASE_STEPS",
    "HALF_TURN",
    "SETTINGS",
    "PAIRS",
    "EXPECTED_S",
    "TICKET_MODULUS",
    "BondRegistry",
    "next_ticket",
    "ticket_draw",
    "origin_bond",
    "ray_salt",
    "bonded_world",
    "Logged",
    "run_world",
    "salt_positions",
    "se_rate",
    "se_corr",
    "correlation_stats",
    "chsh_from",
    "chi2_independence",
    "chi2_sf",
    "mutual_information_bits",
    "number_halves",
    "expected_e",
    "stamp",
    "dump",
    "dataclasses",
    "Simulation",
    "parse_initial_state",
]
