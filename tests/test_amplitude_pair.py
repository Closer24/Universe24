"""The pair, the which-path world, no maintenance and GHZ under the
amplitude law (`amplitude-v1`, the model owner, 2026-09-20; the design,
docs/designs/amplitude-v1/DESIGN.md section 4 and its `bell.py`;
docs/BEAM_LAW.md note 37), on the worlds of series L3 and L4
(`examples/events/amplitude/make_worlds.py`, `expectations.json` under
`pair` and `ghz`, the design's reading written before the runs). The
expected integers of docs/TEST_EXPECTATIONS.md ("The amplitude law: the
pair"), written down before the first run:

(a) the birth of a pair: on `bell_0_8` the lamp births at tick 1 the
    record 2^32 + 1 of four rows of amount 1 and multiplicity 2 at
    (10, 0, 0), the labels 0 and 3 on arm 0 (-x, Alice) and on arm 1
    (+x, Bob), the branch arm x 2^32 + label; the `birth` line carries the
    labels [[0, 1], [3, 1]], 2 arms, 4 units, the multiplicity 2;
(b) the design's test 4 at the CHSH labels: over the lamp's first 64
    records (by birth ordinal, the record's identity: born in the ticks
    1 .. 65 since the fraction-free law of 2026-09-20, the exact clock of
    the paid lamp stalling once at tick 3; a tick window is not a count
    of births, and S does not depend on the alignment) the cells
    (oA, oB) of `bell_0_8` count 27, 5, 5, 27 (E x 64 = 44), `bell_0_24`
    5, 27, 27, 5 (-44), `bell_16_8` and `bell_16_24` 27, 5, 5, 27 (44),
    S = 176/64; Alice's outcome is + for u < 32 and - for u >= 32 on every
    world (the marginal 32/64 exact, both parties); every gather names the
    settings of its two clicks (`windows` [alice_plus, a, 0], [bob_plus,
    b, 0]); the counters alice_minus and bob_minus receive nothing;
(c) the design's test 4 with the choosers (`bell_choosers`, the 960
    records from the 7th, born at tick 8, when the choosers' rows have
    reached both counters; the 6 born before (the ticks 1, 2, 4, 5, 6, 7:
    the exact clock's one stall at tick 3) click at alice_minus, the first
    counter the chooser's rows reach; the bins are read by record, and
    each holds every u once whatever the alignment of the births with the
    streams): the gathers grouped by the settings give the 15
    pairs (0, 12, 25, 38, 51) x (8, 29, 51), 64 records each with every
    u, the counts per pair the reading's and E x 64 = 44, -60, 20, 60, -8,
    -48, -8, 60, -52, -64, 40, 20, -28, -36, 64 in that order; every
    marginal 32/64; S on the registered quadruple (0, 25) x (8, 29) is
    156/64 (2 exactly under the window gate, the register's A2);
(d) the design's test 6, the which-path worlds (`path_*`, a `read` of the
    counter family on Alice's arm reading `sum`): the cells are (label,
    oA, oB), eight per record; E x 64 = 44, -44, 0, 0 and S = 88/64;
(e) the design's test 9, no maintenance (`bell_16_24_far`,
    `path_16_24_far`, Bob's counters 116 Links farther): E x 64 = 44 and 0
    as at the CHSH labels, every record gathering after Bob's rows flew
    at least 200 intervals;
(f) the design's test 5, GHZ (`ghz_xxx` .. `ghz_yyy`): the allowed
    triples are +++, +--, -+-, --+ on XXX (the product +1) and ++-, +-+,
    -++, --- on XYY, YXY, YYX (the product -1), 16 births each, every
    other triple weight 0 (the gather's cells name every triple, the
    forbidden with the rung of the allowed before it); YYY allows all
    eight, 8 each;
(g) the refusals: `branches`, `arms` and an entry's `turn` without the
    key; `arms` not dividing the directions; a label at or above 2^arms; a
    label twice; a weight 0; `turn` on `pass` and beyond N - 1.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

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
PAIR = EXPECTATIONS["pair"]
WORLDS = GENERATOR.pair_worlds()


def run(world: dict[str, object]) -> tuple[NatureBeamSimulation, list[dict[str, object]]]:
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    for _ in range(int(world["ticks"])):  # type: ignore[call-overload]
        simulation.step()
    return simulation, lines


def gathers_of(
    simulation: NatureBeamSimulation, births: int = N, first: int = 1
) -> list[dict[str, object]]:
    """The gathers of the lamp's records of the birth ordinals first ..
    first + births - 1 (the record's identity, number 1's 2^32 + ordinal;
    since the fraction-free law of 2026-09-20 a paid lamp's exact clock
    stalls, so a tick window is not a count of births), in their order."""
    assert simulation.layer is not None
    base = 1 << 32
    found = sorted(
        (
            g
            for g in simulation.layer.gathers
            if base + first <= int(g["record"]) < base + first + births  # type: ignore[call-overload]
        ),
        key=lambda g: int(g["record"]),  # type: ignore[call-overload]
    )
    assert len(found) == births
    return found


def outcome(gather: dict[str, object]) -> str:
    """The chosen channels of the record's factors in the arms' order."""
    return "".join(str(item[2]) for item in gather["chosen"])  # type: ignore[union-attr]


def counts_of(gathers: list[dict[str, object]]) -> dict[str, int]:
    return dict(Counter(outcome(g) for g in gathers))


def correlation(counts: dict[str, int]) -> int:
    return sum(v if k[-2] == k[-1] else -v for k, v in counts.items())


def settings_of(gather: dict[str, object]) -> tuple[int, int]:
    windows = {str(name): int(setting) for name, setting, _ in gather["windows"]}  # type: ignore[union-attr]
    return windows["alice_plus"], windows["bob_plus"]


def test_the_birth_of_a_pair():
    """(a)."""
    world = WORLDS["bell_0_8"]
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(world), observer=lines.append)
    simulation.step()
    first = (1 << 32) + 1
    rows = sorted(
        (r.node, r.direction, r.amount, r.multiplicity, r.branch, r.phase)
        for r in simulation.stores[0].rows()
        if r.record == first
    )
    # The register's birth (`pair.birth`, `pair.labels`): one row per
    # (arm, label) at the lamp's Node, the branch arm x 2^32 + label.
    registered = PAIR["birth"]
    node = tuple(registered["node"])
    labels = [label for label, _ in PAIR["labels"]]
    directions = [
        simulation.world.directions.index(tuple(vector)) for vector in registered["arm_directions"]
    ]
    assert rows == sorted(
        (node, directions[arm], 1, registered["multiplicity"], (arm << 32) | label, 0)
        for arm in range(registered["arms"])
        for label in labels
    )
    birth = next(line for line in lines if line.get("event") == "birth")
    assert birth["record"] == first and birth["labels"] == PAIR["labels"]
    assert birth["arms"] == registered["arms"] and birth["units"] == registered["units"]
    assert birth["multiplicity"] == registered["multiplicity"]


def test_the_pair_at_the_chsh_labels():
    """(b)."""
    correlations: dict[str, int] = {}
    for a, b in GENERATOR.CHSH:
        name = f"bell_{a}_{b}"
        simulation, _ = run(WORLDS[name])
        gathers = gathers_of(simulation)
        counts = counts_of(gathers)
        assert counts == PAIR["chsh"][f"{a}_{b}"]["counts"], name
        correlations[name] = correlation(counts)
        assert correlations[name] == PAIR["chsh"][f"{a}_{b}"]["E"]
        for gather in gathers:
            assert gather["windows"] == [["alice_plus", a, 0], ["bob_plus", b, 0]]
            assert outcome(gather)[0] == ("+" if int(gather["u"]) < N // 2 else "-")  # type: ignore[call-overload]
        assert sum(v for k, v in counts.items() if k[1] == "+") == N // 2
        for detector in simulation.detectors():
            if detector["name"] in ("alice_minus", "bob_minus"):
                assert all(f["clicks"] == 0 for f in detector["families"].values()), name  # type: ignore[union-attr]
    s = (
        correlations["bell_0_8"]
        - correlations["bell_0_24"]
        + correlations["bell_16_8"]
        + correlations["bell_16_24"]
    )
    assert s == PAIR["chsh_S"]
    assert correlations == {f"bell_{key}": entry["E"] for key, entry in PAIR["chsh"].items()}


def test_the_pair_with_the_choosers_reads_the_registered_quadruple():
    """(c)."""
    simulation, _ = run(WORLDS["bell_choosers"])
    assert simulation.layer is not None
    # The records born before tick CHOOSERS_FIRST meet no setting at
    # Alice's plus counter and click at alice_minus: 6 records (the
    # lamp's exact clock stalls once, at tick 3, so the 7th record is born
    # at tick 8; 7 records in 7 ticks until the fraction-free law of
    # 2026-09-20); the 960 records from the next one, by ordinal, are
    # analysed.
    early = [g for g in simulation.layer.gathers if int(g["born"]) < GENERATOR.CHOOSERS_FIRST]  # type: ignore[call-overload]
    registered_early = PAIR["choosers_early"]
    assert len(early) == registered_early["count"]
    assert all(g["chosen"][0][0] == "alice_minus" for g in early)  # type: ignore[index]
    assert sorted(int(g["born"]) for g in early) == registered_early["born"]  # type: ignore[call-overload]
    gathers = gathers_of(simulation, GENERATOR.CHOOSERS_BIRTHS, len(early) + 1)
    by_settings: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for gather in gathers:
        by_settings[settings_of(gather)].append(gather)
    a_settings, b_settings = GENERATOR.CHOOSER_SETTINGS
    assert sorted(by_settings) == sorted((a, b) for a in a_settings for b in b_settings)
    correlations: dict[tuple[int, int], int] = {}
    for (a, b), found in by_settings.items():
        assert len(found) == N and sorted(int(g["u"]) for g in found) == list(range(N))  # type: ignore[call-overload]
        counts = counts_of(found)
        assert counts == PAIR["choosers"][f"{a}_{b}"]["counts"], (a, b)
        assert sum(v for k, v in counts.items() if k[0] == "+") == N // 2
        assert sum(v for k, v in counts.items() if k[1] == "+") == N // 2
        correlations[(a, b)] = correlation(counts)
    assert [correlations[(a, b)] for a in a_settings for b in b_settings] == [
        PAIR["choosers"][f"{a}_{b}"]["E"] for a in a_settings for b in b_settings
    ]
    (a1, a2), (b1, b2) = GENERATOR.REGISTERED_QUADRUPLE
    s = correlations[(a1, b1)] - correlations[(a1, b2)] + correlations[(a2, b1)] + correlations[(a2, b2)]
    assert s == PAIR["registered_S"] == 156


def test_the_which_path_read_makes_the_joint_a_product():
    """(d)."""
    correlations: dict[str, int] = {}
    for a, b in GENERATOR.CHSH:
        name = f"path_{a}_{b}"
        simulation, _ = run(WORLDS[name])
        gathers = gathers_of(simulation)
        assert all(len(g["cells"]) == 8 for g in gathers), name  # type: ignore[arg-type]
        counts = counts_of(gathers)
        assert counts == PAIR["which_path"][f"{a}_{b}"]["counts"], name
        correlations[name] = correlation(counts)
    assert [correlations[f"path_{a}_{b}"] for a, b in GENERATOR.CHSH] == [
        PAIR["which_path"][f"{a}_{b}"]["E"] for a, b in GENERATOR.CHSH
    ]
    s = (
        correlations["path_0_8"]
        - correlations["path_0_24"]
        + correlations["path_16_8"]
        + correlations["path_16_24"]
    )
    assert s == PAIR["which_path_S"]


def test_no_maintenance_over_a_long_flight():
    """(e)."""
    for name, expected in PAIR["far"].items():
        simulation, _ = run(WORLDS[f"{name}_far"])
        gathers = gathers_of(simulation)
        assert correlation(counts_of(gathers)) == expected, name
        flown = min(int(g["tick"]) - int(g["born"]) for g in gathers)  # type: ignore[call-overload]
        assert flown >= PAIR["far_min_flight"], name


def test_ghz_allows_four_triples_per_basis_with_the_products():
    """(f)."""
    for basis in GENERATOR.GHZ_BASES:
        expected = EXPECTATIONS["ghz"][basis.lower()]
        simulation, _ = run(WORLDS[f"ghz_{basis.lower()}"])
        gathers = gathers_of(simulation)
        counts = counts_of(gathers)
        assert counts == expected["counts"], basis
        assert sorted(counts) == expected["allowed"]
        products = sorted({1 if k.count("-") % 2 == 0 else -1 for k in counts})
        assert products == expected["products"]
        assert all(len(g["cells"]) == 8 for g in gathers)  # type: ignore[arg-type]
    assert EXPECTATIONS["ghz"]["xxx"]["products"] == [1]
    assert all(EXPECTATIONS["ghz"][k]["products"] == [-1] for k in ("xyy", "yxy", "yyx"))


def test_the_refusals_of_the_pair_keys():
    """(g)."""

    def lamp_world(amplitude: bool, **lamp: object) -> dict[str, object]:
        world = GENERATOR.bell("refusals", (0, 8))
        measured = world["measured"]
        assert isinstance(measured, list)
        measured[0]["lamp"] = {"rate": [1, 1], "directions": [[-1, 0, 0], [1, 0, 0]], **lamp}
        return world

    with pytest.raises(ValueError, match=r"lamp\.arms must be an integer from 1 through 2"):
        parse_nature_beam_world(lamp_world(True, arms=3))
    world = lamp_world(True, arms=2)
    measured = world["measured"]
    assert isinstance(measured, list)
    measured[0]["lamp"]["directions"] = [[-1, 0, 0], [1, 0, 0], [0, 1, 0]]
    with pytest.raises(ValueError, match=r"lamp\.arms 2 does not divide the 3 directions"):
        parse_nature_beam_world(world)
    with pytest.raises(ValueError, match=r"branches\[1\]\.label must be an integer from 0 through 3"):
        parse_nature_beam_world(lamp_world(True, arms=2, branches=[[0, 1], [4, 1]]))
    with pytest.raises(ValueError, match=r"branches names the label 3 twice"):
        parse_nature_beam_world(lamp_world(True, arms=2, branches=[[3, 1], [3, 1]]))
    with pytest.raises(ValueError, match=r"branches\[0\]\.weight must be an integer from 1"):
        parse_nature_beam_world(lamp_world(True, arms=2, branches=[[0, 0], [3, 1]]))
    keyed = lamp_world(True, arms=2, branches=[[0, 1], [3, 1]])
    measured = keyed["measured"]
    assert isinstance(measured, list)
    measured[1]["table"]["sa"] = {"rule": "pass", "turn": 1}
    with pytest.raises(ValueError, match=r"\.turn is refused on pass"):
        parse_nature_beam_world(keyed)
    measured[1]["table"]["sa"] = "pass"
    measured[1]["table"]["light"] = {"phase_window": 0, "turn": N}
    with pytest.raises(ValueError, match=r"\.turn must be an integer from 0 through 63"):
        parse_nature_beam_world(keyed)
    measured[1]["table"]["light"] = {"phase_window": 0, "turn": 16}
    assert parse_nature_beam_world(keyed).measured[1].label_turns[0] == 16
