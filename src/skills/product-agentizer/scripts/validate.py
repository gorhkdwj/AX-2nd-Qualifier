#!/usr/bin/env python3
"""Validate product-agentizer structured JSON against schema and taxonomy rules."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - exercised only when dependency is absent.
    print(
        "Missing dependency: jsonschema. Install it with `python -m pip install jsonschema`.",
        file=sys.stderr,
    )
    sys.exit(2)


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = SKILL_DIR / "references" / "schema.json"
DEFAULT_TAXONOMY = SKILL_DIR / "references" / "taxonomy.json"


def load_json(path: str | None) -> Any:
    if not path or path == "-":
        raw = sys.stdin.read()
        source = "stdin"
    else:
        raw = Path(path).read_text(encoding="utf-8")
        source = path
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{source}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc


def error_path(error: Any) -> str:
    path = ".".join(str(part) for part in error.path)
    return path or "<root>"


def load_validator(schema_path: Path) -> Draft202012Validator:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def load_taxonomy(taxonomy_path: Path) -> dict[str, Any]:
    return json.loads(taxonomy_path.read_text(encoding="utf-8"))


def iter_structured_products(payload: Any) -> Iterable[tuple[str, dict[str, Any]]]:
    if isinstance(payload, dict) and isinstance(payload.get("products"), list):
        for index, item in enumerate(payload["products"]):
            if not isinstance(item, dict):
                yield f"products[{index}]", {}
                continue
            product_id = str(item.get("product_id") or f"products[{index}]")
            structured = item.get("structured_product")
            if isinstance(structured, dict):
                yield product_id, structured
            else:
                yield product_id, {}
        return

    if isinstance(payload, list):
        for index, item in enumerate(payload):
            product_id = f"items[{index}]"
            if isinstance(item, dict) and isinstance(item.get("structured_product"), dict):
                product_id = str(item.get("product_id") or product_id)
                yield product_id, item["structured_product"]
            elif isinstance(item, dict):
                yield product_id, item
            else:
                yield product_id, {}
        return

    if isinstance(payload, dict):
        yield "product", payload
        return

    yield "product", {}


def taxonomy_sets(taxonomy: dict[str, Any]) -> dict[str, set[str]]:
    vocabularies = taxonomy.get("vocabularies", {})
    categories = taxonomy.get("categories", {})
    return {
        "attribute_keys": set(taxonomy.get("attribute_keys", [])),
        "categories": set(taxonomy.get("scope", {}).get("supported_categories", [])),
        "subcategories": {
            subcategory.get("id")
            for category in categories.values()
            for subcategory in category.get("subcategories", [])
        },
        "materials": {item.get("id") for item in vocabularies.get("materials", [])},
        "material_parts": {item.get("id") for item in vocabularies.get("material_parts", [])},
        "ratio_statuses": {item.get("id") for item in vocabularies.get("ratio_statuses", [])},
        "fits": {item.get("id") for item in vocabularies.get("fits", [])},
        "colors": {item.get("id") for item in vocabularies.get("colors", [])},
        "seasons": {item.get("id") for item in vocabularies.get("seasons", [])},
        "tpo_tags": {item.get("id") for item in vocabularies.get("tpo_tags", [])},
        "care": {item.get("id") for item in vocabularies.get("care", [])},
    }


def custom_checks(product: dict[str, Any], tax: dict[str, set[str]], product_id: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    structured = product.get("product", {})
    quality = product.get("quality", {})

    if quality.get("out_of_scope") is not True and structured.get("category") not in tax["categories"]:
        errors.append(
            {
                "product_id": product_id,
                "path": "product.category",
                "message": "category must be outer or top unless the product is out of scope",
            }
        )

    missing_fields = set(quality.get("missing_fields") or [])
    ambiguous_fields = set(quality.get("ambiguous_fields") or [])
    explicit_ratio_by_part: dict[str, float] = {}
    saw_missing_ratio = False
    saw_ambiguous_ratio = False

    for index, material in enumerate(structured.get("materials") or []):
        if not isinstance(material, dict):
            continue
        path = f"product.materials[{index}]"
        part = material.get("part")
        status = material.get("ratio_status")
        ratio = material.get("ratio")

        if part not in tax["material_parts"]:
            errors.append({"product_id": product_id, "path": f"{path}.part", "message": "unknown material part"})
        if material.get("name") not in tax["materials"]:
            errors.append({"product_id": product_id, "path": f"{path}.name", "message": "unknown material name"})
        if status not in tax["ratio_statuses"]:
            errors.append({"product_id": product_id, "path": f"{path}.ratio_status", "message": "unknown ratio status"})

        if status == "explicit" and isinstance(ratio, (int, float)) and part:
            explicit_ratio_by_part[part] = explicit_ratio_by_part.get(part, 0.0) + float(ratio)
        elif status == "missing":
            saw_missing_ratio = True
        elif status == "ambiguous":
            saw_ambiguous_ratio = True

    for part, total in explicit_ratio_by_part.items():
        if total > 100.01:
            errors.append(
                {
                    "product_id": product_id,
                    "path": "product.materials",
                    "message": f"explicit material ratios for part `{part}` sum to more than 100",
                }
            )

    if saw_missing_ratio and "material_ratio" not in missing_fields:
        errors.append(
            {
                "product_id": product_id,
                "path": "quality.missing_fields",
                "message": "material_ratio must be listed when a material ratio is missing",
            }
        )
    if saw_ambiguous_ratio and "material_ratio" not in ambiguous_fields:
        errors.append(
            {
                "product_id": product_id,
                "path": "quality.ambiguous_fields",
                "message": "material_ratio must be listed when a material ratio is ambiguous",
            }
        )

    return errors


def validate_payload(payload: Any, schema_path: Path, taxonomy_path: Path) -> dict[str, Any]:
    validator = load_validator(schema_path)
    taxonomy = taxonomy_sets(load_taxonomy(taxonomy_path))

    all_errors: list[dict[str, str]] = []
    checked = 0

    for product_id, product in iter_structured_products(payload):
        checked += 1
        for error in sorted(validator.iter_errors(product), key=lambda item: list(item.path)):
            all_errors.append(
                {
                    "product_id": product_id,
                    "path": error_path(error),
                    "message": error.message,
                }
            )
        if isinstance(product, dict):
            all_errors.extend(custom_checks(product, taxonomy, product_id))

    return {
        "valid": not all_errors,
        "checked": checked,
        "errors": all_errors,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate product-agentizer structured JSON.")
    parser.add_argument("input", nargs="?", help="Input JSON file. Reads stdin when omitted or set to '-'.")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA), help="Path to schema.json.")
    parser.add_argument("--taxonomy", default=str(DEFAULT_TAXONOMY), help="Path to taxonomy.json.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the validation report.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = load_json(args.input)
        report = validate_payload(payload, Path(args.schema), Path(args.taxonomy))
    except Exception as exc:  # Keep CLI failures explicit for Codex and users.
        print(json.dumps({"valid": False, "checked": 0, "errors": [{"path": "<runtime>", "message": str(exc)}]}))
        return 2

    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
