#!/usr/bin/env python3
"""Run S7.8 size_info pattern validation and preserve results."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "size_info_patterns"
RESULT_PATH = ROOT / "docs" / "reports" / "s7-8-size-info-coverage-results.json"
REPORT_PATH = ROOT / "docs" / "reports" / "s7-8-size-info-coverage-report.md"
KST = timezone(timedelta(hours=9))
SYNTHETIC_URL_PREFIX = "https://example.com/musinsa-size-info-pattern/"

HASH_TARGETS = [
    "src/skills/product-agentizer/SKILL.md",
    "src/skills/product-agentizer/references/schema.json",
    "src/skills/product-agentizer/references/taxonomy.json",
    "src/skills/product-agentizer/scripts/validate.py",
    "tools/generate_size_info_pattern_fixtures.py",
    "tools/run_size_info_pattern_validation.py",
    "tools/run_full_page_codex_smoke20_cli.py",
    "tests/fixtures/size_info_patterns/source_inputs.json",
    "tests/fixtures/size_info_patterns/expected_products.json",
    "tests/fixtures/size_info_patterns/actual_products.json",
    "tests/fixtures/size_info_patterns/actual_metadata.json",
    "tests/fixtures/size_info_patterns/case_metadata.json",
    "tests/fixtures/size_info_patterns/prompt.md",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_validate(path: Path) -> dict[str, Any]:
    process = subprocess.run(
        [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            str(path.relative_to(ROOT)),
        ],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    try:
        parsed = json.loads(process.stdout)
    except json.JSONDecodeError:
        parsed = {"valid": False, "checked": 0, "errors": [{"message": process.stdout.strip()}]}
    return {
        "path": str(path.relative_to(ROOT)),
        "exit_code": process.returncode,
        "valid": process.returncode == 0 and bool(parsed.get("valid")),
        "checked": parsed.get("checked", 0),
        "errors": parsed.get("errors", []),
        "stderr": process.stderr.strip(),
    }


def product_map(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in payload.get("products", []):
        structured = item.get("structured_product")
        if isinstance(structured, dict):
            result[str(item["product_id"])] = structured
    return result


def size_tokens(product: dict[str, Any]) -> set[str]:
    values = product.get("product", {}).get("size_info") or []
    if not isinstance(values, list):
        return set()
    return {str(value).strip() for value in values if str(value).strip()}


def metric(tp: int, fp: int, fn: int) -> dict[str, Any]:
    precision: float | str = "not_applicable"
    recall: float | str = "not_applicable"
    if tp + fp:
        precision = round(tp / (tp + fp), 4)
    if tp + fn:
        recall = round(tp / (tp + fn), 4)
    return {
        "precision": precision,
        "recall": recall,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
    }


def display_metric(value: Any) -> str:
    if isinstance(value, float):
        return f"{value * 100:.2f}%"
    return str(value)


def evaluate_size_info(expected: dict[str, Any], actual: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    expected_products = product_map(expected)
    actual_products = product_map(actual)
    metadata_by_id = {item["product_id"]: item for item in metadata.get("cases", [])}

    total_counts = {"tp": 0, "fp": 0, "fn": 0}
    group_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
    cases: list[dict[str, Any]] = []
    noise_false_positive_cases: list[dict[str, Any]] = []

    for product_id in sorted(set(expected_products) | set(actual_products)):
        expected_tokens = size_tokens(expected_products.get(product_id, {}))
        actual_tokens = size_tokens(actual_products.get(product_id, {}))
        tp_values = expected_tokens & actual_tokens
        fp_values = actual_tokens - expected_tokens
        fn_values = expected_tokens - actual_tokens
        meta = metadata_by_id.get(product_id, {})
        group = str(meta.get("pattern_group", "unknown"))

        for key, values in (("tp", tp_values), ("fp", fp_values), ("fn", fn_values)):
            total_counts[key] += len(values)
            group_counts[group][key] += len(values)

        case_report = {
            "product_id": product_id,
            "pattern_group": group,
            "metrics": metric(len(tp_values), len(fp_values), len(fn_values)),
            "expected": sorted(expected_tokens),
            "actual": sorted(actual_tokens),
            "false_positive": sorted(fp_values),
            "false_negative": sorted(fn_values),
        }
        cases.append(case_report)
        if meta.get("negative_size_info_case") and fp_values:
            noise_false_positive_cases.append(case_report)

    group_metrics = {
        group: metric(counts["tp"], counts["fp"], counts["fn"])
        for group, counts in sorted(group_counts.items())
    }
    return {
        "micro": metric(total_counts["tp"], total_counts["fp"], total_counts["fn"]),
        "by_group": group_metrics,
        "cases": cases,
        "noise_false_positive_count": len(noise_false_positive_cases),
        "noise_false_positive_cases": noise_false_positive_cases,
        "missing_actual_product_ids": sorted(set(expected_products) - set(actual_products)),
        "extra_actual_product_ids": sorted(set(actual_products) - set(expected_products)),
    }


def synthetic_source_check(sources: dict[str, Any]) -> dict[str, Any]:
    cases = sources.get("cases", [])
    non_synthetic_urls = [
        item.get("source_url")
        for item in cases
        if not str(item.get("source_url", "")).startswith(SYNTHETIC_URL_PREFIX)
    ]
    non_synthetic_methods = [
        item.get("product_id")
        for item in cases
        if item.get("source_method") != "synthetic_size_info_pattern"
    ]
    return {
        "source_count": len(cases),
        "auto_fetch_count": 0,
        "real_page_copy_count": 0,
        "legal_compliance_judgment_count": 0,
        "non_synthetic_url_count": len(non_synthetic_urls),
        "non_synthetic_method_count": len(non_synthetic_methods),
        "non_synthetic_url_examples": non_synthetic_urls[:5],
        "non_synthetic_method_examples": non_synthetic_methods[:5],
    }


def write_report(result: dict[str, Any]) -> None:
    summary = result["acceptance_summary"]
    size_metrics = result["size_info_metrics"]
    lines = [
        "# S7.8 size_info 표기 패턴 보강 검증 보고서",
        "",
        "## 요약",
        "",
        "- 목적: 실제 상품 원문을 저장하지 않고, 실제 페이지에서 나올 법한 size_info 표기 유형을 합성 fixture로 확장해 검증한다.",
        f"- 생성 일시(UTC): `{result['generated_at_utc']}`",
        f"- 기준 KST 날짜: `{result['generated_for_kst_date']}`",
        f"- 전체 통과: `{summary['passed']}`",
        f"- actual mode: `{summary['actual_mode']}`",
        f"- actual 생성 일시(UTC): `{summary['actual_generated_at_utc']}`",
        "",
        "## 주요 지표",
        "",
        "| 지표 | 결과 |",
        "|---|---:|",
        f"| expected schema-valid | {summary['expected_schema_valid']} |",
        f"| actual schema-valid | {summary['actual_schema_valid']} |",
        f"| actual checked | {summary['actual_checked']} |",
        f"| size_info precision | {display_metric(summary['size_info_precision'])} |",
        f"| size_info recall | {display_metric(summary['size_info_recall'])} |",
        f"| size_info true/false positive/false negative | {summary['size_info_true_positive']} / {summary['size_info_false_positive']} / {summary['size_info_false_negative']} |",
        f"| recommendation_noise false positive cases | {summary['noise_false_positive_count']} |",
        f"| 자동 fetch | {summary['auto_fetch_count']} |",
        f"| 실제 상품 원문 저장 | {summary['real_page_copy_count']} |",
        f"| 법적 적합/부적합 판정 | {summary['legal_compliance_judgment_count']} |",
        "",
        "## 패턴 그룹별 결과",
        "",
        "| 그룹 | Precision | Recall | TP | FP | FN |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for group, metrics in size_metrics["by_group"].items():
        lines.append(
            f"| {group} | {display_metric(metrics['precision'])} | {display_metric(metrics['recall'])} | {metrics['true_positive']} | {metrics['false_positive']} | {metrics['false_negative']} |"
        )

    failed_cases = [
        case
        for case in size_metrics["cases"]
        if case["false_positive"] or case["false_negative"]
    ]
    lines.extend(
        [
            "",
            "## 해석",
            "",
            "- 이 검증은 실제 판매 데이터 전체 성능이 아니라, size_info 표기 패턴을 넓힌 합성 fixture 기준 검증이다.",
            "- source 입력에는 expected label이나 pattern_group을 넣지 않고, pattern_group은 `case_metadata.json`에만 보존했다.",
            "- actual은 expected fixture가 없는 격리 workspace에서 실제 Codex CLI로 생성한다.",
            "- `recommendation_noise` 그룹은 구매자 만족도, 개인화 추천, 후기 요약처럼 정적 상품 사이즈가 아닌 문구가 size_info로 들어가지 않는지 확인한다.",
            "",
            "## 실패 사례",
            "",
        ]
    )
    if failed_cases:
        for case in failed_cases:
            lines.append(
                f"- `{case['product_id']}` ({case['pattern_group']}): FP={case['false_positive']}, FN={case['false_negative']}"
            )
    else:
        lines.append("- 없음")

    lines.extend(
        [
            "",
            "## 실행 명령",
            "",
        ]
    )
    for command in result["commands"]:
        lines.append(f"- `{command['id']}`: `{' '.join(command['argv'])}` -> exit `{command['exit_code']}`")

    lines.extend(
        [
            "",
            "## 재현 방법",
            "",
            "```powershell",
            "python tools\\generate_size_info_pattern_fixtures.py",
            "python tools\\run_full_page_codex_smoke20_cli.py --fixture size_info_patterns --timeout 3600",
            "python tools\\run_size_info_pattern_validation.py",
            "```",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    sources = load_json(FIXTURE_DIR / "source_inputs.json")
    expected = load_json(FIXTURE_DIR / "expected_products.json")
    actual = load_json(FIXTURE_DIR / "actual_products.json")
    metadata = load_json(FIXTURE_DIR / "case_metadata.json")
    actual_metadata = load_json(FIXTURE_DIR / "actual_metadata.json") if (FIXTURE_DIR / "actual_metadata.json").exists() else {}

    commands = [
        {
            "id": "expected_schema",
            "argv": [
                sys.executable,
                "src/skills/product-agentizer/scripts/validate.py",
                "tests/fixtures/size_info_patterns/expected_products.json",
            ],
            "result": run_validate(FIXTURE_DIR / "expected_products.json"),
        },
        {
            "id": "actual_schema",
            "argv": [
                sys.executable,
                "src/skills/product-agentizer/scripts/validate.py",
                "tests/fixtures/size_info_patterns/actual_products.json",
            ],
            "result": run_validate(FIXTURE_DIR / "actual_products.json"),
        },
    ]
    size_info_metrics = evaluate_size_info(expected, actual, metadata)
    source_check = synthetic_source_check(sources)
    hashes = {
        target: sha256(ROOT / target)
        for target in HASH_TARGETS
        if (ROOT / target).exists()
    }
    codex_version = subprocess.run(
        ["codex", "--version"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    generated_at_utc = datetime.now(timezone.utc)
    micro = size_info_metrics["micro"]
    expected_schema = commands[0]["result"]
    actual_schema = commands[1]["result"]
    passed = (
        expected_schema["valid"]
        and actual_schema["valid"]
        and isinstance(micro["precision"], float)
        and micro["precision"] >= 0.95
        and isinstance(micro["recall"], float)
        and micro["recall"] >= 0.95
        and size_info_metrics["noise_false_positive_count"] == 0
        and source_check["non_synthetic_url_count"] == 0
        and source_check["non_synthetic_method_count"] == 0
    )
    result = {
        "generated_at_utc": generated_at_utc.isoformat(),
        "generated_for_kst_date": generated_at_utc.astimezone(KST).date().isoformat(),
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "codex_version": codex_version.stdout.strip(),
        },
        "commands": [
            {**command["result"], "id": command["id"], "argv": command["argv"], "exit_code": command["result"]["exit_code"]}
            for command in commands
        ],
        "source_check": source_check,
        "size_info_metrics": size_info_metrics,
        "hashes_sha256": hashes,
        "acceptance_summary": {
            "passed": passed,
            "actual_mode": actual_metadata.get("actual_mode", "unknown"),
            "actual_generated_at_utc": actual_metadata.get("generated_at_utc"),
            "expected_schema_valid": expected_schema["valid"],
            "actual_schema_valid": actual_schema["valid"],
            "actual_checked": actual_schema["checked"],
            "size_info_precision": micro["precision"],
            "size_info_recall": micro["recall"],
            "size_info_true_positive": micro["true_positive"],
            "size_info_false_positive": micro["false_positive"],
            "size_info_false_negative": micro["false_negative"],
            "noise_false_positive_count": size_info_metrics["noise_false_positive_count"],
            "auto_fetch_count": source_check["auto_fetch_count"],
            "real_page_copy_count": source_check["real_page_copy_count"],
            "legal_compliance_judgment_count": source_check["legal_compliance_judgment_count"],
        },
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(result)
    print(
        json.dumps(
            {
                "result_path": str(RESULT_PATH),
                "report_path": str(REPORT_PATH),
                "passed": passed,
                "size_info_precision": micro["precision"],
                "size_info_recall": micro["recall"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
