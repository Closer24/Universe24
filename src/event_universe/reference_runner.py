"""Explicit CLI for historical configurations that supply complete equations."""

from pathlib import Path

from .runner import main, run_initialization


def run_reference_initialization(
    initialization: Path,
    output: Path,
    *,
    ticks: int | None = None,
    visualize: bool = False,
    frame_stride: int = 1,
    observer: Path | None = None,
) -> Path:
    return run_initialization(
        initialization,
        output,
        ticks=ticks,
        visualize=visualize,
        frame_stride=frame_stride,
        observer=observer,
        reference=True,
    )


if __name__ == "__main__":
    main(reference=True)
