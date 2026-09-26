"""Commit 2 of the one stroke (ALGEBRA.md 9.91 (10) 2; 9.91 (3)): the body's numbers, the holds
of every part, the dipoles, the carried remainders, the leak test per part."""

import re
from pathlib import Path


def edit(path, pairs):
    p = Path(path)
    s = p.read_text()
    for old, new in pairs:
        if s.count(old) == 0 and s.count(new) >= 1:
            continue  # already applied
        assert s.count(old) == 1, (path, s.count(old), old[:90])
        s = s.replace(old, new)
    p.write_text(s)


W = "wt_ec/src/event_universe/events/world.py"
edit(
    W,
    [
        # the keys
        (
            """    "pair",
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit 1):
    # the body's rest pair on a family whose pair is the body's
    "kind",
""",
            """    "pair",
    # THE BODY'S KIND (ALGEBRA.md 9.85 (3), 9.91 (7); the one stroke, commit 1):
    # the body's rest pair on a family whose pair is the body's
    "kind",
    # THE BODY'S NUMBERS the holds read (ALGEBRA.md 9.91 (3), (7); commit 2): its
    # charge Q, its spin S and its moment mu (the momentum n is `momentum`)
    "charge",
    "spin",
    "moment",
""",
        ),
        (
            """    "held",
    "kind",
    "phase",
    "momentum",
""",
            """    "held",
    "kind",
    "charge",
    "spin",
    "moment",
    "phase",
    "momentum",
""",
        ),
        # BlockDefinition fields
        (
            """    ramp: int = 0
    start: int = 0
    margin: str = MARGIN_KINDS[0]
""",
            """    ramp: int = 0
    start: int = 0
    # THE BODY'S NUMBERS (ALGEBRA.md 9.91 (3), (7); the one stroke, commit 2): the
    # charge Q (the held sign's count at its Nodes), the spin S and the moment mu
    # (the dipoles on its Node's six neighbours); the momentum n is `momentum`
    charge: int = 0
    spin: tuple[int, int, int] = (0, 0, 0)
    moment: tuple[int, int, int] = (0, 0, 0)
    margin: str = MARGIN_KINDS[0]
""",
        ),
        # the parse
        (
            """    ramp = 0 if "ramp" not in obj else _integer(obj["ramp"], f"{label}.ramp", 0)
    start = 0 if "start" not in obj else _integer(obj["start"], f"{label}.start", 0)
""",
            """    ramp = 0 if "ramp" not in obj else _integer(obj["ramp"], f"{label}.ramp", 0)
    start = 0 if "start" not in obj else _integer(obj["start"], f"{label}.start", 0)
    # THE BODY'S NUMBERS (ALGEBRA.md 9.91 (3), (7); commit 2): charge, spin and moment,
    # required under the law (no default), integers on the axes (record 2084)
    if detector_law:
        _require_under_law(obj, label, {"charge", "spin", "moment"})
    charge = (
        0
        if "charge" not in obj
        else _integer(obj["charge"], f"{label}.charge", -AMOUNT_BOUND, AMOUNT_BOUND)
    )
    spin = _axes_vector(obj.get("spin", [0, 0, 0]), f"{label}.spin")
    moment = _axes_vector(obj.get("moment", [0, 0, 0]), f"{label}.moment")
""",
        ),
        (
            """        ramp=ramp,
        start=start,
        margin=str(margin),
""",
            """        ramp=ramp,
        start=start,
        charge=charge,
        spin=spin,
        moment=moment,
        margin=str(margin),
""",
        ),
        # the helper
        (
            """def _emitter(
    value: object,
    label: str,
""",
            """def _axes_vector(value: object, label: str) -> tuple[int, int, int]:
    \"\"\"An integer vector on the axes (record 2084: every directed thing an integer
    vector on the axes), three integers.\"\"\"
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{BEAM_LAW}: {label} must be three integers, a vector on the axes")
    return (
        _integer(value[0], f"{label}[0]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[1], f"{label}[1]", -AMOUNT_BOUND, AMOUNT_BOUND),
        _integer(value[2], f"{label}[2]", -AMOUNT_BOUND, AMOUNT_BOUND),
    )


def _emitter(
    value: object,
    label: str,
""",
        ),
        # the reach reads the body's declared charge
        (
            """        if family.held == "sign":
            return abs(
                sum(other.charge[0] * held for other, held in zip(families, entry.held, strict=True))
            )
        return quanta
""",
            """        if family.held == "sign":
            declared = entry.block.charge if entry.block is not None else 0
            return abs(
                declared
                + sum(other.charge[0] * held for other, held in zip(families, entry.held, strict=True))
            )
        return quanta
""",
        ),
    ],
)

E = "wt_ec/src/event_universe/events/detector_law.py"
edit(
    E,
    [
        # Block: the holds' accumulators
        (
            """    residue_pending: bool = False


class PairView:
""",
            """    residue_pending: bool = False
    # THE HOLDS' REMAINDERS (ALGEBRA.md 9.91 (3); the one stroke, commit 2): per
    # held family and part, the division's remainder carried between intervals
    # and the value written, (family, part) for the support's writes and ("d",
    # family, i, j, sigma) for the dipole's on the Node + sigma e_j; exact and
    # inverted with the body
    hold_carry: dict[tuple[object, ...], int] = field(default_factory=dict)
    hold_value: dict[tuple[object, ...], int] = field(default_factory=dict)


# THE COMPONENT ORDER (ALGEBRA.md 9.91 (1)): (t), (x, y, z), (xx, yy, zz, xy, xz,
# yz); the tensor's component to its two axes
TENSOR_AXES = ((0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2))


def cross_with_axis(vector: tuple[int, int, int], axis: int) -> tuple[int, int, int]:
    \"\"\"D x e_j for the axis j (ALGEBRA.md 9.91 (3)): (0, D_z, -D_y), (-D_z, 0, D_x),
    (D_y, -D_x, 0).\"\"\"
    x, y, z = vector
    return ((0, z, -y), (-z, 0, x), (y, -x, 0))[axis]


class PairView:
""",
        ),
        # the sourced flags per part
        (
            """        self._sourced_ever: dict[int, bool] = {family: False for family in self.held_families}
""",
            """        # per part (9.91 (9) (a)): (family, part), the time part 0
        self._sourced_ever: dict[tuple[int, int], bool] = {
            (family, part): False
            for family in self.held_families
            for part in range(self.families[family].components)
        }
""",
        ),
        # the body's charge
        (
            """        return sum(
            sign * quanta for sign, quanta in zip(self.family_charge, self.held[number], strict=True)
        )
""",
            """        block = self.block_by_number.get(number)
        declared = block.definition.charge if block is not None else 0
        return declared + sum(
            sign * quanta for sign, quanta in zip(self.family_charge, self.held[number], strict=True)
        )
""",
        ),
        # the hold
        (
            """        for family, record in self.held_records.items():
            source = self.families[family].held
            assert source is not None
            for number in range(len(self.held)):
                value = self.body_source(number, source)
                if value:
                    self._sourced_ever[family] = True
                block = self.block_by_number.get(number)
                mask = block.mask if block is not None else self.span_masks[number]
                record.now[mask] = value
                record.before[mask] = value
                record.remainder[mask] = 0
            self.node_level[family] = record.now
        self._effective.clear()
""",
            """        for family, record in self.held_records.items():
            source = self.families[family].held
            assert source is not None
            for number in range(len(self.held)):
                value = self.body_source(number, source)
                if value:
                    self._sourced_ever[(family, 0)] = True
                block = self.block_by_number.get(number)
                mask = block.mask if block is not None else self.span_masks[number]
                record.now[mask] = value
                record.before[mask] = value
                record.remainder[mask] = 0
            self.node_level[family] = record.now
            # THE VECTOR AND TENSOR PARTS AT THE BODIES (ALGEBRA.md 9.91 (3); commit
            # 2): the body's numbers times the held factors over the wall, the
            # remainder carried; then the dipoles on the body's Node's six neighbours
            for part_record in self.held_parts[family]:
                for block in self.blocks:
                    self._hold_part(block, family, part_record, advance, inverse)
            if advance and not inverse:
                for block in self.blocks:
                    self._hold_dipole(block, family)
        self._effective.clear()

    def _part_axes(self, family: int, part: int) -> tuple[int, tuple[int, ...]]:
        \"\"\"A component's part group (0 the time part, 1 the vector, 2 the tensor)
        and the axes it multiplies (ALGEBRA.md 9.91 (1), (3): n_a for the vector,
        n_a n_b for the tensor), by the family's parts list.\"\"\"
        offset = 0
        for group, count in enumerate(self.families[family].parts):
            if part < offset + count:
                index = part - offset
                if group == 0:
                    return 0, ()
                if group == 1:
                    return 1, (index,)
                return 2, TENSOR_AXES[index]
            offset += count
        raise ValueError(f"{BEAM_LAW}: the part {part} is beyond the family's components")

    @staticmethod
    def _carried_division(
        block: Block, key: tuple[object, ...], numerator: int, wall: int, advance: bool, inverse: bool
    ) -> int:
        \"\"\"THE DIVISION WITH ITS REMAINDER CARRIED (ALGEBRA.md 9.91 (3)): forward,
        value_t = (S + r_(t-1)) div W and r_t the remainder, kept on the body;
        backward, from (value_t, r_t) to (value_(t-1), r_(t-1)) exactly: r_(t-1)
        = value_t W + r_t - S, and value_(t-1) = S div W plus one where r_(t-1)
        is below S mod W (the only two values the sum S + r can reach); a hold
        that neither advances nor inverts rewrites the value as it stands.\"\"\"
        if inverse:
            value_now = block.hold_value.get(key, 0)
            remainder = block.hold_carry.get(key, 0)
            previous = value_now * wall + remainder - numerator
            whole, fraction = divmod(numerator, wall)
            value = whole + (1 if previous < fraction else 0)
            block.hold_value[key] = value
            block.hold_carry[key] = previous
            return value
        if advance:
            value, remainder = divmod(numerator + block.hold_carry.get(key, 0), wall)
            block.hold_value[key] = value
            block.hold_carry[key] = remainder
            return value
        return block.hold_value.get(key, 0)

    def _hold_part(
        self, block: Block, family: int, record: LiveRecord, advance: bool, inverse: bool
    ) -> None:
        \"\"\"One body's write into one component of a held family beyond the time
        part (ALGEBRA.md 9.91 (3)): factor x count x n_a (div W) for the vector,
        factor x count x n_a n_b (div W^2) for the tensor, the count the body's
        source (s or Q), n its momentum now on its wall W, the factors the
        families file's; written at every Node of the body's support at both
        levels with the remainder 0; a part no body ever sources stays silent.\"\"\"
        definition = self.families[family]
        source = definition.held
        assert source is not None
        group, axes = self._part_axes(family, record.part)
        numerator = definition.held_factors[group] * self.body_source(block.number, source)
        momentum = self._momentum_now(block)
        for axis in axes:
            numerator *= int(momentum[axis])
        wall = block.wall ** len(axes)
        if numerator:
            self._sourced_ever[(family, record.part)] = True
        value = self._carried_division(
            block, (family, record.part), numerator, wall, advance, inverse
        )
        if value == 0 and record.silent:
            return
        record.silent = False
        record.now[block.mask] = value
        record.before[block.mask] = value
        record.remainder[block.mask] = 0

    def _dipole_writes(
        self, block: Block, family: int
    ) -> list[tuple[tuple[object, ...], int, LiveRecord, tuple[int, int, int]]]:
        \"\"\"The dipole's terms of one body into a held family's vector part
        (ALGEBRA.md 9.91 (3)): at the Node + sigma e_j, the component i gains
        sigma x (D x e_j)_i, D the body's spin or moment by the family's declared
        dipole, over the family's dipole divisor with the remainder carried;
        (key, term, the component's record, the Node) per write, none beyond an
        open face.\"\"\"
        definition = self.families[family]
        if definition.held_dipole is None or len(definition.parts) < 2:
            return []
        vector = block.definition.spin if definition.held_dipole == "spin" else block.definition.moment
        if not any(vector):
            return []
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        wrap = self.kind_wrap[family]
        found: list[tuple[tuple[object, ...], int, LiveRecord, tuple[int, int, int]]] = []
        for j in range(3):
            cross = cross_with_axis(vector, j)
            for sigma in (1, -1):
                node = list(centre)
                node[j] += sigma
                if wrap[j] or self.shape[j] == 1:
                    node[j] %= self.shape[j]
                elif not 0 <= node[j] < self.shape[j]:
                    continue
                at = (int(node[0]), int(node[1]), int(node[2]))
                for i in range(3):
                    term = sigma * cross[i]
                    if term == 0:
                        continue
                    found.append((("d", family, i, j, sigma), term, self.held_parts[family][i], at))
        return found

    def _hold_dipole(self, block: Block, family: int) -> None:
        \"\"\"The dipole's writes added at the interval's hold (forward; the load's
        write included).\"\"\"
        div = self.families[family].held_dipole_div
        for key, term, record, node in self._dipole_writes(block, family):
            value = self._carried_division(block, key, term, div, True, False)
            self._sourced_ever[(family, record.part)] = True
            if value == 0:
                continue
            record.silent = False
            record.now[node] += value
            record.before[node] += value

    def _unhold_dipoles(self) -> None:
        \"\"\"The interval's dipole writes taken back (the inverse, before the fields
        step back), and their divisions stepped back to the previous interval.\"\"\"
        for family in self.held_records:
            div = self.families[family].held_dipole_div
            for block in self.blocks:
                for key, term, record, node in self._dipole_writes(block, family):
                    value = block.hold_value.get(key, 0)
                    record.now[node] -= value
                    record.before[node] -= value
                    self._carried_division(block, key, term, div, False, True)
""",
        ),
        (
            """    def _hold(self) -> None:
        \"\"\"THE HOLD (ALGEBRA.md 9.45 (2), 9.48 (2); item 51): at every body's
""",
            """    def _hold(self, advance: bool = False, inverse: bool = False) -> None:
        \"\"\"THE HOLD (ALGEBRA.md 9.45 (2), 9.48 (2); item 51; the vector and tensor
        parts and the dipoles, 9.91 (3), commit 2): at every body's
""",
        ),
        # the call sites: the load and the fields' step advance the carried divisions; the step's
        # start rewrites; the inverse steps back
        (
            """        for parts in self.held_parts.values():
            for record in parts:
                record.silent = True
        self._hold()
""",
            """        for parts in self.held_parts.values():
            for record in parts:
                record.silent = True
        self._hold(advance=True)
""",
        ),
        (
            """        for record in self.held_component_records():
            self._advance(record)
        self._hold()
""",
            """        for record in self.held_component_records():
            self._advance(record)
        self._hold(advance=True)
""",
        ),
        (
            """        for family, record in self.held_records.items():
            self.node_level[family] = record.before
        self._effective.clear()
        for block in self.blocks:
            if block.window is not None:
                self._point_window_inverse(block)
""",
            """        for family, record in self.held_records.items():
            self.node_level[family] = record.before
        self._effective.clear()
        # the interval's dipole writes taken back first (9.91 (3); commit 2): they
        # were the last writes of the forward interval, after the fields' step
        self._unhold_dipoles()
        for block in self.blocks:
            if block.window is not None:
                self._point_window_inverse(block)
""",
        ),
        (
            """        for record in reversed(self.held_component_records()):
            self._advance_inverse(record)
        self._hold()
        self.tick -= 1
""",
            """        for record in reversed(self.held_component_records()):
            self._advance_inverse(record)
        self._hold(inverse=True)
        self.tick -= 1
""",
        ),
        # the leak test per part
        (
            """        found: list[str] = []
        for family, record in self.held_records.items():
            if self._sourced_ever[family]:
                continue
            if record.now.any() or record.before.any() or record.remainder.any():
                found.append(self.families[family].name)
        # every other part of a held family with no source of its own stays
        # exactly zero (9.91 (9) (a): the leak test per part)
        for family, parts in self.held_parts.items():
            for record in parts:
                if record.silent:
                    continue
                if record.now.any() or record.before.any() or record.remainder.any():
                    name = f"{self.families[family].name}[{record.part}]"
                    if name not in found:
                        found.append(name)
""",
            """        found: list[str] = []
        for family, record in self.held_records.items():
            if self._sourced_ever[(family, 0)]:
                continue
            if record.now.any() or record.before.any() or record.remainder.any():
                found.append(self.families[family].name)
        # every other part of a held family with no source of its own stays
        # exactly zero (9.91 (9) (a): the leak test per part)
        for family, parts in self.held_parts.items():
            for record in parts:
                if self._sourced_ever[(family, record.part)]:
                    continue
                if record.now.any() or record.before.any() or record.remainder.any():
                    name = f"{self.families[family].name}[{record.part}]"
                    if name not in found:
                        found.append(name)
""",
        ),
    ],
)

# ---- generators
edit(
    "wt_ec/examples/events/massive_record/make_worlds.py",
    [
        (
            """        entry["pair"] = block["pair"]
        if any(item["name"] == family and item.get("pair") == "body" for item in families):
            entry["kind"] = list(block.get("kind", pair))  # the body's rest pair (9.91 (7))
""",
            """        entry["pair"] = block["pair"]
        if any(item["name"] == family and item.get("pair") == "body" for item in families):
            entry["kind"] = list(block.get("kind", pair))  # the body's rest pair (9.91 (7))
        # the body's numbers the holds read (ALGEBRA.md 9.91 (3), (7); commit 2), no default
        entry["charge"] = block.get("charge", 0)
        entry["spin"] = list(block.get("spin", [0, 0, 0]))
        entry["moment"] = list(block.get("moment", [0, 0, 0]))
""",
        ),
    ],
)
edit(
    "wt_ec/examples/events/detector_law/make_worlds.py",
    [
        (
            """    entry = body(position, "charge")
    entry["extents"] = extents
    entry["pair"] = list(WALL_PAIR)
""",
            """    entry = body(position, "charge")
    entry["extents"] = extents
    entry["pair"] = list(WALL_PAIR)
    # the body's numbers (ALGEBRA.md 9.91 (3), (7); commit 2): a mirror carries none
    entry["charge"] = 0
    entry["spin"] = [0, 0, 0]
    entry["moment"] = [0, 0, 0]
""",
        ),
    ],
)
edit(
    "wt_ec/examples/events/dark_body/make_worlds.py",
    [
        (
            """        "kind": list(MATTER),  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        "amount": amount,
""",
            """        "kind": list(MATTER),  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        "charge": 0,  # the body's numbers (ALGEBRA.md 9.91 (3), (7); commit 2)
        "spin": [0, 0, 0],
        "moment": [0, 0, 0],
        "amount": amount,
""",
        ),
    ],
)
edit(
    "wt_ec/examples/events/point_emitter/make_worlds.py",
    [
        (
            """        "kind": list(KIND),  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        "amount": 1,
""",
            """        "kind": list(KIND),  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        "charge": 0,  # the body's numbers (ALGEBRA.md 9.91 (3), (7); commit 2)
        "spin": [0, 0, 0],
        "moment": [0, 0, 0],
        "amount": 1,
""",
        ),
    ],
)

# ---- the tests' helper and the multi-line block literals
edit(
    "wt_ec/tests/test_massive_record.py",
    [
        (
            """            "momentum": block.get("momentum", [0, 0, 0]),
            "side": block["side"],
            "pair": block["pair"],
        }
        for key in (
            "seed",
""",
            """            "momentum": block.get("momentum", [0, 0, 0]),
            "side": block["side"],
            "pair": block["pair"],
            # the body's numbers (ALGEBRA.md 9.91 (3), (7); commit 2), no loader default
            "charge": block.get("charge", 0),
            "spin": block.get("spin", [0, 0, 0]),
            "moment": block.get("moment", [0, 0, 0]),
        }
        for key in (
            "seed",
""",
        ),
    ],
)
sites = {
    "test_algebra_visualizer.py": [347, 636],
    "test_board_properties.py": [108],
    "test_body_record.py": [316, 354],
    "test_detector_law.py": [89, 697],
    "test_emitter.py": [221],
    "test_extents_and_face_slab.py": [129],
    "test_flux_reading.py": [217],
    "test_hop_taking.py": [55],
    "test_initial_state.py": [106, 217, 275],
    "test_massive_record.py": [713, 852, 921, 1202, 1230, 1503, 1645, 1703, 1750],
    "test_point_emitter.py": [50],
    "test_receiver_by_name.py": [58],
}
for name, lines in sites.items():
    p = Path("wt_ec/tests") / name
    text = p.read_text().split("\n")
    if any('"spin": [0, 0, 0],' in line for line in text):
        continue
    # the helper's own line moved by the edit above: re-find the listed lines by content
    for number in sorted(lines, reverse=True):
        # the listed line numbers predate the helper edit in test_massive_record: locate
        # the nearest line matching the key within 8 lines
        candidates = [
            k
            for k in range(max(0, number - 1 - 8), min(len(text), number + 8))
            if re.match(r'^\s*"(side|extents)": .*,\s*$', text[k])
        ]
        assert candidates, (name, number)
        k = min(candidates, key=lambda k: abs(k - (number - 1)))
        indent = re.match(r"^(\s*)", text[k]).group(1)
        text[k + 1 : k + 1] = [
            f'{indent}"charge": 0,',
            f'{indent}"spin": [0, 0, 0],',
            f'{indent}"moment": [0, 0, 0],',
        ]
    p.write_text("\n".join(text))
print("ok")
