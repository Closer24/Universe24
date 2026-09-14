"""Author a local response to a reencoded position-basis carrier state.

Source and captured moments follow the immutable local row of a declared
nearest-Link momentum operator. Rank-one position reencoding sets the new
carrier's moments; it does not recover its incident momentum or query the remote
wave. These moments are metadata, not fixed conserved quantum inventory. The
later ordinary pair rules preserve their first and second moments explicitly.
Gate and measurement exchange remain outside a closed total-energy claim.
"""

if __package__:
    from .local_moment_exchange import configuration as moment_configuration
    from .spatial_momentum import local_position_moments
else:
    from local_moment_exchange import configuration as moment_configuration
    from spatial_momentum import local_position_moments


def _position_values(local_row, axis):
    moments = local_position_moments(local_row)
    mean = [0, 0, 0]
    mean[axis] = moments["mean_momentum"]
    return {
        "coarse_momentum": mean,
        "momentum_spread": moments["variance"],
        "momentum_known": int(moments["variance"] == 0),
    }


def configuration(axis=0, sign=1, reservoir=True, normal_budget=10000, link_ticks=1, capture="endpoint"):
    """Return an endpoint or middle capture, with three incoming reservoir hops.

    The chain's oriented Links are register 0 to 1 and register 1 to 2.
    Its endpoint local rows have one unit coefficient; the middle has two.
    No evolving amplitude, global sum or diagnostic feeds this authoring path.
    """
    if capture not in ("endpoint", "middle"):
        raise ValueError("capture must be endpoint or middle")
    raw = moment_configuration(axis, sign, reservoir, normal_budget, link_ticks)
    raw["model_id"] = "position-reencoding-local-moment-response-candidate-v1"
    for field in raw["fields"]:
        if field["name"] in ("coarse_momentum", "momentum_spread"):
            field["conserved"] = False

    source_values = _position_values((-1,), axis)
    capture_values = _position_values((1,) if capture == "endpoint" else (1, -1), axis)
    for kind in raw["disturbance_types"]:
        if kind["name"] == "incoming_charge":
            kind["defaults"].update(source_values)
        elif kind["name"] == "localized_charge":
            kind["defaults"].update(capture_values)
    for seed in raw["seeds"]:
        if seed["type"] == "incoming_charge":
            seed.setdefault("values", {}).update(source_values)

    domain = raw["event_program"]["domains"][0]
    domain["capture"]["register_indices"] = [2 if capture == "endpoint" else 1]
    domain["capture"]["output"].setdefault("values", {}).update(capture_values)
    if capture == "middle":
        for address in raw["event_program"]["addresses"]:
            address[axis] += 1
        for seed in raw["seeds"]:
            if seed["type"] == "incoming_charge" or (
                seed["type"] == "contact_probe" and seed["position"][axis] == 1
            ):
                seed["position"][axis] += 1
        # The existing capture probe remains at coordinate 3, now the middle.
        # Reservoir starts and the three-hop routing phase remain unchanged.

    for rule in raw["interactions"]:
        for name, field in (
            ("total_first_moment", "coarse_momentum"),
            ("total_spread", "momentum_spread"),
        ):
            rule["invariants"].append(
                {
                    "name": name,
                    "expression": {
                        "op": "add",
                        "args": [
                            {"field": field, "side": "left"},
                            {"field": field, "side": "right"},
                        ],
                    },
                }
            )
    return raw
