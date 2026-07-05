#!/usr/bin/env python3
"""Generate synthetic full-page-like fixtures for S7.7 validation."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import generate_expanded_validation_fixtures as base


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "tests" / "fixtures"
FULL_DIR = FIXTURE_ROOT / "full_page_dummy"
SUBSET_DIR = FIXTURE_ROOT / "full_page_codex_subset"
SMOKE_DIR = FIXTURE_ROOT / "full_page_codex_smoke20"
SYNTHETIC_URL_PREFIX = "https://example.com/musinsa-full-page-dummy/"

BRANDS = ["DUMMY STANDARD", "AX TEST LABEL", "SYNTHETIC WORKS", "REPRO SAMPLE"]
DENSITY_SEQUENCE = [
    "sparse",
    "sparse",
    "medium",
    "medium",
    "medium",
    "medium",
    "full",
    "full",
    "full",
    "noisy_ambiguous",
]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_reference_actual(path: Path, metadata_path: Path, data: Any) -> None:
    metadata = {}
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("actual_mode") == "codex_cli_actual":
        return
    write_json(path, data)
    write_json(
        metadata_path,
        {
            "actual_mode": "deterministic_reference_actual_pending_cli_run",
            "note": "Generator writes reference actual until a real Codex CLI actual is saved.",
        },
    )


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def density_for_index(index: int) -> str:
    return DENSITY_SEQUENCE[index % len(DENSITY_SEQUENCE)]


def category_for_index(index: int, count: int) -> str:
    return "outer" if index < count // 2 else "top"


def detail_for_index(index: int, category: str, count: int) -> tuple[str, str]:
    sequence = base.OUTER_DETAIL_TYPE_SEQUENCE if category == "outer" else base.TOP_DETAIL_TYPE_SEQUENCE
    local_index = index if category == "outer" else index - (count // 2)
    return sequence[local_index % len(sequence)]


def material_rows_for(
    index: int,
    category: str,
    subcategory: str,
    detail_type: str,
    density: str,
) -> tuple[list[dict[str, Any]], str, list[str], list[str]]:
    if density == "sparse":
        return [], "", ["materials", "fit", "seasons", "tpo_tags", "care", "size_info"], []

    if density == "noisy_ambiguous":
        if category == "outer":
            return (
                [
                    {
                        "part": "unknown",
                        "name": "cashmere",
                        "ratio": None,
                        "ratio_status": "ambiguous",
                        "evidence": "캐시미어를 블렌드한 듯한 부드러운 터치감",
                    },
                    {
                        "part": "unknown",
                        "name": "wool",
                        "ratio": None,
                        "ratio_status": "ambiguous",
                        "evidence": "고급 울 터치 원단",
                    }
                ],
                "소재: 캐시미어를 블렌드한 듯한 부드러운 터치감의 고급 울 터치 원단. 정확한 혼용률은 상세 이미지 참고.",
                [],
                ["material_ratio"],
            )
        return (
            [
                {
                    "part": "unknown",
                    "name": "linen",
                    "ratio": None,
                    "ratio_status": "ambiguous",
                    "evidence": "린넨 라이크 터치",
                },
                {
                    "part": "unknown",
                    "name": "rayon",
                    "ratio": None,
                    "ratio_status": "ambiguous",
                    "evidence": "레이온 블렌드 느낌",
                }
            ],
            "소재: 린넨 라이크 터치와 레이온 블렌드 느낌을 살린 원단. 숫자 혼용률은 제공되지 않습니다.",
            [],
            ["material_ratio"],
        )

    if density == "medium":
        rows, text, missing, ambiguous = base.material_pattern(index + (0 if category == "outer" else 5))
        rows = copy.deepcopy(rows)
        for row in rows:
            if row["name"] in {"recycled_fiber", "faux_leather"} and row["part"] == "shell":
                row["part"] = "unknown"
        if any(row["part"] == "unknown" for row in rows):
            missing = unique([*missing, "material_part"])
        return rows, f"소재: {text}.", missing, ambiguous

    if detail_type in {"short_padding_heavy_outer", "long_padding_heavy_outer", "lightweight_padding_vest"}:
        return (
            [
                {"part": "shell", "name": "nylon", "ratio": 100, "ratio_status": "explicit", "evidence": "겉감 나일론 100%"},
                {"part": "lining", "name": "polyester", "ratio": 100, "ratio_status": "explicit", "evidence": "안감 폴리에스터 100%"},
                {"part": "fill", "name": "duck_down", "ratio": 80, "ratio_status": "explicit", "evidence": "충전재 덕다운 80%, 구스다운 20%"},
                {"part": "fill", "name": "goose_down", "ratio": 20, "ratio_status": "explicit", "evidence": "충전재 덕다운 80%, 구스다운 20%"},
            ],
            "소재 정보:\n- 겉감: 나일론 100%\n- 안감: 폴리에스터 100%\n- 충전재: 덕다운 80%, 구스다운 20%",
            [],
            [],
        )

    if detail_type in {"winter_double_coat", "winter_single_coat", "winter_other_coat", "cardigan", "knit_sweater"}:
        return (
            [
                {"part": "shell", "name": "wool", "ratio": 70, "ratio_status": "explicit", "evidence": "겉감 울 70%, 캐시미어 30%"},
                {"part": "shell", "name": "cashmere", "ratio": 30, "ratio_status": "explicit", "evidence": "겉감 울 70%, 캐시미어 30%"},
            ],
            "소재 정보:\n- 겉감: 울 70%, 캐시미어 30%",
            [],
            [],
        )

    if detail_type == "leather_rider_jacket":
        return (
            [
                {"part": "shell", "name": "leather", "ratio": 100, "ratio_status": "explicit", "evidence": "겉감 천연가죽 100%"},
                {"part": "lining", "name": "polyester", "ratio": 100, "ratio_status": "explicit", "evidence": "안감 폴리에스터 100%"},
            ],
            "소재 정보:\n- 겉감: 천연가죽 100%\n- 안감: 폴리에스터 100%",
            [],
            [],
        )

    if category == "top":
        return (
            [
                {"part": "shell", "name": "cotton", "ratio": 95, "ratio_status": "explicit", "evidence": "겉감 면 95%, 폴리우레탄 5%"},
                {"part": "shell", "name": "polyurethane", "ratio": 5, "ratio_status": "explicit", "evidence": "겉감 면 95%, 폴리우레탄 5%"},
            ],
            "소재 정보:\n- 겉감: 면 95%, 폴리우레탄 5%",
            [],
            [],
        )

    return (
        [
            {"part": "shell", "name": "nylon", "ratio": 100, "ratio_status": "explicit", "evidence": "겉감 나일론 100%"},
            {"part": "lining", "name": "polyester", "ratio": 100, "ratio_status": "explicit", "evidence": "안감 폴리에스터 100%"},
        ],
        "소재 정보:\n- 겉감: 나일론 100%\n- 안감: 폴리에스터 100%",
        [],
        [],
    )


def season_tpo_for(index: int, category: str, density: str) -> tuple[list[str], str, list[str], str]:
    if density == "sparse":
        return [], "", [], ""
    variants = [
        (["spring", "summer"], "봄여름", ["daily", "casual"], "데일리와 캐주얼"),
        (["fall", "winter"], "가을겨울", ["layering", "travel"], "레이어드와 여행용"),
        (["spring", "fall"], "간절기", ["commute", "formal"], "출근룩과 포멀"),
        (["summer"], "여름", ["daily", "street"], "데일리와 스트리트"),
        (["winter"], "겨울", ["outdoor", "travel"], "아웃도어와 여행"),
    ]
    return variants[index % len(variants)]


def care_for(index: int, density: str) -> tuple[list[str], str, list[str]]:
    if density == "sparse":
        return [], "", ["care"]
    care = base.CARE[(index * 2) % len(base.CARE)]
    if density == "full":
        extra = "no_tumble_dry" if care != "no_tumble_dry" else "shade_dry"
        care_values = unique([care, extra])
        text = "관리 방법: " + ", ".join(base.CARE_TEXT[item] for item in care_values)
        return care_values, text, []
    return [care], f"관리 방법: {base.CARE_TEXT[care]}", []


def size_for(index: int, category: str, density: str) -> tuple[list[str], str, list[str]]:
    if density == "sparse":
        return [], "", ["size_info"]
    if density == "medium":
        sizes = "S, M, L" if category == "top" else "M, L, XL"
        return sizes.split(", "), f"사이즈 옵션: {sizes}", []

    first = 64 + (index % 10)
    second = first + 2
    size_info = [
        f"M 총장 {first}cm 어깨 {46 + index % 8}cm 가슴 {54 + index % 8}cm",
        f"L 총장 {second}cm 어깨 {48 + index % 8}cm 가슴 {56 + index % 8}cm",
    ]
    text = "사이즈 실측:\n" + "\n".join(size_info)
    return size_info, text, []


def structured_product(
    product_id: str,
    title: str,
    category: str,
    subcategory: str,
    detail_type: str,
    materials: list[dict[str, Any]],
    fit: list[str],
    colors: list[str],
    seasons: list[str],
    tpo_tags: list[str],
    care: list[str],
    size_info: list[str],
    source_url: str,
    missing_fields: list[str],
    ambiguous_fields: list[str],
) -> dict[str, Any]:
    color_text = ", ".join(base.KO_COLOR[color] for color in colors) if colors else "색상 미상"
    type_text = base.KO_DETAIL_TYPE.get(detail_type) or base.KO_SUBCATEGORY[subcategory]
    fit_text = ", ".join(base.KO_FIT[item] for item in fit) if fit else "핏 정보 부족"
    reasons = [
        f"입력 텍스트의 카테고리 단서를 {category}/{subcategory}/{detail_type}로 정규화했습니다.",
        f"색상 단서는 {color_text}로 정규화했습니다.",
    ]
    if missing_fields:
        reasons.append(f"입력에서 {', '.join(sorted(set(missing_fields)))} 정보가 부족해 missing으로 기록했습니다.")
    if ambiguous_fields:
        reasons.append(f"입력에서 {', '.join(sorted(set(ambiguous_fields)))} 정보가 모호해 ambiguous로 기록했습니다.")

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
                "fit": fit,
                "colors": colors,
                "seasons": seasons,
                "tpo_tags": tpo_tags,
                "care": care,
                "size_info": size_info,
            },
            "agent_descriptor": {
                "search_summary": f"{color_text} {fit_text} {type_text}",
                "query_tags": unique([color_text, type_text, fit_text, *tpo_tags]),
                "explainable_reasons": reasons,
            },
            "quality": {
                "missing_fields": sorted(set(missing_fields)),
                "ambiguous_fields": sorted(set(ambiguous_fields)),
                "out_of_scope": False,
                "confidence": "low" if len(missing_fields) >= 4 else ("medium" if missing_fields or ambiguous_fields else "high"),
            },
        },
    }


def source_case(
    product_id: str,
    title: str,
    category: str,
    source_url: str,
    density: str,
    product_text: str,
) -> dict[str, Any]:
    return {
        "product_id": product_id,
        "source_title": title,
        "source_url": source_url,
        "category_hint": category,
        "locale": "ko-KR",
        "source_method": "synthetic_full_page_like",
        "information_density": density,
        "product_text": product_text,
    }


def build_product_text(
    title: str,
    brand: str,
    category: str,
    subcategory: str,
    detail_type: str,
    colors: list[str],
    fit: list[str],
    density: str,
    material_text: str,
    season_text: str,
    tpo_text: str,
    care_text: str,
    size_text: str,
) -> str:
    category_text = f"{base.KO_SUBCATEGORY[subcategory]} > {base.KO_DETAIL_TYPE[detail_type]}"
    color_text = ", ".join(base.KO_COLOR[color] for color in colors)
    fit_text = ", ".join(base.KO_FIT[item] for item in fit)

    if density == "sparse":
        return "\n".join(
            [
                f"브랜드: {brand}",
                f"상품명: {title}",
                f"카테고리: {'아우터' if category == 'outer' else '상의'} > {category_text}",
                f"컬러: {color_text}",
                "판매가: 99,000원",
            ]
        )

    blocks = [
        "[상품 상단]",
        f"브랜드: {brand}",
        f"상품명: {title}",
        f"카테고리: {'아우터' if category == 'outer' else '상의'} > {category_text}",
        f"컬러 옵션: {color_text}",
        "",
        "[상품 정보]",
        material_text,
        f"핏: {fit_text}",
        size_text,
    ]
    if season_text:
        blocks.append(f"추천 계절: {season_text}")
    if tpo_text:
        blocks.append(f"추천 상황: {tpo_text}")
    if care_text:
        blocks.append(care_text)

    if density == "full":
        blocks.extend(
            [
                "",
                "[상세 설명]",
                "데일리 착용과 반복 세탁을 고려해 봉제선과 여밈 부위를 안정적으로 설계한 합성 상세페이지 샘플입니다.",
                "자동 수집 데이터가 아니며 실제 상품 원문을 복제하지 않은 검증용 문장입니다.",
            ]
        )
    elif density == "noisy_ambiguous":
        blocks.extend(
            [
                "",
                "[배송/혜택]",
                "오늘 22시까지 결제 시 내일 도착 예정이라는 예시 배송 문구입니다.",
                "첫 구매 쿠폰과 리뷰 요약은 구조화 대상 속성이 아닙니다.",
                "후기 요약: 따뜻해요, 사이즈가 여유 있어요, 색상이 화면과 비슷해요.",
            ]
        )

    return "\n".join(block for block in blocks if block is not None)


def make_case(index: int, count: int) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    category = category_for_index(index, count)
    subcategory, detail_type = detail_for_index(index, category, count)
    density = density_for_index(index)
    brand = BRANDS[index % len(BRANDS)]
    color = base.COLORS[(index * 3 + (0 if category == "outer" else 1)) % len(base.COLORS)]
    extra_color = base.COLORS[(index * 5 + 2) % len(base.COLORS)]
    colors = unique([color, extra_color]) if density in {"full", "noisy_ambiguous"} else [color]
    fit_value = base.FITS[(index * 5 + (1 if category == "outer" else 2)) % len(base.FITS)]
    fit = [] if density == "sparse" else [fit_value]
    product_id = f"full_{category}_{index:03d}"
    title = f"{brand} {base.KO_COLOR[color]} {base.KO_DETAIL_TYPE[detail_type]} {index:03d}"
    source_url = f"{SYNTHETIC_URL_PREFIX}{product_id}"

    materials, material_text, material_missing, material_ambiguous = material_rows_for(index, category, subcategory, detail_type, density)
    seasons, season_text, tpo_tags, tpo_text = season_tpo_for(index, category, density)
    care, care_text, care_missing = care_for(index, density)
    size_info, size_text, size_missing = size_for(index, category, density)
    missing_fields = unique([*material_missing, *care_missing, *size_missing])
    if any(item["part"] == "unknown" for item in materials):
        missing_fields = unique([*missing_fields, "material_part"])
    ambiguous_fields = unique(material_ambiguous)

    text = build_product_text(
        title,
        brand,
        category,
        subcategory,
        detail_type,
        colors,
        fit,
        density,
        material_text,
        season_text,
        tpo_text,
        care_text,
        size_text,
    )
    source = source_case(product_id, title, category, source_url, density, text)
    product = structured_product(
        product_id,
        title,
        category,
        subcategory,
        detail_type,
        materials,
        fit,
        colors,
        seasons,
        tpo_tags,
        care,
        size_info,
        source_url,
        missing_fields,
        ambiguous_fields,
    )
    metadata = {
        "product_id": product_id,
        "sequence_index": index,
        "category": category,
        "subcategory": subcategory,
        "detail_type": detail_type,
        "information_density": density,
        "synthetic_source": True,
        "has_explicit_material_ratio": any(item.get("ratio_status") == "explicit" for item in materials),
        "expected_missing_fields": sorted(set(missing_fields)),
        "expected_ambiguous_fields": sorted(set(ambiguous_fields)),
    }
    return source, product, metadata


def make_duplicate(base_source: dict[str, Any], base_product: dict[str, Any], base_metadata: dict[str, Any], new_index: int) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = copy.deepcopy(base_source)
    product = copy.deepcopy(base_product)
    metadata = copy.deepcopy(base_metadata)
    category = metadata["category"]
    product_id = f"full_{category}_{new_index:03d}"
    old_title = source["source_title"]
    new_title = f"{old_title} 리오더"
    source_url = f"{SYNTHETIC_URL_PREFIX}{product_id}"

    source["product_id"] = product_id
    source["source_title"] = new_title
    source["source_url"] = source_url
    source["product_text"] = source["product_text"].replace(old_title, new_title)

    structured = product["structured_product"]
    product["product_id"] = product_id
    structured["source"]["source_url"] = source_url
    structured["source"]["source_title"] = new_title
    structured["product"]["title"] = new_title
    structured["agent_descriptor"]["search_summary"] = structured["agent_descriptor"]["search_summary"].replace(old_title, new_title)

    metadata["product_id"] = product_id
    metadata["sequence_index"] = new_index
    metadata["duplicate_of"] = base_source["product_id"]
    return source, product, metadata


def filtered_payloads(
    selected_ids: list[str],
    sources: list[dict[str, Any]],
    products: list[dict[str, Any]],
    labels: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    selected = set(selected_ids)
    source_by_id = {item["product_id"]: item for item in sources}
    product_by_id = {item["product_id"]: item for item in products}
    return (
        {"cases": [source_by_id[product_id] for product_id in selected_ids]},
        {"products": [product_by_id[product_id] for product_id in selected_ids]},
        {
            "pairs": [
                item
                for item in labels["pairs"]
                if item["left_id"] in selected and item["right_id"] in selected
            ]
        },
    )


def select_representative_ids(
    metadata_items: list[dict[str, Any]],
    duplicate_pairs: list[tuple[str, str]],
    target_size: int,
) -> list[str]:
    if target_size % 2 != 0:
        raise ValueError("target_size must be even")

    target_by_category = {"outer": target_size // 2, "top": target_size // 2}
    selected: list[str] = []
    selected_set: set[str] = set()
    count_by_category = {"outer": 0, "top": 0}
    metadata_by_id = {item["product_id"]: item for item in metadata_items}

    def add(product_id: str) -> bool:
        if product_id in selected_set:
            return False
        item = metadata_by_id[product_id]
        category = item["category"]
        if count_by_category[category] >= target_by_category[category]:
            return False
        selected.append(product_id)
        selected_set.add(product_id)
        count_by_category[category] += 1
        return True

    pairs_by_category: dict[str, list[tuple[str, str]]] = {"outer": [], "top": []}
    for left_id, right_id in duplicate_pairs:
        pairs_by_category[metadata_by_id[left_id]["category"]].append((left_id, right_id))

    forced_pairs_per_category = 1 if target_size <= 20 else 2
    for pairs in pairs_by_category.values():
        for left_id, right_id in pairs[:forced_pairs_per_category]:
            add(left_id)
            add(right_id)

    for category in ("outer", "top"):
        for density in ("sparse", "medium", "full", "noisy_ambiguous"):
            if count_by_category[category] >= target_by_category[category]:
                break
            candidates = [
                item
                for item in metadata_items
                if item["category"] == category
                and item["information_density"] == density
                and item["product_id"] not in selected_set
            ]
            if candidates:
                add(candidates[0]["product_id"])

    sequence_by_category = {
        "outer": [detail_type for _, detail_type in base.OUTER_DETAIL_TYPE_SEQUENCE],
        "top": [detail_type for _, detail_type in base.TOP_DETAIL_TYPE_SEQUENCE],
    }
    for category, detail_sequence in sequence_by_category.items():
        for detail_type in detail_sequence:
            if count_by_category[category] >= target_by_category[category]:
                break
            candidates = [
                item
                for item in metadata_items
                if item["category"] == category
                and item["detail_type"] == detail_type
                and item["product_id"] not in selected_set
            ]
            if candidates:
                add(candidates[0]["product_id"])

    density_order = ["sparse", "medium", "full", "noisy_ambiguous"]
    while len(selected) < target_size:
        progressed = False
        for density in density_order:
            for item in metadata_items:
                if item["information_density"] != density:
                    continue
                if add(item["product_id"]):
                    progressed = True
                    break
        if not progressed:
            break

    ordered = sorted(selected, key=lambda product_id: metadata_by_id[product_id]["sequence_index"])
    if len(ordered) != target_size:
        raise ValueError(f"selected {len(ordered)} cases, expected {target_size}")
    return ordered


def build_dataset(
    count: int, subset_size: int
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    if count < 100 or count % 2 != 0:
        raise ValueError("count must be an even integer greater than or equal to 100")
    if subset_size < 20 or subset_size > count:
        raise ValueError("subset_size must be between 20 and count")

    sources: list[dict[str, Any]] = []
    products: list[dict[str, Any]] = []
    metadata_items: list[dict[str, Any]] = []
    duplicate_pairs: list[tuple[str, str]] = []
    base_cases: dict[int, tuple[dict[str, Any], dict[str, Any], dict[str, Any]]] = {}
    duplicate_indices = {15: 14, 45: 44, 75: 74, 105: 104, 135: 134, 165: 164, 195: 194, 225: 224, 255: 254, 285: 284}
    duplicate_indices = {key: value for key, value in duplicate_indices.items() if key < count and value < count}

    for index in range(count):
        if index in duplicate_indices and duplicate_indices[index] in base_cases:
            base_source, base_product, base_metadata = base_cases[duplicate_indices[index]]
            source, product, metadata = make_duplicate(base_source, base_product, base_metadata, index)
            duplicate_pairs.append((base_source["product_id"], source["product_id"]))
        else:
            source, product, metadata = make_case(index, count)
        base_cases[index] = (source, product, metadata)
        sources.append(source)
        products.append(product)
        metadata_items.append(metadata)

    distinct_pairs = [
        ("full_outer_000", f"full_top_{count // 2:03d}"),
        ("full_outer_006", f"full_top_{count // 2 + 9:03d}"),
        ("full_outer_026", f"full_top_{count // 2 + 27:03d}"),
        ("full_outer_056", f"full_top_{count // 2 + 54:03d}"),
        ("full_outer_086", f"full_top_{count // 2 + 81:03d}"),
        ("full_outer_116", f"full_top_{count // 2 + 108:03d}"),
        ("full_outer_146", f"full_top_{count // 2 + 135:03d}"),
        ("full_outer_004", "full_outer_034"),
        (f"full_top_{count // 2 + 4:03d}", f"full_top_{count // 2 + 34:03d}"),
        (f"full_top_{count // 2 + 74:03d}", f"full_top_{count // 2 + 124:03d}"),
    ]
    existing_ids = {item["product_id"] for item in sources}
    labels = {
        "pairs": [
            {"left_id": left, "right_id": right, "expected_decision": "duplicate"}
            for left, right in duplicate_pairs
        ]
        + [
            {"left_id": left, "right_id": right, "expected_decision": "distinct"}
            for left, right in distinct_pairs
            if left in existing_ids and right in existing_ids
        ]
    }

    subset_ids = select_representative_ids(metadata_items, duplicate_pairs, subset_size)
    subset_sources, subset_expected, subset_labels = filtered_payloads(subset_ids, sources, products, labels)

    return (
        {"cases": sources},
        {"products": products},
        labels,
        {"cases": metadata_items},
        subset_sources,
        subset_expected,
        subset_labels,
    )


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
- Do not fetch URLs. URLs are synthetic source metadata only.
- Do not judge legal label compliance.
- Never estimate fabric ratios. Use `missing` or `ambiguous` when the input does not provide a numeric ratio.
- Preserve product_id values exactly.
- Treat 배송, 쿠폰, 후기 요약, 가격 문구 as noise unless they directly state product attributes.

Input cases:
{cases_json}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate S7.7 full-page-like synthetic fixtures.")
    parser.add_argument("--count", type=int, default=300, help="Number of full_page_dummy cases.")
    parser.add_argument("--subset-size", type=int, default=50, help="Number of full_page_codex_subset cases.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources, expected, labels, metadata, subset_sources, subset_expected, subset_labels = build_dataset(args.count, args.subset_size)

    write_json(FULL_DIR / "source_inputs.json", sources)
    write_json(FULL_DIR / "expected_products.json", expected)
    write_json(FULL_DIR / "reference_actual_products.json", expected)
    write_json(FULL_DIR / "duplicate_labels.json", labels)
    write_json(FULL_DIR / "case_metadata.json", metadata)

    write_json(SUBSET_DIR / "source_inputs.json", subset_sources)
    write_json(SUBSET_DIR / "expected_products.json", subset_expected)
    write_reference_actual(SUBSET_DIR / "actual_products.json", SUBSET_DIR / "actual_metadata.json", subset_expected)
    write_json(SUBSET_DIR / "duplicate_labels.json", subset_labels)
    write_prompt(SUBSET_DIR / "prompt.md", "Full-page synthetic Codex subset conversion prompt", subset_sources)
    write_prompt(
        SUBSET_DIR / "prompt_template.md",
        "Full-page synthetic Codex subset conversion prompt template",
        {"cases": ["<replace with source_inputs.json cases>"]},
    )

    smoke_duplicate_pairs = [
        (item["left_id"], item["right_id"])
        for item in labels["pairs"]
        if item["expected_decision"] == "duplicate"
    ]
    smoke_ids = select_representative_ids(metadata["cases"], smoke_duplicate_pairs, 20)
    smoke_sources, smoke_expected, smoke_labels = filtered_payloads(
        smoke_ids, sources["cases"], expected["products"], labels
    )
    write_json(SMOKE_DIR / "source_inputs.json", smoke_sources)
    write_json(SMOKE_DIR / "expected_products.json", smoke_expected)
    write_reference_actual(SMOKE_DIR / "actual_products.json", SMOKE_DIR / "actual_metadata.json", smoke_expected)
    write_json(SMOKE_DIR / "duplicate_labels.json", smoke_labels)
    write_prompt(SMOKE_DIR / "prompt.md", "Full-page synthetic Codex smoke20 conversion prompt", smoke_sources)
    write_prompt(
        SMOKE_DIR / "prompt_template.md",
        "Full-page synthetic Codex smoke20 conversion prompt template",
        {"cases": ["<replace with source_inputs.json cases>"]},
    )
    print(
        json.dumps(
            {
                "full_page_dummy": args.count,
                "full_page_codex_subset": args.subset_size,
                "full_page_codex_smoke20": 20,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
