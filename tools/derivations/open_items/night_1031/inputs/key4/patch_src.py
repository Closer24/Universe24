"""KEY4's change to node-all 9d75a4904's src, written into the copy (tree_key4/src, taken from tree_all/src): each edit an
exact text replacement whose count is asserted, so key4_src.diff is this script's work alone. Run: python3 -I
patch_src.py <tree_key4/src/tensor24>.
"""

import sys
from pathlib import Path

SRC = Path(sys.argv[1])

FILES = [
    (
        "Board: the three files read and checked, then laid out as the load's arrays; the universe's chosen block names the key, the push's switch and the five strengths (the notch, the hold, the held rows' own spring, the tie and the mesh), each CHOSEN by name, and nothing else is laid: no coupling, particle or mass.",
        "Board: the three files read and checked, then laid out as the load's arrays; the universe's chosen block names the push's switch and the five strengths (the notch, the hold, the held rows' own spring, the tie and the mesh), each CHOSEN by name; the setting, the world's initialization, lays its gears and its one key, the key's middle, once for the world (KEY4); and nothing else is laid: no coupling, particle or mass.",
    ),
    ("from tensor24.algebra.carry import carry\n", ""),
    (
        '    "couplings": "no file declares a coupling; the coupling family\'s one plan lays the terms at G3"\n}',
        '    "couplings": "no file declares a coupling; the coupling family\'s one plan lays the terms at G3",\n'
        '    "key": "the world\'s key is laid once, in the setting, as the key\'s middle (setting.middle); the node computes the"\n'
        '    " click\'s unit and every edge side\'s dial from it at the initialization (KEY4)",\n}',
    ),
    (
        "# the key odd: a pair's two click teeth, each born at (key - 1) div senses, sum to key - 1 only then, and with the\n"
        "# pair's S_L + S_M = 0 that forces q_L + q_M = 0 (NOT_CLOSED 11; the first hostile code reader's M6 and the second's 3:\n"
        "# with an even key the two sum to key - 2 and the pair's books miss)\n"
        "ODD = Rule(\n"
        "    lambda v: whole(v) and v >= 1 and carry(v, SENSES, 0)[1] == 1,\n"
        '    f"an odd whole number, a pair\'s two click teeth, each born at (key - 1) div {SENSES}, summing to key - 1",\n'
        ")\n",
        "# the world's one key as the initialization lays it, the key's middle, its own complement under the mirror (middle =\n"
        "# K - 1 - middle): the click's unit K = senses middle + 1, odd by construction, the senses read as the pair's two ends;\n"
        "# the node computes from it every edge side's dial D = (kappa div senses) K and its tooth's birth (D - 1) div senses at\n"
        "# the initialization, and the load refuses an even D by name (load.dialled), as a side's two teeth sum to D - 1 only\n"
        "# where D is odd, and with an edge's two passings P and -P that forces its two quotients to sum to 0 (NOT_CLOSED 11);\n"
        "# no parity is read here (KEY4)\n"
        "MIDDLE = Rule(\n"
        "    lambda v: whole(v) and v >= 0,\n"
        '    f"a whole number of at least 0, the key\'s middle laid once for the world, the click\'s unit {SENSES} middle + 1",\n'
        ")\n",
    ),
    (
        "    # the key, the push's switch and the five strengths, each CHOSEN by name: the whole click's key (G5; its value\n"
        "    # G3's), the metric's push on or off (term 5 claims no strength) and the volume's notch (G2), the held hand's tie,\n"
        "    # the held rows' own spring, the hands' tie and the gradient vertex through the Mesh (G3's frame)\n"
        '    "chosen": {\n'
        '        "key": ODD,\n',
        "    # the push's switch and the five strengths, each CHOSEN by name: the metric's push on or off (term 5 claims no\n"
        "    # strength) and the volume's notch (G2), the held hand's tie, the held rows' own spring, the hands' tie and the\n"
        "    # gradient vertex through the Mesh (G3's frame); the whole click's key left it for the setting (RETIRED, KEY4)\n"
        '    "chosen": {\n',
    ),
    (
        'SETTING = {"version": VERSIONED, "ticks": NONE_BELOW, "gears": GEAR}',
        'SETTING = {"version": VERSIONED, "ticks": NONE_BELOW, "middle": MIDDLE, "gears": GEAR}',
    ),
]

KEYED = '''# the fields a key is laid in: the setting's middle, and the retired key's own name
KEYED = ("key", "middle")


def keyed(universe: dict[str, Any], setting: dict[str, Any]) -> tuple[Any, list[str]]:
    """The load's promise on the key, read on the files as held: the world's one key is the setting's middle, the key's middle, a whole number of at least 0 (0 for the click's unit 1), laid once for the world; a middle laid as anything but one whole number (at a tooth or a site, as a list or rows) and every other field that lays a key in the universe or the setting, at any depth, are named, a second key each: a key varying across the clocks would lay a click-rate field, a dilation the initialization sets instead of the clocks showing it; a world that lays no key is named too, so that none falls silently to the unit."""
    laid: list[str] = []
    left: list[tuple[str, Any]] = [("universe", universe), ("setting", setting)]
    while left:
        where, held = left.pop()
        if isinstance(held, dict):
            laid += [f"{where}.{name}" for name in held if name in KEYED]
            left += [(f"{where}.{name}", value) for name, value in held.items()]
        elif isinstance(held, list):
            left += [(f"{where}[{at}]", value) for at, value in enumerate(held)]
    middle: Any = setting.get("middle")
    found = [
        f"{where}: a second key: the world's key is laid once, as the setting's middle"
        for where in sorted(laid)
        if where != "setting.middle"
    ]
    if "middle" not in setting:
        found.append(
            "setting.middle: no key laid: the world's key is laid once, as the key's middle, a whole number of at least"
            " 0 (0 for the click's unit 1)"
        )
    elif not (whole(middle) and middle >= 0):
        many = isinstance(middle, (list, dict))
        shown = f"a {type(middle).__name__} of {len(middle)}" if many else repr(middle)
        found.append(
            "setting.middle: one whole number of at least 0, laid once for the world and at no tooth or site,"
            f" not {shown}"
        )
    return middle, found


def dial(ends: Z, middle: Z) -> Z:
    """The click's unit K at the node's initialization from the world's one key: the key's middle is its own complement, middle = K - 1 - middle, so K = ends middle + 1, ends the pair's two ends (a quantum given at one, taken at the other), the two summing to K - 1; odd by construction, so no parity is read; the node's edge dials are its multiples (dialled)."""
    return ends * middle + 1


def dialled(key: Z, senses: Z, spare: Z) -> tuple[Z, list[str]]:
    """Every edge side's click tooth at its birth, (D - 1) div senses, D's own middle, and the load's promise on the edge dial D = (kappa div senses) K that edging lays, each departure named, so nothing is loaded: the scale whole, kappa over senses leaving no remainder (spare, edging's: a kappa off its form, as kappa + 1, leaves the scale as it was and its remainder alone, the ninth code reader's MINOR 6); and D odd, so that a side's two teeth born there sum to D - 1 and an edge's two quotients sum to 0 by the carry's law (NOT_CLOSED 11). K is odd for every middle, and D is odd for every middle while kappa div senses is, as on every plan laid today (kappa 2, or 6 where a tie's three legs lie on an edge; the hands' tie holds two); a monomial on an edge holding four legs makes kappa div senses 4 or 12, its weights quarters of kappa, and D even for every middle."""
    birth, half = carry(key - 1, senses, 0)
    pairs = zip(key.ravel().tolist(), half.ravel().tolist(), strict=True)
    even = sorted({int(d) for d, r in pairs if r})
    found: list[str] = []
    if spare:
        found.append(
            f"the edge dials' scale: kappa over senses leaves {spare}, so no dial and no Mesh edge's factor is"
            " kappa / two"
        )
    return birth, found + [
        f"the edge dial {d}: even, so a side's two click teeth born at (D - 1) div senses would sum to D - 2, not"
        " D - 1, and the edge's books would open (NOT_CLOSED 11); K being odd by construction, D = (kappa div senses) K"
        " is even only where kappa div senses is, as a monomial on an edge holding four legs makes it"
        for d in even
    ]


def load('''

LOAD = [
    (
        "the edge key the universe file's CHOSEN integer times kappa / two (runner/plans.py's edging), every side's click tooth born at (key - 1) div 2, the Spokes along one axis the divisor.",
        "the click's unit K the node's own at its initialization, senses middle + 1 from the setting's one middle (the key's middle, laid once for the world), the edge dial D = (kappa div senses) K (runner/plans.py's edging), every side's click tooth born at (D - 1) div senses, D's middle, a scale with a remainder and an even D refused by name, the Spokes along one axis the count, read as the pair's two ends.",
    ),
    (
        "from tensor24.runner.files import GEAR, entries, star, vocabulary\n",
        "from tensor24.runner.files import GEAR, entries, star, vocabulary, whole\n",
    ),
    (
        '    """What the load makes of the universe and the setting: the trains\' rows, J\'s potential, the state laid, term 11 on the edges with the edge key, the metric\'s push, the gradient vertex\'s plan."""',
        '    """What the load makes of the universe and the setting: the trains\' rows, J\'s potential, the state laid, term 11 on the edges with the edge key, the metric\'s push, the gradient vertex\'s plan, and edging\'s scale, kappa / two: every edge dial over the click\'s unit, the Mesh edges\' factor."""',
    ),
    (
        "    ]  # the gradient vertex: per term its readings on the plan's planes, its factor, its row\n\n\ndef load(",
        "    ]  # the gradient vertex: per term its readings on the plan's planes, its factor, its row\n"
        "    scale: Z  # kappa div senses, edging's own: every edge dial over the click's unit, the Mesh edges' factor\n\n\n"
        + KEYED,
    ),
    (") -> tuple[Loaded, list[str]]:", ") -> tuple[Loaded | None, list[str]]:"),
    (
        "term 11 on the edges laid from J's potential, every side's key the edge key, the universe file's one CHOSEN integer times kappa / two, its click tooth born at (key - 1) div 2;",
        "term 11 on the edges laid from J's potential, every side's key the edge dial D = (kappa div senses) K, K the click's unit the node computes at its initialization from the setting's one key's middle, senses middle + 1 (a key laid anywhere else, or none, named by keyed, and a scale with a remainder or an even D named by dialled, so nothing is loaded), its click tooth born at (D - 1) div senses, D's own middle;",
    ),
    (
        "    senses, _ = carry(len(star(side)), side, 0)  # the Spokes along one axis, its + and its -\n",
        "    # the Spokes along one axis, its + and its -, read as the pair's two ends: the count of the node's dials\n"
        "    senses, _ = carry(len(star(side)), side, 0)\n"
        "    middle, refused = keyed(universe, setting)  # the initialization's one scalar, its other lays named\n"
        "    if refused:\n"
        "        return None, refused\n"
        "    unit = dial(senses, middle)  # the click's unit K, the node's own at its initialization\n",
    ),
    (
        "    # term 11 on the edges, every side's key the edge key, at its own Node-clock and across each Spoke\n"
        '    click = edging(trains, potential, chosen["key"], star(side))\n'
        "    _, _, key = click\n"
        "    birth, _ = carry(\n"
        "        key - 1, senses, 0\n"
        "    )  # every side's click tooth at its birth, an edge's two summing to key - 1\n",
        "    # term 11 on the edges, every side's key the edge dial D = (kappa div senses) K, at its own Node-clock and across\n"
        "    # each Spoke, with the scale kappa / two and what its carry leaves\n"
        "    click, scale, spare = edging(trains, potential, unit, star(side))\n"
        "    _, _, key = click\n"
        "    # every side's click tooth at its birth, D's middle; a scale with a remainder or an even D named\n"
        "    birth, uneven = dialled(key, senses, spare)\n"
        "    if uneven:\n"
        "        return None, uneven\n",
    ),
    (
        "    return Loaded(trains, potential, state, click, push, mesh), laid",
        "    return Loaded(trains, potential, state, click, push, mesh, scale), laid",
    ),
    (
        "the board's neighbours and the edge key over the file's key, kappa / two) with the edge key,",
        "the board's neighbours and edging's scale, kappa / two, the load's) with the edge key,",
    ),
    (
        "    scale, _ = carry(\n"
        '        key[:1], universe["chosen"]["key"], 0\n'
        "    )  # the edge key over the file's key: kappa / two\n"
        "    across, onto = crossing(loaded.trains, loaded.mesh, spokes, nb, scale)\n",
        "    across, onto = crossing(loaded.trains, loaded.mesh, spokes, nb, loaded.scale)  # edging's kappa / two\n",
    ),
]

PLANS = [
    (
        "its weight on every train and the train of the leg it pushes; and every side's key. A monomial's legs:",
        "its weight on every train and the train of the leg it pushes, and every side's key; and the scale, kappa / two, with what its carry leaves, which the load reads (load.dialled names a remainder; laid_out's Mesh edges take the scale). A monomial's legs:",
    ),
    (
        "kappa: the product of two and of every legs count a live monomial on an edge holds, each once, so that every weight is whole (6 on every world laid: the hands' tie's two legs and the tie's three); every side's key the universe file's one CHOSEN key times kappa / two, 3 there (David's OPEN, a change of a declared number, NC29b), the same for every side at every reach, its own Node-clock and across each Spoke (crossing, the Mesh's edges), odd as the key is, so a side's two teeth born at (key - 1) div senses sum to key - 1 (load.load) and stay so by the carry's law;",
        "kappa: the product of two and of every legs count a live monomial on an edge holds, each once, so that every weight is whole (6 on the click and mesh worlds, where the tie's three legs lie on an edge; 2 on our bang and the live and well worlds, where no monomial lies on an edge); every side's key the click's unit K times kappa / two, K the node's own from the setting's one key's middle (load.dial), 3K on the click and mesh worlds (David's OPEN, a change of a declared number, NC29b), the same for every side at every reach, its own Node-clock and across each Spoke (crossing, the Mesh's edges), odd while kappa / two is, as on every plan laid today, so a side's two teeth born at (key - 1) div senses sum to key - 1 (load.load) and stay so by the carry's law; a monomial on an edge holding four legs makes kappa / two even and the key even for every middle, which the load refuses by name (load.dialled);",
    ),
    (
        "def edging(trains: Z, potential: tuple[Z, tuple[Z, Z, Z, Z]], key: Z, spokes: Z) -> tuple[Z, Z, Z]:\n",
        "def edging(\n"
        "    trains: Z, potential: tuple[Z, tuple[Z, Z, Z, Z]], unit: Z, spokes: Z\n"
        ") -> tuple[tuple[Z, Z, Z], Z, Z]:\n",
    ),
    (
        "    scale, _ = carry(kappa, senses, 0)\n"
        "    return (\n"
        "        (weight[:, :, None] * present[None, :, :]).reshape(positions * monomials, count),\n"
        "        (train * value).reshape(-1),\n"
        "        np.full(((1 + n) * count * count, 1), key * scale, dtype=object),\n"
        "    )\n",
        "    # kappa / two, and what the carry leaves: 0 as kappa is formed\n"
        "    scale, spare = carry(kappa, senses, 0)\n"
        "    return (\n"
        "        (\n"
        "            (weight[:, :, None] * present[None, :, :]).reshape(positions * monomials, count),\n"
        "            (train * value).reshape(-1),\n"
        "            np.full(((1 + n) * count * count, 1), unit * scale, dtype=object),\n"
        "        ),\n"
        "        scale,\n"
        "        spare,\n"
        "    )\n",
    ),
]

STATE = [
    (
        "the edge key: the universe file's CHOSEN key times kappa / two, the same for every side",
        "the edge dial: the click's unit K, the node's own from the setting's one key's middle, times kappa / two, the same for every side",
    ),
]

RUN = [
    (
        "    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square, lifted)\n    if found:\n",
        "    loaded, found = load(universe, setting, sites_of(shape), kinds, tables, square, lifted)\n"
        "    # a refused key, a scale with a remainder or an even edge dial loads nothing (load.keyed, load.dialled)\n"
        "    if found or loaded is None:\n",
    ),
]

RECORDS = [
    (
        "# train cards name each train once, each card's winding 1 or more (a winding counts its train's notches, and the books\n"
        "# read each train's windings at it); every value stands",
        "# train cards name each train once, each card's winding 1 or more (a winding counts its train's notches, and the books\n"
        "# read each train's windings at it), and each card's key the world's one key, the 1.4 header's dial (KEY4); every\n"
        "# value stands",
    ),
    (
        '    """The first train card off the record: a winding below 1, or a train an earlier card names; or nothing."""',
        '    """The first train card off the record: a winding below 1, a train an earlier card names, or a key off the world\'s one key, the 1.4 header\'s dial or else the first card\'s (the load\'s promise of one key, read in the record: KEY4, the physicist\'s m5); or nothing."""',
    ),
    (
        '    return f"train cards name the train {twice[0]} twice" if twice else ""\n',
        "    if twice:\n"
        '        return f"train cards name the train {twice[0]} twice"\n'
        '    keys = [(n, t["key"]) for n, t in enumerate(cards, start=1) if whole(t.get("key"))]\n'
        '    one = header["dial"] if whole(header.get("dial")) else next((k for _, k in keys), None)\n'
        "    off = [(n, k) for n, k in keys if k != one]\n"
        "    if off:\n"
        '        return f"train card {off[0][0]} holds the key {off[0][1]}, off the world\'s one key {one}"\n'
        '    return ""\n',
    ),
]

for name, edits in (
    ("runner/files.py", FILES),
    ("runner/load.py", LOAD),
    ("runner/plans.py", PLANS),
    ("engine/state.py", STATE),
    ("runner/run.py", RUN),
    ("decoder/records.py", RECORDS),
):
    path = SRC.joinpath(*name.split("/"))
    text = path.read_text(encoding="utf-8")
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:80])
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"{name}: {len(edits)} edits")
