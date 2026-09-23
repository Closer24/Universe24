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
# Every row names a kept test; main() still skips a selected test that does not exist.
RESOURCE_CONSUMERS: dict[str, tuple[str, ...]] = {
    "examples/events/README.md": ("tests/test_nature_beam_worlds.py",),
    # The registers a test reads a world's numbers from (2026-09-21).
    "examples/events/expectations.json": ("tests/test_nature_beam_worlds.py",),
    "examples/events/bell/expectations.json": ("tests/test_nature_beam_worlds.py",),
    "examples/events/amplitude/expectations.json": (
        "tests/test_amplitude_bell_24_4.py",
        "tests/test_amplitude_cone.py",
        "tests/test_amplitude_gate.py",
        "tests/test_amplitude_layer.py",
        "tests/test_amplitude_malus.py",
        "tests/test_amplitude_mz_345_n.py",
        "tests/test_amplitude_pair.py",
        "tests/test_amplitude_split.py",
    ),
    "examples/events/c_measured/expectations.json": ("tests/test_c_measured.py",),
    "examples/events/c_measured/c_measured.json": ("tests/test_c_measured.py",),
    # The massive rows' register, worlds and generators (2026-09-21): the
    # test that reads the pin, the byte-identity digests and the replay.
    "examples/events/massive_rows/expectations.json": ("tests/test_massive_rows.py",),
    "examples/events/massive_rows/make_worlds.py": ("tests/test_massive_rows.py",),
    "tools/click_readings/massive_rows_replay.py": ("tests/test_massive_rows.py",),
    "examples/events/massive_rows/slits_matter.json": ("tests/test_massive_rows.py",),
    "examples/events/massive_rows/slits_matter_1024.json": ("tests/test_massive_rows.py",),
    "examples/events/massive_rows/slits_matter_small.json": ("tests/test_massive_rows.py",),
    # Side A of Newton on the side (2026-09-23): the worlds, the register and
    # the generator the reading tool's test pins.
    "examples/events/newton_side/expectations.json": ("tests/test_newton_side_readings.py",),
    "examples/events/newton_side/make_worlds.py": ("tests/test_newton_side_readings.py",),
    "examples/events/newton_side/control.json": ("tests/test_newton_side_readings.py",),
    "examples/events/newton_side/mass.json": ("tests/test_newton_side_readings.py",),
    "examples/events/newton_side/light.json": ("tests/test_newton_side_readings.py",),
    "examples/events/gate_set.json": (
        "tests/test_nature_beam_worlds.py",
        "tests/test_amplitude_click.py",
        "tests/test_massive_rows.py",
        "tests/test_drive_b.py",
    ),
    # The drive-b register, worlds and generator (2026-09-22): the test that
    # reads the pins and replays the deciding worlds.
    "examples/events/drive_b/expectations.json": ("tests/test_drive_b.py",),
    "examples/events/drive_b/make_worlds.py": ("tests/test_drive_b.py",),
    "examples/events/detector/entities/detectors.json": (
        "tests/test_entity_definitions.py",
        "tests/test_configuration_validation.py",
        "tests/test_entity_loading_consumers.py",
    ),
    # The shipped worlds take their families from `families.json` since
    # 2026-09-20: every test that loads a shipped world depends on it.
    "examples/events/entities/families.json": (
        "tests/test_entity_definitions.py",
        "tests/test_configuration_validation.py",
        "tests/test_nature_beam_worlds.py",
        "tests/test_bell_choosers.py",
        "tests/test_entity_loading_consumers.py",
        "tests/test_amplitude_layer.py",
        "tests/test_amplitude_click.py",
    ),
    "examples/events/entities/apparatus.json": ("tests/test_entity_definitions.py",),
    # The weak register and its generator: the tests that derive or replay
    # their entries (J2 from the flight table, J1 and J3 from the warm runs).
    "examples/events/weak/expectations.json": ("tests/test_weak_readings.py",),
    "examples/events/weak/make_worlds.py": ("tests/test_weak_readings.py",),
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
        if path.endswith(".md") or path == "MANIFEST.in":
            tests.add("tests/test_repository_navigation.py")
        # Paths and duplicate contents can change in any source file, not just Python.
        tests.update(("tests/test_repository_language.py", "tests/test_repository_hygiene.py"))
        if path.startswith("src/") and path.endswith(".py"):
            tests.add("tests/test_architecture.py")
            # The algebra gate reads the physical modules by their path.
            tests.add("tests/test_integer_algebra.py")
        # A world, an asset or a tool is a runtime dependency of the tests
        # that name its file (a tool is loaded by its path, never imported).
        if path.startswith(("examples/", "tools/")):
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
            ["pytest", "-n", "auto", "--junitxml=artifacts/junit.xml"],
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
            commands.append(["pytest", "-n", "auto", *tests, "--junitxml=artifacts/junit.xml"])
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
