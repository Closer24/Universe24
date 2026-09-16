"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import importlib.util
import json
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from event_universe.retention import MAX_AGE_SECONDS, cleanup_expired

SPEC = importlib.util.spec_from_file_location(
    "check_scope", Path(__file__).resolve().parents[1] / "tools/check.py"
)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


@pytest.mark.parametrize(
    ("name", "consumer"),
    [
        ("finite-residence.json", "tests/test_native_ray_coupling.py"),
        ("field-sampling.json", "tests/test_ray_heading_flux.py"),
        ("evidence.py", "tests/test_ray_coupling_evidence.py"),
        ("render_gif.py", "tests/test_ray_coupling_evidence.py"),
        ("run_experiments.py", "tests/test_ray_coupling_evidence.py"),
        ("compare_controls.py", "tests/test_ray_coupling_evidence.py"),
    ],
)
def test_ray_candidate_resources_select_their_direct_consumers(name, consumer):
    selected, _ = CHECK.select(["examples/generic-ray-coupling/" + name], {})
    assert consumer in selected
    assert "tests/test_collisions.py" not in selected


@pytest.mark.parametrize("name", ["causal_charge.json", "repeated_contacts.json"])
def test_contact_composition_resources_select_their_preflight_regressions(name):
    selected, _ = CHECK.select(["examples/quantum/" + name], {})
    assert "tests/test_contact_profile_composition.py" in selected


@pytest.mark.parametrize(
    "name",
    [
        "spatial_momentum.py",
        "position_moment_response.py",
        "run_position_moment_response.py",
        "spatial_measurement_controls.py",
        "localized_charge.json",
    ],
)
def test_position_moment_resources_select_native_experiment(name):
    selected, _ = CHECK.select(["examples/quantum/" + name], {})
    assert "tests/test_position_moment_response.py" in selected


@pytest.mark.parametrize(
    "name",
    [
        "local_moment_exchange.py",
        "run_local_moment_exchange.py",
        "momentum_state_exchange.py",
        "localized_charge.json",
    ],
)
def test_local_moment_resources_select_their_experiment(name):
    selected, _ = CHECK.select(["examples/quantum/" + name], {})
    assert "tests/test_local_moment_exchange.py" in selected


def test_local_field_example_selects_state_and_physical_contract_consumers():
    selected, _ = CHECK.select(["examples/local_lorentz_field.json"], {})
    assert "tests/test_node_state_contract.py" in selected
    assert "tests/test_local_lorentz_field.py" in selected


def test_spatial_graph_example_selects_its_causal_contract():
    selected, _ = CHECK.select(["examples/spatial_causal_events.json"], {})
    assert "tests/test_spatial_causal_events.py" in selected


def test_many_contacts_selects_its_experiment_contract():
    selected, _ = CHECK.select(["examples/quantum/many_contacts.json"], {})
    assert "tests/test_many_contacts.py" in selected
    assert "tests/test_collisions.py" not in selected


def test_repeated_contacts_selects_its_runtime_input_consumer():
    selected, _ = CHECK.select(["examples/quantum/repeated_contacts.json"], {})
    assert "tests/test_recurrent_quantum_contact.py" in selected
    assert "tests/test_collisions.py" not in selected


@pytest.mark.parametrize(
    "name",
    [
        "quantum_classical_check.py",
        "environment_coherence_check.py",
        "trajectory_support_check.py",
        "run_physics_checks.py",
        "interference.json",
        "partial_dephasing.json",
        "repeated_contacts.json",
    ],
)
def test_quantum_classical_resources_select_the_bounded_experiment(name):
    selected, _ = CHECK.select(["examples/quantum/" + name], {})
    assert "tests/test_quantum_classical_experiment.py" in selected
    assert "tests/test_collisions.py" not in selected


@pytest.mark.parametrize(
    "path",
    [
        "examples/catalog-contact/experiment.json",
        "examples/catalog-contact/prepare.py",
        "examples/known-entities/catalog.json",
        "examples/known-entities/physical-units.json",
        "examples/quantum/causal_charge.json",
    ],
)
def test_catalog_contact_dependencies_select_their_integration_contract(path):
    selected, _ = CHECK.select([path], {})
    assert "tests/test_catalog_contact.py" in selected


def test_causal_interference_harness_selects_its_acceptance_contract():
    for path in ("examples/quantum/causal_interference.py", "examples/quantum/causal_charge.json"):
        selected, _ = CHECK.select([path], {})
        assert "tests/test_causal_interference.py" in selected
        assert "tests/test_collisions.py" not in selected


def test_causal_charge_example_selects_its_field_contract_without_unrelated_worlds():
    selected, typed = CHECK.select(["examples/quantum/causal_charge.json"], {})
    assert "tests/test_causal_contact_fields.py" in selected
    assert "tests/test_configuration_validation.py" in selected
    assert "tests/test_collisions.py" not in selected
    assert "tests/test_native_wave_origins.py" not in selected
    assert not typed


@pytest.mark.parametrize("name", ["runtime.py", "definitions.json", "README.md"])
def test_standalone_lab_changes_select_its_contract_suite(name):
    tests, typed = CHECK.select(["tools/generic_vector_lab/" + name], {})
    assert "tests/test_generic_vector_lab.py" in tests
    assert not typed


def test_transitive_imports_and_relative_helpers_retain_only_related_tests():
    sources = {
        "src/domain/math.py": "def calculate(): pass",
        "src/domain/engine.py": "from .math import calculate",
        "tests/helper.py": "from domain.engine import calculate",
        "tests/test_scalar_engine.py": "from .helper import calculate",
        "tests/test_unrelated.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["src/domain/math.py"], sources)
    assert "tests/test_scalar_engine.py" in tests
    assert "tests/test_unrelated.py" not in tests
    assert typed == ["src/domain/engine.py", "src/domain/math.py"]


def test_named_lazy_exports_do_not_pull_in_unrelated_physics():
    sources = {
        "src/event_universe/__init__.py": 'from .generic import Simulation\nmodules = {"ScalarSimulation": ".historical"}',
        "src/event_universe/generic.py": "class Simulation: pass",
        "src/event_universe/historical.py": "class ScalarSimulation: pass",
        "tests/test_generic.py": "from event_universe import Simulation",
        "tests/test_history.py": "from event_universe import ScalarSimulation",
    }
    tests, _ = CHECK.select(["src/event_universe/generic.py"], sources)
    assert "tests/test_generic.py" in tests
    assert "tests/test_history.py" not in tests
    tests, _ = CHECK.select(["src/event_universe/historical.py"], sources)
    assert "tests/test_history.py" in tests
    assert "tests/test_generic.py" not in tests


def test_deleted_module_retains_old_consumers_and_cycles_terminate():
    sources = {
        "src/demo/old.py": "from .other import run",
        "src/demo/other.py": "from .old import run",
        "tests/test_old.py": "from demo.old import run",
    }
    tests, _ = CHECK.select(["src/demo/old.py"], sources)
    assert "tests/test_old.py" in tests


def test_docs_and_validation_changes_do_not_schedule_simulations():
    tests, typed = CHECK.select(["AGENTS.md", "tools/check.py", ".github/workflows/check.yml"], {})
    assert tests == [
        "tests/test_check_scope.py",
        "tests/test_repository_hygiene.py",
        "tests/test_repository_language.py",
        "tests/test_repository_navigation.py",
    ]
    assert not typed


def test_example_selects_its_consumers_and_not_other_collision_candidates():
    sources = {
        "tests/test_atomic_interactions.py": 'EXAMPLE = "04-unequal-mass-collision.json"',
        "tests/test_collisions.py": "def test_old_candidate(): pass",
    }
    tests, _ = CHECK.select(["examples/04-unequal-mass-collision.json"], sources)
    assert "tests/test_atomic_interactions.py" in tests
    assert "tests/test_workspace.py" in tests
    assert "tests/test_collisions.py" not in tests


def test_shared_fixture_includes_all_its_consumers():
    sources = {"tests/test_a.py": "", "tests/test_b.py": ""}
    tests, _ = CHECK.select(["tests/conftest.py"], sources)
    assert {"tests/test_a.py", "tests/test_b.py"} <= set(tests)


@pytest.mark.parametrize(
    "example", ["basic", "exchange", "finite_fields", "open_world", "spatial_turning"]
)
def test_dynamic_example_paths_retain_identity_checks_without_unrelated_physics(example):
    sources = {
        "tests/test_generic_identity.py": 'filename = f"{name}.json"',
        "tests/test_collisions.py": "def test_historical(): pass",
    }
    tests, _ = CHECK.select([f"examples/{example}.json"], sources)
    assert "tests/test_generic_identity.py" in tests
    assert "tests/test_collisions.py" not in tests


def test_runpy_acceptance_tool_retains_application_consumer():
    sources = {
        "tests/test_legacy_application.py": 'runpy.run_path(root / "tools/check_diagonal_motion.py")',
        "tests/test_collisions.py": "def test_historical(): pass",
    }
    tests, _ = CHECK.select(["tools/check_diagonal_motion.py"], sources)
    assert "tests/test_legacy_application.py" in tests
    assert "tests/test_collisions.py" not in tests


@pytest.mark.parametrize(
    "filename", ["law.json", "definition.json", "experiments.json", "prepare.py", "observe.py"]
)
def test_directional_field_resources_select_the_candidate_consumer(filename):
    tests, _ = CHECK.select([f"examples/directional-wave/{filename}"], {})
    assert "tests/test_directional_wave.py" in tests


@pytest.mark.parametrize(
    "resource", ["entities.json", "build_reference_configurations.py", "electron-proton.json"]
)
def test_particle_resources_select_the_dynamic_contract_consumer(resource):
    tests, _ = CHECK.select(["examples/particle-contracts/" + resource], {})
    assert "tests/test_rational_particles.py" in tests
    assert "tests/test_collisions.py" not in tests


def no_change_main(monkeypatch, tmp_path, *arguments):
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    monkeypatch.setattr(CHECK, "git", lambda *args: "base" if args[0] == "merge-base" else "")
    monkeypatch.setattr(CHECK.sys, "argv", ["check.py", *arguments])
    monkeypatch.setattr(CHECK, "previous_sources", lambda *args: pytest.fail("no prior tree needed"))
    monkeypatch.setattr(CHECK, "select", lambda *args: pytest.fail("no dependency graph needed"))
    monkeypatch.setattr(
        CHECK.subprocess, "run", lambda *args, **kwargs: pytest.fail("no checks were selected")
    )
    CHECK.main()


def test_clean_checkout_still_honors_explicit_test_selection(monkeypatch, tmp_path, capsys):
    target = tmp_path / "tests/test_selected.py"
    target.parent.mkdir()
    target.write_text("def test_boundary(): pass", encoding="utf-8")
    no_change_main(
        monkeypatch, tmp_path, "--dry-run", "--tests", "tests/test_selected.py::test_boundary"
    )
    report = json.loads(capsys.readouterr().out)
    assert report["changed"] == []
    assert report["commands"] == [
        ["pytest", "tests/test_selected.py::test_boundary", "--junitxml=artifacts/junit.xml"]
    ]


@pytest.fixture
def git_checkout():
    # Git init cannot use a Windows reserved directory name in an ancestor path.
    with TemporaryDirectory(prefix="universe-check-tree-") as directory:
        yield Path(directory)


def test_batched_prior_tree_preserves_exact_sources_and_deleted_consumers(monkeypatch, git_checkout):
    # A real tiny Git tree tests framing, empty blobs, spaces and missing final newlines.
    tmp_path = git_checkout
    monkeypatch.setenv("GIT_DIR", ".git")
    monkeypatch.setenv("GIT_WORK_TREE", ".")
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    sources = {
        "src/demo/old.py": "def calculate(): return 7\n",
        "src/demo/empty.py": "",
        "tests/test_old.py": "from demo.old import calculate",
        "tools/with space.py": "# framed\n\n",
    }
    for path, content in {
        **sources,
        "tests/reference/archive.py": "archived",
        "src/data.json": "{}",
    }.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "core.autocrlf=false", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "fixture"],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "src/demo/old.py").unlink()
    (tmp_path / "tests/test_old.py").write_text("def test_replacement(): pass", encoding="utf-8")
    actual = CHECK.subprocess.check_output
    calls = []

    def counted(command, **kwargs):
        calls.append(command)
        return actual(command, **kwargs)

    monkeypatch.setattr(CHECK.subprocess, "check_output", counted)
    previous = CHECK.previous_sources("HEAD")
    assert previous == sources
    assert len(calls) == 2
    tests, _ = CHECK.select(["src/demo/old.py"], previous)
    assert "tests/test_old.py" in tests


def test_scope_report_is_registered_and_expires_without_removing_unregistered_files(
    monkeypatch, tmp_path
):
    no_change_main(monkeypatch, tmp_path)
    report = tmp_path / "artifacts/check-scope.json"
    assert json.loads(report.read_text(encoding="utf-8")) == {
        "mode": "affected",
        "changed": [],
        "commands": [],
    }
    original = report.parent / "original.json"
    original.write_text("preserved original", encoding="utf-8")
    result = cleanup_expired(report.parent, now=time.time() + MAX_AGE_SECONDS + 1)
    assert result["errors"] == [] and result["deleted"] == [str(report)]
    assert not report.exists() and original.read_text(encoding="utf-8") == "preserved original"


def test_dry_run_creates_no_scope_report_or_retention_registry(monkeypatch, tmp_path):
    no_change_main(monkeypatch, tmp_path, "--dry-run")
    assert list(tmp_path.iterdir()) == []


def test_scope_report_stays_leased_until_failed_selected_command_finishes(monkeypatch, tmp_path):
    selected = tmp_path / "tests/test_selected.py"
    selected.parent.mkdir()
    selected.touch()
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    monkeypatch.setattr(CHECK, "git", lambda *args: "base" if args[0] == "merge-base" else "")
    monkeypatch.setattr(CHECK.sys, "argv", ["check.py", "--tests", "tests/test_selected.py"])
    report = tmp_path / "artifacts/check-scope.json"

    def fail_command(command, **kwargs):
        assert command[2:4] == ["pytest", "tests/test_selected.py"]
        active = cleanup_expired(report.parent, now=time.time() + 2 * MAX_AGE_SECONDS)
        assert not active["errors"] and not active["deleted"] and report.exists()
        assert any(item["reason"] == "active writer" for item in active["skipped"])
        raise CHECK.subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(CHECK.subprocess, "run", fail_command)
    with pytest.raises(CHECK.subprocess.CalledProcessError):
        CHECK.main()
    finished = cleanup_expired(report.parent, now=time.time() + MAX_AGE_SECONDS + 1)
    assert not finished["errors"] and finished["deleted"] == [str(report)]
    assert selected.exists()


def test_quantum_profile_and_experiment_resources_select_consumers():
    tests, _ = CHECK.select(["examples/known-entities/catalog.json"], {})
    assert "tests/test_quantum_entities.py" in tests
    assert "tests/test_native_quantum_channels.py" in tests
    assert "tests/test_small_space_experiments.py" in tests
    assert "tests/test_entity_catalog.py" in tests
    assert "tests/test_entity_compiler.py" in tests
    assert "tests/test_physical_entities.py" in tests
    tests, _ = CHECK.select(["examples/known-entities/representation-probes.json"], {})
    assert {
        "tests/test_entity_compiler.py",
        "tests/test_quantum_entities.py",
        "tests/test_native_quantum_channels.py",
        "tests/test_small_space_experiments.py",
    } <= set(tests)
    tests, _ = CHECK.select(["examples/quantum/partial_dephasing.json"], {})
    assert "tests/test_native_quantum_channels.py" in tests


@pytest.mark.parametrize(
    "path",
    [
        "examples/new-world.json",
        "examples/directional-wave/display.json",
        "skills/simulation-configuration/assets/two-streams.json",
    ],
)
def test_configuration_inventory_selects_preflight_without_unrelated_worlds(path):
    tests, _ = CHECK.select([path], {})
    assert "tests/test_configuration_validation.py" in tests
    assert "tests/test_collisions.py" not in tests


@pytest.mark.parametrize("name", ["catalog.json", "representation-probes.json"])
def test_profile_validation_retains_explicit_data_dependencies(name):
    tests, _ = CHECK.select(["examples/known-entities/" + name], {})
    assert "tests/test_profile_validation.py" in tests
    assert "tests/test_configuration_validation.py" in tests


@pytest.mark.parametrize("filename", ["law.json", "definition.json", "experiments.json", "prepare.py"])
def test_coupled_excitation_resources_select_their_behavioral_consumer(filename):
    tests, _ = CHECK.select([f"examples/coupled-excitations/{filename}"], {})
    assert "tests/test_coupled_excitations.py" in tests
    assert "tests/test_directional_wave.py" not in tests


@pytest.mark.parametrize("name", ["catalog.json", "property-coupling-probes.json"])
def test_property_coupling_profiles_select_their_behavioral_consumer(name):
    tests, _ = CHECK.select([f"examples/known-entities/{name}"], {})
    assert "tests/test_property_entity_profiles.py" in tests
