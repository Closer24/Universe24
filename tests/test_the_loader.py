"""The loader on the family-less universe file (the owner's word of 2026-10-24, "declaring a family is forbidden; they must emerge by themselves at the click"; ALGEBRA.md, A family's declaration, The circle of den; ENGINE.md section 4): a universe of den, the clock, the unit and the volume's gap alone loads, its rows derived from den (the massless point on one real line, the sign holder and the volume holder by their roles, every point of den's circle a plane named by its exponent vector), a file carrying a family row is refused by name with the derivation's sentence, the labels read from the integers meet the former names at the file's den, and every other refusal of the loader's own functions stands by name."""

import json

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.loader import circle, keys, universe
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, load_file, refused, universe_beside, universe_copy

ONE_UNIVERSE = EVENTS / "universe24" / "universe_universe24.json"  # the one universe file
DEN = 53_567_765  # nature's den of the one universe file, 5 x 17 x 73 x 89 x 97
TOP = 1_166_991_900_949_580_266_237  # the constants hand's three-prime den, 649,421 x 13,586,597 x 132,260,701
PEV = 21_397_363_965_165_989_151_899_244_775_347_635_252_768_274_397  # the record's den since 2026-10-24


def test_the_loader_refuses_every_wrong_key_of_the_files_by_name():
    """Every refusal of the loader's own functions, by name and with no world run: the keys (an object, an unknown key, a lacking key, an integer's bounds, a Node's form, a repository path with no file), the gone key `families` with the derivation's sentence, an unknown key among the integers, a lacking integer, the gap no key of the file, and the width and the Link unit the engine's, refused by name."""
    document, shape = universe_copy(), (4, 2, 1)
    integers = document["integers"]
    refusals = [
        ("must be an object", lambda: keys.keyed(3, "k", ("a",), ())),
        ("unknown key 'b'", lambda: keys.keyed({"b": 1}, "k", ("a",), ())),
        ("lacks the key 'a'", lambda: keys.keyed({}, "k", ("a",), ("a",))),
        ("integer from 1 through 3", lambda: keys.integer(4, "n", 1, 3)),
        (r"must be a Node \[x, y, z\]", lambda: keys.node_of([1, 2], "node", shape)),
        ("no file stands at that repository path", lambda: keys.document_at({}, "u.json", "u")),
        (
            "the universe file holds the key 'families', a declaration no file carries: the families are no "
            "rows of the file",
            lambda: universe.universe_of(
                {**document, "families": [{"name": "a", "pair": [2, 3], "dimension": 1}]}
            ),
        ),
        (
            "the universe file holds the unknown key 'reads'",
            lambda: universe.universe_of({**document, "reads": 1}),
        ),
        (
            "integers holds the unknown key 'act'",
            lambda: universe.universe_of({"integers": {**integers, "act": 1}}),
        ),
        (
            "integers lacks the key 'den'",
            lambda: universe.universe_of(
                {"integers": {k: v for k, v in integers.items() if k != "den"}}
            ),
        ),
        (
            "integers holds the unknown key 'volume_gap'",
            lambda: universe.universe_of({"integers": {**integers, "volume_gap": 6}}),
        ),  # the gapped volume holder by name, no integer of the file
        (
            "the key 'link_unit', an integer of the engine and not of the universe",
            lambda: universe.universe_of({"integers": {**integers, "link_unit": 16}}),
        ),
        (
            "the key 'width', an integer of the engine and not of the universe",
            lambda: universe.universe_of({"integers": {**integers, "width": 92}}),
        ),
    ]
    for match, call in refusals:
        refused(match, call)
    for key in universe.GONE:
        assert "2026-10-24" in universe.GONE[key] and "kept by name" in universe.GONE[key]


def test_dens_circle_is_read_from_its_integers_alone():
    """The circle of den (loader/circle.py): den factored, its primes 1 mod 4 split as two squares, every point of the open quadrant a product of their Gaussian primes labelled by its exponent vector, 3^n - 1 points for n primes once each; at the file's den the least leg is the former electron's pair and the former proton's pair is the vector (-2, 0, 0, 0, 2), the file's gravity pair a point too; at the three-prime den the former electron and proton are the lifts of the two heavier primes; the vector -v the point with the legs swapped; den's part outside the primes 1 mod 4 carries no angle (den 6,000: six points of the prime 5's angle, scale 48)."""
    assert circle.factors(DEN) == {5: 1, 17: 1, 73: 1, 89: 1, 97: 1}
    assert circle.factors(6000) == {2: 4, 3: 1, 5: 3} and circle.factors(1) == {}
    assert circle.is_prime(1021) and not circle.is_prime(1105) and circle.is_prime(132_260_701)
    assert circle.gaussian_of(5) == (2, 1) and circle.gaussian_of(1021) == (30, 11)
    points = circle.circle_points(DEN)
    assert len(points) == 3**5 - 1 and len({vector for vector, _n, _s in points}) == len(points)
    by_pair = {(num, sine): vector for vector, num, sine in points}
    for _vector, num, sine in points:
        assert num > 0 and sine > 0 and num * num + sine * sine == DEN * DEN
        assert by_pair[(sine, num)] == tuple(-step for step in by_pair[(num, sine)])
    least = min(points, key=lambda point: point[2])
    assert least[1:] == (53_567_757, 29_276) and circle.label_of(least[0]) == "point 2 -2 -2 2 -2"
    assert by_pair[(4_859_756, 53_346_867)] == (-2, 0, 0, 0, 2)  # the former proton's pair
    assert by_pair[(53_529_741, 2_017_988)] == (2, -2, 2, -2, 0)  # the former gravity pair
    assert by_pair[(32_140_659, 42_854_212)] == (
        2,
        0,
        0,
        0,
        0,
    )  # the former matter pair, the prime 5's lift
    assert circle.vector_of(circle.label_of((-2, 0, 0, 0, 2))) == (-2, 0, 0, 0, 2)
    assert circle.vector_of("massless") is None and circle.vector_of("point x") is None
    assert circle.angled(6000) == ([(5, 3)], 48)
    small = {circle.label_of(v): (n, s) for v, n, s in circle.circle_points(6000)}
    assert small == {
        "point -6": (5616, 2112),
        "point -4": (1680, 5760),
        "point -2": (4800, 3600),
        "point 2": (3600, 4800),
        "point 4": (5760, 1680),
        "point 6": (2112, 5616),
    }
    assert circle.circle_points(12) == []  # no prime 1 mod 4: no point, no plane row
    top = {(num, sine): vector for vector, num, sine in circle.circle_points(TOP)}
    assert len(top) == 3**3 - 1 and circle.factors(TOP) == {649_421: 1, 13_586_597: 1, 132_260_701: 1}
    assert top[(1_166_991_729_163_826_857_995, 633_202_287_062_780_012)] == (0, 2, 0)  # the least leg
    assert top[(100_503_613_922_092_705_013, 1_162_656_062_845_119_254_100)] == (0, 0, 2)
    assert (
        circle.factors(1021) == {1021: 1}
        and circle.factors(PEV)
        == {
            8_909_066_857_637: 1,
            79_961_009_336_473: 1,
            30_036_532_038_439_967_297: 1,
        }
    )  # Brent's cycle (2026-10-24): the same factors as Floyd's split found on SMALL, the top tier and the PeV den
    one = json.loads(
        ONE_UNIVERSE.read_text(encoding="utf-8")
    )  # the one test that factors the shipped den (2026-10-24): its rows and its own numbers here
    assert set(one) == {"integers"} and set(one["integers"]) == {"den", "node_clock", "quantum_action"}
    assert (
        one["integers"]["den"] == PEV
    )  # the PeV tier since 2026-10-24, the den chosen after the clicks
    shipped, planes = universe.universe_of(one)
    assert len(planes) == 3 + 3**3 - 1 and planes[0].pair == (PEV, PEV) and shipped["den"] == PEV
    least = min((f for f in planes if f.plane), key=lambda f: f.pair[1] ** 2 - f.pair[0] ** 2)
    assert (least.name, least.pair) == (
        "point 0 0 2",
        (21_397_363_965_165_989_150_474_488_818_982_086_595_722_885_795, PEV),
    )  # the electron, the least leg, the heaviest prime's lift at this den (point 0 2 0 at the top tier)
    proton = next(f for f in planes if f.name == "point 2 0 0")
    assert proton.pair == (
        21_397_363_965_161_185_649_061_722_838_116_504_985_189_627_435,
        PEV,
    )  # the proton, the lightest prime's lift, s_p / s_e = 1836.15265582 (point 0 0 2 at the top tier)
    legs = [circle.largest_below(PEV * PEV - f.pair[0] ** 2) for f in (proton, least)]  # s_p and s_e
    assert legs == [
        14_337_524_090_452_503_379_101_009_450_350_924_059_372,
        7_808_459_740_549_578_735_922_594_780_248_829_328,
    ]
    assert (
        1_492_403 * legs[0] <= PEV < 1_492_404 * legs[0]
    )  # den over the proton's leg, the massless point's wall over the proton's
    assert PEV == 8_909_066_857_637 * 79_961_009_336_473 * 30_036_532_038_439_967_297  # the PeV tier
    assert circle.lightest_point(PEV) == (least.pair[0], legs[1])  # the lightest point, the least leg
    captions = load_file("captions_for_the_loader", ROOT / "tools" / "look" / "captions.py")
    header = {
        "seed": "massless",
        "primes": sorted(circle.factors(PEV).items()),
        "points": {circle.label_of(v): [n, s] for v, n, s in circle.circle_points(PEV)},
    }
    assert captions.captions_for(header) == {
        "massless": "light",
        "point 0 0 2": "electron",
        "point 2 0 0": "proton",
        "point 0 2 0": "neutron",
    }  # the pages' captions at this den, the prime lifts named by rising sine (tools/look/captions.py)


def test_the_rows_are_derived_from_den_and_the_one_file_loads():
    """The rows at load from den (loader/universe.rows_of): the volume holder and the sign holder by their roles, both at the massless point (den, den), the gap gone for good (the gapped holder the former record's form, by name); then the massless point on one real line, the seed; every point of the circle a plane row named by its vector, reading the volume and the sign; the one universe file loads with its 26 planes at the three-prime den and no family row."""
    integers, families = universe.universe_of(universe_copy())
    names = [family.name for family in families]
    assert names[:3] == [universe.VOLUME, universe.SIGN, universe.MASSLESS] and len(names) == 3 + 6
    volume, sign, massless = families[:3]
    assert (massless.pair, massless.lines, massless.plane, massless.held) == (
        (6000, 6000),
        1,
        False,
        False,
    )
    assert sign.held and sign.wronskian and sign.rotation and sign.pair == (6000, 6000)
    assert (
        (sign.width, sign.records) == (4, 1 + 2 * 6)
    )  # the time line and three odd lines per row, two rows per plane (the list's two children, 2026-10-24) and the free row
    assert volume.held and not volume.wronskian and not volume.rotation and volume.pair == (6000, 6000)
    for plane in families[3:]:
        assert (
            plane.plane
            and plane.width == 2
            and plane.records == 2
            and not plane.held
            and plane.pair[1] == 6000
        )  # two lines per record, two records (the list's children, 2026-10-24)
        assert sorted(read.family for read in plane.reads) == [0, 1]  # the volume and the sign
        assert circle.vector_of(plane.name) is not None
    assert [read.family for read in massless.reads] == [0] and sign.reads == ()
    assert (sign.write_weight, sign.write_wall) == (
        2048,
        375,
    )  # alpha = T / Gamma reduced by 16, inside the write


def test_the_loader_refuses_a_massless_family_on_a_box_periodic_on_three_even_axes(
    tmp_path, monkeypatch
):
    """The board against the massless row's second double root (`loader/world.even_box_refused`; the mathematician's reading of the shelved ion's refusal): on the tests' universe, whose volume holder is its first massless row, a box periodic on three even axes is refused by name with the family and the shape, an odd extent admitted; the torus's former face keys refused as unknown (2026-10-24)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    universe_beside(tmp_path, den=1021)  # the two-point den: six loads under the width's derivation
    world = dict(intervals=1, universe="u.json")

    def written(name, **changes):
        (path := tmp_path / f"{name}.json").write_text(
            json.dumps({**world, **changes}), encoding="utf-8"
        )
        return path

    refusal = str(refused("staggered mode", load_world, written("even", shape=[4, 4, 2])))
    assert (
        f"'{universe.VOLUME}'" in refusal and "[4, 4, 2]" in refusal and "odd extent" in refusal
    )  # the first massless row, the volume holder
    assert Lattice(load_world(written("odd", shape=[4, 4, 3]))).shape == (4, 4, 3)
    for key in (
        "boundary",
        "face_depth",
        "faces",
        "receding",
    ):  # the torus is the one board (2026-10-24)
        refused(f"unknown key '{key}'", load_world, written(key, shape=[4, 4, 3], **{key: {}}))


def test_a_file_integer_of_310_bits_loads_and_a_big_dens_turned_room_is_exact():
    """The den enlarged as content (2026-10-24, the builder's two findings): a file's integer is bounded by no number of the tool's, Python's integers (the bound 2^512 gone 2026-10-24), and not the host's 63 bits (`keys.FILE_INTEGER`; a den of 70 bits at the top tier), and plane.turned_room's arrivals at that den are exact in Python's integers, the room beyond 2^63, read against the pairs by hand."""
    from event_universe.core.ports import LINK_UNIT
    from event_universe.plane import link_wall, sign_pairs, turned_room

    big = 2**310 - 1
    assert keys.integer(big, "n", 1) == big and keys.integer(2**513, "n", 1) == 2**513
    refused("integer from 1 through 3", keys.integer, 4, "n", 1, 3)
    pair, gamma, square = (1_166_991_729_163_826_857_995, TOP), 1000, LINK_UNIT * LINK_UNIT
    by_hand = max(
        abs(int(even[0])) + abs(int(odd[0]))
        for n in range(link_wall(gamma) + 1)
        for even, odd in [sign_pairs(pair, gamma, (square,), (n,))]
    )
    assert turned_room(pair, gamma, LINK_UNIT) == by_hand + 1 > 2**63
