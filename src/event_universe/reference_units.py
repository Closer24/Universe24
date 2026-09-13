"""Host-only unit authoring: external references to bounded integer components.

This module never participates in physical stepping or infers a particle law.
Rational SI scales remain authoring metadata; only checked integers enter state.
"""

import argparse
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from event_universe.core.disturbance_state import MAX_VALUE
from event_universe.entity_catalog import resolve_property
from event_universe.initialization import parse_json_document

DIMENSION_ORDER = ("length", "mass", "time", "current", "temperature", "amount", "luminous_intensity")
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]{1,3})?\Z")


@dataclass(frozen=True)
class ReferenceUnit:
    """One positive SI scale and its seven dimension exponents."""

    dimensions: tuple[int, ...]
    si_scale: Fraction
    measured_dependencies: tuple[str, ...] = ()


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object")
    return value


def _bounded(value: Fraction) -> Fraction:
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > 2048:
        raise ValueError("authoring ratio exceeds 2048 bits")
    return value


def _number(value: object) -> Fraction:
    if not isinstance(value, str) or len(value) > 128 or not NUMBER.fullmatch(value):
        raise ValueError("reference values require finite decimal strings")
    return _bounded(Fraction(value))


def _ratio(value: object) -> Fraction:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(type(v) is not int or v <= 0 or v.bit_length() > 512 for v in value)
    ):
        raise ValueError("unit ratio requires two positive bounded integers")
    return Fraction(*value)


def parse_reference_units(raw: object) -> dict[str, ReferenceUnit]:
    """Validate the complete explicit registry, including unused definitions."""
    data = _object(raw, "reference units")
    if (
        set(data) != {"version", "purpose", "dimension_order", "sources", "definitions", "notes"}
        or type(data["version"]) is not int
        or data["version"] != 1
        or data["purpose"] != "physical_reference_units"
        or data["dimension_order"] != list(DIMENSION_ORDER)
    ):
        raise ValueError("expected physical_reference_units version 1 with SI dimensions")
    sources = _object(data["sources"], "sources")
    for source in sources.values():
        if (
            not isinstance(source, str)
            or urlsplit(source).scheme != "https"
            or not urlsplit(source).netloc
        ):
            raise ValueError("unit sources require absolute HTTPS URLs")
    if (
        not isinstance(data["notes"], list)
        or not data["notes"]
        or any(not isinstance(note, str) or not note.strip() for note in data["notes"])
    ):
        raise ValueError("reference units require nonempty notes")
    definitions = _object(data["definitions"], "definitions")
    if not 1 <= len(definitions) <= 128:
        raise ValueError("reference registry requires 1 through 128 definitions")
    result: dict[str, ReferenceUnit] = {}
    visiting: set[str] = set()

    def resolve(name: str) -> ReferenceUnit:
        if name in result:
            return result[name]
        if name not in definitions or name in visiting or len(visiting) >= 32:
            raise ValueError("unknown, cyclic or excessively deep unit reference")
        if not name.strip() or len(name) > 128:
            raise ValueError("unit names require 1 through 128 characters")
        visiting.add(name)
        row = _object(definitions[name], name)
        if set(row) == {"dimensions", "si_ratio"}:
            dims = row["dimensions"]
            if (
                not isinstance(dims, list)
                or len(dims) != 7
                or any(type(v) is not int or abs(v) > 16 for v in dims)
            ):
                raise ValueError("dimensions require seven bounded integer exponents")
            unit = ReferenceUnit(tuple(dims), _ratio(row["si_ratio"]))
        elif set(row) == {"factors", "ratio"}:
            factors = _object(row["factors"], "factors")
            scale, dimensions = _ratio(row["ratio"]), [0] * 7
            measured: set[str] = set()
            for dependency, power in factors.items():
                if type(power) is not int or not -16 <= power <= 16 or power == 0:
                    raise ValueError("unit powers require nonzero bounded integer exponents")
                item = resolve(dependency)
                measured.update(item.measured_dependencies)
                scale = _bounded(scale * _bounded(item.si_scale**power))
                dimensions = [a + power * b for a, b in zip(dimensions, item.dimensions, strict=True)]
            if any(abs(v) > 16 for v in dimensions):
                raise ValueError("derived dimension exceeds the exponent bound")
            unit = ReferenceUnit(tuple(dimensions), scale, tuple(sorted(measured)))
        else:
            required = {"unit", "value_decimal", "status", "sources", "context"}
            if not required <= row.keys() or set(row) - required - {"uncertainty_decimal"}:
                raise ValueError("unsupported constant definition")
            refs = row["sources"]
            if (
                not isinstance(refs, list)
                or not refs
                or any(not isinstance(ref, str) or ref not in sources for ref in refs)
            ):
                raise ValueError("constant requires known sources")
            if (
                row["status"] not in ("exact", "measured")
                or not isinstance(row["context"], str)
                or not row["context"].strip()
            ):
                raise ValueError("constant requires exact/measured status and context")
            if row["status"] == "measured":
                if _number(row.get("uncertainty_decimal")) <= 0:
                    raise ValueError("measured constant requires positive uncertainty")
            elif "uncertainty_decimal" in row:
                raise ValueError("exact constants must not declare measured uncertainty")
            if not isinstance(row["unit"], str):
                raise ValueError("constant unit must be a name")
            parent = resolve(row["unit"])
            value = _number(row["value_decimal"])
            if value <= 0:
                raise ValueError("constant used as a unit scale must be positive")
            measured = set(parent.measured_dependencies)
            if row["status"] == "measured":
                measured.add(name)
            unit = ReferenceUnit(
                parent.dimensions, _bounded(value * parent.si_scale), tuple(sorted(measured))
            )
        visiting.remove(name)
        result[name] = unit
        return unit

    for name in definitions:
        resolve(name)
    return result


def encode_components(
    registry: object,
    values: str | list[str],
    source_unit: str,
    field: object,
    *,
    max_error: str | None = None,
) -> dict[str, Any]:
    """Encode a Scalar/Vector; optional error budget is per component in source units.

    Exact mode is the default. Explicit rounding uses nearest, ties away from zero.
    Errors describe representation of the central value, not experimental uncertainty.
    """
    units = parse_reference_units(registry)
    definition = _object(field, "field")
    components = definition.get("components")
    scale = definition.get("scale", 1)
    signed = definition.get("signed")
    target_name = definition.get("units")
    if type(components) is not int or components not in (1, 3):
        raise ValueError("field components must be 1 or 3")
    if type(scale) is not int or not 1 <= scale <= MAX_VALUE or type(signed) is not bool:
        raise ValueError("field scale/sign must respect the runtime schema")
    if not isinstance(target_name, str) or target_name not in units or source_unit not in units:
        raise ValueError("unknown source or field unit")
    source, target = units[source_unit], units[target_name]
    if source.dimensions != target.dimensions:
        raise ValueError("incompatible physical dimensions")
    items = [values] if isinstance(values, str) else values
    if not isinstance(items, list) or len(items) != components:
        raise ValueError("input must match the declared Scalar/Vector shape")
    tolerance = None if max_error is None else _number(max_error)
    if tolerance is not None and tolerance < 0:
        raise ValueError("max_error must be nonnegative")
    factor = _bounded(source.si_scale * scale / target.si_scale)
    encoded, errors = [], []
    for item in items:
        value = _number(item)
        if not signed and value < 0:
            raise ValueError("negative reference cannot enter an unsigned field")
        exact = _bounded(value * factor)
        if exact.denominator == 1:
            integer = exact.numerator
        elif tolerance is None:
            raise ValueError(
                "value is not an exact integer field multiple; choose a scale or explicit max_error"
            )
        else:
            magnitude = abs(exact)
            integer = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
            if exact < 0:
                integer = -integer
        if abs(integer) > MAX_VALUE:
            raise ValueError("encoded component exceeds the runtime payload bound")
        error = _bounded(Fraction(integer) / factor - value)
        if tolerance is not None and abs(error) > tolerance:
            raise ValueError("representation error exceeds max_error")
        encoded.append(integer)
        errors.append(str(error))
    quantum = _bounded(target.si_scale / scale)
    return {
        "value": encoded[0] if components == 1 else encoded,
        "source_unit": source_unit,
        "field_unit": target_name,
        "scale": scale,
        "quantum_si_ratio": [quantum.numerator, quantum.denominator],
        "errors_source_units": errors,
        "rounding": "exact" if tolerance is None else "nearest_ties_away_from_zero",
        "measured_scale_dependencies": sorted(
            set(source.measured_dependencies) | set(target.measured_dependencies)
        ),
        "experimental_uncertainty_propagated": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, required=True)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--value", nargs="+")
    inputs.add_argument("--entity")
    parser.add_argument("--catalog", type=Path)
    parser.add_argument("--property", default="mass")
    parser.add_argument("--from-unit")
    parser.add_argument("--field-unit", required=True)
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--unsigned", action="store_true")
    parser.add_argument("--max-error")
    args = parser.parse_args()
    registry = parse_json_document(args.registry.read_text(encoding="utf-8"))
    values, unit = args.value, args.from_unit
    if args.entity:
        if args.catalog is None or args.from_unit is not None:
            parser.error("--entity requires --catalog and uses the property's own source unit")
        catalog = parse_json_document(args.catalog.read_text(encoding="utf-8"))
        prop = resolve_property(catalog, args.entity, args.property)
        if "value_decimal" not in prop:
            parser.error("selected property has no numerical central value")
        values, unit = [prop["value_decimal"]], prop["unit"]
    if unit is None:
        parser.error("--value requires --from-unit")
    field = {
        "components": len(values),
        "units": args.field_unit,
        "scale": args.scale,
        "signed": not args.unsigned,
    }
    result = encode_components(registry, values, unit, field, max_error=args.max_error)
    if args.entity:
        result["property_reference"] = {
            "entity": args.entity,
            "property": args.property,
            "descriptor": prop,
        }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
