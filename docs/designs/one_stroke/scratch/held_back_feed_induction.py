"""HELD BACK (the one stroke, commit 6; BUILD.md section 26 item 65): the feed and the induction of
ALGEBRA.md 9.78 (4), 9.52 (2), (4) as built into `_body_step`, then taken out before the commit: with
them the two tools of every chain world fall together (the chain content field is a tent). This is
the edit script that put them in, kept beside the handoff note for the mathematician's answer; not
run by anything. The feed: n_a += (C_+ - C_-) x W div (2 Gamma D_a F_a); the induction: n_a -=
factor x W x (the change of the read vector component over the body) div (2 Gamma N).
"""

# Commit 6, the engine, as first built: the body's contraction at its Node, the feed, the
# induction, the spin's step (ALGEBRA.md 9.91 (8) (v), 9.78 (4), (5), 9.52 (2), (4)).
from pathlib import Path

ROOT = Path("/home/user/Universe24")
PATH = ROOT / "src/event_universe/events/detector_law.py"
text = PATH.read_text(encoding="utf-8")


def edit(pairs):
    global text
    for old, new in pairs:
        assert text.count(old) == 1, (old[:90], text.count(old))
        text = text.replace(old, new)


edit(
    [
        # Block: the live spin and its leapfrog partner
        (
            "    momentum: list[int]\n"
            "    drive: list[int] = field(default_factory=lambda: [0, 0, 0])\n"
            "    count: int = 0\n",
            "    momentum: list[int]\n"
            "    drive: list[int] = field(default_factory=lambda: [0, 0, 0])\n"
            "    # THE SPIN AS STATE (ALGEBRA.md 9.78 (5), 9.91 (8) (v); commit 6): S now and S one\n"
            "    # interval back, the leapfrog's two integers; the load's write is the body's\n"
            "    # declared `spin` at both\n"
            "    spin: list[int] = field(default_factory=lambda: [0, 0, 0])\n"
            "    spin_before: list[int] = field(default_factory=lambda: [0, 0, 0])\n"
            "    count: int = 0\n",
        ),
        (
            "            )\n"
            "            self._write_pair(block)\n"
            "            if definition.seed > 0 and world.body_record:\n",
            "            )\n"
            "            block.spin = list(definition.spin)\n"
            "            block.spin_before = list(definition.spin)\n"
            "            self._write_pair(block)\n"
            "            if definition.seed > 0 and world.body_record:\n",
        ),
        (
            '        vector = block.definition.spin if definition.held_dipole == "spin" else block.definition.moment\n',
            "        vector = (\n"
            "            (block.spin[0], block.spin[1], block.spin[2])\n"
            '            if definition.held_dipole == "spin"\n'
            "            else block.definition.moment\n"
            "        )\n",
        ),
        # the stock of the given family: the body's own quanta set aside, or its held quanta
        (
            "        # the stock is the given family's content held at the body (ALGEBRA.md\n"
            "        # 9.51 (8); item 47): nothing fires once it is spent\n"
            "        if self.held[block.number][emitter.family] <= 0:\n"
            "            return\n",
            "        # the stock is the given family's content held at the body (ALGEBRA.md\n"
            "        # 9.51 (8); item 47), or the body's own quanta set aside (9.96 (5); commit\n"
            "        # 6): nothing fires once it is spent\n"
            "        if self.stock_of(block) <= 0:\n"
            "            return\n",
        ),
        (
            "        block.emit_now = False\n"
            "        block.wait = 0\n"
            "        own.u, own.wheel = residue, wheel\n"
            "        if self.held[number][family] > 0:\n"
            "            block.excitations += 1\n",
            "        block.emit_now = False\n"
            "        block.wait = 0\n"
            "        own.u, own.wheel = residue, wheel\n"
            "        if self.stock_of(block) > 0:\n"
            "            block.excitations += 1\n",
        ),
        (
            "        live.giving_line = None\n"
            "        block.wait = 0\n"
            "        if self.held[block.number][family] > 0:\n"
            "            block.excitations += 1\n",
            "        live.giving_line = None\n"
            "        block.wait = 0\n"
            "        if self.stock_of(block) > 0:\n"
            "            block.excitations += 1\n",
        ),
        (
            "    def _momentum_now(self, block: Block) -> list[int]:\n",
            "    def stock_of(self, block: Block) -> int:\n"
            '        """THE STOCK of the family a body gives (ALGEBRA.md 9.51 (8), 9.96 (5)): its\n'
            "        held quanta of another family; of its own family, its declared `stock` less\n"
            '        its givings (each giving lowered M by one, the held count of its own)."""\n'
            "        emitter = block.definition.emitter\n"
            "        assert emitter is not None\n"
            "        if emitter.family == block.family:\n"
            "            return block.definition.stock - block.givings\n"
            "        return self.held[block.number][emitter.family]\n"
            "\n"
            "    def _momentum_now(self, block: Block) -> list[int]:\n",
        ),
        # the step: the bodies on one Node after the holds
        (
            "        # the held families step last, after every family read their levels,\n"
            "        # and are held at the bodies' Nodes at the sources the interval's\n"
            "        # clicks and givings left (ALGEBRA.md 9.45 (2); item 51)\n"
            "        self._advance_fields()\n",
            "        # the held families step last, after every family read their levels,\n"
            "        # and are held at the bodies' Nodes at the sources the interval's\n"
            "        # clicks and givings left (ALGEBRA.md 9.45 (2); item 51)\n"
            "        self._advance_fields()\n"
            "        # THE BODIES ON ONE NODE (ALGEBRA.md 9.91 (8) (v); commit 6): the feed, the\n"
            "        # induction and the spin's step from the fields as the interval leaves them\n"
            "        for block in self.blocks:\n"
            "            self._body_step(block, False)\n",
        ),
        # the inverse: the bodies first, hops refused
        (
            "        for block in self.blocks:\n"
            "            if any(int(component) != 0 for component in block.momentum):\n"
            "                raise ValueError(\n"
            '                    f"{BEAM_LAW}: the inverse map is defined at rest (block {block.number} moves)"\n'
            "                )\n"
            "        # the joint inverse (ALGEBRA.md 9.41 (2), 9.45 (2); item 51): every\n",
            "        for block in self.blocks:\n"
            "            if block.stepped > 0 or any(block.hop):\n"
            "                raise ValueError(\n"
            '                    f"{BEAM_LAW}: the inverse map is defined for a body that has not hopped (block "\n'
            '                    f"{block.number} hopped; the hop\'s inverse, the field moved back through the "\n'
            '                    "body, ALGEBRA.md 9.52 (4) (i), is not built)"\n'
            "                )\n"
            "        # the bodies' step back first (9.91 (8) (v); commit 6): the momentum and the\n"
            "        # spin as the interval began, from the fields as it left them\n"
            "        for block in self.blocks:\n"
            "            self._body_step(block, True)\n"
            "        # the joint inverse (ALGEBRA.md 9.41 (2), 9.45 (2); item 51): every\n",
        ),
        (
            "        for record in reversed(self.held_component_records()):\n"
            "            self._advance_inverse(record)\n"
            "        self._hold(inverse=True)\n"
            "        self.tick -= 1\n",
            "        for record in reversed(self.held_component_records()):\n"
            "            self._advance_inverse(record)\n"
            "        self._hold(inverse=True)\n"
            "        # the drive's accumulator back (no hop this interval: drive' = drive + n)\n"
            "        for block in self.blocks:\n"
            "            momentum = self._momentum_now(block)\n"
            "            for axis in range(3):\n"
            "                block.drive[axis] -= momentum[axis]\n"
            "        self.tick -= 1\n",
        ),
        (
            '                        "drive": list(block.drive),\n'
            '                        "momentum": list(block.momentum),\n',
            '                        "drive": list(block.drive),\n'
            '                        "momentum": list(block.momentum),\n'
            '                        "spin": list(block.spin),\n',
        ),
    ]
)

BODY = '''    # THE BODIES ON ONE NODE (ALGEBRA.md 9.91 (8) (v), 9.78 (4), (5), 9.52 (2), (4); the
    # one stroke, commit 6): the contraction, the feed, the induction, the spin's step,
    # written once for any body and any read

    def _read_factor(self, block: Block, weight: int, by: str) -> int:
        """A read's factor on a body (ALGEBRA.md 9.78 (4)): the weight plainly, or minus
        the body's charge Q times the weight for a read by q (the pace's convention,
        `_effective_content`: like signs a hill)."""
        return weight if by == "plain" else -self._body_charge(block.number) * weight

    def _face_layer(self, block: Block, axis: int, sigma: int) -> np.ndarray:
        """The Nodes across the body's Ports toward sigma on the axis (ALGEBRA.md 9.52
        (4) (iii): the seat's neighbour, a block's outside layer), none beyond an open
        face or on a folded axis."""
        if self.shape[axis] == 1:
            return np.zeros(self.shape, dtype=bool)
        wrap = self.kind_wrap[block.family]
        across = self._shift(block.mask, axis, sigma, fill=False, wrap=wrap)
        layer: np.ndarray = across & ~block.mask
        return layer

    def _contraction_sum(
        self, block: Block, mask: np.ndarray, key: tuple[object, ...], advance: bool, inverse: bool
    ) -> int:
        """THE CONTRACTION at the Nodes of `mask`, summed (ALGEBRA.md 9.78 (4), 9.91 (8)
        (v)): SUM over the body's family's reads of the read's factor times [the t level
        - (n_a V_a) div W + (n_a n_b h_ab) div W^2], the body's momentum n on its wall W
        contracted with the read family's vector and tensor parts, one division per
        read and power with the remainder carried on the body under `key`."""
        momentum = self._momentum_now(block)
        wall = self.wall_of(block)
        total = 0
        for position, (other, weight, by, _) in enumerate(self.families[block.family].reads):
            factor = self._read_factor(block, weight, by)
            if factor == 0:
                continue
            level = int(np.sum(self.held_records[other].now[mask]))
            parts = self.families[other].parts
            vector = self.held_parts[other]
            if len(parts) > 1:
                numerator = -sum(
                    momentum[axis] * int(np.sum(vector[axis].now[mask]))
                    for axis in range(3)
                    if not vector[axis].silent
                )
                value, _ = self._carried_division(
                    block, (*key, position, 1), numerator, wall, advance, inverse
                )
                level += value
            if len(parts) > 2:
                numerator = sum(
                    momentum[a] * momentum[b] * int(np.sum(vector[3 + index].now[mask]))
                    for index, (a, b) in enumerate(TENSOR_AXES)
                    if not vector[3 + index].silent
                )
                value, _ = self._carried_division(
                    block, (*key, position, 2), numerator, wall * wall, advance, inverse
                )
                level += value
            total += factor * level
        return total

    def _curl(self, records: list[LiveRecord], centre: tuple[int, int, int], wrap: tuple[bool, bool, bool]) -> list[int]:
        """The curl of a vector part at the centre Node from its six neighbours' levels
        (ALGEBRA.md 9.77 (3), 9.91 (8) (v)): (curl V)_x = V_z(+y) - V_z(-y) - V_y(+z) +
        V_y(-z) and cyclic; a read beyond an open face is 0."""
        def at(component: int, axis: int, sigma: int) -> int:
            if records[component].silent or self.shape[axis] == 1:
                return 0
            node = list(centre)
            node[axis] += sigma
            if wrap[axis]:
                node[axis] %= self.shape[axis]
            elif not 0 <= node[axis] < self.shape[axis]:
                return 0
            return int(records[component].now[node[0], node[1], node[2]])

        return [
            at(z, y, 1) - at(z, y, -1) - at(y, z, 1) + at(y, z, -1)
            for y, z in ((1, 2), (2, 0), (0, 1))
        ]

    def _body_step(self, block: Block, inverse: bool) -> None:
        """THE BODY'S STEP AT (v) (ALGEBRA.md 9.91 (8) (v)), from the fields as the
        interval leaves them (their `now` levels, which the inverse meets first):
        THE FEED per axis, n_a += (C_+ - C_-) x W div (2 Gamma D_a F_a), C_+ and C_- the
        contraction summed over the F_a Nodes across the body's Ports toward +a and -a
        and D_a their distance, the body's extent plus one (9.52 (2): the acceleration
        grad c / (2 Gamma) toward content; (4) (iii), (iv)); THE INDUCTION, n_a -= factor
        x W x (the change over the interval of the read's vector component a summed over
        the body's Nodes) div (2 Gamma N) (9.78 (4): minus the change of the
        contraction's momentum part, Faraday's term and its mass twin); THE SPIN'S STEP,
        S_(t+1) = S_(t-1) + (2 [(Omega x S_t) + mu x B_q] + carry) div (W Gamma), the
        leapfrog of the body's two integers with the doubled term (the Euler line's rate,
        exactly invertible; 9.78 (5) leaves the choice), Omega_i = [factor x (curl V)_i +
        3 ((grad c) x n)_i div W] div 8 from a read whose dipole is the spin, B_q = (curl
        V_q) div 2 from a read whose dipole is the moment, every remainder carried on the
        body. Backward the same terms are recomputed and subtracted, the divisions
        stepped back."""
        definition = self.families[block.family]
        if not definition.reads:
            return
        advance = not inverse
        gamma = self.node_clock
        wall = self.wall_of(block)
        centre = tuple(int(axis[0]) for axis in np.nonzero(self.centre_mask(block)))
        wrap = self.kind_wrap[block.family]
        count = int(np.count_nonzero(block.mask))
        # the spin's term from S_t (the leapfrog's middle), before the momentum moves
        spin_now = (block.spin[0], block.spin[1], block.spin[2]) if advance else (
            block.spin_before[0], block.spin_before[1], block.spin_before[2]
        )
        omega = [0, 0, 0]
        torque = [0, 0, 0]
        momentum = self._momentum_now(block)
        for position, (other, weight, by, _) in enumerate(definition.reads):
            factor = self._read_factor(block, weight, by)
            read = self.families[other]
            if factor == 0 or len(read.parts) < 2 or read.held_dipole is None:
                continue
            curl = self._curl(self.held_parts[other][:3], centre, wrap)
            if read.held_dipole == "spin":
                content = self.held_records[other].now
                gradient = [0, 0, 0]
                for axis in range(3):
                    if self.shape[axis] == 1:
                        continue
                    plus, minus = list(centre), list(centre)
                    plus[axis] += 1
                    minus[axis] -= 1
                    for node in (plus, minus):
                        if wrap[axis]:
                            node[axis] %= self.shape[axis]
                    inside = all(0 <= node[axis] < self.shape[axis] for node in (plus, minus))
                    if inside or wrap[axis]:
                        gradient[axis] = int(content[plus[0], plus[1], plus[2]]) - int(
                            content[minus[0], minus[1], minus[2]]
                        )
                cross = (
                    gradient[1] * momentum[2] - gradient[2] * momentum[1],
                    gradient[2] * momentum[0] - gradient[0] * momentum[2],
                    gradient[0] * momentum[1] - gradient[1] * momentum[0],
                )
                for i in range(3):
                    tidal, _ = self._carried_division(
                        block, ("gradc", position, i), 3 * cross[i], wall, advance, inverse
                    )
                    value, _ = self._carried_division(
                        block, ("omega", position, i), factor * curl[i] + tidal, 8, advance, inverse
                    )
                    omega[i] += value
            else:
                for i in range(3):
                    value, _ = self._carried_division(
                        block, ("bq", position, i), factor * curl[i], 2, advance, inverse
                    )
                    torque[i] += value
        mu = block.definition.moment
        turn = [
            omega[1] * spin_now[2] - omega[2] * spin_now[1] + mu[1] * torque[2] - mu[2] * torque[1],
            omega[2] * spin_now[0] - omega[0] * spin_now[2] + mu[2] * torque[0] - mu[0] * torque[2],
            omega[0] * spin_now[1] - omega[1] * spin_now[0] + mu[0] * torque[1] - mu[1] * torque[0],
        ]
        for i in range(3):
            step, _ = self._carried_division(block, ("spin", i), 2 * turn[i], wall * gamma, advance, inverse)
            if advance:
                block.spin[i], block.spin_before[i] = block.spin_before[i] + step, block.spin[i]
            else:
                block.spin[i], block.spin_before[i] = block.spin_before[i], block.spin[i] - step
        # the feed and the induction per axis
        for axis in range(3):
            plus = self._face_layer(block, axis, 1)
            minus = self._face_layer(block, axis, -1)
            faces = int(np.count_nonzero(plus))
            feed = 0
            if faces and faces == int(np.count_nonzero(minus)):
                distance = block.definition.extents[axis] + 1
                difference = self._contraction_sum(
                    block, plus, ("face", axis, 1), advance, inverse
                ) - self._contraction_sum(block, minus, ("face", axis, -1), advance, inverse)
                feed, _ = self._carried_division(
                    block, ("feed", axis), difference * wall, 2 * gamma * distance * faces, advance, inverse
                )
            induction = 0
            for position, (other, weight, by, _) in enumerate(definition.reads):
                factor = self._read_factor(block, weight, by)
                if factor == 0 or len(self.families[other].parts) < 2:
                    continue
                record = self.held_parts[other][axis]
                if record.silent:
                    continue
                change = int(np.sum(record.now[block.mask])) - int(np.sum(record.before[block.mask]))
                value, _ = self._carried_division(
                    block, ("induction", position, axis), -factor * change * wall, 2 * gamma * count, advance, inverse
                )
                induction += value
            if advance:
                block.momentum[axis] += feed + induction
            else:
                block.momentum[axis] -= feed + induction

'''
anchor = "    def shell_mask(self, block: Block) -> np.ndarray:\n"
assert text.count(anchor) == 1
text = text.replace(anchor, BODY + anchor)
PATH.write_text(text, encoding="utf-8")
print("ok")
