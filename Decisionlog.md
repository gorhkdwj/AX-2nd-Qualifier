# Decisionlog · AX해커톤 예선 2차 제출(무신사 문제 2)

방향을 바꾸거나 이후 작업에 영향을 주는 **중요한 결정만** 기록한다. 사소한 수정은 Worklog에만 남긴다. (규칙: CLAUDE.md / AGENTS.md 11절)

## 기록 형식
```
### D-00N · 결정 제목
**상황** / **검토한 선택지** / **결정** / **근거** / **영향** / **재검토 조건**
```

---

### D-024 · 배색 소재 부위 보수 기준 정렬
**상황**
- S7.7 50건 Codex subset에서 micro precision/recall이 99.74%로 남은 원인은 `materials` 2건의 `trim`/`unknown` 차이였다.
- 입력 문구는 `리사이클 섬유와 배색 폴리에스터를 사용했으나 숫자 혼용률은 표기되어 있지 않습니다`였고, expected는 `배색 폴리에스터`를 `trim`으로 라벨링했지만 Codex actual은 구체 부위가 없다고 보고 `unknown`으로 기록했다.
- 사용자는 `unknown` 기준으로 정렬하는 것과 현상 유지의 차이를 확인한 뒤, 보수 기준 정렬을 진행하라고 요청했다.

**검토한 선택지**
- 기존 expected의 `trim` 라벨을 유지하고 99.74% 결과를 설명한다.
- `배색`이라는 단어가 보이면 항상 `trim`으로 추출하도록 SKILL을 강화한다.
- 실제 적용 부위가 명시되지 않은 `배색 폴리에스터`는 `unknown`으로 두고, `배색부`, `카라 배색`, `소매 배색`처럼 구체 부위가 있을 때만 `trim` 또는 더 구체적인 부위로 기록한다.

**결정**
- 세 번째 선택지를 채택한다.
- `배색 폴리에스터`처럼 구체 적용 부위가 없는 소재는 `trim`으로 단정하지 않고 `part: "unknown"`으로 둔다.
- 소재 항목 중 하나라도 `part: "unknown"`이면 `quality.missing_fields`에 `material_part`를 추가한다.
- 이 기준을 `docs/requirements-contract.md`, `src/skills/product-agentizer/SKILL.md`, fixture 생성기와 S7.7/S7.5 검증 fixture에 반영한다.

**근거**
- 소재 부위는 상품정보 고지와 연결될 수 있으므로, 입력 근거가 없는 부위를 과감하게 추정하는 것보다 보수적으로 `unknown`을 남기는 편이 프로젝트의 엄격 처리 원칙과 맞다.
- 특정 상품 ID를 맞추는 예외가 아니라, "구체 부위가 없으면 단정하지 않는다"는 일반 규칙이므로 과적합 위험을 줄인다.
- 변경 후 S7.7 50건 subset과 20건 smoke actual 모두 schema-valid 및 micro precision/recall 100.00%를 기록했다.

**영향**
- S7.7 50건 subset 결과는 schema-valid 50/50, micro precision 100.00%, micro recall 100.00%, `materials` precision/recall 100.00%, `size_info` precision/recall 100.00%로 갱신됐다.
- `tests/fixtures/full_page_dummy`, `full_page_codex_subset`, `full_page_codex_smoke20`, `expanded_dummy`의 expected/reference 기준이 보수 라벨로 정렬됐다.
- S7.7 smoke20 actual은 새 SKILL 기준으로 재실행해 보존했다.

**재검토 조건**
- 실제 운영 데이터에서 `배색 폴리에스터`가 일관되게 특정 부위를 뜻한다는 근거가 확보되는 경우.
- taxonomy에 `contrast_panel`, `color_blocking`처럼 더 세밀한 소재 부위/디자인 역할 구분이 추가되는 경우.

---

### D-023 · S7.8 size_info 표기 패턴 보강 검증 채택
**상황**
- S7.7 실제 페이지형 합성 subset 50건에서 `size_info` precision/recall 100.00%를 달성했지만, 이 결과는 합성 상세페이지형 50건 기준이었다.
- 사용자는 실제 상품페이지에서 등장할 수 있는 사이즈 표기 방식이 합성데이터에 충분히 반영되지 않았을 가능성을 지적했다.
- 실제 상품 원문 전체를 저장하거나 로컬 전용 비공개 검증 데이터를 만드는 방식은 윤리·재현성 기준과 맞지 않으므로 제외해야 했다.

**검토한 선택지**
- 현재 S7.7 결과만 유지하고 한계로 기록한다.
- 실제 공개 상품 페이지 전체를 수집해 검증한다.
- 실제 페이지에서 나올 법한 size 표기 패턴을 합성 fixture로 확장하고, 실제 Codex CLI actual을 격리 workspace에서 생성한다.

**결정**
- S8 패키징 전에 S7.8 `size_info` 표기 패턴 보강 검증을 추가한다.
- 실제 상품 원문은 저장하지 않고, 문자형 옵션, 숫자형 옵션, `FREE`/`ONE SIZE`, 괄호 혼합 표기, 실측 행, 표 형태 실측, 모델 착용, 비교 가이드, 추천·후기 noise를 48건 합성 fixture로 구성한다.
- actual은 expected fixture가 없는 격리 workspace에서 실제 Codex CLI로 생성하고, 입력·expected·actual·metadata·prompt·평가 결과를 모두 보존한다.

**근거**
- `size_info`는 실제 상품 페이지에서 표기 방식이 다양하므로, S7.7의 50건 결과만으로는 coverage 설명이 부족하다.
- 합성 fixture는 정답 라벨과 재현성을 보장하면서도 실제 상품 페이지 전체 복사나 자동 크롤링을 피할 수 있다.
- 추천·후기 기반 문구를 negative case로 넣어 정적 상품 size_info와 동적/개인화 정보를 구분하는 안전 기준도 확인할 수 있다.

**영향**
- `docs/size-info-coverage-plan.md`, `tests/fixtures/size_info_patterns/`, `tools/generate_size_info_pattern_fixtures.py`, `tools/run_size_info_pattern_validation.py`, S7.8 report/results가 추가됐다.
- `SKILL.md`와 `requirements-contract.md`의 size_info 처리 규칙이 문자/숫자/실측/모델착용/비교가이드/추천노이즈 유형까지 확장됐다.
- 최종 검증 설명은 S7.5, S7.7, S7.8을 함께 언급한다.
- 현재 결과는 schema-valid 48/48, `size_info` precision/recall 100.00%, TP/FP/FN 97/0/0, recommendation_noise false positive 0건이다.

**재검토 조건**
- 실제 허가된 상품 데이터셋을 사용할 수 있게 되거나, shoes/bottom 등 size 체계가 크게 다른 카테고리를 추가하는 경우.
- `size_info`를 필터·추천·비교 질의에서 typed field로 직접 사용해야 하는 요구가 생기는 경우.

---

### D-022 · size_info schema 변경 보류와 SKILL-only 원자화 채택
**상황**
- S7.7 50건 실제 Codex subset 검증은 전체 수용 기준을 통과했지만, `size_info` precision 59.65%, recall 33.01%로 낮게 남았다.
- 주요 원인은 `사이즈 옵션: M, L, XL` 같은 한 줄 옵션을 Codex가 하나의 문자열로 보존한 반면, expected는 `M`, `L`, `XL` 개별 항목으로 라벨링한 차이였다.
- 사용자는 schema 변경 계획은 문서화하되, 당장은 SKILL 변경 계획을 진행하라고 요청했다.

**검토한 선택지**
- `schema_version`을 `0.3.0`으로 올리고 `size_info`를 객체 배열로 변경한다.
- schema는 `0.2.0`으로 유지하고 `SKILL.md`와 기준 계약 문서에 size option 원자화 규칙을 명확히 추가한다.
- `size_info` 평가 기준을 완화한다.

**결정**
- 현재 MVP에서는 schema 변경을 보류하고, `size_info` schema v0.3 변경안은 `docs/size-info-schema-change-plan.md`에 조건부 계획으로 보존한다.
- `schema_version: "0.2.0"`의 `size_info: string[]` 구조는 유지한다.
- 판매 가능한 사이즈 옵션은 개별 항목으로 원자화하고, 실측표는 사이즈별 행 단위로 보존하며, 후기·배송·쿠폰·이벤트 문구는 `size_info`에 섞지 않는 기준을 `docs/requirements-contract.md`와 `SKILL.md`에 반영한다.

**근거**
- 현재 문제는 schema가 표현하지 못하는 정보 구조 전체의 문제가 아니라, 반복적으로 나타난 한 줄 옵션 원자화 지침 부족에 가까웠다.
- 패키징 직전 schema 변경은 fixture, evaluator, README, 보고서, actual 재실행 범위를 크게 흔들 수 있다.
- SKILL-only 보강 후 같은 50건 prompt를 재실행한 결과 `size_info` precision/recall이 100.00%/100.00%로 개선되어 목표치를 충족했다.

**영향**
- S7.7 50건 subset 최종 결과는 schema-valid 50/50, micro precision 99.74%, micro recall 99.74%, `detail_type` precision/recall 100.00%, `size_info` precision/recall 100.00%, dedup accuracy 100.00%로 갱신됐다.
- schema v0.3 변경 계획은 활성 구현 기준이 아니라 조건부 재검토 문서로 남는다.
- 남은 주요 개선 후보는 `배색 폴리에스터` 같은 소재 부위 표현의 `trim`/`unknown` 해석 차이다.

**재검토 조건**
- SKILL-only 기준이 다른 실제 입력에서 다시 흔들리거나, typed size query가 MVP 이후 핵심 요구로 부상하는 경우.
- bottom, shoes 등 size 체계가 더 복잡한 카테고리 확장이 확정되는 경우.

---

### D-021 · S7.7 실제 Codex smoke20 격리 실행과 라벨 기준 보정
**상황**
- 20건 실제 Codex CLI smoke 검증을 시작하면서 기존 50건 subset이 앞쪽 50건 중심이라 아우터에 치우쳐 있음을 확인했다.
- 또한 repo 루트 read-only 실행은 expected fixture가 같은 작업 루트에 있어 blind extraction 검증으로 보기 어렵다는 문제가 있었다.
- 첫 격리 실행 결과는 schema-valid였지만 micro precision 0.8629, micro recall 0.9149로 나왔고, 차이는 주로 입력 근거보다 공격적으로 작성된 expected 라벨에서 발생했다.

**검토한 선택지**
- 기존 50건 subset을 그대로 유지하고 20건만 실행한다.
- 20건 smoke와 50건 subset을 대표 선별 방식으로 재구성한다.
- repo 루트에서 실행하되 결과만 기록한다.
- expected/actual fixture가 없는 격리 workspace에 skill과 reference만 복사해 실행한다.

**결정**
- `full_page_codex_subset` 50건과 `full_page_codex_smoke20` 20건을 category, density, detail_type, duplicate pair를 고려한 대표 선별 방식으로 재구성한다.
- 실제 Codex CLI smoke20은 `out/full_page_codex_smoke20_workspace`에 skill과 reference만 복사한 격리 workspace에서 실행한다.
- 입력 텍스트에 없는 TPO를 expected에 넣지 않고, 사이즈 옵션은 개별 사이즈 토큰으로 비교하며, 소재 부위가 명시되지 않은 경우 `part: unknown`과 `quality.missing_fields: material_part`로 라벨링한다.

**근거**
- expected를 볼 수 있는 실행 환경에서는 실제 추출 성능을 평가했다고 보기 어렵다.
- 검증 라벨은 수치를 맞추기 위해 완화하면 안 되지만, 입력 텍스트 근거보다 강한 라벨을 부여하면 오히려 실제 성능을 부당하게 낮게 평가한다.
- 20건 smoke는 50건 전체 실행 전 비용과 리스크를 줄이는 선행 검증이다.

**영향**
- smoke20 실제 Codex CLI 결과는 schema-valid 20/20, micro precision/recall 100.00%, detail_type precision/recall 100.00%, dedup accuracy 100.00%로 기록됐다.
- 50건 full subset은 representative reference actual 상태로 남아 있으며, 실제 CLI 실행은 다음 단계로 남는다.
- S7.7 보고서에는 보완 전후 수치와 원인을 함께 남긴다.

**재검토 조건**
- 50건 전체 Codex CLI 실행에서 같은 유형의 라벨 기준 충돌이나 실제 추출 실패가 다시 나타나는 경우.

---

### D-020 · S7.7 Codex subset actual 실행 분리
**상황**
- S7.7 실제 페이지형 합성 더미 검증을 구현하면서 `full_page_dummy` 300건과 `full_page_codex_subset` 50건을 생성할 수 있게 됐다.
- 다만 50건의 상세페이지형 입력을 실제 Codex CLI로 변환하는 작업은 토큰·시간 소모가 크고, 모델 출력 변동에 따라 반복 실행 결과가 달라질 수 있다.
- 먼저 생성기, schema, evaluator, dedup label, 정보 밀도 coverage가 재현 가능한지 확인해야 했다.

**검토한 선택지**
- 생성과 동시에 Codex CLI 50건 actual을 즉시 실행한다.
- S7.7 구현을 생성기·기준 actual self-check와 실제 Codex CLI actual 실행으로 나눈다.
- Codex subset actual 파일을 만들지 않고 full_page_dummy self-check만 수행한다.

**결정**
- 이번 단계에서는 `full_page_codex_subset/actual_products.json`을 deterministic reference actual로 저장한다.
- 실제 Codex CLI로 `prompt.md`를 실행해 actual을 덮어쓰는 작업은 후속 단계로 분리한다.
- 보고서와 검증 계획에 이 actual이 실제 Codex CLI 출력이 아니라는 점을 명시한다.

**근거**
- 생성기와 평가 절차가 먼저 안정되어야 실제 Codex 실행 결과의 실패 원인을 올바르게 해석할 수 있다.
- 기준 actual self-check는 blind extraction 성능이 아니라 fixture·schema·evaluator·dedup label의 재현성 검증이다.
- 실제 Codex 실행은 비용과 시간이 큰 작업이므로, 사용자가 규모(최소 20건, 축소 30건, 기본 50건)를 선택할 여지를 남기는 것이 안전하다.

**영향**
- S7.7의 현재 통과 수치는 기준 actual 기준이며, 운영 extraction 성능으로 과대 해석하면 안 된다.
- 다음 단계에서 실제 Codex CLI actual을 생성하면 `tests/fixtures/full_page_codex_subset/actual_products.json`, `docs/reports/s7-7-full-page-dummy-validation-report.md`, 결과 JSON을 갱신해야 한다.

**재검토 조건**
- 사용자가 실제 Codex CLI subset 실행 규모를 확정하거나, 마감 전 시간상 reference baseline만으로 패키징하기로 결정하는 경우.

---

### D-019 · 실제 페이지형 합성 더미 검증 채택
**상황**
- S7.5 실제 공개 snippet 10건의 탐색적 비교에서 micro precision/recall이 낮게 나왔고, 원인이 실제 공개 입력의 정보 부족인지 플러그인 고도화 과제인지 구분할 필요가 생겼다.
- 사용자는 평가자가 재현할 수 없는 로컬 전용 검증 데이터를 별도로 남기는 방식은 윤리적으로 부적절하다고 판단했다.
- 동시에 실제 무신사 상품페이지는 상품별 정보 밀도가 균일하지 않으므로, 모든 상품을 완전한 상세정보 입력으로 가정하는 것도 실제 운영 환경과 어긋날 수 있다.

**검토한 선택지**
- 실제 상품 페이지 전체 원문을 저장하거나 크롤링해 검증한다.
- 로컬 전용 full-page 검증을 수행하고 결과만 문서화한다.
- 기존 짧은 snippet 검증만 유지한다.
- 실제 페이지 구조와 정보 밀도 차이를 모사한 대규모 합성 더미데이터를 만들고, 입력·expected·actual·결과를 모두 커밋한다.

**결정**
- 실제 상품 페이지 전체 원문 저장, 자동 fetch, 크롤링, 로컬 전용 비공개 검증은 제외한다.
- `sparse`, `medium`, `full`, `noisy_ambiguous` 정보 밀도별 실제 페이지형 합성 더미데이터를 S7.7 검증 단계로 추가한다.
- 새 기준 문서는 `docs/full-page-dummy-validation-plan.md`로 둔다.

**근거**
- 합성 데이터는 저작권·약관 리스크가 낮고, 출제자가 입력·정답·실행 결과를 그대로 재현할 수 있다.
- 정보가 적은 상품도 실제 운영 환경에 포함될 수 있으므로, Sparse 입력에서 모든 필드를 맞히기보다 없는 정보를 추정하지 않는지를 검증해야 한다.
- Full 입력에서는 소재 부위, 혼용률, 실측표, 관리법, 핏을 충분히 제공하므로 플러그인의 세부 추출 성능을 더 엄격하게 볼 수 있다.

**영향**
- S8 패키징 전 단계가 `S7.5 -> S7.6(3단계 구조 개편) -> S7.7 -> S8`로 확장된다.
- 새 fixture 경로는 `tests/fixtures/full_page_dummy/`와 `tests/fixtures/full_page_codex_subset/`를 사용한다.
- 새 보고서는 `docs/reports/s7-7-full-page-dummy-validation-report.md`와 결과 JSON으로 작성한다.

**재검토 조건**
- 주최측이나 기업이 공식 데이터셋, API, 또는 명시적 수집 허가를 제공하는 경우 실제 데이터 기반 검증 설계를 다시 검토한다.

---

### D-018 · Codex subset historical fixture 보존
**상황**
- 3단계 taxonomy 도입 후 `tools/generate_expanded_validation_fixtures.py`를 다시 실행하면 최신 합성 fixture에서 `codex_subset` expected/source를 재생성하려 했다.
- 하지만 `codex_subset` actual은 3단계 도입 이전 Codex 실행 결과를 보존한 세트이며, 현재 schema `0.2.0` 호환을 위해 `schema_version`과 `detail_type: null`만 추가한 마이그레이션본이다.
- 최신 합성 fixture에서 subset을 다시 만들면 expected의 `detail_type`이 non-null로 바뀌어 문서화한 `detail_type not_applicable` 정책과 충돌한다.

**검토한 선택지**
- 최신 합성 fixture 기준으로 `codex_subset` expected/source를 모두 재생성한다.
- historical actual을 버리고 Codex subset actual을 새로 생성한다.
- `codex_subset`은 committed fixture로 보존하고, 생성기는 합성 100건과 실제 공개 snippet 10건만 재생성한다.

**결정**
- `codex_subset`은 historical Codex 실행 보존 세트로 유지한다.
- `tools/generate_expanded_validation_fixtures.py`는 `codex_subset`을 덮어쓰지 않는다.
- `codex_subset`의 재현성은 committed source/expected/actual/prompt/duplicate labels와 `docs/reports/s7-expanded-validation-results.json`의 SHA-256 해시로 검증한다.

**근거**
- Codex actual은 모델 상태에 따라 재생성 결과가 달라질 수 있어 historical output 보존이 S7.5 재현성 목표에 더 맞다.
- `detail_type` 자체의 coverage와 parent-child 검증은 합성 100건, 실제 공개 snippet 10건, schema negative fixture에서 별도로 확인한다.
- 보존 세트를 최신 synthetic에서 재생성하면 수치가 좋아지거나 나빠지는 문제가 아니라 평가 대상의 의미가 바뀐다.

**영향**
- 문서에서는 `tools/generate_expanded_validation_fixtures.py`가 합성 fixture와 실제 공개 snippet fixture를 재생성한다고 설명한다.
- `codex_subset`을 수정해야 하는 경우에는 생성기 재실행이 아니라 별도 결정과 Worklog/Decisionlog 기록이 필요하다.

**재검토 조건**
- 새 Codex 실행을 공식 기준 actual로 채택하거나, 3단계 `detail_type` 추출 성능을 Codex subset에서 직접 측정하기로 범위를 바꾸는 경우 재검토한다.

---

### D-017 · 3단계 상품 분류 구조 도입
**날짜**: 2026-07-06 KST

**결정**
- 상품 분류 구조를 기존 `category/subcategory`에서 `category/subcategory/detail_type`으로 확장한다.
- 이번 구현 범위는 계속 `outer`와 `top`으로 유지한다.
- `detail_type`은 필수 필드로 두되 값은 `string | null`을 허용한다.
- `schema_version`과 `taxonomy_version`은 `0.2.0`으로 올린다.
- 공식 무신사 상의 9개, 아우터 22개 세부 카테고리를 `detail_type` 기준으로 반영한다.

**근거**
- 실제 무신사 몰 카테고리에는 `트러커 재킷`, `레더/라이더스 재킷`, `숏패딩/헤비 아우터`, `후드 티셔츠`처럼 현재 `subcategory`보다 세부적인 유형이 존재한다.
- 이 값을 모두 `subcategory`로 승격하면 형태·소재·계절·스타일 의미가 한 필드에 섞인다.
- `detail_type`을 별도 계층으로 두면 실제 몰 세부 유형을 보존하면서도 소재 질의는 `materials`, 계절 질의는 `seasons`를 우선하도록 역할을 분리할 수 있다.

**영향**
- `schema.json`, `taxonomy.json`, `SKILL.md`, `validate.py`, `dedup.py`, `tests/evaluate_product_agentizer.py`, fixture 전체, README와 docs를 함께 갱신한다.
- 기존 S7.5 검증 결과는 `0.1.0` 기준이므로 `0.2.0` 구조로 재실행하고 보고서를 갱신한다.

---

### D-016 · docs 보고서 폴더 분리
**상황**
- S5/S6/S7.5 검증 보고서와 결과 JSON이 `docs/` 루트의 계획·계약 문서와 섞여 있어, 어떤 문서가 실행 기준이고 어떤 문서가 결과 보고서인지 한눈에 구분하기 어려웠다.
- 사용자가 `docs` 안에 report 하위 폴더를 만들어 plan과 report를 나누는 방안을 제안했다.

**검토한 선택지**
- 기존처럼 `docs/` 루트에 모든 문서 유지
- 모든 보고서를 `tests/` 하위로 이동
- `docs/reports/`를 만들어 검증·실행 결과 보고서만 분리

**결정**
- `docs/reports/`를 신설해 S5/S6/S7.5 보고서와 S7.5 결과 JSON을 보관한다.
- `docs/` 루트에는 과제 원문, 계획, 요구사항 계약, 검증 계획, 제출 답변처럼 현재 작업 기준 문서를 둔다.
- `tests/fixtures/`에는 검증 입력·expected·actual·label만 유지하고, 사람이 읽는 보고서는 넣지 않는다.

**근거**
- 계획 문서와 결과 보고서의 독자·용도가 다르므로 폴더를 나누면 탐색성이 좋아진다.
- `tests/`는 실행 재료와 테스트 코드 중심으로 유지하는 편이 향후 CI나 평가 도구를 붙일 때 혼동이 적다.
- S7.5 결과 JSON은 실행 환경·명령·hash를 포함한 감사 스냅샷이므로 관련 보고서와 같은 `docs/reports/`에 두는 편이 자연스럽다.

**영향**
- README, validation plan, implementation plan, troubleshooting/work logs의 보고서 경로를 `docs/reports/...` 기준으로 갱신한다.
- 이후 새 검증 보고서나 실행 결과 스냅샷은 기본적으로 `docs/reports/`에 추가한다.

**재검토 조건**
- 보고서 수가 늘어나 단계별 하위 폴더가 필요해지면 `docs/reports/s5/`, `docs/reports/s6/`처럼 더 세분화한다.

---

### D-015 · S8 패키징 전 S7.5 확장 검증 게이트 추가
**상황**
- S7 README와 질문 5문항 답변까지 작성했지만, 사용자가 최종 패키징 전에 대규모 더미 데이터와 실제 공개 샘플로 추가 검증하고, 테스트 데이터·검증 과정·결과를 모두 보존해 재현성을 높이자고 제안했다.

**검토한 선택지**
- 기존 S5/S6 검증 결과만으로 S8 패키징 진행
- 실제 공개 샘플만 소량 추가 확인
- S8 전에 S7.5 확장 검증 단계를 추가하고 입력·expected·actual·평가 결과·명령·환경·hash를 보존

**결정**
- S8 패키징 전에 S7.5 확장 검증 게이트를 추가한다.
- 기본 검증 범위는 합성 100건, Codex subset 20건, 실제 공개 snippet 10건으로 둔다.
- 실제 공개 샘플은 전체 상세페이지 사본이나 자동 크롤링 결과를 저장하지 않고, URL·확인일·짧은 factual snippet만 보존한다.
- 재현에 필요한 결과는 `tests/fixtures/`와 `docs/`에 선별 보존하고, `out/`은 임시 실행물 위치로 유지한다.

**근거**
- 최종 제출 직전에는 성능 수치뿐 아니라 같은 입력과 명령으로 결과를 다시 추적할 수 있는지가 중요하다.
- 합성 데이터는 정답 라벨을 통제할 수 있어 도구 정확성 검증에 적합하고, 실제 공개 snippet은 자동 fetch 없이 현실성만 점검할 수 있어 안전하다.
- Codex actual output은 모델 상태에 따라 재생성 결과가 달라질 수 있으므로 제출 기준 actual을 fixture로 보존해야 한다.

**영향**
- S8 패키징 전 README, Worklog, Troubleshootinglog, 비밀정보 검색, 재현성 결과 문서를 추가로 갱신한다.
- 실제 공개 샘플의 precision/recall은 짧은 snippet 기반 탐색 지표로만 해석하고, acceptance threshold는 Codex subset과 schema/dedup gate에 둔다.

**재검토 조건**
- MVP 범위가 `outer`/`top` 밖으로 확장되거나, 공식 API·MCP 기반 데이터 접근이 도입되면 S7.5 fixture 범위와 안전 정책을 다시 정한다.

---

### D-001 · 에이전트 지침 파일 동기화 기준 확정
**상황**
- 기존에는 `CLAUDE.md`만 프로젝트 작업 헌법으로 존재했고, Codex가 우선 참조할 수 있는 `AGENTS.md`가 없었다.

**검토한 선택지**
- `CLAUDE.md`만 유지
- `AGENTS.md`를 별도로 작성
- `CLAUDE.md`와 `AGENTS.md`를 동일 내용으로 유지

**결정**
- `CLAUDE.md`와 `AGENTS.md`를 같은 내용의 쌍둥이 문서로 유지한다.
- 한쪽을 수정하면 다른 쪽도 즉시 동기화하고, 수정 후 두 파일의 내용 또는 해시가 동일한지 확인한다.

**근거**
- Claude 계열 도구와 Codex 계열 도구가 같은 프로젝트 기준을 공유해야 작업 방식, 로그 규칙, 제출물 구조, 보안 원칙이 어긋나지 않는다.
- 같은 내용을 두 문서에 유지하면 도구별 기본 참조 파일 차이로 인한 지침 누락을 줄일 수 있다.

**영향**
- 앞으로 작업 규칙이 바뀌면 두 파일을 모두 갱신해야 한다.
- 지침 의미 변경은 Decisionlog에, 단순 동기화는 Worklog에 기록한다.

**재검토 조건**
- 특정 도구에서 반드시 다른 지침이 필요한 상황이 생기면 두 파일을 분리하지 않고, 같은 문서 안에 도구별 예외 규칙으로 명시한다.

---

### D-002 · GitHub 원격 저장소 연결
**상황**
- 현재 작업 폴더가 아직 Git 저장소가 아니었고, 사용자가 `gorhkdwj/AX-2nd-Qualifier.git` 저장소 연결과 푸시를 요청했다.

**검토한 선택지**
- 로컬 Git 저장소만 초기화
- GitHub 원격 저장소를 연결하되 푸시는 보류
- GitHub 원격 저장소를 연결하고 `main` 브랜치로 즉시 푸시

**결정**
- 로컬 저장소를 `main` 브랜치로 초기화하고 `origin`을 `https://github.com/gorhkdwj/AX-2nd-Qualifier.git`로 설정한 뒤 푸시한다.

**근거**
- 사용자가 원격 저장소 연결과 푸시를 명시적으로 요청했다.
- `git ls-remote` 결과 원격 저장소에 기존 브랜치 출력이 없어 초기 푸시 충돌 위험이 낮았다.

**영향**
- 이후 작업은 `main` 브랜치에서 `origin/main`과 추적 관계를 가진 상태로 진행한다.
- 주요 변경 후 커밋·푸시하는 기존 프로젝트 원칙을 적용한다.

**재검토 조건**
- GitHub 저장소 정책상 브랜치 보호, PR 기반 작업, 또는 별도 브랜치 전략이 필요해지면 원격 운영 방식을 다시 정한다.

---

### D-003 · 매 작업 자동 commit·push + logs/ Git 제외(로컬 전용) 정책
**상황**
- 사용자가 (1) 모든 작업이 끝날 때마다 헌법에 따라 즉시 commit·push 하도록 하고, (2) `logs/`(AI 대화 로그)는 Git에 올리지 말고 로컬에서만 관리하도록 요청했다.
- 기존 헌법(D-002 기준)은 `logs/`를 "과제 제출 대상이므로 Git에서 제외하지 않는다"고 규정하고 있었고, 첫 커밋에 `logs/`가 이미 포함되어 있었다.

**검토한 선택지**
- (자동화) 매 작업 후 자동 commit·push vs 사용자가 요청할 때만
- (logs 처리) Git 추적 유지 vs `.gitignore`로 제외하고 로컬 전용

**결정**
- 매 작업(주요 사용자 요청) 종료 시 자동으로 commit·push 한다.
- `logs/`는 `.gitignore`로 Git에서 제외하고 로컬에서만 관리한다. 이미 추적 중이던 `logs/`는 `git rm --cached`로 추적 해제(로컬 파일은 유지).
- 단, `logs/`는 최종 제출물(`submission.zip`)에는 반드시 원본 그대로 포함한다(git 저장소 ≠ 제출물).

**근거**
- 사용자가 두 정책을 명시적으로 요청했다.
- 과제 규정은 "제출물(zip)"에 로그 포함을 요구할 뿐 Git 저장소 공개를 요구하지 않으므로, 로그를 로컬·zip으로만 관리해도 규정을 충족하며 공개 저장소에 대화 로그가 노출되는 것을 피할 수 있다.

**영향**
- 이후 `logs/` 변경은 커밋되지 않는다. 최종 제출 시 로컬 `logs/`를 zip에 담는 절차를 별도로 수행해야 한다.
- 매 작업 후 commit·push가 기본 동작이 된다. commit 전 `git status`로 `logs/`·비밀정보 혼입 여부를 확인한다.
- 헌법 7·10절과 `.gitignore`를 이에 맞게 갱신했다(CLAUDE.md/AGENTS.md 동기화 유지).

**재검토 조건**
- 과제 제출 방식이 "Git 저장소 URL 제출"로 바뀌면 `logs/` 포함 방식을 다시 정한다.
- 자동 commit·push가 비밀정보 노출 위험을 키운다고 판단되면 커밋 전 검증 절차를 강화한다.

---

### D-004 · 후보 5→3 축소 (채널톡·삼일PwC 제외)
**상황**
- 최종 종합 보고서(`docs/company-research_references/company-research-final-report.md`)와 절대 점수 비교를 바탕으로, 사용자가 채널톡과 삼일PwC를 후보에서 제외하기로 결정했다.

**검토한 선택지**
- 5개 후보 유지 / 일부 제외

**결정**
- 후보를 무신사·메디테라피·마이리얼트립 3개로 좁힌다(채널톡·삼일PwC 제외).

**근거**
- 삼일PwC: 검증된 문제가 감사조서 등 기밀 데이터 영역과 밀접해 공개자료 기반 실증이 가장 어렵고(마감 내 완성 가능성 최저), 삼일 특정 근거가 얇음.
- 채널톡: 공개자료로 검증된 핵심 문제(완전자본잠식)가 "고객이 겪는 문제"·플러그인화 프레이밍이 약함.
- 사용자의 명시적 지시.

**영향**
- 이후 문제 정의·플러그인 설계는 3개 사에 한정한다. `docs/plugin-directions.md`에 3사 각 3개 문제와 플러그인 방향을 정리했다.
- 최종 1개 사 선정은 아직 미확정(사용자 검토 후 결정).

**재검토 조건**
- 3개 사 모두 공개자료·구현 범위에서 막히면 제외한 후보를 다시 검토한다.

---

### D-005 · 안전성(법적 위험) 기준 플러그인 방향 축소
**상황**
- 후보 3사의 플러그인 방향 중 일부(무신사 1-C 평판·리뷰 모니터링, 메디테라피 2-C 글로벌 리뷰 트래커)가 **제3자 UGC(리뷰·커뮤니티) 대량 크롤링**을 핵심 전제로 함.
- 크롤링은 저작권·데이터베이스제작자권·부정경쟁방지법(데이터 부정취득)·개인정보보호법·이용약관 위반 위험이 있으며, 특히 출제 3사는 데이터 부정취득 판례(마이리얼트립 v. 민다, 2025)가 있는 영역이라 민감.

**검토한 선택지**
- 위험 방향도 유지하되 크롤링만 조심 / 텍스트 다루는 방향 전부 제외 / 핵심이 위험한 방향만 제외하고 나머지는 안전한 입력방식으로 재설계

**결정**
- **핵심 전제가 위험한 데이터 수집인 방향만 제외**한다(무신사 1-C, 메디테라피 2-C).
- 나머지 방향은 유지하되 **BYO(사용자 제공/자기 페이지 지정) 입력 + 공개 법령/고시·공식 도움말 + 더미 검증**으로 재설계한다.
- 무신사 1-A·1-B는 하나의 표기 검수기로 통합.
- "텍스트를 다룬다"는 이유만으로 안전한 방향(광고규정 점검·전환 코치·문의 triage 등)까지 버리지 않는다.

**근거**
- 위험한 건 "방향"이 아니라 "데이터 수집 방식"이므로, 방식만 바꾸면 대부분 안전하게 성립.
- 검증은 더미 픽스처 + 소량 공개 인용으로 충분(오히려 더 재현·엄밀). 크롤링이 불필요.
- 과제는 데이터셋 구축을 요구하지 않으며, 위험 스크래퍼 포함은 평가·법적으로 불리.

**영향**
- 남은 안전 방향: 무신사 1개(표기 검수기), 메디테라피 2개(광고규정·전환 코치), 마이리얼트립 3개(문의 triage·규정 네비·도움말 감사).
- 검증 데이터 정책을 `docs/validation-plan.md`에 명문화, 방향 정리를 `docs/plugin-directions.md`에 반영(제외 방향은 부기 B에 사유와 함께 보존).

**재검토 조건**
- 사용자가 권한을 가진 텍스트를 직접 제공하는 축소형이 필요하면, 모니터링성 대량 수집 없이 부활 검토.
- 특정 사이트에 대해 공식 API·라이선스·명시적 이용허락이 확보되면 데이터 사용 범위를 다시 정한다.

---

### D-006 · 플러그인·스킬 제작 불변 규칙 헌법화
**상황**
- `docs/technical_references/`의 공식 문서 검토 결과, 제출 플러그인 구조와 skill 작성 방식에서 반복 실수를 막기 위해 헌법에 고정할 만한 규칙이 확인됐다.
- 사용자가 플러그인 패키징 규칙과 Skill 작성 원칙만 우선 적용하고, hook·override·API/MCP 운영 규칙은 사용 시점에 재검토하겠다고 지시했다.

**검토한 선택지**
- 기술 참고 문서 전체를 헌법에 상세 반영
- 플러그인 패키징·skill 작성의 필수 규칙만 짧게 반영
- 현재 헌법 유지

**결정**
- `CLAUDE.md`와 `AGENTS.md`에 `5.1 Codex 플러그인·스킬 제작 원칙`을 추가한다.
- 반영 범위는 `plugin.json` 위치, 플러그인 루트 구조, manifest 경로 규칙, 안정적 plugin name, skill 단일 책임, `SKILL.md` 필수 metadata, skill description 작성·검증 원칙으로 한정한다.

**근거**
- 이번 과제의 최종 제출물은 Codex 플러그인이므로 구조 오류와 skill 오발동을 초기에 방지해야 한다.
- 기술 참고 문서를 모두 헌법에 옮기면 지침이 장황해지고 실제 작업 토큰을 불필요하게 소비할 수 있으므로, 반복 확인이 필요한 불변 규칙만 반영하는 편이 적절하다.

**영향**
- 이후 구현 단계에서 `src/.codex-plugin/plugin.json`과 `src/skills/*/SKILL.md`를 만들 때 해당 규칙을 기본 검증 기준으로 삼는다.
- hook 신뢰 검토, `AGENTS.override.md`, API·MCP 권한 규칙은 실제로 해당 기능을 도입할 때 별도 결정으로 기록한다.

**재검토 조건**
- 플러그인에 hook, MCP server, app connector, marketplace metadata를 실제로 포함하게 되면 관련 운영 규칙을 추가한다.

---

### D-007 · 2차 도전 기업·문제 확정
**상황**
- 후보 조사와 방향 정리 이후 무신사에는 문제 1(상품정보 표기 검수기)과 문제 2(상품 데이터 에이전트화 변환기) 두 안전한 선택지가 남아 있었다.
- `docs/musinsa-agentizer-plan.md` 검토 결과, 문제 2는 무신사 테크리드 인터뷰의 에이전트-first 비전과 플랫폼·상품 데이터 파편화 신호에 직접 대응한다.
- 사용자가 무신사 문제 2를 이번 제출의 공식 최종 주제로 확정했다.

**검토한 선택지**
- 무신사 문제 1: 상품정보 표기 오류·누락 검수기
- 무신사 문제 2: 상품 데이터 에이전트화 변환기
- 메디테라피 또는 마이리얼트립의 보류 후보

**결정**
- 이번 AX 해커톤 예선 2차 제출은 **무신사 / 문제 2 · 상품 데이터 에이전트화 변환기**로 확정한다.
- MVP는 아우터·상의 2개 카테고리의 상품 상세 텍스트를 구조화 JSON, 표준 taxonomy 매핑, 중복 후보, 에이전트 질의 descriptor로 변환하는 범위로 한정한다.
- 입력은 사용자가 직접 붙여넣은 상품 상세 텍스트(BYO)로 제한하고, URL은 출처 메타데이터로만 사용한다. 자동 크롤링은 포함하지 않는다.

**근거**
- 무신사 인터뷰 전사본에서 “동일한 상품을 두 번 등록해야 되는 불편함”, “기술이 파편화”, “에이전트가 사용하는 첫 번째 도구가 무신사이길”이라는 핵심 신호가 확인됐다.
- 문제 2는 해당 신호와 문제-해결 매칭이 강하고, 좁은 MVP로 정의하면 공개자료·더미 픽스처만으로 안전하게 시연·검증할 수 있다.
- 문제 1은 근거 검증 강도가 더 높지만 규정 준수·백오피스 성격이 강해, 무신사 인터뷰의 에이전트-first 방향성과의 직접성은 문제 2가 더 높다.

**영향**
- `docs/project-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`, `docs/requirements-contract.md`, `docs/company-selection.md`, `CLAUDE.md`, `AGENTS.md`, `README.md`를 무신사 문제 2 기준으로 갱신한다.
- 이후 구현은 `docs/requirements-contract.md`와 `docs/musinsa-agentizer-plan.md`를 기준으로 진행한다.
- 후보 비교 문서들은 선정 근거 보존용으로 유지한다.

**재검토 조건**
- 원본 영상 대조 결과 핵심 인용이 부정확하거나, MVP가 마감 내 검증 가능한 수준으로 좁혀지지 않으면 무신사 문제 1로 회귀를 검토한다.

---

### D-008 · docs 정보 구조 정리와 선정 전 후보 문서 비활성화
**상황**
- 무신사 문제 2가 공식 확정된 뒤에도 `docs/` 루트에 활성 구현 기준 문서와 선정 전 후보 비교 문서가 함께 남아 있어, 다음 작업자가 어떤 문서를 우선 봐야 하는지 혼동할 수 있었다.
- 사용자가 `docs/` 전용 README 생성과 불필요 문서의 `docs/archive/` 이동 검토를 요청했다.

**검토한 선택지**
- 모든 문서를 `docs/` 루트에 유지
- 활성 구현 문서만 루트에 두고, 선정 전 후보 방향 문서는 archive로 이동
- 기업 조사 근거까지 모두 archive로 이동

**결정**
- `docs/README.md`를 생성해 활성 문서, 근거·참조 폴더, archive의 역할을 구분한다.
- `docs/plugin-directions.md`는 선정 전 후보 방향 비교 문서이므로 `docs/archive/plugin-directions_PRE_SELECTION.md`로 이동해 비활성 자료로 보관한다.
- 기업 조사·팩트체크 문서는 선정 근거 추적에 필요하므로 `docs/company-research_references/`에 유지한다.

**근거**
- 현재 구현 기준은 `docs/requirements-contract.md`, `docs/musinsa-agentizer-plan.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`로 충분히 고정되어 있다.
- `plugin-directions`는 후보 3사·복수 문제 비교와 안전성 검토 이력을 담고 있어 삭제하지는 않되, 활성 구현 기준으로 남겨두면 범위 혼동을 만들 수 있다.

**영향**
- 구현 작업자는 `docs/README.md`의 순서에 따라 현재 기준 문서만 우선 확인한다.
- 후보 방향 검토 이력은 archive에서 추적 가능하되, 현재 구현 기준으로는 사용하지 않는다.

**재검토 조건**
- 무신사 문제 2를 포기하고 다른 후보나 무신사 문제 1로 회귀하면 archive의 후보 방향 문서를 다시 활성화할지 검토한다.

---

### D-014 · Troubleshootinglog 기록 대상 구체화
**상황**
- S6 최종 검증 중 fixture 경로 오인으로 실제 명령 실패가 발생했지만, 처음에는 `Troubleshootinglog.md`에 별도 T-ID로 기록하지 않았다.
- 사용자가 T-001 이후 기록이 이어지지 않는 이유를 확인했고, 향후 같은 판단이 반복되지 않도록 `AGENTS.md`와 `CLAUDE.md`에 기준을 명시할 필요가 생겼다.

**검토한 선택지**
- 기존 "실제 오류·실패" 문구만 유지
- Worklog에만 이번 보정 내용을 남기고 지침 파일은 그대로 둠
- `AGENTS.md`와 `CLAUDE.md`에 기록 대상과 제외 대상을 구체화

**결정**
- `Troubleshootinglog.md` 기록 대상에 잘못된 경로·명령·인코딩·환경 설정·의존성 문제, 예상하지 못한 검증 실패, 실행 실패, 설계 기준 충돌, 보안·로그 원칙 위반 가능성을 명시한다.
- 의도된 실패 fixture나 negative test처럼 "실패해야 통과"인 검증은 원칙적으로 T-ID 대상에서 제외한다.
- 단, 기대와 다른 방식으로 실패했거나 원인 분석·우회·검증 절차 변경이 필요했다면 작은 실수라도 T-ID로 남긴다.

**근거**
- 실제 작업을 멈추거나 우회하게 만든 문제는 이후 재현 가능성이 있어 별도 troubleshooting 기록의 가치가 있다.
- 반대로 의도된 실패 테스트까지 모두 T-ID로 만들면 검증 결과와 문제 해결 기록이 섞여 기록의 신호가 약해진다.
- 두 기준을 함께 적어야 에이전트가 매번 일관되게 판단할 수 있다.

**영향**
- 이후 단계 완료 보고의 "발생한 문제·T-ID" 판단 기준이 명확해진다.
- `AGENTS.md`와 `CLAUDE.md`가 동일하게 갱신되며, 두 파일 동기화 검증을 수행한다.

**재검토 조건**
- 향후 T-ID가 과도하게 많아져 실제 문제 추적성이 떨어지거나, 반대로 실무상 중요한 실패가 계속 누락되면 기록 기준을 다시 조정한다.

---

### D-013 · S6 로컬 marketplace와 Codex CLI 검증 방식
**상황**
- S6에서 로컬 Codex CLI 실제 실행과 플러그인 설치 후보 노출을 검증해야 했다.
- 전역 Codex 설정에는 현재 작업과 무관한 stale marketplace가 있어 `codex plugin list`가 실패했다.

**검토한 선택지**
- 전역 Codex 설정에서 stale marketplace를 제거
- repo-scoped marketplace를 추가하고 전역 설정 수정 없이 임시 `CODEX_HOME`에서 설치 검증
- 플러그인 설치 검증을 생략하고 단독 스크립트 검증만 유지

**결정**
- `.agents/plugins/marketplace.json`을 추가해 `src/` 플러그인을 repo-scoped marketplace 후보로 노출한다.
- 사용자의 전역 Codex 설정은 임의 수정하지 않는다.
- 임시 `CODEX_HOME`에서 marketplace 등록·plugin add를 확인하고, 전역 인증 환경에서는 `codex exec`로 변환·질의 시연을 수행한다.

**근거**
- repo-scoped marketplace는 공식 문서의 로컬 플러그인 테스트 방식이며, 프로젝트에 함께 남길 수 있다.
- stale marketplace는 현재 프로젝트 산출물이 아니므로, S6를 위해 사용자 전역 설정을 임의로 삭제하거나 수정하는 것은 영향 범위가 크다.
- `codex exec`는 전역 인증 환경에서 정상 작동하므로 실제 변환 시연은 별도로 가능하다.

**영향**
- S6 보고서에는 설치 검증과 실행 검증을 분리해 기록한다.
- 완전한 전역 plugin browser/install 재현은 stale marketplace 정리 후 다시 확인해야 한다.

**재검토 조건**
- 사용자가 전역 Codex 설정 정리를 승인하면 `openbell-guard-local` marketplace를 제거하거나 유효한 경로로 수정한 뒤 전역 `codex plugin add`를 다시 검증한다.

---

### D-012 · validate.py JSON Schema 검증 의존성
**상황**
- S4에서 `validate.py`를 구현해야 하며, `schema.json`은 JSON Schema draft 2020-12 형식이다.
- 사용자는 추천한 방향대로 진행하라고 요청했다.

**검토한 선택지**
- 표준 라이브러리만으로 부분 검증 구현
- `jsonschema` 라이브러리를 사용해 JSON Schema를 직접 검증
- 검증 스크립트를 나중 단계로 미룸

**결정**
- `validate.py`는 `jsonschema` 라이브러리의 `Draft202012Validator`를 사용한다.
- `jsonschema`가 설치되어 있지 않으면 설치 안내를 출력하고 종료 코드 2로 실패한다.
- schema 검증 외에 소재 혼용률 상태와 `quality` 필드 연결 등 프로젝트 전용 custom check를 추가한다.

**근거**
- 현재 schema가 draft 2020-12와 조건부 검증(`if`/`then`)을 사용하므로 직접 구현보다 검증 전용 라이브러리를 쓰는 편이 안전하다.
- 의존성이 없을 때 조용히 성공하는 것보다 명확히 실패시키는 편이 제출 전 검증 신뢰성이 높다.

**영향**
- 로컬 검증 환경에는 `jsonschema`가 필요하다.
- 제출 README에는 실제 실행 검증 명령과 의존성 안내를 최종 단계에서 명시해야 한다.

**재검토 조건**
- 제출 환경이 외부 Python 패키지 설치를 허용하지 않는 것으로 확인되면 표준 라이브러리 기반의 제한적 검증기로 폴백하는 방안을 검토한다.

---

### D-011 · 소재 혼용률 엄격 처리 기준
**상황**
- S2에서 `materials.ratio`를 허용했으나, 소재 혼용률은 의류 상품 표시·고지와 연결될 수 있어 추정하거나 부위별 정보를 섞으면 법적 오해를 만들 수 있다.
- 사용자가 혼용률 같은 항목은 법적 오해 소지가 있다면 엄격하게 지정해야 하지 않느냐고 지적했다.

**검토한 선택지**
- 기존처럼 `name`, `ratio`, `evidence`만 유지
- 혼용률을 아예 제외
- 소재 부위와 혼용률 상태를 명시하고, 명시된 숫자만 ratio로 기록

**결정**
- `materials` 항목에 `part`와 `ratio_status`를 추가한다.
- `ratio_status: "explicit"`일 때만 숫자 `ratio`를 허용하고, `missing` 또는 `ambiguous`일 때는 `ratio: null`로 고정한다.
- 겉감, 안감, 충전재 등 부위가 다르면 `part`로 분리하고, 부위를 확인할 수 없으면 `unknown`으로 둔다.
- 플러그인은 소재 정보의 구조화와 부족·모호 표시만 수행하며, 상품정보 표시 규정의 적법/위법 판정은 하지 않는다.

**근거**
- 소재 혼용률은 소비자 고지와 직접 연결될 수 있는 민감 속성이므로, 입력에 없는 숫자를 추정하면 제출물의 안전성과 신뢰성을 해칠 수 있다.
- 무신사 문제 2의 목표는 에이전트 질의를 위한 구조화이지, 문제 1의 표기 규정 검수가 아니다.

**영향**
- 이후 `SKILL.md`는 소재 혼용률을 추정하지 말고 `ratio_status`와 `quality.missing_fields` 또는 `quality.ambiguous_fields`를 사용하도록 지시해야 한다.
- `validate.py`는 `ratio_status`와 `ratio`의 조건부 정합성, 소재 부위 분리를 검증해야 한다.

**재검토 조건**
- 문제 1 성격의 표기 규정 검수 기능을 도입하게 되면, 별도 규정 기준과 법적 한계 문구를 추가로 설계한다.

---

### D-010 · 단계 간 정합성 검토 게이트 도입
**상황**
- 무신사 문제 2 구현은 S2~S8 단계가 taxonomy/schema, SKILL.md, 스크립트, 검증, README, 제출 패키징으로 이어지는 구조다.
- 사용자가 각 단계가 이전·이후·전체 단계와 충돌하지 않고, 모든 기획 문서의 의도와 방향성이 어긋나지 않도록 검토·검증하는 절차를 필수 지침으로 추가하길 요청했다.

**검토한 선택지**
- 현재 구현 원칙만 유지
- 단계 완료 보고에만 정합성 검토를 추가
- 단계 시작 전과 완료 전 모두 정합성 검토를 필수 게이트로 추가

**결정**
- `AGENTS.md`와 `CLAUDE.md`에 `4.1 단계 간 정합성 검토 게이트`를 신설한다.
- 모든 단계의 시작 전과 완료 전에 이전 단계 산출물, 이후 단계 입력, 전체 단계 목표, 주요 기획 문서와의 충돌 여부를 확인한다.
- 충돌·누락·모호함이 있으면 구현을 계속하지 않고 기준 문서 갱신 또는 사용자 확인을 먼저 수행한다.

**근거**
- 단계 산출물 간 연결이 끊기면 뒤 단계에서 재작업이 커지고, 제출 README·질문 답변·로그와 구현 결과가 어긋날 수 있다.
- 검토 대상을 명시하면 에이전트가 단일 파일 작업에 몰입하다가 전체 제출 방향을 놓치는 위험을 줄일 수 있다.

**영향**
- 이후 모든 단계 완료 보고에는 정합성 검토 결과를 검증 결과에 포함한다.
- 기준 문서의 의도와 구현 산출물이 충돌하면 코드보다 기준 문서와 사용자 확인을 우선한다.

**재검토 조건**
- 검토 절차가 과도하게 무거워 마감 내 진행을 방해하면, 필수 확인 문서 범위를 유지하되 보고 형식만 더 압축한다.

---

### D-009 · 구현 계획 문서 단일화
**상황**
- `AGENTS.md`와 `CLAUDE.md`에는 `docs/musinsa-agentizer-plan.md`를 직접 참조하는 지침이 없었다.
- `docs/musinsa-agentizer-plan.md`와 `docs/implementation-plan.md`는 모두 무신사 문제 2의 구현 단계와 플러그인 구조를 설명해 활성 기준 역할이 중복됐다.

**검토한 선택지**
- 두 계획 문서를 모두 활성 문서로 유지
- `musinsa-agentizer-plan.md`를 기준 문서로 삼고 `implementation-plan.md`를 축소
- `implementation-plan.md`를 단일 활성 구현 계획으로 확장하고 `musinsa-agentizer-plan.md`를 archive로 이동

**결정**
- `docs/implementation-plan.md`를 단일 활성 구현 계획 문서로 사용한다.
- `docs/musinsa-agentizer-plan.md`의 고유 내용은 `docs/implementation-plan.md`에 병합하고, 원본은 `docs/archive/musinsa-agentizer-plan_MERGED.md`로 보관한다.

**근거**
- `implementation-plan.md`는 이미 단계별 실행 순서와 완료 조건을 담는 문서였으므로, 상세 배경과 제출 구조까지 흡수하면 구현자가 한 문서에서 다음 행동을 결정할 수 있다.
- 활성 계획 문서가 둘이면 마감 직전 작업자가 어느 문서를 우선해야 하는지 혼동할 수 있다.

**영향**
- 이후 구현 기준 문서 목록은 `docs/requirements-contract.md`, `docs/implementation-plan.md`, `docs/validation-plan.md`로 단순화한다.
- `docs/archive/musinsa-agentizer-plan_MERGED.md`는 감사 추적용으로만 확인하며 활성 구현 기준으로 사용하지 않는다.

**재검토 조건**
- 무신사 문제 2의 구현 범위가 크게 바뀌어 별도 상세 설계 문서가 다시 필요해지면 새 문서를 만들되, `docs/README.md`에 우선순위와 관계를 명시한다.

---
