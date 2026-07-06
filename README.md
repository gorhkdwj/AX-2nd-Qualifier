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

## 제출물 구성

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
```

- `src/.codex-plugin/plugin.json`: Codex 플러그인 manifest
- `src/skills/product-agentizer/SKILL.md`: Codex가 상품 텍스트를 구조화하는 절차
- `schema.json`: 출력 JSON 구조와 필수 필드
- `taxonomy.json`: 아우터/상의 MVP의 표준 카테고리, 소재, 색상, 계절, TPO vocabulary
- `validate.py`: 출력 JSON의 schema와 taxonomy 정합성 검증
- `dedup.py`: 구조화 상품 JSON 간 중복 후보 산출
- `logs/`: AI와 주고받은 원본 대화 로그

개발 저장소에는 제출물 외에 `docs/`, `tests/fixtures/`, `tools/`가 있습니다. 이 파일들은 검증 재현과 작업 감사 추적을 위한 내부 자료이며, 최종 제출 zip의 필수 구성은 `src/`, `README.md`, `logs/`입니다.

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

아래 명령은 `docs/`, `tests/`, `tools/`가 함께 있는 개발 저장소 기준입니다. 최종 제출 zip만 받은 경우에는 Codex 출력 JSON을 저장한 뒤 `src/skills/product-agentizer/scripts/validate.py`로 개별 검증하는 흐름을 사용합니다.

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
- 필수 필드 누락, 지원 범위 밖 카테고리, 세부 유형 부모 불일치, 소재 혼용률 상태 불일치, `material_part` 누락, `material_part` 허위 표시 fixture는 기대대로 실패(각 fixture는 표적 규칙 하나만 위반하도록 격리)
- 더미 fixture 5건 기준 속성 micro precision: 98.68%
- 더미 fixture 5건 기준 속성 micro recall: 89.29%
- 더미 중복/비중복 쌍 기준 dedup accuracy: 100.00% (10/10)
- Codex CLI 실제 실행에서 `outer_down_layerpiece` 입력을 구조화 JSON으로 변환했고 `validate.py` 검증을 통과
- S6 Codex 출력은 직전 보완 대상이던 `goose_down`, `khaki`, `travel`, `여유 있는 암홀` 정보를 유지
- S7.5 확장 합성 expected 100건은 schema-valid 100%(100/100), self-check precision/recall 100.00%
- S7.5 Codex subset 20건 actual은 schema-valid 100%(20/20), micro precision 97.93%, micro recall 95.95%
- S7.5 Codex subset의 `detail_type`은 historical actual 보존을 위해 expected/actual 모두 `null`로 둬 precision/recall이 `not_applicable`이며, actual은 schema `0.2.0` 호환을 위해 `schema_version`과 `detail_type: null`만 추가한 마이그레이션본
- S7.5 dedup 검증은 합성 20/20, Codex subset 4/4, 실제 공개 snippet 5/5 모두 통과했고 cross-category high-confidence false duplicate는 0건
- S7.5 실제 공개 상품 snippet 10건은 actual schema-valid 100%(10/10), 탐색 비교 micro precision 65.48%, micro recall 77.46%, 자동 fetch 0건, 법적 적합/부적합 판정 0건으로 확인
- S7.7 실제 페이지형 합성 더미 300건과 대표 subset 50건을 보존했고, 50건 subset은 격리 workspace에서 실제 Codex CLI로 실행
- S7.7 50건 subset 최종 결과는 schema-valid 100%(50/50), micro precision 100.00%, micro recall 100.00%, `detail_type` precision/recall 100.00%, `materials` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%
- 다만 이 50건 subset의 `size_info`는 처음 실행에서 precision 59.65%, recall 33.01%로 낮게 나왔고, 그 실패 사례를 보고 SKILL의 `size_info` 추출 절차를 보강한 뒤 **같은 50건 subset을 재실행해 얻은 결과가 위 100%**다. 즉 이 수치는 신규 blind 테스트가 아니라 같은 subset을 개선 후 재측정한 값이므로, 미지의 신규 입력에 대한 일반화 성능 보장이 아니라 개선 절차가 목표 패턴을 커버함을 확인한 결과로 해석해야 한다.
- S7.8 `size_info` 표기 패턴 합성 fixture 48건은 격리 workspace에서 실제 Codex CLI actual을 생성했고, schema-valid 100%(48/48), `size_info` precision/recall 100.00%, TP/FP/FN 97/0/0, `recommendation_noise` false positive 0건으로 확인

이 수치는 무신사 전체 상품 카탈로그 성능이 아니라, 합성 fixture, 보존된 Codex actual output, 짧은 공개 snippet sanity check로 확인한 MVP 검증 결과입니다. 특히 S7.7의 100% 수치는 실제 상품 페이지를 저장하지 않고 페이지형 입력을 합성해 재현한 검증 결과이며, 실제 운영 전체 카탈로그의 보장 수치가 아닙니다. 또한 `dedup.py`의 속성별 가중치와 판정 임계값은 실제 무신사 운영 데이터로 학습·튜닝한 최종 수치가 아니라, 설명 가능한 도메인 직관으로 정한 **MVP 휴리스틱 baseline**입니다. 운영 적용 시에는 사람이 라벨링한 상품쌍으로 precision/recall과 오탐·미탐을 측정하며 가중치·임계값을 조정해야 합니다. 상세 재현 절차와 원본 결과는 개발 저장소의 `docs/reports/s7-expanded-validation-report.md`, `docs/reports/s7-expanded-validation-results.json`, `docs/reports/s7-7-full-page-dummy-validation-report.md`, `docs/reports/s7-7-full-page-dummy-validation-results.json`, `docs/reports/s7-8-size-info-coverage-report.md`, `docs/reports/s7-8-size-info-coverage-results.json`에 보관했습니다.

## 질문 5문항 답변

### 1. 무엇을, 누가, 어떤 상황에서 쓰나요?

Musinsa Product Agentizer는 사용자가 붙여넣은 패션 상품 상세 텍스트를 Codex가 검색·필터·비교에 쓸 수 있는 표준 JSON으로 바꾸는 플러그인입니다. 무신사 상품 운영자, 카탈로그 데이터 담당자, AI 에이전트 실험 담당자가 신규 상품 등록, 기존 상품 정보 정비, 중복 후보 확인, 패션 질의 응답용 데이터 준비 상황에서 사용합니다. 상품 상세페이지에는 상품명, 소재, 색상, 사이즈, 관리법, 착용 맥락이 문장·표·마케팅 문구로 섞여 있어 에이전트가 "봄에 입는 블랙 재킷", "실측 사이즈가 있는 상의", "같은 상품으로 보이는 등록건"처럼 일관되게 질의하기 어렵습니다. 이 플러그인은 그 비정형 텍스트를 category/subcategory/detail_type, materials, colors, seasons, size_info, quality 메모로 정리해 막힌 지점을 풀어 줍니다.

### 2. 왜 이 문제를 선택했나요?

이 문제를 고른 이유는 무신사가 공개 인터뷰에서 AI 에이전트와 상품 데이터 통합을 중요한 방향으로 말했고, 여러 서비스·플랫폼 확장 과정에서 기술 파편화와 동일 상품 중복 등록 부담을 언급했기 때문입니다. 실제로 패션 커머스의 상품 상세정보는 사람에게 보여 주기 위한 문장과 표로 구성되어, 직원은 상품 속성을 표준 항목으로 다시 정리해야 하고 고객 또는 에이전트는 자연어 질문을 해도 정확한 필터·비교 근거를 얻기 어렵습니다. 예를 들어 소재 혼용률, 부위별 소재, 계절, 핏, 실측 사이즈가 상품마다 다른 표현으로 적혀 있으면 AI가 같은 기준으로 답하기 어렵습니다. 따라서 "상품 데이터를 에이전트가 재사용 가능한 구조로 바꾸는 일"을 무신사 문제 2의 핵심으로 잡았습니다.

출처: https://www.youtube.com/watch?v=OLAWeIuiD5Y

### 3. 플러그인은 어떻게 작동하나요?

사용자가 상품 상세 텍스트를 붙여넣으면 Codex가 `product-agentizer` skill을 호출해 상품명, category, subcategory, detail_type, 소재, 색상, 계절, TPO, 관리법, size_info를 추출합니다. 분류와 표준값은 `taxonomy.json`의 3단계 구조(category → subcategory → detail_type)와 alias를 기준으로 맞추고, 최종 출력은 `schema.json` 계약에 맞춘 JSON입니다. 소재 혼용률은 입력에 숫자가 명시된 경우에만 `explicit`으로 기록하고, "터치", "블렌드", "혼용"처럼 비율이 없는 표현은 추정하지 않고 `missing` 또는 `ambiguous`로 남깁니다. 부위가 불명확한 소재는 `part: unknown`으로 두고 `quality.missing_fields`에 `material_part`를 기록합니다. 생성 JSON은 `validate.py`가 schema, taxonomy, detail_type 부모 관계, material_part 양방향 규칙을 확인합니다. 여러 상품 JSON은 `dedup.py`가 소재·색상·핏·계절·TPO·관리·제목 유사도를 가중 합산해 중복 후보를 냅니다. URL은 출처 메타데이터일 뿐 자동으로 열지 않고, 법적 적합/부적합 판정이나 추천 랭킹은 수행하지 않습니다.

### 4. AI를 어떻게 활용했나요?

AI에는 공개 자료 조사, 후보 기업 비교, 문제 정의 초안, 요구사항 계약, taxonomy/schema 설계, SKILL 작성, validator·dedup 스크립트, fixture 생성, Codex CLI 검증, README·보고서 초안, Claude Code 교차검증을 맡겼습니다. 직접 판단한 부분은 무신사 문제 2 확정, MVP를 outer/top으로 제한한 점, 자동 크롤링·비공개 데이터·법적 적합성 판정을 제외한 점, 실제 공개 상품 전체 복사 대신 짧은 공개 snippet과 합성 페이지형 데이터로 검증한 점입니다. 막혔던 지점은 size_info 누락, material_part 단방향 검증, invalid fixture 이중 함정, worktree 로그 분산, PowerShell UTF-8 검사 오탐이었습니다. 해결은 SKILL 지침 보강, validator 규칙 양방향화, fixture 격리, 로그 source-separated 통합, Python JSON 파서 재검증으로 진행했습니다. 받아들이지 않은 제안은 로컬 전용 비공개 검증 데이터 보존, 실제 사이트 자동 수집, size_info schema 객체화 즉시 적용입니다. 각각 윤리·제출 정합성·일정 리스크 때문에 제외하거나 후속 계획으로만 남겼습니다.

### 5. 어떻게 검증했나요?

정상 예시는 "린넨 블레이저, 겉감 린넨 55% 레이온 45%, 블랙, 봄가을, M 어깨 45cm" 같은 입력입니다. 플러그인은 이를 outer/jacket/suit_blazer_jacket, materials explicit, colors black, seasons spring·fall, size_info로 구조화하고 `validate.py`가 통과시킵니다. 비슷한 블레이저 2건은 `dedup.py`에서 duplicate 후보로 잡았습니다. 예외 상황도 확인했습니다. category가 bottom이면 범위 밖이라 차단하고, detail_type이 부모 subcategory와 맞지 않으면 실패합니다. 소재 part가 unknown인데 `material_part`가 없거나, 반대로 모두 알려졌는데 `material_part`를 허위로 넣어도 차단합니다. 검증은 기본 5건 P 98.68%/R 89.29%/dedup 100%, S7.7 페이지형 합성 50건과 S7.8 size_info 48건에서 실제 Codex CLI actual 기준 100%를 확인했습니다. 다만 100%는 합성 fixture 기준이며 무신사 전체 운영 성능 보장은 아닙니다. 실제 공개 snippet은 정보 부족 리스크를 보는 sanity check로 낮은 탐색 지표도 기록했습니다.

## 한계

- MVP는 아우터와 상의만 지원합니다.
- 실제 무신사 내부 카탈로그나 판매 데이터는 사용하지 않았습니다.
- 공개 상품 전체나 실제 내부 카탈로그에 대한 대규모 성능 검증은 수행하지 않았고, 실제 공개 샘플은 짧은 snippet 10건 sanity check로 제한했습니다.
- 상품정보 표기 규정 위반 여부를 법적으로 판단하지 않습니다.
- URL은 출처 메타데이터일 뿐이며 플러그인이 자동으로 열지 않습니다.
