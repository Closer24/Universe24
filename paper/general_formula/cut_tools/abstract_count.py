"""Count the abstract both ways the venues count it.

Usage: python abstract_count.py main.tex abstract_journal.txt. Prints the TeX tokens of the abstract in
main.tex (the journal's 150 to 250 words, each formula counted by its tokens), its characters, and the words
and characters of the plain copy (the same 250 words; arXiv's 1,920 characters).
"""

import sys
from pathlib import Path


def main() -> None:
    tex = Path(sys.argv[1]).read_text(encoding="utf-8")
    start = tex.index("\\begin{abstract}") + len("\\begin{abstract}")
    end = tex.index("\\end{abstract}")
    abstract = tex[start:end].strip()
    print(f"TeX: {len(abstract.split())} tokens, {len(abstract)} characters")
    if len(sys.argv) > 2:
        plain = Path(sys.argv[2]).read_text(encoding="utf-8").strip()
        print(f"plain: {len(plain.split())} words, {len(plain)} characters (arXiv's cap 1,920)")


if __name__ == "__main__":
    main()
