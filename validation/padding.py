"""Checked passive views of research sectors inside the 48-channel allocation.

These views never advance the Engine or discard active state. A nonzero idle
register, unexpected tail law or noncanonical allocation is an error.
"""
from universe24.core import State, Tensor
from universe24.system.bundle import pad_tensor


def sector_state(state, count):
    if not isinstance(state, State):
        raise ValueError("expected a complete State")
    if state.G == count:
        return state
    if state.G != 48:
        raise ValueError(f"expected {count} research channels or exactly 48 retained channels")
    checked = State(state.L, state.a, state.b, state.r)
    if any(bool((bank[count:] != 0).any()) for bank in (checked.a, checked.b, checked.r)):
        raise ValueError("nonzero idle channel in research sector")
    return State(state.L, state.a[:count], state.b[:count], state.r[:count])


def sector_tensor(tensor, count):
    if tensor.G == count:
        return tensor
    data = tensor.to_dict()
    data['gears'] = data['gears'][:count]
    # Construction rejects any term referencing an allegedly idle channel.
    reduced = Tensor.from_dict(data, strict_support=True)
    if pad_tensor(reduced).fingerprint != tensor.fingerprint:
        raise ValueError("unexpected padded research tensor")
    return reduced


def construction_inputs(bundle):
    """Reclaim only verified idle tail slots when preparing new apparatus."""
    owners = list(bundle.channels)
    count = len(owners)
    while count and owners[count-1]['owner'] == 'system-padding':
        count -= 1
    return sector_tensor(bundle.tensor, count), sector_state(bundle.seed, count), owners[:count]
