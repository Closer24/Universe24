"""The repository's language (AGENTS.md, repository language: English): every tracked text file (.py, .md, .json, .toml, .txt, .yml) and every new one holds ASCII letters only, no Hebrew, Greek or Cyrillic letter in its prose, no directory exempt."""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUFFIXES = (".py", ".md", ".json", ".toml", ".txt", ".yml")


def test_every_text_file_holds_ascii_letters_only():
    """Every letter of every tracked or new text file is an ASCII letter; a dash, a sign or a symbol is no letter and passes."""
    listed = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.splitlines()
    found = [
        f"{name}:{number}: {character!r}"
        for name in listed
        if name.endswith(SUFFIXES) and (ROOT / name).is_file()
        for number, line in enumerate((ROOT / name).read_text(encoding="utf-8").splitlines(), 1)
        for character in line
        if character.isalpha() and not character.isascii()
    ]
    assert not found, found[:20]
