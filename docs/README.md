# docs — 내부 작업 문서 안내

이 폴더는 AX해커톤 예선 2차 제출물 제작을 위한 내부 기획·근거·검증 문서 모음입니다. 최종 제출물에는 루트 `README.md`, `src/`, `logs/`가 들어가며, `docs/` 자체는 제출 대상이 아닙니다.

## 현재 작업 기준
- 확정 기업·문제: **무신사 / 문제 2 · 상품 데이터 에이전트화 변환기**
- 활성 구현 기준: `requirements-contract.md`, `implementation-plan.md`, `validation-plan.md`
- 입력 정책: 사용자가 붙여넣은 BYO 상품 상세 텍스트만 실행 입력으로 사용합니다. URL은 출처 메타데이터이며 자동 크롤링 입력이 아닙니다.

## 활성 문서
| 문서 | 역할 | 언제 보는가 |
|---|---|---|
| `과제.md` | 해커톤 과제 원문 | 제출 구조·실격 조건·질문 5문항 확인 |
| `project-plan.md` | 프로젝트 전체 기획 | 목표, 범위, 산출물, 리스크 확인 |
| `requirements-contract.md` | 구현 기준 계약 | 입력·출력 JSON, 지표, 오류·완료 기준 확인 |
| `implementation-plan.md` | 무신사 문제 2 단일 구현 계획 | 플러그인 구조, 다음 작업 순서, 완료 조건 확인 |
| `validation-plan.md` | 검증 계획 | 더미 픽스처, 안전성, 제출 구조 검증 기준 확인 |
| `full-page-dummy-validation-plan.md` | 실제 페이지형 합성 더미 검증 계획 | 정보 밀도별 합성 상세페이지 데이터셋과 S7.7 검증 기준 확인 |
| `size-info-coverage-plan.md` | size_info 표기 패턴 보강 검증 계획 | 실제 상품페이지에서 나올 법한 사이즈 표기 유형을 합성 fixture로 확장할 때 확인 |
| `size-info-schema-change-plan.md` | size_info schema 변경 조건부 계획 | SKILL-only 개선이 부족하거나 typed size query가 필요해질 때 재검토 |
| `product-agentizer-complete-guide.md` | 구현 전체 상세 설명서 | 전체 구조, 세부 기능, 작동 방식, 지표 의미를 한 번에 이해할 때 확인 |
| `submission-questions.md` | 제출 질문 5문항 답변 초안 | 제출 폼 답변을 복사·검토할 때 확인 |
| `company-selection.md` | 기업 선정 기준·최종 확정 기록 | 왜 무신사 문제 2를 골랐는지 추적 |

## 근거·참조 폴더
| 폴더 | 역할 | 주의 |
|---|---|---|
| `company-research_references/` | 기업 조사·팩트체크·최종 선정 근거 | 구현 기준은 아니지만 선정 사유와 공개 근거 추적에 필요 |
| `reports/` | 단계별 검증·실행 결과 보고서 | S5/S6/S7.5 결과와 재현성 스냅샷 확인 |
| `post-submission/` | 제출 후 감사·회고·정리 자료 | 현재 구현 기준이 아니라 제출 전후 맥락을 보존하는 용도로 확인. 전체 구조 보드는 `post-submission/file-structure-board.html` |
| `technical_references/` | Codex 플러그인·Skill·Hooks·AGENTS 공식 문서 사본 | 구현 중 규격 확인용. 필요한 문서만 열어본다 |
| `archive/` | 폐기·비활성 자료 보관 | 현재 구현 기준으로 쓰지 않는다. 감사 추적용으로만 확인 |

## 구현 단계에서 주로 볼 순서
1. `requirements-contract.md`로 입력·출력·오류 기준 확인
2. `implementation-plan.md`로 플러그인 구조와 현재 단계 확인
3. `validation-plan.md`로 테스트와 안전성 기준 확인
4. 필요한 경우 `technical_references/Build_plugins.md`와 `technical_references/Agent_Skills.md`로 Codex 규격 확인

## 아카이브 정책
- 현재 구현에 직접 필요하지 않은 선정 전 후보 비교·폐기 자료는 `archive/`로 옮깁니다.
- 아카이브 파일은 삭제하지 않고, `archive/README.md`에 폐기·비활성화 사유를 기록합니다.
- 아카이브 자료를 다시 활성 기준으로 되살릴 때는 `Decisionlog.md`에 이유를 남기고 관련 문서 참조를 갱신합니다.

## 제출 후 정리 정책
- 제출 전후의 감사 프롬프트, 회고, 최종 점검 메모처럼 현재 구현 기준이 아닌 문서는 `post-submission/`에 보관합니다.
- `out/`은 Git 제외 임시 영역이므로 제출 완료 후에는 최종 제출 zip만 남기고 staging, audit, 캐시성 실행물은 제거할 수 있습니다.
- `logs/`는 원본 보존 대상이므로 정리 과정에서도 내용 편집·발췌·삭제를 하지 않습니다.
