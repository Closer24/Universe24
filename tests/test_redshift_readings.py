"""The redshift readings tool (series E, `tools/redshift_readings.py`)
under the rule of records 562 and 564 (the model owner, 2026-09-22; the
audit of record 567): the window's k x r^p and the redshift ratio come
from the world replayed through the API, so the tool prints them as
GameBoard diagnostics ("agrees" or "differs"), never counted inside or
outside, and names the probes' own records (the column `k, whole run`)
as the detector reading not yet compared.

(a) `print_shells` on a synthetic reading of two shells: the header names
    the replay as GAMEBOARD and the whole-run column as DETECTOR; every
    verdict is "agrees" or "differs", none "inside" or "outside"; the
    returned list carries one diagnostic per shell from r = 6.
(b) `print_redshift` the same on an `age` reading: the header is labelled
    GAMEBOARD, a diagnostic, not counted.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "redshift_readings_tool", ROOT / "tools" / "redshift_readings.py"
)
assert SPEC is not None and SPEC.loader is not None
TOOL = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TOOL
SPEC.loader.exec_module(TOOL)


def reading(kind: str) -> object:
    found = TOOL.Reading(
        kind=kind,
        suspension=(1, 2),
        centre=(0, 0, 0),
        directions=6,
        ticks=10,
        completed=True,
        balanced=True,
        elapsed=0.0,
    )
    for radius, waited in ((6, 3), (8, 2), (12, 1)):
        probe = TOOL.Probe(
            position=(radius, 0, 0),
            radius=radius,
            age=10,
            waited=waited,
            window_age=5,
            window_waited=waited,
        )
        found.shells[radius] = TOOL.Shell(radius=radius, probes=[probe])
        found.by_position[probe.position] = probe
    return found


def test_the_window_products_are_diagnostics_never_counted(capsys):
    """(a)."""
    diagnostics = TOOL.print_shells([reading("age")])
    out = capsys.readouterr().out
    assert "GAMEBOARD, a diagnostic, not counted" in out
    assert "`k, whole run` is the probes' own records (DETECTOR)" in out
    assert " inside " not in out and " outside " not in out
    assert len(diagnostics) == 3 and all(label.startswith("age: k x r^1") for label, _ in diagnostics)
    assert all(word in out for word in ("agrees", "differs")) or "agrees" in out


def test_the_redshift_ratio_is_a_diagnostic_never_counted(capsys):
    """(b)."""
    diagnostics = TOOL.print_redshift([reading("age")])
    out = capsys.readouterr().out
    assert out.startswith("GAMEBOARD (a replay's window means: a diagnostic, not counted")
    assert "not yet compared" in out and " inside " not in out and " outside " not in out
    assert all(label.startswith("redshift ratio at r = ") for label, _ in diagnostics)
