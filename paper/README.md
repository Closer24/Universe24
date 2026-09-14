# Paper draft

`main.tex` is the manuscript draft for Reality Theory (Universe24). It cites
only measurements recorded in [validation](../docs/VALIDATION.md) and the
experiment reports under [examples](../examples). Build with `pdflatex main.tex`
twice. The draft is not part of the simulator package and no test reads it.

`figures.py` draws the six figures from recorded summary files only (the
interference, phased-ray Bell, crossing-null and bonded-probe summaries);
`figures/` holds the PDFs it wrote from the runs recorded in the validation
log. Regenerate with:

```sh
PYTHONPATH=src python paper/figures.py --interference artifacts/causal-interference/summary.json \
  --bell artifacts/kerengonen-bell/summary.json --crossing artifacts/crossing-nulls/summary.json \
  --bond-sequence artifacts/bell-chsh/summary-bond.json \
  --bond-uniform artifacts/bell-chsh/summary-bond-uniform.json \
  --bond-biased artifacts/bell-chsh/summary-bond-biased.json --output paper/figures
```
