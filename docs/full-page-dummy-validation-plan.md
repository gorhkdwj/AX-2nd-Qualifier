# 실제 페이지형 합성 더미데이터 검증 계획

## 1. 목적

이 문서는 S8 패키징 전에 추가할 `S7.7 실제 페이지형 합성 더미 검증`의 설계 계획이다.

기존 S7.5 검증은 다음 세 가지를 확인했다.

- 합성 더미 100건으로 schema, taxonomy, evaluator, dedup 기준선이 일관되는지 확인
- historical Codex subset 20건으로 실제 Codex 출력 보존 결과가 기준 수치를 만족하는지 확인
- 실제 공개 상품에서 확인한 짧은 factual snippet 10건으로 현실성 sanity check 수행

다만 실제 공개 snippet 검증은 전체 상세페이지 원문 기반 벤치마크가 아니라, 저작권과 약관 리스크를 줄이기 위해 짧은 사실 정보만 보존한 탐색적 비교다. 따라서 실제 상품 페이지의 정보 구조와 노이즈를 더 잘 모사하면서도 재현 가능하고 제출 가능한 검증 데이터가 필요하다.

S7.7의 목표는 다음이다.

> 실제 판매 페이지 전체 원문을 복제하거나 로컬 전용 비공개 데이터를 남기지 않고, 실제 상품 페이지의 정보 밀도 차이를 반영한 대규모 합성 상세페이지형 더미데이터로 플러그인의 운영형 입력 대응력을 검증한다.

## 2. 전제와 판단

### 2.1 확인한 현실 전제

소수 공개 상품 페이지를 확인한 결과, 상품별로 공개 페이지에서 관찰되는 정보 밀도는 균일하지 않다.

- 일부 상품은 카테고리, 상품명, 가격, 이미지 중심으로 비교적 간략하게 보인다.
- 일부 상품은 후기, AI 요약, 배송 문구, 다수 이미지, 상세 설명 등 부가 정보가 더 많이 관찰된다.
- 공개 HTML 텍스트로 바로 확인되는 정보와 이미지 또는 동적 영역에 포함된 정보가 다를 수 있다.

따라서 검증 데이터가 모든 상품을 `Full` 정보 상품으로만 가정하면 실제 운영 환경을 과도하게 단순화한다. 실제 운영에서는 정보가 적은 상품도 정상 입력으로 간주해야 하며, 이 경우 없는 정보를 추정하지 않고 `missing_fields` 또는 `ambiguous_fields`로 표시하는 것이 올바른 동작이다.

### 2.2 제외하는 방식

다음 방식은 사용하지 않는다.

- 실제 상품 상세페이지 전체 원문을 저장하거나 커밋
- 실제 상품 이미지, 리뷰 원문, 사용자 생성 콘텐츠 저장
- 자동 크롤링, 자동 fetch, 대량 수집
- 평가자가 재현할 수 없는 로컬 전용 검증 데이터만 남기는 방식
- 실제 상품 정보의 법적 적합/부적합 판정

### 2.3 채택하는 방식

다음 방식을 채택한다.

- 실제 상품 페이지의 구조와 정보 밀도만 참고한다.
- 상품명, 브랜드, 소재, 사이즈, 관리법, 배송, 쿠폰, 후기 요약 같은 페이지 구성 요소는 합성 데이터로 만든다.
- 모든 입력, expected JSON, reference actual JSON, Codex actual JSON, 평가 결과를 커밋 가능한 파일로 보존한다.
- 실제 브랜드명 대신 `DUMMY STANDARD`, `AX TEST LABEL`, `SYNTHETIC WORKS` 같은 합성 브랜드를 사용한다.
- 실제 URL 대신 `https://example.com/musinsa-full-page-dummy/...` 형태의 합성 URL을 사용한다.

## 3. 데이터셋 설계

### 3.1 위치

새 데이터셋은 아래 경로에 둔다.

```text
tests/fixtures/full_page_dummy/
  source_inputs.json
  expected_products.json
  reference_actual_products.json
  duplicate_labels.json
  case_metadata.json

tests/fixtures/full_page_codex_subset/
  source_inputs.json
  prompt_template.md
  prompt.md
  expected_products.json
  actual_products.json
  duplicate_labels.json

docs/reports/s7-7-full-page-dummy-validation-report.md
docs/reports/s7-7-full-page-dummy-validation-results.json
```

### 3.2 규모

기본 규모는 다음으로 시작한다.

| 세트 | 건수 | 목적 |
|---|---:|---|
| `full_page_dummy` | 300건 | 상세페이지형 합성 입력의 schema, evaluator, dedup, coverage self-check |
| `full_page_codex_subset` | 50건 | 실제 Codex 변환 결과를 보존하고 expected와 비교 |

시간이 부족하면 축소 기준을 사용한다.

| 축소 단계 | `full_page_dummy` | `full_page_codex_subset` | 사용 조건 |
|---|---:|---:|---|
| 기본 | 300 | 50 | 권장 |
| 축소 | 150 | 30 | 마감 전 검증 시간이 부족할 때 |
| 최소 | 100 | 20 | S8 패키징 직전 최소 안전선 |

## 4. 정보 밀도 유형

데이터는 실제 운영 환경을 모사하기 위해 정보 밀도별로 나눈다.

| 유형 | 비율 | 예시 | 검증 초점 |
|---|---:|---|---|
| `sparse` | 20% | 상품명, 카테고리, 컬러 정도만 명확 | 없는 정보를 추정하지 않고 missing 처리하는지 |
| `medium` | 40% | 소재 일부, 색상, 사이즈 옵션, 핏 일부 포함 | 일반 상품 입력의 안정적 구조화 |
| `full` | 30% | 소재 부위, 혼용률, 실측표, 관리법, 핏, 시즌 포함 | 상세 입력에서 높은 recall 달성 |
| `noisy_ambiguous` | 10% | 배송, 쿠폰, 후기 요약, 마케팅 문구, 모호한 소재 표현 포함 | 노이즈 제거와 ambiguous 처리 |

### 4.1 Sparse 예시

```text
상품명: 미니멀 브이넥 카디건 레드
브랜드: DUMMY STANDARD
카테고리: 아우터 > 카디건
컬러: 레드
```

기대 동작:

- `category`, `subcategory`, `detail_type`, `colors`는 추출
- `materials`, `care`, `size_info`, `fit`은 추정하지 않음
- 부족한 필드는 `quality.missing_fields`에 기록

### 4.2 Medium 예시

```text
상품명: 오버핏 트러커 재킷 블랙
브랜드: AX TEST LABEL
카테고리: 아우터 > 재킷 > 트러커 재킷
컬러: 블랙, 라이트 블루
소재: 면 100%
사이즈: M, L, XL
핏: 여유 있는 오버핏
추천 계절: 봄, 가을
```

기대 동작:

- 명시된 소재와 색상, 핏, 계절, 사이즈 옵션을 추출
- 소재 부위가 없으면 `part: "unknown"` 또는 기준에 맞는 missing/ambiguous 처리

### 4.3 Full 예시

```text
상품명: 릴렉스드 나일론 코치 재킷 네이비
브랜드: SYNTHETIC WORKS
카테고리: 아우터 > 재킷 > 나일론/코치 재킷

컬러 옵션:
- 네이비
- 블랙

소재 정보:
- 겉감: 나일론 100%
- 안감: 폴리에스터 100%

사이즈 실측:
M 총장 68cm 어깨 52cm 가슴 60cm 소매 59cm
L 총장 70cm 어깨 54cm 가슴 62cm 소매 60cm

핏: 릴렉스드 핏
추천 계절: 봄, 가을
추천 상황: 데일리, 출근, 레이어링
관리 방법: 단독 손세탁 권장, 건조기 사용 금지
```

기대 동작:

- `materials.part`, `ratio`, `ratio_status`, `size_info`, `care`를 모두 높은 recall로 추출
- 배송, 쿠폰 등 구조화 대상이 아닌 문구가 없는 경우 quality noise가 낮아야 함

### 4.4 Noisy/Ambiguous 예시

```text
상품명: 캐시미어 블렌디드 블루종 자켓 블랙
브랜드: AX TEST LABEL
카테고리: 아우터 > 재킷 > 블루종/MA-1
컬러: 블랙
상품 설명: 캐시미어를 블렌드한 듯한 부드러운 터치감의 겨울 블루종입니다.
소재: 고급 울 터치 원단 사용. 정확한 혼용률은 상품 상세 이미지 참고.
배송 안내: 오늘 22시까지 결제 시 내일 도착 예정
쿠폰 안내: 첫 구매 20% 쿠폰
후기 요약: 따뜻해요, 사이즈가 여유 있어요
```

기대 동작:

- `cashmere`, `wool` 비율을 추정하지 않음
- `material_ratio` 또는 `materials` 모호성을 `quality.ambiguous_fields`에 기록
- 배송, 쿠폰, 후기 요약이 소재나 사이즈 정보로 잘못 섞이지 않음

## 5. 카테고리와 detail_type coverage

MVP 범위는 계속 `outer`와 `top`으로 유지한다.

| category | 목표 |
|---|---|
| `outer` | 전체의 50% |
| `top` | 전체의 50% |

`detail_type`은 taxonomy의 모든 상의/아우터 detail type을 최소 3회 이상 포함한다. 기본 300건 기준으로는 각 detail type이 밀도 유형을 달리해 반복 등장하도록 한다.

예시:

- `stadium_jacket`: sparse, medium, full 각각 1건 이상
- `short_sleeve_tshirt`: sparse, medium, noisy_ambiguous 각각 1건 이상
- `other_outer`, `other_top`: 의도적으로 분류가 어려운 입력에만 사용

## 6. 평가 지표

### 6.1 공통 acceptance criteria

| 지표 | 목표 |
|---|---:|
| expected schema-valid | 100% |
| reference actual schema-valid | 100% |
| Codex subset actual schema-valid | 100% |
| `category` precision/recall | 98% 이상 |
| `subcategory` precision/recall | 95% 이상 |
| `detail_type` precision/recall | 95% 이상 |
| dedup accuracy | 95% 이상 |
| cross-category high-confidence false duplicate | 0건 |
| 자동 fetch | 0건 |
| 실제 상품 원문 저장 | 0건 |
| 법적 적합/부적합 판정 | 0건 |

### 6.2 밀도별 지표 해석

Sparse 입력에서는 모든 세부 필드의 recall을 높이는 것이 목표가 아니다. 입력에 없는 정보는 추정하지 않아야 하므로, Sparse의 핵심 지표는 다음이다.

- 명시된 필드 recall
- hallucinated ratio 0건
- hallucinated care 0건
- missing_fields 정확도
- ambiguous_fields 정확도

Full 입력에서는 정보가 충분히 제공되므로 세부 필드 recall을 높게 요구한다.

- `materials.part` 95% 이상
- `material ratio_status` 95% 이상
- `size_info` 90% 이상
- `fit` 90% 이상
- `care` 90% 이상

Noisy/Ambiguous 입력에서는 노이즈 차단과 모호성 표시가 핵심이다.

- 쿠폰, 배송, 후기 요약이 구조화 속성으로 잘못 들어가는 false positive 최소화
- 비율 없는 소재 표현을 `explicit` ratio로 추정하지 않음
- `린넨 라이크`, `캐시미어 블렌디드`, `울 터치` 같은 표현을 실제 소재 확정으로 과도 해석하지 않음

## 7. 생성기 설계

새 생성기는 다음 경로에 추가한다.

```text
tools/generate_full_page_dummy_fixtures.py
tools/run_full_page_dummy_validation.py
```

### 7.1 입력 생성 규칙

입력은 실제 페이지처럼 여러 섹션을 가진 pasted text로 구성한다.

- header: 브랜드, 상품명, 카테고리
- option section: 컬러, 사이즈 옵션
- material section: 소재표 또는 줄글 소재 설명
- size section: 실측표 또는 단순 옵션
- care section: 세탁/관리
- style section: 핏, 계절, TPO
- noise section: 배송, 쿠폰, 이벤트, 후기 요약

### 7.2 expected 생성 규칙

expected JSON은 입력에 실제로 존재하는 사실만 반영한다.

- 명시된 수치 혼용률만 `ratio_status: "explicit"`
- 소재명은 있으나 비율이 없으면 `ratio: null`
- 부위가 없으면 `part: "unknown"` 또는 `quality.missing_fields` 기준으로 처리
- 실제 법적 라벨 적합성은 판단하지 않음
- 상세페이지 노이즈는 `agent_descriptor` 설명에는 참고할 수 있으나 상품 속성으로 섞지 않음

### 7.3 case_metadata

`case_metadata.json`은 평가 해석을 돕기 위한 보조 메타데이터다. 플러그인 입력에는 제공하지 않는다.

예시:

```json
{
  "product_id": "fp_outer_0001",
  "density": "sparse",
  "category": "outer",
  "subcategory": "cardigan",
  "detail_type": "cardigan",
  "present_fields": ["title", "category", "subcategory", "detail_type", "colors"],
  "intentionally_missing_fields": ["materials", "fit", "care", "size_info"],
  "noise_types": []
}
```

## 8. 개선 루프

1. `full_page_dummy` 생성
2. expected/reference actual self-check 실행
3. schema, taxonomy, dedup, cross-category false duplicate 검증
4. representative 50건을 `full_page_codex_subset`으로 추출
5. Codex actual을 생성해 보존
6. expected와 actual 비교
7. 실패 원인을 아래로 분류

| 실패 분류 | 조치 |
|---|---|
| taxonomy alias 부족 | `taxonomy.json` alias 보강 |
| SKILL 추출 지침 부족 | `SKILL.md` 체크리스트 보강 |
| evaluator 정규화 부족 | `tests/evaluate_product_agentizer.py` 정규화 보강 |
| expected 라벨링 오류 | fixture 수정, 완화 금지 |
| schema/validator 계약 불일치 | `requirements-contract.md`와 Decisionlog 먼저 갱신 |

8. 같은 명령으로 재실행
9. 보완 전후 수치를 보고서에 모두 기록

## 9. 작업 단계

### S7.7-1 설계 고정

- 이 문서를 기준으로 데이터 규모, 밀도 비율, acceptance criteria 확정
- `docs/implementation-plan.md`, `docs/validation-plan.md`에 S7.7 추가

### S7.7-2 생성기 구현

- `tools/generate_full_page_dummy_fixtures.py` 추가
- `tests/fixtures/full_page_dummy/` 생성
- schema-valid 100% 확인

### S7.7-3 평가기 확장

- 밀도별 결과 요약을 위해 평가 결과에 density group summary 추가 여부 검토
- 기존 evaluator를 재사용하되, 필요 시 `case_metadata.json` 기반 요약 스크립트 추가

### S7.7-4 Codex subset 실행

- representative 50건 prompt 생성
- Codex actual output 저장
- expected/actual 비교

### S7.7-5 보고서 작성

- `docs/reports/s7-7-full-page-dummy-validation-report.md`
- `docs/reports/s7-7-full-page-dummy-validation-results.json`
- 실패 원인, 보완 전후 수치, 미검증 범위 기록

## 10. 예상 작업 소요

| 작업 | 예상 소요 |
|---|---:|
| 설계 문서 확정 | 30분 |
| 생성기 구현 | 1.5~2.5시간 |
| self-check와 schema/dedup 검증 | 30~45분 |
| Codex subset 30~50건 실행 및 actual 정리 | 1~2시간 |
| 실패 분석과 1차 보완 | 1~2시간 |
| 보고서와 로그 기록 | 30~45분 |

기본 300건/50건 기준 총 예상 소요는 5~8시간이다. 최소 100건/20건으로 축소하면 3~4시간 수준으로 줄일 수 있다.

## 11. 리스크와 대응

| 리스크 | 설명 | 대응 |
|---|---|---|
| 합성 데이터가 너무 이상적임 | 실제 sparse 상품을 과소반영할 수 있음 | 밀도 비율을 고정하고 sparse/noisy를 반드시 포함 |
| 합성 데이터가 너무 쉬움 | 키워드가 그대로 정답을 노출할 수 있음 | 줄글, 표, 노이즈, alias, 모호 표현을 섞음 |
| Codex actual 변동성 | 모델 상태에 따라 재실행 결과가 달라질 수 있음 | actual JSON과 prompt를 보존하고 재생성 대신 보존 결과를 검증 |
| 수치 개선을 위한 expected 완화 | 검증 신뢰도 저하 | expected 완화 금지, 오류면 원인 분류 후 문서 기록 |
| 마감 시간 부족 | 300/50 전체 구현이 부담될 수 있음 | 150/30 또는 100/20 축소 기준 사용 |

## 12. 완료 조건

S7.7은 다음 조건을 만족해야 완료로 본다.

- 모든 입력, expected, reference actual, Codex actual, duplicate labels, prompt가 커밋되어 있다.
- 실제 상품 페이지 원문, 이미지, 리뷰 원문은 포함하지 않는다.
- `full_page_dummy` expected/reference actual schema-valid 100%.
- `full_page_codex_subset` actual schema-valid 100%.
- `detail_type` precision/recall 95% 이상.
- Full 밀도 세트에서 `materials.part`, `size_info`, `fit`, `care` 주요 필드가 목표치를 만족한다.
- Sparse 밀도 세트에서 hallucinated ratio/care가 0건이다.
- dedup accuracy 95% 이상, cross-category high-confidence false duplicate 0건.
- 보고서만 보고 동일 검증을 재실행할 수 있다.
- Worklog와 필요 시 Decisionlog/Troubleshootinglog에 기록한다.

## 13. 현재 구현 상태

- `tools/generate_full_page_dummy_fixtures.py`로 `full_page_dummy` 300건과 `full_page_codex_subset` 50건을 생성한다.
- `tools/run_full_page_dummy_validation.py`로 schema, evaluator, dedup, density coverage, synthetic source policy를 검증하고 `docs/reports/s7-7-full-page-dummy-validation-report.md`와 결과 JSON을 저장한다.
- 현재 `full_page_codex_subset/actual_products.json`은 실제 Codex CLI 출력이 아니라 deterministic reference actual이다. 즉 생성된 fixture와 평가 절차의 재현성 검증은 완료됐지만, 실제 Codex CLI 기반 blind extraction 검증은 후속 단계로 남아 있다.
