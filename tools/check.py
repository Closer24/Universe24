"""Validate changed files and their affected consumers; full validation is explicit."""

import argparse
import ast
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# These consumers build resource paths at runtime rather than importing modules.
# Every row names a kept test; main() still skips a selected test that does not exist.
RESOURCE_CONSUMERS: dict[str, tuple[str, ...]] = {
    # The registers, worlds and generators a living test reads by path (the ray law's
    # rows were deleted with their tests on 2026-09-26, docs/CANCELLED_WORLDS.md).
    # The law document's words and links (#1198, gate 5).
    "docs/ALGEBRA.md": ("tests/test_law_words.py",),
}


EVERY_PULL_REQUEST = Path(__file__).with_name("every_pull_request.txt")


def every_pull_request() -> list[str]:
    """The tests selected on every pull request: the data file's lines, a line starting with # a note."""
    lines = EVERY_PULL_REQUEST.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


SECONDS = Path(__file__).with_name("test_seconds.json")
REGRESSION = "tests/test_shipped_worlds.py"
WORLD_TEST = "test_a_shipped_world_runs_bit_for_bit_as_recorded"
# a pull request touching none of these runs no world, so it skips the regression (the owner's word)
RUNS_A_WORLD = ("src/", "law/", "examples/", "tools/", "tests/shipped_worlds.json", REGRESSION)
# a pull request that adds one new folder under features/ with its own test file and touches nothing
# else runs that test alone and no world (the owner's word of 2026-09-27); anything existing touched
# (the loop, the loader, a folder that stands) keeps the suite's shards and the worlds
FEATURES = "src/event_universe/features/"
FOLDER_JOB = "folder "
SUITE_SHARDS, HEAVY_WORLDS, WORLD_SHARDS = 3, 3, 2
# the worlds replayed on every pull request that runs a world (the model owner, 2026-09-27); the
# whole record on a push to main, on the body's line "RECORD: all" or on the Boss's dispatch
RECORD_PLAN = Path(__file__).with_name("record_plan.json")
RECORD_ALL_LINE = re.compile(r"^\s*RECORD:\s*all\s*$", re.MULTILINE)
UNRECORDED_SECONDS = 5.0
LINT = [["ruff", "check", "."], ["ruff", "format", "--check", "."], ["mypy"]]


def balanced(seconds, count):
    """The names split into `count` groups of about equal seconds, the longest placed first."""
    groups, loads = [[] for _ in range(count)], [0.0] * count
    for name in sorted(seconds, key=lambda n: (-seconds[n], n)):
        lightest = loads.index(min(loads))
        groups[lightest].append(name)
        loads[lightest] += seconds[name]
    return [sorted(group) for group in groups]


def every_world_planned() -> bool:
    """Whether the whole record replays: the environment's RECORD_ALL (a push to main, a dispatch
    for the whole) or the pull request's body carrying the line "RECORD: all"."""
    return os.environ.get("RECORD_ALL", "").lower() == "true" or bool(
        RECORD_ALL_LINE.search(os.environ.get("PR_BODY", ""))
    )


def shards(runs_worlds, every_world=None):
    """The CI jobs by name, each its pytest targets: the suite in equal parts, and where a world
    runs, the heaviest shipped worlds each alone and the rest in equal parts; on a pull request
    the worlds of tools/record_plan.json alone unless the whole record is planned."""
    if every_world is None:
        every_world = every_world_planned()
    table = json.loads(SECONDS.read_text(encoding="utf-8"))
    files = sorted(
        p.relative_to(ROOT).as_posix()
        for p in (ROOT / "tests").glob("test_*.py")
        if p.relative_to(ROOT).as_posix() != REGRESSION
    )
    suite = {f: table["files"].get(f, UNRECORDED_SECONDS) for f in files}
    plan = {f"suite {i + 1}": group for i, group in enumerate(balanced(suite, SUITE_SHARDS))}
    if not runs_worlds:
        return plan
    record = json.loads((ROOT / "tests/shipped_worlds.json").read_text(encoding="utf-8"))
    planned = json.loads(RECORD_PLAN.read_text(encoding="utf-8"))["every_pull_request"]
    names = record["worlds"] if every_world else [w for w in record["worlds"] if w in planned]
    worlds = {w: table["worlds"].get(w, UNRECORDED_SECONDS) for w in names}
    heavy = sorted(worlds, key=lambda w: (-worlds[w], w))[:HEAVY_WORLDS]
    for world in heavy:
        plan[f"world {Path(world).parent.name}/{Path(world).stem}"] = [
            f"{REGRESSION}::{WORLD_TEST}[{world}]"
        ]
    rest = {w: s for w, s in worlds.items() if w not in heavy}
    tree = ast.parse((ROOT / REGRESSION).read_text(encoding="utf-8"))
    others = [
        f"{REGRESSION}::{node.name}"
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name.startswith("test_")
        and node.name != WORLD_TEST
    ]
    for i, group in enumerate(balanced(rest, WORLD_SHARDS)):
        plan[f"worlds {i + 1}"] = (others if i == 0 else []) + [
            f"{REGRESSION}::{WORLD_TEST}[{w}]" for w in group
        ]
    return plan


def own_test(name):
    """The test file of a folder under features/, by the folder's name."""
    return f"tests/test_feature_{name}.py"


def new_folder_alone(touched, base):
    """The one new folder under features/ a pull request adds with its own test file and nothing else,
    else None: the folder absent at the merge base, every touched path the folder's or its test's."""
    names = {Path(p).relative_to(FEATURES).parts[0] for p in touched if p.startswith(FEATURES)}
    if len(names) != 1:
        return None
    (name,) = names
    folder, test = FEATURES + name + "/", own_test(name)
    if test not in touched or any(not p.startswith((folder, test)) for p in touched):
        return None
    return None if git("ls-tree", base, "--", folder) else name


def jobs(touched, base):
    """The CI jobs of a pull request: a new folder's own test alone, else the suite's shards with
    the worlds where a world path is touched."""
    name = new_folder_alone(touched, base)
    if name is not None:
        return {FOLDER_JOB + name: [own_test(name)]}
    return shards(any(p.startswith(RUNS_A_WORLD) for p in touched))


def shard_commands(shard):
    """One CI job's commands: a new folder's job lints the folder with its test and runs that test
    alone; suite 1 lints the tree; every job runs its targets."""
    junit = "--junitxml=artifacts/junit.xml"
    if shard.startswith(FOLDER_JOB):
        name = shard.removeprefix(FOLDER_JOB)
        paths = [FEATURES + name, own_test(name)]
        return [
            ["ruff", "check", *paths],
            ["ruff", "format", "--check", *paths],
            ["mypy", "--follow-imports=silent", paths[0]],
            ["pytest", "-n", "auto", paths[1], junit],
        ]
    targets = shards(runs_worlds=True)[shard]
    return (LINT if shard == "suite 1" else []) + [["pytest", "-n", "auto", *targets, junit]]


def record_seconds(junit):
    """The seconds per test file and per shipped world read from a junit file, written to the table."""
    import xml.etree.ElementTree as ElementTree

    files, worlds = {}, {}
    for case in ElementTree.parse(junit).getroot().iter("testcase"):
        path, name, seconds = (
            case.get("classname", "").replace(".", "/") + ".py",
            case.get("name", ""),
            float(case.get("time", 0)),
        )
        if path == REGRESSION and name.startswith(WORLD_TEST + "["):
            worlds[name[len(WORLD_TEST) + 1 : -1]] = round(seconds, 1)
        else:
            files[path] = round(files.get(path, 0.0) + seconds, 1)
    table = json.loads(SECONDS.read_text(encoding="utf-8"))
    table.update(files=dict(sorted(files.items())), worlds=dict(sorted(worlds.items())))
    SECONDS.write_text(json.dumps(table, indent=1) + "\n", encoding="utf-8")


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
    if changed:
        # the gates every pull request runs, whatever it changes: one per line in one data file
        tests.update(every_pull_request())
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
        base = git("merge-base", args.base, "HEAD")
        touched = git("diff", "--name-only", base).splitlines()
        print("shards=" + json.dumps(list(jobs(touched, base))))
        return
    for target in args.tests:
        if not (ROOT / target.split("::")[0]).exists():
            parser.error(f"additional test target does not exist: {target}")
    if args.shard:
        commands = shard_commands(args.shard)
        changed = []
    elif args.full:
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
        for command in commands:
            subprocess.run([sys.executable, "-m", *command], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
