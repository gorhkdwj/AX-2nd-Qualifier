# S7.8 size_info 표기 패턴 보강 검증 보고서

## 요약

- 목적: 실제 상품 원문을 저장하지 않고, 실제 페이지에서 나올 법한 size_info 표기 유형을 합성 fixture로 확장해 검증한다.
- 생성 일시(UTC): `2026-07-06T14:05:41.091606+00:00`
- 기준 KST 날짜: `2026-07-06`
- 전체 통과: `True`
- actual mode: `codex_cli_actual`
- actual 생성 일시(UTC): `2026-07-06T01:45:03.275073+00:00`

## 주요 지표

| 지표 | 결과 |
|---|---:|
| expected schema-valid | True |
| actual schema-valid | True |
| actual checked | 48 |
| size_info precision | 100.00% |
| size_info recall | 100.00% |
| size_info true/false positive/false negative | 97 / 0 / 0 |
| recommendation_noise false positive cases | 0 |
| 자동 fetch | 0 |
| 실제 상품 원문 저장 | 0 |
| 법적 적합/부적합 판정 | 0 |

## 패턴 그룹별 결과

| 그룹 | Precision | Recall | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| brand_numeric | 100.00% | 100.00% | 11 | 0 | 0 |
| comparison_guide | 100.00% | 100.00% | 4 | 0 | 0 |
| free_one_size | 100.00% | 100.00% | 5 | 0 | 0 |
| letter_comma | 100.00% | 100.00% | 12 | 0 | 0 |
| letter_slash | 100.00% | 100.00% | 14 | 0 | 0 |
| measurement_rows | 100.00% | 100.00% | 8 | 0 | 0 |
| measurement_table | 100.00% | 100.00% | 7 | 0 | 0 |
| mixed_parentheses | 100.00% | 100.00% | 10 | 0 | 0 |
| model_wear | 100.00% | 100.00% | 4 | 0 | 0 |
| numeric_space | 100.00% | 100.00% | 12 | 0 | 0 |
| recommendation_noise | not_applicable | not_applicable | 0 | 0 | 0 |
| women_numeric | 100.00% | 100.00% | 10 | 0 | 0 |

## 해석

- 이 검증은 실제 판매 데이터 전체 성능이 아니라, size_info 표기 패턴을 넓힌 합성 fixture 기준 검증이다.
- source 입력에는 expected label이나 pattern_group을 넣지 않고, pattern_group은 `case_metadata.json`에만 보존했다.
- actual은 expected fixture가 없는 격리 workspace에서 실제 Codex CLI로 생성한다.
- `recommendation_noise` 그룹은 구매자 만족도, 개인화 추천, 후기 요약처럼 정적 상품 사이즈가 아닌 문구가 size_info로 들어가지 않는지 확인한다.

## 실패 사례

- 없음

## 실행 명령

- `expected_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/size_info_patterns/expected_products.json` -> exit `0`
- `actual_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/size_info_patterns/actual_products.json` -> exit `0`

## 재현 방법

```powershell
python tools\generate_size_info_pattern_fixtures.py
python tools\run_full_page_codex_smoke20_cli.py --fixture size_info_patterns --timeout 3600
python tools\run_size_info_pattern_validation.py
```
