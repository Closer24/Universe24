"""Retired resolution-lift clock candidate.

Its large-divisor field assembly and claimed weak response are not a valid
fixed-six default. Keeping this entrypoint makes old commands fail explicitly.
"""

RETIRED_REASON = (
    "The previous connected-clock candidate is retired with its resolution-lift "
    "construction. No gravity-dependent clock connection is established in the "
    "fixed-six reference model. Use system_inventory and clock_epochs for audits."
)


def build_candidate(*args, **kwargs):
    raise NotImplementedError(RETIRED_REASON)


def paired_control(*args, **kwargs):
    raise NotImplementedError(RETIRED_REASON)


def main():
    raise SystemExit(RETIRED_REASON)


if __name__ == "__main__":
    main()
