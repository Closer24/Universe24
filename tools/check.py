"""Validate changed files and their affected consumers; full validation is explicit."""

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# These consumers build resource paths at runtime rather than importing modules.
RESOURCE_CONSUMERS = {
    "examples/directional-wave/law.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/definition.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/experiments.json": ("tests/test_directional_wave.py",),
    "examples/directional-wave/prepare.py": ("tests/test_directional_wave.py",),
    "examples/directional-wave/observe.py": ("tests/test_directional_wave.py",),
    "examples/local_lorentz_field.json": (
        "tests/test_cell_state_contract.py",
        "tests/test_local_lorentz_field.py",
    ),
    "examples/small-space/experiments.py": ("tests/test_small_space_experiments.py",),
    "examples/small-space/source-pulse.json": ("tests/test_small_space_experiments.py",),
    "examples/small-space/source-response.json": ("tests/test_small_space_experiments.py",),
    "examples/known-entities/catalog.json": ("tests/test_small_space_experiments.py",),
    "examples/known-entities/discrete-pair.json": ("tests/test_small_space_experiments.py",),
    "examples/quantum/contact.json": (
        "tests/test_native_event_runtime.py",
        "tests/test_quantum_contact_trial.py",
    ),
    "examples/quantum/native_classical.json": ("tests/test_native_event_runtime.py",),
    "examples/quantum/native_quantum.json": ("tests/test_native_event_runtime.py",),
    "examples/quantum/native_reflection.json": ("tests/test_native_event_runtime.py",),
    "examples/quantum/native_cost_delay.json": ("tests/test_native_event_runtime.py",),
    "examples/basic.json": ("tests/test_generic_identity.py",),
    "examples/exchange.json": ("tests/test_generic_identity.py",),
    "examples/finite_fields.json": ("tests/test_generic_identity.py",),
    "examples/open_world.json": ("tests/test_generic_identity.py",),
    "examples/spatial_turning.json": ("tests/test_generic_identity.py",),
    "tools/check_diagonal_motion.py": ("tests/test_application.py",),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, encoding="utf-8").strip()


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
        if path.startswith("tools/generic_vector_lab/"):
            tests.add("tests/test_generic_vector_lab.py")
        tests.update(RESOURCE_CONSUMERS.get(path, ()))
        if path.endswith(".md") or path == "MANIFEST.in":
            tests.add("tests/test_repository_navigation.py")
        if path.endswith((".md", ".py", ".js", ".html", ".css", ".json")):
            tests.add("tests/test_repository_language.py")
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
            for p in (ROOT / directory).rglob("*.py")
            if "reference" not in p.parts
        }
        # Include removed/old import edges so deletions and redirected imports retain consumers.
        previous = {}
        for path in git("ls-tree", "-r", "--name-only", base, "src", "tests", "tools").splitlines():
            if path.endswith(".py") and "/reference/" not in path:
                previous[path] = git("show", f"{base}:{path}")
        tests, typed = select(changed, sources)
        old_tests, old_typed = select(changed, previous)
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
