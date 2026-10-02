"""The repository's language (AGENTS.md, repository language: English): every tracked text file (.py, .md, .json, .toml, .txt, .yml) and every new one holds ASCII letters only, no Hebrew, Greek or Cyrillic letter in its prose, no directory exempt."""

import subprocess
from pathlib import Path

ROOT, SUFFIXES = Path(__file__).resolve().parents[1], (".py", ".md", ".json", ".toml", ".txt", ".yml")


def test_every_text_file_holds_ascii_letters_only():
    """Every letter of every tracked or new text file is an ASCII letter; a dash, a sign or a symbol is no letter and passes."""
    git = ["git", "ls-files", "--cached", "--others", "--exclude-standard"]
    listed, found = subprocess.check_output(git, cwd=ROOT, text=True).splitlines(), []
    for name in (n for n in listed if n.endswith(SUFFIXES) and (ROOT / n).is_file()):
        for number, line in enumerate((ROOT / name).read_text(encoding="utf-8").splitlines(), 1):
            found += [f"{name}:{number}: {c!r}" for c in line if c.isalpha() and not c.isascii()]
    assert not found, found[:20]
