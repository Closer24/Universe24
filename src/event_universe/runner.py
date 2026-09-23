"""A world or portable entity bundle -> the engine -> headless artifacts.

The one engine is the engine of the Beam Law (`event_universe.events`,
`beam-v1`; docs/BEAM_LAW.md, Highlights 5.4). The host loader resolves literal entity data
before preparing output or constructing the physical world. A run
writes to an empty output directory the input as read (`initialization.json`),
the events (`events.jsonl`), the final state (`state.json`) and the record
(`run.json`). Dependency-bearing runs also preserve the portable bundle and
expanded world; see `docs/ENTITY_DEFINITIONS.md`. Runs are headless: there is no
visualization switch, no observer and one worker.
"""

import argparse
import hashlib
import sys
from pathlib import Path

from event_universe.events.run import execute_nature_beam_run
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path
from event_universe.trimmed_record import row_clicks_note, world_needs_row_clicks
from event_universe.world_loading import load_world


def source_fingerprint() -> str:
    """The SHA-256 of the package's Python sources, the identity of a run's code."""
    root = Path(__file__).parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_initialization(
    initialization: Path,
    output: Path,
    *,
    ticks: int | None = None,
    keep_row_clicks: bool = False,
) -> Path:
    """Run the world at `initialization` into the empty directory `output` and
    return the path of its `run.json`; `ticks` overrides the world's own;
    `keep_row_clicks` (the command line's `--keep-row-clicks`, off by
    default) keeps the per-row click lines of the measured events in the
    record (`execute_nature_beam_run`). Without it, a world that declares a
    detector set, a measured event with a `measure`, `read` or `pass` entry
    or a window (`world_needs_row_clicks`) is announced by one line on
    stderr naming the option and the readers that need the lines
    (`row_clicks_note`); the run goes on."""
    source = initialization.read_bytes()
    loaded = load_world(source, base_dir=initialization.parent)
    world = loaded.world
    count = world.ticks if ticks is None else ticks
    if type(count) is not int or count < 0:
        raise ValueError("ticks must be nonnegative")
    if not keep_row_clicks and world_needs_row_clicks(world):
        print(row_clicks_note(initialization), file=sys.stderr)
    _prepare_output(initialization, output)
    with ArtifactLease(output.parent, [output.resolve()]):
        initialization_record: dict[str, object] | None = None
        if loaded.dependencies:
            (output / "initialization_bundle.json").write_bytes(loaded.portable_source)
            (output / "resolved_initialization.json").write_bytes(loaded.expanded_source)
            initialization_record = {
                "format": "event-world-bundle-v1",
                "bundle_sha256": hashlib.sha256(loaded.portable_source).hexdigest(),
                "expanded_sha256": hashlib.sha256(loaded.expanded_source).hexdigest(),
                "sources": [
                    {"path": dependency.path, "sha256": dependency.sha256}
                    for dependency in loaded.dependencies
                ],
            }
        return execute_nature_beam_run(
            world,
            source,
            output,
            source_fingerprint(),
            count,
            initialization_record=initialization_record,
            keep_row_clicks=keep_row_clicks,
        )


def _prepare_output(initialization: Path, output: Path) -> None:
    """The output directory of a run: valid, outside the input, empty."""
    validate_output_path(output)
    if initialization.resolve().is_relative_to(output.resolve()):
        raise ValueError("the original initialization must be outside the output directory")
    cleanup_expired(output.parent)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use an empty output directory to preserve earlier run artifacts")
    output.mkdir(parents=True, exist_ok=True)


def main() -> None:
    """Command line: run a world of the Beam Law and write its record."""
    parser = argparse.ArgumentParser(description="Run a world of the Beam Law.")
    parser.add_argument("--init", required=True, type=Path, help="The world file (JSON)")
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--ticks", type=int, help="Override only the requested run duration")
    parser.add_argument(
        "--keep-row-clicks",
        action="store_true",
        help=(
            "Keep the per-row click lines of the measured events in events.jsonl "
            "(a GameBoard diagnostic, most of a long record's bytes; the readers of "
            "those lines need them). Off by default: the lines are left out and "
            "run.json carries omit_row_clicks true; every other line as it is"
        ),
    )
    args = parser.parse_args()
    try:
        artifact = run_initialization(
            args.init, args.output, ticks=args.ticks, keep_row_clicks=args.keep_row_clicks
        )
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())
