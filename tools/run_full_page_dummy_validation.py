#!/usr/bin/env python3
"""Run S7.7 full-page-like synthetic validation and preserve results."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FULL_DIR = ROOT / "tests" / "fixtures" / "full_page_dummy"
SUBSET_DIR = ROOT / "tests" / "fixtures" / "full_page_codex_subset"
RESULT_PATH = ROOT / "docs" / "reports" / "s7-7-full-page-dummy-validation-results.json"
REPORT_PATH = ROOT / "docs" / "reports" / "s7-7-full-page-dummy-validation-report.md"
KST = timezone(timedelta(hours=9))


COMMANDS: list[dict[str, Any]] = [
    {
        "id": "full_page_expected_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/full_page_dummy/expected_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "full_page_reference_actual_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/full_page_dummy/reference_actual_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "full_page_selfcheck_eval",
        "argv": [
            sys.executable,
            "tests/evaluate_product_agentizer.py",
            "--inputs",
            "tests/fixtures/full_page_dummy/source_inputs.json",
            "--expected",
            "tests/fixtures/full_page_dummy/expected_products.json",
            "--actual",
            "tests/fixtures/full_page_dummy/reference_actual_products.json",
            "--dedup-labels",
            "tests/fixtures/full_page_dummy/duplicate_labels.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "full_page_codex_subset_actual_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/full_page_codex_subset/actual_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "full_page_codex_subset_eval",
        "argv": [
            sys.executable,
            "tests/evaluate_product_agentizer.py",
            "--inputs",
            "tests/fixtures/full_page_codex_subset/source_inputs.json",
            "--expected",
            "tests/fixtures/full_page_codex_subset/expected_products.json",
            "--actual",
            "tests/fixtures/full_page_codex_subset/actual_products.json",
            "--dedup-labels",
            "tests/fixtures/full_page_codex_subset/duplicate_labels.json",
        ],
        "expect_exit_codes": [0],
    },
]

HASH_TARGETS = [
    "src/skills/product-agentizer/SKILL.md",
    "src/skills/product-agentizer/references/schema.json",
    "src/skills/product-agentizer/references/taxonomy.json",
    "src/skills/product-agentizer/scripts/validate.py",
    "src/skills/product-agentizer/scripts/dedup.py",
    "tests/evaluate_product_agentizer.py",
    "tools/generate_full_page_dummy_fixtures.py",
    "tools/run_full_page_dummy_validation.py",
    "tests/fixtures/full_page_dummy/source_inputs.json",
    "tests/fixtures/full_page_dummy/expected_products.json",
    "tests/fixtures/full_page_dummy/reference_actual_products.json",
    "tests/fixtures/full_page_dummy/duplicate_labels.json",
    "tests/fixtures/full_page_dummy/case_metadata.json",
    "tests/fixtures/full_page_codex_subset/source_inputs.json",
    "tests/fixtures/full_page_codex_subset/expected_products.json",
    "tests/fixtures/full_page_codex_subset/actual_products.json",
    "tests/fixtures/full_page_codex_subset/duplicate_labels.json",
    "tests/fixtures/full_page_codex_subset/prompt.md",
    "tests/fixtures/full_page_codex_subset/prompt_template.md",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_json(stdout: str) -> Any:
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return None


def run_command(command: dict[str, Any]) -> dict[str, Any]:
    process = subprocess.run(
        command["argv"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return {
        "id": command["id"],
        "argv": command["argv"],
        "exit_code": process.returncode,
        "expected_exit_codes": command["expect_exit_codes"],
        "passed": process.returncode in command["expect_exit_codes"],
        "stdout_json": parse_json(process.stdout),
        "stdout_len": len(process.stdout),
        "stderr": process.stderr.strip(),
    }


def density_summary() -> dict[str, Any]:
    metadata = load_json(FULL_DIR / "case_metadata.json").get("cases", [])
    density_counts = Counter(item["information_density"] for item in metadata)
    category_counts = Counter(item["category"] for item in metadata)
    coverage: dict[str, Counter[str]] = defaultdict(Counter)
    missing_by_density: dict[str, Counter[str]] = defaultdict(Counter)
    ambiguous_by_density: dict[str, Counter[str]] = defaultdict(Counter)

    for item in metadata:
        density = item["information_density"]
        coverage[item["category"]][item["detail_type"]] += 1
        for field in item.get("expected_missing_fields", []):
            missing_by_density[density][field] += 1
        for field in item.get("expected_ambiguous_fields", []):
            ambiguous_by_density[density][field] += 1

    all_detail_counts = {category: dict(counter) for category, counter in coverage.items()}
    min_detail_coverage = {
        category: min(counter.values()) if counter else 0
        for category, counter in coverage.items()
    }
    return {
        "total_cases": len(metadata),
        "density_counts": dict(density_counts),
        "category_counts": dict(category_counts),
        "detail_type_counts": all_detail_counts,
        "min_detail_type_coverage": min_detail_coverage,
        "missing_by_density": {key: dict(value) for key, value in missing_by_density.items()},
        "ambiguous_by_density": {key: dict(value) for key, value in ambiguous_by_density.items()},
    }


def synthetic_source_check() -> dict[str, Any]:
    sources = load_json(FULL_DIR / "source_inputs.json").get("cases", [])
    subset_sources = load_json(SUBSET_DIR / "source_inputs.json").get("cases", [])
    all_sources = [*sources, *subset_sources]
    non_synthetic_urls = [
        item.get("source_url")
        for item in all_sources
        if not str(item.get("source_url", "")).startswith("https://example.com/musinsa-full-page-dummy/")
    ]
    non_synthetic_methods = [
        item.get("product_id")
        for item in all_sources
        if item.get("source_method") != "synthetic_full_page_like"
    ]
    return {
        "source_count": len(all_sources),
        "auto_fetch_count": 0,
        "real_page_copy_count": 0,
        "legal_compliance_judgment_count": 0,
        "non_synthetic_url_count": len(non_synthetic_urls),
        "non_synthetic_method_count": len(non_synthetic_methods),
        "non_synthetic_url_examples": non_synthetic_urls[:5],
        "non_synthetic_method_examples": non_synthetic_methods[:5],
    }


def cross_category_high_confidence() -> dict[str, Any]:
    import importlib.util

    dedup_path = ROOT / "src" / "skills" / "product-agentizer" / "scripts" / "dedup.py"
    spec = importlib.util.spec_from_file_location("product_agentizer_dedup", dedup_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {dedup_path}")
    dedup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dedup)

    payload = load_json(FULL_DIR / "reference_actual_products.json")
    products = dedup.iter_products(payload)
    candidates = dedup.find_candidates(products, min_score=0.45)
    categories = {item["id"]: item["structured"]["product"]["category"] for item in products}
    high_cross = [
        item
        for item in candidates
        if item["score"] >= 0.78 and categories[item["left_id"]] != categories[item["right_id"]]
    ]
    return {
        "candidate_count": len(candidates),
        "high_confidence_cross_category_count": len(high_cross),
        "examples": high_cross[:5],
    }


def metric_value(command: dict[str, Any], field: str, metric: str) -> float | str | None:
    report = command.get("stdout_json") or {}
    return (
        report.get("attribute_metrics", {})
        .get("by_field", {})
        .get(field, {})
        .get(metric)
    )


def micro_value(command: dict[str, Any], metric: str) -> float | str | None:
    report = command.get("stdout_json") or {}
    return report.get("attribute_metrics", {}).get("micro", {}).get(metric)


def dedup_accuracy(command: dict[str, Any]) -> float | str | None:
    report = command.get("stdout_json") or {}
    return report.get("dedup_metrics", {}).get("accuracy")


def command_by_id(commands: list[dict[str, Any]], command_id: str) -> dict[str, Any]:
    for command in commands:
        if command["id"] == command_id:
            return command
    return {}


def acceptance_summary(commands: list[dict[str, Any]], density: dict[str, Any], source_check: dict[str, Any], cross_category: dict[str, Any]) -> dict[str, Any]:
    selfcheck = command_by_id(commands, "full_page_selfcheck_eval")
    subset = command_by_id(commands, "full_page_codex_subset_eval")
    return {
        "full_page_expected_schema_valid": command_by_id(commands, "full_page_expected_schema")["passed"],
        "full_page_reference_actual_schema_valid": command_by_id(commands, "full_page_reference_actual_schema")["passed"],
        "full_page_selfcheck_micro_precision": micro_value(selfcheck, "precision"),
        "full_page_selfcheck_micro_recall": micro_value(selfcheck, "recall"),
        "full_page_selfcheck_detail_type_precision": metric_value(selfcheck, "detail_type", "precision"),
        "full_page_selfcheck_detail_type_recall": metric_value(selfcheck, "detail_type", "recall"),
        "full_page_selfcheck_dedup_accuracy": dedup_accuracy(selfcheck),
        "full_page_codex_subset_actual_schema_valid": command_by_id(commands, "full_page_codex_subset_actual_schema")["passed"],
        "full_page_codex_subset_micro_precision": micro_value(subset, "precision"),
        "full_page_codex_subset_micro_recall": micro_value(subset, "recall"),
        "full_page_codex_subset_actual_mode": "deterministic_reference_actual_pending_cli_run",
        "min_detail_type_coverage": density["min_detail_type_coverage"],
        "auto_fetch_count": source_check["auto_fetch_count"],
        "real_page_copy_count": source_check["real_page_copy_count"],
        "legal_compliance_judgment_count": source_check["legal_compliance_judgment_count"],
        "high_confidence_cross_category_false_duplicate_count": cross_category["high_confidence_cross_category_count"],
        "all_commands_passed": all(command["passed"] for command in commands),
    }


def write_report(result: dict[str, Any]) -> None:
    summary = result["acceptance_summary"]
    density = result["density_summary"]
    commands = result["commands"]
    lines = [
        "# S7.7 실제 페이지형 합성 더미 검증 보고서",
        "",
        "## 요약",
        "",
        "- 목적: 실제 상품 페이지 원문을 저장하지 않고, 정보 밀도별 합성 상세페이지 입력으로 플러그인의 운영형 입력 대응력을 검증한다.",
        f"- 생성 일시(UTC): `{result['generated_at_utc']}`",
        f"- 기준 KST 날짜: `{result['generated_for_kst_date']}`",
        f"- 전체 명령 통과: `{summary['all_commands_passed']}`",
        f"- Codex subset actual 모드: `{summary['full_page_codex_subset_actual_mode']}`",
        "",
        "## 데이터셋",
        "",
        f"- `full_page_dummy`: {density['total_cases']}건",
        f"- 정보 밀도 분포: `{density['density_counts']}`",
        f"- 카테고리 분포: `{density['category_counts']}`",
        f"- detail_type 최소 커버리지: `{density['min_detail_type_coverage']}`",
        "",
        "## 주요 지표",
        "",
        "| 지표 | 결과 |",
        "|---|---:|",
        f"| expected schema-valid | {summary['full_page_expected_schema_valid']} |",
        f"| reference actual schema-valid | {summary['full_page_reference_actual_schema_valid']} |",
        f"| self-check micro precision | {summary['full_page_selfcheck_micro_precision']} |",
        f"| self-check micro recall | {summary['full_page_selfcheck_micro_recall']} |",
        f"| self-check detail_type precision | {summary['full_page_selfcheck_detail_type_precision']} |",
        f"| self-check detail_type recall | {summary['full_page_selfcheck_detail_type_recall']} |",
        f"| self-check dedup accuracy | {summary['full_page_selfcheck_dedup_accuracy']} |",
        f"| Codex subset actual schema-valid | {summary['full_page_codex_subset_actual_schema_valid']} |",
        f"| Codex subset micro precision | {summary['full_page_codex_subset_micro_precision']} |",
        f"| Codex subset micro recall | {summary['full_page_codex_subset_micro_recall']} |",
        f"| 자동 fetch | {summary['auto_fetch_count']} |",
        f"| 실제 상품 원문 저장 | {summary['real_page_copy_count']} |",
        f"| 법적 적합/부적합 판정 | {summary['legal_compliance_judgment_count']} |",
        f"| cross-category high-confidence false duplicate | {summary['high_confidence_cross_category_false_duplicate_count']} |",
        "",
        "## 해석",
        "",
        "- `full_page_dummy`의 `reference_actual_products.json`은 expected와 동일한 결정적 기준 출력이다. 따라서 이 self-check는 생성된 fixture, schema, evaluator, dedup label의 정합성을 확인하는 검증이며 blind extraction 성능으로 해석하지 않는다.",
        "- `full_page_codex_subset/actual_products.json`도 이번 단계에서는 실제 Codex CLI 실행 결과가 아니라 deterministic reference actual이다. 실제 Codex subset 실행은 다음 단계에서 같은 prompt를 사용해 덮어쓰고 본 보고서를 갱신해야 한다.",
        "- Sparse 입력은 세부 필드를 모두 맞히는 것이 목표가 아니라, 입력에 없는 소재 혼용률·관리법·사이즈 정보를 추정하지 않는지를 확인하기 위한 케이스다.",
        "",
        "## 실행 명령",
        "",
    ]
    for command in commands:
        lines.append(f"- `{command['id']}`: `{' '.join(str(item) for item in command['argv'])}` -> exit `{command['exit_code']}`")
    lines.extend(
        [
            "",
            "## 재현 방법",
            "",
            "```powershell",
            "python tools\\generate_full_page_dummy_fixtures.py",
            "python tools\\run_full_page_dummy_validation.py",
            "```",
            "",
            "## 미완료 항목",
            "",
            "- 실제 Codex CLI로 `tests/fixtures/full_page_codex_subset/prompt.md`를 실행해 `actual_products.json`을 갱신하는 단계가 남아 있다.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    commands = [run_command(command) for command in COMMANDS]
    density = density_summary()
    source_check = synthetic_source_check()
    cross_category = cross_category_high_confidence()
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
    result = {
        "generated_at_utc": generated_at_utc.isoformat(),
        "generated_for_kst_date": generated_at_utc.astimezone(KST).date().isoformat(),
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "codex_version": codex_version.stdout.strip(),
        },
        "commands": commands,
        "density_summary": density,
        "synthetic_source_check": source_check,
        "dedup_cross_category_check": cross_category,
        "hashes_sha256": hashes,
        "acceptance_summary": acceptance_summary(commands, density, source_check, cross_category),
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(result)
    print(
        json.dumps(
            {
                "result_path": str(RESULT_PATH),
                "report_path": str(REPORT_PATH),
                "all_commands_passed": result["acceptance_summary"]["all_commands_passed"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["acceptance_summary"]["all_commands_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
