# S7.7 실제 페이지형 합성 더미 검증 보고서

## 요약

- 목적: 실제 상품 페이지 원문을 저장하지 않고, 정보 밀도별 합성 상세페이지 입력으로 플러그인의 운영형 입력 대응력을 검증한다.
- 생성 일시(UTC): `2026-07-05T20:44:53.479185+00:00`
- 기준 KST 날짜: `2026-07-06`
- 전체 명령 통과: `True`
- Codex subset actual 모드: `deterministic_reference_actual_pending_cli_run`
- Codex smoke20 actual 모드: `codex_cli_actual`

## 데이터셋

- `full_page_dummy`: 300건
- `full_page_codex_subset`: 50건, representative reference actual 보존 세트
- `full_page_codex_smoke20`: 20건, 실제 Codex CLI smoke 실행 세트
- 정보 밀도 분포: `{'sparse': 60, 'medium': 120, 'full': 90, 'noisy_ambiguous': 30}`
- 카테고리 분포: `{'outer': 150, 'top': 150}`
- detail_type 최소 커버리지: `{'outer': 6, 'top': 14}`

## 주요 지표

| 지표 | 결과 |
|---|---:|
| expected schema-valid | True |
| reference actual schema-valid | True |
| self-check micro precision | 1.0 |
| self-check micro recall | 1.0 |
| self-check detail_type precision | 1.0 |
| self-check detail_type recall | 1.0 |
| self-check dedup accuracy | 1.0 |
| Codex subset actual schema-valid | True |
| Codex subset micro precision | 1.0 |
| Codex subset micro recall | 1.0 |
| Codex smoke20 actual schema-valid | True |
| Codex smoke20 micro precision | 1.0 |
| Codex smoke20 micro recall | 1.0 |
| Codex smoke20 detail_type precision | 1.0 |
| Codex smoke20 detail_type recall | 1.0 |
| Codex smoke20 dedup accuracy | 1.0 |
| 자동 fetch | 0 |
| 실제 상품 원문 저장 | 0 |
| 법적 적합/부적합 판정 | 0 |
| cross-category high-confidence false duplicate | 0 |

## 해석

- `full_page_dummy`의 `reference_actual_products.json`은 expected와 동일한 결정적 기준 출력이다. 따라서 이 self-check는 생성된 fixture, schema, evaluator, dedup label의 정합성을 확인하는 검증이며 blind extraction 성능으로 해석하지 않는다.
- `full_page_codex_subset/actual_products.json`도 이번 단계에서는 실제 Codex CLI 실행 결과가 아니라 deterministic reference actual이다. 실제 Codex subset 실행은 다음 단계에서 같은 prompt를 사용해 덮어쓰고 본 보고서를 갱신해야 한다.
- `full_page_codex_smoke20/actual_products.json`은 20건 실제 Codex CLI smoke 실행 결과를 저장하는 경로다. actual mode가 `codex_cli_actual`이면 실제 실행 결과이고, `deterministic_reference_actual_pending_cli_run`이면 아직 기준 actual 상태다.
- Sparse 입력은 세부 필드를 모두 맞히는 것이 목표가 아니라, 입력에 없는 소재 혼용률·관리법·사이즈 정보를 추정하지 않는지를 확인하기 위한 케이스다.

## Smoke20 보완 전후

- 첫 격리 workspace smoke20 실행은 schema-valid 20/20이었지만 micro precision 0.8629, micro recall 0.9149였다.
- 원인은 주로 fixture 라벨 기준 문제였다. `사이즈 옵션: M, L, XL`을 expected가 하나의 문자열로 보존했지만 Codex는 개별 사이즈로 분리했고, 입력 텍스트에 없는 `layering`, `daily`, `casual` TPO가 expected에 들어간 케이스가 있었다. 또한 소재 부위가 명시되지 않은 표현을 expected가 `shell`로 둔 케이스가 있었다.
- 보완은 expected 완화가 아니라 입력 근거 기준 정합성 수정으로 처리했다. 사이즈 옵션은 개별 값으로 비교하고, TPO는 텍스트에 있는 상황 단서만 라벨링하며, 부위 미상 소재는 `part: unknown`과 `quality.missing_fields: material_part`로 기록한다.
- 보완 후 smoke20 micro precision은 1.0, micro recall은 1.0이다.

## 실행 명령

- `full_page_expected_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/full_page_dummy/expected_products.json` -> exit `0`
- `full_page_reference_actual_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/full_page_dummy/reference_actual_products.json` -> exit `0`
- `full_page_selfcheck_eval`: `C:\Users\gorhk\MiniConda3\python.exe tests/evaluate_product_agentizer.py --inputs tests/fixtures/full_page_dummy/source_inputs.json --expected tests/fixtures/full_page_dummy/expected_products.json --actual tests/fixtures/full_page_dummy/reference_actual_products.json --dedup-labels tests/fixtures/full_page_dummy/duplicate_labels.json` -> exit `0`
- `full_page_codex_subset_actual_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/full_page_codex_subset/actual_products.json` -> exit `0`
- `full_page_codex_subset_eval`: `C:\Users\gorhk\MiniConda3\python.exe tests/evaluate_product_agentizer.py --inputs tests/fixtures/full_page_codex_subset/source_inputs.json --expected tests/fixtures/full_page_codex_subset/expected_products.json --actual tests/fixtures/full_page_codex_subset/actual_products.json --dedup-labels tests/fixtures/full_page_codex_subset/duplicate_labels.json` -> exit `0`
- `full_page_codex_smoke20_actual_schema`: `C:\Users\gorhk\MiniConda3\python.exe src/skills/product-agentizer/scripts/validate.py tests/fixtures/full_page_codex_smoke20/actual_products.json` -> exit `0`
- `full_page_codex_smoke20_eval`: `C:\Users\gorhk\MiniConda3\python.exe tests/evaluate_product_agentizer.py --inputs tests/fixtures/full_page_codex_smoke20/source_inputs.json --expected tests/fixtures/full_page_codex_smoke20/expected_products.json --actual tests/fixtures/full_page_codex_smoke20/actual_products.json --dedup-labels tests/fixtures/full_page_codex_smoke20/duplicate_labels.json` -> exit `0`

## 재현 방법

```powershell
python tools\generate_full_page_dummy_fixtures.py
python tools\run_full_page_codex_smoke20_cli.py
python tools\run_full_page_dummy_validation.py
```

## 미완료 항목

- 20건 smoke 결과가 안정적이면 실제 Codex CLI로 `tests/fixtures/full_page_codex_subset/prompt.md` 50건 실행을 진행한다.
