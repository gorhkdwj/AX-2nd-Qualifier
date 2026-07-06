# S7.8 size_info 표기 패턴 보강 검증 계획

## 1. 목적

S7.7의 `full_page_codex_subset` 50건은 실제 상품 페이지 원문을 저장하지 않고, 실제 페이지형 합성 상세페이지 입력으로 검증한 세트다. SKILL-only 보강 후 이 세트에서 `size_info` precision/recall 100.00%를 달성했다.

다만 이 결과는 실제 판매 데이터 전체 기준이 아니라, 합성 상세페이지형 50건 기준이다. 실제 상품 페이지에서는 사이즈 옵션, 실측표, 모델 착용, 추천·후기, 비교 가이드 등 더 다양한 표기 방식이 등장할 수 있다.

S7.8의 목적은 다음이다.

> 실제 상품 페이지 원문을 저장하지 않고, 공개 자료와 관찰 가능한 페이지 구조를 참고해 `size_info` 표기 패턴을 확장한 합성 fixture를 만들고, SKILL이 다양한 size 표기에서 오탐·누락을 줄이는지 검증한다.

## 2. 근거와 전제

공개 무신사 뉴스룸 자료에서는 다음 유형의 size 관련 정보가 확인된다.

- 상품 상세 페이지에서 인터내셔널 사이즈 표와 실측 서비스가 제공될 수 있다.
- 실측 필터에는 총장, 어깨너비, 가슴 단면, 소매 길이 같은 숫자형 치수 필드가 사용된다.
- 사이즈 추천이나 구매자 사이즈 만족도 같은 데이터 기반 정보도 상품 상세 경험에 포함될 수 있다.

이 문서는 실제 상품 페이지 전체 원문을 저장하지 않는다. 대신 위 유형을 합성 문장으로 모사한다.

## 3. 검증 데이터셋

경로는 다음과 같다.

```text
tests/fixtures/size_info_patterns/
  source_inputs.json
  expected_products.json
  actual_products.json
  actual_metadata.json
  duplicate_labels.json
  case_metadata.json
  prompt.md
  prompt_template.md

docs/reports/s7-8-size-info-coverage-report.md
docs/reports/s7-8-size-info-coverage-results.json
```

## 4. 패턴 그룹

기본 fixture는 48건으로 구성한다. 각 그룹은 4건씩 만들고, `outer`와 `top`을 섞는다.

| 그룹 | 예시 | 기대 동작 |
|---|---|---|
| `letter_comma` | `사이즈 옵션: S, M, L` | `S`, `M`, `L` 개별 추출 |
| `letter_slash` | `SIZE: XS / S / M / L / XL` | 슬래시 구분 옵션 개별 추출 |
| `numeric_space` | `사이즈: 90 95 100 105` | 숫자 옵션 개별 추출 |
| `women_numeric` | `사이즈 옵션: 44, 55, 66` | 여성 숫자형 옵션 개별 추출 |
| `brand_numeric` | `사이즈: 1 / 2 / 3` | 브랜드 자체 숫자 옵션 개별 추출 |
| `mixed_parentheses` | `M(95), L(100), XL(105)` | 결합 표기 보존 |
| `free_one_size` | `FREE`, `ONE SIZE`, `OS` | 단일 옵션 보존 |
| `measurement_rows` | `M 총장 68cm 어깨 50cm...` | 행 단위 보존 |
| `measurement_table` | `사이즈(cm) 총장 어깨 가슴 소매 / M 68...` | header와 값을 결합해 행 단위 보존 |
| `model_wear` | `모델 181cm/70kg L 착용` | 모델 착용 문구 보존 |
| `comparison_guide` | `무신사 스탠다드 M 사이즈와 비슷` | 비교 가이드 문구 보존 |
| `recommendation_noise` | `사이즈 만족도 적당함 82%` | 정적 상품 size_info로 넣지 않음 |

## 5. 평가 지표

주요 지표는 `size_info`에 집중한다.

- expected/actual schema-valid 100%
- 전체 `size_info` precision 95% 이상
- 전체 `size_info` recall 95% 이상
- 패턴 그룹별 precision/recall 기록
- `recommendation_noise` 그룹의 false positive 0건
- 자동 fetch 0건
- 실제 상품 원문 저장 0건
- 법적 적합/부적합 판정 0건

## 6. 해석 기준

이 검증을 통과해도 "실제 판매 데이터 기준 size_info 100%"라고 말하지 않는다. 올바른 표현은 다음이다.

> S7.8 size_info 표기 패턴 합성 fixture에서 실제 Codex CLI actual 기준 size_info precision/recall을 검증했다.

실제 판매 데이터 기준 성능을 주장하려면, 별도 허가된 실제 데이터셋 또는 합법적·재현 가능한 공개 데이터 수집 기준이 필요하다.

## 7. 완료 조건

- 계획 문서, fixture, prompt, actual, metadata, 평가 결과, 보고서가 모두 보존된다.
- 실제 URL이나 실제 상품 원문을 저장하지 않는다.
- Codex actual은 expected fixture가 없는 격리 workspace에서 생성한다.
- 결과가 목표치를 통과하거나, 실패 시 원인과 후속 보완 방향을 보고서에 남긴다.

## 8. 현재 결과

2026-07-06 기준 S7.8 검증을 실행했다.

- fixture: `tests/fixtures/size_info_patterns/` 48건
- actual mode: `codex_cli_actual`
- 실행 방식: expected fixture가 없는 격리 workspace
- schema-valid: 48/48
- `size_info` precision: 100.00%
- `size_info` recall: 100.00%
- `size_info` true/false positive/false negative: 97 / 0 / 0
- `recommendation_noise` false positive cases: 0
- 자동 fetch: 0건
- 실제 상품 원문 저장: 0건
- 법적 적합/부적합 판정: 0건

상세 결과는 `docs/reports/s7-8-size-info-coverage-report.md`와 `docs/reports/s7-8-size-info-coverage-results.json`에 보존한다.

이 결과도 실제 판매 데이터 전체 기준 성능이 아니라, 실제 페이지에서 나올 법한 표기 방식을 모사한 확장 합성 fixture 기준 성능으로 해석한다.
