"""The two kinds of escape through an open face, in the event stream and in the
summary (issue #614, 2026-09-21; the developer's reply and the Boss's word of
17:03Z: a documentation gap with a regression test, no engine line, no change
of the schema or the ledger).

A face is a detector for two kinds of escapes (BEAM_LAW section 5; ENGINE.md,
"An open face is a detector"), booked on two lines of the ledger:

- a ROW's escape in the walk is a click of `amount` units with a phase, booked
  on the face's `clicks` (`measured`), `content` and `record` (the square of the
  coherent pointer of the rows that left; `Ledger.face_amount`, `face_content`,
  `face_record`);
- a BODY's escape by its step is booked on the face's `measured_content` (its
  held content) and `momentum`, and on the books' `measured.escaped`, never on
  `clicks` or `record` (a measured event is not a row and has no pointer to
  square); its `click` line writes `amount` = its content beside `measured`
  (its number) and `held`, where a row's face click writes `measured` None.

(a) The two frozen worlds of batch #610 (`m_body_tof_mass4`, SHA-256
    59d5465f...; `m_body_tof_reverse`, 70c6f63f...; their entity definitions
    `body_faces.json`, 68f70ab7...), verbatim: a body of content 4 at the
    momentum +-64 on a 25 x 3 x 1 open bar, 160 intervals. The expected
    integers before the run: Q S M + |p| = 64 x 1 x 4 + 64 = 320, so the
    drive counts one Link per 320 / 64 = 5 self-creations; from x = 2 the 23rd
    Link leaves through `face:+x` (x = 24 is the last Node) at tick 23 x 5 =
    115, and from x = 22 the 23rd Link leaves through `face:-x` at 115. One
    `click` line per world: `detector` the face, `measured` 1, `amount` 4,
    `content` 4, `held` [4], `home` [0], `momentum` [+-64, 0, 0]; the face's
    summary `measured_content` 4, `momentum` [+-64, 0, 0], `clicks` 0,
    `measured` 0, `content` 0, `record` 0; the books' `measured.escaped` 4 and
    `transit.escaped` 0, balanced.
(b) The rows' side on `one_content` (the registered world, 25^3 open, the
    source at the centre releasing 2^17 units per heading per interval): the
    first face click at tick 23 on every face (12 Links at the heading's pace
    64 / 110, the flight's 21st interval, one interval of the release and one
    of the walk), one per interval after, so at 60 intervals 38 lines per
    face of `amount` 131072 at phase 0: `clicks` = `measured` = 38 x 131072 =
    4 980 736, `measured_content` 0, and `record` = 38 x (32 x 256 x
    131072)^2 = 38 x 2^60 (the pointer X = 32 x amount x C[0], C[0] = 256).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]

BODY_FACES = (
    '{\n  "format": "event-entities-v2",\n  "entities": [\n'
    '    {"name":"m4_plus","families":[{"name":"body","quantum":0,"phase":false}],'
    '"measured":[{"position":[0,0,0],"family":"body","amount":4,"momentum":[64,0,0],'
    '"directions":[[1,0,0]]}],"detectors":[]},\n'
    '    {"name":"m8_plus","families":[{"name":"body","quantum":0,"phase":false}],'
    '"measured":[{"position":[0,0,0],"family":"body","amount":8,"momentum":[128,0,0],'
    '"directions":[[1,0,0]]}],"detectors":[]},\n'
    '    {"name":"m4_rest","families":[{"name":"body","quantum":0,"phase":false}],'
    '"measured":[{"position":[0,0,0],"family":"body","amount":4,"momentum":[0,0,0],'
    '"directions":[[1,0,0]]}],"detectors":[]},\n'
    '    {"name":"m4_minus","families":[{"name":"body","quantum":0,"phase":false}],'
    '"measured":[{"position":[0,0,0],"family":"body","amount":4,"momentum":[-64,0,0],'
    '"directions":[[-1,0,0]]}],"detectors":[]}\n  ]\n}\n'
)
MASS4 = (
    '{"law":"beam","model_id":"M-BODY-TOF-MASS-INVARIANCE-m4","shape":[25,3,1],"ticks":160,'
    '"K":1024,"N":64,"release":[0,1],"suspension":[0,1],"width":1,'
    '"entity_definitions":"../entities/body_faces.json",'
    '"entities":[{"name":"projectile","definition":"m4_plus","position":[2,1,0]}]}'
)
REVERSE = (
    '{"law":"beam","model_id":"M-BODY-TOF-MASS-INVARIANCE-reversal-control","shape":[25,3,1],'
    '"ticks":160,"K":1024,"N":64,"release":[0,1],"suspension":[0,1],"width":1,'
    '"entity_definitions":"../entities/body_faces.json",'
    '"entities":[{"name":"projectile","definition":"m4_minus","position":[22,1,0]}]}'
)


def _run(world_dir: Path, name: str, text: str, out: Path, ticks: int | None = None) -> Path:
    path = world_dir / f"{name}.json"
    path.write_text(text, encoding="utf-8")
    return run_initialization(path, out, ticks=ticks).parent


def _lines(run: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in (run / "events.jsonl").read_text().splitlines()]


def _face(run: Path, face: str, family: str) -> dict[str, object]:
    report = json.loads((run / "run.json").read_text())
    (entry,) = [d for d in report["detectors"] if d["name"] == face]
    families = entry["families"]
    assert isinstance(families, dict)
    result = families[family]
    assert isinstance(result, dict)
    return result


@pytest.mark.parametrize(
    "name,text,face,sign",
    [("m_body_tof_mass4", MASS4, "face:+x", 1), ("m_body_tof_reverse", REVERSE, "face:-x", -1)],
)
def test_a_bodys_escape_is_its_content_on_the_face_not_a_click(
    tmp_path: Path, name: str, text: str, face: str, sign: int
):
    """(a): the frozen worlds of batch #610, +x and -x."""
    (tmp_path / "entities").mkdir()
    (tmp_path / "entities" / "body_faces.json").write_text(BODY_FACES, encoding="utf-8")
    (tmp_path / "worlds").mkdir()
    run = _run(tmp_path / "worlds", name, text, tmp_path / "out")
    clicks = [e for e in _lines(run) if e["event"] == "click"]
    assert len(clicks) == 1
    (click,) = clicks
    assert click["tick"] == 115 and click["detector"] == face and click["measured"] == 1
    # The body's click line writes `amount` = its content, beside `held`.
    assert click["amount"] == 4 and click["content"] == 4 and click["held"] == [4]
    assert click["home"] == [0] and click["momentum"] == [64 * sign, 0, 0]
    # The summary: the content on `measured_content` and the momentum, never on
    # `clicks` or `record`.
    summary = _face(run, face, "body")
    assert summary["measured_content"] == 4 and summary["momentum"] == [64 * sign, 0, 0]
    assert summary["clicks"] == 0 and summary["measured"] == 0 and summary["content"] == 0
    assert summary["record"] == 0
    for other in ("face:+x", "face:-x", "face:+y", "face:-y"):
        if other != face:
            assert _face(run, other, "body")["measured_content"] == 0
    # The books: the measured line's escape, not the transit line's.
    audit = json.loads((run / "run.json").read_text())["audit"][-1]["families"]["body"]
    assert audit["measured"]["escaped"] == 4 and audit["transit"]["escaped"] == 0
    assert audit["measured"]["balanced"] and audit["transit"]["balanced"]


def test_the_rows_escapes_are_the_faces_clicks_and_record(tmp_path: Path):
    """(b): `one_content` at 60 intervals, every face alike."""
    run = run_initialization(
        ROOT / "examples" / "events" / "one_content.json", tmp_path / "out", ticks=60
    ).parent
    lines = _lines(run)
    amount = 1 << 17
    for face in ("face:+x", "face:-x", "face:+y", "face:-y", "face:+z", "face:-z"):
        on_face = [e for e in lines if e["event"] == "click" and e["detector"] == face]
        assert len(on_face) == 38 and on_face[0]["tick"] == 23
        assert all(e["measured"] is None and e["amount"] == amount for e in on_face)
        summary = _face(run, face, "m")
        assert summary["clicks"] == 38 * amount == sum(int(e["amount"]) for e in on_face)
        assert summary["measured"] == 38 * amount and summary["measured_content"] == 0
        assert summary["record"] == 38 * (32 * 256 * amount) ** 2 == 38 << 60
