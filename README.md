# Musinsa Product Agentizer

무신사 문제 2 `상품 데이터 에이전트화 변환기`를 위한 Codex 플러그인입니다. 사용자가 직접 붙여넣은 한국어 패션 상품 상세 텍스트를 AI 에이전트가 질의, 필터, 설명에 사용할 수 있는 구조화 상품 JSON으로 변환합니다.

## 제출 개요

- 선택 기업: 무신사
- 선택 문제: 상품 데이터 에이전트화 변환기
- 플러그인 이름: `musinsa-product-agentizer`
- 플러그인 루트: `src/`
- MVP 범위: 아우터(`outer`), 상의(`top`)
- 입력 방식: 사용자가 직접 붙여넣은 상품 상세 텍스트만 사용
- 출력 방식: schema-valid 구조화 JSON, taxonomy 매핑, 누락/모호 정보, 에이전트 질의 descriptor, 중복 후보

## 문제 배경

공개 자료 기준으로 무신사는 AI 에이전트와 상품 데이터 통합을 중요한 방향으로 보고 있습니다. 무신사 테크리드 인터뷰 공개영상에서는 기술 파편화, 동일 상품 중복 등록, 패션 질의에서 에이전트가 사용하는 첫 번째 도구가 되고 싶다는 방향성이 확인됩니다.

- 핵심 출처: https://www.youtube.com/watch?v=OLAWeIuiD5Y
- 작업 저장소에는 전사 근거와 선정 결정 기록을 별도 보관했습니다.

이 플러그인은 상품 상세페이지의 비정형 텍스트를 에이전트가 재사용하기 쉬운 정규화 데이터로 바꾸는 데 집중합니다. 상품정보 표기 규정의 적법/위법 판정은 범위 밖입니다.

## 구성

```text
src/
├── .codex-plugin/
│   └── plugin.json
└── skills/
    └── product-agentizer/
        ├── SKILL.md
        ├── references/
        │   ├── schema.json
        │   └── taxonomy.json
        └── scripts/
            ├── dedup.py
            └── validate.py
README.md
logs/
tests/fixtures/
tools/
```

- `src/.codex-plugin/plugin.json`: Codex 플러그인 manifest
- `src/skills/product-agentizer/SKILL.md`: Codex가 상품 텍스트를 구조화하는 절차
- `schema.json`: 출력 JSON 구조와 필수 필드
- `taxonomy.json`: 아우터/상의 MVP의 표준 카테고리, 소재, 색상, 계절, TPO vocabulary
- `validate.py`: 출력 JSON의 schema와 taxonomy 정합성 검증
- `dedup.py`: 구조화 상품 JSON 간 중복 후보 산출
- `logs/`: AI와 주고받은 원본 대화 로그
- `tests/fixtures/`: 재현 가능한 합성·Codex subset·공개 snippet 검증 데이터
- `tools/`: 확장 fixture 생성과 검증 결과 스냅샷 생성 도구

## 기능

1. 상품 상세 텍스트에서 상품명, 카테고리, 소재, 핏, 색상, 계절, TPO, 관리, 사이즈 정보를 추출합니다.
2. 자유 표기를 `taxonomy.json`의 표준 id로 매핑합니다.
3. 소재 혼용률은 입력에 숫자가 명시된 경우에만 `explicit`으로 기록합니다.
4. 혼용률이 없거나 모호하면 `missing` 또는 `ambiguous`로 표시하고 `quality`에 남깁니다.
5. 에이전트 검색과 설명에 쓰기 쉬운 `agent_descriptor`를 생성합니다.
6. 여러 상품을 구조화한 뒤 `dedup.py`로 중복 후보를 찾을 수 있습니다.

## 사용 범위와 금지 범위

사용할 수 있는 입력:

- 사용자가 직접 붙여넣은 상품 상세 텍스트
- 출처 기록용 공개 URL과 제목
- 합성 더미 검증 데이터

사용하지 않는 입력:

- 플러그인이 직접 가져온 URL, 크롤링, scraping 결과
- 로그인이나 권한이 필요한 내부 데이터
- 실제 고객정보, 주문정보, 계좌정보, API 키, 토큰
- 제3자 리뷰나 커뮤니티 글의 대량 수집 데이터

범위 밖 작업:

- 상품정보 표기 규정의 법적 적합/부적합 판정
- 자동 크롤러
- 추천 랭킹, 가격, 재고, 트렌드 예측
- MVP 범위 밖 카테고리의 완전 변환

## Codex에서 사용하는 방법

제출 플러그인의 루트는 `src/`입니다. 개발 저장소에는 로컬 테스트용 repo marketplace도 포함되어 있습니다. 제출 zip만 받은 경우에는 `src/`를 플러그인 루트로 보고, 로컬 marketplace를 직접 만들 때 `source.path`를 `./src`로 지정하면 됩니다.

```powershell
codex plugin marketplace add .
codex plugin list --available
codex plugin add musinsa-product-agentizer@ax-2nd-local
```

설치 후 새 Codex 스레드에서 아래처럼 요청합니다.

```text
product-agentizer를 사용해 아래 상품 상세 텍스트를 schema-valid JSON으로 변환해 주세요.
URL은 출처 메타데이터로만 기록하고 자동으로 열지 마세요.

상품명: ...
소재: ...
핏: ...
세탁: ...
```

전역 Codex 설정에 기존 marketplace 문제가 있으면, 로컬 검증은 임시 `CODEX_HOME`에서 수행할 수 있습니다. 실제 S6 검증 절차와 결과는 `docs/reports/s6-codex-cli-report.md`에 기록했습니다.

## 검증 명령

새 Python 환경에서는 `jsonschema`가 필요합니다.

```powershell
python -m pip install jsonschema
```

개발 저장소 기준 검증 명령은 아래와 같습니다.

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
python src\skills\product-agentizer\scripts\dedup.py tests\fixtures\dedup\sample_products.json --pretty
python tests\evaluate_product_agentizer.py --pretty
python tools\run_expanded_validation.py
python tools\run_full_page_dummy_validation.py
python tools\generate_size_info_pattern_fixtures.py
python tools\run_full_page_codex_smoke20_cli.py --fixture size_info_patterns --timeout 3600
python tools\run_size_info_pattern_validation.py
```

Codex가 생성한 JSON은 파일로 저장한 뒤 다음처럼 검증합니다.

```powershell
python src\skills\product-agentizer\scripts\validate.py <codex-output.json> --pretty
```

## 검증 결과 요약

- schema 정상 fixture 2건 통과
- 필수 필드 누락, 지원 범위 밖 카테고리, 소재 혼용률 상태 불일치 fixture는 기대대로 실패
- 더미 fixture 5건 기준 속성 micro precision: 98.55%
- 더미 fixture 5건 기준 속성 micro recall: 88.31%
- 더미 중복/비중복 쌍 기준 dedup accuracy: 100.00% (10/10)
- Codex CLI 실제 실행에서 `outer_down_layerpiece` 입력을 구조화 JSON으로 변환했고 `validate.py` 검증을 통과
- S6 Codex 출력은 직전 보완 대상이던 `goose_down`, `khaki`, `travel`, `여유 있는 암홀` 정보를 유지
- S7.5 확장 합성 expected 100건은 schema-valid 100%(100/100), self-check precision/recall 100.00%
- S7.5 Codex subset 20건 actual은 schema-valid 100%(20/20), micro precision 95.52%, micro recall 95.85%
- S7.5 Codex subset의 `detail_type`은 historical actual 보존을 위해 expected/actual 모두 `null`로 둬 precision/recall이 `not_applicable`이며, actual은 schema `0.2.0` 호환을 위해 `schema_version`과 `detail_type: null`만 추가한 마이그레이션본
- S7.5 dedup 검증은 합성 20/20, Codex subset 4/4, 실제 공개 snippet 5/5 모두 통과했고 cross-category high-confidence false duplicate는 0건
- S7.5 실제 공개 상품 snippet 10건은 actual schema-valid 100%(10/10), 자동 fetch 0건, 법적 적합/부적합 판정 0건으로 확인
- S7.7 실제 페이지형 합성 더미 300건과 대표 subset 50건을 보존했고, 50건 subset은 격리 workspace에서 실제 Codex CLI로 실행
- S7.7 50건 subset 최종 결과는 schema-valid 100%(50/50), micro precision 99.74%, micro recall 99.74%, `detail_type` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%
- S7.8 `size_info` 표기 패턴 합성 fixture 48건은 격리 workspace에서 실제 Codex CLI actual을 생성했고, schema-valid 100%(48/48), `size_info` precision/recall 100.00%, TP/FP/FN 97/0/0, `recommendation_noise` false positive 0건으로 확인

이 수치는 무신사 전체 상품 카탈로그 성능이 아니라, 합성 fixture, 보존된 Codex actual output, 짧은 공개 snippet sanity check로 확인한 MVP 검증 결과입니다. 상세 재현 절차와 원본 결과는 `docs/reports/s7-expanded-validation-report.md`, `docs/reports/s7-expanded-validation-results.json`, `docs/reports/s7-7-full-page-dummy-validation-report.md`, `docs/reports/s7-7-full-page-dummy-validation-results.json`, `docs/reports/s7-8-size-info-coverage-report.md`, `docs/reports/s7-8-size-info-coverage-results.json`에 보관했습니다.

## 질문 5문항 답변

### 1. 무엇을, 누가, 어떤 상황에서 쓰나요?

이 플러그인은 패션 상품 상세 텍스트를 AI 에이전트가 질의 가능한 구조화 상품 JSON으로 바꾸는 도구입니다. 무신사처럼 많은 브랜드와 상품 데이터를 다루는 패션 플랫폼의 상품 운영자, 데이터 담당자, 에이전트 커머스 실험 담당자, 또는 심사자가 사용할 수 있습니다. 상품 상세페이지 텍스트를 붙여넣으면 에이전트가 검색, 필터, 비교, 설명에 쓸 수 있는 속성 데이터로 정리합니다.

### 2. 왜 이 문제를 선택했나요?

무신사 테크리드 인터뷰에서 기술 파편화, 동일 상품 중복 등록, 에이전트가 패션 질문에 사용할 첫 번째 도구가 되고 싶다는 방향성이 공개적으로 확인됐기 때문입니다. 상품 상세 텍스트는 사람에게는 읽히지만 AI 에이전트가 일관되게 질의하기에는 비정형성이 큽니다. 그래서 아우터와 상의 MVP로 범위를 좁혀, 공개 자료와 더미 fixture만으로 안전하게 구현하고 검증할 수 있는 상품 데이터 에이전트화 문제를 선택했습니다.

### 3. 플러그인은 어떻게 작동하나요?

Codex가 `product-agentizer` skill을 사용해 붙여넣은 상품 텍스트에서 속성을 추출합니다. 추출한 값은 `taxonomy.json`의 표준 id로 정규화하고, `schema.json`에 맞는 JSON으로 만듭니다. 소재 혼용률은 입력 근거가 있는 경우에만 숫자로 기록하고, 누락되거나 모호한 정보는 `quality.missing_fields`와 `quality.ambiguous_fields`에 남깁니다. 생성된 JSON은 `validate.py`로 검증할 수 있고, 여러 상품 JSON은 `dedup.py`로 중복 후보를 계산할 수 있습니다.

### 4. AI를 어떻게 활용했나요?

AI는 공개 자료 조사, 후보 기업 비교, 문제 선정, 요구사항 계약 문서 작성, taxonomy/schema 설계, skill 지침 작성, 검증 스크립트 작성, 평가 fixture 설계, Codex CLI 실행 시연, README 작성에 사용했습니다. 중요한 결정, 작업 이력, 문제 해결 이력은 작업 저장소의 문서로 관리했습니다. AI와 주고받은 대화 로그는 과제 규정에 맞게 원본 그대로 `logs/`에 보관합니다.

### 5. 어떻게 검증했나요?

검증은 여섯 층으로 수행했습니다. 첫째, `schema.json`과 `validate.py`로 정상 JSON은 통과하고 오류 fixture는 실패하는지 확인했습니다. 둘째, 더미 상품 5건의 expected/predicted JSON을 비교해 속성 precision/recall을 산출하고, 중복쌍 10개에서 `dedup.py`의 정확도를 확인했습니다. 셋째, 로컬 Codex CLI에서 실제로 상품 텍스트를 구조화 JSON으로 변환하고, 그 출력이 `validate.py`를 통과하는지 확인했습니다. 넷째, S7.5에서 합성 100건, Codex subset 20건, 실제 공개 snippet 10건의 입력·expected·actual·평가 결과·실행 명령·hash를 보존해 재실행 가능하게 만들었습니다. 다섯째, S7.7에서 실제 페이지형 합성 더미 300건과 대표 subset 50건을 만들고, 50건은 expected fixture가 없는 격리 workspace에서 실제 Codex CLI로 재실행해 schema-valid 50/50, micro precision/recall 99.74%, size_info precision/recall 100.00%를 확인했습니다. 여섯째, S7.8에서 실제 페이지에서 나올 법한 `size_info` 표기 패턴 48건을 별도 합성 fixture로 만들고, 실제 Codex CLI actual 기준 schema-valid 48/48, `size_info` precision/recall 100.00%, 추천·후기 노이즈 false positive 0건을 확인했습니다. 자동 크롤링, 내부 데이터, 비밀정보는 사용하지 않았습니다.

## 한계

- MVP는 아우터와 상의만 지원합니다.
- 실제 무신사 내부 카탈로그나 판매 데이터는 사용하지 않았습니다.
- 공개 상품 전체나 실제 내부 카탈로그에 대한 대규모 성능 검증은 수행하지 않았고, 실제 공개 샘플은 짧은 snippet 10건 sanity check로 제한했습니다.
- 상품정보 표기 규정 위반 여부를 법적으로 판단하지 않습니다.
- URL은 출처 메타데이터일 뿐이며 플러그인이 자동으로 열지 않습니다.
