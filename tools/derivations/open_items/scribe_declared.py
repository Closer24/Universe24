"""What the universe files and the Python worlds declare, listed and never refused.

The owner's word of 2026-10-29, relayed at 10:54 (decision 35, ALGEBRA.md line 35, **Nothing is declared: every particle appears by itself in
the clicks**): no particle, mass or coupling is declared in any file. The gate (scribe_scan.py) reads code and not data files, so a declared
family or train passes it. This reads the data files and the dicts of trains and lists what they name, so that a new declaration is seen at
the push that brings it. It decides nothing and exits 0 on a good call; to make the gate refuse a new declaration needs the owner's word.

It lists: every entry of a `families` list and of a `trains` list in a .json file, with the pair, pinion or ratio it carries; and every Python
dict written with a name and a pinion (a test's or a probe's train), with the pinion as the line writes it.

  python -I scribe_declared.py DIR [DIR ...]     the listing of every .json and .py file under the directories, each name once, its files under it
"""

from __future__ import annotations

import ast
import json
import sys
from collections import defaultdict
from collections.abc import Iterator
from pathlib import Path

LISTS = (("families", "family"), ("trains", "train"))
GEAR = (
    "pinion",
    "pair",
    "ratio",
)  # the key that carries the number a declaration stands for, the first the entry holds
SKIP = frozenset({".git", "node_modules", "venv314", "__pycache__"})
NONE = "-"

Found = tuple[str, str, str]  # kind, name, the number as the file writes it


def from_json(path: Path) -> Iterator[Found]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError, ValueError:
        return
    if not isinstance(data, dict):
        return
    for key, kind in LISTS:
        entries = data.get(key)
        for entry in entries if isinstance(entries, list) else ():
            if isinstance(entry, dict) and isinstance(entry.get("name"), str):
                yield kind, entry["name"], next((json.dumps(entry[g]) for g in GEAR if g in entry), NONE)


def from_python(path: Path) -> Iterator[Found]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except OSError, SyntaxError, ValueError:
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        fields = {
            k.value: v
            for k, v in zip(node.keys, node.values, strict=True)
            if isinstance(k, ast.Constant) and isinstance(k.value, str)
        }
        name = fields.get("name")
        if isinstance(name, ast.Constant) and isinstance(name.value, str) and "pinion" in fields:
            yield "train", name.value, ast.get_source_segment(source, fields["pinion"]) or NONE


def files(root: Path) -> Iterator[Path]:
    for path in sorted(root.rglob("*")):
        if (
            path.suffix in (".json", ".py")
            and path.is_file()
            and not SKIP & set(path.relative_to(root).parts)
        ):
            yield path


def main(argv: list[str]) -> int:
    if not argv:
        raise SystemExit(__doc__)
    found: dict[tuple[str, str], dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for root in map(Path, argv):
        for path in files(root):
            for kind, name, number in from_json(path) if path.suffix == ".json" else from_python(path):
                found[kind, name][number].append(path.as_posix())
    for (kind, name), by_number in sorted(found.items()):
        every = sorted({where for places in by_number.values() for where in places})
        print(
            f"{kind} {name}: "
            + ", ".join(f"{number} in {len(places)}" for number, places in sorted(by_number.items()))
            + f"; {len(every)} files"
        )
        for where in every:
            print(f"    {where}")
    print(f"{len(found)} declared names")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
