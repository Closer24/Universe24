"""The toy worlds of the tests re-declared under the content (the reader's ruling of 2026-10-20, section H (1)): the born universe's holders of the content prepended to a toy universe, the deleted declarations inlined, the ion-like box; shared by the tests as tests/laws.py is."""

import json
from pathlib import Path

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader.world import TORUS  # the board without `boundary`, the torus (2026-10-23)
from event_universe.world_files import load_world
from tests.laws import EMIT_RUN, EVENTS, TOOL, redeclared, world_beside

ION_UNIVERSE = {
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {"name": "ion", "pair": [1, 1299], "dimension": [3, 2], "reads": {}},
        {
            "name": "strong_drive",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1},
            "reads": {},
        },
        {
            "name": "weak_drive",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1},
            "reads": {},
        },
        {
            "name": "fluorescence",
            "pair": [6000, 6000],
            "held": {"sources": ["wronskian"], "level_weight": 1},
            "reads": {},
        },
    ],
}


def ion_universe_beside(folder: Path, content: bool = True) -> None:
    """The ion-like universe written beside a world as u.json (the shelved ion's, inlined 2026-10-20 when its folder left with the toy atom worlds): four families, the ion of dimension [3, 2] and three drives held by the Wronskian at the level weight 1; with `content` (the default, the reader's ruling of 2026-10-20) the holders of the born universe's content prepended and every family reading them (`with_content`), so that the ion's reads carry their draws' totals and the box needs a sink; without, no holder of the content, the exact vacuum, where a periodic box needs no sink and the ion's draws are refused by name."""
    universe = with_content(ION_UNIVERSE) if content else ION_UNIVERSE
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(json.dumps(universe), encoding="utf-8")


def ion_world(  # type: ignore[no-untyped-def]
    folder: Path,
    tool,
    intervals: int = 23,
    amplitude: int = 600,
    body: bool = True,
    content: bool = True,
    counter: bool = True,
) -> Path:
    """The ion-like world on a box of 8 by 6 by 5 (one odd extent, so that the staggered mode (-1)^(x + y + z + t), the band's top, is no exact mode of the board): the three-part ion over two Nodes with its transition at [2, 3] from the strong drive and its emission to the fluorescence at the lifetime 8, the drive a plane wave along x at `amplitude`, the counter the plane x = 0 with the world's draw at the window 18 (dropped with `counter` False), every draw the click's read of the board; the telegraph's shape, its mode file written by the generator; without the ion (`body` False) the drive and the counter alone as beam_alone.json, the twin of the undepleted beam. With `content` (the default; re-pinned 2026-10-20 under the content of the born universe) the universe carries the content's holders, the box is opened along x as the content's sink and the ion's window is the drive's passage derived at load, 21; without, the periodic box at the exact vacuum with the ion's window declared, 1."""
    ion_universe_beside(folder, content)
    shape = (8, 6, 5)
    at, beside = [3, 3, 2], [4, 3, 2]
    parts = [{"part": k, "name": n, "count": int(k == 0)} for k, n in enumerate("SPD")]
    draw = {}  # the window derived (the owner's decision of 2026-10-23)
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
    if content:  # the faces along x the content's sink
        world.setdefault("boundary", dict(TORUS))["x"], world["face_depth"] = "open", 1
    world.update(universe="u.json", bodies=[record] if body else [], packets=[drive])
    world["node_detectors"] = [{"name": "counter", "positions": plane}] if counter else []
    if counter:
        world["draw"] = {}  # the regions' window derived
    (path := folder / ("ion_like.json" if body else "beam_alone.json")).write_text(json.dumps(world))
    tool.main(["--input", str(path)])
    return path


CONTENT_HOLDERS = [  # the content of the born universe (bell_singlet/born.json, pair.json): the holders of the content
    f
    for f in json.loads((EVENTS / "pair.json").read_text(encoding="utf-8"))["families"]
    if f["name"] in ("gravity", "binding")
]


TWO_ATOMS = json.loads((EVENTS / "anticoincidence" / "two_atoms.json").read_text(encoding="utf-8"))
RESONANT = json.loads((EVENTS / "resonance" / "resonant.json").read_text(encoding="utf-8"))


ZENO_ATOM = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
ZENO_1 = {
    "shape": [8, 8, 5],
    "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    "intervals": 48,
    "universe": "examples/events/zeno/zeno_atom.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [4, 4, 2], "weight": 1}, {"node": [5, 4, 2], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
                {"from": "e", "to": "g", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
            ],
            "rates": [],
            "node_detector": {},
        }
    ],
    "packets": [
        {
            "family": "pulse",
            "along": "x",
            "wave": [1, 2],
            "phase": [0, 1],
            "amplitude": 392,
            "top": {"x": [0, 7], "y": [0, 7], "z": [0, 4]},
            "edge": {"x": 0, "y": 0, "z": 0},
        }
    ],
    "node_detectors": [],
}  # the deleted zeno world's declaration, inlined 2026-10-20
ZENO_2 = {
    "shape": [8, 8, 5],
    "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    "intervals": 48,
    "universe": "examples/events/zeno/zeno_atom.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [4, 4, 2], "weight": 1}, {"node": [5, 4, 2], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
                {"from": "e", "to": "g", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
            ],
            "rates": [],
            "node_detector": {},
        }
    ],
    "packets": [
        {
            "family": "pulse",
            "along": "x",
            "wave": [1, 2],
            "phase": [0, 1],
            "amplitude": 392,
            "top": {"x": [0, 7], "y": [0, 7], "z": [0, 4]},
            "edge": {"x": 0, "y": 0, "z": 0},
        }
    ],
    "node_detectors": [],
}  # the deleted zeno world's declaration, inlined 2026-10-20
ZENO_4 = {
    "shape": [8, 8, 5],
    "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
    "intervals": 48,
    "universe": "examples/events/zeno/zeno_atom.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [4, 4, 2], "weight": 1}, {"node": [5, 4, 2], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
                {"from": "e", "to": "g", "drive": "pulse", "weight": 1, "resonance": [2, 3]},
            ],
            "rates": [],
            "node_detector": {},
        }
    ],
    "packets": [
        {
            "family": "pulse",
            "along": "x",
            "wave": [1, 2],
            "phase": [0, 1],
            "amplitude": 392,
            "top": {"x": [0, 7], "y": [0, 7], "z": [0, 4]},
            "edge": {"x": 0, "y": 0, "z": 0},
        }
    ],
    "node_detectors": [],
}  # the deleted zeno world's declaration, inlined 2026-10-20
TWO_PHOTONS = {
    "shape": [96, 1, 1],
    "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
    "face_depth": 1,
    "intervals": 170,
    "universe": "examples/events/anticoincidence/two_atoms_two_records.json",
    "bodies": [
        {
            "family": "atom",
            "nodes": [{"node": [23, 0, 0], "weight": 1}, {"node": [24, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]},
                {"from": "g", "to": "e", "drive": "photon_b", "weight": 6, "resonance": [5414, 6000]},
            ],
            "rates": [],
            "node_detector": {},
        },
        {
            "family": "atom",
            "nodes": [{"node": [71, 0, 0], "weight": 1}, {"node": [72, 0, 0], "weight": 1}],
            "parts": [{"part": 0, "name": "g", "count": 1}, {"part": 1, "name": "e", "count": 0}],
            "transitions": [
                {"from": "g", "to": "e", "drive": "photon", "weight": 6, "resonance": [5414, 6000]},
                {"from": "g", "to": "e", "drive": "photon_b", "weight": 6, "resonance": [5414, 6000]},
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
            "amplitude": 110,
            "top": {"x": [48, 48], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
        {
            "family": "photon_b",
            "along": "x",
            "wave": [-1, 4],
            "phase": [0, 1],
            "amplitude": 110,
            "top": {"x": [47, 47], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": 8, "y": 0, "z": 0},
        },
    ],
    "node_detectors": [],
    "receding": {"x": {"sides": ["low", "high"], "largest": 400, "layers": 16}},
}  # the deleted anticoincidence world's two photons, inlined 2026-10-20
TWO_RECORDS = {
    "integers": {"node_clock": 6000, "quantum_action": 32768, "width": 63, "link_unit": 16},
    "families": [
        {"name": "atom", "pair": [1, 1299], "dimension": [2, 2], "reads": {}},
        {"name": "photon", "pair": [6000, 6000], "dimension": 1, "reads": {}},
        {"name": "photon_b", "pair": [6000, 6000], "dimension": 1, "reads": {}},
    ],
}  # the two photons' universe
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


def opened(world):  # type: ignore[no-untyped-def]
    """A periodic box under the content gets its sink: the faces along x open (the axis the light travels in the toy worlds), the loader deriving the windows where the lays then have an end."""
    world.setdefault("boundary", dict(TORUS))["x"], world["face_depth"] = "open", 1
    for body in world.get("bodies", []):
        if isinstance(body.get("node_detector"), dict):
            body["node_detector"].pop("window", None)
    return world


def content_world(tmp_path, name, document, universe, edit=None, content=True):  # type: ignore[no-untyped-def]
    """A toy world beside tmp_path under the content: the universe with the content written as u.json, the document in the read's shape with its universe u.json and `edit` applied, the generator laying its packets (tools/pixel_mode.py) where it has any; the repository root pointed at tmp_path (the conftest restores it); the world's path. With `content` False the universe stands as given (a load with no run, or the exact vacuum by name)."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "u.json").write_text(
        json.dumps(with_content(universe) if content else universe), encoding="utf-8"
    )
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


def emit_and_take_world(tmp_path, emitter_nodes, taker_nodes):  # type: ignore[no-untyped-def]
    """The resonance world rewritten beside tmp_path under the content of the born universe (re-pinned 2026-10-20): body 0 the emitter on `emitter_nodes` (excited, [2, 3], lifetime 48), body 1 the taker on `taker_nodes` (ground), EMIT_RUN intervals; the universe gains the holders of the content (`with_content`), the box opens along x with its faces as the content's sink, and the windows are derived at load (the lays have an end, the declared key refused), 48 for both. The emitter's quantum, drawn within its span, leaves by the faces before any close of the taker reads it (the reader's and G's measurement of 2026-10-20: the taker's closes to 400 take nothing, the light's share a small fraction of one unit at 400), so no sentence of a take reads on this world; a sentence of a take reads on the shipped chain world (examples/events/chain/chain_x_minus.json), and the ring's sentences stand by name (`ring_of`)."""

    def edit(world):  # type: ignore[no-untyped-def]
        world["intervals"] = EMIT_RUN
        world["bodies"][0]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in emitter_nodes]
        world["bodies"][1]["nodes"] = [{"node": [x, 0, 0], "weight": 1} for x in taker_nodes]
        for body in world["bodies"]:  # the window derived at load on the opened box, the key refused
            body["node_detector"].pop("window", None)
        world.setdefault("boundary", dict(TORUS))["x"], world["face_depth"] = (
            "open",
            1,
        )  # the faces the content's sink

    path = world_beside(tmp_path, EVENTS / "resonance" / "resonant.json", edit)
    universe = json.loads((EVENTS / "zeno" / "zeno_atom.json").read_text(encoding="utf-8"))
    (tmp_path / "examples" / "events" / "zeno" / "zeno_atom.json").write_text(
        json.dumps(with_content(universe)), encoding="utf-8"
    )
    return path


def ring_of(path: Path, window: int = 48) -> Path:
    """The emit-and-take world at `path` re-declared as the periodic chain it was (x periodic, no face, the windows declared at `window`, the key required where a source in time on a ring has no end): under the content the law refuses it at the start by name, the held sums' rest needing a sink, so the ring's sentences (the null window on the body's own circulating train, C5's reach where the lay has no end) are not read under the content and stand by name with their pins as history (the reader's ruling of 2026-10-20); the ring's path."""
    world = json.loads(path.read_text(encoding="utf-8"))
    world.setdefault("boundary", dict(TORUS))["x"] = "periodic"
    world.pop("face_depth", None)
    for body in world["bodies"]:
        body["node_detector"].pop("window", None)  # the window derived, the key refused (2026-10-23)
    (ring := path.with_name("ring.json")).write_text(json.dumps(world), encoding="utf-8")
    return ring
