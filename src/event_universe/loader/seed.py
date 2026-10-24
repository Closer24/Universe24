"""The uniform seed of a world that declares nothing (ALGEBRA.md, The uniform seed is a lay, the owner's word of 2026-10-24): the loader's derivation of the seed family, read by the lattice before the start (`seed.uniform_seed`) and by the board's own reader (`meeting_board`)."""

from __future__ import annotations

from event_universe.loader.derived import FamilyRule


def seed_of(families: tuple[FamilyRule, ...]) -> int:
    """The uniform seed of a world that declares nothing (ALGEBRA.md, The uniform seed is a lay, the owner's word of 2026-10-24): where the world file names none of `bodies`, `packets` and `node_detectors` (`declared` False; a file naming them empty declares an empty board, the former path), the seed is the universe's one massless family of quanta, laid by the engine at one quantum on every Node of the torus (`seed.uniform_seed`) and read by the board itself (`meeting_board`); None where the world declares content, the former start from the laid records (kept by name); a bare world whose universe holds no massless family of quanta, or more than one, is refused by name (nothing to seed, or no one light)."""
    found = [
        index
        for index, family in enumerate(families)
        if family.quanta and not family.held and family.pair[0] == family.pair[1]
    ]
    if len(found) != 1:
        names = [families[index].name for index in found]
        raise ValueError(
            f"the world declares nothing, and its seed is the universe's one massless family of quanta, laid "
            f"at one quantum on every Node (ALGEBRA.md, The uniform seed is a lay): the universe holds {names}"
            + (", none to seed" if not found else ", and the seed is one family")
        )
    return found[0]
