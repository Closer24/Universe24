"""Pure configuration preflight and a read-only command line adapter."""

import argparse
import json
from collections.abc import Sized
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Never, cast

from event_universe.core.disturbance_state import InitialState
from event_universe.entities import validate_profiles
from event_universe.entity_catalog import validate_catalog
from event_universe.initialization import parse_initial_state
from event_universe.json_documents import parse_json_document
from event_universe.observer_configuration import ObserverDefinition

KINDS = ("initialization", "catalog", "profiles", "observer")
_DISCRIMINATORS = {
    "schema_version": "initialization",
    "catalog_version": "catalog",
    "profile_version": "profiles",
}
_UNSET = object()


@dataclass(frozen=True)
class PreparedInitialization:
    initial: InitialState
    observer: ObserverDefinition | None


def prepare_initialization(
    document: object, *, observer_document: object = _UNSET
) -> PreparedInitialization:
    """Check runtime input and observer composition without constructing a world."""
    initial = parse_initial_state(document)
    data = cast(dict[str, object], document)
    validate_observer_selection(document, external=observer_document is not _UNSET)
    raw = data.get("observer", _UNSET) if observer_document is _UNSET else observer_document
    observer = None if raw is _UNSET else ObserverDefinition.parse(raw, initial.shape)
    return PreparedInitialization(initial, observer)


def validate_observer_selection(document: object, *, external: bool) -> None:
    """Reject conflicting sources before an entry point reads an unused sidecar."""
    if external and isinstance(document, dict) and "observer" in document:
        raise ValueError("define observer in initialization or --observer, not both")


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


class _Rejected(ValueError):
    def __init__(self, issue: ValidationIssue) -> None:
        super().__init__(issue.message)
        self.issue = issue


def _reject(code: str, document: str, message: str) -> Never:
    raise _Rejected(ValidationIssue(code, document, message))


def _decode(source: str | bytes, document: str) -> object:
    try:
        if not isinstance(source, (str, bytes)):
            raise ValueError("configuration source must be JSON text or bytes")
        return parse_json_document(source)
    except json.JSONDecodeError as error:
        raise _Rejected(
            ValidationIssue("syntax", document, error.msg, error.lineno, error.colno)
        ) from error
    except RecursionError as error:
        raise _Rejected(
            ValidationIssue("syntax", document, "JSON nesting exceeds the supported depth")
        ) from error
    except ValueError as error:
        raise _Rejected(ValidationIssue("syntax", document, str(error))) from error


def _kind(document: object, requested: str) -> str:
    if requested not in (*KINDS, "auto"):
        _reject("unsupported_kind", "input", f"unsupported configuration kind: {requested}")
    if requested != "auto":
        return requested
    if not isinstance(document, dict):
        _reject("unsupported_kind", "input", "configuration must be a JSON object")
    data = cast(dict[str, object], document)
    matches = [value for key, value in _DISCRIMINATORS.items() if key in data]
    if len(matches) != 1:
        _reject(
            "unsupported_kind",
            "input",
            "unsupported or ambiguous configuration: expected exactly one of "
            "schema_version, catalog_version or profile_version; "
            "observer files require --kind observer",
        )
    return matches[0]


def _initial_summary(prepared: PreparedInitialization) -> dict[str, object]:
    initial = prepared.initial
    return {
        "model": initial.model_id,
        "sampling_profile": initial.sampling_profile,
        "shape": initial.shape,
        "ticks": initial.ticks,
        "fields": len(initial.fields),
        "types": len(initial.disturbances),
        "seeds": len(initial.seeds),
    }


def validate_configuration(
    source: str | bytes,
    *,
    kind: str = "auto",
    catalog_source: str | bytes | None = None,
    initialization_source: str | bytes | None = None,
) -> ValidationReport:
    """Validate supplied content only: no implicit files, simulation or artifacts.

    Each format keeps its domain validator. A report contains the first concrete
    failure, and does not certify future execution or physical correctness.
    """
    resolved = kind
    context = "input"
    try:
        document = _decode(source, "input")
        resolved = _kind(document, kind)
        if catalog_source is not None and resolved != "profiles":
            _reject("unexpected_dependency", "catalog", "catalog is only used for profiles")
        if initialization_source is not None and resolved != "observer":
            _reject(
                "unexpected_dependency",
                "initialization",
                "initialization context is only used for observer files",
            )
        if resolved == "initialization":
            summary = _initial_summary(prepare_initialization(document))
        elif resolved == "catalog":
            validate_catalog(document)
            catalog = cast(dict[str, Sized], document)
            summary = {
                key: len(catalog[key])
                for key in (
                    "field_entities",
                    "particle_entities",
                    "disturbance_families",
                    "interaction_families",
                    "representative_channels",
                    "sources",
                )
            }
        elif resolved == "profiles":
            if catalog_source is None:
                _reject("missing_dependency", "catalog", "profiles require an explicit catalog")
            catalog_document = _decode(catalog_source, "catalog")
            context = "catalog"
            validate_catalog(catalog_document)
            context = "input"
            summary = dict(validate_profiles(catalog_document, document))
        else:
            if initialization_source is None:
                _reject(
                    "missing_dependency",
                    "initialization",
                    "observer files require an explicit initialization for shape and composition",
                )
            initial_document = _decode(initialization_source, "initialization")
            context = "initialization"
            # Attribute invalid context to its source before checking the sidecar.
            prepare_initialization(initial_document)
            context = "input"
            observer = prepare_initialization(initial_document, observer_document=document).observer
            assert observer is not None
            summary = {"position": observer.position, "max_receipts": observer.max_receipts}
        return ValidationReport(resolved, True, summary)
    except _Rejected as error:
        return ValidationReport(resolved, False, {}, (error.issue,))
    except RecursionError:
        return ValidationReport(
            resolved,
            False,
            {},
            (
                ValidationIssue(
                    "validation", context, "configuration nesting exceeds the supported depth"
                ),
            ),
        )
    except (ValueError, OverflowError) as error:
        return ValidationReport(
            resolved, False, {}, (ValidationIssue("validation", context, str(error)),)
        )


def main(argv: list[str] | None = None) -> int:
    """Read explicit paths and print reports; never create run artifacts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--kind", choices=("auto", *KINDS), default="auto")
    parser.add_argument("--catalog", type=Path, help="catalog context for profile files")
    parser.add_argument("--initialization", type=Path, help="world context for observer files")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    dependencies: dict[str, bytes] = {}
    dependency_issue: ValidationIssue | None = None
    for label in ("catalog", "initialization"):
        path = getattr(args, label)
        if path is not None:
            try:
                dependencies[label + "_source"] = path.read_bytes()
            except OSError as error:
                dependency_issue = ValidationIssue("io", label, f"{path}: {error}")
                break
    results: list[dict[str, object]] = []
    for path in args.paths:
        try:
            source = path.read_bytes()
            report = (
                ValidationReport(args.kind, False, {}, (dependency_issue,))
                if dependency_issue is not None
                else validate_configuration(source, kind=args.kind, **dependencies)
            )
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
