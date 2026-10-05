"""A sentence-level grep for the paper's TeX files, which hold one paragraph per line.

Usage: python sent.py main.tex "pattern" ["pattern" ...]. For every pattern, every sentence that matches is
printed with its line number, so the match is read in its sentence and not in its paragraph.
"""

import re
import sys


def sentences(paragraph: str) -> list[str]:
    """Split a paragraph at a full stop, a question mark or an exclamation mark followed by a capital or TeX."""
    return re.split(r"(?<=[.!?])\s+(?=[A-Z\\(\$])", paragraph)


def main() -> None:
    lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
    for pattern in sys.argv[2:]:
        print("###", pattern)
        for number, line in enumerate(lines, 1):
            if re.search(pattern, line):
                for sentence in sentences(line):
                    if re.search(pattern, sentence):
                        print(f"{number}: {sentence[:700]}")


if __name__ == "__main__":
    main()
