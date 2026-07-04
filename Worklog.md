# Worklog · AX해커톤 예선 2차 제출(기업 미정)

주요 사용자 요청이 끝날 때마다 아래 형식으로 누적 기록한다. (규칙: CLAUDE.md / AGENTS.md 11절). 최신 항목을 위에 추가한다.

## 기록 형식
```
### W-00N · 작업 제목
**요청** / **수행 작업** / **변경 파일** / **검증** / **판단 근거** / **결과**
```

---

### W-003 · Codex용 AGENTS.md 구축 및 지침 동기화
**요청**
- `CLAUDE.md`를 확인하고 Codex가 그대로 활용할 수 있도록 `AGENTS.md`를 구축
- 양쪽 모두 변경사항이 있을 때 두 파일이 동기화되도록 하는 지침 추가

**수행 작업**
- `CLAUDE.md`를 읽고 프로젝트 작업 헌법 구조와 기존 규칙 확인
- `CLAUDE.md` 제목과 서문을 Claude/Codex 공용 지침으로 수정
- `0.1 에이전트 지침 파일 동기화` 절 추가
- 수정된 `CLAUDE.md`와 동일한 내용으로 `AGENTS.md` 생성
- 지침 변경 결정 내용을 `Decisionlog.md`에 기록

**변경 파일**
- 수정: `CLAUDE.md`
- 생성: `AGENTS.md`
- 수정: `Decisionlog.md`
- 수정: `Worklog.md`
- 수정: `Troubleshootinglog.md`
- 수정: `docs/company-selection.md`
- 수정: `docs/implementation-plan.md`
- 수정: `docs/deep-research-prompt.md`

**검증**
- `CLAUDE.md`와 `AGENTS.md`의 SHA-256 해시가 동일함을 확인
- 두 파일 모두 `0.1 에이전트 지침 파일 동기화` 절을 포함하는지 확인
- `logs/`를 제외한 작업 문서에서 오래된 기업 선정 Decision ID 고정 참조와 단일 지침 파일 참조를 정리

**판단 근거**
- Codex는 일반적으로 `AGENTS.md`를 프로젝트 지침으로 참조하므로, 기존 Claude용 작업 헌법을 동일하게 제공해야 도구 간 작업 기준이 어긋나지 않음

**결과**
- 완료: Codex용 `AGENTS.md` 구축 및 `CLAUDE.md`와의 동기화 기준 추가

---

### W-002 · Gemini Deep Research용 기업 선정 리서치 프롬프트 작성
**요청**
- 5개 후보 기업 중 어디를 선정할지 판단할 자료를 Gemini Deep Research로 조사하기 위한 프롬프트 작성

**수행 작업**
- `docs/company-selection.md`의 선정 기준(근거 확보 가능성 최우선 등)과 `docs/과제.md`의 실격 조건(비공개 정보·확인 불가 경험·출처 없는 숫자 금지)을 반영해 리서치 프롬프트 작성
- 프롬프트를 `docs/deep-research-prompt.md`로 저장(재사용·재검토 가능하도록 기록)
- `docs/company-selection.md`에 "리서치 도구" 절 추가 — Deep Research 결과를 그대로 신뢰하지 않고 출처를 직접 재확인하도록 명시

**변경 파일**
- 생성: `docs/deep-research-prompt.md`
- 수정: `docs/company-selection.md`(리서치 도구 절 추가)

**검증**
- 프롬프트 내용이 과제 규정(출처 명시, 비공개정보 금지 등)과 모순되지 않는지 문서 대조로 확인. 실제 Gemini 실행 결과는 아직 없음(사용자가 직접 실행 예정).

**판단 근거**
- AI 리서치 도구 결과는 환각 가능성이 있으므로, 프롬프트 자체에 "출처 명시 필수" 조건을 강하게 넣고, 결과 활용 시에도 재검증 절차를 문서에 명시해 과제 실격 조건(출처 없는 근거)을 피하도록 함

**결과**
- 완료: 리서치 프롬프트 작성 및 저장
- 남은 작업: 사용자가 Gemini Deep Research 실행 → 결과를 `docs/company-selection.md`에 반영 → 채점 → 기업 확정

---

### W-001 · 프로젝트 운영 체계 셋업 + 기업 선정 단계 준비
**요청**
- 프로젝트 초기 운영 구조 셋업
- `docs/과제.md` 확인 후, 카카오페이증권 제출 완료 상태에서 추가로 도전할 기업을 선정하는 단계에 필요한 구조를 세팅

**수행 작업**
- 기존 폴더(.claude, .codex, tools/save_log.py, logs/) 확인 — 로그 자동 저장 훅은 이미 구성되어 있음을 확인
- `docs/과제.md`를 읽고 과제 요구사항(제출 구조, 질문 5문항, 실격 조건, 참여 기업 목록) 파악
- 운영 파일 생성: `CLAUDE.md`, `README.md`, `Worklog.md`, `Decisionlog.md`, `Troubleshootinglog.md`, `.gitignore`
- `docs/project-plan.md`, `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md` 생성(2차 과제 전체 관점에서 초안 작성, 세부는 기업 선정 후 확정)
- 기업 선정 전용 문서 `docs/company-selection.md` 신설 — 후보 5곳(채널톡, 메디테라피, 무신사, 삼일PwC, 마이리얼트립) 목록과 선정 기준, 조사 진행 체크리스트 마련
- 빈 작업 폴더 `src/`, `tests/`, `out/`, `docs/references/` 생성(`.gitkeep`)

**변경 파일**
- 생성: `CLAUDE.md`, `README.md`, `Worklog.md`, `Decisionlog.md`, `Troubleshootinglog.md`, `.gitignore`
- 생성: `docs/project-plan.md`, `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/company-selection.md`
- 생성: `src/.gitkeep`, `tests/.gitkeep`, `out/.gitkeep`, `docs/references/.gitkeep`

**검증**
- 파일/폴더 생성 여부 확인. 구현(리서치·플러그인 코드)은 미착수 — 기업 선정 리서치와 실제 조사는 다음 단계.

**판단 근거**
- 해커톤 과제는 기업별로 별도 제출이 필요하고, 근거는 반드시 공개 자료여야 하므로, 조사→비교→결정의 과정을 문서로 남겨야 나중에 심사 및 재검토가 가능함
- 아직 기업이 정해지지 않아 `docs/requirements-contract.md` 등 구현 단계 문서는 뼈대만 만들고 세부는 기업 확정 후 채우기로 함

**결과**
- 완료: 운영 체계 및 기업 선정 단계용 문서 구조 마련
- 남은 작업: `docs/company-selection.md`의 후보 5곳에 대한 공개 자료 리서치 수행 → 비교표 채우기 → 기업 확정 → Decisionlog에 다음 Decision ID로 기록
