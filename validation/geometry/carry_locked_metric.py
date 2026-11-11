"""Retired experiment from the variable-divisor model.

The repository now uses one fixed scalar divisor, six. This module is an
explicit migration marker, not an alternative runtime. Historical sources
and evidence remain in Git history; no old physical claim is revalidated.
"""

REASON = 'Its carry-free checkerboard identity depended on the previous divisor and spatial coefficients. It is not a control of the new fixed-six model.'


def main():
    raise SystemExit("Retired experiment: " + REASON)


if __name__ == "__main__":
    main()
