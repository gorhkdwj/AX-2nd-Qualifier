# 구현 계획 · 무신사 상품 데이터 에이전트화 변환기

> 처음부터 전체를 달리지 않는다. 가장 작은 성공 단위부터. 각 단계는 완료 조건과 검증 방법을 명시한다.

## 단계 개요
| 단계 | 목표 | 완료 조건 | 검증 방법 | 의존/연결 |
|------|------|-----------|-----------|-----------|
| S1 | 주제·계약 고정 | 무신사 문제 2 확정, Decisionlog 기록, requirements-contract 갱신 | 관련 문서에서 이전 미정 상태 제거, 문서 간 모순 확인 | 없음 |
| S2 | 지식 데이터 작성 | `taxonomy.json`, `schema.json` 초안 완성 | 샘플 valid/invalid JSON으로 스키마 판별 | S1 |
| S3 | Skill 작성 | `src/skills/product-agentizer/SKILL.md` 작성 | frontmatter와 발동/비발동 조건 확인 | S2 |
| S4 | 스크립트·manifest 구현 | `validate.py`, `dedup.py`, `src/.codex-plugin/plugin.json` 구현 | 더미 입력 단독 실행 성공 | S2~S3 |
| S5 | 더미 픽스처 검증 | 아우터·상의 더미 입력과 정답 라벨로 정확도 산출 | 속성별 precision/recall, 중복 감지 결과 기록 | S4 |
| S6 | Codex CLI 실제 실행 | 로컬 설치·실행 시연 완료 | 새 Codex 스레드에서 변환→질의 예시 재현 | S5 |
| S7 | 제출 문서 작성 | README, 질문 5문항 답변 작성 | 문서-코드-로그 정합성 점검 | S6 |
| S8 | 패키징·제출 준비 | `submission.zip` 구조 요건 충족 | 구조 체크리스트, 비밀정보·크롤러 없음 확인 | S7 |

## 단계 상세

### S1 · 주제·계약 고정
- 왜 필요한가: 기존 문서에는 이전 미정 상태와 “무신사 문제 2 확정” 상태가 섞여 있어, 구현 전 기준 계약을 하나로 고정해야 한다.
- 이전 단계와 연결: 후보 조사·검토 결과를 바탕으로 사용자가 무신사 문제 2를 공식 확정했다.
- 다음 단계로 전달: 입력/출력/지표/오류 기준이 고정된 `docs/requirements-contract.md`.
- 완료 조건: `Decisionlog.md`에 D-007 기록, `docs/company-selection.md` 확정 체크, `docs/project-plan.md`·`docs/implementation-plan.md`·`docs/validation-plan.md`·`docs/requirements-contract.md` 갱신.
- 검증 방법: `rg`로 이전 미정·미작성 표현 잔존 여부 확인, 문서 간 핵심 명칭 일치 확인.
- 실패 시 중단점: 확정 근거가 부족하면 구현으로 넘어가지 않고 사용자에게 재검토 요청.

### S2 · 지식 데이터 작성
- 왜 필요한가: 에이전트화 변환의 일관성은 taxonomy와 schema에 달려 있다.
- 산출물: `src/skills/product-agentizer/references/taxonomy.json`, `src/skills/product-agentizer/references/schema.json`.
- 완료 조건: 아우터·상의 2개 카테고리에 대해 핵심 속성 vocabulary와 JSON schema가 존재한다.
- 검증 방법: 정상 샘플 JSON은 통과, 필수 필드 누락·범위 밖 카테고리·잘못된 타입은 실패.

### S3 · SKILL.md 작성
- 왜 필요한가: Codex가 언제 이 skill을 써야 하는지, 어떤 절차로 변환해야 하는지 명확히 해야 한다.
- 산출물: `src/skills/product-agentizer/SKILL.md`.
- 완료 조건: `name`, `description` frontmatter 포함. description에 “패션 상품 상세정보→에이전트 질의용 구조화 데이터 변환”과 “표기 규정 검수에는 비발동”을 명시.
- 검증 방법: 대표 프롬프트로 발동/비발동 조건을 검토.

### S4 · 스크립트·manifest 구현
- 왜 필요한가: 스키마 검증과 중복 감지는 결정적으로 재현되어야 한다.
- 산출물: `src/.codex-plugin/plugin.json`, `src/skills/product-agentizer/scripts/validate.py`, `src/skills/product-agentizer/scripts/dedup.py`.
- 완료 조건: 스크립트가 파일 입력과 표준입력 중 최소 하나로 단독 실행 가능하고, `plugin.json`이 `skills: "./skills/"`를 가리킨다.
- 검증 방법: 더미 JSON을 넣어 validate/dedup 실행 결과 확인.

### S5 · 더미 픽스처 검증
- 왜 필요한가: 실제 공개 상품페이지는 정답 라벨이 없으므로, 정확도 검증은 정답을 아는 합성 데이터가 필요하다.
- 산출물: `tests/fixtures/`의 입력 텍스트, 정답 JSON, 중복쌍/비중복쌍.
- 완료 조건: 속성별 precision/recall과 중복 감지 정확도를 산출해 기록한다.
- 검증 방법: 평가 스크립트 또는 수동 비교로 expected/actual 차이를 확인.

### S6 · Codex CLI 실제 실행·시연
- 왜 필요한가: 과제는 Codex 플러그인이므로 문서와 단독 스크립트뿐 아니라 실제 Codex 환경에서 동작해야 한다.
- 완료 조건: 로컬 marketplace 등록 또는 로컬 플러그인 설치 후 새 Codex 스레드에서 더미 상품설명 → 구조화 JSON → 자연어 질의 설명 흐름을 재현한다.
- 검증 방법: 실행 명령, 입력, 출력 요약을 README 또는 검증 기록에 남긴다.

### S7 · 제출 문서 작성
- 왜 필요한가: 심사는 로그·플러그인·질문 답변의 정합성을 함께 본다.
- 완료 조건: 루트 README와 질문 5문항 답변이 실제 구현 기능만 설명한다.
- 검증 방법: README-기능, 질문 답변-로그, 요구사항-코드 정합성 점검.

### S8 · 패키징·제출 준비
- 왜 필요한가: 제출 구조 오류와 로그 누락은 치명적이다.
- 완료 조건: `submission.zip`에 `src/`, `README.md`, `logs/` 포함. `src/.codex-plugin/plugin.json`과 `src/skills/product-agentizer/SKILL.md` 존재.
- 검증 방법: 압축 파일 구조 대조, 비밀정보 패턴 검색, 크롤러/대량 수집 코드 없음 확인.
