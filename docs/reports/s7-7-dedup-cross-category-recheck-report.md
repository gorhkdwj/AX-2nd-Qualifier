# S7.7 dedup cross-category 독립 재계산 보고서

## 요약

- 목적: S7.7 결과 JSON에 저장된 `dedup_cross_category_check` 값을 그대로 신뢰하지 않고, `full_page_dummy/reference_actual_products.json`의 모든 상품쌍을 처음부터 다시 점수화해 cross-category high-confidence false duplicate 0건을 독립 재현한다.
- 생성 일시(UTC): `2026-07-06T14:05:40.851722+00:00`
- 기준 KST 날짜: `2026-07-06`
- 전체 통과: `True`

## 입력과 기준

- 입력 상품 JSON: `tests/fixtures/full_page_dummy/reference_actual_products.json`
- 비교 대상 저장 결과: `docs/reports/s7-7-full-page-dummy-validation-results.json`
- 점수 함수: `src/skills/product-agentizer/scripts/dedup.py`
- 후보 포함 최소 점수: `0.45`
- high-confidence duplicate 임계값: `0.78`
- 재실행 명령: `python tools/run_s7_7_dedup_cross_category_recheck.py`

## 재계산 결과

| 항목 | 값 |
|---|---:|
| 상품 수 | 300 |
| category 분포 | `{"outer": 150, "top": 150}` |
| 전체 상품쌍 | 44850 |
| cross-category 상품쌍 | 22500 |
| score >= 0.45 후보 수 | 2788 |
| score >= 0.45 cross-category 후보 수 | 0 |
| score >= 0.78 high-confidence 후보 수 | 23 |
| high-confidence cross-category false duplicate | 0 |

## 저장 결과 대조

| 항목 | 저장값 | 재계산값 | 일치 |
|---|---:|---:|---:|
| candidate_count | 2788 | 2788 | True |
| high_confidence_cross_category_count | 0 | 0 | True |

## 상위 cross-category 점수

high-confidence 임계값 0.78 이상인 cross-category 쌍은 없었다. 아래는 참고용으로 score가 가장 높은 cross-category 쌍 5개다.

| left_id | right_id | score | decision | matched_fields |
|---|---|---:|---|---|
| `full_outer_146` | `full_top_216` | 0.4150 | `distinct` | materials, colors, seasons, tpo_tags, care |
| `full_outer_017` | `full_top_297` | 0.4147 | `distinct` | materials, seasons, tpo_tags, care |
| `full_outer_058` | `full_top_198` | 0.4076 | `distinct` | materials, seasons, tpo_tags, care |
| `full_outer_057` | `full_top_297` | 0.3850 | `distinct` | materials, seasons, tpo_tags |
| `full_outer_127` | `full_top_297` | 0.3700 | `distinct` | materials, seasons, tpo_tags |

## 해석

- 전체 300개 상품에서 가능한 모든 상품쌍 44,850개를 재계산했고, 그중 outer/top이 다른 cross-category 쌍은 22,500개였다.
- score 0.45 이상으로 후보 목록에 들어온 쌍은 2,788개로 저장된 S7.7 결과와 일치했다.
- score 0.78 이상 high-confidence duplicate 후보는 23개였고, 모두 같은 category 안의 쌍이었다.
- cross-category 쌍 중 score 0.45 이상 후보는 0개였고, high-confidence false duplicate도 0개였다.
- 따라서 S9 보고서의 미검증 범위였던 S7.7 dedup cross-category 재계산 독립 검증은 해소됐다.
