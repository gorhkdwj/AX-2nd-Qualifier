# Musinsa Product Agentizer 상세 설명서

작성일: 2026-07-06 KST

이 문서는 무신사 문제 2 `상품 데이터 에이전트화 변환기`로 구현한 Codex 플러그인의 전체 목적, 구성, 세부 기능, 작동 방식, 검증 방법, 정량 지표의 의미와 결과를 한 번에 이해할 수 있도록 정리한 상세 설명서입니다.

## 1. 문서 목적

이 문서는 아래 질문에 답하기 위해 작성했습니다.

- 우리가 무엇을 만들었는가?
- 왜 무신사 문제 2를 선택했는가?
- 플러그인은 Codex 안에서 어떤 방식으로 동작하는가?
- `SKILL.md`, `schema.json`, `taxonomy.json`, `validate.py`, `dedup.py`는 각각 무슨 역할을 하는가?
- 상품 상세 텍스트가 어떤 JSON 구조로 변환되는가?
- 소재 혼용률, 누락 정보, 모호 정보는 어떻게 판단하는가?
- `precision`, `recall`, `schema-valid`, `dedup accuracy` 같은 지표는 무엇을 의미하는가?
- 각 검증 결과는 어떤 부분에서 통과했고, 어떤 부분은 한계 또는 참고 지표로 남았는가?
- 누가 다시 실행해도 같은 입력, 명령, 결과를 추적하려면 어떤 파일을 보면 되는가?

이 문서는 제출용 짧은 README가 아니라, 프로젝트를 처음 보는 사람이 내부 구현과 검증 흐름까지 이해할 수 있도록 만든 기술 해설서입니다.

## 2. 한 줄 요약

`musinsa-product-agentizer`는 사용자가 직접 붙여넣은 한국어 패션 상품 상세 텍스트를 Codex가 읽고, AI 에이전트가 검색, 필터, 비교, 설명에 사용할 수 있는 schema-valid 구조화 상품 JSON으로 변환하는 플러그인입니다.

## 3. 문제 배경

확정 기업과 문제는 다음과 같습니다.

| 항목 | 내용 |
|---|---|
| 기업 | 무신사 |
| 선택 문제 | 문제 2, 상품 데이터 에이전트화 변환기 |
| 제출 플러그인 이름 | `musinsa-product-agentizer` |
| 플러그인 루트 | `src/` |
| MVP 카테고리 | 아우터 `outer`, 상의 `top` |
| 실행 입력 | 사용자가 직접 붙여넣은 상품 상세 텍스트 |
| 자동 수집 | 하지 않음 |

무신사의 상품 상세정보는 사람에게는 읽기 쉬운 형태입니다. 그러나 AI 에이전트가 질의와 필터에 사용하기에는 비정형 텍스트가 많습니다.

예를 들어 사람은 아래 문장을 보고 상품의 의미를 대략 이해할 수 있습니다.

```text
상품명: 카키 릴랙스 다운 베스트.
겉감 나일론 100%, 충전재 덕다운 80%, 구스다운 20%.
가을겨울 여행용 레이어드에 적합하며 L 기준 총장 68cm, 여유 있는 암홀.
```

하지만 AI 에이전트가 안정적으로 답하려면 이 문장이 아래처럼 구조화되어야 합니다.

```json
{
  "category": "outer",
  "subcategory": "vest",
  "materials": [
    {"part": "shell", "name": "nylon", "ratio": 100, "ratio_status": "explicit"},
    {"part": "fill", "name": "duck_down", "ratio": 80, "ratio_status": "explicit"},
    {"part": "fill", "name": "goose_down", "ratio": 20, "ratio_status": "explicit"}
  ],
  "colors": ["khaki"],
  "seasons": ["fall", "winter"],
  "tpo_tags": ["layering", "outdoor", "travel"],
  "size_info": ["L 기준 총장 68cm", "여유 있는 암홀"]
}
```

이 프로젝트는 바로 이 변환 과정을 Codex 플러그인으로 구현합니다.

## 4. 해결하려는 핵심 문제

### 4.1 비정형 상품 텍스트의 구조화

상품 상세페이지에는 상품명, 소재, 색상, 핏, 사이즈, 세탁 방법, 착용 상황이 한 문장 또는 여러 표 형태로 섞여 있습니다. 플러그인은 이 정보를 표준 JSON 필드로 나눕니다.

### 4.2 자유 표기의 표준 taxonomy 매핑

같은 의미가 여러 방식으로 표기될 수 있습니다.

| 원문 표현 | 표준 id |
|---|---|
| 자켓, 재킷, 블레이저 | `jacket` |
| 카키, 올리브 | `khaki` |
| 린넨, 리넨, 마 | `linen` |
| 여유핏, 세미오버 | `relaxed` |
| 여행, 여행용, 휴가 | `travel` |

AI 에이전트가 일관되게 검색하려면 자유 표기를 표준 id로 바꿔야 합니다. 이 기준은 `taxonomy.json`에 들어 있습니다.

### 4.3 혼용률의 엄격한 근거 기반 처리

소재 혼용률은 법적 오해 소지가 있을 수 있는 민감한 정보입니다. 그래서 이 프로젝트는 숫자를 추정하지 않습니다.

입력에 `면 100%`라고 있으면 `explicit`입니다.

입력에 `코튼 소재`라고만 있으면 소재명은 있지만 숫자 혼용률이 없으므로 `missing`입니다.

입력에 `린넨 터치`, `캐시미어 블렌디드`, `페이크 레더 느낌`처럼 소재감만 암시되어 있으면 `ambiguous`입니다.

중요한 점은 이 플러그인이 상품정보 표기 규정의 적법 또는 부적합 여부를 판단하지 않는다는 것입니다. 입력 텍스트에 근거가 있는 정보를 구조화하고, 부족하거나 모호한 정보는 `quality`에 남기는 데 한정합니다.

### 4.4 중복 후보 감지

같은 상품이 서로 다른 제목이나 약간 다른 표현으로 등록될 수 있습니다. `dedup.py`는 구조화된 상품 JSON 사이의 유사도를 계산해 중복 후보를 찾습니다.

예를 들어 아래 두 상품은 제목이 다르더라도 소재, 색상, 핏, 카테고리, 계절이 거의 같으면 중복 후보가 될 수 있습니다.

```text
상품 A: 블랙 오버핏 울 재킷
상품 B: 블랙 울 블레이저 리오더
```

단, 중복 감지는 확정 삭제 기능이 아닙니다. `duplicate`, `possible_duplicate`, `distinct`로 후보를 분류해 사람이 검토할 수 있게 만드는 보조 기능입니다.

## 5. 전체 시스템 구성

현재 주요 파일 구조는 아래와 같습니다.

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

tests/
└── fixtures/
    ├── schema/
    ├── dedup/
    ├── evaluation/
    ├── expanded_dummy/
    ├── codex_subset/
    └── real_sanity/

tools/
├── generate_expanded_validation_fixtures.py
├── run_expanded_validation.py
└── save_log.py

docs/
├── requirements-contract.md
├── implementation-plan.md
├── validation-plan.md
├── product-agentizer-complete-guide.md
└── reports/
    ├── s5-evaluation-report.md
    ├── s6-codex-cli-report.md
    ├── s7-expanded-validation-report.md
    └── s7-expanded-validation-results.json
```

각 파일의 역할은 다음과 같습니다.

| 파일 | 역할 |
|---|---|
| `src/.codex-plugin/plugin.json` | Codex가 플러그인을 인식하기 위한 manifest |
| `src/skills/product-agentizer/SKILL.md` | Codex가 언제 이 기능을 쓰고 어떤 절차로 변환할지 알려주는 지침 |
| `references/schema.json` | 최종 출력 JSON의 필수 구조와 허용 값 계약 |
| `references/taxonomy.json` | 카테고리, 소재, 색상, 계절, TPO 등 표준 vocabulary |
| `scripts/validate.py` | JSON 출력이 schema와 taxonomy 규칙을 지키는지 검증 |
| `scripts/dedup.py` | 여러 구조화 상품 사이의 중복 후보 점수 계산 |
| `tests/evaluate_product_agentizer.py` | expected JSON과 actual JSON을 비교해 precision, recall, dedup accuracy 산출 |
| `tools/generate_expanded_validation_fixtures.py` | S7.5 확장 검증용 fixture 재생성 |
| `tools/run_expanded_validation.py` | S7.5 전체 검증 실행 및 결과 스냅샷 저장 |
| `tools/save_log.py` | Stop hook에서 대화 로그를 `logs/`에 저장 |

## 6. Codex 플러그인 구조

### 6.1 `plugin.json`

`plugin.json`은 Codex가 플러그인을 찾기 위한 manifest입니다.

```json
{
  "name": "musinsa-product-agentizer",
  "version": "0.1.0",
  "description": "Convert pasted Korean fashion product detail text into schema-valid, agent-query-ready structured JSON for the Musinsa outer/top MVP.",
  "skills": "./skills/"
}
```

핵심은 `"skills": "./skills/"`입니다. 이 값 때문에 Codex는 `src/skills/` 아래의 `product-agentizer/SKILL.md`를 skill로 인식할 수 있습니다.

### 6.2 `SKILL.md`

`SKILL.md`는 이 플러그인의 실제 동작 지침입니다. Codex는 사용자의 요청이 skill description과 맞으면 이 파일을 읽고 작업 절차를 따릅니다.

현재 description은 한영 혼합으로 작성되어 있습니다.

```text
붙여넣은 한국어 패션 상품 상세 텍스트를 Musinsa outer/top MVP용 schema-valid,
agent-query-ready structured product JSON으로 변환합니다.
```

한영 혼합으로 둔 이유는 두 가지입니다.

- 한국어 상품 상세 텍스트를 다루는 목적을 명확히 하기 위해서입니다.
- `schema-valid`, `taxonomy mapping`, `duplicate-candidate`처럼 Codex와 개발 문맥에서 중요한 영어 키워드를 description에 유지하기 위해서입니다.

`SKILL.md`는 다음을 명확히 지시합니다.

- URL을 자동으로 열지 않습니다.
- 사용자가 붙여넣은 상품 상세 텍스트만 사용합니다.
- `outer`, `top`만 MVP 범위로 지원합니다.
- 상품정보 표기 규정의 법적 적합성 판단은 하지 않습니다.
- 소재 혼용률은 입력에 숫자가 직접 있을 때만 `explicit`으로 기록합니다.
- 누락 또는 모호 정보는 `quality.missing_fields`, `quality.ambiguous_fields`에 남깁니다.
- 최종 출력은 `schema.json`과 일치해야 합니다.

## 7. 입력 정책

### 7.1 허용 입력

허용되는 입력은 아래와 같습니다.

```json
{
  "product_text": "사용자가 직접 붙여넣은 상품 상세 텍스트",
  "source_url": "선택: 출처 기록용 URL",
  "source_title": "선택: 상품명 또는 페이지 제목",
  "category_hint": "선택: outer | top",
  "locale": "ko-KR"
}
```

일반 텍스트만 제공되면 그 텍스트를 `product_text`로 취급합니다.

### 7.2 금지 입력

아래 입력은 사용하지 않습니다.

- 플러그인이 직접 가져온 상품 URL 내용
- 자동 scraping, crawling 결과
- 로그인 또는 권한이 필요한 내부 데이터
- 고객정보, 주문정보, 결제정보, 계좌정보
- API key, token, session cookie
- 제3자 리뷰나 커뮤니티 글의 대량 수집 데이터

### 7.3 URL 처리 원칙

URL은 출처 메타데이터입니다. 실행 입력이 아닙니다.

예를 들어 아래처럼 URL이 있어도 플러그인은 URL을 열지 않습니다.

```json
{
  "source_url": "https://www.musinsa.com/products/4308999",
  "product_text": "상품명: 빈폴 레이디스 리넨 체크 더블 재킷..."
}
```

실제 변환은 `product_text`에 이미 붙여넣어진 텍스트만으로 수행합니다.

## 8. 출력 JSON 구조

최종 출력은 `schema.json`에 맞는 JSON 객체입니다.

최상위 필드는 다섯 개입니다.

| 필드 | 의미 |
|---|---|
| `schema_version` | 현재 스키마 버전. `0.1.0` 고정 |
| `source` | 입력 출처와 입력 방식 |
| `product` | 구조화된 상품 속성 |
| `agent_descriptor` | AI 에이전트 검색과 설명에 쓰는 요약 정보 |
| `quality` | 누락, 모호, 범위, 신뢰도 정보 |

### 8.1 `source`

```json
{
  "source_url": "https://example.com/product/1",
  "source_title": "카키 릴랙스 다운 베스트",
  "input_mode": "pasted_text"
}
```

`input_mode`는 항상 `pasted_text`입니다. 이는 자동 fetch가 아니라 사용자가 붙여넣은 텍스트를 입력으로 사용했다는 의미입니다.

### 8.2 `product`

`product`는 실제 상품 속성을 담습니다.

```json
{
  "title": "카키 릴랙스 다운 베스트",
  "category": "outer",
  "subcategory": "vest",
  "materials": [],
  "fit": ["relaxed"],
  "colors": ["khaki"],
  "seasons": ["fall", "winter"],
  "tpo_tags": ["layering", "outdoor", "travel"],
  "care": ["dry_clean"],
  "size_info": ["L 기준 총장 68cm", "여유 있는 암홀"]
}
```

각 속성의 의미는 아래와 같습니다.

| 필드 | 의미 | 예시 |
|---|---|---|
| `title` | 상품명 | `카키 릴랙스 다운 베스트` |
| `category` | 대분류 | `outer`, `top` |
| `subcategory` | 세부 카테고리 | `jacket`, `vest`, `tshirt` |
| `materials` | 소재, 부위, 혼용률 | `shell:nylon:100` |
| `fit` | 핏 또는 실루엣 | `relaxed`, `oversized` |
| `colors` | 표준 색상 id | `khaki`, `black` |
| `seasons` | 계절 태그 | `spring`, `summer`, `fall`, `winter` |
| `tpo_tags` | 착용 상황 또는 스타일 태그 | `travel`, `formal`, `layering` |
| `care` | 세탁 및 관리 방법 | `dry_clean`, `hand_wash` |
| `size_info` | 사이즈, 치수, 착용감 텍스트 | `총장 68cm`, `암홀 여유` |

### 8.3 `materials`

`materials`는 이 프로젝트에서 가장 엄격하게 다루는 필드입니다.

각 소재 항목은 아래 다섯 필드를 반드시 가집니다.

| 필드 | 의미 |
|---|---|
| `part` | 소재가 적용되는 부위 |
| `name` | 표준 소재 id |
| `ratio` | 숫자 혼용률 또는 `null` |
| `ratio_status` | 혼용률 상태 |
| `evidence` | 입력 텍스트에서 근거가 된 표현 |

예시:

```json
{
  "part": "fill",
  "name": "duck_down",
  "ratio": 80,
  "ratio_status": "explicit",
  "evidence": "충전재 덕다운 80%, 구스다운 20%"
}
```

`part` 허용 값은 다음과 같습니다.

| id | 의미 |
|---|---|
| `shell` | 겉감 |
| `lining` | 안감 |
| `fill` | 충전재 |
| `rib` | 립, 시보리 |
| `pocket` | 포켓, 주머니 |
| `trim` | 배색, 부자재, 카라, 후드, 소매 등 |
| `unknown` | 부위를 알 수 없음 |

`name` 허용 값은 다음과 같습니다.

| id | 의미 |
|---|---|
| `cotton` | 면, 코튼 |
| `polyester` | 폴리에스터 |
| `nylon` | 나일론 |
| `wool` | 울, 모, 양모 |
| `cashmere` | 캐시미어 |
| `linen` | 리넨, 린넨, 마 |
| `rayon` | 레이온, 비스코스 |
| `polyurethane` | 폴리우레탄, 스판, 엘라스틴 |
| `acrylic` | 아크릴 |
| `leather` | 천연가죽 |
| `faux_leather` | 합성가죽, 페이크 레더 |
| `duck_down` | 덕다운, 오리털 |
| `goose_down` | 구스다운, 거위털 |
| `recycled_fiber` | 리사이클 섬유 |

### 8.4 `ratio_status`

`ratio_status`는 소재 혼용률의 신뢰 상태입니다.

| 상태 | `ratio` 값 | 의미 |
|---|---:|---|
| `explicit` | 숫자 | 입력에 숫자 혼용률이 직접 있음 |
| `missing` | `null` | 소재명은 있으나 숫자 혼용률이 없음 |
| `ambiguous` | `null` | 소재감 또는 혼방 표현만 있어 비율을 알 수 없음 |

#### explicit 예시

입력:

```text
겉감 면 60%, 폴리에스터 40%
```

출력:

```json
[
  {
    "part": "shell",
    "name": "cotton",
    "ratio": 60,
    "ratio_status": "explicit",
    "evidence": "겉감 면 60%, 폴리에스터 40%"
  },
  {
    "part": "shell",
    "name": "polyester",
    "ratio": 40,
    "ratio_status": "explicit",
    "evidence": "겉감 면 60%, 폴리에스터 40%"
  }
]
```

#### missing 예시

입력:

```text
코튼 소재로 제작했습니다.
```

출력:

```json
{
  "part": "unknown",
  "name": "cotton",
  "ratio": null,
  "ratio_status": "missing",
  "evidence": "코튼 소재"
}
```

이 경우 `quality.missing_fields`에 `material_ratio`가 들어가야 합니다.

#### ambiguous 예시

입력:

```text
린넨 터치의 레이온 블렌드 소재입니다.
```

출력:

```json
[
  {
    "part": "unknown",
    "name": "linen",
    "ratio": null,
    "ratio_status": "ambiguous",
    "evidence": "린넨 터치"
  },
  {
    "part": "unknown",
    "name": "rayon",
    "ratio": null,
    "ratio_status": "ambiguous",
    "evidence": "레이온 블렌드"
  }
]
```

이 경우 `quality.ambiguous_fields`에 `material_ratio`가 들어가야 합니다.

### 8.5 `agent_descriptor`

`agent_descriptor`는 구조화 데이터를 사람이 읽기 위한 설명이 아니라, AI 에이전트가 검색과 답변에 활용하기 쉬운 요약입니다.

```json
{
  "search_summary": "카키 릴랙스 핏 다운 베스트로 가을겨울 여행과 레이어드에 적합합니다.",
  "query_tags": ["카키 베스트", "겨울 여행 아우터", "레이어드 조끼"],
  "explainable_reasons": [
    "입력 텍스트의 카키 색상과 베스트 표현을 khaki, vest로 정규화했습니다.",
    "충전재 덕다운 80%, 구스다운 20%가 명시되어 fill 소재로 분리했습니다."
  ]
}
```

각 필드의 의미는 다음과 같습니다.

| 필드 | 의미 |
|---|---|
| `search_summary` | 검색용 짧은 한국어 요약 |
| `query_tags` | 자연어 질의와 매칭될 수 있는 표현 |
| `explainable_reasons` | 왜 이런 태그와 속성이 붙었는지 설명하는 근거 |

### 8.6 `quality`

`quality`는 변환 결과의 한계와 신뢰도를 기록합니다.

```json
{
  "missing_fields": ["material_ratio"],
  "ambiguous_fields": [],
  "out_of_scope": false,
  "confidence": "medium"
}
```

| 필드 | 의미 |
|---|---|
| `missing_fields` | 입력에 없어서 채울 수 없었던 속성 |
| `ambiguous_fields` | 입력이 모호해 단정할 수 없었던 속성 |
| `out_of_scope` | MVP 범위 밖 입력 여부 |
| `confidence` | `high`, `medium`, `low` 중 하나 |

중요한 구현상 주의점이 있습니다. 현재 `schema.json`은 `product.category`를 `outer` 또는 `top`으로 제한합니다. 따라서 MVP 범위 밖 상품을 완전한 다른 category id로 출력하는 것은 현재 schema-valid하지 않습니다. 범위 밖 상품은 변환을 무리하게 확장하지 않고, 새 taxonomy id를 만들지 않는 것이 원칙입니다.

## 9. Taxonomy 구조

`taxonomy.json`은 자유 표현을 표준 id로 바꾸기 위한 기준 데이터입니다.

### 9.1 지원 카테고리

| category | 한국어 | 설명 |
|---|---|---|
| `outer` | 아우터 | 상의 위에 걸쳐 입는 외투류 |
| `top` | 상의 | 단독 또는 이너로 착용하는 상의류 |

### 9.2 아우터 subcategory

| id | 한국어 | 주요 alias |
|---|---|---|
| `jacket` | 재킷 | 재킷, 자켓, 블레이저, 블루종 |
| `jumper` | 점퍼 | 점퍼, 집업 점퍼, 윈드브레이커, 바람막이 |
| `coat` | 코트 | 코트, 트렌치코트, 맥코트, 더블 코트 |
| `cardigan` | 가디건 | 가디건, 니트 가디건, 집업 가디건 |
| `vest` | 베스트 | 베스트, 조끼, 패딩 베스트 |
| `hoodie_zipup` | 후드 집업 | 후드 집업, 후디 집업, 집업 후드 |

### 9.3 상의 subcategory

| id | 한국어 | 주요 alias |
|---|---|---|
| `tshirt` | 티셔츠 | 티셔츠, 반팔 티, 긴팔 티, 롱슬리브 |
| `shirt_blouse` | 셔츠/블라우스 | 셔츠, 블라우스, 옥스포드 셔츠, 린넨 셔츠 |
| `knit` | 니트 | 니트, 스웨터, 풀오버, 니트탑 |
| `sweatshirt` | 스웨트셔츠 | 스웨트셔츠, 맨투맨, 크루넥 |
| `sleeveless` | 슬리브리스 | 슬리브리스, 민소매, 나시, 탱크톱 |
| `polo` | 폴로 | 폴로, 카라 티, 피케 셔츠 |

### 9.4 색상 vocabulary

허용 색상 id는 다음과 같습니다.

```text
black, white, ivory, gray, beige, brown, navy, blue, denim_blue,
green, khaki, red, pink, yellow, multi
```

특히 `카키`, `올리브`는 넓은 `green`으로 뭉뚱그리지 않고 `khaki`로 매핑합니다. 이 규칙은 S5 검증에서 `khaki`가 `green`으로 잘못 예측된 문제를 보완하면서 강화했습니다.

### 9.5 계절 vocabulary

허용 계절 id는 다음과 같습니다.

```text
spring, summer, fall, winter
```

복합 표현은 여러 계절로 분리합니다.

| 입력 표현 | 출력 |
|---|---|
| 봄여름 | `spring`, `summer` |
| 가을겨울 | `fall`, `winter` |
| 봄가을, 간절기 | `spring`, `fall` |

### 9.6 TPO vocabulary

허용 TPO id는 다음과 같습니다.

```text
daily, casual, commute, formal, guest_look, travel,
outdoor, layering, date, street
```

예시는 아래와 같습니다.

| 입력 표현 | 출력 |
|---|---|
| 출근, 오피스, 직장 | `commute` |
| 포멀, 격식, 세미포멀 | `formal` |
| 하객, 결혼식, 행사 | `guest_look` |
| 여행, 여행용, 휴가 | `travel` |
| 이너, 레이어드, 겹쳐입기 | `layering` |

## 10. 전체 작동 흐름

상품 텍스트가 구조화 JSON이 되는 흐름은 아래와 같습니다.

```text
사용자 입력
  ↓
SKILL.md 발동 여부 판단
  ↓
입력 안전성 확인
  ↓
category와 subcategory 판정
  ↓
상품 속성 추출
  ↓
taxonomy.json 기준 정규화
  ↓
schema.json 기준 JSON 작성
  ↓
quality와 agent_descriptor 작성
  ↓
validate.py로 검증
  ↓
필요 시 dedup.py로 중복 후보 산출
```

### 10.1 입력 안전성 확인

먼저 입력이 사용자가 직접 붙여넣은 텍스트인지 확인합니다. URL만 주고 “열어서 처리해 달라”고 하면 자동으로 열지 않습니다. 내부 데이터나 비밀정보가 들어 있으면 중단하고 안전 문제를 보고해야 합니다.

### 10.2 카테고리 판정

`category_hint`가 있고 텍스트와 모순되지 않으면 우선 사용합니다. 없으면 `outer`, `top` 중 하나로 추론합니다.

예시:

| 입력 단서 | category | subcategory |
|---|---|---|
| 패딩 베스트, 조끼 | `outer` | `vest` |
| 블레이저, 자켓 | `outer` | `jacket` |
| 반팔 티셔츠 | `top` | `tshirt` |
| 린넨 셔츠 | `top` | `shirt_blouse` |

### 10.3 속성 추출

추출 대상은 아래와 같습니다.

- 상품명
- category
- subcategory
- 소재와 혼용률
- 핏
- 색상
- 계절
- TPO
- 세탁 및 관리
- 사이즈와 착용감

### 10.4 정규화

자유 텍스트를 taxonomy id로 바꿉니다.

예시:

```text
원문: 블랙 세미오버 자켓
정규화: colors=["black"], fit=["relaxed"], subcategory="jacket"
```

### 10.5 누락과 모호성 기록

입력에 없는 정보는 억지로 만들지 않습니다.

예시:

```text
원문: 코튼 소재의 티셔츠
```

이 문장은 소재명 `cotton`은 알 수 있지만 숫자 혼용률은 없습니다. 따라서 다음처럼 기록합니다.

```json
{
  "materials": [
    {
      "part": "unknown",
      "name": "cotton",
      "ratio": null,
      "ratio_status": "missing",
      "evidence": "코튼 소재"
    }
  ],
  "quality": {
    "missing_fields": ["material_ratio"]
  }
}
```

## 11. `validate.py` 상세 작동 방식

`validate.py`는 구조화 JSON이 프로젝트 계약을 지키는지 검사합니다.

실행 예:

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
```

### 11.1 입력 형태

`validate.py`는 여러 형태를 처리합니다.

단일 상품 JSON:

```json
{
  "schema_version": "0.1.0",
  "source": {},
  "product": {},
  "agent_descriptor": {},
  "quality": {}
}
```

상품 목록:

```json
[
  {"schema_version": "0.1.0", "source": {}, "product": {}, "agent_descriptor": {}, "quality": {}}
]
```

평가 fixture 형태:

```json
{
  "products": [
    {
      "product_id": "outer_dummy_000",
      "structured_product": {}
    }
  ]
}
```

### 11.2 기본 schema 검증

`validate.py`는 `jsonschema`의 `Draft202012Validator`를 사용합니다. 검사하는 항목은 아래와 같습니다.

- 필수 최상위 필드 존재 여부
- 추가 필드 금지
- 타입 일치 여부
- enum 허용 값 여부
- 문자열 길이
- `source_url` URI 형식
- `ratio_status`와 `ratio`의 관계

### 11.3 custom check

JSON Schema만으로 충분하지 않은 규칙은 Python 코드에서 추가로 검사합니다.

현재 custom check는 아래를 검사합니다.

| 검사 | 의미 |
|---|---|
| category 검사 | `out_of_scope`가 아니면 `outer` 또는 `top`이어야 함 |
| material part 검사 | `part`가 taxonomy의 `material_parts`에 있어야 함 |
| material name 검사 | `name`이 taxonomy의 `materials`에 있어야 함 |
| ratio status 검사 | `explicit`, `missing`, `ambiguous` 중 하나여야 함 |
| 부위별 합계 검사 | 같은 part의 explicit ratio 합이 100을 초과하면 오류 |
| missing 연동 | `ratio_status=missing`이 있으면 `quality.missing_fields`에 `material_ratio` 필요 |
| ambiguous 연동 | `ratio_status=ambiguous`가 있으면 `quality.ambiguous_fields`에 `material_ratio` 필요 |

### 11.4 종료 코드

| exit code | 의미 |
|---:|---|
| 0 | 유효함 |
| 1 | JSON은 읽었지만 검증 실패 |
| 2 | 런타임 오류 또는 dependency 문제 |

## 12. `dedup.py` 상세 작동 방식

`dedup.py`는 구조화 상품 JSON 목록을 입력받아 모든 상품쌍의 유사도 점수를 계산합니다.

실행 예:

```powershell
python src\skills\product-agentizer\scripts\dedup.py tests\fixtures\dedup\sample_products.json --pretty
```

### 12.1 점수 계산 방식

두 상품 사이의 점수는 여러 속성의 가중합입니다.

현재 가중치와 임계값은 실제 무신사 운영 데이터로 학습되거나 검증된 최종 운영 수치가 아닙니다. 이 값들은 구조화 상품 속성의 유사도를 설명 가능하게 합산하기 위한 **휴리스틱 baseline**입니다. 즉 상품 중복 판단에서 소재, 카테고리, 세부 형태, 색상, 제목 등이 상대적으로 중요하다는 도메인 직관을 수치로 둔 초기값입니다.

| 속성 | 최대 가중치 |
|---|---:|
| category 일치 | 0.18 |
| subcategory 일치 | 0.16 |
| materials 유사도 | 0.20 |
| colors 유사도 | 0.12 |
| fit 유사도 | 0.10 |
| seasons 유사도 | 0.08 |
| tpo_tags 유사도 | 0.08 |
| care 유사도 | 0.04 |
| title 토큰 유사도 | 0.14 |

합산 점수는 최대 1.0입니다.

목록형 속성은 Jaccard similarity를 사용합니다.

```text
Jaccard similarity = 교집합 크기 / 합집합 크기
```

예를 들어 두 상품의 색상이 아래와 같다고 하겠습니다.

```text
상품 A colors = {black, gray}
상품 B colors = {black, navy}
```

교집합은 `{black}` 1개이고, 합집합은 `{black, gray, navy}` 3개입니다. 따라서 색상 유사도는 `1/3`입니다. 색상 최대 가중치가 0.12이므로 점수 기여분은 `0.12 * 1/3 = 0.04`입니다.

### 12.2 decision 기준

점수에 따라 판정은 아래처럼 나뉩니다.

| 점수 | decision |
|---:|---|
| 0.78 이상 | `duplicate` |
| 0.55 이상 0.78 미만 | `possible_duplicate` |
| 0.55 미만 | `distinct` |

기본 출력 필터 `min_score`는 0.45입니다. 즉 점수가 0.45보다 낮은 쌍은 결과 목록에 나오지 않을 수 있습니다. 평가할 때는 목록에 없으면 `distinct`로 취급합니다.

실제 운영에 적용하려면 이 임계값도 고정값으로 취급하면 안 됩니다. 운영 데이터에서 사람이 라벨링한 상품쌍을 만든 뒤, 현재 점수로 `precision`, `recall`, false positive, false negative를 측정하면서 가중치와 임계값을 조정해야 합니다.

예를 들어 오탐을 줄여야 하는 운영이라면 `duplicate` 임계값을 높이고, 사람이 검토할 후보를 넓게 뽑는 운영이라면 `possible_duplicate` 임계값을 낮출 수 있습니다. 자동 병합에 가까운 용도라면 precision을 매우 높게 요구해야 하고, 검토 큐를 만드는 용도라면 recall을 더 중시할 수 있습니다.

운영 튜닝 흐름은 아래와 같습니다.

```text
상품쌍 데이터 수집
  ↓
사람이 duplicate / distinct 라벨링
  ↓
dedup feature와 점수 계산
  ↓
precision / recall / false positive / false negative 분석
  ↓
가중치와 threshold 조정
  ↓
재평가 후 운영 기준 확정
```

### 12.3 출력 예시

```json
{
  "duplicate_candidates": [
    {
      "left_id": "outer_linen_blazer_a",
      "right_id": "outer_linen_blazer_b",
      "score": 1.0,
      "decision": "duplicate",
      "matched_fields": ["category", "subcategory", "materials", "colors", "fit"],
      "reason": "score 1.00 from matched fields: category, subcategory, materials, colors, fit"
    }
  ]
}
```

## 13. 평가 스크립트 작동 방식

`tests/evaluate_product_agentizer.py`는 expected JSON과 actual JSON을 비교합니다.

실행 예:

```powershell
python tests\evaluate_product_agentizer.py --pretty
```

경로를 지정하면 특정 fixture를 평가할 수 있습니다.

```powershell
python tests\evaluate_product_agentizer.py `
  --inputs tests\fixtures\codex_subset\source_inputs.json `
  --expected tests\fixtures\codex_subset\expected_products.json `
  --actual tests\fixtures\codex_subset\actual_products.json `
  --dedup-labels tests\fixtures\codex_subset\duplicate_labels.json `
  --pretty
```

### 13.1 비교 대상 필드

평가 대상 필드는 아래와 같습니다.

```text
title
category
subcategory
materials
fit
colors
seasons
tpo_tags
care
size_info
quality.missing_fields
quality.ambiguous_fields
```

### 13.2 materials 비교 방식

소재는 단순히 소재명만 비교하지 않습니다. 아래 네 요소를 합친 token으로 비교합니다.

```text
part:name:ratio_status:ratio
```

예를 들어 아래 소재는:

```json
{
  "part": "fill",
  "name": "duck_down",
  "ratio": 80,
  "ratio_status": "explicit"
}
```

평가 token은 아래와 같습니다.

```text
fill:duck_down:explicit:80
```

따라서 소재명은 맞아도 부위나 혼용률 상태가 틀리면 별도 차이로 잡힙니다.

## 14. 지표 정의

### 14.1 True Positive, False Positive, False Negative

속성 비교에서 세 값은 다음을 의미합니다.

| 지표 | 의미 | 예시 |
|---|---|---|
| True Positive, TP | expected에도 있고 actual에도 있는 값 | expected colors에 `khaki`, actual colors에도 `khaki` |
| False Positive, FP | actual에는 있지만 expected에는 없는 값 | actual이 없는 `green`을 추가함 |
| False Negative, FN | expected에는 있지만 actual에는 없는 값 | expected의 `travel`을 actual이 누락함 |

### 14.2 Precision

Precision은 “추출한 것 중 맞은 비율”입니다.

```text
precision = TP / (TP + FP)
```

예를 들어 actual이 색상을 5개 추출했는데 그중 4개가 expected와 맞고 1개는 불필요한 값이면 precision은 `4 / 5 = 80%`입니다.

Precision이 낮다는 것은 대체로 과잉 추출 또는 잘못된 추출이 많다는 뜻입니다.

### 14.3 Recall

Recall은 “정답 중 찾아낸 비율”입니다.

```text
recall = TP / (TP + FN)
```

예를 들어 expected TPO 태그가 14개인데 actual이 11개만 맞히고 3개를 놓치면 recall은 `11 / 14 = 78.57%`입니다.

Recall이 낮다는 것은 대체로 누락이 많다는 뜻입니다.

### 14.4 Micro precision과 micro recall

Micro 지표는 모든 평가 필드의 TP, FP, FN을 합산한 뒤 한 번에 계산합니다.

예를 들어 필드별 precision을 평균 내는 방식이 아니라, 전체 token을 모두 모아 계산합니다.

```text
micro precision = 전체 TP / (전체 TP + 전체 FP)
micro recall = 전체 TP / (전체 TP + 전체 FN)
```

이 방식은 token 수가 많은 필드의 영향이 더 큽니다. 예를 들어 `materials`, `tpo_tags`, `size_info`처럼 값이 여러 개인 필드가 전체 점수에 더 많이 반영됩니다.

### 14.5 Schema-valid

Schema-valid는 출력 JSON이 `schema.json`과 `validate.py` custom check를 통과했는지를 의미합니다.

Schema-valid가 100%라는 것은 아래가 모두 맞았다는 뜻입니다.

- 필수 필드가 존재합니다.
- 허용되지 않은 추가 필드가 없습니다.
- enum 값이 schema와 taxonomy 안에 있습니다.
- `ratio_status`와 `ratio`의 관계가 맞습니다.
- `missing` 또는 `ambiguous` 혼용률이 `quality`에 반영되어 있습니다.

그러나 schema-valid가 100%라고 해서 모든 속성 추출이 정답이라는 뜻은 아닙니다. 구조가 올바른 것과 내용이 expected와 완전히 일치하는 것은 다른 문제입니다.

### 14.6 Dedup accuracy

Dedup accuracy는 라벨링한 상품쌍에서 `dedup.py`의 판정이 기대 판정과 일치한 비율입니다.

```text
duplicate_accuracy = correct_pair_decisions / total_pair_decisions
```

예를 들어 20개 상품쌍 중 20개를 모두 맞히면 100%입니다.

### 14.7 Cross-category high-confidence false duplicate

서로 다른 category, 예를 들어 `outer`와 `top` 사이에서 높은 확신의 `duplicate`가 나오면 위험합니다.

이 프로젝트에서는 점수 0.78 이상을 high-confidence duplicate로 봅니다. S7.5에서는 서로 다른 category 사이에서 이런 high-confidence false duplicate가 0건인지 확인했습니다.

### 14.8 자동 fetch 0건

실제 공개 샘플 검증에서 URL이 보존되어 있더라도, 플러그인이나 검증 스크립트가 URL을 자동으로 열면 정책 위반입니다.

자동 fetch 0건은 공개 URL을 출처 메타데이터로만 저장했고, 실행 입력은 사람이 짧게 확인해 붙여넣은 factual snippet이었다는 뜻입니다.

### 14.9 법적 적합/부적합 판정 0건

이 프로젝트는 상품정보 표기 규정의 적합 또는 부적합을 판정하지 않습니다.

따라서 출력이나 보고서에 `legal`, `illegal`, `위반`, `적합`, `부적합` 같은 판정을 생성하지 않는 것이 중요합니다. S7.5 실제 공개 snippet 검증에서는 법적 적합/부적합 판정이 0건임을 확인했습니다.

## 15. S5 더미 fixture 검증

S5의 목적은 평가 harness가 제대로 작동하는지 확인하는 것이었습니다.

### 15.1 데이터

| 파일 | 내용 |
|---|---|
| `tests/fixtures/evaluation/source_inputs.json` | 합성 입력 5건 |
| `tests/fixtures/evaluation/expected_products.json` | 정답 JSON |
| `tests/fixtures/evaluation/predicted_products.json` | 의도적으로 일부 차이가 있는 예측 JSON |
| `tests/fixtures/evaluation/duplicate_labels.json` | 중복/비중복 라벨 |

### 15.2 결과

| 항목 | 결과 |
|---|---:|
| 입력 케이스 | 5 |
| expected schema 검증 | 통과, 5건 |
| predicted schema 검증 | 통과, 5건 |
| 속성 micro precision | 98.55% |
| 속성 micro recall | 88.31% |
| 중복 감지 정확도 | 100.00% (10/10) |

### 15.3 해석

S5에서 precision은 높았지만 recall은 상대적으로 낮았습니다. 이는 잘못된 값을 많이 추가한 문제보다는, expected에 있어야 할 값을 일부 놓친 문제가 더 컸다는 뜻입니다.

확인된 주요 누락은 아래였습니다.

| 케이스 | 문제 |
|---|---|
| `outer_down_layerpiece` | `goose_down`, `travel`, `암홀 여유` 누락, `khaki`를 `green`으로 예측 |
| `top_linen_blouse` | `rayon`, `spring`, `formal`, `가슴둘레 여유` 누락 |
| `top_washable_tee` | `layering` 누락 |

### 15.4 보완

S5 결과를 바탕으로 다음 지침을 강화했습니다.

- 복합 소재를 모두 분리합니다.
- `카키`처럼 구체 id가 있는 색상은 넓은 색상군보다 구체 id를 우선합니다.
- `봄여름`, `가을겨울`은 계절을 복수로 기록합니다.
- `이너`, `레이어드`, `여행용`, `포멀한` 같은 TPO 단서를 놓치지 않습니다.
- `암홀 여유`, `가슴둘레 여유` 같은 착용감 정보를 `size_info`에 보존합니다.

## 16. S6 Codex CLI 실제 실행 검증

S6의 목적은 플러그인이 문서와 스크립트로만 존재하는 것이 아니라, 실제 Codex CLI 흐름에서 사용 가능한지 확인하는 것이었습니다.

### 16.1 검증한 내용

- 로컬 marketplace 등록
- 플러그인 후보 목록 확인
- 플러그인 설치
- `codex exec` smoke test
- 상품 텍스트를 실제 Codex로 구조화 JSON 변환
- 변환 결과를 `validate.py`로 검증
- 구조화 JSON을 기반으로 자연어 질의 답변 시연

### 16.2 주요 결과

`outer_down_layerpiece` 입력에 대해 Codex가 생성한 출력은 아래 핵심 값을 유지했습니다.

| 속성 | 결과 |
|---|---|
| title | `카키 릴랙스 다운 베스트` |
| category/subcategory | `outer` / `vest` |
| materials | `shell:nylon:100`, `fill:duck_down:80`, `fill:goose_down:20` |
| colors | `khaki` |
| seasons | `fall`, `winter` |
| tpo_tags | `layering`, `outdoor`, `travel` |
| size_info | `L 기준 총장 68cm`, `여유 있는 암홀` |

`validate.py` 결과는 다음과 같았습니다.

```json
{
  "valid": true,
  "checked": 1,
  "errors": []
}
```

### 16.3 의미

S5에서 보완한 `goose_down`, `khaki`, `travel`, `암홀` 누락 문제가 S6 실제 Codex 출력에서는 개선되었습니다.

다만 전역 Codex 설정에는 기존 stale marketplace 문제가 있어, 이번 검증에서는 임시 `CODEX_HOME`으로 로컬 plugin 설치 흐름을 분리해 확인했습니다.

## 17. S7.5 확장 검증 및 재현성 보존

S7.5의 목적은 “검증을 했다”는 선언이 아니라, 누가 다시 실행해도 같은 입력, 명령, 결과를 추적할 수 있게 보존하는 것이었습니다.

### 17.1 보존된 데이터

| 폴더 | 내용 |
|---|---|
| `tests/fixtures/expanded_dummy/` | 합성 입력 100건, expected JSON, reference actual JSON, duplicate labels |
| `tests/fixtures/codex_subset/` | Codex 실행 subset 20건, prompt, expected JSON, actual JSON, duplicate labels |
| `tests/fixtures/real_sanity/` | 실제 공개 snippet 10건, URL, 확인일, expected JSON, actual JSON, duplicate labels |
| `docs/reports/s7-expanded-validation-results.json` | 실행 환경, 명령, 결과, SHA-256 hash |

### 17.2 합성 더미 100건

합성 더미는 `outer` 50건, `top` 50건으로 구성했습니다.

포함한 케이스는 아래와 같습니다.

- 명시 혼용률
- 누락 혼용률
- 모호 혼용률
- 부위별 소재
- 복합 계절
- TPO 태그
- 색상 alias
- size_info
- 중복 상품쌍과 비중복 상품쌍

결과:

| 지표 | 결과 | 해석 |
|---|---:|---|
| expected schema-valid | 100/100 | 모든 expected JSON이 schema와 custom check를 통과 |
| self-check micro precision | 100.00% | reference actual이 expected와 완전히 일치 |
| self-check micro recall | 100.00% | expected 값 누락 없음 |
| dedup accuracy | 100.00% (20/20) | 라벨링한 20개 중복/비중복 쌍 모두 정답 |
| cross-category high-confidence false duplicate | 0건 | category가 다른 상품 사이의 고확신 오탐 없음 |

여기서 self-check는 모델 성능 검증이 아니라 fixture와 평가 도구가 서로 일관되는지 확인하는 기준선입니다.

### 17.3 Codex subset 20건

합성 100건 중 난이도와 대표성을 고려해 20건을 뽑아 실제 Codex 변환 대상으로 사용했습니다.

결과:

| 지표 | 결과 | 판정 |
|---|---:|---|
| actual schema-valid | 20/20 | 통과 |
| micro precision | 95.52% | 통과, 목표 95% 이상 |
| micro recall | 95.85% | 통과, 목표 85% 이상 |
| detail_type precision/recall | not_applicable | historical actual 보존을 위해 expected/actual 모두 `null` |

`codex_subset` actual은 3단계 taxonomy 도입 이전에 생성한 historical Codex 출력을 기준으로 한다. 따라서 상품 속성 값은 보존하고, 현재 schema `0.2.0`에 맞추기 위해 `schema_version`과 `product.detail_type: null`만 추가한 호환 마이그레이션본이다. 이 세트는 기존 actual의 재현성과 전체 속성 precision/recall을 확인하는 용도이며, `detail_type`의 실제 추출 성능을 측정하는 세트는 아니다.
| dedup accuracy | 100.00% (4/4) | 통과 |

필드별 결과:

| 필드 | Precision | Recall | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| title | 100.00% | 100.00% | 20 | 0 | 0 |
| category | 100.00% | 100.00% | 20 | 0 | 0 |
| subcategory | 100.00% | 100.00% | 20 | 0 | 0 |
| materials | 91.67% | 91.67% | 33 | 3 | 3 |
| fit | 100.00% | 100.00% | 20 | 0 | 0 |
| colors | 100.00% | 100.00% | 20 | 0 | 0 |
| seasons | 100.00% | 100.00% | 34 | 0 | 0 |
| tpo_tags | 100.00% | 81.63% | 40 | 0 | 9 |
| care | 100.00% | 100.00% | 20 | 0 | 0 |
| size_info | 100.00% | 100.00% | 40 | 0 | 0 |
| quality.missing_fields | 16.67% | 100.00% | 2 | 10 | 0 |
| quality.ambiguous_fields | 100.00% | 100.00% | 8 | 0 | 0 |

해석:

- `title`, `category`, `subcategory`, `fit`, `colors`, `seasons`, `care`, `size_info`는 100% 일치했습니다.
- `materials`는 일부 부위, 소재, 상태, 비율 조합에서 차이가 있었습니다.
- `tpo_tags`는 precision 100%이지만 recall 81.63%입니다. 즉 잘못 추가한 TPO는 없었지만 expected에 있던 일부 TPO를 놓쳤습니다.
- `quality.missing_fields`는 recall 100%이지만 precision 16.67%입니다. 즉 expected가 요구한 누락 표시는 모두 잡았지만, Codex가 더 보수적으로 누락 필드를 추가 표시했습니다.

Acceptance 관점에서는 전체 micro precision과 recall이 기준을 넘었고 schema-valid와 dedup도 통과했습니다.

### 17.4 실제 공개 snippet 10건

실제 공개 샘플은 아우터 5건, 상의 5건입니다. 전체 상세페이지 사본을 저장하지 않고, 상품명, 소재, 컬러, 사이즈, 관리처럼 검증에 필요한 짧은 factual snippet만 보존했습니다.

URL은 메타데이터로만 보존했습니다.

```text
https://www.musinsa.com/products/4308999
https://www.musinsa.com/products/2101205
https://www.musinsa.com/products/4922894
https://www.musinsa.com/products/3617977
https://www.musinsa.com/products/4332165
https://www.musinsa.com/products/4783312
https://www.musinsa.com/products/3054408
https://www.musinsa.com/products/3661999
https://www.musinsa.com/products/3054409
https://www.musinsa.com/products/1196892
```

Acceptance 결과:

| 지표 | 결과 | 판정 |
|---|---:|---|
| actual schema-valid | 10/10 | 통과 |
| 자동 fetch | 0건 | 통과 |
| 법적 적합/부적합 판정 | 0건 | 통과 |
| dedup accuracy | 100.00% (5/5) | 통과 |

탐색적 속성 비교:

| 지표 | 결과 |
|---|---:|
| micro precision | 64.38% |
| micro recall | 76.30% |
| detail_type precision | 100.00% |
| detail_type recall | 100.00% |

이 수치는 acceptance gate가 아닙니다. 실제 공개 snippet은 전체 상세페이지를 복사한 정답 데이터가 아니라, 짧은 사실성 snippet입니다. 따라서 Codex actual과 expected 사이의 차이는 모델 성능만을 뜻하지 않고, snippet의 제한성과 expected 라벨링 방식의 차이도 함께 반영합니다.

필드별 탐색 결과:

| 필드 | Precision | Recall | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| title | 100.00% | 100.00% | 10 | 0 | 0 |
| category | 100.00% | 100.00% | 10 | 0 | 0 |
| subcategory | 100.00% | 100.00% | 10 | 0 | 0 |
| materials | 73.33% | 73.33% | 11 | 4 | 4 |
| fit | 66.67% | 20.00% | 2 | 1 | 8 |
| colors | 54.55% | 60.00% | 6 | 5 | 4 |
| seasons | 81.25% | 86.67% | 13 | 3 | 2 |
| tpo_tags | 84.38% | 100.00% | 27 | 5 | 0 |
| care | 100.00% | 100.00% | 1 | 0 | 0 |
| size_info | 0.00% | 0.00% | 0 | 8 | 13 |
| quality.missing_fields | 3.45% | 100.00% | 1 | 28 | 0 |
| quality.ambiguous_fields | 40.00% | 66.67% | 2 | 3 | 1 |

해석:

- `title`, `category`, `subcategory`는 100% 일치했습니다.
- `size_info`는 snippet 기반 expected와 Codex actual의 보존 방식이 크게 달라 0%로 나왔습니다.
- `quality.missing_fields`는 Codex가 더 보수적으로 누락을 많이 표시해 FP가 많았습니다.
- 이 결과는 실제 상품 데이터의 전체 성능 벤치마크가 아니라, 안전 정책을 지키면서 현실적인 입력에서도 schema-valid 출력이 가능한지 확인하는 sanity check입니다.

## 18. 재현성 설계

S7.5 이후에는 아래 파일만 있으면 검증을 재실행할 수 있습니다.

### 18.1 확장 fixture 재생성

```powershell
python tools\generate_expanded_validation_fixtures.py
```

이 명령은 다음을 재생성합니다.

- `tests/fixtures/expanded_dummy/source_inputs.json`
- `tests/fixtures/expanded_dummy/expected_products.json`
- `tests/fixtures/expanded_dummy/reference_actual_products.json`
- `tests/fixtures/expanded_dummy/duplicate_labels.json`
- `tests/fixtures/codex_subset/source_inputs.json`
- `tests/fixtures/codex_subset/expected_products.json`
- `tests/fixtures/codex_subset/prompt.md`
- `tests/fixtures/real_sanity/source_inputs.json`
- `tests/fixtures/real_sanity/expected_products.json`
- `tests/fixtures/real_sanity/prompt.md`

주의할 점은 Codex actual output은 모델 실행 결과이므로 재생성 시 달라질 수 있다는 것입니다. 제출 기준 actual은 `actual_products.json`에 보존되어 있습니다.

### 18.2 전체 확장 검증 실행

```powershell
python tools\run_expanded_validation.py
```

이 명령은 아래 검증을 순서대로 실행합니다.

| command id | 내용 |
|---|---|
| `expanded_expected_schema` | 합성 expected 100건 schema 검증 |
| `expanded_selfcheck_eval` | 합성 expected와 reference actual 비교 |
| `codex_subset_actual_schema` | Codex subset actual 20건 schema 검증 |
| `codex_subset_eval` | Codex subset expected와 actual 비교 |
| `real_sanity_actual_schema` | 실제 공개 snippet actual 10건 schema 검증 |
| `real_sanity_eval_exploratory` | 실제 공개 snippet expected와 actual 탐색 비교 |

결과는 아래에 저장됩니다.

```text
docs/reports/s7-expanded-validation-results.json
```

### 18.3 결과 스냅샷에 포함되는 정보

`s7-expanded-validation-results.json`에는 다음이 들어 있습니다.

- 생성 시각
- KST 기준 날짜
- Python 버전
- OS platform
- Codex CLI 버전
- 실행한 명령 배열
- 각 명령의 exit code
- 각 명령의 stdout JSON
- stderr
- 주요 파일의 SHA-256 hash
- cross-category high-confidence duplicate 점검 결과
- acceptance summary

이 hash는 나중에 “같은 입력과 같은 코드로 검증했는가?”를 확인하는 감사 추적용입니다.

## 19. 실패 사례와 보완 이력

### 19.1 S5에서 드러난 품질 이슈

S5에서는 평가 harness가 아래 문제를 잡아냈습니다.

- 복합 소재 뒤쪽 항목 누락
- `카키`를 `green`으로 넓게 매핑
- 복합 계절 일부 누락
- TPO 단서 일부 누락
- 착용감 문구 일부 누락

이에 따라 `SKILL.md`와 `taxonomy.json`의 지침과 alias를 강화했습니다.

### 19.2 S7.5 구현 중 발생한 실제 오류

S7.5 구현 중에는 아래 실제 오류가 있었습니다.

| 문제 | 원인 | 조치 |
|---|---|---|
| duplicate case title 경로 오류 | fixture 생성기에서 중첩 경로를 잘못 참조 | `structured_product.product.title` 경로 사용 |
| real sanity tuple 위치 오류 | expected 생성 spec의 인자 순서 어긋남 | spec 구조 분리 |
| custom 상대 경로 오류 | 평가 스크립트가 `relative_to(ROOT)`에서 실패 | repo root 기준으로 resolve 후 표시 경로 계산 |
| 한글 출력 깨짐 | Windows 콘솔 인코딩 문제 | 평가 스크립트 stdout UTF-8 고정 |
| subset/real label 부족 | 각 fixture별 duplicate label 필요 | 폴더별 label 파일 보존 |

이 내용은 `Troubleshootinglog.md`에도 기록되어 있습니다.

## 20. 로그 저장 방식

`tools/save_log.py`는 Stop hook helper입니다. Claude Code 또는 Codex의 Stop hook이 실행될 때 대화 transcript를 읽어 `logs/` 아래에 저장합니다.

출력 구조는 아래와 같습니다.

```text
logs/
├── claude-code/
│   └── <session_id>.jsonl
└── codex/
    └── <session_id>.jsonl
```

이 스크립트의 핵심 정책은 다음과 같습니다.

- stdout에 아무것도 쓰지 않아 hook 판단을 방해하지 않습니다.
- 실패해도 exit code 0으로 종료해 작업 세션을 막지 않습니다.
- 가능한 경우 user/assistant 대화 텍스트가 있는 JSONL 라인만 보존합니다.
- 파싱이 불확실하면 원본 transcript를 그대로 복사하는 fallback을 사용합니다.
- Windows에서 한글 경로가 깨지지 않도록 stdin payload를 UTF-8 bytes로 읽습니다.

`logs/`는 gitignore 대상이지만, 최종 제출 zip에는 포함해야 하는 폴더입니다. 로그는 과제 규정상 원본 보존이 중요하므로 수동 편집하지 않는 것이 원칙입니다.

## 21. 안전성과 범위 제한

이 프로젝트의 안전 경계는 명확합니다.

### 21.1 하지 않는 것

- 자동 크롤링을 하지 않습니다.
- 상품 페이지 URL을 자동으로 열지 않습니다.
- 내부 데이터나 고객 데이터를 사용하지 않습니다.
- 법적 적합/부적합 판정을 하지 않습니다.
- 상품 추천 랭킹을 만들지 않습니다.
- 가격, 재고, 트렌드 예측을 하지 않습니다.
- 아우터와 상의 밖의 카테고리를 완전히 지원한다고 주장하지 않습니다.

### 21.2 하는 것

- 사용자가 붙여넣은 상품 상세 텍스트를 읽습니다.
- 입력 근거가 있는 속성을 추출합니다.
- taxonomy id로 정규화합니다.
- schema-valid JSON을 만듭니다.
- 누락과 모호성을 `quality`에 남깁니다.
- 중복 후보 점수를 계산합니다.
- 검증 결과를 재현 가능하게 보존합니다.

## 22. 통과 기준과 현재 상태

현재 주요 acceptance 기준과 상태는 다음과 같습니다.

| 기준 | 현재 상태 |
|---|---|
| `src/.codex-plugin/plugin.json` 존재 | 통과 |
| `src/skills/product-agentizer/SKILL.md` 존재 | 통과 |
| `schema.json`, `taxonomy.json` 존재 | 통과 |
| `validate.py`, `dedup.py` 존재 | 통과 |
| 정상 schema fixture 통과 | 통과 |
| 오류 schema fixture 실패 | 통과 |
| S5 더미 평가 수행 | 통과 |
| S6 Codex CLI 실제 실행 | 통과 |
| S7.5 합성 expected 100건 schema-valid | 통과, 100/100 |
| S7.5 Codex subset schema-valid | 통과, 20/20 |
| S7.5 Codex subset micro precision | 통과, 95.52% |
| S7.5 Codex subset micro recall | 통과, 95.85% |
| S7.5 dedup accuracy | 통과 |
| 실제 공개 snippet 자동 fetch | 통과, 0건 |
| 실제 공개 snippet 법적 판정 | 통과, 0건 |
| cross-category high-confidence false duplicate | 통과, 0건 |

## 23. 실행 명령 모음

### 23.1 dependency 설치

```powershell
python -m pip install jsonschema
```

### 23.2 schema 검증

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
```

### 23.3 오류 fixture 검증

아래 fixture들은 실패해야 정상입니다.

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_missing_quality.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_out_of_scope_category.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_material_ratio_status.json --pretty
```

### 23.4 중복 후보 감지

```powershell
python src\skills\product-agentizer\scripts\dedup.py tests\fixtures\dedup\sample_products.json --pretty
```

### 23.5 기본 평가

```powershell
python tests\evaluate_product_agentizer.py --pretty
```

### 23.6 확장 검증

```powershell
python tools\run_expanded_validation.py
```

## 24. 패키징 관점

최종 제출 zip의 핵심 구조는 아래입니다.

```text
submission.zip
├── src/
│   ├── .codex-plugin/
│   │   └── plugin.json
│   └── skills/
│       └── product-agentizer/
│           ├── SKILL.md
│           ├── references/
│           │   ├── schema.json
│           │   └── taxonomy.json
│           └── scripts/
│               ├── validate.py
│               └── dedup.py
├── README.md
└── logs/
```

`docs/`와 `tests/`는 내부 검증과 감사 추적에는 중요하지만, 현재 과제 제출 구조 기준의 필수 제출 대상은 아닙니다. 다만 제출 전에는 `docs/reports/`와 `tests/fixtures/`를 기준으로 검증이 완료되었는지 확인합니다.

## 25. 주요 한계

현재 구현의 한계는 다음과 같습니다.

- MVP는 `outer`, `top`만 지원합니다.
- 실제 무신사 내부 카탈로그 데이터는 사용하지 않았습니다.
- 실제 공개 샘플은 10건의 짧은 snippet sanity check로 제한했습니다.
- 공개 상품 전체 상세페이지 사본을 저장하지 않았습니다.
- 실제 공개 snippet의 precision/recall은 acceptance 지표가 아니라 탐색 지표입니다.
- 법적 검수 기능이 아닙니다.
- 중복 감지는 후보 점수화이며, 운영상 삭제 또는 병합을 자동 결정하지 않습니다.

## 26. 향후 개선 가능성

후속 개선을 한다면 아래가 우선순위가 높습니다.

1. 실제 공개 snippet의 `size_info` 라벨링 기준과 Codex 출력 기준을 맞춥니다.
2. `quality.missing_fields`가 지나치게 보수적으로 늘어나는 문제를 완화합니다.
3. `materials`의 부위 추론을 더 안정화합니다.
4. `tpo_tags` recall을 높이기 위해 TPO alias와 체크리스트를 보강합니다.
5. category 확장이 필요하면 schema와 taxonomy를 함께 version up합니다.
6. 실제 운영 적용 시에는 내부 데이터 접근 정책, 개인정보 정책, 약관, 상품정보 고시 규정을 별도 검토합니다.

## 27. 빠른 이해를 위한 예시

입력:

```text
상품명: 블랙 세미 오버핏 자켓.
제품분류: 재킷.
색상: 블랙.
겉감 폴리에스터 100%, 안감 폴리에스터 100%.
봄가을 출근룩과 세미포멀 코디에 적합합니다.
반드시 드라이클리닝하십시오.
```

출력 핵심:

```json
{
  "schema_version": "0.1.0",
  "source": {
    "source_url": null,
    "source_title": "블랙 세미 오버핏 자켓",
    "input_mode": "pasted_text"
  },
  "product": {
    "title": "블랙 세미 오버핏 자켓",
    "category": "outer",
    "subcategory": "jacket",
    "materials": [
      {
        "part": "shell",
        "name": "polyester",
        "ratio": 100,
        "ratio_status": "explicit",
        "evidence": "겉감 폴리에스터 100%"
      },
      {
        "part": "lining",
        "name": "polyester",
        "ratio": 100,
        "ratio_status": "explicit",
        "evidence": "안감 폴리에스터 100%"
      }
    ],
    "fit": ["relaxed"],
    "colors": ["black"],
    "seasons": ["spring", "fall"],
    "tpo_tags": ["commute", "formal", "layering"],
    "care": ["dry_clean"],
    "size_info": []
  },
  "agent_descriptor": {
    "search_summary": "블랙 세미 오버핏 재킷으로 봄가을 출근룩과 세미포멀 코디에 적합합니다.",
    "query_tags": ["블랙 재킷", "출근룩 자켓", "세미포멀 아우터"],
    "explainable_reasons": [
      "재킷 표현을 jacket으로 정규화했습니다.",
      "세미 오버핏은 relaxed 핏으로 정규화했습니다.",
      "봄가을은 spring, fall로 분리했습니다."
    ]
  },
  "quality": {
    "missing_fields": [],
    "ambiguous_fields": [],
    "out_of_scope": false,
    "confidence": "high"
  }
}
```

이 예시에서 주목할 점은 아래와 같습니다.

- `자켓`은 `jacket`으로 정규화됩니다.
- `세미 오버핏`은 taxonomy alias에 따라 `relaxed`로 정규화됩니다.
- `봄가을`은 `spring`, `fall` 두 계절로 분리됩니다.
- 겉감과 안감은 각각 별도 소재 항목으로 분리됩니다.
- 혼용률 숫자가 있으므로 `ratio_status`는 `explicit`입니다.
- 법적 적합성 판단은 하지 않습니다.

## 28. 결론

현재 구현은 무신사 문제 2의 MVP 범위에서 다음을 충족합니다.

- 사용자가 붙여넣은 상품 상세 텍스트를 구조화 JSON으로 변환합니다.
- 아우터와 상의에 대해 표준 taxonomy 매핑을 수행합니다.
- 소재 혼용률을 추정하지 않고 근거 기반으로 기록합니다.
- 누락과 모호성을 `quality`에 남깁니다.
- 구조화 JSON의 schema-valid 여부를 결정적으로 검증합니다.
- 구조화 상품 간 중복 후보를 점수화합니다.
- 합성 100건, Codex subset 20건, 실제 공개 snippet 10건으로 확장 검증을 수행했습니다.
- 입력, expected, actual, 명령, 결과, hash를 보존해 재현성을 확보했습니다.

따라서 이 프로젝트는 “AI가 상품 텍스트를 읽었다” 수준이 아니라, Codex 플러그인, schema 계약, taxonomy, deterministic validator, dedup scorer, 재현 가능한 fixture와 보고서를 함께 갖춘 상품 데이터 에이전트화 변환 MVP입니다.
