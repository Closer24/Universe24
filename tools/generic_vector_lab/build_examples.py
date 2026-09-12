"""Authoring helper only: runtime loads the resulting external definitions.json."""

import json
from pathlib import Path


def ref(name):
    return {"ref": name}


def val(value, unit="one"):
    return {"value": value, "unit": unit}


def op(name, *args):
    return {"op": name, "args": list(args)}


def field(unit, size=1):
    return {"unit": unit, "size": size}


def output(kind, **fields):
    return {"type": kind, "fields": fields}


def reaction(kinds, products, **extra):
    return {
        "inputs": [{"alias": chr(97 + i), "types": [kind]} for i, kind in enumerate(kinds)],
        "outputs": products,
        **extra,
    }


units = {"one": [0, 0], "energy": [2, 0], "charge": [0, 1], "amplitude": [1, 0]}
zero_e, zero_q, zero_p = val(0, "energy"), val(0, "charge"), val([0, 0, 0], "energy")
massive = {
    "fields": {
        "mass": field("energy"),
        "p": field("energy", 3),
        "q": field("charge"),
        "E": field("energy"),
    },
    "derived": {
        "rest_energy": ref("mass"),
        "kinetic_energy": op("sub", ref("E"), ref("mass")),
    },
    "constraints": [
        op("gt", ref("mass"), zero_e),
        op("gt", ref("E"), zero_e),
        op(
            "eq",
            op("mul", ref("E"), ref("E")),
            op("add", op("norm2", ref("p")), op("mul", ref("mass"), ref("mass"))),
        ),
    ],
}
photon = {
    "fields": {"p": field("energy", 3), "E": field("energy")},
    "derived": {"q": zero_q},
    "constraints": [
        op("gt", ref("E"), zero_e),
        op("eq", op("mul", ref("E"), ref("E")), op("norm2", ref("p"))),
    ],
}
classical = {
    "fields": {"mass": field("energy"), "p": field("energy", 3), "q": field("charge")},
    "derived": {"E": op("div", op("norm2", ref("p")), op("mul", 2, ref("mass")))},
    "constraints": [op("gt", ref("mass"), zero_e)],
}
wave = {
    "fields": {"amplitude": field("amplitude", 3)},
    "derived": {
        "E": op("div", op("norm2", ref("amplitude")), 2),
        "q": zero_q,
        "p": zero_p,
    },
    "constraints": [],
}


def body(kind, mass, energy, momentum, charge=0):
    return output(
        kind,
        mass=val(mass, "energy"),
        E=val(energy, "energy"),
        p=val(momentum, "energy"),
        q=val(charge, "charge"),
    )


def light(energy, momentum):
    return output("pulse", E=val(energy, "energy"), p=val(momentum, "energy"))


rules = {
    "annihilate": reaction(["electron", "positron"], [light(1, [1, 0, 0]), light(1, [-1, 0, 0])]),
    "pair_creation": reaction(
        ["pulse", "pulse"],
        [body("electron", 1, 1, [0, 0, 0], -1), body("positron", 1, 1, [0, 0, 0], 1)],
    ),
    "decay_x": reaction(["unstable"], [light(1, [1, 0, 0]), light(1, [-1, 0, 0])]),
    "decay_y": reaction(["unstable"], [light(1, [0, 1, 0]), light(1, [0, -1, 0])]),
    "capture": reaction(
        ["constituent", "constituent"],
        [
            body("bound", 1, 1, [0, 0, 0]),
            light({"n": 1, "d": 2}, [{"n": 1, "d": 2}, 0, 0]),
            light({"n": 1, "d": 2}, [{"n": -1, "d": 2}, 0, 0]),
        ],
    ),
    "dissociate": reaction(
        ["bound", "pulse", "pulse"],
        [body("constituent", 1, 1, [0, 0, 0]), body("constituent", 1, 1, [0, 0, 0])],
    ),
    "absorb": reaction(["ground", "pulse"], [body("excited", 4, 5, [3, 0, 0])]),
    "emit": reaction(["excited"], [body("ground", 2, 2, [0, 0, 0]), light(3, [3, 0, 0])]),
}
# Classical elastic impulse, valid for any nonzero 3-D normal and positive masses.
rules["elastic"] = reaction(
    ["classical", "classical"],
    [
        output(
            "classical",
            mass=ref("a.mass"),
            q=ref("a.q"),
            p=op("add", ref("a.p"), ref("impulse")),
        ),
        output(
            "classical",
            mass=ref("b.mass"),
            q=ref("b.q"),
            p=op("sub", ref("b.p"), ref("impulse")),
        ),
    ],
    parameters={"normal": field("one", 3)},
    let={
        "relative_v": op(
            "sub",
            op("div", ref("a.p"), ref("a.mass")),
            op("div", ref("b.p"), ref("b.mass")),
        ),
        "inverse_mass": op("add", op("div", 1, ref("a.mass")), op("div", 1, ref("b.mass"))),
        "scale": op(
            "div",
            op("mul", -2, op("dot", ref("relative_v"), ref("normal"))),
            op("mul", ref("inverse_mass"), op("norm2", ref("normal"))),
        ),
        "impulse": op("mul", ref("scale"), ref("normal")),
    },
    when=op("gt", op("dot", ref("relative_v"), ref("normal")), 0),
)
rules["mix_fields"] = reaction(
    ["field_A", "field_B"],
    [
        output(
            "field_A",
            amplitude=op(
                "add",
                op("mul", val({"n": 3, "d": 5}), ref("a.amplitude")),
                op("mul", val({"n": 4, "d": 5}), ref("b.amplitude")),
            ),
        ),
        output(
            "field_B",
            amplitude=op(
                "add",
                op("mul", val({"n": -4, "d": 5}), ref("a.amplitude")),
                op("mul", val({"n": 3, "d": 5}), ref("b.amplitude")),
            ),
        ),
    ],
)
data = {
    "limits": {
        "cell_capacity": 6,
        "max_participants": 6,
        "max_products": 6,
        "link_capacity": 12,
        "match_attempts": 2000,
    },
    "description": "Mechanism examples in normalized natural units c=1. No fitted real-particle constants or cross sections.",
    "units": units,
    "types": {
        **{
            name: massive
            for name in [
                "electron",
                "positron",
                "unstable",
                "constituent",
                "bound",
                "ground",
                "excited",
            ]
        },
        "pulse": photon,
        "classical": classical,
        "field_A": wave,
        "field_B": wave,
    },
    "balances": {
        name: {"zero": zero, "expression": ref(name)}
        for name, zero in [("E", zero_e), ("p", zero_p), ("q", zero_q)]
    },
    "reactions": rules,
    "quantum_rotation": [
        [{"n": 3, "d": 5}, {"n": -4, "d": 5}],
        [{"n": 4, "d": 5}, {"n": 3, "d": 5}],
    ],
    "schedules": {"decay": {"weights": [3, 1], "branches": [None, "decay_x"]}},
    "example_seed": 12345,
}
# A simultaneous six-input node rule, without contact geometry or a normal.
# All species definitions and the permitted six-way composition live in JSON.
for name in ["disturbance_A", "disturbance_B", "disturbance_C"]:
    data["types"][name] = classical
composition = ["disturbance_A"] * 2 + ["disturbance_B"] * 2 + ["disturbance_C"] * 2
products = []
for i, kind in enumerate(composition):
    alias = chr(97 + i)
    # Cyclic orthogonal map (px,py,pz) -> (pz,px,py), expressed in vector algebra.
    rotated = op(
        "add",
        op(
            "add",
            op("mul", op("dot", ref(alias + ".p"), val([1, 0, 0])), val([0, 1, 0])),
            op("mul", op("dot", ref(alias + ".p"), val([0, 1, 0])), val([0, 0, 1])),
        ),
        op("mul", op("dot", ref(alias + ".p"), val([0, 0, 1])), val([1, 0, 0])),
    )
    products.append(output(kind, mass=ref(alias + ".mass"), q=ref(alias + ".q"), p=rotated))
data["reactions"]["six_node_exchange"] = reaction(composition, products)
data["node_demo"] = {
    "rule": "six_node_exchange",
    "participants": [
        {"type": kind, "fields": {"mass": 1, "q": 0, "p": p}}
        for kind, p in zip(
            composition,
            [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
            strict=True,
        )
    ],
    "view": {
        "frames_per_state": 32,
        "duration_ms": 80,
        "size": 640,
        "colors": ["#ffbc5c", "#59d4ff", "#cf8bff"],
    },
}

if __name__ == "__main__":
    Path(__file__).with_name("definitions.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
