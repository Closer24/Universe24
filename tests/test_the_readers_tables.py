"""The reader's seven tables (tools/clicks_read.py: density_table, tracks_table, distance_table, ledger_table, dilation_vs_clock, spacing_vs_length, births_table; the owner's words of 2026-10-24, 16:3x UTC: all the epochs since the big bang in the clicks, another bang that erases nothing, the attraction of clicking bodies, relativity and the Links' lengthening in the clicks) on a log of a few lines written by hand with the click's view's keys, the eras and nodes lines beside it by hand, every number asserted by hand; the window of tools/back_in_time.py (--from K) on the bare 3-cube; the committed record as the smoke check."""

import json

import pytest

from event_universe import world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import ROOT, load_file
from tests.laws_universe import small_universe

READER = load_file("clicks_read_tables", ROOT / "tools" / "clicks_read.py")
RECORD = ROOT / "examples" / "events" / "universe24"
SHAPE = (5, 5, 5)
LIGHT, A, B, C = [0, 0], [3, 0], [3, 1], [3, 2]  # the identities: light's and the three bodies'
ELECTRON, PROTON, HOLDER = "point 2 0", "point 0 2", "point 1 1"  # the hand eras log's families


def credit(interval, where, identity, proper, family="light", body=None):  # type: ignore[no-untyped-def]
    """A credit line with the click's view's eight keys: the board's own (the Node's index the reader) for light, `body n` for a body."""
    index = where[0] * SHAPE[1] * SHAPE[2] + where[1] * SHAPE[2] + where[2]
    keys = dict(event="credit", label="NODEDETECTOR", interval=interval, family=family, count=1)
    keys.update(node_detector=index if body is None else body, window=[interval, interval])
    keys.update(proper=proper, windows=0, momentum=[[0, 1, 1]] * 3, point=[3, 5], kind=2, sense=-1)
    return {**keys, "support": list(where), "beat": 4, "identity": identity}


def birth(interval, where, child, senses, records, point):  # type: ignore[no-untyped-def]
    children = [child, child]
    found = dict(event="birth", label="NODEDETECTOR", interval=interval, family="light")
    return {
        **found,
        "children": children,
        "senses": senses,
        "nodes": [list(where)],
        "records": records,
        "points": [point, point],
    }


def hand_log(tmp_path):  # type: ignore[no-untyped-def]
    """Light's credits at eight closes over four Nodes, the body A moving one Link toward the bound body B, the body C bound a Link from B across the torus's edge, three births and two lays."""
    rows = [credit(10, (0, 0, 0), LIGHT, 10), credit(10, (1, 1, 1), LIGHT, 10)]
    rows += [
        credit(10, (0, 2, 0), A, 10, ELECTRON, "body 0"),
        credit(10, (2, 2, 0), B, 10, ELECTRON, "body 1"),
    ]
    rows += [credit(10, (2, 2, 4), C, 10, PROTON, "body 2"), credit(12, (0, 0, 0), LIGHT, 12)]
    rows += [credit(14, (1, 1, 1), LIGHT, 14), credit(14, (1, 2, 0), A, 13, ELECTRON, "body 0")]
    rows += [
        credit(14, (2, 2, 0), B, 13, ELECTRON, "body 1"),
        credit(14, (2, 2, 4), C, 11, PROTON, "body 2"),
    ]
    rows += [credit(18, (2, 2, 2), LIGHT, 18), credit(18, (3, 3, 3), LIGHT, 18)]
    rows += [
        credit(18, (1, 2, 0), A, 17, ELECTRON, "body 0"),
        credit(18, (2, 2, 0), B, 16, ELECTRON, "body 1"),
    ]
    rows += [credit(20, (3, 3, 3), LIGHT, 20), credit(22, (2, 2, 2), LIGHT, 26)]
    rows += [
        birth(10, (0, 2, 0), ELECTRON, [-1, 1], [0, 1], [3, 5]),
        birth(14, (1, 1, 1), PROTON, [1, -1], [0, 1], [4, 5]),
    ]
    rows += [birth(18, (2, 2, 2), ELECTRON, [-1, 1], [2, 3], [3, 5])]
    lay = dict(
        event="lay",
        label="LATTICE",
        interval=10,
        family="light",
        line=0,
        before=[1, 1, 0],
        after=[0, 0, 0],
    )
    rows += [
        {**lay, "node": {"label": "LATTICE", "at": [0, 2, 0]}},
        {**lay, "node": {"label": "LATTICE", "at": [1, 2, 0]}},
    ]
    (tmp_path / "hand.clicks.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows), "utf-8")
    return READER.read_log(tmp_path / "hand.clicks.jsonl"), rows


def era(interval):  # type: ignore[no-untyped-def]
    """One eras line by hand: the volume rising to 180 at 8, falling to 110 at 15 and rising again (the return at 15), one fire at the top, the quanta per family stepping at the births, the holder's one quantum spent at the return."""
    volume = (
        100 + 10 * interval
        if interval <= 8
        else (180 - 10 * (interval - 8) if interval <= 15 else 110 + 10 * (interval - 15))
    )
    light = 125 if interval < 10 else (123 if interval < 14 else (121 if interval < 18 else 119))
    quanta = {"light": light, ELECTRON: 0 if interval < 10 else (2 if interval < 18 else 4)}
    quanta.update({PROTON: 0 if interval < 14 else 2, HOLDER: 1 if 2 <= interval <= 14 else 0})
    writes = {"light": 0, ELECTRON: 0, PROTON: 0, HOLDER: 0}
    rows = {"gravity": {"volume": volume, "writes": writes}}
    return {
        "interval": interval,
        "fires": int(interval == 8),
        "horizon": 0,
        "rows": rows,
        "quanta": {f: {"quanta": q} for f, q in quanta.items()},
    }


HEADER = {
    "shape": list(SHAPE),
    "held": ["gravity"],
    "seed": "light",
    "intervals": 24,
    "primes": [[5, 1], [13, 1]],
    "points": {ELECTRON: [3, 4], PROTON: [5, 12]},
}
ERAS = [HEADER] + [era(t) for t in range(1, 25)]


def node_line(interval):  # type: ignore[no-untyped-def]
    """One nodes line by hand: the Link's length 1 everywhere but at [0, 0, 0] (1.2 to 12), at B's Node [2, 2, 0] (1.25) and at [2, 2, 2] (0.5 from 18)."""
    lengths = [1.0] * 125
    lengths[0], lengths[60] = (1.2 if interval <= 12 else 1.0), 1.25
    lengths[62] = 0.5 if interval >= 18 else 1.0
    return {"interval": interval, "length": lengths}


NODES = [node_line(t) for t in (10, 11, 12, 13, 14, 18, 19, 20, 21, 22)]


def test_the_density_the_ledger_and_the_births_read_the_epochs_the_erasure_and_the_senses_by_hand(
    tmp_path,
):  # type: ignore[no-untyped-def]
    """The hand log's clicks per interval and its epochs with the eras log's bounds (bang 1, rise, top 8, fall, return 15, rise) and without them (the density's own runs); the first rise alone where the eras log has no top; the ledger's two cycles with the holder's quantum erased across the return at 15 and the tracks that cross it; the births per cycle per point per sense, the senses summing to 0, the lists equal to the legend's counts."""
    lines, rows = hand_log(tmp_path)
    density = READER.density_table(lines, ERAS)
    assert density["per_interval"] == [
        {"interval": 10, "credits": 5, "births": 1, "lays": 2},
        {"interval": 12, "credits": 1, "births": 0, "lays": 0},
        {"interval": 14, "credits": 4, "births": 1, "lays": 0},
        {"interval": 18, "credits": 4, "births": 1, "lays": 0},
        {"interval": 20, "credits": 1, "births": 0, "lays": 0},
        {"interval": 22, "credits": 1, "births": 0, "lays": 0},
    ]
    assert density["densest"] == {"interval": 10, "credits": 5}
    assert density["birth_spans"] == [{"from": a, "to": a, "most": 1} for a in (10, 14, 18)]
    epochs = [
        (e["name"], e["cycle"], e["from"], e["to"], e["credits"], e["births"], e["lays"])
        for e in density["epochs"]
    ]
    assert epochs == [
        ("bang", 1, 1, 1, 0, 0, 0),
        ("rise", 1, 2, 7, 0, 0, 0),
        ("top", 1, 8, 8, 0, 0, 0),
        ("fall", 1, 9, 14, 10, 2, 2),
        ("return", 2, 15, 15, 0, 0, 0),
        ("rise", 2, 16, 24, 6, 1, 0),
    ]
    fall, rise = density["epochs"][3], density["epochs"][5]
    assert (
        density["epochs"][2]["volume"],
        fall["credits_per_interval"],
        rise["credits_per_interval"],
    ) == (180, 10 / 6, 6 / 9)
    assert (
        fall["words"]
        == "10 credits, 2 births, 2 lays over 6 intervals; the densest clicks of the run at 10"
    )
    assert density["epochs"][0]["words"] == "quiet: no line of the clicks log over 1 interval"
    assert density["bounds"] == "the eras log's tops and returns"
    alone = READER.density_table(lines, ERAS[:9])
    assert [(e["name"], e["from"], e["to"]) for e in alone["epochs"]] == [
        ("bang", 1, 1),
        (READER.FIRST_RISE, 2, 8),
    ]
    assert alone["bounds"].endswith(READER.FIRST_RISE)
    own = READER.density_table(lines)
    assert [e["name"] for e in own["epochs"]] == [
        "bang",
        "quiet",
        "clicks",
        "quiet",
        "clicks",
        "quiet",
        "clicks",
        "quiet",
        "clicks",
        "quiet",
        "clicks",
    ]
    assert [(e["from"], e["to"]) for e in own["epochs"]][:6] == [
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 17),
    ]
    ledger = READER.ledger_table(lines, ERAS)
    first, second = ledger["rows"]
    assert (
        first["cycle"],
        first["bang"],
        first["to"],
        first["top"],
        first["volume"],
        first["return"],
        first["open"],
    ) == (1, 1, 14, 8, 180, 15, False)
    assert first["births"] == {ELECTRON: {"-1": 1, "1": 1}, PROTON: {"1": 1, "-1": 1}} and first[
        "points"
    ] == {ELECTRON: [3, 5], PROTON: [4, 5]}
    assert first["counts"] == {
        "at_top": {"light": 125, ELECTRON: 0, PROTON: 0, HOLDER: 1},
        "before_return": {"light": 121, ELECTRON: 2, PROTON: 2, HOLDER: 1},
        "at_return": {"light": 121, ELECTRON: 2, PROTON: 2, HOLDER: 0},
    }
    assert first["erased"] == [HOLDER] and first["standing"] == first["counts"]["before_return"]
    across = {
        tuple(t["identity"]): (t["closes_before"], t["closes_after"]) for t in first["tracks_across"]
    }
    assert across == {(0, 0): (4, 4), (3, 0): (2, 1), (3, 1): (2, 1)}
    assert (first["credits"], first["lays"], first["turns"], first["horizon"]) == (10, 2, 1, 0)
    assert (second["bang"], second["to"], second["top"], second["return"], second["open"]) == (
        15,
        24,
        None,
        None,
        True,
    )
    assert second["births"] == {ELECTRON: {"-1": 1, "1": 1}} and second["counts"] == {
        "at_top": None,
        "before_return": None,
        "at_return": None,
    }
    assert (
        second["erased"],
        second["tracks_across"],
        second["credits"],
        second["lays"],
        second["turns"],
    ) == ([], [], 6, 0, 0)
    assert second["standing"] == {"light": 119, ELECTRON: 4, PROTON: 2, HOLDER: 0}
    assert ledger["finding"] == f"Erased across a return: cycle 1 at 15: {HOLDER}"
    births = READER.births_table(lines, ERAS)
    assert [
        (r["cycle"], r["point"], r["shown"], r["caption"], r["senses"], r["records"], r["lists"])
        for r in births["rows"]
    ] == [
        (1, PROTON, f"{PROTON} (proton)", "proton", {"-1": 1, "1": 1}, 2, 1),
        (1, ELECTRON, f"{ELECTRON} (electron)", "electron", {"-1": 1, "1": 1}, 2, 1),
        (2, ELECTRON, f"{ELECTRON} (electron)", "electron", {"-1": 1, "1": 1}, 2, 1),
    ]
    assert births["cycles"] == [
        {"cycle": 1, "bang": 1, "to": 14, "lists": 2, "records": 4, "sense_sum": 0, "charge_kept": True},
        {
            "cycle": 2,
            "bang": 15,
            "to": 24,
            "lists": 1,
            "records": 2,
            "sense_sum": 0,
            "charge_kept": True,
        },
    ]
    assert births["total"] == {
        PROTON: {"shown": f"{PROTON} (proton)", "lists": 1, "records": 2},
        ELECTRON: {"shown": f"{ELECTRON} (electron)", "lists": 2, "records": 4},
    }
    legend = READER.captions_module().legend_of(ERAS, [], rows, None)
    counted = {row["kind"]: row["count"] for row in legend["rows"]}
    assert counted[f"{ELECTRON} (electron) births"] == births["total"][ELECTRON]["lists"] == 2
    assert counted[f"{PROTON} (proton) births"] == births["total"][PROTON]["lists"] == 1
    alone = READER.births_table(lines)
    assert alone["cycles"] == [
        {"cycle": 1, "bang": 10, "to": 18, "lists": 3, "records": 6, "sense_sum": 0, "charge_kept": True}
    ]
    assert alone["rows"][0]["shown"] == PROTON and alone["rows"][0]["caption"] is None


def test_the_tracks_the_distance_the_dilation_and_the_spacing_read_the_bodies_and_light_by_hand(
    tmp_path,
):  # type: ignore[no-untyped-def]
    """The tracks per identity with the where per close; the distance A to B falling from 2 to 1 Links (the slope -1 / 8 Links per interval), B to C standing at 1 Link across the torus's edge, named; the dilation at every where against the nodes log's pace, within one interval at seven wheres and off by three at C's; light's spacing against e^U, longer where e^U is smaller, on both sides of the return at 15."""
    lines, _rows = hand_log(tmp_path)
    tracks = {tuple(r["identity"]): r for r in READER.tracks_table(lines, SHAPE)["rows"]}
    light, a = tracks[(0, 0)], tracks[(3, 0)]
    assert (light["credits"], light["closes"], light["one_body"], light["note"]) == (
        8,
        [10, 12, 14, 18, 20, 22],
        False,
        READER.NO_ONE_BODY,
    )
    assert light["series"][:2] == [
        {"close": 10, "where": [0, 0, 0], "proper": 10, "point": [3, 5], "sense": -1},
        {"close": 10, "where": [1, 1, 1], "proper": 10, "point": [3, 5], "sense": -1},
    ]
    assert (
        a["credits"],
        a["one_body"],
        [s["where"] for s in a["series"]],
        [s["proper"] for s in a["series"]],
    ) == (3, True, [[0, 2, 0], [1, 2, 0], [1, 2, 0]], [10, 13, 17])
    distance = READER.distance_table(lines, SHAPE)
    assert distance["identities"] == [A, B]
    assert [
        (r["close"], r["wheres"], r["links"], r["distance"], r["square"]) for r in distance["rows"]
    ] == [
        (10, [[0, 2, 0], [2, 2, 0]], [2, 0, 0], 2, 4),
        (14, [[1, 2, 0], [2, 2, 0]], [1, 0, 0], 1, 1),
        (18, [[1, 2, 0], [2, 2, 0]], [1, 0, 0], 1, 1),
    ]
    assert (distance["slope"], distance["fall"], distance["note"]) == (
        -0.125,
        -1,
        "the distance falls over the run",
    )
    assert distance["light_fall"] == {"identity": [0, 0], "credits": 8, "note": READER.NO_ONE_BODY}
    stands = READER.distance_table(lines, SHAPE, B, C)
    assert [(r["close"], r["links"], r["distance"]) for r in stands["rows"]] == [
        (10, [0, 0, -1], 1),
        (14, [0, 0, -1], 1),
    ]
    assert (stands["slope"], stands["fall"], stands["note"]) == (0, 0, READER.STANDS)
    dilation = READER.dilation_vs_clock(lines, NODES, SHAPE)
    read = [
        (
            r["where"],
            r["proper_intervals"],
            r["intervals"],
            r["length"],
            round(r["clock_intervals"], 4),
            round(r["difference"], 4),
            r["within_one_interval"],
        )
        for r in dilation["rows"]
    ]
    assert read == [
        ([0, 0, 0], 2, 2, [1.2, 1.2], 1.6667, 0.3333, True),
        ([1, 1, 1], 4, 4, [1.0, 1.0], 4.0, 0.0, True),
        ([1, 2, 0], 4, 4, [1.0, 1.0], 4.0, 0.0, True),
        ([2, 2, 0], 3, 4, [1.25, 1.25], 3.2, -0.2, True),
        ([2, 2, 0], 3, 4, [1.25, 1.25], 3.2, -0.2, True),
        ([2, 2, 2], 8, 4, [0.5, 0.5], 8.0, 0.0, True),
        ([2, 2, 4], 1, 4, [1.0, 1.0], 4.0, -3.0, False),
        ([3, 3, 3], 2, 2, [1.0, 1.0], 2.0, 0.0, True),
    ]
    assert (
        dilation["rows"][2]["clock"]
        == "the two closes' mean pace over 4 intervals: the nodes log lacks the Node's length at [15, 16, 17]"
    )
    assert (
        dilation["rows"][1]["clock"] == "the pace e^-U summed over the intervals after the first close"
    )
    assert (
        dilation["verdict"] == "off by more than one interval at 1 of 8 wheres: [[2, 2, 4]]"
        and dilation["note"] == ""
    )
    spacing = READER.spacing_vs_length(lines, NODES, SHAPE, "light", ERAS)
    spans = [
        (r["where"], s["closes"], s["spacing"], s["length"], s["mean_length"])
        for r in spacing["rows"]
        for s in r["spans"]
    ]
    assert spans == [
        ([0, 0, 0], [10, 12], 2, [1.2, 1.2], 1.2),
        ([1, 1, 1], [10, 14], 4, [1.0, 1.0], 1.0),
        ([2, 2, 2], [18, 22], 4, [0.5, 0.5], 0.5),
        ([3, 3, 3], [18, 20], 2, [1.0, 1.0], 1.0),
    ]
    relation = spacing["relation"]
    assert (relation["spans"], relation["sign"], relation["words"]) == (4, -1, READER.WORDS[-1])
    assert relation["slope"] == pytest.approx(-0.7 / 0.2675)
    (side,) = spacing["sides"]
    assert (side["return"], side["across"], side["same_sign"]) == (15, 0, True)
    assert (side["before"]["slope"], side["after"]["slope"]) == pytest.approx((-10.0, -4.0))
    assert (
        spacing["note"] == "" and READER.spacing_vs_length(lines, [], SHAPE)["note"] == READER.NO_NODES
    )


def test_the_back_in_time_window_runs_forward_to_k_with_no_snapshot_then_the_window_forward_and_back(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The bare 3-cube under the small universe, forward to 4 with no snapshot, then 4 intervals forward and 4 back: MATCH at the window's first interval with `from` in the report; the plain run's report as before, no `from` key."""
    back = load_file("back_in_time_window", ROOT / "tools" / "back_in_time.py")
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    (tmp_path / "bare.json").write_text(
        json.dumps({"universe": "u.json", "shape": [3, 3, 3], "intervals": 9}), "utf-8"
    )
    found = back.verdict(Lattice(load_world(tmp_path / "bare.json")), 4, 4)
    assert found == {"verdict": "MATCH", "intervals": 4, "interval": 4, "from": 4}
    plain = back.verdict(Lattice(load_world(tmp_path / "bare.json")), 2)
    assert plain == {"verdict": "MATCH", "intervals": 2, "interval": 1}


def test_the_seven_tables_read_the_committed_record_through_the_command_line(tmp_path):  # type: ignore[no-untyped-def]
    """The smoke check: the CLI with the eras and nodes logs beside the committed record writes the thirteen tables; 26 epochs over 7 cycles (the clicks at 30 in the first rise), the ledger's 7 rows with nothing erased, 125 proton lists in the births, the tracks and the clock tables unreadable with their keys named."""
    out = tmp_path / "readings_clicks.json"
    logs = [str(RECORD / f"universe24.{kind}.jsonl") for kind in ("clicks", "eras", "nodes")]
    READER.main([logs[0], "--eras", logs[1], "--nodes", logs[2], "--out", str(out)])
    tables = json.loads(out.read_text("utf-8"))
    assert tables["shape"] == [5, 5, 5] and len(tables["density"]["epochs"]) == 26
    assert tables["density"]["densest"] == {"interval": 30, "credits": 125}
    assert [e["name"] for e in tables["density"]["epochs"]][:6] == [
        "bang",
        "rise",
        "top",
        "fall",
        "return",
        "rise",
    ]
    assert len(tables["ledger"]["rows"]) == 7 and tables["ledger"]["finding"].startswith(
        "Nothing erased across the 6 returns"
    )
    assert tables["births"]["total"] == {"proton": {"shown": "proton", "lists": 125, "records": 250}}
    assert (
        tables["tracks"]["note"] == READER.lacking("identity")
        and tables["dilation_vs_clock"]["rows"] == []
    )
    assert tables["spacing_vs_length"]["note"] == "one credit per where: no spacing"
