"""Retired experiment from the variable-divisor model.

The repository now uses one fixed scalar divisor, six. This module is an
explicit migration marker, not an alternative runtime. Historical sources
and evidence remain in Git history; no old physical claim is revalidated.
"""

REASON = 'Its refinement family changed the shared divisor and used fractional effective couplings. The old clock-convergence claims do not apply to the fixed-six law.'


def main():
    raise SystemExit("Retired experiment: " + REASON)


if __name__ == "__main__":
    main()
