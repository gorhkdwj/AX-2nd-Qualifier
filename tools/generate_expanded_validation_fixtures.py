#!/usr/bin/env python3
"""Generate reproducible expanded validation fixtures for product-agentizer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"
EXPANDED_DIR = FIXTURE_ROOT / "expanded_dummy"
REAL_DIR = FIXTURE_ROOT / "real_sanity"


OUTER_SUBCATEGORIES = ["jacket", "jumper", "coat", "cardigan", "vest", "hoodie_zipup", "other_outer"]
TOP_SUBCATEGORIES = ["tshirt", "shirt_blouse", "knit", "sweatshirt", "sleeveless", "polo", "hoodie", "other_top"]
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
OUTER_DETAIL_TYPE_SEQUENCE = [
    (subcategory, detail_type)
    for subcategory in OUTER_SUBCATEGORIES
    for detail_type in OUTER_DETAIL_TYPES[subcategory]
]
TOP_DETAIL_TYPE_SEQUENCE = [
    (subcategory, detail_type)
    for subcategory in TOP_SUBCATEGORIES
    for detail_type in TOP_DETAIL_TYPES[subcategory]
]
COLORS = ["black", "white", "ivory", "gray", "beige", "brown", "navy", "blue", "denim_blue", "green", "khaki", "red", "pink", "yellow"]
FITS = ["regular", "slim", "relaxed", "oversized", "cropped", "longline", "straight", "boxy"]
CARE = ["machine_wash", "hand_wash", "dry_clean", "do_not_bleach", "low_temp_iron", "shade_dry", "no_tumble_dry"]

KO_COLOR = {
    "black": "블랙",
    "white": "화이트",
    "ivory": "아이보리",
    "gray": "그레이",
    "beige": "베이지",
    "brown": "브라운",
    "navy": "네이비",
    "blue": "블루",
    "denim_blue": "데님 블루",
    "green": "그린",
    "khaki": "카키",
    "red": "레드",
    "pink": "핑크",
    "yellow": "옐로우",
    "multi": "멀티",
}

KO_FIT = {
    "regular": "레귤러핏",
    "slim": "슬림핏",
    "relaxed": "릴랙스 핏",
    "oversized": "오버핏",
    "cropped": "크롭 핏",
    "longline": "롱라인",
    "straight": "스트레이트 핏",
    "boxy": "박시핏",
}

KO_SUBCATEGORY = {
    "jacket": "재킷",
    "jumper": "점퍼",
    "coat": "코트",
    "cardigan": "가디건",
    "vest": "베스트",
    "hoodie_zipup": "후드 집업",
    "other_outer": "기타 아우터",
    "tshirt": "티셔츠",
    "shirt_blouse": "셔츠",
    "knit": "니트",
    "sweatshirt": "스웨트셔츠",
    "sleeveless": "슬리브리스",
    "polo": "폴로",
    "hoodie": "후드 티셔츠",
    "other_top": "기타 상의",
}

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

CARE_TEXT = {
    "machine_wash": "세탁기 사용 가능",
    "hand_wash": "단독 손세탁 권장",
    "dry_clean": "드라이클리닝 권장",
    "do_not_bleach": "표백 금지",
    "low_temp_iron": "저온 다림질 가능",
    "shade_dry": "그늘 건조 권장",
    "no_tumble_dry": "건조기 사용 금지",
}


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def material_pattern(index: int) -> tuple[list[dict[str, Any]], str, list[str], list[str]]:
    pattern = index % 10
    if pattern == 0:
        return (
            [
                {"part": "shell", "name": "linen", "ratio": 60, "ratio_status": "explicit", "evidence": "겉감 리넨 60%, 면 40%"},
                {"part": "shell", "name": "cotton", "ratio": 40, "ratio_status": "explicit", "evidence": "겉감 리넨 60%, 면 40%"},
            ],
            "겉감 리넨 60%, 면 40%",
            [],
            [],
        )
    if pattern == 1:
        return (
            [{"part": "shell", "name": "polyester", "ratio": 100, "ratio_status": "explicit", "evidence": "겉감 폴리에스터 100%"}],
            "겉감 폴리에스터 100%",
            [],
            [],
        )
    if pattern == 2:
        return (
            [{"part": "unknown", "name": "cotton", "ratio": None, "ratio_status": "missing", "evidence": "코튼 소재"}],
            "코튼 소재이며 숫자 혼용률은 표기되어 있지 않습니다",
            ["material_ratio"],
            [],
        )
    if pattern == 3:
        return (
            [
                {"part": "unknown", "name": "linen", "ratio": None, "ratio_status": "ambiguous", "evidence": "린넨 터치"},
                {"part": "unknown", "name": "rayon", "ratio": None, "ratio_status": "ambiguous", "evidence": "레이온 블렌드"},
            ],
            "린넨 터치의 레이온 블렌드 소재",
            [],
            ["material_ratio"],
        )
    if pattern == 4:
        return (
            [
                {"part": "shell", "name": "wool", "ratio": 70, "ratio_status": "explicit", "evidence": "겉감 울 70%, 캐시미어 30%"},
                {"part": "shell", "name": "cashmere", "ratio": 30, "ratio_status": "explicit", "evidence": "겉감 울 70%, 캐시미어 30%"},
            ],
            "겉감 울 70%, 캐시미어 30%",
            [],
            [],
        )
    if pattern == 5:
        return (
            [
                {"part": "shell", "name": "nylon", "ratio": 100, "ratio_status": "explicit", "evidence": "겉감 나일론 100%"},
                {"part": "lining", "name": "polyester", "ratio": 100, "ratio_status": "explicit", "evidence": "안감 폴리에스터 100%"},
            ],
            "겉감 나일론 100%, 안감 폴리에스터 100%",
            [],
            [],
        )
    if pattern == 6:
        return (
            [
                {"part": "fill", "name": "duck_down", "ratio": 80, "ratio_status": "explicit", "evidence": "충전재 덕다운 80%, 구스다운 20%"},
                {"part": "fill", "name": "goose_down", "ratio": 20, "ratio_status": "explicit", "evidence": "충전재 덕다운 80%, 구스다운 20%"},
            ],
            "충전재 덕다운 80%, 구스다운 20%",
            [],
            [],
        )
    if pattern == 7:
        return (
            [
                {"part": "shell", "name": "cotton", "ratio": 95, "ratio_status": "explicit", "evidence": "겉감 면 95%, 폴리우레탄 5%"},
                {"part": "shell", "name": "polyurethane", "ratio": 5, "ratio_status": "explicit", "evidence": "겉감 면 95%, 폴리우레탄 5%"},
            ],
            "겉감 면 95%, 폴리우레탄 5%",
            [],
            [],
        )
    if pattern == 8:
        return (
            [
                {"part": "unknown", "name": "recycled_fiber", "ratio": None, "ratio_status": "missing", "evidence": "리사이클 섬유"},
                {"part": "unknown", "name": "polyester", "ratio": None, "ratio_status": "missing", "evidence": "배색 폴리에스터"},
            ],
            "리사이클 섬유와 배색 폴리에스터를 사용했으나 숫자 혼용률은 표기되어 있지 않습니다",
            ["material_part", "material_ratio"],
            [],
        )
    return (
        [
            {"part": "shell", "name": "faux_leather", "ratio": None, "ratio_status": "ambiguous", "evidence": "페이크 레더 느낌"},
        ],
        "페이크 레더 느낌의 소재",
        [],
        ["material_ratio"],
    )


def season_tpo(index: int, category: str) -> tuple[list[str], str, list[str], str]:
    variants = [
        (["spring", "summer"], "봄여름", ["daily", "casual"], "데일리와 캐주얼"),
        (["fall", "winter"], "가을겨울", ["layering", "travel"], "레이어드와 여행용"),
        (["spring", "fall"], "간절기", ["commute", "formal"], "출근룩과 포멀"),
        (["summer"], "여름", ["daily", "street"], "데일리와 스트리트"),
        (["winter"], "겨울", ["outdoor", "travel"], "아웃도어와 여행"),
    ]
    seasons, season_text, tpo, tpo_text = variants[index % len(variants)]
    if category == "outer" and "layering" not in tpo:
        tpo = [*tpo, "layering"]
    return seasons, season_text, tpo, tpo_text


def structured_product(
    product_id: str,
    title: str,
    category: str,
    subcategory: str,
    detail_type: str | None,
    materials: list[dict[str, Any]],
    fit: str,
    color: str,
    seasons: list[str],
    tpo_tags: list[str],
    care: str | list[str],
    size_info: list[str],
    source_url: str | None,
    missing_fields: list[str],
    ambiguous_fields: list[str],
) -> dict[str, Any]:
    care_values = care if isinstance(care, list) else [care]
    normalized_missing_fields = sorted(
        set([*missing_fields, "material_part"] if any(item.get("part") == "unknown" for item in materials) else missing_fields)
    )
    normalized_ambiguous_fields = sorted(set(ambiguous_fields))
    return {
        "product_id": product_id,
        "structured_product": {
            "schema_version": "0.2.0",
            "source": {
                "source_url": source_url,
                "source_title": title,
                "input_mode": "pasted_text",
            },
            "product": {
                "title": title,
                "category": category,
                "subcategory": subcategory,
                "detail_type": detail_type,
                "materials": materials,
                "fit": [fit],
                "colors": [color],
                "seasons": seasons,
                "tpo_tags": tpo_tags,
                "care": care_values,
                "size_info": size_info,
            },
            "agent_descriptor": {
                "search_summary": f"{KO_COLOR[color]} {KO_FIT[fit]} {KO_DETAIL_TYPE[detail_type] if detail_type else KO_SUBCATEGORY[subcategory]}",
                "query_tags": [
                    f"{KO_COLOR[color]} {KO_DETAIL_TYPE[detail_type] if detail_type else KO_SUBCATEGORY[subcategory]}",
                    f"{KO_FIT[fit]} 상품",
                ],
                "explainable_reasons": [
                    f"입력 텍스트의 색상, 핏, 카테고리 단서를 {color}, {fit}, {subcategory}로 정규화했습니다."
                ],
            },
            "quality": {
                "missing_fields": normalized_missing_fields,
                "ambiguous_fields": normalized_ambiguous_fields,
                "out_of_scope": False,
                "confidence": "medium" if normalized_missing_fields or normalized_ambiguous_fields else "high",
            },
        },
    }


def source_case(
    product_id: str,
    title: str,
    category: str,
    source_url: str | None,
    product_text: str,
) -> dict[str, Any]:
    return {
        "product_id": product_id,
        "source_title": title,
        "source_url": source_url,
        "category_hint": category,
        "locale": "ko-KR",
        "product_text": product_text,
    }


def make_dummy_case(index: int, category: str, duplicate_of: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    if duplicate_of is not None:
        src = dict(duplicate_of["source"])
        product = json.loads(json.dumps(duplicate_of["product"], ensure_ascii=False))
        product_id = f"{category}_dummy_{index:03d}"
        title = f"{product['structured_product']['product']['title']} 리오더"
        src["product_id"] = product_id
        src["source_title"] = title
        src["source_url"] = f"https://example.com/musinsa-expanded/{product_id}"
        src["product_text"] = src["product_text"].replace(duplicate_of["source"]["source_title"], title)
        product["product_id"] = product_id
        product["structured_product"]["source"]["source_title"] = title
        product["structured_product"]["source"]["source_url"] = src["source_url"]
        product["structured_product"]["product"]["title"] = title
        product["structured_product"]["agent_descriptor"]["search_summary"] = product["structured_product"]["agent_descriptor"]["search_summary"].replace(
            duplicate_of["source"]["source_title"], title
        )
        return src, product

    detail_type_sequence = OUTER_DETAIL_TYPE_SEQUENCE if category == "outer" else TOP_DETAIL_TYPE_SEQUENCE
    local_index = index if category == "outer" else index - 50
    subcategory, detail_type = detail_type_sequence[local_index % len(detail_type_sequence)]
    color = COLORS[(index * 3 + (0 if category == "outer" else 1)) % len(COLORS)]
    fit = FITS[(index * 5 + (1 if category == "outer" else 2)) % len(FITS)]
    care = CARE[(index * 2 + (0 if category == "outer" else 1)) % len(CARE)]
    materials, material_text, missing, ambiguous = material_pattern(index + (0 if category == "outer" else 3))
    seasons, season_text, tpo_tags, tpo_text = season_tpo(index, category)
    product_id = f"{category}_dummy_{index:03d}"
    title = f"{KO_COLOR[color]} {KO_FIT[fit]} {KO_DETAIL_TYPE[detail_type]} {index:03d}"
    source_url = f"https://example.com/musinsa-expanded/{product_id}"
    size_info = [f"{'L' if category == 'outer' else 'M'} 기준 총장 {62 + (index % 18)}cm", "어깨와 가슴둘레 여유"]
    text = (
        f"상품명: {title}. 제품분류: {KO_SUBCATEGORY[subcategory]} > {KO_DETAIL_TYPE[detail_type]}. 컬러: {KO_COLOR[color]}. {material_text}. "
        f"{KO_FIT[fit]} 실루엣이며 {size_info[0]}, {size_info[1]}가 특징입니다. "
        f"{season_text} {tpo_text}에 활용하기 좋습니다. {CARE_TEXT[care]}."
    )
    source = source_case(product_id, title, category, source_url, text)
    product = structured_product(
        product_id,
        title,
        category,
        subcategory,
        detail_type,
        materials,
        fit,
        color,
        seasons,
        tpo_tags,
        care,
        size_info,
        source_url,
        missing,
        ambiguous,
    )
    return source, product


def build_expanded_dummy() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []
    duplicate_pairs: list[tuple[str, str]] = []

    outer_duplicates: dict[int, dict[str, Any]] = {}
    top_duplicates: dict[int, dict[str, Any]] = {}
    duplicate_indices = {1: 0, 11: 10, 21: 20, 31: 30, 41: 40}

    for index in range(50):
        duplicate_base = outer_duplicates.get(duplicate_indices[index]) if index in duplicate_indices else None
        source, product = make_dummy_case(index, "outer", duplicate_base)
        if index in duplicate_indices:
            duplicate_pairs.append((f"outer_dummy_{duplicate_indices[index]:03d}", source["product_id"]))
        if index in duplicate_indices.values():
            outer_duplicates[index] = {"source": source, "product": product}
        sources.append(source)
        products.append(product)

    for offset in range(50):
        index = 50 + offset
        local_index = offset
        duplicate_base = top_duplicates.get(duplicate_indices[local_index]) if local_index in duplicate_indices else None
        source, product = make_dummy_case(index, "top", duplicate_base)
        if local_index in duplicate_indices:
            duplicate_pairs.append((f"top_dummy_{50 + duplicate_indices[local_index]:03d}", source["product_id"]))
        if local_index in duplicate_indices.values():
            top_duplicates[local_index] = {"source": source, "product": product}
        sources.append(source)
        products.append(product)

    distinct_pairs: list[tuple[str, str]] = []
    for left, right in [
        ("outer_dummy_000", "top_dummy_050"),
        ("outer_dummy_002", "outer_dummy_006"),
        ("outer_dummy_004", "outer_dummy_008"),
        ("outer_dummy_014", "top_dummy_064"),
        ("top_dummy_052", "top_dummy_058"),
        ("top_dummy_060", "top_dummy_070"),
        ("outer_dummy_024", "top_dummy_074"),
        ("outer_dummy_034", "outer_dummy_048"),
        ("top_dummy_080", "top_dummy_092"),
        ("outer_dummy_044", "top_dummy_098"),
    ]:
        distinct_pairs.append((left, right))

    labels = {
        "pairs": [
            {"left_id": left, "right_id": right, "expected_decision": "duplicate"}
            for left, right in duplicate_pairs
        ]
        + [
            {"left_id": left, "right_id": right, "expected_decision": "distinct"}
            for left, right in distinct_pairs
        ]
    }
    return {"cases": sources}, {"products": products}, labels


def real_sanity_payloads() -> tuple[dict[str, Any], dict[str, Any]]:
    cases = [
        {
            "product_id": "real_outer_beanpole_linen_jacket_4308999",
            "source_title": "빈폴 레이디스 리넨 체크 더블 재킷",
            "source_url": "https://www.musinsa.com/products/4308999",
            "category_hint": "outer",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 빈폴 레이디스 리넨 체크 더블 재킷. 제품분류 재킷. 색상 베이지. 사이즈 S, M, L. 소재 겉감 면 50%, 마 50%, 안감 폴리에스터 100%.",
        },
        {
            "product_id": "real_outer_limelike_coverpiece_2101205",
            "source_title": "라임라이크 브이넥 크로스 가디건_3color",
            "source_url": "https://www.musinsa.com/products/2101205",
            "category_hint": "outer",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 라임라이크 브이넥 크로스 가디건_3color. 제품분류 아우터 카디건. 컬러 네이비, 그레이, 오트. 혼용률 울 50%, 폴리에스테르 10%, 나일론 30%.",
        },
        {
            "product_id": "real_outer_8seconds_jacket_4922894",
            "source_title": "에잇세컨즈 쓰리버튼 세미 오버핏 자켓 블랙",
            "source_url": "https://www.musinsa.com/products/4922894",
            "category_hint": "outer",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 에잇세컨즈 쓰리버튼 세미 오버핏 자켓 블랙. 제품분류 재킷. 색상 블랙. 겉감 폴리에스터 100%, 안감 폴리에스터 100%. 반드시 드라이크리닝.",
        },
        {
            "product_id": "real_outer_247_cashmere_blouson_3617977",
            "source_title": "247시리즈 캐시미어 블렌디드 블루종 자켓 BLACK",
            "source_url": "https://www.musinsa.com/products/3617977",
            "category_hint": "outer",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 247시리즈 캐시미어 블렌디드 블루종 자켓 BLACK. 제품분류 자켓. 컬러 블랙. 캐시미어 블렌디드 소재로 소개되며 정확한 숫자 혼용률은 snippet에 없습니다.",
        },
        {
            "product_id": "real_outer_lenina_woolcover_4332165",
            "source_title": "르니나 SALENA 울 브이넥 가디건_RED",
            "source_url": "https://www.musinsa.com/products/4332165",
            "category_hint": "outer",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 르니나 SALENA 울 브이넥 가디건_RED. 제품분류 아우터 카디건. 컬러 레드. 울 브이넥 가디건 이름에서 울 소재 단서가 있으나 숫자 혼용률은 snippet에 없습니다.",
        },
        {
            "product_id": "real_top_armedes_tee_4783312",
            "source_title": "아르메데스 면 20수 아트그래픽 티셔츠",
            "source_url": "https://www.musinsa.com/products/4783312",
            "category_hint": "top",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 아르메데스 면 20수 아트그래픽 티셔츠. 제품분류 티셔츠. 컬러 블랙, 화이트. 사이즈 S, M, L, XL, 2XL. 소재 면 100%.",
        },
        {
            "product_id": "real_top_ms_linen_like_shirt_black_3054408",
            "source_title": "무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 블랙",
            "source_url": "https://www.musinsa.com/products/3054408",
            "category_hint": "top",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 블랙. 제품분류 상의 셔츠/블라우스. 컬러 블랙. 여유 있는 릴렉스 핏. 린넨과 유사한 질감의 여름 셔츠.",
        },
        {
            "product_id": "real_top_ms_basic_tee_3661999",
            "source_title": "무신사 스탠다드 베이식 크루 넥 티셔츠",
            "source_url": "https://www.musinsa.com/products/3661999",
            "category_hint": "top",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 무신사 스탠다드 베이식 크루 넥 티셔츠. 제품분류 티셔츠. 촘촘한 면 100% 코마사 20수 싱글 저지 원단. 편안한 착용감.",
        },
        {
            "product_id": "real_top_ms_linen_like_shirt_navy_3054409",
            "source_title": "무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 네이비",
            "source_url": "https://www.musinsa.com/products/3054409",
            "category_hint": "top",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 네이비. 제품분류 상의 셔츠/블라우스. 컬러 네이비. 여유 있는 릴렉스 핏. 린넨과 유사한 질감의 여름 셔츠.",
        },
        {
            "product_id": "real_top_ms_basic_short_tee_1196892",
            "source_title": "무신사 스탠다드 베이식 크루 넥 반팔 티셔츠",
            "source_url": "https://www.musinsa.com/products/1196892",
            "category_hint": "top",
            "locale": "ko-KR",
            "checked_at": "2026-07-05",
            "source_method": "manual_short_public_snippet",
            "product_text": "상품명: 무신사 스탠다드 베이식 크루 넥 반팔 티셔츠. 제품분류 티셔츠. 면 100% 코마사 20수 싱글 저지 원단. 편안한 착용감.",
        },
    ]

    specs = [
        ("real_outer_beanpole_linen_jacket_4308999", "빈폴 레이디스 리넨 체크 더블 재킷", "outer", "jacket", "suit_blazer_jacket", "beige", "regular", [["shell", "cotton", 50, "explicit", "겉감 면 50%, 마 50%"], ["shell", "linen", 50, "explicit", "겉감 면 50%, 마 50%"], ["lining", "polyester", 100, "explicit", "안감 폴리에스터 100%"]], ["spring", "summer"], ["commute", "formal", "guest_look", "layering"], [], ["S, M, L"], [], []),
        ("real_outer_limelike_coverpiece_2101205", "라임라이크 브이넥 크로스 가디건_3color", "outer", "cardigan", "cardigan", "multi", "regular", [["shell", "wool", 50, "explicit", "울 50%, 폴리에스테르 10%, 나일론 30%"], ["shell", "polyester", 10, "explicit", "울 50%, 폴리에스테르 10%, 나일론 30%"], ["shell", "nylon", 30, "explicit", "울 50%, 폴리에스테르 10%, 나일론 30%"]], ["fall", "winter"], ["daily", "layering", "commute"], [], ["컬러 네이비, 그레이, 오트"], [], []),
        ("real_outer_8seconds_jacket_4922894", "에잇세컨즈 쓰리버튼 세미 오버핏 자켓 블랙", "outer", "jacket", "suit_blazer_jacket", "black", "relaxed", [["shell", "polyester", 100, "explicit", "겉감 폴리에스터 100%"], ["lining", "polyester", 100, "explicit", "안감 폴리에스터 100%"]], ["spring", "fall"], ["commute", "formal", "layering"], ["dry_clean"], [], [], []),
        ("real_outer_247_cashmere_blouson_3617977", "247시리즈 캐시미어 블렌디드 블루종 자켓 BLACK", "outer", "jacket", "blouson_ma1", "black", "regular", [["unknown", "cashmere", None, "ambiguous", "캐시미어 블렌디드 소재"]], ["fall", "winter"], ["daily", "commute", "layering"], [], [], [], ["material_ratio"]),
        ("real_outer_lenina_woolcover_4332165", "르니나 SALENA 울 브이넥 가디건_RED", "outer", "cardigan", "cardigan", "red", "regular", [["unknown", "wool", None, "missing", "울 브이넥 가디건"]], ["fall", "winter"], ["daily", "layering", "commute"], [], [], ["material_ratio"], []),
        ("real_top_armedes_tee_4783312", "아르메데스 면 20수 아트그래픽 티셔츠", "top", "tshirt", "short_sleeve_tshirt", "multi", "regular", [["unknown", "cotton", 100, "explicit", "소재 면 100%"]], ["summer"], ["daily", "casual", "street"], [], ["S, M, L, XL, 2XL"], [], []),
        ("real_top_ms_linen_like_shirt_black_3054408", "무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 블랙", "top", "shirt_blouse", "shirt_blouse", "black", "relaxed", [["unknown", "linen", None, "ambiguous", "린넨과 유사한 질감"]], ["summer"], ["daily", "casual"], [], [], [], ["material_ratio"]),
        ("real_top_ms_basic_tee_3661999", "무신사 스탠다드 베이식 크루 넥 티셔츠", "top", "tshirt", "short_sleeve_tshirt", "white", "regular", [["unknown", "cotton", 100, "explicit", "면 100% 코마사 20수 싱글 저지"]], ["summer"], ["daily", "casual"], [], [], [], []),
        ("real_top_ms_linen_like_shirt_navy_3054409", "무신사 스탠다드 릴렉스드 린넨 라이크 반소매 셔츠 네이비", "top", "shirt_blouse", "shirt_blouse", "navy", "relaxed", [["unknown", "linen", None, "ambiguous", "린넨과 유사한 질감"]], ["summer"], ["daily", "casual"], [], [], [], ["material_ratio"]),
        ("real_top_ms_basic_short_tee_1196892", "무신사 스탠다드 베이식 크루 넥 반팔 티셔츠", "top", "tshirt", "short_sleeve_tshirt", "white", "regular", [["unknown", "cotton", 100, "explicit", "면 100% 코마사 20수 싱글 저지"]], ["summer"], ["daily", "casual"], [], [], [], []),
    ]

    source_by_id = {case["product_id"]: case for case in cases}
    products: list[dict[str, Any]] = []
    for product_id, title, category, subcategory, detail_type, color, fit, material_rows, seasons, tpo, care, size_info, missing, ambiguous in specs:
        materials = [
            {
                "part": part,
                "name": name,
                "ratio": ratio,
                "ratio_status": status,
                "evidence": evidence,
            }
            for part, name, ratio, status, evidence in material_rows
        ]
        products.append(
            structured_product(
                product_id,
                title,
                category,
                subcategory,
                detail_type,
                materials,
                fit,
                color,
                seasons,
                tpo,
                care,
                ["snippet 기반 제한 정보", *size_info],
                source_by_id[product_id]["source_url"],
                missing,
                ambiguous,
            )
        )

    return {"cases": cases}, {"products": products}


def write_prompt(path: Path, title: str, source_payload: dict[str, Any]) -> None:
    cases_json = json.dumps(source_payload, ensure_ascii=False, indent=2)
    prompt = f"""# {title}

Use `src/skills/product-agentizer/SKILL.md`, `references/schema.json`, and `references/taxonomy.json`.
Convert every case below into a raw JSON object with this exact top-level shape:

```json
{{"products":[{{"product_id":"...","structured_product":{{}}}}]}}
```

Rules:
- Return raw JSON only, with no Markdown fences.
- Do not fetch URLs. URLs are source metadata only.
- Do not judge legal label compliance.
- Never estimate fabric ratios. Use `missing` or `ambiguous` when the input does not provide a numeric ratio.
- Preserve product_id values exactly.

Input cases:
{cases_json}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")


def main() -> None:
    expanded_sources, expanded_expected, duplicate_labels = build_expanded_dummy()
    write_json(EXPANDED_DIR / "source_inputs.json", expanded_sources)
    write_json(EXPANDED_DIR / "expected_products.json", expanded_expected)
    write_json(EXPANDED_DIR / "reference_actual_products.json", expanded_expected)
    write_json(EXPANDED_DIR / "duplicate_labels.json", duplicate_labels)

    # Codex subset fixtures preserve a historical Codex run. Do not regenerate
    # them from the current synthetic fixtures because detail_type is intentionally
    # null for expected/actual compatibility checks.

    real_sources, real_expected = real_sanity_payloads()
    real_labels = {
        "pairs": [
            {
                "left_id": "real_outer_beanpole_linen_jacket_4308999",
                "right_id": "real_top_armedes_tee_4783312",
                "expected_decision": "distinct",
            },
            {
                "left_id": "real_outer_limelike_coverpiece_2101205",
                "right_id": "real_top_ms_basic_tee_3661999",
                "expected_decision": "distinct",
            },
            {
                "left_id": "real_outer_8seconds_jacket_4922894",
                "right_id": "real_top_ms_linen_like_shirt_black_3054408",
                "expected_decision": "distinct",
            },
            {
                "left_id": "real_outer_247_cashmere_blouson_3617977",
                "right_id": "real_top_ms_linen_like_shirt_navy_3054409",
                "expected_decision": "distinct",
            },
            {
                "left_id": "real_outer_lenina_woolcover_4332165",
                "right_id": "real_top_ms_basic_short_tee_1196892",
                "expected_decision": "distinct",
            },
        ]
    }
    write_json(REAL_DIR / "source_inputs.json", real_sources)
    write_json(REAL_DIR / "expected_products.json", real_expected)
    write_json(REAL_DIR / "duplicate_labels.json", real_labels)
    write_prompt(REAL_DIR / "prompt.md", "Real sanity conversion prompt", real_sources)
    write_prompt(REAL_DIR / "prompt_template.md", "Real sanity conversion prompt template", {"cases": ["<replace with source_inputs.json cases>"]})


if __name__ == "__main__":
    main()
