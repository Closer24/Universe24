"""The gate's configuration follows the one list of cancelled paths (docs/CANCELLED_WORLDS.md
section 4 through tools/cancelled_paths.py): the type checker ignores exactly the modules
cancelled whole under `src/`, so the full gate (`tools/check.py --full`) is green on a tree that
keeps the ray law's modules on disk without deleting them (records 2102, 2103, 2133)."""

from __future__ import annotations

import importlib.util
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cancelled_modules() -> set[str]:
    spec = importlib.util.spec_from_file_location(
        "cancelled_paths", ROOT / "tools" / "cancelled_paths.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    paths = [p for p in module.cancelled_paths("modules") if p.startswith("src/event_universe/")]
    return {p[len("src/") : -len(".py")].replace("/", ".") for p in paths}


def test_the_type_checker_ignores_exactly_the_modules_cancelled_whole() -> None:
    configuration = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    overrides = configuration["tool"]["mypy"]["overrides"]
    ignored = {
        name
        for override in overrides
        if override.get("ignore_errors") is True
        for name in override["module"]
    }
    assert ignored == cancelled_modules()
