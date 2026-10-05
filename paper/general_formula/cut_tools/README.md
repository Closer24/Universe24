# The cut tools

Scripts the writer used on the long version and hands to the editor for the short one. Each reads the two TeX files it is given and changes nothing but what its name says.

| Script | What it does | How to run |
| --- | --- | --- |
| `reorder_bib.py` | Puts each file's bibliography into the order of first citation (the venue's numbered style), printing the keys cited without an entry and the entries never cited. Run after every edit; the pointers gate demands the order. | `python paper/general_formula/cut_tools/reorder_bib.py paper/general_formula/main.tex paper/general_formula/supplement.tex` |
| `sn_build.py` | Builds a TeX source in Springer's `sn-jnl` class (`../sn/sn-jnl.cls`) in a scratch folder and prints the page count and the page at which every section starts. A source already in `sn-jnl` is built as it is; an `article` source is converted (the front matter to `\title`, `\author*`, `\affil`, `\abstract`, `\keywords`). | `python paper/general_formula/cut_tools/sn_build.py paper/general_formula/main.tex --out /tmp/sn` |
| `abstract_count.py` | Counts the abstract: the TeX tokens of `main.tex`'s abstract and the words and characters of `abstract_journal.txt` (the rules: 150 to 250 words in both counts; at most 1,920 characters for arXiv). | `python paper/general_formula/cut_tools/abstract_count.py paper/general_formula/main.tex paper/general_formula/abstract_journal.txt` |
| `dupfind.py` | Prints the word runs (eleven words by default) that occur twice or more in a file, and the formulas with an equals sign written twice. | `python paper/general_formula/cut_tools/dupfind.py paper/general_formula/main.tex` |
| `crossref_check.py` | Checks every `\bibitem` with a DOI against Crossref (volume, year, first page, title words), printing the mismatches and the entries without a DOI. Needs the network. | `python paper/general_formula/cut_tools/crossref_check.py paper/general_formula/main.tex paper/general_formula/supplement.tex` |
| `sent.py` | A sentence-level grep: prints the sentence that matches, not the paragraph (the TeX files hold one paragraph per line). | `python paper/general_formula/cut_tools/sent.py paper/general_formula/main.tex "pattern"` |

The class and the style Springer's template zip of 2024-12-13 holds, `sn-jnl.cls` (LPPL 1.3c) and `sn-mathphys-num.bst`, are in `../sn/`, so that `sn_build.py` builds from the repository alone.
