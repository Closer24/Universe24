"""Matter's birth from light, the gapless meeting's own clause (the law's sentence on the owner's word of 2026-10-23; `conversion.birth_of`, `act.born_pair`), on the small structured board of the universe test with the matter universe's families (gravity gapped [990, 1000], the holder of the sign, matter [600, 1000] as one clump, light uniform, the proton [0, 1000] and the electron [800, 1000] as planes, and the clicks world's absorber at [2, 2, 2] reading the light at its own beat 15): at the absorber's emission back into the light (e to g at the interval 45, the window's third close) the emitted light quantum arrives at a Node where the uniform light's quantum already stands, is not written there, and in place of the books' deficit the two quanta make the lightest conjugate pair the universe declares, the electron at the senses -1 and 1 (3,600 T against the two light quanta's 6,000 T), laid at that Node as two items of the same write step: the clauses (1) one birth line at 45, the family light, the children electron and electron at the senses -1 and 1 summing to 0, at [2, 2, 2]; (2) the electron's record stands on the board after it (its quanta at the Node and over the board at least one) where none stood before, the books' count of the electron 2 and of the light 26 as read (the births counted in the children and not in the light); (3) the run back of the whole course is exact through the birth, 70 of 70 states (the lay logged at its interval and undone, The lay's inverse); (4) the books' deficits as read and not assumed: the light's 1 from the take at the absorber's Node at 15 (the undepleted beam, standing as before the sentence) and the electron's -1, the conjugate pair's share at one Node reading one quantum against the books' two, named for the reading of the pair's share; the rest 0."""

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import input_digest, load_world
from tests.laws import ROOT, board_state, same_state
from tests.laws_universe import CLUMP, CUBE, GAMMA, GAP, NOW, flat

MATTER = ROOT / "examples" / "events" / "universe24" / "universe_universe24_matter.json"
ABSORBER = [2, 2, 2]
MATTER_COUNT = 429  # the gate's count of the clump's share at [600, 1000] on the 3-cube at T 36,000
END = 70


def birth_board(folder: Path) -> Path:
    universe = json.loads(MATTER.read_text(encoding="utf-8"))
    universe["families"][0]["pair"] = [GAP, GAMMA]
    universe["families"].append(
        {"name": "absorber", "pair": [666, GAMMA], "reads": {"gravity": 1}, "dimension": [2, 2]}
    )
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")
    nodes = [[x, y, z] for x in range(CUBE) for y in range(CUBE) for z in range(CUBE)]
    world: dict[str, object] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "intervals": 200,
        "universe": "u.json",
        "bodies": [
            {"family": "matter", "nodes": [{"node": CLUMP, "count": MATTER_COUNT}]},
            {
                "family": "light",
                "nodes": [{"node": n, "count": 1} for n in nodes if n not in (CLUMP, ABSORBER)],
            },
            {
                "family": "absorber",
                "nodes": [{"node": ABSORBER, "weight": 1}],
                "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
                "transitions": [
                    {
                        "from": "g",
                        "to": "e",
                        "drive": "light",
                        "weight": [23, 2],
                        "resonance": [902, GAMMA],
                    }
                ],
                "rates": [{"from": "e", "to": "g", "lifetime": 24, "gives_to": "light"}],
                "node_detector": {},
            },
        ],
        "node_detectors": [],
    }
    at = lambda node: (node[0] * CUBE + node[1]) * CUBE + node[2]  # noqa: E731
    levels = lambda node, now: [now if i == at(node) else 0 for i in range(CUBE**3)]  # noqa: E731
    mode = {
        "world_digest": input_digest(world),
        "bodies": [
            {
                "family": "matter",
                "pair": [600, GAMMA],
                "moving": {"now": levels(CLUMP, NOW), "before": levels(CLUMP, round(NOW * 0.6))},
            },
            {
                "family": "light",
                "pair": [GAMMA, GAMMA],
                "moving": {"now": [636] * CUBE**3, "before": [446] * CUBE**3},
            },
        ],
        "packets": [],
    }
    path = folder / "birth.json"
    path.write_text(json.dumps(world), encoding="utf-8")
    path.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    return path


def test_the_emitted_light_quantum_meeting_the_standing_one_births_the_electron_pair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(birth_board(tmp_path)), output=lines.append)
    names = [family.name for family in board.families]
    electron = names.index("electron")
    at = (ABSORBER[0] * CUBE + ABSORBER[1]) * CUBE + ABSORBER[2]
    assert int(sum(flat(board.quanta(electron)[0]))) == 0  # no electron stands at the start
    states = {0: board_state(board)}
    for t in range(1, END + 1):
        board.step()
        states[t] = board_state(board)
    births = [line for line in lines if line.get("event") == "birth"]
    assert [(b["interval"], b["family"], b["children"], b["senses"], b["nodes"]) for b in births] == [
        (45, "light", ["electron", "electron"], [-1, 1], [ABSORBER])
    ]  # (1) one birth, the conjugate electron pair at the absorber's Node, the senses summing to 0
    credits = [
        (int(c["interval"]), str(c["before"]) + ">" + str(c["realised"]))
        for c in lines
        if c.get("event") == "credit" and c.get("before") != c.get("realised")
    ]
    assert credits[:2] == [
        (15, "g>e"),
        (45, "e>g"),
    ]  # the absorption and the emission the birth rides on
    quanta = np.asarray(board.quanta(electron)[0], dtype=object).reshape(-1)
    assert (
        int(quanta[at]) >= 1 and int(quanta.sum()) >= 1
    )  # (2) the electron's record stands where it was born
    books = board.books()
    assert (
        books["electron"]["count"] == 2 and books["light"]["count"] == 26
    )  # the births counted in the children, the light's count as read
    assert books["light"]["deficit"] == 1 and books["electron"]["deficit"] == -1, (
        books
    )  # (4) as read: the take's deficit at 15, the pair's share one against the books' two
    assert all(books[name]["deficit"] == 0 for name in ("matter", "proton", "charge", "absorber")), books
    back = 0
    for k in range(END):  # (3) the run back exact through the birth
        board.step_inverse()
        back += same_state(board_state(board), states[END - 1 - k])
    assert back == END
