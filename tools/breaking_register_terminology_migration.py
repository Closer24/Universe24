"""One-shot migration removing Site as an active physical-location synonym."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_PREFIXES = ("tests/reference/",)
SKIP_FILES = {
    "docs/VALIDATION.md",
    "AGENTS.md",
    "docs/TERMINOLOGY.md",
    "src/event_universe/ui.py",  # HTTP Sec-Fetch-Site is an external standard name.
    "src/event_universe/retention.py",  # Python site-packages is an external package term.
    "tools/breaking_register_terminology_migration.py",
}

# Underscore-separated identifiers are not matched by word-boundary replacement.
# Rename each by its actual responsibility rather than mechanically calling it a Node.
IDENTIFIER_REPLACEMENTS = (
    ("source_site", "source_register_index"),
    ("record_sites", "record_register_indices"),
    ("local_sites", "local_register_indices"),
    ("another_site", "another_register"),
    ("other_sites", "other_origins"),
    ("def _site(", "def _validate_register_index("),
    ("self._site(", "self._validate_register_index("),
)


def tracked_files() -> list[str]:
    return subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()


def skipped(path: str) -> bool:
    return path in SKIP_FILES or path.startswith(SKIP_PREFIXES)


def quantum_register_context(path: str) -> bool:
    lower = path.lower()
    return (
        "quantum" in lower
        or "native_event" in lower
        or "event_program" in lower
        or "event_runtime" in lower
        or path == "docs/EVENT_GRAPH_CONFIGURATION.md"
        or path == "tests/test_event_program_validation.py"
    )


def replace_words(text: str, plural: str, singular: str) -> str:
    text = re.sub(r"\bSites\b", plural.capitalize(), text)
    text = re.sub(r"\bsites\b", plural, text)
    text = re.sub(r"\bSite\b", singular.capitalize(), text)
    text = re.sub(r"\bsite\b", singular, text)
    return text


def migrate(path: str, text: str) -> str:
    for old, new in IDENTIFIER_REPLACEMENTS:
        text = text.replace(old, new)

    suffix = Path(path).suffix.lower()
    if quantum_register_context(path):
        if suffix in {".py", ".json"}:
            return replace_words(text, "register_indices", "register_index")
        # Documentation uses readable nouns but keeps schema/API spellings in code spans.
        text = text.replace('"sites"', '"register_indices"').replace('"site"', '"register_index"')
        text = text.replace("`sites`", "`register_indices`").replace("`site`", "`register_index`")
        return replace_words(text, "registers", "register")
    return replace_words(text, "Nodes", "Node")


def main() -> None:
    for path in tracked_files():
        if skipped(path):
            continue
        file_path = ROOT / path
        if not file_path.is_file():
            continue
        try:
            before = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        after = migrate(path, before)
        if after != before:
            file_path.write_text(after, encoding="utf-8")


if __name__ == "__main__":
    main()
