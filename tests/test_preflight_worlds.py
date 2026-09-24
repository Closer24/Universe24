"""The pre-GO loader check (`tools/preflight_worlds.py`): every world a run list names is
loaded and its engine constructed, no interval stepped (the model owner's rule of
2026-09-24: nothing runs before it is checked and approved)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("preflight_worlds", ROOT / "tools/preflight_worlds.py")
assert SPEC is not None and SPEC.loader is not None
PREFLIGHT = importlib.util.module_from_spec(SPEC)
# registered before the load: the tool's dataclass looks its module up by name
sys.modules["preflight_worlds"] = PREFLIGHT
SPEC.loader.exec_module(PREFLIGHT)


def test_the_preflight_loads_every_listed_world_and_runs_none(tmp_path: Path, capsys) -> None:
    """The names of a list (a path as written, a bare name searched under the root, a brace
    group expanded, `expectations.json` skipped) resolve to files; a registered
    detector-law world and a ray-law world load with their engines constructed and no
    interval stepped (the engine's tick 0 is not observed: the tool keeps no engine), a
    world refused by the loader is REFUSED with its message, a name without a file is
    MISSING; the exit is 0 with a missing world and 1 with a refused one or under
    `--strict` with a missing one; the real RUN_LIST.md's registered worlds all load."""
    root = tmp_path / "events"
    (root / "massive_record").mkdir(parents=True)
    (root / "bell").mkdir()
    good = ROOT / "examples/events/massive_record/layer_pin_rest_14.json"
    (root / "massive_record/layer_pin_rest_14.json").write_bytes(good.read_bytes())
    ray = ROOT / "examples/events/one_content.json"
    (root / "bell/bell_a0b0.json").write_bytes(ray.read_bytes())
    # the ray world's entity definitions, referenced relative to its own file
    (root / "bell/entities").mkdir()
    (root / "bell/entities/families.json").write_bytes(
        (ROOT / "examples/events/entities/families.json").read_bytes()
    )
    bad = json.loads(good.read_text(encoding="utf-8"))
    del bad["amplitude_bound"]
    (root / "massive_record/unbounded.json").write_text(json.dumps(bad), encoding="utf-8")
    listing = tmp_path / "RUN_LIST.md"
    listing.write_text(
        "| row | `massive_record/layer_pin_rest_14.json` | `bell_{a0b0,a1b1}.json` |\n"
        "| row | `unbounded.json` and `expectations.json` | `to_write.json` |\n",
        encoding="utf-8",
    )
    names = PREFLIGHT.listed(listing.read_text(encoding="utf-8"))
    assert names == [
        "massive_record/layer_pin_rest_14.json",
        "bell_a0b0.json",
        "bell_a1b1.json",
        "unbounded.json",
        "to_write.json",
    ]
    outcomes = PREFLIGHT.preflight(names, root)
    assert [o.status for o in outcomes] == ["LOADED", "LOADED", "MISSING", "REFUSED", "MISSING"]
    assert "detector_law" in outcomes[0].detail and "rays" in outcomes[1].detail
    assert "amplitude_bound" in outcomes[3].detail
    assert PREFLIGHT.main(["--list", str(listing), "--root", str(root)]) == 1
    assert PREFLIGHT.main(["--list", str(listing), "--root", str(root), "--strict"]) == 1
    only_missing = tmp_path / "missing.md"
    only_missing.write_text("`to_write.json`\n", encoding="utf-8")
    assert PREFLIGHT.main(["--list", str(only_missing), "--root", str(root)]) == 0
    assert PREFLIGHT.main(["--list", str(only_missing), "--root", str(root), "--strict"]) == 1
    printed = capsys.readouterr().out
    assert "no world run" in printed and "REFUSED" in printed
    # Reviewer 3's CHECKs 1 and 2 on a pair lamp (a Bell world): "ordinal"
    # refused, fewer than W births within the ticks or the stock refused,
    # "seed" with W births admitted
    from tests.test_detector_law import pair_world

    for document, message in (
        (pair_world("ordinal", None, 64), "CHECK 1"),
        (pair_world("seed", 9, 32), "CHECK 2"),
        (dict(pair_world("seed", 9, 64), ticks=40), "CHECK 2"),
    ):
        (root / "bell/pair.json").write_text(json.dumps(document), encoding="utf-8")
        outcome = PREFLIGHT.load_one(root / "bell/pair.json")
        assert outcome.status == "REFUSED" and message in outcome.detail, outcome
    (root / "bell/pair.json").write_text(json.dumps(pair_world("seed", 9, 64)), encoding="utf-8")
    assert PREFLIGHT.load_one(root / "bell/pair.json").status == "LOADED"
    # the real list: every registered world loads, none is refused
    real = PREFLIGHT.preflight(
        PREFLIGHT.listed((ROOT / PREFLIGHT.DEFAULT_LIST).read_text(encoding="utf-8")),
        ROOT / PREFLIGHT.DEFAULT_ROOT,
    )
    assert real and not [o for o in real if o.status == "REFUSED"], [
        o for o in real if o.status == "REFUSED"
    ]
    assert any(o.status == "LOADED" for o in real)
