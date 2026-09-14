"""Semantic support of configured local occupation-transfer outcomes."""

from .event_rules import LocalInstrument
from .state import Amplitude


def validate_outcomes(instrument: LocalInstrument, effects: tuple[str, ...], *, source: bool) -> None:
    """Completeness belongs to LocalInstrument; effects constrain every coefficient."""
    if type(source) is not bool:
        raise ValueError("contact source selection must be boolean")
    if type(effects) is not tuple or len(effects) != len(instrument.branches):
        raise ValueError("one effect per contact outcome is required")
    if not source and (not effects or effects[0] != "null" or effects.count("null") != 1):
        raise ValueError("capture requires exactly one null outcome at index zero")
    permitted = (
        {"localized": {(0, 0), (1, 1)}, "new_wave": {(1, 0), (0, 1)}}
        if source
        else {
            "null": {(0, 0)},
            "continue": {(1, 1)},
            "localized": {(0, 1)},
            "new_wave": {(1, 1)},
        }
    )
    for matrix, effect in zip(instrument.branches, effects, strict=True):
        if effect not in permitted or len(matrix) != 2:
            raise ValueError("unsupported local contact outcome effect or dimension")
        for row, coefficients in enumerate(matrix):
            for column, coefficient in enumerate(coefficients):
                if coefficient != Amplitude(0, 0) and (row, column) not in permitted[effect]:
                    raise ValueError("contact matrix violates its declared inventory effect")
