"""Public assembly of the engine, current candidate model and optional observations."""

from event_universe.core.contracts import Observer
from event_universe.core.engine import Engine
from event_universe.core.linked_engine import LinkedEngine
from event_universe.core.links import LengthRule, LinkConfig
from event_universe.core.state import Config
from event_universe.dynamics.transit import transit_ticks
from event_universe.dynamics.turning import FieldTurning
from event_universe.fields.policies import ScalarActivity, sample_changed_or_source
from event_universe.fields.scalar import ScalarFieldRule
from event_universe.models.current_field import CURRENT_MODEL, CurrentFieldModel
from event_universe.models.linked_field import LINKED_MODEL, geometry_policy


class Simulation(Engine):
    """Default model with no retained history. Use the CLI runner for saved experiments."""

    def __init__(
        self,
        config: Config | None = None,
        *,
        observer: Observer | None = None,
        field: ScalarFieldRule | None = None,
        turning: FieldTurning | None = None,
        field_activity: ScalarActivity | None = None,
    ) -> None:
        # Preserve the current scheduler; a supplied field tracks its full scalar sample.
        activity = CURRENT_MODEL.activity if field is None else sample_changed_or_source
        model = CurrentFieldModel(
            field=CURRENT_MODEL.field if field is None else field,
            turning=CURRENT_MODEL.turning if turning is None else turning,
            activity=activity if field_activity is None else field_activity,
        )
        super().__init__(
            config if config is not None else Config(),
            model.update_field,
            model.update_particle,
            observer,
            field_activity=model.field_is_active,
        )


class LinkedSimulation(LinkedEngine):
    """Opt-in candidate: integer stretched links, causal mailboxes and frozen transits."""

    def __init__(
        self,
        config: Config | None = None,
        *,
        links: LinkConfig | None = None,
        observer: Observer | None = None,
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
        )
