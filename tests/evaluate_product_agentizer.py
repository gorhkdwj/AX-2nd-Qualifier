#!/usr/bin/env python3
"""Evaluate product-agentizer dummy fixtures against expected labels."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "evaluation"
DEFAULT_INPUTS = FIXTURE_DIR / "source_inputs.json"
DEFAULT_EXPECTED = FIXTURE_DIR / "expected_products.json"
DEFAULT_ACTUAL = FIXTURE_DIR / "predicted_products.json"
DEFAULT_DEDUP_LABELS = FIXTURE_DIR / "duplicate_labels.json"
VALIDATE_SCRIPT = ROOT / "src" / "skills" / "product-agentizer" / "scripts" / "validate.py"
DEDUP_SCRIPT = ROOT / "src" / "skills" / "product-agentizer" / "scripts" / "dedup.py"

EVALUATED_FIELDS = [
    "title",
    "category",
    "subcategory",
    "materials",
    "fit",
    "colors",
    "seasons",
    "tpo_tags",
    "care",
    "size_info",
    "quality.missing_fields",
    "quality.ambiguous_fields",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_dedup_module() -> Any:
    spec = importlib.util.spec_from_file_location("product_agentizer_dedup", DEDUP_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {DEDUP_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def product_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    products: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(payload.get("products", [])):
        product_id = str(item.get("product_id") or f"product_{index + 1}")
        structured = item.get("structured_product")
        if isinstance(structured, dict):
            products[product_id] = structured
    return products


def ratio_token(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value)


def material_tokens(product: dict[str, Any]) -> set[str]:
    tokens: set[str] = set()
    for item in product.get("product", {}).get("materials") or []:
        if not isinstance(item, dict):
            continue
        tokens.add(
            ":".join(
                [
                    str(item.get("part")),
                    str(item.get("name")),
                    str(item.get("ratio_status")),
                    ratio_token(item.get("ratio")),
                ]
            )
        )
    return tokens


def list_tokens(product: dict[str, Any], field: str) -> set[str]:
    values = product.get("product", {}).get(field) or []
    if not isinstance(values, list):
        return set()
    return {str(item).strip() for item in values if str(item).strip()}


def quality_tokens(product: dict[str, Any], field: str) -> set[str]:
    values = product.get("quality", {}).get(field) or []
    if not isinstance(values, list):
        return set()
    return {str(item).strip() for item in values if str(item).strip()}


def field_tokens(product: dict[str, Any], field: str) -> set[str]:
    structured = product.get("product", {})
    if field in {"title", "category", "subcategory"}:
        value = structured.get(field)
        return {str(value).strip()} if value is not None and str(value).strip() else set()
    if field == "materials":
        return material_tokens(product)
    if field.startswith("quality."):
        return quality_tokens(product, field.split(".", 1)[1])
    return list_tokens(product, field)


def metric(tp: int, fp: int, fn: int) -> dict[str, Any]:
    precision_denominator = tp + fp
    recall_denominator = tp + fn
    precision: float | str = "not_applicable"
    recall: float | str = "not_applicable"
    if precision_denominator:
        precision = round(tp / precision_denominator, 4)
    if recall_denominator:
        recall = round(tp / recall_denominator, 4)
    return {
        "precision": precision,
        "recall": recall,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
    }


def evaluate_attributes(expected: dict[str, Any], actual: dict[str, Any]) -> dict[str, Any]:
    expected_products = product_map(expected)
    actual_products = product_map(actual)
    ids = sorted(set(expected_products) | set(actual_products))

    by_field_counts = {field: {"tp": 0, "fp": 0, "fn": 0} for field in EVALUATED_FIELDS}
    case_reports: list[dict[str, Any]] = []

    for product_id in ids:
        expected_product = expected_products.get(product_id, {})
        actual_product = actual_products.get(product_id, {})
        case_counts = {"tp": 0, "fp": 0, "fn": 0}
        differences: list[dict[str, Any]] = []

        for field in EVALUATED_FIELDS:
            expected_tokens = field_tokens(expected_product, field)
            actual_tokens = field_tokens(actual_product, field)
            tp_values = expected_tokens & actual_tokens
            fp_values = actual_tokens - expected_tokens
            fn_values = expected_tokens - actual_tokens

            counts = by_field_counts[field]
            counts["tp"] += len(tp_values)
            counts["fp"] += len(fp_values)
            counts["fn"] += len(fn_values)
            case_counts["tp"] += len(tp_values)
            case_counts["fp"] += len(fp_values)
            case_counts["fn"] += len(fn_values)

            if fp_values or fn_values:
                differences.append(
                    {
                        "field": field,
                        "false_positive": sorted(fp_values),
                        "false_negative": sorted(fn_values),
                    }
                )

        case_reports.append(
            {
                "product_id": product_id,
                "metrics": metric(case_counts["tp"], case_counts["fp"], case_counts["fn"]),
                "differences": differences,
            }
        )

    by_field = {
        field: metric(counts["tp"], counts["fp"], counts["fn"])
        for field, counts in by_field_counts.items()
    }
    total = {
        "tp": sum(counts["tp"] for counts in by_field_counts.values()),
        "fp": sum(counts["fp"] for counts in by_field_counts.values()),
        "fn": sum(counts["fn"] for counts in by_field_counts.values()),
    }
    return {
        "micro": metric(total["tp"], total["fp"], total["fn"]),
        "by_field": by_field,
        "cases": case_reports,
        "missing_actual_product_ids": sorted(set(expected_products) - set(actual_products)),
        "extra_actual_product_ids": sorted(set(actual_products) - set(expected_products)),
    }


def pair_key(left_id: str, right_id: str) -> tuple[str, str]:
    return tuple(sorted((left_id, right_id)))


def evaluate_dedup(actual: dict[str, Any], labels: dict[str, Any], min_score: float) -> dict[str, Any]:
    dedup = load_dedup_module()
    candidates = dedup.find_candidates(dedup.iter_products(actual), min_score=min_score)
    candidates_by_pair = {
        pair_key(str(item["left_id"]), str(item["right_id"])): item for item in candidates
    }

    pair_reports: list[dict[str, Any]] = []
    correct = 0
    for label in labels.get("pairs", []):
        left_id = str(label["left_id"])
        right_id = str(label["right_id"])
        expected_decision = str(label["expected_decision"])
        candidate = candidates_by_pair.get(pair_key(left_id, right_id))
        actual_decision = candidate["decision"] if candidate else "distinct"
        score = candidate["score"] if candidate else 0.0
        matched_fields = candidate["matched_fields"] if candidate else []
        is_correct = actual_decision == expected_decision
        correct += int(is_correct)
        pair_reports.append(
            {
                "left_id": left_id,
                "right_id": right_id,
                "expected_decision": expected_decision,
                "actual_decision": actual_decision,
                "score": score,
                "matched_fields": matched_fields,
                "correct": is_correct,
            }
        )

    total = len(pair_reports)
    return {
        "accuracy": round(correct / total, 4) if total else "not_applicable",
        "correct": correct,
        "total": total,
        "min_score": min_score,
        "candidate_count": len(candidates),
        "pairs": pair_reports,
    }


def validate_fixture(path: Path) -> dict[str, Any]:
    process = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT), str(path)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    try:
        report = json.loads(process.stdout)
    except json.JSONDecodeError:
        report = {"valid": False, "checked": 0, "errors": [{"message": process.stdout.strip()}]}
    return {
        "path": str(path.relative_to(ROOT)),
        "exit_code": process.returncode,
        "valid": process.returncode == 0 and bool(report.get("valid")),
        "checked": report.get("checked", 0),
        "errors": report.get("errors", []),
        "stderr": process.stderr.strip(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate product-agentizer dummy fixtures.")
    parser.add_argument("--inputs", type=Path, default=DEFAULT_INPUTS, help="Source input fixture path.")
    parser.add_argument("--expected", type=Path, default=DEFAULT_EXPECTED, help="Expected structured products.")
    parser.add_argument("--actual", type=Path, default=DEFAULT_ACTUAL, help="Actual/predicted structured products.")
    parser.add_argument("--dedup-labels", type=Path, default=DEFAULT_DEDUP_LABELS, help="Duplicate pair labels.")
    parser.add_argument("--min-score", type=float, default=0.45, help="Minimum dedup score used by dedup.py.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = load_json(args.inputs)
    expected = load_json(args.expected)
    actual = load_json(args.actual)
    labels = load_json(args.dedup_labels)

    validations = [validate_fixture(args.expected), validate_fixture(args.actual)]
    attribute_metrics = evaluate_attributes(expected, actual)
    dedup_metrics = evaluate_dedup(actual, labels, args.min_score)

    report = {
        "summary": {
            "input_cases": len(inputs.get("cases", [])),
            "expected_products": len(expected.get("products", [])),
            "actual_products": len(actual.get("products", [])),
            "evaluated_fields": EVALUATED_FIELDS,
        },
        "validations": validations,
        "attribute_metrics": attribute_metrics,
        "dedup_metrics": dedup_metrics,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2 if args.pretty else None))

    validation_ok = all(item["valid"] for item in validations)
    dedup_ok = dedup_metrics["accuracy"] == 1.0
    return 0 if validation_ok and dedup_ok else 1


if __name__ == "__main__":
    sys.exit(main())
