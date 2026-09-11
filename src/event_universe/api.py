"""Public assembly of the engine, current candidate model and optional observations."""

from event_universe.core.contracts import LocalCellRule, Observer
from event_universe.core.engine import Engine
from event_universe.core.linked_engine import LinkedEngine
from event_universe.core.links import LengthRule, LinkConfig
from event_universe.core.state import Config
from event_universe.core.streaming_engine import StreamingEngine
from event_universe.dynamics.movement import MovementRule, advance_balanced_movement
from event_universe.dynamics.transit import transit_ticks
from event_universe.dynamics.turning import FieldTurning
from event_universe.fields.policies import ScalarActivity, sample_changed_or_source
from event_universe.fields.scalar import ScalarFieldRule
from event_universe.models.causal_stream import (
    STREAM_FIELD,
    STREAM_MODEL,
    STREAM_SAMPLES,
    CausalStreamConfig,
)
from event_universe.models.collisions import collide
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel
from event_universe.models.linked_field import LINKED_MODEL, geometry_policy


class ScalarSimulation(Engine):
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
        )


class BalancedSimulation(ScalarSimulation):
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
        self, settings: CausalStreamConfig | None = None, *, observer: Observer | None = None
    ) -> None:
        choices = CausalStreamConfig() if settings is None else settings
        super().__init__(
            choices.engine_config(),
            STREAM_MODEL.update_particle,
            STREAM_FIELD.emit,
            choices.source_per_octant,
            STREAM_SAMPLES,
            observer,
        )
