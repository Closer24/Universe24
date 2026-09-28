"""The English repository rule: the gate detects scripts other than Latin, not language; escaped strings below are deliberate negative inputs."""

import ast
import re
import unicodedata
from pathlib import Path

import pytest

from tests.running import repository_files

BLOCKED_SCRIPTS = ("HEBREW", "ARABIC", "CYRILLIC", "CJK", "HIRAGANA", "KATAKANA", "HANGUL")
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
    ".bash",
    ".ps1",
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
    for path in repository_files(root):
        if path.suffix in TEXT_SUFFIXES or path.name in {
            ".gitignore",
            ".gitattributes",
            ".python-version",
        }:
            yield path


def invalid_path_names(root):
    return [
        path.relative_to(root).as_posix()
        for path in repository_files(root)
        if any(not re.fullmatch(r"[A-Za-z0-9_.-]+", part) for part in path.relative_to(root).parts)
    ]


def non_ascii_identifiers(source):
    found = set()
    for node in ast.walk(ast.parse(source)):
        names = []
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        elif isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, ast.arg):
            names.append(node.arg)
        elif isinstance(node, ast.Attribute):
            names.append(node.attr)
        elif isinstance(node, ast.alias):
            names.extend((node.name, node.asname or ""))
        found.update(name for name in names if not name.isascii())
    return sorted(found)


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


def test_language_scan_covers_nested_source_and_keeps_generated_outputs_out(tmp_path):
    source = tmp_path / "new_component" / "nested" / "rules.md"
    source.parent.mkdir(parents=True)
    source.write_text("English instructions")
    artifact = tmp_path / "artifacts" / "run.html"
    artifact.parent.mkdir()
    artifact.write_text("Generated output")
    assert set(repository_text_files(tmp_path)) == {source}


def test_repository_paths_use_portable_english_names():
    assert not invalid_path_names(Path(__file__).resolve().parents[1])


def test_python_identifiers_use_ascii_names():
    root = Path(__file__).resolve().parents[1]
    violations = {
        path.relative_to(root).as_posix(): names
        for path in repository_files(root)
        if path.suffix == ".py" and (names := non_ascii_identifiers(path.read_text(encoding="utf-8")))
    }
    assert not violations, violations


@pytest.mark.parametrize("filename", ["unclear name.py", "\u05e9\u05dd.py"])
def test_path_gate_rejects_spaces_and_non_ascii_names(tmp_path, filename):
    (tmp_path / filename).write_text("# English text", encoding="utf-8")
    assert invalid_path_names(tmp_path) == [filename]


def test_identifier_gate_checks_names_attributes_arguments_and_import_aliases():
    found = non_ascii_identifiers("def \u03b1(\u03b2): return obj.\u03b3")
    assert found == ["\u03b1", "\u03b2", "\u03b3"]
    assert non_ascii_identifiers("import math as \u03b1") == ["\u03b1"]
    assert not non_ascii_identifiers("def momentum_delta(value): return value.px")


def test_language_scan_includes_powershell_and_interpreter_file(tmp_path):
    paths = [tmp_path / "run_reference_checks.ps1", tmp_path / ".python-version"]
    for path in paths:
        path.write_text("English text", encoding="utf-8")
    assert set(repository_text_files(tmp_path)) == set(paths)
