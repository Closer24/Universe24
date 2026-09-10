"""Guard the English repository rule without banning scientific notation.

This detects scripts, not language. Latin-script prose still needs human review.
Escaped multilingual strings below are deliberate negative test inputs.
"""

import os
import unicodedata
from pathlib import Path

import pytest

BLOCKED_SCRIPTS = ("HEBREW", "ARABIC", "CYRILLIC", "CJK", "HIRAGANA", "KATAKANA", "HANGUL")
GENERATED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "artifacts",
    "build",
    "dist",
    "node_modules",
}
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".rst",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".in",
}


def non_english_script_lines(source):
    return [
        number
        for number, line in enumerate(source.splitlines(), start=1)
        if any(
            unicodedata.category(char).startswith("L")
            and any(script in unicodedata.name(char, "") for script in BLOCKED_SCRIPTS)
            for char in line
        )
    ]


def repository_text_files(root):
    for directory, folders, files in os.walk(root):
        folders[:] = [
            name
            for name in folders
            if name not in GENERATED_DIRECTORIES and not name.endswith(".egg-info")
        ]
        for name in files:
            path = Path(directory) / name
            if path.suffix in TEXT_SUFFIXES or name in {".gitignore", ".gitattributes"}:
                yield path


def test_repository_uses_english_text():
    root = Path(__file__).parents[1]
    violations = {
        str(path.relative_to(root)): lines
        for path in repository_text_files(root)
        if (lines := non_english_script_lines(path.read_text(encoding="utf-8")))
    }
    assert not violations, f"Translate repository prose to English: {violations}"


@pytest.mark.parametrize(
    "source",
    [
        "# \u05d4\u05e2\u05e8\u05d4",
        '"""\u05d4\u05e2\u05e8\u05d4"""',
        "# \u05db\u05dc\u05dc\u05d9\u05dd\n",
        "# \u041f\u0440\u0438\u043c\u0435\u0440",
    ],
)
def test_language_gate_rejects_non_english_comments_and_documentation(source):
    assert non_english_script_lines(source) == [1]


def test_language_gate_allows_english_and_mathematical_notation():
    assert not non_english_script_lines('"""Integer momentum exchange."""\n# Δp = −ΔP; 1500×1275')


def test_language_rule_has_one_authoritative_entry_point():
    root = Path(__file__).parents[1]
    instructions = (root / "AGENTS.md").read_text()
    assert "## Repository language: English" in instructions
    for term in ("comments", "docstrings", "documentation", "every directory"):
        assert term in instructions
    assert "../AGENTS.md#repository-language-english" in (root / "docs/ARCHITECTURE.md").read_text()


def test_language_scan_covers_nested_source_and_keeps_generated_outputs_out(tmp_path):
    source = tmp_path / "new_component" / "nested" / "rules.md"
    source.parent.mkdir(parents=True)
    source.write_text("English instructions")
    artifact = tmp_path / "artifacts" / "run.html"
    artifact.parent.mkdir()
    artifact.write_text("Generated output")
    assert set(repository_text_files(tmp_path)) == {source}
