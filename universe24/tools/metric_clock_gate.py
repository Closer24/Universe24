"""Retired clock-rate preset; its variable-divisor calibration is not portable.

The active engine has fixed divisor six. The former weak-field frequency sweep
was a different model and cannot validate clocks in the current default.
Use clock_epochs for passive recurrence measurements of explicit fixed-six data.
"""

RETIRED_REASON = (
    "The previous metric clock-rate preset is retired. Its calibration depended "
    "on a variable divisor. No equivalent fixed-six gravitational clock model "
    "has been established. Use universe24.tools.clock_epochs for generic audits."
)


def run_gate(*args, **kwargs):
    raise NotImplementedError(RETIRED_REASON)


def main():
    raise SystemExit(RETIRED_REASON)


if __name__ == "__main__":
    main()
