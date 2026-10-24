"""The reader of the clicks log alone (tools/clicks_read.py; ALGEBRA.md, The uncertainty principle is the record's and the click's; The paces compose): the committed record's credits read, and a log with the eight keys read, every number computed by hand."""

import json

from tests.laws import ROOT, load_file


def test_the_committed_records_credits_give_the_counts_floor_and_the_torus_wide_where_and_name_the_lacking_keys():
    """125 credits of light in the one window [30, 30]: the count's floor 1, the where 5 Links on every axis, the momentum unreadable with its key named, the bodies and the GR tables unreadable with their keys named."""
    reader = load_file("clicks_read_tool", ROOT / "tools" / "clicks_read.py")
    lines = reader.read_log(ROOT / "examples" / "events" / "universe24" / "universe24.clicks.jsonl")
    lacking = reader.lacking
    assert (len(lines.credits), len(lines.births), len(lines.lays)) == (125, 125, 625)
    assert reader.shape_of(lines) == (5, 5, 5)
    (row,) = reader.uncertainty_table(lines)
    assert (row["family"], row["window"], row["credits"]) == ("light", [30, 30], 125)
    assert (row["count_min"], row["count_sum"], row["where_spread"]) == (1, 125, [5, 5, 5])
    assert row["distinct_wheres"] == 125 and row["violations"] == []
    assert row["momentum_spread"] == row["product"] == lacking("momentum")
    bodies = reader.bodies_table(lines)
    assert len(bodies) == 125 and {b["identity"] for b in bodies} == {lacking("identity")}
    assert all(b["mass"]["label"] == "proton" and b["mass"]["mass"] == lacking("point") for b in bodies)
    assert all(b["velocity"] == lacking("identity") and b["position"]["when"] == 30 for b in bodies)
    assert all(b["momentum"]["momentum"] == lacking("momentum") for b in bodies)
    assert all(b["position"]["proper"] == "constant 0: no clock written on this log" for b in bodies)
    born = sorted(tuple(node) for birth in lines.births for node in birth["nodes"])
    assert sorted(tuple(b["position"]["where"]) for b in bodies) == born
    gr = reader.gr_table(lines)
    assert gr["dilation"] == {"rows": [], "note": lacking("identity", "proper")}
    assert (
        gr["tracks"] == {"rows": [], "note": lacking("identity")} and gr["light_spacing"]["rows"] == []
    )
    assert gr["silent"] == {"rows": [], "note": reader.ONE_WINDOW, "last_close": 30}


def test_a_log_with_the_eight_keys_gives_velocity_verdict_dilation_and_product_by_hand(tmp_path):
    """Two bodies over two closes on the 5-cube: A free from [0, 0, 0] to [2, 0, 0] in 4 intervals and 3 of its own, B bound at [1, 1, 1] with the beat 4; the dilation 3 / 4 against 4 / 4; the where's spread 2 and the momentum's 4 along x, their product 8."""

    def credit(interval, body, support, identity, momentum, proper):  # type: ignore[no-untyped-def]
        line = {"event": "credit", "label": "NODEDETECTOR", "interval": interval, "family": "light"}
        line.update(node_detector=body, window=[interval, interval], proper=proper, windows=0, count=1)
        line.update(before=None, realised=None, kept=None, left=None, absorbed="light", emitted=None)
        line.update(
            momentum=momentum, fan=[0, 0, 0], lost=None, source=None, recoil=[-p for p in momentum]
        )
        line.update(point=[3, 5], kind=2, sense=-1, support=support, beat=4, identity=identity)
        return line

    reader = load_file("clicks_read_tool_eight", ROOT / "tools" / "clicks_read.py")
    rows = [credit(10, "body 0", [0, 0, 0], [3, 0], [2, 0, 0], 8)]
    rows.append(credit(10, "body 1", [1, 1, 1], [3, 1], [-2, 0, 0], 10))
    rows.append(credit(14, "body 0", [2, 0, 0], [3, 0], [2, 0, 0], 11))
    rows.append(credit(14, "body 1", [1, 1, 1], [3, 1], [-2, 0, 0], 14))
    (tmp_path / "eight.clicks.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), "utf-8")
    lines = reader.read_log(tmp_path / "eight.clicks.jsonl")
    shape = reader.shape_of(lines, (5, 5, 5))
    a, b = reader.bodies_table(lines, shape)
    assert (a["identity"], a["velocity"]["links"], a["velocity"]["intervals"]) == ([3, 0], [2, 0, 0], 4)
    assert (a["velocity"]["per_interval"], a["velocity"]["proper_intervals"]) == ([0.5, 0.0, 0.0], 3)
    assert a["velocity"]["per_proper_interval"] == [2 / 3, 0.0, 0.0]
    assert a["bound_or_free"]["verdict"] == "free, v = [0.5, 0.0, 0.0] Links per interval"
    mass = a["mass"]
    assert (mass["mass"], mass["point"], mass["kind"], mass["sense"]) == (0.8, [3, 5], 2, -1)
    assert (a["energy"]["quanta"], a["energy"]["rest"]) == (1, 0.8)
    bound = b["bound_or_free"]
    assert (bound["verdict"], bound["beats"], bound["beat"]) == ("bound at [1, 1, 1]", [4], [4, 4])
    dilation = reader.gr_table(lines, shape)["dilation"]["rows"]
    read = [(r["identity"], r["proper_intervals"], r["intervals"], r["ratio"]) for r in dilation]
    assert read == [([3, 0], 3, 4, 0.75), ([3, 1], 4, 4, 1.0)]
    first, second = reader.uncertainty_table(lines, shape)
    assert (first["window"], first["where_spread"]) == ([10, 10], [2, 2, 2])
    assert (first["momentum_spread"], first["product"], first["violations"]) == (
        [4, 0, 0],
        [8, 0, 0],
        [],
    )
    assert (second["window"], second["product"], second["violations"]) == ([14, 14], [8, 0, 0], [])
