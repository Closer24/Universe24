"""Experimental shared field-bank assembly with old local response snapshots."""

from collections.abc import Callable, Mapping
from types import MappingProxyType

from .contracts import CollisionRule, FieldRule, Observer, ParticleRule, ParticleUpdate
from .engine import Engine
from .field_bank import Definition, Faces, FieldBank
from .state import Address, CellState, Config, Neighbors, ParticleState, Vector

VectorRule = Callable[[ParticleState, CellState, Vector, Config, int], ParticleUpdate]
FaceDecoder = Callable[[Faces], Neighbors]


class GenericEngine(Engine):
    """One bank for every field type; no field-name or concrete-type dispatch."""

    def __init__(
        self,
        config: Config,
        definitions: tuple[Definition, ...],
        field_rule: FieldRule,
        particle_rule: ParticleRule,
        vector_rule: VectorRule,
        decode_faces: FaceDecoder,
        observer: Observer | None = None,
        *,
        link_length: int = 1,
        collision_rule: CollisionRule | None = None,
    ) -> None:
        super().__init__(
            config,
            field_rule,
            particle_rule,
            observer,
            old_face_response=True,
            collision_rule=collision_rule,
        )
        self.bank = FieldBank(self._lattice, definitions, link_length=link_length)
        self._vector_rule = vector_rule
        self._decode_faces = decode_faces
        self._old_vectors: Mapping[Address, Vector] = {}
        self.display_field_name = definitions[0].name

    @property
    def field_faces(self) -> Mapping[Address, Neighbors]:
        """Diagnostic primary-field projection only; physical response uses all fields."""
        return MappingProxyType({p: self.face_at(p) for p in self.bank.cells})

    @property
    def field_faces_by_name(self) -> Mapping[str, Mapping[Address, Neighbors]]:
        return MappingProxyType(
            {
                definition.name: MappingProxyType(
                    {
                        p: self._decode_faces(self.bank.at(p, index).response_faces)
                        for p in self.bank.cells
                    }
                )
                for index, definition in enumerate(self.bank.definitions)
            }
        )

    @property
    def field_inventory_by_name(self) -> Mapping[str, Mapping[Address, tuple[int, ...]]]:
        """Diagnostic inventory, including remainders; separate from face arrivals."""
        return MappingProxyType(
            {
                definition.name: MappingProxyType(
                    {p: self.bank.inventory_at(p, index) for p in self.bank.cells}
                )
                for index, definition in enumerate(self.bank.definitions)
            }
        )

    def face_at(self, position: Address) -> Neighbors:
        return self._decode_faces(self.bank.at(position).response_faces)

    def seed_field(self, position: Address, phi: int) -> None:
        raise NotImplementedError(
            "generic fields require definition-owned initialization; scalar seeding is unsupported"
        )

    def _begin_tick(self) -> None:
        self._old_vectors = {p: self.bank.response_at(p) for p in self.bank.cells}

    def _field_step(self) -> None:
        sources = {p: sum(pid >= 0 for pid in slots) for p, slots in self._occupancy.items()}
        self.bank.advance(sources, self.tick)

    def _propose_particle(self, particle: ParticleState, position: Address) -> ParticleUpdate:
        return self._vector_rule(
            particle,
            self.cell_at(position),
            self._old_vectors.get(position, (0, 0, 0)),
            self.config,
            self.tick,
        )

    def step(self) -> "GenericEngine":
        try:
            super().step()
        finally:
            self._old_vectors = {}
        return self
