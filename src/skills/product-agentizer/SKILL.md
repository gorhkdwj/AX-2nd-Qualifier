---
name: product-agentizer
description: "붙여넣은 한국어 패션 상품 상세 텍스트를 Musinsa outer/top MVP용 schema-valid, agent-query-ready structured product JSON으로 변환합니다. Use for taxonomy mapping, missing/ambiguous field reporting, material-ratio evidence handling, and duplicate-candidate preparation; do not use for legal label-compliance audits, automatic URL fetching/crawling, recommendation ranking, or private/internal data."
---

# Product Agentizer

이 스킬은 사용자가 직접 붙여넣은 한국어 패션 상품 상세 텍스트를 AI 에이전트가 질의, 필터, 설명에 사용할 수 있는 구조화 상품 JSON으로 변환합니다.

## 범위

사용자가 무신사 상품 데이터 에이전트화 변환기 MVP를 위해 패션 상품 상세 텍스트를 구조화 상품 데이터로 바꾸려 할 때 이 스킬을 사용합니다.

지원 카테고리는 다음 2개입니다.
- `outer`
- `top`

다음 작업에는 이 스킬을 사용하지 않습니다.
- 상품정보 표기 규정의 적법/위법 판정 또는 법적 검수
- URL 자동 fetch, scraping, crawling, 대량 수집
- 비공개, 로그인 필요, 내부, 고객, 주문, 판매, 카탈로그 데이터 처리
- 추천 랭킹, 가격, 재고, 트렌드 예측
- bottom, dress, shoes, bag, beauty, kids, accessory 등 MVP 범위 밖 카테고리 변환. 단, 범위 밖임을 표시하는 것은 가능합니다.

URL은 출처 메타데이터일 뿐입니다. Never fetch a URL automatically. 사용자가 직접 붙여넣은 상품 텍스트만 사용합니다.

## 참조 파일

최종 구조화 출력을 만들기 전에 아래 파일을 기준으로 삼습니다.
- `references/taxonomy.json`: 지원 카테고리, 별칭, vocabulary id, 소재 부위, 혼용률 상태 값
- `references/schema.json`: 필수 출력 구조와 허용 값

JSON 구조는 schema가 기준입니다. 정규화 id와 alias 매핑은 taxonomy가 기준입니다.

## 입력

입력은 자유 텍스트이거나 아래와 비슷한 JSON 형태일 수 있습니다.

```json
{
  "product_text": "사용자가 직접 붙여넣은 상품 상세 텍스트",
  "source_url": "선택: 출처 기록용 URL. 자동으로 열지 않음",
  "source_title": "선택: 상품명 또는 페이지 제목",
  "category_hint": "선택: outer | top",
  "locale": "ko-KR"
}
```

사용자가 일반 텍스트만 제공하면 그 텍스트를 `product_text`로 취급합니다.

## 작업 절차

1. 입력이 사용자가 직접 붙여넣은 상품 상세 텍스트인지 확인합니다.
   - 사용자가 URL을 열어 가져오라고 요청해도 열지 않습니다. 상품 상세 텍스트를 붙여넣어 달라고 하거나, 이미 제공된 텍스트만 사용합니다.
   - 입력에 비밀정보, 고객정보, 내부정보가 포함된 것으로 보이면 중단하고 안전 문제를 보고합니다.

2. 카테고리를 판정합니다.
   - `category_hint`가 있고 텍스트와 모순되지 않으면 우선 사용합니다.
   - 힌트가 없으면 `outer`와 `top` 중에서만 추론합니다.
   - MVP 범위 밖 상품이면 `quality.out_of_scope`를 `true`로 설정하고, 안전하게 판단 가능한 값만 제한적으로 채웁니다. 범위 제한은 `agent_descriptor.explainable_reasons`에 설명합니다.

3. 입력 텍스트의 근거에 기반해 상품 속성을 추출합니다.
   - `title`
   - `category`
   - `subcategory`
   - `materials`
   - `fit`
   - `colors`
   - `seasons`
   - `tpo_tags`
   - `care`
   - `size_info`

4. 추출한 값을 `references/taxonomy.json`으로 정규화합니다.
   - 예를 들어 `자켓`, `블레이저`는 taxonomy 기준 `jacket`으로 매핑합니다.
   - JSON 값에는 표시명보다 taxonomy id를 우선 사용합니다.
   - taxonomy 또는 schema enum에 없는 값은 새로 만들지 않습니다.
   - 더 구체적인 alias가 있으면 넓은 색상/맥락보다 구체 id를 우선합니다. 예를 들어 `카키`, `올리브`는 `green`이 아니라 `khaki`로 매핑합니다.

5. 소재와 혼용률은 엄격하게 처리합니다.
   - 각 소재에는 반드시 `part`, `name`, `ratio`, `ratio_status`, `evidence`를 포함합니다.
   - 입력 텍스트에 해당 소재와 부위의 숫자 혼용률이 직접 표시된 경우에만 `ratio_status: "explicit"`을 사용합니다.
   - `ratio_status`가 `explicit`이면 `ratio`는 0~100 사이 숫자여야 합니다.
   - 소재명은 있지만 숫자 혼용률이 없으면 `ratio: null`, `ratio_status: "missing"`으로 두고 `quality.missing_fields`에 `material_ratio`를 추가합니다.
   - "혼방", "터치", "느낌", "라이크"처럼 소재감만 암시하는 표현이면 `ratio: null`, `ratio_status: "ambiguous"`로 두고 `quality.ambiguous_fields`에 `material_ratio`를 추가합니다.
   - 부위가 다르면 `shell`, `lining`, `fill`, `rib`, `pocket`, `trim`, `unknown` 중 하나로 나누어 기록합니다.
   - 한 문장에 여러 소재나 혼용률이 함께 나오면 모두 별도 `materials[]` 항목으로 분리합니다. 예: `충전재 덕다운 80%, 구스다운 20%`는 `fill:duck_down:80`과 `fill:goose_down:20`으로 나눕니다.
   - `겉감`, `안감`, `충전재`, `립`, `포켓`, `배색` 같은 부위 단어가 먼저 나오면, 다음 부위 단어가 나오기 전까지 같은 구간의 모든 소재에 그 `part`를 적용합니다.
   - `린넨 터치`, `레이온 블렌드`처럼 정확한 숫자 혼용률이 없는 소재 표현은 소재 후보를 누락하지 말고 각각 `ratio: null`, `ratio_status: "ambiguous"`로 기록합니다.
   - Never estimate fabric ratios. Never judge legal compliance.

6. 복합 표현 누락을 점검합니다.
   - 계절: `봄여름`은 `spring`, `summer`를 모두 기록하고, `가을겨울`은 `fall`, `winter`를 모두 기록합니다.
   - TPO: `이너`, `레이어드`, `겹쳐입기`는 `layering`; `여행`, `여행용`, `휴가`는 `travel`; `포멀`, `격식`, `세미포멀`은 `formal`로 매핑합니다.
   - 사이즈/착용 정보: `총장`, `어깨`, `가슴둘레`, `소매`, `암홀`, `밑단`, `기장`, `여유`처럼 치수나 착용감을 설명하는 구절은 `size_info`에 보존합니다.
   - 한 상품 안에서 소재, 계절, TPO, 사이즈 단서가 쉼표로 나열되면 첫 항목만 기록하지 말고 목록 전체를 다시 훑습니다.

7. `agent_descriptor`를 작성합니다.
   - `search_summary`: 에이전트 검색에 유용한 짧은 한국어 요약 1문장
   - `query_tags`: 이 상품이 대응할 수 있는 자연어 한국어 질의 표현
   - `explainable_reasons`: 추출 근거와 taxonomy 매핑에 기반한 짧은 한국어 설명

8. `quality`를 작성합니다.
   - 입력에 없는 중요 속성은 `missing_fields`에 넣습니다.
   - 불확실한 속성은 `ambiguous_fields`에 넣습니다.
   - 근거가 얼마나 명확한지에 따라 `confidence`를 `high`, `medium`, `low` 중 하나로 설정합니다.
   - 지원 범위 밖 상품이면 `out_of_scope: true`를 사용합니다.

9. 최종 출력 전에 검증합니다.
   - 최종 객체는 `references/schema.json`과 일치해야 합니다.
   - `scripts/validate.py`가 존재하면 최종 JSON에 대해 실행하고, 통과한 뒤 완료를 보고합니다.
   - 아직 검증 스크립트가 없다면 schema 핵심 요구사항을 수동으로 확인하고, 스크립트 검증은 pending이라고 명시합니다.

10. 배치 입력이나 중복 감지 요청이 있으면 다음 순서를 따릅니다.
   - 먼저 상품별로 schema-valid 구조화 JSON을 하나씩 만듭니다.
   - `scripts/dedup.py`가 존재하고 사용자가 중복 감지를 요청했다면 구조화 상품 JSON 목록에 대해 실행합니다.
   - 구조화 JSON 없이 원문 텍스트만으로 중복 감지를 수행하지 않습니다.

## 출력

단일 상품은 `references/schema.json`과 일치하는 JSON 객체 하나로 반환합니다.

여러 상품은 상품별 schema-valid 객체를 먼저 반환합니다. 중복 후보 결과는 사용자가 요청했거나 배치 맥락상 필요한 경우에만 제공합니다.

schema 밖의 필드를 추가하지 않습니다. "legal", "illegal", "valid label", "violation"처럼 적법/위법 또는 표기 규정 위반을 판정하는 표현을 출력하지 않습니다.

## 완료 체크리스트

응답 전에 아래 항목을 확인합니다.
- category가 `outer` 또는 `top`이거나, `quality.out_of_scope`가 true입니다.
- 모든 정규화 id가 `taxonomy.json`과 `schema.json`에 존재합니다.
- 소재의 `part`, `ratio`, `ratio_status`가 엄격한 혼용률 규칙을 지킵니다.
- 복합 소재, 복합 계절, TPO 단서, 사이즈/착용감 구절을 한 번 더 훑어 누락이 없습니다.
- 명확하지 않은 추출 속성에는 입력 텍스트 근거가 있습니다.
- 누락 또는 모호한 정보가 `quality`에 반영되어 있습니다.
- URL을 자동으로 열지 않았고, 비공개·내부 데이터를 사용하지 않았습니다.
- 최종 JSON이 schema-valid이거나, 검증 한계를 명시적으로 보고했습니다.
