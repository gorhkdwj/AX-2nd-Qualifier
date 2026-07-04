# S5 더미 픽스처 검증 결과

확인일: 2026-07-04 KST

## 목적
S5의 목적은 실제 공개 상품페이지에 정답 라벨이 없다는 한계를 피하기 위해, 정답을 아는 합성 상품 텍스트와 구조화 JSON을 사용해 평가 루프가 작동하는지 확인하는 것이다. 이 결과는 실제 Codex 실행 성능 수치가 아니라, 더미 fixture 기준의 검증 harness 결과다.

## 검증 데이터
- 입력 원문: `tests/fixtures/evaluation/source_inputs.json`
- 정답 구조화 JSON: `tests/fixtures/evaluation/expected_products.json`
- 예측 구조화 JSON: `tests/fixtures/evaluation/predicted_products.json`
- 중복 라벨: `tests/fixtures/evaluation/duplicate_labels.json`

데이터는 모두 합성 상품이며, URL은 실행 입력이 아니라 출처 메타데이터 형식 확인용 `example.com` 주소다.

## 실행 명령
```powershell
python -m py_compile tests\evaluate_product_agentizer.py
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\evaluation\expected_products.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\evaluation\predicted_products.json --pretty
python tests\evaluate_product_agentizer.py --pretty
```

## 결과 요약
| 항목 | 결과 |
|---|---:|
| 입력 케이스 | 5 |
| 정답 JSON schema 검증 | 통과, 5건 |
| 예측 JSON schema 검증 | 통과, 5건 |
| 속성 micro precision | 98.55% |
| 속성 micro recall | 88.31% |
| 중복 감지 정확도 | 100.00% (10/10) |
| dedup 후보 수 | 1 |

## 속성별 결과
| 필드 | Precision | Recall | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| title | 100.00% | 100.00% | 5 | 0 | 0 |
| category | 100.00% | 100.00% | 5 | 0 | 0 |
| subcategory | 100.00% | 100.00% | 5 | 0 | 0 |
| materials | 100.00% | 80.00% | 8 | 0 | 2 |
| fit | 100.00% | 100.00% | 5 | 0 | 0 |
| colors | 80.00% | 80.00% | 4 | 1 | 1 |
| seasons | 100.00% | 88.89% | 8 | 0 | 1 |
| tpo_tags | 100.00% | 78.57% | 11 | 0 | 3 |
| care | 100.00% | 100.00% | 5 | 0 | 0 |
| size_info | 100.00% | 83.33% | 10 | 0 | 2 |
| quality.missing_fields | 100.00% | 100.00% | 1 | 0 | 0 |
| quality.ambiguous_fields | 100.00% | 100.00% | 1 | 0 | 0 |

## 확인된 차이
- `outer_down_vest`: `goose_down` 충전재, `travel` 태그, `암홀 여유` 사이즈 정보가 누락됐고, 색상이 `khaki` 대신 `green`으로 예측됐다.
- `top_linen_blouse`: `rayon` 소재, `spring` 계절, `formal` 태그, `가슴둘레 여유` 사이즈 정보가 누락됐다.
- `top_washable_tee`: `layering` 태그가 누락됐다.

## 중복 감지 결과
- `outer_linen_blazer_a`와 `outer_linen_blazer_b`는 score `1.0`, decision `duplicate`로 탐지됐다.
- 나머지 9개 라벨 쌍은 모두 `distinct`로 판정되어 정답과 일치했다.

## 해석
- S5 산출물은 `validate.py`와 `dedup.py`가 더미 fixture 기반 정량 검증에 연결되는지 확인했다.
- 의도적으로 누락·오분류가 포함된 예측 JSON에서도 평가 스크립트가 false positive와 false negative를 분리해 보고했다.
- 다음 S6에서는 실제 Codex CLI에서 skill을 실행해 만든 출력 JSON을 `predicted_products.json` 같은 형식으로 저장하거나 표준입력으로 평가해, 더미 harness와 실제 실행 흐름을 연결한다.
