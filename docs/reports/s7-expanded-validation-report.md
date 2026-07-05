# S7.5 확장 검증 및 재현성 보존 보고서

## 요약
- 실행일: 2026-07-06 KST
- 결과 스냅샷: `docs/reports/s7-expanded-validation-results.json`
- 목적: S8 패키징 전에 합성 더미, 실제 Codex 출력, 짧은 공개 상품 snippet 기반 sanity check를 같은 입력·명령·결과로 다시 추적할 수 있게 보존
- 결론: 패키징 전 필수 acceptance gate를 통과했다. 실제 공개 샘플 10건은 전체 성능 벤치마크가 아니라 자동 fetch 없이 짧은 공개 snippet으로 수행한 현실성 점검이다.

## 보존된 산출물
| 위치 | 내용 |
|---|---|
| `tests/fixtures/expanded_dummy/` | 합성 입력 100건, expected JSON, reference actual JSON, duplicate labels |
| `tests/fixtures/codex_subset/` | Codex 실행 subset 20건, prompt, prompt template, expected JSON, actual JSON, duplicate labels |
| `tests/fixtures/real_sanity/` | 공개 상품 snippet 10건, URL, 확인일, expected JSON, actual JSON, duplicate labels |
| `docs/reports/s7-expanded-validation-results.json` | 실행 환경, 명령, 평가 결과, dedup 교차 카테고리 점검, 주요 파일 SHA-256 |
| `tools/generate_expanded_validation_fixtures.py` | 합성 fixture와 실제 공개 snippet fixture 재생성 스크립트 |
| `tools/run_expanded_validation.py` | 재현성 검증 실행 및 결과 스냅샷 생성 스크립트 |

## 실행 환경
- Python: `3.12.4 | packaged by Anaconda, Inc.`
- Platform: `Windows-11-10.0.26200-SP0`
- Codex CLI: `codex-cli 0.142.5`
- 결과 생성 시각: `2026-07-05T19:22:02.964634+00:00` (KST 2026-07-06 04:22:02)

## 재실행 명령
합성 fixture와 실제 공개 snippet fixture는 아래 명령으로 재생성한다. `codex_subset`은 3단계 taxonomy 도입 이전 Codex 실행 결과를 보존하는 historical 세트이므로 이 명령이 덮어쓰지 않는다.

```powershell
python tools\generate_expanded_validation_fixtures.py
```

보존된 expected/actual JSON을 기준으로 전체 검증을 다시 실행한다.

```powershell
python tools\run_expanded_validation.py
```

개별 비교가 필요하면 아래처럼 실행한다.

```powershell
python tests\evaluate_product_agentizer.py --inputs tests\fixtures\codex_subset\source_inputs.json --expected tests\fixtures\codex_subset\expected_products.json --actual tests\fixtures\codex_subset\actual_products.json --dedup-labels tests\fixtures\codex_subset\duplicate_labels.json --pretty
```

Codex actual 재생성은 모델 상태에 따라 값이 달라질 수 있다. 이번 제출 기준 actual은 `tests/fixtures/codex_subset/actual_products.json`과 `tests/fixtures/real_sanity/actual_products.json`에 보존했으며, 사용 prompt는 각 폴더의 `prompt.md`에 저장했다. 단, `codex_subset` actual은 historical Codex 출력의 구조화 값을 보존하되 현재 schema `0.2.0`에 맞추기 위해 `schema_version`과 `product.detail_type: null`만 추가한 호환 마이그레이션본이다.

## 검증 결과
| 영역 | 결과 | 판정 |
|---|---:|---|
| 합성 expected 100건 schema-valid | 100/100 | 통과 |
| 합성 self-check micro precision | 100.00% | 통과 |
| 합성 self-check micro recall | 100.00% | 통과 |
| 합성 self-check detail_type precision/recall | 100.00% / 100.00% | 통과 |
| 합성 dedup accuracy | 100.00% (20/20) | 통과 |
| 합성 cross-category high-confidence false duplicate | 0건 | 통과 |
| Codex subset 20건 actual schema-valid | 20/20 | 통과 |
| Codex subset micro precision | 95.52% | 통과 |
| Codex subset micro recall | 95.85% | 통과 |
| Codex subset detail_type precision/recall | not_applicable | historical actual 보존을 위해 expected/actual 모두 null |
| Codex subset dedup accuracy | 100.00% (4/4) | 통과 |
| 실제 공개 snippet 10건 actual schema-valid | 10/10 | 통과 |
| 실제 공개 snippet detail_type precision/recall | 100.00% / 100.00% | 통과 |
| 실제 공개 snippet 자동 fetch | 0건 | 통과 |
| 실제 공개 snippet 법적 적합/부적합 판정 | 0건 | 통과 |
| 실제 공개 snippet dedup accuracy | 100.00% (5/5) | 통과 |

합성 self-check는 `reference_actual_products.json`이 expected와 같은 기준선인지 확인하는 coverage/self-check다. 합성 입력에는 `제품분류: <subcategory> > <detail_type>` 단서가 포함되어 있으므로, 이 100% 수치를 blind extraction 모델 성능으로 해석하지 않는다.

Codex subset은 3단계 taxonomy 도입 이전에 생성한 historical actual을 보존하는 재현성 세트다. 따라서 `detail_type`은 expected와 actual 모두 `null`로 두었고, 해당 필드의 precision/recall은 `not_applicable`로 기록된다. 3단계 `detail_type` 자체의 schema/parent-child 검증은 합성 100건, 실제 공개 snippet 10건, schema negative fixture에서 확인했다.

## 실제 공개 샘플 해석
실제 공개 샘플은 10건이며 아우터 5건, 상의 5건으로 구성했다. 전체 상세페이지 사본을 저장하지 않고 상품명, 소재, 컬러, 사이즈, 관리처럼 검증에 필요한 짧은 factual snippet만 `source_inputs.json`에 보존했다.

탐색적 비교 결과는 micro precision 64.38%, micro recall 76.30%다. 이는 acceptance threshold가 아니라 짧은 snippet 라벨과 Codex의 보수적 누락 표시가 얼마나 충돌하는지 보기 위한 분석 수치다. `title`, `category`, `subcategory`, `detail_type`은 100% 일치했고, 주요 차이는 `fit`, `size_info`, `quality.missing_fields`, 일부 소재 `part` 해석에서 발생했다.

실제 공개 샘플 출처는 아래 URL을 메타데이터로만 보존했다. 플러그인과 평가 스크립트는 URL을 자동으로 열지 않는다.

- https://www.musinsa.com/products/4308999
- https://www.musinsa.com/products/2101205
- https://www.musinsa.com/products/4922894
- https://www.musinsa.com/products/3617977
- https://www.musinsa.com/products/4332165
- https://www.musinsa.com/products/4783312
- https://www.musinsa.com/products/3054408
- https://www.musinsa.com/products/3661999
- https://www.musinsa.com/products/3054409
- https://www.musinsa.com/products/1196892

## 실패 분석과 보완
확장 검증 구현 중 실제 문제가 발생해 `Troubleshootinglog.md`에 기록했다.

- fixture 생성기에서 duplicate case title 경로를 잘못 참조해 `KeyError`가 발생했다. `structured_product.product.title` 경로를 사용하도록 수정했다.
- 실제 공개 샘플 expected 생성 시 `size_info`, `missing_fields`, `ambiguous_fields` tuple 위치가 어긋나 schema 검증이 실패했다. spec 구조를 분리해 수정했다.
- 평가 스크립트가 custom 상대 경로를 받을 때 `relative_to(ROOT)`에서 실패했다. 상대 경로를 repo root 기준으로 해석한 뒤 표시 경로만 안전하게 계산하도록 수정했다.
- Windows 콘솔 인코딩 때문에 평가 JSON의 한글 차이 토큰이 깨졌다. 평가 스크립트 stdout을 UTF-8로 고정했다.
- subset/real sanity 평가에는 각각의 duplicate label 파일이 필요했다. 각 fixture 폴더에 전용 label을 보존했다.

성능 수치를 맞추기 위해 expected fixture를 완화하지 않았다. 이번 보완은 fixture 생성, 평가 경로 처리, 출력 인코딩, 재현성 보존 구조에 한정했다.

## 패키징 전 판정
- 필수 acceptance gate는 통과했다.
- 공개 샘플은 법적 적합성 판단을 하지 않았고, 자동 fetch도 수행하지 않았다.
- `out/`의 raw 실행물은 임시 산출물로 남기고, 최종 재현에 필요한 입력·expected·actual·평가 결과·명령·hash는 `tests/fixtures/`와 `docs/`에 선별 보존했다.
- README, Worklog, Troubleshootinglog 갱신 후 S8 패키징으로 넘어갈 수 있다.
