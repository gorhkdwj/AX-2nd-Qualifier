# AX해커톤 예선 · 2차 제출물 (기업 선정 전)

> Jocoding AX해커톤 예선 과제 — 참여 기업의 공개·검증 가능한 문제를 해결하는 Codex 플러그인을 제출한다. 카카오페이증권 제출을 마쳤고, 이 작업 공간은 **추가로 도전할 기업 1곳을 선정하고 그 플러그인을 준비**하기 위한 것이다.

## 개요
- 목적: `docs/과제.md` 과제 수행 (기업의 공개·검증 가능한 문제 → Codex 플러그인)
- 주요 사용자: 해커톤 심사위원/주최측
- 최종 산출물: `submission.zip` (`src/` 플러그인 코드 + 루트 `README.md` + 루트 `logs/`) + 질문 5문항 답변
- 현재 상태: **기업 미선정** — `docs/company-selection.md` 기준으로 후보 5곳(채널톡, 메디테라피, 무신사, 삼일PwC, 마이리얼트립) 중 1곳 조사·선정 진행 중

## 실행 방법
(아직 실행 가능한 플러그인 코드가 없다. 기업 선정과 플러그인 설계가 끝난 뒤 이 항목을 갱신한다.)

## 프로젝트 구조
- `src/` 실제 제출될 Codex 플러그인 코드 (`.codex-plugin/plugin.json` 등) — submission.zip에 포함
- `logs/` AI 대화 로그 (claude-code, codex) — submission.zip에 원본 그대로 포함
- `docs/` 기획·리서치·근거·검증 등 내부 문서 (제출물 아님)
  - `docs/과제.md` 해커톤 과제 원문
  - `docs/technical_references/` Codex 플러그인 공식 문서 사본(Plugins, Build_plugins, Agent_Skills) — 이미 준비되어 있음
  - `docs/company-selection.md` 기업 선정 기준·후보 비교
  - `docs/project-plan.md`, `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`
- `tools/` 개발 보조 스크립트 (예: `save_log.py` — 로그 자동 저장 훅)
- `tests/` 플러그인 검증용 (필요 시 사용)
- `out/` 로컬 실행 결과·임시 산출물 (Git 제외)

## 문서
- 작업 규칙: `CLAUDE.md`
- 작업 이력: `Worklog.md`
- 주요 결정: `Decisionlog.md`
- 문제 해결: `Troubleshootinglog.md`

> 주의: 이 README는 아직 최종 제출용이 아니다. 기업 선정 → 플러그인 구현이 끝나면 실제 기능 설명으로 교체한다.
