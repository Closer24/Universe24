"""The readers' half of the closing round: the sub-agent readers' prompts for the sections a diff touches, and the
collector that turns their reports into one table.

Usage: python readers.py prompts --since <commit> [--sha HEAD] [--out DIR]   (the prompts to launch, one file each)
       python readers.py collect <reports directory> [--out summary.md]          (the rows of every report, B first)
The prompts are the templates in readers/ filled with the commit and the files; whoever launches them (a session's
Agent workers, the Boss's workers) launches the same text at every cut, and the reports land as Markdown tables the
collector reads. The three coherence readers (the cold read, the statuses, the terms) and the hostile pass run at
every cut; the section and derivation readers run for what the diff touched.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
TEMPLATES = HERE / "readers"
GROUP = 5  # derivations per reader
ROW = re.compile(r"^\|\s*(\d+)[^|]*\|(.*)\|\s*(B|N)[^|]*\|\s*$", re.M)


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True).stdout


def changed_lines(since: str, sha: str, path: str) -> list[int]:
    """The line numbers of the file at sha that the diff since the commit touched."""
    out = git("diff", "-U0", f"{since}..{sha}", "--", path)
    lines: list[int] = []
    for start, count in re.findall(r"^@@ -[\d,]+ \+(\d+)(?:,(\d+))? @@", out, re.M):
        lines += list(range(int(start), int(start) + max(int(count or 1), 1)))
    return lines


def sections_of(main: str) -> list[tuple[str, int, int]]:
    """(label, first line, last line) of every section and subsection of the main."""
    lines = main.split("\n")
    heads = [
        (i + 1, m.group(1))
        for i, line in enumerate(lines)
        if (m := re.search(r"\\(?:sub)*section\{[^}]*\}\\label\{([^}]*)\}", line))
    ]
    return [
        (label, start, heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines))
        for k, (start, label) in enumerate(heads)
    ]


def derivations_of(supplement: str) -> list[tuple[int, int, int]]:
    """(S.n, first line, last line) of every derivation environment."""
    lines = supplement.split("\n")
    starts = [i + 1 for i, line in enumerate(lines) if "\\begin{derivation}" in line]
    ends = [i + 1 for i, line in enumerate(lines) if "\\end{derivation}" in line]
    return [(n, s, e) for n, (s, e) in enumerate(zip(starts, ends, strict=True), 1)]


def prompts(since: str, sha: str, out: Path) -> list[Path]:
    sha = git("rev-parse", "--short", sha).strip()
    main = git("show", f"{sha}:paper/general_formula/main.tex")
    supplement = git("show", f"{sha}:paper/general_formula/supplement.tex")
    common = (TEMPLATES / "_common.md").read_text(encoding="utf-8")
    fill = {
        "sha": sha,
        "main": str(HERE / "main.tex"),
        "supplement": str(HERE / "supplement.tex"),
        "long_main": "git show 441b2399:paper/general_formula/main.tex",
        "long_supplement": "git show 441b2399:paper/general_formula/supplement.tex",
        "law": str(ROOT / "docs" / "ALGEBRA.md"),
    }
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def write(name: str, template: str, **extra: str) -> None:
        report = out / f"{name}.report.md"
        text = (TEMPLATES / template).read_text(encoding="utf-8")
        body = text.format(common=common.format(report=str(report), **fill), **extra)
        path = out / f"{name}.prompt.md"
        path.write_text(body, encoding="utf-8")
        written.append(path)

    for name in ("cold_read", "statuses", "terms", "hostile"):
        write(name, f"{name}.md")
    touched_main = set(changed_lines(since, sha, "paper/general_formula/main.tex"))
    for label, start, end in sections_of(main):
        if touched_main & set(range(start, end + 1)):
            write(
                f"section_{label.replace('sec:', '')}",
                "section.md",
                section=label,
                lines=f"{start} to {end}",
            )
    touched_sup = set(changed_lines(since, sha, "paper/general_formula/supplement.tex"))
    hit = sorted({n for n, s, e in derivations_of(supplement) if touched_sup & set(range(s, e + 1))})
    groups: list[list[int]] = []
    for n in hit:
        if groups and n - groups[-1][0] < GROUP and n - groups[-1][-1] <= 2:
            groups[-1].append(n)
        else:
            groups.append([n])
    for group in groups:
        write(
            f"derivations_{group[0]}_{group[-1]}",
            "derivations.md",
            first=str(group[0]),
            last=str(group[-1]),
        )
    return written


def collect(reports: Path, out: Path) -> str:
    rows: list[tuple[str, str, str]] = []
    counts: list[str] = []
    for path in sorted(reports.glob("*.report.md")):
        text = path.read_text(encoding="utf-8")
        found = [
            (m.group(3), m.group(2).strip(), path.stem.replace(".report", ""))
            for m in ROW.finditer(text)
        ]
        rows += found
        blocking = sum(1 for kind, _, _ in found if kind == "B")
        counts.append(f"| {path.stem.replace('.report', '')} | {blocking} | {len(found) - blocking} |")
    rows.sort(key=lambda r: (r[0] != "B", r[2]))
    lines = [
        "## The readers' rows, blocking first",
        "",
        "| reader | B | N |",
        "| --- | --- | --- |",
        *counts,
        "",
    ]
    lines += ["| B/N | reader | the row |", "| --- | --- | --- |"]
    lines += [f"| {kind} | {reader} | {row} |" for kind, row, reader in rows]
    text = "\n".join(lines) + "\n"
    out.write_text(text, encoding="utf-8")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prompts")
    p.add_argument("--since", required=True)
    p.add_argument("--sha", default="HEAD")
    p.add_argument("--out", default=str(HERE / "readers_out"))
    c = sub.add_parser("collect")
    c.add_argument("reports")
    c.add_argument("--out", default=None)
    args = parser.parse_args()
    if args.command == "prompts":
        for path in prompts(args.since, args.sha, Path(args.out)):
            print(path)
        return 0
    reports = Path(args.reports)
    summary = collect(reports, Path(args.out) if args.out else reports / "summary.md")
    print(summary.split("\n| B/N")[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
