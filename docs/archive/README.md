# docs/archive — 폐기·비활성 자료 보관소

이 폴더의 자료는 **더 이상 활성 구현 기준으로 사용하지 않는 폐기·비활성 자료**입니다. 감사 추적(왜 폐기·비활성화했는지 검증 가능하도록)을 위해 삭제하지 않고 원본을 보관합니다.

## 보관 기준
- **폐기**: 환각·오류·출처 문제 등으로 근거로 사용하지 않는 자료.
- **비활성**: 당시 판단 과정에는 필요했지만, 현재 확정된 무신사 문제 2 구현에는 직접 필요하지 않은 자료.

## company-research-report_gemini_DISCARDED.md
- **폐기일**: 2026-07-04
- **폐기 사유**: 공개자료 팩트체크(4단계 서브에이전트 검토, `docs/company-research_references/company-research-review-report.md`) 결과, 5개 기업 전체에서 반복적인 환각·출처 왜곡·무출처 수치·시점 오도가 확인되어 신뢰성이 극도로 낮다고 판단됨.
- **대표 문제**: 실재하지 않는 파트너 발언 인용(삼일PwC), 무출처 "비전 LLM 99% 인식률"·"최대 200% 배상 페널티"(무신사·마이리얼트립), 2023년 시정 완료 사안을 현재 위기로 오도(마이리얼트립), 모든 출처의 확인일이 기계적으로 동일(2026-03-17).
- **후속**: 최종 근거는 `docs/company-research_references/company-research-report_codex.md`(검증 통과)와 서브에이전트 독립 조사를 종합한 `docs/company-research_references/company-research-final-report.md`를 사용함.

## plugin-directions_PRE_SELECTION.md
- **비활성화일**: 2026-07-04
- **비활성화 사유**: 무신사 문제 2 `상품 데이터 에이전트화 변환기`가 공식 확정되어, 후보 3사·여러 문제 방향 비교 문서는 더 이상 활성 구현 기준이 아님.
- **보존 이유**: 후보 방향 축소, 법적 안전성 기준, 무신사 문제 1/2 비교, 최종 선택 전 판단 흐름을 추적하기 위함.
- **후속**: 현재 구현 기준은 `docs/requirements-contract.md`, `docs/musinsa-agentizer-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`를 사용함.
