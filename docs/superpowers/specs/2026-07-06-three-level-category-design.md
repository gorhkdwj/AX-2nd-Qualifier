# 3단계 상품 분류 구조 설계

작성일: 2026-07-06 KST

상태: 사용자 검토 대기

## 1. 목적

이 문서는 `musinsa-product-agentizer`의 상품 분류 구조를 기존 2단계에서 3단계로 확장하기 위한 설계 문서다.

현재 출력 구조는 아래처럼 `category`와 `subcategory`만 가진다.

```json
{
  "product": {
    "category": "outer",
    "subcategory": "jacket"
  }
}
```

이 구조는 MVP를 빠르게 검증하기에는 충분했지만, 실제 무신사 상의·아우터 카테고리의 세부성을 담기에는 부족하다. 예를 들어 실제 몰에는 `트러커 재킷`, `레더/라이더스 재킷`, `숏패딩/헤비 아우터`, `후드 티셔츠` 같은 세부 유형이 있다. 이를 모두 `subcategory`에 직접 추가하면 `subcategory`가 너무 많은 의미를 떠안고, 소재·계절·스타일 정보와도 충돌할 수 있다.

따라서 분류 구조를 아래 3단계로 확장한다.

```text
category     = 큰 상품군
subcategory  = 안정적인 상품 형태
detail_type  = 실제 몰 카테고리에 가까운 세부 유형
```

예시:

```json
{
  "product": {
    "category": "outer",
    "subcategory": "jacket",
    "detail_type": "trucker_jacket"
  }
}
```

이번 구현의 실제 지원 범위는 계속 `outer`와 `top`으로 유지한다. 다만 데이터 모델은 향후 `bottom`, `bag`, `shoes` 등을 같은 방식으로 확장할 수 있게 일반화한다.

## 2. 수정하게 된 문제

### 2.1 실제 무신사 카테고리와 현재 taxonomy의 차이

현재 taxonomy의 `outer`와 `top`은 각각 6개 subcategory를 가진다.

현재 `outer`:

```text
jacket, jumper, coat, cardigan, vest, hoodie_zipup
```

현재 `top`:

```text
tshirt, shirt_blouse, knit, sweatshirt, sleeveless, polo
```

공식 무신사 카테고리 페이지를 확인하면, 실제 상의와 아우터는 더 많은 세부 카테고리를 제공한다.

확인 출처:

- 무신사 상의 카테고리: https://www.musinsa.com/category/001
- 무신사 아우터 카테고리: https://www.musinsa.com/category/002
- 확인일: 2026-07-06 KST

상의는 `전체`를 제외하면 9개 세부 카테고리가 확인된다.

| 공식 카테고리명 | 제안 subcategory | 제안 detail_type |
|---|---|---|
| 반소매 티셔츠 | `tshirt` | `short_sleeve_tshirt` |
| 셔츠/블라우스 | `shirt_blouse` | `shirt_blouse` |
| 민소매 티셔츠 | `sleeveless` | `sleeveless_tshirt` |
| 피케/카라 티셔츠 | `polo` | `polo_collar_tshirt` |
| 긴소매 티셔츠 | `tshirt` | `long_sleeve_tshirt` |
| 니트/스웨터 | `knit` | `knit_sweater` |
| 기타 상의 | `other_top` | `other_top` |
| 맨투맨/스웨트 | `sweatshirt` | `sweatshirt` |
| 후드 티셔츠 | `hoodie` | `hoodie_tshirt` |

아우터는 `전체`를 제외하면 22개 세부 카테고리가 확인된다. 이전 대화에서 21개라고 설명한 것은 `기타 아우터`를 카운트에서 빠뜨린 오류이며, 본 설계에서는 22개로 바로잡는다.

| 공식 카테고리명 | 제안 subcategory | 제안 detail_type |
|---|---|---|
| 스타디움 재킷 | `jacket` | `stadium_jacket` |
| 트러커 재킷 | `jacket` | `trucker_jacket` |
| 무스탕/퍼 | `jumper` | `mustang_fur` |
| 기타 아우터 | `other_outer` | `other_outer` |
| 플리스/뽀글이 | `jacket` | `fleece_jacket` |
| 베스트 | `vest` | `vest` |
| 아노락 재킷 | `jacket` | `anorak_jacket` |
| 겨울 기타 코트 | `coat` | `winter_other_coat` |
| 슈트/블레이저 재킷 | `jacket` | `suit_blazer_jacket` |
| 사파리/헌팅 재킷 | `jacket` | `safari_hunting_jacket` |
| 레더/라이더스 재킷 | `jacket` | `leather_rider_jacket` |
| 트레이닝 재킷 | `jacket` | `training_jacket` |
| 숏패딩/헤비 아우터 | `jumper` | `short_padding_heavy_outer` |
| 경량 패딩/패딩 베스트 | `vest` | `lightweight_padding_vest` |
| 나일론/코치 재킷 | `jacket` | `nylon_coach_jacket` |
| 겨울 더블 코트 | `coat` | `winter_double_coat` |
| 겨울 싱글 코트 | `coat` | `winter_single_coat` |
| 롱패딩/헤비 아우터 | `jumper` | `long_padding_heavy_outer` |
| 카디건 | `cardigan` | `cardigan` |
| 후드 집업 | `hoodie_zipup` | `hoodie_zipup` |
| 환절기 코트 | `coat` | `transitional_coat` |
| 블루종/MA-1 | `jacket` | `blouson_ma1` |

### 2.2 `subcategory`가 과도하게 비대해지는 문제

공식 세부 카테고리를 모두 `subcategory`에 직접 넣으면 `subcategory`의 의미가 흐려진다.

예를 들어 아래 값들은 모두 세부 카테고리처럼 보이지만 의미 성격이 다르다.

| 표현 | 섞여 있는 의미 |
|---|---|
| `leather_rider_jacket` | 형태 + 소재/스타일 |
| `short_padding_heavy_outer` | 길이 + 보온성 + 계절성 |
| `winter_double_coat` | 계절 + 여밈 방식 + 코트 형태 |
| `fleece_jacket` | 소재감/텍스처 + 외형 |
| `hoodie_tshirt` | 후드 디테일 + 상의 형태 |

이를 `subcategory`에 직접 넣으면 `subcategory`가 형태, 소재, 계절, 스타일을 동시에 표현하게 된다. 그러면 AI 에이전트가 어떤 필드를 우선해야 하는지 애매해진다.

3단계 구조는 이 문제를 줄인다.

```json
{
  "category": "outer",
  "subcategory": "jacket",
  "detail_type": "leather_rider_jacket",
  "materials": [
    {
      "name": "faux_leather",
      "ratio_status": "missing",
      "evidence": "합성가죽"
    }
  ]
}
```

여기서 `detail_type`은 몰 카테고리 또는 상품 유형 신호이고, `materials`는 실제 소재 근거다.

## 3. 실사용 관점

이 플러그인은 무신사 실제 홈페이지에 텍스트를 삽입하거나 사이트를 수정하지 않는다. 직접 사용 대상은 외부 쇼핑 사용자가 아니라 내부 AI 에이전트, 상품 데이터 처리 파이프라인, 상품 운영자에 가깝다.

실사용 흐름은 다음과 같다.

```text
브랜드/MD 상품 상세 텍스트
  ↓
product-agentizer 변환
  ↓
구조화 상품 JSON 생성
  ↓
검색 인덱스, 상품 데이터 품질 점검, AI 쇼핑 에이전트 컨텍스트에 활용
  ↓
외부 고객은 더 정확한 검색·필터·AI 설명을 간접적으로 경험
```

예를 들어 외부 사용자가 나중에 AI 쇼핑 에이전트에게 아래처럼 묻는 상황을 상정한다.

```text
블랙 라이더스 재킷 찾아줘.
```

이때 에이전트는 `detail_type=leather_rider_jacket`, `colors=black`을 볼 수 있다.

반면 사용자가 아래처럼 묻는 경우는 다르다.

```text
천연가죽 재킷만 보여줘.
```

이때는 `detail_type`만 보면 안 된다. `materials.name=leather`를 우선해야 한다. `detail_type=leather_rider_jacket`이어도 실제 소재가 `faux_leather`일 수 있기 때문이다.

따라서 필드 우선순위를 명시한다.

| 질의 유형 | 우선 사용 필드 | 보조 필드 |
|---|---|---|
| 상품 유형 질의 | `category`, `subcategory`, `detail_type` | `agent_descriptor.query_tags` |
| 소재 질의 | `materials.name`, `materials.ratio_status`, `materials.evidence` | `detail_type` |
| 계절 질의 | `seasons` | `detail_type`, `materials`, `tpo_tags` |
| 색상 질의 | `colors` | `title`, `agent_descriptor.query_tags` |
| 스타일/TPO 질의 | `tpo_tags` | `detail_type`, `fit`, `agent_descriptor` |
| 중복 후보 | `category`, `subcategory`, `detail_type`, `materials`, `colors`, `fit`, `title` | `care`, `seasons`, `tpo_tags` |

원칙:

- `detail_type`은 실제 몰 카테고리와 상품 유형을 보존하는 필드다.
- 소재 질의에는 `materials`를 우선한다.
- 계절 질의에는 `seasons`를 우선한다.
- `detail_type`에 소재나 계절 단어가 들어 있어도, 해당 구조화 속성 필드와 충돌하면 구조화 속성 필드를 우선한다.
- `detail_type`만으로 법적 상품정보 표기 적합성을 판단하지 않는다.

## 4. 설계 선택지

### 4.1 접근 A: alias만 보강

실제 무신사 세부 카테고리명을 기존 `subcategory.aliases`에 추가한다.

예:

```json
{
  "id": "jacket",
  "aliases": ["재킷", "자켓", "트러커 재킷", "스타디움 재킷"]
}
```

장점:

- 변경 폭이 작다.
- 기존 schema와 fixture에 영향이 적다.
- S8 패키징 전 안정성이 높다.

단점:

- 실제 세부 유형 정보가 구조적으로 사라진다.
- `트러커 재킷`, `블루종/MA-1`, `레더/라이더스 재킷`을 모두 `jacket`으로 뭉갠다.
- 외부 검색 질의에서 세부 유형 대응력이 약하다.

### 4.2 접근 B: 3단계 구조 도입

`category/subcategory/detail_type` 구조로 확장한다.

예:

```json
{
  "category": "outer",
  "subcategory": "jacket",
  "detail_type": "trucker_jacket"
}
```

장점:

- 현재 MVP 범위를 유지하면서 실제 몰 세부 카테고리를 더 정확히 반영한다.
- `subcategory`의 의미를 안정적으로 유지한다.
- 향후 `bottom`, `bag`, `shoes` 등으로 확장할 때 같은 구조를 재사용할 수 있다.
- AI 에이전트가 상품 유형 질의에 더 직접 대응할 수 있다.

단점:

- schema, taxonomy, Skill, validator, dedup, evaluator, fixture, 문서가 모두 바뀐다.
- `detail_type` 판정 난도가 추가된다.
- 검증 수치가 변경될 수 있다.

### 4.3 접근 C: 전체 카테고리 확장

이번에 `bottom`, `bag`, `shoes` 등 무신사 전체 대분류까지 schema에 포함한다.

장점:

- 장기 확장성은 가장 크다.
- 실제 쇼핑몰 전체 모델에 가까워진다.

단점:

- 현재 과제 MVP 범위가 급격히 커진다.
- 검증 fixture와 실제 sanity sample이 크게 늘어난다.
- 마감 전 안정적인 검증이 어렵다.

### 4.4 추천

접근 B를 선택한다.

이번 구현은 `outer/top`에 집중하고, schema와 taxonomy 구조만 향후 다른 대분류가 들어올 수 있게 일반화한다.

## 5. 목표 출력 구조

### 5.1 기존 구조

```json
{
  "schema_version": "0.1.0",
  "product": {
    "category": "outer",
    "subcategory": "jacket"
  }
}
```

### 5.2 변경 구조

```json
{
  "schema_version": "0.2.0",
  "product": {
    "category": "outer",
    "subcategory": "jacket",
    "detail_type": "trucker_jacket"
  }
}
```

### 5.3 `detail_type` nullable 정책

`detail_type`은 `product.required`에 포함한다. 다만 값은 string 또는 null로 허용한다.

```json
{
  "detail_type": null
}
```

이 정책의 이유:

- 모든 상품 텍스트가 세부 유형을 명확히 제공하지 않는다.
- Codex가 세부 유형을 억지로 추정하면 precision이 떨어질 수 있다.
- 필드는 항상 존재하므로 소비자가 같은 구조로 읽을 수 있다.

### 5.4 schema version

`schema_version`은 `0.2.0`으로 올린다.

이유:

- 출력 JSON 구조에 필드가 추가된다.
- 기존 `0.1.0` fixture와 호환되지 않는다.
- 보고서와 README에서 구조 변경을 명확히 구분해야 한다.

## 6. Taxonomy 설계

### 6.1 taxonomy version

`taxonomy_version`과 `schema_version`을 모두 `0.2.0`으로 올린다.

### 6.2 category 구조

`detail_types`는 각 subcategory 아래에 중첩한다.

예:

```json
{
  "categories": {
    "outer": {
      "subcategories": [
        {
          "id": "jacket",
          "ko_name": "재킷",
          "aliases": ["재킷", "자켓"],
          "detail_types": [
            {
              "id": "trucker_jacket",
              "ko_name": "트러커 재킷",
              "aliases": ["트러커 재킷", "데님 재킷"]
            }
          ]
        }
      ]
    }
  }
}
```

이 구조의 장점:

- `detail_type`이 어느 `subcategory`에 속하는지 명확하다.
- validator가 parent-child 관계를 검사할 수 있다.
- 향후 새 대분류를 추가해도 같은 패턴을 따른다.

### 6.3 신규 subcategory

완성도 우선 원칙에 따라 다음 subcategory를 추가한다.

| category | 신규 subcategory | 이유 |
|---|---|---|
| `top` | `hoodie` | 공식 카테고리의 `후드 티셔츠`를 현재 `sweatshirt`로 흡수하면 의미 손실이 큼 |
| `top` | `other_top` | 공식 카테고리의 `기타 상의` 반영 |
| `outer` | `other_outer` | 공식 카테고리의 `기타 아우터` 반영 |

`other_*`는 남용하지 않는다. 공식 몰 카테고리에서 실제로 `기타`가 주어진 경우 또는 구체 분류가 불가능한 경우에만 쓴다.

## 7. Schema 변경

### 7.1 변경 항목

`schema.json`에서 다음을 변경한다.

- `schema_version.const`: `0.1.0` → `0.2.0`
- `product.required`에 `detail_type` 추가
- `product.properties.detail_type` 추가
- `product.properties.subcategory.enum`에 신규 subcategory 추가
- `$defs.attribute_key.enum`에 `detail_type` 추가
- `detail_type` enum 추가

### 7.2 detail_type enum

`detail_type` enum은 공식 상의·아우터 detail_type과 `null`을 포함한다.

예:

```json
{
  "detail_type": {
    "type": ["string", "null"],
    "enum": [
      "short_sleeve_tshirt",
      "shirt_blouse",
      "hoodie_tshirt",
      "trucker_jacket",
      "leather_rider_jacket",
      "other_outer",
      null
    ]
  }
}
```

Schema enum은 값의 존재만 검사한다. `detail_type`이 올바른 parent 아래에 있는지는 `validate.py` custom check가 검사한다.

## 8. Skill 변경

`SKILL.md`에는 다음 지침을 추가한다.

### 8.1 추출 대상 추가

기존 추출 대상:

```text
title, category, subcategory, materials, fit, colors, seasons, tpo_tags, care, size_info
```

변경 후:

```text
title, category, subcategory, detail_type, materials, fit, colors, seasons, tpo_tags, care, size_info
```

### 8.2 분류 절차

Skill은 다음 순서를 따른다.

1. `category`를 `outer` 또는 `top`으로 판정한다.
2. 안정적인 형태 기준으로 `subcategory`를 판정한다.
3. 공식 몰 세부 카테고리 또는 상품명 단서가 있으면 `detail_type`을 판정한다.
4. 불확실하면 `detail_type: null`로 두고 `quality.missing_fields` 또는 `quality.ambiguous_fields`에 `detail_type`을 기록한다.

### 8.3 필드 우선순위

Skill에 다음 원칙을 명시한다.

```text
detail_type은 몰 카테고리/상품 유형 신호다.
소재 질의에는 materials를 우선한다.
계절 질의에는 seasons를 우선한다.
detail_type 안에 소재·계절 단어가 포함되어도, 해당 속성 필드와 충돌하면 속성 필드를 우선한다.
```

## 9. Validator 변경

`validate.py`는 다음 검사를 추가한다.

### 9.1 taxonomy set 확장

현재는 subcategory set만 만든다. 변경 후에는 다음을 만든다.

- `categories`
- `subcategories`
- `detail_types`
- `subcategory_by_detail_type`
- `category_by_subcategory`

### 9.2 parent-child 관계 검증

아래는 유효해야 한다.

```json
{
  "category": "outer",
  "subcategory": "jacket",
  "detail_type": "trucker_jacket"
}
```

아래는 오류여야 한다.

```json
{
  "category": "top",
  "subcategory": "tshirt",
  "detail_type": "trucker_jacket"
}
```

오류 메시지는 다음 수준이면 충분하다.

```text
detail_type must belong to the selected category/subcategory
```

### 9.3 null 처리

`detail_type`이 `null`이면 parent-child 검사는 건너뛴다.

단, 입력 텍스트에 구체 detail_type 단서가 명확한데도 null인지 여부는 validator가 판단하지 않는다. 이는 Codex 추출 품질 평가의 영역이다.

### 9.4 quality 연동

`quality.missing_fields`와 `quality.ambiguous_fields`에 `detail_type`을 허용한다.

## 10. Dedup 변경

`dedup.py`는 `detail_type`을 보조 신호로 추가한다.

### 10.1 가중치

권장 변경:

| 속성 | 기존 | 변경 |
|---|---:|---:|
| category | 0.18 | 0.16 |
| subcategory | 0.16 | 0.14 |
| detail_type | 없음 | 0.08 |
| materials | 0.20 | 0.18 |
| colors | 0.12 | 0.11 |
| fit | 0.10 | 0.09 |
| seasons | 0.08 | 0.07 |
| tpo_tags | 0.08 | 0.07 |
| care | 0.04 | 0.04 |
| title | 0.14 | 0.06 |

합계는 1.0이다.

### 10.2 설계 이유

`detail_type`은 유용하지만 너무 큰 가중치를 주면 위험하다. 같은 상품도 한쪽은 `trucker_jacket`, 다른 쪽은 넓게 `jacket` 또는 `null`로 나올 수 있다. 따라서 중복 감지는 여전히 `materials`, `colors`, `fit`, `title`을 함께 본다.

### 10.3 matched_fields

`detail_type`이 일치하면 `matched_fields`에 `detail_type`을 포함한다.

## 11. Evaluator 변경

`tests/evaluate_product_agentizer.py`는 `EVALUATED_FIELDS`에 `detail_type`을 추가한다.

변경 전:

```python
EVALUATED_FIELDS = [
    "title",
    "category",
    "subcategory",
    ...
]
```

변경 후:

```python
EVALUATED_FIELDS = [
    "title",
    "category",
    "subcategory",
    "detail_type",
    ...
]
```

`field_tokens()`에서는 `detail_type`을 `title`, `category`, `subcategory`와 같은 단일 문자열 필드로 처리한다.

## 12. Fixture 변경

모든 fixture의 `structured_product.product`에 `detail_type`을 추가해야 한다.

영향 대상:

- `tests/fixtures/schema/*.json`
- `tests/fixtures/dedup/*.json`
- `tests/fixtures/evaluation/*.json`
- `tests/fixtures/expanded_dummy/*.json`
- `tests/fixtures/codex_subset/*.json`
- `tests/fixtures/real_sanity/*.json`

### 12.1 Codex actual 처리

기존 보존 actual은 `schema_version=0.1.0`이고 `detail_type`이 없다. 선택지는 두 가지다.

1. 기존 actual을 deterministic하게 보강한다.
2. Codex actual을 새 prompt로 재생성한다.

추천은 1번이다.

이유:

- 기존 S7.5 재현성 산출물을 갑자기 모델 재실행 변동성에 맡기지 않는다.
- schema 구조 변경 검증을 먼저 안정적으로 끝낼 수 있다.
- 필요하면 별도 후속 검증에서 Codex actual 재생성을 수행한다.

단, 보강 기준은 fixture 생성기와 taxonomy 기준에 의해 결정적으로 수행해야 한다.

### 12.2 확장 fixture 생성기

`tools/generate_expanded_validation_fixtures.py`는 다음을 갖도록 수정한다.

- `OUTER_DETAIL_TYPES`
- `TOP_DETAIL_TYPES`
- `KO_DETAIL_TYPE`
- subcategory와 detail_type의 parent-child 매핑
- source text에 detail_type 단서 삽입
- expected JSON에 detail_type 삽입

## 13. 문서 변경

다음 문서를 갱신한다.

| 문서 | 변경 내용 |
|---|---|
| `README.md` | 3단계 분류와 `detail_type` 설명 추가 |
| `docs/requirements-contract.md` | 출력 계약과 지표 정의 갱신 |
| `docs/implementation-plan.md` | S7.6 또는 신규 단계로 3단계 구조 개편 추가 |
| `docs/validation-plan.md` | parent-child 검증과 detail_type 평가 기준 추가 |
| `docs/product-agentizer-complete-guide.md` | 전체 상세 설명서 2단계 구조 설명을 3단계로 갱신 |
| `docs/reports/s7-expanded-validation-report.md` | 재검증 후 결과 갱신 |
| `docs/reports/s7-expanded-validation-results.json` | `run_expanded_validation.py` 재실행 결과로 갱신 |
| `docs/submission-questions.md` | 필요 시 제출 답변의 기능 설명 갱신 |
| `Decisionlog.md` | 사용자 승인 후 3단계 구조 도입 결정 기록 |
| `Worklog.md` | 설계와 구현 작업 기록 |
| `Troubleshootinglog.md` | 실제 오류 발생 시 기록 |

## 14. 검증 계획

### 14.1 단위 검증

아래 명령이 통과해야 한다.

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
python src\skills\product-agentizer\scripts\dedup.py tests\fixtures\dedup\sample_products.json --pretty
python tests\evaluate_product_agentizer.py --pretty
```

### 14.2 invalid fixture

아래 invalid fixture를 추가 또는 갱신한다.

| fixture | 기대 결과 |
|---|---|
| `invalid_detail_type_parent.json` | `detail_type`이 잘못된 parent 아래 있어 실패 |
| `invalid_missing_detail_type.json` | 필수 필드 누락으로 실패 |
| `invalid_unknown_detail_type.json` | schema enum 밖 값으로 실패 |

### 14.3 S7.5 확장 검증

아래 명령으로 전체 재검증한다.

```powershell
python tools\run_expanded_validation.py
```

Acceptance 기준은 기본적으로 기존과 같다. 다만 `detail_type` 필드 추가로 precision/recall이 변할 수 있으므로 변경 전후 수치를 보고서에 남긴다.

권장 기준:

| 항목 | 기준 |
|---|---|
| 합성 expected schema-valid | 100% |
| Codex subset actual schema-valid | 100% |
| Codex subset micro precision | 95% 이상 |
| Codex subset micro recall | 85% 이상 |
| dedup accuracy | 95% 이상 |
| cross-category high-confidence false duplicate | 0건 |
| 자동 fetch | 0건 |
| 법적 적합/부적합 판정 | 0건 |

## 15. 기대 효과

3단계 구조 도입으로 기대하는 효과는 다음과 같다.

- 실제 무신사 상의·아우터 카테고리 체계를 더 정확히 반영한다.
- `subcategory`가 과도하게 비대해지는 것을 막는다.
- `detail_type`을 통해 몰 카테고리 수준의 세부성을 보존한다.
- AI 에이전트가 `트러커 재킷`, `후드 티셔츠`, `숏패딩` 같은 질의에 더 잘 대응한다.
- 소재, 계절, TPO 같은 속성 필드와 상품 유형 필드의 역할을 분리한다.
- 향후 `bottom`, `bag`, `shoes` 확장 시 같은 모델을 재사용할 수 있다.
- 중복 감지에서 큰 분류와 세부 유형을 함께 활용할 수 있다.

## 16. 리스크와 대응

| 리스크 | 설명 | 대응 |
|---|---|---|
| schema 변경 폭 증가 | `detail_type` 추가로 모든 fixture 갱신 필요 | fixture 생성기부터 수정하고 재생성 |
| Codex detail_type 오분류 | 세부 유형이 많아지면 판단 난도 상승 | `detail_type=null` 허용, 불확실 시 quality에 기록 |
| 소재/계절 의미 충돌 | detail_type에 소재나 계절 단어가 포함될 수 있음 | 소재 질의는 materials, 계절 질의는 seasons 우선 규칙 명시 |
| dedup 점수 흔들림 | detail_type 불일치로 같은 상품 점수가 낮아질 수 있음 | detail_type 가중치를 0.08로 제한 |
| 문서 불일치 | README와 상세 설명서가 2단계 구조 기준 | 관련 문서 일괄 갱신 |
| 검증 수치 변화 | 평가 필드 추가로 precision/recall 변동 | 변경 전후 수치를 보고서에 기록 |
| `other_*` 남용 | 세부 분류 회피 수단으로 쓰일 수 있음 | 공식 기타 카테고리 또는 불명확 케이스에만 사용 |

## 17. 구현 순서 제안

사용자 승인 후 구현 순서는 다음과 같다.

1. `Decisionlog.md`에 3단계 구조 도입 결정 기록
2. `taxonomy.json`을 `0.2.0`과 nested `detail_types` 구조로 확장
3. `schema.json`을 `0.2.0`으로 갱신하고 `detail_type` 추가
4. `validate.py`에 category-subcategory-detail_type parent-child 검증 추가
5. `SKILL.md`에 detail_type 추출 지침과 필드 우선순위 추가
6. `dedup.py`에 detail_type 점수 반영
7. `tests/evaluate_product_agentizer.py`에 detail_type 평가 추가
8. schema fixture 갱신 및 invalid detail_type fixture 추가
9. `tools/generate_expanded_validation_fixtures.py` 수정
10. S7.5 fixture 재생성 또는 보강
11. 전체 검증 재실행
12. README와 docs 갱신
13. Worklog/Troubleshootinglog 기록
14. 비밀정보 패턴 검색
15. commit/push

## 18. 승인 기준

이 설계는 다음 조건을 만족하면 구현으로 넘어간다.

- 사용자가 3단계 구조 도입을 승인한다.
- `detail_type` nullable 필수 필드 정책에 동의한다.
- `schema_version=0.2.0` 상승에 동의한다.
- 이번 구현 범위는 `outer/top`으로 유지하고, 다른 대분류는 구조만 확장 가능하게 둔다.
- 공식 무신사 카테고리는 상의 9개, 아우터 22개 기준으로 반영한다.

## 19. 자체 검토

- Placeholder 없음: 이 문서는 미완성 표식 없이 작성되었다.
- 범위: 이번 구현은 `outer/top`의 3단계 구조 개편으로 제한한다.
- 일관성: schema, taxonomy, validator, evaluator, dedup, fixture, 문서 영향 범위를 모두 같은 `detail_type` 정책에 맞췄다.
- 모호성: `detail_type`은 필수 필드이되 `null` 허용으로 정의했다.
- 사용자 지적 반영: 아우터 공식 세부 카테고리는 `기타 아우터`를 포함해 22개로 정정했다.
