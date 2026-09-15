"""Bell's test on the ray: a CHSH measurement of two phased rays from one source.

Two records at one Node each emit one quantum, one toward Alice along -x and
one toward Bob along +x, with a shared hidden phase: Alice's ray carries
lambda, Bob's lambda plus a half turn. Each side has a "plus" detector where a
reference lamp lands one quantum per tick at the detector's setting phase, so
the coherence of the arriving ray with the reference is cos^2 of half their
phase difference and the lottery capture takes the ray with that probability
(Malus's law on the Kerengonen coherence); a ray not taken walks on to a
"minus" detector that takes it surely. Every capture opens a claim, so the
surviving root of each train says where that quantum landed. Over every
hidden phase and many capture seeds, for the four CHSH setting pairs, the
correlations E(a, b) and S = |E(a,b) - E(a,b') + E(a',b) + E(a',b')| are
measured against the local bound 2 and the quantum value 2 sqrt 2. Every
number is a read-only world/event audit at host lattice coordinates; no
angle unit or constant is identified: a setting is a phase step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path

from event_universe import Simulation
from event_universe.core.spatial_state import (
    PHASE_COSINE_SCALE,
    TICKET_MODULUS,
    origin_bond,
    phase_cosines,
)
from event_universe.fields.bonds import BondRegistry
from event_universe.initialization import parse_initial_state
from event_universe.runner import source_fingerprint

WIDTH = 13
CENTER = WIDTH // 2
DISTANCE = 3  # links from the source to each plus detector; the minus detector is one further
PHASE_STEPS = 64
HALF_TURN = PHASE_STEPS // 2
# CHSH settings as phase steps: Alice 0 and a quarter turn, Bob an eighth and three eighths.
SETTINGS = {"a": 0, "a2": 16, "b": 8, "b2": 24}
PAIRS = (("a", "b"), ("a", "b2"), ("a2", "b"), ("a2", "b2"))
SEEDS = 16
TICKS = DISTANCE + 6
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


def document(
    hidden_phase: int,
    alice: int,
    bob: int,
    seed: int,
    ticks: int = TICKS,
    capture: str = "lottery",
    stream: int | None = None,
) -> dict:
    """One pair at hidden phase lambda, detector settings for Alice and Bob, one capture seed.

    With capture "bond" and a stream number, the registry takes the pair's
    number from outside the world instead of from its own sequence: the door
    of postulate 22 for a source outside the world's state.

    With capture "threshold" the detectors are deterministic hidden-variable
    devices: a ray is taken when its coherence with the reference reaches one
    half, so the outcome is fixed by lambda and the setting alone. With capture
    "bond" the two rays are bonded to their origin, the Node and tick of their
    birth, which each carries until its next interaction; each plus detector
    holds its setting, and the bond registry, the declared exception to the
    causal bound, answers for both ends with the singlet's joint law. The seed
    then seeds the registry and there are no reference lamps.
    """
    body = {
        "fields": ["quanta", "momentum"],
        "defaults": {"quanta": 0, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    plus_alice, plus_bob = CENTER - DISTANCE, CENTER + DISTANCE
    bonded = capture == "bond"
    detector = {
        "fields": ["quanta", "momentum", "setting"],
        "transport": {"mode": "hold"},
    }
    raw = {
        "schema_version": 1,
        "model_id": "bell-chsh-ray-probe-v1",
        "shape": [WIDTH, 3, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
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
        "disturbance_types": [
            {
                "name": "source_alice",
                "fields": ["quanta", "momentum", "train"],
                "defaults": {"quanta": 1, "momentum": [0, 0, 0], "train": 1},
                "transport": {"mode": "hold"},
            },
            {
                "name": "source_bob",
                "fields": ["quanta", "momentum", "train"],
                "defaults": {"quanta": 1, "momentum": [0, 0, 0], "train": 2},
                "transport": {"mode": "hold"},
            },
            {
                "name": "reference_alice",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "reference_bob",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": ticks, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "plus_alice",
                **detector,
                "defaults": {"quanta": 0, "momentum": [0, 0, 0], "setting": alice % PHASE_STEPS},
            },
            {"name": "minus_alice", **body},
            {
                "name": "plus_bob",
                **detector,
                "defaults": {"quanta": 0, "momentum": [0, 0, 0], "setting": bob % PHASE_STEPS},
            },
            {"name": "minus_bob", **body},
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": [[-1, 0, 0], [1, 0, 0], [0, -1, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "kerengonen": {
                    "phase_steps": PHASE_STEPS,
                    "phase_advance": 0,
                    "capture": "share" if bonded else capture,
                    **({"capture_seed": seed} if capture == "lottery" else {}),
                },
                "claim": {"ticks": 4 * ticks, "slots": 4},
                **(
                    {"bond": {"seed": seed, **({"stream": [stream]} if stream is not None else {})}}
                    if bonded
                    else {}
                ),
            }
        ],
        "emissions": [
            {
                "type": "source_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": hidden_phase % PHASE_STEPS,
                "train_field": "train",
                "heading": [-1, 0, 0],
                **({"bond_field": "origin"} if bonded else {}),
            },
            {
                "type": "source_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": (hidden_phase + HALF_TURN) % PHASE_STEPS,
                "train_field": "train",
                "heading": [1, 0, 0],
                **({"bond_field": "origin"} if bonded else {}),
            },
            {
                "type": "reference_alice",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": alice % PHASE_STEPS,
                "heading": [0, -1, 0],
            },
            {
                "type": "reference_bob",
                "field": "quanta",
                "amount": 1,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "kerengonen_phase": bob % PHASE_STEPS,
                "heading": [0, -1, 0],
            },
        ],
        "spatial_couplings": [
            {
                "name": f"{name}_absorbs",
                "field": "quanta",
                "mode": "absorb",
                "momentum_field": "momentum",
                "claim": True,
                # Each detector draws its own ticket sequence: two devices, two dice.
                **({"capture_salt": salt} if capture == "lottery" else {}),
                # Bonded: the plus detectors hold their settings; the registry answers.
                **({"bond_setting": "setting"} if bonded and name.startswith("plus") else {}),
                "type": name,
            }
            for name, salt in (
                ("plus_alice", 0),
                ("minus_alice", 1),
                ("plus_bob", 2),
                ("minus_bob", 3),
            )
        ],
        "seeds": [
            {"position": [CENTER, 1, 1], "type": "source_alice"},
            {"position": [CENTER, 1, 1], "type": "source_bob"},
            {"position": [plus_alice, 1, 1], "type": "plus_alice"},
            {"position": [plus_alice - 1, 1, 1], "type": "minus_alice"},
            {"position": [plus_alice, 2, 1], "type": "reference_alice"},
            {"position": [plus_bob, 1, 1], "type": "plus_bob"},
            {"position": [plus_bob + 1, 1, 1], "type": "minus_bob"},
            {"position": [plus_bob, 2, 1], "type": "reference_bob"},
        ],
    }
    if bonded:
        # No reference lamps: the setting lives in the detector, the coin in the registry.
        raw["disturbance_types"] = [
            kind for kind in raw["disturbance_types"] if not kind["name"].startswith("reference")
        ]
        raw["emissions"] = [
            rule for rule in raw["emissions"] if not rule["type"].startswith("reference")
        ]
        raw["seeds"] = [seed_ for seed_ in raw["seeds"] if not seed_["type"].startswith("reference")]
    return raw


def outcomes(raw: dict) -> dict:
    """Where each train landed: +1 at a plus detector, -1 at a minus detector."""
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()["quanta"][0]
    for _ in range(raw["ticks"]):
        world.step()
    names = [kind["name"] for kind in raw["disturbance_types"]]
    detectors = {
        node.position: names[record.type_index]
        for node in world.inventory_view().nodes
        for record in node.records
        if record is not None and names[record.type_index].split("_")[0] in ("plus", "minus")
    }
    landed: dict[int, int] = {}
    for node in world.inventory_view().nodes:
        for claim in node.claims[0] if node.claims else ():
            if claim.parent < 0:
                landed[claim.train] = 1 if str(detectors.get(claim.origin)).startswith("plus") else -1
    escaped = world.escaped_totals()["quanta"][0]
    return {
        "alice": landed.get(1),
        "bob": landed.get(2),
        "closed": world.totals()["quanta"][0] + escaped == initial,
    }


SOURCES = ("sequence", "uniform", "biased", "agreement")


def external_number(key: int, source: str) -> int | None:
    """The pair's number from outside the world: none, uniform, coin-biased or agreement-biased.

    The uniform source is a generator that is not the registry's: the same physics
    must follow. The biased source keeps the upper half of every number below one
    half, so the end that asks first always answers +1; its lower half stays
    uniform, so the singlet's agreement law is untouched. The agreement source
    keeps the coin even and fixes the lower half at one half of the modulus,
    which lies above the agreement threshold of the settings a quarter turn
    apart (75/512) and below that of the settings three quarters apart
    (437/512): the ends disagree at (a, b), (a', b) and (a', b') and agree at
    (a, b'), the Popescu-Rohrlich box, with each end's marginal still even.
    """
    if source == "sequence":
        return None
    generator = random.Random(1_000_003 * key + 7)
    if source == "agreement":
        return TICKET_MODULUS // 4 + generator.randrange(2) * (TICKET_MODULUS // 2)
    draw = generator.randrange(TICKET_MODULUS)
    if source == "biased":
        return draw // 2
    return draw


def correlation(
    alice: int, bob: int, seeds: int = SEEDS, capture: str = "lottery", source: str = "sequence"
) -> dict:
    """E(a, b) over every hidden phase and the given number of capture seeds."""
    total = count = 0
    plus_alice = plus_bob = 0
    missing = 0
    closed = True
    for hidden in range(PHASE_STEPS):
        for seed in range(1, seeds + 1):
            # A bonded pair has no hidden phase: every run seeds the registry afresh.
            registry_seed = hidden * seeds + seed if capture == "bond" else seed
            stream = external_number(registry_seed, source) if capture == "bond" else None
            result = outcomes(
                document(hidden, alice, bob, registry_seed, capture=capture, stream=stream)
            )
            closed = closed and result["closed"]
            if result["alice"] is None or result["bob"] is None:
                missing += 1
                continue
            total += result["alice"] * result["bob"]
            count += 1
            plus_alice += result["alice"] > 0
            plus_bob += result["bob"] > 0
    turn = 2 * math.pi * (alice - bob) / PHASE_STEPS
    if capture == "threshold":
        # Deterministic detectors: the triangle-wave correlation of the sign model.
        fraction = (abs(alice - bob) % PHASE_STEPS) / PHASE_STEPS
        fraction = min(fraction, 1 - fraction)
        predicted = -(1 - 4 * fraction)
    elif capture == "bond":
        # The registry draws the singlet: the quantum correlation itself.
        predicted = -math.cos(turn)
    else:
        predicted = -0.5 * math.cos(turn)
    return {
        "alice": alice,
        "bob": bob,
        "pairs": count,
        "missing": missing,
        "E": round(total / count, 4) if count else None,
        "predicted_E": round(predicted, 4),
        "quantum_E": round(-math.cos(turn), 4),
        "alice_plus_rate": round(plus_alice / count, 4) if count else None,
        "bob_plus_rate": round(plus_bob / count, 4) if count else None,
        "closed": closed,
    }


def signalling(results: dict) -> dict:
    """How far each end's plus rate moves with the other end's setting: zero without a signal."""
    alice = max(
        abs(results["a,b"]["alice_plus_rate"] - results["a,b2"]["alice_plus_rate"]),
        abs(results["a2,b"]["alice_plus_rate"] - results["a2,b2"]["alice_plus_rate"]),
    )
    bob = max(
        abs(results["a,b"]["bob_plus_rate"] - results["a2,b"]["bob_plus_rate"]),
        abs(results["a,b2"]["bob_plus_rate"] - results["a2,b2"]["bob_plus_rate"]),
    )
    return {"alice_rate_shift": round(alice, 4), "bob_rate_shift": round(bob, 4)}


def chsh(seeds: int = SEEDS, capture: str = "lottery", source: str = "sequence") -> dict:
    results = {
        f"{left},{right}": correlation(SETTINGS[left], SETTINGS[right], seeds, capture, source)
        for left, right in PAIRS
    }
    e = {key: value["E"] for key, value in results.items()}
    s = abs(e["a,b"] - e["a,b2"] + e["a2,b"] + e["a2,b2"])
    predicted = abs(
        results["a,b"]["predicted_E"]
        - results["a,b2"]["predicted_E"]
        + results["a2,b"]["predicted_E"]
        + results["a2,b2"]["predicted_E"]
    )
    quantum = abs(
        results["a,b"]["quantum_E"]
        - results["a,b2"]["quantum_E"]
        + results["a2,b"]["quantum_E"]
        + results["a2,b2"]["quantum_E"]
    )
    return {
        "settings": SETTINGS,
        "seeds": seeds,
        "capture": capture,
        "correlations": results,
        "S": round(s, 4),
        "predicted_S": round(predicted, 4),
        "local_bound": 2,
        "quantum_S": round(quantum, 4),
        "same_setting_E": correlation(0, 0, seeds, capture, source)["E"],
        "closed": all(value["closed"] for value in results.values()),
        "source": source,
        **signalling(results),
    }


# --- Statistics of the bonded value and the causal factorization of every candidate ---

EXPECTED_BOND_S = Fraction(
    abs(
        sum(
            sign * -phase_cosines(PHASE_STEPS)[(SETTINGS[left] - SETTINGS[right]) % PHASE_STEPS]
            for sign, (left, right) in zip((1, -1, 1, 1), PAIRS, strict=True)
        )
    ),
    PHASE_COSINE_SCALE,
)
"""The registry's exact expectation of S on the 64-step table: 724/256 = 2.828125.

The second end agrees when the number's lower half, uniform below the modulus,
falls under (256 - c) / 512, so E(a, b) = -c / 256 in expectation for the table
cosine c of the settings' difference; the four terms give 4 x 181 / 256.
"""
PROBE_BOND = origin_bond((CENTER, 1, 1), (WIDTH, 3, 3), 0)
LATTICE_LEVELS = (64, 256, 1024, 4096)
REGISTRY_LEVELS = (1000, 10000, 100000, 1000000)
REPLICAS = 4


def sweep_seed(pairs: int, replica: int, setting: int, index: int) -> int:
    """A registry seed for one pair: fresh for every level, replica, setting pair and pair."""
    offset = pairs.bit_length() * 2**26 + (replica * len(PAIRS) + setting) * pairs + index
    return 1 + offset % (TICKET_MODULUS - 1)


def registry_pair(seed: int, alice: int, bob: int) -> tuple[int, int]:
    """The registry alone, no lattice: Alice asks first at her setting, Bob second at his."""
    registry = BondRegistry(seed, PHASE_STEPS)
    return registry.draw(PROBE_BOND, alice, 1), registry.draw(PROBE_BOND, bob, 2)


def lattice_pair(job: tuple[int, int, int]) -> tuple[int | None, int | None, bool]:
    """One bonded pair on the lattice: (Alice's outcome, Bob's outcome, closed)."""
    seed, alice, bob = job
    result = outcomes(document(0, alice, bob, seed, capture="bond"))
    return result["alice"], result["bob"], result["closed"]


def standard_error(e: float, count: int) -> float:
    """The binomial standard error of a correlation of +-1 products over count pairs."""
    return math.sqrt(max(1 - e * e, 0) / count) if count else 0.0


def bonded_statistics(pairs: int, replica: int, lattice: bool, workers: int = 1) -> dict:
    """E(a, b) over `pairs` fresh bonded pairs per setting pair, with standard errors.

    Every setting pair draws its own pairs, so the four correlations are independent
    samples and the error of S is the root of the sum of their squared errors. On
    the lattice every pair is also computed by the registry alone from the same
    seed, and the two are compared outcome by outcome.
    """
    correlations = {}
    closed = True
    identical = 0
    for setting, (left, right) in enumerate(PAIRS):
        alice, bob = SETTINGS[left], SETTINGS[right]
        seeds = [sweep_seed(pairs, replica, setting, index) for index in range(pairs)]
        registry = [registry_pair(seed, alice, bob) for seed in seeds]
        if lattice:
            jobs = [(seed, alice, bob) for seed in seeds]
            if workers > 1:
                with ProcessPoolExecutor(max_workers=workers) as pool:
                    landed = list(pool.map(lattice_pair, jobs, chunksize=16))
            else:
                landed = [lattice_pair(job) for job in jobs]
            closed = closed and all(row[2] for row in landed)
            sample = [(row[0], row[1]) for row in landed]
            identical += sum(a == b for a, b in zip(sample, registry, strict=True))
        else:
            sample = registry
        total = sum(a * b for a, b in sample if a is not None and b is not None)
        count = sum(a is not None and b is not None for a, b in sample)
        e = total / count if count else 0.0
        correlations[f"{left},{right}"] = {
            "pairs": count,
            "missing": pairs - count,
            "E": round(e, 5),
            "sigma_E": round(standard_error(e, count), 5),
            "expected_E": round(
                -phase_cosines(PHASE_STEPS)[(alice - bob) % PHASE_STEPS] / PHASE_COSINE_SCALE, 5
            ),
            "alice_plus_rate": round(sum(a > 0 for a, _ in sample) / count, 4) if count else None,
            "bob_plus_rate": round(sum(b > 0 for _, b in sample) / count, 4) if count else None,
        }
    e = {key: value["E"] for key, value in correlations.items()}
    s = abs(e["a,b"] - e["a,b2"] + e["a2,b"] + e["a2,b2"])
    sigma = math.sqrt(sum(value["sigma_E"] ** 2 for value in correlations.values()))
    return {
        "pairs_per_correlation": pairs,
        "replica": replica,
        "lattice": lattice,
        "correlations": correlations,
        "S": round(s, 5),
        "sigma_S": round(sigma, 5),
        "expected_S": float(EXPECTED_BOND_S),
        "quantum_S": round(2 * math.sqrt(2), 5),
        "z": round((s - float(EXPECTED_BOND_S)) / sigma, 3) if sigma else None,
        **({"closed": closed, "identical_to_registry": identical} if lattice else {}),
    }


def sweep(
    lattice_levels: tuple[int, ...] = LATTICE_LEVELS,
    registry_levels: tuple[int, ...] = REGISTRY_LEVELS,
    replicas: int = REPLICAS,
    workers: int = 1,
) -> dict:
    """S against the number of pairs: the lattice up to 4096, the registry alone beyond."""
    levels = []
    for lattice, level_list in ((True, lattice_levels), (False, registry_levels)):
        for pairs in level_list:
            runs = [bonded_statistics(pairs, replica, lattice, workers) for replica in range(replicas)]
            values = [run["S"] for run in runs]
            mean = sum(values) / len(values)
            spread = (
                math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1))
                if len(values) > 1
                else 0.0
            )
            levels.append(
                {
                    "pairs_per_correlation": pairs,
                    "lattice": lattice,
                    "replicas": replicas,
                    "S_values": values,
                    "S_mean": round(mean, 5),
                    "S_spread": round(spread, 5),
                    "S_error_of_mean": round(spread / math.sqrt(len(values)), 5),
                    "sigma_S_predicted": runs[0]["sigma_S"],
                    "deviation_from_expected": round(mean - float(EXPECTED_BOND_S), 5),
                    "runs": runs,
                }
            )
    return {
        "settings": SETTINGS,
        "expected_S": float(EXPECTED_BOND_S),
        "expected_S_exact": f"{EXPECTED_BOND_S.numerator}/{EXPECTED_BOND_S.denominator}",
        "quantum_S": round(2 * math.sqrt(2), 5),
        "local_bound": 2,
        "levels": levels,
    }


CANDIDATES = ("lottery", "threshold", "bond")


def causal_factors(capture: str, seeds: int = 4, workers: int = 1) -> dict:
    """Does either end's outcome move with the other end's setting at fixed hidden variable?

    For every hidden variable lambda (hidden phase and seed) the four setting pairs
    are run and the outcomes tabulated as A(a, b, lambda) and B(a, b, lambda).
    Parameter independence at Alice means A(a, b) = A(a, b') for every lambda,
    and at Bob B(a, b) = B(a', b); the rates of violation are counted. Locality in
    Bell's sense, P(A, B | a, b, lambda) = P(A | a, lambda) P(B | b, lambda),
    needs both rates to vanish. The hidden variable's distribution is the same
    for every setting pair by construction: the seed and hidden phase are chosen
    before the settings and do not read them, which is measurement independence.
    """
    jobs = []
    for hidden in range(PHASE_STEPS):
        for seed in range(1, seeds + 1):
            registry_seed = hidden * seeds + seed if capture == "bond" else seed
            for left, right in PAIRS:
                jobs.append((hidden, seed, left, right, registry_seed))

    jobs = [(capture,) + job for job in jobs]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(_causal_job, jobs, chunksize=16))
    else:
        rows = [_causal_job(job) for job in jobs]
    table: dict[tuple[int, int], dict[tuple[str, str], tuple[int | None, int | None]]] = {}
    closed = True
    for (hidden, seed, left, right), a, b, ok in rows:
        table.setdefault((hidden, seed), {})[(left, right)] = (a, b)
        closed = closed and ok
    alice_moves = {"a": 0, "a2": 0}
    bob_moves = {"b": 0, "b2": 0}
    complete = 0
    for cells in table.values():
        if any(None in pair for pair in cells.values()):
            continue
        complete += 1
        for setting in alice_moves:
            alice_moves[setting] += cells[(setting, "b")][0] != cells[(setting, "b2")][0]
        for setting in bob_moves:
            bob_moves[setting] += cells[("a", setting)][1] != cells[("a2", setting)][1]
    return {
        "capture": capture,
        "hidden_variables": complete,
        "closed": closed,
        "alice_moves_with_bob_setting": {
            key: round(value / complete, 4) for key, value in alice_moves.items()
        },
        "bob_moves_with_alice_setting": {
            key: round(value / complete, 4) for key, value in bob_moves.items()
        },
        "parameter_independent": all(v == 0 for v in alice_moves.values())
        and all(v == 0 for v in bob_moves.values()),
    }


def _causal_job(job: tuple) -> tuple:
    capture, hidden, seed, left, right, registry_seed = job
    result = outcomes(document(hidden, SETTINGS[left], SETTINGS[right], registry_seed, capture=capture))
    return (hidden, seed, left, right), result["alice"], result["bob"], result["closed"]


def causal_analysis(seeds: int = 4, workers: int = 1) -> dict:
    """The parameter-independence rates of the three ray candidates."""
    return {
        "settings": SETTINGS,
        "candidates": {capture: causal_factors(capture, seeds, workers) for capture in CANDIDATES},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", type=int, default=SEEDS)
    parser.add_argument("--capture", choices=("lottery", "threshold", "bond"), default="lottery")
    parser.add_argument("--source", choices=SOURCES, default="sequence")
    parser.add_argument(
        "--sweep",
        action="store_true",
        help="S against the number of bonded pairs, with standard errors, lattice and registry",
    )
    parser.add_argument("--lattice-pairs", type=int, nargs="*", default=list(LATTICE_LEVELS))
    parser.add_argument("--registry-pairs", type=int, nargs="*", default=list(REGISTRY_LEVELS))
    parser.add_argument("--replicas", type=int, default=REPLICAS)
    parser.add_argument(
        "--causal",
        action="store_true",
        help="parameter-independence rates of the lottery, threshold and bonded candidates",
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="processes for the sweep and causal modes"
    )
    args = parser.parse_args()
    if args.source != "sequence" and args.capture != "bond":
        raise SystemExit("an external number source applies to the bonded capture only")
    args.output.mkdir(parents=True, exist_ok=True)
    stamp = {
        "source_sha256": source_fingerprint(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "measurement_scope": "read-only world/event audit",
        "phase_steps": PHASE_STEPS,
    }
    if args.sweep:
        result = sweep(
            tuple(args.lattice_pairs), tuple(args.registry_pairs), args.replicas, args.workers
        )
        (args.output / "summary-bond-sweep.json").write_text(
            json.dumps({**stamp, **result}, indent=2) + "\n"
        )
        for level in result["levels"]:
            print(
                "lattice" if level["lattice"] else "registry",
                level["pairs_per_correlation"],
                "pairs: S",
                level["S_mean"],
                "+-",
                level["S_error_of_mean"],
                "(spread",
                level["S_spread"],
                "predicted sigma",
                level["sigma_S_predicted"],
                ") expected",
                result["expected_S"],
                *(
                    ("identical to registry", sum(r["identical_to_registry"] for r in level["runs"]))
                    if level["lattice"]
                    else ()
                ),
            )
        print("Wrote report: " + str(args.output / "summary-bond-sweep.json"))
        return
    if args.causal:
        result = causal_analysis(args.seeds if args.seeds != SEEDS else 4, args.workers)
        (args.output / "summary-causal.json").write_text(
            json.dumps({**stamp, **result}, indent=2) + "\n"
        )
        for name, row in result["candidates"].items():
            print(
                name,
                "Alice moves with Bob's setting",
                row["alice_moves_with_bob_setting"],
                "Bob moves with Alice's setting",
                row["bob_moves_with_alice_setting"],
                "closed",
                row["closed"],
            )
        print("Wrote report: " + str(args.output / "summary-causal.json"))
        return
    result = chsh(args.seeds if args.capture != "threshold" else 1, args.capture, args.source)
    report = {**stamp, **result}
    name = args.capture if args.source == "sequence" else f"{args.capture}-{args.source}"
    (args.output / f"summary-{name}.json").write_text(json.dumps(report, indent=2) + "\n")
    for key, value in result["correlations"].items():
        print(
            key,
            "E",
            value["E"],
            "predicted",
            value["predicted_E"],
            "quantum",
            value["quantum_E"],
            "plus rates",
            value["alice_plus_rate"],
            value["bob_plus_rate"],
            "missing",
            value["missing"],
            "closed",
            value["closed"],
        )
    print(
        "S",
        result["S"],
        "predicted",
        result["predicted_S"],
        "local bound",
        result["local_bound"],
        "quantum",
        result["quantum_S"],
        "same setting E",
        result["same_setting_E"],
    )
    print(
        "source", result["source"], "rate shifts", result["alice_rate_shift"], result["bob_rate_shift"]
    )
    print("Wrote report: " + str(args.output / f"summary-{name}.json"))


if __name__ == "__main__":
    main()
