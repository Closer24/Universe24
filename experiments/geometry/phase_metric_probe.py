"""Retired experiment from the variable-divisor model.

The repository now uses one fixed scalar divisor, six. This module is an
explicit migration marker, not an alternative runtime. Historical sources
and evidence remain in Git history; no old physical claim is revalidated.
"""

REASON = 'Its phase and probe normalization used a nonunit divisor. The old signal-speed comparison has not been re-established for the fixed-six law.'


def main():
    raise SystemExit("Retired experiment: " + REASON)


if __name__ == "__main__":
    main()
