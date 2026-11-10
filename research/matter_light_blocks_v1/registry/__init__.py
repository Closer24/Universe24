"""Registered parametric blocks and their composer (data generators only).

    from research.matter_light_blocks_v1.registry import compose, d1_main_spec, init_data
    prepared, assertions = compose(d1_main_spec(100))
    data = init_data(prepared, steps=140)       # official init format

Imports only ``universe24``, ``research.components`` and the standard library; it never
needs the program's working folder. See README.md.
"""
from .compose import FORMAT, apply_control, check_assertions, compose, expand, init_data, junctions, state_digest
from .compositions import d1_main_spec, d1_skeleton_spec
from . import compositions, symmetry
from .generators import BLOCKS, GLIDERS, LINEAGE, SILENT, glider_cells

__all__ = ["BLOCKS", "FORMAT", "GLIDERS", "LINEAGE", "SILENT", "apply_control", "check_assertions", "compose",
           "compositions", "d1_main_spec", "d1_skeleton_spec", "expand", "glider_cells", "init_data", "junctions",
           "state_digest", "symmetry"]
