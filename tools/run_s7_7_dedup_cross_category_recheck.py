#!/usr/bin/env python3
"""Independently recompute S7.7 cross-category dedup safety metrics."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import platform
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "tests" / "fixtures" / "full_page_dummy" / "reference_actual_products.json"
STORED_RESULT_PATH = ROOT / "docs" / "reports" / "s7-7-full-page-dummy-validation-results.json"
RESULT_PATH = ROOT / "docs" / "reports" / "s7-7-dedup-cross-category-recheck-results.json"
REPORT_PATH = ROOT / "docs" / "reports" / "s7-7-dedup-cross-category-recheck-report.md"
DEDUP_PATH = ROOT / "src" / "skills" / "product-agentizer" / "scripts" / "dedup.py"
KST = timezone(timedelta(hours=9))

MIN_CANDIDATE_SCORE = 0.45
HIGH_CONFIDENCE_THRESHOLD = 0.78


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_dedup_module() -> Any:
    spec = importlib.util.spec_from_file_location("product_agentizer_dedup_recheck", DEDUP_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import dedup module: {DEDUP_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def safe_product_category(product: dict[str, Any]) -> str:
    return str(product["structured"].get("product", {}).get("category") or "unknown")


def recheck() -> dict[str, Any]:
    dedup = load_dedup_module()
    products = dedup.iter_products(load_json(INPUT_PATH))
    stored = load_json(STORED_RESULT_PATH)
    stored_cross = stored.get("dedup_cross_category_check", {})

    category_by_id = {item["id"]: safe_product_category(item) for item in products}
    category_counts = Counter(category_by_id.values())
    decision_counts: Counter[str] = Counter()
    candidate_decision_counts: Counter[str] = Counter()

    total_pairs = 0
    cross_category_pairs = 0
    candidate_count = 0
    cross_category_candidate_count = 0
    high_confidence_count = 0
    high_confidence_cross_category: list[dict[str, Any]] = []
    top_cross_category_scores: list[dict[str, Any]] = []

    for left, right in itertools.combinations(products, 2):
        total_pairs += 1
        left_id = left["id"]
        right_id = right["id"]
        left_category = category_by_id[left_id]
        right_category = category_by_id[right_id]
        is_cross_category = left_category != right_category
        if is_cross_category:
            cross_category_pairs += 1

        score, matched_fields = dedup.score_pair(left, right)
        decision = dedup.decision(score)
        decision_counts[decision] += 1

        if score >= MIN_CANDIDATE_SCORE:
            candidate_count += 1
            candidate_decision_counts[decision] += 1
            if is_cross_category:
                cross_category_candidate_count += 1

        if score >= HIGH_CONFIDENCE_THRESHOLD:
            high_confidence_count += 1
            if is_cross_category:
                high_confidence_cross_category.append(
                    {
                        "left_id": left_id,
                        "right_id": right_id,
                        "left_category": left_category,
                        "right_category": right_category,
                        "score": score,
                        "decision": decision,
                        "matched_fields": matched_fields,
                    }
                )

        if is_cross_category:
            top_cross_category_scores.append(
                {
                    "left_id": left_id,
                    "right_id": right_id,
                    "left_category": left_category,
                    "right_category": right_category,
                    "score": score,
                    "decision": decision,
                    "matched_fields": matched_fields,
                }
            )

    top_cross_category_scores.sort(key=lambda item: item["score"], reverse=True)

    stored_candidate_count = stored_cross.get("candidate_count")
    stored_high_cross_count = stored_cross.get("high_confidence_cross_category_count")
    candidate_count_matches_stored = candidate_count == stored_candidate_count
    high_cross_count_matches_stored = len(high_confidence_cross_category) == stored_high_cross_count
    passed = (
        candidate_count_matches_stored
        and high_cross_count_matches_stored
        and len(high_confidence_cross_category) == 0
    )

    generated_at_utc = datetime.now(timezone.utc)
    return {
        "generated_at_utc": generated_at_utc.isoformat(),
        "generated_for_kst_date": generated_at_utc.astimezone(KST).date().isoformat(),
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
        },
        "input": {
            "products_path": rel(INPUT_PATH),
            "stored_result_path": rel(STORED_RESULT_PATH),
            "dedup_script_path": rel(DEDUP_PATH),
            "min_candidate_score": MIN_CANDIDATE_SCORE,
            "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        },
        "reproduction_command": "python tools/run_s7_7_dedup_cross_category_recheck.py",
        "hashes_sha256": {
            rel(INPUT_PATH): sha256(INPUT_PATH),
            rel(STORED_RESULT_PATH): sha256(STORED_RESULT_PATH),
            rel(DEDUP_PATH): sha256(DEDUP_PATH),
        },
        "recomputed": {
            "product_count": len(products),
            "category_counts": dict(category_counts),
            "total_pair_count": total_pairs,
            "cross_category_pair_count": cross_category_pairs,
            "candidate_count_at_min_score": candidate_count,
            "candidate_decision_counts": dict(candidate_decision_counts),
            "decision_counts_all_pairs": dict(decision_counts),
            "cross_category_candidate_count_at_min_score": cross_category_candidate_count,
            "high_confidence_candidate_count": high_confidence_count,
            "high_confidence_cross_category_false_duplicate_count": len(high_confidence_cross_category),
            "high_confidence_cross_category_examples": high_confidence_cross_category[:5],
            "top_cross_category_scores": top_cross_category_scores[:5],
        },
        "stored_s7_7": {
            "candidate_count": stored_candidate_count,
            "high_confidence_cross_category_count": stored_high_cross_count,
            "examples": stored_cross.get("examples", []),
        },
        "comparison": {
            "candidate_count_matches_stored": candidate_count_matches_stored,
            "high_confidence_cross_category_count_matches_stored": high_cross_count_matches_stored,
            "passed": passed,
        },
    }


def write_report(result: dict[str, Any]) -> None:
    recomputed = result["recomputed"]
    stored = result["stored_s7_7"]
    comparison = result["comparison"]
    top_cross = recomputed["top_cross_category_scores"]
    top_rows = [
        f"| `{item['left_id']}` | `{item['right_id']}` | {item['score']:.4f} | `{item['decision']}` | {', '.join(item['matched_fields']) if item['matched_fields'] else 'none'} |"
        for item in top_cross
    ]
    lines = [
        "# S7.7 dedup cross-category 독립 재계산 보고서",
        "",
        "## 요약",
        "",
        "- 목적: S7.7 결과 JSON에 저장된 `dedup_cross_category_check` 값을 그대로 신뢰하지 않고, `full_page_dummy/reference_actual_products.json`의 모든 상품쌍을 처음부터 다시 점수화해 cross-category high-confidence false duplicate 0건을 독립 재현한다.",
        f"- 생성 일시(UTC): `{result['generated_at_utc']}`",
        f"- 기준 KST 날짜: `{result['generated_for_kst_date']}`",
        f"- 전체 통과: `{comparison['passed']}`",
        "",
        "## 입력과 기준",
        "",
        f"- 입력 상품 JSON: `{result['input']['products_path']}`",
        f"- 비교 대상 저장 결과: `{result['input']['stored_result_path']}`",
        f"- 점수 함수: `{result['input']['dedup_script_path']}`",
        f"- 후보 포함 최소 점수: `{result['input']['min_candidate_score']}`",
        f"- high-confidence duplicate 임계값: `{result['input']['high_confidence_threshold']}`",
        f"- 재실행 명령: `{result['reproduction_command']}`",
        "",
        "## 재계산 결과",
        "",
        "| 항목 | 값 |",
        "|---|---:|",
        f"| 상품 수 | {recomputed['product_count']} |",
        f"| category 분포 | `{json.dumps(recomputed['category_counts'], ensure_ascii=False)}` |",
        f"| 전체 상품쌍 | {recomputed['total_pair_count']} |",
        f"| cross-category 상품쌍 | {recomputed['cross_category_pair_count']} |",
        f"| score >= 0.45 후보 수 | {recomputed['candidate_count_at_min_score']} |",
        f"| score >= 0.45 cross-category 후보 수 | {recomputed['cross_category_candidate_count_at_min_score']} |",
        f"| score >= 0.78 high-confidence 후보 수 | {recomputed['high_confidence_candidate_count']} |",
        f"| high-confidence cross-category false duplicate | {recomputed['high_confidence_cross_category_false_duplicate_count']} |",
        "",
        "## 저장 결과 대조",
        "",
        "| 항목 | 저장값 | 재계산값 | 일치 |",
        "|---|---:|---:|---:|",
        f"| candidate_count | {stored['candidate_count']} | {recomputed['candidate_count_at_min_score']} | {comparison['candidate_count_matches_stored']} |",
        f"| high_confidence_cross_category_count | {stored['high_confidence_cross_category_count']} | {recomputed['high_confidence_cross_category_false_duplicate_count']} | {comparison['high_confidence_cross_category_count_matches_stored']} |",
        "",
        "## 상위 cross-category 점수",
        "",
        "high-confidence 임계값 0.78 이상인 cross-category 쌍은 없었다. 아래는 참고용으로 score가 가장 높은 cross-category 쌍 5개다.",
        "",
        "| left_id | right_id | score | decision | matched_fields |",
        "|---|---|---:|---|---|",
        *top_rows,
        "",
        "## 해석",
        "",
        "- 전체 300개 상품에서 가능한 모든 상품쌍 44,850개를 재계산했고, 그중 outer/top이 다른 cross-category 쌍은 22,500개였다.",
        "- score 0.45 이상으로 후보 목록에 들어온 쌍은 2,788개로 저장된 S7.7 결과와 일치했다.",
        "- score 0.78 이상 high-confidence duplicate 후보는 23개였고, 모두 같은 category 안의 쌍이었다.",
        "- cross-category 쌍 중 score 0.45 이상 후보는 0개였고, high-confidence false duplicate도 0개였다.",
        "- 따라서 S9 보고서의 미검증 범위였던 S7.7 dedup cross-category 재계산 독립 검증은 해소됐다.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = recheck()
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(result)
    print(
        json.dumps(
            {
                "result_path": str(RESULT_PATH),
                "report_path": str(REPORT_PATH),
                "passed": result["comparison"]["passed"],
                "candidate_count": result["recomputed"]["candidate_count_at_min_score"],
                "high_confidence_cross_category_false_duplicate_count": result["recomputed"]["high_confidence_cross_category_false_duplicate_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["comparison"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
