# S7.8 size_info pattern conversion prompt

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
    {
      "product_id": "sizepat_000",
      "source_title": "SIZE TEST LABEL letter_comma 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_000",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_comma 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈 옵션: S, M, L\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_001",
      "source_title": "SIZE TEST LABEL letter_comma 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_001",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_comma 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n구매 가능 사이즈: M, L, XL\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_002",
      "source_title": "SIZE TEST LABEL letter_comma 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_002",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_comma 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\nSIZE OPTION: XS, S, M\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_003",
      "source_title": "SIZE TEST LABEL letter_comma 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_003",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_comma 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n옵션 사이즈: L, XL, XXL\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_004",
      "source_title": "SIZE TEST LABEL letter_slash 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_004",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_slash 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\nSIZE: XS / S / M / L / XL\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_005",
      "source_title": "SIZE TEST LABEL letter_slash 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_005",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_slash 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n사이즈: S/M/L\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_006",
      "source_title": "SIZE TEST LABEL letter_slash 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_006",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_slash 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n옵션: M | L | XL\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_007",
      "source_title": "SIZE TEST LABEL letter_slash 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_007",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL letter_slash 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nSize: FREE / M / L\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_008",
      "source_title": "SIZE TEST LABEL numeric_space 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_008",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL numeric_space 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈: 90 95 100 105\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_009",
      "source_title": "SIZE TEST LABEL numeric_space 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_009",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL numeric_space 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nSIZE: 85 90 95\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_010",
      "source_title": "SIZE TEST LABEL numeric_space 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_010",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL numeric_space 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n옵션: 100 105 110\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_011",
      "source_title": "SIZE TEST LABEL numeric_space 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_011",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL numeric_space 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n사이즈 선택: 95 100\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_012",
      "source_title": "SIZE TEST LABEL women_numeric 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_012",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL women_numeric 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈 옵션: 44, 55, 66\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_013",
      "source_title": "SIZE TEST LABEL women_numeric 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_013",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL women_numeric 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nSIZE: 55 / 66 / 77\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_014",
      "source_title": "SIZE TEST LABEL women_numeric 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_014",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL women_numeric 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈: 44 55\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_015",
      "source_title": "SIZE TEST LABEL women_numeric 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_015",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL women_numeric 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n옵션: 66, 77\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_016",
      "source_title": "SIZE TEST LABEL brand_numeric 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_016",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL brand_numeric 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n브랜드 사이즈: 1 / 2 / 3\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_017",
      "source_title": "SIZE TEST LABEL brand_numeric 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_017",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL brand_numeric 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n옵션: 0, 1, 2\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_018",
      "source_title": "SIZE TEST LABEL brand_numeric 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_018",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL brand_numeric 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\nSIZE: 2 3 4\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_019",
      "source_title": "SIZE TEST LABEL brand_numeric 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_019",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL brand_numeric 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n사이즈 선택: 1, 2\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_020",
      "source_title": "SIZE TEST LABEL mixed_parentheses 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_020",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL mixed_parentheses 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈: M(95), L(100), XL(105)\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_021",
      "source_title": "SIZE TEST LABEL mixed_parentheses 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_021",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL mixed_parentheses 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n옵션: S(90) / M(95) / L(100)\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_022",
      "source_title": "SIZE TEST LABEL mixed_parentheses 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_022",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL mixed_parentheses 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\nSIZE: 1(44-55), 2(66), 3(77)\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_023",
      "source_title": "SIZE TEST LABEL mixed_parentheses 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_023",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL mixed_parentheses 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n사이즈: FREE(44-66)\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_024",
      "source_title": "SIZE TEST LABEL free_one_size 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_024",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL free_one_size 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈: FREE\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_025",
      "source_title": "SIZE TEST LABEL free_one_size 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_025",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL free_one_size 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nSIZE: ONE SIZE\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_026",
      "source_title": "SIZE TEST LABEL free_one_size 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_026",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL free_one_size 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n옵션: OS\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_027",
      "source_title": "SIZE TEST LABEL free_one_size 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_027",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL free_one_size 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n사이즈 옵션: FREE, ONE SIZE\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_028",
      "source_title": "SIZE TEST LABEL measurement_rows 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_028",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_rows 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈 실측:\nM 총장 68cm 어깨 50cm 가슴 58cm 소매 60cm\nL 총장 70cm 어깨 52cm 가슴 60cm 소매 61cm\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_029",
      "source_title": "SIZE TEST LABEL measurement_rows 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_029",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_rows 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n실측 사이즈:\nS 총장 64cm 어깨 46cm 가슴 53cm\nM 총장 66cm 어깨 48cm 가슴 55cm\nL 총장 68cm 어깨 50cm 가슴 57cm\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_030",
      "source_title": "SIZE TEST LABEL measurement_rows 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_030",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_rows 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\nFREE 총장 72cm 가슴 64cm 밑단 62cm\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_031",
      "source_title": "SIZE TEST LABEL measurement_rows 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_031",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_rows 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n1 총장 65cm 어깨 48cm 가슴 56cm\n2 총장 67cm 어깨 50cm 가슴 58cm\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_032",
      "source_title": "SIZE TEST LABEL measurement_table 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_032",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_table 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈(cm) 총장 어깨 가슴 소매\nM 68 50 58 60\nL 70 52 60 61\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_033",
      "source_title": "SIZE TEST LABEL measurement_table 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_033",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_table 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nSIZE(cm) LENGTH SHOULDER CHEST SLEEVE\nS 64 46 53 58\nM 66 48 55 59\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_034",
      "source_title": "SIZE TEST LABEL measurement_table 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_034",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_table 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈표\nFREE 총장 71 가슴단면 62 암홀 28\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_035",
      "source_title": "SIZE TEST LABEL measurement_table 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_035",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL measurement_table 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n실측 정보(cm)\n1 총장 65 어깨 48 가슴 56\n2 총장 67 어깨 50 가슴 58\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_036",
      "source_title": "SIZE TEST LABEL model_wear 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_036",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL model_wear 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n모델 181cm/70kg L 착용\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_037",
      "source_title": "SIZE TEST LABEL model_wear 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_037",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL model_wear 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n여성 모델 170cm S 착용\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_038",
      "source_title": "SIZE TEST LABEL model_wear 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_038",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL model_wear 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n남성 모델 178cm 68kg M 사이즈 착용\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_039",
      "source_title": "SIZE TEST LABEL model_wear 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_039",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL model_wear 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\nLOOKBOOK MODEL 186cm XL 착용\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_040",
      "source_title": "SIZE TEST LABEL comparison_guide 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_040",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL comparison_guide 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈 비교 가이드: 무신사 스탠다드 M 사이즈 티셔츠와 비슷한 사이즈입니다.\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_041",
      "source_title": "SIZE TEST LABEL comparison_guide 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_041",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL comparison_guide 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n이 상품은 가슴단면 기준으로 무신사 스탠다드 XS 민소매와 비슷합니다.\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_042",
      "source_title": "SIZE TEST LABEL comparison_guide 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_042",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL comparison_guide 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n어깨너비 기준으로 무신사 스탠다드 L 점퍼와 유사한 사이즈입니다.\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_043",
      "source_title": "SIZE TEST LABEL comparison_guide 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_043",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL comparison_guide 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n기존 착용 상품과 비교하면 100 사이즈 셔츠에 가까운 핏입니다.\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_044",
      "source_title": "SIZE TEST LABEL recommendation_noise 01",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_044",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL recommendation_noise 01\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n사이즈 추천: 178cm 70kg 고객은 L을 많이 선택했습니다.\n후기 요약: 사이즈가 적당해요 82%\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_045",
      "source_title": "SIZE TEST LABEL recommendation_noise 02",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_045",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL recommendation_noise 02\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n구매자 사이즈 만족도: 커요 12%, 적당해요 82%, 작아요 6%\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_046",
      "source_title": "SIZE TEST LABEL recommendation_noise 03",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_046",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL recommendation_noise 03\n카테고리: 아우터 > 재킷 > 나일론/코치 재킷\n컬러 옵션: 블랙\n\n[상품 정보]\n소재 정보: 겉감 나일론 100%\n핏: 레귤러핏\n내 체형 기준 추천 사이즈는 로그인 후 확인할 수 있습니다.\n추천 계절: 간절기\n추천 상황: 데일리\n관리 방법: 단독 손세탁 권장\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    },
    {
      "product_id": "sizepat_047",
      "source_title": "SIZE TEST LABEL recommendation_noise 04",
      "source_url": "https://example.com/musinsa-size-info-pattern/sizepat_047",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_size_info_pattern",
      "product_text": "[상품 상단]\n브랜드: SIZE TEST LABEL\n상품명: SIZE TEST LABEL recommendation_noise 04\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트\n\n[상품 정보]\n소재 정보: 겉감 면 100%\n핏: 레귤러핏\n후기 요약: 사이즈가 여유 있어요. 배송 안내: 오늘 출발.\n추천 계절: 여름\n추천 상황: 데일리\n관리 방법: 세탁기 사용 가능\n\n[노이즈]\n첫 구매 쿠폰, 배송 안내, 리뷰 요약은 상품의 정적 사이즈 옵션이 아닐 수 있습니다."
    }
  ]
}
