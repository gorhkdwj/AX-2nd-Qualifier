#!/usr/bin/env python3
"""Find deterministic duplicate candidates from structured product JSON."""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any


def load_json(path: str | None) -> Any:
    if not path or path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def iter_products(payload: Any) -> list[dict[str, Any]]:
    products: list[dict[str, Any]] = []
    raw_items = payload.get("products") if isinstance(payload, dict) else payload
    if not isinstance(raw_items, list):
        raise ValueError("input must be a list or an object with a products list")

    for index, item in enumerate(raw_items):
        if not isinstance(item, dict):
            continue
        product_id = str(item.get("product_id") or item.get("id") or f"product_{index + 1}")
        structured = item.get("structured_product") if isinstance(item.get("structured_product"), dict) else item
        products.append({"id": product_id, "structured": structured})
    return products


def values(product: dict[str, Any], field: str) -> set[str]:
    raw = product.get("product", {}).get(field) or []
    if isinstance(raw, list):
        return {str(item) for item in raw if item is not None}
    if raw is None:
        return set()
    return {str(raw)}


def material_values(product: dict[str, Any]) -> set[str]:
    materials = product.get("product", {}).get("materials") or []
    result: set[str] = set()
    for item in materials:
        if not isinstance(item, dict):
            continue
        part = item.get("part") or "unknown"
        name = item.get("name")
        if name:
            result.add(f"{part}:{name}")
    return result


def text_tokens(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[\w가-힣]+", text) if len(token) >= 2}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def score_pair(left: dict[str, Any], right: dict[str, Any]) -> tuple[float, list[str]]:
    left_product = left["structured"].get("product", {})
    right_product = right["structured"].get("product", {})
    matched: list[str] = []
    score = 0.0

    if left_product.get("category") and left_product.get("category") == right_product.get("category"):
        score += 0.18
        matched.append("category")
    if left_product.get("subcategory") and left_product.get("subcategory") == right_product.get("subcategory"):
        score += 0.16
        matched.append("subcategory")

    weighted_sets = [
        ("materials", material_values(left["structured"]), material_values(right["structured"]), 0.20),
        ("colors", values(left["structured"], "colors"), values(right["structured"], "colors"), 0.12),
        ("fit", values(left["structured"], "fit"), values(right["structured"], "fit"), 0.10),
        ("seasons", values(left["structured"], "seasons"), values(right["structured"], "seasons"), 0.08),
        ("tpo_tags", values(left["structured"], "tpo_tags"), values(right["structured"], "tpo_tags"), 0.08),
        ("care", values(left["structured"], "care"), values(right["structured"], "care"), 0.04),
    ]

    for field, left_values, right_values, weight in weighted_sets:
        similarity = jaccard(left_values, right_values)
        if similarity > 0:
            score += weight * similarity
        if similarity >= 0.5:
            matched.append(field)

    title_left = text_tokens(str(left_product.get("title") or ""))
    title_right = text_tokens(str(right_product.get("title") or ""))
    title_similarity = jaccard(title_left, title_right)
    if title_similarity > 0:
        score += 0.14 * title_similarity
    if title_similarity >= 0.35:
        matched.append("title")

    return round(min(score, 1.0), 4), matched


def decision(score: float) -> str:
    if score >= 0.78:
        return "duplicate"
    if score >= 0.55:
        return "possible_duplicate"
    return "distinct"


def find_candidates(products: list[dict[str, Any]], min_score: float) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for left, right in itertools.combinations(products, 2):
        score, matched = score_pair(left, right)
        if score < min_score:
            continue
        candidates.append(
            {
                "left_id": left["id"],
                "right_id": right["id"],
                "score": score,
                "decision": decision(score),
                "matched_fields": matched,
                "reason": f"score {score:.2f} from matched fields: {', '.join(matched) if matched else 'none'}",
            }
        )
    return candidates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Detect duplicate candidates from structured product JSON.")
    parser.add_argument("input", nargs="?", help="Input JSON file. Reads stdin when omitted or set to '-'.")
    parser.add_argument("--min-score", type=float, default=0.45, help="Minimum score to include in output.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        products = iter_products(load_json(args.input))
        output = {"duplicate_candidates": find_candidates(products, args.min_score)}
    except Exception as exc:
        print(json.dumps({"duplicate_candidates": [], "error": str(exc)}))
        return 2

    print(json.dumps(output, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
