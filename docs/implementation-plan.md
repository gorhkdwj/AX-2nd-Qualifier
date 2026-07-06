# 구현 계획 · 무신사 상품 데이터 에이전트화 변환기

> 무신사 문제 2의 단일 활성 구현 계획이다. 병합 전 상세 계획 보관본은 `docs/archive/musinsa-agentizer-plan_MERGED.md`에 두고, 세부 계약은 `docs/requirements-contract.md`, 검증 기준은 `docs/validation-plan.md`를 따른다.

## Context
AX 해커톤 2차 제출 대상 기업·문제는 **무신사 / 문제 2 · 상품 데이터 에이전트화 변환기**로 확정한다. 무신사 테크리드 인터뷰 공개영상(https://www.youtube.com/watch?v=OLAWeIuiD5Y)의 핵심 비전인 "AI 에이전트가 패션 질문 때 첫 번째로 쓰는 도구가 무신사이길", "동일 상품을 두 번 등록해야 하는 파편화"에 대응한다.

문제는 무신사 상품 상세정보가 소비자에게는 읽히지만, AI 에이전트가 정확·일관·설명 가능하게 질의하기에는 비정형 텍스트 중심이라는 점이다. 해결책은 상품 상세페이지 텍스트를 **정규화된 구조화 속성 + 표준 taxonomy 매핑 + 중복 감지 + 에이전트 질의 descriptor**로 변환하는 Codex 플러그인이다.

## 확정 스코프
- 근거: 무신사 인터뷰 공개영상 URL을 1차 출처로 사용하고, 무신사 멀티플랫폼·글로벌 확장·에이전트 커머스 관련 공개 사실로 보강한다.
- MVP 카테고리: **아우터·상의 2개 카테고리**. taxonomy는 데이터 주도로 설계해 이후 카테고리 확장을 쉽게 한다.
- 입력 방식: 상품 URL은 출처 메타데이터로만 기록하고, 실제 실행 입력은 사용자가 직접 붙여넣은 상품 상세 텍스트로 제한한다. 자동 fetch·크롤링은 포함하지 않는다.
- 구성: **SKILL + 결정적 스크립트**. instruction SKILL, 정적 taxonomy/schema 데이터, Python 검증·중복감지 스크립트를 조합한다.
- 검증: 더미 픽스처로 정량 검증하고, 로컬 Codex CLI에서 실제 설치·실행·시연한 뒤, S8 패키징 전 S7.5 확장 검증, S7.7 실제 페이지형 합성 더미 검증, S7.8 `size_info` 표기 패턴 보강 검증으로 재현성 패키지를 보존한다.

## 제출물 구조
플러그인 루트는 `src/`이다. 제출 zip은 `src/` + 루트 `README.md` + 루트 `logs/`로 구성한다.

```text
src/
├── .codex-plugin/plugin.json
└── skills/product-agentizer/
    ├── SKILL.md
    ├── references/
    │   ├── taxonomy.json
    │   └── schema.json
    └── scripts/
        ├── validate.py
        └── dedup.py
README.md
logs/
tests/fixtures/
docs/references/
```

- `src/.codex-plugin/plugin.json`: 필수 manifest. `.codex-plugin/` 폴더에는 manifest만 둔다.
- `src/skills/product-agentizer/SKILL.md`: `name`, `description` frontmatter와 변환 절차 지시문.
- `references/taxonomy.json`: 아우터·상의 카테고리, 소재, 핏, 계절, TPO 등 표준 용어.
- `references/schema.json`: 출력 JSON 스키마.
- `scripts/validate.py`: 출력 JSON 스키마, 필수 속성, taxonomy 용어 유효성 검증.
- `scripts/dedup.py`: 속성 유사도 기반 중복 후보 감지.
- `logs/`: `tools/save_log.py` 훅이 자동 저장한 원본 로그. 수동 편집하지 않는다.
- `tests/fixtures/`: 제출물은 아니며, 더미 상품설명·정답 라벨·중복쌍·Codex actual output·공개 snippet sanity 검증용으로 사용한다.

## 재사용 자산
- `tools/save_log.py`: 대화 로그 자동 저장 훅. 기존 구현을 그대로 사용하고 편집하지 않는다.
- `src/`, `tests/`, `docs/references/`: 이미 마련된 작업 폴더를 사용한다.
- `docs/archive/plugin-directions_PRE_SELECTION.md`: 선정 전 후보 방향과 안전성 검토 이력 보관본.
- `docs/technical_references/`: Codex 플러그인·Skill 규격 확인용 공식 문서 사본. 구현 중 필요한 문서만 확인한다.

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
| S7.5 | 확장 검증·재현성 보존 | 합성 100건, Codex subset 20건, 실제 공개 snippet 10건의 입력·expected·actual·결과 보존 | `tools/run_expanded_validation.py`, schema/precision/recall/dedup/hash 확인 | S7 |
| S7.7 | 실제 페이지형 합성 더미 검증 | 정보 밀도별 합성 상세페이지 입력으로 운영형 입력 대응력 검증 | schema/precision/recall/dedup/density별 missing·ambiguous 확인 | S7.5 |
| S7.8 | size_info 표기 패턴 보강 검증 | 실제 페이지에서 나올 법한 size 표기 48건 합성 fixture와 Codex actual 보존 | `tools/run_size_info_pattern_validation.py`, size_info precision/recall, recommendation noise FP 확인 | S7.7 |
| S8 | 패키징·제출 준비 | `submission.zip` 구조 요건 충족 | 구조 체크리스트, 비밀정보·크롤러 없음 확인 | S7.8 |

## 단계 상세

### S1 · 주제·계약 고정
- 왜 필요한가: 구현 전 기준 계약을 하나로 고정해 입력, 출력, 지표, 오류 기준의 흔들림을 막는다.
- 완료 내용: `docs/requirements-contract.md`에 붙여넣기 상품 상세 텍스트 입력, 정규화 JSON 출력, 속성별 precision/recall·중복감지 정확도, 상태·오류 판정, 누락·모호 속성 처리 규칙을 고정한다.
- 완료 내용: `docs/project-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/company-selection.md`, `Decisionlog.md`를 무신사 문제 2 기준으로 정리한다.
- 남은 세부 작업: `docs/references/`에 인터뷰 URL, 원본 영상 대조 인용, 공개 사실 출처·확인일을 구현 과정에서 보강한다.
- 검증 방법: `rg`로 이전 미정·미작성 표현 잔존 여부를 확인하고, 문서 간 핵심 명칭과 입력 정책이 일치하는지 확인한다.

### S2 · 지식 데이터 작성
- 왜 필요한가: 에이전트화 변환의 일관성은 taxonomy와 schema에 달려 있다.
- 산출물: `src/skills/product-agentizer/references/taxonomy.json`, `src/skills/product-agentizer/references/schema.json`.
- 내용: 아우터·상의 2개 카테고리의 카테고리/서브카테고리, 핏·실루엣, 소재, 컬러, 계절, TPO·스타일 태그, 관리, 사이즈 vocabulary를 정의한다.
- 완료 조건: 정상 샘플 JSON은 통과하고, 필수 필드 누락·범위 밖 카테고리·잘못된 타입은 실패한다.

### S3 · SKILL.md 작성
- 왜 필요한가: Codex가 언제 이 skill을 써야 하는지, 어떤 절차로 변환해야 하는지 명확히 해야 한다.
- 산출물: `src/skills/product-agentizer/SKILL.md`.
- 완료 조건: `name`, `description` frontmatter 포함. description에 “패션 상품 상세정보→에이전트 질의용 구조화 데이터 변환”과 “표기 규정 검수에는 비발동”을 명시한다.
- 지시 흐름: 텍스트에서 속성 추출 → taxonomy 매핑 → schema 준수 JSON 생성 → 부족·모호 속성 표기 → 에이전트 질의 descriptor 생성 → `validate.py` 검증 → 배치 입력이면 `dedup.py` 중복 감지.

### S4 · 스크립트·manifest 구현
- 왜 필요한가: 스키마 검증과 중복 감지는 결정적으로 재현되어야 한다.
- 산출물: `src/.codex-plugin/plugin.json`, `src/skills/product-agentizer/scripts/validate.py`, `src/skills/product-agentizer/scripts/dedup.py`.
- `validate.py`: 출력 JSON을 schema와 대조하고, 필수 속성·taxonomy 용어 유효성을 검사한다. 표준입력 또는 파일 인자로 단독 실행 가능해야 한다.
- `dedup.py`: 상품 JSON 리스트를 입력받아 속성 유사도로 중복 후보를 판별한다.
- `plugin.json`: name `musinsa-product-agentizer`, version `0.1.0`, description, `"skills": "./skills/"`.

### S5 · 더미 픽스처 검증
- 왜 필요한가: 실제 공개 상품페이지는 정답 라벨이 없으므로, 정확도 검증은 정답을 아는 합성 데이터가 필요하다.
- 산출물: `tests/fixtures/`의 아우터·상의 더미 상품설명, 정답 JSON, 중복쌍/비중복쌍.
- 완료 조건: 속성별 precision/recall과 중복 감지 정확도를 산출해 기록한다.
- 검증 방법: 평가 스크립트 또는 수동 비교로 expected/actual 차이를 확인한다.

### S6 · Codex CLI 실제 실행·시연
- 왜 필요한가: 과제는 Codex 플러그인이므로 문서와 단독 스크립트뿐 아니라 실제 Codex 환경에서 동작해야 한다.
- 완료 조건: 로컬 marketplace 등록 또는 로컬 플러그인 설치 후 새 Codex 스레드에서 더미 상품설명 → 구조화 JSON → 자연어 질의 설명 흐름을 재현한다.
- 검증 방법: 실행 명령, 입력, 출력 요약을 README 또는 검증 기록에 남긴다.

### S7 · 제출 문서 작성
- 왜 필요한가: 심사는 로그·플러그인·질문 답변의 정합성을 함께 본다.
- 완료 조건: 루트 README와 질문 5문항 답변이 실제 구현 기능만 설명한다.
- 검증 방법: README-기능, 질문 답변-로그, 요구사항-코드 정합성을 점검한다.

### S7.5 · 확장 검증·재현성 보존
- 왜 필요한가: 최종 패키징 전에는 단순 성공 여부가 아니라, 같은 입력·명령·결과를 다시 추적할 수 있어야 한다.
- 산출물: `tests/fixtures/expanded_dummy/`, `tests/fixtures/codex_subset/`, `tests/fixtures/real_sanity/`, `docs/reports/s7-expanded-validation-report.md`, `docs/reports/s7-expanded-validation-results.json`.
- 완료 조건: 합성 expected 100건 schema-valid 100%, Codex subset 20건 actual schema-valid 100%, Codex subset micro precision 95% 이상·recall 85% 이상, dedup accuracy 95% 이상, cross-category high-confidence false duplicate 0건. 3단계 taxonomy 반영 후 Codex subset의 `detail_type`은 historical actual 보존을 위해 `not_applicable`로 기록하고, `detail_type` coverage와 parent-child 검증은 합성 100건·실제 공개 snippet·schema negative fixture에서 확인한다.
- 공개 sanity: 공개 무신사 상품페이지 10건은 URL·확인일·짧은 factual snippet만 저장한다. 전체 상세페이지 복사본이나 자동 fetch 결과는 저장하지 않는다.
- 검증 방법: `python tools\generate_expanded_validation_fixtures.py`, `python tools\run_expanded_validation.py`를 실행하고, 실패 사례와 보완 내역을 Worklog/Troubleshootinglog에 기록한다. 단, `codex_subset`은 historical Codex 실행 보존 세트이므로 생성기가 덮어쓰지 않고 보존 fixture를 검증 대상으로 사용한다.

### S7.7 · 실제 페이지형 합성 더미 검증
- 왜 필요한가: 실제 무신사 상품페이지는 상품별 정보 밀도가 균일하지 않다. 모든 상품이 소재 부위, 혼용률, 실측표, 관리법을 완전하게 제공한다고 가정하면 실제 운영 입력을 과도하게 단순화한다.
- 산출물: `docs/full-page-dummy-validation-plan.md`, `tests/fixtures/full_page_dummy/`, `tests/fixtures/full_page_codex_subset/`, `docs/reports/s7-7-full-page-dummy-validation-report.md`, `docs/reports/s7-7-full-page-dummy-validation-results.json`.
- 완료 조건: 실제 페이지 원문이나 로컬 전용 비공개 데이터를 쓰지 않고, `sparse`, `medium`, `full`, `noisy_ambiguous` 밀도별 합성 상세페이지형 입력을 보존한다. expected/reference actual schema-valid 100%, Codex subset actual schema-valid 100%, `detail_type` precision/recall 95% 이상, dedup accuracy 95% 이상, cross-category high-confidence false duplicate 0건을 목표로 한다.
- 현재 결과: SKILL-only `size_info` 원자화 보강 후 50건 Codex subset은 schema-valid 50/50, micro precision 99.74%, micro recall 99.74%, `detail_type` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%를 기록했다.
- 검증 방법: 새 생성기와 실행 스크립트로 입력·expected·actual·평가 결과를 모두 재현 가능하게 보존하고, 밀도별로 missing/ambiguous 판단이 의도대로 작동하는지 확인한다.

### S7.8 · size_info 표기 패턴 보강 검증
- 왜 필요한가: S7.7의 `size_info` 100%는 합성 상세페이지형 50건 기준이다. 실제 판매 페이지에는 문자형 옵션, 숫자형 옵션, 브랜드 자체 사이즈, 실측표, 모델 착용, 비교 가이드, 추천·후기 노이즈가 더 다양하게 등장할 수 있으므로 별도 coverage가 필요하다.
- 산출물: `docs/size-info-coverage-plan.md`, `tests/fixtures/size_info_patterns/`, `docs/reports/s7-8-size-info-coverage-report.md`, `docs/reports/s7-8-size-info-coverage-results.json`.
- 완료 조건: 실제 상품 원문을 저장하지 않고, 12개 패턴 그룹 × 4건의 합성 fixture 48건을 보존한다. expected/actual schema-valid 100%, `size_info` precision/recall 95% 이상, `recommendation_noise` false positive 0건을 목표로 한다.
- 현재 결과: 격리 workspace에서 실제 Codex CLI actual을 생성했고, schema-valid 48/48, `size_info` precision 100.00%, recall 100.00%, TP/FP/FN 97/0/0, `recommendation_noise` false positive 0건을 기록했다.
- 해석 기준: 이 결과는 실제 판매 데이터 전체 기준 성능이 아니라, 실제 페이지에서 나올 법한 size 표기 방식을 모사한 확장 합성 fixture 기준 성능이다.
- 검증 방법: `python tools\generate_size_info_pattern_fixtures.py`, `python tools\run_full_page_codex_smoke20_cli.py --fixture size_info_patterns --timeout 3600`, `python tools\run_size_info_pattern_validation.py`로 입력·expected·actual·평가 결과를 재현한다.

### S8 · 패키징·제출 준비
- 왜 필요한가: 제출 구조 오류와 로그 누락은 치명적이다.
- 완료 조건: `submission.zip`에 `src/`, `README.md`, `logs/` 포함. `src/.codex-plugin/plugin.json`과 `src/skills/product-agentizer/SKILL.md` 존재.
- 검증 방법: 압축 파일 구조 대조, 비밀정보 패턴 검색, 크롤러/대량 수집 코드 없음 확인.

## 종합 검증
1. **구조**: `src/.codex-plugin/plugin.json` 존재, manifest 경로 `./skills/` 유효, 제출 zip 레이아웃 일치.
2. **스크립트 단위**: `python validate.py`, `python dedup.py`를 `tests/fixtures/`에 실행하고 속성 precision/recall·중복 정확도를 산출한다.
3. **Codex 실 실행**: marketplace 등록 또는 로컬 설치 후 새 스레드에서 변환→에이전트 질의 데모를 재현한다.
4. **확장 재현성**: 합성 100건, Codex subset 20건, 공개 snippet 10건의 입력·expected·actual·평가 결과·실행 환경·hash를 보존하고 재실행한다.
5. **실제 페이지형 합성 검증**: 합성 상세페이지형 300건과 대표 subset 50건의 입력·expected·actual·평가 결과를 보존하고, 50건 subset은 격리 workspace에서 실제 Codex CLI actual을 검증한다.
6. **size_info 표기 패턴 검증**: 사이즈 옵션·실측표·모델 착용·비교 가이드·추천 노이즈를 모사한 48건 합성 fixture로 `size_info` 오탐·누락을 별도 확인한다.
7. **정합성**: requirements-contract ↔ SKILL/스크립트 동작 ↔ README ↔ 질문 5문항 사이에 모순이 없어야 한다.
8. **안전·규정**: 크롤러·비밀정보 없음, 로그 원본 무편집, 근거는 공개 URL·확인일과 함께 기록한다.

## 열린 리스크
- 인터뷰 전사본은 자동 전사이므로, 제출 인용문은 원본 영상과 대조해 정확히 인용한다.
- taxonomy는 MVP 범위인 아우터·상의로 한정한다. 범위 밖 상품은 “지원 범위 밖”으로 처리한다.
- SKILL이 스크립트를 호출하는 정확한 경로 문법은 S6 실 실행으로 확정한다. 호출이 불안정하면 instruction-only로 폴백하고 스크립트는 개발자 검증용으로 둔다.
