# AX해커톤 예선 · 2차 제출물 (무신사 문제 2)

> Jocoding AX해커톤 예선 과제 — 참여 기업의 공개·검증 가능한 문제를 해결하는 Codex 플러그인을 제출한다. 카카오페이증권 제출을 마쳤고, 이 작업 공간은 **무신사 상품 데이터 에이전트화 변환기** 제출물을 준비하기 위한 것이다.

## 개요
- 확정 기업·문제: **무신사 / 문제 2 · 상품 데이터 에이전트화 변환기**
- 목적: 상품 상세페이지의 비정형 텍스트를 에이전트가 질의 가능한 구조화 상품 데이터로 변환하는 Codex 플러그인 제작
- 주요 사용자: 해커톤 심사위원/주최측
- 최종 산출물: `submission.zip` (`src/` 플러그인 코드 + 루트 `README.md` + 루트 `logs/`) + 질문 5문항 답변
- 현재 상태: 주제 확정, 구현 계약·계획 문서 갱신, taxonomy/schema, `SKILL.md`, manifest, 검증·중복감지 스크립트, S5 더미 픽스처 정량 검증 작성 완료. Codex CLI 실제 설치·시연은 아직 전이다.

## 실행 방법
검증 스크립트는 로컬에서 실행 가능하다. `validate.py`는 `jsonschema`가 필요하므로, 새 환경에서는 `python -m pip install jsonschema`로 설치한 뒤 실행한다. Codex 플러그인 설치·실행 방법은 로컬 Codex CLI 시연 후 최종 제출용 내용으로 갱신한다.

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\dedup.py tests\fixtures\dedup\sample_products.json --pretty
python tests\evaluate_product_agentizer.py --pretty
```

## 프로젝트 구조
- `src/` 실제 제출될 Codex 플러그인 코드 (`.codex-plugin/plugin.json`, `skills/` 등) — `submission.zip`에 포함
- `logs/` AI 대화 로그 (claude-code, codex) — `submission.zip`에 원본 그대로 포함
- `docs/` 기획·리서치·근거·검증 등 내부 문서 (제출물 아님)
  - `docs/과제.md` 해커톤 과제 원문
  - `docs/requirements-contract.md` 무신사 에이전트화 변환기 기준 계약
  - `docs/project-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`
  - `docs/company-selection.md` 기업 선정 기준·확정 기록
  - `docs/company-research_references/` 기업 조사·검증 근거
  - `docs/technical_references/` Codex 플러그인 공식 문서 사본
- `tools/` 개발 보조 스크립트 (예: `save_log.py` — 로그 자동 저장 훅)
- `tests/` 플러그인 검증용 더미 픽스처와 테스트 스크립트
- `out/` 로컬 실행 결과·임시 산출물 (Git 제외)

## 문서
- 작업 규칙: `CLAUDE.md`, `AGENTS.md`
- 작업 이력: `Worklog.md`
- 주요 결정: `Decisionlog.md`
- 문제 해결: `Troubleshootinglog.md`

> 주의: 이 README는 아직 최종 제출용이 아니다. 플러그인 구현과 검증이 끝나면 실제 기능·설치·실행 방법만 남기도록 교체한다.
