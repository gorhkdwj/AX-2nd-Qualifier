# Full-page synthetic Codex smoke20 conversion prompt template

Use `src/skills/product-agentizer/SKILL.md`, `references/schema.json`, and `references/taxonomy.json`.
Convert every case below into a raw JSON object with this exact top-level shape:

```json
{"products":[{"product_id":"...","structured_product":{}}]}
```

Rules:
- Return raw JSON only, with no Markdown fences.
- Do not fetch URLs. URLs are synthetic source metadata only.
- Do not judge legal label compliance.
- Never estimate fabric ratios. Use `missing` or `ambiguous` when the input does not provide a numeric ratio.
- Preserve product_id values exactly.
- Treat 배송, 쿠폰, 후기 요약, 가격 문구 as noise unless they directly state product attributes.

Input cases:
{
  "cases": [
    "<replace with source_inputs.json cases>"
  ]
}
