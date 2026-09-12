"""Configuration routing and authoring checks without running a simulated world."""

import json
import subprocess
import sys
from copy import deepcopy
from dataclasses import is_dataclass
from pathlib import Path

import pytest

from event_universe.configuration_validation import prepare_initialization, validate_configuration
from event_universe.disturbance_api import Simulation

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "examples/known-entities/catalog.json"
PROFILES = CATALOG.with_name("representation-probes.json")
BASIC = ROOT / "examples/basic.json"
AUXILIARY = [
    ROOT / "examples/directional-wave/definition.json",
    ROOT / "examples/directional-wave/display.json",
    ROOT / "examples/directional-wave/experiments.json",
    ROOT / "examples/particle-contracts/entities.json",
]


def _read(path):
    return path.read_text(encoding="utf-8")


def _initializations():
    return sorted(
        path
        for folder in (ROOT / "examples", ROOT / "skills")
        for path in folder.rglob("*.json")
        if "schema_version" in json.loads(_read(path))
    )


def _assert_invalid(report, message=None):
    assert report.valid is False
    assert isinstance(report.kind, str)
    assert report.issues
    assert isinstance(report.summary, dict)
    for issue in report.issues:
        assert is_dataclass(issue)
        assert issue.code and issue.document and issue.message
    if message is not None:
        assert message.lower() in " ".join(issue.message for issue in report.issues).lower()
    encoded = report.to_dict()
    assert encoded["valid"] is False
    assert encoded["issues"]
    json.dumps(encoded, allow_nan=False)


def _cli(*arguments):
    return subprocess.run(
        [sys.executable, "-m", "event_universe.configuration_validation", *map(str, arguments)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize("path", _initializations(), ids=lambda path: path.relative_to(ROOT).as_posix())
def test_every_shipped_initialization_routes_to_its_existing_owner(path):
    report = validate_configuration(path.read_bytes())
    assert is_dataclass(report)
    assert report.valid, report.to_dict()
    assert report.kind == "initialization"
    assert report.issues == ()
    assert report.to_dict()["kind"] == "initialization"


def test_shipped_catalog_and_profiles_are_distinct_supported_documents():
    catalog = CATALOG.read_bytes()
    profiles = PROFILES.read_bytes()
    reference = validate_configuration(catalog)
    experiments = validate_configuration(profiles, catalog_source=catalog)
    assert reference.valid, reference.to_dict()
    assert experiments.valid, experiments.to_dict()
    assert reference.kind == "catalog"
    assert experiments.kind == "profiles"
    assert reference.issues == experiments.issues == ()


@pytest.mark.parametrize("path", AUXILIARY, ids=lambda path: path.relative_to(ROOT).as_posix())
def test_auxiliary_example_documents_are_reported_as_unsupported(path):
    _assert_invalid(validate_configuration(path.read_bytes()))


@pytest.mark.parametrize("source", ["null", "[]", "42", '"not a configuration"', "{}"])
def test_arbitrary_json_is_not_mistaken_for_a_supported_configuration(source):
    _assert_invalid(validate_configuration(source))


@pytest.mark.parametrize("discriminator", ["catalog_version", "profile_version"])
def test_multiple_format_discriminators_are_ambiguous(discriminator):
    raw = json.loads(_read(BASIC))
    raw[discriminator] = 2
    _assert_invalid(validate_configuration(json.dumps(raw)), "ambig")


@pytest.mark.parametrize("version", [0, 3, True, "1", []])
def test_unsupported_initialization_versions_preserve_owner_rejection(version):
    raw = json.loads(_read(BASIC))
    raw["schema_version"] = version
    _assert_invalid(validate_configuration(json.dumps(raw)), "schema_version")


def test_legacy_catalog_is_not_misreported_as_valid_physical_reference():
    raw = json.loads(_read(CATALOG))
    raw["catalog_version"] = 1
    _assert_invalid(validate_configuration(json.dumps(raw)))


@pytest.mark.parametrize(
    "source",
    [
        "{",
        '{"schema_version":1,"schema_version":1}',
        '{"schema_version":1,"metadata":{"a":1,"a":2}}',
        '{"schema_version":1,"value":NaN}',
        '{"schema_version":1,"value":Infinity}',
        '{"schema_version":1,"value":-Infinity}',
        '{"schema_version":1,"value":1e309}',
        b"\xff",
    ],
)
def test_invalid_json_is_a_report_instead_of_an_uncaught_exception(source):
    _assert_invalid(validate_configuration(source))


def test_existing_initialization_validator_remains_the_owner_of_semantic_errors():
    raw = json.loads(_read(BASIC))
    raw["seeds"][0]["type"] = "missing disturbance"
    _assert_invalid(validate_configuration(json.dumps(raw)), "type")


def test_profile_validation_requires_an_explicit_catalog_and_checks_every_representation():
    _assert_invalid(validate_configuration(_read(PROFILES)), "catalog")
    raw = json.loads(_read(PROFILES))
    raw["profiles"][-1]["quantum_profile"]["claim_level"] = "invented_species_law"
    _assert_invalid(validate_configuration(json.dumps(raw), catalog_source=_read(CATALOG)))


@pytest.mark.parametrize("change", ["orphan", "duplicate", "invalid_classical", "version"])
def test_profile_catalog_mismatches_and_invalid_profiles_are_rejected(change):
    raw = json.loads(_read(PROFILES))
    if change == "orphan":
        raw["profiles"][-1]["entity_id"] = "missing entity"
    elif change == "duplicate":
        raw["profiles"].append(deepcopy(raw["profiles"][0]))
    elif change == "invalid_classical":
        raw["profiles"][-1]["executable_profile"]["seed_values"] = {}
    else:
        raw["profile_version"] = 2
    _assert_invalid(validate_configuration(json.dumps(raw), catalog_source=_read(CATALOG)))


@pytest.mark.parametrize("dependency", ['{"catalog_version":2,"catalog_version":2}', "NaN", "{}"])
def test_invalid_catalog_dependency_never_reports_profiles_as_valid(dependency):
    _assert_invalid(validate_configuration(_read(PROFILES), catalog_source=dependency))


def test_observer_requires_explicit_kind_and_initialization_context():
    source = '{"position":[0,0,0]}'
    _assert_invalid(validate_configuration(source), "observer")
    report = validate_configuration(source, kind="observer")
    _assert_invalid(report, "initialization")
    assert report.to_dict()["issues"][0]["document"] == "initialization"
    assert report.to_dict()["issues"][0]["code"] == "missing_dependency"


def test_observer_coordinates_use_the_supplied_world_shape():
    initial = json.loads(_read(BASIC))
    source = json.dumps({"position": [initial["shape"][0], 0, 0], "max_receipts": 12})
    _assert_invalid(
        validate_configuration(
            source,
            kind="observer",
            initialization_source=json.dumps(initial),
        ),
        "observer position",
    )
    initial["shape"][0] += 1
    report = validate_configuration(source, kind="observer", initialization_source=json.dumps(initial))
    assert report.valid, report.to_dict()
    assert report.kind == "observer"
    assert tuple(report.summary["position"]) == (initial["shape"][0] - 1, 0, 0)
    assert report.summary["max_receipts"] == 12


@pytest.mark.parametrize(
    "source",
    [
        "null",
        '{"position":[true,0,0]}',
        '{"position":[0,0,0],"max_receipts":0}',
        '{"position":[0,0,0],"position":[1,1,1]}',
    ],
)
def test_invalid_sidecar_is_not_silently_ignored(source):
    _assert_invalid(
        validate_configuration(
            source,
            kind="observer",
            initialization_source=_read(BASIC),
        )
    )


@pytest.mark.parametrize("source", ["{", "{}", '{"schema_version":3}'])
def test_invalid_world_context_is_attributed_to_its_document(source):
    report = validate_configuration(
        '{"position":[0,0,0]}',
        kind="observer",
        initialization_source=source,
    )
    _assert_invalid(report)
    assert report.issues[0].document == "initialization"


@pytest.mark.parametrize("dependency", ["catalog_source", "initialization_source"])
def test_dependencies_are_rejected_when_the_selected_format_does_not_use_them(dependency):
    report = validate_configuration(_read(BASIC), **{dependency: "{}"})
    _assert_invalid(report)
    assert report.issues[0].code == "unexpected_dependency"


def test_preparing_input_keeps_inline_observer_separate_and_does_not_mutate_documents():
    raw = json.loads(_read(BASIC))
    plain = prepare_initialization(raw)
    assert plain.observer is None
    raw["observer"] = {"position": [0, 0, 0], "max_receipts": 17}
    before = deepcopy(raw)
    prepared = prepare_initialization(raw)
    assert prepared.observer.position == (0, 0, 0)
    assert prepared.observer.max_receipts == 17
    assert prepared.initial == plain.initial
    assert raw == before


def test_preparing_external_observer_preserves_inputs_and_rejects_null_or_double_placement():
    raw = json.loads(_read(BASIC))
    observer = {"position": [0, 0, 0]}
    before = deepcopy((raw, observer))
    prepared = prepare_initialization(raw, observer_document=observer)
    assert prepared.observer.position == (0, 0, 0)
    assert (raw, observer) == before
    with pytest.raises(ValueError, match="observer"):
        prepare_initialization(raw, observer_document=None)
    raw["observer"] = observer
    with pytest.raises(ValueError, match="not both"):
        prepare_initialization(raw, observer_document=observer)
    report = validate_configuration(
        json.dumps(observer),
        kind="observer",
        initialization_source=json.dumps(raw),
    )
    _assert_invalid(report, "not both")


def test_pure_validation_does_not_read_files_write_outputs_or_construct_a_simulation(monkeypatch):
    initial = _read(BASIC)
    catalog = _read(CATALOG)
    profiles = _read(PROFILES)

    def forbidden(*args, **kwargs):
        pytest.fail("Pure validation attempted filesystem access or simulation construction")

    monkeypatch.setattr(Simulation, "__init__", forbidden)
    for method in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir"):
        monkeypatch.setattr(Path, method, forbidden)
    reports = [
        validate_configuration(initial),
        validate_configuration(catalog),
        validate_configuration(profiles, catalog_source=catalog),
        validate_configuration('{"position":[0,0,0]}', kind="observer", initialization_source=initial),
    ]
    assert all(report.valid for report in reports)
    assert initial and catalog and profiles


def test_json_issue_report_retains_location_and_document_identity():
    report = validate_configuration('{\n"schema_version": }')
    issue = report.to_dict()["issues"][0]
    assert issue["code"] == "syntax"
    assert issue["document"] == "input"
    assert issue["line"] == 2
    assert isinstance(issue["column"], int) and issue["column"] > 0
    assert issue["message"]


def test_cli_reports_batch_success_without_creating_files(tmp_path):
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    first.write_bytes(BASIC.read_bytes())
    second.write_bytes(CATALOG.read_bytes())
    before = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    result = _cli(first, second, "--json")
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["report_version"] == 1 and report["valid"] is True
    assert [row["kind"] for row in report["results"]] == ["initialization", "catalog"]
    assert [row["path"] for row in report["results"]] == [str(first), str(second)]
    assert {path.name: path.read_bytes() for path in tmp_path.iterdir()} == before


def test_cli_continues_after_io_and_invalid_configuration_errors(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}", encoding="utf-8")
    missing = tmp_path / "missing.json"
    result = _cli(missing, invalid, BASIC, "--json")
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["valid"] is False
    assert [row["valid"] for row in report["results"]] == [False, False, True]
    assert report["results"][0]["issues"][0]["code"] == "io"


def test_cli_profile_dependencies_are_explicit_and_io_errors_are_reports(tmp_path):
    result = _cli(PROFILES, "--catalog", CATALOG, "--json")
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["results"][0]["kind"] == "profiles"
    result = _cli(PROFILES, "--catalog", tmp_path / "missing.json", "--json")
    assert result.returncode == 1
    issue = json.loads(result.stdout)["results"][0]["issues"][0]
    assert issue["document"] == "catalog" and issue["code"] == "io"


def test_cli_argument_errors_have_a_distinct_exit_status():
    result = _cli(BASIC, "--kind", "imaginary")
    assert result.returncode == 2
    assert "invalid choice" in result.stderr


def _deep_catalog(depth=2000):
    nested = "[" * depth + "0" + "]" * depth
    return _read(CATALOG).replace('"scope": {', '"scope": {"nested_audit":' + nested + ",", 1)


def test_excessive_json_nesting_returns_an_input_syntax_issue_and_ui_rejection():
    from event_universe.ui import MAX_REQUEST, validate_source

    source = "[" * 50000 + "0" + "]" * 50000
    assert len(source.encode("utf-8")) < MAX_REQUEST
    report = validate_configuration(source, kind="initialization")
    _assert_invalid(report, "nesting")
    assert report.issues[0].document == "input"
    assert report.issues[0].code == "syntax"
    with pytest.raises(ValueError) as caught:
        validate_source(source)
    assert str(caught.value) == report.issues[0].message


@pytest.mark.parametrize("as_dependency", [False, True])
def test_deep_catalog_domain_recursion_is_attributed_to_the_correct_document(as_dependency):
    source = _deep_catalog()
    if as_dependency:
        report = validate_configuration(_read(PROFILES), catalog_source=source)
    else:
        report = validate_configuration(source)
    _assert_invalid(report, "nesting")
    assert report.issues[0].document == ("catalog" if as_dependency else "input")
    assert report.issues[0].code == "validation"


def test_cli_batch_continues_after_excessively_nested_json_and_catalog(tmp_path):
    nested = tmp_path / "nested.json"
    nested.write_text("[" * 50000 + "0" + "]" * 50000, encoding="utf-8")
    catalog = tmp_path / "catalog.json"
    catalog.write_text(_deep_catalog(), encoding="utf-8")
    result = _cli(nested, catalog, BASIC, "--json")
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert [row["valid"] for row in report["results"]] == [False, False, True]
    assert [row["issues"][0]["code"] for row in report["results"][:2]] == ["syntax", "validation"]
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("case", ["schema", "native_capacity"])
def test_ui_and_runner_reuse_semantic_preflight_before_any_output(tmp_path, case):
    from event_universe.runner import run_initialization
    from event_universe.ui import validate_source

    if case == "schema":
        raw = json.loads(_read(BASIC))
        raw["schema_version"] = 3
    else:
        raw = json.loads(_read(ROOT / "examples/quantum/native_quantum.json"))
        raw["event_program"]["capacity"] = 0
    source = json.dumps(raw)
    report = validate_configuration(source, kind="initialization")
    _assert_invalid(report)
    with pytest.raises(ValueError) as caught:
        validate_source(source)
    assert str(caught.value) == report.issues[0].message
    path = tmp_path / "input.json"
    path.write_text(source, encoding="utf-8")
    output = tmp_path / "output"
    with pytest.raises((ValueError, OverflowError)):
        run_initialization(path, output)
    assert not output.exists()


def test_conflicting_observer_sources_reject_before_reading_the_sidecar(tmp_path, monkeypatch):
    from event_universe.runner import run_initialization

    document = json.loads(_read(BASIC))
    document["observer"] = {"position": [0, 0, 0]}
    path = tmp_path / "input.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    sidecar = tmp_path / "observer.json"
    read_bytes = Path.read_bytes

    def explicit_input_only(selected):
        assert selected != sidecar, "Conflicting sidecar must not be read"
        return read_bytes(selected)

    monkeypatch.setattr(Path, "read_bytes", explicit_input_only)
    with pytest.raises(ValueError, match="not both"):
        run_initialization(path, tmp_path / "output", observer=sidecar)
    assert not (tmp_path / "output").exists()
