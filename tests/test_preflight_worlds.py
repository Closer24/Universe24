"""The pre-GO loader check (`tools/preflight_worlds.py`): every world a run list names is
loaded and its engine constructed, no interval stepped (the model owner's rule of
2026-09-24: nothing runs before it is checked and approved)."""

from __future__ import annotations

import json
from pathlib import Path

from tests.worlds import load_file

ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = load_file("preflight_worlds", ROOT / "tools/preflight_worlds.py")


def test_the_preflight_loads_every_listed_world_and_runs_none(tmp_path: Path, capsys) -> None:
    """The names of a list (a path as written, a bare name searched under the root, a brace
    group expanded, `expectations.json` skipped) resolve to files; a registered world of
    the engine loads with its engine constructed and no interval stepped (the engine's
    tick 0 is not observed: the tool keeps no engine), a ray-law world (cancelled) is
    REFUSED by its keys, a
    world refused by the loader is REFUSED with its message, a name without a file is
    MISSING; the exit is 0 with a missing world and 1 with a refused one or under
    `--strict` with a missing one; the real RUN_LIST.md's registered worlds all load."""
    root = tmp_path / "events"
    (root / "massive_record").mkdir(parents=True)
    (root / "bell").mkdir()
    good = ROOT / "examples/events/massive_record/muon_moving_clock_at_rest_14.json"
    (root / "massive_record/muon_moving_clock_at_rest_14.json").write_bytes(good.read_bytes())
    ray = ROOT / "examples/events/one_content.json"
    (root / "bell/bell_a0b0.json").write_bytes(ray.read_bytes())
    bad = json.loads(good.read_text(encoding="utf-8"))
    bad["amplitude_bound"] = 1 << 20  # a second copy of the families file's integer (item 59)
    (root / "massive_record/unbounded.json").write_text(json.dumps(bad), encoding="utf-8")
    listing = tmp_path / "RUN_LIST.md"
    listing.write_text(
        "| row | `massive_record/muon_moving_clock_at_rest_14.json` | `bell_{a0b0,a1b1}.json` |\n"
        "| row | `unbounded.json` and `expectations.json` | `to_write.json` |\n",
        encoding="utf-8",
    )
    names = PREFLIGHT.listed(listing.read_text(encoding="utf-8"))
    assert names == [
        "massive_record/muon_moving_clock_at_rest_14.json",
        "bell_a0b0.json",
        "bell_a1b1.json",
        "unbounded.json",
        "to_write.json",
    ]
    outcomes = PREFLIGHT.preflight(names, root)
    assert [o.status for o in outcomes] == ["LOADED", "REFUSED", "MISSING", "REFUSED", "MISSING"]
    assert "engine" in outcomes[0].detail and "law" in outcomes[1].detail  # the ray world's `law`
    assert "amplitude_bound" in outcomes[3].detail
    assert PREFLIGHT.main(["--list", str(listing), "--root", str(root)]) == 1
    assert PREFLIGHT.main(["--list", str(listing), "--root", str(root), "--strict"]) == 1
    only_missing = tmp_path / "missing.md"
    only_missing.write_text("`to_write.json`\n", encoding="utf-8")
    assert PREFLIGHT.main(["--list", str(only_missing), "--root", str(root)]) == 0
    assert PREFLIGHT.main(["--list", str(only_missing), "--root", str(root), "--strict"]) == 1
    printed = capsys.readouterr().out
    assert "no world run" in printed and "REFUSED" in printed
    # Reviewer 3's CHECKs 1 and 2 on a pair lamp (a Bell world) rest with the
    # Bell worlds, held until the crystal (BUILD.md section 26; the lamp is
    # refused under the detector law, the CHECKs return on the emitter that
    # fires at a crystal)
    # the real list: every registered world loads, none is refused
    real = PREFLIGHT.preflight(
        PREFLIGHT.listed((ROOT / PREFLIGHT.DEFAULT_LIST).read_text(encoding="utf-8")),
        ROOT / PREFLIGHT.DEFAULT_ROOT,
    )
    assert real and not [o for o in real if o.status == "REFUSED"], [
        o for o in real if o.status == "REFUSED"
    ]
    assert any(o.status == "LOADED" for o in real)
