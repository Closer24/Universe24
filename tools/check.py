"""Validate changed files and their affected consumers; full validation is explicit."""

import argparse
import ast
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# These consumers build resource paths at runtime rather than importing modules.
RESOURCE_CONSUMERS = {
    "examples/quantum/spatial_momentum.py": (
        "tests/test_spatial_momentum.py",
        "tests/test_position_moment_response.py",
    ),
    "examples/quantum/position_moment_response.py": ("tests/test_position_moment_response.py",),
    "examples/quantum/run_position_moment_response.py": ("tests/test_position_moment_response.py",),
    "examples/quantum/spatial_measurement_controls.py": ("tests/test_position_moment_response.py",),
    "examples/quantum/local_moment_exchange.py": ("tests/test_local_moment_exchange.py",),
    "examples/quantum/run_local_moment_exchange.py": ("tests/test_local_moment_exchange.py",),
    "examples/quantum/momentum_state_exchange.py": ("tests/test_local_moment_exchange.py",),
    "examples/quantum/localized_charge.json": (
        "tests/test_localized_quantum_contact.py",
        "tests/test_local_moment_exchange.py",
        "tests/test_position_moment_response.py",
    ),
    "examples/quantum/repeated_contacts.json": (
        "tests/test_recurrent_quantum_contact.py",
        "tests/test_quantum_classical_experiment.py",
        "tests/test_contact_profile_composition.py",
    ),
    "examples/quantum/quantum_classical_check.py": ("tests/test_quantum_classical_experiment.py",),
    "examples/quantum/environment_coherence_check.py": ("tests/test_quantum_classical_experiment.py",),
    "examples/quantum/trajectory_support_check.py": ("tests/test_quantum_classical_experiment.py",),
    "examples/catalog-contact/experiment.json": ("tests/test_catalog_contact.py",),
    "examples/catalog-contact/prepare.py": ("tests/test_catalog_contact.py",),
    "examples/known-entities/physical-units.json": (
        "tests/test_reference_units.py",
        "tests/test_catalog_contact.py",
    ),
    "examples/quantum/many_contacts.json": ("tests/test_many_contacts.py",),
    "examples/quantum/many_contacts.py": ("tests/test_many_contacts.py",),
    "examples/quantum/many_contacts_view.py": ("tests/test_many_contacts.py",),
    "examples/quantum/event_paths.json": ("tests/test_quantum_node_events.py",),
    "examples/quantum/wave_origins.json": ("tests/test_native_wave_origins.py",),
    "examples/quantum/causal_interference.py": ("tests/test_causal_interference.py",),
    "examples/quantum/crossing_nulls.py": ("tests/test_null_notices.py",),
    "examples/quantum/bell_chsh.py": ("tests/test_bell_chsh.py",),
    "examples/quantum/bell_chsh.json": ("tests/test_bell_chsh.py",),
    "examples/quantum/bell_chsh_view.py": ("tests/test_bell_chsh.py",),
    "examples/gallery/particle_gallery.py": ("tests/test_particle_gallery.py",),
    "examples/gallery/lepton_reactions.json": ("tests/test_particle_gallery.py",),
    "examples/isotropy-probe/run_experiments.py": ("tests/test_isotropy_probe.py",),
    "examples/particle-contracts/electron-positron.json": ("tests/test_particle_gallery.py",),
    "examples/quantum/causal_charge.json": (
        "tests/test_causal_contact_fields.py",
        "tests/test_catalog_contact.py",
        "tests/test_contact_profile_composition.py",
        "tests/test_causal_interference.py",
        "tests/test_null_notices.py",
        "tests/test_field_phase.py",
        "tests/test_funded_envelope.py",
    ),
    "examples/node-vector/six-records.json": (
        "tests/test_node_vector_examples.py",
        "tests/test_node_vector_integration.py",
    ),
    "examples/node-vector/two-fields.json": (
        "tests/test_node_vector_examples.py",
        "tests/test_node_vector_integration.py",
    ),
    "examples/known-entities/property-coupling-probes.json": ("tests/test_property_entity_profiles.py",),
    "examples/coupled-excitations/law.json": ("tests/test_coupled_excitations.py",),
    "examples/coupled-excitations/definition.json": ("tests/test_coupled_excitations.py",),
    "examples/coupled-excitations/experiments.json": ("tests/test_coupled_excitations.py",),
    "examples/coupled-excitations/prepare.py": ("tests/test_coupled_excitations.py",),
    "examples/inverse-square/run_experiments.py": ("tests/test_inverse_square_experiments.py",),
    "examples/gravity-probe/run_experiments.py": (
        "tests/test_gravity_probe.py",
        "tests/test_gathered_gravity.py",
    ),
    "examples/particle-interactions/run_experiments.py": ("tests/test_particle_interactions.py",),
    "examples/quantum-classical/run_experiments.py": ("tests/test_quantum_classical.py",),
    "examples/kerengonen-double-slit/run_experiments.py": ("tests/test_kerengonen.py",),
    "examples/kerengonen-bell/run_experiments.py": ("tests/test_kerengonen_bell.py",),
    "examples/de-broglie/run_experiments.py": ("tests/test_de_broglie.py",),
    "examples/matter-wave/run_experiments.py": (
        "tests/test_matter_wave.py",
        "tests/test_claim_gather.py",
    ),
    "examples/kerengonen-mirror/run_experiments.py": ("tests/test_kerengonen_mirror.py",),
    "examples/euclidean-pace/run_experiments.py": ("tests/test_euclidean_pace.py",),
    "examples/claim-gather/run_experiments.py": ("tests/test_claim_gather.py",),
    "examples/bell-chsh/run_experiments.py": ("tests/test_ray_bell_chsh.py",),
    "examples/gathered-gravity/run_experiments.py": ("tests/test_gathered_gravity.py",),
    "examples/directional-wave/law.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/definition.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/experiments.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/prepare.py": ("tests/test_directional_wave.py",),
    "examples/directional-wave/observe.py": ("tests/test_directional_wave.py",),
    "examples/maxwell/configuration.py": ("tests/test_maxwell_configuration.py",),
    "examples/maxwell/measurements.py": ("tests/test_maxwell_configuration.py",),
    "examples/local_lorentz_field.json": (
        "tests/test_node_state_contract.py",
        "tests/test_local_lorentz_field.py",
    ),
    "examples/quantum/interference.json": (
        "tests/test_native_quantum_channels.py",
        "tests/test_quantum_classical_experiment.py",
    ),
    "examples/quantum/phase_reversal.json": ("tests/test_native_quantum_channels.py",),
    "examples/quantum/dephasing.json": ("tests/test_native_quantum_channels.py",),
    "examples/quantum/partial_dephasing.json": (
        "tests/test_native_quantum_channels.py",
        "tests/test_quantum_classical_experiment.py",
    ),
    "examples/quantum/run_physics_checks.py": (
        "tests/test_native_quantum_channels.py",
        "tests/test_quantum_classical_experiment.py",
    ),
    "examples/known-entities/catalog.json": (
        "tests/test_catalog_contact.py",
        "tests/test_property_entity_profiles.py",
        "tests/test_entity_catalog.py",
        "tests/test_profile_validation.py",
        "tests/test_entity_compiler.py",
        "tests/test_physical_entities.py",
        "tests/test_quantum_entities.py",
        "tests/test_native_quantum_channels.py",
    ),
    "examples/known-entities/representation-probes.json": (
        "tests/test_profile_validation.py",
        "tests/test_entity_compiler.py",
        "tests/test_quantum_entities.py",
        "tests/test_native_quantum_channels.py",
    ),
    "examples/quantum/contact.json": (
        "tests/test_native_event_runtime.py",
        "tests/test_quantum_contact_trial.py",
    ),
    "examples/quantum/native_classical.json": ("tests/test_native_event_runtime.py",),
    "examples/spatial_causal_events.json": ("tests/test_spatial_causal_events.py",),
    "examples/quantum/native_quantum.json": ("tests/test_native_event_runtime.py",),
    "examples/quantum/native_reflection.json": ("tests/test_native_event_runtime.py",),
    "examples/quantum/native_cost_delay.json": ("tests/test_native_event_runtime.py",),
    "examples/basic.json": ("tests/test_generic_identity.py",),
    "examples/exchange.json": ("tests/test_generic_identity.py",),
    "examples/finite_fields.json": ("tests/test_generic_identity.py",),
    "examples/open_world.json": ("tests/test_generic_identity.py",),
    "examples/spatial_turning.json": ("tests/test_generic_identity.py",),
    "examples/04-unequal-mass-collision.json": ("tests/test_reference_examples.py",),
    "examples/three_mass_finite.json": ("tests/test_reference_examples.py",),
    "examples/known-entities/three-masses-low-budget.json": ("tests/test_reference_examples.py",),
    "examples/known-entities/boundary-periodic.json": ("tests/test_reference_examples.py",),
    "examples/known-entities/boundary-open.json": ("tests/test_reference_examples.py",),
    "examples/known-entities/run_reference_checks.py": ("tests/test_reference_examples.py",),
    "examples/known-entities/run_reference_checks.ps1": ("tests/test_reference_examples.py",),
    "tools/check_diagonal_motion.py": ("tests/test_legacy_application.py",),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, encoding="utf-8").strip()


def previous_sources(base):
    """Read the prior Python tree in two Git processes, including deleted providers."""
    listing = subprocess.check_output(
        ["git", "ls-tree", "-rz", base, "--", "src", "tests", "tools"], cwd=ROOT
    )
    entries = []
    for entry in listing.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        path = name.decode("utf-8")
        if path.endswith(".py") and "reference" not in Path(path).parts:
            entries.append((metadata.split()[2], path))
    if not entries:
        return {}
    payload = subprocess.check_output(
        ["git", "cat-file", "--batch"],
        input=b"".join(identity + b"\n" for identity, _ in entries),
        cwd=ROOT,
    )
    stream = io.BytesIO(payload)
    sources = {}
    for identity, path in entries:
        actual, kind, length = stream.readline().split()
        if actual != identity or kind != b"blob":
            raise ValueError("unexpected Git source object")
        content = stream.read(int(length))
        if len(content) != int(length) or stream.read(1) != b"\n":
            raise ValueError("incomplete Git source object")
        sources[path] = content.decode("utf-8")
    return sources


def module_name(path):
    parts = Path(path).with_suffix("").parts
    if parts[0] == "src":
        parts = parts[1:]
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def dependency_graph(sources):
    """Resolve local imports, re-exports and declared lazy export mappings."""
    modules = {module_name(path): path for path in sources}
    trees = {path: ast.parse(source, filename=path) for path, source in sources.items()}
    graph = {path: set() for path in sources}
    exports = {}
    for path, tree in trees.items():
        package = (
            module_name(path) if path.endswith("/__init__.py") else module_name(path).rpartition(".")[0]
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                prefix = (
                    package.split(".")[: len(package.split(".")) - node.level + 1] if node.level else []
                )
                target = ".".join([*prefix, *([node.module] if node.module else [])])
                for item in node.names:
                    exports[(module_name(path), item.asname or item.name)] = (target, item.name)
            # Public lazy imports are expressed as literal name -> relative module maps.
            if path.endswith("/__init__.py") and isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values, strict=True):
                    if (
                        isinstance(key, ast.Constant)
                        and isinstance(key.value, str)
                        and isinstance(value, ast.Constant)
                        and isinstance(value.value, str)
                        and value.value.startswith(".")
                    ):
                        exports[(module_name(path), key.value)] = (
                            module_name(path) + value.value,
                            key.value,
                        )

    def resolve(target, name, seen=None):
        seen = set() if seen is None else seen
        key = (target, name)
        if key in seen:
            return {modules[target]} if target in modules else set()
        seen.add(key)
        if target + "." + name in modules:
            return {modules[target + "." + name]}
        if key in exports:
            result = resolve(*exports[key], seen)
            # Retain the re-export file as an interface dependency, without
            # pulling unrelated exports into the consumer's dependency closure.
            return result | (
                {modules[target]}
                if target in modules and not target.endswith("event_universe")
                else set()
            )
        return {modules[target]} if target in modules else set()

    for path, tree in trees.items():
        package = (
            module_name(path) if path.endswith("/__init__.py") else module_name(path).rpartition(".")[0]
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                graph[path].update(modules[item.name] for item in node.names if item.name in modules)
            elif isinstance(node, ast.ImportFrom):
                prefix = (
                    package.split(".")[: len(package.split(".")) - node.level + 1] if node.level else []
                )
                target = ".".join([*prefix, *([node.module] if node.module else [])])
                for item in node.names:
                    graph[path].update(resolve(target, item.name))
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                # CLI subprocess module names are dependencies too.
                if node.value in modules:
                    graph[path].add(modules[node.value])
        graph[path].discard(path)
    return graph


def affected(changed, sources):
    graph = dependency_graph(sources)
    impacted = set(changed)
    while True:
        new = {path for path, dependencies in graph.items() if dependencies & impacted} - impacted
        if not new:
            break
        impacted.update(new)
    return impacted


def select(changed, sources):
    impacted = affected(changed, sources)
    tests = {p for p in impacted if p.startswith("tests/test_") and p.endswith(".py")}
    # Non-import dependencies: configuration, assets, repository scanners and fixtures.
    for path in changed:
        tests.update(RESOURCE_CONSUMERS.get(path, ()))
        if path.endswith(".json") and path.startswith(("examples/", "skills/")):
            tests.add("tests/test_configuration_validation.py")
        if path.startswith("examples/particle-contracts/"):
            tests.add("tests/test_rational_particles.py")
        if path.endswith(".md") or path == "MANIFEST.in":
            tests.add("tests/test_repository_navigation.py")
        # Paths and duplicate contents can change in any source file, not just Python.
        tests.update(("tests/test_repository_language.py", "tests/test_repository_hygiene.py"))
        if path.startswith("src/") and path.endswith(".py"):
            tests.update(("tests/test_architecture.py", "tests/test_locality.py"))
        if path.startswith(("src/event_universe/quantum/", "src/event_universe/integration/")):
            tests.add("tests/test_quantum_architecture.py")
        if path.startswith("examples/") or path.startswith("src/event_universe/ui_assets/"):
            tests.update(("tests/test_workspace.py", "tests/test_recorded_movie.py"))
            tests.update(
                p
                for p, text in sources.items()
                if p.startswith("tests/test_") and Path(path).name in text
            )
        if path.startswith("tools/") or path.startswith(".github/workflows/"):
            tests.add("tests/test_check_scope.py")
        if path in ("tests/conftest.py", "pyproject.toml", ".python-version"):
            # Shared fixtures, interpreter and package configuration affect all consumers.
            tests.update(p for p in sources if p.startswith("tests/test_"))
        if path == "src/event_universe/__init__.py":
            tests.update(
                p
                for p, text in sources.items()
                if p.startswith("tests/test_") and "event_universe" in text
            )
    return sorted(tests), sorted(
        p for p in impacted if p.startswith("src/") and p.endswith(".py") and p in sources
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base", default="origin/main", help="Compare against the merge base of this Git revision"
    )
    parser.add_argument(
        "--tests", nargs="*", default=[], help="Additional related pytest paths or node IDs"
    )
    parser.add_argument(
        "--full", action="store_true", help="Explicitly run the complete validation suite"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print selected checks without executing them"
    )
    args = parser.parse_args()
    for target in args.tests:
        if not (ROOT / target.split("::")[0]).exists():
            parser.error(f"additional test target does not exist: {target}")
    if args.full:
        commands = [
            ["ruff", "check", "."],
            ["ruff", "format", "--check", "."],
            ["mypy"],
            ["pytest", "--junitxml=artifacts/junit.xml"],
        ]
        changed = []
    else:
        base = git("merge-base", args.base, "HEAD")
        changed = sorted(
            set(git("diff", "--name-only", base).splitlines())
            | set(git("ls-files", "--others", "--exclude-standard").splitlines())
        )
        sources = {
            p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8")
            for directory in ("src", "tests", "tools")
            for p in ((ROOT / directory).rglob("*.py") if changed else ())
            if "reference" not in p.parts
        }
        # Include removed/old import edges so deletions and redirected imports retain consumers.
        previous = previous_sources(base) if changed else {}
        tests, typed = select(changed, sources) if changed else ([], [])
        old_tests, old_typed = select(changed, previous) if changed else ([], [])
        tests = sorted({*tests, *old_tests, *args.tests})
        tests = [p for p in tests if (ROOT / p.split("::")[0]).exists()]
        typed = sorted(p for p in {*typed, *old_typed} if (ROOT / p).exists())
        python = [p for p in changed if p.endswith(".py") and (ROOT / p).is_file()]
        if "pyproject.toml" in changed:
            python = ["."]
            typed = sorted(p for p in sources if p.startswith("src/"))
        commands = []
        if python:
            commands += [["ruff", "check", *python], ["ruff", "format", "--check", *python]]
        if typed:
            commands.append(["mypy", "--follow-imports=silent", *typed])
        if tests:
            commands.append(["pytest", *tests, "--junitxml=artifacts/junit.xml"])
        if {"pyproject.toml", "MANIFEST.in"} & set(changed):
            commands.append(["build"])
    report = {"mode": "full" if args.full else "affected", "changed": changed, "commands": commands}
    print(json.dumps(report, indent=2), flush=True)
    if not args.dry_run:
        from event_universe.retention import ArtifactLease, validate_output_path

        report_path = ROOT / "artifacts/check-scope.json"
        validate_output_path(report_path)
        report_path.parent.mkdir(exist_ok=True)
        report_path.touch(exist_ok=True)
        with ArtifactLease(report_path.parent, [report_path]):
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            for command in commands:
                subprocess.run([sys.executable, "-m", *command], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
