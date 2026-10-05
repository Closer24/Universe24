"""Find the prose a TeX file repeats: word runs that occur twice or more, and formulas written twice.

Usage: python dupfind.py main.tex [--run 11]. The bibliography is left out; citations, references and labels
are removed before the words are compared.
"""

import collections
import re
import sys


def words_of(text: str) -> list[str]:
    stripped = re.sub(
        r"\\cite\[[^\]]*\]\{[^}]*\}|\\cite\{[^}]*\}|\\ref\{[^}]*\}|\\label\{[^}]*\}", "", text
    )
    return re.findall(r"[A-Za-z$\\{}^_0-9'.,()=+-]+", stripped)


def repeated_runs(words: list[str], run: int) -> list[tuple[str, list[int]]]:
    seen: dict[str, list[int]] = collections.defaultdict(list)
    for index in range(len(words) - run):
        seen[" ".join(words[index : index + run])].append(index)
    hits = [(key, places) for key, places in seen.items() if len(places) > 1]
    merged: list[tuple[str, list[int]]] = []
    last = -run
    for key, places in sorted(hits, key=lambda hit: hit[1][0]):
        if places[0] - last > run:
            merged.append((key, places))
        last = places[0]
    return merged


def main() -> None:
    name = sys.argv[1]
    run = int(sys.argv[sys.argv.index("--run") + 1]) if "--run" in sys.argv else 11
    text = open(name, encoding="utf-8").read()
    cut = text.find("\\begin{thebibliography}")
    body = text[: cut if cut > 0 else len(text)]
    runs = repeated_runs(words_of(body), run)
    print(f"===== {name}: repeated {run}-word runs: {len(runs)}")
    for key, places in runs:
        print(len(places), "|", key)
    formulas = collections.Counter(match.group(0) for match in re.finditer(r"\$[^$]{18,}=[^$]*\$", body))
    print("===== formulas with an equals sign written twice:")
    for formula, count in formulas.items():
        if count > 1:
            print(count, "|", formula)


if __name__ == "__main__":
    main()
