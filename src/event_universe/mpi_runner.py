"""Optional prelaunched MPI workers; rank zero owns the simulation and its outputs."""

import argparse
from collections.abc import Callable, Sequence
from concurrent.futures import Executor
from contextlib import AbstractContextManager, ExitStack
from importlib import import_module
from pathlib import Path
from typing import Protocol, cast

from event_universe.core.event_resolution import Planner
from event_universe.local_execution import worker_initializer
from event_universe.runner import run_initialization


class Communicator(Protocol):
    def Get_rank(self) -> int: ...

    def Get_size(self) -> int: ...


type ContextFactory = Callable[..., AbstractContextManager[Executor | None]]


class MPIExecution:
    """Borrow one static MPI pool, initialized from the canonical run's actual law."""

    def __init__(self, communicator: Communicator, context_factory: ContextFactory) -> None:
        self.communicator = communicator
        self.context_factory = context_factory
        self.stack = ExitStack()
        self.entered = False

    def __call__(self, planner: Planner) -> Executor:
        if self.entered:
            raise RuntimeError("one MPI execution context belongs to one simulation")
        initializer, arguments = worker_initializer(planner)
        self.entered = True
        executor = self.stack.enter_context(
            self.context_factory(self.communicator, root=0, initializer=initializer, initargs=arguments)
        )
        if executor is None:
            raise RuntimeError("only the coordinator may initialize an MPI simulation")
        return executor

    def close(self) -> None:
        if not self.entered:
            # Workers enter the collective before rank zero validates local input.
            # Even a preflight failure must join and close their unused context.
            self.entered = True
            self.stack.enter_context(self.context_factory(self.communicator, root=0))
        self.stack.close()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one simulation with prelaunched MPI workers and one output coordinator."
    )
    parser.add_argument("--init", required=True, type=Path, help="Initialization JSON file")
    parser.add_argument("--output", type=Path, default=Path("artifacts/run"))
    parser.add_argument("--ticks", type=int, help="Override only the requested run duration")
    parser.add_argument("--observer", type=Path, help="Local reception probe placement JSON")
    parser.add_argument("--parallel-threshold", type=int, default=64)
    parser.add_argument("--chunk-size", type=int, default=32)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Use ``mpiexec -n 3 python -m event_universe.mpi_runner --init ...``."""
    parser = _parser()
    try:
        mpi = import_module("mpi4py.MPI")
        context_factory = cast(ContextFactory, import_module("mpi4py.futures").MPICommExecutor)
    except (ImportError, RuntimeError, OSError) as error:
        parser.exit(1, f"MPI unavailable: install event-universe[mpi] and an MPI runtime. {error}\n")
    communicator = cast(Communicator, mpi.COMM_WORLD)
    if communicator.Get_size() < 2:
        parser.exit(
            1, "MPI requires prelaunched ranks; use mpiexec -n 3 python -m event_universe.mpi_runner.\n"
        )
    if communicator.Get_rank() != 0:
        with context_factory(communicator, root=0):
            pass
        return
    execution = MPIExecution(communicator, context_factory)
    try:
        args = parser.parse_args(argv)
        try:
            artifact = run_initialization(
                args.init,
                args.output,
                ticks=args.ticks,
                observer=args.observer,
                workers=communicator.Get_size() - 1,
                parallel_threshold=args.parallel_threshold,
                chunk_size=args.chunk_size,
                executor_factory=execution,
                execution_backend="mpi",
            )
        except Exception as error:
            parser.exit(1, f"Run failed: {error}\n")
        print(artifact.resolve())
    finally:
        execution.close()


if __name__ == "__main__":
    main()
