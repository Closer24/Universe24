"""Compose the separately owned nuclear and electron initialization builders."""

from electron_configuration import add_electron
from strong_configuration import build_strong_document


def build_joint_document(
    *,
    electron_parameters: dict[str, int],
    shape: tuple[int, int, int],
    ticks: int,
    strong_parameters: dict[str, int] | None = None,
) -> dict[str, object]:
    pair = build_strong_document(parameters=strong_parameters or {}, shape=shape, ticks=ticks)
    return add_electron(pair, parameters=electron_parameters)
