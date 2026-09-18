"""Build one self-contained HTML page for the model owner from a tables.md, a
record and a GIF (embedded as a data URI). Usage:
  python build_page.py --title T --tables tables.md --gif file.gif --notes notes.md --out page.html
"""
import argparse
import base64
import html
import re
from pathlib import Path


def md_to_html(text):
    """A small Markdown subset: headings, paragraphs, pipe tables, bullet lists, code spans."""
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [r.strip().strip("|").split("|") for r in rows]
            head = cells[0]
            body = [r for r in cells[1:] if not all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in r)]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c.strip())}</th>" for c in head) + "</tr></thead><tbody>")
            for r in body:
                out.append("<tr>" + "".join(f"<td>{inline(c.strip())}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1)) + 1
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                item = lines[i][2:]
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and not lines[i].startswith("- "):
                    item += " " + lines[i].strip()
                    i += 1
                items.append(item)
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        if not line.strip():
            i += 1
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "#", "- ")):
            para.append(lines[i])
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


CSS = """
:root { --bg: #fbfaf7; --ink: #1d1d1b; --muted: #5c5a55; --line: #d9d5cc; --accent: #7a3e12; --head: #efeae0; --code: #f1eee7; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #16171a; --ink: #e7e5df; --muted: #a09d95; --line: #3a3c42; --accent: #e0a070; --head: #23252b; --code: #23252b; } }
:root[data-theme="dark"] { --bg: #16171a; --ink: #e7e5df; --muted: #a09d95; --line: #3a3c42; --accent: #e0a070; --head: #23252b; --code: #23252b; }
html { background: var(--bg); }
body { margin: 0; padding: 24px 16px 48px; background: var(--bg); color: var(--ink); font: 15px/1.5 Georgia, "Times New Roman", serif; max-width: 1100px; margin-inline: auto; }
h1 { font-size: 1.7em; margin: 0 0 4px; } h2 { font-size: 1.3em; margin: 32px 0 8px; border-bottom: 1px solid var(--line); padding-bottom: 4px; }
h3 { font-size: 1.1em; margin: 24px 0 6px; } h4 { font-size: 1em; margin: 18px 0 4px; }
p { margin: 8px 0; } .muted { color: var(--muted); font-size: 0.92em; }
code { font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.9em; background: var(--code); padding: 1px 4px; border-radius: 3px; }
table { border-collapse: collapse; margin: 10px 0 18px; font-size: 0.86em; display: block; overflow-x: auto; max-width: 100%; }
th, td { border: 1px solid var(--line); padding: 4px 8px; text-align: right; white-space: nowrap; } th { background: var(--head); text-align: center; }
td:first-child, th:first-child { text-align: left; }
figure { margin: 16px 0; } figure img { max-width: 100%; height: auto; border: 1px solid var(--line); border-radius: 4px; background: #000; }
figcaption { color: var(--muted); font-size: 0.9em; margin-top: 4px; }
ul { padding-left: 22px; }
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--tables", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--gif", type=Path, required=True)
    parser.add_argument("--gif-caption", default="")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    gif = base64.b64encode(args.gif.read_bytes()).decode("ascii")
    notes = md_to_html(args.notes.read_text(encoding="utf-8"))
    tables = md_to_html(args.tables.read_text(encoding="utf-8"))
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(args.title)}</title><style>{CSS}</style></head>
<body>
<h1>{html.escape(args.title)}</h1>
<p class="muted">{inline(args.subtitle)}</p>
{notes}
<h2>The rendering</h2>
<figure><img src="data:image/gif;base64,{gif}" alt="{html.escape(args.gif_caption)}"><figcaption>{inline(args.gif_caption)}</figcaption></figure>
<h2>The tables</h2>
{tables}
</body></html>
"""
    args.out.write_text(page, encoding="utf-8")
    print(args.out, len(page.encode("utf-8")), "bytes")


if __name__ == "__main__":
    main()
