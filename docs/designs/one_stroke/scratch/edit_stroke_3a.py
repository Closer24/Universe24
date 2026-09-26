"""Commit 3 of the one stroke (ALGEBRA.md 9.91 (10) 3; 9.91 (2)): the four paces."""

from pathlib import Path


def edit(path, pairs):
    p = Path(path)
    s = p.read_text()
    for old, new in pairs:
        assert s.count(old) == 1, (path, s.count(old), old[:90])
        s = s.replace(old, new)
    p.write_text(s)


edit(
    "wt_ec/src/event_universe/events/rule.py",
    [
        (
            """def rule_total_bound(
""",
            """def axis_rule_coefficients(  # type: ignore[no-untyped-def]
    num, den, gamma, content, axis_contents
):
    \"\"\"THE FOUR PACES (ALGEBRA.md 9.91 (2); the one stroke, commit 3): p_0 = Gamma -
    c (c the reads' time components) and p_a = p_0 - t_a (t_a the reads' aa
    components halved, `axis_contents`), and the rule's integers with them:
    R_a = 2 p_a^2 num on the two reads along the axis a, S = 12 den Gamma^2 - 6
    (p_0^2 + Gamma^2)(den - num) - 4 num (p_x^2 + p_y^2 + p_z^2), w = 6 den
    Gamma^2. At p_a = p_0 the isotropic rule term for term (`rule_coefficients`
    with the weak field). Returns ((R_x, R_y, R_z), S, w); integers or integer
    arrays alike.\"\"\"
    pace = gamma - content
    paces = [pace - axis_contents[axis] for axis in range(3)]
    gamma_squared = gamma * gamma
    reads = tuple(2 * p * p * num for p in paces)
    squares = paces[0] * paces[0] + paces[1] * paces[1] + paces[2] * paces[2]
    self_coefficient = (
        12 * den * gamma_squared - 6 * (pace * pace + gamma_squared) * (den - num) - 4 * num * squares
    )
    return reads, self_coefficient, 6 * den * gamma_squared


def rule_total_bound(
""",
        ),
    ],
)

E = "wt_ec/src/event_universe/events/detector_law.py"
edit(
    E,
    [
        (
            """from event_universe.events.rule import rule_coefficients
""",
            """from event_universe.events.rule import axis_rule_coefficients, rule_coefficients
""",
        ),
        # the caches
        (
            """        self._effective: dict[int, np.ndarray] = {}  # HOST: per interval, cleared by the hold
""",
            """        self._effective: dict[int, np.ndarray] = {}  # HOST: per interval, cleared by the hold
        # THE FOUR PACES (ALGEBRA.md 9.91 (2); commit 3): per reading family the
        # three axis contents t_a (the reads' aa components halved, the division's
        # remainder carried per Node, `_pace_carry` keyed (family, read, axis)),
        # computed once per interval (HOST cache by tick); None where every read's
        # tensor part is silent (the isotropic rule, bit for bit)
        self._pace_carry: dict[tuple[int, int, int], np.ndarray] = {}
        self._axis_effective: dict[int, tuple[int, bool, tuple[np.ndarray, ...] | None]] = {}
""",
        ),
        # the neighbours per axis and the axis contents, after _neighbours
        (
            """    # The flux reading (ALGEBRA.md 9.19 (3), the mathematician's derivation
    # of 2026-09-24 from 8.2; BUILD.md section 26 item 13): the flux into a
""",
            """    def _axis_neighbours(
        self, a: np.ndarray, wrap: tuple[bool, bool, bool] | None = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        \"\"\"The two reads along each axis summed, (a_(+x) + a_(-x), ...), as
        `_neighbours` reads them (ALGEBRA.md 9.91 (2): the rule's R_a on the
        axis a's two reads).\"\"\"
        sums: list[np.ndarray] = []
        for axis in range(3):
            if self.shape[axis] == 1:
                sums.append(2 * a)
                continue
            sums.append(self._shift(a, axis, 1, wrap=wrap) + self._shift(a, axis, -1, wrap=wrap))
        return sums[0], sums[1], sums[2]

    def _axis_contents(self, family: int, inverse: bool = False) -> tuple[np.ndarray, ...] | None:
        \"\"\"THE AXIS CONTENTS t_a of a reading family (ALGEBRA.md 9.91 (2); commit
        3): SUM over its reads of weight x by x (the read family's aa component
        div 2), one division per read per axis with the remainder kept at the
        Node (`_pace_carry`), advanced once per interval; backward the same
        values with the remainder stepped back (r_(t-1) = (r_t - S) mod 2, the
        value (S + r_(t-1)) div 2), so the inverse reads the paces the step
        read. None where no read's tensor part was ever sourced: the rule is
        then isotropic, p_a = p_0, bit for bit.\"\"\"
        cached = self._axis_effective.get(family)
        if cached is not None and cached[0] == self.tick and cached[1] == inverse:
            return cached[2]
        sign = self.family_charge[family]
        found: list[np.ndarray] | None = None
        for other, weight, by, _ in self.families[family].reads:
            parts = self.families[other].parts
            if len(parts) < 3:
                continue
            diagonal = self.held_parts[other][parts[1] : parts[1] + 3]  # xx, yy, zz
            if all(record.silent for record in diagonal):
                continue
            factor = weight if by == "plain" else -sign * weight
            if factor == 0:
                continue
            if found is None:
                found = [np.zeros(self.shape, dtype=np.int64) for _ in range(3)]
            for axis, record in enumerate(diagonal):
                key = (family, other, axis)
                carry = self._pace_carry.get(key)
                if carry is None:
                    carry = np.zeros(self.shape, dtype=np.int64)
                level = record.before if inverse else record.now
                numerator = factor * level
                if inverse:
                    carry = np.mod(carry - numerator, 2)
                    value = np.floor_divide(numerator + carry, 2)
                else:
                    total = numerator + carry
                    value = np.floor_divide(total, 2)
                    carry = total - 2 * value
                self._pace_carry[key] = carry
                found[axis] += value
        result = None if found is None else (found[0], found[1], found[2])
        self._axis_effective[family] = (self.tick, inverse, result)
        return result

    # The flux reading (ALGEBRA.md 9.19 (3), the mathematician's derivation
    # of 2026-09-24 from 8.2; BUILD.md section 26 item 13): the flux into a
""",
        ),
        # the guard on the paces
        (
            """            most = int(np.max(np.abs(self._effective_content(family))))
            if most >= self.node_clock:
""",
            """            most = int(np.max(np.abs(self._effective_content(family))))
            axis_contents = self._axis_contents(family)
            if axis_contents is not None:
                # every axis pace p_a = Gamma - c - t_a stays positive too (9.91 (2))
                content = self._effective_content(family)
                most = max(most, *(int(np.max(np.abs(content + t))) for t in axis_contents))
            if most >= self.node_clock:
""",
        ),
        # the wheel with the axis paces
        (
            """        read, self_coefficient, wall = rule_coefficients(num, den, gamma, content, True)
        step = gcd(wall, self_coefficient, read)
        return step, wall // step
""",
            """        axis_contents = self._axis_contents(family)
        if axis_contents is None:
            read, self_coefficient, wall = rule_coefficients(num, den, gamma, content, True)
            step = gcd(wall, self_coefficient, read)
        else:
            reads, self_coefficient, wall = axis_rule_coefficients(
                num, den, gamma, content, tuple(int(t[node]) for t in axis_contents)
            )
            step = gcd(wall, self_coefficient, *reads)
        return step, wall // step
""",
        ),
        # the forward step
        (
            """        window = self._window(live.box, self.kind_wrap[live.family])
        if window is None:
            neighbours = self._neighbours(live.now, self.kind_wrap[live.family])
            nxt, live.remainder = self.one_rule(
                num, den, gamma, content, neighbours, live.now, live.before, live.remainder, not field
            )
            live.box = None
        else:
""",
            """        axis_contents = None if field else self._axis_contents(live.family)
        window = self._window(live.box, self.kind_wrap[live.family])
        if axis_contents is not None:
            # THE FOUR PACES (ALGEBRA.md 9.91 (2); commit 3): the rule per axis on the
            # whole board (the tensor's diagonal read; HOST: no window shortcut here)
            nxt, live.remainder = self.one_rule_axes(
                num,
                den,
                gamma,
                content,
                axis_contents,
                self._axis_neighbours(live.now, self.kind_wrap[live.family]),
                live.now,
                live.before,
                live.remainder,
            )
            live.box = None
        elif window is None:
            neighbours = self._neighbours(live.now, self.kind_wrap[live.family])
            nxt, live.remainder = self.one_rule(
                num, den, gamma, content, neighbours, live.now, live.before, live.remainder, not field
            )
            live.box = None
        else:
""",
        ),
        # the inverse step
        (
            """        if live.box is None or self._window(live.box, self.kind_wrap[live.family]) is None:
            neighbours = self._neighbours(live.before, self.kind_wrap[live.family])
            a_before, live.remainder = self.one_rule_inverse(
                num, den, gamma, content, neighbours, live.now, live.before, live.remainder, not field
            )
        else:
""",
            """        axis_contents = None if field else self._axis_contents(live.family, inverse=True)
        if axis_contents is not None:
            a_before, live.remainder = self.one_rule_axes_inverse(
                num,
                den,
                gamma,
                content,
                axis_contents,
                self._axis_neighbours(live.before, self.kind_wrap[live.family]),
                live.now,
                live.before,
                live.remainder,
            )
        elif live.box is None or self._window(live.box, self.kind_wrap[live.family]) is None:
            neighbours = self._neighbours(live.before, self.kind_wrap[live.family])
            a_before, live.remainder = self.one_rule_inverse(
                num, den, gamma, content, neighbours, live.now, live.before, live.remainder, not field
            )
        else:
""",
        ),
        # the rule per axis beside the one rule
        (
            """    def _advance(self, live: LiveRecord) -> None:
        # THE EMITTER'S NODES ARE NODES LIKE EVERY OTHER""",
            """    @staticmethod
    def one_rule_axes(  # type: ignore[no-untyped-def]
        num, den, gamma, content, axis_contents, axis_neighbours, now, before, remainder
    ):
        \"\"\"THE ONE RULE WITH THE FOUR PACES (ALGEBRA.md 9.91 (2); commit 3): w a_next
        + r' = SUM_a R_a (a_(+a) + a_(-a)) + S a_now - w a_before + r with (R_a, S,
        w) of `axis_rule_coefficients`; at t_a = 0 the one rule bit for bit.\"\"\"
        reads, self_coefficient, wall = axis_rule_coefficients(num, den, gamma, content, axis_contents)
        total = reads[0] * axis_neighbours[0]
        total += reads[1] * axis_neighbours[1]
        total += reads[2] * axis_neighbours[2]
        total += self_coefficient * now
        total -= wall * before
        total += remainder
        nxt = np.floor_divide(total, wall) if isinstance(total, np.ndarray) else total // wall
        return nxt, total - wall * nxt

    @staticmethod
    def one_rule_axes_inverse(  # type: ignore[no-untyped-def]
        num, den, gamma, content, axis_contents, axis_neighbours_of_before, now, before, remainder
    ):
        \"\"\"The rule with the four paces one interval back, the same integers
        (ALGEBRA.md 9.50 (8); 9.91 (2)).\"\"\"
        reads, self_coefficient, wall = axis_rule_coefficients(num, den, gamma, content, axis_contents)
        total = reads[0] * axis_neighbours_of_before[0]
        total += reads[1] * axis_neighbours_of_before[1]
        total += reads[2] * axis_neighbours_of_before[2]
        total += self_coefficient * before
        total -= wall * now + remainder
        a_before = (
            -np.floor_divide(-total, wall) if isinstance(total, np.ndarray) else -((-total) // wall)
        )
        return a_before, wall * a_before - total

    def _advance(self, live: LiveRecord) -> None:
        # THE EMITTER'S NODES ARE NODES LIKE EVERY OTHER""",
        ),
    ],
)
print("ok")
