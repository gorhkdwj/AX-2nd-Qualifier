# Worklog · AX해커톤 예선 2차 제출(무신사 문제 2)

주요 사용자 요청이 끝날 때마다 아래 형식으로 누적 기록한다. (규칙: CLAUDE.md / AGENTS.md 11절). 최신 항목을 위에 추가한다.

## 기록 형식
```
### W-00N · 작업 제목
**요청** / **수행 작업** / **변경 파일** / **검증** / **판단 근거** / **결과**
```

---

### W-022 · S5 더미 픽스처 정량 검증 구현
**요청**
- 다음 단계 진행: S5 더미 데이터셋과 정량 검증 스크립트 작성

**수행 작업**
- 단계 간 정합성 검토 게이트에 따라 기준 계약, 구현 계획, 검증 계획, README, Worklog, Decisionlog 확인
- `tests/fixtures/evaluation/source_inputs.json` 작성: 아우터·상의 합성 상품 원문 5건
- `tests/fixtures/evaluation/expected_products.json` 작성: 정답 구조화 JSON 5건
- `tests/fixtures/evaluation/predicted_products.json` 작성: 평가 harness 검증용 예측 JSON 5건
- `tests/fixtures/evaluation/duplicate_labels.json` 작성: 중복 1쌍, 비중복 9쌍 라벨
- `tests/evaluate_product_agentizer.py` 작성: schema 검증, 속성별 precision/recall, dedup 정확도 산출
- `docs/s5-evaluation-report.md` 작성: S5 실행 명령, 결과, 차이 사례, 해석 기록
- `docs/validation-plan.md`, `docs/README.md`, 루트 `README.md` 현재 상태와 검증 명령 갱신

**변경 파일**
- 생성: `tests/evaluate_product_agentizer.py`
- 생성: `tests/fixtures/evaluation/source_inputs.json`, `expected_products.json`, `predicted_products.json`, `duplicate_labels.json`
- 생성: `docs/s5-evaluation-report.md`
- 수정: `README.md`, `docs/README.md`, `docs/validation-plan.md`, `Worklog.md`

**검증**
- 통과: `python -m py_compile tests\evaluate_product_agentizer.py`
- 통과: `validate.py`로 S5 정답 JSON 5건 schema-valid 확인
- 통과: `validate.py`로 S5 예측 JSON 5건 schema-valid 확인
- 통과: `python tests\evaluate_product_agentizer.py --pretty`
- 결과: 속성 micro precision 98.55%, micro recall 88.31%
- 결과: 중복 감지 정확도 100.00%(10/10), `outer_linen_blazer_a`/`outer_linen_blazer_b` duplicate 후보 score 1.0
- 완료: S5 산출물이 S4 `validate.py`/`dedup.py`를 사용하고 S6 Codex CLI 실제 실행 결과 평가 입력으로 이어지는지 확인

**판단 근거**
- 실제 공개 상품페이지에는 정답 라벨이 없으므로, S5는 합성 원문과 정답 JSON을 사용해 평가 방식 자체를 검증해야 한다.
- 예측 JSON에 일부 누락·오분류를 의도적으로 포함하면 평가 스크립트가 false positive와 false negative를 분리해 잡는지 확인할 수 있다.

**결과**
- 완료: S5 더미 픽스처 기반 정량 검증 구현 및 결과 기록 완료
- 다음 단계: S6 Codex CLI 실제 설치·실행 시연

---

### W-021 · S4 manifest 및 검증·중복감지 스크립트 구현
**요청**
- S4 구현 방식은 추천대로 `jsonschema` 의존을 사용하고, 없을 때 명확한 안내와 함께 실패하도록 진행

**수행 작업**
- 단계 간 정합성 검토 게이트에 따라 기준 계약, 구현 계획, 검증 계획, schema/taxonomy, `SKILL.md` 확인
- `src/.codex-plugin/plugin.json` 작성: plugin name, version, description, `"skills": "./skills/"` manifest 구성
- `src/skills/product-agentizer/scripts/validate.py` 작성: JSON Schema draft 2020-12 검증, taxonomy 기반 custom check, 소재 혼용률 상태와 `quality` 필드 연결 검증
- `src/skills/product-agentizer/scripts/dedup.py` 작성: 구조화 상품 JSON 간 deterministic similarity 기반 중복 후보 산출
- `tests/fixtures/dedup/sample_products.json` 작성: 중복 후보 2건과 비중복 상의 1건 샘플
- `docs/validation-plan.md`에 `jsonschema` 의존 검증 정책 반영
- `Decisionlog.md` D-012 기록
- 루트 `README.md` 현재 상태와 로컬 검증 스크립트 실행 예시 갱신

**변경 파일**
- 생성: `src/.codex-plugin/plugin.json`
- 생성: `src/skills/product-agentizer/scripts/validate.py`, `src/skills/product-agentizer/scripts/dedup.py`
- 생성: `tests/fixtures/dedup/sample_products.json`
- 수정: `README.md`, `docs/validation-plan.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- 통과: `python -m py_compile`로 `validate.py`, `dedup.py` 문법 확인
- 통과: `validate.py` 정상 fixture 2건(`valid_outer`, `valid_top`) 성공
- 통과: `validate.py` 오류 fixture 3건(`invalid_missing_quality`, `invalid_out_of_scope_category`, `invalid_material_ratio_status`) 기대대로 실패
- 통과: `validate.py`가 dedup 샘플 상품 3건을 schema-valid로 판정
- 통과: `dedup.py`가 `outer_a`/`outer_b`를 score 1.0의 `duplicate` 후보로 산출
- 통과: `plugin.json` JSON 형식 확인
- 완료: S4 산출물이 S5 더미 fixture/정량 검증 단계와 충돌하지 않는지 확인

**판단 근거**
- `schema.json`이 JSON Schema draft 2020-12와 조건부 검증을 사용하므로 `jsonschema`를 쓰는 편이 직접 구현보다 안전하다.
- `dedup.py`는 이후 S5의 중복쌍/비중복쌍 검증으로 이어질 수 있게 구조화 JSON만 입력으로 받는 결정적 스크립트로 작성했다.

**결과**
- 완료: S4 manifest, 검증 스크립트, 중복 후보 스크립트, 샘플 fixture 초안 작성 및 실행 검증 완료
- 다음 단계: S5 더미 데이터셋과 정량 검증 스크립트로 precision/recall 및 중복 탐지 기준을 고정

---

### W-020 · SKILL.md description 한영 혼합 및 본문 한국어화
**요청**
- `src/skills/product-agentizer/SKILL.md`가 영어일 필요가 있는지 확인 후, frontmatter `description`은 한영 혼합으로 수정하고 본문은 한국어 중심으로 수정

**수행 작업**
- 현재 `SKILL.md`, 기준 계약 문서, 구현 계획을 확인해 지시 의미가 바뀌지 않도록 정합성 검토
- `name`은 그대로 유지하고, `description`은 한국어 트리거 표현과 영어 technical trigger/boundary를 함께 담는 한영 혼합 문장으로 수정
- 본문 섹션과 작업 절차, 입력·출력·완료 체크리스트를 한국어 중심으로 재작성
- 공식/시스템 트리거에 중요한 일부 문구(`Never fetch a URL automatically`, `Never estimate fabric ratios`, `Never judge legal compliance`, `schema-valid`)는 그대로 보존

**변경 파일**
- 수정: `src/skills/product-agentizer/SKILL.md`
- 수정: `Worklog.md`

**검증**
- frontmatter 유지 확인: `name`과 한영 혼합 `description` 파싱 통과
- 필수 trigger/boundary 문구 유지 확인: `schema-valid`, `agent-query-ready`, `taxonomy mapping`, `do not use`, `automatic URL fetching/crawling`, `private/internal data`
- 본문 필수 지침 유지 확인: `references/taxonomy.json`, `references/schema.json`, `ratio_status`, `material_ratio`, `scripts/validate.py`, `scripts/dedup.py`
- 단계 간 정합성 검토: S3 지시 의미는 유지하면서 한국어 가독성만 개선했으므로 S4 이후 작업과 충돌 없음
- `git diff --check` 통과, 실제 키·토큰 형식 민감정보 없음 확인

**판단 근거**
- `SKILL.md` 본문은 한글로 작성해도 작동상 문제가 없고, 이 프로젝트의 사용 언어와 입력 데이터가 한국어이므로 본문은 한국어가 더 읽기 쉽다.
- `description`은 Codex의 implicit invocation 판단에 쓰이므로, 한국어 사용 맥락을 반영하되 `schema-valid`, `taxonomy mapping`, `do not use` 같은 영어 trigger/boundary 표현을 함께 보존한다.

**결과**
- 완료: `SKILL.md` description 한영 혼합 및 본문 한국어화 완료

---

### W-019 · S3 product-agentizer SKILL.md 작성
**요청**
- 다음 작업 진행: `docs/implementation-plan.md` 기준 S3 `src/skills/product-agentizer/SKILL.md` 작성

**수행 작업**
- 단계 간 정합성 검토 게이트에 따라 `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, Codex Skill/Plugin 공식 참고 문서, S2 schema/taxonomy를 확인
- `src/skills/product-agentizer/SKILL.md` 작성: frontmatter `name`, `description` 추가
- 발동 범위: 사용자가 붙여넣은 패션 상품 상세 텍스트를 무신사 문제 2 MVP용 구조화 JSON으로 변환
- 비발동 범위: 표기 규정 적법/위법 판정, 자동 URL fetch/크롤링, 내부·비공개 데이터, 추천 랭킹, 범위 밖 카테고리
- 변환 절차: 입력 확인, category 판정, taxonomy 매핑, 소재 혼용률 엄격 처리, agent descriptor 생성, quality 필드 작성, schema 검증, 배치 중복 감지 준비
- 루트 `README.md` 현재 상태를 `SKILL.md` 초안 작성 완료로 갱신

**변경 파일**
- 생성: `src/skills/product-agentizer/SKILL.md`
- 수정: `README.md`, `Worklog.md`

**검증**
- frontmatter 파싱 통과: `name: product-agentizer`, `description` 존재 확인
- description 발동/비발동 조건 확인: pasted product detail text 변환, legal label-compliance audit·automatic URL fetching/crawling·private/internal data 비발동 명시
- schema/taxonomy 참조 정합성 확인: `references/taxonomy.json`, `references/schema.json`, `ratio_status`, `material_ratio`, `scripts/validate.py`, `scripts/dedup.py` 연결 확인
- 단계 간 정합성 검토: S2 schema/taxonomy를 입력으로 사용하고, S4 scripts가 생기면 검증·중복감지로 이어지는 구조와 충돌 없음
- `git diff --check` 통과, 실제 키·토큰 형식 민감정보 없음 확인

**판단 근거**
- S3는 Codex가 어떤 상황에서 이 skill을 써야 하는지와 어떤 절차로 schema-valid JSON을 만들어야 하는지 고정하는 단계다.
- S4의 `validate.py`, `dedup.py`가 아직 없으므로 스킬에는 스크립트 존재 시 실행하고, 없을 때는 schema-critical 수동 검토와 pending 보고를 하도록 연결했다.

**결과**
- 완료: S3 `SKILL.md` 작성 완료
- 남은 작업: S4 `plugin.json`, `validate.py`, `dedup.py` 구현

---

### W-018 · 소재 혼용률 엄격 처리 보완
**요청**
- 소재 혼용률은 법적 오해 소지가 있으므로 엄격하게 지정하고 넘어가야 하는지 검토 후 보완 진행

**수행 작업**
- 단계 간 정합성 검토 게이트에 따라 기준 계약, 구현 계획, 검증 계획, schema/taxonomy를 확인
- `docs/requirements-contract.md`에 소재 혼용률 원칙 추가: 명시 숫자만 기록, 미기재·모호 표현은 추정 금지, 부위별 분리, 법적 적합 판정 금지
- `docs/validation-plan.md`에 소재 혼용률 전용 검증 항목과 검증 데이터 정책 추가
- `schema.json`의 `materials` 항목에 `part`, `ratio_status`를 추가하고, `ratio_status`와 `ratio`의 조건부 정합성 규칙 추가
- `taxonomy.json`에 `material_part`, `material_ratio` 정규화 원칙과 `material_parts`, `ratio_statuses` vocabulary 추가
- valid/invalid schema 샘플을 새 소재 구조에 맞게 갱신하고, 잘못된 혼용률 상태 샘플 추가

**변경 파일**
- 수정: `docs/requirements-contract.md`, `docs/validation-plan.md`
- 수정: `src/skills/product-agentizer/references/schema.json`, `src/skills/product-agentizer/references/taxonomy.json`
- 수정: `tests/fixtures/schema/valid_outer.json`, `tests/fixtures/schema/valid_top.json`, `tests/fixtures/schema/invalid_out_of_scope_category.json`
- 생성: `tests/fixtures/schema/invalid_material_ratio_status.json`
- 수정: `Decisionlog.md`, `Worklog.md`

**검증**
- JSON 파싱 통과: schema/taxonomy와 schema fixture 5개
- JSON Schema 판별 통과: 정상 샘플 2개 통과 / `quality` 누락, 범위 밖 카테고리, 혼용률 상태 불일치 샘플 실패 확인
- taxonomy-schema enum 정합성 통과: attribute_keys, materials, material_parts, ratio_statuses, fit, colors, seasons, tpo_tags, care, subcategories
- 소재 ratio 조건부 검증 통과: `ratio_status: explicit`은 숫자 ratio, `missing`/`ambiguous`는 `ratio: null` 구조로 제한
- 단계 간 정합성 검토: 계약 문서, 검증 계획, schema/taxonomy, fixture가 같은 소재 혼용률 정책을 가리키는지 확인
- `git diff --check` 통과, 실제 키·토큰 형식 민감정보 없음 확인

**판단 근거**
- 의류 상품의 소재 혼용률은 표시·고지와 연결될 수 있으므로, 에이전트화 변환기라도 추정 숫자를 만들거나 부위별 소재를 섞어 보여주면 법적 오해를 만들 수 있다.
- 이번 플러그인은 무신사 문제 1인 표기 규정 검수기가 아니므로 적법/위법 판정은 하지 않고, 입력 근거 기반 구조화와 부족·모호 표시까지만 수행해야 한다.

**결과**
- 완료: 소재 혼용률 엄격 처리 보완 완료

---

### W-017 · S2 taxonomy/schema 작성
**요청**
- 다음 작업 진행: `docs/implementation-plan.md` 기준 S2 `taxonomy.json`, `schema.json` 작성

**수행 작업**
- 단계 간 정합성 검토 게이트에 따라 `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/project-plan.md`, `docs/README.md`, 루트 `README.md` 확인
- `src/skills/product-agentizer/references/taxonomy.json` 작성: 아우터·상의 MVP 범위, 하위 카테고리, 소재, 핏, 컬러, 계절, TPO, 관리 vocabulary 정의
- `src/skills/product-agentizer/references/schema.json` 작성: 단일 상품 변환 출력 JSON schema 정의
- `tests/fixtures/schema/`에 valid/invalid 샘플 4개 작성
- 루트 `README.md` 현재 상태를 taxonomy/schema 초안 작성 완료로 갱신

**변경 파일**
- 생성: `src/skills/product-agentizer/references/taxonomy.json`, `src/skills/product-agentizer/references/schema.json`
- 생성: `tests/fixtures/schema/valid_outer.json`, `tests/fixtures/schema/valid_top.json`, `tests/fixtures/schema/invalid_missing_quality.json`, `tests/fixtures/schema/invalid_out_of_scope_category.json`
- 수정: `README.md`, `Worklog.md`

**검증**
- JSON 파싱 통과: `taxonomy.json`, `schema.json`, valid/invalid 샘플 4개
- JSON Schema 판별 통과: `valid_outer.json`, `valid_top.json` 통과 / `invalid_missing_quality.json`, `invalid_out_of_scope_category.json` 실패 확인
- taxonomy-schema enum 정합성 통과: attribute_keys, materials, fit, colors, seasons, tpo_tags, care, subcategories, subcategory default TPO 검증
- 단계 간 정합성 검토: S2 산출물이 S3 `SKILL.md`, S4 `validate.py`, S5 더미 픽스처 검증의 입력으로 이어지는 구조와 충돌 없음
- `git diff --check`, 민감정보 패턴 검색 통과

**판단 근거**
- S3 `SKILL.md`와 S4 `validate.py`가 흔들리지 않으려면 먼저 표준 vocabulary와 출력 schema를 고정해야 한다.
- S5 검증에서 더미 픽스처를 비교하려면 정상·오류 샘플이 schema 기준으로 판별 가능해야 한다.

**결과**
- 완료: S2 taxonomy/schema 초안과 스키마 판별 샘플 작성 완료
- 남은 작업: S3 `src/skills/product-agentizer/SKILL.md` 작성

---

### W-016 · 단계 간 정합성 검토 지침 추가
**요청**
- `AGENTS.md`와 `CLAUDE.md`에 모든 단계에서 이전·이후·전체 단계와 충돌하지 않도록 검토하고, 기획 문서의 의도와 방향성이 어긋나지 않도록 검증하는 절차를 필수 지침으로 추가

**수행 작업**
- 두 에이전트 지침 파일에 `4.1 단계 간 정합성 검토 게이트` 신설
- 단계 시작 전·완료 전 검토, 최소 확인 문서, 단계 산출물과 이후 단계 입력의 연결, 충돌 발견 시 기준 문서 우선 갱신 또는 사용자 확인, 완료 보고 시 정합성 검토 결과 포함 규칙 명시
- Decisionlog D-010 기록

**변경 파일**
- 수정: `AGENTS.md`, `CLAUDE.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- `AGENTS.md`와 `CLAUDE.md` 해시 동일 확인
- `git diff --check`, 민감정보 패턴 검색 통과

**판단 근거**
- 남은 S2~S8 단계는 taxonomy, schema, skill, scripts, README, 제출 패키징이 서로 입력·출력으로 이어지므로 한 단계의 명칭·형식 변경이 전체 흐름을 흔들 수 있다.
- 정합성 검토를 헌법에 명시하면 기획 문서의 의도와 구현 산출물이 갈라지는 위험을 줄일 수 있다.

**결과**
- 완료: 단계 간 정합성 검토 게이트 지침 반영 완료

---

### W-015 · 구현 계획 문서 병합 및 중복 계획 아카이브
**요청**
- `AGENTS.md`와 `CLAUDE.md`가 `docs/musinsa-agentizer-plan.md`를 참조하는지 확인
- 직접 참조가 없다면 `docs/implementation-plan.md`와 문서 성격이 겹치므로 병합 가능성 검토

**수행 작업**
- `AGENTS.md`와 `CLAUDE.md`에는 `docs/musinsa-agentizer-plan.md` 직접 참조가 없음을 확인
- `docs/musinsa-agentizer-plan.md`의 Context, 확정 스코프, 제출물 구조, 재사용 자산, Verification, 열린 리스크를 `docs/implementation-plan.md`로 병합
- 기존 `docs/musinsa-agentizer-plan.md`를 `docs/archive/musinsa-agentizer-plan_MERGED.md`로 이동해 병합 보관본으로 전환
- `README.md`, `docs/README.md`, `docs/project-plan.md`, `docs/company-selection.md`, `docs/archive/README.md`, `docs/archive/plugin-directions_PRE_SELECTION.md`의 구현 기준 참조를 단일 계획 문서 기준으로 갱신
- Decisionlog D-009 기록

**변경 파일**
- 이동: `docs/musinsa-agentizer-plan.md` → `docs/archive/musinsa-agentizer-plan_MERGED.md`
- 수정: `docs/implementation-plan.md`, `README.md`, `docs/README.md`, `docs/project-plan.md`, `docs/company-selection.md`, `docs/archive/README.md`, `docs/archive/plugin-directions_PRE_SELECTION.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- `AGENTS.md`와 `CLAUDE.md`에 `docs/musinsa-agentizer-plan.md` 직접 참조 없음 확인
- 활성 문서의 구현 기준 참조가 `docs/implementation-plan.md` 중심으로 정리되는지 검색 확인
- `git diff --check`, 민감정보 패턴 검색 통과

**판단 근거**
- 두 계획 문서 모두 S1~S8 구현 단계와 플러그인 구조를 설명해 활성 기준으로 함께 두면 다음 작업자가 우선순위를 혼동할 수 있다.
- `implementation-plan.md`는 기존 단계별 계획 문서였으므로 고유 내용을 흡수해 단일 활성 계획으로 만드는 편이 문서 정보 구조에 맞다.

**결과**
- 완료: 구현 계획 단일화 및 중복 계획 보관 완료

---

### W-014 · docs 전용 README 생성 및 선정 전 후보 문서 아카이브
**요청**
- `docs/`만의 README를 생성해 문서 구조를 파악하기 쉽게 정리
- 작업 진행에 더 이상 불필요한 문서가 있다면 `docs/archive/`로 옮겨 폐기 검토

**수행 작업**
- `docs/README.md` 생성: 현재 작업 기준, 활성 문서, 근거·참조 폴더, 구현 단계에서 볼 순서, 아카이브 정책 정리
- `docs/plugin-directions.md`를 `docs/archive/plugin-directions_PRE_SELECTION.md`로 이동해 선정 전 후보 비교·안전성 검토 이력으로 비활성화
- `docs/archive/README.md`를 폐기·비활성 자료 보관소 기준으로 확장하고, 이동한 파일의 비활성화 사유 기록
- 활성 문서(`docs/musinsa-agentizer-plan.md`, `docs/validation-plan.md`)의 `plugin-directions` 참조를 archive 경로 또는 현재 기준 문서로 갱신
- Decisionlog D-008 기록

**변경 파일**
- 생성: `docs/README.md`
- 이동: `docs/plugin-directions.md` → `docs/archive/plugin-directions_PRE_SELECTION.md`
- 수정: `docs/archive/README.md`, `docs/musinsa-agentizer-plan.md`, `docs/validation-plan.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- 활성 문서에서 `docs/plugin-directions.md` 직접 참조가 남지 않는지 검색 확인(남은 옛 경로는 과거 Worklog/Decisionlog 기록뿐)
- `docs/` 파일 목록 확인
- 민감정보 패턴 검색 결과 실제 키·토큰 형식 일치 없음

**판단 근거**
- 무신사 문제 2 확정 이후 실제 구현 기준은 requirements-contract·musinsa-agentizer-plan·implementation-plan·validation-plan에 모였으므로, 후보 비교 문서를 루트에 계속 두면 범위 혼동이 생길 수 있다.

**결과**
- 완료: docs 구조 안내 생성 및 선정 전 후보 문서 비활성화
- 남은 작업: 없음. 다음은 `taxonomy.json`·`schema.json` 작성

---

### W-013 · 무신사 문제 2 공식 확정 및 계획 문서 동기화
**요청**
- 무신사 2번 문제(`상품 데이터 에이전트화 변환기`)를 공식 확정하고 관련 문서 갱신 진행

**수행 작업**
- `Decisionlog.md`에 D-007 `2차 도전 기업·문제 확정` 기록
- `CLAUDE.md`·`AGENTS.md` 0절과 현재 최소 작업 단위를 무신사 문제 2 기준으로 갱신
- `README.md`, `docs/project-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/requirements-contract.md`를 기업 미정 상태에서 무신사 문제 2 확정 상태로 갱신
- `docs/company-selection.md` 최종 확정 상태와 체크리스트 반영
- `docs/musinsa-agentizer-plan.md`의 입력 범위를 “붙여넣기 텍스트 + URL은 출처 메타데이터”로 명확화
- `docs/plugin-directions.md`에 현재 최종 선택 상태 표시

**변경 파일**
- 수정: `CLAUDE.md`, `AGENTS.md`, `README.md`, `Decisionlog.md`, `Worklog.md`
- 수정: `docs/company-selection.md`, `docs/project-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/requirements-contract.md`, `docs/musinsa-agentizer-plan.md`, `docs/plugin-directions.md`

**검증**
- `CLAUDE.md`와 `AGENTS.md` 해시 동일 확인
- “기업 미정/기업 선정 전/기업 확정 후 채움” 잔존 표현 검색 수행(남은 항목은 과거 Worklog 기록 또는 검증 설명 문구)
- 민감정보 패턴 검색 수행: 실제 키·토큰 형식 일치 없음(검증 계획의 일반 용어만 검색됨)

**판단 근거**
- 사용자가 무신사 문제 2를 공식 확정했으므로, 구현 전 기준 계약과 계획 문서가 같은 대상·범위·입력 정책을 가리키도록 동기화해야 한다.
- 자동 크롤링 위험을 피하기 위해 URL은 출처 메타데이터로만 쓰고 실제 실행 입력은 BYO 텍스트로 제한했다.

**결과**
- 완료: 무신사 문제 2 공식 확정 문서 반영
- 남은 작업: taxonomy/schema, SKILL.md, validate/dedup 스크립트 구현 및 더미 픽스처 검증

---

### W-012 · 문서 이동에 따른 참조 경로 정리
**요청**
- 사용자가 `company-selection.md`를 `docs/`로 되돌린 뒤, 다른 파일들의 경로가 괜찮은지 확인 요청

**수행 작업**
- 현재 파일 위치 재확인: `company-selection.md`는 `docs/`로 복귀(이를 참조하던 CLAUDE·AGENTS·README·project-plan·implementation-plan·requirements-contract는 자동으로 정상화됨)
- `docs/company-research_references/`로 이동된 3개 보고서(final-report·codex·review)를 옛 경로로 가리키던 현행 문서만 새 경로로 수정: `docs/archive/README.md`, `docs/company-selection.md`, `Decisionlog.md`(D-004)
- Worklog 과거 기록(W-005·W-007 등)의 옛 경로는 "그 시점 실제 경로"이므로 역사 기록으로 보존(수정하지 않음)

**변경 파일**
- 수정: `docs/archive/README.md`, `docs/company-selection.md`, `Decisionlog.md`, `Worklog.md`
- 이동 반영: `docs/company-research_references/company-selection.md` 삭제 + `docs/company-selection.md` 복귀(사용자 조치 스테이징)

**검증**
- grep으로 현행 문서(Worklog·logs 제외)에 남은 깨진 참조 0건 확인
- 수정된 새 경로 3개가 실제 파일과 매칭됨을 파일 존재로 확인, `docs/company-selection.md` 존재 확인

**판단 근거**
- 활성 문서의 참조는 실제 위치를 가리켜야 문서 정합성(헌법 8절) 유지. 역사 기록(Worklog)은 당시 사실이므로 보존이 정확

**결과**
- 완료: 현행 문서의 참조 경로 정합성 회복
- 남은 작업: 없음(경로 관련). 다음은 MVP 방향 확정

---

### W-011 · 무신사 인터뷰 기반 플러그인 방향 추가(에이전트화 변환기)
**요청**
- 무신사 테크리드 인터뷰(`docs/company-research_references/무신사 인터뷰.txt`)를 기준으로 플러그인 방향을 하나 더 제안하고, `docs/plugin-directions.md`에 정식 추가

**수행 작업**
- 인터뷰 핵심 신호(에이전트-first "첫 번째 도구", 동일 상품 두 번 등록/파편화) 분석
- 무신사 섹션에 **문제 2 · `상품 데이터 에이전트화(化) 변환기`** 추가: 근거·공개자료 가능 이유·플러그인 방향(입력/처리/출력/형태/검증)·"에이전트가 첫 번째 도구가 되는 인과 사슬 6단계"·정직한 경계·end-to-end 시연·문제1 vs 문제2 선택 비교표
- 무신사 섹션 헤더(방향 1개→2개 택일) 및 부기 A 요약 갱신

**변경 파일**
- 수정: `docs/plugin-directions.md`

**검증**
- 추가 방향이 안전 원칙(BYO 입력·공개 taxonomy·더미 검증·크롤링 없음)을 지키는지 확인
- 인터뷰는 자동 전사본이므로 근거 등급을 `[인터뷰 신호 — 원본 공개영상 URL·정확 인용 확인 필요]`로 표기(단정 회피)
- 문제 1(표기 검수기)과의 트레이드오프(근거 검증 강도 vs 주제 정합성)를 비교표로 명시, 택일 후보임을 분명히 함

**판단 근거**
- 인터뷰가 심사자(무신사) 신호이므로 주제 정합성을 높인 방향을 제시하되, 표기 검수기의 근거 강점을 버리지 않도록 택일 구조로 병기

**결과**
- 완료: 에이전트화 변환기 방향 추가 및 선택 기준 정리
- 남은 작업: 무신사 문제 1/2 중 택일(또는 타 2사 포함) → 1개 MVP 확정 → requirements-contract 착수. 인터뷰를 제출 근거로 쓸 경우 원본 공개영상 출처 확보

---

### W-010 · 플러그인·스킬 제작 원칙 헌법 반영
**요청**
- `docs/technical_references/` 검토 결과 중 1번(플러그인 패키징 불변 규칙)과 2번(Skill 작성 원칙)을 헌법에 적용
- 3번은 토큰 소모 우려 검토, 4번은 추가 설명, 5·6번은 당장 보류

**수행 작업**
- `CLAUDE.md`와 `AGENTS.md`를 모두 읽고 동일 상태 확인
- `5.1 Codex 플러그인·스킬 제작 원칙` 절을 두 헌법 파일에 동일하게 추가
- 플러그인 manifest 구조, `.codex-plugin/` 배치, manifest 경로 규칙, plugin name 규칙, skill `name`/`description`, skill 단일 책임, 발동 조건 검증 원칙을 명문화
- Decisionlog D-006 기록

**변경 파일**
- 수정: `CLAUDE.md`, `AGENTS.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- `CLAUDE.md`와 `AGENTS.md`의 SHA-256 해시 동일 확인
- 기술 참조 원문(`Build_plugins.md`, `Agent_Skills.md`)의 필수·권장 규칙만 짧게 반영했는지 대조

**판단 근거**
- 제출 플러그인의 구조 오류와 skill 오발동은 구현 후반에 발견되면 수정 비용이 크므로, 헌법에 최소 불변 규칙으로 고정하는 것이 안전하다.

**결과**
- 완료: 1번·2번 헌법 반영
- 보류: hook 신뢰 규칙, `AGENTS.override.md`, API·MCP 운영 규칙은 실제 사용 시점에 추가 검토

---

### W-009 · 안전성 기준 플러그인 방향 축소 및 검증 데이터 정책 명문화
**요청**
- 안전하지 않은 작업(제3자 UGC 대량 크롤링)이 핵심 전제인 방향은 제외
- 남은 방향을 안전한 입력방식으로 정리

**수행 작업**
- `docs/plugin-directions.md` 개정: "0. 데이터 취득·검증 정책" 신설, 무신사 1-A+1-B를 표기 검수기로 통합, 무신사 1-C·메디테라피 2-C 제외(부기 B에 사유 보존), 남은 방향을 BYO/공개자료 기준으로 재정의, 메디테라피 2-B는 리뷰 의존 제거·자사 페이지 기반으로 재설계
- `docs/validation-plan.md`에 "검증 데이터 정책"(더미 우선 + 소량 공개 인용, 지식원은 공식·공공 자료, BYO 입력, 제3자 UGC 대량 크롤링 금지) 추가
- Decisionlog D-005 기록

**변경 파일**
- 수정: `docs/plugin-directions.md`, `docs/validation-plan.md`, `Decisionlog.md`, `Worklog.md`

**검증**
- 남은 방향(무신사 1 / 메디테라피 2 / 마이리얼트립 3)이 모두 공개 소스·더미로 시연 가능한지 항목별 확인
- 제외 방향의 사유(크롤링 법적 위험: 저작권·DB권·부정경쟁방지법·개인정보보호법·이용약관)를 문서에 명시했는지 확인
- plugin-directions.md와 validation-plan.md의 데이터 정책 서술이 상호 모순 없는지 대조

**판단 근거**
- 위험 요소는 "방향"이 아니라 "데이터 수집 방식"이므로, 방식만 안전화하면 대부분 성립. 핵심이 위험한 방향만 제외하고 안전한 방향은 유지하는 것이 과제 요건(공개·검증 가능·재현 가능)과 법적 안전성을 함께 충족

**결과**
- 완료: 방향 축소·재설계, 검증 데이터 정책 명문화
- 남은 작업: 1개 사·1개 문제(MVP) 확정 → Decisionlog 기록 → requirements-contract 등 구현 문서 착수

---

### W-008 · 후보 3사(무신사·메디테라피·마이리얼트립) 문제 3개씩 + 플러그인 방향 정리
**요청**
- 채널톡·삼일PwC 제외
- 무신사·메디테라피·마이리얼트립 순으로, 외부 공개 자료만으로 AX(AI)로 해결·개선·제안 가능한 문제 3개씩과 각 플러그인 방향 제시

**수행 작업**
- `docs/company-research-final-report.md`에서 각 사의 검증된 공개 사실만 추려 문제 도출(미검증 추정은 문제로 세우지 않음)
- 각 문제마다 "공개자료만으로 가능한 이유"(플러그인 입력이 되는 공개 소스)와 Codex 플러그인 방향(입력→처리→출력·형태) 정리
- `docs/plugin-directions.md` 생성
- 후보 5→3 축소를 Decisionlog D-004에 기록

**변경 파일**
- 생성: `docs/plugin-directions.md`
- 수정: `Decisionlog.md`(D-004), `Worklog.md`

**검증**
- 각 문제의 근거가 최종 보고서의 `[검증됨]`·`[교차확인]` 항목과 일치하는지 대조. 공개 소스만으로 시연 가능하도록 설계했는지 항목별 확인.
- 무신사(표기 정합성/고시항목/평판신호), 메디테라피(광고규정/전환·콘텐츠/글로벌리뷰), 마이리얼트립(문의 triage/규정 네비/도움말 감사) 각 3개 도출.

**판단 근거**
- 과제 규정상 근거는 공개·검증 가능해야 하고 심사자가 재현 가능해야 하므로, 내부 비공개 데이터 없이 공개 소스만으로 동작·시연되는 문제로 한정하는 것이 안전

**결과**
- 완료: 3사 각 3개 문제·플러그인 방향 정리
- 남은 작업: 사용자가 1개 사·1개 문제(MVP)를 확정 → Decisionlog 기록 → requirements-contract 등 구현 문서 착수

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
