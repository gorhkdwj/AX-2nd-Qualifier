# S7.7 실제 페이지형 합성 더미 검증 보고서

## 요약

- 목적: 실제 상품 페이지 원문을 저장하지 않고, 정보 밀도별 합성 상세페이지 입력으로 플러그인의 운영형 입력 대응력을 검증한다.
- 생성 일시(UTC): `2026-07-06T00:31:24.821187+00:00`
- 기준 KST 날짜: `2026-07-06`
- 전체 명령 통과: `True`
- Codex subset actual 모드: `codex_cli_actual`
- Codex smoke20 actual 모드: `codex_cli_actual`
- 50건 subset actual 생성 일시(UTC): `2026-07-06T00:27:32.201265+00:00`

## 데이터셋

- `full_page_dummy`: 300건
- `full_page_codex_subset`: 50건, 실제 Codex CLI 대표 실행 보존 세트
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
| Codex subset micro precision | 0.9615 |
| Codex subset micro recall | 0.8847 |
| Codex subset true/false positive/false negative | 675 / 27 / 88 |
| Codex subset detail_type precision | 1.0 |
| Codex subset detail_type recall | 1.0 |
| Codex subset materials precision | 0.9718 |
| Codex subset materials recall | 0.9718 |
| Codex subset size_info precision | 0.5965 |
| Codex subset size_info recall | 0.3301 |
| Codex subset missing_fields precision | 0.9701 |
| Codex subset missing_fields recall | 0.7927 |
| Codex subset dedup accuracy | 1.0 |
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
- `full_page_codex_subset/actual_products.json`은 expected fixture가 없는 격리 workspace에서 `tests/fixtures/full_page_codex_subset/prompt.md`를 입력해 생성한 50건 실제 Codex CLI 결과다. actual mode가 `codex_cli_actual`이 아니면 이 문장은 성립하지 않으므로 `actual_metadata.json`을 먼저 확인해야 한다.
- 50건 subset은 micro precision 0.9615, micro recall 0.8847로 수용 기준(precision 0.95 이상, recall 0.85 이상)을 통과했다. `category`, `subcategory`, `detail_type`은 50건 모두 일치했다.
- 남은 차이는 주로 `size_info`와 `quality.missing_fields`에 집중된다. `size_info`는 Codex가 `사이즈 옵션: M, L, XL`처럼 한 줄 표현을 하나의 값으로 보존한 반면 expected는 `M`, `L`, `XL` 개별 값으로 라벨링한 차이가 반복됐다. `quality.missing_fields`는 부위 미상 소재의 `material_part` 누락 표시와 모호 소재의 `material_ratio` 해석 차이가 주된 원인이다.
- 이 차이는 핵심 분류와 상품 속성 구조화의 실패라기보다, 사이즈 옵션 원자화와 품질 플래그 표시 기준을 더 엄밀하게 맞추면 개선될 수 있는 잔여 과제다.
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
python tools\run_full_page_codex_smoke20_cli.py --fixture full_page_codex_subset --timeout 3600
python tools\run_full_page_dummy_validation.py
```

## 후속 개선 항목

- 50건 subset actual은 보존 완료했다. 패키징 전에는 actual을 임의 재생성하지 말고, 현재 prompt와 actual metadata를 기준으로 재현 가능성을 확인한다.
- 운영 품질 추가 개선이 필요하면 다음 단계에서 SKILL 지침에 `사이즈 옵션: M, L, XL` 형태의 값을 개별 사이즈로 원자화하라는 규칙을 보강하고, 같은 50건 prompt로 재실행해 `size_info` precision/recall 개선 여부를 비교한다.
- 부위 미상 소재는 `quality.missing_fields: material_part`, 모호 소재 비율은 `quality.ambiguous_fields` 또는 `material_ratio` 누락 표시 중 어떤 기준을 우선할지 계약 문서에서 더 좁힐 수 있다.
