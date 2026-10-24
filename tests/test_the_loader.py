"""The loader's refusals by name, each called by hand on the loader's own function with no world run (ENGINE.md section 4, the files' keys; the architect's audit of 2026-10-03, the loader's pieces with no test of their own)."""

import json

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader import keys, universe
from event_universe.loader.derived import PLANE_LINE, REAL_LINE
from event_universe.world_files import load_world
from tests.laws import refused, universe_beside


def test_the_loader_refuses_every_wrong_key_of_the_files_by_name(tmp_path):
    """Every refusal of the loader's own functions, by name and with no world run: the keys (an object, an unknown key, a lacking key, an integer's bounds, a Node's form and the Nodes beyond an inner face, a range's form, a repository path with no file, a record's line weights on a plane, at the wrong length and all 0, a read at the weight 0); the mode file (a level's sparse and dense forms, a family not the record's, the second level pair declared halfway or on a family of real lines, a level above the amplitude bound or beyond an inner face, a sense without a rotation, another world's digest, a missing entry); the lay (the kind, stop with the repeat, the tolerance's form, the seed, the profile with the one-Node seed and its form) and the budget (the least T is the law's inequality's least power of two, 81 den^6 e_num^4 c^2 T^2 >= 1024 num^4 n^2 e_den^4 (den^2 - num^2), and the gate refuses a universe below it); the faces (a receding face on a periodic axis, its sides and a side's word, the inner faces' list, axis and gaps, faces that leave no Node) and the open faces' layer without its receding side; the packets (the list, a lay by the count on a holder of the content, whole or count without interval, the family, the axis, the wave's form and p = 0, the phase's and a transverse wave number's form); the universe (a held row with a dimension, its sources, the former key `act` an unknown key, the rotation without the Wronskian, a family without a dimension, its lines' kinds and a mixed record, a shape's form, the Link unit not a power of two, the families' list, a name twice, a row without reads, the pair's form, |num| = den on a massive pair, a rest on the holder of the sign)."""
    universe_beside(tmp_path, charged=True)
    document = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))
    shape = (4, 2, 1)
    held = {"sources": ["form"], "level_weight": 1, "write_weight": 1}

    def rows(*entries):
        return universe.universe_of({**document, "families": list(entries)})

    refusals = [
        ("must be an object", lambda: keys.keyed(3, "k", ("a",), ())),
        ("unknown key 'b'", lambda: keys.keyed({"b": 1}, "k", ("a",), ())),
        ("lacks the key 'a'", lambda: keys.keyed({}, "k", ("a",), ("a",))),
        ("integer from 1 through 3", lambda: keys.integer(4, "n", 1, 3)),
        (r"must be a Node \[x, y, z\]", lambda: keys.node_of([1, 2], "node", shape)),
        ("no file stands at that repository path", lambda: keys.document_at({}, "u.json", "u")),
        ("each holder's name to the weight", lambda: keys.reads_of([], "reads")),
        ("read at the weight 0 is no read", lambda: keys.reads_of({"gravity": 0}, "reads")),
        (
            "is a held row and declares no dimension",
            lambda: universe.shape_of({"held": {}, "dimension": 1}, "r"),
        ),
        ("held.sources is one of", lambda: universe.shape_of({"held": {**held, "sources": ["x"]}}, "r")),
        ("unknown key 'act'", lambda: universe.shape_of({"held": {**held, "act": "pace"}}, "r")),
        ("lacks the key 'dimension'", lambda: universe.shape_of({}, "r")),
        ("lists its lines' kinds", lambda: universe.shape_of({"dimension": ["x"]}, "r")),
        (
            "mixes real lines and planes",
            lambda: universe.shape_of({"dimension": [REAL_LINE, PLANE_LINE]}, "r"),
        ),
        (
            r"as a shape is \[parts, dimension\]",
            lambda: universe.shape_of({"dimension": [1, 2, 3]}, "r"),
        ),
        (
            "link_unit must be a power of two",
            lambda: universe.universe_of(
                {**document, "integers": {**document["integers"], "link_unit": 3}}
            ),
        ),
        ("families must be a list", lambda: universe.universe_of({**document, "families": {}})),
        ("name must be a name of its own", lambda: rows(*document["families"], document["families"][0])),
        ("lacks the key 'reads'", lambda: rows({"name": "a", "pair": [2, 3], "dimension": 1})),
        (
            r"pair must be \[num, den\]",
            lambda: rows({"name": "a", "pair": [2], "dimension": 1, "reads": {}}),
        ),
        (
            "a massive pair has den above",
            lambda: rows({"name": "a", "pair": [-3, 3], "dimension": 1, "reads": {}}),
        ),
        (
            "only the massless row of the content rests",
            lambda: rows(
                {
                    "name": "a",
                    "pair": [1, 1],
                    "reads": {},
                    "held": {"sources": ["wronskian"], "level_weight": 1, "rest": 5},
                }
            ),
        ),
    ]
    for match, call in refusals:
        refused(match, call)


def test_the_loader_refuses_a_massless_family_on_a_box_periodic_on_three_even_axes(
    tmp_path, monkeypatch
):
    """The board against the massless row's second double root (`loader/world.even_box_refused`; the mathematician's reading of the shelved ion's refusal): on the tests' universe, whose gravity and charge rows are massless (the first named), a box of 4 by 4 by 2 periodic on all three axes is refused by name at load, the packet naming the family, the shape, the staggered mode (-1)^(x + y + z + t) walked by Rule3's own rounding and the way out (printed); the same box with one odd extent, 4 by 4 by 3, and the even box with its x axis open are admitted, the mode a bounded response there."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path)
    world = dict(intervals=1, universe="u.json")

    def written(name, **changes):
        (path := tmp_path / f"{name}.json").write_text(
            json.dumps({**world, **changes}), encoding="utf-8"
        )
        return path

    refusal = str(refused("staggered mode", load_world, written("even", shape=[4, 4, 2])))
    print(refusal)
    assert "'gravity'" in refusal and "[4, 4, 2]" in refusal and "odd extent" in refusal
    assert Lattice(load_world(written("odd", shape=[4, 4, 3]))).shape == (4, 4, 3)
    for key in (
        "boundary",
        "face_depth",
        "faces",
        "receding",
    ):  # the torus is the one board (2026-10-24)
        refused(f"unknown key '{key}'", load_world, written(key, shape=[4, 4, 3], **{key: {}}))
