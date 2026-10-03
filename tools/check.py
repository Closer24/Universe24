"""Validate changed files and their affected consumers; full validation is explicit."""

import argparse
import ast
import io
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVERY_PULL_REQUEST = Path(__file__).with_name("every_pull_request.txt")


def every_pull_request() -> list[str]:
    """The tests selected on every pull request: the data file's lines, a line starting with # a note."""
    lines = EVERY_PULL_REQUEST.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


SECONDS = Path(__file__).with_name("test_seconds.json")
# no world replays in CI (the owner's decision of 2026-09-27: the worlds recorded on the earlier
# engine are no reference for this one); the plan is the test suite alone, its test functions in
# equal shards (the owner's ceiling of 2026-10-02: every CI run ends under ten minutes)
SUITE_SHARDS = 5
UNRECORDED_SECONDS = 5.0
# the suite's bound (the owner's word of 2026-10-03: a test runs under 30 seconds): a test function above
# it fails the plan by name, on the recorded table at --plan and on the run's own junit after every pytest
TEST_SECONDS_BOUND = 30.0
LINT = [["ruff", "check", "."], ["ruff", "format", "--check", "."], ["mypy"]]
# the ratchets against the merge base (CHECK_BASE, the `--base` revision), each one script of
# tools/ run by its path and failing with its own message: on every selection, with --full and
# in the lint shard
RATCHETS = [
    ["tools/engine_gates.py"],
    ["tools/record_code_shape.py"],
    ["tools/tests_shape.py"],
    ["tools/ownership.py"],
]


def balanced(seconds, count):
    """The names split into `count` groups of about equal seconds, the longest placed first; the
    groups from the heaviest to the lightest."""
    groups, loads = [[] for _ in range(count)], [0.0] * count
    for name in sorted(seconds, key=lambda n: (-seconds[n], n)):
        lightest = loads.index(min(loads))
        groups[lightest].append(name)
        loads[lightest] += seconds[name]
    return [sorted(group) for _, group in sorted(zip(loads, groups, strict=True), key=lambda x: -x[0])]


def recorded_seconds():
    """The test files and the table's seconds per test function the files still hold
    (`tests/<file>.py::<function>`; a name a file no longer has is left out)."""
    table = json.loads(SECONDS.read_text(encoding="utf-8"))
    files = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py"))
    recorded = {}
    for file in files:
        text = (ROOT / file).read_text(encoding="utf-8")
        for target, seconds in table["tests"].items():
            if target.startswith(file + "::") and f"\ndef {target.partition('::')[2]}(" in text:
                recorded[target] = seconds
    return files, recorded


def shards():
    """The CI jobs by name, each its pytest arguments: the suite's test functions in equal parts by
    their recorded seconds (`tests/<file>.py::<function>`, its parametrizations with it); a file runs
    whole in the part of its longest function, less the functions placed elsewhere (`--deselect`), so
    a function the table does not hold, or holds under a name the file no longer has, runs with its
    file; the parts from the heaviest to the lightest, the lint in the last; no world job."""
    files, recorded = recorded_seconds()
    whole = {file: UNRECORDED_SECONDS for file in files}  # the file's own target: its other tests
    for target in sorted(recorded, key=lambda t: recorded[t]):
        whole[target.partition("::")[0]] = target  # the file stands with its longest function
    plain = {f: s for f, s in whole.items() if not isinstance(s, str)}
    jobs = {}
    for i, group in enumerate(balanced({**recorded, **plain}, SUITE_SHARDS)):
        held = set(group)
        arguments = []
        for target in group:
            file, _, name = target.partition("::")
            if name and whole[file] in held and whole[file] != target:
                continue  # the file runs whole in this part, this function with it
            if name and whole[file] != target:
                arguments.append(target)
                continue
            arguments.append(file)  # the file whole, less its functions placed in other parts
            for other in sorted(recorded):
                if other.startswith(file + "::") and other not in held:
                    arguments += ["--deselect", other]
        if arguments:
            jobs[f"suite {i + 1}"] = arguments
    return jobs


def seconds_of(junit):
    """The seconds per test function read from a junit file (`tests/<file>.py::<function>`, its
    parametrizations summed)."""
    import xml.etree.ElementTree as ElementTree

    tests = {}
    for case in ElementTree.parse(junit).getroot().iter("testcase"):
        path = case.get("classname", "").replace(".", "/") + ".py"
        target = path + "::" + case.get("name", "").partition("[")[0]  # the function, its parts summed
        tests[target] = round(tests.get(target, 0.0) + float(case.get("time", 0)), 1)
    return tests


def record_seconds(junit):
    """The seconds per test function read from a junit file, written to the table."""
    table = json.loads(SECONDS.read_text(encoding="utf-8"))
    table.update(tests=dict(sorted(seconds_of(junit).items())))
    SECONDS.write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")


def above_the_bound(seconds, clock):
    """The test functions above the suite's bound on the `clock` named, each with its seconds, the
    slowest first; the message that fails the plan by name, or None."""
    slow = sorted(((n, s) for n, s in seconds.items() if s > TEST_SECONDS_BOUND), key=lambda x: -x[1])
    if not slow:
        return None
    names = ", ".join(f"{name} ({seconds:.1f} s)" for name, seconds in slow)
    return f"above the bound of {TEST_SECONDS_BOUND:.0f} seconds per test on {clock}: {names}"


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
        if path.startswith("src/") and path.endswith(".py"):
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
        if path in ("tests/conftest.py", "pyproject.toml", ".python-version"):
            # Shared fixtures, interpreter and package configuration affect all consumers.
            tests.update(p for p in sources if p.startswith("tests/test_"))
        if path == "src/event_universe/__init__.py":
            tests.update(
                p
                for p, text in sources.items()
                if p.startswith("tests/test_") and "event_universe" in text
            )
    if changed:
        # the gates every pull request runs, whatever it changes: one per line in one data file
        tests.update(every_pull_request())
    return sorted(tests), sorted(
        p for p in impacted if p.startswith("src/") and p.endswith(".py") and p in sources
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=os.environ.get("CHECK_BASE") or "origin/main",
        help="Compare against the merge base of this Git revision (CHECK_BASE, else origin/main)",
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
    parser.add_argument(
        "--plan", action="store_true", help="Print the CI jobs as a GitHub output line and exit"
    )
    parser.add_argument("--shard", help="Run one CI job of the plan: the whole suite in parts")
    parser.add_argument("--record-seconds", metavar="JUNIT", help="Re-record tools/test_seconds.json")
    args = parser.parse_args()
    if args.record_seconds:
        record_seconds(args.record_seconds)
        return
    if args.plan:
        slow = above_the_bound(recorded_seconds()[1], "the recorded clock of tools/test_seconds.json")
        if slow:
            sys.exit(slow)
        print("shards=" + json.dumps(list(shards())))
        return
    for target in args.tests:
        if not (ROOT / target.split("::")[0]).exists():
            parser.error(f"additional test target does not exist: {target}")
    if args.shard:
        targets = shards()[args.shard]  # the lint and the ratchets run in the lightest part, the last
        commands = (LINT + RATCHETS if args.shard == list(shards())[-1] else []) + [
            ["pytest", "-n", "auto", *targets, "--junitxml=artifacts/junit.xml"]
        ]
        changed = []
    elif args.full:
        commands = [*LINT, *RATCHETS, ["pytest", "-n", "auto", "--junitxml=artifacts/junit.xml"]]
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
        if changed:
            commands += RATCHETS  # the gates every pull request runs, whatever it changes
        if tests:
            commands.append(["pytest", "-n", "auto", *tests, "--junitxml=artifacts/junit.xml"])
        if {"pyproject.toml", "MANIFEST.in"} & set(changed):
            commands.append(["build"])
    report = {
        "mode": args.shard or ("full" if args.full else "affected"),
        "changed": changed,
        "commands": commands,
    }
    print(json.dumps(report, indent=2), flush=True)
    if not args.dry_run:
        report_path = ROOT / "artifacts/check-scope.json"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        environment = {**os.environ, "CHECK_BASE": args.base}
        for command in commands:
            # a script of tools/ runs by its path, a package by its module name
            run = (
                [sys.executable, *command]
                if command[0].endswith(".py")
                else [sys.executable, "-m", *command]
            )
            subprocess.run(run, cwd=ROOT, env=environment, check=True)
            if command[0] == "pytest":  # the suite's bound on this run's own clock, by name
                slow = above_the_bound(seconds_of(ROOT / "artifacts/junit.xml"), "this run's clock")
                if slow:
                    sys.exit(slow)


if __name__ == "__main__":
    main()
