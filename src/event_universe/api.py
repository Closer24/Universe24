"""Public assembly of the engine, current candidate model and optional observations."""

from event_universe.core.contracts import LocalCellRule, Observer
from event_universe.core.engine import Engine
from event_universe.core.faces import FacePublisher
from event_universe.core.generic_engine import GenericEngine
from event_universe.core.linked_engine import LinkedEngine
from event_universe.core.links import LengthRule, LinkConfig
from event_universe.core.state import Config
from event_universe.core.streaming_engine import StreamingEngine
from event_universe.dynamics.movement import MovementRule, advance_balanced_movement
from event_universe.dynamics.transit import transit_ticks
from event_universe.dynamics.turning import FieldTurning, full_response
from event_universe.fields.definition import FieldDefinition
from event_universe.fields.definitions import decode_response_faces
from event_universe.fields.faces import scalar_broadcast
from event_universe.fields.policies import ScalarActivity, sample_changed_or_source
from event_universe.fields.scalar import ScalarFieldRule
from event_universe.fields.streaming import OctantFieldRule
from event_universe.models.causal_stream import (
    STREAM_FIELD,
    STREAM_MODEL,
    STREAM_SAMPLES,
    CausalStreamConfig,
)
from event_universe.models.collisions import collide
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel
from event_universe.models.linked_field import LINKED_MODEL, geometry_policy


class Simulation(Engine):
    """Default model with no retained history. Use the CLI runner for saved experiments."""

    def __init__(
        self,
        config: Config | None = None,
        *,
        observer: Observer | None = None,
        collisions: bool = False,
        field: ScalarFieldRule | None = None,
        turning: FieldTurning | None = None,
        field_activity: ScalarActivity | None = None,
        movement: MovementRule | None = None,
        post_motion_halo: LocalCellRule | None = None,
        face_publisher: FacePublisher = scalar_broadcast,
        historical_response_staging: bool = True,
        old_face_response: bool = False,
    ) -> None:
        # Preserve the current scheduler; a supplied field tracks its full scalar sample.
        activity = CURRENT_MODEL.activity if field is None else sample_changed_or_source
        model = CurrentFieldModel(
            field=CURRENT_MODEL.field if field is None else field,
            turning=CURRENT_MODEL.turning if turning is None else turning,
            activity=activity if field_activity is None else field_activity,
            movement=CURRENT_MODEL.movement if movement is None else movement,
        )
        super().__init__(
            config if config is not None else Config(),
            model.update_field,
            model.update_particle,
            observer,
            field_activity=model.field_is_active,
            collision_rule=collide if collisions else None,
            post_motion_halo=post_motion_halo,
            face_publisher=face_publisher,
            historical_response_staging=historical_response_staging,
            old_face_response=old_face_response,
        )


class LinkedSimulation(LinkedEngine):
    """Opt-in candidate: integer stretched links, causal mailboxes and frozen transits."""

    def __init__(
        self,
        config: Config | None = None,
        *,
        links: LinkConfig | None = None,
        observer: Observer | None = None,
        collisions: bool = False,
        field: ScalarFieldRule | None = None,
        turning: FieldTurning | None = None,
        length_rule: LengthRule | None = None,
        old_face_response: bool = False,
    ) -> None:
        link_config = LinkConfig() if links is None else links
        model = CurrentFieldModel(
            field=LINKED_MODEL.field if field is None else field,
            turning=LINKED_MODEL.turning if turning is None else turning,
            activity=sample_changed_or_source,
            movement=LINKED_MODEL.movement,
        )
        super().__init__(
            Config() if config is None else config,
            model.update_field,
            model.update_particle,
            observer,
            link_config=link_config,
            length_rule=geometry_policy(link_config) if length_rule is None else length_rule,
            transit_rule=transit_ticks,
            merge_rule=max,
            field_activity=model.field_is_active,
            collision_rule=collide if collisions else None,
            old_face_response=old_face_response,
        )


class BalancedSimulation(Simulation):
    """Opt-in balanced motion with a synchronous old/new six-neighbor halo."""

    def __init__(
        self, config: Config | None = None, *, observer: Observer | None = None, collisions: bool = False
    ) -> None:
        super().__init__(
            config,
            observer=observer,
            movement=advance_balanced_movement,
            collisions=collisions,
            post_motion_halo=CURRENT_MODEL.cancel_scalar_halo,
        )


class CausalStreamSimulation(StreamingEngine):
    """Opt-in outward stream transport with locally delivered full-vector response."""

    def __init__(
        self,
        settings: CausalStreamConfig | None = None,
        *,
        observer: Observer | None = None,
        field: OctantFieldRule | None = None,
        old_face_response: bool = False,
    ) -> None:
        choices = CausalStreamConfig() if settings is None else settings
        super().__init__(
            choices.engine_config(),
            STREAM_MODEL.update_particle,
            (STREAM_FIELD if field is None else field).emit,
            choices.source_per_octant,
            STREAM_SAMPLES,
            observer,
            old_face_response=old_face_response,
        )


class FaceScalarSimulation(Simulation):
    """Experimental full response to old delivered scalar faces; not self-force accepted."""

    model_id = "scalar-buffered-matter-v2-experimental"

    def __init__(
        self,
        config: Config | None = None,
        *,
        observer: Observer | None = None,
        collisions: bool = False,
        field: ScalarFieldRule | None = None,
        face_publisher: FacePublisher = scalar_broadcast,
    ) -> None:
        super().__init__(
            config,
            observer=observer,
            collisions=collisions,
            field=field,
            turning=FieldTurning(select_direction=full_response),
            face_publisher=face_publisher,
            historical_response_staging=False,
            old_face_response=True,
        )


class FaceLinkedSimulation(LinkedSimulation):
    """Experimental full response to the previous local delivered link inbox."""

    model_id = "linked-delivered-faces-v1-experimental"

    def __init__(
        self,
        config: Config | None = None,
        *,
        links: LinkConfig | None = None,
        observer: Observer | None = None,
        collisions: bool = False,
        field: ScalarFieldRule | None = None,
        length_rule: LengthRule | None = None,
    ) -> None:
        super().__init__(
            config,
            links=links,
            observer=observer,
            collisions=collisions,
            field=field,
            length_rule=length_rule,
            turning=FieldTurning(select_direction=full_response),
            old_face_response=True,
        )


class FaceStreamSimulation(CausalStreamSimulation):
    """Experimental old-face response; its isolated co-arrival gate remains mandatory."""

    model_id = "octant-buffered-matter-v2-experimental"

    def __init__(
        self,
        settings: CausalStreamConfig | None = None,
        *,
        observer: Observer | None = None,
        field: OctantFieldRule | None = None,
    ) -> None:
        super().__init__(settings, observer=observer, field=field, old_face_response=True)


class GenericFaceSimulation(GenericEngine):
    """Experimental simultaneous definitions; unit links, unresolved self-force gates."""

    model_id = "generic-buffered-matter-v3-experimental"

    def __init__(
        self,
        config: Config | None = None,
        *,
        definitions: tuple[FieldDefinition, ...],
        link_length: int = 1,
        observer: Observer | None = None,
        collisions: bool = False,
    ) -> None:
        model = CurrentFieldModel(
            field=CURRENT_MODEL.field,
            turning=FieldTurning(select_direction=full_response),
            activity=CURRENT_MODEL.activity,
            movement=CURRENT_MODEL.movement,
        )
        super().__init__(
            Config() if config is None else config,
            definitions,
            model.update_field,
            model.update_particle,
            model.update_particle_from_vector,
            decode_response_faces,
            observer,
            link_length=link_length,
            collision_rule=collide if collisions else None,
        )
