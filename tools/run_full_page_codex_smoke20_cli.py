#!/usr/bin/env python3
"""Run Codex CLI for a product-agentizer validation fixture and save actual JSON."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"
OUT_DIR = ROOT / "out"
RAW_RESPONSE_FILENAME = "codex_raw_response.txt"


def parse_json_response(text: str) -> Any:
    raw = text.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(raw[start : end + 1])


def prepare_workspace(run_root: Path) -> None:
    out_root = OUT_DIR.resolve()
    resolved_run_root = run_root.resolve()
    if out_root not in resolved_run_root.parents:
        raise RuntimeError(f"refusing to prepare workspace outside out/: {resolved_run_root}")
    if run_root.exists():
        shutil.rmtree(run_root)
    (run_root / "src" / "skills" / "product-agentizer" / "references").mkdir(parents=True, exist_ok=True)
    source_skill = ROOT / "src" / "skills" / "product-agentizer" / "SKILL.md"
    source_refs = ROOT / "src" / "skills" / "product-agentizer" / "references"
    shutil.copy2(source_skill, run_root / "src" / "skills" / "product-agentizer" / "SKILL.md")
    for name in ("schema.json", "taxonomy.json"):
        shutil.copy2(source_refs / name, run_root / "src" / "skills" / "product-agentizer" / "references" / name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Codex CLI for a validation fixture in an isolated workspace.")
    parser.add_argument(
        "--fixture",
        default="full_page_codex_smoke20",
        choices=["full_page_codex_smoke20", "full_page_codex_subset", "size_info_patterns"],
        help="Fixture directory under tests/fixtures.",
    )
    parser.add_argument("--timeout", type=int, default=1800, help="Codex CLI timeout in seconds.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    args = parse_args()
    fixture_dir = FIXTURE_ROOT / args.fixture
    prompt_path = fixture_dir / "prompt.md"
    actual_path = fixture_dir / "actual_products.json"
    metadata_path = fixture_dir / "actual_metadata.json"
    run_root = OUT_DIR / f"{args.fixture}_workspace"

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prepare_workspace(run_root)
    prompt = (
        "Blind validation rule: the current workspace intentionally contains only the skill and reference files, "
        "not expected or actual fixture labels. Do not use any tests/fixtures files or hidden answer files.\n\n"
        + prompt_path.read_text(encoding="utf-8")
    )
    argv = [
        "codex",
        "exec",
        "--ephemeral",
        "-C",
        ".",
        "--sandbox",
        "read-only",
        "-o",
        RAW_RESPONSE_FILENAME,
        "-",
    ]
    process = subprocess.run(
        argv,
        cwd=run_root,
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=args.timeout,
    )
    raw_response_path = run_root / RAW_RESPONSE_FILENAME
    raw_response = raw_response_path.read_text(encoding="utf-8") if raw_response_path.exists() else process.stdout
    metadata = {
        "actual_mode": "codex_cli_actual",
        "execution_mode": "isolated_workspace_without_expected_fixtures",
        "fixture": args.fixture,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": argv,
        "exit_code": process.returncode,
        "prompt_path": str(prompt_path.relative_to(ROOT)),
        "workspace_path": str(run_root.relative_to(ROOT)),
        "raw_response_path": str(raw_response_path.relative_to(ROOT)),
        "stdout_len": len(process.stdout),
        "stderr_len": len(process.stderr),
        "stderr_warning_preview": process.stderr.strip().splitlines()[:20],
    }

    if process.returncode != 0:
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(
            json.dumps(
                {"ok": False, "exit_code": process.returncode, "stderr_len": len(process.stderr)},
                ensure_ascii=False,
            )
        )
        return process.returncode

    try:
        actual = parse_json_response(raw_response)
    except json.JSONDecodeError as exc:
        metadata["parse_error"] = str(exc)
        metadata["raw_response_preview"] = raw_response[:2000]
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"ok": False, "parse_error": str(exc)}, ensure_ascii=False))
        return 1

    actual_path.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "actual_path": str(actual_path), "metadata_path": str(metadata_path)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
