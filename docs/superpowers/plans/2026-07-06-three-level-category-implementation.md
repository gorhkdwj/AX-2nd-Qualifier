# Three-Level Category Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the product-agentizer output model from a 2-level `category/subcategory` structure to a 3-level `category/subcategory/detail_type` structure while keeping the MVP scope limited to Musinsa `outer` and `top`.

**Architecture:** Add `detail_type` as a required-but-nullable product field, raise schema/taxonomy versions to `0.2.0`, and nest official Musinsa detail types under their parent subcategories in `taxonomy.json`. Update validation, dedup scoring, evaluation, fixtures, and docs so `detail_type` is treated as a product type signal, while material and season questions continue to use `materials` and `seasons` first.

**Tech Stack:** Codex Skill Markdown, JSON Schema draft 2020-12, Python 3.12, `jsonschema`, deterministic fixture JSON, PowerShell validation commands.

---

## File Structure And Responsibilities

| Path | Responsibility |
|---|---|
| `Decisionlog.md` | Record the accepted design decision before implementation. |
| `Worklog.md` | Record each implementation milestone and verification result. |
| `Troubleshootinglog.md` | Record actual errors encountered during implementation. |
| `src/skills/product-agentizer/references/taxonomy.json` | Source of truth for category, subcategory, detail type, aliases, and parent-child relationships. |
| `src/skills/product-agentizer/references/schema.json` | Output contract for schema-valid structured product JSON. |
| `src/skills/product-agentizer/SKILL.md` | Codex extraction instructions, field priority rules, and completion checklist. |
| `src/skills/product-agentizer/scripts/validate.py` | Deterministic schema and taxonomy relationship validator. |
| `src/skills/product-agentizer/scripts/dedup.py` | Deterministic duplicate-candidate scorer. |
| `tests/evaluate_product_agentizer.py` | Attribute precision/recall and dedup label evaluator. |
| `tools/generate_expanded_validation_fixtures.py` | Reproducible S7.5 fixture generator. |
| `tools/run_expanded_validation.py` | Reproducible validation runner and result snapshot generator. |
| `tests/fixtures/schema/*.json` | Small valid/invalid schema fixtures. |
| `tests/fixtures/evaluation/*.json` | S5 baseline expected/predicted fixture set. |
| `tests/fixtures/dedup/sample_products.json` | Small dedup smoke fixture. |
| `tests/fixtures/expanded_dummy/*.json` | S7.5 synthetic fixtures. |
| `tests/fixtures/codex_subset/*.json` | S7.5 preserved Codex subset fixtures. |
| `tests/fixtures/real_sanity/*.json` | S7.5 real snippet sanity fixtures. |
| `README.md` | Submission-facing summary. |
| `docs/requirements-contract.md` | Current implementation contract. |
| `docs/implementation-plan.md` | Active project implementation roadmap. |
| `docs/validation-plan.md` | Validation strategy and thresholds. |
| `docs/product-agentizer-complete-guide.md` | Detailed technical guide. |
| `docs/reports/s7-expanded-validation-report.md` | Human-readable S7.5 validation report. |
| `docs/reports/s7-expanded-validation-results.json` | Machine-readable S7.5 validation snapshot. |

## Canonical Detail Type Vocabulary

Use these exact ids in schema, taxonomy, fixtures, and docs.

### Top Detail Types

| Official category | `subcategory` | `detail_type` |
|---|---|---|
| 반소매 티셔츠 | `tshirt` | `short_sleeve_tshirt` |
| 셔츠/블라우스 | `shirt_blouse` | `shirt_blouse` |
| 민소매 티셔츠 | `sleeveless` | `sleeveless_tshirt` |
| 피케/카라 티셔츠 | `polo` | `polo_collar_tshirt` |
| 긴소매 티셔츠 | `tshirt` | `long_sleeve_tshirt` |
| 니트/스웨터 | `knit` | `knit_sweater` |
| 기타 상의 | `other_top` | `other_top` |
| 맨투맨/스웨트 | `sweatshirt` | `sweatshirt` |
| 후드 티셔츠 | `hoodie` | `hoodie_tshirt` |

### Outer Detail Types

| Official category | `subcategory` | `detail_type` |
|---|---|---|
| 스타디움 재킷 | `jacket` | `stadium_jacket` |
| 트러커 재킷 | `jacket` | `trucker_jacket` |
| 무스탕/퍼 | `jumper` | `mustang_fur` |
| 기타 아우터 | `other_outer` | `other_outer` |
| 플리스/뽀글이 | `jacket` | `fleece_jacket` |
| 베스트 | `vest` | `vest` |
| 아노락 재킷 | `jacket` | `anorak_jacket` |
| 겨울 기타 코트 | `coat` | `winter_other_coat` |
| 슈트/블레이저 재킷 | `jacket` | `suit_blazer_jacket` |
| 사파리/헌팅 재킷 | `jacket` | `safari_hunting_jacket` |
| 레더/라이더스 재킷 | `jacket` | `leather_rider_jacket` |
| 트레이닝 재킷 | `jacket` | `training_jacket` |
| 숏패딩/헤비 아우터 | `jumper` | `short_padding_heavy_outer` |
| 경량 패딩/패딩 베스트 | `vest` | `lightweight_padding_vest` |
| 나일론/코치 재킷 | `jacket` | `nylon_coach_jacket` |
| 겨울 더블 코트 | `coat` | `winter_double_coat` |
| 겨울 싱글 코트 | `coat` | `winter_single_coat` |
| 롱패딩/헤비 아우터 | `jumper` | `long_padding_heavy_outer` |
| 카디건 | `cardigan` | `cardigan` |
| 후드 집업 | `hoodie_zipup` | `hoodie_zipup` |
| 환절기 코트 | `coat` | `transitional_coat` |
| 블루종/MA-1 | `jacket` | `blouson_ma1` |

---

### Task 1: Record The Design Decision

**Files:**
- Modify: `Decisionlog.md`
- Modify: `Worklog.md`

- [ ] **Step 1: Inspect the latest Decisionlog id**

Run:

```powershell
rg -n "^### D-" Decisionlog.md
```

Expected: the latest id is visible. If the latest id is `D-016`, use `D-017` for this task.

- [ ] **Step 2: Add the 3-level category decision**

Add this entry near the top of `Decisionlog.md`, adjusting the id only if Step 1 shows a later id:

```markdown
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
```

- [ ] **Step 3: Add Worklog entry**

Add this entry near the top of `Worklog.md`:

```markdown
### W-034 · 3단계 상품 분류 구조 구현 착수
**요청**
- 승인된 3단계 상품 분류 구조 설계를 구현 계획에 따라 진행

**수행 작업**
- `Decisionlog.md`에 3단계 구조 도입 결정 기록
- `schema_version=0.2.0`, `taxonomy_version=0.2.0`, `detail_type` nullable 필수 필드 정책을 구현 기준으로 고정

**변경 파일**
- 수정: `Decisionlog.md`
- 수정: `Worklog.md`

**검증**
- 확인: 이후 태스크에서 schema/taxonomy/code/fixture/doc 검증 수행

**판단 근거**
- 실제 무신사 세부 카테고리를 보존하면서도 `subcategory`의 안정성을 유지하기 위해 `detail_type` 계층이 필요하다.

**결과**
- 완료: 3단계 구조 구현 기준 고정 및 다음 태스크 준비
```

- [ ] **Step 4: Verify docs parse as text and commit**

Run:

```powershell
git diff --check
git add Decisionlog.md Worklog.md
git commit -m "docs: record three-level category decision"
```

Expected: `git diff --check` exits 0 and commit succeeds.

---

### Task 2: Update Schema Contract To Version 0.2.0

**Files:**
- Modify: `src/skills/product-agentizer/references/schema.json`
- Test: `python -m json.tool src\skills\product-agentizer\references\schema.json`

- [ ] **Step 1: Add `detail_type` to schema version and required fields**

In `schema.json`, change:

```json
"schema_version": {
  "const": "0.1.0"
}
```

to:

```json
"schema_version": {
  "const": "0.2.0"
}
```

Then add `"detail_type"` immediately after `"subcategory"` in `product.required`:

```json
"required": [
  "title",
  "category",
  "subcategory",
  "detail_type",
  "materials",
  "fit",
  "colors",
  "seasons",
  "tpo_tags",
  "care",
  "size_info"
]
```

- [ ] **Step 2: Expand `subcategory` enum**

Replace the existing `subcategory.enum` list with:

```json
[
  "jacket",
  "jumper",
  "coat",
  "cardigan",
  "vest",
  "hoodie_zipup",
  "other_outer",
  "tshirt",
  "shirt_blouse",
  "knit",
  "sweatshirt",
  "sleeveless",
  "polo",
  "hoodie",
  "other_top",
  null
]
```

- [ ] **Step 3: Add `detail_type` property**

Add this property immediately after `subcategory`:

```json
"detail_type": {
  "type": ["string", "null"],
  "enum": [
    "short_sleeve_tshirt",
    "shirt_blouse",
    "sleeveless_tshirt",
    "polo_collar_tshirt",
    "long_sleeve_tshirt",
    "knit_sweater",
    "other_top",
    "sweatshirt",
    "hoodie_tshirt",
    "stadium_jacket",
    "trucker_jacket",
    "mustang_fur",
    "other_outer",
    "fleece_jacket",
    "vest",
    "anorak_jacket",
    "winter_other_coat",
    "suit_blazer_jacket",
    "safari_hunting_jacket",
    "leather_rider_jacket",
    "training_jacket",
    "short_padding_heavy_outer",
    "lightweight_padding_vest",
    "nylon_coach_jacket",
    "winter_double_coat",
    "winter_single_coat",
    "long_padding_heavy_outer",
    "cardigan",
    "hoodie_zipup",
    "transitional_coat",
    "blouson_ma1",
    null
  ]
}
```

- [ ] **Step 4: Add `detail_type` to quality attribute keys**

In `$defs.attribute_key.enum`, add `"detail_type"` immediately after `"subcategory"`:

```json
"subcategory",
"detail_type",
"materials",
```

- [ ] **Step 5: Validate JSON syntax**

Run:

```powershell
python -m json.tool src\skills\product-agentizer\references\schema.json > $null
```

Expected: command exits 0.

- [ ] **Step 6: Commit schema contract**

Run:

```powershell
git add src\skills\product-agentizer\references\schema.json
git commit -m "feat: add detail_type to product schema"
```

Expected: commit succeeds.

---

### Task 3: Update Taxonomy To Nested Detail Types

**Files:**
- Modify: `src/skills/product-agentizer/references/taxonomy.json`
- Test: `python -m json.tool src\skills\product-agentizer\references\taxonomy.json`

- [ ] **Step 1: Update versions and attribute keys**

Change:

```json
"taxonomy_version": "0.1.0",
"schema_version": "0.1.0",
```

to:

```json
"taxonomy_version": "0.2.0",
"schema_version": "0.2.0",
```

Add `"detail_type"` after `"subcategory"` in `attribute_keys`:

```json
"category",
"subcategory",
"detail_type",
"materials",
```

- [ ] **Step 2: Add normalization rule**

Add this key to `normalization_rules` after the existing category-related rules:

```json
"detail_type": "detail_type은 실제 몰 카테고리와 상품 유형 신호다. 소재 질의에는 materials를 우선하고, 계절 질의에는 seasons를 우선한다. 세부 유형이 불명확하면 null로 두고 quality에 detail_type을 기록한다.",
```

- [ ] **Step 3: Replace `outer.subcategories` with nested detail types**

Use these exact subcategory ids and detail type ids. Keep existing `ko_name`, `description`, and `default_tpo_tags` style.

```json
{
  "id": "jacket",
  "ko_name": "재킷",
  "aliases": ["재킷", "자켓", "블레이저", "블루종", "스타디움 재킷", "트러커 재킷", "아노락 재킷", "슈트/블레이저 재킷", "사파리/헌팅 재킷", "레더/라이더스 재킷", "트레이닝 재킷", "나일론/코치 재킷", "블루종/MA-1", "플리스", "뽀글이"],
  "default_tpo_tags": ["commute", "formal", "guest_look", "layering"],
  "detail_types": [
    {"id": "stadium_jacket", "ko_name": "스타디움 재킷", "aliases": ["스타디움 재킷", "바시티 재킷", "야구 점퍼"]},
    {"id": "trucker_jacket", "ko_name": "트러커 재킷", "aliases": ["트러커 재킷", "데님 재킷"]},
    {"id": "fleece_jacket", "ko_name": "플리스/뽀글이", "aliases": ["플리스", "뽀글이", "플리스 재킷"]},
    {"id": "anorak_jacket", "ko_name": "아노락 재킷", "aliases": ["아노락", "아노락 재킷"]},
    {"id": "suit_blazer_jacket", "ko_name": "슈트/블레이저 재킷", "aliases": ["슈트 재킷", "블레이저", "블레이저 재킷"]},
    {"id": "safari_hunting_jacket", "ko_name": "사파리/헌팅 재킷", "aliases": ["사파리 재킷", "헌팅 재킷"]},
    {"id": "leather_rider_jacket", "ko_name": "레더/라이더스 재킷", "aliases": ["레더 재킷", "라이더스 재킷", "가죽 재킷"]},
    {"id": "training_jacket", "ko_name": "트레이닝 재킷", "aliases": ["트레이닝 재킷", "트랙 재킷"]},
    {"id": "nylon_coach_jacket", "ko_name": "나일론/코치 재킷", "aliases": ["나일론 재킷", "코치 재킷"]},
    {"id": "blouson_ma1", "ko_name": "블루종/MA-1", "aliases": ["블루종", "MA-1", "항공 점퍼"]}
  ]
}
```

Add the remaining outer subcategories with these detail types:

```json
{
  "id": "jumper",
  "detail_types": [
    {"id": "mustang_fur", "ko_name": "무스탕/퍼", "aliases": ["무스탕", "퍼 재킷", "퍼 아우터"]},
    {"id": "short_padding_heavy_outer", "ko_name": "숏패딩/헤비 아우터", "aliases": ["숏패딩", "헤비 아우터"]},
    {"id": "long_padding_heavy_outer", "ko_name": "롱패딩/헤비 아우터", "aliases": ["롱패딩", "롱 헤비 아우터"]}
  ]
}
```

```json
{
  "id": "coat",
  "detail_types": [
    {"id": "winter_other_coat", "ko_name": "겨울 기타 코트", "aliases": ["겨울 기타 코트", "겨울 코트"]},
    {"id": "winter_double_coat", "ko_name": "겨울 더블 코트", "aliases": ["겨울 더블 코트", "더블 코트"]},
    {"id": "winter_single_coat", "ko_name": "겨울 싱글 코트", "aliases": ["겨울 싱글 코트", "싱글 코트"]},
    {"id": "transitional_coat", "ko_name": "환절기 코트", "aliases": ["환절기 코트", "트렌치코트", "맥코트"]}
  ]
}
```

```json
{
  "id": "cardigan",
  "detail_types": [
    {"id": "cardigan", "ko_name": "카디건", "aliases": ["카디건", "가디건", "니트 가디건", "집업 가디건"]}
  ]
}
```

```json
{
  "id": "vest",
  "detail_types": [
    {"id": "vest", "ko_name": "베스트", "aliases": ["베스트", "조끼"]},
    {"id": "lightweight_padding_vest", "ko_name": "경량 패딩/패딩 베스트", "aliases": ["경량 패딩", "패딩 베스트", "경량 패딩 베스트"]}
  ]
}
```

```json
{
  "id": "hoodie_zipup",
  "detail_types": [
    {"id": "hoodie_zipup", "ko_name": "후드 집업", "aliases": ["후드 집업", "후디 집업", "집업 후드"]}
  ]
}
```

```json
{
  "id": "other_outer",
  "ko_name": "기타 아우터",
  "aliases": ["기타 아우터", "기타 외투"],
  "default_tpo_tags": ["daily", "casual"],
  "detail_types": [
    {"id": "other_outer", "ko_name": "기타 아우터", "aliases": ["기타 아우터", "기타 외투"]}
  ]
}
```

- [ ] **Step 4: Replace `top.subcategories` with nested detail types**

Add detail types to the existing top subcategories and add `hoodie` and `other_top`:

```json
{
  "id": "tshirt",
  "ko_name": "티셔츠",
  "aliases": ["티셔츠", "반팔 티", "긴팔 티", "롱슬리브", "그래픽 티", "반소매 티셔츠", "긴소매 티셔츠"],
  "default_tpo_tags": ["daily", "casual", "street"],
  "detail_types": [
    {"id": "short_sleeve_tshirt", "ko_name": "반소매 티셔츠", "aliases": ["반소매 티셔츠", "반팔 티", "반팔 티셔츠"]},
    {"id": "long_sleeve_tshirt", "ko_name": "긴소매 티셔츠", "aliases": ["긴소매 티셔츠", "긴팔 티", "롱슬리브"]}
  ]
}
```

Use one detail type for each remaining top parent:

```json
{"id": "shirt_blouse", "detail_types": [{"id": "shirt_blouse", "ko_name": "셔츠/블라우스", "aliases": ["셔츠", "블라우스", "셔츠/블라우스"]}]}
{"id": "sleeveless", "detail_types": [{"id": "sleeveless_tshirt", "ko_name": "민소매 티셔츠", "aliases": ["민소매", "민소매 티셔츠", "나시", "탱크톱"]}]}
{"id": "polo", "detail_types": [{"id": "polo_collar_tshirt", "ko_name": "피케/카라 티셔츠", "aliases": ["피케", "카라 티", "피케 셔츠", "피케/카라 티셔츠"]}]}
{"id": "knit", "detail_types": [{"id": "knit_sweater", "ko_name": "니트/스웨터", "aliases": ["니트", "스웨터", "니트/스웨터"]}]}
{"id": "sweatshirt", "detail_types": [{"id": "sweatshirt", "ko_name": "맨투맨/스웨트", "aliases": ["맨투맨", "스웨트셔츠", "맨투맨/스웨트"]}]}
{"id": "hoodie", "ko_name": "후드 티셔츠", "aliases": ["후드 티셔츠", "후디", "후드티"], "default_tpo_tags": ["daily", "casual", "street"], "detail_types": [{"id": "hoodie_tshirt", "ko_name": "후드 티셔츠", "aliases": ["후드 티셔츠", "후디", "후드티"]}]}
{"id": "other_top", "ko_name": "기타 상의", "aliases": ["기타 상의"], "default_tpo_tags": ["daily", "casual"], "detail_types": [{"id": "other_top", "ko_name": "기타 상의", "aliases": ["기타 상의"]}]}
```

- [ ] **Step 5: Validate taxonomy JSON**

Run:

```powershell
python -m json.tool src\skills\product-agentizer\references\taxonomy.json > $null
```

Expected: command exits 0.

- [ ] **Step 6: Commit taxonomy**

Run:

```powershell
git add src\skills\product-agentizer\references\taxonomy.json
git commit -m "feat: add nested detail type taxonomy"
```

Expected: commit succeeds.

---

### Task 4: Add Detail Type Validation Fixtures

**Files:**
- Modify: `tests/fixtures/schema/valid_outer.json`
- Modify: `tests/fixtures/schema/valid_top.json`
- Create: `tests/fixtures/schema/invalid_missing_detail_type.json`
- Create: `tests/fixtures/schema/invalid_unknown_detail_type.json`
- Create: `tests/fixtures/schema/invalid_detail_type_parent.json`

- [ ] **Step 1: Update valid schema fixtures**

In `valid_outer.json`, set:

```json
"schema_version": "0.2.0"
```

and add:

```json
"detail_type": "trucker_jacket"
```

after `"subcategory": "jacket"`.

In `valid_top.json`, set:

```json
"schema_version": "0.2.0"
```

and add:

```json
"detail_type": "short_sleeve_tshirt"
```

after `"subcategory": "tshirt"`.

- [ ] **Step 2: Create missing detail type invalid fixture**

Create `tests/fixtures/schema/invalid_missing_detail_type.json` by copying `valid_outer.json` after Step 1 and removing only the `detail_type` line.

- [ ] **Step 3: Create unknown detail type invalid fixture**

Create `tests/fixtures/schema/invalid_unknown_detail_type.json` by copying `valid_outer.json` after Step 1 and changing:

```json
"detail_type": "trucker_jacket"
```

to:

```json
"detail_type": "unknown_detail_type"
```

- [ ] **Step 4: Create parent mismatch invalid fixture**

Create `tests/fixtures/schema/invalid_detail_type_parent.json` by copying `valid_top.json` after Step 1 and changing:

```json
"detail_type": "short_sleeve_tshirt"
```

to:

```json
"detail_type": "trucker_jacket"
```

This fixture should pass JSON Schema enum validation but fail `validate.py` custom taxonomy relationship validation after Task 5.

- [ ] **Step 5: Commit fixture additions**

Run:

```powershell
git add tests\fixtures\schema
git commit -m "test: add detail type schema fixtures"
```

Expected: commit succeeds.

---

### Task 5: Add Parent-Child Validation To `validate.py`

**Files:**
- Modify: `src/skills/product-agentizer/scripts/validate.py`
- Test: `tests/fixtures/schema/*.json`

- [ ] **Step 1: Extend taxonomy sets**

Update `taxonomy_sets()` so it returns parent-child maps. Use this complete function body:

```python
def taxonomy_sets(taxonomy: dict[str, Any]) -> dict[str, Any]:
    vocabularies = taxonomy.get("vocabularies", {})
    categories = taxonomy.get("categories", {})
    subcategories: set[str] = set()
    detail_types: set[str] = set()
    category_by_subcategory: dict[str, str] = {}
    parent_by_detail_type: dict[str, tuple[str, str]] = {}

    for category_id, category in categories.items():
        for subcategory in category.get("subcategories", []):
            subcategory_id = subcategory.get("id")
            if not subcategory_id:
                continue
            subcategories.add(subcategory_id)
            category_by_subcategory[subcategory_id] = category_id
            for detail_type in subcategory.get("detail_types", []):
                detail_type_id = detail_type.get("id")
                if not detail_type_id:
                    continue
                detail_types.add(detail_type_id)
                parent_by_detail_type[detail_type_id] = (category_id, subcategory_id)

    return {
        "attribute_keys": set(taxonomy.get("attribute_keys", [])),
        "categories": set(taxonomy.get("scope", {}).get("supported_categories", [])),
        "subcategories": subcategories,
        "detail_types": detail_types,
        "category_by_subcategory": category_by_subcategory,
        "parent_by_detail_type": parent_by_detail_type,
        "materials": {item.get("id") for item in vocabularies.get("materials", [])},
        "material_parts": {item.get("id") for item in vocabularies.get("material_parts", [])},
        "ratio_statuses": {item.get("id") for item in vocabularies.get("ratio_statuses", [])},
        "fits": {item.get("id") for item in vocabularies.get("fits", [])},
        "colors": {item.get("id") for item in vocabularies.get("colors", [])},
        "seasons": {item.get("id") for item in vocabularies.get("seasons", [])},
        "tpo_tags": {item.get("id") for item in vocabularies.get("tpo_tags", [])},
        "care": {item.get("id") for item in vocabularies.get("care", [])},
    }
```

- [ ] **Step 2: Add relationship checks**

In `custom_checks()`, after the existing category check, add:

```python
    category = structured.get("category")
    subcategory = structured.get("subcategory")
    detail_type = structured.get("detail_type")

    if subcategory and subcategory not in tax["subcategories"]:
        errors.append(
            {
                "product_id": product_id,
                "path": "product.subcategory",
                "message": "unknown subcategory",
            }
        )

    expected_category = tax["category_by_subcategory"].get(subcategory)
    if subcategory and expected_category and category != expected_category:
        errors.append(
            {
                "product_id": product_id,
                "path": "product.subcategory",
                "message": "subcategory must belong to the selected category",
            }
        )

    if detail_type is not None:
        if detail_type not in tax["detail_types"]:
            errors.append(
                {
                    "product_id": product_id,
                    "path": "product.detail_type",
                    "message": "unknown detail_type",
                }
            )
        else:
            expected_parent = tax["parent_by_detail_type"].get(detail_type)
            if expected_parent and expected_parent != (category, subcategory):
                errors.append(
                    {
                        "product_id": product_id,
                        "path": "product.detail_type",
                        "message": "detail_type must belong to the selected category/subcategory",
                    }
                )
```

- [ ] **Step 3: Run valid fixture checks**

Run:

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
```

Expected: both commands exit 0 and output `"valid": true`.

- [ ] **Step 4: Run invalid fixture checks**

Run:

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_missing_detail_type.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_unknown_detail_type.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_detail_type_parent.json --pretty
```

Expected: each command exits 1 and output contains `"valid": false`.

- [ ] **Step 5: Commit validator update**

Run:

```powershell
git add src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema
git commit -m "feat: validate detail type hierarchy"
```

Expected: commit succeeds.

---

### Task 6: Add `detail_type` To Evaluator

**Files:**
- Modify: `tests/evaluate_product_agentizer.py`

- [ ] **Step 1: Add field to evaluated fields**

Change:

```python
EVALUATED_FIELDS = [
    "title",
    "category",
    "subcategory",
    "materials",
```

to:

```python
EVALUATED_FIELDS = [
    "title",
    "category",
    "subcategory",
    "detail_type",
    "materials",
```

- [ ] **Step 2: Treat detail type as scalar field**

Change:

```python
if field in {"title", "category", "subcategory"}:
```

to:

```python
if field in {"title", "category", "subcategory", "detail_type"}:
```

- [ ] **Step 3: Compile evaluator**

Run:

```powershell
python -m py_compile tests\evaluate_product_agentizer.py
```

Expected: command exits 0.

- [ ] **Step 4: Commit evaluator update**

Run:

```powershell
git add tests\evaluate_product_agentizer.py
git commit -m "test: evaluate detail_type extraction"
```

Expected: commit succeeds.

---

### Task 7: Add `detail_type` To Dedup Scoring

**Files:**
- Modify: `src/skills/product-agentizer/scripts/dedup.py`
- Test: `tests/fixtures/dedup/sample_products.json`

- [ ] **Step 1: Add scalar value helper**

Add this helper after `values()`:

```python
def scalar_value(product: dict[str, Any], field: str) -> str | None:
    raw = product.get("product", {}).get(field)
    if raw is None:
        return None
    text = str(raw).strip()
    return text or None
```

- [ ] **Step 2: Update score weights**

In `score_pair()`, change category and subcategory weights:

```python
    if left_product.get("category") and left_product.get("category") == right_product.get("category"):
        score += 0.16
        matched.append("category")
    if left_product.get("subcategory") and left_product.get("subcategory") == right_product.get("subcategory"):
        score += 0.14
        matched.append("subcategory")
```

Add detail type comparison immediately after subcategory:

```python
    left_detail_type = scalar_value(left["structured"], "detail_type")
    right_detail_type = scalar_value(right["structured"], "detail_type")
    if left_detail_type and left_detail_type == right_detail_type:
        score += 0.08
        matched.append("detail_type")
```

- [ ] **Step 3: Update weighted set values**

Replace `weighted_sets` with:

```python
    weighted_sets = [
        ("materials", material_values(left["structured"]), material_values(right["structured"]), 0.18),
        ("colors", values(left["structured"], "colors"), values(right["structured"], "colors"), 0.11),
        ("fit", values(left["structured"], "fit"), values(right["structured"], "fit"), 0.09),
        ("seasons", values(left["structured"], "seasons"), values(right["structured"], "seasons"), 0.07),
        ("tpo_tags", values(left["structured"], "tpo_tags"), values(right["structured"], "tpo_tags"), 0.07),
        ("care", values(left["structured"], "care"), values(right["structured"], "care"), 0.04),
    ]
```

Change title contribution from `0.14` to `0.06`:

```python
    if title_similarity > 0:
        score += 0.06 * title_similarity
```

- [ ] **Step 4: Compile dedup script**

Run:

```powershell
python -m py_compile src\skills\product-agentizer\scripts\dedup.py
```

Expected: command exits 0.

- [ ] **Step 5: Commit dedup update**

Run:

```powershell
git add src\skills\product-agentizer\scripts\dedup.py
git commit -m "feat: include detail_type in dedup scoring"
```

Expected: commit succeeds.

---

### Task 8: Update Skill Instructions

**Files:**
- Modify: `src/skills/product-agentizer/SKILL.md`

- [ ] **Step 1: Add detail type to reference file description**

Change the taxonomy reference bullet to include detail type:

```markdown
- `references/taxonomy.json`: 지원 카테고리, 서브카테고리, detail_type, 별칭, vocabulary id, 소재 부위, 혼용률 상태 값
```

- [ ] **Step 2: Add detail type to extraction list**

In the extraction list, add `detail_type` after `subcategory`:

```markdown
   - `subcategory`
   - `detail_type`
   - `materials`
```

- [ ] **Step 3: Add classification procedure**

Add this paragraph after category judgment instructions:

```markdown
   - `subcategory`는 안정적인 상품 형태를 나타냅니다.
   - `detail_type`은 실제 몰 세부 카테고리나 상품명에 나타난 세부 유형을 나타냅니다.
   - 세부 유형이 명확하면 taxonomy의 `detail_types` id를 사용합니다.
   - 세부 유형이 불명확하면 `detail_type: null`로 두고 `quality.missing_fields` 또는 `quality.ambiguous_fields`에 `detail_type`을 기록합니다.
```

- [ ] **Step 4: Add field priority rules**

Add this section before `agent_descriptor` instructions:

```markdown
### 필드 우선순위

- 상품 유형 질의에는 `category`, `subcategory`, `detail_type`을 우선 사용합니다.
- 소재 질의에는 `materials.name`, `materials.ratio_status`, `materials.evidence`를 우선 사용합니다.
- 계절 질의에는 `seasons`를 우선 사용합니다.
- `detail_type` 안에 소재나 계절 단어가 포함되어도, 해당 구조화 속성 필드와 충돌하면 `materials` 또는 `seasons`를 우선합니다.
- `detail_type`만으로 천연소재 여부, 보온성, 법적 표기 적합성을 단정하지 않습니다.
```

- [ ] **Step 5: Update completion checklist**

Add:

```markdown
- `detail_type`이 null이 아니면 선택한 category/subcategory 아래에 존재하는 taxonomy id입니다.
```

- [ ] **Step 6: Commit skill update**

Run:

```powershell
git add src\skills\product-agentizer\SKILL.md
git commit -m "docs: instruct detail_type extraction"
```

Expected: commit succeeds.

---

### Task 9: Update Fixture Generator

**Files:**
- Modify: `tools/generate_expanded_validation_fixtures.py`

- [ ] **Step 1: Add detail type constants**

Add these constants after `TOP_SUBCATEGORIES`:

```python
OUTER_DETAIL_TYPES = {
    "jacket": ["stadium_jacket", "trucker_jacket", "fleece_jacket", "anorak_jacket", "suit_blazer_jacket", "safari_hunting_jacket", "leather_rider_jacket", "training_jacket", "nylon_coach_jacket", "blouson_ma1"],
    "jumper": ["mustang_fur", "short_padding_heavy_outer", "long_padding_heavy_outer"],
    "coat": ["winter_other_coat", "winter_double_coat", "winter_single_coat", "transitional_coat"],
    "cardigan": ["cardigan"],
    "vest": ["vest", "lightweight_padding_vest"],
    "hoodie_zipup": ["hoodie_zipup"],
    "other_outer": ["other_outer"],
}

TOP_DETAIL_TYPES = {
    "tshirt": ["short_sleeve_tshirt", "long_sleeve_tshirt"],
    "shirt_blouse": ["shirt_blouse"],
    "knit": ["knit_sweater"],
    "sweatshirt": ["sweatshirt"],
    "sleeveless": ["sleeveless_tshirt"],
    "polo": ["polo_collar_tshirt"],
    "hoodie": ["hoodie_tshirt"],
    "other_top": ["other_top"],
}
```

- [ ] **Step 2: Add Korean labels**

Add `KO_DETAIL_TYPE` after `KO_SUBCATEGORY`:

```python
KO_DETAIL_TYPE = {
    "short_sleeve_tshirt": "반소매 티셔츠",
    "shirt_blouse": "셔츠/블라우스",
    "sleeveless_tshirt": "민소매 티셔츠",
    "polo_collar_tshirt": "피케/카라 티셔츠",
    "long_sleeve_tshirt": "긴소매 티셔츠",
    "knit_sweater": "니트/스웨터",
    "other_top": "기타 상의",
    "sweatshirt": "맨투맨/스웨트",
    "hoodie_tshirt": "후드 티셔츠",
    "stadium_jacket": "스타디움 재킷",
    "trucker_jacket": "트러커 재킷",
    "mustang_fur": "무스탕/퍼",
    "other_outer": "기타 아우터",
    "fleece_jacket": "플리스/뽀글이",
    "vest": "베스트",
    "anorak_jacket": "아노락 재킷",
    "winter_other_coat": "겨울 기타 코트",
    "suit_blazer_jacket": "슈트/블레이저 재킷",
    "safari_hunting_jacket": "사파리/헌팅 재킷",
    "leather_rider_jacket": "레더/라이더스 재킷",
    "training_jacket": "트레이닝 재킷",
    "short_padding_heavy_outer": "숏패딩/헤비 아우터",
    "lightweight_padding_vest": "경량 패딩/패딩 베스트",
    "nylon_coach_jacket": "나일론/코치 재킷",
    "winter_double_coat": "겨울 더블 코트",
    "winter_single_coat": "겨울 싱글 코트",
    "long_padding_heavy_outer": "롱패딩/헤비 아우터",
    "cardigan": "카디건",
    "hoodie_zipup": "후드 집업",
    "transitional_coat": "환절기 코트",
    "blouson_ma1": "블루종/MA-1",
}
```

- [ ] **Step 3: Add detail_type parameter to `structured_product()`**

Add `detail_type: str | None,` after `subcategory: str,` in the function signature.

Add this property after `subcategory`:

```python
"detail_type": detail_type,
```

Update `search_summary` and `query_tags` to include detail type:

```python
"search_summary": f"{KO_COLOR[color]} {KO_FIT[fit]} {KO_DETAIL_TYPE[detail_type] if detail_type else KO_SUBCATEGORY[subcategory]}",
"query_tags": [
    f"{KO_COLOR[color]} {KO_DETAIL_TYPE[detail_type] if detail_type else KO_SUBCATEGORY[subcategory]}",
    f"{KO_FIT[fit]} 상품",
],
```

- [ ] **Step 4: Generate detail type in `make_dummy_case()`**

After selecting `subcategory`, add:

```python
    detail_types = OUTER_DETAIL_TYPES if category == "outer" else TOP_DETAIL_TYPES
    detail_type_options = detail_types[subcategory]
    detail_type = detail_type_options[index % len(detail_type_options)]
```

Update title:

```python
    title = f"{KO_COLOR[color]} {KO_FIT[fit]} {KO_DETAIL_TYPE[detail_type]} {index:03d}"
```

Update text to include product category detail:

```python
        f"상품명: {title}. 제품분류: {KO_SUBCATEGORY[subcategory]} > {KO_DETAIL_TYPE[detail_type]}. 컬러: {KO_COLOR[color]}. {material_text}. "
```

Pass `detail_type` to `structured_product()`.

- [ ] **Step 5: Update real sanity specs**

For every real sanity product tuple, add `detail_type` immediately after `subcategory`. Use:

```text
real_outer_beanpole_linen_jacket_4308999 -> suit_blazer_jacket
real_outer_limelike_cardigan_2101205 -> cardigan
real_outer_8seconds_jacket_4922894 -> suit_blazer_jacket
real_outer_247_cashmere_blouson_3617977 -> blouson_ma1
real_outer_lenina_cardigan_4332165 -> cardigan
real_top_armedes_tee_4783312 -> short_sleeve_tshirt
real_top_ms_linen_like_shirt_black_3054408 -> shirt_blouse
real_top_ms_basic_tee_3661999 -> short_sleeve_tshirt
real_top_ms_linen_like_shirt_navy_3054409 -> shirt_blouse
real_top_ms_basic_short_tee_1196892 -> short_sleeve_tshirt
```

Update the loop unpacking accordingly:

```python
for product_id, title, category, subcategory, detail_type, color, fit, material_rows, seasons, tpo, care, size_info, missing, ambiguous in specs:
```

Pass `detail_type` to `structured_product()`.

- [ ] **Step 6: Compile generator**

Run:

```powershell
python -m py_compile tools\generate_expanded_validation_fixtures.py
```

Expected: command exits 0.

- [ ] **Step 7: Commit generator update**

Run:

```powershell
git add tools\generate_expanded_validation_fixtures.py
git commit -m "test: generate detail_type validation fixtures"
```

Expected: commit succeeds.

---

### Task 10: Regenerate And Backfill Fixtures

**Files:**
- Modify: `tests/fixtures/expanded_dummy/*`
- Modify: `tests/fixtures/codex_subset/*`
- Modify: `tests/fixtures/real_sanity/*`
- Modify: `tests/fixtures/evaluation/*`
- Modify: `tests/fixtures/dedup/sample_products.json`

- [ ] **Step 1: Regenerate generated fixtures**

Run:

```powershell
python tools\generate_expanded_validation_fixtures.py
```

Expected: command exits 0 and generated JSON files now contain `schema_version: "0.2.0"` and `product.detail_type`.

- [ ] **Step 2: Backfill preserved actual JSON files**

For these files, add `schema_version: "0.2.0"` and the matching `product.detail_type` based on the product id and expected fixture:

```text
tests/fixtures/codex_subset/actual_products.json
tests/fixtures/real_sanity/actual_products.json
```

Use this PowerShell sanity check after editing:

```powershell
Select-String -Path tests\fixtures\codex_subset\actual_products.json,tests\fixtures\real_sanity\actual_products.json -Pattern '"detail_type"'
```

Expected: each product object has one `detail_type` field.

- [ ] **Step 3: Update baseline evaluation fixtures**

Edit:

```text
tests/fixtures/evaluation/expected_products.json
tests/fixtures/evaluation/predicted_products.json
tests/fixtures/evaluation/source_inputs.json
```

Apply these known mappings:

```text
outer_linen_blazer_a -> suit_blazer_jacket
outer_linen_blazer_b -> suit_blazer_jacket
outer_down_vest -> lightweight_padding_vest
top_linen_blouse -> shirt_blouse
top_washable_tee -> short_sleeve_tshirt
```

Every structured product must have:

```json
"schema_version": "0.2.0"
```

and:

```json
"detail_type": "<mapped value>"
```

- [ ] **Step 4: Update dedup sample fixture**

Edit `tests/fixtures/dedup/sample_products.json` so every product uses `schema_version: "0.2.0"` and includes `detail_type`.

Use:

```text
outer_a -> suit_blazer_jacket
outer_b -> suit_blazer_jacket
top_a -> short_sleeve_tshirt
```

- [ ] **Step 5: Validate all fixture JSON syntax**

Run:

```powershell
python -m json.tool tests\fixtures\evaluation\expected_products.json > $null
python -m json.tool tests\fixtures\evaluation\predicted_products.json > $null
python -m json.tool tests\fixtures\dedup\sample_products.json > $null
python -m json.tool tests\fixtures\codex_subset\actual_products.json > $null
python -m json.tool tests\fixtures\real_sanity\actual_products.json > $null
```

Expected: all commands exit 0.

- [ ] **Step 6: Commit fixture migration**

Run:

```powershell
git add tests\fixtures
git commit -m "test: migrate fixtures to detail_type schema"
```

Expected: commit succeeds.

---

### Task 11: Run Core Validation Suite

**Files:**
- No source edits expected.
- Validate: scripts and fixtures.

- [ ] **Step 1: Compile Python scripts**

Run:

```powershell
python -m py_compile src\skills\product-agentizer\scripts\validate.py
python -m py_compile src\skills\product-agentizer\scripts\dedup.py
python -m py_compile tests\evaluate_product_agentizer.py
python -m py_compile tools\generate_expanded_validation_fixtures.py
python -m py_compile tools\run_expanded_validation.py
```

Expected: all commands exit 0.

- [ ] **Step 2: Validate schema fixtures**

Run:

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_outer.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\valid_top.json --pretty
```

Expected: both exit 0.

- [ ] **Step 3: Validate invalid fixtures fail**

Run each command and confirm exit code 1:

```powershell
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_missing_detail_type.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_unknown_detail_type.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_detail_type_parent.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_missing_quality.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_out_of_scope_category.json --pretty
python src\skills\product-agentizer\scripts\validate.py tests\fixtures\schema\invalid_material_ratio_status.json --pretty
```

Expected: each command outputs `"valid": false`.

- [ ] **Step 4: Run baseline evaluator**

Run:

```powershell
python tests\evaluate_product_agentizer.py --pretty
```

Expected: command exits 0, expected and actual fixtures are schema-valid, and dedup accuracy remains 100%.

- [ ] **Step 5: Commit validation checkpoint if fixes were needed**

If Steps 1-4 required code or fixture fixes, commit them:

```powershell
git add src tests tools
git commit -m "fix: stabilize detail_type validation"
```

Expected: commit succeeds only if files changed. If no files changed, skip this step.

---

### Task 12: Run Expanded Validation And Update Reports

**Files:**
- Modify: `docs/reports/s7-expanded-validation-results.json`
- Modify: `docs/reports/s7-expanded-validation-report.md`

- [ ] **Step 1: Run expanded validation**

Run:

```powershell
python tools\run_expanded_validation.py
```

Expected: output contains:

```json
{"all_commands_passed": true}
```

- [ ] **Step 2: Extract headline metrics**

Run:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new();
$r = Get-Content -LiteralPath 'docs\reports\s7-expanded-validation-results.json' -Encoding UTF8 | ConvertFrom-Json
$r.acceptance_summary | ConvertTo-Json -Depth 5
$r.dedup_cross_category_check | ConvertTo-Json -Depth 5
```

Expected:

```text
expanded_expected_schema_valid: true
codex_subset_schema_valid: true
real_sanity_schema_valid: true
all_commands_passed: true
high_confidence_cross_category_count: 0
```

- [ ] **Step 3: Update S7 report text**

In `docs/reports/s7-expanded-validation-report.md`, update:

- schema version references to `0.2.0`
- the generated timestamp from `s7-expanded-validation-results.json`
- the fact that `detail_type` is now evaluated
- changed precision/recall metrics
- changed dedup metrics
- note that dedup weights remain heuristic baseline values requiring operating-data tuning

Use this sentence in the report:

```markdown
`detail_type` 추가 후 dedup 가중치와 임계값은 여전히 운영 데이터로 학습된 최종값이 아니라 설명 가능한 휴리스틱 baseline이며, 실제 운영 적용 시 라벨링된 상품쌍으로 precision/recall과 오탐·미탐을 비교해 조정해야 한다.
```

- [ ] **Step 4: Commit expanded validation snapshot**

Run:

```powershell
git add docs\reports\s7-expanded-validation-results.json docs\reports\s7-expanded-validation-report.md
git commit -m "test: refresh expanded validation for detail_type"
```

Expected: commit succeeds.

---

### Task 13: Update User-Facing And Project Docs

**Files:**
- Modify: `README.md`
- Modify: `docs/requirements-contract.md`
- Modify: `docs/implementation-plan.md`
- Modify: `docs/validation-plan.md`
- Modify: `docs/product-agentizer-complete-guide.md`
- Modify: `docs/submission-questions.md`

- [ ] **Step 1: Update README feature summary**

In `README.md`, add `detail_type` to the feature list:

```markdown
1. 상품 상세 텍스트에서 상품명, 카테고리, 서브카테고리, 세부 유형(detail_type), 소재, 핏, 색상, 계절, TPO, 관리, 사이즈 정보를 추출합니다.
```

Add this clarification near the dedup description:

```markdown
`dedup.py`의 가중치와 임계값은 실제 운영 데이터로 학습된 값이 아니라 설명 가능한 휴리스틱 baseline입니다. 운영 적용 시에는 라벨링된 상품쌍으로 precision/recall과 오탐·미탐을 비교해 재튜닝해야 합니다.
```

- [ ] **Step 2: Update requirements contract**

In `docs/requirements-contract.md`, add `detail_type` after `subcategory` in the output JSON example:

```json
"subcategory": "선택",
"detail_type": "선택: 공식 몰 세부 유형 또는 null",
```

Update schema version mentions to `0.2.0`.

- [ ] **Step 3: Update implementation plan**

In `docs/implementation-plan.md`, add a new row after S7.5:

```markdown
| S7.6 | 3단계 분류 구조 개편 | `category/subcategory/detail_type` 구조 반영, schema/taxonomy 0.2.0 갱신 | schema/parent-child/dedup/evaluator/S7.5 재검증 | S7.5 |
```

- [ ] **Step 4: Update validation plan**

In `docs/validation-plan.md`, add:

```markdown
- 3단계 분류 검증: `detail_type`이 schema enum에 존재하고 선택된 `category/subcategory` 아래에 속하는지 `validate.py` custom check로 확인한다.
```

- [ ] **Step 5: Update complete guide**

In `docs/product-agentizer-complete-guide.md`, replace 2-level examples with 3-level examples. Use this canonical example:

```json
{
  "category": "outer",
  "subcategory": "jacket",
  "detail_type": "trucker_jacket"
}
```

Keep the existing warning that material questions must use `materials`, not `detail_type` alone.

- [ ] **Step 6: Update submission questions if needed**

In `docs/submission-questions.md`, mention `detail_type` in the answer about how the plugin works:

```markdown
분류는 `category/subcategory/detail_type` 3단계로 나누어, 큰 상품군과 안정적인 형태, 실제 몰 세부 유형을 분리합니다.
```

- [ ] **Step 7: Commit docs**

Run:

```powershell
git add README.md docs\requirements-contract.md docs\implementation-plan.md docs\validation-plan.md docs\product-agentizer-complete-guide.md docs\submission-questions.md
git commit -m "docs: document detail_type product model"
```

Expected: commit succeeds.

---

### Task 14: Final Verification And Push

**Files:**
- Modify: `Worklog.md`
- Modify: `Troubleshootinglog.md` only if actual implementation errors occurred.

- [ ] **Step 1: Add final Worklog entry**

Add a `Worklog.md` entry summarizing:

```markdown
### W-035 · 3단계 상품 분류 구조 구현 완료
**요청**
- 3단계 `category/subcategory/detail_type` 구조 구현

**수행 작업**
- schema/taxonomy 0.2.0 갱신
- `detail_type` 추출 지침, validator parent-child 검증, dedup 보조 가중치, evaluator 필드, fixtures, S7.5 검증, 문서 반영

**검증**
- `python tools\run_expanded_validation.py`
- `python tests\evaluate_product_agentizer.py --pretty`
- `git diff --check`
- 비밀정보 고위험 패턴 검색 0건

**결과**
- 완료: 3단계 상품 분류 구조 구현 및 재검증 완료
```

- [ ] **Step 2: Run final code and JSON checks**

Run:

```powershell
python -m json.tool src\skills\product-agentizer\references\schema.json > $null
python -m json.tool src\skills\product-agentizer\references\taxonomy.json > $null
python -m py_compile src\skills\product-agentizer\scripts\validate.py
python -m py_compile src\skills\product-agentizer\scripts\dedup.py
python -m py_compile tests\evaluate_product_agentizer.py
python -m py_compile tools\generate_expanded_validation_fixtures.py
python -m py_compile tools\run_expanded_validation.py
python tests\evaluate_product_agentizer.py --pretty
python tools\run_expanded_validation.py
git diff --check
```

Expected: all commands pass.

- [ ] **Step 3: Run secret pattern scan**

Run:

```powershell
rg -n "sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{20,}|AKIA[0-9A-Z]{16}" -g '!logs/**' -g '!out/**' .
```

Expected: no matches and exit code 1.

- [ ] **Step 4: Commit final logs**

Run:

```powershell
git add Worklog.md Troubleshootinglog.md
git commit -m "docs: record detail_type implementation"
```

Expected: commit succeeds if either file changed. If `Troubleshootinglog.md` did not change, commit only `Worklog.md`.

- [ ] **Step 5: Push and confirm clean status**

Run:

```powershell
git push
git status --short --ignored
```

Expected: push succeeds. `git status --short --ignored` shows only ignored `.claude/settings.local.json`, `logs/`, and `out/`.

---

## Self-Review

- Spec coverage: The plan covers decision logging, schema, taxonomy, Skill, validator, dedup, evaluator, fixtures, expanded validation, docs, and final push.
- Placeholder scan: No incomplete placeholders are used as work instructions.
- Type consistency: The plan consistently uses `detail_type` as `string | null`, schema/taxonomy version `0.2.0`, and `category/subcategory/detail_type` parent-child validation.
- Scope check: The implementation scope is limited to `outer` and `top`; future categories are supported by structure, not implemented now.
- Dedup caveat: The plan preserves the documented principle that dedup weights and thresholds are heuristic baseline values requiring operating-data tuning before real production use.
