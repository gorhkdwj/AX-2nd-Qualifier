# size_info schema 변경 조건부 계획

## 1. 문서 상태

- 상태: 조건부 계획
- 현재 활성 schema: `schema_version: "0.2.0"`
- 현재 결정: 당장은 schema를 변경하지 않고 `SKILL.md` 지침 보강으로 `size_info` 품질을 먼저 개선한다.
- 활용 시점: SKILL-only 개선으로도 size option, 실측표, 모델 착용 정보의 구분이 안정적으로 되지 않거나, 에이전트 질의가 typed size field를 요구할 때 재검토한다.
- 비활성화 기준: SKILL-only 개선 후 `size_info` precision/recall이 운영 목표를 충분히 만족하고, typed size query가 MVP 제출 범위에 필요 없다고 판단되면 `docs/archive/`로 이동한다.

## 1.1 현재 검토 결과

2026-07-06 기준으로 SKILL-only `size_info` 원자화 지침을 보강한 뒤 `full_page_codex_subset` 50건을 같은 격리 workspace 방식으로 재실행했다.

| 지표 | 개선 전 | 개선 후 |
|---|---:|---:|
| subset micro precision | 96.15% | 100.00% |
| subset micro recall | 88.47% | 100.00% |
| size_info precision | 59.65% | 100.00% |
| size_info recall | 33.01% | 100.00% |

따라서 현재 MVP 제출 범위에서는 schema v0.3 변경을 보류한다. 이후 소재 부위 보수 라벨 기준까지 정렬하면서 S7.7 50건 subset의 전체 micro precision/recall도 100.00%가 되었지만, 이 문서는 typed size query나 category 확장 시 재검토할 조건부 설계안으로 유지한다.

## 2. 변경을 검토하게 된 문제

현재 `schema.json`의 `product.size_info`는 단순 문자열 배열이다.

```json
{
  "size_info": ["M", "L", "XL"]
}
```

이 구조는 구현과 검증이 단순하다는 장점이 있지만, 다음 정보를 schema 차원에서 구분하지 못한다.

- 판매 옵션: `S`, `M`, `L`, `XL`, `FREE`
- 숫자형 옵션: `90`, `95`, `100`
- 실측표 행: `M 총장 68cm 어깨 52cm 가슴 60cm`
- 모델 착용 정보: `모델 178cm L 착용`
- 기타 사이즈 설명: `정사이즈 추천`, `여유 있는 착용감`
- 노이즈: `후기 요약: 사이즈가 여유 있어요`

S7.7 50건 실제 Codex subset 검증에서 전체 micro precision/recall과 `detail_type`은 수용 기준을 통과했지만, `size_info`는 낮게 남았다. 주요 원인은 `사이즈 옵션: M, L, XL`을 하나의 문자열로 보존한 출력과, expected의 개별 option 라벨(`M`, `L`, `XL`)이 충돌한 것이다.

## 3. 변경하지 않는 경우의 한계

`schema_version 0.2.0`을 유지하면 다음 한계가 남는다.

- schema-valid가 좋은 size 출력 형태를 강제하지 못한다.
- Codex가 `사이즈 옵션: M, L, XL`을 하나의 문자열로 넣어도 schema상 오류가 아니다.
- `option`, `measurement_row`, `model_wear`, `note` 같은 의미 구분은 evaluator와 SKILL 지침에 의존한다.
- `M 사이즈 있는 상품`, `가슴 실측 60cm 이상`, `모델 L 착용 상품` 같은 정밀 질의는 후처리 없이 안정적으로 처리하기 어렵다.

## 4. schema v0.3 제안

schema를 변경한다면 `schema_version`을 `0.3.0`으로 올리고, `product.size_info`를 문자열 배열에서 객체 배열로 바꾼다.

```json
{
  "schema_version": "0.3.0",
  "product": {
    "size_info": [
      {
        "type": "option",
        "label": "M",
        "evidence": "사이즈 옵션: M, L, XL"
      },
      {
        "type": "measurement_row",
        "label": "M",
        "text": "M 총장 68cm 어깨 52cm 가슴 60cm 소매 59cm",
        "evidence": "사이즈 실측: M 총장 68cm 어깨 52cm 가슴 60cm 소매 59cm"
      }
    ]
  }
}
```

### 4.1 필드 후보

| 필드 | 타입 | 필수 여부 | 설명 |
|---|---|---:|---|
| `type` | enum | 필수 | `option`, `measurement_row`, `model_wear`, `note`, `ambiguous` |
| `label` | string/null | 조건부 | option label 또는 실측표 행의 size label |
| `text` | string/null | 조건부 | 실측표 행, 모델 착용 문장, 기타 설명 원문 |
| `evidence` | string | 필수 | 입력 텍스트 근거 |

### 4.2 type 정의

| type | 용도 | 예시 |
|---|---|---|
| `option` | 구매 가능한 사이즈 옵션 | `S`, `M`, `L`, `XL`, `FREE`, `90`, `95` |
| `measurement_row` | 실측표의 한 행 | `M 총장 68cm 어깨 52cm 가슴 60cm` |
| `model_wear` | 모델 착용 정보 | `모델 178cm L 착용` |
| `note` | 기타 사이즈 안내 | `정사이즈 추천`, `여유 있는 착용감` |
| `ambiguous` | 사이즈 관련이지만 구조화가 애매한 정보 | `상세 이미지 참고` |

## 5. 작업 범위

schema 변경 시 다음 파일·영역이 영향을 받는다.

- `src/skills/product-agentizer/references/schema.json`
- `src/skills/product-agentizer/SKILL.md`
- `src/skills/product-agentizer/scripts/validate.py`
- `tests/evaluate_product_agentizer.py`
- `tools/generate_full_page_dummy_fixtures.py`
- `tools/run_expanded_validation.py`
- `tools/run_full_page_dummy_validation.py`
- `tests/fixtures/**/expected_products.json`
- `tests/fixtures/**/actual_products.json`
- `tests/fixtures/**/reference_actual_products.json`
- `docs/requirements-contract.md`
- `docs/validation-plan.md`
- `docs/reports/*.md`
- 루트 `README.md`
- `docs/product-agentizer-complete-guide.md`

## 6. 예상 작업량

| 작업 | 예상 소요 |
|---|---:|
| 계약 문서와 Decisionlog 갱신 | 30분 |
| schema v0.3 설계·구현 | 40~60분 |
| validator 조건부 검증 보강 | 30~45분 |
| SKILL 출력 지침 수정 | 20~30분 |
| fixture 전체 마이그레이션 | 1~1.5시간 |
| evaluator 비교 로직 수정 | 1시간 |
| Codex smoke/subset 재실행 | 40~60분 |
| 보고서·README·상세 설명서 갱신 | 40~60분 |

총 예상 소요는 약 4~6시간이다. fixture 마이그레이션이나 evaluator에서 예외가 발생하면 더 늘어날 수 있다.

## 7. 기대 효과

- schema가 size option 원자화를 강제할 수 있다.
- 판매 옵션, 실측표, 모델 착용 정보, 기타 노트를 구분할 수 있다.
- `size_info` precision/recall이 단순 문자열 비교보다 안정적으로 해석된다.
- 에이전트가 `M 사이즈`, `FREE 사이즈`, `가슴 실측`, `모델 착용 사이즈` 같은 질의를 더 잘 처리할 수 있다.
- 장기적으로 bottom, shoes 등 size 체계가 더 중요한 카테고리로 확장할 때 기반이 된다.

## 8. 리스크

- 이미 통과한 S7.7 actual과 보고서를 모두 재생성해야 한다.
- `schema_version` 변경으로 S7.5/S7.7 기존 수치와 직접 비교하기 어려워진다.
- 패키징 직전에는 fixture, evaluator, README, 제출 설명까지 연쇄 변경되어 회귀 위험이 크다.
- 현재 MVP는 outer/top 중심이므로 typed size schema가 제출 가치를 크게 올리는지 불확실하다.

## 9. 전환 조건

다음 중 하나 이상에 해당하면 schema v0.3 변경을 재검토한다.

- SKILL-only 개선 후에도 `size_info` precision 90% 또는 recall 85% 미만이 반복된다.
- 심사·데모 시나리오에서 사이즈 옵션과 실측표를 구분하는 질의가 핵심 가치로 부상한다.
- bottom, shoes, bag 등 size 체계가 더 복잡한 카테고리 확장이 확정된다.
- 실제 운영 데이터에서 size field가 검색·필터 품질에 큰 영향을 준다는 근거가 생긴다.

## 10. 비활성화와 archive 기준

다음 조건을 만족하면 이 문서는 활성 기준에서 제외하고 `docs/archive/`로 이동한다.

- SKILL-only 개선으로 S7.7 subset의 `size_info` 목표치를 만족한다.
- 제출 MVP에서 typed size object가 필수 기능이 아니라고 판단한다.
- schema 변경으로 얻는 이익보다 패키징 전 회귀 리스크가 크다고 판단한다.

archive 처리 시 `docs/archive/README.md`에 이동 사유를 남기고, `docs/README.md`의 활성 문서 목록에서 제거한다.
