"""The closing round's runner and the readers' half (paper/general_formula/closing_round.py, readers.py): the accepted
misses are read, the sections and derivations are located, the prompts fill, and the collector reads a report's rows."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
FORMULA = ROOT / "paper" / "general_formula"


def load(name: str) -> ModuleType:
    if str(FORMULA) not in sys.path:
        sys.path.insert(0, str(FORMULA))
    spec = importlib.util.spec_from_file_location(name, FORMULA / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_accepted_misses_are_one_number_per_line() -> None:
    lines = [
        line.strip()
        for line in (FORMULA / "accepted_misses.txt").read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]
    assert lines and all(" " not in line for line in lines)


def test_the_sections_and_the_derivations_are_located() -> None:
    readers = load("readers")
    main = (FORMULA / "main.tex").read_text(encoding="utf-8")
    supplement = (FORMULA / "supplement.tex").read_text(encoding="utf-8")
    sections = readers.sections_of(main)
    assert sections and sections[0][0] == "sec:intro" and all(s <= e for _, s, e in sections)
    derivations = readers.derivations_of(supplement)
    assert derivations[0][0] == 1 and derivations[-1][0] >= 55 and all(s < e for _, s, e in derivations)


def test_the_templates_fill_and_the_collector_reads_the_rows(tmp_path: Path) -> None:
    readers = load("readers")
    common = (readers.TEMPLATES / "_common.md").read_text(encoding="utf-8")
    filled = common.format(
        sha="abc1234",
        main="m",
        supplement="s",
        long_main="lm",
        long_supplement="ls",
        law="law",
        report="r",
    )
    assert "abc1234" in filled and "{" not in filled.replace("{{", "").replace("}}", "")
    (tmp_path / "x.report.md").write_text(
        "| # | place | the words | what is wrong | the fix | B/N |\n|---|---|---|---|---|---|\n"
        "| 1 | main.tex:10 | a | b | c | N |\n| 2 | S.3 | d | e | f | B (wrong input) |\n",
        encoding="utf-8",
    )
    summary = readers.collect(tmp_path, tmp_path / "summary.md")
    assert "| x | 1 | 1 |" in summary
    assert summary.index("| B | x |") < summary.index("| N | x |")


def test_the_runner_reads_the_checker_and_the_gates_output_forms() -> None:
    closing = load("closing_round")
    assert closing.LONG_REF == "441b2399" and closing.NOT_CROSSREF == ("10.5281/", "10.11429/")
