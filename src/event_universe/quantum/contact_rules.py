"""Occupation contracts for the finite localized contact candidate."""

from .event_rules import LocalInstrument, LocalUnitary
from .state import Amplitude


def preserves_occupation(rule: LocalUnitary) -> None:
    """Every nonzero coefficient stays within one binary occupation sector."""
    if len(rule.matrix) not in (2, 4):
        raise ValueError("contact propagation acts on one or two binary modes")
    for output, row in enumerate(rule.matrix):
        for source, coefficient in enumerate(row):
            if coefficient != Amplitude(0, 0) and output.bit_count() != source.bit_count():
                raise ValueError("contact propagation must preserve occupation")


def validates_preparation(rule: LocalUnitary) -> None:
    if len(rule.matrix) != 2 or rule.matrix[0][0] != Amplitude(0, 0):
        raise ValueError("contact preparation must take vacuum to one excitation")


def validates_capture(instrument: LocalInstrument) -> None:
    if len(instrument.branches) != 2 or any(len(m) != 2 for m in instrument.branches):
        raise ValueError("capture requires binary null and absorption outcomes")
    for outcome, matrix in enumerate(instrument.branches):
        for row, coefficients in enumerate(matrix):
            for column, coefficient in enumerate(coefficients):
                if (row, column) != (0, outcome) and coefficient != Amplitude(0, 0):
                    raise ValueError("capture must leave vacuum and transfer occupied inventory")
