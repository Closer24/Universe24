"""The look's viewer (docs/ENGINE.md #6-how-to-run-a-world): the host reader writes one diagnostic file per world and the page builder one page from it, generic for any world; a smoke test on the chain."""

from __future__ import annotations

import json

from event_universe import world_files
from tests.laws import CHAIN, ROOT, chain_body_world, load_file

TOOL = load_file("pixel_mode", ROOT / "tools" / "pixel_mode.py")
RECORD = load_file("look_record", ROOT / "tools" / "look" / "record.py")
PAGE = load_file("look_page", ROOT / "tools" / "look" / "page.py")
ROLE_OF = {"sign": "light", "content": "field"}  # a holder of nothing is matter


def test_the_reader_writes_the_look_and_the_page_shows_it_with_the_roles_from_the_file(
    tmp_path, monkeypatch
):
    """(a) The look of the chain over three intervals: the label, the file's families, per frame every array sized to the board, frame 0 the declared counts, each click line in its interval's frame (one per interval from the test's own GameBoard), the books; (b) the page: the label, the roles from the file's rows (the holder of the sign light, a holder of the content a field, a holder of nothing matter, a further one dashed), the blind file's window, and no interpolation between Nodes."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    world = chain_body_world(tmp_path, TOOL, at=(24, 40), holds={"charge": 64}, taker=True)

    class Clicking(RECORD.GameBoard):
        """The GameBoard with one click line per interval on the taker (the chain does not click by itself in three intervals): the line's placement in its frame is what is checked."""

        def step(self) -> None:
            super().step()
            line = {"event": "click", "tick": self.tick, "family": "charge", "detector": "taker"}
            self.observer({**line, "node": [24, 0, 0], "axis": [0, 1], "count": 1})

    monkeypatch.setattr(RECORD, "GameBoard", Clicking)
    RECORD.main([str(world), "--ticks", "3"])
    look = json.loads(world.with_suffix(".look.json").read_text(encoding="utf-8"))
    universe = json.loads((tmp_path / "u.json").read_text(encoding="utf-8"))["families"]
    assert look["label"] == "GameBoard reading" and look["verdict"] == "LAWFUL" and look["ticks"] == 3
    assert [f["name"] for f in look["families"]] == [f["name"] for f in universe]
    assert len(look["frames"]) == 4 and look["shape"] == [CHAIN, 1, 1] and look["arrays"] == "dense"
    for frame in look["frames"]:
        for family in look["families"]:
            row = frame["families"][family["name"]]
            arrays = [row[k] for k in ("now", "second", "count")] if family["quanta"] else [row["level"]]
            assert all(
                len(a) == CHAIN and all(len(x) == 1 and len(x[0]) == 1 for x in a) for a in arrays
            )
    laid = [look["frames"][0]["families"][f["name"]]["count"] for f in look["families"] if f["quanta"]]
    assert sum(x[0][0] for a in laid for x in a) == sum(
        b["declared"] + sum(map(sum, b["holds"].values())) for b in look["bodies"]
    )
    assert all(line["tick"] == t for t, frame in enumerate(look["frames"]) for line in frame["lines"])
    assert [len(frame["lines"]) for frame in look["frames"]] == [0, 1, 1, 1]
    assert set(look["books"]) == {f["name"] for f in look["families"] if f["quanta"]}
    blind = {"expected": {"taker": 3}, "family": "charge", "window": [1, 2]}
    (tmp_path / "chain.blind.json").write_text(json.dumps(blind), encoding="utf-8")
    PAGE.main([str(world.with_suffix(".look.json")), "--blind", str(tmp_path / "chain.blind.json")])
    html = (tmp_path / "chain.look.html").read_text(encoding="utf-8")
    roles = PAGE.roles(look["families"])
    for family, role in zip(universe, roles.values(), strict=True):
        assert role["role"] == ROLE_OF.get(family.get("held", {}).get("count"), "matter")
    dashed = [name for name, role in roles.items() if role["dashed"]]
    assert dashed == [f["name"] for f in universe if "held" not in f][1:]
    assert "GameBoard reading" in html and PAGE.embedded(roles) in html and '"window":[1,2]' in html
    assert "<title>Chain look</title>" in html and "interpolat" not in html.lower()
