"""Core of Universe24: geometry, the fixed tensor and generic Rule3 gear engine."""
from .lattice import DIRECTIONS, OFFSETS, Lattice, lattice
from .tensor import (AcyclicityError, Block, Factor, GearType, LocalityError, Monomial, Tensor, TensorBuilder, build,
                     check_locality, compose, inverse_stages, reference_block, reference_names, vacuum_map)
from .engine import ClickLog, Engine, State, extract_clicks, handedness_kind
from .reciprocity import ReciprocityReport, check_reciprocity
from .reversors import (GEAR_MAPS, Composite, FunctionMap, GearwiseMap, GroupLinearMap, SpatialMap, StateMap,
                        identity_map, inversion_about_box_centre, inversion_about_cube_centre, inversion_about_node,
                        is_fixed, remainder_map, reversor_check, uniform)

__all__ = ["DIRECTIONS", "OFFSETS", "Lattice", "lattice", "AcyclicityError", "Block", "Factor", "GearType",
           "LocalityError", "Monomial", "Tensor", "TensorBuilder", "build", "check_locality", "compose",
           "inverse_stages", "reference_block", "reference_names", "vacuum_map", "ClickLog", "Engine", "State",
           "extract_clicks", "handedness_kind", "ReciprocityReport", "check_reciprocity", "GEAR_MAPS", "Composite",
           "FunctionMap", "GearwiseMap", "GroupLinearMap", "SpatialMap", "StateMap", "identity_map",
           "inversion_about_box_centre", "inversion_about_cube_centre", "inversion_about_node", "is_fixed",
           "remainder_map", "reversor_check", "uniform"]
