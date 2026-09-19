"""Pure configuration preflight and a read-only command line adapter.

A world file is checked without running it: decoded strictly
(`json_documents`), then parsed by the engine's own world parser
(`event_universe.events.world`), whose refusals name the key at fault. A valid
report summarizes the world; it does not certify a run or any physics.
"""

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from event_universe.events.world import RAYS_LAW
from event_universe.world_loading import DocumentSyntaxError, load_world

KINDS = ("rays",)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    document: str
    message: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class ValidationReport:
    kind: str
    valid: bool
    summary: dict[str, object]
    issues: tuple[ValidationIssue, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return JSON-compatible report data; validity is configuration-only."""
        return {
            "kind": self.kind,
            "valid": self.valid,
            "summary": self.summary.copy(),
            "issues": [asdict(issue) for issue in self.issues],
        }


def validate_configuration(
    source: str | bytes, *, kind: str = "auto", base_dir: Path | None = None
) -> ValidationReport:
    """Validate supplied content only: no implicit files, simulation or artifacts.

    A report contains the first concrete failure, and does not certify a run or
    physical correctness. The only kind is `rays`, a world of the law of the ray.
    """
    if kind not in (*KINDS, "auto"):
        issue = ValidationIssue("unsupported_kind", "input", f"unsupported configuration kind: {kind}")
        return ValidationReport(kind, False, {}, (issue,))
    resolved = "rays"
    try:
        world = load_world(source, base_dir=base_dir).world
        summary = {
            "model": world.model_id,
            "law": RAYS_LAW,
            "shape": world.shape,
            "boundary": world.boundary_per_axis,
            "ticks": world.ticks,
            "families": len(world.families),
            "measured": len(world.measured),
            "detectors": len(world.detectors),
        }
        return ValidationReport(resolved, True, summary)
    except DocumentSyntaxError as error:
        issue = ValidationIssue("syntax", error.document, str(error), error.line, error.column)
        return ValidationReport(resolved, False, {}, (issue,))
    except OSError as error:
        return ValidationReport(resolved, False, {}, (ValidationIssue("io", "input", str(error)),))
    except RecursionError:
        issue = ValidationIssue(
            "validation", "input", "configuration nesting exceeds the supported depth"
        )
        return ValidationReport(resolved, False, {}, (issue,))
    except (ValueError, OverflowError) as error:
        return ValidationReport(
            resolved, False, {}, (ValidationIssue("validation", "input", str(error)),)
        )


def main(argv: list[str] | None = None) -> int:
    """Read explicit paths and print reports; never create run artifacts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--kind", choices=("auto", *KINDS), default="auto")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    results: list[dict[str, object]] = []
    for path in args.paths:
        try:
            report = validate_configuration(path.read_bytes(), kind=args.kind, base_dir=path.parent)
        except OSError as error:
            report = ValidationReport(
                args.kind, False, {}, (ValidationIssue("io", "input", str(error)),)
            )
        results.append({"path": str(path), **report.to_dict()})
        if not args.as_json:
            status = "VALID" if report.valid else "INVALID"
            print(f"{status} {path} ({report.kind}; configuration only)")
            for issue in report.issues:
                print(f"  {issue.document}: {issue.message}")
    valid = all(result["valid"] for result in results)
    if args.as_json:
        print(json.dumps({"report_version": 1, "valid": valid, "results": results}, indent=2))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
