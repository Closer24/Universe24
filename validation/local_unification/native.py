"""Bounded conservative carrier–record collisions in the unchanged Engine.

Every node retains two four-rail banks.  The local involution exchanges
1001 and 0110 in (record+, record-, carrier+, carrier-) order.  A paired-bank
lift alternates local collision and face transport without composing
multi-edge products.  It is a research tensor, not an installed default.
"""
from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path

import numpy as np

from universe24.core import DIRECTIONS, Engine, GearType, State, Tensor, lattice
from universe24.core import exact_json


ZERO = (0, 0, 0)
LANES = ("record_plus", "record_minus", "carrier_plus", "carrier_minus")
BANKS = ("A", "B")
CHANNEL_NAMES = tuple(f"local_unification.{bank}.{lane}" for bank in BANKS for lane in LANES)
ROLES = {"record": (0, 1, 4, 5), "carrier": (2, 3, 6, 7)}
GATE_TABLE = tuple((0, 1, 1, 0) if row == (1, 0, 0, 1) else
                  (1, 0, 0, 1) if row == (0, 1, 1, 0) else row
                  for row in product((0, 1), repeat=4))
# delta = ad(1-b-c)-bc(1-a-d); quartic terms cancel exactly.
DELTA_TERMS = ((1, (0, 3)), (-1, (0, 1, 3)), (-1, (0, 2, 3)),
               (-1, (1, 2)), (1, (0, 1, 2)), (1, (1, 2, 3)))


def _options(direction, coupled, stream_records):
    direction = tuple(direction)
    if (len(direction) != 3 or any(type(v) is not int for v in direction)
            or direction not in DIRECTIONS):
        raise ValueError("direction must be one exact integer face direction")
    if type(coupled) is not bool or type(stream_records) is not bool:
        raise ValueError("coupled and stream_records must be exact booleans")
    return direction


def velocities(direction=(1, 0, 0), *, stream_records=True):
    direction = _options(direction, True, stream_records)
    reverse = tuple(-v for v in direction)
    return (direction if stream_records else ZERO,
            reverse if stream_records else ZERO, direction, reverse)


def gate(bits, *, coupled=True):
    """Literal truth-table oracle, independent of compiled polynomial terms."""
    if type(coupled) is not bool:
        raise ValueError("coupled must be an exact boolean")
    row = tuple(bits)
    if len(row) != 4 or any(type(v) is not int or v not in (0, 1) for v in row):
        raise ValueError("collision requires four exact Boolean integers")
    if coupled and row == (1, 0, 0, 1):
        return (0, 1, 1, 0)
    if coupled and row == (0, 1, 1, 0):
        return (1, 0, 0, 1)
    return row


def build_tensor(direction=(1, 0, 0), *, coupled=True, stream_records=True):
    """Compile F(A,B)=(G(B),S(A)) via u=3(F+F^-1).

    F^-1(A,B)=(S^-1(B),G(A)), since G is an involution.  Each G term
    is onsite, each S term linear across one face.  All eight triples are
    retained.  The proof requires Boolean current rails and a=F^-1(b).
    """
    direction = _options(direction, coupled, stream_records)
    speed = velocities(direction, stream_records=stream_records)
    terms = []
    for bank in range(2):
        source = 4 * (1-bank)
        for lane, sign in enumerate((-1, 1, 1, -1)):
            target = 4*bank+lane
            # G on the opposite bank.
            terms.append((target, 3, [(source+lane, ZERO, "b")]))
            if coupled:
                for coefficient, factors in DELTA_TERMS:
                    terms.append((target, 3*sign*coefficient,
                                  [(source+factor, ZERO, "b") for factor in factors]))
            # Bank A receives S^-1(B), bank B receives S(A).
            offset = speed[lane] if bank == 0 else tuple(-v for v in speed[lane])
            terms.append((target, 3, [(source+lane, offset, "b")]))
    return Tensor([GearType(name, "audit") for name in CHANNEL_NAMES], terms, strict_support=True)


def _rails(values, L):
    grid = lattice(L)
    values = np.asarray(values, dtype=object)
    if values.shape != (8, grid.N):
        raise ValueError("provide exactly eight complete current rail rows")
    if any(not isinstance(v, (int, np.integer)) or isinstance(v, (bool, np.bool_))
           or int(v) not in (0, 1) for v in values.flat):
        raise ValueError("current rails must be Boolean integers, not truthy values")
    return values.copy()


def first_order(values, L, direction=(1, 0, 0), *, coupled=True,
                stream_records=True, inverse=False):
    """Literal collision/shift oracle; does not evaluate the tensor polynomial."""
    direction = _options(direction, coupled, stream_records)
    if type(inverse) is not bool:
        raise ValueError("inverse must be an exact boolean")
    values = _rails(values, L)
    grid = lattice(L)
    speed = velocities(direction, stream_records=stream_records)
    result = np.zeros_like(values)
    collision_bank, collision_target = (0, 4) if inverse else (4, 0)
    for node in range(grid.N):
        result[collision_target:collision_target+4, node] = gate(
            tuple(int(v) for v in values[collision_bank:collision_bank+4, node]), coupled=coupled)
    stream_bank, stream_target = (4, 0) if inverse else (0, 4)
    for lane, direction_for_lane in enumerate(speed):
        offset = direction_for_lane if inverse else tuple(-v for v in direction_for_lane)
        result[stream_target+lane] = values[stream_bank+lane, grid.shift_index(offset)]
    return result


def prepare_state(current, L, direction=(1, 0, 0), *, coupled=True,
                  stream_records=True, remainders=None):
    """Prepare the complete invariant sector; no history is zeroed afterwards."""
    current = _rails(current, L)
    previous = first_order(current, L, direction, coupled=coupled,
                           stream_records=stream_records, inverse=True)
    if remainders is None:
        remainders = np.zeros_like(current)
    else:
        remainders = np.asarray(remainders, dtype=object)
    if (remainders.shape != current.shape
            or any(not isinstance(v, (int, np.integer)) or isinstance(v, (bool, np.bool_))
                   or not 0 <= int(v) < 6 for v in remainders.flat)):
        raise ValueError("provide eight complete legal carry rows")
    return State(L, previous, current, remainders.copy())


def validate_prepared_state(state, direction=(1, 0, 0), *, coupled=True, stream_records=True):
    if not isinstance(state, State):
        raise ValueError("a complete State is required")
    expected = first_order(state.b, state.L, direction, coupled=coupled,
                           stream_records=stream_records, inverse=True)
    if state.a.shape != expected.shape or not np.array_equal(state.a, expected):
        raise ValueError("complete history is outside a=F^-1(b)")
    if any(not isinstance(v, (int, np.integer)) or isinstance(v, (bool, np.bool_))
           or not 0 <= int(v) < 6 for v in state.r.flat):
        raise ValueError("invalid retained remainder")
    return True


def totals(values):
    """Exact packet accounts; no claim of an operational energy calibration."""
    values = np.asarray(values, dtype=object)
    if values.ndim != 2 or values.shape[0] != 8:
        raise ValueError("eight current rail rows required")
    if any(not isinstance(v, (int, np.integer)) or isinstance(v, (bool, np.bool_))
           or int(v) not in (0, 1) for v in values.flat):
        raise ValueError("packet accounts require the declared Boolean rail sector")
    energy = sum(int(v) for v in values.flat)
    momentum = sum((1 if g % 4 in (0, 2) else -1)*int(v)
                   for g in range(8) for v in values[g])
    return {"energy": energy, "momentum": momentum,
            "records": sum(int(v) for g in ROLES["record"] for v in values[g]),
            "carriers": sum(int(v) for g in ROLES["carrier"] for v in values[g])}


def repeated_fixture(L=7, direction=(1, 0, 0), *, coupled=True, stream_records=True):
    """Two collisions per bank cohort at one receiver, before recirculation.

    Expected receiver collisions are microsteps1,2,5,6 with the default law.
    Incoming record+/carrier- packets are present in the complete seed only.
    Return (tensor, complete_seed, passive_protocol); no runtime injection.
    """
    direction = _options(direction, coupled, stream_records)
    if type(L) is not int or L < 7:
        raise ValueError("the four-encounter fixture requires integer L>=7")
    grid = lattice(L)
    current = np.zeros((8, grid.N), dtype=object)
    def node(distance):
        return grid.index(*(distance*v for v in direction))
    for distance in (0, 2):
        current[4, node(-distance)] = 1
        current[7, node(distance)] = 1
    for distance in (1, 3):
        current[0, node(-distance)] = 1
        current[3, node(distance)] = 1
    carries = np.asarray([[(g+n) % 6 for n in range(grid.N)] for g in range(8)], dtype=object)
    seed = prepare_state(current, L, direction, coupled=coupled,
                         stream_records=stream_records, remainders=carries)
    protocol = {"receiver": node(0), "steps": 6, "expected_selected_steps": [1, 2, 5, 6],
                "same_cohort_steps": [[1, 5], [2, 6]], "direction": list(direction),
                "scope": "finite preloaded packet train; no runtime preparation or reset"}
    return build_tensor(direction, coupled=coupled, stream_records=stream_records), seed, protocol


def matched_record_pair(L=3, direction=(1, 0, 0), *, coupled=True):
    """Change record orientation while ALL retained carrier triples agree.

    Both preparations contain one record and one carrier. Their signed
    record momentum differs; this is not a same-stress intervention.
    """
    direction = _options(direction, coupled, True)
    grid = lattice(L)
    left = np.zeros((8, grid.N), dtype=object)
    left[4, 0] = 1; left[7, 0] = 1
    right = left.copy(); right[4, 0] = 0; right[5, 0] = 1
    carries = np.asarray([[(g+n) % 6 for n in range(grid.N)] for g in range(8)], dtype=object)
    seeds = [prepare_state(values, L, direction, coupled=coupled, remainders=carries)
             for values in (left, right)]
    for field in ("a", "b", "r"):
        assert np.array_equal(getattr(seeds[0], field)[list(ROLES["carrier"])],
                              getattr(seeds[1], field)[list(ROLES["carrier"])])
    return build_tensor(direction, coupled=coupled), seeds[0], seeds[1]


def audit(out=None):
    """Independent truth table, complete-state execution and held-out controls."""
    truth_rows = []
    for bits in product((0, 1), repeat=4):
        a, b, c, d = bits
        delta = a*d*(1-b-c)-b*c*(1-a-d)
        polynomial = (a-delta, b+delta, c+delta, d-delta)
        expected = gate(bits)
        assert polynomial == expected and gate(expected) == bits
        assert sum(expected) == sum(bits)
        assert expected[0]+expected[2] == a+c
        assert expected[1]+expected[3] == b+d
        truth_rows.append({"before": list(bits), "after": list(expected)})
    rng = np.random.default_rng(630108)
    transitions = comparisons = 0
    runs = []
    for direction in DIRECTIONS:
        law = build_tensor(direction)
        assert law.G == 8 and law.rank <= 4 and not law.support_violations()
        for trial in range(3):
            current = rng.integers(0, 2, size=(8, 27)).astype(object)
            carries = np.asarray([[(g+n+trial) % 6 for n in range(27)] for g in range(8)], dtype=object)
            seed = prepare_state(current, 3, direction, remainders=carries)
            state = seed
            initial_totals = totals(seed.b)
            engine = Engine(law)
            for _ in range(12):
                expected = first_order(state.b, 3, direction)
                after = engine.step(state)
                assert np.array_equal(after.a, state.b) and np.array_equal(after.b, expected)
                assert np.array_equal(after.r, carries)
                validate_prepared_state(after, direction)
                assert totals(after.b) == initial_totals
                assert engine.inverse_step(after).same_as(state)
                transitions += 1
                comparisons += 3*8*27
                state = after
            assert engine.rewind(state, 12).same_as(seed)
            runs.append({"direction": list(direction), "trial": trial, "steps": 12,
                         "tensor_hash": law.fingerprint, "totals": initial_totals})
    cases = []
    for label, coupled, streamed in (("connected", True, True), ("collision_off", False, True),
                                      ("record_transport_off", True, False)):
        law, seed, protocol = repeated_fixture(coupled=coupled, stream_records=streamed)
        engine = Engine(law); state = seed
        encounters = []
        for step in range(1, protocol["steps"]+1):
            node = protocol["receiver"]
            incoming = tuple(int(x) for x in state.b[4:8, node])
            after = engine.step(state)
            outgoing = tuple(int(x) for x in after.b[:4, node])
            encounters.append({"step": step, "input": list(incoming), "output": list(outgoing),
                               "selected": incoming == (1, 0, 0, 1) and outgoing == (0, 1, 1, 0)})
            assert np.array_equal(after.b, first_order(state.b, state.L, coupled=coupled,
                                                       stream_records=streamed))
            assert engine.inverse_step(after).same_as(state)
            state = after
        assert engine.rewind(state, protocol["steps"]).same_as(seed)
        selected = [row["step"] for row in encounters if row["selected"]]
        if label == "connected":
            assert selected == protocol["expected_selected_steps"]
        if label == "collision_off":
            assert not selected
        if label == "record_transport_off":
            assert selected != protocol["expected_selected_steps"]
        cases.append({"label": label, "tensor_hash": law.fingerprint,
                      "encounters": encounters, "selected_steps": selected,
                      "complete_rewind": True})
    report = {"schema": "universe24/local-unification/native/1", "channels": 8,
              "retained_integers_per_node": 24, "gate_table": truth_rows,
              "prepared_sector": "all current rails Boolean; a=F^-1(b); every carry0..5",
              "complete_transitions": transitions, "integer_comparisons": comparisons,
              "random_runs": runs, "repeated_cases": cases,
              "maximum_rail_bits": 1, "maximum_carry_bits": 3,
              "all_time_boolean_and_inverse_theorem": True,
              "source_scope": "positive packet energy and signed propagation momentum; uncalibrated",
              "general_Einstein": "not_established", "complexity_growth": "not_established"}
    interventions = []
    for direction in DIRECTIONS:
        for coupled in (True, False):
            law, left, right = matched_record_pair(direction=direction, coupled=coupled)
            engine = Engine(law)
            outputs = [engine.step(state) for state in (left, right)]
            differences = int(np.sum(outputs[0].b[list(ROLES["carrier"])] !=
                                     outputs[1].b[list(ROLES["carrier"])]))
            assert differences == (2 if coupled else 0)
            assert all(engine.inverse_step(after).same_as(before)
                       for before, after in zip((left, right), outputs))
            interventions.append({"direction": list(direction), "coupled": coupled,
                                  "complete_initial_carriers_equal": True,
                                  "future_carrier_component_differences": differences,
                                  "equal_initial_packet_energy": True,
                                  "equal_initial_momentum": False})
    report["matched_record_interventions"] = interventions
    if out is not None:
        path = Path(out); path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(exact_json.dumps(report, sort_keys=True)+"\n")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("runs/local_unification/native.json"))
    args = parser.parse_args(argv)
    report = audit(args.out)
    print(exact_json.dumps({k: report[k] for k in ("channels", "complete_transitions", "integer_comparisons")}))


if __name__ == "__main__":
    main()
