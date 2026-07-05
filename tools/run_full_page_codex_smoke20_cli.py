#!/usr/bin/env python3
"""Run Codex CLI for the S7.7 20-case smoke subset and save actual JSON."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SMOKE_DIR = ROOT / "tests" / "fixtures" / "full_page_codex_smoke20"
OUT_DIR = ROOT / "out"
RUN_ROOT = OUT_DIR / "full_page_codex_smoke20_workspace"
PROMPT_PATH = SMOKE_DIR / "prompt.md"
ACTUAL_PATH = SMOKE_DIR / "actual_products.json"
METADATA_PATH = SMOKE_DIR / "actual_metadata.json"
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


def prepare_workspace() -> None:
    out_root = OUT_DIR.resolve()
    run_root = RUN_ROOT.resolve()
    if out_root not in run_root.parents:
        raise RuntimeError(f"refusing to prepare workspace outside out/: {run_root}")
    if RUN_ROOT.exists():
        shutil.rmtree(RUN_ROOT)
    (RUN_ROOT / "src" / "skills" / "product-agentizer" / "references").mkdir(parents=True, exist_ok=True)
    source_skill = ROOT / "src" / "skills" / "product-agentizer" / "SKILL.md"
    source_refs = ROOT / "src" / "skills" / "product-agentizer" / "references"
    shutil.copy2(source_skill, RUN_ROOT / "src" / "skills" / "product-agentizer" / "SKILL.md")
    for name in ("schema.json", "taxonomy.json"):
        shutil.copy2(source_refs / name, RUN_ROOT / "src" / "skills" / "product-agentizer" / "references" / name)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prepare_workspace()
    prompt = (
        "Blind validation rule: the current workspace intentionally contains only the skill and reference files, "
        "not expected or actual fixture labels. Do not use any tests/fixtures files or hidden answer files.\n\n"
        + PROMPT_PATH.read_text(encoding="utf-8")
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
        cwd=RUN_ROOT,
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=1200,
    )
    raw_response_path = RUN_ROOT / RAW_RESPONSE_FILENAME
    raw_response = raw_response_path.read_text(encoding="utf-8") if raw_response_path.exists() else process.stdout
    metadata = {
        "actual_mode": "codex_cli_actual",
        "execution_mode": "isolated_workspace_without_expected_fixtures",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "command": argv,
        "exit_code": process.returncode,
        "prompt_path": str(PROMPT_PATH.relative_to(ROOT)),
        "workspace_path": str(RUN_ROOT.relative_to(ROOT)),
        "raw_response_path": str(raw_response_path.relative_to(ROOT)),
        "stdout_len": len(process.stdout),
        "stderr_len": len(process.stderr),
        "stderr_warning_preview": process.stderr.strip().splitlines()[:20],
    }

    if process.returncode != 0:
        METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
        METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"ok": False, "parse_error": str(exc)}, ensure_ascii=False))
        return 1

    ACTUAL_PATH.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    METADATA_PATH.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "actual_path": str(ACTUAL_PATH), "metadata_path": str(METADATA_PATH)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
