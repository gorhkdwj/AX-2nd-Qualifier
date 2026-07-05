# Codex subset conversion prompt

Use `src/skills/product-agentizer/SKILL.md`, `references/schema.json`, and `references/taxonomy.json`.
Convert every case below into a raw JSON object with this exact top-level shape:

```json
{"products":[{"product_id":"...","structured_product":{}}]}
```

Rules:
- Return raw JSON only, with no Markdown fences.
- Do not fetch URLs. URLs are source metadata only.
- Do not judge legal label compliance.
- Never estimate fabric ratios. Use `missing` or `ambiguous` when the input does not provide a numeric ratio.
- Preserve product_id values exactly.

Input cases:
{
  "cases": [
    {
      "product_id": "outer_dummy_000",
      "source_title": "블랙 슬림핏 재킷 000",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_000",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 블랙 슬림핏 재킷 000. 컬러: 블랙. 겉감 리넨 60%, 면 40%. 슬림핏 실루엣이며 L 기준 총장 62cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 세탁기 사용 가능."
    },
    {
      "product_id": "outer_dummy_001",
      "source_title": "블랙 슬림핏 재킷 000 리오더",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_001",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 블랙 슬림핏 재킷 000 리오더. 컬러: 블랙. 겉감 리넨 60%, 면 40%. 슬림핏 실루엣이며 L 기준 총장 62cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 세탁기 사용 가능."
    },
    {
      "product_id": "outer_dummy_004",
      "source_title": "핑크 롱라인 베스트 004",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_004",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 핑크 롱라인 베스트 004. 컬러: 핑크. 겉감 울 70%, 캐시미어 30%. 롱라인 실루엣이며 L 기준 총장 66cm, 어깨와 가슴둘레 여유가 특징입니다. 겨울 아웃도어와 여행에 활용하기 좋습니다. 단독 손세탁 권장."
    },
    {
      "product_id": "outer_dummy_006",
      "source_title": "베이지 박시핏 재킷 006",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_006",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 베이지 박시핏 재킷 006. 컬러: 베이지. 충전재 덕다운 80%, 구스다운 20%. 박시핏 실루엣이며 L 기준 총장 68cm, 어깨와 가슴둘레 여유가 특징입니다. 가을겨울 레이어드와 여행용에 활용하기 좋습니다. 그늘 건조 권장."
    },
    {
      "product_id": "outer_dummy_008",
      "source_title": "카키 슬림핏 코트 008",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_008",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 카키 슬림핏 코트 008. 컬러: 카키. 리사이클 섬유와 배색 폴리에스터를 사용했으나 숫자 혼용률은 표기되어 있지 않습니다. 슬림핏 실루엣이며 L 기준 총장 70cm, 어깨와 가슴둘레 여유가 특징입니다. 여름 데일리와 스트리트에 활용하기 좋습니다. 드라이클리닝 권장."
    },
    {
      "product_id": "outer_dummy_011",
      "source_title": "아이보리 오버핏 베스트 010 리오더",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_011",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 아이보리 오버핏 베스트 010 리오더. 컬러: 아이보리. 겉감 리넨 60%, 면 40%. 오버핏 실루엣이며 L 기준 총장 72cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 건조기 사용 금지."
    },
    {
      "product_id": "outer_dummy_020",
      "source_title": "베이지 롱라인 코트 020",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_020",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 베이지 롱라인 코트 020. 컬러: 베이지. 겉감 리넨 60%, 면 40%. 롱라인 실루엣이며 L 기준 총장 64cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 그늘 건조 권장."
    },
    {
      "product_id": "outer_dummy_031",
      "source_title": "네이비 박시핏 재킷 030 리오더",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_031",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 네이비 박시핏 재킷 030 리오더. 컬러: 네이비. 겉감 리넨 60%, 면 40%. 박시핏 실루엣이며 L 기준 총장 74cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 저온 다림질 가능."
    },
    {
      "product_id": "outer_dummy_040",
      "source_title": "데님 블루 슬림핏 베스트 040",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_040",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 데님 블루 슬림핏 베스트 040. 컬러: 데님 블루. 겉감 리넨 60%, 면 40%. 슬림핏 실루엣이며 L 기준 총장 66cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 표백 금지."
    },
    {
      "product_id": "outer_dummy_049",
      "source_title": "블루 스트레이트 핏 점퍼 049",
      "source_url": "https://example.com/musinsa-expanded/outer_dummy_049",
      "category_hint": "outer",
      "locale": "ko-KR",
      "product_text": "상품명: 블루 스트레이트 핏 점퍼 049. 컬러: 블루. 페이크 레더 느낌의 소재. 스트레이트 핏 실루엣이며 L 기준 총장 75cm, 어깨와 가슴둘레 여유가 특징입니다. 겨울 아웃도어와 여행에 활용하기 좋습니다. 세탁기 사용 가능."
    },
    {
      "product_id": "top_dummy_050",
      "source_title": "레드 크롭 핏 니트 050",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_050",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 레드 크롭 핏 니트 050. 컬러: 레드. 린넨 터치의 레이온 블렌드 소재. 크롭 핏 실루엣이며 M 기준 총장 76cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 표백 금지."
    },
    {
      "product_id": "top_dummy_051",
      "source_title": "레드 크롭 핏 니트 050 리오더",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_051",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 레드 크롭 핏 니트 050 리오더. 컬러: 레드. 린넨 터치의 레이온 블렌드 소재. 크롭 핏 실루엣이며 M 기준 총장 76cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 표백 금지."
    },
    {
      "product_id": "top_dummy_054",
      "source_title": "그린 레귤러핏 티셔츠 054",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_054",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 그린 레귤러핏 티셔츠 054. 컬러: 그린. 겉감 면 95%, 폴리우레탄 5%. 레귤러핏 실루엣이며 M 기준 총장 62cm, 어깨와 가슴둘레 여유가 특징입니다. 겨울 아웃도어와 여행에 활용하기 좋습니다. 저온 다림질 가능."
    },
    {
      "product_id": "top_dummy_056",
      "source_title": "화이트 릴랙스 핏 니트 056",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_056",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 화이트 릴랙스 핏 니트 056. 컬러: 화이트. 페이크 레더 느낌의 소재. 릴랙스 핏 실루엣이며 M 기준 총장 64cm, 어깨와 가슴둘레 여유가 특징입니다. 가을겨울 레이어드와 여행용에 활용하기 좋습니다. 단독 손세탁 권장."
    },
    {
      "product_id": "top_dummy_058",
      "source_title": "블루 크롭 핏 슬리브리스 058",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_058",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 블루 크롭 핏 슬리브리스 058. 컬러: 블루. 겉감 폴리에스터 100%. 크롭 핏 실루엣이며 M 기준 총장 66cm, 어깨와 가슴둘레 여유가 특징입니다. 여름 데일리와 스트리트에 활용하기 좋습니다. 그늘 건조 권장."
    },
    {
      "product_id": "top_dummy_061",
      "source_title": "옐로우 스트레이트 핏 티셔츠 060 리오더",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_061",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 옐로우 스트레이트 핏 티셔츠 060 리오더. 컬러: 옐로우. 린넨 터치의 레이온 블렌드 소재. 스트레이트 핏 실루엣이며 M 기준 총장 68cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 드라이클리닝 권장."
    },
    {
      "product_id": "top_dummy_070",
      "source_title": "화이트 레귤러핏 슬리브리스 070",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_070",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 화이트 레귤러핏 슬리브리스 070. 컬러: 화이트. 린넨 터치의 레이온 블렌드 소재. 레귤러핏 실루엣이며 M 기준 총장 78cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 단독 손세탁 권장."
    },
    {
      "product_id": "top_dummy_081",
      "source_title": "그레이 릴랙스 핏 니트 080 리오더",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_081",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 그레이 릴랙스 핏 니트 080 리오더. 컬러: 그레이. 린넨 터치의 레이온 블렌드 소재. 릴랙스 핏 실루엣이며 M 기준 총장 70cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 세탁기 사용 가능."
    },
    {
      "product_id": "top_dummy_090",
      "source_title": "브라운 크롭 핏 티셔츠 090",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_090",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 브라운 크롭 핏 티셔츠 090. 컬러: 브라운. 린넨 터치의 레이온 블렌드 소재. 크롭 핏 실루엣이며 M 기준 총장 62cm, 어깨와 가슴둘레 여유가 특징입니다. 봄여름 데일리와 캐주얼에 활용하기 좋습니다. 건조기 사용 금지."
    },
    {
      "product_id": "top_dummy_099",
      "source_title": "베이지 슬림핏 스웨트셔츠 099",
      "source_url": "https://example.com/musinsa-expanded/top_dummy_099",
      "category_hint": "top",
      "locale": "ko-KR",
      "product_text": "상품명: 베이지 슬림핏 스웨트셔츠 099. 컬러: 베이지. 코튼 소재이며 숫자 혼용률은 표기되어 있지 않습니다. 슬림핏 실루엣이며 M 기준 총장 71cm, 어깨와 가슴둘레 여유가 특징입니다. 겨울 아웃도어와 여행에 활용하기 좋습니다. 표백 금지."
    }
  ]
}
