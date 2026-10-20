"""The toy worlds of the tests re-declared under the content (the reader's ruling of 2026-10-20, section H (1)): the born universe's holders of the content prepended to a toy universe, the deleted declarations inlined, the ion-like box; shared by the tests as tests/laws.py is."""

import json
from pathlib import Path

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import EMIT_RUN, EVENTS, TOOL, redeclared, world_beside

ION_UNIVERSE = {
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {"name": "ion", "pair": [1, 1299], "dimension": [3, 2], "reads": {}},
        {
            "name": "strong_drive",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1, "act": "rotation", "write_weight": 1},
            "reads": {},
        },
        {
            "name": "weak_drive",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1, "act": "rotation", "write_weight": 1},
            "reads": {},
        },
        {
            "name": "fluorescence",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1, "act": "rotation", "write_weight": 1},
            "reads": {},
        },
    ],
}


def ion_universe_beside(folder: Path) -> None:
    """The ion-like universe written beside a world as u.json (the shelved ion's, inlined 2026-10-20 when its folder left with the toy atom worlds): four families, the ion of dimension [3, 2] and three drives held by the Wronskian at the level weight 1, no holder of the content, so a periodic box needs no sink."""
    (folder / "u.json").write_text(json.dumps(ION_UNIVERSE), encoding="utf-8")


def ion_world(folder: Path, tool, intervals: int = 23, amplitude: int = 600, body: bool = True) -> Path:  # type: ignore[no-untyped-def]
    """The ion-like world on a periodic box of 8 by 6 by 5 (one odd extent, so that the staggered mode (-1)^(x + y + z + t), the band's top, is no exact mode of the board): the three-part ion over two Nodes with its transition at [2, 3] from the strong drive and its emission to the fluorescence at the lifetime 8, the drive a plane wave along x at `amplitude`, the counter the plane x = 0 with the world's draw at the window 18, every draw the click's read of the board; the telegraph's shape, its mode file written by the generator; without the ion (`body` False) the drive and the counter alone as beam_alone.json, the twin of the undepleted beam."""
    ion_universe_beside(folder)
    shape = (8, 6, 5)
    at, beside = [3, 3, 2], [4, 3, 2]
    parts = [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {"window": 1}
    nodes = [{"node": at, "weight": 1}, {"node": beside, "weight": 1}]
    record = {"family": "ion", "nodes": nodes, "parts": parts, "node_detector": draw}
    record["transitions"] = [
        {"from": "S", "to": "P", "drive": "strong_drive", "weight": 1, "resonance": [2, 3]}
    ]
    record["rates"] = [{"from": "P", "to": "S", "lifetime": 8, "gives_to": "fluorescence"}]
    drive = {
        "family": "strong_drive",
        "along": "x",
        "wave": [1, 2],
        "phase": [0, 1],
        "amplitude": amplitude,
    }
    top = {axis: [0, extent - 1] for axis, extent in zip("xyz", shape, strict=True)}
    drive.update(top=top, edge={"x": 0, "y": 0, "z": 0})
    plane = [[0, y, z] for y in range(shape[1]) for z in range(shape[2])]
    world = dict(
        shape=list(shape), boundary=dict(x="periodic", y="periodic", z="periodic"), intervals=intervals
    )
    world.update(universe="u.json", bodies=[record] if body else [], packets=[drive])
    world.update(node_detectors=[{"name": "counter", "positions": plane}], draw={"window": 18})
    (path := folder / ("ion_like.json" if body else "beam_alone.json")).write_text(json.dumps(world))
    tool.main(["--input", str(path)])
    return path


CONTENT_HOLDERS = [  # the content of the born universe (bell_singlet/born.json, pair.json): the holders of the content
    f
    for f in json.loads((EVENTS / "pair.json").read_text(encoding="utf-8"))["families"]
    if f["name"] in ("gravity", "binding")
]


TWO_ATOMS = json.loads((EVENTS / "anticoincidence" / "two_atoms.json").read_text(encoding="utf-8"))


ONE_PHOTON = {
    "shape": [96, 1, 1],
    "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
    "face_depth": 1,
    "intervals": 170,
    "universe": "examples/events/anticoincidence/two_atoms.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [23, 0, 0], "weight": 1}, {"node": [24, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]}
            ],
            "rates": [],
            "node_detector": {},
        },
        {
            "family": "atom",
            "nodes": [{"node": [71, 0, 0], "weight": 1}, {"node": [72, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]}
            ],
            "rates": [],
            "node_detector": {},
        },
    ],
    "packets": [
        {
            "family": "photon",
            "along": "x",
            "wave": [1, 4],
            "phase": [0, 1],
            "amplitude": 78,
            "top": {"x": [48, 48], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
        {
            "family": "photon",
            "along": "x",
            "wave": [-1, 4],
            "phase": [0, 1],
            "amplitude": 78,
            "top": {"x": [47, 47], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
    ],
    "node_detectors": [],
    "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
}  # the deleted anticoincidence world's one photon, inlined 2026-10-20


def with_content(universe):  # type: ignore[no-untyped-def]
    """A toy universe re-declared with the vacuum content (the reader's ruling of 2026-10-20, section H (1); G's probe): the born universe's holders gravity and binding prepended as they stand in pair.json, every toy family reading them at 1, so that light's remainders walk on w div F = 108,000,000 and a body's read carries its draw's total."""
    families = [
        {**f, "reads": {**f.get("reads", {}), "gravity": 1, "binding": 1}} for f in universe["families"]
    ]
    return {**universe, "families": CONTENT_HOLDERS + families}


def content_world(tmp_path, name, document, universe, edit=None):  # type: ignore[no-untyped-def]
    """A toy world beside tmp_path under the content: the universe with the content written as u.json, the document in the read's shape with its universe u.json and `edit` applied, the generator laying its packets (tools/pixel_mode.py) where it has any; the repository root pointed at tmp_path (the conftest restores it); the world's path."""
    (tmp_path / "u.json").write_text(json.dumps(with_content(universe)), encoding="utf-8")
    world = {**redeclared(json.loads(json.dumps(document))), "universe": "u.json"}
    if edit is not None:
        edit(world)
    (path := tmp_path / f"{name}.json").write_text(json.dumps(world), encoding="utf-8")
    world_files.REPOSITORY_ROOT = tmp_path
    if world.get("packets"):
        TOOL.main(["--input", str(path)])
    return path


def one_photon_board(tmp_path, draw: bool = True):  # type: ignore[no-untyped-def]
    """The one-photon world (`ONE_PHOTON`, the deleted anticoincidence world's declaration) under the content on the two atoms' universe (`content_world`, re-pinned 2026-10-20 under the content of the born universe), its output lines collected; with `draw` False the twin without the detector's draw, transitions and rates (the parts alone)."""

    def twin(world):  # type: ignore[no-untyped-def]
        for body in world["bodies"]:  # the parts alone: no draw, no transition, no rate
            body.pop("node_detector"), body.pop("transitions"), body.pop("rates")

    path = content_world(tmp_path, "one_photon", ONE_PHOTON, TWO_ATOMS, None if draw else twin)
    return Lattice(load_world(path), (lines := []).append), lines


def emit_and_take_world(tmp_path, emitter_nodes, taker_nodes, window=61):  # type: ignore[no-untyped-def]
    """The resonance world rewritten beside tmp_path under the content of the born universe (`with_content`, re-pinned 2026-10-20; the box open on x with its faces, the content's sink): body 0 the emitter on `emitter_nodes` (excited, [2, 3], lifetime 48, its window `window`, 61 by default: in the exact dark its emission falls at its window's close, `meeting.emission_fell`), body 1 the taker on `taker_nodes` (ground, window 48), 200 intervals on the periodic chain of 48."""

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = EMIT_RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in emitter_nodes]
        world["bodies"][1]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in taker_nodes]
        world["bodies"][0]["node_detector"]["window"] = window
        world["bodies"][1]["node_detector"]["window"] = 48
        world["boundary"]["x"], world["face_depth"] = (
            "open",
            1,
        )  # the content needs a sink: the faces open along x

    path = world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    (tmp_path / "examples" / "events" / "zeno" / "zeno_atom.json").write_text(
        json.dumps(with_content(universe)), encoding="utf-8"
    )  # the content
    return path
