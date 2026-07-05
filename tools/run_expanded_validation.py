#!/usr/bin/env python3
"""Run expanded validation and preserve a reproducible results snapshot."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "docs" / "reports" / "s7-expanded-validation-results.json"
KST = timezone(timedelta(hours=9))


COMMANDS: list[dict[str, Any]] = [
    {
        "id": "expanded_expected_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/expanded_dummy/expected_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "expanded_selfcheck_eval",
        "argv": [
            sys.executable,
            "tests/evaluate_product_agentizer.py",
            "--inputs",
            "tests/fixtures/expanded_dummy/source_inputs.json",
            "--expected",
            "tests/fixtures/expanded_dummy/expected_products.json",
            "--actual",
            "tests/fixtures/expanded_dummy/reference_actual_products.json",
            "--dedup-labels",
            "tests/fixtures/expanded_dummy/duplicate_labels.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "codex_subset_actual_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/codex_subset/actual_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "codex_subset_eval",
        "argv": [
            sys.executable,
            "tests/evaluate_product_agentizer.py",
            "--inputs",
            "tests/fixtures/codex_subset/source_inputs.json",
            "--expected",
            "tests/fixtures/codex_subset/expected_products.json",
            "--actual",
            "tests/fixtures/codex_subset/actual_products.json",
            "--dedup-labels",
            "tests/fixtures/codex_subset/duplicate_labels.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "real_sanity_actual_schema",
        "argv": [
            sys.executable,
            "src/skills/product-agentizer/scripts/validate.py",
            "tests/fixtures/real_sanity/actual_products.json",
        ],
        "expect_exit_codes": [0],
    },
    {
        "id": "real_sanity_eval_exploratory",
        "argv": [
            sys.executable,
            "tests/evaluate_product_agentizer.py",
            "--inputs",
            "tests/fixtures/real_sanity/source_inputs.json",
            "--expected",
            "tests/fixtures/real_sanity/expected_products.json",
            "--actual",
            "tests/fixtures/real_sanity/actual_products.json",
            "--dedup-labels",
            "tests/fixtures/real_sanity/duplicate_labels.json",
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
    "tools/generate_expanded_validation_fixtures.py",
    "tools/run_expanded_validation.py",
    "tests/fixtures/expanded_dummy/source_inputs.json",
    "tests/fixtures/expanded_dummy/expected_products.json",
    "tests/fixtures/expanded_dummy/reference_actual_products.json",
    "tests/fixtures/expanded_dummy/duplicate_labels.json",
    "tests/fixtures/codex_subset/source_inputs.json",
    "tests/fixtures/codex_subset/expected_products.json",
    "tests/fixtures/codex_subset/actual_products.json",
    "tests/fixtures/codex_subset/duplicate_labels.json",
    "tests/fixtures/codex_subset/prompt.md",
    "tests/fixtures/codex_subset/prompt_template.md",
    "tests/fixtures/real_sanity/source_inputs.json",
    "tests/fixtures/real_sanity/expected_products.json",
    "tests/fixtures/real_sanity/actual_products.json",
    "tests/fixtures/real_sanity/duplicate_labels.json",
    "tests/fixtures/real_sanity/prompt.md",
    "tests/fixtures/real_sanity/prompt_template.md",
]


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
    parsed = parse_json(process.stdout)
    return {
        "id": command["id"],
        "argv": command["argv"],
        "exit_code": process.returncode,
        "expected_exit_codes": command["expect_exit_codes"],
        "passed": process.returncode in command["expect_exit_codes"],
        "stdout_json": parsed,
        "stdout_len": len(process.stdout),
        "stderr": process.stderr.strip(),
    }


def cross_category_high_confidence() -> dict[str, Any]:
    import importlib.util

    dedup_path = ROOT / "src" / "skills" / "product-agentizer" / "scripts" / "dedup.py"
    spec = importlib.util.spec_from_file_location("product_agentizer_dedup", dedup_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {dedup_path}")
    dedup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dedup)

    payload = json.loads((ROOT / "tests" / "fixtures" / "expanded_dummy" / "expected_products.json").read_text(encoding="utf-8"))
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


def main() -> int:
    commands = [run_command(command) for command in COMMANDS]
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
        "hashes_sha256": hashes,
        "commands": commands,
        "dedup_cross_category_check": cross_category_high_confidence(),
        "acceptance_summary": {
            "expanded_expected_schema_valid": commands[0]["passed"],
            "codex_subset_schema_valid": commands[2]["passed"],
            "real_sanity_schema_valid": commands[4]["passed"],
            "all_commands_passed": all(command["passed"] for command in commands),
        },
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result_path": str(RESULT_PATH), "all_commands_passed": result["acceptance_summary"]["all_commands_passed"]}, ensure_ascii=False))
    return 0 if result["acceptance_summary"]["all_commands_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
