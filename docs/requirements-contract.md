# 기준 계약 문서 · 무신사 상품 데이터 에이전트화 변환기

> 구현 전에 합의해 고정한다. 기준이 바뀌면 코드보다 이 문서를 먼저 갱신하고 Decisionlog에 이유를 남긴다. 같은 지표가 파일마다 다르게 정의되지 않게 한다.

## 문제와 목표
- 확정 기업·문제: 무신사 / 문제 2 `상품 데이터 에이전트화 변환기`
- 목표: 상품 상세페이지의 비정형 텍스트를 AI 에이전트가 질의·필터·설명할 수 있는 구조화 JSON으로 변환한다.
- MVP 범위: 아우터·상의 2개 카테고리.
- 비목표: 상품정보 표기 규정 검수(무신사 문제 1), 실시간 크롤러, 내부 카탈로그 연동, 랭킹/추천 모델 학습, 전체 무신사 상품 커버리지.

## 입력 형식
### 단일 상품 변환 입력
```json
{
  "product_text": "상품 상세페이지에서 사용자가 직접 붙여넣은 비정형 텍스트",
  "source_url": "선택: 출처 기록용 공개 URL. 플러그인이 자동 fetch하지 않음",
  "source_title": "선택: 상품명 또는 페이지 제목",
  "category_hint": "선택: outer | top",
  "locale": "ko-KR"
}
```

### 중복 감지 입력
```json
{
  "products": [
    {
      "product_id": "선택: 사용자가 붙인 임시 ID",
      "structured_product": "{단일 상품 변환 출력 JSON}"
    }
  ]
}
```

### 허용 입력
- 사용자가 직접 붙여넣은 상품 상세 텍스트
- 사용자가 출처로 기록한 공개 URL과 제목
- 합성 더미 픽스처
- 사람이 소량으로 확인한 공개 상품 샘플 텍스트

### 비허용 입력
- 플러그인이 제3자 사이트에서 자동 수집한 상품 페이지
- 로그인·권한이 필요한 내부 데이터
- 실제 고객정보, 계좌정보, API 키, 세션 쿠키, 액세스 토큰
- 제3자 리뷰·커뮤니티 등 UGC 대량 수집 데이터

## 출력 형식
단일 상품 변환은 아래 구조의 JSON을 출력한다. 실제 스키마는 `src/skills/product-agentizer/references/schema.json`에 구현한다.

```json
{
  "schema_version": "0.2.0",
  "source": {
    "source_url": "선택",
    "source_title": "선택",
    "input_mode": "pasted_text"
  },
  "product": {
    "title": "추출 또는 정규화된 상품명",
    "category": "outer | top",
    "subcategory": "선택",
    "detail_type": "선택: 공식 몰 세부 유형 또는 null",
    "materials": [
      {
        "part": "shell | lining | fill | rib | pocket | trim | unknown",
        "name": "표준 소재명",
        "ratio": 0,
        "ratio_status": "explicit | missing | ambiguous",
        "evidence": "입력 텍스트 근거"
      }
    ],
    "fit": ["표준 핏/실루엣 태그"],
    "colors": ["표준 컬러명"],
    "seasons": ["spring", "summer", "fall", "winter"],
    "tpo_tags": ["예: 하객룩", "예: 출근룩"],
    "care": ["세탁/관리 정보"],
    "size_info": ["M", "L", "XL", "M 총장 68cm 어깨 52cm 가슴 60cm"]
  },
  "agent_descriptor": {
    "search_summary": "에이전트 질의에 쓰기 쉬운 요약",
    "query_tags": ["자연어 질의 매칭 태그"],
    "explainable_reasons": ["왜 해당 태그와 연결되는지"]
  },
  "quality": {
    "missing_fields": ["부족한 속성"],
    "ambiguous_fields": ["모호한 속성"],
    "out_of_scope": false,
    "confidence": "high | medium | low"
  }
}
```

중복 감지는 상품 쌍 또는 후보군별로 아래를 출력한다.
```json
{
  "duplicate_candidates": [
    {
      "left_id": "상품 A",
      "right_id": "상품 B",
      "score": 0.0,
      "decision": "duplicate | possible_duplicate | distinct",
      "matched_fields": ["category", "materials", "fit"],
      "reason": "판정 근거"
    }
  ]
}
```

중복 감지 점수의 가중치와 `duplicate`/`possible_duplicate` 임계값은 실제 운영 데이터로 학습된 최종 수치가 아니라, 더미 fixture에서 동작을 확인하기 위한 설명 가능한 휴리스틱 baseline이다. 실제 운영 적용 시에는 사람이 라벨링한 상품쌍을 기준으로 precision, recall, false positive, false negative를 비교하며 가중치와 임계값을 재튜닝해야 한다.

### size_info 표준화 계약(schema v0.2)

현재 `schema_version: "0.2.0"`에서 `product.size_info`는 문자열 배열을 유지한다. 다만 각 문자열은 에이전트 질의에 재사용하기 쉬운 최소 의미 단위로 보존한다.

- 판매 옵션은 개별 값으로 원자화한다.
  - `사이즈 옵션: M, L, XL` -> `["M", "L", "XL"]`
  - `옵션: S/M/L` -> `["S", "M", "L"]`
  - `SIZE: 90 95 100` -> `["90", "95", "100"]`
  - `사이즈 옵션: 44, 55, 66` -> `["44", "55", "66"]`
  - `사이즈: 1 / 2 / 3` -> `["1", "2", "3"]`
  - `M(95), L(100), XL(105)` -> `["M(95)", "L(100)", "XL(105)"]`
- 단일 옵션은 그대로 한 항목으로 보존한다.
  - `FREE`, `ONE SIZE`, `OS` 등
- 실측표는 사이즈별 행 단위로 보존한다.
  - `M 총장 68cm 어깨 52cm 가슴 60cm`
  - `L 총장 70cm 어깨 54cm 가슴 62cm`
  - 표 형태 입력(`사이즈(cm) 총장 어깨 가슴 소매 / M 68 50 58 60`)도 행 단위 문자열로 정리한다.
- 모델 착용 정보는 입력에 명시된 경우 size 관련 설명으로 보존할 수 있다.
  - `모델 178cm L 착용`
- 무신사 스탠다드 등 기준 상품과의 사이즈 비교 문구는 입력에 명시된 경우 보존할 수 있다.
  - `무신사 스탠다드 M 사이즈 티셔츠와 비슷한 사이즈`
- 후기, 배송, 쿠폰, 이벤트, 마케팅 문구는 size_info에 넣지 않는다.
  - `후기 요약: 사이즈가 여유 있어요`는 구매자 반응 요약이므로 size_info가 아니다.
- 개인화·통계형 추천 문구는 정적 상품 사이즈가 아니므로 size_info에 넣지 않는다.
  - `178cm 70kg 고객은 L을 많이 선택`, `사이즈 만족도 적당함 82%`
- 입력에 사이즈 정보가 없으면 `size_info: []`로 두고 `quality.missing_fields`에 `size_info`를 추가한다.
- 모호한 사이즈 표현은 단정하지 않고, 보존할 필요가 있으면 입력 구절 그대로 남기며 `quality.ambiguous_fields`에 `size_info`를 추가한다.

이 계약은 schema 구조를 바꾸지 않는 SKILL-only 개선 기준이다. 판매 옵션, 실측표, 모델 착용 정보를 객체로 구분해야 할 필요가 생기면 `docs/size-info-schema-change-plan.md`의 schema v0.3 계획을 재검토한다.

## 주요 지표 정의
- 속성 precision: 추출된 속성 중 정답 라벨과 일치한 속성의 비율.
- 속성 recall: 정답 라벨 중 플러그인이 올바르게 추출한 속성의 비율.
- taxonomy 매핑 정확도: 자유표기 입력을 기대 표준용어로 매핑한 비율.
- 중복 감지 정확도: 더미 중복쌍/비중복쌍에서 `dedup.py` 판정이 정답과 일치한 비율.
- 스키마 유효성: 출력 JSON이 `schema.json`을 통과하는지 여부.

## 수식
- `precision = true_positive / (true_positive + false_positive)`
- `recall = true_positive / (true_positive + false_negative)`
- `duplicate_accuracy = correct_pair_decisions / total_pair_decisions`
- 지표 산출 시 분모가 0이면 해당 지표는 `not_applicable`로 표기하고 평균에서 제외한다.

## 상태 판정 기준
- `valid`: schema 통과, 지원 카테고리, 필수 속성 일부 이상 추출, 치명 오류 없음.
- `needs_review`: schema는 통과하지만 핵심 속성이 부족하거나 모호 속성이 많아 사람이 검토해야 함.
- `out_of_scope`: 아우터·상의가 아니거나 상품 상세정보가 아닌 입력.
- `invalid`: JSON 형식 오류, 필수 최상위 필드 누락, 비허용 입력 감지.

## 오류 판정 기준
- 필수 필드 누락: `schema_version`, `product`, `quality` 등 schema 필수 항목 없음.
- 타입 오류: 문자열/배열/숫자 등 schema 타입 불일치.
- 지원 범위 밖: `category`가 `outer` 또는 `top`이 아님.
- 근거 부족: 추출 속성에 입력 텍스트 근거가 없거나 추론만으로 단정.
- 안전 위반: 자동 크롤링, 비밀정보, 내부 데이터, 대량 UGC 수집 의존.

## 허용 값 / 허용하지 않을 값
- 허용 카테고리: `outer`, `top`
- 허용 locale: `ko-KR` 우선. 다른 locale은 `needs_review` 또는 `out_of_scope`로 처리한다.
- 허용 confidence: `high`, `medium`, `low`
- 허용 중복 판정: `duplicate`, `possible_duplicate`, `distinct`
- 비허용: 출처 없는 숫자 단정, 공개 자료로 확인할 수 없는 사실, 내부 데이터 전제, 자동 크롤링 결과
- 소재 혼용률 허용 원칙:
  - 입력 텍스트에 숫자 혼용률이 명시된 경우에만 `ratio_status: "explicit"`과 숫자 `ratio`를 기록한다.
  - 숫자 혼용률이 없으면 `ratio: null`, `ratio_status: "missing"`으로 기록하고 `quality.missing_fields`에 `material_ratio`를 넣는다.
  - "혼방", "터치", "느낌", "라이크"처럼 소재감만 암시하는 표현은 `ratio: null`, `ratio_status: "ambiguous"`로 기록하고 `quality.ambiguous_fields`에 `material_ratio`를 넣는다.
  - 겉감, 안감, 충전재, 립 등 부위가 다르면 `part`를 분리해 기록한다. 부위를 확인할 수 없으면 `part: "unknown"`으로 둔다.
  - 소재 항목 중 하나라도 `part: "unknown"`이면 입력에서 소재 부위를 확인할 수 없다는 뜻이므로 `quality.missing_fields`에 `material_part`를 넣는다.
  - `배색 폴리에스터`처럼 배색 표현이 있지만 카라, 소매, 포켓, 배색부 등 구체 부위가 명시되지 않은 소재는 `trim`으로 단정하지 않고 `part: "unknown"`으로 둔다.
  - `배색부 폴리에스터`, `카라 배색 폴리에스터`, `소매 배색 폴리에스터`처럼 실제 적용 부위가 명시된 경우에만 `trim` 또는 더 구체적인 부위(`pocket`, `rib` 등)를 사용한다.
  - 이 플러그인은 상품정보 표기 규정 적합/부적합을 판정하지 않는다. 입력 텍스트에 근거가 있는 소재 정보를 구조화하고, 부족·모호한 혼용률을 표시하는 데 한정한다.

## 누락 데이터 처리
- 입력에 없는 속성은 만들지 않고 `quality.missing_fields`에 기록한다.
- 모호한 표현은 단정하지 않고 `quality.ambiguous_fields`에 기록한다.
- 범위 밖 상품은 변환을 억지로 수행하지 않고 `out_of_scope: true`로 표시한다.
- 소재 혼용률이 명시되지 않으면 `ratio`를 추정하지 않는다. `ratio_status`로 `missing` 또는 `ambiguous`를 표시하고, 필요한 경우 `quality.missing_fields` 또는 `quality.ambiguous_fields`에 `material_ratio`를 기록한다.

## 시간대·단위·반올림 기준
- 확인일과 기록일은 KST 기준 `YYYY-MM-DD`로 쓴다.
- 비율은 0~100%로 기록하되, JSON 내부 score는 0.0~1.0 범위로 둔다.
- 정량 지표는 소수점 셋째 자리에서 반올림해 둘째 자리까지 보고한다.

## 제출 구조 기준 (과제 규정 — 고정)
- `submission.zip` 루트: `src/`, `README.md`, `logs/`
- `src/.codex-plugin/plugin.json` 필수
- `src/skills/product-agentizer/SKILL.md` 필수
- `plugin.json` 외에 실제 동작 구성요소 1개 이상 필요: `SKILL.md`, 정적 reference, 검증 스크립트
- `logs/`는 AI와 주고받은 대화 로그 원본을 편집·발췌 없이 그대로 포함
- 질문 5문항: 무엇을·누가·어떤 상황에서 쓰는가 / 왜 이 문제를 선택했는가 / 플러그인은 어떻게 작동하는가 / AI를 어떻게 활용했는가 / 어떻게 검증했는가

## 완료 기준
- `Decisionlog.md`에 무신사 문제 2 확정 기록 존재
- `src/.codex-plugin/plugin.json`, `src/skills/product-agentizer/SKILL.md`, `schema.json`, `taxonomy.json`, `validate.py`, `dedup.py` 존재
- 더미 픽스처 기반 속성 추출·중복 감지 검증 결과 기록
- 로컬 Codex CLI에서 플러그인 설치·실행 흐름 확인
- README와 질문 5문항 답변이 실제 구현·로그와 모순 없음
- 근거로 사용한 모든 공개 자료가 출처(URL/제목/확인일)와 함께 기록됨
- `submission.zip`에 `src/`, `README.md`, `logs/`가 포함되고, 비밀정보·자동 크롤러가 없음
