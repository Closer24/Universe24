"""The reader of the clicks log alone (tools/clicks_read.py; ALGEBRA.md, The uncertainty principle is the record's and the click's; The paces compose): a log with the click's view's keys read (the momentum the frame's running cosine with the Link current's sign, 2026-10-24), every number computed by hand; the reading of the committed record's log, a pin on the record's counts, struck 2026-10-24 with the tests' audit."""

import json

from tests.laws import ROOT, load_file


def test_a_log_with_the_click_views_keys_gives_velocity_verdict_dilation_rest_and_product_by_hand(
    tmp_path,
):
    """Two bodies over two closes on the 5-cube, the momentum the frame's running cosine with the Link current's sign (2026-10-24): A free from [0, 0, 0] to [2, 0, 0] in 4 intervals (its two credits two Nodes' clocks, no own interval) with [1, -1, 2] on x, p_x = T sqrt(3) / 2 toward +x, its rest point 3 (3 / 5) / (3 / 2) = 6 / 5 and its band energy sin omega(k) at cos omega(k) = 3 / 5 - 1 / 2 = 1 / 10, 9 / 10; B bound at [1, 1, 1] with [-1, -1, 2] on x and [1, 0, 1] on y, p = [-sqrt(3) / 2, 1, 0] T, its Node's clock 3 whole intervals over the 4, the dilation 3 / 4; the where's spread 2 Links and the momentum's sqrt(3) T along x, 1 T along y and 0 along z, the products 2 sqrt(3), 2 and 0 Links x T, the 0 below the floor T / 2 named; the massless record's own credit with the point [1, 1] and [0, 1, 1] on every axis reads the rest 1 at the vacuum's paces; a born record's first credit at a one-Node lay, its three spatial pairs (0, 1), reads the rest None, named."""

    def credit(interval, body, support, identity, momentum, proper, point=(3, 5)):  # type: ignore[no-untyped-def]
        line = {"event": "credit", "label": "NODEDETECTOR", "interval": interval, "family": "light"}
        line.update(node_detector=body, window=[interval, interval], proper=proper, windows=0, count=1)
        line.update(before=None, realised=None, kept=None, left=None, absorbed="light", emitted=None)
        line.update(momentum=momentum, lost=None, source=None)
        line.update(point=list(point), kind=2, sense=-1, support=support, beat=4, identity=identity)
        return line

    reader = load_file("clicks_read_tool_view", ROOT / "tools" / "clicks_read.py")
    along = [[1, -1, 2], [0, 1, 1], [0, 1, 1]]  # A: cos k_x = -1 / 2 toward +x, at rest on y and z
    back = [[-1, -1, 2], [1, 0, 1], [0, 1, 1]]  # B: toward -x on x, cos k_y = 0 toward +y
    rows = [
        credit(10, "body 0", [0, 0, 0], [3, 0], along, 8),
        credit(10, "body 1", [1, 1, 1], [3, 1], back, 10),
    ]
    rows += [
        credit(14, "body 0", [2, 0, 0], [3, 0], along, 11),
        credit(14, "body 1", [1, 1, 1], [3, 1], back, 13),
    ]
    rows.append(
        credit(12, 62, [2, 2, 2], [0, 0], [[0, 1, 1]] * 3, 12, (1, 1))
    )  # the massless record's own
    rows.append(credit(16, 93, [3, 3, 3], [5, 0], [[0, 0, 1]] * 3, 16))  # a born record's first credit
    (tmp_path / "view.clicks.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), "utf-8")
    lines = reader.read_log(tmp_path / "view.clicks.jsonl")
    shape = reader.shape_of(lines, (5, 5, 5))
    a, b, massless, born = reader.bodies_table(lines, shape)
    assert (a["identity"], a["velocity"]["links"], a["velocity"]["intervals"]) == ([3, 0], [2, 0, 0], 4)
    assert (a["velocity"]["per_interval"], a["velocity"]["per_proper_interval"]) == (
        [0.5, 0.0, 0.0],
        reader.TWO_CLOCKS,
    )
    assert a["bound_or_free"]["verdict"] == "free, v = [0.5, 0.0, 0.0] Links per interval"
    root = reader.leg_below(3) / 2  # sin k at cos k = -1 / 2, the leg's floor over the den
    assert a["momentum"] == {"momentum": along, "p": [root, 0.0, 0.0]}
    mass = a["mass"]
    assert (mass["mass"], mass["point"], mass["kind"], mass["sense"], mass["beat"]) == (
        0.8,
        [3, 5],
        2,
        -1,
        4,
    )
    assert (mass["rest"]["rest"], mass["rest"]["value"]) == ([6, 5], 1.2)
    assert mass["rest"]["paces"].startswith(
        "approximate: the Node's clock 11 against the board's interval 14"
    )
    assert (a["energy"]["quanta"], a["energy"]["rest"], a["energy"]["with_momentum"]) == (1, 0.8, 0.9)
    assert b["momentum"]["p"] == [-root, 1.0, 0.0] and b["mass"]["rest"]["rest"] == [18, 5]
    bound = b["bound_or_free"]
    assert (bound["verdict"], bound["beats"], bound["beat"]) == ("bound at [1, 1, 1]", [4], [4, 4])
    assert massless["mass"]["rest"] == {"rest": [1, 1], "value": 1.0, "paces": reader.VACUUM_PACES}
    assert born["mass"]["rest"] == {"rest": None, "note": reader.ONE_NODE_LAY}
    dilation = reader.gr_table(lines, shape)["dilation"]["rows"]
    read = [
        (r["where"], r["identities"], r["proper_intervals"], r["intervals"], r["ratio"])
        for r in dilation
    ]
    assert read == [([1, 1, 1], [(3, 1), (3, 1)], 3, 4, 0.75)]
    first, light, second, lay = reader.uncertainty_table(lines, shape)
    assert (first["window"], first["where_spread"], first["floor"]) == (
        [10, 10],
        [2, 2, 2],
        reader.FLOOR,
    )
    assert (first["momentum_spread"], first["product"]) == ([2 * root, 1.0, 0.0], [4 * root, 2.0, 0.0])
    assert first["violations"] == [
        "axis 2: Delta x Delta p = 0.0 Links x T, below the law's floor T / 2"
    ]
    assert (second["window"], second["product"], second["violations"]) == (
        [14, 14],
        first["product"],
        first["violations"],
    )
    assert (light["where_spread"], light["momentum_spread"], light["violations"]) == (
        [1, 1, 1],
        [0.0, 0.0, 0.0],
        [],
    )
    assert (lay["window"], lay["momentum_spread"], lay["product"]) == (
        [16, 16],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
    )
