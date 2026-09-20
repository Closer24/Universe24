"""The gate between records and the pair at N = 1024 and 4096 under the
amplitude law (`amplitude-v1`, the model owner, 2026-09-20; the design,
docs/designs/amplitude-v1/DESIGN.md section 10 and its `gate.py`, section 4.3 and
`bell.py`; docs/BEAM_LAW.md note 37), on the worlds of series L5 and L6
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`gate` and `pair_n`, the design's reading written before the runs). The
expected integers of docs/TEST_EXPECTATIONS.md ("The amplitude law: the
gate"), written down before the first run:

(a) the Hadamard and the CNOT on the GameBoard (`cnot_pair_0_8`): the
    Hadamard re-emitter turns the control's row into two rows on the label
    bit 0, amounts 181 (C'[16] of the 128 tables) at the phases u and
    u + 32, the multiplicity 65536 (the `rotate` line); at the gate the
    control (the record 2^32 + 1, the survivor) and the target join: the
    `gate` line names the survivor, the joined record, the labels
    [[0, 1], [3, 1]] and 2 arms; after it the control's rows on +y carry
    the labels 0 (amount 181, phase u) and 3 (181, u + 32) with the
    multiplicity 65536 and the target's rows on -y the labels 0 and 3 with
    the amount 1 and the multiplicity 2: the design's |00> - |11>;
(b) the pair by the gate at the CHSH labels with Bob at -b: E x 64 = 44,
    -44, 44, 44 over the 64 births, S = 176/64, the marginals 32/64;
(c) CNOT twice (`cnot_twice`): after the second gate the rows carry the
    labels 0 and 1 on both arms (the target's bit cleared: H|0> x |0>
    again), the amounts 181, 181 and 1, 1; every record gathers at the
    absorber;
(d) GHZ by one gate of three parties (`cnot_ghz_*`): the allowed triples
    ++-, +-+, -++, --- on XXX (the product -1, this convention's H) and
    +++, +--, -+-, --+ on XYY, YXY, YYX (+1), 16 births each; the `gate`
    line's labels [[0, 1], [7, 1]], 3 arms, 6 rows (at most n x 2^n = 24
    after n = 3 records joined; the pair's 4 at most 8);
(e) the register's ceiling: `rotations_3` runs (the rows' multiplicity
    2^48 at the absorber, 64 gathers) and `rotations_4` is refused at load,
    the multiplicity through its re-emitters 2^64 beyond 2^62 - 1, naming
    the fourth rotation's Node (8, 0, 0) (the review's S6):
    Grover's six rotations are not a world of the GameBoard, as the design's
    section 10 states;
(f) the refusals: `rotate` and `gate` without the key and on `measure`; a
    gate kind other than cnot; `hold` not a boolean; `parties` 0; a
    rotation's bit beyond 31; at N = 4096 the half-angle entry of an odd
    setting refused and of the setting 512 the 4096 table's at 256;
(g) the pair at N = 1024 (`bell_n1024_*`, one birth per u): the cells'
    counts the reading's, E x 1024 = 724, -724, 724, 724, S = 2896/1024
    (the design's), |E - cos| <= 1/N on every pair;
(h) the pair at N = 4096 (`bell_n4096_0_512`, 4096 births): the counts the
    reading's, E x 4096 = 2900 where the exact cosine gives 2896.3: the
    tables' rounding (entries in 1/256) exceeds 1/N at this N, so the
    design's bound |E - cos| <= 1/N is pinned as the design's value and
    marked failing; S = 11584/4096 = 2.828125, below 2 sqrt 2;
(i) the review of (v), B1: the units the gate's copies add are booked on
    the layer's live count (the `gate` line's `added`, 1 on `cnot_pair_0_8`:
    the target's row of amount 1 into two), so every gathered record of
    the world ends at live 0, none at -1;
(j) the review's B2: a record that reaches a gate with an offer already
    made or with units elsewhere is refused naming the record, the units
    and the sets (`cnot_pair_0_8` with the control's path split (1, 1) at
    (6, 5) between the Hadamard and the gate, the second output into an
    absorber reading `sum`: the lazy relabelling of the design's section
    10 is not built);
(k) the review's S1 and B3: the control is the record whose rows arrive
    on the entry's declared `control` direction, read from the rows
    pending alone: `cnot_pair_0_8` with its `measured` list reversed gives
    the same multiset of outcomes over the run (E x 64 = 44 either way);
(l) the refusals of the control: a gate of two parties without `control`;
    a gate of one party with one; a control direction no record arrives
    on (refused at the gate naming the count of control records).
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from collections import Counter
from pathlib import Path

import pytest

from event_universe.core.phase import phase_cosines, phase_sines
from event_universe.events import NatureBeamSimulation, parse_nature_beam_world
from event_universe.events.amplitude import half_angle

ROOT = Path(__file__).resolve().parents[1]
N = 64


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
GATE = EXPECTATIONS["gate"]
PAIR_N = EXPECTATIONS["pair_n"]
FIRST = (1 << 32) + 1


def run(
    world: dict[str, object], ticks: int | None = None
) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"]) if ticks is None else ticks):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def gathers_of(simulation: NatureBeamSimulation, births: int = N) -> list[dict[str, object]]:
    """The gathers of the first `births` records of the lamp of number 1
    (by the record's ordinal: a lamp's clock skips a step now and then as
    the births spend its content, so a birth is not one per tick)."""
    assert simulation.layer is not None
    found = [g for g in simulation.layer.gathers if int(g["record"]) <= FIRST - 1 + births]  # type: ignore[call-overload]
    assert len(found) == births
    return found


def outcome(gather: dict[str, object]) -> str:
    return "".join(str(item[2]) for item in gather["chosen"])  # type: ignore[union-attr]


def counts_of(gathers: list[dict[str, object]]) -> dict[str, int]:
    return dict(Counter(outcome(g) for g in gathers))


def correlation(counts: dict[str, int]) -> int:
    return sum(v if k[-2] == k[-1] else -v for k, v in counts.items())


def rows_of(simulation: NatureBeamSimulation, record: int) -> list[tuple[object, ...]]:
    vectors = simulation.world.directions
    return sorted(
        (
            tuple(vectors[r.direction]),
            r.branch >> 32,
            r.branch & 0xFFFFFFFF,
            r.amount,
            r.phase,
            r.multiplicity,
        )
        for r in simulation.stores[0].rows()
        if r.record == record
    )


def test_the_hadamard_and_the_cnot_on_the_game_board():
    """(a)."""
    world = GENERATOR.cnot_pair("probe", 0, 8)
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    gate_line = None
    while gate_line is None:
        simulation.step()
        gate_line = next(
            (line for line in lines if line.get("event") == "gate" and line["survivor"] == FIRST), None
        )
        assert simulation.tick < 40
    rotate = next(line for line in lines if line.get("event") == "rotate")
    assert rotate["setting"] == 16 and rotate["bit"] == 0 and rotate["rows"] == 2
    assert gate_line["kind"] == "cnot" and gate_line["arms"] == 2 and gate_line["rows"] == 4
    assert gate_line["labels"] == [[0, 1], [3, 1]]
    assert len(gate_line["joined"]) == 1 and gate_line["joined"][0] >> 32 == 4  # type: ignore[index]
    c = phase_cosines(2 * N)[16]
    assert c == 181 == phase_sines(2 * N)[16]
    assert rows_of(simulation, FIRST) == [
        ((0, -1, 0), 1, 0, 1, 0, 2),
        ((0, -1, 0), 1, 3, 1, 0, 2),
        ((0, 1, 0), 0, 0, c, 0, 65536),
        ((0, 1, 0), 0, 3, c, 32, 65536),
    ]
    assert GATE["pair"] == {"00": [3036676096, 0], "11": [-3036676096, 0]}


def test_the_pair_by_the_gate_at_the_chsh_labels():
    """(b)."""
    correlations: dict[str, int] = {}
    for a, b in GENERATOR.CHSH:
        simulation, _ = run(GENERATOR.gate_worlds()[f"cnot_pair_{a}_{b}"])
        counts = counts_of(gathers_of(simulation))
        assert counts == GATE["chsh"][f"{a}_{b}"]["counts"], (a, b)
        correlations[f"{a}_{b}"] = correlation(counts)
        assert sum(v for k, v in counts.items() if k[0] == "+") == N // 2
    assert correlations == {"0_8": 44, "0_24": -44, "16_8": 44, "16_24": 44}
    assert (
        correlations["0_8"] - correlations["0_24"] + correlations["16_8"] + correlations["16_24"]
        == GATE["chsh_S"]
        == 176
    )


def test_cnot_twice_is_the_identity():
    """(c)."""
    world = GENERATOR.gate_worlds()["cnot_twice"]
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    second = None
    while second is None:
        simulation.step()
        gates = [line for line in lines if line.get("event") == "gate" and line["survivor"] == FIRST]
        second = gates[1] if len(gates) == 3 else None
        assert simulation.tick < 60
    assert [g["joined"] for g in gates[1:]] == [[], []]
    assert [g["labels"] for g in gates[1:]] == [[[0, 1], [1, 1]]] * 2
    assert {g["node"][0] for g in gates[1:]} == {11, 8}
    c = phase_cosines(2 * N)[16]
    assert rows_of(simulation, FIRST) == [
        ((0, 1, 0), 0, 0, c, 0, 65536),
        ((0, 1, 0), 0, 1, c, 32, 65536),
        ((0, 1, 0), 1, 0, 1, 0, 2),
        ((0, 1, 0), 1, 1, 1, 0, 2),
    ]
    assert GATE["twice"] is True
    finished, _ = run(world)
    assert len(gathers_of(finished)) == N


def test_ghz_by_one_gate_of_three_parties():
    """(d)."""
    for basis in GENERATOR.GATE_BASES:
        expected = GATE["ghz"][basis.lower()]
        simulation, lines = run(GENERATOR.gate_worlds()[f"cnot_ghz_{basis.lower()}"])
        counts = counts_of(gathers_of(simulation))
        assert counts == expected["counts"], basis
        assert sorted({1 if k.count("-") % 2 == 0 else -1 for k in counts}) == expected["products"]
        gate_line = next(line for line in lines if line.get("event") == "gate")
        assert gate_line["labels"] == [[0, 1], [7, 1]] and gate_line["arms"] == 3
        assert gate_line["rows"] == 6 <= 3 * 2**3
    assert GATE["ghz"]["xxx"]["products"] == [-1]
    assert all(GATE["ghz"][k]["products"] == [1] for k in ("xyy", "yxy", "yyx"))


def test_the_register_ceiling_of_the_rotations():
    """(e)."""
    simulation, lines = run(GENERATOR.gate_worlds()["rotations_3"])
    assert len(gathers_of(simulation)) == N
    click = next(
        line for line in lines if line.get("event") == "click" and line.get("detector") == "end"
    )
    assert click["multiplicity"] == 65536**3 == 1 << 48
    assert GATE["rotations_within_bound"] == 3
    with pytest.raises(
        ValueError, match=r"reaches 18446744073709551616 at measured\[4\] at \[8, 0, 0\]"
    ):
        parse_nature_beam_world(GENERATOR.gate_worlds()["rotations_4"])


def test_the_copies_of_the_gate_are_booked_on_the_live_count():
    """(i)."""
    simulation, lines = run(GENERATOR.gate_worlds()["cnot_pair_0_8"])
    assert simulation.layer is not None
    gathered = [live for live in simulation.layer.records.values() if live.gathered]
    assert len(gathered) >= N and all(live.live == 0 for live in gathered)
    gates = [line for line in lines if line.get("event") == "gate"]
    assert gates and all(line["added"] == 1 for line in gates)


def prior_offer_world() -> dict[str, object]:
    """The review's B2 world: the control's path split (1, 1) between the
    Hadamard and the gate, one output into an absorber reading `sum`."""
    world = GENERATOR.cnot_pair("prior", 0, 8)
    measured = world["measured"]
    assert isinstance(measured, list)
    measured.insert(
        2,
        {
            "position": [6, 5, 0],
            "family": "light",
            "amount": 1,
            "fixed": True,
            "table": {"light": {"rule": "rerelease", "inputs": [[1, 0, 0]], "weights": [[1, 1]]}},
            "directions": [[1, 0, 0], [0, -1, 0]],
        },
    )
    measured.append({"position": [6, 3, 0], "family": "counter", "amount": 1, "fixed": True})
    detectors = world["detectors"]
    assert isinstance(detectors, list)
    detectors.append({"name": "absorber", "positions": [[6, 3, 0]], "reading": "sum"})
    return world


def test_a_record_with_an_offer_or_units_elsewhere_is_refused_at_the_gate():
    """(j)."""
    simulation = NatureBeamSimulation(parse_nature_beam_world(prior_offer_world()))
    with pytest.raises(ValueError, match=r"record 4294967297 reaches the gate with .* elsewhere"):
        for _ in range(40):
            simulation.step()
    assert simulation.tick < 40


def test_the_control_is_the_declared_arrival_and_not_the_declaration_order():
    """(k)."""
    world = GENERATOR.cnot_pair("order", 0, 8)
    reversed_world = dict(world)
    measured = world["measured"]
    assert isinstance(measured, list)
    reversed_world["measured"] = list(reversed(measured))
    outcomes = []
    for candidate in (world, reversed_world):
        simulation, _ = run(candidate)
        assert simulation.layer is not None
        outcomes.append(Counter(outcome(g) for g in simulation.layer.gathers))
    assert outcomes[0] == outcomes[1] and correlation(dict(outcomes[0])) > 0


def test_the_refusals_of_the_control():
    """(l)."""
    world = GENERATOR.cnot_pair("control", 0, 8)
    measured = world["measured"]
    assert isinstance(measured, list)
    gate = measured[2]["table"]["light"]["gate"]  # type: ignore[index]
    assert gate["control"] == [1, 0, 0]
    without = json.loads(json.dumps(world))
    del without["measured"][2]["table"]["light"]["gate"]["control"]
    with pytest.raises(ValueError, match=r"gate of 2 parties declares its control"):
        parse_nature_beam_world(without)
    one = json.loads(json.dumps(world))
    one["measured"][2]["table"]["light"]["gate"]["parties"] = 1
    with pytest.raises(ValueError, match=r"a gate of one party has no control"):
        parse_nature_beam_world(one)
    nobody = json.loads(json.dumps(world))
    nobody["measured"][2]["table"]["light"]["gate"]["control"] = [0, 1, 0]
    simulation = NatureBeamSimulation(parse_nature_beam_world(nobody))
    with pytest.raises(ValueError, match=r"finds 0 records arriving on its control direction"):
        for _ in range(40):
            simulation.step()


def test_the_refusals_of_the_gate_keys():
    """(f)."""

    def entry(**keys: object) -> dict[str, object]:
        world = GENERATOR.cnot_pair("refusals", 0, 8)
        measured = world["measured"]
        assert isinstance(measured, list)
        measured[1]["table"]["light"] = {"rule": "rerelease", **keys}
        return world

    with pytest.raises(ValueError, match=r"\.rotate belongs to a `rerelease` entry, not to measure"):
        parse_nature_beam_world(entry(rule="measure", rotate={"setting": 16}))
    with pytest.raises(ValueError, match=r"\.gate belongs to a `rerelease` entry, not to measure"):
        parse_nature_beam_world(entry(rule="measure", gate={"kind": "cnot"}))
    with pytest.raises(ValueError, match=r"\.gate\.kind must be one of \['cnot'\]"):
        parse_nature_beam_world(entry(gate={"kind": "swap"}))
    with pytest.raises(ValueError, match=r"\.gate\.hold must be true or false"):
        parse_nature_beam_world(entry(gate={"kind": "cnot", "hold": 1}))
    with pytest.raises(ValueError, match=r"\.gate\.parties must be an integer from 1"):
        parse_nature_beam_world(entry(gate={"kind": "cnot", "parties": 0}))
    with pytest.raises(ValueError, match=r"\.rotate\.bit must be an integer from 0 through 31"):
        parse_nature_beam_world(entry(rotate={"setting": 16, "bit": 32}))
    assert parse_nature_beam_world(entry(rotate={"setting": 16, "bit": 1, "turn": 3})).measured[
        1
    ].rotations[0] == GENERATOR_ROTATION(16, 1, 3)
    with pytest.raises(ValueError, match=r"setting 1 has no half-angle entry at N = 65536"):
        half_angle(1, 65536)
    assert half_angle(1, 4096) == (phase_cosines(8192)[1], phase_sines(8192)[1])
    assert half_angle(512, 4096) == (phase_cosines(8192)[512], phase_sines(8192)[512])
    assert half_angle(1024, 65536) == (phase_cosines(65536)[512], phase_sines(65536)[512])
    assert half_angle(16, N) == (181, 181)


def GENERATOR_ROTATION(setting: int, bit: int, turn: int):
    from event_universe.events.world import Rotation

    return Rotation(setting, bit, turn)


def test_the_pair_at_n_1024():
    """(g)."""
    n = 1024
    expected = PAIR_N[str(n)]
    correlations: list[int] = []
    for a, b in GENERATOR.chsh_labels(n):
        simulation, _ = run(GENERATOR.pair_n_worlds()[f"bell_n{n}_{a}_{b}"])
        counts = counts_of(gathers_of(simulation, n))
        assert counts == expected["pairs"][f"{a}_{b}"]["counts"], (a, b)
        e = correlation(counts)
        correlations.append(e)
        assert e == expected["pairs"][f"{a}_{b}"]["E"]
        assert abs(e / n - math.cos(2 * math.pi * (a - b) / n)) <= 1 / n
    assert correlations == [724, -724, 724, 724]
    assert correlations[0] - correlations[1] + correlations[2] + correlations[3] == expected["S"] == 2896
    assert PAIR_N["design_S_1024"] == 2896


def test_the_pair_at_n_4096():
    """(h)."""
    n = 4096
    expected = PAIR_N[str(n)]
    simulation, _ = run(GENERATOR.pair_n_worlds()[f"bell_n{n}_0_512"])
    counts = counts_of(gathers_of(simulation, n))
    assert counts == expected["pairs"]["0_512"]["counts"]
    assert correlation(counts) == expected["pairs"]["0_512"]["E"] == 2900
    assert expected["S"] == 11584 and 11584 / 4096 < 2 * math.sqrt(2)
    assert [v["E"] for v in expected["pairs"].values()] == [2900, -2900, 2892, 2892]


@pytest.mark.xfail(
    strict=True,
    reason="the design's bound |E - cos| <= 1/N at N = 4096: the tables' entries in 1/256 "
    "round E by more than 1/4096 (2900/4096 against the cosine's 2896.3/4096)",
)
def test_the_bound_on_e_at_n_4096():
    """(h), the design's value pinned."""
    n = 4096
    for key, row in PAIR_N[str(n)]["pairs"].items():
        a, b = (int(part) for part in key.split("_"))
        assert abs(row["E"] / n - math.cos(2 * math.pi * (a - b) / n)) <= 1 / n
