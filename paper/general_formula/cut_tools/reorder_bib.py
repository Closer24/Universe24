"""Put a TeX file's bibliography into the order of first citation, the venue's numbered style.

Usage: python reorder_bib.py main.tex [supplement.tex ...]. Each file is rewritten in place; the keys cited
with no entry and the entries never cited are printed, and the exit status is 1 if either list is not empty.
"""

import re
import sys
from pathlib import Path


def reorder(text: str) -> tuple[str, list[str], list[str]]:
    """Return the text with its bibliography reordered, the missing keys and the uncited keys."""
    start = text.index("\\begin{thebibliography}")
    end = text.index("\\end{thebibliography}")
    head_end = text.index("\n", start) + 1
    block = text[head_end:end]
    items = re.findall(r"\\bibitem\{[^}]*\}.*?(?=\\bibitem\{|$)", block, re.S)
    keyed = {re.match(r"\\bibitem\{([^}]*)\}", item).group(1): item.strip() for item in items}
    order: list[str] = []
    for match in re.finditer(r"\\cite(?:\[[^\]]*\])?\{([^}]*)\}", text[:start]):
        for key in match.group(1).split(","):
            key = key.strip()
            if key not in order:
                order.append(key)
    missing = [key for key in order if key not in keyed]
    uncited = [key for key in keyed if key not in order]
    new_block = "\n".join(keyed[key] for key in order if key in keyed) + "\n"
    return text[:head_end] + new_block + text[end:], missing, uncited


def main() -> int:
    status = 0
    for name in sys.argv[1:]:
        path = Path(name)
        text, missing, uncited = reorder(path.read_text(encoding="utf-8"))
        path.write_text(text, encoding="utf-8")
        print(f"{path.name}: missing {missing} uncited {uncited}")
        status |= bool(missing or uncited)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
