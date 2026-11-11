"""Divisor rescaling is no longer a runtime feature."""
def lift_tensor(tensor, factor):
    """Identity is harmless; all nonidentity divisor changes are rejected."""
    if type(factor) is not int or factor != 1:
        raise ValueError("divisor scaling was removed; only identity factor 1 is allowed")
    return tensor
