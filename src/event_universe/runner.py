"""A world file -> the engine -> headless artifacts.

The one engine is the engine of the law of events (`event_universe.events`,
`events-v1`; Highlights 5.4). A run reads a world (a JSON object with
`"law": "events"`), refuses anything else by name, and
writes to an empty output directory the input as read (`initialization.json`),
the events (`events.jsonl`), the final state (`state.json`) and the record
(`run.json`); see `event_universe.events.run`. Runs are headless: there is no
visualization switch, no observer and one worker.
"""

import argparse
import hashlib
from pathlib import Path

from event_universe.events.run import execute_event_run
from event_universe.events.world import parse_event_world
from event_universe.json_documents import parse_json_document
from event_universe.retention import ArtifactLease, cleanup_expired, validate_output_path


def source_fingerprint() -> str:
    """The SHA-256 of the package's Python sources, the identity of a run's code."""
    root = Path(__file__).parent
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*.py")):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_initialization(initialization: Path, output: Path, *, ticks: int | None = None) -> Path:
    """Run the world at `initialization` into the empty directory `output` and
    return the path of its `run.json`; `ticks` overrides the world's own."""
    source = initialization.read_bytes()
    world = parse_event_world(parse_json_document(source))
    count = world.ticks if ticks is None else ticks
    if type(count) is not int or count < 0:
        raise ValueError("ticks must be nonnegative")
    _prepare_output(initialization, output)
    with ArtifactLease(output.parent, [output.resolve()]):
        return execute_event_run(world, source, output, source_fingerprint(), count)


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
    parser = argparse.ArgumentParser(description="Run a world of the law of events.")
    parser.add_argument("--init", required=True, type=Path, help="The world file (JSON)")
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--ticks", type=int, help="Override only the requested run duration")
    args = parser.parse_args()
    try:
        artifact = run_initialization(args.init, args.output, ticks=args.ticks)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Run failed: {error}\n")
    print(artifact.resolve())
