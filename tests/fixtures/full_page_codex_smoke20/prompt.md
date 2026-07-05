# Full-page synthetic Codex smoke20 conversion prompt

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
    {
      "product_id": "full_outer_000",
      "source_title": "DUMMY STANDARD 블랙 스타디움 재킷 000",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_000",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "sparse",
      "product_text": "브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 블랙 스타디움 재킷 000\n카테고리: 아우터 > 재킷 > 스타디움 재킷\n컬러: 블랙\n판매가: 99,000원"
    },
    {
      "product_id": "full_outer_001",
      "source_title": "AX TEST LABEL 그레이 트러커 재킷 001",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_001",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "sparse",
      "product_text": "브랜드: AX TEST LABEL\n상품명: AX TEST LABEL 그레이 트러커 재킷 001\n카테고리: 아우터 > 재킷 > 트러커 재킷\n컬러: 그레이\n판매가: 99,000원"
    },
    {
      "product_id": "full_outer_002",
      "source_title": "SYNTHETIC WORKS 네이비 플리스/뽀글이 002",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_002",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 네이비 플리스/뽀글이 002\n카테고리: 아우터 > 재킷 > 플리스/뽀글이\n컬러 옵션: 네이비\n\n[상품 정보]\n소재: 코튼 소재이며 숫자 혼용률은 표기되어 있지 않습니다.\n핏: 오버핏\n사이즈 옵션: M, L, XL\n추천 계절: 간절기\n추천 상황: 출근룩과 포멀\n관리 방법: 저온 다림질 가능"
    },
    {
      "product_id": "full_outer_003",
      "source_title": "REPRO SAMPLE 그린 아노락 재킷 003",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_003",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: REPRO SAMPLE\n상품명: REPRO SAMPLE 그린 아노락 재킷 003\n카테고리: 아우터 > 재킷 > 아노락 재킷\n컬러 옵션: 그린\n\n[상품 정보]\n소재: 린넨 터치의 레이온 블렌드 소재.\n핏: 레귤러핏\n사이즈 옵션: M, L, XL\n추천 계절: 여름\n추천 상황: 데일리와 스트리트\n관리 방법: 건조기 사용 금지"
    },
    {
      "product_id": "full_outer_006",
      "source_title": "SYNTHETIC WORKS 베이지 레더/라이더스 재킷 006",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_006",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "full",
      "product_text": "[상품 상단]\n브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 베이지 레더/라이더스 재킷 006\n카테고리: 아우터 > 재킷 > 레더/라이더스 재킷\n컬러 옵션: 베이지\n\n[상품 정보]\n소재 정보:\n- 겉감: 천연가죽 100%\n- 안감: 폴리에스터 100%\n핏: 박시핏\n사이즈 실측:\nM 총장 70cm 어깨 52cm 가슴 60cm\nL 총장 72cm 어깨 54cm 가슴 62cm\n추천 계절: 가을겨울\n추천 상황: 레이어드와 여행용\n관리 방법: 그늘 건조 권장, 건조기 사용 금지\n\n[상세 설명]\n데일리 착용과 반복 세탁을 고려해 봉제선과 여밈 부위를 안정적으로 설계한 합성 상세페이지 샘플입니다.\n자동 수집 데이터가 아니며 실제 상품 원문을 복제하지 않은 검증용 문장입니다."
    },
    {
      "product_id": "full_outer_009",
      "source_title": "AX TEST LABEL 옐로우 블루종/MA-1 009",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_009",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "noisy_ambiguous",
      "product_text": "[상품 상단]\n브랜드: AX TEST LABEL\n상품명: AX TEST LABEL 옐로우 블루종/MA-1 009\n카테고리: 아우터 > 재킷 > 블루종/MA-1\n컬러 옵션: 옐로우, 브라운\n\n[상품 정보]\n소재: 캐시미어를 블렌드한 듯한 부드러운 터치감의 고급 울 터치 원단. 정확한 혼용률은 상세 이미지 참고.\n핏: 스트레이트 핏\n사이즈 실측:\nM 총장 73cm 어깨 47cm 가슴 55cm\nL 총장 75cm 어깨 49cm 가슴 57cm\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 저온 다림질 가능\n\n[배송/혜택]\n오늘 22시까지 결제 시 내일 도착 예정이라는 예시 배송 문구입니다.\n첫 구매 쿠폰과 리뷰 요약은 구조화 대상 속성이 아닙니다.\n후기 요약: 따뜻해요, 사이즈가 여유 있어요, 색상이 화면과 비슷해요."
    },
    {
      "product_id": "full_outer_014",
      "source_title": "SYNTHETIC WORKS 블랙 겨울 더블 코트 014",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_014",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 블랙 겨울 더블 코트 014\n카테고리: 아우터 > 코트 > 겨울 더블 코트\n컬러 옵션: 블랙\n\n[상품 정보]\n소재: 겉감 울 70%, 캐시미어 30%.\n핏: 박시핏\n사이즈 옵션: M, L, XL\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 세탁기 사용 가능"
    },
    {
      "product_id": "full_outer_015",
      "source_title": "SYNTHETIC WORKS 블랙 겨울 더블 코트 014 리오더",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_015",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 블랙 겨울 더블 코트 014 리오더\n카테고리: 아우터 > 코트 > 겨울 더블 코트\n컬러 옵션: 블랙\n\n[상품 정보]\n소재: 겉감 울 70%, 캐시미어 30%.\n핏: 박시핏\n사이즈 옵션: M, L, XL\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 세탁기 사용 가능"
    },
    {
      "product_id": "full_outer_022",
      "source_title": "SYNTHETIC WORKS 카키 스타디움 재킷 022",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_022",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 카키 스타디움 재킷 022\n카테고리: 아우터 > 재킷 > 스타디움 재킷\n컬러 옵션: 카키\n\n[상품 정보]\n소재: 코튼 소재이며 숫자 혼용률은 표기되어 있지 않습니다.\n핏: 박시핏\n사이즈 옵션: M, L, XL\n추천 계절: 간절기\n추천 상황: 출근룩과 포멀\n관리 방법: 드라이클리닝 권장"
    },
    {
      "product_id": "full_outer_024",
      "source_title": "DUMMY STANDARD 아이보리 플리스/뽀글이 024",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_outer_024",
      "category_hint": "outer",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 아이보리 플리스/뽀글이 024\n카테고리: 아우터 > 재킷 > 플리스/뽀글이\n컬러 옵션: 아이보리\n\n[상품 정보]\n소재: 겉감 울 70%, 캐시미어 30%.\n핏: 슬림핏\n사이즈 옵션: M, L, XL\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 건조기 사용 금지"
    },
    {
      "product_id": "full_top_150",
      "source_title": "SYNTHETIC WORKS 그레이 반소매 티셔츠 150",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_150",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "sparse",
      "product_text": "브랜드: SYNTHETIC WORKS\n상품명: SYNTHETIC WORKS 그레이 반소매 티셔츠 150\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러: 그레이\n판매가: 99,000원"
    },
    {
      "product_id": "full_top_151",
      "source_title": "REPRO SAMPLE 네이비 긴소매 티셔츠 151",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_151",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "sparse",
      "product_text": "브랜드: REPRO SAMPLE\n상품명: REPRO SAMPLE 네이비 긴소매 티셔츠 151\n카테고리: 상의 > 티셔츠 > 긴소매 티셔츠\n컬러: 네이비\n판매가: 99,000원"
    },
    {
      "product_id": "full_top_152",
      "source_title": "DUMMY STANDARD 그린 셔츠/블라우스 152",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_152",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 그린 셔츠/블라우스 152\n카테고리: 상의 > 셔츠 > 셔츠/블라우스\n컬러 옵션: 그린\n\n[상품 정보]\n소재: 겉감 면 95%, 폴리우레탄 5%.\n핏: 릴랙스 핏\n사이즈 옵션: S, M, L\n추천 계절: 간절기\n추천 상황: 출근룩과 포멀\n관리 방법: 표백 금지"
    },
    {
      "product_id": "full_top_153",
      "source_title": "AX TEST LABEL 핑크 니트/스웨터 153",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_153",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: AX TEST LABEL\n상품명: AX TEST LABEL 핑크 니트/스웨터 153\n카테고리: 상의 > 니트 > 니트/스웨터\n컬러 옵션: 핑크\n\n[상품 정보]\n소재: 리사이클 섬유와 배색 폴리에스터를 사용했으나 숫자 혼용률은 표기되어 있지 않습니다.\n핏: 박시핏\n사이즈 옵션: S, M, L\n추천 계절: 여름\n추천 상황: 데일리와 스트리트\n관리 방법: 그늘 건조 권장"
    },
    {
      "product_id": "full_top_156",
      "source_title": "DUMMY STANDARD 블루 피케/카라 티셔츠 156",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_156",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "full",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 블루 피케/카라 티셔츠 156\n카테고리: 상의 > 폴로 > 피케/카라 티셔츠\n컬러 옵션: 블루, 핑크\n\n[상품 정보]\n소재 정보:\n- 겉감: 면 95%, 폴리우레탄 5%\n핏: 스트레이트 핏\n사이즈 실측:\nM 총장 70cm 어깨 50cm 가슴 58cm\nL 총장 72cm 어깨 52cm 가슴 60cm\n추천 계절: 가을겨울\n추천 상황: 레이어드와 여행용\n관리 방법: 저온 다림질 가능, 건조기 사용 금지\n\n[상세 설명]\n데일리 착용과 반복 세탁을 고려해 봉제선과 여밈 부위를 안정적으로 설계한 합성 상세페이지 샘플입니다.\n자동 수집 데이터가 아니며 실제 상품 원문을 복제하지 않은 검증용 문장입니다."
    },
    {
      "product_id": "full_top_159",
      "source_title": "REPRO SAMPLE 아이보리 반소매 티셔츠 159",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_159",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "noisy_ambiguous",
      "product_text": "[상품 상단]\n브랜드: REPRO SAMPLE\n상품명: REPRO SAMPLE 아이보리 반소매 티셔츠 159\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 아이보리, 옐로우\n\n[상품 정보]\n소재: 린넨 라이크 터치와 레이온 블렌드 느낌을 살린 원단. 숫자 혼용률은 제공되지 않습니다.\n핏: 롱라인\n사이즈 실측:\nM 총장 73cm 어깨 53cm 가슴 61cm\nL 총장 75cm 어깨 55cm 가슴 63cm\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 표백 금지\n\n[배송/혜택]\n오늘 22시까지 결제 시 내일 도착 예정이라는 예시 배송 문구입니다.\n첫 구매 쿠폰과 리뷰 요약은 구조화 대상 속성이 아닙니다.\n후기 요약: 따뜻해요, 사이즈가 여유 있어요, 색상이 화면과 비슷해요."
    },
    {
      "product_id": "full_top_161",
      "source_title": "AX TEST LABEL 데님 블루 셔츠/블라우스 161",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_161",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "sparse",
      "product_text": "브랜드: AX TEST LABEL\n상품명: AX TEST LABEL 데님 블루 셔츠/블라우스 161\n카테고리: 상의 > 셔츠 > 셔츠/블라우스\n컬러: 데님 블루\n판매가: 99,000원"
    },
    {
      "product_id": "full_top_164",
      "source_title": "DUMMY STANDARD 그레이 민소매 티셔츠 164",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_164",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 그레이 민소매 티셔츠 164\n카테고리: 상의 > 슬리브리스 > 민소매 티셔츠\n컬러 옵션: 그레이\n\n[상품 정보]\n소재: 페이크 레더 느낌의 소재.\n핏: 스트레이트 핏\n사이즈 옵션: S, M, L\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 건조기 사용 금지"
    },
    {
      "product_id": "full_top_165",
      "source_title": "DUMMY STANDARD 그레이 민소매 티셔츠 164 리오더",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_165",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "medium",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 그레이 민소매 티셔츠 164 리오더\n카테고리: 상의 > 슬리브리스 > 민소매 티셔츠\n컬러 옵션: 그레이\n\n[상품 정보]\n소재: 페이크 레더 느낌의 소재.\n핏: 스트레이트 핏\n사이즈 옵션: S, M, L\n추천 계절: 겨울\n추천 상황: 아웃도어와 여행\n관리 방법: 건조기 사용 금지"
    },
    {
      "product_id": "full_top_168",
      "source_title": "DUMMY STANDARD 화이트 반소매 티셔츠 168",
      "source_url": "https://example.com/musinsa-full-page-dummy/full_top_168",
      "category_hint": "top",
      "locale": "ko-KR",
      "source_method": "synthetic_full_page_like",
      "information_density": "full",
      "product_text": "[상품 상단]\n브랜드: DUMMY STANDARD\n상품명: DUMMY STANDARD 화이트 반소매 티셔츠 168\n카테고리: 상의 > 티셔츠 > 반소매 티셔츠\n컬러 옵션: 화이트, 아이보리\n\n[상품 정보]\n소재 정보:\n- 겉감: 면 95%, 폴리우레탄 5%\n핏: 릴랙스 핏\n사이즈 실측:\nM 총장 72cm 어깨 46cm 가슴 54cm\nL 총장 74cm 어깨 48cm 가슴 56cm\n추천 계절: 여름\n추천 상황: 데일리와 스트리트\n관리 방법: 세탁기 사용 가능, 건조기 사용 금지\n\n[상세 설명]\n데일리 착용과 반복 세탁을 고려해 봉제선과 여밈 부위를 안정적으로 설계한 합성 상세페이지 샘플입니다.\n자동 수집 데이터가 아니며 실제 상품 원문을 복제하지 않은 검증용 문장입니다."
    }
  ]
}
