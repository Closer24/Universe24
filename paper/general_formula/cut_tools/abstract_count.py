"""Count the abstract both ways the venues count it.

Usage: python abstract_count.py main.tex abstract_journal.txt. Prints the whitespace tokens of the abstract in
main.tex (an article-class environment or Springer's class's one-line \\abstract), the tokens carrying a letter
(the journal's 150 to 250 words, a formula's symbols aside), its characters, and the words and characters of
the plain copy (arXiv's 1,920 characters).
"""

import re
import sys
from pathlib import Path


def main() -> None:
    tex = Path(sys.argv[1]).read_text(encoding="utf-8")
    if "\\begin{abstract}" in tex:
        start = tex.index("\\begin{abstract}") + len("\\begin{abstract}")
        end = tex.index("\\end{abstract}")
        abstract = tex[start:end].strip()
    else:  # Springer's class: one line, \abstract{...}
        abstract = re.search(r"\\abstract\{(.*)\}\n", tex).group(1)
    tokens = abstract.split()
    words = sum(1 for token in tokens if re.search(r"[A-Za-z]", token))
    print(f"TeX: {len(tokens)} tokens, {words} words carrying a letter, {len(abstract)} characters")
    if len(sys.argv) > 2:
        plain = Path(sys.argv[2]).read_text(encoding="utf-8").strip()
        print(f"plain: {len(plain.split())} tokens, {len(plain)} characters (arXiv's cap 1,920)")


if __name__ == "__main__":
    main()
