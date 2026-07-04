---
name: product-agentizer
description: Convert pasted Korean fashion product detail text into schema-valid, agent-query-ready structured product JSON for the Musinsa outer/top MVP. Use for taxonomy mapping, missing/ambiguous field reporting, material-ratio evidence handling, and duplicate-candidate preparation; do not use for legal label-compliance audits, automatic URL fetching/crawling, recommendation ranking, or private/internal data.
---

# Product Agentizer

Convert user-pasted fashion product detail text into structured product JSON that an AI agent can query, filter, and explain.

## Scope

Use this skill when the user provides or asks to transform fashion product detail text into structured product data for the Musinsa product agentizer MVP.

Supported categories:
- `outer`
- `top`

Do not use this skill for:
- product information label compliance audits or legal pass/fail judgments
- automatic URL fetching, scraping, crawling, or bulk data collection
- private, logged-in, internal, customer, order, sales, or catalog data
- recommendation ranking, pricing, inventory, or trend prediction
- categories outside the MVP such as bottom, dress, shoes, bag, beauty, kids, or accessory, except to mark them as out of scope

URLs are source metadata only. Never fetch a URL automatically. Use only product text that the user pasted directly.

## References

Read these files before producing final structured output:
- `references/taxonomy.json`: supported categories, aliases, vocabulary ids, material parts, ratio status values
- `references/schema.json`: required output structure and allowed values

The schema is authoritative for JSON shape. The taxonomy is authoritative for allowed normalized ids and alias mapping.

## Input

Expected input may be informal text or a JSON-like object containing:

```json
{
  "product_text": "user-pasted product detail text",
  "source_url": "optional source URL for metadata only",
  "source_title": "optional product/page title",
  "category_hint": "optional outer | top",
  "locale": "ko-KR"
}
```

If the user provides plain text, treat it as `product_text`.

## Workflow

1. Confirm the input is user-pasted product detail text.
   - If the user asks you to fetch a URL, do not fetch it. Ask for pasted product text or proceed only with already provided text.
   - If the input appears to contain secrets, customer data, or private/internal data, stop and report the safety issue.

2. Determine category.
   - Use `category_hint` if provided and consistent with the text.
   - Otherwise infer only between `outer` and `top`.
   - If the product is outside the MVP, set `quality.out_of_scope` to `true`, use the closest available fields only when safe, and explain the scope limit in `agent_descriptor.explainable_reasons`.

3. Extract product attributes from evidence in the input text.
   - `title`
   - `category`
   - `subcategory`
   - `materials`
   - `fit`
   - `colors`
   - `seasons`
   - `tpo_tags`
   - `care`
   - `size_info`

4. Normalize extracted values using `references/taxonomy.json`.
   - Map aliases to taxonomy ids, for example `자켓` or `블레이저` to `jacket`.
   - Prefer taxonomy ids over display names in JSON values.
   - Do not invent values that are not in taxonomy/schema enums.

5. Apply strict material and ratio handling.
   - For each material, include `part`, `name`, `ratio`, `ratio_status`, and `evidence`.
   - Use `ratio_status: "explicit"` only when the input text contains a numeric material ratio for that material and part.
   - When `ratio_status` is `explicit`, `ratio` must be a number from 0 to 100.
   - If a material is mentioned without a numeric ratio, set `ratio: null`, `ratio_status: "missing"`, and add `material_ratio` to `quality.missing_fields`.
   - If the text says only "혼방", "터치", "느낌", "라이크", or similar material-feel language, set `ratio: null`, `ratio_status: "ambiguous"`, and add `material_ratio` to `quality.ambiguous_fields`.
   - Keep different parts separate: `shell`, `lining`, `fill`, `rib`, `pocket`, `trim`, or `unknown`.
   - Never estimate fabric ratios. Never judge legal compliance.

6. Build `agent_descriptor`.
   - `search_summary`: one concise Korean sentence useful for agent retrieval.
   - `query_tags`: natural Korean query phrases the structured product can answer.
   - `explainable_reasons`: short Korean reasons grounded in extracted evidence and taxonomy mapping.

7. Fill `quality`.
   - Put absent required/important attributes in `missing_fields`.
   - Put uncertain attributes in `ambiguous_fields`.
   - Use `confidence` as `high`, `medium`, or `low` based on evidence clarity.
   - Use `out_of_scope: true` for unsupported categories.

8. Validate before final output.
   - The final object must match `references/schema.json`.
   - If `scripts/validate.py` exists, run it against the output JSON before reporting completion.
   - If the validation script is not available yet, manually check the schema-critical requirements and state that script validation is pending.

9. For batch duplicate preparation.
   - First produce one schema-valid structured JSON object per product.
   - If `scripts/dedup.py` exists and the user requested duplicate detection, run it on the structured products.
   - Do not perform duplicate detection from raw text alone when structured product JSON is not available.

## Output

Return a single JSON object matching `references/schema.json` for one product.

For multiple products, return one schema-valid object per product, then provide duplicate-candidate output only if duplicate detection was requested or the batch context requires it.

Do not include fields outside the schema. Do not include compliance verdicts such as "legal", "illegal", "valid label", or "violation".

## Completion Checklist

Before answering, verify:
- category is `outer` or `top`, or `quality.out_of_scope` is true
- all normalized ids exist in `taxonomy.json` and `schema.json`
- material `part`, `ratio`, and `ratio_status` obey the strict ratio rules
- every non-obvious extracted attribute has evidence in the input text
- missing or ambiguous data is reflected in `quality`
- no URL was fetched and no private/internal data was used
- final JSON is schema-valid or validation limitations are explicitly reported
