#!/bin/sh
# Builds arrow.pdf from arrow.tex, figures.tex and the .bib files with the Springer Nature class in sn/:
# pdflatex, bibtex, pdflatex, pdflatex; no network, no shell escape. Then tools/run_clocks.py (the two clocks counted on the board, run_clocks.json) and the eight checks, in order, stopping at the first failure:
# check_numbers (every integer against the run's data), check_formulas (every derived number recomputed), check_words
# (the forbidden words, the mandated sentences, the Abstract's length), check_notation (every symbol defined before its first use, one meaning),
# check_terms (every term defined before its first use), check_circularity (results against assumptions),
# check_refs (the citations and the .bib files), check_layout (the body ending by page 18, the figure's labels, overfull boxes).
set -e
cd "$(dirname "$0")"
export TEXINPUTS="sn:${TEXINPUTS}"
export BSTINPUTS="sn:${BSTINPUTS}"
python3 -I tools/make_figure.py   # Figure 1 as TikZ into figures_board.tex
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape arrow.tex > build.log 2>&1
bibtex arrow >> build.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape arrow.tex >> build.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error -no-shell-escape arrow.tex >> build.log 2>&1
grep -c "^!" build.log && echo "errors above" || echo "no errors"
pdfinfo arrow.pdf | grep Pages
RUN_DIR="${RUN_DIR:-./run3d_fixed}"   # the fixed-board run's world, report and rows, committed beside the paper
PYTHONPATH=../../src python3 -I tools/run_clocks.py ../../src   # the two clocks counted on the board with the program's functions, run_clocks.json
python3 -I tools/run_momentum.py ../../src   # the momentum at the click read on the board as the click runs, run_momentum.json
python3 -I "$RUN_DIR/ensemble/ensemble_seeds.py" --check   # the ensemble's summary recomputed from its saved rows (the 1,200 runs themselves take about fifteen minutes and are not rerun here)
python3 -I tools/check_numbers.py "$RUN_DIR"
python3 -I tools/check_formulas.py "$RUN_DIR"
# the Abstract's limit is 250 words
python3 -I tools/check_words.py arrow.pdf "${ABSTRACT_WORDS:-250}"
python3 -I tools/check_notation.py
python3 -I tools/check_terms.py
python3 -I tools/check_circularity.py
python3 -I tools/check_refs.py
python3 -I tools/check_layout.py arrow.pdf arrow.log
rm -f arrow.aux arrow.blg arrow.log arrow.out build.log
