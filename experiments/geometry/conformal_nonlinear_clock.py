"""Retired experiment from the variable-divisor model.

The repository now uses one fixed scalar divisor, six. This module is an
explicit migration marker, not an alternative runtime. Historical sources
and evidence remain in Git history; no old physical claim is revalidated.
"""

REASON = 'Its coupled-clock refinement used a variable divisor. No fixed-six replacement with the same continuum estimates has been established.'


def main():
    raise SystemExit("Retired experiment: " + REASON)


if __name__ == "__main__":
    main()
