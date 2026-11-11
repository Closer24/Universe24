"""Former divisor-changing preparation API, explicitly retired.

The only supported divisor is six. Multiplying remainders would leave its
allowed range and does not define an equivalent preparation.
"""
from ..core import State, Tensor


def _identity_only(state: State, tensor: Tensor, factor: int) -> State:
    if not isinstance(state, State) or not isinstance(tensor, Tensor):
        raise TypeError("a complete State and validated Tensor are required")
    if type(factor) is not int or factor != 1:
        raise ValueError("divisor-changing resolution lifts are retired; only identity factor one is supported")
    if state.G != tensor.G or any(not 0 <= int(v) < 6 for v in state.r.flat):
        raise ValueError("state does not match the fixed-divisor tensor")
    return state.copy()


def lift_state(state: State, tensor: Tensor, factor: int) -> State:
    return _identity_only(state, tensor, factor)


def unlift_state(state: State, tensor: Tensor, factor: int) -> State:
    return _identity_only(state, tensor, factor)


__all__ = ["lift_state", "unlift_state"]
