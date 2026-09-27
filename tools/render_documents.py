"""The documents that are rendered from the tree, never written by hand (the owner, 2026-09-27).

Two pages are rendered into docs/generated/ and compared by tests/test_documents.py on every
pull request: FILES.md, the keys of the run's files from the frame's schemas and the folders'
cards; STATUS.md, the primitives from the register, the step file's acts, the expected failures
of the tests with their reasons, the owners' map and the shipped worlds. Two pages are rendered
on demand from git and printed: the history (every commit on the first parent of the branch, by
day) and the decisions (each line of HIGHLIGHTS.md with the date of its last change). The same
module checks the hand-written documents against the tree: every path a document cites in
backticks exists, and a decision line naming a path that does not exist says "ahead of the tree".

    PYTHONPATH=src python tools/render_documents.py            # write docs/generated/
    PYTHONPATH=src python tools/render_documents.py --check    # the documents against the tree
    PYTHONPATH=src python tools/render_documents.py --history  # the history, printed
    PYTHONPATH=src python tools/render_documents.py --decisions
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from event_universe.core.readings import SCHEMA as READING_KINDS
from event_universe.core.register import Declaration, discover
from event_universe.core.schema import (
    Either,
    Flag,
    Integer,
    IntegerName,
    Kind,
    ListOf,
    MapOf,
    Name,
    ObjectOf,
    OneOf,
    Word,
)
from event_universe.core.step import STEP_FILE, read_step
from event_universe.loader import cards, frame
from event_universe.world_files import input_digest

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "docs" / "generated"
HAND_WRITTEN = (
    "docs/ALGEBRA.md",
    "docs/ENGINE.md",
    "docs/HIGHLIGHTS.md",
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
)
PACKAGE = "src/event_universe"
# a path under these is written by a run, never in the tree
RUN_FOLDERS = ("artifacts/", "runs/")
SUFFIXES = (".py", ".md", ".json", ".yml", ".txt", ".svg", ".toml", ".cff")
# a branch name or a remote's ref cited in a Git example, never a path of the tree
GIT_REFS = ("origin/", "feature/", "exp/")
SHIPPED_OUTPUT = "examples/events/massive_record/light_clock.output.json"
AHEAD = "ahead of the tree"
CITED = re.compile(r"`([^`\n]+)`")
PATH_TOKEN = re.compile(r"[\w./-]+")
LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
HEADER = "<!-- rendered by tools/render_documents.py from the tree; do not edit by hand -->\n"


def kind_text(kind: Kind) -> str:
    """One kind of the schema in English."""
    if isinstance(kind, Integer):
        text = "an integer"
        if kind.least is not None:
            text += f" from {bound_text(kind.least)}"
        if kind.most is not None:
            text += f" through {bound_text(kind.most)}"
        return text
    if isinstance(kind, Flag):
        return "true or false"
    if isinstance(kind, OneOf):
        return "one of " + ", ".join(f"`{choice}`" for choice in kind.choices)
    if isinstance(kind, Word):
        return "a word"
    if isinstance(kind, Name):
        return "a family's name"
    if isinstance(kind, IntegerName):
        return "the name of one of the universe's integers"
    if isinstance(kind, ListOf):
        inner = kind_text(kind.of)
        return f"a list of {kind.length}, each {inner}" if kind.length else f"a list, each {inner}"
    if isinstance(kind, ObjectOf):
        keys = ", ".join(
            f"`{key}` ({kind_text(value)}{', optional' if key in kind.optional else ''})"
            for key, value in kind.keys.items()
        )
        return f"an object with {keys}"
    if isinstance(kind, MapOf):
        return f"an object mapping {kind_text(kind.keys)} to {kind_text(kind.of)}"
    if isinstance(kind, Either):
        return " or ".join(kind_text(option) for option in kind.kinds)
    raise TypeError(f"{kind!r} is no kind of the schema")


def bound_text(bound: int | str) -> str:
    """A bound as written, or the universe's integer it names."""
    return f"the universe's `{bound}`" if isinstance(bound, str) else str(bound)


def table(header: tuple[str, ...], rows: Sequence[tuple[str, ...]]) -> str:
    """A markdown table."""
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines) + "\n"


def object_rows(shape: ObjectOf, owners: dict[str, str] | None = None) -> list[tuple[str, ...]]:
    """One row per key of an object: the key, required or optional, its kind, and its owner where given."""
    rows: list[tuple[str, ...]] = []
    for key, kind in shape.keys.items():
        row: tuple[str, ...] = (
            f"`{key}`",
            "optional" if key in shape.optional else "required",
            kind_text(kind),
        )
        if owners is not None:
            row += (owners.get(key, "the frame"),)
        rows.append(row)
    return rows


def files_page() -> str:
    """FILES.md: the keys of the run's files from the schemas and the cards."""
    register = discover()
    owners = cards.owners(register)["a family's entry"]
    keys = ("key", "required", "kind")
    out = [
        HEADER,
        "# The run's files, key by key\n",
        "The kinds are the frame's schemas (`src/event_universe/loader/frame.py`) and the folders'"
        " cards; a key the frame does not name and no card declares is refused by name. The rules"
        " between keys (a key admitted only with another) stay in the loader's prose"
        " (docs/ENGINE.md, section 4).\n",
        "## The world file\n",
        table(keys, object_rows(frame.WORLD)),
        "\nHanded on as written to their readers, once the world's own keys are checked:\n",
        table(
            ("key", "required", "what it holds"),
            [
                ("`universe`", "required", "the repository path of the universe file"),
                ("`measured`", "required", "the bodies, each in one of the two forms below"),
                ("`detectors`", "required", "the detectors, below"),
                ("`readings`", "optional", "the readings, below"),
                ("`twist_table`", "optional", "an inline world's twist table, the universe file's form"),
            ],
        ),
        "\n### A body by its position (today's form)\n",
        table(keys, object_rows(frame.BODY)),
        "\n### A body's emitter\n",
        table(keys, object_rows(frame.EMITTER)),
        "\n### A body by its Nodes (the law's form)\n",
        table(keys, object_rows(frame.COUNTED)),
        "\n### A detector\n",
        table(keys, object_rows(frame.DETECTOR)),
        "\n### A reading\n",
        "Every reading has a `name` and a `kind`; the kind takes its own keys"
        " (`src/event_universe/core/readings.py`).\n",
        table(
            ("kind", "label", "its keys"),
            [
                (f"`{kind}`", label, ", ".join(f"`{k}`" for k in keys))
                for kind, (label, keys) in READING_KINDS.items()
            ],
        ),
        "\n## The universe file\n",
        f"Two keys: {', '.join(f'`{key}`' for key in frame.UNIVERSE_KEYS)}.\n",
        "\n### The integers\n",
        table(keys, object_rows(frame.INTEGERS)),
        "\n### A family's entry\n",
        "Each key beyond the frame's is one folder's, declared on its card.\n",
        table(keys + ("declared by",), object_rows(frame.entry_kind(register), owners)),
        "\n## The start file\n",
        table(keys, object_rows(frame.START)),
        "\n## The step file\n",
        f"`{STEP_FILE}`: an object with the one key `interval`, a list of acts, each"
        " `[place, name]` or `[place, name, words]`, a primitive's name at its declared place with"
        " the words of its call; a name has one place; no act twice. The acts as the file lists"
        " them today are in STATUS.md.\n",
        "\n## The pins file\n",
        "An object keyed by the input's file stem; each pin has a `detector`, one of `count`,"
        " `first_click` or `mean_interval`, and a `band`; passed to `tools/run_inputs.py` with"
        " `--pins`, refused under the mode `check`, required under `pin`.\n",
        "\n## The output file\n",
        output_section(),
    ]
    return "\n".join(out)


def output_section() -> str:
    """The keys of the shipped output file, as one run wrote them."""
    path = ROOT / SHIPPED_OUTPUT
    document = json.loads(path.read_text(encoding="utf-8"))
    rows = [(f"`{key}`", value_text(value)) for key, value in sorted(document.items())]
    clicks = document.get("clicks") or [{}]
    click_rows = [(f"`{key}`", value_text(value)) for key, value in sorted(clicks[0].items())]
    return (
        f"One file per world, `<name>.output.json`, as `{SHIPPED_OUTPUT}` shows it"
        f" ({document.get('ticks')} intervals, the verdict `{document.get('verdict')}`).\n\n"
        + table(("key", "in the shipped output"), rows)
        + "\nEach click:\n\n"
        + table(("key", "in the first click"), click_rows)
    )


def value_text(value: object) -> str:
    """A JSON value's shape in a few words."""
    if isinstance(value, dict):
        return "an object with " + ", ".join(f"`{key}`" for key in value) if value else "an empty object"
    if isinstance(value, list):
        return f"a list of {len(value)}" if value else "an empty list"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return f"the integer {value}"
    return f"`{value}`"


def how_it_runs(declaration: Declaration) -> str:
    """How the loop reaches a primitive today."""
    if declaration.function is not None and declaration.binder is None:
        return "its own `apply`"
    if declaration.binder is not None and declaration.function is not None:
        return "bound through the loop's `bind`; its own `apply` waits"
    if declaration.binder is not None:
        return "bound through the loop's `bind`"
    return "not built"


def status_page() -> str:
    """STATUS.md: the primitives, the step file's acts, the expected failures, the owners, the shipped worlds."""
    register = discover()
    owners = cards.owners(register)
    keys_of: dict[str, list[str]] = {name: [] for name in register.names}
    for place, declared in owners.items():
        for key, name in declared.items():
            keys_of[name].append(f"`{key}` ({place})")
    built = register.built_names()
    own = [
        n
        for n in built
        if register.declarations[n].function is not None and register.declarations[n].binder is None
    ]
    rows = [
        (
            f"**{name}**",
            declaration.place,
            declaration.word or "",
            how_it_runs(declaration),
            ", ".join(keys_of[name]) or "",
            declaration.section,
        )
        for name, declaration in register.declarations.items()
    ]
    document = json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8"))
    step = read_step(document, input_digest(document))
    acts = [
        (
            str(index),
            place,
            name,
            json.dumps(dict(words)) if words else "",
            "yes" if name in built else "no",
        )
        for index, (place, name, words) in enumerate(step.acts)
    ]
    owners_map = json.loads((ROOT / "tools" / "owners.json").read_text(encoding="utf-8"))
    record = json.loads((ROOT / "tests" / "shipped_worlds.json").read_text(encoding="utf-8"))
    out = [
        HEADER,
        "# The state of the engine\n",
        "## The primitives\n",
        f"{len(register.names)} folders under `src/event_universe/features/`: {len(built)} built,"
        f" {len(own)} of them running their own code; {len(register.names) - len(built)} not built."
        " The register reads every card at load; a term of the files naming an unbuilt primitive is"
        " refused.\n",
        table(
            (
                "primitive",
                "place",
                "word",
                "how it runs",
                "its keys of the files",
                "its line in ALGEBRA.md",
            ),
            rows,
        ),
        "\n## The step file's acts\n",
        f"`{STEP_FILE}`, digest `{step.digest}` (written into every output as `step.hash`):"
        f" {len(step.acts)} acts, of which {sum(1 for a in acts if a[4] == 'yes')} are built and walked.\n",
        table(("#", "place", "primitive", "words", "built"), acts),
        "\n## The expected failures\n",
        "Each mark names what the tree does not do yet; it comes off when the cut lands.\n",
        table(("test", "reason"), expected_failures()),
        "\n## The owners\n",
        f"One owner per area (`tools/owners.json`); the arbiter is {owners_map['arbiter']}.\n",
        table(
            ("owner", "areas"),
            [
                (owner, ", ".join(f"`{area}`" for area in entry["areas"]))
                for owner, entry in owners_map["owners"].items()
            ],
        ),
        "\n## The shipped worlds\n",
        f"{len(record['worlds'])} worlds under `examples/events/`, each replayed bit for bit on"
        " every pull request that runs a world (`tests/shipped_worlds.json`).\n",
        table(
            ("world", "ticks", "intervals recorded"),
            [
                (
                    f"`{world}`",
                    str(entry["ticks"]),
                    str(entry["intervals"]),
                )
                for world, entry in sorted(record["worlds"].items())
            ],
        ),
    ]
    return "\n".join(out)


def expected_failures() -> list[tuple[str, ...]]:
    """Every xfail mark or call under tests/ with its reason, by file and line."""
    found: list[tuple[str, ...]] = []
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            callee = ast.unparse(node.func)
            if callee not in ("pytest.mark.xfail", "pytest.xfail"):
                continue
            reason = next((k.value for k in node.keywords if k.arg == "reason"), None)
            if reason is None and node.args:
                reason = node.args[0]
            found.append((f"`{path.relative_to(ROOT).as_posix()}:{node.lineno}`", reason_text(reason)))
    return found


def reason_text(node: ast.expr | None) -> str:
    """A reason's literal text, the constant parts of an f-string kept."""
    if node is None:
        return ""
    parts = [node] if not isinstance(node, ast.JoinedStr) else list(node.values)
    text = "".join(str(part.value) for part in parts if isinstance(part, ast.Constant))
    text = " ".join(text.split())
    return text if len(text) <= 160 else text[:157] + "..."


def history_page(ref: str = "HEAD") -> str:
    """The history of `ref`'s first parent, one line per commit, by day, newest first."""
    log = subprocess.run(
        ["git", "log", "--first-parent", "--format=%h%x1f%cs%x1f%P%x1f%s", ref],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    ).stdout
    out = ["# The history of main, first parent, newest first\n"]
    day = None
    for line in log.splitlines():
        sha, date, parents, subject = line.split("\x1f", 3)
        if date != day:
            out.append(f"\n## {date}\n")
            day = date
        mark = "merge" if len(parents.split()) > 1 else "commit"
        out.append(f"- `{sha}` ({mark}) {subject}")
    return "\n".join(out) + "\n"


def decisions_page() -> str:
    """Every decision line of HIGHLIGHTS.md with the date of its last change and the commit."""
    blame = subprocess.run(
        ["git", "blame", "--line-porcelain", "--", "docs/HIGHLIGHTS.md"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    ).stdout
    rows = []
    sha, date, summary = "", "", ""
    for line in blame.splitlines():
        if re.match(r"^[0-9a-f]{40} ", line):
            sha = line[:7]
        elif line.startswith("committer-time "):
            date = subprocess.run(
                ["date", "-u", "-d", f"@{line.split()[1]}", "+%Y-%m-%d"], capture_output=True, text=True
            ).stdout.strip()
        elif line.startswith("summary "):
            summary = line[8:]
        elif line.startswith("\t- **"):
            decision = line[1:].split("**")[1]
            rows.append((date, f"`{sha}`", f"**{decision}**", summary[:90]))
    return "# The decisions, each with its last change\n\n" + table(
        ("since", "commit", "decision", "the change"), rows
    )


def cited_paths(text: str) -> list[str]:
    """Every backticked token of `text` that reads as a path (a command's first word), its line numbers dropped."""
    found = []
    for token in CITED.findall(text):
        token = LINE_SUFFIX.sub("", token.split()[0]) if token.strip() else token
        if not PATH_TOKEN.fullmatch(token) or ("/" not in token and not token.endswith(SUFFIXES)):
            continue
        if "..." in token or token.startswith(GIT_REFS):
            continue
        found.append(token)
    return found


def resolves(root: Path, token: str) -> bool:
    """Whether a cited path exists: as written, under the package, or, a bare file name, anywhere in the tree."""
    if token.startswith(RUN_FOLDERS):
        return True
    if (root / token).exists() or (root / PACKAGE / token).exists():
        return True
    if "/" not in token:
        return any(root.rglob(token))
    return False


def documents_to_check(root: Path) -> list[str]:
    """The hand-written documents, the skills and the generated pages."""
    skills = sorted(p.relative_to(root).as_posix() for p in (root / "skills").rglob("*.md"))
    generated = sorted(
        p.relative_to(root).as_posix() for p in (root / "docs" / "generated").glob("*.md")
    )
    return [*HAND_WRITTEN, *skills, *generated]


def missing_paths(root: Path) -> list[str]:
    """Every cited path of the documents that the tree lacks, as document:line path."""
    found = []
    for rel in documents_to_check(root):
        for number, line in enumerate((root / rel).read_text(encoding="utf-8").splitlines(), 1):
            for token in cited_paths(line):
                if not resolves(root, token):
                    found.append(f"{rel}:{number} {token}")
    return found


def unmarked_decisions(root: Path) -> list[str]:
    """Every decision line of HIGHLIGHTS.md citing a path the tree lacks without the words 'ahead of the tree'."""
    found = []
    text = (root / "docs" / "HIGHLIGHTS.md").read_text(encoding="utf-8")
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("- **") or AHEAD in line:
            continue
        absent = [token for token in cited_paths(line) if not resolves(root, token)]
        if absent:
            found.append(
                f"docs/HIGHLIGHTS.md:{number} names {', '.join(absent)} and does not say '{AHEAD}'"
            )
    return found


def rendered() -> dict[str, str]:
    """The two generated pages by name."""
    return {"FILES.md": files_page(), "STATUS.md": status_page()}


def stale_pages(root: Path) -> list[str]:
    """The generated pages whose committed text differs from the render."""
    found = []
    for name, text in rendered().items():
        path = root / "docs" / "generated" / name
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            found.append(name)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--check", action="store_true", help="the documents against the tree; exit 1 on a finding"
    )
    parser.add_argument("--history", action="store_true", help="print the history of the first parent")
    parser.add_argument("--decisions", action="store_true", help="print the decisions with their dates")
    arguments = parser.parse_args(argv)
    if arguments.history:
        print(history_page(), end="")
        return 0
    if arguments.decisions:
        print(decisions_page(), end="")
        return 0
    if arguments.check:
        findings = [*missing_paths(ROOT), *unmarked_decisions(ROOT)]
        findings += [f"docs/generated/{name} differs from the render" for name in stale_pages(ROOT)]
        print("\n".join(findings) if findings else "the documents match the tree")
        return 1 if findings else 0
    GENERATED.mkdir(parents=True, exist_ok=True)
    for name, text in rendered().items():
        (GENERATED / name).write_text(text, encoding="utf-8")
        print(f"wrote docs/generated/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
