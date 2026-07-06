# S7.8 size_info pattern conversion prompt template

Use `src/skills/product-agentizer/SKILL.md`, `references/schema.json`, and `references/taxonomy.json`.
Convert every case below into a raw JSON object with this exact top-level shape:

```json
{"products":[{"product_id":"...","structured_product":{}}]}
```

Rules:
- Return raw JSON only, with no Markdown fences.
- Do not fetch URLs. URLs are synthetic source metadata only.
- Do not judge legal label compliance.
- Preserve product_id values exactly.
- Treat 배송, 쿠폰, 후기 요약, 구매자 만족도, 개인화 추천 문구 as noise unless they directly state static product size attributes.
- Follow the SKILL.md size_info atomization rules exactly.

Input cases:
{
  "cases": [
    "<replace with source_inputs.json cases>"
  ]
}
