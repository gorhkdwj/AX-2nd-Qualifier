# Worklog · AX해커톤 예선 2차 제출(기업 미정)

주요 사용자 요청이 끝날 때마다 아래 형식으로 누적 기록한다. (규칙: CLAUDE.md / AGENTS.md 11절). 최신 항목을 위에 추가한다.

## 기록 형식
```
### W-00N · 작업 제목
**요청** / **수행 작업** / **변경 파일** / **검증** / **판단 근거** / **결과**
```

---

### W-007 · Gemini 보고서 폐기 + Codex·독립조사 종합 최종 보고서 생성
**요청**
- 신뢰성이 극도로 낮은 Gemini 보고서를 폐기
- 서브에이전트 독립 조사 내용을 문서화하여 Codex 조사와 종합·비교한 최종 보고서 생성
- 카카오페이증권 제외, 평가 항목별 절대 점수·총점 비교, 단일 기업 추천 금지, 공개자료만으로 판단

**수행 작업**
- W-005 워크플로우 journal에서 서브에이전트의 독립 조사(`independent_findings`)·출처 검증(`citation_checks`) 전체 추출
- Gemini 보고서를 `docs/archive/company-research-report_gemini_DISCARDED.md`로 이동(하드 삭제 대신 감사 추적용 보존), 폐기 사유를 `docs/archive/README.md`에 기록
- `docs/company-research-final-report.md` 생성: 근거 등급([검증됨]/[교차확인]/[확인 필요]) 도입, 기업별 종합(Codex 검증 사실 + 독립 조사 신규 사실 + 주의점 + 출처), 평가 6항목 절대 점수 재산정(이전 검토 보고서 대비 변화 명시), 총점 비교표, 사용자 선정용 중립 참고·확인 필요 항목 정리
- `docs/company-selection.md` 체크리스트 갱신 및 3개 결과 문서 연결

**변경 파일**
- 생성: `docs/company-research-final-report.md`, `docs/archive/README.md`
- 이동(폐기): `docs/company-research-report_gemini.md` → `docs/archive/company-research-report_gemini_DISCARDED.md`
- 수정: `docs/company-selection.md`, `Worklog.md`

**검증**
- 독립 조사에서 두 보고서가 놓친 신규 검증 사실 확인: 채널톡 완전자본잠식(2025말 자본총계 약 -9.4억), 마이리얼트립 2025.7 민다 상대 1.5억 배상 판결, 무신사 셀러 수수료 갈등·표기오류 반복 등. 각 사실에 근거 등급 표기.
- 최종 총점(30점): 무신사 26, 메디테라피 19, 마이리얼트립 19, 채널톡 18, 삼일PwC 15
- 단일 기업 추천 문구 없음, 카카오페이증권 미포함 재확인

**판단 근거**
- Gemini는 5개 기업 전반에서 환각이 반복 확인돼 근거로 부적합. 다만 검토·최종 보고서가 Gemini의 구체적 오류를 인용하므로 원본을 삭제하지 않고 아카이브해 추적성 유지
- 종합 보고서는 검증된 사실만 점수 근거로 삼고, 독립 조사로 확인된 신규 사실을 반영해 이전 검토 대비 점수 변화를 투명하게 기록

**결과**
- 완료: Gemini 폐기, 최종 종합 보고서 생성
- 남은 작업: 사용자가 최종 보고서 검토 후 기업 1곳 확정 → Decisionlog 기록 및 후속 문서 갱신. 확정 전 `[확인 필요]` 항목(채널톡 DART 등) 재확인 권장

---

### W-006 · 헌법에 자동 commit·push 규칙 추가 + logs/ Git 제외(로컬 전용)
**요청**
- 두 헌법(CLAUDE.md/AGENTS.md)에 모든 작업 이후 바로 commit·push 하도록 규칙 추가하고 즉시 commit·push까지 진행
- `logs/` 폴더는 Git에 반영하지 말고 로컬에서만 관리

**수행 작업**
- CLAUDE.md·AGENTS.md 10절(Git 원칙) 개정: 원격 저장소 명시, 매 작업 종료 시 자동 commit·push, `logs/`는 Git 제외·로컬 전용(단 submission.zip에는 포함), commit 전 `git status`로 혼입 확인
- 두 헌법 7절(보안)에 로그 로컬 관리·제출물 포함 원칙 보강
- `.gitignore`에 `logs/` 추가, 기존 "logs/는 제외 금지" 주석 삭제
- 이미 추적 중이던 `logs/`를 `git rm --cached -r logs/`로 추적 해제(로컬 파일 유지)
- Decisionlog에 D-003 기록

**변경 파일**
- 수정: `CLAUDE.md`, `AGENTS.md`(동기화 유지), `.gitignore`, `Decisionlog.md`, `Worklog.md`
- Git 추적 해제(로컬 유지): `logs/**`

**검증**
- CLAUDE.md·AGENTS.md SHA-256 해시 동일 확인
- `git ls-files logs/` 결과가 비어 있음(추적 해제 완료), 로컬 `logs/` 파일은 그대로 존재함 확인
- commit·push 결과는 아래 커밋에서 확인

**판단 근거**
- 사용자가 두 정책을 명시적으로 요청. 로그는 제출물(zip)에만 포함하면 규정을 충족하므로 공개 저장소 노출을 피하는 편이 안전

**결과**
- 완료: 헌법·gitignore 개정, logs 추적 해제, 기록, commit·push
- 남은 작업: 최종 제출 시 로컬 `logs/`를 submission.zip에 포함하는 절차(추후 제출 단계에서 수행)

---

### W-005 · codex/gemini 기업 리서치 보고서 환각·오류 검토 (4단계 서브에이전트 워크플로우)
**요청**
- `docs/company-research-report_codex.md`와 `docs/company-research-report_gemini.md` 두 리서치 보고서를 환각·부정확한 정보·비합리적 판단 여부로 엄격히 검토
- (1)조사 내용 리서치, (2)리서치-보고서 비교, (3)종합 판단, (4)검토자 4단계를 각각 서브에이전트로 수행
- 카카오페이증권 제외, 평가 항목별 절대 점수 부여, 총점 비교만 하고 단일 기업 추천 금지, 공개자료만으로 판단

**수행 작업**
- Workflow 도구로 4단계 파이프라인 실행: 5개 기업(채널톡, 메디테라피, 무신사, 삼일PwC, 마이리얼트립) 각각에 대해 리서치(출처 URL 직접 WebFetch 검증) → 비교(codex/gemini 주장별 정확·과장·환각·비약 판정) → 전체 종합(평가 항목 정의 + 절대 점수 + 총점표) → 검토(요구사항 준수 감사 및 최종본 확정)
- 검토자 단계에서 종합 초안의 위반 사항 2건(미검증 사실 단정, 출처 오귀속) 발견·수정
- 최종 결과를 `docs/company-research-review-report.md`로 저장

**변경 파일**
- 생성: `docs/company-research-review-report.md`

**검증**
- 각 사실 주장에 대해 서브에이전트가 실제 URL을 WebFetch로 열어 원문과 대조. 12개 서브에이전트 호출 모두 정상 완료(에러 0건).
- 검토자 단계가 종합 단계의 위반 사항을 실제로 잡아냈음을 확인(2건 수정).

**판단 근거**
- 두 보고서 모두 AI가 작성한 리서치이므로 환각 가능성이 있어, 팩트체크 없이 그대로 기업 선정 근거로 쓰면 과제 실격 조건(출처 없는/틀린 근거)에 노출될 위험이 컸음
- 리서치와 판단을 분리된 서브에이전트로 나누고 마지막에 검토자를 둬서, 종합 단계 자체가 새로운 미검증 주장을 만들어내는 것도 걸러내도록 설계

**결과**
- 완료: codex 보고서가 gemini 보고서보다 전반적으로 신뢰도가 뚜렷이 높음을 확인(gemini는 5개 기업 전체에서 반복되는 환각 패턴 다수 발견). 절대 점수 총점(30점 만점): 채널톡 14, 메디테라피 19, 무신사 25, 삼일PwC 16, 마이리얼트립 16
- 특기사항: 채널톡 관련 "채널코퍼레이션 완전자본잠식" 단서가 검토 과정에서 발견됐으나 정식 검증 절차를 거치지 않아 최종 보고서 본문에서는 제외되고 별도 "확인 필요" 항목으로 남김(`docs/company-research-review-report.md` 5절)
- 남은 작업: 사용자가 `docs/company-research-review-report.md`를 검토해 최종 기업 1곳 확정 → `Decisionlog.md`에 다음 Decision ID로 기록

---

### W-004 · GitHub 원격 저장소 연결 및 푸시
**요청**
- `https://github.com/gorhkdwj/AX-2nd-Qualifier.git` 저장소에 현재 작업 폴더를 Git으로 연결하고 푸시

**수행 작업**
- `AGENTS.md`와 `CLAUDE.md` 동기화 상태 확인 중 두 파일 차이를 발견해 더 최근 `CLAUDE.md` 기준으로 `AGENTS.md` 동기화
- 민감정보 패턴 검색 수행
- 원격 저장소 상태 확인(`git ls-remote` 결과 비어 있음)
- `main` 브랜치로 Git 저장소 초기화
- `origin` 원격을 `https://github.com/gorhkdwj/AX-2nd-Qualifier.git`로 연결
- 전체 추적 대상 파일을 첫 커밋으로 생성하고 `origin/main`에 푸시

**변경 파일**
- 수정: `AGENTS.md`(`CLAUDE.md`와 동기화)
- 수정: `Worklog.md`
- 수정: `Decisionlog.md`

**검증**
- 민감정보 패턴 검색 결과 일치 항목 없음
- `CLAUDE.md`와 `AGENTS.md`의 SHA-256 해시 동일 확인
- 첫 커밋 `dbed5f0` 푸시 성공
- `main` 브랜치가 `origin/main`을 추적하도록 설정됨

**판단 근거**
- 사용자가 명시적으로 GitHub 저장소 연결과 푸시를 요청했고, 프로젝트 지침상 주요 단계는 커밋·푸시 및 기록을 남겨야 함

**결과**
- 완료: Git 초기화, 원격 연결, 첫 푸시 완료
- 남은 작업: 없음

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
