"""Shared helpers for the paper's checks: reading arrow.tex, stripping LaTeX to plain text, splitting it into sentences and into its parts (abstract, sections, conclusion)."""
from __future__ import annotations
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
TEX = PAPER / "arrow.tex"


def read_tex(path: Path = TEX) -> str:
    return path.read_text(encoding="utf-8")


def strip_comments(tex: str) -> str:
    return "\n".join(line.split("%", 1)[0] if not line.lstrip().startswith("%") else "" for line in tex.splitlines())


def abstract_of(tex: str) -> str:
    """The abstract's text as written between \\abstract{ and the matching brace."""
    i = tex.index("\\abstract{") + len("\\abstract{")
    depth, j = 1, i
    while depth:
        c = tex[j]
        depth += 1 if c == "{" else -1 if c == "}" else 0
        j += 1
    return tex[i:j - 1]


def body_of(tex: str) -> str:
    """From \\maketitle to the Statements and Declarations: the body with its section headings."""
    i = tex.index("\\maketitle")
    j = tex.index("\\section*{Statements and Declarations}")
    return tex[i:j]


def sections_of(tex: str) -> dict[str, str]:
    """The body split by \\section{...}: {title: text}."""
    body = body_of(tex)
    parts = re.split(r"\\section\{([^}]*)\}\\label\{[^}]*\}", body)
    out = {}
    for k in range(1, len(parts), 2):
        out[parts[k]] = parts[k + 1]
    return out


def plain(tex: str) -> str:
    """LaTeX stripped to plain words: figures and tables dropped, math kept as its text, commands removed."""
    t = strip_comments(tex)
    t = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", " ", t, flags=re.S)
    t = re.sub(r"\\begin\{table\}.*?\\end\{table\}", " ", t, flags=re.S)
    t = re.sub(r"\\begin\{equation\}.*?\\end\{equation\}", " [formula] ", t, flags=re.S)
    t = re.sub(r"\\cite\{[^}]*\}", "[cite]", t)
    t = re.sub(r"\\(?:ref|label|url)\{[^}]*\}", " ", t)
    t = re.sub(r"\\(?:section\*?|paragraph|caption|textbf|emph)\{([^}]*)\}", r"\1", t)
    t = t.replace("``", '"').replace("''", '"')
    t = re.sub(r"\\item", " ", t)
    t = re.sub(r"\\begin\{[^}]*\}|\\end\{[^}]*\}", " ", t)
    t = re.sub(r"\$([^$]*)\$", r"\1", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = t.replace("{,}", ",").replace("{", "").replace("}", "").replace("~", " ")
    return re.sub(r"[ \t]+", " ", t)


def sentences(text: str) -> list[str]:
    """Sentences of a plain text, split at a full stop, question or exclamation mark followed by a space and a capital or a quote."""
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"\[(])", text)
    return [p.strip() for p in parts if p.strip()]
