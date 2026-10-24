"""The click written on the lattice (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision: after a click the paths are cancelled on the lattice, not in the clicks' books, Rule3 kept; the owner's word, the click the meeting of two quanta at one Node, the write their exchange there): the NodeDetectors' acts outside Rule3, taken by the engine's loop at the NodeDetectors' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the click's read of the board, one Link and one number (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24; the owner's words), Rule3's kept remainders at the Node and beyond its six Ports read as the digits of one number (`read_number`, the Node's digit first and the Link digits in the order of their values, `digits.read_of`), and the number divided by the unit once, the remainder the whether placed on the cumulative weights (the first whose cumulative weight exceeds it, the lower index on a tie) and the quotient the number left for the close's later draws (`drawn_from`); no generator and no seed: no number of the run is born outside the world file and Rule3, the same world read twice gives the same click, and the ensemble of worlds is the variety. The hole: the arriving record's levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one. The lay of a record at one Node: the levels of `count` quanta of a pair standing at one Node at the pair's own rotation, the amplitude A from the count's measure, A^2 = count T den^2 div (2 (den^2 - num^2)) so that the share 6 den A^2 sin^2 omega reads the count (the count is the record's share), and for the massless pair the two levels alike, A^2 = count T div 2; a direction taken from the levels of the part the quantum leaves, so the phase passes with the quantum (the mathematician's hand, the arriving quantum's phase 0 on a real line of light); the level before the level now turned by the rest rotation, cos omega = num / den, in the record's own sense; the remainder at the lay's origin, the half wall. The face (the mathematician's hand, the advisor's second, two hands; the owner's word, the node_detector operates Rule3 on the families): the giver's write is no assignment but one value presented at one Port of the Node for two intervals, the least arrival that lifts Rule3's numerator at the Node into the target's window, arr_face = ceiling((w a* - SUM over the other Ports of R_j arr_j - S a_now + w a_before - r) / R_face) with the target a* = 0, so that Rule3 itself writes the level 0 and its own remainder, below one read coefficient; the second interval's face makes the new now 0 and the new before the 0 of the first, the record's lines at (0, 0) from then where every neighbour stands at 0, and the hole spreading by Rule3 alone elsewhere; the same value presented on the way back, Rule3's inverse crosses the click bit for bit, the Node knowing neither (the faces the books' log, `Face`). The undepleted beam (the two hands' line, the owner's word for the simple solution): a record of many quanta per Node is a beam, and the absorption of one of its quanta is read in the books and not written on the board, exact as the count per Node grows, so where the record's booked share at the Node, the share the credit reads there (`share.share`, the conserved form's density at the Node over 2 p_i^2 G^2), is above its own quantum W_rec, no face is booked and no front begins, the record's levels stand, its count in the books goes down by one and the board's share then exceeds the books' count by the quanta taken, the deficit, a tally per family printed in the books' line by name (`Lattice.books`); the hole to 0, both levels to 0, stands where the booked share at the Node is at most W_rec, the record there being local and whole, the front erasing what spread beyond it where the count reaches 0 (`take.faced`); the count goes down by one either way, the front erases only a record at count 0, and the inverse presents the kept value whatever the target."""

from __future__ import annotations

from collections.abc import Sequence

from event_universe.core.rule3 import division_forward, largest_below


def read_number(digits: Sequence[int], bases: Sequence[int]) -> int:
    """The click's read of the board as one integer (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24): the digits `digits`, each a kept remainder of Rule3 read as its index on a lattice, r div F (`digits.read_of`: the Node's own remainder on the Node's own lattice F_i, each neighbour's on the Link's lattice F_ij; per line the Node's digit first and then the Link digits in the order of their values, no Port order), each in [0, w div F), as one number with the first digit the most significant, x = ((d_1 b_2 + d_2) b_3 + d_3) ... in the mixed radix of the bases `bases`, each w div F + 1, one above its digit's count of values so that no total built of the wall's primes divides it (a digit carries log2(w div F) bits: 26.7 at the shipped universes' content 60, 11.9 for the atom [1, 1299], 1.6 for light at the exact vacuum paces), multiply and add in Python's integers, no division and no number of the run born here; the records' remainders are read and never written."""
    found = 0
    for digit, base in zip(digits, bases, strict=True):
        found = found * int(base) + int(digit)
    return found


def drawn_from(number: int, weights: Sequence[int], label: str, read: bool = False) -> tuple[int, int]:
    """One draw from the number the click read (ALGEBRA.md, The click's read of the board, the sentence of 2026-10-24; `read_number`, `digits.read_of`): among the weights (each at or above 0, their total T above 0, refused by name otherwise) one division act of the number by T, the remainder the pick placed on the cumulative weights in their declared order, the first index whose cumulative weight exceeds it (the lower index on a tie, a weight of 0 never drawn), and the quotient the number left for the close's later draws (the pair among the candidates by its residue modulo their count where a selector asks one; main's selector asks none and the quotient stands), returned with the index; the board's own close divides by the unit once, the weights the rest and the unit less it (`meeting_board.closed`); one weight above 0 (one weight, or one beside weights of 0) is a certain draw and consumes nothing, the number returned whole; a number below T is refused by name in two texts (the reader's G2 of 2026-10-20): the number read, the interval's read itself below the total (`read`, the first draw: the board at the Node does not carry the draw), and the number left, spent by the interval's earlier draws (a residue of a number below T is no residue of the whole). Derived: a residue uniform on [0, T) falls in the cell of the index i with probability w_i / T exactly, Born with no 2^-width term. No digit is erased from the residue and no bias bound is booked (2026-10-24): every base is w div F + 1 with F a divisor of w, none 0 modulo den, so no place value is 0 modulo the unit, and the former bound by the read's two moduli (the bases less one and the last base, `bias_bound` to 2026-10-24, the reader's F of 2026-10-20, with its one refusal where their product reached the total) is kept by name; the equidistribution of the digits' combination modulo T is measured on the ensembles and not derived (the law's honest clause)."""
    total = sum(int(weight) for weight in weights)
    if total <= 0:
        raise ValueError("the board draws among weights whose total is above 0")
    live = [index for index, weight in enumerate(weights) if int(weight) > 0]
    if len(live) == 1:
        return live[0], int(number)  # a certain draw: one weight above 0 consumes nothing
    if number < total:
        if read:  # the interval's read itself below the total: the board does not carry the draw
            raise RuntimeError(
                f"the click's read of the board at {label} has the number {number} read, below the draw's total "
                f"{total}: the digits read at this interval do not carry the draw (a residue of a number below the "
                "total is no residue of the whole); the world's declaration answers, the body's record over more "
                "Nodes, a well, a drive with a content, no key on the draw"
            )
        raise RuntimeError(
            f"the click's read of the board at {label} has the number {number} left, below the draw's total "
            f"{total}: the digits read are spent at this interval by its earlier draws (a residue of a number below "
            "the total is no residue of the whole); a shorter window, fewer draws per close or more Nodes read"
        )
    left, residue = division_forward(int(number), total, 0)
    reached = 0
    for index, weight in enumerate(weights):
        reached += int(weight)
        if residue < reached:
            return index, int(left)
    return len(weights) - 1, int(left)


def squared(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """A^2 of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): (the largest x with x^2 <= count^2 T^2 den^2 div (4 laid^2 (den^2 - num^2))), one search on the whole product by the search on the share reading (`rule3.largest_below`), the invariant 2 A^2 sin omega = T per quantum per line (ALGEBRA.md, the absorption's A^2 = (N + 1) T / (2 sin omega_part); the two hands' word on R8, #1793), count T div (2 laid) for the massless pair, the number `amplitude` takes the largest integer whose square is at most it of."""
    num, den = pair
    gap = den * den - num * num
    if gap:
        half = (
            count * action * den
        )  # 2 laid A^2 s = count T den with s^2 = gap: the search on the whole product
        return largest_below(int(division_forward(half * half, 2 * laid * 2 * laid * gap, 0)[0]))
    return int(division_forward(count * action, 2 * laid, 0)[0])


def amplitude(count: int, action: int, pair: tuple[int, int], laid: int = 1) -> int:
    """The amplitude A of `count` quanta standing at one Node on `laid` lines alike (one, the taker's part): A^2 = count T den^2 div (2 laid (den^2 - num^2)), the share 6 den A^2 sin^2 omega per line over W_c = 3 den T the count, by the search on the share reading (`rule3.largest_below`); for the massless pair, whose one-Node record has no rotation, A^2 = count T div (2 laid), the two levels alike (the lay by the count, `emission.laid_by_count`: every laid line of the record alike, the symmetric lay, the mathematician's hand)."""
    return largest_below(squared(count, action, pair, laid))
