"""The closing round's mechanical part in one command, with a convergence verdict.

At a commit of the short version (the checkout as it stands) the runner runs every check the closing round
runs by hand (the owner's word of 2026-10-05, "everything the long version had runs at a closing round"):
the ten gates, the claims reader with its counts, the checker against the long version at its tag with the
accepted misses, the seam gates' counts against their baseline, the Crossref check of every DOI entry, the
Springer build of both documents, the project's checks, CI's check runs at the commit and the open audit
issues newer than it. It prints one table, writes it as Markdown and exits 0 only when the paper CONVERGES
on every mechanical count; the readers (the sub-agents) are the other half, see readers.py.

Usage: python closing_round.py [--sha HEAD] [--out closing_round.md] [--offline] [--no-ci] [--full]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PYTHON = sys.executable
LONG_REF = "441b2399"
REPOSITORY = "closer24/universe24"
NOT_CROSSREF = (
    "10.5281/",
    "10.11429/",
)  # DataCite and JaLC prefixes, resolving at doi.org, not at Crossref


def run(command: list[str], cwd: Path = HERE, timeout: int = 900) -> tuple[int, str]:
    environment = {**os.environ, "TEXINPUTS": "sn:"}  # the Springer class and style under sn/
    done = subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=environment
    )
    return done.returncode, done.stdout + done.stderr


def git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], cwd=ROOT, capture_output=True, text=True).stdout.strip()


# 1. the ten gates
def gates() -> tuple[bool, str]:
    code, out = run([PYTHON, "paper_gates.py"])
    misses = sum(int(m) for m in re.findall(r": (\d+) miss", out))
    return code == 0 and misses == 0, f"{misses} misses"


# 2. the claims reader
def reader() -> tuple[bool, str]:
    before = (ROOT / "paper" / "claims.md").read_text(encoding="utf-8")
    run([PYTHON, "claims_table.py"])
    summary = (ROOT / "paper" / "claims.md").read_text(encoding="utf-8").split("\n")[4]
    (ROOT / "paper" / "claims.md").write_text(before, encoding="utf-8")
    counts = {
        key: int(value)
        for key, value in re.findall(
            r"(rows of Table 1 without a marked sentence|marks outside the key|breakers keyed to another derivation)"
            r": (\d+)",
            summary,
        )
    }
    ok = all(value == 0 for value in counts.values()) and len(counts) == 3
    return ok, ", ".join(f"{k.split()[0]}… {v}" for k, v in counts.items()) or summary[:80]


# 3. the checker against the long version at its tag, the accepted misses
def checker() -> tuple[bool, str]:
    accepted = {
        line.strip()
        for line in (HERE / "accepted_misses.txt").read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    }
    _, out = run(
        [
            PYTHON,
            "short_checker.py",
            "--short-main",
            "main.tex",
            "--short-supplement",
            "supplement.tex",
            "--long-ref",
            LONG_REF,
        ]
    )
    misses = {m.strip() for m in re.findall(r"^MISS [^|]*\| ([^\n]*)$", out, re.M)}
    weak = len(re.findall(r"^WEAK ", out, re.M))
    unresolved = re.search(r"(\d+) unresolved pointers", out)
    new = sorted(misses - accepted)
    ok = not new and (unresolved is None or unresolved.group(1) == "0")
    return (
        ok,
        f"{len(misses)} misses ({len(new)} not accepted{': ' + ', '.join(new) if new else ''}), {weak} weak",
    )


# 4. the seam gates against their baseline
def seams() -> tuple[bool, str]:
    if not (HERE / "seam_gates.py").exists():
        return True, "not on this commit (the branch seam-gates)"
    _, out = run([PYTHON, "seam_gates.py", "--quiet"])
    counts = {name: int(n) for name, n in re.findall(r"^(.*?): (\d+) rows?$", out, re.M)}
    baseline_path = HERE / "seam_baseline.json"
    if baseline_path.exists():
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        rose = [name for name, n in counts.items() if n > baseline.get(name, n)]
        return not rose, ", ".join(f"{n}" for n in counts.values()) + (
            f"; rose: {', '.join(rose)}" if rose else ""
        )
    return True, ", ".join(str(n) for n in counts.values()) + " (no baseline yet)"


# 5. Crossref
def crossref() -> tuple[bool, str]:
    _, out = run([PYTHON, "cut_tools/crossref_check.py", "main.tex", "supplement.tex"], timeout=1800)
    rows = [line for line in out.split("\n") if " | " in line and "| no DOI |" not in line]
    real = []
    for row in rows:
        if "<mml:" in row or "| year " in row:
            continue  # MathML in the record's title; the online-first year against the print year
        if "Crossref failed" in row and any(prefix in row for prefix in NOT_CROSSREF):
            continue
        if "Crossref failed" in row and resolves(row):
            continue  # an empty reply from the proxy, the record read on the retry
        real.append(row.split(" | ")[0])
    entries = re.search(r"(\d+) entries", out)
    return (
        not real,
        f"{entries.group(1) if entries else '?'} entries, mismatches: {', '.join(real) or 'none'}",
    )


def resolves(row: str) -> bool:
    """A second fetch of the DOI a 'Crossref failed' row names; True when Crossref answers with a record."""
    doi = re.search(r"\| (10\.\S+) ", row)
    if not doi:
        return False
    code, out = run(
        ["curl", "-sS", "--max-time", "25", f"https://api.crossref.org/works/{doi.group(1)}"], timeout=40
    )
    try:
        return code == 0 and "message" in json.loads(out)
    except ValueError:
        return False


# 6. the Springer build
def build() -> tuple[bool, str]:
    report = []
    ok = True
    for name in ("main", "supplement"):
        for _ in range(3):
            code, _ = run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"],
                timeout=600,
            )
            if code != 0:
                break
        log = (
            (HERE / f"{name}.log").read_text(encoding="utf-8", errors="replace")
            if (HERE / f"{name}.log").exists()
            else ""
        )
        errors, undefined, overfull = log.count("\n!"), log.count("undefined"), log.count("Overfull")
        pages = re.search(r"Output written on .*\((\d+) pages", log)
        ok = ok and code == 0 and errors == 0 and undefined == 0 and overfull == 0
        report.append(
            f"{name} {pages.group(1) if pages else '?'} pages, {errors}/{undefined}/{overfull}"
        )
        for suffix in ("aux", "log", "out", "bbl"):
            (HERE / f"{name}.{suffix}").unlink(missing_ok=True)
    git("checkout", "--", "paper/general_formula/main.pdf", "paper/general_formula/supplement.pdf")
    return ok, "; ".join(report) + " (errors/undefined/overfull)"


# 7. the project's checks
def checks(full: bool) -> tuple[bool, str]:
    code, out = run([PYTHON, "tools/check.py"] + (["--full"] if full else []), cwd=ROOT, timeout=1800)
    passed = re.search(r"(\d+) passed", out)
    return code == 0, f"{passed.group(1) if passed else '?'} passed, exit {code}"


# 8. CI at the commit
def ci(sha: str) -> tuple[bool, str]:
    code, out = run(
        ["gh", "api", f"repos/{REPOSITORY}/commits/{sha}/check-runs?per_page=50"], cwd=ROOT, timeout=60
    )
    if code != 0:
        return False, "gh api failed"
    runs = json.loads(out).get("check_runs", [])
    if not runs:
        return False, "no check run at the commit"
    bad = [r["name"] for r in runs if r.get("conclusion") != "success"]
    return not bad, f"{len(runs)} runs" + (f", not green: {', '.join(bad)}" if bad else ", all green")


# 9. the audit issues newer than the commit
def audits(sha: str) -> tuple[bool, str]:
    since = git("show", "-s", "--format=%cI", sha)
    code, out = run(
        ["gh", "api", f"repos/{REPOSITORY}/issues?state=open&since={since}&per_page=50"],
        cwd=ROOT,
        timeout=60,
    )
    if code != 0:
        return True, "gh api failed (unweighed)"
    new = [
        f"#{i['number']}"
        for i in json.loads(out)
        if "pull_request" not in i and i["title"].startswith("Paper audit") and i["created_at"] >= since
    ]
    return not new, f"open audit issues newer than the commit: {', '.join(new) or 'none'}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--sha", default="HEAD")
    parser.add_argument("--out", default=str(ROOT / "artifacts" / "closing_round.md"))
    parser.add_argument("--offline", action="store_true", help="skip Crossref")
    parser.add_argument("--no-ci", action="store_true", help="skip CI and the audit issues")
    parser.add_argument("--full", action="store_true", help="tools/check.py --full")
    args = parser.parse_args()
    sha = git("rev-parse", "--short", args.sha)
    rows: list[tuple[str, bool, str]] = []
    for name, check in (
        ("the ten gates", gates),
        ("the claims reader", reader),
        ("the checker against the long version", checker),
        ("the seam gates", seams),
    ):
        ok, detail = check()
        rows.append((name, ok, detail))
        print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    if not args.offline:
        ok, detail = crossref()
        rows.append(("Crossref", ok, detail))
        print(f"{'ok  ' if ok else 'FAIL'} Crossref: {detail}")
    ok, detail = build()
    rows.append(("the Springer build", ok, detail))
    print(f"{'ok  ' if ok else 'FAIL'} the Springer build: {detail}")
    ok, detail = checks(args.full)
    rows.append(("the project's checks", ok, detail))
    print(f"{'ok  ' if ok else 'FAIL'} the project's checks: {detail}")
    if not args.no_ci:
        for name, check in (("CI at the commit", ci), ("the audit issues", audits)):
            ok, detail = check(sha)
            rows.append((name, ok, detail))
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}")
    converged = all(ok for _, ok, _ in rows)
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"## The closing round's mechanical part at {sha} ({stamp}): {'CONVERGED' if converged else 'NOT YET'}",
        "",
    ]
    lines += ["| check | result | detail |", "| --- | --- | --- |"]
    lines += [f"| {name} | {'ok' if ok else 'FAIL'} | {detail} |" for name, ok, detail in rows]
    lines += [
        "",
        "The readers' half is `readers.py`: the prompts for the changed sections and the collector of their rows.",
    ]
    Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n{'CONVERGED' if converged else 'NOT YET'} at {sha}; the table in {args.out}")
    return 0 if converged else 1


if __name__ == "__main__":
    sys.exit(main())
